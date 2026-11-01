Write-Host 'Operating system:'; Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,FreePhysicalMemory
Write-Host 'Hardware:'; Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory,NumberOfLogicalProcessors
foreach ($cmd in @('py','node','npm','rustc','cargo','ollama')) { try { Get-Command $cmd -ErrorAction Stop | Select-Object Name,Source } catch { Write-Warning "$cmd not found" } }
Write-Host 'Worker reachability:'
try { Invoke-RestMethod 'http://127.0.0.1:8765/api/health' | ConvertTo-Json } catch { Write-Warning 'Worker not responding' }
Write-Host 'Ollama:'
try { Invoke-RestMethod 'http://127.0.0.1:11434/api/tags' | ConvertTo-Json -Depth 3 } catch { Write-Warning 'Ollama not responding' }
