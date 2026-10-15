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
| MELA bathroomware | via Bathroom City | Bathroom City **live** list price × (1 − SILVER trade discount) ÷ 1.1; the 2025 MELA catalogue RRP only where Bathroom City doesn't list the item (checked 12 Oct 2026, `reports/mela-catalogue-check-2026-10-12.csv`) | ex GST |
| BAT, BAT Trims, Raimondi, Panther, NICLIS, Washboy, Atika, ADA | BAT | `supplier-books-2026-05.csv` (Tools Book 1, Project Trims Book 1, Trims Book 1, Raimondi price list – May 2026), net price; 1,948 variants checked 12 Oct 2026 | ex GST |
| Roberts Designs, Maxisil, Sigma, Siri, Barwalt, Baron | Roberts Designs | unit cost already in Shopify (no price list on file yet) | ex GST |
| BAT SynSafe Acid 20 L, RLA Quick Set 5 L, Click Powerblock | – | **no cost recorded**, prices left alone | – |

SILVER trade discounts (owner's sheet `2026_NEW_SILVER_TRADE_PRICE.pdf`), off the GST-inclusive list price:
vanity package & handles 25%, basins 30%, tapware 40%, accessories 35%, mirrors & PORTER cabinets 25%,
inset baths (BOSTON, KASTEN) 20%, freestanding baths 40%, shower screens 40%, toilets 40%, bidet seat 20%,
sinks 40%, pop-up wastes 40%, heated towel rails 30%, floor waste/channel 40%, kitchen/laundry cabinets 20%.
Back-to-wall and corner baths (KORI, MIZO, NOOK) are **not on the sheet**; 20% is assumed until the owner
confirms. MELA towel rails are non-heated, so they use accessories 35%.

Delivery: the supplier's delivery charge is not added to costs; bulky-item delivery is charged to the
customer at checkout (owner, 3 Oct 2026).

## Supplier price files on hand (checked 12 Oct 2026)

The owner sent his supplier price files on 12 Oct 2026. They are owner-only (never to customers); the
parsed numbers live in this folder so the next check can be repeated.

| Owner's file | Covers | In the repo |
|---|---|---|
| Tools Book 1 – May 2026 (xlsx) | BAT tools, Panther, NICLIS, Washboy, Atika, ADA | `supplier-books-2026-05.csv`, book `tools` |
| Project Trims Book 1 – May 2026 (xlsx) | BAT Trims project range | book `project_trims` |
| Trims Book 1 (pdf) | BAT Trims premium range | book `premium_trims` |
| Raimondi Price List May 2026 (xlsx) | Raimondi | book `raimondi` |
| 2026 NEW SILVER TRADE PRICE (pdf) | Bathroom City trade discounts | the discount list above |
| 2025 MELA catalogue (pdf) | MELA RRPs (vanity, basin, mirror and toilet names are pictures: read by eye) | `reports/mela-catalogue-check-2026-10-12.csv` |

Result: every BAT-family cost equals the book (`reports/bat-cost-check-2026-10-12.csv`); every MELA cost is
at or above what the catalogue implies, because Bathroom City's live list is the same as the 2025 catalogue
for 479 variants and $20–$200 above it for 97 (CLARK/CLASSIC/BRITTANY vanities, MORRIS screens, a few
shower sets and mixers). **Rule: the live Bathroom City list is the cost basis; the catalogue is the fallback
and the cross-check.** If the owner's invoices show the catalogue prices still apply, re-cost those 97 and
prices drop about 5%. Full write-up: `reports/supplier-cost-check-2026-10-12.md`. Still missing: the Roberts
Designs price list, BAT Trims Book 2 (cove corners, stair nosings, APC60 caps, half-rounds, ETS-HW items),
and a cost for the three no-cost items.

## Competitors

| Competitor | What they sell | How we read prices |
|---|---|---|
| Bathroom City (bathroom-city.com.au) | MELA, the only other stockist | public `products.json`; matched per variant in `mela-pricing-2026-10-01.csv` (`bc_title` + `bc_sku`) |
| B&B Hardware, Maddington (bbhardware.com.au) | tiling hardware, ~50 identical items | public `products.json`; matched by hand in `BB_MATCH` (`reprice_2026_10.py`) |
| Terweys Total Hardware, Cannington | tiling hardware | **no online prices**; phone (08) 9451 9599 for spot checks |
| Eternity Tiles' own shop and WA stockists | tiles | sell at Eternity RRP |

Competitor sale prices can be below our cost (e.g. Bathroom City clearance on gun-metal finishes, NOOK/KORI
baths). Those are reported as "can't beat profitably", never matched.

## The rules (all prices inc GST, costs ex GST) – from 11 Oct 2026, thin-margin rule added 12 Oct

Owner's instruction, 11 Oct 2026: cheaper than every competitor on every item, cheaper again on
high-margin items, trade accounts cheaper still, always profitable. On 12 Oct he added: "we don't always
have to make 20% profit, sometimes more, sometimes less, depends on the product". `reprice_2026_10_12.py`
applies:

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
- **Thin-margin rule (12 Oct 2026).** 20% is the target, not an absolute floor. When the competitor is
  below our 20% price we go 1% under them (at least $1) as long as we still keep **10%** of the selling
  price. Between 5% and 10% only on products the owner has named (`OWNER_OK` in the script: Sigma ART 4CU,
  Baron E120). Never under 5%, never under cost: those items stay at the 20% price and are flagged
  "not undercut; owner's call" with the profit we'd make at 1% under. Thin-margin items get trade band 0
  when no band keeps them above the trade floor. A thin-margin price is raised back to the 20% price
  as soon as the competitor's price is no longer below it (the weekly run does this).
- A price is raised only when it is below the floor that applies, and never to or above the competitor.
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
- The old `trade-band-*` collections were deleted and the `trade-N` product tags removed on 12 Oct 2026
  (duplicates check); the band lives only in `ets.trade_band` and the `trade-list-N` collections.

## Files

| File | What it is |
|---|---|
| `store-pricing-2026-10-12.csv` | **Master price list** (12 Oct: supplier-file check, then the thin-margin rule – 22 prices cut): every active variant with old price, new price, the rule that set it, cost, margins, trade band (and the band it had before), trade price, competitor price, flags. Update it whenever prices change. |
| `reprice_2026_10_12.py` | Builds the master list from a Shopify bulk export (`products` with variants + unit cost) + competitor feeds + the current `trade-list-N` membership. Holds `BB_MATCH` and `OWNER_OK`. (`reprice_2026_10_11.py` is the same without the thin-margin rule.) |
| `reports/reprice-2026-10-11.md` | What the 11 Oct run changed, with the owner-review tables. |
| `store-pricing-2026-10-11.csv`, `store-pricing-2026-10-03.csv`, `reprice_2026_10.py` | Earlier plans, kept for history. |
| `supplier-books-2026-05.csv` | BAT, BAT Trims and Raimondi May 2026 price books (net ex GST), parsed from the owner's files. |
| `reports/supplier-cost-check-2026-10-12.md` | 12 Oct cost check against the supplier files, with the owner-review tables; detail in `reports/bat-cost-check-2026-10-12.csv` and `reports/mela-catalogue-check-2026-10-12.csv`. |
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
