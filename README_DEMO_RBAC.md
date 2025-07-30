## 📘 README Snippet (Usage Instructions)

````markdown
# 🧪 RBAC Gallery Demo

This repository includes a dynamic HTML gallery system that respects subscription access levels (Free, Trial, Silver, Gold).

## 📂 How It Works

- Each membership tier has its own Git branch:
  - `membership-free`
  - `membership-trial`
  - `membership-silver`
  - `membership-gold`

- Running `./view_gallery.sh` in any branch generates a responsive HTML gallery based on the access level.

## 🚀 Quick Demo

Use this script to cycle through all branches and preview access-specific galleries:

```bash
./demo_membership_galleries.sh
````

It will:

* Switch to each branch
* Run `generate_gallery.py`
* Open `gallery.html` in your browser
* Pause for confirmation before moving to the next tier

## 🛠 Add New Articles?

1. Add the article HTML under the appropriate `membership-*/articles/` directory
2. Update `rbac-map.json` accordingly
3. Re-run:

```bash
python3 test_rbac_access.py
./view_gallery.sh
```

That’s it!
