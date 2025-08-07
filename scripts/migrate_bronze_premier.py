#!/usr/bin/env python3
import re
import sys
import json
import argparse
import subprocess
from pathlib import Path

def smart_rename(old: Path, new: Path):
    if old.resolve() == new.resolve() or not old.exists():
        return False
    try:
        # Prefer git mv if available (preserves history)
        subprocess.run(["git", "mv", str(old), str(new)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
        new.parent.mkdir(parents=True, exist_ok=True)
        old.rename(new)
    return True

def patch_gallery(gallery_path: Path):
    html = gallery_path.read_text(encoding="utf-8")
    changed = False

    # Ensure filter uses .card (already done, but idempotent)
    html2 = re.sub(r'querySelectorAll\(\s*"\.tile"\s*\)', 'querySelectorAll(".card")', html)
    if html2 != html:
        html = html2
        changed = True

    # Normalize label classes + visible text
    replacements = [
        (r'(\blabel\s+)trial\b', r'\1bronze'),
        (r'(\blabel\s+)gold\b', r'\1premier'),
        (r'>(\s*)Trial(\s*)<', r'>\1Bronze\2<'),
        (r'>(\s*)Gold(\s*)<', r'>\1Premier\2<'),
    ]
    for pat, rep in replacements:
        new_html = re.sub(pat, rep, html)
        if new_html != html:
            html = new_html
            changed = True

    # Add/refresh data-tier for each card based on the label class within that card
    def card_cb(m):
        open_tag, gt, inner, close = m.group(1), m.group(2), m.group(3), m.group(4)
        # Detect tier from label inside the card
        mlabel = re.search(r'<div\s+class="label\s+([a-zA-Z0-9_-]+)"', inner)
        tier = (mlabel.group(1).lower() if mlabel else "").strip()
        tier_map = {"trial":"bronze", "gold":"premier", "bronze":"bronze", "silver":"silver", "premier":"premier", "free":"free", "featured":"featured"}
        tier = tier_map.get(tier)
        if tier and tier != "featured":
            if re.search(r'\sdata-tier="[^"]*"', open_tag):
                open_tag = re.sub(r'\sdata-tier="[^"]*"', f' data-tier="{tier}"', open_tag)
            else:
                open_tag = open_tag[:-1] + f' data-tier="{tier}">'
        # For premier/bronze cards, fix inner text that still says Gold/Trial
        if tier == "premier":
            inner_new = re.sub(r'(\b)Gold(\b)', r'\1Premier\2', inner)
            inner_new = re.sub(r'(\b)gold(\b)', r'\1premier\2', inner_new)
            inner = inner_new
        elif tier == "bronze":
            inner_new = re.sub(r'(\b)Trial(\b)', r'\1Bronze\2', inner)
            inner_new = re.sub(r'(\b)trial(\b)', r'\1bronze\2', inner_new)
            inner = inner_new
        return f"{open_tag}{gt}{inner}{close}"

    card_re = re.compile(r'(<a\s+class="card"[^>]*)(>)(.*?)(</a>)', re.DOTALL | re.IGNORECASE)
    new_html = card_re.sub(card_cb, html)
    if new_html != html:
        html = new_html
        changed = True

    # Fix href filenames inside cards: -gold.html → -premier.html, _trial.html → _bronze.html
    rename_pairs = []  # (old, new) relative paths found in gallery
    def href_cb(m):
        href_val = m.group(1)
        new_href = href_val
        if href_val.endswith(".html"):
            new_href = re.sub(r'-gold\.html\b', '-premier.html', new_href)
            new_href = re.sub(r'_trial\.html\b', '_bronze.html', new_href)
        if new_href != href_val:
            rename_pairs.append((href_val, new_href))
        return f'href="{new_href}"'
    html2 = re.sub(r'href="([^"]+)"', href_cb, html)
    if html2 != html:
        html = html2
        changed = True

    # Ensure CSS rules exist (idempotent insertion)
    for tier, rule in {
        "bronze": "{ background: #cd7f32; color: white; }",
        "premier": "{ background: #b45309; color: white; }"
    }.items():
        if not re.search(rf'\.label\.{tier}\b', html):
            html = html.replace("</style>", f"    .label.{tier} {rule}\n</style>", 1)
            changed = True

    if changed:
        gallery_path.write_text(html, encoding="utf-8")
    return changed, rename_pairs

def patch_access_map(access_map_path: Path, rename_pairs):
    if not access_map_path.exists():
        return False
    data = json.loads(access_map_path.read_text(encoding="utf-8"))
    # We expect top-level "plans" with per-plan {articles:[]}
    plans = data.get("plans") or {}
    changed = False
    def apply_pairs(s: str) -> str:
        new_s = s
        for old, new in rename_pairs:
            if s == old.lstrip('/'):
                new_s = new.lstrip('/')
        return new_s
    for plan, obj in plans.items():
        arts = obj.get("articles") or []
        new_arts = [apply_pairs(a) for a in arts]
        if new_arts != arts:
            obj["articles"] = new_arts
            changed = True
    if changed:
        access_map_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return changed

def do_file_renames(project_root: Path, rename_pairs):
    changed = False
    for old_href, new_href in rename_pairs:
        # only handle site-local article HTML paths like /articles/...
        if not old_href.startswith("/articles/"):
            continue
        old_fs = project_root / old_href.lstrip("/")
        new_fs = project_root / new_href.lstrip("/")
        if old_fs.exists() and old_fs.suffix == ".html" and old_fs != new_fs:
            if smart_rename(old_fs, new_fs):
                changed = True
    return changed

def main():
    ap = argparse.ArgumentParser(description="Migrate trial→bronze and gold→premier in gallery + access_map, optionally rename files.")
    ap.add_argument("--gallery", required=True, help="Path to gallery.html")
    ap.add_argument("--map", default="access_map.json", help="Path to access_map.json (default: access_map.json)")
    ap.add_argument("--rename-files", action="store_true", help="Also rename article files on disk and update references")
    args = ap.parse_args()

    project_root = Path(".").resolve()
    gallery_path = Path(args.gallery)
    map_path = Path(args.map)

    g_changed, rename_pairs = patch_gallery(gallery_path)
    if g_changed:
        print(f"✓ Patched {gallery_path}")
    else:
        print(f"• No changes needed in {gallery_path}")

    # Patch access_map.json using discovered href renames
    m_changed = False
    if rename_pairs and map_path.exists():
        m_changed = patch_access_map(map_path, rename_pairs)
        if m_changed:
            print(f"✓ Updated {map_path} with new article names")

    # Optionally rename files on disk
    if args.rename_files and rename_pairs:
        f_changed = do_file_renames(project_root, rename_pairs)
        if f_changed:
            print("✓ Renamed article files on disk (git mv or os.rename)")
        else:
            print("• No matching files to rename on disk")

    # Summary of planned renames
    if rename_pairs:
        print("Detected href renames:")
        for old, new in rename_pairs:
            print(f"  {old}  →  {new}")

if __name__ == "__main__":
    main()


