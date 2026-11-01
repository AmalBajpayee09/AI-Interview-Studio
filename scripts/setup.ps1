$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Write-Host 'AI Interview Studio | Initial setup'
Write-Host 'Checking: Python launcher, Node/npm and Rust (for Windows desktop).'
py -3.11 --version
node --version
npm --version
rustc --version
cargo --version
if (-not (Test-Path "$Root\.env")) { Copy-Item "$Root\.env.example" "$Root\.env" }
Push-Location "$Root\services\ai_worker"
try {
  py -3.11 -m venv .venv
  & .\.venv\Scripts\python.exe -m pip install --upgrade pip
  & .\.venv\Scripts\python.exe -m pip install -r requirements.txt
} finally { Pop-Location }
Push-Location "$Root\apps\desktop"
try { npm install } finally { Pop-Location }
Write-Host 'Setup complete. Open .env to configure optional local/cloud inference, then run .\scripts\dev.ps1'
