param([string]$Dir)
$co = Join-Path $env:USERPROFILE '.claude\company\company.ps1'
$arms = @()
foreach ($m in 'gpt-6-luna','gpt-5.6-terra','gpt-5.6-luna') {
  $arms += @{ a='codex'; m=$m; e='medium'; t='C1'; r='bug-finder' }
  $arms += @{ a='codex'; m=$m; e='medium'; t='C2'; r='backend-developer' }
}
foreach ($m in 'gemini-4-hydrogen-high','gemini-4-argon-high','gemini-4-neon-high','gemini-3.8-flash-medium') {
  $arms += @{ a='antigravity'; m=$m; e=''; t='A1'; r='data-analyst' }
  $arms += @{ a='antigravity'; m=$m; e=''; t='A2'; r='translator' }
}
$jobs = foreach ($x in $arms) {
  Start-Job -ArgumentList $co, $Dir, $x.a, $x.m, $x.e, $x.t, $x.r -ScriptBlock {
    param($co, $Dir, $a, $m, $e, $t, $r)
    $p = Get-Content (Join-Path $Dir "$t.txt") -Raw -Encoding UTF8
    $out = Join-Path $Dir "out-$t-$m.txt"
    & $co delegate -Agent $a -Department rnd -Task "rnd-004 $t" -Role $r -Model $m -Effort $e -Prompt $p -TimeoutSec 300 *> $out
  }
}
$jobs | Wait-Job -Timeout 1200 | Out-Null
Get-ChildItem $Dir -Filter 'out-*.txt' | ForEach-Object { '{0} {1}B' -f $_.Name, $_.Length }
