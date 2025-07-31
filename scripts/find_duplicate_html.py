import os
import re
from collections import defaultdict

ARTICLE_ROOT = "articles"

def find_html_files():
    html_files = []
    for root, _, files in os.walk(ARTICLE_ROOT):
        for f in files:
            if f.endswith(".html"):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, ARTICLE_ROOT)
                size = os.path.getsize(full_path)
                html_files.append((rel_path, size))
    return html_files

def group_variants(files):
    pattern = re.compile(r"^(.*?)(?:-(\d+))?\.html$")
    groups = defaultdict(list)
    for path, size in files:
        match = pattern.match(os.path.basename(path))
        if match:
            key = os.path.join(os.path.dirname(path), match.group(1))
            num = int(match.group(2)) if match.group(2) else None
            groups[key].append((path, size, num))
    return groups

def report_exact_size_dupes(groups):
    found = False
    for base, versions in groups.items():
        numbered = [v for v in versions if v[2] is not None]
        unnumbered = [v for v in versions if v[2] is None]
        if not numbered or not unnumbered:
            continue
        last = max(numbered, key=lambda x: x[2])
        orig = unnumbered[0]
        print(f"🔍 Checking: {orig[0]} vs {last[0]} | sizes: {orig[1]} vs {last[1]}")
        if last[1] == orig[1]:
            print("⚠️ Last-numbered file is same size as original:")
            print(f"  • {orig[0]}")
            print(f"  • {last[0]}\n")
            found = True
    if not found:
        print("✅ No same-size duplicates between unnumbered and highest-numbered files.")

if __name__ == "__main__":
    files = find_html_files()
    grouped = group_variants(files)
    report_exact_size_dupes(grouped)

