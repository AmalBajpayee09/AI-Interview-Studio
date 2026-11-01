$ErrorActionPreference='Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
. "$PSScriptRoot\load-env.ps1" -Path "$Root\.env"
$Worker="$Root\services\ai_worker"
$Python="$Worker\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) { throw 'Worker virtual environment missing. Run scripts/setup.ps1.' }
Push-Location $Worker
try {
  & $Python -m pip install 'pyinstaller==6.11.1'
  if ($LASTEXITCODE -ne 0) { throw 'PyInstaller installation failed' }
  & $Python -m PyInstaller --noconfirm --clean --onefile --name ai-studio-worker --paths . --collect-submodules app --collect-data app --hidden-import multipart run_worker.py
  if ($LASTEXITCODE -ne 0) { throw 'Worker packaging failed' }
} finally { Pop-Location }
$Resources="$Root\apps\desktop\src-tauri\resources"
New-Item -ItemType Directory -Force $Resources | Out-Null
Copy-Item "$Worker\dist\ai-studio-worker.exe" "$Resources\ai-studio-worker.exe" -Force
Push-Location "$Root\apps\desktop"
try {
  npm run build
  if ($LASTEXITCODE -ne 0) { throw 'Frontend production build failed' }
  npm run tauri build -- --config src-tauri/tauri.prod.conf.json --bundles nsis
  if ($LASTEXITCODE -ne 0) { throw 'Native Windows build failed' }
} finally { Pop-Location }
Write-Host "NSIS output: $Root\apps\desktop\src-tauri\target\release\bundle\nsis"
