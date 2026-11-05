# ETS pricing playbook

How Excellent Tiling Services prices every product, where the data lives, and how to change prices
safely. Written for the owner and for the `ets-pricing` agent (`.claude/agents/ets-pricing.md`).

## The goal

1. **Public price**: cheaper than the competitor that sells the same item, but always profitable.
   **Exception, MELA (20 Oct 2026):** Bathroom City is our MELA supplier and we are not allowed to advertise
   MELA below their price. MELA public prices are set **equal to Bathroom City's current price**, never under.
2. **Trade price**: cheaper again for approved trade accounts, still profitable.
3. **Profit first**: if the competitor is below our profit floor, we don't follow them down.

## Suppliers and costs

| Range | Supplier | Cost source | Cost basis |
|---|---|---|---|
| Tiles (Eternity) | Eternity Tiles | `eternity-price-list-2026-10-05.txt` (5 Oct 2026 wholesale PDF), "non pallet" price | ex GST |
| MELA bathroomware | via Bathroom City | Bathroom City list price × (1 − SILVER trade discount) ÷ 1.1 | ex GST |
| Roberts Designs, Maxisil | Roberts Designs | unit cost in Shopify = trade-account price x 1.1 (owner, 14 Oct 2026: the account prices did not include GST) | as stored; use the floor formula as is |
| Sigma, Siri, Barwalt, Baron | Roberts Designs | unit cost already in Shopify (trade-account price, 28 Sep 2026) | ex GST |
| BAT, Click (a few items) | – | **no cost recorded**, prices left alone | – |
| RLA and Gripset (69 products, live 29 Oct 2026, 0 stock, not purchasable) | RLA Polymers | **no cost yet** (trade account pending); priced a little under AU retail, see `../supplier-sync/rla-market-prices-2026-10-28.csv`. No trade band until a cost exists. | – |

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
| Bathroom City (bathroom-city.com.au) | MELA supplier and the only other stockist; **we must not advertise below their price** | public `products.json`; matched per variant in `mela-pricing-2026-10-01.csv` (`bc_title` + `bc_sku`) |
| B&B Hardware, Maddington (bbhardware.com.au) | tiling hardware, ~50 identical items | public `products.json`; matched by hand in `BB_MATCH` (`reprice_2026_10.py`) |
| Terweys Total Hardware, Cannington | tiling hardware | **no online prices**; phone (08) 9451 9599 for spot checks |
| Eternity Tiles' own shop and WA stockists | tiles | sell at Eternity RRP |

Competitor sale prices can be below our cost (e.g. Bathroom City clearance on gun-metal finishes, NOOK/KORI
baths). Those are reported as "can't beat profitably", never matched.

## The rules (all prices inc GST, costs ex GST)

- **Public floor** = cost × 1.1 × 1.25 (at least 20% of the selling price is profit).
- **Trade floor** (owner, 14 Oct 2026): the trade price must leave **20% margin ex GST**, i.e. trade price ≥ cost ÷ 0.8 × 1.1. (Until 14 Oct it was cost × 1.1 × 1.15, about 13%, which the owner found too cheap.)
- **MELA** = **the same as Bathroom City's current price** (owner, 20 Oct 2026: supplier does not allow us to
  advertise cheaper). Where Bathroom City's clearance price is below our public floor we stay above them.
  (Until 20 Oct it was 5% under Bathroom City.)
- **Hardware B&B also sells** = 5% under B&B, rounded down to 5c.
- **Other hardware** = 10% under the supplier RRP (our old price), rounded down to 5c.
- **Tiles** = 15% under Eternity RRP, rounded down to 10c (`eternity_2026_10.py`).
- Never undercut below the public floor. Prices below the floor are raised only with the owner's OK.
- **Trade bands** (per product, not per variant): the deepest of 25 / 20 / 15 / 10 / 5% that keeps every
  variant above the trade floor. Tiles max 15%. A product with no band that works gets no trade discount (it is in none of the `trade-list-N` collections).

## Where things are in Shopify

