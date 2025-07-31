import os
import json

RBAC_FILE = "rbac-map.json"
META_FILE = "article-metadata.json"
THUMBNAIL_MAP_FILE = "thumbnail-map.json"
THUMBNAIL_DIRS = ["thumbnails", "assets"]
DEFAULT_THUMB = "assets/devon-og.jpg"
OUTPUT_HTML = "charlotteeverley-site/gallery.html"
TIER_ORDER = ["free", "trial", "silver", "gold", "main"]

def get_current_tier():
    branch = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
    for tier in TIER_ORDER:
        if tier in branch:
            return tier
    raise ValueError(f"Cannot determine member tier from '{branch}'")

def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

rmap = load_json(THUMBNAIL_MAP_FILE)
meta = load_json(META_FILE)

def find_thumbnail(article, slug):
    if article in rmap and os.path.exists(rmap[article]):
        return rmap[article]
    for d in THUMBNAIL_DIRS:
        for ext in [".jpg", ".png"]:
            p = os.path.join(d, slug + ext)
            if os.path.exists(p):
                return p
    return DEFAULT_THUMB

def resolve_link(article):
    # Try various paths in descending order
    for tier in reversed(TIER_ORDER):
        p = f"membership-{tier}/articles/{article}"
        if os.path.exists(p):
            return p
    for root, _, files in os.walk("articles"):
        if article in files:
            return os.path.relpath(os.path.join(root, article), "charlotteeverley-site")
    return f"#missing:{article}"

def generate_card_html(tier, article):
    slug = os.path.splitext(article)[0]
    m = meta.get(article, {})
    title = m.get("title", slug.replace("-", " ").title())
    desc = m.get("description", "")
    thumb = find_thumbnail(article, slug)
    link = resolve_link(article)
    return f"""
    <a class="card" href="{link}" target="_blank">
      <img src="{thumb}" alt="{title}" class="thumb"/>
      <div class="content"><span class="tier {tier}">{tier.capitalize()}</span>
        <h2>{title}</h2><p>{desc}</p>
      </div>
    </a>
    """

def get_articles_for_tier(rbac_map, tier):
    idx = TIER_ORDER.index(tier)
    allowed = TIER_ORDER[:idx+1]
    articles = []
    for t in reversed(allowed):
        articles.extend((t, a) for a in rbac_map.get(t, []))
    return articles

def generate_html(cards, tier):
    header = f"Membership Gallery ({tier.capitalize()} Subscriber)"
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{header}</title>


<style>
body {{ font-family:sans-serif; background:#f9f9f9; padding:2rem; }}
h1 {{ font-size:2rem; margin-bottom:1rem; }}
.gallery {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:1.5rem; }}
.card {{ display:block; background:white; border-radius:8px; text-decoration:none; color:inherit; overflow:hidden; box-shadow:0 0 8px rgba(0,0,0,0.1); transition:transform .2s; }}
.card:hover {{ transform:scale(1.02); }}
.thumb {{ width:100%; height:160px; object-fit:cover; }}
.content {{ padding:1rem; }}
.tier {{ font-size:.75rem; padding:.25rem .5rem; border-radius:4px; [Ocolor:white; display:inline-block; margin-bottom:.5rem; }}
.tier.free {{ background:#10b981 }} .tier.trial {{ background:#3b82f6 }} .tier.silver {{ background:#a1a1aa }} .tier.gold {{ background:#f59e0b }} .tier.main {{ background:#facc15 }}
h2 {{ margin:0; font-size:1.1rem }} p {{ font-size:.9rem; color:#555 }}
    body { font-family: sans-serif; padding: 20px; }
    .tiles { display: flex; flex-wrap: wrap; gap: 20px; }
    .card {
        width: 240px; text-decoration: none; color: black;
        border: 1px solid #ccc; border-radius: 6px; overflow: hidden;
        box-shadow: 1px 2px 4px rgba(0,0,0,0.1);
    }
    .card img { width: 100%; height: 150px; object-fit: cover; }
    .label {
        font-size: 12px; font-weight: bold; padding: 4px 8px;
        display: inline-block; border-radius: 4px; margin: 6px;
        color: white;
    }
    .label.free   { background-color: #10b981; } /* Emerald */
    .label.trial  { background-color: #3b82f6; } /* Blue */
    .label.silver { background-color: #a1a1aa; } /* Gray */
    .label.gold   { background-color: #f59e0b; } /* Amber */
    .label.main   { background-color: #f43f5e; } /* Rose */
    .caption { font-size: 14px; font-weight: 600; padding: 10px; }
</style>

</head>
<body><h1>{header}</h1><div class="gallery">
{''.join(cards)}</div></body></html>
"""

def main():
    tier = get_current_tier()
    rbac_map = load_json(RBAC_FILE)
    cards = [generate_card_html(t, art) for t, art in get_articles_for_tier(rbac_map, tier)]
    html = generate_html(cards, tier)
    os.makedirs(os.path.dirname(OUTPUT_HTML), exist_ok=True)
    with open(OUTPUT_HTML, "w") as f:
        f.write(html)
    print(f"✅ Gallery updated for {tier}: {len(cards)} tiles")

if __name__ == "__main__":
    main()

