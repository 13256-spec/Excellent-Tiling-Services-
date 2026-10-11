# ETS pricing playbook

How Excellent Tiling Services prices every product, where the data lives, and how to change prices
safely. Written for the owner and for the `ets-pricing` agent (`.claude/agents/ets-pricing.md`).

## The goal

1. **Public price**: cheaper than the competitor that sells the same item, but always profitable.
2. **Trade price**: cheaper again for approved trade accounts, still profitable.
3. **Profit first**: if the competitor is below our profit floor, we don't follow them down.

## Suppliers and costs

| Range | Supplier | Cost source | Cost basis |
|---|---|---|---|
| Tiles (Eternity) | Eternity Tiles | `eternity-price-list-2026-10-05.txt` (5 Oct 2026 wholesale PDF), "non pallet" price | ex GST |
| MELA bathroomware | via Bathroom City | Bathroom City list price × (1 − SILVER trade discount) ÷ 1.1 | ex GST |
| Roberts Designs, Maxisil, Sigma, Siri, Barwalt, Baron | Roberts Designs | unit cost already in Shopify | ex GST |
| BAT, RLA, Click (a few items) | – | **no cost recorded**, prices left alone | – |

SILVER trade discounts (owner's sheet `2026_NEW_SILVER_TRADE_PRICE.pdf`), off the GST-inclusive list price:
vanity package & handles 25%, basins 30%, tapware 40%, accessories 35%, mirrors & PORTER cabinets 25%,
inset baths (BOSTON, KASTEN) 20%, freestanding baths 40%, shower screens 40%, toilets 40%, bidet seat 20%,
sinks 40%, pop-up wastes 40%, heated towel rails 30%, floor waste/channel 40%, kitchen/laundry cabinets 20%.
Back-to-wall and corner baths (KORI, MIZO, NOOK) are **not on the sheet**; 20% is assumed until the owner
confirms. MELA towel rails are non-heated, so they use accessories 35%.

Delivery: the supplier's delivery charge is not added to costs; bulky-item delivery is charged to the
customer at checkout (owner, 3 Oct 2026).

## Competitors

| Competitor | What they sell | How we read prices |
|---|---|---|
| Bathroom City (bathroom-city.com.au) | MELA, the only other stockist | public `products.json`; matched per variant in `mela-pricing-2026-10-01.csv` (`bc_title` + `bc_sku`) |
| B&B Hardware, Maddington (bbhardware.com.au) | tiling hardware, ~50 identical items | public `products.json`; matched by hand in `BB_MATCH` (`reprice_2026_10.py`) |
| Terweys Total Hardware, Cannington | tiling hardware | **no online prices**; phone (08) 9451 9599 for spot checks |
| Eternity Tiles' own shop and WA stockists | tiles | sell at Eternity RRP |

Competitor sale prices can be below our cost (e.g. Bathroom City clearance on gun-metal finishes, NOOK/KORI
baths). Those are reported as "can't beat profitably", never matched.

## The rules (all prices inc GST, costs ex GST) – from 11 Oct 2026

Owner's instruction, 11 Oct 2026: cheaper than every competitor on every item, cheaper again on
high-margin items, trade accounts cheaper still, always profitable. `reprice_2026_10_11.py` applies:

- **Public floor** = cost × 1.1 × 1.25 (at least 20% of the selling price is profit).
- **Trade floor** = cost × 1.1 × 1.15.
- **Margin cap 40%**: an item earning more than 40% is cut to 40% (price = cost × 1.1 ÷ 0.6). This is
  the "high-margin items get cheaper" rule and it applies to every range, tiles included.
- **Competitor**: 5% under the competitor's current price (Bathroom City for MELA, B&B Hardware for the
  hardware it also sells, matched by hand in `BB_MATCH`); 10% under when we'd still make 40%+ at 5% under.
- **New products / no competitor**: the current price stands unless the margin cap or the floor moves it.
  (Earlier rules: tiles 15% under Eternity RRP, other hardware 10% under the supplier RRP; those prices
  are the starting point the cap works from.)
- **Rounding**: MELA down to the dollar, tiles down to 10c, everything else down to 5c. Floors round up.
- **Never below the floor.** If the competitor is below our floor we sit at the floor and the item is
  flagged "competitor is below our floor; not undercut". A price is raised only when it is below the
  floor, and never to or above the competitor (those are flagged BELOW PROFIT FLOOR for the owner).
- **Cost sanity check**: a product whose sizes all share one cost while their prices differ by 25%+ has a
  copied cost; price kept, flagged COST CHECK, trade band 5% until the supplier confirms the cost.
- **Trade bands** (per product, not per variant): the deepest of 25 / 20 / 15 / 10 / 5% that keeps every
  variant above the trade floor. Tiles max 15%. Products with a variant that has no cost get 5%.

## Discount codes (from 11 Oct 2026)

