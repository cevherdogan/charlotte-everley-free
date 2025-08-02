#!/bin/bash

TARGET_SCRIPT='<script src="/assets/js/check_user_tier_access.js"></script>'

# Loop through all relevant HTML files
find membership -type f -name "*.html" | while read -r file; do
  # Remove existing tier_guard.js or duplicate check_user_tier_access.js
  sed -i '' '/<script src="\/assets\/js\/tier_guard\.js"><\/script>/d' "$file"
  sed -i '' '/<script src="\/assets\/js\/check_user_tier_access\.js"><\/script>/d' "$file"

  # Find the <head> tag and insert the target script two lines after it
  awk -v target="$TARGET_SCRIPT" '
    BEGIN { injected = 0 }
    /<head[^>]*>/ {
      print
      getline; print  # Print next line
      print target     # Insert script
      injected = 1
      next
    }
    { print }
  ' "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"

  echo "✅ Re-injected guard into: $file"
done

