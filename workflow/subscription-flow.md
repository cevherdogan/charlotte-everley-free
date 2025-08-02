# 📦 Charlotte Everley – Subscription Flow & RBAC Access

This document outlines the end-to-end user journey for subscribing, accessing, and upgrading content based on role-based access control (RBAC).

---

## 🔑 Plan Tiers

| Plan     | Features                              | Price         |
|----------|----------------------------------------|---------------|
| Free     | 3 GPT prompts                         | Free          |
| Bronze   | 3 prompts/month, seasonal tone         | $29/mo        |
| Silver   | 5 prompts/month, community access      | $49/mo        |
| Premier  | Unlimited, instant edits, calendar     | $99/mo        |

Each plan is managed via Stripe Checkout buttons embedded in `index.html`.

---

## 🔐 Authentication + RBAC

- Upon login (or trial start), user is tagged with their plan.
- `access_map.json` defines what each plan can access:
  - `membership/<plan>/articles/*.html`
  - `gallery.html` tiles marked with `data-tier="..."`

---

## 🖼 Gallery View

- Responsive grid of story tiles
- Each tile is wrapped in:
  ```html
  <div class="tile" data-tier="silver">...</div>
  ```
- Users see only tiles within or below their plan tier

---

## 🛒 Upsell & Promotion Logic

If a tile is not within the user’s access, show a soft upsell message:
```html
<div class="text-sm text-gray-600 italic">
  This content is available in Silver or higher.
  <a href="/upgrade" class="text-blue-600 underline">Upgrade</a>
</div>
```

---

## 🧪 Dev Mode / Simulation

- JS-based dropdown included in gallery for tier preview
- Useful for local testing or QA

---

## 📁 Files Involved

- `index.html` → plan overview + Stripe links
- `charlotteeverley-site/gallery.html` → RBAC-enforced tile view
- `access_map.json` → actual tier mapping
- `README_WORKFLOW.md` → implementation logic
- `workflow/subscription-flow.md` → high-level product flow

