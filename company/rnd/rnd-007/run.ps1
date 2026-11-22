param([string]$Dir)
$co = Join-Path $env:USERPROFILE '.claude\company\company.ps1'
$spec = Get-Content (Join-Path $Dir 'spec.tsv') -Encoding UTF8 | % { $k,$v = $_ -split "`t",2; [pscustomobject]@{ k=$k; v=$v } }
$common = 'Use the Blender 5.1 Python API (bpy), run headless with --background. Build the model procedurally (no downloads, no add-ons), with simple materials (Principled BSDF). Export a .glb and render a 1024x1024 PNG preview: three-quarter view, soft studio lighting, neutral light grey background, the object filling most of the frame. At the end print the triangle count and object dimensions.'
$jobs = foreach ($s in $spec) {
  $agyDir = Join-Path $Dir 'agy'
  $pA = "Model: $($s.v). $common Write the script to $agyDir\$($s.k).py, set it to export $agyDir\$($s.k).glb and render $agyDir\$($s.k).png, then run it with: & 'C:\Program Files\Blender Foundation\Blender 5.1\blender.exe' --background --python $agyDir\$($s.k).py . Fix errors and rerun until both files exist. If you are not allowed to run Blender, say so and still write the script."
  Start-Job -ArgumentList $co,$Dir,$s.k,$pA -ScriptBlock { param($co,$Dir,$k,$p) & $co delegate -Agent antigravity -Department rnd -Task "rnd-007 $k" -Role 3d-modeler -Prompt $p -TimeoutSec 900 *> (Join-Path $Dir "out-agy-$k.txt") }
  $cDir = Join-Path $Dir 'codex'
  $pC = "Write a complete Blender Python script. Model: $($s.v). $common Hard-code these output paths: GLB = r'$cDir\$($s.k).glb', PNG = r'$cDir\$($s.k).png'. Your sandbox is read-only and you cannot run Blender, so check the API carefully. Reply with the full script in ONE python code block, then a 3-line report."
  Start-Job -ArgumentList $co,$Dir,$s.k,$pC -ScriptBlock { param($co,$Dir,$k,$p) & $co delegate -Agent codex -Department rnd -Task "rnd-007 $k" -Model gpt-6-luna -Effort medium -Prompt $p *> (Join-Path $Dir "out-codex-$k.txt") }
}
$jobs | Wait-Job -Timeout 1800 | Out-Null