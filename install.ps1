# Installs slash commands from this repo into Claude Code (user level, all projects).
#   .\install.ps1              install every command
#   .\install.ps1 open-it      install only the named command(s)
#   .\install.ps1 -List        show what's available
param([string[]]$Names, [switch]$List)

$src = $PSScriptRoot
$dst = Join-Path $HOME '.claude'
$all = Get-ChildItem (Join-Path $src 'commands') -Filter *.md |
  Where-Object { $_.BaseName -ne '_template' } | ForEach-Object BaseName

if ($List) { $all; return }
if (-not $Names) { $Names = $all }

New-Item -ItemType Directory -Force (Join-Path $dst 'commands'), (Join-Path $dst 'tools') | Out-Null
foreach ($n in $Names) {
  $md = Join-Path $src "commands\$n.md"
  if (-not (Test-Path $md)) { Write-Warning "no such command: $n"; continue }
  Copy-Item $md (Join-Path $dst "commands\$n.md") -Force
  $tool = Join-Path $src "tools\$n"
  if (Test-Path $tool) {
    $to = Join-Path $dst "tools\$n"
    New-Item -ItemType Directory -Force $to | Out-Null
    Copy-Item (Join-Path $tool '*') $to -Recurse -Force
  }
  Write-Host "installed /$n"
}
Write-Host "Restart Claude Code (or open a new session) to pick them up."
