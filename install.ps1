<#
.SYNOPSIS
  Installs the AI company into %USERPROFILE%\.claude for Claude Code (Windows, PowerShell 5.1+).
  Existing files are backed up to %USERPROFILE%\.claude\backup-<timestamp> before being replaced.
#>
$ErrorActionPreference = 'Stop'
$src = $PSScriptRoot
$dst = Join-Path $env:USERPROFILE '.claude'
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backup = Join-Path $dst "backup-$stamp"
$utf8 = New-Object Text.UTF8Encoding $false

function Copy-Tree($from, $to) {
  Get-ChildItem $from -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($from.Length).TrimStart('\')
    $target = Join-Path $to $rel
    if (Test-Path $target) {
      $b = Join-Path $backup ($target.Substring($dst.Length).TrimStart('\'))
      New-Item -ItemType Directory -Force (Split-Path $b) | Out-Null
      Copy-Item $target $b -Force
    }
    New-Item -ItemType Directory -Force (Split-Path $target) | Out-Null
    if ($_.Extension -in '.md', '.ps1', '.py', '.json', '.txt', '.csv', '.tsv', '.js') {
      # {{HOME}} placeholders become this machine's user profile path
      $text = [IO.File]::ReadAllText($_.FullName).Replace('{{HOME}}', $env:USERPROFILE)
      $enc = if ($_.Extension -eq '.ps1') { New-Object Text.UTF8Encoding $true } else { $utf8 }
      [IO.File]::WriteAllText($target, $text, $enc)
    } else { Copy-Item $_.FullName $target -Force }
  }
}

New-Item -ItemType Directory -Force $dst | Out-Null
Copy-Tree (Join-Path $src 'claude') $dst
Copy-Tree (Join-Path $src 'company') (Join-Path $dst 'company')

Write-Output "Installed to $dst"
if (Test-Path $backup) { Write-Output "Replaced files were backed up to $backup" }
Write-Output "Next: set real daily budgets in $dst\company\budgets.json, install the agent CLIs you want (see README), restart Claude Code."
