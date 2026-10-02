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

# Eternity tiles, price list effective 5 Oct 2026 (plan, 2 Oct 2026, not yet applied)

`eternity-price-list-2026-10-05.txt` is the text of Eternity's PDF. `eternity_2026_10.py` turns it
into `eternity-tiles-2026-10-05.csv`: one row per tile variant with the current price, the new
SKU (Eternity renamed ET... codes to DSA...), RRP, cost tiers and the new price.

Rules:
- **Cost** recorded in Shopify = Eternity "non pallet" price ex GST. Pallet (57.6 m² porcelain /
  86.4 m² ceramic) and mixed 3+ pallet (172.8 m²+) prices are in the CSV for quoting big jobs.
- **New price** = 10% under Eternity's RRP, rounded down to 10c. Eternity's own shop and WA
  stockists (e.g. Online Flooring WA, Lava $55/m²) sell at RRP.
- **Floor**: price at least 25% above cost incl. GST. Prices are never raised.
- Not on the new list (price kept, no cost): Lava Etna Gloss 300x600 and 600x600, Lava Kraka
  600x1200 Matt, Cement White and Cement Grey 300x300. The list prints Time Stone Moon matt as
  YSR...; Eternity's site and our SKUs use YFR..., treated as the same tile.
