# Shipping weights and box sizes (28 Sep 2026)

`product-weights.csv` has a shipping weight, packed box size and shipping method for every variant in the store (1,691 variants, 1,539 of them live). `estimate_weights.py` builds it from a Shopify product export.

## Where the numbers come from
None of our suppliers publish shipping weights. Roberts Designs, Bathroom City (MELA) and Eternity Tiles were all checked. So every weight is an estimate. Sizes come from the product description or title where they are given (vanity width, bath length, basin dimensions, trim length, blade diameter, pack count). The weight then follows from the material. The `basis` column says which source was used for each row.

Check a few against real parcels. The ones most worth weighing are vanities, baths, shower screens, mirrors and tile cutters.

## Columns
- `weight_kg`: packed weight of one unit. Tiles are per m².
- `box_cm`: packed box, longest side first.
- `cubic_kg`: Australia Post cubic weight (L×W×H ÷ 4000). Couriers charge the higher of this and the real weight.
- `ship_by`: `auspost` if it fits a MyPost Business parcel (22 kg, 105 cm longest side, 0.25 m³), otherwise `freight`. Tiles are always freight.
- `in_shopify`: whether the weight has been entered on the Shopify variant yet.

## Summary (live variants)
| Ship by | Variants | What |
| --- | --- | --- |
| auspost | 956 | tapware, accessories, silicone, grout up to 10 kg, tools, spacers, blades, basins, sinks up to 770 mm, most mirrors, tile cutters up to 84 cm, 1 m trims, linear drains up to 900 mm |
| freight | 583 | 3 m and 2.5 m trims, tiles, vanities, baths, toilets, shower screens, tallboys, mirror cabinets over 22 kg, large mirrors, cutters 95 cm and up, Kera Cut/Lift, Baron mixers, linear drains 1200 mm+ |

156 live variants are in "Local delivery or pickup - large items" but fit Australia Post: basins, kitchen sinks, mirrors, grout, niche boxes, floor wastes, freestanding bath mixers/spouts and small tile cutters. These can be sold Australia-wide once they move to a parcel shipping profile. Ceramic and glass items are marked fragile.

3 m trims are light (under 4 kg) but too long for Australia Post, so they need a courier that takes long parcels. Until then they are Perth delivery or pickup.

## Status
Weights have been entered in Shopify for 550 variants (141 products). The other 1,141 are still to be entered. Weights do not change what customers pay until calculated shipping rates are turned on.
