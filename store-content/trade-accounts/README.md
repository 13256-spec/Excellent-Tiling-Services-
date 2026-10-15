# Trade accounts – how it works in Shopify (11 Oct 2026)

Approved trade customers see their trade price on every product (retail price crossed out) and the
same discount comes off in the cart and at checkout. Nothing changes for retail shoppers.

## The pieces

| Piece | Where | What it does |
|---|---|---|
| Application form | `/pages/trade-account` (Shopify Forms block, form 1172088, in `sections/ets-trade-apply.liquid`) | Saves the applicant as a customer with their business details in the `custom.trade_*` customer metafields. **Don't change the form.** |
| Approval | Customers → the person → **Tags** → add `trade` → Save | The tag is the switch. Everything below keys off it. |
| Segment "Trade customers" | Customers → Segments | `customer_tags CONTAINS 'trade'`. The five automatic discounts are limited to this segment. |
| Segment "Trade applicants (waiting for approval)" | Customers → Segments | Applicants tagged `trade-applicant` who don't have `trade` yet. Check it when an application email arrives. |
| Trade band per product | Product → Metafields → **Trade discount band (%)** (`ets.trade_band`: 0, 5, 10, 15, 20 or 25) | What the website shows a logged-in trade customer. |
| Collections `trade-list-5` … `trade-list-25` | Products → Collections (unpublished, manual) | Which products each "Trade price – N%" automatic discount applies to. A product is in exactly one. |
| Automatic discounts "Trade price – 5/10/15/20/25%" | Discounts | Take the percentage off in the cart for the Trade customers segment. They don't combine with codes. |
| Theme | `snippets/ets-trade-rate.liquid` reads `ets.trade_band`; `snippets/price.liquid` shows "Trade $X" with "Retail $Y" struck through; `snippets/ets-trade-bar.liquid` adds a green "Trade account · Logged in as <name>" bar under the header on every page | Product pages, collection grids, search, recommendations, and the sitewide bar. |

The metafield and the collection must agree. The pricing scripts set both from the master price list; if you
change one by hand, change the other.

## Approving an application (about one minute)

1. The application arrives by email and the person appears in Customers (look in the segment
   **Trade applicants (waiting for approval)**, or search by email).
2. Check the ABN at abr.business.gov.au and anything else you want to check.
3. Open the customer, click **Tags**, add `trade`, Save.
4. Email them: "Your trade account is approved. Log in at excellenttilingservice.com.au/account with this
   email address and you'll see your trade prices." If they have never set a password, the login page
   sends them a one-time code; no invite is needed with the new customer accounts.

To take trade pricing away, remove the `trade` tag.

## Changing one product's trade discount

1. Product → Metafields → **Trade discount band (%)** → set 5, 10, 15, 20 or 25 (0 = no trade discount).
2. Products → Collections → remove it from its old `trade-list-N` and add it to the new one.
3. Keep every variant above the trade floor (cost × 1.1 × 1.15); `store-content/pricing/PRICING-PLAYBOOK.md`.

## Theme status

**Live since 11 Oct 2026.** The theme "ETS 2026 – Trade prices on site (draft 11 Oct)"
(gid://shopify/OnlineStoreTheme/143975940159) was published by the owner that day. It carries the five files in
this repo under `theme/snippets/ets-trade-rate.liquid`, `ets-pdp-trade.liquid`, `ets-trade-rates.liquid`,
`theme/sections/ets-trade-apply.liquid` and `ets-trade-band.liquid`, plus the ETS-modified `snippets/price.liquid`.
A logged-in trade customer now sees the same price on the page that comes off in the cart.
