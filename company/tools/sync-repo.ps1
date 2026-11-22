<#
.SYNOPSIS
  Copies the live AI company (~/.claude) into the public repo clone, removes personal data,
  runs a privacy scan, and (with -Push) commits and pushes.
.EXAMPLE
  sync-repo.ps1                       # update the clone and show what changed (no commit)
  sync-repo.ps1 -Push -Message "Add X" # commit and push after a clean scan
.NOTES
  Never copies: ledger.csv, memory, settings, .claude.json, R&D images/logs/raw outputs, vendor or
  third-party files (vendors\, studio-template\agents\). Personal paths become {{HOME}}.
#>
param(
  [string]$Repo = 'D:\Projects\ai-company',
  [switch]$Push,
  [string]$Message = 'Sync company updates'
)
$ErrorActionPreference = 'Stop'
$h = Join-Path $env:USERPROFILE '.claude'
$c = Join-Path $h 'company'
$utf8 = New-Object Text.UTF8Encoding $false
if (-not (Test-Path (Join-Path $Repo '.git'))) { Write-Output "ERROR: $Repo is not a git clone"; exit 1 }

function Put($from, $to) {
  New-Item -ItemType Directory -Force (Split-Path $to) | Out-Null
  Copy-Item $from $to -Force
}

# 1) Global Claude files
Put (Join-Path $h 'CLAUDE.md') (Join-Path $Repo 'claude\CLAUDE.md')
foreach ($s in 'company', 'ask-codex', 'ask-antigravity', 'brainstorming', 'systematic-debugging', 'test-driven-development', 'writing-plans', 'verification-before-completion', 'requesting-code-review', 'receiving-code-review', 'dispatching-parallel-agents') {
  Get-ChildItem (Join-Path $h "skills\$s") -Recurse -File | ForEach-Object {
    Put $_.FullName (Join-Path $Repo ('claude\skills\' + $s + $_.FullName.Substring((Join-Path $h "skills\$s").Length)))
  }
}
Get-ChildItem (Join-Path $h 'agents') -Filter *.md | Where-Object { $_.Name -match '^(director|manager|worker)-' } |
  ForEach-Object { Put $_.FullName (Join-Path $Repo "claude\agents\$($_.Name)") }

# 2) Company files
foreach ($f in 'ORG.md', 'roster.md', 'budgets.json', 'company.ps1', 'THIRD_PARTY_NOTICES.md') { Put (Join-Path $c $f) (Join-Path $Repo "company\$f") }
foreach ($d in 'roles', 'tools', 'meeting') {
  Get-ChildItem (Join-Path $c $d) -Recurse -File | ForEach-Object { Put $_.FullName (Join-Path $Repo ('company\' + $_.FullName.Substring($c.Length + 1))) }
}
Get-ChildItem (Join-Path $c 'studio-template') -File -ErrorAction SilentlyContinue | ForEach-Object { Put $_.FullName (Join-Path $Repo "company\studio-template\$($_.Name)") }
Get-ChildItem (Join-Path $c 'rnd') -Recurse -File | Where-Object {
  $_.Extension -in '.md', '.txt', '.csv', '.js', '.ps1', '.py', '.tsv' -and $_.Name -notmatch '^out-|log|raw|blind-map|g4-map' -and $_.Length -lt 60KB
} | ForEach-Object { Put $_.FullName (Join-Path $Repo ('company\' + $_.FullName.Substring($c.Length + 1))) }

# 3) Remove personal paths
$userPath = $env:USERPROFILE
$variants = @($userPath, $userPath.Replace('\', '\\'), $userPath.Replace('\', '\\\\'), $userPath.Replace('\', '/'))
Get-ChildItem (Join-Path $Repo 'claude'), (Join-Path $Repo 'company') -Recurse -File | ForEach-Object {
  $s = [IO.File]::ReadAllText($_.FullName); $n = $s
  foreach ($v in $variants) { $n = $n.Replace($v, '{{HOME}}') }
  if ($n -ne $s) { [IO.File]::WriteAllText($_.FullName, $n, $utf8) }
}

# 4) Privacy scan: user name, mail domains, tokens, cloud-sync folders
$userName = Split-Path $userPath -Leaf
$pattern = [regex]::Escape($userName) + '|@(hotmail|gmail|outlook|yahoo)\.|gho_[A-Za-z0-9]{10}|sk-ant-[A-Za-z0-9]|AIza[0-9A-Za-z_\-]{20}|OneDrive'
$leaks = Get-ChildItem $Repo -Recurse -File | Where-Object { $_.FullName -notmatch '\\\.git\\' -and $_.Name -ne 'sync-repo.ps1' } | Select-String -Pattern $pattern
if ($leaks) {
  Write-Output 'PRIVACY SCAN FAILED - nothing committed:'
  $leaks | ForEach-Object { Write-Output "  $($_.Path.Replace($Repo, '')):$($_.LineNumber)" }
  exit 2
}

$ErrorActionPreference = 'Continue'
$changes = git -C $Repo status --short
if (-not $changes) { Write-Output 'Repo already up to date.'; exit 0 }
Write-Output 'Changed files:'; $changes
if ($Push) {
  git -C $Repo add -A
  git -C $Repo -c user.name='ai-company' -c user.email='ai-company@localhost' commit -q -m $Message
  git -C $Repo push 2>&1 | Select-Object -Last 1
  Write-Output "Pushed: $(git -C $Repo log -1 --format='%h %s')"
} else { Write-Output 'Scan clean. Run again with -Push -Message "..." to publish.' }
