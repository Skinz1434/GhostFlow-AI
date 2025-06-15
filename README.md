# GhostFlow-AI

This repository hosts the monorepo for the **GhostFlow AI** project. It contains several modules organized
by functional area, such as analytics, content management, and compliance. The
structure is intentionally lightweight so each team can expand their module as
needed.

## Directory overview

```
GhostFlow-AI/
├── apps/           # application front-ends
├── bots/           # automation bots
├── functions/      # serverless functions
├── infra/          # infrastructure configuration
├── scripts/        # helper utilities
├── analytics/      # data collection and reporting scripts
├── cloaking/       # risk mitigation utilities
├── compliance/     # regulatory automation
├── content/        # CMS templates and scripts
├── financial/      # revenue tracking tools
├── security/       # authentication and security checks
├── ui/             # front‑end assets (CSS, JS, images)
└── docs/           # internal documentation
```

## Prerequisites

The following tools are used across the project. Install them globally to ensure
smooth local development:

```bash
npm i -g vercel netlify-cli @aws-amplify/cli
pip install openai==1.* pandas python-dotenv slack_sdk stripe cryptography
# Package `ahrefs` is optional and may not be available on PyPI
apt-get install -y postgresql
```

These commands install hosting CLIs, data libraries, and a local PostgreSQL
server. Run them from a privileged shell (`sudo`) if required.

## Repository setup

1. Clone the repository or run `git init` in a new directory.
2. Stage and commit the initial structure:

   ```bash
   git add .
   git commit -m "chore: initial structure"
   ```
3. Connect to your GitHub repository and push the commit:

   ```bash
   git remote add origin git@github.com:<user>/ghostflow-ai.git
   git push -u origin main
   ```
4. Create feature branches for development.
5. Use `npx cz` to compose commits following Conventional Commits.
6. Pre-commit hooks via Husky run `lint-staged` to format code.

To view the directory tree from the project root:

```bash
tree -L 2
```

Feel free to expand each module with additional code or documentation.

## Local development (Replit)

1. Open the **Secrets** panel in Replit and add the following keys:

   | Key Name | Value |
   | --- | --- |
   | `OPENAI_API_KEY` | `sk-...` |
   | `STRIPE_KEY` | `rk_test_xxx` |

   Keep these secrets out of version control.

2. Install Python dependencies:

   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. Start the FastAPI server:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

   Before launching any service, run `python scripts/check_env.py` to ensure
   required environment variables are present.

   Visiting the root path should return `{"status": "GhostFlow AI operational!"}`.

## Security and compliance

All modules must adhere to internal security guidelines. Avoid committing
sensitive credentials or production data. Use environment variables and
`.env` files that are excluded via `.gitignore` for secrets.

### Secure key management

Store API keys such as `OPENAI_API_KEY`, `STRIPE_KEY`, and `GF_ENC_KEY` in
**Replit Secrets**. Rotate them manually on a regular basis to maintain high
security standards.

### AES-256 encryption helper

The module `security/scripts/encryption_helper.py` exposes `seal()` and
`open()` helpers for encrypting and decrypting bytes. Ensure `GF_ENC_KEY` is
defined in your environment before using the helper.

## SEO & Traffic Acquisition Tools

Two bots automate keyword discovery and publishing:

1. **Keyword Miner** – Fetches top terms from Ahrefs hourly and stores them to `data/daily_keywords.csv`.
2. **Content Publisher** – Posts generated Markdown articles to your site each day.

These scripts require environment variables:

```bash
AHREFS_API_TOKEN=your_ahrefs_token
SITE_API_ENDPOINT=https://example.com/api/post
SITE_API_KEY=secret-key
```

GitHub Actions workflows in `.github/workflows/` run these bots on a schedule.

## Cloaking & Link Management

The `cloaking/` module provides a small FastAPI service that securely redirects
affiliate links while recording click metadata. Configure it with the following
environment variables:

```bash
PG_DSN=postgresql://user:pass@localhost/dbname
AFF_EXAMPLE=https://affiliate.example.com/landing
```

Run the redirector with:

```bash
uvicorn cloaking.scripts.redirector:app --host 0.0.0.0 --port 8001
```

