import os, json

RBAC = "rbac-map.json"
THUMB_MAP = "thumbnail-map.json"
META = "article-metadata.json"
OUTPUT = "charlotteeverley-site/gallery.html"
TIERS = ["free", "trial", "silver", "gold", "main"]

def branch_to_tier():
    b = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
    return next((t for t in TIERS if t in b), "main")

def scan_mapping():
    return json.load(open(THUMB_MAP))

def load_meta():
    return json.load(open(META)) if os.path.exists(META) else {}

def get_articles(rbac, tier):
    m = json.load(open(rbac))
    idx = TIERS.index(tier) if tier in TIERS else len(TIERS) - 1
    allowed = TIERS[:idx + 1]
    arts = []
    for t in reversed(allowed):
        for a in m.get(t, []):
            arts.append((a, a, t))  # filename, title, tier
    return arts

def resolve_link(filename):
    for t in TIERS:
        path = f"membership-{t}/articles/{filename}"
        if os.path.exists(path):
            return f"/{path}"
    for root, _, files in os.walk("articles"):
        if filename in files:
            return "/" + os.path.join(root, filename).replace("\\", "/")
    return f"/articles/{filename}"

def build_tile_html(filename, title, tier, thumb_map):
    thumbnail = thumb_map.get(filename, "assets/default.png")
    link = resolve_link(filename)
    short_title = os.path.splitext(os.path.basename(title))[0].replace("-", " ").title()
    return f"""
    <a class="card" href="{link}">
        <img src="/{thumbnail}" alt="{short_title}">
        <div class="label {tier}">{tier.title()}</div>
        <div class="caption">{short_title}</div>
    </a>
    """

def build_special_gallery_tile():
    return """
    <a class="card" href="/articles/gallery.html">
        <img src="/assets/charlotte-everley-articles.png" alt="Legacy Visual Gallery">
        <div class="label featured">Featured Posters</div>
        <div class="caption">Legacy Digital Gallery</div>
    </a>
    """

def main():
    tier = branch_to_tier()
    thumb_map = scan_mapping()
    articles = get_articles(RBAC, tier)
    tiles = [build_tile_html(fn, title, t, thumb_map) for fn, title, t in articles]
    tiles.append(build_special_gallery_tile())  # add static tile
    content = "\n".join(tiles)

    html = f"""
    <html>
    <head>
        <title>Membership Gallery – {tier.title()}</title>
        <style>
            body {{ font-family: sans-serif; padding: 20px; }}
            .tiles {{ display: flex; flex-wrap: wrap; gap: 20px; }}
            .card {{
                width: 240px; text-decoration: none; color: black;
                border: 1px solid #ccc; border-radius: 6px; overflow: hidden;
                box-shadow: 1px 2px 4px rgba(0,0,0,0.1);
            }}
            .card img {{ width: 100%; height: 150px; object-fit: cover; }}
            .label {{
                font-size: 12px; font-weight: bold; padding: 4px 8px;
                display: inline-block; border-radius: 4px; margin: 6px;
            }}
            .label.free {{ background: #10b981; color: white; }}
            .label.trial {{ background: #3b82f6; color: white; }}
            .label.silver {{ background: #6b7280; color: white; }}
            .label.gold {{ background: #f59e0b; color: white; }}
            .label.featured {{ background: #8b5cf6; color: white; }}
            .caption {{ font-size: 14px; font-weight: 600; padding: 10px; }}
        </style>
    </head>
    <body>
        <h1>Membership Gallery – {tier.title()}</h1>
        <div class="tiles">{content}</div>
    </body>
    </html>
    """

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w") as f:
        f.write(html)
    print(f"✅ Gallery built for tier '{tier}', {len(articles)} dynamic + 1 legacy tile.")

if __name__ == "__main__":
    main()


