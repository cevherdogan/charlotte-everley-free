## 📝 **Release Notes – Charlotte Everley Site**

# Charlotte Everley – Main Line Living

## Release Notes

## v1.1.0 — RBAC Gallery Engine 🎉

### ✨ Features

- 💡 **RBAC-Driven Article Access**
  - Each branch (`membership-free`, `-trial`, `-silver`, `-gold`) contains its own gated content
  - `rbac-map.json` governs tier-specific access
  - `test_rbac_access.py` validates visibility rules per simulated user

- 🖼 **Responsive Gallery Generator**
  - `generate_gallery.py` dynamically creates a tile-based HTML gallery
  - Renders only accessible articles based on current Git branch
  - Tier badges, article links, and hierarchy-aware ordering

- 🔁 **Visual Testing Script**
  - `view_gallery.sh` regenerates and opens tier-based gallery
  - `demo_membership_galleries.sh` cycles through all membership levels for visual QA

- 🧪 **Testing + Documentation**
  - `tests/RBAC_TEST_GUIDE.md` documents setup and testing flow
  - `README_DEMO_RBAC.md` provides clear onboarding + usage

---

### v1.0.0 – July 2025

- Launched article-first static site at [charlotteeverley.foundral.tech](https://charlotteeverley.foundral.tech)
- Published first two lifestyle features:
  - Berwyn: “Where the Quiet Speaks Volumes”
  - Devon: “Tradition with a Quiet Grace”
- SEO-enabled with `sitemap.xml`, `robots.txt`, and meta tags
- Directory structure redesigned for scaling content, clarity, and search indexing
- GitHub Pages integration complete

---

Next release: dynamic article index, MDX authoring, and image SEO enhancements.

### Version: `v0.3.5`

📅 Date: 2025-07-13
🔖 Tag: `v0.3.5`
👤 Author: Cevher Dogan

---

### 🎯 Summary

This release unifies all pricing plan cards—**Bronze**, **Silver**, and **Premier**—with a consistent visual and interactive structure. All plans are now fully clickable, styled with smooth hover effects, and integrated with live Stripe checkout links.

---

### ✅ What’s New

* 🟤 **Bronze Plan**

  * Added hover-highlighted border
  * Clickable entire card via `<a>` wrap
  * Linked to live Stripe subscription: `$29/mo or $79/quarter`

* 🥈 **Silver Plan**

  * Highlighted card with blue border ring and subtle shadow
  * Most Popular tag retained
  * Linked to Stripe with free trial support

* 💎 **Premier Plan**

  * Premium layout with full-card link
  * Clean shadow and hover styling
  * Direct checkout via Stripe

---

### 🔧 Technical Improvements

* Tailwind utility classes used for clean transitions:
  `group-hover:border-*`, `group-hover:shadow-*`, `transition`, `rounded-2xl`
* Removed legacy mixed HTML blocks causing syntax issues
* Ensured full accessibility and mobile responsiveness
* Schema.org structured data remains untouched for SEO

---

### 🔗 Live Stripe Links

| Plan    | Link                                                        |
| ------- | ----------------------------------------------------------- |
| Bronze  | [Subscribe](https://buy.stripe.com/7sY9AT9xG4BH7Kf9FPfQI09) |
| Silver  | [Subscribe](https://buy.stripe.com/6oU4gzeS07NTc0v7xHfQI06) |
| Premier | [Subscribe](https://buy.stripe.com/bJe28reS03xDfcHg4dfQI07) |

---

### 📌 Next Steps

* Add branded illustrations or plan-specific icons
* Add trial-based dynamic messaging via JS (`?trial=true`)
* Implement plan comparison table for FAQ-style clarity

