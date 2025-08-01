(function() {
  const tier = localStorage.getItem("userTier") || "free";
  const current = window.location.pathname;

  const target = `/membership/${tier}/index.html`;

  if (!current.includes("/membership/") && current !== target) {
    console.log(`[Tier Redirect] Detected tier: ${tier}. Redirecting to ${target}`);
    window.location.replace(target);
  }
})();


