# current Lab website design

Moved from Downloads on 2026-08-13.

## GitHub Pages (publish from this folder)

The live site files are at the **root of this folder** (`index.html` here, not inside `docs/`).

To push to https://github.com/NVA-KIST/NVA-KIST.github.io.git:

```bash
cd "E:\current Lab website design"
```

Set Pages to deploy from the repository **root** (or `/docs` only if you later nest the site). Do **not** commit `original-design/` or `source/` — they are archives and older drafts. A `.gitignore` is included for that.

Local preview (do not use `file://`):

```bash
python -m http.server 8080
```

Then open http://localhost:8080/

## Layout

| Path | What it is |
|------|------------|
| `index.html`, `*.dc.html`, `support.js`, `content/`, `assets/` | **Publishable GitHub Pages site** (former `docs/` folder) |
| `.nojekyll` | Tells GitHub Pages not to run Jekyll |
| `content/board.json` | Board (Album / News / Blogs) data — edit this to update the board |
| `original-design/` | Older design pages not in the live site (Blog, Demos, Team, larger logo) |
| `source/` | Source zips, Contact HTML/PPTX, and zip extract / design handoff |
| `README-site.md` | Original site README from `docs/` |

## Pages

| File | URL path |
|------|----------|
| `index.html` | `/` (home) |
| `Director.dc.html` | Members — Director |
| `Students.dc.html` | Members — Students |
| `Publications.dc.html` | Publications |
| `Projects.dc.html` | Projects |
| `Board.dc.html` | Board (Album / News / Research Blogs) |
| `Contact.dc.html` | Contact |

## Update Board content (no layout edits)

Edit `content/board.json`, then commit and push.

- **album** — `src` is a path like `assets/album/seminar.jpg` (put the image in that folder). Leave `src` empty for a placeholder tile.
- **news** — announcements. `href` can be another page, a PDF, or an external URL.
- **blogs** — research notes. `href` can be a Notion/Medium link, or `#` until the post exists.

The site goes live about a minute after the push.
