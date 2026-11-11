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

**15 Oct 2026:** the owner said Maxisil costs were also ex GST. The 120 Maxisil variants in Shopify now carry cost x 1.1 as well; Sigma, Siri, Baron and Barwalt are still at their 28 Sep cost.

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

## Roberts Designs costs refreshed from the trade account (23 Oct 2026)

The owner asked for the Roberts Designs trade prices to be recorded as Shopify unit cost with GST added. All 935 variants bought through Roberts (vendors Roberts Designs, Maxisil, Sigma, Siri, Baron, Barwalt) were checked against the logged-in trade price on robertsdesigns.com.au on 23 Oct. Unit cost = trade price (ex GST) x 1.1.

- 834 variants were already right (Roberts Designs and Maxisil, done 14-15 Oct).
- 100 variants updated in Shopify, listed in `../pricing/reports/roberts-cost-update-2026-10-23.csv`:
  - 73 were still at the 28 Sep ex-GST figure (Sigma, Siri, Baron, Barwalt): cost x 1.1.
  - 13 where Roberts now shows a trade discount that it did not in September (Sigma Kera-Cut parts, bench hooks, extension bars, 24N handle, two flanges, a cove joiner): cost went down 45-50%.
  - 13 where Roberts now charges full list with no trade discount (Baron F200/F300 mixers, heads, switches and wheel; Sigma 90D3/90LD/90LE bars, 19B3 square, 14C wheel; Tile Insert Linear Drain 76mm 1500mm): cost roughly doubled.
  - RDXT630 Siri Eco Roller Wash Up Bucket is no longer on the Roberts site; its 28 Sep ex-GST cost was multiplied by 1.1.
- ETS-HW-005 pocket knife was already at the box-of-6 trade price / 6 x 1.1 and was left alone.
- Selling prices were not changed. `../pricing/reports/roberts-below-floor-2026-10-23.csv` lists the 19 variants now under the playbook floor (cost inc GST x 1.25, i.e. 20% margin ex GST); 13 of them sell below cost, all Baron and Sigma items in the no-trade-discount group above plus the 1500mm linear drain. The owner should confirm with Roberts whether these carry a trade discount, or reprice them.
- `roberts-designs-pricing.csv` and `../pricing/store-pricing-2026-10-03.csv`: cost and margins refreshed on the changed rows.

## DSA toilet collection (26 Oct 2026)

Ten toilet products created live from Eternity's product sheets (`dsa_toilets_2026_10.py` -> `dsa-toilets-2026-10-26.json`,
images in `dsa-toilet-sheets/`), and the Crystal smart toilet renamed Crystal Elite with SKU DSAYC318GE. Price = RRP, cost =
estimate (RRP x 0.5, tag `cost-estimate`). Details in the main README under "DSA toilet collection".
Facts worth knowing: the two sheets disagree on the Crystal Prime and Nova heights (brochure: Prime 460 mm, Nova 440 mm;
the shared spec table says the reverse). The brochure figures are on the product pages. The Eternal Element, Clarice and
Edna Care sheets give no WELS figure, so none is claimed for them.


## RLA Polymers range (28 Oct 2026, live)

New supplier, trade account pending. Every product from the two printed catalogues the supplier gave the owner,
**RLA Tiling Product Range 2026 (V2)** and the **Gripset Waterproofing Product Guide (V3)**, is now in Shopify:
69 products / 165 variants, vendor "RLA", tags `RLA`, `supplier-import`, `needs-cost`, `rla-2026-10`
(plus `Gripset` on the 32 Gripset items). Created as drafts, then set **Active on 29 Oct 2026** on the owner's
instruction, **visible but not purchasable**: stock is 0 at Maddington and every variant is set to stop selling when
out of stock, so the pages show as sold out / Enquire until RLA costs and stock arrive (then set stock or switch the
variants to "continue selling").
Script: `rla_2026_10.py` (catalogue data -> productSet inputs). Sent payload: `rla-2026-10-28.json`.
Shopify ids per product and variant: `rla-created-2026-10-28.json`. Price research: `rla-market-prices-2026-10-28.csv`.

- Range: RLA powder adhesives (TileBond Extra, MoreFlex, TileFlex, AddFlextra, Trade Mastik, Mastik, UniLite S1/S2,
  UniGrip, FastSet, StoneSet, PolyMastic), membranes (WPU, WPM, Safe2o, 2Part, 1Komponent, PU850, ATC, Moisture Seal,
  Primer PU), Max SMP 25, waterproof tape, corners and collars, Luminous EF (16 colours), Luminous SSG (12 colours x
  4/10 kg), Luminous Silicone (13 colours), Epoxy Grout (4 colours), The Once Over, Porous and Non-Porous Primer,
  Plastinex, Silikon 700 (14 colours), caulking guns, dry and wet area acoustic adhesives; Gripset E60, GP, OP, 11Y,
  Elastoproof B50 band, corners (sold each) and collar packs, BRW PF tape and square, 38FC, P39, LS, 51, Xpress Primer
  H2O Plus, Xpress Multi Pro, XpressLay, 2P, C-1P, C-Bed, C-Level, C-Plug, Butyl HD tape, BRW HD, BRW PFN, BRW FG tape,
  C-Lite, C-Mastic, C-Stone, C-Rubber, B26 and B09.
