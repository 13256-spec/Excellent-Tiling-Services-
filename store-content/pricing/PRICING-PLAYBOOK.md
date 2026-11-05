# ETS pricing playbook (rules book)

How Excellent Tiling Services prices every product, where the data lives in Shopify and in this repo, and how to
change prices safely. Written for the owner and for every Claude Code session (`CLAUDE.md` points here; the
`ets-pricing` agent follows it). **Version 2, 5 Nov 2026**: margin policy rewritten after the move to native B2B.
The dated history of what was done and why is in `README.md` next to this file.

## 1. Goals, in order

1. **Profit first.** Every price, public or trade, must clear its floor. If a competitor is below our floor, we do not follow.
2. **Public price**: at or a little under the competitor that sells the same item. MELA is the exception: equal to
   Bathroom City's price, never under (supplier condition, owner 20 Oct 2026).
3. **Trade price**: a real but affordable discount for approved trade accounts, charged through Shopify B2B.
4. **Simple to run**: one cost basis, one set of formulas, scripts for the bulk work, the owner approves every change.

## 2. The numbers (all prices inc GST)

Margin is always **(price - cost) / price with both inc GST**, which equals the margin ex GST. Markup is cost / (1 - margin).

| Rule | Formula | Example (cost $100 inc GST) |
|---|---|---|
| **Cost** | supplier price inc GST. Ex-GST sheets x 1.1 | $90.91 ex -> $100.00 |
| **Public floor** (minimum) | cost / 0.75 (25% margin) | $133.35 |
| **Public target** (new or uncontested items) | cost / 0.65 (35% margin) | $153.85 |
| **Public floor, price-matched lines** (MELA, items B&B Hardware also sells) | cost / 0.80 (20% margin) | $125.00 |
| **Trade floor, hardware and tiles** | trade price >= cost / 0.75 (25% margin) | $133.35 |
| **Trade floor, MELA and price-matched lines** | trade price >= cost / 0.80 (20% margin) | $125.00 |
| **Trade band cap** | hardware 20%, tiles 15%, MELA 15% | - |
| **Rounding** | public: down to the next 5c (tiles: 10c); trade: to the cent, half up | $133.35 -> $133.30 |

- **Tiles (not mosaics) are sold in 0.01 m² units** (tag `m2-units`, since 5 Nov 2026): price per m² in whole dollars,
  Shopify price = that / 100, trade price per unit rounded **up**. See README "Tiles sold by exact m²".
- **Trade band** is per product, the deepest of 20 / 15 / 10 / 5% (within the cap) that keeps **every** variant above the
  trade floor. If none does, the product has no trade discount. A product with any variant lacking a cost gets no band.
- Public margin under 25% (price-matched lines under 20%) is a flag: raise the price to the floor at the next review,
  unless it is a deliberate match the owner has approved.
- Why these numbers: 25% at trade covers card fees (about 2%), freight on bulky items we absorb, returns and the time
  spent on trade quotes, and still leaves a profit. 20% was the floor until 5 Nov 2026; the owner found it too thin
  (median trade margin was 24%, a fifth of items sat right on 20%).

### Competitor rules

| Line | Rule |
|---|---|
| MELA (Bathroom City supplies us) | public price = Bathroom City's current price, never lower. If their clearance is under our floor, we stay at the floor. |
| Hardware that B&B Hardware (Maddington) also sells | 5% under B&B, rounded down to 5c, never under the floor. ~50 items, matched in `BB_MATCH` in `reprice_2026_10.py`. |
| Roberts Designs lines | 10% under Roberts' own retail unless a closer competitor is on file (`roberts-designs-pricing.csv`). |
| Eternity tiles | 15% under Eternity RRP, rounded down to 10c (Eternity and WA stockists sell at RRP). |
| Everything else (BAT, Raimondi, RLA, house brand) | the public target (35%) unless a competitor is on file, then 5% under it. |
| Competitor clearance below our cost | reported, never matched. |

## 3. Suppliers and cost basis

