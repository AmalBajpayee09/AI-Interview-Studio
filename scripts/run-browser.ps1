$ErrorActionPreference='Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
. "$PSScriptRoot\load-env.ps1" -Path "$Root\.env"
$Python="$Root\services\ai_worker\.venv\Scripts\python.exe"
$Worker="$Root\services\ai_worker"
if (-not (Test-Path $Python)) { throw 'Install Python worker first using WINDOWS_SETUP.md' }
$process=Start-Process -FilePath $Python -ArgumentList 'run_worker.py' -WorkingDirectory $Worker -PassThru -NoNewWindow
try {
  $ready=$false
  for($i=0;$i -lt 30;$i++){
    try { $status=Invoke-RestMethod 'http://127.0.0.1:8765/api/health' -TimeoutSec 1; if($status.status -eq 'ok') { $ready=$true;break } } catch { Start-Sleep -Milliseconds 500 }
  }
  if(-not $ready) { throw 'Worker did not start, review Python package installation or port conflicts.' }
  Start-Process 'http://127.0.0.1:8765'
  Write-Host 'AI Interview Studio companion running. Close this PowerShell window to stop worker.'
  Wait-Process -Id $process.Id
} finally {
  if ($process -and -not $process.HasExited) { Stop-Process -Id $process.Id -ErrorAction SilentlyContinue }
}
