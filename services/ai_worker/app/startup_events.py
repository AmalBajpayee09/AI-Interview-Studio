"""Minimal startup telemetry. Only static stage names and fixed error classifications.

No credentials, prompts, transcripts, HTTP data, device information or filesystem
paths are included in log records. Disabled when STUDIO_DIAGNOSTIC_DIR is absent.
"""
import json
import os
import time
from pathlib import Path

STAGES = frozenset({'process_started', 'environment_loaded', 'database_initialized',
                    'database_failure', 'server_starting', 'worker_stopping'})
OUTCOMES = frozenset({'ok', 'error'})
MAX_SIZE = 128 * 1024


def record(stage: str, outcome: str = 'ok') -> None:
    if stage not in STAGES or outcome not in OUTCOMES:
        raise ValueError('Unknown startup diagnostic event')
    root = os.environ.get('STUDIO_DIAGNOSTIC_DIR', '')
    if not root:
        return
    try:
        directory = Path(root)
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / 'worker-startup.jsonl'
        if path.exists() and path.stat().st_size >= MAX_SIZE:
            previous = directory / 'worker-startup.previous.jsonl'
            previous.unlink(missing_ok=True)
            path.replace(previous)
        line = {'timestamp_ms': int(time.time() * 1000), 'component': 'python-worker',
                'stage': stage, 'outcome': outcome}
        with path.open('a', encoding='utf-8') as output:
            output.write(json.dumps(line, separators=(',', ':')) + '\n')
    except OSError:
        # Logging failures may never prevent the local worker from functioning.
        pass
