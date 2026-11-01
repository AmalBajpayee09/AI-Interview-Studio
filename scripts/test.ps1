$ErrorActionPreference='Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location "$Root\services\ai_worker"
try { & .\.venv\Scripts\python.exe -m pytest -q; if ($LASTEXITCODE -ne 0) { throw 'Python tests failed' } } finally { Pop-Location }
Push-Location "$Root\apps\desktop"
try { npm run build; if ($LASTEXITCODE -ne 0) { throw 'Frontend build failed' } } finally { Pop-Location }
Push-Location "$Root\apps\desktop\src-tauri"
try { cargo test; if ($LASTEXITCODE -ne 0) { throw 'Rust tests failed' } } finally { Pop-Location }
