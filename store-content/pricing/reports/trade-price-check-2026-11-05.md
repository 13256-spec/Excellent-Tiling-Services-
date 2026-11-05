# Trade price check, 5 Nov 2026

Owner asked whether trade prices are too cheap (Baron E120 paddles: $477.25 retail, $381.80 trade). Every fixed price in the B2B
price list (3,320 variants, 837 products) was checked against the unit cost in Shopify, GST basis per the playbook and the
`cost_src` column of the master list. Rule: trade price must leave 20% margin ex GST. Full data: `trade-price-check-2026-11-05.csv`.

| Trade margin ex GST | Variants |
|---|---|
| under 20% (floor) | 11 |
| 20-25% | 1,881 |
| 25-30% | 1,004 |
| 30% or more | 421 |
| no cost on file | 3 |

Median 24.2%. The Baron E120 paddles are at **22.0%** at the trade price (cost $297.83 inc GST = $270.75 ex, Roberts account), so they
pass the rule; at the public price the margin is 37.6%.

## The 11 under the floor (nothing changed yet, owner to decide)

| Product | Band | Public | Trade | Cost inc GST | Trade margin | Band that keeps 20% |
|---|---|---|---|---|---|---|
| Raimondi Self Levelling Compound Gauging Rake  | 10% | $131.99 | $118.79 | $112.20 | 5.5% | 0% |
| Sigma 64B2 Non-Slip Magnetic Mat  | 15% | $178.20 | $151.47 | $133.10 | 12.1% | 5% |
| Sigma 90NE Swivel Measurement Bar 64cm-0-64cm  | 15% | $348.30 | $296.06 | $260.15 | 12.1% | 5% |
| Sigma 37C Table Fixing Kit  | 15% | $240.55 | $204.47 | $179.68 | 12.1% | 5% |
| Sigma 17A Extension Bar 500mm  | 15% | $178.20 | $151.47 | $133.10 | 12.1% | 5% |
| Sigma 14G Kera-Cut Spare Scoring Wheel 12mm  | 20% | $32.20 | $25.76 | $22.14 | 14.0% | 10% |
| Sigma 8AEP2 Kera-Cut Extension Bar 50cm  | 20% | $299.25 | $239.40 | $205.40 | 14.2% | 10% |
| Sigma 421 Carriage Kit (2 Wheel Sets with Slab Support and Angle Support)  | 20% | $1035.95 | $828.76 | $710.63 | 14.3% | 10% |
| Sigma 402 Work Bench Storage Hooks for Kera-Cut  | 20% | $126.65 | $101.32 | $86.88 | 14.3% | 10% |
| Sigma 196725 Rubber Foot  | 10% | $4.85 | $4.37 | $3.63 | 16.9% | 5% |
| Roberts Designs Square Grate Shower Floor Waste - 50mm Outlet Chrome | 20% | $18.99 | $15.19 | $12.43 | 18.2% | 15% |

- **Raimondi Self Levelling Compound Gauging Rake**: the public price $131.99 is itself under the public floor (cost $112.20 inc GST x 1.25 =
  $140.25); public margin 15%. Needs a price rise to at least $140.25 (then band 0) or confirmation of the cost.
- **Roberts Designs Square Grate Shower Floor Waste 50mm, Chrome**: 18.2% at 20% band; 15% band gives 21.8%.
- **Nine Sigma items created 21 Oct 2026** (not in the master list, never on the 23 Oct cost refresh): their Shopify costs equal the
  `our_cost` in `../supplier-sync/roberts-designs-pricing.csv`, which for Sigma is the Roberts account price **ex GST**. If so they sit at
  12-17% and the bands should drop to 5-10%. If the owner confirms those costs already include GST, they pass (20-22%).

## If 20% feels too thin

| Floor | Variants that get a shallower band | Variants that lose the trade discount |
|---|---|---|
| 20% (today) | 11 | 1 |
| 25% | 1,897 | 296 |
| 30% | 2,897 | 1,005 |

Any change is applied with `trade_price_metafields_2026_11.py` + `b2b_price_list_2026_11.py` after the bands are moved (and
`priceListFixedPricesDelete` for variants that drop to band 0).
