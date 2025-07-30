#!/bin/bash
set -e

echo "🔄 Syncing article thumbnails from assets..."

while IFS= read -r article; do
  slug="${article%.html}"
  filename="${slug}.jpg"
  src="assets/${slug}.png"
  dest="thumbnails/${filename}"

  if [[ -f "$src" ]]; then
    cp "$src" "$dest"
    echo "✔️ Copied $src → $dest"
  else
    echo "⚠️ No asset for $article; skipping"
  fi
done < <(jq -r '.trial[], .silver[], .gold[], .free[]' rbac-map.json)

