param([string]$Path)
if (Test-Path $Path) {
 Get-Content $Path | ForEach-Object {
   $line=$_.Trim()
   if ($line -and -not $line.StartsWith('#') -and $line.Contains('=')) {
     $split=$line.Split('=',2);$key=$split[0].Trim();$value=$split[1].Trim().Trim('"').Trim("'")
     if ($key -match '^[A-Z_][A-Z0-9_]*$') { [Environment]::SetEnvironmentVariable($key,$value,'Process') }
   }
 }
}
