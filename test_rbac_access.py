import json

RBAC_FILE = "rbac-map.json"

# Simulated test users and their plans
test_accounts = {
    "test_free": {
        "plan": "free",
        "expected_count": 4
    },
    "test_trial": {
        "plan": "trial",
        "expected_count": 6  # 4 free + 2 trial
    },
    "test_silver": {
        "plan": "silver",
        "expected_count": 9  # 6 from trial + silver
    },
    "test_gold": {
        "plan": "gold",
        "expected_count": 14  # all tiers
    }
}

# Order of tiers (hierarchical inheritance)
tier_order = ["free", "trial", "silver", "gold"]

def get_accessible_articles(rbac_map, current_plan):
    idx = tier_order.index(current_plan)
    allowed_tiers = tier_order[:idx + 1]

    articles = []
    for tier in allowed_tiers:
        articles.extend(rbac_map.get(tier, []))
    return sorted(set(articles))

def main():
    with open(RBAC_FILE, "r") as f:
        rbac_map = json.load(f)

    print("🔐 RBAC Access Test Summary\n")

    for user, info in test_accounts.items():
        accessible = get_accessible_articles(rbac_map, info["plan"])
        actual_count = len(accessible)
        expected_count = info["expected_count"]
        status = "✅ PASS" if actual_count == expected_count else "❌ FAIL"

        print(f"{status} — {user} ({info['plan']}): "
              f"{actual_count} articles (expected {expected_count})")

        if status == "❌ FAIL":
            print(f"    → Accessible: {accessible}\n")

if __name__ == "__main__":
    main()

