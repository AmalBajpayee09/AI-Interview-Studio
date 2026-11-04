"""Playwright/CDP test against the *installed* Tauri WebView2 Windows application.

Runs only on isolated Windows GitHub Actions runner. Production WebView debugging is
NEVER enabled by application code. No cloud provider, Docker or microphone is used.
Synthetic test questions only; no worker secrets or private content are logged.
"""
from __future__ import annotations

import argparse
import ctypes
import json
import os
import re
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path
from contextlib import contextmanager

from playwright.sync_api import sync_playwright, expect

APP_VERSION = '1.0.0-rc.3'


def free_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def close_window(pid: int):
    user32 = ctypes.windll.user32
    # WM_CLOSE exercises the same native lifecycle as clicking the window close
    # button. It must not be replaced by a forced process kill to count as pass.
    fn = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p)
    found = []

    def each(hwnd, _):
        target = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(target))
        if target.value == pid and user32.IsWindowVisible(hwnd):
            found.append(hwnd)
        return True

    callback = fn(each)
    user32.EnumWindows(callback, 0)
    if not found:
        raise AssertionError('Installed desktop has no accessible top-level window')
    user32.PostMessageW(found[0], 0x0010, 0, 0)  # WM_CLOSE


def wait_debug_port(port, proc, seconds=60):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        if proc.poll() is not None:
            raise AssertionError('Installed desktop exited before WebView2 CDP readiness')
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/json/version', timeout=1) as response:
                obj = json.load(response)
                if obj.get('webSocketDebuggerUrl'):
                    return
        except (OSError, TimeoutError, ValueError):
            pass
        time.sleep(.3)
    raise AssertionError('Installed WebView2 never exposed test-only loopback CDP endpoint')



@contextmanager
def temporary_test_only_webview_cdp_policy(exe_name: str, port: int):
    """Enable loopback CDP only during one CI launch; restore every registry value.

    Elevated WebView2 ignores user-scoped environment and HKCU policy flags.
    HKLM AdditionalBrowserArguments is honored, so try it first; non-admin
    runners can use HKCU. This code runs only inside the Python acceptance test,
    never in the installed application's production startup.
    """
    import winreg

    policy = r'Software\Policies\Microsoft\Edge\WebView2\AdditionalBrowserArguments'
    flags = f'--remote-debugging-port={port} --remote-debugging-address=127.0.0.1'
    changed = []
    for name, hive in [('HKLM', winreg.HKEY_LOCAL_MACHINE), ('HKCU', winreg.HKEY_CURRENT_USER)]:
        try:
            key = winreg.CreateKeyEx(hive, policy, 0,
                                     winreg.KEY_QUERY_VALUE | winreg.KEY_SET_VALUE)
            try:
                try:
                    previous = winreg.QueryValueEx(key, exe_name)
                except FileNotFoundError:
                    previous = None
                winreg.SetValueEx(key, exe_name, 0, winreg.REG_SZ, flags)
                changed.append((name, hive, previous))
            finally:
                winreg.CloseKey(key)
        except OSError:
            # A non-admin test runner may lack HKLM policy-write permission.
            # A failure to set both policies must not masquerade as UI acceptance.
            continue
    if not changed:
        raise AssertionError('Test runner could not configure WebView2 debugging policy')
    try:
        yield [item[0] for item in changed]
    finally:
        for name, hive, previous in reversed(changed):
            try:
                key = winreg.OpenKey(hive, policy, 0, winreg.KEY_SET_VALUE)
                try:
                    if previous is None:
                        winreg.DeleteValue(key, exe_name)
                    else:
                        winreg.SetValueEx(key, exe_name, 0, previous[1], previous[0])
                finally:
                    winreg.CloseKey(key)
            except OSError:
                # Do not hide the original test failure; ephemeral CI runner is
                # discarded. Record only the policy hive, not its prior value.
                print(f'WARNING: could not restore temporary WebView2 {name} policy')

