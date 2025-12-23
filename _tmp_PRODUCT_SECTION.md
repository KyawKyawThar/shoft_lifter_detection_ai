---

## PRODUCTIZED OFFERINGS & SUBSCRIPTION PLANS

This project is offered as a software-only, subscription product tailored to three primary personas:

- **Home / DIY users** — simple plug-and-play installs, mobile notifications, minimal configuration.
- **Store owners (SMB)** — multi-camera orchestration, web dashboard, alert history, multi-user roles.
- **Installers / Integrators** — provisioning tools, reseller accounts, bulk onboarding, optional managed services.

Subscription model (example tiers):

- **Personal** — $9/month
  - Up to 2 cameras, mobile alerts, local-only processing, basic cloud sync (optional).

- **Standard** — $29/month
  - Up to 6 cameras, web dashboard, alert history (7 days), basic analytics, email support.

- **Business** — $99/month
  - Up to 20 cameras, multi-user roles, 30-day alert retention, priority support, cloud backups (optional).

- **Enterprise** — Custom pricing
  - 20+ cameras, SLA, dedicated onboarding, multi-site management, custom integrations.

Key product decisions:

- **Software-only**: Customers supply cameras/NVRs and on-site hardware; you provide the software, cloud services, and support.
- **Edge-first, hybrid-cloud**: Run inference locally (edge) for low-latency alerts; sync alerts and metadata to cloud for analytics, multi-site views and backups.
- **Installer onboarding**: Provide a provisioning API and QR-code image to bind devices to customer accounts. Offer installer docs and a reseller portal.

Sales & go-to-market:

- Provide a concise one-pager (`SUBSCRIPTION_PLANS.md`) for website and installers (created alongside this doc).
- Offer 14–30 day free trials for new customers; auto-upgrade to paid when trial ends.
- Provide reseller discounts and volume pricing for installers.

Operational notes:

- Implement device authentication (mutual TLS or token-based) and encrypted transport for all edge→cloud traffic.
- Build health/heartbeat telemetry and an admin dashboard to monitor active subscriptions and device health.

See `SUBSCRIPTION_PLANS.md` for the full one-pager and billing examples.
