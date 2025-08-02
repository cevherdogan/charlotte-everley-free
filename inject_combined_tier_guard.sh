#!/bin/bash

COMBINED_SCRIPT='<script src="/assets/js/combined_user_tier_guard.js"></script>'
TARGET_DIRS=("membership/free" "membership/trial" "membership/silver" "membership/gold")

for dir in "${TARGET_DIRS[@]}"; do
  find "$dir" -name "*.html" | while read -r file; do
    if grep -q "<head>" "$file"; then
      # Remove any previous tier_guard or check_user_tier_access includes
      sed -i '' '/tier_guard.js/d' "$file"
      sed -i '' '/check_user_tier_access.js/d' "$file"

      # Insert the combined script two lines after <head>
      awk -v script="$COMBINED_SCRIPT" '
        /<head>/ { print; getline; print; print script; next }
        { print }
      ' "$file" > tmpfile && mv tmpfile "$file"

      echo "✅ Injected combined script into: $file"
    fi
  done
done