**Rule: every unit cost in Shopify is inc GST.** The MELA, Eternity tile and DSA costs that were stored ex GST were
converted (x 1.1) on 5 Nov 2026, so no basis juggling is needed any more: margin = (price - cost) / price, straight from
Shopify. The 21 Oct 2026 Roberts batch (Baron, Sigma spares) was confirmed inc GST by the owner the same day.

| Range | Supplier | Cost source | Stored |
|---|---|---|---|
| Tiles (Eternity) | Eternity Tiles | `eternity-price-list-2026-10-05.txt`, "non pallet" price x 1.1 | inc GST |
| MELA bathroomware | Bathroom City | Bathroom City list x (1 - SILVER discount) (estimate until invoices confirm) | inc GST |
| Roberts Designs, Maxisil, Sigma, Siri, Barwalt, Baron | Roberts Designs | trade-account price x 1.1 | inc GST |
| BAT, BAT Trims, Raimondi, Panther, NICLIS, Washboy, Atika, ADA | B.A.T. Trims Pty Ltd | price books (Tools Book 1 May 2026, Raimondi May 2026, Trims Book 1 Aug 2026, Project Trims May 2026), NET x 1.1 | inc GST |
| Sika, house-brand items | owner's invoice | invoice price inc GST | inc GST |
| DSA bathroomware, Malaga packages | Eternity/DSA | RRP less 45% account discount, x 1.1 (estimate) | inc GST |
| RLA and Gripset | RLA Polymers | **no cost yet**; no trade band until one exists | - |

