# BAT Trims 2023-24 catalogue

All of BAT's 2023-24 trims catalogue is in Shopify as **DRAFT** products, waiting on Adam's trade
price list. BAT is a separate supplier from Roberts Designs: different products and different codes.

- 40 products, 1,350 variants. Every variant has a BAT code as its SKU, a weight, the
  `shipping.box_size` metafield and a photo.
- All are in the **Tile Trims & Edging** collection (it's a smart collection, so it uses the existing
  product types) and in **Hardware**.
- Category: Hardware > Building Materials > Molding. Google category metafield
  `mm-google-shopping.google_product_category` = `7112`.
- Each product has its own SEO title and description, written for Perth buyers.
- Tags on every product: `BAT Trims`, `BAT`, `supplier-bat`, `bat-catalogue-2023-24`, `price-needed`,
  plus `ship-local-only` + `ship-long` or `ship-parcel`.

## Photos

- The main photos come from BAT's own website (battrims.com): a studio photo first, then the profile
  drawing with dimensions. There are 75 images, renamed `bat-trims-*.jpg`, with alt text for Google
  Images.
  - `website-images.json`: which photo goes on which product.
  - `shopify-website-file-ids.json`: the Shopify file IDs.
- The catalogue crops stay on the products, after the website photos. The colour swatches (Antique
  Brass, Copper, Gunmetal and others) are linked to their colour variants.
- The site is behind a bot check, so plain curl is blocked. A headless browser gets through after about
  20 seconds and can then read `/wp-json/wc/store/v1/products?category=trim`.

## Shipping

- 3m+ lengths (36 products, 1,172 variants) are in the **Perth only (local delivery / pickup)**
  profile.
- These stay in the General profile, so they can go by parcel:
  - mosaic corner pieces
  - cove trim corners
  - balcony corners
  - end caps

## To publish (once Adam sends prices)

1. Put Adam's trade prices (ex GST) in the `cost_ex_gst` column of `bat-variants.csv`.
2. Price each variant:
   - Price inc GST must be at least **cost × 1.1 × 1.25**. This is the public floor in
     `../pricing/PRICING-PLAYBOOK.md`.
   - Check Tradiecart, TSP Trims and Adheseal (all three sell BAT), then price 5–8% under them, but
     never below the floor.
3. Set the unit cost on each variant, so Shopify reports margin.
4. Set the prices, then remove the `price-needed` tag and set the products to ACTIVE.
   - Never publish a $0 variant. Any code Adam doesn't price stays in draft.
5. Make sure each product is on the Online Store, Google & YouTube and Shop sales channels.

## Getting found on Google

- Active products go into the Shopify sitemap (`/sitemap.xml`) on their own, and Google picks them up
  from there.
- To speed it up, use URL Inspection → Request indexing in Search Console for:
  - `/collections/tile-trims-edging`
  - the top sellers: Aluminium Tiling Angle, Stairnosing, Cove Trim, Mosaic Corner Angle
- Merchant Center gets the products through the Google & YouTube channel. Each one already has a
  brand (BAT Trims), SKU, weight, category 7112 and a photo. GTINs aren't in the catalogue, so they're
  sent as "no identifier" until BAT provides barcodes.

## Checks for Adam

Some items on BAT's website differ from the 2023-24 catalogue. Confirm them with Adam before
publishing.

- **MORTARLOC length.** The website lists 1.8m lengths and the catalogue says 3m. The listings say
  3m.
- **Aluminium Angle 28mm (AA-28-3).** It's on the website but not in the catalogue, so it isn't
  listed.
- **On the website only, not listed:**
  - Aluminium Channel Trim (U-channel)
  - Aluminium Angle 1m
  - Brass Angle 1m
  - Stainless Angle 2.7m (Marine 316)
  - Stainless Half Round 2.5m (Grade 304 and Marine 316)
  - Project Aluminium Angle (PA)
  - Project Mosaic Corner Angle (PMCA)
  - BATEX 3.3m for vinyl
  - Rubber stairnosing insert (sold alone)
  - Joiner packs (CTJ-6, APC60J-6, BETJ-6)

  These are easy to add once Adam confirms they're stocked and sends prices.

## Files

| File | What it is |
|---|---|
| `build_bat_products.py` | The catalogue typed out as data. Run it to rebuild `bat-products.json` and `bat-variants.csv` |
| `bat-products.json` | Every product: title, description, SEO, options, variants (SKU, weight, box) |
| `bat-variants.csv` | One row per variant, with empty `cost_ex_gst` / `price_inc_gst` columns for pricing |
| `build_bulk_jsonl.py` → `bat-productset.jsonl` | The `productSet` payloads used to create the products |
| `image-files.json`, `shopify-file-ids.json` | Catalogue image crops and their Shopify file IDs |
| `website-images.json`, `shopify-website-file-ids.json` | Website photos per product and their Shopify file IDs |
| `message-to-adam.md` | The text asking Adam for the trade price list |
