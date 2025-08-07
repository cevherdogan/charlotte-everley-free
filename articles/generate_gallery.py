#!/usr/bin/env python3
import os
import json

# ---- Config ----
RBAC   = "rbac-map.json"                         # { "free": [...], "bronze": [...], "silver": [...], "premier": [...] }
OUTPUT = "charlotteeverley-site/gallery.html"    # generated file
TIERS  = ["free", "bronze", "silver", "premier"] # strict order, higher includes all lower

# ---- Helpers ----
def branch_to_tier() -> str:
    """
    Detect the current tier from the Git branch name.
    Defaults to the highest tier ('premier') if none is found.
    """
    try:
        b = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
    except Exception:
        b = ""
    for t in TIERS:
        if t in b:
            return t
    # Default to highest (so release branches generate full access)
    return TIERS[-1]

def load_json(path: str, default):
    return json.load(open(path, "r", encoding="utf-8")) if os.path.exists(path) else default

def get_articles(rbac_path: str, current_tier: str):
    """
    Returns list of (filename, title, normalized_tier) for all tiers
    up to and including current_tier, with current tier first.
    """
    rbac = load_json(rbac_path, {})
    if current_tier not in TIERS:
        current_tier = TIERS[-1]
    idx = TIERS.index(current_tier)
    allowed = TIERS[: idx + 1]  # inheritance

    items = []
    # Show current tier first, then lower ones
    for t in reversed(allowed):
        for fname in rbac.get(t, []):
            # Title derived from filename (you can wire real metadata later)
            title = os.path.splitext(os.path.basename(fname))[0].replace("-", " ").title()
            items.append((fname, title, t))
    return items

def resolve_link(filename: str) -> str:
    """
    Prefer a membership article if it exists (membership/<tier>/articles/<file>),
    otherwise fall back to /articles/** search.
    Returns a site-root-relative URL.
    """
    # Search in membership/*/articles
    membership_root = "membership"
    if os.path.isdir(membership_root):
        for band in os.listdir(membership_root):
            candidate = os.path.join(membership_root, band, "articles", filename)
            if os.path.exists(candidate):
                return "/" + candidate.replace("\\", "/")
    # Fallback: search articles/
    for root, _, files in os.walk("articles"):
        if filename in files:
            return "/" + os.path.join(root, filename).replace("\\", "/")
    # Last resort: best-guess under /articles
    return "/articles/" + filename

def build_tile_html(filename: str, title: str, tier: str) -> str:
    thumb = "/assets/default.png"  # plug in a real thumb map later if desired
    return f"""
<a class="card" href="{resolve_link(filename)}" data-tier="{tier}">
  <img alt="{title}" src="{thumb}"/>
  <div class="label {tier}">{tier.title()}</div>
  <div class="caption">{title}</div>
</a>""".strip()

def generate_html(cards_html: str, tier: str) -> str:
    return f"""<html>
<head>
  <meta charset="utf-8"/>
  <title>Membership Gallery – {tier.title()}</title>
  <style>
    body {{ font-family: sans-serif; padding: 20px; }}
    .tiles {{ display: flex; flex-wrap: wrap; gap: 20px; }}
    .card {{ width: 240px; text-decoration: none; color: black; border: 1px solid #ccc; border-radius: 6px; overflow: hidden; box-shadow: 1px 2px 4px rgba(0,0,0,0.1); }}
    .card img {{ width: 100%; height: 150px; object-fit: cover; }}
    .label {{ font-size: 12px; font-weight: bold; padding: 4px 8px; display: inline-block; border-radius: 4px; margin: 6px; }}
    .label.free {{ background: #10b981; color: #fff; }}
    .label.bronze {{ background: #cd7f32; color: #fff; }}
    .label.silver {{ background: #6b7280; color: #fff; }}
    .label.premier {{ background: #f59e0b; color: #fff; }}
    .caption {{ font-size: 14px; font-weight: 600; padding: 10px; }}
  </style>
</head>
<body>
  <h1>Membership Gallery – {tier.title()}</h1>
  <div class="tiles">
{cards_html}
  </div>
</body>
</html>"""

def main():
    tier = branch_to_tier()
    articles = get_articles(RBAC, tier)
    cards = "\n".join(build_tile_html(f, t, band) for (f, t, band) in articles)
    html = generate_html(cards, tier)
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Gallery built for '{tier}' with {len(articles)} items (tiers included: {TIERS[:TIERS.index(tier)+1]}).")

if __name__ == "__main__":
    main()


