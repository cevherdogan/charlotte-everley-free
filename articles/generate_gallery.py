import os
import json

RBAC_FILE = "rbac-map.json"
THUMBNAIL_MAP_FILE = "thumbnail-map.json"
ARTICLE_DIR = "articles"
OUTPUT_HTML = "charlotteeverley-site/gallery.html"
DEFAULT_THUMB = "assets/devon-og.jpg"
TIER_ORDER = ["free", "trial", "silver", "gold", "main"]

def get_current_tier():
    branch = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
    for tier in TIER_ORDER:
        if tier in branch:
            return tier
    return "main"

def load_json(path):
    return json.load(open(path)) if os.path.exists(path) else {}

def get_all_articles(rbac_map):
    tiered_articles = {}
    for tier, articles in rbac_map.items():
        for article in articles:
            tiered_articles[article] = tier
    return tiered_articles

def resolve_link(filename):
    for root, _, files in os.walk("articles"):
        if filename in files:
            rel = os.path.relpath(os.path.join(root, filename), "articles")
            return f"/articles/{rel}".replace("\\", "/")
    return f"/articles/{filename}"

def generate_card_html(article, tier, thumb_map):
    slug = os.path.splitext(article)[0]
    thumb = thumb_map.get(article, DEFAULT_THUMB)
    title = os.path.basename(slug).replace("-", " ").title()
    link = resolve_link(article)
    return f"""
    <a class="card" href="{link}">
        <img src="{thumb}" alt="{title}">
        <div class="label {tier}">{tier.title()}</div>
        <div class="caption">{title}</div>
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
    }}
    .label.free {{ background: #10b981; color: white; }}
    .label.trial {{ background: #3b82f6; color: white; }}
    .label.silver {{ background: #a1a1aa; color: white; }}
    .label.gold {{ background: #f59e0b; color: black; }}
    .caption {{ font-size: 14px; font-weight: 600; padding: 10px; }}
  </style>
</head>
<body>
  <h1>Membership Gallery – {tier.title()}</h1>
  <div class="tiles">
    {''.join(cards)}
  </div>
</body>
</html>"""

def main():
    tier = get_current_tier()
    rbac_map = load_json(RBAC_FILE)
    thumb_map = load_json(THUMBNAIL_MAP_FILE)
    tiered_articles = get_all_articles(rbac_map)

    cards = []
    for article, article_tier in tiered_articles.items():
        allowed_idx = TIER_ORDER.index(tier)
        article_idx = TIER_ORDER.index(article_tier)
        if article_idx <= allowed_idx:
            cards.append(generate_card_html(article, article_tier, thumb_map))

    html = generate_html(cards, tier)
    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    with open(OUTPUT_HTML, "w") as f:
        f.write(html)
    print(f"✅ Gallery updated for {tier}: {len(cards)} tiles")

if __name__ == "__main__":
    main()

