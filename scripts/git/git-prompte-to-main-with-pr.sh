# keep history clean with a fast-forward if possible:
git switch main
git merge --ff-only fix/tier-inheritance   # if this fails, use a PR or do a regular merge
git push


