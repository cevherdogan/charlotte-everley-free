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

def group_by_base_name(files):
    pattern = re.compile(r"(.*?)(?:-(\d+))?\.html$")
    groups = defaultdict(list)
    for path, size in files:
        match = pattern.match(path)
        if match:
            base = match.group(1)
            number = match.group(2)
            key = base if number is None else f"{base}-*"
            groups[key].append((path, size, int(number) if number else None))
    return groups

def detect_duplicates(groups):
    for key, entries in groups.items():
        if len(entries) < 2:
            continue
        sorted_entries = sorted(entries, key=lambda x: (x[2] is None, x[2] if x[2] is not None else 0))
        if sorted_entries[-1][2] is not None:
            last_numbered = sorted_entries[-1]
            unnumbered = next((e for e in sorted_entries if e[2] is None), None)
            if unnumbered and last_numbered[1] == unnumbered[1]:
                print(f"⚠️ Potential duplicate (size={unnumbered[1]} bytes):")
                print(f"  • {unnumbered[0]}")
                print(f"  • {last_numbered[0]}\n")

if __name__ == "__main__":
    html_files = find_html_files()
    grouped = group_by_base_name(html_files)
    detect_duplicates(grouped)

