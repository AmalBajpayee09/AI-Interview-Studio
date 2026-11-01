"""Stand-alone packaged worker entry point. Listens only on localhost."""
import os
import sys
import uvicorn
from pathlib import Path

def load_env():
    # .env is read from an explicit environment override or the repository root.
    path=Path(os.environ.get('STUDIO_ENV_FILE') or (Path.home()/'.ai-interview-studio'/'.env' if getattr(sys,'frozen',False) else Path(__file__).resolve().parents[2]/'.env'))
    if path.exists():
        for row in path.read_text(encoding='utf8').splitlines():
            row=row.strip()
            if not row or row.startswith('#') or '=' not in row: continue
            key,value=row.split('=',1);key=key.strip()
            if key.isidentifier() and key not in os.environ:
                os.environ[key]=value.strip().strip('"').strip("'")

if __name__=='__main__':
    load_env()
    uvicorn.run('app.main:app',host='127.0.0.1',port=int(os.environ.get('STUDIO_PORT','8765')),log_level='warning',workers=1)
