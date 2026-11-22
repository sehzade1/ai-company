<#
.SYNOPSIS
  Generate an image locally with ComfyUI + FLUX.1-schnell (fp8). Free, no quota, nothing leaves this machine.
.EXAMPLE
  comfy-generate.ps1 -Prompt "flat vector logo of a coffee cup, white background" -Out D:\out\logo.png -Width 1024 -Height 1024
.NOTES
  Requires the ComfyUI server: D:\AI\ComfyUI_windows_portable (start with start-comfyui.ps1). Logs usage to the company ledger as agent 'local-image' (tokens = 0, one row per image).
#>
param(
  [Parameter(Mandatory = $true)][string]$Prompt,
  [Parameter(Mandatory = $true)][string]$Out,
  [int]$Width = 1024,
  [int]$Height = 1024,
  [int]$Steps = 4,
  [long]$Seed = -1,
  [string]$Department = 'creative',
  [string]$Task = 'local image',
  [int]$TimeoutSec = 600
)
$ErrorActionPreference = 'Stop'
$api = 'http://127.0.0.1:8188'
if ($Seed -lt 0) { $Seed = Get-Random -Minimum 1 -Maximum 2147483647 }

try { Invoke-RestMethod "$api/system_stats" -TimeoutSec 5 | Out-Null } catch { Write-Output "LOCAL_IMAGE_ERROR: ComfyUI server not running on $api. Start it with {{HOME}}\.claude\company\tools\start-comfyui.ps1"; exit 1 }

$wf = @{
  '1' = @{ class_type = 'CheckpointLoaderSimple'; inputs = @{ ckpt_name = 'flux1-schnell-fp8.safetensors' } }
  '2' = @{ class_type = 'CLIPTextEncode'; inputs = @{ text = $Prompt; clip = @('1', 1) } }
  '3' = @{ class_type = 'CLIPTextEncode'; inputs = @{ text = ''; clip = @('1', 1) } }
  '4' = @{ class_type = 'EmptySD3LatentImage'; inputs = @{ width = $Width; height = $Height; batch_size = 1 } }
  '5' = @{ class_type = 'KSampler'; inputs = @{ model = @('1', 0); positive = @('2', 0); negative = @('3', 0); latent_image = @('4', 0); seed = $Seed; steps = $Steps; cfg = 1.0; sampler_name = 'euler'; scheduler = 'simple'; denoise = 1.0 } }
  '6' = @{ class_type = 'VAEDecode'; inputs = @{ samples = @('5', 0); vae = @('1', 2) } }
  '7' = @{ class_type = 'SaveImage'; inputs = @{ images = @('6', 0); filename_prefix = 'company' } }
}
$body = @{ prompt = $wf; client_id = [guid]::NewGuid().ToString() } | ConvertTo-Json -Depth 10
$sw = [Diagnostics.Stopwatch]::StartNew()
$resp = Invoke-RestMethod "$api/prompt" -Method Post -Body ([Text.Encoding]::UTF8.GetBytes($body)) -ContentType 'application/json; charset=utf-8'
$id = $resp.prompt_id

$img = $null
while ($sw.Elapsed.TotalSeconds -lt $TimeoutSec) {
  Start-Sleep -Seconds 2
  $h = Invoke-RestMethod "$api/history/$id"
  $entry = $h.$id
  if ($entry) {
    if ($entry.status.status_str -eq 'error') { Write-Output "LOCAL_IMAGE_ERROR: ComfyUI reported an error: $($entry.status.messages | ConvertTo-Json -Depth 5 -Compress)"; exit 1 }
    $img = $entry.outputs.'7'.images | Select-Object -First 1
    if ($img) { break }
  }
}
if (-not $img) { Write-Output "LOCAL_IMAGE_ERROR: timed out after $TimeoutSec s"; exit 1 }

$dir = Split-Path -Parent $Out
if ($dir) { New-Item -ItemType Directory -Force $dir | Out-Null }
$q = "filename=$([uri]::EscapeDataString($img.filename))&subfolder=$([uri]::EscapeDataString($img.subfolder))&type=$($img.type)"
Invoke-WebRequest "$api/view?$q" -OutFile $Out -UseBasicParsing
$sec = [math]::Round($sw.Elapsed.TotalSeconds, 1)

# Finance: one ledger row per image (free, 0 tokens)
$ledger = Join-Path $env:USERPROFILE '.claude\company\ledger.csv'
$t = ($Task -replace '[",\r\n]', ' ')
$line = '{0},local-image,{1},"{2}",0,False,ok' -f (Get-Date -Format 'yyyy-MM-ddTHH:mm:ss'), $Department, $t
for ($i = 0; $i -lt 20; $i++) { try { Add-Content -Encoding UTF8 $ledger $line -ErrorAction Stop; break } catch { Start-Sleep -Milliseconds 200 } }

Write-Output "OK: $Out (${Width}x${Height}, seed $Seed, $sec s)"
