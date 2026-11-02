$Root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Zip=Join-Path (Split-Path $Root -Parent) 'AI-Interview-Studio-Source-v0.5.0.zip'
if (Test-Path $Zip) { Remove-Item $Zip }
# Do not include virtualenv, personal data, packages or credentials.
$Temp=Join-Path $env:TEMP ('studio-source-'+[guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force $Temp | Out-Null
try {
  robocopy $Root (Join-Path $Temp 'AI-Interview-Studio') /E /XD .git .venv node_modules dist build target __pycache__ .pytest_cache resources /XF .env *.db *.sqlite3 *.log *.pyc | Out-Null
  Compress-Archive -Path (Join-Path $Temp 'AI-Interview-Studio') -DestinationPath $Zip
} finally { Remove-Item $Temp -Recurse -Force }
Write-Host $Zip