SILVER trade discounts (owner's sheet `2026_NEW_SILVER_TRADE_PRICE.pdf`), off Bathroom City's GST-inclusive list: vanity
package & handles 25%, basins 30%, tapware 40%, accessories 35%, mirrors & PORTER cabinets 25%, inset baths 20%,
freestanding baths 40%, shower screens 40%, toilets 40%, bidet seat 20%, sinks 40%, pop-up wastes 40%, heated towel rails
30%, floor waste/channel 40%, kitchen/laundry cabinets 20%. Back-to-wall and corner baths are not on the sheet: 20% assumed.

Delivery: the supplier's delivery charge is not added to costs; bulky-item delivery is charged to the customer at
checkout (owner, 3 Oct 2026). When the same part is sold by two suppliers, the cheaper one is the recorded supplier
(`ets.supplier`) and its code is the SKU; the other code goes in the description.

## 4. Where things live

**Shopify**
- Price and unit cost: on each variant. Supplier: product metafield `ets.supplier`.
- Trade pricing: Shopify B2B. Market **Trade accounts (B2B)** (all company locations) -> catalog **Trade price list** ->
  price list **Trade prices** with a fixed price per variant (= public price x (1 - band/100)) and the public price as
  compare-at. Band-0 products have no fixed price. A trade customer is a **company** with a location and a contact.
- Band record: product metafield `ets.trade_band` (0/5/10/15/20) and the manual collection `trade-list-N` the product sits in
  (one only). The theme and the scripts read the metafield; the collections are the owner's view in admin.
- Read-only records: variant `custom.trade_price` and product `ets.trade_price` ("$x (N% off)"), for looking up in admin.
- Grow plan: up to 3 active B2B catalogs, attached to markets, not to single companies. Deposits need Plus.
- Nothing else sets trade prices: no automatic discounts, no customer tags, no discount codes.

**Repo** (`store-content/pricing/`)

| File | What it is |
|---|---|
| `store-pricing-2026-10-03.csv` | **Master price list**: every variant with price, cost, cost source, margins, band, trade price, competitor. Update whenever prices change. |
| `reprice_2026_10.py` | Builds the master list from a Shopify export + competitor feeds. Holds `BB_MATCH`. |
| `monitor_competitors.py` | Weekly competitor check (public feeds only, changes nothing) -> `reports/price-check-YYYY-MM-DD.md`. |
| `trade_price_metafields_2026_11.py` | Rewrites `custom.trade_price` / `ets.trade_price` from the live price x band. |
| `b2b_price_list_2026_11.py` | Rewrites the B2B price list fixed prices (what trade accounts pay). |
| `price_list_pdf.py` | PDFs in `price-lists/`: retail, trade, and the **owner-only** cost list (never send to customers). |
| `reports/` | Dated audits and proposals. Latest trade check: `trade-price-check-2026-11-05.*`; band proposal under these rules: `trade-band-proposal-2026-11-05.*`. |
| `eternity_*.py`, `bat_*.py`, `audit_roberts_*.py`, `mela-pricing-*.csv` | Supplier-specific loaders and matches. |

## 5. Changing prices safely (the procedure)

1. **Read first**: this file, the master list, the latest report.
2. **Propose**: a table per item (old price, new price, competitor, cost inc GST, public margin, band, trade price, trade
   margin). **Get the owner's explicit "yes" before any write.** Proposals are free; writes need approval.
3. **Apply, in this order**, each step verified before the next:
   1. Variant prices and costs: `productVariantsBulkUpdate`, several products per request with aliases, under 16,384
      characters per request (`bulkOperationRunMutation` is blocked).
   2. Band: set `ets.trade_band` and move the product between `trade-list-N` collections.
   3. Trade prices: rerun `b2b_price_list_2026_11.py` (fixed prices + compare-at). Products whose band dropped to 0:
      `priceListFixedPricesDelete` for their variants.
   4. Records: rerun `trade_price_metafields_2026_11.py`.
   5. Verify with `contextualPricing` for a company location on a few changed variants.
4. **Record**: update the master list, rerun `price_list_pdf.py`, add a dated entry to `README.md`, commit and push.
5. **Tell the owner** in plain words: what changed, how many items, the biggest moves, anything left for their decision.

Shopify quirks: when changing a product's SEO title, always send the meta description too, or it is wiped. Metafield
and price list writes take 25 / 100 items per call. Queries return at most 100 items per page.

## 6. Trade accounts (B2B)

- **Approve an applicant** (customer tagged `trade-applicant` from the website form): Customers -> Companies -> Add company:
  business name, ABN as tax ID, the applicant's existing email as the contact (assign as Location admin and main contact),
  one location with their address. Payment terms: **none** (card at checkout) for every new account. Net 7/15/30 only after a
  credit application and a few paid orders, and turn on "submit orders as drafts" for any account with credit. Then remove
  the `trade-applicant` tag. The location joins the Trade market automatically.
- Pickup-only accounts: set the location's shipping address to the showroom and untick "editable shipping address".
- The customer logs in with their email and a one-time code; no invitation needed. The storefront then shows the trade price
  with retail crossed out, a "Trade" chip and a corner pill, and hides every "apply for trade" link.

## 7. Cadence

| When | What |
|---|---|
| Weekly | `monitor_competitors.py`; report breaches (MELA under Bathroom City, B&B now cheaper, items under floor). |
| Monthly | Trade margin check (the `trade-price-check` script logic): every banded variant against the floors and caps. |
| New supplier price list | Load costs (inc GST), recompute floors, propose price and band changes, apply after approval. |
| New product | Cost inc GST, public price by section 2, band by section 2, both metafields, collection, price list row, master list row. |
| Any price or band change | Steps 3.3 and 3.4 above, always. Stale trade prices are the main failure mode. |

## 8. Decisions log (owner)

- 3 Oct 2026: store-wide pricing applied; trade via tag + discounts (superseded).
- 14 Oct 2026: trade floor 20% (superseded 5 Nov).
- 20 Oct 2026: MELA equal to Bathroom City, never under.
- 23 Oct 2026: Roberts repricing "make money but a tiny bit cheaper than the competitor".
- 5 Nov 2026: B2B on Shopify Grow; this policy (floors 25/20, caps 20/15/15, one cost basis). Band re-set under it is
  proposed in `reports/trade-band-proposal-2026-11-05.md`, waiting for the owner's approval.
