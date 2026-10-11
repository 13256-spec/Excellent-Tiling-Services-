# MELA pricing vs Bathroom City (plan, 1 Oct 2026, not yet applied)

`mela-pricing-2026-10-01.csv` has one row per MELA variant: our current price, Bathroom City's
price and list price, the new price, unit cost, margin and any flag. It doubles as the backup of
the old prices.

Rules:
- **Cost** = Bathroom City list price × (1 − SLIVER trade discount for the category).
  Back to wall and corner baths aren't on the sheet, so they use the lowest bath rate (20%).
- **New price** = 5% under Bathroom City's current price, rounded down to the dollar.
- **Floor**: after our own trade discount (5% small / 10% large items) the price must still be
  5% above cost. Where Bathroom City's sale price is below that, we go $1 under them only if
  trade buyers still break even; otherwise we stay at the floor (flagged).
- Prices are never raised. Variants already below target keep their price; 11 that are below
  the floor (CLASSIC vanities, BRITTANY 600, DAVISSON basin) are flagged for review.
- 79 variants have no Bathroom City equivalent and are left alone.

Scripts: `price.py` (plan), `manual.py` + `fuzzy.py` (name matching for items without a SKU).

# Eternity tiles, price list effective 5 Oct 2026 (applied 2 Oct 2026)

`eternity-price-list-2026-10-05.txt` is the text of Eternity's PDF. `eternity_2026_10.py` turns it
into `eternity-tiles-2026-10-05.csv`: one row per tile variant with the current price, the new
SKU (Eternity renamed ET... codes to DSA...), RRP, cost tiers and the new price.

Rules:
- **Cost** recorded in Shopify = Eternity "non pallet" price ex GST. Pallet (57.6 m² porcelain /
  86.4 m² ceramic) and mixed 3+ pallet (172.8 m²+) prices are in the CSV for quoting big jobs.
- **New price** = 15% under Eternity's RRP, rounded down to 10c ("option B", approved by the
  owner). Eternity's own shop and WA stockists (e.g. Online Flooring WA, Lava $55/m²) sell at RRP.
  Margin is about 35-37% ex GST; the CSV's `trade_price` (15% off public) keeps trade at 24-27%.
- **Floor**: price at least 25% above cost incl. GST.
- Applied in Shopify: 42 variants got the new price and cost; 16 SKUs renamed ET... -> DSA...,
  Lava Kraka 600x1200 Gloss given SKU YW277315.
- Not on the new list (price kept, no cost): Lava Etna Gloss 300x600 and 600x600, Lava Kraka
  600x1200 Matt, Cement White and Cement Grey 300x300. The list prints Time Stone Moon matt as
  YSR...; Eternity's site and our SKUs use YFR..., treated as the same tile.

## Range update to match the 5 Oct 2026 list (2 Oct 2026)

- Removed sizes not on the list: Lava Etna Gloss 300x600 and 600x600, Lava Kraka Matt 600x1200,
  Cement White and Cement Grey 300x300 (tags and descriptions updated to match).
- Added missing sizes: Morgan Hail 600x1200 (DSA126AK661), Morgan Cloud 300x300 (DSA33AK662) and
  300x600 (DSA36AK662), Cement White 300x600 (DSA36MQ01).
- Created 31 products (43 variants) with `eternity_new_products_2026_10.py` -> `eternity-new-products-2026-10.json`:
  Lava Vesuv, Fumosa, Astra White/Greige, Sand White/Beige/Grey, Bianco Greco, Caliza, E-Time Calcare/Chiaro,
  Oak Aube, Subway and Subwave ceramics, White/Eternal Marble/Eternal Carrara/Element Grey/Whisper Grey
  ceramic wall tiles, and 8 natural stone mosaics (sold per sheet). Same pricing rule (15% under RRP),
  cost recorded, published to all channels, added to `tiles`, delivery profile "Local delivery or pickup -
  large items".
- Photos: Eternity's own product photos for the ceramic ranges; swatches cut from the price list PDF
  (`eternity-swatches/`, about 200px, alt text says "indicative swatch") for ranges Eternity's shop doesn't
  list yet. Replace with proper photos when Eternity publishes them.
- New smart collections: `ceramic-wall-tiles` (tag Ceramic + type Tile) and `mosaic-tiles` (tag Mosaic).

# Store-wide public and trade pricing (applied 3 Oct 2026, approved by the owner)

`reprice_2026_10.py` → `store-pricing-2026-10-03.csv`: one row per active variant with the old price
(backup), new public price, trade band and trade price, cost (ex GST), margins, the competitor price it
was compared with, and any flag. Rules are in the script's docstring. In short:

