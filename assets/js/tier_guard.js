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


