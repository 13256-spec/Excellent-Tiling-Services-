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

## Fix 5 Oct 2026 (afternoon): interstate checkout had no shipping option
Earlier today free shipping over $100 was made WA-only. That left the General profile's "Rest of Australia" zone (ACT, NSW, NT, QLD, SA, TAS, VIC) with only the Australia Post live rate, which returns nothing at checkout on the Basic plan. So **any cart with a small item going outside WA could not check out.**

Owner's rule from today: **free delivery only on orders of $1,000 or more**, everywhere. Small-item delivery should stay reasonable.

General profile (small items) now:

| Zone | Rate | Condition |
| --- | --- | --- |
| Western Australia | Standard shipping $20 | order $0 to $999.99 |
| Western Australia | Free shipping (orders $1000+) | order $1,000+ |
| Rest of Australia | Australia Post tracked parcel $20 | up to 2.99 kg |
| Rest of Australia | Australia Post tracked parcel $30 | 3 to 4.99 kg |
| Rest of Australia | Australia Post tracked parcel $45 | 5 to 9.99 kg |
| Rest of Australia | Australia Post tracked parcel $69 | 10 to 22 kg |
| Rest of Australia | Australia Post tracked parcels (2 boxes) $119 | 22.01 to 44 kg |
| Rest of Australia | Australia Post tracked parcels (3-4 boxes) $199 | 44.01 to 100 kg |
| Rest of Australia | Free shipping (orders $1000+) | order $1,000+ |

The Australia Post live rate (+$3 fee) is still on in Rest of Australia. It shows nothing on the Basic plan, but it will appear next to the fixed prices if live checkout rates are ever enabled.

Unchanged: the bulky-items profile (Australia Post $25 to $179 by weight, no free shipping), and large items (pickup or Perth local delivery only). A mixed cart pays the small-item rate plus the bulky-item rate.

**Still to do:** the theme and SEO text says "free shipping over $100" in about 20 places (header bar, homepage, FAQs, product perks, delivery page, collection SEO text, shipping policy, "Finish it right" campaign graphics). It needs changing to the $1,000 rule.

## International shipping live (5 Oct 2026)
The draft market **"International – Phase 1"** (NZ, US, UK, UAE) was switched to **Active**. Prices are in AUD. Australian GST is taken off at checkout (exports are GST-free), and the customer pays any import duties or taxes on delivery.

**Small items only** (General profile). Bulky items (basins, mirrors) and large items (tiles, vanities, baths) have no international rate, so overseas customers can't check out with them. They need to contact the shop for a quote.

Sent with the owner's MyPost Business account (Australia Post International, tracked). Create the label from the order as for domestic orders, and fill in the customs description and value on the label.

| Packed weight | New Zealand | US, UK, UAE |
| --- | --- | --- |
| up to 0.99 kg | $35 | $55 |
| 1 to 1.99 kg | $49 | $85 |
| 2 to 4.99 kg | $85 | $159 |
| 5 to 10 kg | $149 | $279 |

Over 10 kg: no rate, contact the shop. No free international shipping.

Check the first few real labels against these prices and adjust if Australia Post costs more. To add a country: add it to the market (Settings → Markets) and to one of the two international zones in the General profile.

## Live Australia Post rates removed from checkout (5 Oct 2026, evening)
The live Australia Post rate started showing at checkout next to the fixed prices. It used the default "Tile box 60x45x30", so a Brisbane (4069) order showed Parcel Post $105.05 and Express $371.95 next to the fixed $45. The carrier rate was deleted from the General profile (Rest of Australia) and from the bulky-items profile. Checkout now shows only the fixed prices. Labels still come from the MyPost Business carrier account, which is a separate setting. Make the 30x25x20 small box the default package so label prices are right.

## Same rates for WA, free over $1,000 everywhere, wording updated (5 Oct 2026, night)
- **WA zone** now uses the same weight prices as the rest of Australia ($20 / $30 / $45 / $69 / $119 / $199), free from $1,000. The old $20 flat rate is gone.
- **Bulky items profile** also got "Free shipping (orders $1000+)", so "free over $1,000" is true for basins and mirrors too. Shopify checks the price condition on the items in each profile, so a mixed cart only gets free shipping on a profile whose items alone total $1,000+.
- **Theme wording** ("free over $100" → "from $20, free over $1,000", "no international" → NZ/US/UK/UAE small items) was uploaded to the unpublished theme "ETS 2026 – Restored (5 Oct)" (header bar, trust strip, homepage cards and FAQ, delivery page, FAQs page, trade FAQ, product perks, product page FAQ, collection ticker). It goes live when the owner publishes that theme.
- **Live store data updated directly:** SEO descriptions of 66 products and 9 collections, the descriptions of 5 tapware collections, and the Delivery & Pickup and FAQs page bodies.
- **Shipping policy:** the app has no `write_legal_policies` access, so the new text is in `store-content/policies/shipping-policy.html`. Paste it in at Settings → Policies → Shipping policy.
- Not changed: the "Finish it right" campaign graphics still say "free shipping over $100 (WA)". They need redoing before they're posted.

## International prices lowered (5 Oct 2026, late)
A UK test cart (2 pull-out sink mixers, 3 kg each = 6 kg) was charged A$279 (£150) by the old 5–10 kg band. The international bands were too padded and too coarse, so they now go up in smaller steps:

| Packed weight | New Zealand | US, UK, UAE |
| --- | --- | --- |
| up to 0.99 kg | $29 | $45 |
| 1 to 1.99 kg | $39 | $65 |
| 2 to 2.99 kg | $49 | $85 |
| 3 to 4.99 kg | $65 | $119 |
| 5 to 6.99 kg | $85 | $149 |
| 7 to 10 kg | $109 | $189 |

The same 6 kg UK cart now pays A$149 (~£75). Check the first real international labels against these prices.

Shipping weights for tapware are estimates (kitchen mixers 2.4–3 kg). Weighing a packed pull-out mixer would let checkout use the real weight.

The theme (now published as "ETS 2026 – Restored (5 Oct)") still says "from $35" for international in two places: the delivery page "Where we deliver" panel (`sections/ets-standard-page.liquid`) and the delivery FAQ (`templates/page.delivery.json`). The repo copies say "from $29", but theme writes to the live theme are blocked. Fix in the theme editor (Delivery page FAQ) or through a draft copy of the theme. The Delivery & Pickup page body and the shipping policy text already say $29.