- Competitors: Bathroom City for MELA (5% under, to the dollar); B&B Hardware, Maddington, for the ~50
  hardware items it also sells (5% under, to 5c). Terweys Total Hardware has no online prices. Other
  hardware: 10% under our old (supplier RRP) price. Tiles keep the 2 Oct prices.
- Profit floor: public ≥ cost inc GST × 1.25, trade ≥ cost inc GST × 1.15. Prices below the floor rise
  at most 10% and stay under the competitor; bigger gaps are flagged `BELOW PROFIT FLOOR` and left.
- MELA costs are estimates (Bathroom City list × (1 − SLIVER trade discount)); the sheet's discount is off
  the GST-inclusive list, so they're stored ex GST (÷ 1.1).
- Trade: per-product bands of 5/10/15/20/25% (tiles max 15%), each the deepest that keeps every
  variant above the trade floor. Shopify Basic has no B2B price lists, so each band is a manual (unpublished)
  collection `trade-list-5` ... `trade-list-25` with an automatic discount "Trade price – N%" for the
  "Trade customers" segment (customer tag `trade`). To change one item's trade discount, move it to another
  `trade-list-N` collection in Shopify admin. The old tag-based `trade-band-*` collections are no longer used.
  (A `custom.trade_price` variant metafield definition exists but isn't filled.)
- Applied: 1,388 prices, 599 MELA costs (ex GST), 5 trade discounts. 4 B&B items and 64 MELA items stay above
  the competitor because it sells below our profit floor; ~30 `BELOW PROFIT FLOOR` items left for the owner.
- PDFs: `price_list_pdf.py` -> `price-lists/ETS-price-list-2026-10.pdf` (retail) and
  `price-lists/ETS-trade-price-list-2026-10.pdf` (retail + trade).
- Supplier delivery (SILVER sheet: $80 metro, $120 at 30-50 km) isn't added to costs: the owner confirmed
  (3 Oct) that delivery for bulky items is charged to the customer at checkout.

## On hold: MELA DAVISSON basin, White (4 Oct 2026)

Set to sold out (inventory tracked, 0 stock, "continue selling when out of stock" off) so it can't be
ordered at $199. Its recorded cost ($225.91 ex GST) was copied from the Matt White, because Bathroom City
doesn't list a plain White, so the "below cost" flag may be wrong. Owner to confirm whether MELA supplies
it and at what SILVER cost. To bring it back: set the variant's inventory policy to CONTINUE (or untrack
inventory) and re-price against the real cost. Matt Black and Matt White ($337) are unaffected.

# Store-wide repricing, 11 Oct 2026 (owner's instruction, applied the same day)

The owner asked for prices cheaper than every competitor, cheaper again on high-margin items, and trade
accounts cheaper still. `reprice_2026_10_11.py` → `store-pricing-2026-10-11.csv` (master list, replaces
the 3 Oct one) and `reports/reprice-2026-10-11.md` (what changed, owner-review tables).

- The store had grown to 780 active products / 3,562 variants: ~1,950 BAT, BAT Trims, Raimondi, Panther,
  Washboy, NICLIS, Atika and ADA variants were added after 4 Oct with costs but no competitor check or
  trade band. All are now in the plan.
- New rule on top of the playbook: **margin cap 40%**. 563 variants above 40% were cut to 40% (Roberts
  trims, BAT trims and tools, some tiles and mosaics). Competitor rule unchanged (5% under; 10% under when
  still at 40%+). 67 variants that were under the 20% floor went up to the floor (CLASSIC/BRITTANY/CLARK
  vanities, Baron F300 and parts, Maxisil wet-area silicone). 9 stay below the floor because the
  competitor is lower (NOOK/KORI/MIZO baths, Sigma 4CU, Baron E120); 28 Expansion-trim variants are
  flagged COST CHECK (same $23.99 cost on every size).
- Applied: 646 prices (579 down, 67 up), `ets.trade_band` metafield on all 780 products, 361 products moved
  between the `trade-list-N` collections (now 25%: 264, 20%: 185, 15%: 173, 10%: 19, 5%: 137, none: 2).
- New B&B matches for BAT and Raimondi items in `BB_MATCH`. `monitor_competitors.py` now reads this plan.
- PDFs regenerated in `price-lists/`.

## Second Raimondi batch, 11 Oct 2026 (evening)

144 Raimondi products imported during the day were priced with the same rules (22 variants cut to the 40% cap, the rest kept),
given trade bands (25%: 54, 15%: 53, 20%: 37) and added to the `trade-list-N` collections. Four BAT/Panther items that got a
cost during the day were capped too and ten moved out of the 5% "no cost" band. Report:
`reports/reprice-2026-10-11-raimondi-batch2.md`. The master CSV and PDFs include them.

Any product imported later needs the same three steps (price check, `ets.trade_band`, `trade-list-N`); the `ets-pricing` agent
does them from a fresh bulk export.
