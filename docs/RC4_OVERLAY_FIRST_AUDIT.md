# Overlay-first product direction — engineering audit (RC4 foundation)

## Source and existing behavior

Baseline: `feature/v1.0-rc3-production-acceptance` at `528236b4d74e0c8ba3631dd400cbe730957d4bed`.
New branch: `feature/overlay-first-foundation-rc4`; production `main` untouched.
The existing Tauri application launched a single 1320×860 decorated `main` window. `apps/desktop/src/App.tsx` initialized `page='dashboard'`; `set_compact` only resized that same window, and its `WindowEvent::Destroyed` stopped the worker. No tray or global shortcut plugin was installed.

## Existing work preserved

- Tauri 2/Rust native packaged Python-worker supervisor, authenticated loopback readiness, bounded restart/recovery, diagnostics and resource packaging.
- React/TypeScript dashboard and all assessment, coding, SQL, resume, live audio, session history, settings and analytics pages unchanged as the secondary workspace.
- FastAPI/Python providers (Ollama, opt-in cloud), real Linux Ollama tests, Docker isolation, privacy controls and SQLite migration v7.
- Exact RC3 Windows WebView2 assessment acceptance and native NSIS installation/upgrade evidence, run #41823829065.

## Public interaction patterns reviewed (no code/assets reused)

- Final Round AI: collapsible live feed, speaking cues, configurable shortcuts and clear generation states — https://docs.finalroundai.com/docs/live-copilot/using-copilot
- ParakeetAI: call sessions, context, prepared documents and streaming — https://www.parakeet-ai.com/
- Ofradr: desktop overlay and local-model availability — https://www.ofradr.com/invisible-ai-assistant
- LockedIn AI: user-adjustable desktop overlay controls and multi-display workflows; product claims of invisibility are *not* reproduced — https://www.lockedinai.com/support
- OphyAI: compact overlay versus separate practice/coding areas — https://ophyai.com/ai-interview-assistant
- Ghotly AI: Windows small panel, configurable shortcuts, resume context and local credential protection — https://www.ghotlyai.in/
- Chiku AI: glanceable spoken answers and selective visual context — https://www.chiku-ai.in/
- Product pages are descriptions of their products, not independent proof of platform compatibility or capture exclusion.

## Target architecture: smallest safe change

`main` becomes a 470×590 resizable, OS-decorated, always-on-top overlay; its tray icon and a native global shortcut survive hiding the window. A separate `workspace` WebView opens the existing untouched React `App` at `?workspace=1`. A shared Rust worker supervisor persists for the process lifetime; closing either window must not kill the worker. Native explicit Quit stops all owned worker processes. Both windows use the existing same authenticated backend and SQLite session data.

Added `Overlay.tsx` and isolated CSS: Compact, Teleprompter, Split desk and Q&A Feed, manually entered practice questions, provider/mode controls, genuine existing SSE stream and cancellation, local session history and restoration. New UI never silently activates microphone, cloud inference, screenshot capture or raw-audio storage.

A small supported set of global hotkeys can be re-bound; failed registration surfaces an error and attempts to retain the previous mapping. Default: Ctrl+Alt+Shift+O. OS title bar allows mouse move/resize; skip-taskbar is a user-experience choice, **not** process hiding or screen-capture evasion. Tray remains the visible process control.

## Status and unimplemented behaviors

- Code path implemented, Rust native build and installed acceptance pending until exact-commit Windows CI success.
- Full free-form shortcut editing, persistent startup preferences, click-through toggle, emergency-hide, screen selection, speaker diarization, and overlay-driven audio devices are NOT implemented in this foundation.
- Multi-monitor placement, mixed DPI, global shortcut behavior against conflicting third-party software and all screen-capture modes require actual device tests.
- No universal capture-exclusion promise. Respect each platform's assistance/recording rules. Do not implement monitoring or proctoring bypass.

## Acceptance and regression gates

`PYTHONPATH=services/ai_worker python -m pytest services/ai_worker/tests -q`; `npm ci && npm run build` in `apps/desktop`; `cargo check && cargo test` in `apps/desktop/src-tauri`; `.github/workflows/windows-release.yml` on the exact RC4 SHA.

`scripts/rc4-windows-acceptance.ps1`: checks SHA-256-verified RC3 predecessor, Unicode installation path, session persistence through upgrade, authenticated worker restart and data retention on uninstall. For RC4, closing the window must preserve the resident process; test cleanup is explicitly marked forced here. `scripts/rc4-overlay-acceptance.py`: tests actual installed overlay, tray/shortcut native state, four layouts, SQLite session, workspace, system-global hide/show keys, closing overlay while worker lives, and explicit Exit cleanup.

No result is considered PASS before its exact-commit CI step concludes successfully.
