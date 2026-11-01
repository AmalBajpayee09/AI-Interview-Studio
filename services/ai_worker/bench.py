import json,statistics,time,platform,psutil
from app import logic,db
from fastapi.testclient import TestClient
from app.main import app

with TestClient(app) as client:
    starts=[]
    for i in range(250):
        t=time.perf_counter(); logic.classify('Implement a binary search function in Python'); starts.append((time.perf_counter()-t)*1000)
    b=[]
    for i in range(80):
        t=time.perf_counter();client.get('/api/health');b.append((time.perf_counter()-t)*1000)
    out={'environment':platform.platform(),'cpu':platform.processor(),'ram_total_gb':round(psutil.virtual_memory().total/2**30,2),'worker_rss_mb':round(psutil.Process().memory_info().rss/2**20,2),'classification_p50_ms':round(statistics.median(starts),4),'classification_p95_ms':round(sorted(starts)[int(len(starts)*.95)],4),'health_http_p50_ms':round(statistics.median(b),3),'health_http_p95_ms':round(sorted(b)[int(len(b)*.95)],3),'stt':'not run: optional model unavailable','llm':'not run: provider not configured','desktop_ui':'not run: Windows build unavailable'}
    print(json.dumps(out,indent=2))