A code is only safe where the trade band already proves the margin. Every product in `trade-list-20` or
`trade-list-25` keeps all its variants above the trade floor at 20–25% off, so a 10% public code on those
products leaves at least 22.7% of the selling price as profit (price × 0.9 ≥ cost × 1.1 × 1.29). Tiles (band
max 15), vanities, baths, toilets and everything in bands 5, 10 and 15 are outside every percentage code.
The codes are scoped to the collections, so when a product changes band the codes follow automatically.

| Code | What it does | Where it works | Limits | Shopify ID |
|---|---|---|---|---|
| `WELCOME10` | 10% off | products in `trade-list-20` + `trade-list-25` (547 products, 2,625 variants on 11 Oct) | once per customer; combines with shipping discounts only, never with the automatic trade discounts | DiscountCodeNode/1385793290303 |
| `COMEBACK10` | 10% off | same collections | once per customer; same combining rules | DiscountCodeNode/1385793323071 |
| `FREEPOST` | free standard shipping (shipping line up to $30) | Australian addresses, order subtotal $60 or more | once per customer; combines with product discounts | DiscountCodeNode/1385793355839 |

Where each code is used: WELCOME10 in the welcome email series and on the site's sign-up pop-up, COMEBACK10 in
the win-back email, FREEPOST in the second abandoned-checkout email (`store-content/email/README.md`).

Rules for any new code or sale:
- 10% off: bands 20 and 25 only. 15% off: band 25 only (margin stays ≥ 23%). 5% off: bands 15 and up.
- Never on tiles, vanities, baths or toilets, never on band 5 or 10 products, never below the public floor.
- Keep the automatic "Trade price – N%" discounts at `combinesWith.productDiscounts = false` so a trade
  customer can't stack a code on top of trade pricing. Shipping codes may combine with both.
- Check before launch: for every variant in scope, `price × (1 − discount)` must be ≥ `cost × 1.1 × 1.25`
  (the columns are in the master CSV).
- `ETSWELCOME10` ($10 off $200 of tapware/accessories) was created in Shopify on 11 Oct outside this plan; it
  is not referenced anywhere. The owner decides whether to keep it; the playbook does not use it.

## Where things are in Shopify

- Prices and unit costs: on each variant.
- Trade discounts: manual collections `trade-list-5`, `-10`, `-15`, `-20`, `-25`, each with an automatic
  discount "Trade price – N%" limited to the customer segment "Trade customers" (customer tag `trade`).
  Shopify Basic has no B2B price lists, so this is how per-item trade pricing works. A product must be in
  only one of them.
- **Product metafield `ets.trade_band`** ("Trade discount band (%)", 0/5/10/15/20/25) mirrors the
  collection and is what the theme reads to show a logged-in trade customer their price with the retail
  price crossed out. To change an item's trade discount, set the metafield AND move it between the
  collections; the scripts do both. Full guide: `store-content/trade-accounts/README.md`.
- Old `trade-band-*` collections and `trade-N` product tags are no longer used.

## Files

| File | What it is |
|---|---|
| `store-pricing-2026-10-11.csv` | **Master price list**: every active variant with old price, new price, the rule that set it, cost, margins, trade band (and the band it had before), trade price, competitor price, flags. Update it whenever prices change. |
| `reprice_2026_10_11.py` | Builds the master list from a Shopify bulk export (`products` with variants + unit cost) + competitor feeds + the current `trade-list-N` membership. Holds `BB_MATCH`. |
| `reports/reprice-2026-10-11.md` | What the 11 Oct run changed, with the owner-review tables. |
| `store-pricing-2026-10-03.csv`, `reprice_2026_10.py` | The 3 Oct plan, kept for history. |
| `monitor_competitors.py` | Weekly check (public feeds only, changes nothing) → `reports/price-check-YYYY-MM-DD.md`. |
| `price_list_pdf.py` | PDFs in `price-lists/`: retail, trade, and **owner-only** cost & price list (never send to customers). |
| `eternity_2026_10.py`, `eternity_new_products_2026_10.py` | Eternity tile pricing and new tile products. |
| `mela-pricing-2026-10-01.csv` | MELA ↔ Bathroom City matching + cost estimates. |

## Changing prices safely (for the agent)

1. Run `monitor_competitors.py`; read the report.
2. Propose changes in a table (item, old, new, competitor, cost, profit %, trade band). **Get the owner's
   explicit approval before any price write** (a standing instruction like the one on 11 Oct 2026 counts;
   say what you are about to do and report what changed).
3. Export the catalogue with `bulkOperationRunQuery` (allowed; `bulkOperationRunMutation` is blocked),
   download the JSONL, run `reprice_2026_10_11.py`, read the summary and the flagged rows.
4. Apply with `productVariantsBulkUpdate`, many products per request using GraphQL aliases. Keep each
   request under 16,384 characters.
5. Set `ets.trade_band` with `productUpdate` (metafields) and move the product between `trade-list-N`
   collections (`collectionRemoveProducts` / `collectionAddProducts`). Both, always.
6. Update the master CSV, rerun `price_list_pdf.py`, write `reports/reprice-YYYY-MM-DD.md`, commit, and
   tell the owner in plain words what changed.

Shopify quirk: when changing a product's SEO title, always send the meta description too, or it is wiped.
