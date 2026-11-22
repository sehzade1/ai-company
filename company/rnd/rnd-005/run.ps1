param([string]$Dir)
$co = Join-Path $env:USERPROFILE '.claude\company\company.ps1'
$arms = foreach ($e in 'low','medium','high') { @{ e=$e; t='H1'; r='bug-finder' }; @{ e=$e; t='H2'; r='code-reviewer' } }
$jobs = foreach ($x in $arms) {
  Start-Job -ArgumentList $co, $Dir, $x.e, $x.t, $x.r -ScriptBlock {
    param($co, $Dir, $e, $t, $r)
    $p = Get-Content (Join-Path $Dir "$t.txt") -Raw -Encoding UTF8
    & $co delegate -Agent codex -Department rnd -Task "rnd-005 $t" -Role $r -Model 'gpt-6-luna' -Effort $e -Prompt $p *> (Join-Path $Dir "out-$t-$e.txt")
  }
}
$jobs | Wait-Job -Timeout 1200 | Out-Null