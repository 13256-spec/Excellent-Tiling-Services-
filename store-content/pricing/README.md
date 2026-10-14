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
- 14 Oct 2026: the 873 Roberts-supplied rows (Roberts Designs, Maxisil, Sigma, Siri, Baron, Barwalt) had their cost multiplied by 1.1 after the owner confirmed the Roberts account prices did not include GST; `new_price` on those rows was refreshed to the live price and both margins recomputed. Prices unchanged. The 121 variants now under the floor are in `reports/roberts-gst-below-floor-2026-10-14.csv`.
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

## Eternity "wholesale essentials" list (V27102025.01, received 14 Oct 2026)

`eternity-essentials-2025-10-27.csv`: the 30 lines from Eternity's essentials sheet (cement, Easy Screed, WPA
waterproofing, TPA/Sika adhesives, Ardex FS-DD grout and SE silicone, aluminium angles, LX linear drains, tile
insert and square-plate floor wastes), wholesale ex GST. It does **not** cover the DSA bathroomware (tapware,
showers, vanities, basins, sinks, mirrors, toilet); that request is still `DSA-trade-price-request-2026-10-14.xlsx`.

Applied: BL-TID50 ($38.25) and BL-TID80 ($38.25) recorded as the cost of the two DSA tile insert floor wastes
(50mm given SKU BL-TID50; the 80mm keeps its web code; `needs-cost` removed). The two FLRG-SFD square-plate
drains ($11.01 / $16.11) probably match the Twist Top Floor Drains 80mm/100mm but the sizes don't line up, so
nothing recorded until Eternity confirms. The other 25 items are not stocked; `proposed_price_inc_gst` in the CSV
is cost x 1.1 (GST) / 0.65 (35% margin on the ex-GST sale price), rounded up to 5c, for the owner to approve.

## Eternity vanity packages (sheet "Wholesale Vanity Package Pricing 2025", received 14 Oct 2026)

`eternity-vanity-packages-2025.csv`: RRP and the three wholesale tiers (account 45% off, COD / 5-buy account 50%,
5-buy COD 55%) for the Malaga all-in-one packages. Two products created live at RRP (owner: sell at Eternity's
price for now), `malaga_packages_2026_10.py` -> `supplier-sync/malaga-packages-2026-10-14.json`:
China Top (3 colours x 750/900/1200) and Stone Top (3 colours x 750/900/1200/1500/1800). Stone colour (White Burst /
Blanco Bliss) and basin shape are taken in the order notes, not as variants. Cost = the sheet's **account deal 45%** column (owner, 14 Oct 2026), stored ex GST (÷ 1.1):
china top $590.00 / $771.82 / $953.64, stone top $734.55 / $852.73 / $1,052.73 / $1,416.36 / $1,680.00. Margin 46-50%
at RRP; both products in `trade-list-25`; 24 rows appended to the master CSV. Package photos are the sheet's own images (`supplier-sync/malaga-package-images/`).
