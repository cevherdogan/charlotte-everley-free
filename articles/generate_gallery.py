import os
import json

RBAC_FILE = "rbac-map.json"
OUTPUT_HTML = "charlotteeverley-site/gallery.html"
TIER_ORDER = ["free", "trial", "silver", "gold"]

def get_current_tier():
    branch = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
    return branch.replace("membership-", "")

def get_articles_for_tier(rbac_map, tier):
    idx = TIER_ORDER.index(tier)
    allowed = TIER_ORDER[:idx + 1]
    articles = []
    for t in allowed:
        for article in rbac_map.get(t, []):
            articles.append((t, article))
    return articles

def generate_card_html(tier, filename):
    return f"""
    <div class="card">
      <span class="tier {tier}">{tier.capitalize()}</span><br>
      <a href="../membership/{tier}/articles/{filename}" target="_blank">{filename}</a>
    </div>
    """

def generate_gallery_html(cards):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Membership Gallery</title>
  <style>
    body {{
      font-family: sans-serif;
      background: #f9f9f9;
      padding: 2rem;
    }}
    h1 {{
      font-size: 2rem;
      margin-bottom: 1rem;
    }}
    .gallery {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
      gap: 1.5rem;
    }}
    .card {{
      background: white;
      border-radius: 8px;
      padding: 1rem;
      box-shadow: 0 0 8px rgba(0,0,0,0.1);
    }}
    .tier {{
      font-size: 0.8rem;
      font-weight: bold;
      padding: 0.25rem 0.5rem;
      border-radius: 4px;
      color: white;
      display: inline-block;
      margin-bottom: 0.5rem;
    }}
    .tier.free {{ background: #10b981; }}
    .tier.trial {{ background: #3b82f6; }}
    .tier.silver {{ background: #a1a1aa; }}
    .tier.gold {{ background: #f59e0b; }}
    a {{
      color: #1e40af;
      text-decoration: none;
      font-weight: 500;
    }}
    a:hover {{
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <h1>Membership Gallery</h1>
  <div class="gallery">
    {''.join(cards)}
  </div>
</body>
</html>"""

def main():
    current_tier = get_current_tier()
    with open(RBAC_FILE, "r") as f:
        rbac_map = json.load(f)

    articles = get_articles_for_tier(rbac_map, current_tier)
    cards = [generate_card_html(tier, filename) for tier, filename in articles]
    html = generate_gallery_html(cards)

    with open(OUTPUT_HTML, "w") as f:
        f.write(html)

    print(f"✅ Gallery updated for tier: {current_tier} → {len(articles)} articles")

if __name__ == "__main__":
    main()