- Not created: RLA QuickSet (already in the store), the Gripset Enviro crack sealing machine, and Xpress SP / 30SC
  (not in the printed guide). The RLA **Sealants** catalogue (Silikon 100-600, Flex-Pro, FirePro, UltraGrip, Max Grab,
  Max SMP Crystal) is in the script behind `INCLUDE_SEALANTS_CATALOGUE = False` because it is not one of the two
  catalogues the owner was given; flip it and rerun if RLA supplies those too.
- Codes come from the printed catalogues, which differ from rlapolymers.com.au in places: Luminous Silicone uses the
  6107xx codes, Luminous SSG is `LUMSSG02-4` (not `-04`), The Once Over is 506210, C-Level is GWS209 and C-Rubber
  GWS157 (the Gripset PDF has typos), Silikon 700 is a 300 g cartridge. Max SMP 25 colour codes are "TBC" in the
  catalogue, so the website 6205xx codes are used. ATC has no code in either source (`RLA-ATC-15` placeholder).
- **Price = a little under the common AU retail price (no cost yet).** Method per variant in the `market` column of
  the CSV: 5% under B&B Hardware where they list the item, otherwise just under the lowest of TradieCart, Adheseal
  (ex GST x 1.1), Tilers Direct, Beaumont, Tile Mart, Bunnings. 20 products / 26 variants carry `price-check`: no
  listing found, or only Beaumont (who run well above trade shops). No cost, no margin check, no trade band
  (`ets.trade_band` = 0). When the RLA trade price list arrives: enter costs, run the playbook floor
  (cost x 1.1 x 1.25), pick a trade band, remove `needs-cost` and `price-check`.
- Content: full description (intro, uses, colours, specs, good-to-know, TDS and SDS links), SEO title and description,
  one or two product photos (RLA and Gripset press shots, catalogue crops for the accessories; `needs-photo` on the
  wet area acoustic adhesive), alt text, Shopify taxonomy category, `ets.*` metafields (supplier "RLA Polymers",
  material, range, warranty, freight_class, lead_time, trade_band) and `custom.supplier`, so the theme's product
  JSON-LD renders as for the rest of the store.
- Delivery: 55 variants (20 kg bags, 15 L pails, kits, sheet rolls) on "Perth only (local delivery / pickup)"
  (`ship-local-only`); PU850, ATC and Primer PU (solvent based) on "Dangerous goods (road only)"
  (`ship-dangerous-goods`); the rest General (`ship-parcel` / `ship-bulky`, eBay tags `ebay-post-15/20/39`).
- Channels: published to all six (Online Store, POS, Shop, Google & YouTube, Facebook & Instagram, Inbox).
- Collections: new product types "Waterproofing Membranes", "Waterproofing Accessories" and "Screeds & Levellers".
  The **Waterproofing** smart collection (303308341311) now matches *any of*: type "Waterproofing Tools", tag
  `Waterproofing`, or the two new waterproofing types (it only matched the tools type before). Adhesives, grout and
  sealants fall into Tile Adhesive, Grout and Silicone & Sealants through the existing type/tag rules; everything
  is in Hardware via the `Hardware` tag.
- Photos are in Shopify Files, not the repo (98 files, 22 MB).

## Eternity flash drive sync (10 Nov 2026)

The owner's external drive (`D:\Eternity`) holds everything Eternity has sent: the 26 Oct Drive material plus Caliza, Ceramic,
Lava, Time Stone and Terrazzo Lumina photo folders dated 9-10 Nov. Applied live: 26 supplier photos on 14 tiles, the two generated
swatches (Lava Vesuv, Caliza) replaced with real photos, Time Stone Sand published with photos, Cement featured images fixed, and
five unpriced basins created as drafts (`price-check`). Documents copied to `Eternity/`. Details, file map and the list of what
still needs a price or a photo: `drive-eternity-2026-11-10/README.md`.

## ARDEX Australia range (11 Nov 2026, live, price on request)

Owner's instruction: "add all Ardex materials to our website ... live SEO pages and all categories and catalogues ...
not available to sell, out of stock for now". There is no ARDEX account, price list or catalogue PDF yet, so the whole
range was taken from ARDEX Australia's own website (every product in its `product` sitemap except the training-event
tickets and two empty draft pages): **206 products / 361 variants**, vendor "ARDEX", tags `ARDEX`, `ardex-2026-11`,
`supplier-import`, `needs-cost`, `price-check`, plus one `ardex-<group>` tag each (adhesives, grouts, waterproofing,
levelling, primers, sealants, concrete-repair, civil, render, flooring-adhesives, tools, wedi).

