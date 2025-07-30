# 📚 RBAC Design & DevOps Flow for `charlotte-everley-free`

## 🔐 1. Role-Based Access Control (RBAC) Architecture

### 🎯 Principle

Access is determined by:

* **Subscription plan** (free, trial, silver, gold)
* **Folder structure** (`membership/{tier}/articles/`)
* **Git branch** (`membership-{tier}` branch reflects tier access scope)

### 📁 Directory-to-Plan Mapping

| Plan Name | Git Branch          | Access Includes                |
| --------- | ------------------- | ------------------------------ |
| `free`    | `membership-free`   | `free/` only                   |
| `trial`   | `membership-trial`  | `trial/` + `free/`             |
| `silver`  | `membership-silver` | `silver/` + `trial/` + `free/` |
| `gold`    | `membership-gold`   | All tiers                      |

---

## 🛠 2. Dev & Test Workflow

### ⏳ Setup

* Always start a new feature or content under the appropriate branch
* Ensure `rbac-map.json` is regenerated after changes:

```bash
python3 generate_rbac_map.py
```

### 🧪 Local Testing

#### 🔹 Content Visibility

* Run gallery generator script
* Verify that current branch matches expected RBAC visibility:

```bash
git rev-parse --abbrev-ref HEAD  # should return membership-gold, etc.
```

#### 🔹 Branch-Scoped Article Count (via RBAC map)

Expected article counts:

* `free`: 4
* `trial`: 6 (4 free + 2 trial)
* `silver`: 9 (trial + silver + free)
* `gold`: 13 (all)

### 🔹 Gallery Rendering

Update `generate_gallery.py` to:

* Read `rbac-map.json`
* Detect current tier from branch
* Merge lower tier access
* Output only permitted articles

---

## 🏭 3. Production System Behavior

### 💳 Subscriber Authentication

* Users authenticate via login or API key
* Each account is assigned a `plan` (`free`, `silver`, etc.)

### 📜 On Access

* Server reads `rbac-map.json`
* Looks up `plan → allowed articles`
* Gallery or article access is filtered in backend or via API responses

---

## 👥 4. Simulated Test Accounts

| Username     | Plan   | Expected Access Count |
| ------------ | ------ | --------------------- |
| test\_free   | free   | 4                     |
| test\_trial  | trial  | 6                     |
| test\_silver | silver | 9                     |
| test\_gold   | gold   | 13                    |

You can mock this with a simple Python CLI or JSON-driven front end to validate access responses.

