harika—let’s kick this off. I’ll speak English; you can answer in Turkish. Below is a concrete, “do-now” plan to: (1) decouple Stripe-backed membership tiers on the **landing page**, and (2) migrate from **GitHub Pages → AWS S3 + CloudFront** with authentication + personalization.

# Goal & Architecture (at a glance)

* **Stripe** is the source of truth for tiers (`free`, `trial`, `silver`, `gold`).
* **Auth**: Amazon **Cognito** (Hosted UI, OIDC) or Auth0 (pick one). I’ll default to Cognito for a smooth AWS path.
* **Static hosting**: **S3 (private)** + **CloudFront** (OAC, HTTPS).
* **Personalization & gating**:

  * Client reads the user’s **tier** from an ID token claim (Cognito custom attribute) or via a signed API call.
  * **Landing page** renders tier-specific sections (cards/CTAs) dynamically.
* **Stripe → Cognito bridge**: Stripe **Webhook** → API Gateway → Lambda updates the user’s tier in Cognito (custom attribute `custom:tier`).

---

# Step 1 — Branching & minimal repo setup

Create a working branch:

```bash
git checkout -b infra/s3-cloudfront-auth
```

Add a simple config file for tier rendering:

```yaml
# config/tier_sections.yaml
tiers:
  free:
    show_sections: [ "hero", "features_basic", "cta_signup" ]
  trial:
    show_sections: [ "hero", "features_basic", "features_trial", "cta_upgrade" ]
  silver:
    show_sections: [ "hero", "features_basic", "features_silver", "gallery_quickstart", "cta_upgrade_gold" ]
  gold:
    show_sections: [ "hero", "features_basic", "features_silver", "features_gold", "gallery_quickstart", "priority_support" ]
```

---

# Step 2 — Landing page tier gating (client)

Minimal, framework-agnostic snippet (vanilla JS) that:

* reads `tier` from Cognito ID token (JWT claim `custom:tier`)
* falls back to `free` if not signed in
* shows/hides sections by `data-section` attributes

```html
<!-- index.html -->
<section data-section="hero"> ... </section>
<section data-section="features_basic"> ... </section>
<section data-section="features_trial" hidden> ... </section>
<section data-section="features_silver" hidden> ... </section>
<section data-section="features_gold" hidden> ... </section>
<section data-section="gallery_quickstart" hidden> ... </section>
<section data-section="priority_support" hidden> ... </section>
<section data-section="cta_signup" hidden> ... </section>
<section data-section="cta_upgrade" hidden> ... </section>
<section data-section="cta_upgrade_gold" hidden> ... </section>

<script type="module">
import config from './config/tier_sections.json' assert { type: 'json' };

function getIdToken() {
  // If using Cognito Hosted UI + Amplify, replace with Auth.currentSession()
  const raw = localStorage.getItem('id_token'); // placeholder
  return raw;
}

function decodeJwt(token) {
  try { return JSON.parse(atob(token.split('.')[1])); } catch { return null; }
}

function currentTierFromToken() {
  const token = getIdToken();
  if (!token) return 'free';
  const payload = decodeJwt(token);
  return payload?.['custom:tier'] || 'free';
}

function applyTierSections(tier) {
  const visible = new Set(config.tiers[tier]?.show_sections || config.tiers['free'].show_sections);
  document.querySelectorAll('[data-section]').forEach(el => {
    const sec = el.getAttribute('data-section');
    el.hidden = !visible.has(sec);
  });
}

const tier = currentTierFromToken();
applyTierSections(tier);
</script>
```

> If you’re using React, I can swap this for a `TierGate` component, but this vanilla approach works anywhere.

---

# Step 3 — Stripe product → tier mapping

In Stripe, set **Price** metadata: `tier=free|trial|silver|gold`.
Then, add a webhook handler to **sync tier → Cognito**.

**Stripe → API → Lambda (Node.js)**

```js
// lambda/stripeWebhook.js
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const AWS = require('aws-sdk');
const cognito = new AWS.CognitoIdentityServiceProvider();

exports.handler = async (event) => {
  const sig = event.headers['Stripe-Signature'];
  const body = event.body;
  let evt;

  try {
    evt = stripe.webhooks.constructEvent(body, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    return { statusCode: 400, body: `Webhook Error: ${err.message}` };
  }

  if (evt.type === 'checkout.session.completed' || evt.type === 'customer.subscription.updated') {
    const session = evt.data.object;
    const customerId = session.customer;
    // 1) Find active subscription and attached price
    const subs = session.subscription
      ? await stripe.subscriptions.retrieve(session.subscription)
      : (await stripe.subscriptions.list({ customer: customerId, status: 'active', limit: 1 })).data[0];

    const priceId = subs?.items?.data?.[0]?.price?.id;
    const price = await stripe.prices.retrieve(priceId, { expand: ['product'] });

    const tier = price.metadata?.tier || 'free';
    // 2) Resolve user’s Cognito sub (store Stripe customer_id -> cognito_sub mapping in your DB)
    const { cognitoSub, userPoolId } = await lookupMapping(customerId); // implement

    // 3) Update Cognito custom attribute
    await cognito.adminUpdateUserAttributes({
      UserPoolId: userPoolId,
      Username: cognitoSub,
      UserAttributes: [{ Name: 'custom:tier', Value: tier }]
    }).promise();
  }

  return { statusCode: 200, body: 'ok' };
};
```

