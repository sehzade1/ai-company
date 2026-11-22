<#
.SYNOPSIS
  Start a new, clean project for the AI company. Nothing from older projects is copied in.
.EXAMPLE
  new-project.ps1 -Name kahve-sitesi                      # general project
  new-project.ps1 -Name yeni-oyun -Type game              # game: fresh Claude Code Game Studios from GitHub + company routing
.NOTES
  What carries over to every project automatically (global, in ~/.claude): the company rules (CLAUDE.md),
  skills, director/worker agents, company.ps1, roles, tools, R&D decisions, Finance ledger.
  What never carries over: another project's CLAUDE.md, code, git history, session history or project memory
  (Claude Code keys these by folder, so a new folder starts empty).
#>
param(
  [Parameter(Mandatory = $true)][ValidatePattern('^[a-z0-9][a-z0-9\-]*$')][string]$Name,
  [ValidateSet('general', 'game')][string]$Type = 'general',
  [string]$Root = 'D:\Projects'
)
$ErrorActionPreference = 'Stop'
$dir = Join-Path $Root $Name
if (Test-Path $dir) { Write-Output "ERROR: $dir already exists. Pick another name."; exit 1 }
$utf8 = New-Object Text.UTF8Encoding $false
$company = Join-Path $env:USERPROFILE '.claude\company'

if ($Type -eq 'game') {
  # Fresh copy of the studio framework (latest release), with its own new git history
  $ErrorActionPreference = 'Continue'
  git clone --depth 1 https://github.com/Donchitos/Claude-Code-Game-Studios.git $dir 2>&1 | Out-Null
  $ErrorActionPreference = 'Stop'
  if (-not (Test-Path (Join-Path $dir '.claude\agents'))) { Write-Output "ERROR: could not clone the studio template"; exit 1 }
  Remove-Item -Recurse -Force (Join-Path $dir '.git')
  # Company standards: pin agent models (Opus only for the CEO), add cross-model routing
  Get-ChildItem (Join-Path $dir '.claude\agents') -Filter *.md | ForEach-Object {
    $s = [IO.File]::ReadAllText($_.FullName)
    $s = [regex]::Replace($s, '(?m)^model:\s*(opus|inherit)\s*$', 'model: sonnet')
    [IO.File]::WriteAllText($_.FullName, $s, $utf8)
  }
  $routing = Join-Path $company 'studio-template\ai-company-routing.md'
  if (Test-Path $routing) {
    Copy-Item $routing (Join-Path $dir '.claude\docs\ai-company-routing.md')
    Add-Content (Join-Path $dir 'CLAUDE.md') "`n## AI Company Routing (Codex, Gemini, local tools)`n`n@.claude/docs/ai-company-routing.md`n" -Encoding UTF8
  }
  $note = 'Studio framework cloned fresh. Next: open the folder and run /start (it sets the engine; then archive the engine agents you do not use).'
} else {
  New-Item -ItemType Directory -Force $dir | Out-Null
  $claude = @"
# $Name

## Goal
(1-3 sentences: what this project is and who it is for.)

## Stack
(languages, frameworks, how to run, how to test)

## Project rules
- Facts about THIS project live in this file and in the repo, never in the global company files.
- The AI company workflow applies (global ~/.claude/CLAUDE.md): CEO plans, work is split across Claude, Codex and Gemini, cross-reviewed, Finance tracks tokens.
"@
  [IO.File]::WriteAllText((Join-Path $dir 'CLAUDE.md'), $claude, $utf8)
  [IO.File]::WriteAllText((Join-Path $dir 'README.md'), "# $Name`n", $utf8)
  [IO.File]::WriteAllText((Join-Path $dir '.gitignore'), ".env`n*.local.json`nnode_modules/`n__pycache__/`n.venv/`nbuild/`ndist/`n", $utf8)
  $note = 'Fill in Goal and Stack in CLAUDE.md, or ask Claude to do it in the first session.'
}

Push-Location $dir
$ErrorActionPreference = 'Continue'
git init -q 2>&1 | Out-Null
git add -A 2>&1 | Out-Null
git -c user.name="$(if (git config user.name) { git config user.name } else { 'project' })" -c user.email="$(if (git config user.email) { git config user.email } else { 'project@localhost' })" commit -q -m "chore: start $Name" 2>&1 | Out-Null
Pop-Location

Write-Output "OK: $dir ($Type)"
Write-Output $note
Write-Output "Open it (not as administrator):  code `"$dir`"   then run  claude  in that folder."
