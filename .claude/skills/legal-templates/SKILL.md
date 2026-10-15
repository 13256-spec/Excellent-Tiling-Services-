---
name: legal-templates
description: Attorney-drafted legal document templates (NDA mutual and one-way, master services agreement, terms of use, privacy policy, cookie notice, data processing addendum, advisor agreement, employee offer letter, HIPAA BAA) to use as a starting point when drafting or reviewing a contract or website legal page. Use when the user mentions an NDA, confidentiality agreement, contract with a supplier or subcontractor, terms of use/service, privacy policy, cookie notice/banner, DPA, advisor agreement, or offer letter. The templates are written for US law and must be adapted for Australia.
---

# Legal templates

Twelve templates from General Legal (github.com/General-Legal/legal-templates, commit 6d68054, CC0 1.0, see
`LICENSE`). Each folder in `templates/` has a `README.md` (what it's for, key provisions) and `template.md`
(the full text). Fields to fill in are wrapped in `<mark>` tags.

## Read this first: these are US documents

Excellent Tiling Services Pty Ltd is an Australian company (ABN 63 150 082 054, Maddington WA). The templates
assume US law: Delaware governing law, US state privacy laws (CCPA/CPRA), California employment law, HIPAA.
Before using any of them:

- Change governing law and courts to **Western Australia** and the parties to the real Australian entities.
- Privacy: the law that applies is the **Privacy Act 1988 (Cth)** and the Australian Privacy Principles. Use the
  US/GDPR privacy templates only for structure. GDPR matters only for customers in the EU/UK.
- Consumer sales: the **Australian Consumer Law** guarantees can't be excluded. Delete or rewrite US-style
  "AS IS" / warranty-disclaimer and liability-cap wording for consumers, and never contradict the store's
  refund policy (`store-content/policies/refund-policy.html`).
- Employment: don't use the California offer letter. Australian hires fall under the Fair Work Act and the
  relevant modern award (e.g. Building and Construction General On-site Award for tilers).
- Remove the US-only parts rather than leaving them in.
- These are drafts. Say plainly that the owner should have a lawyer check anything he signs or publishes.

## Which template for which job

| Template | Folder | Use for ETS | Fit |
|---|---|---|---|
| Mutual NDA | `mutual-nda` | Talks with a supplier, partner or buyer where both sides share prices or plans | Good after adapting |
| One-way NDA | `one-way-nda` | Showing supplier costs, price lists or customer data to a contractor or designer | Good after adapting |
| Master Services Agreement | `master-services-agreement` | Structure for a subcontractor or builder agreement (it's written for software services, so rewrite the scope) | Partial |
| Terms of Use | `terms-of-use` | Checking the website terms against `store-content/policies/terms-of-service.html` | Partial |
| Privacy Policy (U.S.) | `privacy-policy-us` | Structure ideas only; compare with `store-content/policies/privacy-policy.html` | Low |
| Privacy Policy (GDPR) | `privacy-policy-gdpr` | Only if selling to the UK/EU (the store ships to the UK) | Low |
| Cookie Notice | `cookie-notice` | Website cookie/tracking notice (Shopify, Meta pixel, Google) | Good after adapting |
| DPA (U.S.) / DPA (Global) | `dpa-us`, `dpa-global` | Rarely: only if a business customer asks ETS to process their personal data | Low |
| Advisor Agreement | `advisor-agreement` | Only if someone is given shares to advise the company | Low |
| Employee Offer Letter (California) | `employee-offer-letter` | Don't use; see above | Not applicable |
| Business Associate Agreement (HIPAA) | `business-associate-agreement` | Not relevant (US health data) | Not applicable |

## How to work

1. Read the template's `README.md`, then `template.md`.
2. Ask for (or look up in the repo) the facts the `<mark>` fields need: parties, ABN, address, dates, scope.
3. Draft the adapted document in plain English where possible, with every US-specific clause changed or removed.
4. List what you changed from the template and anything a lawyer should look at.
5. Website policies live in `store-content/policies/`. The owner pastes them into Shopify admin → Settings → Policies.
   Don't publish anything yourself.
