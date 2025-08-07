#!/usr/bin/env python3
import re
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python3 scripts/auto_fix_gallery.py charlotteeverley-site/gallery.html")
    sys.exit(1)

p = Path(sys.argv[1])
html = p.read_text(encoding="utf-8")

# 1) JS: change .tile to .card
html = re.sub(r'querySelectorAll\(\s*"\.tile"\s*\)', 'querySelectorAll(".card")', html)

# 2) Labels: trial → bronze, gold → premier (classes + visible text)
html = re.sub(r'(\blabel\s+)trial\b', r'\1bronze', html)
html = re.sub(r'(\blabel\s+)gold\b', r'\1premier', html)
html = re.sub(r'>(\s*)Trial(\s*)<', r'>\1Bronze\2<', html)
html = re.sub(r'>(\s*)Gold(\s*)<', r'>\1Premier\2<', html)

# 3) Add data-tier to each .card based on label class
def add_data_tier(match):
    open_tag, close_tag, inner = match.group(1), match.group(2), match.group(3)
    m = re.search(r'<div\s+class="label\s+([a-zA-Z0-9_-]+)"', inner)
    if m:
        tier_map = {
            "trial": "bronze",
            "gold": "premier",
            "bronze": "bronze",
            "silver": "silver",
            "premier": "premier",
            "free": "free",
            "featured": "featured"
        }
        tier = tier_map.get(m.group(1).lower())
        if tier and tier != "featured":
            if 'data-tier=' in open_tag:
                open_tag = re.sub(r'data-tier="[^"]*"', f'data-tier="{tier}"', open_tag)
            else:
                open_tag = open_tag[:-1] + f' data-tier="{tier}">'
    return f"{open_tag}{close_tag}{inner}</a>"

card_pattern = re.compile(r'(<a\s+class="card"[^>]*)(>)(.*?)(</a>)', re.DOTALL | re.IGNORECASE)
html = card_pattern.sub(add_data_tier, html)

# 4) Ensure CSS rules for bronze/premier exist
css_rules = {
    "bronze": "{ background: #cd7f32; color: white; }",
    "premier": "{ background: #b45309; color: white; }"
}
for tier, rule in css_rules.items():
    if not re.search(rf'\.label\.{tier}\b', html):
        html = html.replace("</style>", f"    .label.{tier} {rule}\n</style>", 1)

p.write_text(html, encoding="utf-8")
print(f"✓ Patched {p}")


