# simulate_rbac_access.py

import json

ACCESS_FILE = "access_map.json"
GALLERY_YAML = "config/gallery_items.yaml"

def load_access_map():
    with open(ACCESS_FILE, "r") as f:
        return json.load(f)["plans"]

def simulate(plan, access_map):
    if plan not in access_map:
        print(f"❌ Plan '{plan}' bulunamadı. Mevcut planlar: {', '.join(access_map.keys())}")
        return

    data = access_map[plan]
    print(f"\n📦 Plan: {plan.upper()}")
    print("📄 Articles:")
    for a in data.get("articles", []):
        print(f"  - {a}")

    print("\n🖼 Gallery Tags:")
    for tag in data.get("gallery_tags", []):
        print(f"  - {tag}")

if __name__ == "__main__":
    access_map = load_access_map()
    print("💡 Mevcut planlar:", ", ".join(access_map.keys()))
    selected = input("👉 Lütfen bir plan adı girin (örnek: bronze): ").strip().lower()
    simulate(selected, access_map)

