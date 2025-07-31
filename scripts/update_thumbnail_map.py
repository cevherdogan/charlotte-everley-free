#!/usr/bin/env python3
import os
import json

MAP_FILE = "thumbnail-map.json"
PLACEHOLDER = "assets/default.png"
ARTICLE_DIR = "articles"

def scan_articles():
    htmls = []
    for root, _, files in os.walk(ARTICLE_DIR):
        for f in files:
            if f.lower().endswith(".html"):
                rel_path = os.path.relpath(os.path.join(root, f), ARTICLE_DIR)
                key = rel_path.replace("\\", "/")
                htmls.append(key)
    return sorted(set(htmls))

def load_map():
    if os.path.exists(MAP_FILE):
        return json.load(open(MAP_FILE))
    return {}

def save_map(mapping):
    with open(MAP_FILE, "w") as f:
        json.dump(mapping, f, indent=2, sort_keys=True)
    print(f"✅ Updated {MAP_FILE}, now has {len(mapping)} entries.")

def main():
    articles = scan_articles()
    mapping = load_map()
    changed = False

    for art in articles:
        if art not in mapping:
            mapping[art] = PLACEHOLDER
            print(f"+ Added placeholder entry for: {art}")
            changed = True

    removed = [k for k in mapping if k not in articles]
    for extra in removed:
        mapping.pop(extra, None)
        print(f"- Removed obsolete entry: {extra}")
        changed = True

    if changed:
        save_map(mapping)
    else:
        print("No changes needed — map is complete.")

if __name__ == "__main__":
    main()


