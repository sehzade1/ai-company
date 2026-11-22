# Starts the local ComfyUI server (FLUX image generation) if it is not already running. Localhost only.
$api = 'http://127.0.0.1:8188'
try { Invoke-RestMethod "$api/system_stats" -TimeoutSec 3 | Out-Null; "ComfyUI already running at $api"; exit 0 } catch {}
$root = 'D:\AI\ComfyUI_windows_portable'
Start-Process -FilePath "$root\python_embeded\python.exe" -ArgumentList '-s', 'ComfyUI\main.py', '--windows-standalone-build', '--listen', '127.0.0.1', '--port', '8188', '--disable-auto-launch' -WorkingDirectory $root -WindowStyle Hidden -RedirectStandardOutput 'D:\AI\comfyui-server.log' -RedirectStandardError 'D:\AI\comfyui-server.err.log'
for ($i = 0; $i -lt 60; $i++) { Start-Sleep -Seconds 2; try { Invoke-RestMethod "$api/system_stats" -TimeoutSec 3 | Out-Null; "ComfyUI started at $api"; exit 0 } catch {} }
"ComfyUI did not start within 120 s; see D:\AI\comfyui-server.err.log"; exit 1