- Prices and unit costs: on each variant.
- Trade price, for reading in admin: product metafield `ets.trade_price` ("$x (N% off)", pinned on the product
  page) and variant metafield `custom.trade_price` (the number). Written by `trade_price_metafields_2026_11.py`.
- **Trade pricing is native B2B (since 5 Nov 2026, Shopify Grow plan).** One B2B market "Trade accounts (B2B)"
  (all company locations) carries the catalog "Trade price list" with the price list "Trade prices": a fixed price
  per variant = public price x (1 - `ets.trade_band`/100). A trade customer is a **company** (Customers -> Companies)
  with a location and a contact; when they log in they see and pay the trade prices on every channel, no tag, no
  discount code. Products with band 0 have no fixed price and sell at the public price. Grow allows 3 active B2B
  catalogs, attached to the market, not to single companies.
- The old scheme is kept only as the band record: manual collections `trade-list-5` ... `-25` and the product
  metafield `ets.trade_band` still say which band a product is in, and `custom.trade_price` / `ets.trade_price`
  show the number. The five automatic discounts "Trade price – N%" are **deactivated**; the customer tag `trade`
  is no longer used for pricing.
- Old `trade-band-*` collections and `trade-N` product tags are no longer used.
- **Approving a trade applicant** (tag `trade-applicant`, from the website form): Customers -> Companies -> Add
  company: business name, the applicant as contact (their existing customer email), one location with their
  address, payment terms "No payment terms" (pay at checkout) unless the owner agrees credit terms (Net 7/15/30
  are available per location). The company location joins the Trade market automatically. Then remove the
  `trade-applicant` tag. Nothing else: no `trade` tag, no discount.

## Files

| File | What it is |
|---|---|
| `store-pricing-2026-10-03.csv` | **Master price list**: every active variant with old price, new price, cost, margins, trade band, trade price, competitor price, flags. Update it whenever prices change. |
| `reprice_2026_10.py` | Builds the master list from a Shopify export + competitor feeds. Holds `BB_MATCH`. |
| `monitor_competitors.py` | Weekly check (public feeds only, changes nothing) → `reports/price-check-YYYY-MM-DD.md`. |
| `price_list_pdf.py` | PDFs in `price-lists/`: retail, trade, and **owner-only** cost & price list (never send to customers). |
| `eternity_2026_10.py`, `eternity_new_products_2026_10.py` | Eternity tile pricing and new tile products. |
| `mela-pricing-2026-10-01.csv` | MELA ↔ Bathroom City matching + cost estimates. |
| `../supplier-sync/rla-market-prices-2026-10-28.csv` | RLA / Gripset drafts: proposed price per variant with the competitor prices it came from and a `price_check` flag. Add to the master list once costs exist. |

## Changing prices safely (for the agent)

1. Run `monitor_competitors.py`; read the report.
2. Propose changes in a table (item, old, new, competitor, cost, profit %, trade band). **Get the owner's
   explicit approval before any price write.**
3. Apply with `productVariantsBulkUpdate`, many products per request using GraphQL aliases. Keep each
   request under 16,384 characters. `bulkOperationRunMutation` is blocked in this setup.
4. If a trade band changes, move the product between `trade-list-N` collections
   (`collectionRemoveProducts` / `collectionAddProducts`).
   **Also set the product metafield `ets.trade_band` to the same number (0 if no list).** The theme shows the
   trade price and the "N% off" note from this field, not from the collection, so a stale value shows trade
   customers the wrong price.
   **Then refresh the trade prices themselves**: `b2b_price_list_2026_11.py` rewrites the fixed prices in the B2B
   price list (what trade accounts pay), and `trade_price_metafields_2026_11.py` the record fields `custom.trade_price`
   and `ets.trade_price`. Both go stale whenever a public price or a band changes. A product whose band drops to 0
   also needs its fixed prices deleted from the price list (`priceListFixedPricesDelete`).
5. Update `store-pricing-2026-10-03.csv`, rerun `price_list_pdf.py`, commit, and tell the owner in plain
   words what changed.

Shopify quirk: when changing a product's SEO title, always send the meta description too, or it is wiped.
