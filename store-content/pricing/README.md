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
