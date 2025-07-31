import os, json

RBAC = "rbac-map.json"
THUMB_MAP = "thumbnail-map.json"
META = "article-metadata.json"
OUTPUT = "charlotteeverley-site/gallery.html"
TIERS = ["free", "trial", "silver", "gold", "main"]

def branch_to_tier():
    b = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
    return next((t for t in TIERS if t in b), None) or "gold"

def load_mapping(path):
    return json.load(open(path)) if os.path.exists(path) else {}

def get_articles(rbac_path, tier):
    rbac = load_mapping(rbac_path)
    idx = TIERS.index(tier)
    allowed = TIERS[:idx + 1]
    articles = []
    for t in reversed(allowed):
        for art in rbac.get(t, []):
            articles.append((art, art))  # (filename, title)
    return articles

def resolve_link(filename):
    for t in TIERS:
        path = f"membership-{t}/articles/{filename}"
        if os.path.exists(path):
            return path
    for root, _, files in os.walk("articles"):
        if filename in files:
            return os.path.join(root, filename)
    return filename

def build_tile_html(article, thumb_map, tier):
    filename, title = article
    thumbnail = thumb_map.get(filename, "assets/default.png")
    link = resolve_link(filename)
    short_title = os.path.splitext(os.path.basename(title))[0].replace("-", " ").title()
    return f"""
    <a class="card" href="{link}">
        <img src="{thumbnail}" alt="{short_title}">
        <div class="label {tier}">{tier.title()}</div>
        <div class="caption">{short_title}</div>
    </a>
    """

def generate_html(cards, tier):
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
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
            color: white;
        }}
        .label.free   {{ background-color: #10b981; }}
        .label.trial  {{ background-color: #3b82f6; }}
        .label.silver {{ background-color: #a1a1aa; }}
        .label.gold   {{ background-color: #f59e0b; }}
        .label.main   {{ background-color: #f43f5e; }}
        .caption {{ font-size: 14px; font-weight: 600; padding: 10px; }}
    </style>
</head>
<body>
    <h1>Membership Gallery – {tier.title()} Subscriber</h1>
    <div class="tiles">
        {''.join(cards)}
    </div>
</body>
</html>
"""

def main():
    tier = branch_to_tier()
    thumb_map = load_mapping(THUMB_MAP)
    articles = get_articles(RBAC, tier)
    cards = [build_tile_html(article, thumb_map, tier) for article in articles]
    html = generate_html(cards, tier)
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w") as f:
        f.write(html)
    print(f"✅ Gallery built for tier '{tier}', {len(cards)} cards.")

if __name__ == "__main__":
    main()