- **Status: Active.** Shopify's "publish new products automatically" setting put them on **Online Store, Point of Sale,
  Shop and Microsoft Copilot** (not Google & YouTube, Facebook or Inbox). The API tool refuses to unpublish, so the owner
  should take them off POS, Shop and Copilot until they have a price: Products → filter tag `ardex-2026-11` → select all →
  More actions → Manage sales channels → untick those three. **Price 0.00 on every variant**, inventory tracked, 0 at
  Maddington, "stop selling when out of stock", so every page shows **Sold out / Enquire** and cannot be bought. The draft
  theme "ETS 2026 – Price on request" shows "Price on request" instead of $0.00 (root README); the one $0 left on an
  all-ARDEX collection page is Horizon's price filter ("The highest price is $0.00"), which fixes itself once prices exist.
  Trade band 0.
- **Content**: ARDEX's own product text, key features, technical data (location, coverage, pack sizes, drying times),
  links to the ARDEX technical and safety data sheets, ARDEX product photos (fetched straight from ardexaustralia.com)
  and the ARDEX YouTube videos where a product has them. SEO title and description on every product, `ets.*` metafields
  (supplier "ARDEX Australia", material, range, warranty, freight class, lead time, trade band) and `custom.supplier`.
- **Variants**: pack sizes as a Size option (20kg bag, 5L, 310ml cartridge...). Grouts carry the ARDEX colour chart as a
  Colour option: FG 8 20 colours x 1.5/5/20kg (52 variants; Macchiato, Pewter Blue, Sandalwood and Mocha in 5kg only),
  FS-DD 11 colours (1.5kg and 20kg in Ultra White only), WJ 50 6 colours, EG 15 8 colours. wedi items use wedi's own
  article numbers as SKU; every other SKU is a placeholder `ARDEX-<product>-<size>` until the ARDEX price list gives the
  real codes.
- **Delivery**: 20kg bags, pails, rolls, boards and shower bases on "Perth only (local delivery / pickup)"
  (`ship-local-only`); solvent-based primers and PU resins (WPM 240, WPM 270, WA 98 adhesive and solvent, CE 300, CE 330)
  on "Dangerous goods (road only)"; the rest General (`ship-parcel` / `ship-bulky`). Weights from the pack size.
- **Collections** (smart, all published, with SEO title, description and body copy): **ARDEX** (`/collections/ardex`,
  vendor = ARDEX) and twelve sub-collections by `ardex-<group>` tag: `ardex-tile-adhesives`, `ardex-grouts`,
  `ardex-waterproofing`, `ardex-floor-levelling`, `ardex-primers-additives`, `ardex-silicones-sealants`,
  `ardex-concrete-repair`, `ardex-civil-engineering`, `ardex-render`, `ardex-flooring-adhesives`, `ardex-tools`, `wedi`.
  The existing Hardware, Tile Adhesive, Grout, Waterproofing and Silicone collections pick the products up through their
  type and tag rules. New product types: "Primers & Additives", "Concrete Repair", "Civil Engineering", "Render",
  "Flooring Adhesives", "Uncoupling & Acoustic Mats", "Tile Backer Boards", "Shower Systems".
- **Menu**: "ARDEX adhesives, grout & waterproofing" added under Hardware in `main-menu-2026` (the live header menu).
- **Catalogue page**: `/pages/ardex-catalogues-data-sheets` (Page 119680499775) lists ARDEX's literature library,
  calculators, grout colour selector and technical bulletins, the four grout colour charts as colour swatches, and links to
  the twelve range collections. `ardex-catalogue-page-full.html` is the same page with every product's TDS/SDS links (too
  big for the API tool; paste it into the page in admin if wanted).
- **Files** (`ardex-2026-11/`): `parse_ardex_pages.py` (page parser), `ardex-catalogue-2026-11-11.json` (parsed site data),
  `ardex-categories.json`, `grout-colours.json`, `ardex_2026_11.py` (one level up: builds the productSet inputs),
  `ardex-2026-11-11.json` (what was sent), `ardex-created-2026-11-11.json` (Shopify ids per product and variant),
  `collect_results.py`, `followup_batches.py`, `catalogue_page.py` -> `ardex-catalogue-page.html` (the page body).
- One fix after creation: the ARDEX LQ 92 description had a stray control character from the ARDEX site (`2mm \x96 5mm`),
  replaced with an en dash.
- **When the ARDEX price list and account arrive**: enter costs inc GST and prices by the playbook (section 2), set the
  trade band, replace the placeholder SKUs, set stock (or switch the variants to "continue selling"), publish to the other
  five channels, remove `needs-cost` / `price-check`. Prices must be set before Google & YouTube is turned on.
- Not created: ARDEX WA grout (no product page on the ARDEX site), the two AUTO-DRAFT pages. Colour choices for ARDEX SE
  and ST silicone are not listed on the ARDEX site, so they are single-variant products with the colour taken in the order
  notes until the price list gives the colour codes.
