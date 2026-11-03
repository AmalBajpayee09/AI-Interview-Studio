"""Bounded asynchronous orchestration for Docker-only untrusted code execution.

Submitted source is retained only in a running job's closure; not logged or stored.
No non-Docker fallback is allowed.
"""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
import threading
import time
import uuid
from . import code_runner

MAX_CONCURRENT=2
MAX_RETAINED=80
RETENTION_SECONDS=3600

@dataclass
class ExecutionJob:
    id: str=field(default_factory=lambda:str(uuid.uuid4()))
    state: str='queued'
    created_at: float=field(default_factory=time.time)
    updated_at: float=field(default_factory=time.time)
    result: dict|None=None
    error: str|None=None
    cancelled: threading.Event=field(default_factory=threading.Event,repr=False)
    def public(self):
        return {'id':self.id,'state':self.state,'created_at':self.created_at,
                'updated_at':self.updated_at,'result':self.result,'error':self.error}

class ExecutionQueue:
    def __init__(self):
        self._lock=threading.RLock()
        self._slots=threading.BoundedSemaphore(MAX_CONCURRENT)
        self._executor=ThreadPoolExecutor(max_workers=MAX_CONCURRENT,thread_name_prefix='docker-practice')
        self._jobs:dict[str,ExecutionJob]={}
        self._closed=False
    def _prune(self):
        now=time.time()
        for key,job in list(self._jobs.items()):
            if job.state in ('finished','failed','cancelled') and now-job.updated_at>RETENTION_SECONDS:
                self._jobs.pop(key,None)
        finished=sorted((j for j in self._jobs.values() if j.state in ('finished','failed','cancelled')),key=lambda j:j.updated_at)
        for job in finished[:max(0,len(self._jobs)-MAX_RETAINED)]:
            self._jobs.pop(job.id,None)
    def submit(self,code,language,stdin='',expected=None,timeout_seconds=5):
        code_runner.validate(code,language,stdin,expected,timeout_seconds)
        if not code_runner.docker_available()['available']:
            raise code_runner.ExecutionUnavailable('Docker Linux container engine is unavailable; isolated execution disabled')
        with self._lock:
            if self._closed:raise code_runner.ExecutionUnavailable('Execution service is shutting down')
            if not self._slots.acquire(blocking=False):
                raise code_runner.ExecutionUnavailable('Two code executions are already active; retry later')
            self._prune()
            job=ExecutionJob()
            self._jobs[job.id]=job
            try:self._executor.submit(self._work,job,code,language,stdin,expected,timeout_seconds)
            except Exception:
                self._jobs.pop(job.id,None);self._slots.release();raise
            return job.public()
    def _work(self,job,code,language,stdin,expected,timeout_seconds):
        try:
            with self._lock:
                job.state='cancelled' if job.cancelled.is_set() else 'running';job.updated_at=time.time()
            if job.state=='cancelled':return
            try:
                result=code_runner.run(code,language,stdin,expected,timeout_seconds,cancel_event=job.cancelled)
                with self._lock:
                    job.result=result
                    job.state='cancelled' if result.get('status')=='cancelled' or job.cancelled.is_set() else 'finished'
                    job.updated_at=time.time()
            except (code_runner.ExecutionUnavailable,code_runner.InvalidCode) as exc:
                with self._lock:
                    job.error=str(exc)
                    job.state='cancelled' if job.cancelled.is_set() else 'failed'
                    job.updated_at=time.time()
            except Exception:
                with self._lock:
                    job.error='Isolated runner failed unexpectedly';job.state='failed';job.updated_at=time.time()
        finally:self._slots.release()
    def get(self,job_id):
        with self._lock:
            job=self._jobs.get(job_id)
            if not job:raise KeyError('Unknown or expired execution job')
            return job.public()
    def cancel(self,job_id):
        with self._lock:
            job=self._jobs.get(job_id)
            if not job:raise KeyError('Unknown execution job')
            if job.state not in ('finished','failed','cancelled'):job.cancelled.set()
            return job.public()
    def shutdown(self):
        with self._lock:
            self._closed=True
            for job in self._jobs.values():
                if job.state in ('queued','running'):job.cancelled.set()
        self._executor.shutdown(wait=False,cancel_futures=False)

_global_lock=threading.Lock()
_execution_queue:ExecutionQueue|None=None
def get_queue()->ExecutionQueue:
    global _execution_queue
    with _global_lock:
        if _execution_queue is None:_execution_queue=ExecutionQueue()
        return _execution_queue
def shutdown_jobs()->None:
    global _execution_queue
    with _global_lock:
        queue=_execution_queue;_execution_queue=None
    if queue is not None:queue.shutdown()
