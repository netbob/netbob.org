#!/usr/bin/env python3
"""Fetch The Shattered Lens chapters into _lens/ at build time.

Run from the netbob.org repo root, or prepended to the Cloudflare Pages
build command:  python3 tools/fetch-lens.py && <existing build command>

Clones the public Lens repo (shallow), copies chapters/*/module-*.md into
_lens/ preserving the chapter directories, and injects the YAML front
matter Jekyll needs to render each module as a page. _lens/ is git-ignored
build output, never committed.

The heading line that supplies the front-matter title is removed from the
body, so the rendered page shows the title once (from front matter)
instead of twice (front matter + body heading). Chapter 1 files keep
their H1 act / H2 chapter headers; only the H3 module-title line is
removed, since that is the line the title came from.

Chapters 2-12 files carry no act or chapter header lines (the filing
rule strips them), so the script injects them at build time from the
act/chapter table below, mirroring Chapter 1's on-page structure: an
H1 act line and an H2 chapter line above the prose. Chapter 1 files
already carry those lines, so they are left untouched. The manuscript
files are never modified; every change happens in the fetched copy.

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

# Act/chapter headers, from outline.md (bare act names, matching Chapter
# 1's on-page style; the outline's parenthetical act subtitles are not
# used). Keyed by chapter number parsed from the directory name.
ACT_CHAPTER = {
    1: ("Act I: The Logic Loop", "Chapter 1: The Ephemeris Error"),
    2: ("Act I: The Logic Loop", "Chapter 2: The Dying of the Keys"),
    3: ("Act I: The Logic Loop", "Chapter 3: The Ash Migration"),
    4: ("Act II: The Great Disconnection", "Chapter 4: The Hillside Vaults"),
    5: ("Act II: The Great Disconnection", "Chapter 5: The Ash Walkers"),
    6: ("Act II: The Great Disconnection", "Chapter 6: Securing the Vault"),
    7: ("Act III: The Kingdom of the Brass Cog", "Chapter 7: The Ledger and the Token"),
    8: ("Act III: The Kingdom of the Brass Cog", "Chapter 8: The Oracle of Shaver Lake"),
    9: ("Act III: The Kingdom of the Brass Cog", "Chapter 9: Bit-Rot"),
    10: ("Act IV: The Iron Winter", "Chapter 10: The Winter Solstice Skirmish"),
    11: ("Act IV: The Iron Winter", "Chapter 11: The Death of the Screen"),
    12: ("Act IV: The Iron Winter", "Chapter 12: The Paper Kingdom"),
}


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
            if m is not None:
                # Drop the heading line that supplied the title, so the
                # rendered page does not show it twice. Also drop the
                # blank line that followed it, if any, so the body starts
                # cleanly on the first prose paragraph.
                start, end = m.span()
                while end < len(text) and text[end] == "\n":
                    end += 1
                text = text[:start] + text[end:]
            try:
                chapter_no = int(chapter_dir.name.split("-")[1])
            except (IndexError, ValueError):
                chapter_no = 0
            # Chapters 2-12 files have no act/chapter header lines, so
            # inject them here (build-time only). Chapter 1 files already
            # start with their "# Act ..." line after the title strip,
            # so they are left alone. Unknown chapter numbers get no
            # injection rather than a wrong header.
            headers = ACT_CHAPTER.get(chapter_no)
            if headers is not None and not text.startswith("# Act "):
                act, chapter = headers
                text = f"# {act}\n\n## {chapter}\n\n" + text
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
