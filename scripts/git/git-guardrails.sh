# delete the scratch branch if you want
git branch -D restore/tier-inheritance-OK

# (optional) rebase related branches on top of the good commit
git switch membership-silver
git rebase fix/tier-inheritance
# repeat for other membership/* branches as needed


