# Transparent manual capture compatibility record. Not an evasion tool.
$Root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Path=Join-Path $Root 'capture-observations.csv'
$testApp=Read-Host 'Meeting app / capture tool (e.g. Zoom mock call)'
$mode=Read-Host 'Capture mode (window or desktop)'
$visible=Read-Host 'Was the visible Studio helper shown to the remote observer? yes/no/unknown'
$notes=Read-Host 'Test notes (no credentials or sensitive material)'
[pscustomobject]@{UTC=(Get-Date).ToUniversalTime().ToString('o');Application=$testApp;CaptureMode=$mode;Visible=$visible;Notes=$notes} | Export-Csv -Path $Path -NoTypeInformation -Append
Write-Host "Observation recorded at $Path. This does not change capture or browser behavior."
