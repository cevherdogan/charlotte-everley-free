# pick up token
unset GITHUB_TOKEN


export $(grep -v '^#' .env | xargs)
export GH_TOKEN="$GH_PAT"         # gh prefers GH_TOKEN
export GITHUB_TOKEN="$GH_PAT"     # also fine; belt & suspenders

gh auth status -h github.com
gh api rate_limit | jq '.resources.core'

# sadece görselleri geri al (çalışma alanı + staged aynı anda)
git restore --staged --worktree \
  assets \
  charlotteeverley-site/assets \
  sb/gallery_quickstart/assets/images/raw

