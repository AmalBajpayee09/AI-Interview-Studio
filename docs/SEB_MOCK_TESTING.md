# Controlled mock-exam compatibility testing

The uploaded `seb-win-refactoring-3.10.2.zip` was read as a source reference **without running, altering, patching, or repackaging it**. Its README identifies a Windows 10 1803+ prerequisite and its LICENSE.txt identifies the Mozilla Public License 2.0. There are 1,677 archive entries. The archive is not copied into the Studio source distribution.

To test authorized mock practice with a secure browser:

1. Set up a **separate test Windows VM** without real candidate or organizational data.
2. Obtain explicit approval from the mock-exam organizer / administrator for permitted assistant tools, screen sharing and external windows.
3. Use the officially supported SEB test configuration and documented permitted-app policy. Do not change OS security policy, proctoring, process monitoring, lock-down, display-capture or deny-list behavior to conceal the assistant.
4. Run the Studio app outside the secure browser and record whether the organizer-approved configuration allows it. If disallowed, treat this as an intended compatibility limit.
5. Use `scripts/mock-capture-test.ps1` to record *operator-observed* overlay visibility in ordinary screen-sharing modes, with consent from all participants. Compare Zoom and Google Meet test calls manually. The script does not automate bypasses, alter process visibility, suppress detection or hide overlays.
6. Review the CSV test log with the organizer and document supported configurations before use.

An ordinary visible, on-top helper window may appear or disappear differently depending on which **window or display** the meeting application shares. The app does not guarantee exclusion from screen capture or invisibility to remote viewers. Never rely on such behavior during an exam or remote assessment.
