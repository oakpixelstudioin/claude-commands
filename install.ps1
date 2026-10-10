# Installs the /open-it command for Claude Code (user-level, all projects).
$dst = Join-Path $HOME '.claude'
New-Item -ItemType Directory -Force (Join-Path $dst 'commands'), (Join-Path $dst 'open-it') | Out-Null
Copy-Item "$PSScriptRoot\commands\open-it.md" (Join-Path $dst 'commands\open-it.md') -Force
Copy-Item "$PSScriptRoot\open-it\open_it.py" (Join-Path $dst 'open-it\open_it.py') -Force
Write-Host "Installed /open-it to $dst - restart Claude Code to pick it up."
