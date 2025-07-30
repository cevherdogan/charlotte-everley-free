import os
import json

RBAC_ROOT = "membership"
OUTPUT_FILE = "rbac-map.json"

def collect_rbac_map():
    rbac_map = {}

    for band in os.listdir(RBAC_ROOT):
        band_path = os.path.join(RBAC_ROOT, band, "articles")
        if not os.path.isdir(band_path):
            continue

        files = [
            f for f in os.listdir(band_path)
            if os.path.isfile(os.path.join(band_path, f)) and f.endswith(".html")
        ]

        rbac_map[band] = sorted(files)

    return rbac_map

def main():
    rbac_data = collect_rbac_map()

    with open(OUTPUT_FILE, "w") as out:
        json.dump(rbac_data, out, indent=2)
    
    print(f"✅ RBAC map generated at: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()


