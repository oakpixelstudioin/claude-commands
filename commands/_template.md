---
description: One line shown in the slash-command menu
argument-hint: [what the user can pass]
allowed-tools: Bash, PowerShell, Read
---

What this command does with `$ARGUMENTS`.

If it needs a helper script, put it in `tools/<command-name>/` and call it as
`python ~/.claude/tools/<command-name>/<script>.py` — install.ps1 copies that
folder there.
