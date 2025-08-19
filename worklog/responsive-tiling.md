# Phased Approach [1-5]

I have this state in my code and would like to miove to the next phase 

i have these issues to solve
1- i would like to have a bit more attractive responsiveness in tiles - i have seen some hovering action, making it more live so it is awesome
2- would like to fix tile thumbnail automation - there is a image to article map as for article index and gallery gets generated for statis HTML
3- In phase3 would like to have metadata in DB - sqlite and images on disk, intelligent code to pull things to build dev and prod versions 
4- link with the other work - based on subscription tier 
5- merge to main 


# Phase 1 — Make tiles feel “alive” (hover + focus, accessible)

Add this CSS (no framework assumptions). It’s performant (GPU transforms only), keyboard-friendly, and mobile-safe.

```css
/* Tile container */
.tiles {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 18px;
}

/* Tile */
.tile {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  background: #0f1115;
  box-shadow: 0 3px 16px rgba(0,0,0,.18);
  transition: transform .22s ease, box-shadow .22s ease;
  will-change: transform;
}
.tile:focus-within,
.tile:hover {
  transform: translateY(-6px) scale(1.015);
  box-shadow: 0 10px 28px rgba(0,0,0,.28);
}

/* Image */
.tile img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  display:block;
  transition: transform .5s ease;
}
.tile:hover img,
.tile:focus-within img {
  transform: scale(1.06);
}

/* Gradient + text */
.tile__body {
  position: absolute;
  inset: auto 0 0 0;
  padding: 14px 16px;
  color: #fff;
  background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,.55) 55%, rgba(0,0,0,.85) 100%);
}
.tile__title {
  font-size: 1.05rem;
  font-weight: 600;
  margin: 0 0 6px;
}
.tile__meta { opacity:.8; font-size:.88rem; }

/* Reduce motion */
@media (prefers-reduced-motion: reduce) {
  .tile, .tile img { transition: none; }
}
```

HTML shape:

```html
<a class="tile" href="/articles/slug-here/" data-tier="silver" aria-label="Open: Title">
  <img src="/images/thumbs/slug-here.jpg" alt="Descriptive alt text">
  <div class="tile__body">
    <h3 class="tile__title">Article Title</h3>
    <div class="tile__meta">5 min • Space/Cloud</div>
  </div>
</a>
```

# Phase 2 — Tile thumbnail automation (static gallery + mapping)

Keep your source of truth simple: a manifest that maps each article to its hero image; a script generates thumbnails + `index.html`.

## 2.1 Repo layout (suggested)

```
/content/articles/<slug>/index.md
/assets/images/raw/<slug>.jpg
/assets/images/thumbs/           # generated
/scripts/gallery/build_gallery.py
/data/articles.json              # manifest (generated or curated)
```

## 2.2 Manifest (can be built from frontmatter or kept manual)

`/data/articles.json`

```json
[
  {
    "slug": "edge-caching-on-a-budget",
    "title": "Edge Caching on a Budget",
    "minutes": 6,
    "category": "Cloud",
    "tier": "silver",
    "image": "/assets/images/raw/edge-caching-on-a-budget.jpg"
  }
]
```

## 2.3 Build script (Pillow + Jinja2)

* Generates web-optimized thumbnails
* Writes a static `gallery.html` from a template
* Validates image/article mapping

```python
#!/usr/bin/env python3
import json, os, hashlib
from pathlib import Path
from PIL import Image
from jinja2 import Template

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "articles.json"
RAW = ROOT / "assets" / "images" / "raw"
THUMBS = ROOT / "assets" / "images" / "thumbs"
OUT = ROOT / "site" / "gallery.html"
TEMPLATE = ROOT / "scripts" / "gallery" / "gallery.tmpl.html"

THUMBS.mkdir(parents=True, exist_ok=True)

def mkthumb(src: Path, width=640):
    img = Image.open(src).convert("RGB")
    w, h = img.size
    ratio = width / w
    dst = img.resize((width, int(h*ratio)), Image.LANCZOS)
    # hashed filename to allow cache-busting
    hsh = hashlib.md5(src.read_bytes()).hexdigest()[:8]
    out = THUMBS / f"{src.stem}-{hsh}.jpg"
    dst.save(out, "JPEG", optimize=True, quality=82, progressive=True)
    return f"/assets/images/thumbs/{out.name}"

articles = json.loads(DATA.read_text())
for a in articles:
    src = ROOT / a["image"].lstrip("/")
    if not src.exists():
        raise SystemExit(f"Missing image for {a['slug']}: {src}")
    a["thumb"] = mkthumb(src)

tmpl = Template(TEMPLATE.read_text())
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(tmpl.render(articles=articles), encoding="utf-8")
print(f"✅ Gallery built: {OUT}")
```

