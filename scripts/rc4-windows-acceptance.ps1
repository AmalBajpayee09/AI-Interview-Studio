# v1.0 RC4 Windows acceptance. Run only on an isolated GitHub Windows runner.
# Real NSIS upgrade and subprocess checks; no model, Docker Desktop or audio acceptance implied.
param(
  [Parameter(Mandatory=$true)][string]$CurrentInstaller,
  [string]$Repository='AmalBajpayee09/AI-Interview-Studio',
  [string]$PriorRun='41823829065'
)
$ErrorActionPreference='Stop'
$oldVersion='1.0.0-rc.3'
$newVersion='1.0.0-rc.4'
$dest=Join-Path $env:RUNNER_TEMP 'AI Studio RC4 安装 test folder'
$download=Join-Path $env:RUNNER_TEMP 'AIStudio RC2 predecessor artifact'
$env:STUDIO_DATA_DIR=Join-Path $env:RUNNER_TEMP 'AI Studio RC4 durable user data'
$logDir=Join-Path $env:LOCALAPPDATA 'com.interviewstudio.desktop/logs'
$marker=Join-Path $logDir 'worker-readiness.json'
$evidence=Join-Path $env:RUNNER_TEMP 'rc4-windows-acceptance.json'
$steps=[System.Collections.Generic.List[object]]::new()
function Record([string]$stage,[string]$outcome,[object]$details) {
  $script:steps.Add(@{stage=$stage;outcome=$outcome;details=$details;at=[DateTimeOffset]::UtcNow.ToString('o')})
  Write-Host "RC4 acceptance [$stage]: $outcome"
}
function Require-File([string]$path) {if(-not (Test-Path -LiteralPath $path)){throw "Missing expected file: $path"}}
function Install-NSIS([string]$installer,[string]$stage) {
  Require-File $installer
  $result=Start-Process -FilePath $installer -ArgumentList @('/S',"/D=$dest") -Wait -PassThru
  if($result.ExitCode -ne 0){throw "$stage NSIS exited with code $($result.ExitCode)"}
  $desktop=@(Get-ChildItem -LiteralPath $dest -Filter 'ai-interview-studio.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1)
  $worker=@(Get-ChildItem -LiteralPath $dest -Filter 'ai-studio-worker.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1)
  if($desktop.Count -ne 1 -or $worker.Count -ne 1){throw "$stage installed desktop or worker executable missing"}
  Record $stage 'PASS' @{installer_file=[IO.Path]::GetFileName($installer);desktop_present=$true;worker_present=$true}
  return $desktop[0].FullName
}
function Wait-Ready([System.Diagnostics.Process]$app,[string]$expected,[int]$timeoutSeconds=85) {
  $sw=[System.Diagnostics.Stopwatch]::StartNew()
  while($sw.Elapsed.TotalSeconds -lt $timeoutSeconds) {
    $app.Refresh()
    if($app.HasExited){throw "Desktop exited before readiness; exit code $($app.ExitCode)"}
    if(Test-Path -LiteralPath $marker) {
      try {
        $state=Get-Content -LiteralPath $marker -Raw | ConvertFrom-Json
        if($state.authenticated -eq $true -and $state.stage -eq 'ready' -and $state.app_version -eq $expected){
          $workerPid=[int]$state.worker_pid
          if($workerPid -gt 0 -and (Get-Process -Id $workerPid -ErrorAction SilentlyContinue)){
            return @{pid=$workerPid;startup_ms=$sw.ElapsedMilliseconds;worker_ready_ms=$state.startup_ms}
          }
        }
      }catch { # Partial marker replacement is normal; retry boundedly.
        Start-Sleep -Milliseconds 100
      }
    }
    Start-Sleep -Milliseconds 250
  }
  throw "Installed desktop did not report authenticated worker readiness for $expected"
}
function Close-And-Assert([System.Diagnostics.Process]$app,[int]$workerPid,[string]$stage) {
  $app.Refresh()
  if(-not $app.HasExited) {
    $closed=$app.CloseMainWindow()
    if($stage -ne 'previous-version-shutdown') {
      # RC4 overlays hide on close. The process and authenticated worker MUST stay
      # resident; explicit Exit is tested separately via installed WebView2 UI.
      Start-Sleep -Milliseconds 700
      $app.Refresh()
      if($app.HasExited){throw "$stage: Closing overlay incorrectly exited the application"}
      if(-not (Get-Process -Id $workerPid -ErrorAction SilentlyContinue)){throw "$stage: Closing overlay killed worker"}
      Record 'overlay-close-retains-background-worker' 'PASS' @{pid=$app.Id;worker_pid=$workerPid}
      # Forced teardown here is test isolation ONLY, not a successful graceful quit.
      & taskkill.exe /PID $app.Id /T /F | Out-Null
      $app.WaitForExit(15000) | Out-Null
      Record $stage 'PASS' @{resident_overlay_close=$true;forced_test_teardown=$true;native_quit_verified_here=$false}
      return
    }
    if(-not $app.WaitForExit(15000)){
      $app.Kill($true);$app.WaitForExit()
      throw "$stage desktop required forced termination; graceful shutdown NOT verified (CloseMainWindow=$closed)"
    }
  }
  $sw=[System.Diagnostics.Stopwatch]::StartNew()
  while($sw.Elapsed.TotalSeconds -lt 15 -and (Get-Process -Id $workerPid -ErrorAction SilentlyContinue)){
    Start-Sleep -Milliseconds 250
  }
  if(Get-Process -Id $workerPid -ErrorAction SilentlyContinue) {
    & taskkill.exe /PID $workerPid /T /F | Out-Null
    throw "$stage left an orphaned worker after desktop exit"
  }
  Record $stage 'PASS' @{graceful_desktop_shutdown=$true;worker_exited=$true;worker_pid=$workerPid}
}
function Assert-Database([string]$stage,[int]$minimumSchema=7) {
  $file=Join-Path $env:STUDIO_DATA_DIR 'studio.sqlite3'
  Require-File $file
  $env:RC4_VERIFY_DB=$file
  $env:RC4_MIN_SCHEMA=[string]$minimumSchema
  & py -3.11 -c "import sqlite3,os; c=sqlite3.connect(os.environ['RC4_VERIFY_DB']); version=c.execute('PRAGMA user_version').fetchone()[0]; minimum=int(os.environ['RC4_MIN_SCHEMA']); assert version>=minimum,(version,minimum,'schema not migrated'); c.close()"
  if($LASTEXITCODE -ne 0){throw "$stage SQLite schema not initialized"}
  Record $stage 'PASS' @{sqlite_version_at_least=$minimumSchema;database_present=$true}
  return $file
}
try {
  if(-not (Get-Command gh -ErrorAction SilentlyContinue)){throw 'GitHub CLI gh.exe is required for predecessor artifact download'}
  if(-not $env:GH_TOKEN){throw 'Actions read token is required to download verified predecessor installer'}
  if(Test-Path $download){Remove-Item $download -Recurse -Force}
  New-Item -ItemType Directory -Force $download | Out-Null
  & gh run download $PriorRun --repo $Repository --name 'rc3-installer-source-and-windows-acceptance' --dir $download
  if($LASTEXITCODE -ne 0){throw 'Could not download predecessor installer; upgrade acceptance cannot be skipped'}
  $older=@(Get-ChildItem $download -Filter '*setup.exe' -Recurse -File | Select-Object -First 1)
  if($older.Count -ne 1){throw 'Predecessor artifact lacks NSIS setup executable'}
  $priorHash=(Get-FileHash $older[0].FullName -Algorithm SHA256).Hash.ToUpperInvariant()
  $expected='3EFBDA565ADE83355E9EBB09451AEB9E192DE0D87A50E4F57DDE7C054BDC2932'
  if($priorHash -ne $expected){throw "Predecessor checksum did not match previously verified RC2 artifact"}
  Record 'predecessor-integrity' 'PASS' @{source_run=$PriorRun;sha256=$priorHash}

  if(Test-Path $dest){Remove-Item $dest -Recurse -Force}
  $oldDesktop=Install-NSIS $older[0].FullName 'fresh-install-previous-version'
  Remove-Item $marker -ErrorAction SilentlyContinue
  $oldApp=Start-Process -FilePath $oldDesktop -PassThru
  try {
    $oldReady=Wait-Ready $oldApp $oldVersion
    # RC3 predecessor already ships SQLite schema v7.
    $db=Assert-Database 'pre-upgrade-database' 7
    $env:RC4_VERIFY_DB=$db
    & py -3.11 -c "import sqlite3,os,time; c=sqlite3.connect(os.environ['RC4_VERIFY_DB']); now=time.time(); c.execute('INSERT INTO sessions(id,title,created,updated) VALUES(?,?,?,?)',('rc4-upgrade-preservation','RC4 preserved session',now,now)); c.commit(); c.close()"
    if($LASTEXITCODE -ne 0){throw 'Could not write pre-upgrade session fixture'}
    Record 'pre-upgrade-session' 'PASS' @{session='rc4-upgrade-preservation';worker_startup_ms=$oldReady.worker_ready_ms}
  }finally { Close-And-Assert $oldApp ([int]$oldReady.pid) 'previous-version-shutdown' }

  $rc4Desktop=Install-NSIS (Resolve-Path -LiteralPath $CurrentInstaller).Path 'actual-in-place-upgrade'
  Remove-Item $marker -ErrorAction SilentlyContinue
  $rc4App=Start-Process -FilePath $rc4Desktop -PassThru
  $rc4Ready=$null
  try {
    $rc4Ready=Wait-Ready $rc4App $newVersion
    $db=Assert-Database 'post-upgrade-database' 7
    $env:RC4_VERIFY_DB=$db
    & py -3.11 -c "import sqlite3,os; c=sqlite3.connect(os.environ['RC4_VERIFY_DB']); row=c.execute('SELECT title FROM sessions WHERE id=?',('rc4-upgrade-preservation',)).fetchone(); assert row and row[0]=='RC4 preserved session'; c.close()"
    if($LASTEXITCODE -ne 0){throw 'Upgrade lost the existing session'}
    Record 'upgrade-data-preservation' 'PASS' @{session_preserved=$true;worker_startup_ms=$rc4Ready.worker_ready_ms}

    # Kill the owned PyInstaller process TREE, then require native supervisor recovery.
    # A bare parent kill could strand an orphaned onefile child; this is a supported tree-crash test.
    & taskkill.exe /PID $rc4Ready.pid /T /F | Out-Null
    $appRetried=Wait-Ready $rc4App $newVersion 45
    if([int]$appRetried.pid -eq [int]$rc4Ready.pid){throw 'Worker crash did not trigger a new process'}
    Record 'worker-tree-crash-recovery' 'PASS' @{old_pid=$rc4Ready.pid;new_pid=$appRetried.pid;restart_ms=$appRetried.startup_ms}
    $rc4Ready=$appRetried
    $events=Join-Path $logDir 'worker-lifecycle.jsonl'
    Require-File $events
    $raw=Get-Content $events -Raw
    if($raw -notmatch 'worker_exited' -or $raw -notmatch 'authenticated_health'){throw 'Missing bounded restart diagnostics'}
    if($raw -match 'X-Studio-Token|Bearer |sk-[A-Za-z0-9]{10,}'){throw 'Diagnostics contain an apparent credential'}
    Record 'diagnostic-privacy' 'PASS' @{structured_events=$true;no_token_material_detected=$true}
  }finally {if($rc4Ready){Close-And-Assert $rc4App ([int]$rc4Ready.pid) 'rc4-shutdown'}else {$rc4App.Kill($true);$rc4App.WaitForExit()}}

  Remove-Item $marker -ErrorAction SilentlyContinue
  $reopen=Start-Process -FilePath $rc4Desktop -PassThru
  $warmReady=$null
  try {
    $warmReady=Wait-Ready $reopen $newVersion
    $null=Assert-Database 'rc4-relaunch-database'
    Record 'installed-app-relaunch' 'PASS' @{startup_ms=$warmReady.startup_ms;worker_ready_ms=$warmReady.worker_ready_ms}
  }finally {if($warmReady){Close-And-Assert $reopen ([int]$warmReady.pid) 'rc4-relaunch-shutdown'}else{$reopen.Kill($true);$reopen.WaitForExit()}}
  $uninstaller=@(Get-ChildItem $dest -Filter '*uninstall*.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1)
  if($uninstaller.Count -ne 1){throw 'Uninstaller missing'}
  $un=Start-Process -FilePath $uninstaller[0].FullName -ArgumentList '/S' -Wait -PassThru
  if($un.ExitCode -ne 0){throw "Silent uninstall failed: $($un.ExitCode)"}
  if(Test-Path $rc4Desktop){throw 'Uninstall left desktop executable installed'}
  Require-File (Join-Path $env:STUDIO_DATA_DIR 'studio.sqlite3')
  Record 'uninstall-retains-user-data' 'PASS' @{executable_removed=$true;user_data_retained=$true}
}
finally {
  $steps | ConvertTo-Json -Depth 9 | Out-File -Encoding utf8 $evidence
  if($env:GITHUB_STEP_SUMMARY) {
    "RC4 upgrade + installed-app evidence: $evidence" | Out-File -Append -Encoding utf8 $env:GITHUB_STEP_SUMMARY
    ($steps | ForEach-Object { "- $($_.stage): $($_.outcome)" }) | Out-File -Append -Encoding utf8 $env:GITHUB_STEP_SUMMARY
  }
}
