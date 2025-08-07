#!/usr/bin/env python3
import re, sys
from pathlib import Path

p = Path(sys.argv[1])
html = p.read_text(encoding="utf-8")

# Normalize any anchors where data-tier leaked into href or we have >>.
def fix_card(m):
    open_tag, gt, inner, close = m.group(1), m.group(2), m.group(3), m.group(4)
    # Ensure href is closed before we add data-tier
    open_tag = re.sub(r'href="([^"]*?)\s+data-tier="[^"]*"', r'href="\1"', open_tag)
    # Remove accidental double '>'
    gt = '>'
    # Determine tier from label inside
    lab = re.search(r'<div\s+class="label\s+([a-zA-Z0-9_-]+)"', inner)
    tier = lab.group(1).lower() if lab else None
    tier_map = {"trial":"bronze","gold":"premier","bronze":"bronze","silver":"silver","premier":"premier","free":"free"}
    tier = tier_map.get(tier)
    if tier and 'data-tier=' not in open_tag:
        open_tag = open_tag + f' data-tier="{tier}"'
    # Fix href filename endings
    inner = re.sub(r'href="([^"]+)"', lambda hm: f'href="{hm.group(1).replace("-gold.html","-premier.html").replace("_trial.html","_bronze.html")}"', inner)
    return f"{open_tag}{gt}{inner}{close}"

card_re = re.compile(r'(<a\s+class="card"[^>]*)(>)(.*?)(</a>)', re.DOTALL|re.IGNORECASE)
html2 = card_re.sub(fix_card, html)

# Also fix any stragglers outside cards
html2 = html2.replace("-gold.html", "-premier.html").replace("_trial.html","_bronze.html")

if html2 != html:
    p.write_text(html2, encoding="utf-8")
    print(f"✓ Repaired anchors and filenames in {p}")
else:
    print("• No changes needed")


