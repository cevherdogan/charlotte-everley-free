# 🧭 RBAC Tiered Access Flow

This branch implements Role-Based Access Control (RBAC) for Charlotte Everley content and galleries.

## 📁 Structure

- `rbac-map.json`: Original tier access mapping (raw format)
- `access_map.json`: Normalized version used for rendering
- `gallery.html`: Tier-based tile rendering (coming next)
- `membership/`: Articles separated by tier (trial, silver, etc.)
- `scripts/`: Helpers for syncing or previewing content

## 🧠 Tier Logic

Each plan (`free`, `trial`, `silver`, `gold`) controls:
- Visible articles (`membership/<tier>/articles/`)
- Visible gallery tags (`charlotteeverley-site/gallery.html` tiles filtered)

## 🚦 Dev Mode Switcher

A simple dropdown-based plan simulator will be available to preview as different roles.

## 🧪 Branch

- Name: `dev/rbac-tiered-access`
- Status: ⚙️ In progress (patching gallery tier gating next)
