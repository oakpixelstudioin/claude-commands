# Claude Code slash commands

A collection of user-level slash commands for [Claude Code](https://claude.com/claude-code).
Each command is one Markdown file; commands that need a helper script carry it in a
matching folder under `tools/`.

## Commands

| Command | What it does |
|---|---|
| [`/open-it`](commands/open-it.md) | Opens the most recently created file in the best app for its type |

## Install (Windows)

```powershell
git clone https://github.com/oakpixelstudioin/claude-commands
cd claude-commands
powershell -ExecutionPolicy Bypass -File install.ps1            # all commands
powershell -ExecutionPolicy Bypass -File install.ps1 open-it    # just one
powershell -ExecutionPolicy Bypass -File install.ps1 -List      # see what's here
```

Commands land in `~/.claude/commands/`, helper scripts in `~/.claude/tools/<command>/`.
Re-run the installer after `git pull` to update.

## Layout

```
commands/
  open-it.md          the slash command (prompt + frontmatter)
  _template.md        starting point for a new command (not installed)
tools/
  open-it/            helper scripts for /open-it
install.ps1
```

## Adding a command

1. Copy `commands/_template.md` to `commands/<name>.md`.
2. If it needs a script, add `tools/<name>/` and reference it as `~/.claude/tools/<name>/...`.
3. Add a row to the table above.
4. Never commit secrets, API keys, personal paths or emails; read keys from env vars or a secret manager at run time.

---

## /open-it

| File type | Opens in |
|---|---|
| `.html` `.htm` `.pdf` `.svg` | Google Chrome |
| Video & audio | Media Player Classic (MPC-HC) |
| Code, text, JSON, Markdown, CSV, subtitles | VS Code |
| Archives | 7-Zip |
| Folders | Explorer |
| Images, Office docs, anything else | Windows default app |

Falls back to the Windows default association when a preferred app isn't installed.

```
/open-it                 newest file (the one Claude just created, else newest on disk)
/open-it html            newest of a type (html, pdf, video, audio, image, or an extension)
/open-it keema           newest file whose name contains "keema"
/open-it <path>          that exact file
/open-it --list          show the 10 newest, open nothing
```

Without a target it scans the current directory (recursively, skipping `node_modules`,
`.git` and build caches), Downloads and Desktop. Requires Python 3.8+.

## License

MIT
