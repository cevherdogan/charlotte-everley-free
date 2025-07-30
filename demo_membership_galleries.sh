#!/bin/bash

# Script: demo_membership_galleries.sh
# Purpose: Switch to each membership branch and open its gallery

branches=("membership-free" "membership-trial" "membership-silver" "membership-gold")

for branch in "${branches[@]}"; do
  echo "🔄 Switching to: $branch"
  git checkout "$branch" >/dev/null 2>&1 || {
    echo "❌ Branch $branch does not exist. Skipping..."
    continue
  }

  echo "⚡ Running gallery viewer for: $branch"
  ./view_gallery.sh
  echo "✅ Opened gallery for: $branch"
  echo ""
  read -p "Press [Enter] to continue to the next tier..." temp
done

echo "🎉 All membership galleries previewed."

