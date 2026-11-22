param([string]$Dir)
$co = Join-Path $env:USERPROFILE '.claude\company\company.ps1'
$vr = Join-Path $env:USERPROFILE '.claude\company\work\vendor-review\wshobson'
$ws = @{ H1 = 'plugins_comprehensive-review_agents_code-reviewer.md'; H2 = 'plugins_comprehensive-review_agents_security-auditor.md' }
$ours = @{ H1 = 'bug-finder'; H2 = 'code-reviewer' }
$arms = @()
foreach ($t in 'H1','H2') { foreach ($rep in 1,2) { $arms += @{ t=$t; arm='wshobson'; rep=$rep } }; $arms += @{ t=$t; arm='ours'; rep=1 } }
$jobs = foreach ($a in $arms) {
  Start-Job -ArgumentList $co,$Dir,$vr,$a.t,$a.arm,$a.rep,$ws[$a.t],$ours[$a.t] -ScriptBlock { param($co,$Dir,$vr,$t,$arm,$rep,$wsFile,$ourRole)
    $task = [IO.File]::ReadAllText((Join-Path $Dir "$t.txt"))
    $out = Join-Path $Dir "out-$t-$arm-$rep.txt"
    if ($arm -eq 'wshobson') {
      $brief = [IO.File]::ReadAllText((Join-Path $vr $wsFile)) -replace '(?s)^---.*?---\s*',''
      $p = "ROLE BRIEF:`n$brief`n`nTASK:`n$task`n`nYour sandbox is read-only. End with a short report."
      & $co delegate -Agent codex -Department rnd -Task "rnd-011 $t $arm $rep" -Model gpt-6-luna -Effort medium -Prompt $p *> $out
    } else {
      & $co delegate -Agent codex -Department rnd -Task "rnd-011 $t $arm $rep" -Role $ourRole -Model gpt-6-luna -Effort medium -Prompt $task *> $out
    } }
}
$jobs | Wait-Job -Timeout 1800 | Out-Null