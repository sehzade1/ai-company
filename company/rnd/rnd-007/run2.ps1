param([string]$Dir)
$co = Join-Path $env:USERPROFILE '.claude\company\company.ps1'
$spec = Get-Content (Join-Path $Dir 'spec.tsv') -Encoding UTF8 | % { $k,$v = $_ -split "`t",2; [pscustomobject]@{ k=$k; v=$v } }
$common = 'Use the Blender 5.1 Python API (bpy), run headless with --background. Build the model procedurally (no downloads, no add-ons), with simple materials (Principled BSDF). Export a .glb and render a 1024x1024 PNG preview: three-quarter view, soft studio lighting, neutral light grey background, the object filling most of the frame. At the end print the triangle count and object dimensions.'
$jobs = foreach ($s in $spec) {
  $aDir = Join-Path $Dir 'agy'
  $p = "Write a complete Blender Python script. Model: $($s.v). $common Hard-code these output paths: GLB = r'$aDir\$($s.k).glb', PNG = r'$aDir\$($s.k).png'. Do NOT create or write any files yourself and do not run anything: the CEO saves and runs the script. Check the API carefully. Reply with the full script in ONE python code block, then a 3-line report."
  Start-Job -ArgumentList $co,$Dir,$s.k,$p -ScriptBlock { param($co,$Dir,$k,$p) & $co delegate -Agent antigravity -Department rnd -Task "rnd-007 $k script" -Role 3d-modeler -Prompt $p -TimeoutSec 900 *> (Join-Path $Dir "out-agy-$k.txt") }
}
$jobs | Wait-Job -Timeout 1800 | Out-Null