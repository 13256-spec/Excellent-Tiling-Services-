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
- `in_shopify`: whether the weight has been entered on the Shopify variant.

## Summary (live variants)
| Ship by | Variants | What |
| --- | --- | --- |
| auspost | 956 | tapware, accessories, silicone, grout up to 10 kg, tools, spacers, blades, basins, sinks up to 770 mm, most mirrors, tile cutters up to 84 cm, 1 m trims, linear drains up to 900 mm |
| freight | 583 | 3 m and 2.5 m trims, tiles, vanities, baths, toilets, shower screens, tallboys, mirror cabinets over 22 kg, large mirrors, cutters 95 cm and up, Kera Cut/Lift, Baron mixers, linear drains 1200 mm+ |

156 live variants are in "Local delivery or pickup - large items" but fit Australia Post: basins, kitchen sinks, mirrors, grout, niche boxes, floor wastes, freestanding bath mixers/spouts and small tile cutters. These can be sold Australia-wide once they move to a parcel shipping profile. Ceramic and glass items are marked fragile.

3 m trims are light (under 4 kg) but too long for Australia Post, so they need a courier that takes long parcels. Until then they are Perth delivery or pickup.

## Status
Weights are entered in Shopify for all 1,691 variants (checked against a fresh Shopify export on 28 Sep 2026: all match). They don't change what customers pay until calculated shipping rates are turned on.

## Australia Post parcels profile (28 Sep 2026)
New delivery profile **"Australia Post parcels - bulky items"** (gid://shopify/DeliveryProfile/94542069823), zone Australia (all states), rate = live Australia Post MyPost Business prices from the connected account, all services, no handling fee.

184 variants (156 live) moved into it from "Local delivery or pickup - large items": basins, kitchen sinks, mirrors, LED mirrors, small mirror cabinets, grout, niche boxes, floor wastes and linear drains up to 900 mm, freestanding bath mixers/spouts, tile cutters up to 84 cm and small Sigma parts. Pickup and Perth local delivery still apply (they are set on the location).

Small items stay in the General profile ($20 under $100, free from $100). A mixed cart pays both: the small-item rate plus the Australia Post price for the bulky item.

Parcel Post and Express Post were switched on for this rate on 28 Sep 2026 (the rate had no services selected).

### Storefront test (28 Sep 2026, cart shipping-rate lookup)
| Cart | Address | Rates returned |
| --- | --- | --- |
| Silicone $17.40 | Maddington 6109 | Standard $20, Local Delivery $130 |
| Basin mixer $259 | Sydney 2000 | Free shipping |
| Basin $315 | Sydney 2000 / Darwin 0800 | none |
| Basin $315 | Maddington 6109 | Local Delivery $130 |
| Silicone + basin | Melbourne 3000 | none |

Australia Post returns no rates for any item in the profile, even a 0.35 kg primer, so the cause is the account setup, not the weights. The likely causes are no default package in Shopify, or a MyPost Business connection that isn't finished. Until that's fixed, these items still sell as pickup or Perth delivery only, the same as before the move.

Update, same day: the owner set a $100 minimum on both local delivery zones (30 km $130, 50 km $180) and made "Tile box 60x45x30" (0.5 kg) the default package. They also connected their own MyPost Business account, which Shopify added as a new carrier service ("Australia Post MyPost Business (own account)"). The profile's rate was moved to that service, with Parcel Post and Express Post on.

Retest: the $17.40 cart now shows only Standard $20. Australia Post still returns no rates for any item in the profile. Check that rate calculation is turned on for the Australia Post carrier account in Shopify admin (Carrier accounts → Australia Post → Calculate rates).

## Backup Australia Post prices (28 Sep 2026)
Australia Post live rates still return nothing, so the "Australia Post parcels - bulky items" profile now also has fixed prices by cart weight (bulky items only, Australia-wide):

| Weight of bulky items in cart | Price |
| --- | --- |
| up to 2.99 kg | $25 |
| 3 to 4.99 kg | $39 |
| 5 to 9.99 kg | $79 |
| 10 to 22 kg | $99 |
| 22.01 to 44 kg (2-3 boxes) | $179 |

These items are light but bulky: a basin weighs about 8 kg, but its box is charged by Australia Post as 15 to 26 kg (cubic weight). So the prices are set to cover the cubic charge to far zones such as Darwin. Over 44 kg there is no rate, and the customer has to contact the shop.

When Australia Post live rates start working, customers will see both. Then delete these five fixed rates, or keep them and remove the live rate.

Retest after adding them (cart shipping-rate lookup):
| Cart | Address | Rates |
| --- | --- | --- |
| Silicone $17.40 | Maddington 6109 | Standard $20 |
| Basin mixer $259 | Sydney 2000 | Free |
| Basin 8.3 kg | Sydney 2000 / Darwin 0800 | Australia Post $79 |
| Basin 8.3 kg | Maddington 6109 | Australia Post $79, Local Delivery $130 |
| Silicone + basin | Melbourne 3000 | $79 |
| Primer 0.35 kg | Sydney 2000 | Australia Post $25 |
| 3 basins | Brisbane 4000 | Australia Post $179 |
| Vanity (freight item) | Sydney 2000 | none (pickup / Perth delivery only) |

## Update 5 Oct 2026
- **Labels work.** The owner's MyPost Business account is connected in Shopify (Carrier accounts → Australia Post). From an order, **Create shipping label** shows live Parcel Post and Express Post prices from that account. Postage is billed to MyPost Business, and tracking is emailed to the customer automatically.
- **Use the right box.** The first label for order #1001 (6 small items, 4.65 kg, Perth → Brisbane) quoted Parcel Post at $102.05 and Express Post at $368.95. That was because it used the default "Tile box 60x45x30", which Australia Post charges as 20.25 kg cubic weight. The owner added and saved a **30x25x20 small box** (0.1 kg empty, 3.75 kg cubic) for small orders. Next step: make it the default package (Settings → Shipping and delivery → Saved packages), so labels don't start from the tile box.
- **Checkout still shows the fixed backup prices only.** Retest (cart shipping-rate lookup): MELA ARCH basin to Sydney 2000 and to Brisbane 4069 both returned only "Australia Post tracked parcel $79". Live Australia Post prices work for labels but not at checkout. On the Basic plan, carrier-calculated rates at checkout usually need a paid add-on or a higher plan. Keep the fixed weight prices until then.
- Order #1001's $0 shipping is correct: it's over $100, so it got the General profile's free-shipping rate.
