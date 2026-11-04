"""Installed Windows Tauri overlay-first lifecycle acceptance.

Requires Playwright Python bindings and a genuine installed NSIS desktop.
Uses temporary WebView2 CDP policy only within isolated Windows CI.
Never enables browser debugging in production application defaults.
"""
from __future__ import annotations
import ctypes
import json
import os
import runpy
import socket
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

helpers=runpy.run_path(str(Path(__file__).with_name('rc3-installed-webview-assessment.py')))
policy=helpers['temporary_test_only_webview_cdp_policy']
wait_debug_port=helpers['wait_debug_port']
close_window=helpers['close_window']
temporary_folder=helpers['verified_temporary_directory']
free_port=helpers['free_port']

VERSION='1.0.0-rc.4'

def chord(letter: str) -> None:
    # Actual system-global shortcut, not an injected JavaScript keydown event.
    user32=ctypes.windll.user32
    keys=[0x11,0x12,0x10,ord(letter.upper())]  # CTRL + ALT + SHIFT + key
    for code in keys:
        user32.keybd_event(code,0,0,0)
    time.sleep(.15)
    for code in reversed(keys):
        user32.keybd_event(code,0,2,0)


def wait_native_state(page, expected, timeout=10):
    end=time.monotonic()+timeout
    while time.monotonic()<end:
        try:
            state=page.evaluate("() => window.__TAURI_INTERNALS__.invoke('overlay_window_status')")
            if state.get('visible') is expected:return state
        except Exception:
            pass
        time.sleep(.2)
    raise AssertionError(f'Native overlay visibility did not become {expected}')


def wait_worker(log_dir:Path,proc,seconds=75):
    marker=log_dir/'worker-readiness.json'
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        if proc.poll() is not None:raise AssertionError('Installed desktop exited before worker readiness')
        if marker.exists():
            try:
                m=json.loads(marker.read_text(encoding='utf8'))
                if m.get('stage')=='ready' and m.get('authenticated') and m.get('app_version')==VERSION:
                    return int(m['worker_pid'])
            except (OSError,ValueError,KeyError):
                pass
        time.sleep(.25)
    raise AssertionError('Installed worker never achieved authenticated readiness')


