# 1) Do we have node_modules tracked?
git ls-files node_modules | wc -l

# 2) Repo size & loose objects
git count-objects -vH

# 3) Biggest objects in history (top 20)
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  awk '$1=="blob"{print $3, $4}' | sort -n | tail -20


