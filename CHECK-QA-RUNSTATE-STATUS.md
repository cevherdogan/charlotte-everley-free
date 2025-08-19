Perfect—let’s run the latest **local** exactly as-is and sanity-check tiers, including the old **bronze/premier** mapping.

Below is a tight, copy-paste plan using the scripts you already have.

# 0) Save your current state (optional but wise)

```bash
git add -A && git commit -m "wip: pre-local-run" || true
./scripts/chk-branch.sh || git branch
./scripts/safepoint.sh || true
```

# 1) Discover flags (so we don’t guess)

```bash
# See what the helpers expect:
./runserver.sh -h 2>/dev/null || true
./start-local-test.sh -h 2>/dev/null || true
./prj-start-local-test.sh -h 2>/dev/null || true

python3 scripts/simulate_rbac_access.py --help || true
python3 scripts/migrate_bronze_premier.py --help || true
python3 scripts/render_gallery.py --help || true
```

# 2) Run the local server

Try in this order (stop at the first that works):

```bash
./prj-start-local-test.sh || ./start-local-test.sh || ./runserver.sh
```

Typical outcomes:

* prints a **localhost** URL (e.g., [http://127.0.0.1:8080](http://127.0.0.1:8080) or 3000)
* serves the static site you had on GH Pages

# 3) Quick gallery/assets sanity

```bash
./view_gallery.sh || true
./sync_thumbnails.sh || true
```

# 4) Check the tier matrix (current truth)

You have a ready helper:

```bash
./scripts/check_tiers.sh || true
python3 scripts/simulate_rbac_access.py --all || true
```

If `--all` isn’t supported, try a few specifics (common patterns):

```bash
python3 scripts/simulate_rbac_access.py --tier free --url /   || true
python3 scripts/simulate_rbac_access.py --tier trial --url /  || true
python3 scripts/simulate_rbac_access.py --tier silver --url / || true
python3 scripts/simulate_rbac_access.py --tier gold --url /   || true
# legacy ones, if supported:
python3 scripts/simulate_rbac_access.py --tier bronze --url /   || true
python3 scripts/simulate_rbac_access.py --tier premier --url /  || true
```

# 5) Bronze/Premier → current tiers (dry-run first)

Use your dedicated migrator to see what it would change:

```bash
python3 scripts/migrate_bronze_premier.py --dry-run || true
# If it supports explicit mapping flags, something like:
# python3 scripts/migrate_bronze_premier.py --map bronze=silver --map premier=gold --dry-run
```

If the output looks good, run the real thing:

```bash
python3 scripts/migrate_bronze_premier.py || true
git status
```

# 6) Verify galleries respect trial/gold (your helper exists)

You’ve got a convenience script:

```bash
./sync-gold-to-trial-bands-gallery-support.sh || true
```

Then re-render/select a sample page:

```bash
python3 scripts/render_gallery.py --help || true
# Example guesses:
python3 scripts/render_gallery.py --tier trial   --out .local_out/trial   || true
python3 scripts/render_gallery.py --tier gold    --out .local_out/gold    || true
python3 scripts/render_gallery.py --tier silver  --out .local_out/silver  || true
python3 scripts/render_gallery.py --tier free    --out .local_out/free    || true
```

# 7) Manual spot-checks in the browser

Open the local server URL and check:

* **Free**: only public/marketing sections; no premium galleries.
* **Trial**: trial-enabled galleries visible; upsell CTA shows.
* **Silver**: everything Free+Trial+Silver features; no Gold-only.
* **Gold**: full access, including premium gallery sections.
* (Legacy) **Bronze/Premier**: confirm they now behave as **Silver/Gold** respectively (post-migration).

# 8) Link and content hygiene (optional but handy)

```bash
node scripts/linkChecker.esm.js || true
python3 scripts/find_duplicate_html.py || true
python3 scripts/find_duplicate_html_2.py || true
python3 scripts/fix_gallery_anchors.py || true
python3 scripts/auto_fix_gallery.py || true
python3 scripts/update_thumbnail_map.py || true
```

# 9) Zip a snapshot (if you want a portable build)

```bash
./zipit.sh || true
```

---

## If something looks off

* Rewind to your restore point:

  ```bash
  ./scripts/git/force-lock-or-guard.sh 2>/dev/null || true
  git restore -SW . 2>/dev/null || true
  ```
* Or compare to a **known-good tag** you listed:

  ```bash
  git diff --stat good/tier-inheritance-2025-08-08...HEAD
  ```

---

When you’ve run steps 1–5, tell me which **localhost URL** it served and any console errors you saw. I’ll map that to your exact server and wire the tier gates on the landing page next (keeping the bronze/premier compatibility you mentioned).


