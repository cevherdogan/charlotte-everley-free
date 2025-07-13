## 📝 **Release Notes – Charlotte Everley Site**

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

