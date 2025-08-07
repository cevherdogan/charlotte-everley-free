#!/bin/bash
set -e

# Detect where we came from
origin_branch=$(git reflog | grep -m1 "checkout: moving from" | head -n1 | sed -E 's/.*moving from ([^ ]+) to.*/\1/')

if [ -z "$origin_branch" ]; then
    echo "❌ Could not detect origin branch from reflog."
    exit 1
fi

current_branch=$(git rev-parse --abbrev-ref HEAD)

echo "🔍 Detected origin branch: $origin_branch"
echo "🔍 Current branch: $current_branch"

read -p "➡️ Merge $current_branch into $origin_branch and delete $current_branch? (y/n) " confirm
if [[ "$confirm" != "y" ]]; then
    echo "❌ Aborted."
    exit 1
fi

# Checkout origin branch
git checkout "$origin_branch"

# Merge the changes
git merge --no-ff "$current_branch"

# Optional: delete the branch after merge
read -p "🗑 Delete branch $current_branch? (y/n) " delconfirm
if [[ "$delconfirm" == "y" ]]; then
    git branch -d "$current_branch"
fi

echo "✅ Merge complete."

