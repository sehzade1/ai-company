<#
.SYNOPSIS
  Runs the producer loop autonomously: one work package per FRESH headless Claude session (General Manager on
  Sonnet), with the 5-hour and weekly brakes. When a brake is hit it schedules itself to resume and exits.
.EXAMPLE
  loop-runner.ps1                      # run until the list is done or a brake/stop condition is hit
  loop-runner.ps1 -DryRun              # show checks and the command, launch nothing
  loop-runner.ps1 -MaxPackages 3       # stop after 3 packages
.NOTES
  State lives in files (production/producer/*, active.md), so no long conversation is re-read each step.
  Log: <project>\production\producer\runner.log. Scheduled resume task: "AICompany-ProducerLoop" (Task Scheduler).
#>
param(
  [string]$Project = 'D:\Projects\system-game',
  [string]$Model = 'sonnet',
  [int]$MaxPackages = 0,             # 0 = no limit (stop when the list is done)
  [int]$PackageTimeoutMin = 90,
  [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$tools = Join-Path $env:USERPROFILE '.claude\company\tools'
$pdir = Join-Path $Project 'production\producer'
$log = Join-Path $pdir 'runner.log'
$taskName = 'AICompany-ProducerLoop'
New-Item -ItemType Directory -Force $pdir | Out-Null
function Write-Log($m) { $l = "{0:yyyy-MM-dd HH:mm:ss}  {1}" -f (Get-Date), $m; Add-Content -Path $log -Value $l -Encoding UTF8; Write-Output $l }

function Get-Limits {
  $o = & (Join-Path $tools 'limit-check.ps1') 2>$null
  $h = @{}; foreach ($line in $o) { if ($line -match '^([a-z_]+):\s*(.*)$') { $h[$Matches[1]] = $Matches[2].Trim() } }
  return $h
}

function Get-WeeklyClearDate([double]$brake) {
  # First day on which the rolling 7-day Claude total drops below the brake (older days fall out of the window).
  $exe = Join-Path $env:USERPROFILE '.claude\company\vendor\ccusage\node_modules\@ccusage\ccusage-win32-x64\bin\ccusage.exe'
  $raw = & $exe claude daily --offline --json --since ((Get-Date).AddDays(-7).ToString('yyyyMMdd')) 2>$null | Out-String
  $days = @{}; try { foreach ($d in ($raw | ConvertFrom-Json).daily) { $k = if ($d.date) { $d.date } else { $d.period }; $days[$k] = [double]$d.totalCost } } catch {}
  for ($i = 1; $i -le 7; $i++) {
    $day = (Get-Date).Date.AddDays($i); $sum = 0.0
    for ($j = 0; $j -lt 7; $j++) { $k = $day.AddDays(-$j).ToString('yyyy-MM-dd'); if ($days.ContainsKey($k)) { $sum += $days[$k] } }
    if ($sum -lt $brake) { return $day.AddMinutes(5) }
  }
  return (Get-Date).Date.AddDays(7).AddMinutes(5)
}

function Register-Resume([datetime]$at, [string]$why) {
  Write-Log "PAUSE ($why). Resume scheduled for $($at.ToString('yyyy-MM-dd HH:mm'))."
  if ($DryRun) { return }
  $ErrorActionPreference = 'Continue'
  $ps = (Get-Command powershell.exe).Source
  $tr = "`"$ps`" -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$PSCommandPath`" -Project `"$Project`" -Model $Model"
  & schtasks.exe /Create /F /SC ONCE /TN $taskName /TR $tr /SD $at.ToString('dd.MM.yyyy') /ST $at.ToString('HH:mm') 2>&1 | Out-Null
  if ($LASTEXITCODE -ne 0) {
    # date format differs by locale; retry with ISO-like US format
    & schtasks.exe /Create /F /SC ONCE /TN $taskName /TR $tr /SD $at.ToString('MM/dd/yyyy') /ST $at.ToString('HH:mm') 2>&1 | Out-Null
  }
  Write-Log ("schtasks exit {0}" -f $LASTEXITCODE)
  $ErrorActionPreference = 'Stop'
}

function Get-ProducerStatus {
  $n = Join-Path $pdir 'next.md'
  if (-not (Test-Path $n)) { return 'NONE' }
  $m = Select-String $n -Pattern '^STATUS:\s*(\S+)' | Select-Object -First 1
  if ($m) { return $m.Matches[0].Groups[1].Value } else { return 'UNKNOWN' }
}

$instruction = @'
You are the GENERAL MANAGER of the AI company (Claude Sonnet), running ONE iteration of the producer-loop skill
in this project, then you stop. Use the producer-loop skill. Directors are Gemini: for reviews call
`powershell -File "%USERPROFILE%\.claude\company\company.ps1" delegate -Agent antigravity -Role director-<dept> ...`
and attach test output/diffs; use Claude director subagents only if Gemini returns exit 75.
Do exactly one work package from production/producer/next.md (or get the next prompt with producer.ps1 if it
is already done), verify it, commit per the project rules, write production/producer/last-report.md, update
active.md, call producer.ps1 -Mode next, then end with ONE line: "PACKAGE_DONE <item id>" or
"LOOP_STOP <reason>". Escalate to the CEO (write ESCALATE in the report) only for strategic issues.
Never push, never install, never touch Steam, never delete saves; every wait has a timeout.
'@

$done = 0
Write-Log "runner start (project $Project, model $Model, max $MaxPackages, dry=$DryRun)"
if (-not $DryRun) { $ErrorActionPreference = 'Continue'; & schtasks.exe /Delete /F /TN $taskName 2>&1 | Out-Null; $ErrorActionPreference = 'Stop' }   # a running loop owns the schedule

while ($true) {
  $st = Get-ProducerStatus
  if ($st -in 'DONE', 'WAIT_FOR_USER') { Write-Log "STOP: producer status $st. See production/bekleyen-kararlar.md."; break }

  $lim = Get-Limits
  if ($lim['weekly_brake_hit'] -eq 'True') {
    $at = Get-WeeklyClearDate ([double]$lim['weekly_brake_usd'])
    Register-Resume $at "weekly brake: $($lim['weekly_usd']) USD >= $($lim['weekly_brake_usd']) USD in 7 days"; break
  }
  if ($lim.ContainsKey('minutes_left') -and [int]$lim['minutes_left'] -lt 10) {
    Register-Resume ([datetime]$lim['resume_at_local']) '5-hour block almost used'; break
  }

  if ($DryRun) {
    Write-Log "DRY RUN: would run: claude -p <GM instruction> --model $Model --permission-mode auto (cwd $Project). Limits: weekly $($lim['weekly_usd'])/$($lim['weekly_brake_usd']) USD, block left $($lim['minutes_left']) min. Producer status: $st"
    break
  }

  Write-Log "package $($done + 1): starting fresh $Model session"
  $outFile = Join-Path $pdir ("run-{0:yyyyMMdd-HHmmss}.json" -f (Get-Date))
  $job = Start-Job -ArgumentList $Project, $instruction, $Model, $outFile -ScriptBlock {
    param($Project, $instruction, $Model, $outFile)
    Set-Location $Project
    $instruction | & claude -p --model $Model --permission-mode auto --output-format json 2>&1 | Out-File -FilePath $outFile -Encoding utf8
  }
  if (-not (Wait-Job $job -Timeout ($PackageTimeoutMin * 60))) {
    Stop-Job $job; Write-Log "STOP: package exceeded $PackageTimeoutMin min (killed). Check $outFile."; break
  }
  Remove-Job $job -Force
  $raw = if (Test-Path $outFile) { [IO.File]::ReadAllText($outFile) } else { '' }
  $result = ''; $cost = ''
  try { $j = $raw | ConvertFrom-Json; $result = [string]$j.result; $cost = $j.total_cost_usd } catch { $result = $raw }

  if ($raw -match '(?i)usage limit|limit reached|resets at|rate.?limit|weekly limit') {
    $lim = Get-Limits
    if ($raw -match '(?i)weekly') { Register-Resume (Get-WeeklyClearDate ([double]$lim['weekly_brake_usd'])) 'Claude weekly limit message' }
    else { Register-Resume ([datetime]$lim['resume_at_local']) 'Claude usage limit message' }
    break
  }
  $last = ($result -split "`n" | Where-Object { $_ -match 'PACKAGE_DONE|LOOP_STOP' } | Select-Object -Last 1)
  Write-Log ("package $($done + 1) finished: {0} (api-equiv {1} USD)" -f ($(if ($last) { $last.Trim() } else { 'no marker' })), $cost)
  if ($last -match 'LOOP_STOP') { Write-Log 'STOP: general manager stopped the loop.'; break }
  if (-not $last) { Write-Log 'STOP: no PACKAGE_DONE marker; inspect the run file before continuing.'; break }
  $done++
  if ($MaxPackages -gt 0 -and $done -ge $MaxPackages) { Write-Log "STOP: reached MaxPackages $MaxPackages."; break }
}
Write-Log "runner end ($done packages)"