def run(executable:Path,report:Path):
    steps=[]
    evidence={'commit':os.getenv('GITHUB_SHA','unknown'),
              'version':VERSION,'environment':'GitHub Windows installed NSIS / WebView2',
              'steps':steps,'result':'NOT RUN'}
    report.parent.mkdir(parents=True,exist_ok=True)
    app=None;browser=None;worker_pid=None
    try:
        with temporary_folder(report) as root, sync_playwright() as playwright:
            data,profile=root/'data',root/'webview-profile'
            data.mkdir();profile.mkdir()
            log_dir=Path(os.environ['LOCALAPPDATA'])/'com.interviewstudio.desktop'/'logs'
            port=free_port()
            env=os.environ.copy()
            env['STUDIO_DATA_DIR']=str(data)
            env['WEBVIEW2_USER_DATA_FOLDER']=str(profile)
            env['WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS']=f'--remote-debugging-port={port} --remote-debugging-address=127.0.0.1'
            with policy(executable.name,port):
                app=subprocess.Popen([str(executable)],env=env,stdin=subprocess.DEVNULL,
                                     stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                wait_debug_port(port,app)
            browser=playwright.chromium.connect_over_cdp(f'http://127.0.0.1:{port}',timeout=20000)
            context=browser.contexts[0]
            page=None
            end=time.monotonic()+40
            while time.monotonic()<end:
                for p in context.pages:
                    if p.locator('#overlay-question-input').count():
                        page=p;break
                if page:break
                time.sleep(.25)
            assert page is not None,'Default window never loaded the small overlay'
            expect(page.get_by_text('Floating practice assistant')).to_be_visible()
            assert page.locator('aside.sidebar').count()==0,'Dashboard launched as primary interface'
            state=wait_native_state(page,True)
            assert state.get('tray_installed') and state.get('hotkey_registered'),state
            steps.append({'stage':'overlay-first-native-tray-and-shortcut','result':'PASS'})
            worker_pid=wait_worker(log_dir,app)
            expect(page.get_by_text('Local AI worker connected')).to_be_visible(timeout=25000)
            steps.append({'stage':'authenticated-bundled-worker','result':'PASS','worker_pid':worker_pid})
            for layout,text in [('Teleprompter','Teleprompter · speaking cues'),
                                ('Split desk','Question and context'),
                                ('Q&A feed','Chronological Q&A feed'),
                                ('Compact','Suggested answer')]:
                page.get_by_role('button',name=layout,exact=True).click()
                expect(page.get_by_text(text,exact=True)).to_be_visible()
            steps.append({'stage':'four-overlay-layouts-share-active-session','result':'PASS'})
            page.get_by_role('button',name='New session').click()
            end=time.monotonic()+10
            db=data/'studio.sqlite3'
            while time.monotonic()<end:
                if db.exists():
                    conn=sqlite3.connect(db)
                    try:
                        row=conn.execute('SELECT count(*) FROM sessions').fetchone()
                    finally:
                        conn.close()
                    if row and row[0]>=1:break
                time.sleep(.2)
            else:raise AssertionError('Overlay did not create persistent session')
            steps.append({'stage':'overlay-session-persists-in-real-sqlite','result':'PASS'})
            page.get_by_role('button',name='Open workspace and settings').click()
            end=time.monotonic()+20;workspace=None
            while time.monotonic()<end:
                for p in context.pages:
                    if p!=page and p.locator('aside.sidebar').count():
                        workspace=p;break
                if workspace:break
                time.sleep(.2)
            assert workspace is not None,'Secondary workspace was not created'
            expect(workspace.get_by_text('Assessments',exact=True).first).to_be_visible()
            workspace.close()
            assert app.poll() is None,'Closing workspace terminated the background service'
            steps.append({'stage':'secondary-workspace-retained-and-close-does-not-exit','result':'PASS'})
            chord('O');wait_native_state(page,False)
            assert app.poll() is None,'Hiding overlay terminated the application'
            assert wait_worker(log_dir,app)==worker_pid,'Hiding overlay restarted or killed the worker'
            chord('O');wait_native_state(page,True)
            steps.append({'stage':'real-global-shortcut-hide-show-keeps-worker','result':'PASS'})
            page.locator('select[aria-label="Global overlay shortcut"]').select_option('Ctrl+Alt+Shift+P')
            state=page.evaluate("() => window.__TAURI_INTERNALS__.invoke('overlay_window_status')")
            assert state['hotkey']=='Ctrl+Alt+Shift+P' and state['hotkey_registered']
            chord('P');wait_native_state(page,False)
            chord('P');wait_native_state(page,True)
            steps.append({'stage':'reconfigurable-global-shortcut','result':'PASS'})
            close_window(app.pid)
            wait_native_state(page,False)
            assert app.poll() is None,'Window close terminated tray-resident app'
            assert wait_worker(log_dir,app)==worker_pid
            chord('P');wait_native_state(page,True)
            steps.append({'stage':'closing-overlay-preserves-worker-and-tray','result':'PASS'})
            page.once('dialog',lambda dialog:dialog.accept())
            page.get_by_role('button',name='Exit',exact=True).click()
            app.wait(timeout=20)
            end=time.monotonic()+15
            while time.monotonic()<end:
                handle=ctypes.windll.kernel32.OpenProcess(0x1000,False,worker_pid)
                if not handle:break
                code=ctypes.c_ulong()
                ctypes.windll.kernel32.GetExitCodeProcess(handle,ctypes.byref(code))
                ctypes.windll.kernel32.CloseHandle(handle)
                if code.value!=259:break  # STILL_ACTIVE is Windows exit code 259
                time.sleep(.2)
            else:raise AssertionError('Worker process remained alive after native exit')
            steps.append({'stage':'native-explicit-exit-stops-owned-worker','result':'PASS'})
            evidence['result']='PASS'
    except Exception as exc:
        evidence['result']='FAIL'
        evidence['failure_category']=type(exc).__name__
        evidence['failure_message']=str(exc)[:220]
        raise
    finally:
        if browser:
            try:browser.close()
            except Exception:pass
        if app and app.poll() is None:
            subprocess.run(['taskkill','/PID',str(app.pid),'/T','/F'],capture_output=True)
            app.wait(timeout=10)
        report.write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf8')
    print('RC4 installed overlay acceptance:',evidence['result'])

if __name__=='__main__':
    if sys.platform!='win32':raise SystemExit('BLOCKED: real Windows desktop / WebView2 required')
    import argparse
    cli=argparse.ArgumentParser()
    cli.add_argument('--installed-exe',type=Path,required=True)
    cli.add_argument('--report',type=Path,required=True)
    args=cli.parse_args()
    assert args.installed_exe.is_file(),'NSIS installed executable missing'
    run(args.installed_exe,args.report)
