### ⚠️ Quick Fix for the Bug in `index.html`

You've added this line:

```html
<script src="preview-tier/components/tier_switcher.html"></script>
```

That **will not work**, because `.html` files can’t be loaded as `<script src="...">`. That syntax is for `.js` files only.

---

### ✅ Fix: Use `fetch()` to dynamically inject it (like below):

You should **remove** that script tag and instead use:

```html
<script>
  window.location.href = "membership/free/";
</script>

<!-- Optional Dev Tool: Tier Dropdown Preview -->
<div id="tier-preview-ui"></div>
<script>
  fetch('preview-tier/components/tier_switcher.html')
    .then(res => res.text())
    .then(html => {
      document.getElementById('tier-preview-ui').innerHTML = html;
    });
</script>
```

> 🔁 That way, your redirect still works as-is for users, but if you're debugging in local mode, you’ll see the dropdown **before** being redirected.

---

### 🧹 You should also clean up your structure like this:

| Location                          | Purpose                      |
| --------------------------------- | ---------------------------- |
| `assets/js/simulate_user_tier.js` | 🔐 Auth logic (used by site) |
| `preview-tier/components/`        | 🧪 Reusable HTML snippets    |
| `preview-tier/test/`              | 🧪 Full test/demo pages      |

---

### ✅ Recommendation for Next Steps

1. ✅ Fix `index.html` per above (remove bad `<script src=...>`).
2. ✅ Add new test file `tier_preview_demo.html` to `preview-tier/test/`
3. ✅ Commit + tag with `v1.4.2-preview-tier-ui`
4. ✅ Push branch and test live at GitHub Pages
5. ✅ Optional: Create `README_PREVIEW.md` to explain test tools


