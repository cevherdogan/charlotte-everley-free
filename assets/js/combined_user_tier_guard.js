// combined_user_tier_guard.js
// Merged from: tier_guard.js and check_user_tier_access.js
// Redirects unauthorized access to /unauthorized.html silently

(function () {
  const path = window.location.pathname;
  const tier = localStorage.getItem("tier") || "free";

  const tierRank = {
    free: 0,
    trial: 1,
    silver: 2,
    gold: 3
  };

  function requiredTierFromPath(path) {
    const match = path.match(/\/membership\/(free|trial|silver|gold)\//);
    return match ? match[1] : "free";
  }

  const requiredTier = requiredTierFromPath(path);

  if (tierRank[tier] < tierRank[requiredTier]) {
    console.warn(`🔒 Access denied: '${tier}' cannot view '${requiredTier}' content.`);
    window.location.href = "/membership/free/";
  }
})();

// check_user_tier_access.js

(function () {
  const tiers = ["free", "silver", "gold", "premier"];
  const userTier = localStorage.getItem("tier") || "free";

  // Match any of the tier names in the pathname (early segment)
  const match = window.location.pathname.match(/\b(free|silver|gold|premier)\b/);
  const requiredTier = match ? match[1] : "free";

  const userIndex = tiers.indexOf(userTier);
  const requiredIndex = tiers.indexOf(requiredTier);

  if (userIndex < requiredIndex) {
    console.warn(`⛔️ Access denied:
    User tier '${userTier}' [${userIndex}]
    Tried to access '${requiredTier}' [${requiredIndex}]
    → Redirecting to /membership/free/`);
    window.location.href = "/membership/free/";
  } else {
    console.log(`✅ Access granted for '${userTier}' to '${requiredTier}' content.`);
  }
})();