Each affiliate link is exposed at `/out/<slug>` where `slug` matches the
`AFF_<SLUG>` variable. Only alphanumeric characters, underscores and dashes are
allowed in `slug` to prevent injection attacks.

## Analytics & KPI Monitoring

Serverless scripts in `analytics/scripts` relay events to Google Tag Manager and log KPI metrics to PostgreSQL. Set `PG_DSN` in your environment. The `lambda_handler` function forwards events after consent checks, while `ingest_kpi_event` writes metrics for Metabase dashboards.

An additional script, `kpi_alerts.py`, checks critical metrics every few minutes and posts alerts to Slack when values drop below configured thresholds. It requires `SLACK_BOT_TOKEN` in your environment.


## Hosting and deployment

The project can be deployed using common frontend hosting providers. The base configuration files are included in the repository.

### Vercel

Use Vercel for deploying the Next.js front-end contained in `apps/web`.

```bash
vercel login                   # opens a browser for authentication
vercel link --project ghostflow-web
vercel env add OPENAI_API_KEY production
vercel --prod                  # first deploy
```

The configuration file `vercel.json` defines a custom route for serverless functions located under `functions/`.

### Netlify

Netlify can host our functions and periodic jobs.

```bash
netlify init                   # follow prompts to connect the repo
netlify env:set STRIPE_KEY sk_live_xxx
netlify deploy --prod
```

The basic build settings live in `netlify.toml` and specify the `functions` directory and a sitemap plugin.

### AWS Amplify

For teams preferring AWS, initialize Amplify and enable hosting:

```bash
amplify init --yes
amplify add hosting            # choose continuous deploy
amplify push
```

These commands require authentication with AWS beforehand.

## Compliance Automation

To meet FTC and GDPR requirements, the `compliance/` module provides a Next.js middleware and a cookie consent component.

### Middleware

`compliance/scripts/middleware.ts` adds security headers and an affiliate disclosure:

```ts
import { NextResponse, type NextRequest } from 'next/server'

export function middleware(req: NextRequest) {
  const res = NextResponse.next()
  res.headers.set('Content-Security-Policy', "script-src 'self' 'unsafe-inline' *.googletagmanager.com")
  res.headers.set('X-FTC-Disclosure', 'GhostFlow AI earns commissions on qualifying purchases.')
  res.headers.set('Set-Cookie', 'Secure; HttpOnly; SameSite=Strict')
  return res
}
```

### GDPR cookie consent

The React component `compliance/scripts/GDPRCookieConsent.tsx` displays a banner to manage user consent.
Add `react-cookie-consent` to your dependencies and include the component near the root of your app.


## Financial Automation

The `financial/` module automates payouts from Stripe. The script
`financial/scripts/stripe_payout.js` transfers available funds to your
primary account when the balance exceeds $1,000.

Set the following environment variables in your hosting provider or `.env`
file:

```bash
STRIPE_KEY=<your-stripe-secret>
MAIN_PAYOUT_ACC=<destination-account-id>
```

Run the payout script manually with `node financial/scripts/stripe_payout.js` or
schedule it using Netlify Functions or another cron service.

## Brand Styling

The `ui` module now includes a lightweight theme for SkinZAI and QBit branding.
Import `ui/css/theme.css` in your app to apply the dark background, gradient
buttons, and typography defaults.

A reusable React component `ui/js/GlowCard.tsx` provides a glowing card effect
for highlighting content. Use it in Next.js pages as:

```tsx
import GlowCard from '../../ui/js/GlowCard'

export default function Example() {
  return (
    <GlowCard title="Welcome">
      <p>This card uses the SkinZAI gradient glow.</p>
    </GlowCard>
  )
}
```

These assets keep the UI consistent across modules. Customize colors by editing
`theme.css`.


## Database setup

Initialize the PostgreSQL schema using the provided SQL file:

```bash
psql -f ./infra/schema.sql
```

This creates tables for click tracking, KPI metrics, and the financial ledger.

## Load testing

Run a simple load test against the redirector to ensure it stays under 100ms at the 95th percentile:

```bash
k6 run tests/perf.js --vus 500 --duration 30s
```

Adjust the target URL in `tests/perf.js` if needed.
