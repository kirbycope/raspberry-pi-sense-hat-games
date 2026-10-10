"""Gathers the web version into one folder, ready to serve.

    python web/build.py site
    python -m http.server -d site     # then open http://localhost:8000

Copies the page and its worker, the simulator's sense_hat package, the games'
Python files and the images they load, and writes files.json, the list the
worker fetches. GitHub Actions runs the same thing to publish GitHub Pages.
"""

import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Everything the games read at run time, relative to the repository's top.
GAME_FILES = ["simulator/sense_hat", "spaceInvaders", "legendOfZelda"]
KEEP = (".py", ".bmp")


def main():
    out = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "site")
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    for name in ("index.html", "worker.js"):
        shutil.copy(os.path.join(ROOT, "web", name), out)
    files = []
    for top in GAME_FILES:
        for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, top)):
            dirnames[:] = [d for d in dirnames if d != "__pycache__"]
            for f in sorted(filenames):
                if not f.endswith(KEEP):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, f), ROOT).replace(os.sep, "/")
                os.makedirs(os.path.join(out, os.path.dirname(rel)), exist_ok=True)
                shutil.copy(os.path.join(ROOT, rel), os.path.join(out, rel))
                files.append(rel)
    with open(os.path.join(out, "files.json"), "w") as f:
        json.dump(files, f)
    print(f"{len(files)} files into {out}")


if __name__ == "__main__":
    main()
