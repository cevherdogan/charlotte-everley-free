#!/usr/bin/env bash
set -euo pipefail

#######################################################################
# 0. CONFIG ––– CHANGE THIS ONLY
#######################################################################
# GPT_LINK="https://chatgpt.com/g/xxxxxxxxxxxxxxxxxxxxxxxx"
GPT_LINK="https://chatgpt.com/g/g-6860c800e62c81919f3dcb86a558e1d1"
PAGE_REDIRECT=true        # true  = auto-redirect GitHub Pages to GPT
DISCUSS_PIN=true          # false = skip creating a pinned Discussion
#######################################################################

QS_BLOCK=$(cat <<EOF
## Quick Start

### macOS  
\`1.\` Open ${GPT_LINK} in any browser.  
\`2.\` Drag the URL onto your desktop to create a shortcut.  

### iOS  
\`1.\` Open the link in **Safari**.  
\`2.\` Share → **Add to Home Screen**.  

> **Note:** Free-plan users get **GPT-4o** by default; Plus/Pro users can switch models if available.
EOF
)

echo "▸ Updating README.md …"
if ! grep -q "## Quick Start" README.md 2>/dev/null; then
  printf "\n%s\n" "$QS_BLOCK" >> README.md
else
  echo "  README already contains a Quick Start section – skipped."
fi

echo "▸ Creating docs/index.md …"
mkdir -p docs
{
  $PAGE_REDIRECT && echo "<meta http-equiv=\"refresh\" content=\"0; url=${GPT_LINK}\" />"
  printf "\n# Charlotte Everley — Quick Start\n\nSee the **README** for macOS & iOS shortcut steps.\n"
} > docs/index.md

echo "▸ Committing README + Pages …"
git add README.md docs/index.md
git commit -m "Docs: Quick Start instructions (README + GitHub Pages)"
git push origin main

echo "▸ Ensuring GitHub Pages is enabled …"
gh api -X PATCH "repos/:owner/:repo" \
  -f "has_pages=true" >/dev/null
# Default branch /docs folder is auto-detected because .nojekyll + docs/index.md exist.

echo "▸ Seeding Wiki …"
TMP_DIR=$(mktemp -d)
git clone --quiet "https://github.com/$(gh repo view --json nameWithOwner -q .nameWithOwner).wiki.git" "$TMP_DIR/wiki"
printf "# Getting Started\n\n%s\n" "$QS_BLOCK" > "$TMP_DIR/wiki/Getting-Started.md"
(
  cd "$TMP_DIR/wiki"
  git add Getting-Started.md
  git commit -m "Getting Started page: desktop & iOS instructions" >/dev/null
  git push --quiet
)

if $DISCUSS_PIN; then
  echo "▸ Creating pinned Discussion …"
  # 1. create discussion
  DISC_ID=$(gh api graphql -f query='
    mutation($repo:ID!,$title:String!,$body:String!) {
      createDiscussion(input:{
        repositoryId:$repo,
        title:$title,
        body:$body,
        categoryId:(repositoryDiscussionCategories(first:1){nodes{id}}).nodes[0].id
      }) { discussion { id number } }
    }' -F repo=$(gh api graphql -f query='{repository(name:"'$(
      gh repo view -q .name
    )'",owner:"'$(gh repo view -q .owner.login)'"){id}}' -q .data.repository.id) \
    -F title="How to launch the GPT" \
    -F body="$QS_BLOCK" | jq -r '.data.createDiscussion.discussion.id')

  # 2. pin it
  gh api graphql -f query='
    mutation($id:ID!){
      pinDiscussion(input:{discussionId:$id}){discussion{id}}
    }' -F id="$DISC_ID" >/dev/null
fi

echo "✅  All done!  README, GitHub Pages, Wiki page, and Discussion (pinned) are live."

