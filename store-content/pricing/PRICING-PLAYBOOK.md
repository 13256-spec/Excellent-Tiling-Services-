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
| Roberts Designs, Maxisil | Roberts Designs | unit cost in Shopify = trade-account price x 1.1 (owner, 14 Oct 2026: the account prices did not include GST) | as stored; use the floor formula as is |
| Sigma, Siri, Barwalt, Baron | Roberts Designs | unit cost already in Shopify (trade-account price, 28 Sep 2026) | ex GST |
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

## The rules (all prices inc GST, costs ex GST)

- **Public floor** = cost × 1.1 × 1.25 (at least 20% of the selling price is profit).
- **Trade floor** (owner, 14 Oct 2026): the trade price must leave **20% margin ex GST**, i.e. trade price ≥ cost ÷ 0.8 × 1.1. (Until 14 Oct it was cost × 1.1 × 1.15, about 13%, which the owner found too cheap.)
- **MELA** = 5% under Bathroom City's current price, rounded down to the dollar.
- **Hardware B&B also sells** = 5% under B&B, rounded down to 5c.
- **Other hardware** = 10% under the supplier RRP (our old price), rounded down to 5c.
- **Tiles** = 15% under Eternity RRP, rounded down to 10c (`eternity_2026_10.py`).
- Never undercut below the public floor. Prices below the floor are raised only with the owner's OK.
- **Trade bands** (per product, not per variant): the deepest of 25 / 20 / 15 / 10 / 5% that keeps every
  variant above the trade floor. Tiles max 15%. A product with no band that works gets no trade discount (it is in none of the `trade-list-N` collections).

## Where things are in Shopify

- Prices and unit costs: on each variant.
- Trade discounts: manual collections `trade-list-5`, `-10`, `-15`, `-20`, `-25`, each with an automatic
  discount "Trade price – N%" limited to the customer segment "Trade customers" (customer tag `trade`).
  Shopify Basic has no B2B price lists, so this is how per-item trade pricing works. To change an item's
  trade discount, move it between those collections. A product must be in only one of them.
- Old `trade-band-*` collections and `trade-N` product tags are no longer used.

## Files

| File | What it is |
|---|---|
| `store-pricing-2026-10-03.csv` | **Master price list**: every active variant with old price, new price, cost, margins, trade band, trade price, competitor price, flags. Update it whenever prices change. |
| `reprice_2026_10.py` | Builds the master list from a Shopify export + competitor feeds. Holds `BB_MATCH`. |
| `monitor_competitors.py` | Weekly check (public feeds only, changes nothing) → `reports/price-check-YYYY-MM-DD.md`. |
| `price_list_pdf.py` | PDFs in `price-lists/`: retail, trade, and **owner-only** cost & price list (never send to customers). |
| `eternity_2026_10.py`, `eternity_new_products_2026_10.py` | Eternity tile pricing and new tile products. |
| `mela-pricing-2026-10-01.csv` | MELA ↔ Bathroom City matching + cost estimates. |

## Changing prices safely (for the agent)

1. Run `monitor_competitors.py`; read the report.
2. Propose changes in a table (item, old, new, competitor, cost, profit %, trade band). **Get the owner's
   explicit approval before any price write.**
3. Apply with `productVariantsBulkUpdate`, many products per request using GraphQL aliases. Keep each
   request under 16,384 characters. `bulkOperationRunMutation` is blocked in this setup.
4. If a trade band changes, move the product between `trade-list-N` collections
   (`collectionRemoveProducts` / `collectionAddProducts`).
5. Update `store-pricing-2026-10-03.csv`, rerun `price_list_pdf.py`, commit, and tell the owner in plain
   words what changed.

Shopify quirk: when changing a product's SEO title, always send the meta description too, or it is wiped.
