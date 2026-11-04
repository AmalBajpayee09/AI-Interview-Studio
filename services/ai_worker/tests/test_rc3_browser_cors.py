"""Browser preflight regression for packaged Tauri->FastAPI worker.

A real browser omits X-Studio-Token from its OPTIONS preflight, then sends it
with the actual request. This test does not replace installed WebView2 E2E.
"""


def test_installed_tauri_origin_preflight_is_unauthenticated_but_post_is_not(client, monkeypatch):
    secret='synthetic-cors-test-token'
    monkeypatch.setenv('STUDIO_WORKER_TOKEN',secret)
    origin='http://tauri.localhost'
    preflight=client.options('/api/assessments',headers={
        'Origin':origin,
        'Access-Control-Request-Method':'POST',
        'Access-Control-Request-Headers':'content-type,x-studio-token'
    })
    assert preflight.status_code==200,preflight.text
    assert preflight.headers.get('access-control-allow-origin')==origin
    assert 'x-studio-token' in preflight.headers.get('access-control-allow-headers','').lower()

    payload={
        'title':'Synthetic browser CORS attempt','duration_seconds':120,'require_start':True,
        'questions':[{
            'id':'q1','stem':'Choose an answer','kind':'single','correct':'B',
            'options':[{'label':'A','text':'Wrong'},{'label':'B','text':'Correct'}]
        }]
    }
    unauthenticated=client.post('/api/assessments',headers={'Origin':origin},json=payload)
    assert unauthenticated.status_code==401
    assert unauthenticated.headers.get('access-control-allow-origin')==origin
    authenticated=client.post('/api/assessments',headers={
        'Origin':origin,'X-Studio-Token':secret
    },json=payload)
    assert authenticated.status_code==200,authenticated.text
    assert authenticated.json().get('id')
    assert authenticated.headers.get('access-control-allow-origin')==origin


def test_preflight_rejects_untrusted_browser_origin(client,monkeypatch):
    monkeypatch.setenv('STUDIO_WORKER_TOKEN','synthetic-cors-test-token')
    rejected=client.options('/api/assessments',headers={
        'Origin':'https://attacker.example',
        'Access-Control-Request-Method':'POST',
        'Access-Control-Request-Headers':'content-type,x-studio-token'
    })
    assert rejected.status_code==400
    assert 'access-control-allow-origin' not in rejected.headers
    real=client.get('/api/health',headers={
        'Origin':'https://attacker.example',
        'X-Studio-Token':'synthetic-cors-test-token'})
    assert real.status_code==403
    assert 'access-control-allow-origin' not in real.headers


def test_frontend_put_and_tauri_https_preflight(client,monkeypatch):
    monkeypatch.setenv('STUDIO_WORKER_TOKEN','synthetic-cors-test-token')
    origin='https://tauri.localhost'
    preflight=client.options('/api/code/drafts/python',headers={
        'Origin':origin,
        'Access-Control-Request-Method':'PUT',
        'Access-Control-Request-Headers':'content-type,x-studio-token'})
    assert preflight.status_code==200
    assert 'PUT' in preflight.headers.get('access-control-allow-methods','')
    assert preflight.headers.get('access-control-allow-origin')==origin
    reply=client.put('/api/code/drafts/python',headers={
        'Origin':origin,'X-Studio-Token':'synthetic-cors-test-token'},
        json={'code':'print(123)'})
    assert reply.status_code==200,reply.text
