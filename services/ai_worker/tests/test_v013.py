"""v0.13 resume evidence tests: no actual LLM interview is claimed."""
from app import resume_intelligence
SAMPLE="""Name: Candidate
Skills
Python, SQL, React
Education
B.Tech in Computer Science
Projects
Inventory Portal - React frontend and SQLite backend
Interview Bot - Speech transcription
Achievements
Won an internal hackathon
"""

def test_source_lines_are_preserved():
    output=resume_intelligence.sections(SAMPLE,'doc123')
    assert output['document_id']=='doc123' and output['source_grounded']
    assert len(output['sections'])==4
    assert output['sections'][0]['source']=={'document_id':'doc123','start_line':3,'end_line':3}
    assert 'Inventory Portal' in output['questions'][0]['question']
    assert 'experience' in output['missing_categories']

def test_unknown_resume_does_not_invent_projects():
    report=resume_intelligence.sections('No structured sections','ref')
    assert report['sections']==[] and report['questions']==[]

def test_resume_endpoint_reads_saved_document(client):
    r=client.post('/api/documents',json={'filename':'resume.txt','content':SAMPLE})
    assert r.status_code==200
    result=client.get('/api/documents/'+r.json()['id']+'/analyze')
    assert result.status_code==200 and 'Inventory Portal' in result.text
    assert client.get('/api/documents/missing/analyze').status_code==404
