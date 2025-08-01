// check_user_tier_access.js

(function () {
  const tiers = ["free", "silver", "gold", "premier"];

  // 🧠 Step 1: Get user tier from localStorage
  const userTier = localStorage.getItem("tier") || "free";

  // 🔍 Step 2: Infer required tier from current URL path
  const match = window.location.pathname.match(/^\/membership\/(free|silver|gold|premier)\b/);
  const requiredTier = match ? match[1] : "free";

  const userIndex = tiers.indexOf(userTier);
  const requiredIndex = tiers.indexOf(requiredTier);

  // ✅ Step 3: Enforce access control
  if (userIndex < requiredIndex) {
    console.warn(`⛔️ Tier Access Violation:
  User tier '${userTier}' [${userIndex}] tried to access '${requiredTier}' [${requiredIndex}]
  → Redirecting to /membership/free/`);
    window.location.href = "/membership/free/";
  } else {
    console.log(`✅ Access granted for '${userTier}' to '${requiredTier}' content.`);
  }
})();


