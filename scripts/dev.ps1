$ErrorActionPreference='Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
. "$PSScriptRoot\load-env.ps1" -Path "$Root\.env"
$Python="$Root\services\ai_worker\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) { throw 'Python virtual environment missing; run .\scripts\setup.ps1 first.' }
$worker=Start-Process -FilePath $Python -ArgumentList '-m','uvicorn','app.main:app','--host','127.0.0.1','--port','8765' -WorkingDirectory "$Root\services\ai_worker" -PassThru -NoNewWindow
try {
  Start-Sleep -Seconds 2
  Push-Location "$Root\apps\desktop"
  try { npm run tauri dev } finally { Pop-Location }
} finally {
  if ($worker -and -not $worker.HasExited) { Stop-Process -Id $worker.Id -ErrorAction SilentlyContinue }
}