def launch(executable, data_dir, profile_dir, log_dir, playwright, steps):
    port = free_port()
    env = os.environ.copy()
    env['STUDIO_DATA_DIR'] = str(data_dir)
    env['WEBVIEW2_USER_DATA_FOLDER'] = str(profile_dir)
    env['WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS'] = f'--remote-debugging-port={port} --remote-debugging-address=127.0.0.1'
    proc = None
    try:
        with temporary_test_only_webview_cdp_policy(executable.name, port) as policies:
            proc = subprocess.Popen([str(executable)], env=env, stdin=subprocess.DEVNULL,
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # This is a bounded readiness check, not an arbitrary startup sleep.
            wait_debug_port(port, proc)
        steps.append({'stage': 'test-only-webview-cdp-attach',
                      'result': 'PASS', 'policy_hives': policies})
        browser = playwright.chromium.connect_over_cdp(f'http://127.0.0.1:{port}', timeout=20000)
        context = browser.contexts[0]
        deadline = time.monotonic() + 35
        while time.monotonic() < deadline:
            pages = [p for p in context.pages if not p.is_closed()]
            for page in pages:
                if page.locator('aside.sidebar').count():
                    expect(page.locator('aside').get_by_text('AI worker connected')).to_be_visible(timeout=35000)
                    steps.append({'stage': 'installed-webview-authenticated-worker', 'result': 'PASS'})
                    return proc, browser, page
            time.sleep(.3)
        raise AssertionError('Installed desktop CDP target did not contain the actual Tauri UI')
    except Exception:
        if proc is not None and proc.poll() is None:
            subprocess.run(['taskkill', '/PID', str(proc.pid), '/T', '/F'],capture_output=True)
        raise


def stop(proc, browser, steps):
    close_window(proc.pid)
    try:
        proc.wait(timeout=20)
    except subprocess.TimeoutExpired:
        subprocess.run(['taskkill', '/PID', str(proc.pid), '/T', '/F'],capture_output=True)
        raise AssertionError('Desktop did not close gracefully after WM_CLOSE')
    steps.append({'stage': 'installed-webview-graceful-shutdown', 'result': 'PASS'})
    try:
        browser.close()
    except Exception:
        pass


def navigate_assessments(page):
    page.locator('aside.sidebar button').filter(has_text='Assessments').click()
    expect(page.get_by_role('heading', name='Timed assessments')).to_be_visible(timeout=20000)


def create_quiz(page, title, duration_minutes=1):
    navigate_assessments(page)
    page.get_by_role('button', name=re.compile(r'Create assessment')).click()
    page.locator('input[placeholder="Title"]').fill(title)
    page.locator('label').filter(has_text='Duration (minutes)').locator('input').fill(str(duration_minutes))
    page.locator('label').filter(has_text='Penalty per wrong answer').locator('input').fill('0.5')
    page.locator('label').filter(has_text='Pass cutoff').locator('input').fill('75')
    questions = [
        {'id': 'w1', 'stem': 'RC3 synthetic choice question', 'kind': 'single', 'section': 'Logic',
         'options': [{'label': 'A', 'text': 'Wrong option'}, {'label': 'B', 'text': 'Correct choice'}],
         'correct': 'B', 'points': 1},
        {'id': 'w2', 'stem': 'RC3 synthetic numerical question', 'kind': 'numerical', 'section': 'Quant',
         'correct': 4, 'tolerance': 0, 'points': 1}
    ]
    page.locator('textarea').fill(json.dumps(questions))
    page.get_by_role('button', name='Save assessment').click()
    card = page.locator('section.panel').filter(has=page.get_by_role('heading', name=title))
    expect(card).to_be_visible(timeout=20000)
    return card


def begin(page, title):
    card = page.locator('section.panel').filter(has=page.get_by_role('heading', name=title))
    card.get_by_role('button', name=re.compile('Begin assessment')).click()
    expect(page.get_by_role('heading', name=title)).to_be_visible(timeout=20000)
    expect(page.locator('.question-title')).to_contain_text('synthetic choice', timeout=20000)


def db_row(path, title):
    with sqlite3.connect(path, timeout=15) as db:
        row = db.execute('SELECT a.id,d.started,d.answers_json,d.review_json FROM assessments a '
                         'LEFT JOIN assessment_drafts d ON d.assessment_id=a.id '
                         'WHERE a.title=? ORDER BY a.created DESC LIMIT 1', (title,)).fetchone()
    if not row:
        raise AssertionError('UI-created assessment was not found in real SQLite database')
    return row


def check_receipt(path, title, expected=1):
    with sqlite3.connect(path, timeout=15) as db:
        count = db.execute('SELECT count(*) FROM attempts t JOIN assessments a ON a.id=t.assessment_id '
                           'WHERE a.title=?', (title,)).fetchone()[0]
        schema = db.execute('PRAGMA user_version').fetchone()[0]
    if count != expected:
        raise AssertionError(f'Expected {expected} persisted attempt, found {count}')
    if schema != 7:
        raise AssertionError(f'Installed SQLite schema is {schema}, expected v7')


def run_ui(executable, report):
    steps = []
    report_path = Path(report)
    evidence = {'test_id': 'RC3-WIN-ASSESSMENT-UI-01', 'test_type': 'installed-Windows-WebView2-CDP',
                'app_version': APP_VERSION, 'steps': steps, 'status': 'NOT RUN',
                'note': 'Synthetic local-only assessment; remote debugging enabled only in isolated CI process.'}
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='rc3-ui-') as root, sync_playwright() as playwright:
        root = Path(root)
        data, profile, logs = root / 'data', root / 'webview-profile', root / 'logs'
        data.mkdir(); profile.mkdir(); logs.mkdir()
        active = None
        title = 'RC3 installed assessment recovery'
        try:
            active = launch(executable, data, profile, logs, playwright, steps)
            proc, browser, page = active
            card = create_quiz(page, title)
            steps.append({'stage': 'created-strict-quiz-through-installed-UI', 'result': 'PASS'})
            begin(page, title)
            page.locator('label.choice').filter(has_text='Correct choice').click()
            expect(page.get_by_text('Answers saved locally')).to_be_visible(timeout=15000)
            page.get_by_role('button', name=re.compile('Next')).click()
            page.locator('input[placeholder="Enter a number"]').fill('4')
            page.get_by_role('button', name=re.compile('Mark for review')).click()
            time.sleep(1.1)  # Assert persisted DB values below; this is not a readiness substitute.
            row = db_row(data / 'studio.sqlite3', title)
            saved_at = row[1]
            if not saved_at or json.loads(row[2]) != {'w1':'B','w2':'4'} or 'w2' not in json.loads(row[3]):
                raise AssertionError('Installed UI autosave did not persist both answers and review state')
            steps.append({'stage': 'real-webview-autosave-to-sqlite', 'result': 'PASS'})
            stop(proc, browser, steps); active = None

            active = launch(executable, data, profile, logs, playwright, steps)
            proc, browser, page = active
            navigate_assessments(page)
            begin(page, title)
            expect(page.get_by_text('Restored locally saved answers')).to_be_visible(timeout=15000)
            expect(page.locator('label.choice').filter(has_text='Correct choice').locator('input')).to_be_checked()
            page.get_by_role('button', name=re.compile('Next')).click()
            expect(page.locator('input[placeholder="Enter a number"]')).to_have_value('4')
            assert db_row(data/'studio.sqlite3', title)[1] == saved_at, 'Server reset original assessment deadline'
            steps.append({'stage': 'installed-UI-relaunch-recovers-answers-and-original-deadline', 'result': 'PASS'})
            page.once('dialog', lambda dialog: dialog.accept())
            page.get_by_role('button', name='Submit assessment').click()
            expect(page.get_by_text('Your results')).to_be_visible(timeout=20000)
            expect(page.get_by_text('Cutoff reached')).to_be_visible(timeout=10000)
            check_receipt(data/'studio.sqlite3', title)
            steps.append({'stage': 'installed-UI-submission-scoring-and-exactly-once-receipt', 'result': 'PASS'})
            stop(proc, browser, steps); active = None

            active = launch(executable, data, profile, logs, playwright, steps)
            proc, browser, page = active
            navigate_assessments(page)
            card = page.locator('section.panel').filter(has=page.get_by_role('heading', name=title))
            card.get_by_role('button', name='Review last result').click()
            expect(page.get_by_text('Your results')).to_be_visible(timeout=20000)
            expect(page.get_by_text('Cutoff reached')).to_be_visible()
            check_receipt(data/'studio.sqlite3', title)
            steps.append({'stage': 'installed-UI-relaunch-recovers-completed-result', 'result': 'PASS'})
            stop(proc, browser, steps); active = None
            evidence['status'] = 'PASS'
        except Exception as exc:
            evidence['status'] = 'FAIL'
            evidence['failure_category'] = type(exc).__name__
            evidence['failure_message'] = str(exc)[:260]  # Must not contain real user data or credentials.
            if active is not None:
                proc, browser, page = active
                try:
                    page.screenshot(path=str(report_path.parent/'rc3-synthetic-assessment-failure.png'), timeout=3500)
                    evidence['synthetic_screenshot'] = str(report_path.parent/'rc3-synthetic-assessment-failure.png')
                except Exception:
                    pass
                try:
                    stop(proc,browser,steps)
                except Exception:
                    if proc.poll() is None:
                        subprocess.run(['taskkill','/PID',str(proc.pid),'/T','/F'],capture_output=True)
            raise
        finally:
            report_path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False)+'\n',encoding='utf-8')
    print('RC3 installed WebView2 assessment acceptance:', evidence['status'])
    return 0


if __name__ == '__main__':
    if sys.platform != 'win32':
        raise SystemExit('BLOCKED: this test requires the real installed Windows desktop and WebView2 runtime')
    cli = argparse.ArgumentParser()
    cli.add_argument('--installed-exe', type=Path, required=True)
    cli.add_argument('--report', type=Path, required=True)
    args = cli.parse_args()
    if not args.installed_exe.is_file():
        raise SystemExit('Installed desktop binary is missing; cannot run UI acceptance')
    sys.exit(run_ui(args.installed_exe, args.report))
