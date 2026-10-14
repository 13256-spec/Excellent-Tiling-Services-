# Supplier sync – 26 Sep 2026

Sources: eternitytiles.com.au (tiles) and bathroom-city.com.au (MELA), read from their public Shopify product feeds.

## Applied
- 45 tile variants: Eternity product code set as SKU
- Morgan Hail (3 photos) and Cement White (1 photo) from Eternity
- Time Stone Charcoal: removed 300x600 Lappato and 600x600 Matt (not offered by Eternity)
- 7 MELA variants: SKU from Bathroom City (toilet suites, BRITTANY 600/1200)
- Photos: SURI Framed Round Mirror (9), DEBBA Half Inset Basin (1), TRITON 770 Double Sink (1)
- 71 product descriptions: removed 'Catalogue RRP', 'from the 2025 MELA catalogue' and internal staff notes

## Needs a decision – our price is below Eternity's listed price

| Tile | Size / finish | Ours | Eternity |
| --- | --- | --- | --- |
| Time Stone Moon Porcelain Tile | 300x600mm / Lappato | $59.00 | $65.00 |
| Time Stone Moon Porcelain Tile | 600x600mm / Lappato | $59.00 | $65.00 |
| Time Stone Cinder Porcelain Tile | 300x600mm / Lappato | $59.00 | $65.00 |
| Time Stone Cinder Porcelain Tile | 600x600mm / Lappato | $59.00 | $65.00 |
| Lava Etna Porcelain Tile | 300x600mm / Gloss | $55.00 | $59.00 |
| Lava Etna Porcelain Tile | 600x600mm / Gloss | $55.00 | $59.00 |
| Lava Ash Porcelain Tile | 300x600mm / Gloss | $55.00 | $59.00 |
| Lava Ash Porcelain Tile | 600x600mm / Gloss | $55.00 | $59.00 |
| Lava Kraka Porcelain Tile | 300x600mm / Gloss | $55.00 | $59.00 |
| Lava Kraka Porcelain Tile | 600x600mm / Gloss | $55.00 | $59.00 |
| Cement White Porcelain Tile | 600x1200mm / Matt | $44.00 | $59.00 |
| Cement Grey Porcelain Tile | 600x1200mm / Matt | $44.00 | $59.00 |

## Sizes Eternity offers that we don't list

| Tile | Variant | Code | Price |
| --- | --- | --- | --- |
| Morgan Cloud Porcelain Tile | Morgan Cloud / 300x300x9.5 / Matt | ETA33AK666 | $50.00 |
| Morgan Cloud Porcelain Tile | Morgan Cloud / 300x600x9.5 / Matt | ET36AK662 | $44.00 |
| Cement White Porcelain Tile | Cement White / 300x600x9.5 / Matt | ET36MQ01 | $44.00 |

## Shipping profile: free shipping on small items (26 Sep 2026, superseded)

> **Superseded.** As of 1 Oct 2026 this profile no longer exists. Shipping is now: General profile (small items) $20 flat, free on orders $100+; "Australia Post parcels - bulky items" by weight; "Local delivery or pickup - large items" for tiles, baths, toilets, vanities and screens. See `store-content/policies/shipping-policy.html`.

