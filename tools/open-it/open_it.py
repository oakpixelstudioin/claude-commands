"""Open a file in the best app for its type.

  python open_it.py <path>            open that exact file
  python open_it.py                   open the newest file under the roots
  python open_it.py --ext html,pdf    newest file with one of these extensions
  python open_it.py --match keema     newest file whose name contains this
  python open_it.py --list            show the 10 newest, open nothing
  python open_it.py --root D:/x ...   scan these roots instead of the defaults
"""
import argparse, os, subprocess, sys, time
from pathlib import Path

HOME = Path.home()
CHROME = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
          r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
MPC = [r"C:\Program Files (x86)\K-Lite Codec Pack\MPC-HC64\mpc-hc64.exe",
       r"C:\Program Files\MPC-HC\mpc-hc64.exe"]
VSCODE = [str(HOME / r"AppData\Local\Programs\Microsoft VS Code\Code.exe"),
          r"C:\Program Files\Microsoft VS Code\Code.exe"]
SEVENZIP = [r"C:\Program Files\7-Zip\7zFM.exe"]

BROWSER = {".html", ".htm", ".pdf", ".svg", ".xhtml", ".mhtml"}
MEDIA = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v", ".wmv", ".flv", ".ts", ".mts",
         ".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".opus", ".wma"}
CODE = {".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".json", ".jsonl", ".md", ".txt",
        ".css", ".scss", ".yml", ".yaml", ".toml", ".ini", ".cfg", ".env", ".sh", ".ps1",
        ".bat", ".cmd", ".sql", ".csv", ".tsv", ".log", ".xml", ".srt", ".vtt", ".ass",
        ".gradle", ".properties", ".kt", ".java", ".c", ".cpp", ".h", ".go", ".rs", ".lua"}
ARCHIVE = {".zip", ".7z", ".rar", ".tar", ".gz", ".tgz", ".bz2", ".xz"}
# images, Office docs, .apk etc. -> Windows default association

SKIP_DIRS = {"node_modules", ".git", "__pycache__", ".venv", "venv", ".expo", ".gradle",
             ".next", ".cache", ".wrangler", "job-feed", "build", ".cxx", "intermediates"}
SKIP_SUFFIX = {".tmp", ".part", ".crdownload", ".lock", ".pyc", ".bak"}


def first(paths):
    return next((p for p in paths if Path(p).exists()), None)


def app_for(path: Path):
    """(label, argv) for this file; argv None = shell default association."""
    if path.is_dir():
        return "Explorer", ["explorer.exe", str(path)]
    ext = path.suffix.lower()
    if ext in BROWSER and (exe := first(CHROME)):
        return "Chrome", [exe, path.resolve().as_uri()]
    if ext in MEDIA and (exe := first(MPC)):
        return "Media Player Classic", [exe, str(path)]
    if ext in CODE and (exe := first(VSCODE)):
        return "VS Code", [exe, str(path)]
    if ext in ARCHIVE and (exe := first(SEVENZIP)):
        return "7-Zip", [exe, str(path)]
    return "default app", None


def stamp(st):
    # "created" on Windows = st_ctime; also count rewrites of an existing file
    return max(st.st_ctime, st.st_mtime)


def walk(root: Path, depth=8):
    stack = [(root, 0)]
    while stack:
        d, lvl = stack.pop()
        try:
            it = os.scandir(d)
        except OSError:
            continue
        with it:
            for e in it:
                try:
                    if e.is_dir(follow_symlinks=False):
                        if lvl < depth and e.name not in SKIP_DIRS and not e.name.startswith("$"):
                            stack.append((Path(e.path), lvl + 1))
                    elif e.is_file():
                        if Path(e.name).suffix.lower() in SKIP_SUFFIX or e.name.startswith("~$"):
                            continue
                        yield Path(e.path), stamp(e.stat())
                except OSError:
                    continue


def default_roots():
    roots = [Path.cwd(), HOME / "Downloads", HOME / "Desktop"]
    seen, out = set(), []
    for r in roots:
        k = str(r.resolve()).lower()
        if r.exists() and k not in seen:
            seen.add(k); out.append(r)
    return out


def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB":
            return f"{n:.0f} {u}" if u == "B" else f"{n:.1f} {u}"
        n /= 1024


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?")
    ap.add_argument("--ext", help="comma list, e.g. html,pdf")
    ap.add_argument("--match", help="substring of the file name")
    ap.add_argument("--root", nargs="+")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()

    if a.path:
        target = Path(a.path).expanduser()
        if not target.exists():
            sys.exit(f"not found: {target}")
    else:
        roots = [Path(r) for r in a.root] if a.root else default_roots()
        exts = {"." + e.strip().lstrip(".").lower() for e in a.ext.split(",")} if a.ext else None
        cands = []
        for r in roots:
            for p, t in walk(r):
                if exts and p.suffix.lower() not in exts:
                    continue
                if a.match and a.match.lower() not in p.name.lower():
                    continue
                cands.append((t, p))
        cands.sort(reverse=True)
        if not cands:
            sys.exit("no matching files under: " + ", ".join(map(str, roots)))
        if a.list:
            for t, p in cands[:10]:
                print(f"{time.strftime('%Y-%m-%d %H:%M', time.localtime(t))}  "
                      f"{human(p.stat().st_size):>9}  {app_for(p)[0]:<20}  {p}")
            return
        target = cands[0][1]

    label, argv = app_for(target)
    if argv:
        subprocess.Popen(argv, close_fds=True,
                         creationflags=getattr(subprocess, "DETACHED_PROCESS", 0))
    else:
        os.startfile(str(target))
    st = target.stat()
    print(f"opened in {label}: {target}  "
          f"({human(st.st_size)}, {time.strftime('%Y-%m-%d %H:%M', time.localtime(stamp(st)))})")


if __name__ == "__main__":
    main()