> Mapping strategy: when a user signs in via Cognito and initiates checkout, store `{ cognito_sub, stripe_customer_id }` in DynamoDB. Webhook uses this to update `custom:tier`.

---

# Step 4 — Migrate hosting: GitHub Pages → S3 + CloudFront (secure)

**Option A: Fast manual (no IaC)**

1. Create S3 bucket (private), enable **OAC** from CloudFront.
2. Create CloudFront distro:

   * Origin: S3 bucket (OAC attached)
   * Default root object: `index.html`
   * Add error responses (SPA): 403/404 → `/index.html` (200)
3. Upload build:

   ```bash
   aws s3 sync dist/ s3://YOUR_BUCKET --delete
   aws cloudfront create-invalidation --distribution-id DIST_ID --paths "/*"
   ```

**Option B: Minimal Terraform (recommended)**

```hcl
# infra/main.tf
provider "aws" { region = "us-east-1" }

resource "aws_s3_bucket" "site" {
  bucket = var.bucket_name
}

resource "aws_cloudfront_origin_access_control" "oac" {
  name                              = "${var.bucket_name}-oac"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "cdn" {
  enabled = true
  default_root_object = "index.html"

  origin {
    domain_name = aws_s3_bucket.site.bucket_regional_domain_name
    origin_id   = "s3-origin"
    origin_access_control_id = aws_cloudfront_origin_access_control.oac.id
  }

  default_cache_behavior {
    target_origin_id = "s3-origin"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods = ["GET","HEAD","OPTIONS"]
    cached_methods  = ["GET","HEAD"]
  }

  restrictions { geo_restriction { restriction_type = "none" } }
  viewer_certificate { cloudfront_default_certificate = true }

  custom_error_response {
    error_code = 404
    response_code = 200
    response_page_path = "/index.html"
  }
  custom_error_response {
    error_code = 403
    response_code = 200
    response_page_path = "/index.html"
  }
}
```

---

# Step 5 — GitHub Actions: CI/CD to S3 + CloudFront

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to S3 + CloudFront
on:
  push:
    branches: [ "main" ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npm run build
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_DEPLOY_ROLE_ARN }}
          aws-region: us-east-1
      - name: Sync to S3
        run: aws s3 sync dist/ s3://$S3_BUCKET --delete
        env:
          S3_BUCKET: ${{ secrets.S3_BUCKET }}
      - name: Invalidate CloudFront
        run: aws cloudfront create-invalidation --distribution-id $DIST --paths "/*"
        env:
          DIST: ${{ secrets.CF_DISTRIBUTION_ID }}
```

> Set these **repo secrets**: `AWS_DEPLOY_ROLE_ARN`, `S3_BUCKET`, `CF_DISTRIBUTION_ID`.

---

# Step 6 — Cognito (auth) wiring

* **User Pool**: add custom attribute `custom:tier` (String).
* **App Client**: use Hosted UI (Google/Apple optional).
* **Callback URL**: your CloudFront domain.
* After login, store `id_token` (or use Amplify) and read `custom:tier` to drive the landing page.

If you prefer **Auth0**, identical flow: set `app_metadata.tier` and read that claim (`https://yourdomain/tier`) in the ID token.

---

# Step 7 — Protecting premium assets (optional hardening)

For truly private pages/files (e.g., `/silver/…`, `/gold/…`):

* Store premium bundles in a **separate S3 bucket** behind CloudFront.
* Serve via **Signed Cookies** or **Signed URLs** issued by a small auth edge function after the user is verified (Cognito JWT).
* For most marketing content, client-side gating is enough; for real content/IP, add signed delivery.

---

# Step 8 — Stripe Customer Portal links (CTAs)

On the landing page:

* If unauthenticated → “Start Free / Sign in”
* If `free`/`trial` → “Upgrade (Stripe checkout)”
* If `silver`/`gold` → “Manage Subscription (Stripe Customer Portal)”

Wire the buttons to your checkout/portal endpoints; after successful payment, webhook updates `custom:tier`.

---

# Step 9 — PR checklist (drop into GitHub)

* [ ] S3 + CloudFront deployed with OAC, SPA 403/404 → `index.html`.
* [ ] Cognito Hosted UI working; `custom:tier` present in ID token.
* [ ] Stripe products/prices carry `metadata.tier`.
* [ ] Webhook path updates Cognito `custom:tier` on new/updated subscriptions.
* [ ] Landing page sections gated per `config/tier_sections.*`.
* [ ] CTAs route to correct Stripe checkout/portal.
* [ ] (Optional) Premium assets behind Signed Cookies/URLs.
* [ ] GitHub Actions deploys on `main` push.

---

## Next move (fastest)

* Sen “Cognito mu Auth0 mu?” seçimini Türkçe yaz; ben hemen seçtiğine göre dosyaları ve kod bloklarını repo-friendly hale getirip PR taslağı ve klasör yapısı vereyim.
* Ayrıca, mevcut repo’da hangi build komutu var? (`npm run build`/`vite build`/`next build`?) Bana söyle, workflow’u ona göre netleştireyim.


