#!/usr/bin/env python3
"""
Build gallery tiles from SQLite metadata + disk images.
- Reads articles + 'hero' images from SQLite
- Generates hashed JPEG thumbnails (skip if unchanged)
- Emits gallery HTML from Jinja2 template
- Supports dev/prod modes and optional per-tier outputs
"""
import os, json, hashlib, sqlite3
from pathlib import Path
from typing import Dict, List

# External deps required at runtime (install in your env):
#   pip install pillow jinja2
from PIL import Image
from jinja2 import Template

# -------- Settings (env-driven) --------
ENV = os.getenv("ENV", "dev")               # dev | prod
DB_PATH = Path(os.getenv("DB_PATH", "data/site.db"))
ASSET_BASE = os.getenv("ASSET_BASE", "/assets")
RAW_DIR = Path(os.getenv("IMG_RAW_DIR", "assets/images/raw"))
THUMBS_DIR = Path(os.getenv("IMG_OUT_DIR", "assets/images/thumbs"))
OUTPUT_FILE = Path(os.getenv("OUTPUT_FILE", "site/gallery.html"))
TEMPLATE_FILE = Path(os.getenv("TEMPLATE_FILE", "scripts/gallery/gallery.tmpl.html"))
MULTI_TIER = os.getenv("MULTI_TIER", "0") in ("1", "true", "True", "YES", "yes")

# If MULTI_TIER=1, we also write tier-specific pages here:
TIERS = ["free","bronze","silver","premier"]
TIER_OUTPUT_DIR = Path(os.getenv("TIER_OUTPUT_DIR", "site/membership"))

# Build cache file to speed up repeated runs
CACHE_FILE = Path(os.getenv("CACHE_FILE", ".buildcache.json"))

# Thumb options
DEV_QUALITY = 80
PROD_QUALITY = 82
DEV_WIDTH = 560
PROD_WIDTH = 768

def load_cache() -> Dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except Exception:
            return {}
    return {}

def save_cache(cache: Dict):
    CACHE_FILE.write_text(json.dumps(cache, indent=2))

def file_md5(p: Path) -> str:
    h = hashlib.md5()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def ensure_dirs():
    THUMBS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    if MULTI_TIER:
        for t in TIERS:
            (TIER_OUTPUT_DIR / t).mkdir(parents=True, exist_ok=True)

def select_articles(conn) -> List[dict]:
    q = """
    SELECT a.slug, a.title, a.minutes, a.category, a.tier, i.rel_path
    FROM articles a
    JOIN images i ON i.article_id = a.id AND i.role = 'hero'
    ORDER BY a.created_at DESC, a.id DESC
    """
    rows = conn.execute(q).fetchall()
    out = []
    for slug, title, minutes, category, tier, rel_path in rows:
        out.append({
            "slug": slug,
            "title": title,
            "minutes": minutes,
            "category": category,
            "tier": tier or "free",
            "hero_rel": rel_path,  # e.g. /assets/images/raw/file.jpg
        })
    return out

def mkthumb(src_abs: Path, width: int, quality: int) -> str:
    """
    Create (or reuse) a hashed JPEG thumbnail.
    Returns web path like /assets/images/thumbs/<name>.jpg
    """
    if not src_abs.exists():
        raise FileNotFoundError(src_abs)

    # Use md5 of source file for cache-busting
    hsh = file_md5(src_abs)[:10]
    out_name = f"{src_abs.stem}-{hsh}.jpg"
    out_abs = THUMBS_DIR / out_name
    out_web = f"{ASSET_BASE}/images/thumbs/{out_name}"

    # If exists, reuse
    if out_abs.exists():
        return out_web

    # Create thumbnail
    img = Image.open(src_abs).convert("RGB")
    w, h = img.size
    if w > width:
        ratio = width / float(w)
        new_size = (width, int(h * ratio))
        img = img.resize(new_size, Image.LANCZOS)

    img.save(out_abs, "JPEG", optimize=True, progressive=True, quality=quality)
    return out_web

def hydrate_articles(articles: List[dict], cache: Dict) -> List[dict]:
    width = PROD_WIDTH if ENV == "prod" else DEV_WIDTH
    quality = PROD_QUALITY if ENV == "prod" else DEV_QUALITY

    for a in articles:
        # Map hero rel path to absolute on disk
        # rel path may begin with leading "/", strip it for disk path
        rel = a["hero_rel"].lstrip("/")
        src_abs = Path(rel)
        if not src_abs.is_absolute():
            src_abs = Path.cwd() / rel

        # Fallback: if path is not under RAW_DIR, try to join RAW_DIR with filename
        if not src_abs.exists():
            maybe = Path.cwd() / RAW_DIR / Path(rel).name
            if maybe.exists():
                src_abs = maybe

        a["thumb"] = mkthumb(src_abs, width=width, quality=quality)
        a["href"] = f"/articles/{a['slug']}/"
        a["alt"] = a["title"]
        a["locked"] = False  # can be toggled at template time if doing client-side gating
    return articles

def render_html(articles: List[dict], outfile: Path, current_tier: str = None):
    tmpl = Template(TEMPLATE_FILE.read_text())
    # If current_tier is provided, mark items above it as locked
    ordered = {t:i for i,t in enumerate(TIERS)}
    items = []
    for a in articles:
        if current_tier is None:
            items.append(dict(a, locked=False))
            continue
        needed = a.get("tier", "free")
        locked = ordered[current_tier] < ordered[needed]
        items.append(dict(a, locked=locked))

    html = tmpl.render(
        title="Gallery",
        heading="Latest Articles",
        articles=items
    )
    outfile.parent.mkdir(parents=True, exist_ok=True)
    outfile.write_text(html, encoding="utf-8")

def build():
    ensure_dirs()
    if not DB_PATH.exists():
        raise SystemExit(f"❌ DB not found: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.row_factory = sqlite3.Row
        articles = select_articles(conn)
    finally:
        conn.close()

    cache = load_cache()
    articles = hydrate_articles(articles, cache)

    # Single gallery
    render_html(articles, OUTPUT_FILE)

    # Optional per-tier pages
    if MULTI_TIER:
        for tier in TIERS:
            out = TIER_OUTPUT_DIR / tier / "gallery.html"
            render_html(articles, out, current_tier=tier)

    # Save cache last
    save_cache(cache)
    print(f"✅ Built {OUTPUT_FILE} ({len(articles)} tiles)")
    if MULTI_TIER:
        print(f"✅ Per-tier outputs under {TIER_OUTPUT_DIR}")
    print(f"Mode: {ENV}  |  Thumbs dir: {THUMBS_DIR}")

if __name__ == "__main__":
    build()
