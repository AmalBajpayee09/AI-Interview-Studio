# Import the full v0.3.0 project

The actual project source is distributed in `AI-Interview-Studio-Source-v0.3.0.zip` in the ChatGPT conversation. This GitHub repository currently contains only initialization documentation and a Windows CI workflow, **not** the complete source project. Do not start a release build until the full source is committed.

## Import on Windows (PowerShell)

1. Download the ZIP from the ChatGPT conversation.
2. Extract it. The ZIP has a top-level `AI-Interview-Studio` folder.
3. Open PowerShell and run the following (replace the two paths):

```powershell
$source = 'C:\\Users\\YOUR_NAME\\Downloads\\AI-Interview-Studio'
$repo = 'C:\\Users\\YOUR_NAME\\Documents\\AI-Interview-Studio-Repo'
git clone https://github.com/AmalBajpayee09/AI-Interview-Studio.git $repo
Get-ChildItem -LiteralPath $source -Force | Copy-Item -Destination $repo -Recurse -Force
Set-Location $repo
# Keep this repository's stricter Windows release workflow:
git restore .github/workflows/windows-release.yml
git add -A
git commit -m 'Import AI Interview Studio v0.3.0 source'
git push origin main
```

The input ZIP does **not** contain an npm package-lock.json. From the repository root run:

```powershell
Set-Location apps/desktop
npm install --package-lock-only
Set-Location ../..
git add apps/desktop/package-lock.json
git commit -m 'Lock frontend dependencies'
git push origin main
```

Once the full source and lockfile are committed, use GitHub Actions → **Windows native build and installer** → **Run workflow**. Inspect the run logs and download the `windows-build-artifacts-and-logs` artifact only if the build succeeds. A successful compile does not substitute for clean-machine install, upgrade and uninstall tests.

This document is not an installer and does not assert that GitHub Actions has run.
