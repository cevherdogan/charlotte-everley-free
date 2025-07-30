# 🧪 RBAC Test Strategy & Maintenance Guide

## 🎯 Purpose

This script (`test_rbac_access.py`) ensures that subscription-based article access matches the expected Role-Based Access Control (RBAC) configuration defined in `rbac-map.json`.

---

## 📁 Structure Overview

| Tier     | Path                          |
| -------- | ----------------------------- |
| `free`   | `membership/free/articles/`   |
| `trial`  | `membership/trial/articles/`  |
| `silver` | `membership/silver/articles/` |
| `gold`   | `membership/gold/articles/`   |

> Access is **cumulative**: gold users can view everything in lower tiers.

---

## 🧪 Running the Test

### 1. Regenerate the RBAC map:

```bash
python3 generate_rbac_map.py
```

### 2. Run the test suite:

```bash
python3 test_rbac_access.py
```

### ✅ Output

The script will print whether each test user has the correct number of articles available based on their tier.

---

## ✍️ When to Update Things

### 🆕 When Adding an Article:

1. Place the article in the correct folder:

   ```
   membership/{tier}/articles/
   ```
2. Use a **clear, tier-specific filename** if there's an article version split (e.g., `_trial`, `_gold`)
3. Rerun:

   ```bash
   python3 generate_rbac_map.py
   ```

### 🧮 Then Update Expected Counts in `test_rbac_access.py`:

```python
"test_gold": {
    "plan": "gold",
    "expected_count": 15  # update this if article count changed
}
```

### 🔁 Rerun Test:

```bash
python3 test_rbac_access.py
```

---

## 🧠 Tips

* Keep filenames **unique per tier** unless you mean to overwrite
* Use suffixes like `_free`, `_trial`, `_silver`, `_gold` if content is related but distinct
* Commit both the new article and the updated `rbac-map.json`


