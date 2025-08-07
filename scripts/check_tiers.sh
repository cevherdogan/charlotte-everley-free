#!/usr/bin/env bash
set -euo pipefail
if grep -RInE '\b(trial|gold)\b' charlotteeverley-site/ articles/ scripts/ sync_thumbnails.sh test_rbac_access.py rbac-map.json --exclude-dir=.git ; then
  echo "❌ Legacy tier names found"; exit 1
fi
jq -e '.plans | keys | sort == ["bronze","free","premier","silver"]' access_map.json >/dev/null \
  || { echo "❌ access_map.json plans mismatch"; exit 1; }
echo "✅ Tier names OK"
