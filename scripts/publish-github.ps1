# Full source import from the extracted v0.4 release directory into the designated GitHub repository.
# Requires only Git, Node/npm, a GitHub account with push permission, and normal network access.
param(
  [string]$Remote = 'https://github.com/AmalBajpayee09/AI-Interview-Studio.git',
  [string]$Branch = 'import/v0.4.0'
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Temp = Join-Path ([System.IO.Path]::GetTempPath()) ('studio-import-' + [guid]::NewGuid().ToString('N'))
if (-not (Test-Path (Join-Path $Root 'apps/desktop/package.json'))) {throw 'Run this script from the extracted v0.4.0 source archive.'}
New-Item -ItemType Directory -Path $Temp | Out-Null
try {
  & git clone $Remote $Temp
  if ($LASTEXITCODE -ne 0) {throw 'Unable to clone GitHub repository; check connectivity and permissions.'}
  Push-Location $Temp
  try {
    & git checkout -b $Branch
    if ($LASTEXITCODE -ne 0) {throw 'Unable to create import branch.'}
    # Import every source file, including .github and .gitignore, but never .git or local secrets.
    # The source ZIP is generated with these exclusions before delivery.
    Get-ChildItem -LiteralPath $Root -Force | Where-Object { $_.Name -notin @('.git','.env','node_modules','.venv') } | ForEach-Object {
      Copy-Item -LiteralPath $_.FullName -Destination $Temp -Recurse -Force
    }
    # Keep the build-gated workflow already committed on main.
    & git restore --source=origin/main -- .github/workflows/windows-release.yml
    if ($LASTEXITCODE -ne 0) {throw 'Unable to restore existing repository build workflow.'}
    Push-Location 'apps/desktop'
    try {
      & npm install --package-lock-only --ignore-scripts
      if ($LASTEXITCODE -ne 0) {throw 'Cannot generate lockfile; check Node/npm internet access.'}
      & npm ci
      if ($LASTEXITCODE -ne 0) {throw 'npm ci dependency check failed.'}
      & npm run build
      if ($LASTEXITCODE -ne 0) {throw 'Frontend build failed; correct errors before publishing.'}
    } finally {Pop-Location}
    & git add -A
    if ($LASTEXITCODE -ne 0) {throw 'git add failed'}
    & git status --short
    & git -c user.name='AI Interview Studio Import' -c user.email='ci-import@users.noreply.github.com' commit -m 'Import complete AI Interview Studio v0.4.0 source and lockfile'
    if ($LASTEXITCODE -ne 0) {throw 'Commit failed; no source imported.'}
    & git push --set-upstream origin $Branch
    if ($LASTEXITCODE -ne 0) {throw 'Push failed; check GitHub credentials and repository permissions.'}
    Write-Host "Source import branch pushed: $Branch. Open GitHub and create a PR into main."
  } finally {Pop-Location}
} finally {
  if (Test-Path $Temp) {Remove-Item -LiteralPath $Temp -Recurse -Force}
}
