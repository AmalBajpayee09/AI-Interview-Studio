"""v1.0 hardening tests. Real FastAPI/SQLite and PCM fixtures; not Windows or live AI."""
import io
import wave
import time
from array import array
from app import db, audio_offline


def create_quiz(client, duration=120):
    r=client.post('/api/assessments',json={'title':'Timed recovery validation',
        'duration_seconds':duration,
        'questions':[{'id':'num','kind':'numerical','stem':'Compute 6x7','correct':'42'},
                     {'id':'one','kind':'single','stem':'One correct','correct':'B',
                      'options':[{'label':'A','text':'Wrong'},{'label':'B','text':'Right'}]}]})
    assert r.status_code==200,r.text
    return r.json()['id']


def test_server_start_cannot_be_changed_by_autosave(client):
    aid=create_quiz(client)
    start=client.post(f'/api/assessments/{aid}/start').json()['draft']['started']
    good={'started':start,'answers':{'num':'42'},'review':['num']}
    assert client.post(f'/api/assessments/{aid}/draft',json=good).status_code==200
    bad={**good,'started':start+5,'answers':{'num':'12'}}
    assert client.post(f'/api/assessments/{aid}/draft',json=bad).status_code==409
    draft=client.get(f'/api/assessments/{aid}/draft').json()['draft']
    assert draft['started']==start and draft['answers']=={'num':'42'}
    assert client.post(f'/api/assessments/{aid}/start').json()['draft']['started']==start
    assert client.post(f'/api/assessments/{aid}/submit',json={'started':start+5,'answers':{'num':'42'}}).status_code==409
    assert client.get(f'/api/assessments/{aid}/draft').json()['draft'] is not None


def test_expired_exam_scores_only_previously_saved_answers(client):
    aid=create_quiz(client)
    start=client.post(f'/api/assessments/{aid}/start').json()['draft']['started']
    assert client.post(f'/api/assessments/{aid}/draft',json={
        'started':start,'answers':{'num':'42'},'review':[]}).status_code==200
    expired=time.time()-125
    with db.connect() as connection:
        connection.execute('UPDATE assessment_drafts SET started=? WHERE assessment_id=?',(expired,aid))
    assert client.post(f'/api/assessments/{aid}/draft',json={
        'started':expired,'answers':{'num':'0','one':'B'},'review':[]}).status_code==409
    response=client.post(f'/api/assessments/{aid}/submit',json={
        'started':expired,'answers':{'num':'0','one':'B'}})
    assert response.status_code==200,response.text
    result=response.json()
    assert result['timed_out'] is True and result['timing_enforcement']=='server_started_draft'
    assert result['correct']==1 and result['incorrect']==0 and result['unanswered']==1
    assert result['elapsed_seconds']>=120
    assert client.get(f'/api/assessments/{aid}/draft').json()['draft'] is None
    retry=client.post(f'/api/assessments/{aid}/submit',json={
        'started':expired,'answers':{'one':'B','num':'42'}}).json()
    assert retry['attempt_id']==result['attempt_id'] and retry['duplicate_submission']
    with db.connect() as connection:
        assert connection.execute('SELECT count(*) FROM attempts WHERE assessment_id=?',(aid,)).fetchone()[0]==1


def test_legacy_unstarted_submission_is_explicitly_labelled(client):
    aid=create_quiz(client)
    response=client.post(f'/api/assessments/{aid}/submit',json={
        'started':time.time(),'answers':{'one':'B'}})
    assert response.status_code==200
    assert response.json()['timing_enforcement']=='legacy_unstarted_practice'
    assert response.json()['timed_out'] is False


def test_opposite_phase_stereo_is_not_silence():
    rate=16000
    samples=array('h')
    for index in range(rate):
        value=8000 if rate//10 <= index < rate*8//10 else 0
        samples.extend([value,-value])
    output=io.BytesIO()
    with wave.open(output,'wb') as file:
        file.setnchannels(2);file.setsampwidth(2);file.setframerate(rate)
        file.writeframes(samples.tobytes())
    result=audio_offline.analyze_wav(output.getvalue())
    assert result['channels']==2 and len(result['segments'])==1
    assert result['segments'][0]['speaker']=='unknown'
    assert not result['transcription_performed']
