# 340 Collective website alignment

**Pack version:** 0.2.0

**Sources reviewed:** 2026-10-15

**Status:** Public statements inform policy design; technical implementation, role acceptance and policy approval remain unverified.

## Sources and resulting policy decisions

| Source | What it establishes | How the pack uses it |
| --- | --- | --- |
| [About](https://340collective.com/about) | Las Vegas real-estate media studio; human-led production; David C. as CEO & Founder; Faris N. as Strategy & Operations Lead | Scope policies to production and client information. Propose leadership responsibilities without asserting acceptance. |
| [Home and contact form](https://340collective.com/) | Planning, capture, editing and digital delivery; form fields include contact details, social handles and brand/project goals | Define project-based access, secure capture/transfer, appropriate contact handling and delivery checks. |
| [FAQ: content and working practices](https://340collective.com/faq) | Studio/directly managed crew; limited AI support; permission and minor-consent requirements; raw files generally kept around 60 days after delivery | Preserve human production, control media permissions and propose an exact 60-day operational raw-media default. |
| [FAQ: privacy and security](https://340collective.com/faq) | Public access-log limit of 90 days; Cloudflare analytics; published security controls and help@340collective.com reporting route | Replace the earlier 12-month log proposal, identify controls to verify and distinguish intake from staffed incident coverage. |
| [FAQ: customer accounts and newsletter](https://340collective.com/faq) | Client social access depends on the contracted service; newsletter participation is separate and optional | Require scoped delegated access; separate project communication from subscription and suppression records. |
| [Pricing](https://340collective.com/pricing) | Additional social, advertising and website offerings; Stripe is named; page markup also contains an unconnected-checkout notice | Scope access to purchased services. Treat payment activation as unverified and require configuration evidence. |
| [FAQ: governing law](https://340collective.com/faq) | Terms refer to Nevada and Clark County | Remove the UK-specific accounting rationale; identify relevant U.S./Nevada assessment without inferring incorporation or tax status. |
| [IRS recordkeeping guidance](https://www.irs.gov/businesses/small-businesses-self-employed/how-long-should-i-keep-records) | Retention depends on record type and circumstances | Label the seven-year accounting baseline as a proposed internal choice requiring accountant review. |

Publicly described security features are requirements to verify, not controls certified by this lab. Public professional experience in an individual's biography does not establish 340 Collective's client geography, regulatory scope or technical estate. The site references security-framework alignment without claiming third-party certification; this pack makes no certification claim.

## Conflicts and decisions still open

| Item | Evidence and implication | Required resolution |
| --- | --- | --- |
| Monthly renewals | The About-page helper text describes monthly auto-renewal; Pricing and the FAQ describe a single-month payment without renewal. | Studio Lead confirms one authoritative billing rule and aligns customer-facing copy and checkout. Until then, use the specific approved client terms; do not infer recurring consent. |
| Routine response times | The home-page summary gives a 12-hour-to-10-day range; About/FAQ messaging text gives 5–7 business days. | Operations Lead confirms the applicable client promise and resolves copy inconsistencies. Neither is an incident response target. |
| Checkout activation | Stripe is named, but an unconnected-checkout notice is present in page content. No transaction or runtime activation was tested. | Confirm the live payment route and permissions before marking the integration active or assessed. |
| Raw-media disposal | FAQ wording is approximate; storage behaviour and per-client agreements are not supplied. | Confirm the proposed exact 60-day default, exceptions, deletion process and customer communication. |
| Access logs | The 90-day public maximum is known; log inventories, content and expiry settings are not. | Inventory ordinary access logs and verify expiry across primary, archive and backup copies. |
| Roles and collaborators | Public leadership names are known; policy acceptance, deputies, administrator and complete lab roster are not. | Obtain real acceptance and the actual collaborator roster. Do not request or infer acknowledgments from a public profile. |
| Legal/accounting scope | Nevada business context is published; legal form, tax treatment, other jurisdictions and client-specific obligations are not. | Confirm before approving accounting retention and notification decisions. |
| Technology and evidence | AWS/IAM Identity Center comes from the lab brief. Cloudflare, Google Meet and Stripe are named publicly. Exact accounts/configuration and vendor approvals are not supplied. | Record verified inventories, permissions and evidence separately from these policy drafts. |

The website was read without submitting forms, payments or messages. No live configuration or website content was changed. These notes support the policy revision; they do not constitute a full website, contractual or compliance review.
