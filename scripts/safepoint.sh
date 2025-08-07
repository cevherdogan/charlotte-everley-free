#!/usr/bin/env bash
set -euo pipefail
ts=$(date +'%Y%m%d-%H%M')
msg=${1:-"checkpoint"}
git add -A
git commit -m "$msg @ $ts" || echo "No changes to commit"
git tag -a "checkpoint-$ts" -m "$msg"
git push -u origin "$(git rev-parse --abbrev-ref HEAD)"
git push origin --tags
echo "✅ safepoint created: checkpoint-$ts"

