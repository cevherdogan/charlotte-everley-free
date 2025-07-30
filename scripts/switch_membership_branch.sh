#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 <tier>"
  echo "Available tiers: free, trial, silver, gold"
  exit 1
fi

TIER="$1"
BRANCH="membership-$TIER"
SRC_FILE="membership/$TIER/index.html"
DEST_FILE="index.html"

# Validate source
if [ ! -f "$SRC_FILE" ]; then
  echo "❌ File not found: $SRC_FILE"
  exit 1
fi

# Create or switch to the branch
if git show-ref --verify --quiet refs/heads/$BRANCH; then
  echo "✔️ Switching to existing branch: $BRANCH"
  git checkout $BRANCH
else
  echo "🆕 Creating and switching to new branch: $BRANCH"
  git checkout -b $BRANCH
fi

# Move the file
cp "$SRC_FILE" "$DEST_FILE"

# Commit and push
git add "$DEST_FILE"
git commit -m "🏕️ Set up $TIER membership landing page"
echo "✅ $DEST_FILE updated for $TIER tier."

# Optional push
# git push -u origin $BRANCH



