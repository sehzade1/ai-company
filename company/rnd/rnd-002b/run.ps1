param([string]$Dir)
$co = Join-Path $env:USERPROFILE '.claude\company\company.ps1'
$tools = Join-Path $env:USERPROFILE '.claude\company\tools'
$briefs = Get-Content (Join-Path $Dir 'briefs.tsv') -Encoding UTF8 | % { $k,$v = $_ -split "`t",2; [pscustomobject]@{ k=$k; v=$v } }
$log = Join-Path $Dir 'run.log'
# 1) local FLUX (4 images), then stop ComfyUI to free memory
& (Join-Path $tools 'start-comfyui.ps1') *>> $log
foreach ($b in $briefs) {
  & (Join-Path $tools 'comfy-generate.ps1') -Prompt ("Illustration, not a photo. " + $b.v) -Out (Join-Path $Dir "img\$($b.k)-flux.png") -Width 1344 -Height 768 -Department rnd -Task "rnd-002b $($b.k) flux" *>> $log
}
Get-CimInstance Win32_Process -Filter "Name='python.exe'" | ? { $_.CommandLine -like '*ComfyUI\main.py*' } | % { Stop-Process -Id $_.ProcessId -Force }
"comfyui stopped" | Add-Content $log
# 2) Antigravity, strictly one image call at a time
foreach ($b in $briefs) {
  foreach ($r in 'image-generator','image-illustration','rnd-image-sections') {
    $out = Join-Path $Dir "img\$($b.k)-$r.png"
    if (Test-Path $out) { continue }
    $p = "$($b.v) Wide 16:9. Save exactly one PNG file to this path: $out"
    "=== $($b.k) $r $(Get-Date -Format HH:mm:ss)" | Add-Content $log
    & $co delegate -Agent antigravity -Department rnd -Task "rnd-002b $($b.k)" -Role $r -Prompt $p -TimeoutSec 600 *>> $log
    if ($LASTEXITCODE -eq 75) { "budget exhausted" | Add-Content $log; break }
    if ((Get-Content $log -Raw) -match 'RESOURCE_EXHAUSTED') { "QUOTA HIT, stopping" | Add-Content $log; exit 2 }
  }
}
"ALL DONE" | Add-Content $log