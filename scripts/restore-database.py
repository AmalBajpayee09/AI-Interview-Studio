"""Offline SQLite restore utility. Stop the worker before invoking this script.

Usage: python scripts/restore-database.py BACKUP.sqlite3 --target DESTINATION.sqlite3
"""
import argparse
import os
import shutil
import socket
import sqlite3
import tempfile
from pathlib import Path
from datetime import datetime

def verify(path:Path):
    if not path.is_file() or path.stat().st_size>250*1024*1024:
        raise ValueError('Expected an existing SQLite backup file under 250 MB')
    with sqlite3.connect(f'file:{path.as_posix()}?mode=ro',uri=True) as database:
        if database.execute('PRAGMA integrity_check').fetchone()[0]!='ok':
            raise ValueError('Database integrity check failed')
        if not 1<=database.execute('PRAGMA user_version').fetchone()[0]<=4:
            raise ValueError('Unsupported database schema version')
        names={x[0] for x in database.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if not {'sessions','turns','assessments','documents'}.issubset(names):
            raise ValueError('File is not a supported AI Interview Studio database')

def restore(source:Path,target:Path,check_port:bool=True):
    source=source.expanduser().resolve()
    target=target.expanduser().resolve()
    if source==target: raise ValueError('Source and target must differ')
    if check_port:
        with socket.socket() as sock:
            sock.settimeout(0.2)
            if sock.connect_ex(('127.0.0.1',8765))==0:
                raise RuntimeError('AI worker is running on port 8765; shut it down before restoring')
    verify(source)
    target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():
        stamp=datetime.now().strftime('%Y%m%d-%H%M%S')
        shutil.copy2(target,target.with_name(f'{target.name}.before-restore-{stamp}.bak'))
    handle,tmp=tempfile.mkstemp(prefix='.studio-restore-',suffix='.sqlite3',dir=target.parent)
    os.close(handle)
    try:
        shutil.copy2(source,tmp)
        verify(Path(tmp))
        os.replace(tmp,target)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Restore a validated SQLite backup while AI worker is STOPPED')
    parser.add_argument('backup',type=Path)
    parser.add_argument('--target',type=Path,default=Path.home()/'.ai-interview-studio'/'studio.sqlite3')
    args=parser.parse_args()
    restore(args.backup,args.target)
    print('Restore complete. Existing database preserved as a timestamped .bak if present.')