Delivery profile "Free shipping - small bathroom items" (gid://shopify/DeliveryProfile/94502682687): Australia-wide, $0, 384 variants from Maddington.
Included product types: tapware (basin/wall/sink mixers, spouts), shower heads, arms, sets, hoses, towel rails, hooks, holders, shelves, wastes, shower screen fittings (except the 2000 mm U channel).
Everything else stays in the General profile with no delivery rate (pickup or quote). New small products must be added to this profile in Settings > Shipping and delivery.

### Update 27 Sep 2026: $100 minimum for free shipping
Small items now sit in the General profile (gid://shopify/DeliveryProfile/94347526207), zone Australia, with two rates:
- "Free shipping (orders $100+)": $0 when the order subtotal is $100.00 or more
- "Standard shipping": $20 flat when the order subtotal is $0.00 to $99.99
Large items are in "Local delivery or pickup - large items" (pickup or quote).

## Trade pricing tiers (27 Sep 2026)
Trade customers (customer tag `trade`, segment "Trade customers") get an automatic discount set by a product tag:

| Product tag | Collection | Discount | Products |
| --- | --- | --- | --- |
| `trade-5` | Trade – 5% | 5% | 230 |
| `trade-10` | Trade – 10% | 10% | 11 |
| `trade-15` | Trade – 15% | 15% | 0 |

Only products with a unit cost in Shopify and at least 35% margin are on `trade-10` (MELA FLOVA/PALCO/RONDO tapware and accessories, Roberts pocket knife). Everything else has no cost entered, so it stays on `trade-5` until a cost is added. Products with no trade tag get no trade discount. Trade discounts don't combine with other product or order discounts.

## Roberts Designs import (27 Sep 2026)
264 Roberts Designs products (935 variants) added to Shopify as **drafts**, vendor "Roberts Designs", tags `supplier-import` and `needs-cost`. Nothing is visible to customers until a product is set to Active.

- Source: public product feed on robertsdesigns.com.au (names, options, SKUs, photos, specs). Carton quantities and "min buy" notes were removed from descriptions.
- Skipped: Pocket Folding Knife box of 6 and Turbo Diamond Blades (already in the store as drafts), plus 10 spare parts and 64 option combinations that Roberts lists without a price.
- Price = 3% below the lowest market price found, rounded to .95:
  - `web:` 12 flagship items checked by hand online (Sigma cutters, Kera Cut, Kera Lift, Baron E120). Market is 52–72% of the Roberts list price for these.
  - `match:` 140 variants matched to Tile Mart, Port Kembla Tiles, Western Distributors or Builders Centre listings.
  - `roberts-list`: everything else is priced 3% under the public Roberts price. Tile Mart sells at about Roberts +4%, so this is at or below common retail but may be above discount shops.
- `price-check` tag: items where the Roberts data or market looked unreliable (Baron F200/F300 and parts, Sigma parts and workbench, one linear drain, tile wedges, cylinder gun).
- Shipping: 77 bulky products (3m trims, tile cutters, Kera/Sigma tables, Baron mixers, linear drains, niche boxes, grout 5kg+, pallet wrap, floor protection roll) moved to "Local delivery or pickup - large items". The rest stay in the General profile ($20 under $100, free over $100).
- No trade tag yet, so trade customers get no discount on these until a tier is chosen.
- Costs were added on 28 Sep 2026 (see below).

### Collections for the Roberts Designs products

The existing Hardware smart collections now also match on **product type**, so Roberts products (and future imports that use the same types) sort themselves automatically:

| Collection | Matches | Products |
|---|---|---|
| Hardware | tag `Hardware` + every Roberts tool, blade, spacer, sealant, cutter and trim type | 253 |
| Trowels & Tiling Tools | existing tags + Tiling Tools, Mixers, Sponges and Grouting Systems, Brushes and Rollers, Packaging, protection mats | 85 |
| Diamond Blades & Drill Bits | existing tags + Drill Bits, Diamond Blades, Grinding Wheels and Polishing Pads | 15 |
| Tile Spacers & Wedges | tag + Tile Spacers, Tile Leveling Systems | 24 |
| Silicone, Additives & Cleaners | existing tags + Silicone Sealants/Accessories, Hybrid Sealants, Adhesives, Grout | 30 |
| **Tile Trims & Edging** (new, `tile-trims-edging`) | the 15 trim product types | 33 |
| **Tile Cutters & Accessories** (new, `tile-cutters-accessories`) | type Tile Cutters | 67 |

The bathroom items were added by hand to the manual collections: Bathroom Wastes (floor wastes, linear drains and flanges, +15), Soap & Shelf Holders (+7), and Accessories (niche boxes and a vent, +4).

Both collections were published on 28 Sep 2026 (see below).

## Roberts Designs costs and go-live (28 Sep 2026)

Cost prices were taken from our logged-in trade account on robertsdesigns.com.au, which shows prices **ex GST** (a $9.00 item adds $0.90 GST in the cart). All 935 variants matched by SKU.

- `our_cost` = Roberts trade price ex GST. This is also the unit cost on every Shopify variant.
- `margin_pct` = (our price ÷ 1.1 − cost) ÷ (our price ÷ 1.1). Shopify prices include GST, so GST is taken off the sale price first. Shopify's own margin figure ignores GST and will show about 9 points higher.
- Median margin is 41.9%.
- `needs-cost` tag removed from all 264 products.
- Baron E120 (RDXM50030): the sheet showed $6,371.95, but Shopify had $4,557.95 (3% under CeramicsWest). The sheet now shows the Shopify price.

### Under 20% margin
37 variants were under 20%. The target price was cost ÷ 0.8 + GST, rounded up to .95. It was only raised where that stayed at or under `market_price_used`:

| SKU | Product | Old | New |
| --- | --- | --- | --- |
| RDXA3519 | Sigma 24M10X Handle | $309.95 | $314.95 |
| RDXA3539 | Sigma 24M20X Handle | $309.95 | $314.95 |

For the other 35 the new price would be above market, so these **36 products stay as drafts** (listed with the current margin):

- **Cost equals the Roberts list price (no trade discount):** Baron F200 and F300 mixers and their heads, paddles, switches and rubber wheel (−13 to −14%), E120 power cable (−13.9%), Sigma 90D3/90DG/90LD/90LE measurement bars, 19B3 square, 14C scoring wheel and 108362 nut (−13 to −15%), and Tile Insert Linear Drain 76mm (the 1500mm Gold variant is at −13.6%, so the whole product stays in draft). Worth asking Roberts whether these should carry a trade discount.
- **Sigma cutters priced to the online market:** ART 2G, 2B3, 7F, 4BU, 4CU, 4DU, 4EN, 4FN, NEX 4BN/4CN/4DN, Kera Cut kit 8AE2 and Kera Lift 1A6 (−18% to 12.6%). Discount sellers are close to our cost.
- **Small items:** Maxisil Sausage Caulking Gun 600ml (10.4%), Splash Trowel (14.8%), Waterproofing Kit (13.1%), White Rubber Mallet (−14.9%), and Stainless Square Notched Maxi Grip Trowel – Large (the 12mm variant is at −0.3%).

### Status
- **228 products Active** and published to Online Store, Point of Sale, Shop, Google & YouTube and Facebook & Instagram. Every variant on these is at 20% margin or more.
- `price-check` items: 30 went live because their cost is below the Roberts list and margin is 20% or more. 10 stay as drafts (all in the lists above).
- Tile Trims & Edging and Tile Cutters & Accessories are published to all channels and added under **Hardware** in the main menu.
- Roberts pocket knife (ETS-HW-005) was not in this sheet and was left as it was.

## Roberts Designs costs corrected for GST (14 Oct 2026)

The owner confirmed the Roberts Designs trade-account prices recorded as cost on 28 Sep did not include GST. Every unit cost on the 715 variants with vendor **Roberts Designs** (including the pocket knife ETS-HW-005) was multiplied by 1.1. The other brands bought through Roberts (Maxisil, Sigma, Siri, Baron, Barwalt: 205 variants) were left at their 28 Sep cost on the owner's instruction. Selling prices were not changed: the owner's call is that prices follow the market, not the cost.

- `roberts-designs-pricing.csv`: `our_cost` x 1.1 on the Roberts Designs rows, `our_price` refreshed to the live price on every row, `margin_pct` recomputed.
- `../pricing/store-pricing-2026-10-03.csv`: cost, price and margins refreshed on the 694 Roberts Designs rows (`cost_src` says so); the other Roberts-supplied brands had their price and margins refreshed only.
- 48 Roberts Designs variants are now under the 25% profit floor (cost x 1.1 x 1.25), between 12.0% and 19.1% margin. They are listed worst-first in `../pricing/reports/roberts-gst-below-floor-2026-10-14.csv` for the owner to decide. Nothing was repriced.

## DSA bathroomware from Eternity (14 Oct 2026)

Everything Eternity lists under vendor "DSA" that is not a tile (the tiles were already in the store):
62 products / 111 variants added, tagged `supplier-import` + `needs-cost`, published to all six sales channels.
Created as drafts, then set **Active on 14 Oct 2026** on the owner's instruction: sell at Eternity's price until DSA
sends a trade price list. The list of items to ask for is `store-content/pricing/DSA-trade-price-request-2026-10-14.xlsx`
(and `.txt` for pasting into an email); once it comes back, price by the playbook and remove `needs-cost`.

- Range: Celine tapware, showers and accessories (26), Chloe showers (4), Malaga wall hung vanities,
  cubby/single door cabinets and kickboards (10), Caden and Callan kitchen sinks (6), Cosimo/Olivia/Ria/Mezo/Cube
  basins (9), Capsule and Eclipse LED mirrors (2), Crystal smart toilet (1), floor wastes, pop up wastes and a
  bottle trap (7). Two zero-price "installation accessory" entries on Eternity's site were skipped.
- **Price = Eternity's listed retail price, no cost recorded.** There is no DSA cost sheet yet, so the playbook
  floor can't be checked; the owner needs DSA trade costs before these are priced (and before a trade band or
  `trade-list-N` collection is chosen). Drafts until then.
- Supplier name hidden (owner rule): vendor "Excellent Tiling Services", `custom.supplier` = "Eternity Tiles",
  "Eternity Range" stripped from the Malaga titles. Typos fixed (Pup Up, Chole, Towel Tail, Divertor).
- Options cleaned: Eternity's "Size: See Diagram" and "Default Title" colour values dropped; finish option is
  `Finish` (Chrome / Brushed Nickel), Malaga sizes are 600/750/900/1200mm (full dimensions in the description).
- Photos: Eternity's own product photos (some are size diagrams). Descriptions: Eternity's text where it had any,
  otherwise one plain line per product type.
- Delivery: vanities, cabinets, kickboards and the toilet on "Perth only (local delivery / pickup)"
  (`ship-local-only`); everything else General profile (`ship-parcel` / `ship-bulky`), same as the MELA equivalents.
- Collections: added to the manual department collections (tapware, basins, mirrors, sinks, towel rails,
  bathroom wastes, bathroom vanities...). Two new product types were added to the menu smart collections:
  "Wall Hung Basin" and "Vanity Kickboard" to Vanities & Basins, "Bottle Trap" to Mirrors & Accessories.
- Files: `dsa_bathroomware_2026_10.py` (feed -> productSet inputs), `dsa-eternity-feed-2026-10-14.json` (Eternity's
  feed that day), `dsa-bathroomware-2026-10-14.json` (what was sent), `dsa-bathroomware-created-2026-10-14.json`
  (Shopify product and variant ids per source handle).
