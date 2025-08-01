(function () {
  const userTier = localStorage.getItem("tier") || "free"; // Default to free if not set

  // Infer required tier from path
  const path = window.location.pathname;
  const requiredTier = path.split("/")[2]; // e.g., "gold" from "/membership/gold/page.html"

  const tiers = ["free", "silver", "gold", "premier"];
  const userIndex = tiers.indexOf(userTier);
  const requiredIndex = tiers.indexOf(requiredTier);

  if (userIndex < requiredIndex) {
    // Insufficient access
    console.log(`[RBAC] Insufficient tier (${userTier}) for ${requiredTier}, redirecting...`);
    window.location.href = "/membership/free/";
  }
})();

