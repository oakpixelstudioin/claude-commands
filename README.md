# /open-it — a Claude Code slash command

Opens the most recently created file in the best app for its type.

| File type | Opens in |
|---|---|
| `.html` `.htm` `.pdf` `.svg` | Google Chrome |
| Video & audio | Media Player Classic (MPC-HC) |
| Code, text, JSON, Markdown, CSV, subtitles | VS Code |
| Archives | 7-Zip |
| Folders | Explorer |
| Images, Office docs, anything else | Windows default app |

If a preferred app isn't installed, it falls back to the Windows default association.

## Usage

```
/open-it                 newest file (the one Claude just created, else newest on disk)
/open-it html            newest file of a type (html, pdf, video, audio, image, or an extension)
/open-it keema           newest file whose name contains "keema"
/open-it <path>          that exact file
/open-it --list          show the 10 newest, open nothing
```

Without a target it scans the current working directory (recursively, skipping
`node_modules`, `.git` and build caches), Downloads and Desktop.

The helper also works on its own:

```
python ~/.claude/open-it/open_it.py [path] [--ext html,pdf] [--match name] [--root DIR ...] [--list]
```

## Install (Windows)

```powershell
git clone https://github.com/oakpixelstudioin/claude-open-it
powershell -ExecutionPolicy Bypass -File claude-open-it\install.ps1
```

Requires Python 3.8+. Windows only (uses `os.startfile` and Windows app paths).

## License

MIT
