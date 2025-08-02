#!/bin/bash

# Path to the JS block you'd like to insert (adjust if needed)
TIER_GUARD_SCRIPT='<script src="/assets/js/tier_guard.js"></script>'

# Find and process all .html files under membership/
find membership/ -type f -name "*.html" | while read -r file; do
  # Check if it already has the guard (skip if it does)
  grep -q "$TIER_GUARD_SCRIPT" "$file" && echo "✔️ Already injected: $file" && continue

  # Insert after <head> (on a new line after the first occurrence)
  awk -v script="$TIER_GUARD_SCRIPT" '
    BEGIN { injected = 0 }
    /<head[^>]*>/ {
      print $0;
      if (!injected) {
        print "  " script;
        injected = 1;
        next
      }
    }
    { print }
  ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
  
  echo "✅ Injected into: $file"
done

