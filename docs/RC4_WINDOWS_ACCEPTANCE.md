# RC4 installed Windows overlay acceptance protocol

**Commit:** use the exact SHA of `feature/overlay-first-foundation-rc4` from the GitHub Actions run.
**Version:** `1.0.0-rc.4`. **Previous verified installer:** RC3 SHA-256 `3EFBDA565ADE83355E9EBB09451AEB9E192DE0D87A50E4F57DDE7C054BDC2932`, CI run #41823829065.
**Security:** temporary CDP debug port only inside the isolated CI test process, removed after launch; no production debugging defaults. No screen-capture exclusion or stealth behavior.

## Steps tested by automation

1. Build React with locked npm deps; compile/test Rust and Python; package bundled worker and NSIS.
2. Verify source ZIP integrity with exact Git SHA manifest and verify NSIS SHA-256.
3. Install predecessor RC3 using its authentic artifact, verify checksum and prior database schema; save a synthetic session; shut down old desktop.
4. Upgrade in place to RC4 and assert session preserved and worker authenticated; intentionally crash worker tree, require bounded recovery.
5. Close RC4 overlay without terminating app or worker. Script uses forced process termination only to isolate the next test; **forced test cleanup is not graceful-quit acceptance**.
6. Fresh-install RC4 separately, launch actual Tauri WebView2 through test-only CDP, verify compact overlay and no initial dashboard.
7. Check native tray/shortcut registration, authenticated worker, four layouts, persistent session, secondary workspace opening/closing, real OS shortcut hide/show and reconfiguration, close-to-tray, explicit exit with worker shutdown.
8. Uninstall test application and record data-retention behavior.
9. Review emitted JSON evidence, Python JUnit, source ZIP checksum and NSIS SHA-256.

## Windows manual checks still required

Real tray menu mouse click and notification-area presence in Explorer, multi-monitor moves and DPI scaling, taskbar/alt-tab behavior, shortcut collisions with other apps, keyboard focus non-interference and all Windows screen-capture workflows. Windows Server GitHub Actions is not equivalent to the user's physical laptop.

## Reproduction

Use `feature/overlay-first-foundation-rc4` GitHub Actions → Windows RC4 workflow (automatic on branch commit). After downloading the exact-commit installer, compare its SHA-256 with the workflow output. Test on a throwaway Windows 11 machine. Start and observe the small overlay; use Ctrl+Alt+Shift+O to hide/show, close with the X to keep it resident, right-click the tray icon for Workspace, Settings and Exit. Open workspace and confirm historical assessments still work.

**Status until final runner result:** NOT VERIFIED. Failure of any mandatory stage keeps RC4 a source checkpoint and the installer unreleased.
