# Trade price check, 5 Nov 2026

Owner asked whether trade prices are too cheap (Baron E120 paddles: $477.25 retail, $381.80 trade). Every fixed price in the B2B
price list (3,320 variants, 837 products) was checked against the unit cost in Shopify, GST basis per the playbook and the
`cost_src` column of the master list. Rule: trade price must leave 20% margin ex GST. Full data: `trade-price-check-2026-11-05.csv`.

| Trade margin ex GST | Variants |
|---|---|
| under 20% (floor) | 2 |
| 20-25% | 1,890 |
| 25-30% | 1,004 |
| 30% or more | 421 |
| no cost on file | 3 |

Median 24.2%. The Baron E120 paddles are at **22.0%** at the trade price (cost $297.83 inc GST = $270.75 ex, Roberts account), so they
pass the rule; at the public price the margin is 37.6%.

## The 2 under the floor (nothing changed yet, owner to decide)

Owner confirmed (5 Nov) that the Shopify costs on the 21 Oct Roberts items (Baron paddles $297.83, nine Sigma spares) already
include GST, so those all pass at 20-22%. Left:

| Product | Band | Public | Trade | Cost inc GST | Trade margin | Band that keeps 20% |
|---|---|---|---|---|---|---|
| Roberts Designs Square Grate Shower Floor Waste - 50mm Outlet Chrome | 20% | $18.99 | $15.19 | $12.43 | 18.2% | 15% |
| Raimondi Self Levelling Compound Gauging Rake  | 10% | $131.99 | $118.79 | $112.20 | 5.5% | 0% |

- **Raimondi Self Levelling Compound Gauging Rake**: the public price $131.99 is itself under the public floor (cost $112.20 inc GST x 1.25 =
  $140.25); public margin 15%. Needs a price rise to at least $140.25 (then band 0) or confirmation of the cost.
- **Roberts Designs Square Grate Shower Floor Waste 50mm, Chrome**: 18.2% at 20% band; 15% band gives 21.8%.

## If 20% feels too thin

| Floor | Variants that get a shallower band | Variants that lose the trade discount |
|---|---|---|
| 20% (today) | 11 | 1 |
| 25% | 1,897 | 296 |
| 30% | 2,897 | 1,005 |

Any change is applied with `trade_price_metafields_2026_11.py` + `b2b_price_list_2026_11.py` after the bands are moved (and
`priceListFixedPricesDelete` for variants that drop to band 0).
