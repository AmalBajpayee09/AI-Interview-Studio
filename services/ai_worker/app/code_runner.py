"""Optional Docker-isolated code practice. Without a verified container runtime: refuse.

Requires user-installed local images. The host does NOT execute supplied programs.
Security boundary: Docker's Linux VM with no network, dropped capabilities, read-only
root, nonroot UID, pids/cpu/memory limits, and no host secrets mounted.
"""
from __future__ import annotations
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

LANGUAGES = {
    'python': ('python:3.11-alpine', 'Main.py', 'python /code/Main.py'),
    'javascript': ('node:22-alpine', 'Main.js', 'node /code/Main.js'),
    'cpp': ('gcc:14', 'Main.cpp', 'cp /code/Main.cpp /work/Main.cpp && g++ -std=c++17 -O2 -o /work/solution /work/Main.cpp && /work/solution'),
    'java': ('eclipse-temurin:21-jdk', 'Main.java', 'cp /code/Main.java /work/Main.java && javac -d /work /work/Main.java && java -cp /work Main'),
}

class ExecutionUnavailable(Exception): pass
class InvalidCode(ValueError): pass

def docker_available() -> dict:
    if not shutil.which('docker'):
        return {'available':False,'reason':'Docker CLI not installed; execution disabled.'}
    try:
        r=subprocess.run(['docker','info','--format','{{.ServerVersion}}'],capture_output=True,text=True,timeout=4)
        if r.returncode: return {'available':False,'reason':'Docker engine unavailable; enable Docker Desktop Linux containers.'}
        return {'available':True,'engine':r.stdout.strip(), 'languages':list(LANGUAGES)}
    except (OSError, subprocess.TimeoutExpired):
        return {'available':False,'reason':'Docker engine did not respond; execution disabled.'}

def available_image(language: str) -> str:
    if language not in LANGUAGES: raise InvalidCode('Unsupported language')
    image=LANGUAGES[language][0]
    try:
        r=subprocess.run(['docker','image','inspect',image],capture_output=True,timeout=5)
    except (OSError,subprocess.TimeoutExpired) as e:
        raise ExecutionUnavailable('Docker cannot inspect installed images') from e
    if r.returncode: raise ExecutionUnavailable(f'Container image {image} is missing. Pull it manually with: docker pull {image}')
    return image

def run(code: str, language: str, stdin: str = '', expected: str | None = None, timeout_seconds: int = 5) -> dict:
    if language not in LANGUAGES: raise InvalidCode('Use python, javascript, cpp, or java')
    if not isinstance(code,str) or not 0<len(code)<=40000: raise InvalidCode('Code size must be 1–40,000 characters')
    if not isinstance(stdin,str) or len(stdin)>16000: raise InvalidCode('Standard input must be at most 16,000 characters')
    if expected is not None and (not isinstance(expected,str) or len(expected)>16000): raise InvalidCode('Expected output is too long')
    if not 1<=timeout_seconds<=10: raise InvalidCode('Timeout must be between 1 and 10 seconds')
    status=docker_available()
    if not status['available']: raise ExecutionUnavailable(status['reason'])
    image=available_image(language)
    _, filename, program = LANGUAGES[language]
    start=time.perf_counter()
    with tempfile.TemporaryDirectory(prefix='studio-run-') as directory:
        folder=Path(directory)
        os.chmod(folder,0o755)
        source=folder/filename
        source.write_text(code,encoding='utf-8')
        # On Docker Desktop for Windows the path is mounted inside the Linux VM.
        command=['docker','run','--rm','-i','--network','none','--read-only',
            '--cap-drop','ALL','--security-opt','no-new-privileges','--pids-limit','64',
            '--memory','256m','--cpus','1','--user','65534:65534',
            '--tmpfs','/tmp:rw,nosuid,noexec,size=16m',
            '--tmpfs','/work:rw,nosuid,size=96m',
            '--mount',f'type=bind,source={folder.resolve()},target=/code,readonly',
            '--workdir','/work',image,'sh','-c',program]
        cidfile=folder/'container.cid'
        command[2:2]=['--cidfile',str(cidfile)]
        # Capture output to bounded temporary files instead of unbounded PIPE memory.
        # Monitor both files; stop the container if a program floods output.
        stdout_file=folder/'stdout.bin'
        stderr_file=folder/'stderr.bin'
        input_file=folder/'stdin.txt'
        input_file.write_text(stdin,encoding='utf-8')
        output_limit=32768
        exceeded=False
        timed_out=False
        try:
            with input_file.open('rb') as inf, stdout_file.open('wb') as outf, stderr_file.open('wb') as errf:
                process=subprocess.Popen(command,stdin=inf,stdout=outf,stderr=errf)
                deadline=time.monotonic()+timeout_seconds+3
                while process.poll() is None:
                    if stdout_file.stat().st_size>output_limit or stderr_file.stat().st_size>output_limit:
                        exceeded=True
                        break
                    if time.monotonic()>deadline:
                        timed_out=True
                        break
                    time.sleep(.03)
                if exceeded or timed_out:
                    process.kill()
                try: process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=2)
        except OSError as exc:
            raise ExecutionUnavailable('Docker execution process failed.') from exc
        finally:
            # A detached container may outlive a killed Docker CLI. Exact-CID cleanup.
            if cidfile.exists():
                try:
                    cid=cidfile.read_text(encoding='ascii').strip()
                    if len(cid)==64 and all(c in '0123456789abcdef' for c in cid):
                        subprocess.run(['docker','rm','-f',cid],capture_output=True,timeout=5)
                except (OSError,subprocess.TimeoutExpired): pass
        if timed_out: raise ExecutionUnavailable('Execution timed out; container termination requested.')
        out_bytes=stdout_file.read_bytes()[:output_limit]
        err_bytes=stderr_file.read_bytes()[:output_limit]
        stdout=out_bytes.decode('utf-8',errors='replace')
        stderr=err_bytes.decode('utf-8',errors='replace')
        if exceeded: stderr += '\nOutput limit exceeded; container stopped.'
        elapsed=round((time.perf_counter()-start)*1000,1)
        exit_code=process.returncode if not exceeded else -1
        passed=(not exceeded and exit_code==0 and (expected is None or stdout.strip()==expected.strip()))
        return {'status':'passed' if passed else 'failed','exit_code':exit_code,
            'stdout':stdout,'stderr':stderr,'stdout_truncated':stdout_file.stat().st_size>output_limit,
            'stderr_truncated':stderr_file.stat().st_size>output_limit,'elapsed_ms':elapsed,
            'expected':expected,'matched':None if expected is None else stdout.strip()==expected.strip(),
            'isolation':'Docker Linux container (network disabled, nonroot, resource limited)',
            'image':image}
