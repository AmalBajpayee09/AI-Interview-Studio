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
