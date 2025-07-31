#!/usr/bin/env python3
import os
from collections import defaultdict

root = "articles"
dup = defaultdict(list)

for dirpath, _, filenames in os.walk(root):
    for fname in filenames:
        if fname.lower().endswith(".html"):
            fpath = os.path.join(dirpath, fname)
            try:
                size = os.path.getsize(fpath)
                dup[size].append(fpath)
            except OSError:
                continue

for size, paths in sorted(dup.items(), key=lambda x: -len(x[1])):
    if len(paths) > 1:
        print(f"\n⚠️ Possible duplicates ({len(paths)} files, size={size} bytes):")
        for p in paths:
            print("  •", p)

