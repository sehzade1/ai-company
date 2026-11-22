<#
.SYNOPSIS
  Company toolkit: delegate work to agents, track token usage (Finance dept), report budgets.

.EXAMPLES
  company.ps1 delegate -Agent codex -Department engineering -Task "fix bug" -Prompt "..."
  company.ps1 log -Agent claude-opus -Department ceo -Task "planning" -Tokens 12000
  company.ps1 status            # budget status per agent (today)
  company.ps1 report            # full finance report + reassignment recommendations
#>
param(
  [Parameter(Position = 0, Mandatory = $true)][ValidateSet('delegate', 'log', 'status', 'report', 'usage')][string]$Command,
  [string]$Agent,
  [string]$Department = 'general',
  [string]$Task = '',
  [string]$Prompt = '',
  [string]$Role = '',
  [int]$Tokens = 0,
  [string]$Model = '',
  [string]$Effort = '',
  [int]$TimeoutSec = 120
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Home_ = Join-Path $env:USERPROFILE '.claude\company'
$Ledger = Join-Path $Home_ 'ledger.csv'
$BudgetFile = Join-Path $Home_ 'budgets.json'

if (-not (Test-Path $Ledger)) {
  'timestamp,agent,department,task,tokens,estimated,status' | Set-Content -Encoding UTF8 $Ledger
}
$budgets = Get-Content $BudgetFile -Raw | ConvertFrom-Json

function Add-Ledger($agent, $dept, $task, $tokens, $estimated, $status) {
  $t = ($task -replace '[",\r\n]', ' ')
  $line = '{0},{1},{2},"{3}",{4},{5},{6}' -f (Get-Date -Format 'yyyy-MM-ddTHH:mm:ss'), $agent, $dept, $t, $tokens, $estimated, $status
  # Retry: parallel delegate calls may hold the file briefly.
  for ($i = 0; $i -lt 20; $i++) {
    try { Add-Content -Encoding UTF8 $Ledger $line -ErrorAction Stop; return } catch { Start-Sleep -Milliseconds (100 + (Get-Random -Maximum 300)) }
  }
  Write-Warning "Could not write ledger line: $line"
}

function Get-TodayUsage($agent) {
  $today = Get-Date -Format 'yyyy-MM-dd'
  $rows = Import-Csv $Ledger | Where-Object { $_.agent -eq $agent -and $_.timestamp.StartsWith($today) }
  $sum = ($rows | Measure-Object -Property tokens -Sum).Sum
  if ($null -eq $sum) { return 0 }
  return [int]$sum
}

function Get-BudgetState($agent) {
  $cfg = $budgets.agents.$agent
  if ($null -eq $cfg) { return [pscustomobject]@{ Agent = $agent; Used = 0; Budget = 0; Pct = 0; State = 'unknown' } }
  $used = Get-TodayUsage $agent
  $budget = [int]$cfg.dailyTokenBudget
  $pct = if ($budget -gt 0) { [math]::Round(100.0 * $used / $budget, 1) } else { 0 }
  $state = if ($budget -le 0) { 'untracked' }
           elseif ($pct -ge 100) { 'EXHAUSTED' }
           elseif ($pct -ge $budgets.thresholds.critical) { 'CRITICAL' }
           elseif ($pct -ge $budgets.thresholds.warning) { 'WARNING' }
           else { 'ok' }
  return [pscustomobject]@{ Agent = $agent; Used = $used; Budget = $budget; Pct = $pct; State = $state }
}

function Get-Fallbacks($agent) {
  $cfg = $budgets.agents.$agent
  if ($cfg -and $cfg.fallback) { return ($cfg.fallback -join ', ') }
  return '(none)'
}
function Get-RealUsage([string]$since) {
  # Real token counts from the CLIs' own local logs via ccusage (pinned 20.0.48, --offline: no network).
  $exe = Join-Path $Home_ 'vendor\ccusage\node_modules\@ccusage\ccusage-win32-x64\bin\ccusage.exe'
  if (-not (Test-Path $exe)) { return $null }
  $rows = foreach ($a in 'claude', 'codex', 'antigravity') {
    $ErrorActionPreference = 'Continue'
    $raw = & $exe $a daily --offline --json --since $since 2>$null | Out-String
    $ErrorActionPreference = 'Stop'
    try { $j = $raw | ConvertFrom-Json } catch { continue }
    $d = @($j.daily)
    [pscustomobject]@{
      Agent      = $a
      Input      = ($d | Where-Object { $_.PSObject.Properties['inputTokens'] } | Measure-Object inputTokens -Sum).Sum
      Output     = ($d | Where-Object { $_.PSObject.Properties['outputTokens'] } | Measure-Object outputTokens -Sum).Sum
      CacheWrite = ($d | Where-Object { $_.PSObject.Properties['cacheCreationTokens'] } | Measure-Object cacheCreationTokens -Sum).Sum
      CacheRead  = ($d | Where-Object { $_.PSObject.Properties['cacheReadTokens'] } | Measure-Object cacheReadTokens -Sum).Sum
      Total      = ($d | Where-Object { $_.PSObject.Properties['totalTokens'] } | Measure-Object totalTokens -Sum).Sum
      ApiEquivUSD = [math]::Round(($d | ForEach-Object { foreach ($p in 'totalCost', 'costUSD', 'cost') { if ($_.PSObject.Properties[$p]) { [double]$_.$p; break } } } | Measure-Object -Sum).Sum, 2)
    }
  }
  return $rows
}

switch ($Command) {

  'log' {
    if (-not $Agent) { throw '-Agent required' }
    Add-Ledger $Agent $Department $Task $Tokens 'False' 'ok'
    "Logged $Tokens tokens for $Agent."
  }

  'usage' {
    $today = Get-Date -Format 'yyyyMMdd'; $week = (Get-Date).AddDays(-6).ToString('yyyyMMdd')
    "=== REAL USAGE (ccusage, local CLI logs) ==="
    "Today:"; Get-RealUsage $today | Format-Table -AutoSize | Out-String
    "Last 7 days:"; Get-RealUsage $week | Format-Table -AutoSize | Out-String
    'ApiEquivUSD = what the tokens would cost on the pay-as-you-go API; on subscriptions it is not billed. Antigravity models are unpriced. Ledger budgets (status/report) are per-task estimates; use these numbers for real load.'
  }
  'status' {
    $budgets.agents.PSObject.Properties.Name | ForEach-Object { Get-BudgetState $_ } | Format-Table -AutoSize
  }

  'report' {
    "=== FINANCE REPORT $(Get-Date -Format 'yyyy-MM-dd HH:mm') ==="
    $states = $budgets.agents.PSObject.Properties.Name | ForEach-Object { Get-BudgetState $_ }
    $states | Format-Table -AutoSize | Out-String
    $hot = $states | Where-Object { $_.State -in 'WARNING', 'CRITICAL', 'EXHAUSTED' }
    if ($hot) {
      'RECOMMENDATIONS (Finance -> CEO):'
      foreach ($h in $hot) {
        $action = switch ($h.State) {
          'EXHAUSTED' { 'STOP assigning new work; hand all pending tasks to fallback' }
          'CRITICAL'  { 'Reduce workload sharply; only critical tasks; move the rest to fallback' }
          default     { 'Reduce workload; prefer fallback for new non-specialist tasks' }
        }
        "- $($h.Agent) [$($h.State), $($h.Pct)%]: $action. Fallbacks: $(Get-Fallbacks $h.Agent)"
      }
    } else { 'All agents within budget. No reassignment needed.' }
    ''
    'Usage by department (all time):'
    Import-Csv $Ledger | Group-Object department | ForEach-Object {
      [pscustomobject]@{ Department = $_.Name; Tokens = ($_.Group | Measure-Object -Property tokens -Sum).Sum; Calls = $_.Count }
    } | Format-Table -AutoSize | Out-String
    'External vendor - TestSprite credits:'
    if (Get-Command testsprite -ErrorAction SilentlyContinue) {
      $ErrorActionPreference = 'Continue'
      $ts = (testsprite usage 2>&1 | ForEach-Object { "$_" }) -join "`n"
      $ErrorActionPreference = 'Stop'
      if ($ts -match 'Authentication is required') { '  not logged in (user must run: testsprite setup)' } else { $ts }
    } else { '  testsprite CLI not installed' }
    ''
    'Real usage today (ccusage, local logs):'
    $ru = Get-RealUsage (Get-Date -Format 'yyyyMMdd'); if ($ru) { $ru | Format-Table -AutoSize | Out-String } else { '  ccusage not installed' }
    'Note: tokens marked estimated=True are chars/4 approximations; only Codex reports real counts. Budgets are user-defined in budgets.json, not read from provider quotas.'
  }

  'delegate' {
    if (-not $Agent) { throw '-Agent required (codex|antigravity|kimi)' }
    if (-not $Prompt) { throw '-Prompt required' }
    $state = Get-BudgetState $Agent
    if ($state.State -eq 'EXHAUSTED') {
      Write-Output "BUDGET_EXHAUSTED: $Agent used $($state.Used)/$($state.Budget) tokens today. Reassign to: $(Get-Fallbacks $Agent)"
      exit 75
    }
    if ($state.State -in 'WARNING', 'CRITICAL') {
      Write-Warning "FINANCE: $Agent is at $($state.Pct)% of daily budget ($($state.State)). Consider fallback: $(Get-Fallbacks $Agent)"
    }

    $fullPrompt = $Prompt
    if ($Role) {
      $roleFile = Join-Path $Home_ "roles\$Agent\$Role.md"
      if (-not (Test-Path $roleFile)) { throw "Role file not found: $roleFile (see roles.md)" }
      $raw = Get-Content $roleFile -Raw -Encoding UTF8
      if ($raw -match '(?s)^---(.*?)---') { $fm = $Matches[1]; if (-not $Model -and $fm -match '(?m)^model:\s*(\S+)') { $Model = $Matches[1] }; if (-not $Effort -and $fm -match '(?m)^effort:\s*(\S+)') { $Effort = $Matches[1] } }
      $roleText = $raw -replace '(?s)^---.*?---\s*', ''
      $fullPrompt = "ROLE BRIEF:`n$roleText`n`nTASK:`n$Prompt`n`nEnd with a short report: what you did, files touched, what is unverified. Your report goes to a director for review."
      $Task = "[$Role] $Task"
    }
    $safePrompt = $fullPrompt -replace '"', "'"

    if ($Agent -eq 'local') {
      # Local model via Ollama REST API: free, private, real token counts.
      $model = if ($env:COMPANY_LOCAL_MODEL) { $env:COMPANY_LOCAL_MODEL } else { 'gemma3:12b' }
      $body = @{ model = $model; prompt = $fullPrompt; stream = $false; options = @{ num_ctx = 8192 } } | ConvertTo-Json -Depth 3
      $bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
      try {
        $r = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/generate' -Method Post -Body $bytes -ContentType 'application/json; charset=utf-8' -TimeoutSec ([Math]::Max($TimeoutSec, 600))
        $out = $r.response; $tokens = [int]$r.prompt_eval_count + [int]$r.eval_count; $status = 'ok'; $code = 0
      } catch {
        $out = "LOCAL_ERROR: $($_.Exception.Message) (is 'ollama serve' running and model '$model' pulled?)"; $tokens = 0; $status = 'error(local)'; $code = 1
      }
      Add-Ledger "local" $Department $Task $tokens 'False' $status
      $out
      $after = Get-BudgetState 'local'
      Write-Output "--- FINANCE: local ($model) $($after.Used) tokens today (free, untracked budget) ---"
      if ($code -ne 0) { exit $code }
      return
    }

    $exe = $null; $args_ = @()
    switch ($Agent) {
      'codex'       { $exe = Join-Path $env:LOCALAPPDATA 'Programs\OpenAI\Codex\bin\codex.exe'; $lastMsg = [IO.Path]::GetTempFileName(); $args_ = @('exec', '--skip-git-repo-check', '-o', $lastMsg); if ($Model) { $args_ += @('-m', $Model) }; if ($Effort) { $args_ += @('-c', "model_reasoning_effort=$Effort") }; $args_ += $safePrompt }
      'antigravity' { $exe = Join-Path $env:LOCALAPPDATA 'agy\bin\agy.exe'; $args_ = @('-p', $safePrompt, '--print-timeout', "${TimeoutSec}s"); if ($Model) { $args_ += @('--model', $Model) }; if ($Effort) { $args_ += @('--effort', $Effort) } }
      'kimi'        { $exe = Join-Path $env:USERPROFILE '.kimi-code\bin\kimi.exe'; $args_ = @('-p', $safePrompt) }
      default       { throw "Unknown agent '$Agent'. Claude agents are used directly, not via delegate." }
    }
    if (-not (Test-Path $exe)) { throw "Agent binary not found: $exe" }

    # Native stderr must not abort the script (PS 5.1 wraps it in ErrorRecords); empty stdin stops codex waiting for input.
    if ($Model -or $Effort) { $Task = "$Task {$Model/$Effort}" }
    $sw = [Diagnostics.Stopwatch]::StartNew()
    $ErrorActionPreference = 'Continue'
    $out = ($null | & $exe @args_ 2>&1 | ForEach-Object { "$_" }) -join "`n"
    $code = $LASTEXITCODE
    $ErrorActionPreference = 'Stop'

    $real = $null
    if ($Agent -eq 'codex' -and $out -match '(?m)^tokens used\s*\r?\n\s*(\d[\d\.,]*)\s*\r?$') {
      $real = [int](($Matches[1]) -replace '[\.,]', '')
    }
    $tokens = if ($null -ne $real) { $real } else { [int][math]::Ceiling(($safePrompt.Length + $out.Length) / 4.0) }
    $est = if ($null -ne $real) { 'False' } else { 'True' }
    $status = if ($code -eq 0) { 'ok' } else { "error($code)" }
    # Provider usage limit (Codex is on a non-paid plan): log, tell the CEO to reassign, exit 75 like an exhausted budget
    $limitHit = ($code -ne 0 -and $out -match '(?i)usage limit|rate.?limit|quota|RESOURCE_EXHAUSTED|\b429\b|too many requests') -or ($out -match '(?i)hit your usage limit|usage limit reached|QUOTA_EXHAUSTED')
    if ($limitHit) { $status = 'LIMIT' }
    Add-Ledger $Agent $Department $Task $tokens $est $status

    # Codex: print the clean final answer (stderr/stdout can interleave inside code blocks)
    if ($lastMsg -and (Test-Path $lastMsg) -and (Get-Item $lastMsg).Length -gt 0) { [IO.File]::ReadAllText($lastMsg); Remove-Item $lastMsg -ErrorAction SilentlyContinue } else { $out }
    $after = Get-BudgetState $Agent
    Write-Output "--- TIME: $([math]::Round($sw.Elapsed.TotalSeconds,1)) s; model: $(if ($Model) { $Model } else { 'default' }) effort: $(if ($Effort) { $Effort } else { 'default' }) ---"
    Write-Output "--- FINANCE: $Agent $($after.Used)/$($after.Budget) tokens today ($($after.Pct)%, $($after.State)) ---"
    if ($limitHit) { Write-Output "PROVIDER_LIMIT: $Agent hit its plan limit. Reassign to: $(Get-Fallbacks $Agent)"; exit 75 }
    if ($code -ne 0) { exit $code }
  }
}
