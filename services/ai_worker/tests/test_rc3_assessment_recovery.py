"""RC3 assessment read-side and schema regression; Linux API/SQLite, not installed Windows UI."""
import sqlite3
import time

import pytest
from app import config, db


def _strict(client, title='RC3 recovery'):
    response = client.post('/api/assessments', json={
        'title': title, 'duration_seconds': 180, 'require_start': True,
        'negative_marking': 0.5, 'cutoff_pct': 75,
        'questions': [{'id': 'q1', 'kind': 'single', 'stem': 'A or B?', 'correct': 'B',
                       'options': [{'label': 'A', 'text': 'No'}, {'label': 'B', 'text': 'Yes'}]},
                      {'id': 'q2', 'kind': 'numerical', 'stem': '2 + 2?', 'correct': 4}]
    })
    assert response.status_code == 200, response.text
    return response.json()['id']


def test_fresh_schema_is_v7_and_usage_table_survives_reinit(tmp_path, monkeypatch):
    monkeypatch.setattr(config, 'DATA_DIR', tmp_path)
    monkeypatch.setattr(config, 'DB_PATH', tmp_path / 'fresh.sqlite3')
    db.initialize()
    with db.connect() as conn:
        assert conn.execute('PRAGMA user_version').fetchone()[0] == 7
        assert conn.execute("SELECT name FROM sqlite_master WHERE name='ai_usage'").fetchone()
        assert conn.execute("SELECT name FROM sqlite_master WHERE name='attempt_receipts'").fetchone()
    db.initialize()
    with db.connect() as conn:
        assert conn.execute('PRAGMA user_version').fetchone()[0] == 7


def test_old_v6_schema_usage_backfill_and_data_preservation(client):
    session = db.session_create('Keep on upgrade')
    with db.connect() as conn:
        conn.execute('DROP TABLE IF EXISTS ai_usage')
        conn.execute('PRAGMA user_version=6')
    db.initialize()
    with db.connect() as conn:
        assert conn.execute('PRAGMA user_version').fetchone()[0] == 7
        assert conn.execute("SELECT name FROM sqlite_master WHERE name='ai_usage'").fetchone()
        assert conn.execute('SELECT id FROM sessions WHERE id=?', (session['id'],)).fetchone()


def test_result_read_before_and_after_submit_no_answers_leak(client):
    aid = _strict(client)
    url = f'/api/assessments/{aid}'
    listing = next(x for x in client.get('/api/assessments').json() if x['id'] == aid)
    assert listing['attempt_count'] == 0
    assert all('correct' not in q and 'explanation' not in q for q in listing['questions'])
    assert client.get(url + '/latest-result').json() == {'attempt': None}
    clock = client.post(url + '/start')
    assert clock.status_code == 200, clock.text
    state = clock.json()
    assert abs(state['server_now']-time.time()) < 10
    assert state['deadline_at'] == pytest.approx(state['draft']['started'] + 180)
    assert client.post(url + '/draft', json={
        'started': state['draft']['started'], 'answers': {'q1': 'B'}, 'review': ['q2']
    }).status_code == 200
    # No read path leaks the answer key before finalization.
    assert client.get(url + '/latest-result').json()['attempt'] is None
    done = client.post(url + '/submit', json={
        'started': state['draft']['started'], 'answers': {'q1': 'B', 'q2': '5'}
    })
    assert done.status_code == 200, done.text
    expected = done.json()
    assert expected['score'] == 0.5
    assert expected['passed_cutoff'] is False
    stored = client.get(url + '/latest-result')
    assert stored.status_code == 200, stored.text
    record = stored.json()['attempt']
    assert record['attempt_id'] == expected['attempt_id']
    assert record['result']['score'] == expected['score']
    assert record['result']['explanations'][0]['correct'] == 'B'
    assert record['finished'] >= record['started']
    listing = next(x for x in client.get('/api/assessments').json() if x['id'] == aid)
    assert listing['attempt_count'] == 1
    # A second submission is the same committed receipt and cannot modify score.
    retry = client.post(url + '/submit', json={
        'started': state['draft']['started'], 'answers': {'q1': 'A', 'q2': '4'}
    })
    assert retry.status_code == 200 and retry.json()['duplicate_submission']
    assert client.get(url + '/latest-result').json()['attempt'] == record
    db.initialize()  # Simulates a worker restart against the same persisted SQLite.
    assert client.get(url + '/latest-result').json()['attempt'] == record


def test_nonexistent_assessment_latest_result_returns_404(client):
    assert client.get('/api/assessments/no-such-id/latest-result').status_code == 404


