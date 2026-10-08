# Standing orders — netbob.org

## What this repo is
The owner's book site: home of the novel *The Dark Fills the Space*,
published serially, chapter by chapter (CC BY 4.0). Jekyll + Chirpy, in a
fork of the theme's own repo (the theme source IS the site tree).
GitHub: netbob/netbob.org. Cloudflare Pages project: netbob-inner-org —
the only one for this site. Push to main = live in about two minutes.

## Working rules
- NEVER run git push. You run as a sandbox identity that cannot reach the
  owner's GitHub credentials; pushes fail and burn the session.
  Commit and stop. Michael reviews and pushes.
- Pull before editing, on every device (the owner also edits from an
  iPad via Working Copy). git status never touches the network — a repo
  can look clean against a months-stale origin. Read merged files before
  pushing. One device per file at a time.
- After Michael pushes, verify the live URL. A 404 five minutes later
  means the build failed — check the front-matter date first.

## Front matter is code
- An unquoted YAML value must never contain a colon followed by a space.
  On Oct 5, 2026, descriptions beginning "Ch 1: " invalidated three
  chapters at once — titles, dates, and categories gone. Use a hyphen
  ("Ch 1 - ...") or quote the value.
- Chapters follow _posts/_chapter-template.md: category [Zo's Page],
  zero-padded numbers in titles (Chapter 01, 02, ...). The book page's
  chapter list sorts by title, so the padding IS the reading order.
- Bylines: the author value is an ID looked up in _data/authors.yml.
  Chapters use author: michael. Known state: that key does not exist in
  this repo's authors.yml yet, so chapter bylines render blank. The cure
  is Michael's to schedule — do not freelance it.

## Load-bearing details
- .gitmodules defines the assets/lib submodule. Never delete it.
- memory/ is a separate personal repo that lives nearby on disk. It must
  never enter this repo's index (it is gitignored): on Oct 1, 2026 a
  commit swept it in as a gitlink with no submodule URL and every
  Cloudflare build failed while the site silently served a stale build.
- _tabs/book.md: its front-matter title must stay exactly "Book". The
  theme builds the tab's browser title from _data/locales (key: book).
  Changing the title to "The Book" makes the browser title render blank.
- Runbooks and process docs live in the PRIVATE netbob-docs repo, never
  in this tree — Jekyll serves root-level Markdown files to the world.

## Hard limit
This repo is PUBLIC. Never write secrets, tokens, API keys, account
numbers, or personal identifiers into any file here.
