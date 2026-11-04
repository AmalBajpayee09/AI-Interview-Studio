# RC4 overlay-first foundation — release and evidence gate

- Starting verified RC3 commit: `528236b4d74e0c8ba3631dd400cbe730957d4bed`.
- Current development branch: `feature/overlay-first-foundation-rc4`; exact final commit from completed CI only.
- Product: Tauri 2 / Rust, React 19 / TypeScript / Vite, packaged Python/FastAPI, SQLite. No major architecture change.
- Version: `1.0.0-rc.4`.
- Implementation: native tray, default overlay-first window, workspace as secondary WebView, native global shortcut with three conflict-checked preset mappings, resident worker shutdown ownership, four overlay layouts on shared session/stream API.
- Existing assessment and practice workspace modules preserved.
- Requirement matrix: 161 preexisting IDs + nine RC4-specific requirements = **170**; all nine are partial/blocked until actual Windows evidence. Historical statuses retained.
- Previous RC3 Windows run #41823829065 PASSED, but does not certify RC4.
- Local baseline against extracted RC3 source: 121 passed, 14 skipped (no native toolchains; before RC4 changes).
- Post-change Windows CI and artifact SHA-256 are required and must be appended only after actual successful run.
- No cloud/API credentials embedded, no default microphone activation, no proctoring or screen-capture bypass.
- Remaining: full shortcut action map, capture/privacy preferences, click-through, Windows display/DPI, actual overlay audio/STT, Windows genuine model streaming/cancellation, Docker Desktop, target laptop performance and security review.

**Decision at code commit:** development milestone pending native Windows acceptance; not production-ready.
