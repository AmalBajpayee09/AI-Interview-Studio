# GitHub import status and next build

Repository: https://github.com/AmalBajpayee09/AI-Interview-Studio

The repository was initialized and a strict Windows build workflow was committed on its `main` branch. The source ZIP cannot be unpacked and published directly through the GitHub tool connection's available file operations; this is a data-transfer limitation, not a claim that the source was uploaded.

This release contains `scripts/publish-github.ps1`. From the extracted source on a networked Windows PC with Git, Node and GitHub credentials, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\publish-github.ps1
```

The script clones the repository, imports the source including dotfiles, preserves the committed Windows workflow, creates the *real* frontend lockfile using npm, builds the React frontend and pushes a dedicated `import/v0.4.0` branch. Review the branch and open a PR to `main`. The workflow triggers automatically on the PR; it must pass before merge. The workflow also triggers on pushes to `main` and version tags.

If the GitHub account uses 2FA, an HTTPS Git credential manager or SSH remote must be configured. Never paste tokens in the command line or source. If a build fails, inspect the exact GitHub Actions log and correct the first error. A passing GitHub Actions build is not a substitute for clean-machine Windows install/uninstall validation.
