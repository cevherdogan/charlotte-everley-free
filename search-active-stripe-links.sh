# for example 
open https://buy.stripe.com/6oU4gzeS07NTc0v7xHfQI06

grep -ri stripe ./**/*.html

mkdir -p recovered_stripe_links

for ref in $(git for-each-ref --format='%(refname:short)' refs/heads/ refs/tags/); do
  echo "🔎 Checking $ref ..."
  git checkout $ref --quiet 2>/dev/null
  mkdir -p "recovered_stripe_links/$ref"
  cp *welcome*.html "recovered_stripe_links/$ref/" 2>/dev/null
  grep -H 'https://buy.stripe.com' recovered_stripe_links/$ref/*.html
done

git checkout main