def test_real_authenticated_worker_subprocess_result_restoration(tmp_path):
    """Real HTTP subprocess and persistent SQLite across three worker lifetimes.

    No Tauri UI or Ollama model is involved; this specifically tests the new
    assessment-read API, local worker authentication, and restart boundaries.
    """
    import os
    import socket
    import subprocess
    import sys
    from pathlib import Path
    import httpx

    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0))
        port = sock.getsockname()[1]
    token='rc3-subprocess-'+('x'*28)
    service=Path(__file__).resolve().parents[1]
    env={**os.environ,'STUDIO_WORKER_TOKEN':token,'STUDIO_PORT':str(port),
         'STUDIO_DATA_DIR':str(tmp_path/'saved-data'),
         'STUDIO_DIAGNOSTIC_DIR':str(tmp_path/'logs'), 'PYTHONPATH':str(service)}
    uri=f'http://127.0.0.1:{port}'
    executable=service/'run_worker.py'
    aid=first_start=receipt=None
    for phase in range(3):
        process=subprocess.Popen([sys.executable,str(executable)],env=env,
                                 stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL)
        try:
            start=time.monotonic()
            with httpx.Client(timeout=1.5,headers={'X-Studio-Token':token}) as http:
                while True:
                    if process.poll() is not None:raise AssertionError('Worker exited before authenticated readiness')
                    try:
                        res=http.get(uri+'/api/health')
                        if res.status_code==200 and res.json()['version']=='1.0.0-rc.3':break
                    except httpx.HTTPError:pass
                    if time.monotonic()-start>14:raise AssertionError('Worker failed authenticated readiness')
                    time.sleep(.08)
                assert http.get(uri+'/api/health',headers={'X-Studio-Token':'wrong'}).status_code==401
                if phase==0:
                    payload={'title':'Subprocess persisted result','duration_seconds':90,
                             'require_start':True,'questions':[{'id':'q','stem':'Choose A',
                             'kind':'single','correct':'A','options':[{'label':'A','text':'Yes'},
                                                                     {'label':'B','text':'No'}]}]}
                    created=http.post(uri+'/api/assessments',json=payload)
                    assert created.status_code==200,created.text
                    aid=created.json()['id']
                    first_start=http.post(uri+f'/api/assessments/{aid}/start').json()['draft']['started']
                    save=http.post(uri+f'/api/assessments/{aid}/draft',json={
                        'answers':{'q':'A'},'review':[],'started':first_start})
                    assert save.status_code==200,save.text
                    assert http.get(uri+f'/api/assessments/{aid}/latest-result').json()['attempt'] is None
                elif phase==1:
                    restored=http.post(uri+f'/api/assessments/{aid}/start').json()['draft']
                    assert restored['started']==first_start and restored['answers']=={'q':'A'}
                    done=http.post(uri+f'/api/assessments/{aid}/submit',json={
                        'started':first_start,'answers':{'q':'A'}})
                    assert done.status_code==200,done.text
                    receipt=done.json()['attempt_id']
                    assert http.get(uri+f'/api/assessments/{aid}/latest-result').json()['attempt']['attempt_id']==receipt
                else:
                    item=http.get(uri+f'/api/assessments/{aid}/latest-result').json()['attempt']
                    assert item['attempt_id']==receipt and item['result']['score']==1
                    assert item['result']['percent']==100
        finally:
            process.terminate()
            try:process.wait(timeout=8)
            except subprocess.TimeoutExpired:
                process.kill();process.wait(timeout=5)
    with sqlite3.connect(tmp_path/'saved-data'/'studio.sqlite3') as connection:
        assert connection.execute('PRAGMA user_version').fetchone()[0]==7
        assert connection.execute('SELECT COUNT(*) FROM attempts WHERE assessment_id=?',(aid,)).fetchone()[0]==1
    assert token not in (tmp_path/'logs'/'worker-startup.jsonl').read_text()


def test_historical_completed_attempt_without_receipt_is_readable(client):
    """Preserve legacy practice result history from before receipt migration v6."""
    aid = _strict(client, title='Legacy completed result recovery')
    started=time.time()-20
    result={'score':1,'percent':100,'explanations':[]}
    attempt_id=db.save_attempt(aid,{'q1':'B'},result,started)
    restored=client.get(f'/api/assessments/{aid}/latest-result')
    assert restored.status_code==200,restored.text
    row=restored.json()['attempt']
    assert row['attempt_id']==attempt_id and row['result']==result
    assert row['finished']>=started
