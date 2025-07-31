import os, json

RBAC = "rbac-map.json"
THUMB_MAP = "thumbnail-map.json"
META = "article-metadata.json"
OUTPUT = "charlotteeverley-site/gallery.html"
TIERS = ["free", "trial", "silver", "gold"]

def branch_to_tier():
    b = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
    return next((t for t in TIERS if t in b), "gold")

def scan_mapping():
    return json.load(open(THUMB_MAP))

def get_articles(rbac_path, tier):
    rbac = json.load(open(rbac_path))
    idx = TIERS.index(tier)
    allowed = TIERS[:idx+1]
    articles = []
    for t in reversed(allowed):
        for a in rbac.get(t, []):
            articles.append((a, a))
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
        h1 {{ font-size: 1.8rem; }}
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
            color: #000;
        }}
        .label.free {{ background: #defce7; color: #046c4e; }}
        .label.trial {{ background: #e0f0ff; color: #1d4ed8; }}
        .label.silver {{ background: #f0f0f0; color: #555; }}
        .label.gold {{ background: #fff4c2; color: #a15c00; }}
        .caption {{ font-size: 14px; font-weight: 600; padding: 10px; }}
    </style>
</head>
<body>
    <h1>Membership Gallery – {tier.title()}</h1>
    <div class="tiles">
        {''.join(cards)}
    </div>
</body>
</html>
"""

def main():
    tier = branch_to_tier()
    thumb_map = scan_mapping()
    articles = get_articles(RBAC, tier)
    cards = [build_tile_html(a, thumb_map, tier) for a in articles]
    html = generate_html(cards, tier)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w") as f:
        f.write(html)
    print(f"✅ Gallery built for tier '{tier}', {len(cards)} cards.")

if __name__ == "__main__":
    main()

