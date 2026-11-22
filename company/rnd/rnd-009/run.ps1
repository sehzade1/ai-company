param([string]$Dir)
$co = Join-Path $env:USERPROFILE '.claude\company\company.ps1'
$roles = @{ G1='data-analyst'; G2='data-analyst'; G3='researcher'; G4='translator' }
$jobs = foreach ($m in 'gemini-4-hydrogen-high','gemini-4-neon-high','gemini-3.8-flash-medium') { foreach ($t in 'G1','G2','G3','G4') {
  Start-Job -ArgumentList $co,$Dir,$m,$t,$roles[$t] -ScriptBlock { param($co,$Dir,$m,$t,$r)
    $p = (Get-Content (Join-Path $Dir "$t.txt") -Raw -Encoding UTF8) + "`nAnswer directly in your reply. Do not create or write any files."
    & $co delegate -Agent antigravity -Department rnd -Task "rnd-009 $t" -Role $r -Model $m -Prompt $p -TimeoutSec 600 *> (Join-Path $Dir "out-$t-$m.txt") }
} }
$jobs | Wait-Job -Timeout 1800 | Out-Null