# ✅ TODO – Membership Tracker (2025-08-01)

This tracker complements the August 1, 2025 status report for the `aa-access-refactor` branch and v1.3.0 tag.

---

## 🔁 Restorations

* [x] Determine last tag with confirmed `/membership/` content → ✅ `v1.0-launch-charlotteeverley`
* [ ] Restore all tier directories via:

```bash
git checkout v1.0-launch-charlotteeverley -- membership/
```

* [ ] Confirm correct rendering via `http-server` or Vercel/GHP preview

---

## 🧪 Functional QA

* [ ] Confirm buttons on `/index.html` route properly to each tier page
* [ ] Confirm at least 1 article exists and is readable in each `/membership/{tier}/`
* [ ] Ensure metadata overlays and gallery thumbnails work on `gallery.html`

---

## 🔄 Transitional Logic

* [ ] Add dropdown or toggle for tier switching using `localStorage`
* [ ] Display correct banner message by simulated tier state
* [ ] Optional: allow query param override (?tier=silver)

---

## 🔐 Authentication Prep

* [ ] Stub logic to detect tier from JWT / session token
* [ ] Move tier detection into `/auth/membership-check.js`
* [ ] Annotate current hardcoded behavior for future AA replacement

---

## 🧱 Build Cleanup

* [ ] Tag restored version: `v1.4.0-aa-base`
* [ ] Prepare `/membership` backup as downloadable zip
* [ ] Add shell script to auto-restore in future if files go missing

---

Prepared: August 1, 2025
By: Cevher Dogan & AI Support

