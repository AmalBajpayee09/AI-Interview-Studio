# Publish AI Interview Studio v0.4.0 into this repository

This GitHub repository is **not** the complete application until the verified source ZIP is imported. The source ZIP is provided in the ChatGPT conversation and cannot be fetched from a public GitHub URL because it has not yet been uploaded. The GitHub connector can edit repository text files but cannot unpack and upload the binary ZIP as a repository tree.

## One-command source import on Windows

Download and extract `AI-Interview-Studio-Source-v0.4.0.zip`, open Windows PowerShell in its extracted `AI-Interview-Studio` folder, and run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\\scripts\\publish-github.ps1
```

This imports the *actual source* (including hidden configuration folders), excludes ignored generated content, creates a dedicated `import/v0.4.0` branch, generates a real `package-lock.json`, executes `npm ci` and `npm run build`, and pushes the branch. The script exits without pushing if dependency setup or the frontend build fails. The repository must be reachable and Git authentication must already be configured.

Open a pull request from that import branch into `main`. [Windows CI workflow](.github/workflows/windows-release.yml) then runs Python tests, builds the React UI, checks Rust, packages the Python worker, bundles an NSIS installer, validates that the installer exists and uploads artifacts when the build gets that far.

## Evidence from the first actual Windows run

[Run #41346727566](https://github.com/AmalBajpayee09/AI-Interview-Studio/actions/runs/41346727566) started on a GitHub Windows runner and failed at the required source check (`apps/desktop/package.json` missing). Subsequent build jobs were skipped. **This is a genuine CI failure and is not a successful Windows application build.**

Do not declare a release until actual installer artifacts exist and have passed clean-machine install, launch, upgrade, uninstall and recovery verification. This repository is public: ensure no personal documents, API keys, transcripts or private databases are committed.
