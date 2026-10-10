---
description: Open the most recently created file in the best app for it (HTML/PDF → Chrome, video/audio → Media Player Classic, code/text → VS Code, else Windows default)
argument-hint: [path | name fragment | html|pdf|video|...] [--list]
allowed-tools: Bash, PowerShell
---

Open a file for the user. Target: `$ARGUMENTS` (empty = the most recent file).

This only **opens** — never edits, moves, renders or deletes anything.

## 1. Pick the file

In this order:

1. **A path** in the arguments → that exact file.
2. **No arguments and you created or wrote a file earlier in this conversation**
   (Write, a script output, a render, a download) → the latest one of those.
   That is what "the most recently created file" means to the user.
3. Otherwise scan with the helper:
   - no argument → `python ~/.claude/tools/open-it/open_it.py`
   - a type word → `--ext`: `html`→`html,htm`, `pdf`, `video`→`mp4,mov,mkv,webm`,
     `audio`→`mp3,wav,m4a,flac`, `image`→`png,jpg,jpeg,webp,gif`, or the literal extension
   - a name fragment (`keema`, `brochure`) → `--match <fragment>`
   - `--list` → print the 10 newest and stop; open nothing.

   Default roots are the current working directory (recursive, skipping
   node_modules/.git/build caches), Downloads and Desktop. If the file is likely
   in one of the session's additional working directories, pass
   `--root "<dir>" ...` instead.

If the newest candidate is clearly an intermediate (temp, partial, a file still
growing because a render/download is running), show `--list` and ask with
AskUserQuestion options instead of guessing.

## 2. Open it

Always open through the helper so the app choice is consistent:

```bash
python ~/.claude/tools/open-it/open_it.py "<full path>"
```

App map (in `open_it.py`): `.html/.htm/.pdf/.svg` → Chrome · video & audio →
Media Player Classic (K-Lite MPC-HC64) · code, text, JSON, Markdown, CSV,
subtitles → VS Code · archives → 7-Zip · folders → Explorer · images, Office
docs and everything else → the Windows default association. If the user names
an app ("open it in firefox"), launch that exe with the path instead.

## 3. Report

One line: file name, which app, size and time — the helper prints it.