Template `gallery.tmpl.html` just loops `articles` to render the `.tile` markup from Phase 1 using `a["thumb"]`.

> If you prefer frontmatter parsing, I’ll switch this to read each `/content/articles/**/index.md` and build `articles.json` automatically.

# Phase 3 — Metadata in SQLite + disk-backed images (dev/prod aware)

Keep images on disk, metadata in SQLite. Let the build read from DB and emit static HTML for **dev** and **prod**.

## 3.1 SQLite schema

```sql
CREATE TABLE articles (
  id INTEGER PRIMARY KEY,
  slug TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  minutes INTEGER,
  category TEXT,
  tier TEXT CHECK(tier IN ('free','bronze','silver','premier')) NOT NULL DEFAULT 'free',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE images (
  id INTEGER PRIMARY KEY,
  article_id INTEGER NOT NULL,
  role TEXT CHECK(role IN ('hero','thumb','gallery')) NOT NULL,
  rel_path TEXT NOT NULL,         -- e.g. /assets/images/raw/<file>.jpg
  hash TEXT NOT NULL,
  width INTEGER,
  height INTEGER,
  FOREIGN KEY(article_id) REFERENCES articles(id) ON DELETE CASCADE
);

CREATE INDEX idx_articles_tier ON articles(tier);
CREATE INDEX idx_images_article_role ON images(article_id, role);
```

## 3.2 Build profile (dev vs prod)

Use an env var to drive paths/minifiers:

```
ENV=dev|prod
ASSET_BASE=/assets
IMG_RAW_DIR=assets/images/raw
IMG_OUT_DIR=assets/images/thumbs
```

Build command examples:

```bash
# dev: fast thumbs, no minify
ENV=dev python scripts/build.py

# prod: full optimize, hash filenames, HTML minify
ENV=prod python scripts/build.py
```

## 3.3 Intelligent pull

* If an image’s file hash hasn’t changed, skip work.
* If article rows changed (updated\_at > last\_build), rebuild only affected tiles.
* Write a small `.buildcache.json` with last hashes per file.

I can wire that into the Python script above.

# Phase 4 — Wire into subscription tiers (RBAC)

You already have tier inheritance (free→bronze→silver→premier). Two clean options for a mostly-static site:

**A) Build-time filtering (safest)**

* Generate separate `gallery.html` per tier (e.g., `/membership/free/gallery.html`, `/membership/premier/gallery.html`) including only allowed articles.
* Your router/nav points to the right one after auth.
* Zero client-side leakage.

**B) Client-side gating (quick)**

* Render all tiles but mark them: `data-tier="silver"`.
* Hide/disable tiles above the user’s `currentTier` at runtime.

```js
// currentTier from your auth/session
const order = ['free','bronze','silver','premier'];
const currentTier = window.__CURRENT_TIER__ || 'free';

document.querySelectorAll('.tile').forEach(t => {
  const needed = t.dataset.tier || 'free';
  if (order.indexOf(currentTier) < order.indexOf(needed)) {
    t.setAttribute('aria-disabled','true');
    t.classList.add('tile--locked');
    t.href = '/membership/upgrade/';
  }
});
```

CSS lock styling:

```css
.tile--locked::after{
  content:"Upgrade to view";
  position:absolute; inset:auto 0 0 0;
  padding:10px 12px; text-align:center;
  background:rgba(0,0,0,.7); color:#fff; font-weight:600;
}
.tile--locked img { filter: blur(2px) grayscale(40%); }
```

If you want both, we can default to A in prod and B in dev.

# Phase 5 — Merge to main (guardrails)

Since you’ve been tagging restore points, let’s keep it crisp:

```bash
# 1) Update your feature branch
git checkout fix/tile-automation   # or your current branch
git fetch origin
git rebase origin/main

# 2) Run builds & smoke tests
ENV=dev python scripts/gallery/build_gallery.py
ENV=prod python scripts/gallery/build_gallery.py

# 3) Commit generated artifacts (if versioned) or ensure .gitignore is correct
git add .
git commit -m "Phase 1-3: tiles, thumbs, DB build; tier wiring"

# 4) Push and open PR
git push -u origin HEAD
# -> Open PR with checklist & screenshots

# 5) Squash merge via PR, tag a release
# (after approval)
git checkout main
git pull
git tag -a "release-gallery-v1" -m "Tile UX + gallery automation"
git push --tags

# 6) Delete feature branch
git branch -d fix/tile-automation
git push origin --delete fix/tile-automation
```
