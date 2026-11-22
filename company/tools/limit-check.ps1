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
