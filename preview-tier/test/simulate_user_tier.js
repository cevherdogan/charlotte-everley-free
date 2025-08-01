// assets/js/simulate_user_tier.js
function setTier(tier) {
  localStorage.setItem('user_tier', tier);
  console.log(`User tier set to: ${tier}`);
  location.reload();
}

function getTier() {
  return localStorage.getItem('user_tier') || 'free';
}

function clearTier() {
  localStorage.removeItem('user_tier');
  console.log('User tier cleared.');
  location.reload();
}


