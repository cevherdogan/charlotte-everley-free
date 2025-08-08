# 🛠 Restore Point Playbook

This playbook outlines the **safe and repeatable steps** for rolling back a branch to a **known good commit** and protecting that state.

---

## 1️⃣ Pre-flight: Backup & Safety

```bash
# Save any uncommitted changes
git status
git stash push -u -m "pre-restore $(date +%F-%H%M)"

# Create a rescue branch from current HEAD
git switch -c rescue/$(date +%F-%H%M)
````

---

## 2️⃣ Identify the Known Good Commit

Use one of the following:

```bash
# Check recent commits on this branch
git log --oneline --decorate -n 20

# Search for commits in deleted branches
git reflog --all --date=iso | grep -i "<keyword>"
```

Example: we identified commit `3f0266b` (`Fixed tier cascading`) as the good one.

---

## 3️⃣ Create a Test Branch at That Commit

```bash
git switch -c restore/<short-name>-OK <commit_sha>

# Run local tests
bash charlotteeverley-site/runserver.sh
# OR
python3 -m http.server 8000
# Then open and verify in browser
```

---

## 4️⃣ Promote to Target Branch

Once confirmed good:

```bash
git switch <target_branch>   # e.g. fix/tier-inheritance
git reset --hard restore/<short-name>-OK
git push --force-with-lease
```

---

## 5️⃣ Tag the Restore Point

```bash
git tag -a good/<short-name>-$(date +%F) -m "Known good commit"
git push origin good/<short-name>-$(date +%F)
```

---

## 6️⃣ (Optional) Merge to Main

```bash
git switch main
git merge --ff-only <target_branch> || git merge <target_branch>
git push
```

---

## 7️⃣ Cleanup

```bash
git branch -d restore/<short-name>-OK
# Keep rescue/* branches as long as needed
```

---

## Notes & Tips

* Always **stash or commit** before resets.
* Prefer `--force-with-lease` over `--force` for safer pushes.
* Tagging good states allows instant rollback later:

  ```bash
  git switch -c restore-from-tag good/<short-name>-2025-08-08
  ```
* If unsure about the commit SHA, use:

  ```bash
  git log --graph --decorate --oneline --all
  ```

---
