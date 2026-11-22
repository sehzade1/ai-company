param([string]$Dir)
$co = Join-Path $env:USERPROFILE '.claude\company\company.ps1'
$method = [IO.File]::ReadAllText((Join-Path $env:USERPROFILE '.claude\skills\systematic-debugging\SKILL.md')) -replace '(?s)^---.*?---\s*',''
$jobs = foreach ($t in 'D1','D2') { foreach ($arm in 'base','method') { foreach ($rep in 1,2) {
  Start-Job -ArgumentList $co,$Dir,$t,$arm,$rep,$method -ScriptBlock { param($co,$Dir,$t,$arm,$rep,$method)
    $p = [IO.File]::ReadAllText((Join-Path $Dir "$t.txt"))
    if ($arm -eq 'method') { $p = "Follow this debugging method strictly before you answer:`n`n$method`n`n---`n`n$p" }
    & $co delegate -Agent antigravity -Department rnd -Task "rnd-010 $t $arm $rep" -Model gemini-4-hydrogen-high -Prompt $p -TimeoutSec 600 *> (Join-Path $Dir "out-$t-$arm-$rep.txt") }
} } }
$jobs | Wait-Job -Timeout 1800 | Out-Null