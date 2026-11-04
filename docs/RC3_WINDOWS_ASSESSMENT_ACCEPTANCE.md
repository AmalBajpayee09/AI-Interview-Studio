# RC3 real installed Windows WebView2 assessment acceptance

Test ID: `RC3-WIN-ASSESSMENT-UI-01`.
Source: `scripts/rc3-installed-webview-assessment.py`, invoked by `.github/workflows/windows-release.yml` against the **installed** Tauri NSIS executable on an ephemeral GitHub Windows runner. The test must fail, not skip, if WebView2 CDP, an installed executable or authenticated worker is missing.

The harness sets `WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=<loopback-port>` on the **test process only**. It uses Playwright's `connect_over_cdp()` to drive the actual installed WebView2 renderer. No test-only remote-debugging port is enabled in the production executable. Because CDP controls a token-bearing renderer, this must only run in an isolated CI account; do not turn it on in ordinary user sessions.

## Acceptance procedure

1. Install RC3 NSIS to an isolated Windows path; launch actual installed desktop and authenticated bundled worker.
2. Via WebView2 UI click Assessments → Create assessment. Submit two synthetic questions with scoring/section/cutoff rules.
3. Start assessment via UI; choose an answer, navigate to numerical question, enter value, mark for review.
4. Wait for autosave confirmation and independently inspect isolated SQLite data to verify answers/review are persisted.
5. Gracefully close the actual desktop via WM_CLOSE. Relaunch using identical isolated data. Recover original start timestamp, answers, review state and deadline.
6. Manually submit through UI, accept the confirmation dialog, verify cutoff result and exactly one persisted attempt receipt.
7. Close/relaunch again; click Review last result; confirm same score and receipt without creating duplicate attempts.
8. Close gracefully, uninstall the synthetic test installation. CI publishes a redacted JSON evidence record; on failure an optional screenshot contains only synthetic assessment data.

Additional deadline-expiration, Windows clock/timezone change, process crash mid-autosave, sleep/wake, browser profile failure, accessibility, and multi-monitor acceptance are **not** covered by this first UI scenario and must remain separate gates.

The previous RC2 Windows lifecycle test [#41718783390](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41718783390) passed install/upgrade/crash-recovery/retention, **not** this WebView2 test. The RC3 UI test's status depends strictly on its completed exact-commit CI step, not on the presence of this harness or API-only tests.
