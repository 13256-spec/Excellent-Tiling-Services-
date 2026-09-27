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

## Shipping profile: free shipping on small items (26 Sep 2026, updated 27 Sep 2026)

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
- Costs are unknown (need the logged-in Roberts price list). Fill `our_cost` in `roberts-designs-pricing.csv` or send the price list, then check margin before activating anything.

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

The two new collections are **not yet published** to the Online Store. Publish them and add them to the menu once the Roberts products go live.
