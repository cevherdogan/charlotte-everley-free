#!/usr/bin/env python3
import os
import json
import urllib.parse

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
    return TIERS[-1]  # default highest

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
    for t in reversed(allowed):            # show current tier first
        for fname in rbac.get(t, []):
            title = os.path.splitext(os.path.basename(fname))[0].replace("-", " ").title()
            items.append((fname, title, t))
    return items

def resolve_link(filename: str) -> str:
    """
    Prefer membership/<tier>/articles/<file>, else fall back to /articles/**.
    Returns a site-root-relative URL.
    """
    membership_root = "membership"
    if os.path.isdir(membership_root):
        for band in os.listdir(membership_root):
            candidate = os.path.join(membership_root, band, "articles", filename)
            if os.path.exists(candidate):
                return "/" + candidate.replace("\\", "/")
    for root, _, files in os.walk("articles"):
        if filename in files:
            return "/" + os.path.join(root, filename).replace("\\", "/")
    return "/articles/" + filename

def build_tile_html(filename: str, title: str, tier: str) -> str:
    thumb = "/assets/default.png"
    return f"""
<a class="card" href="{resolve_link(filename)}" data-tier="{tier}">
  <img alt="{title}" src="{thumb}"/>
  <div class="label {tier}">{tier.title()}</div>
  <div class="caption">{title}</div>
</a>""".strip()

def _options_html(selected: str) -> str:
    opts = []
    for t in ["all"] + TIERS:
        label = "All (no filter)" if t == "all" else t.title()
        sel = ' selected="selected"' if t == selected else ""
        opts.append(f'<option value="{t}"{sel}>{label}</option>')
    return "\n".join(opts)

def generate_html(cards_html: str, current_tier: str) -> str:
    # Build the selector pre-filled to current tier (can be overridden by ?tier=... at runtime)
    selector_html = f"""
<div class="toolbar">
  <label for="tierSelect">Test as tier:</label>
  <select id="tierSelect" class="tier-select">
    {_options_html(current_tier)}
  </select>
  <small class="hint">Tip: use <code>?tier=silver</code> in the URL to preset</small>
</div>
""".strip()

    # Tiny JS tester: lets you switch tiers in the browser and applies inheritance visually.
    # This does NOT change the source-of-truth; it’s only for verification.
    js = f"""
<script>
(function() {{
  const TIERS = {json.dumps(TIERS)};
  const tierIndex = Object.fromEntries(TIERS.map((t, i) => [t, i]));

  function includesLower(selected, required) {{
    if (selected === "all") return true;
    return (tierIndex[selected] >= tierIndex[required]);
  }}

  function getQueryTier() {{
    const p = new URLSearchParams(window.location.search);
    const q = (p.get("tier") || "").toLowerCase();
    return TIERS.includes(q) ? q : null;
  }}

  function applyFilter(selected) {{
    document.querySelectorAll(".card").forEach(tile => {{
      const required = tile.dataset.tier;
      tile.style.display = includesLower(selected, required) ? "" : "none";
    }});
  }}

  const select = document.getElementById("tierSelect");
  const preset = getQueryTier();
  if (preset) select.value = preset;

  applyFilter(select.value);
  select.addEventListener("change", () => applyFilter(select.value));
}})();
</script>
"""

    return f"""<html>
<head>
  <meta charset="utf-8"/>
  <title>Membership Gallery – {current_tier.title()}</title>
  <style>
    body {{ font-family: sans-serif; padding: 20px; }}
    .toolbar {{ margin: 0 0 16px 0; display: flex; gap: 12px; align-items: center; }}
    .tier-select {{ padding: 6px 8px; }}
    .hint {{ color: #6b7280; }}
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
  <h1>Membership Gallery – {current_tier.title()}</h1>
  {selector_html}
  <div class="tiles">
{cards_html}
  </div>
  {js}
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


