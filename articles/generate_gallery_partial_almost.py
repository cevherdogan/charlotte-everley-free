import os, json

RBAC_FILE = "rbac-map.json"
META_FILE = "article-metadata.json"
THUMBNAIL_MAP_FILE = "thumbnail-map.json"
OUTPUT_HTML = "charlotteeverley-site/gallery.html"
DEFAULT_THUMB = "assets/devon-og.jpg"
TIERS = ["free", "trial", "silver", "gold", "main"]

def branch_to_tier():
    b = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
    return next((t for t in TIERS if t in b), None) or "gold"

def load_json(path):
    return json.load(open(path)) if os.path.exists(path) else {}

def resolve_link(filename):
    # Prefer articles from actual folders
    for root, _, files in os.walk("articles"):
        if filename in files:
            return os.path.join(root, filename)
    return filename  # fallback

def get_articles_by_rbac(rbac_path, tier):
    rbac = load_json(rbac_path)
    idx = TIERS.index(tier)
    allowed = TIERS[:idx + 1]
    articles = []
    for t in allowed:
        for a in rbac.get(t, []):
            articles.append((a, t))  # (filename, tier)
    return articles

def scan_thumbnails():
    return load_json(THUMBNAIL_MAP_FILE)

def load_metadata():
    return load_json(META_FILE)

def build_tile_html(filename, access_tier, thumb_map, meta):
    title = meta.get(filename, {}).get("title", os.path.splitext(os.path.basename(filename))[0].replace("-", " ").title())
    thumbnail = thumb_map.get(filename, DEFAULT_THUMB)
    link = resolve_link(filename)
    return f"""
    <a class="card" href="{link}">
        <img src="{thumbnail}" alt="{title}">
        <div class="label {access_tier}">{access_tier.title()}</div>
        <div class="caption">{title}</div>
    </a>
    """

def generate_html(tiles, current_branch_tier):
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Membership Gallery – {current_branch_tier.title()}</title>
    <style>
        body {{ font-family: sans-serif; padding: 20px; background: #f9f9f9; }}
        h1 {{ font-size: 2rem; margin-bottom: 1.5rem; }}
        .tiles {{ display: flex; flex-wrap: wrap; gap: 20px; }}
        .card {{
            width: 240px; text-decoration: none; color: black;
            background: white; border: 1px solid #ccc; border-radius: 6px;
            overflow: hidden; box-shadow: 1px 2px 4px rgba(0,0,0,0.1);
        }}
        .card img {{ width: 100%; height: 150px; object-fit: cover; }}
        .label {{
            font-size: 12px; font-weight: bold; padding: 4px 8px;
            display: inline-block; border-radius: 4px; margin: 6px;
        }}
        .label.free {{ background: #10b981; color: white; }}
        .label.trial {{ background: #3b82f6; color: white; }}
        .label.silver {{ background: #a1a1aa; color: white; }}
        .label.gold {{ background: #f59e0b; color: white; }}
        .label.main {{ background: #ef4444; color: white; }}
        .caption {{ font-size: 14px; font-weight: 600; padding: 10px; }}
    </style>
</head>
<body>
    <h1>Membership Gallery – {current_branch_tier.title()}</h1>
    <div class="tiles">
        {''.join(tiles)}
    </div>
</body>
</html>
"""

def main():
    tier = branch_to_tier()
    rbac_articles = get_articles_by_rbac(RBAC_FILE, tier)
    thumb_map = scan_thumbnails()
    meta = load_metadata()

    tiles = [build_tile_html(filename, article_tier, thumb_map, meta) for filename, article_tier in rbac_articles]
    html = generate_html(tiles, tier)

    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    with open(OUTPUT_HTML, "w") as f:
        f.write(html)

    print(f"✅ Gallery generated for tier '{tier}', {len(tiles)} tiles.")

if __name__ == "__main__":
    main()

