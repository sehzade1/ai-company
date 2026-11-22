<#
.SYNOPSIS
  Asks the Producer (Gemini via Antigravity) for the next work prompts of a project, or to brainstorm the list.
.EXAMPLE
  producer.ps1 -Mode brainstorm                       # improve the master list before starting
  producer.ps1 -Mode next                             # review the last report, get the next prompt(s)
.NOTES
  Reads (inside -Project): the master list section, the session checkpoint, pending decisions and the last report.
  Writes: production/producer/next.md (latest reply) and appends production/producer/log.md.
  Exit 75 = budget/provider limit (see company.ps1); the loop must wait or fall back.
#>
param(
  [ValidateSet('next', 'brainstorm')][string]$Mode = 'next',
  [string]$Project = 'D:\Projects\system-game',
  [string]$ListFile = 'system game\docs\YOL_HARITASI.md',
  [string]$SectionPattern = '^# Kontrol Noktası',   # the LAST heading matching this starts the current section
  [int]$MaxListChars = 18000
)
$ErrorActionPreference = 'Stop'
$utf8 = New-Object Text.UTF8Encoding $false
$pdir = Join-Path $Project 'production\producer'
New-Item -ItemType Directory -Force $pdir | Out-Null
$co = Join-Path $env:USERPROFILE '.claude\company\company.ps1'

function Read-Opt($path) { if (Test-Path $path) { [IO.File]::ReadAllText($path) } else { '' } }

# Current section of the master list
$lines = [IO.File]::ReadAllLines((Join-Path $Project $ListFile))
$start = 0
for ($i = 0; $i -lt $lines.Count; $i++) { if ($lines[$i] -match $SectionPattern) { $start = $i } }
$list = ($lines[$start..($lines.Count - 1)] -join "`n")
if ($list.Length -gt $MaxListChars) { $list = $list.Substring(0, $MaxListChars) + "`n[...truncated]" }

$active = Read-Opt (Join-Path $Project 'production\session-state\active.md')
if ($active -match '(?s)<!-- CHECKPOINT -->(.*?)<!-- /CHECKPOINT -->') { $active = $Matches[1].Trim() }
$pending = Read-Opt (Join-Path $Project 'production\bekleyen-kararlar.md')
$report = Read-Opt (Join-Path $pdir 'last-report.md')
if ($report.Length -gt 6000) { $report = $report.Substring(0, 6000) + "`n[...truncated]" }

if ($Mode -eq 'brainstorm') {
  $task = @"
BRAINSTORM MODE. Before work starts, improve the master list below with the CEO. Look for: missing steps
or tests, risky ordering, items that are too big (split them), items that need a user decision first
(list them as DEFERRED), and good additions that fit the GDD and the current checkpoint's goal. Use
PROPOSED_ITEMS for additions/splits, DEFERRED for decisions, and put the recommended FIRST work package
in NEXT_PROMPTS. STATUS should be CONTINUE.

MASTER LIST (current section):
$list

SESSION CHECKPOINT:
$active

ALREADY PENDING USER DECISIONS:
$pending
"@
} else {
  $task = @"
NEXT MODE. Review the last work report, then give the next prompt(s) from the master list.

MASTER LIST (current section):
$list

SESSION CHECKPOINT:
$active

ALREADY PENDING USER DECISIONS (do not ask these again):
$pending

LAST WORK REPORT FROM THE CEO:
$(if ($report) { $report } else { '(none yet: this is the first call)' })
"@
}

$out = & $co delegate -Agent antigravity -Role producer -Department production -Task "producer $Mode" -Prompt $task -TimeoutSec 900 2>&1 | ForEach-Object { "$_" }
$code = $LASTEXITCODE
$text = ($out -join "`n")
$reply = ($text -split '(?m)^--- (TIME|FINANCE):')[0].Trim()

$stamp = Get-Date -Format 'yyyy-MM-dd HH:mm'
[IO.File]::WriteAllText((Join-Path $pdir 'next.md'), "# Producer reply ($Mode, $stamp)`n`n$reply`n", $utf8)
[IO.File]::AppendAllText((Join-Path $pdir 'log.md'), "`n## $stamp — producer $Mode (exit $code)`n`n$reply`n", $utf8)
$reply
if ($code -ne 0) { exit $code }
