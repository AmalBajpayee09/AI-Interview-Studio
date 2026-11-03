"""Real ZIP/DOCX admission tests; no LLM or Windows claims."""
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from docx import Document
from app import file_security


def _zip(entries):
    buffer=BytesIO()
    with ZipFile(buffer, 'w', ZIP_DEFLATED) as z:
        for filename, body in entries.items():
            z.writestr(filename, body)
    return buffer.getvalue()


def _post(client,data,name='resume.docx'):
    return client.post('/api/files/extract',files={'file':(name,data,'application/vnd.openxmlformats-officedocument.wordprocessingml.document')})


def test_real_docx_resume_and_table_extraction(client):
    d=Document();d.add_paragraph('Experience: Backend software developer')
    t=d.add_table(rows=1,cols=2);t.cell(0,0).text='Project';t.cell(0,1).text='Search API'
    stream=BytesIO();d.save(stream)
    assert file_security.validate_docx(stream.getvalue()) is None
    result=_post(client,stream.getvalue())
    assert result.status_code==200,result.text
    assert 'Backend software developer' in result.json()['text']
    assert 'Project | Search API' in result.json()['text']


def test_reject_archive_expansion_bomb(client):
    # 11 MB of repeated XML compresses to kilobytes, bypassing input byte limits.
    data=_zip({'[Content_Types].xml':'types','word/document.xml':'A'*11_000_000})
    assert len(data)<6_000_000
    response=_post(client,data)
    assert response.status_code==422
    assert 'UnsafeDocument' in response.text


def test_reject_path_traversal_archive_member(client):
    data=_zip({'[Content_Types].xml':'types','word/document.xml':'doc','../user-data.txt':'not safe'})
    assert _post(client,data).status_code==422


def test_reject_macro_enabled_docx(client):
    data=_zip({'[Content_Types].xml':'types','word/document.xml':'doc','word/vbaProject.bin':'bytecode'})
    assert _post(client,data).status_code==422


def test_reject_non_zip_and_missing_parts(client):
    assert _post(client,b'not a zip at all').status_code==422
    assert _post(client,_zip({'word/document.xml':'not enough'})).status_code==422


def test_reject_excess_archive_entries(client):
    content={'[Content_Types].xml':'types','word/document.xml':'document'}
    content.update({f'word/media/file{i}.xml':'x' for i in range(file_security.MAX_ENTRIES+1)})
    assert _post(client,_zip(content)).status_code==422
