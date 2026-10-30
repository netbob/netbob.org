#!/usr/bin/env python3
"""Fetch The Shattered Lens chapters into _lens/ at build time.

Run from the netbob.org repo root, or prepended to the Cloudflare Pages
build command:  python3 tools/fetch-lens.py && <existing build command>

Clones the public Lens repo (shallow), copies chapters/*/module-*.md into
_lens/ preserving the chapter directories, and injects the YAML front
matter Jekyll needs to render each module as a page. _lens/ is git-ignored
build output, never committed.

Resilience: if the Lens repo cannot be reached, this exits 0 with a
warning and leaves _lens/ absent. The Books tab then falls back to linking
the GitHub repository instead of failing the whole site build.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = "https://github.com/netbob/The-Shattered-Lens.git"
ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "_lens"
TMP = ROOT / ".lens-clone"


def main() -> int:
    shutil.rmtree(DEST, ignore_errors=True)
    shutil.rmtree(TMP, ignore_errors=True)
    try:
        subprocess.run(
            ["git", "clone", "--depth", "1", REPO, str(TMP)],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"fetch-lens: WARNING: could not clone Lens repo ({exc}); "
              "site will link GitHub instead.", file=sys.stderr)
        return 0

    count = 0
    for chapter_dir in sorted((TMP / "chapters").glob("chapter-*")):
        for src in sorted(chapter_dir.glob("module-*.md")):
            text = src.read_text(encoding="utf-8")
            # Module title: prefer a "Module NX:" heading at any level.
            # Chapter 1 files uniquely use H1 act / H2 chapter / H3 module
            # headers, so "first H1" would wrongly yield the act name for
            # all five of them. Other chapters use H1 module headings.
            m = re.search(r"^#{1,3} (Module \d+[A-E]:.+)$", text, re.M)
            if m is None:
                m = re.match(r"^# (.+)\n", text)
            title = m.group(1).strip() if m else src.stem
            title = title.replace('"', "'")
            try:
                chapter_no = int(chapter_dir.name.split("-")[1])
            except (IndexError, ValueError):
                chapter_no = 0
            front_matter = (
                "---\n"
                f'title: "{title}"\n'
                "layout: page\n"
                "toc: false\n"
                f"chapter: {chapter_no}\n"
                "---\n\n"
            )
            out = DEST / chapter_dir.name / src.name
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(front_matter + text, encoding="utf-8")
            count += 1
    shutil.rmtree(TMP, ignore_errors=True)
    print(f"fetch-lens: fetched {count} Lens modules into _lens/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
