<#
.SYNOPSIS
  Estimates when the current Claude 5-hour usage block ends (ccusage blocks, local logs, offline) and when to resume.
.OUTPUTS
  Lines: block_end_local, minutes_left, resume_at_local (end + 1 min), seconds_until_resume, tokens_in_block.
.NOTES
  This is an estimate from local logs. If Claude Code shows its own "resets at ..." time in a limit message,
  that time wins. Weekly limits cannot be predicted here.
#>
$exe = Join-Path $env:USERPROFILE '.claude\company\vendor\ccusage\node_modules\@ccusage\ccusage-win32-x64\bin\ccusage.exe'
if (-not (Test-Path $exe)) { Write-Output 'ccusage not installed'; exit 1 }
$ErrorActionPreference = 'Continue'
# Weekly brake (rolling 7 days, API-equivalent USD from local logs)
$brake = 200
try { $bj = Get-Content (Join-Path $env:USERPROFILE '.claude\company\budgets.json') -Raw | ConvertFrom-Json; if ($bj.claudeWeekly.loopBrakeUsd) { $brake = [double]$bj.claudeWeekly.loopBrakeUsd } } catch {}
$since = (Get-Date).AddDays(-6).ToString('yyyyMMdd')
$wraw = & $exe claude daily --offline --json --since $since 2>$null | Out-String
$week = 0.0; try { $week = (($wraw | ConvertFrom-Json).daily | Measure-Object totalCost -Sum).Sum } catch {}
Write-Output ("weekly_usd: {0:N2}" -f $week)
Write-Output ("weekly_brake_usd: {0}" -f $brake)
Write-Output ("weekly_brake_hit: {0}" -f ($week -ge $brake))
$raw = & $exe blocks --active --offline --json 2>$null | Out-String
try { $b = ($raw | ConvertFrom-Json).blocks | Where-Object { $_.isActive } | Select-Object -First 1 } catch { $b = $null }
if (-not $b) { Write-Output 'no_active_block: usage window is free (resume now)'; exit 0 }
$end = ([datetime]$b.endTime).ToLocalTime()
$resume = $end.AddMinutes(1)
$secs = [math]::Max(0, [int]($resume - (Get-Date)).TotalSeconds)
Write-Output ("block_end_local: {0:yyyy-MM-dd HH:mm}" -f $end)
Write-Output ("minutes_left: {0}" -f [math]::Max(0, [int]($end - (Get-Date)).TotalMinutes))
Write-Output ("resume_at_local: {0:yyyy-MM-dd HH:mm}" -f $resume)
Write-Output ("seconds_until_resume: {0}" -f $secs)
Write-Output ("tokens_in_block: {0}" -f $b.totalTokens)
