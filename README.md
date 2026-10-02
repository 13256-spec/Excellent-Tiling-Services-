# Excellent Tiling Services – Shopify theme

Theme source for [excellenttilingservice.com.au](https://excellenttilingservice.com.au)
(Excellent Tiling Services Pty Ltd, 17A Olga Road, Maddington WA 6109).

`theme/` holds the custom ETS files (sections, snippets, templates, CSS/JS) from the
Horizon-based "ETS Premium" theme. Stock Horizon files are not duplicated here.

## Showroom bookings

The showroom is open **by appointment only**, Monday to Saturday 4:30 pm to 9 pm (closed Sunday).

- Page: `/pages/book-appointment` (template `page.book-appointment` → section `ets-booking-page`).
- Out of the box the section uses Shopify's native contact form. Each request is emailed to
  the store's sender email with appointment type, preferred date/time, name, phone, email,
  suburb and order number.
- Open days and time slots are editable in the theme editor (Availability settings).
- To use a bookings app instead, add its app block to the "ETS showroom booking" section in
  the theme editor. When an app block is present it replaces the built-in form.

## Deploying

Edits are made on an unpublished copy of the live theme, previewed, then published from
Shopify admin → Online Store → Themes.

## Navigation (draft theme, 1 Oct 2026)

The live header (`sections/ets-header.liquid`) builds its dropdowns from a Shopify menu. In the old
`main-menu`, the combined items linked to only half their range ("Baths & toilets" opened
`/collections/baths`, so no toilets showed). Fix, staged without touching the live theme:

- Four smart collections (by product type, published, manual order that alternates the two halves):
  `baths-toilets`, `vanities-basins`, `tapware-sinks`, `mirrors-accessories`.
- New menu `main-menu-2026` (copy of `main-menu` whose combined items point at those collections,
  plus "All baths", "All vanities", "All tapware" and "All accessories" links).
- Unpublished theme **"ETS 2026 – Menu fix: baths & toilets (draft)"** (duplicate of the live theme)
  uses `main-menu-2026` in the header, footer "Shop" column, collection hero chips, All departments
  page and page-hero chips. It also replaces "free shipping on small items" wording with "free
  shipping over $100" to match the current shipping rates.
- New products are picked up automatically by product type; to keep the dropdown mix, drag new items
  into place under Products → Collections (sort is manual).

This theme is now the live (published) theme, confirmed 2 Oct 2026, so `main-menu-2026` is the live
menu and `main-menu` is no longer used by the header.

2 Oct 2026: "Ceramic & wall tiles" (`/collections/ceramic-wall-tiles`) and "Mosaic tiles"
(`/collections/mosaic-tiles`) added under Tiles, after "300 x 300 mm", in both `main-menu` and
`main-menu-2026`.

## Store content

`store-content/policies/` holds the policy text (updated 1 Oct 2026: shipping matches the live rates,
Australian privacy policy, trade-account and quote terms). Paste each file into Shopify admin →
Settings → Policies (the API connector used here can't write legal policies).

## SEO

- `seo/generate_product_seo.py` builds every product's search title (≤60 chars) and meta
  description (≤155 chars, always mentions Perth) from the product's own specs.
  `seo/product-seo.json` is the exact set written to Shopify on 26 Sep 2026 (224 products).
- `seo/collection-seo.json` holds the titles/descriptions added to 27 collections that had none.
- Search-term pass (1 Oct 2026), applied live in Shopify, aimed at shoppers Australia-wide
  (no city in titles; delivery wording follows the shipping policy):
  - `seo/search-keyword-collections.json`: 21 collections retitled around what people search
    ("bathroom vanities for sale", "double vanities", "bathroom taps", "basin taps",
    "shower mixer", "shower heads", "bath taps", "kitchen mixer taps"...), with new search
    titles/descriptions and a keyword-rich first paragraph. Visible collection names changed
    for tapware → "Bathroom Taps & Tapware", basin-mixers → "Basin Mixers & Basin Taps",
    wall-mixers → "Shower Mixers & Wall Mixers", shower-tapware → "Shower Heads & Shower Sets",
    bath-tapware → "Bath Taps & Spouts", kitchen-tapware → "Kitchen Mixer Taps",
    double-vanities → "Double Vanities", single-vanities → "Single Vanities". Handles/URLs unchanged.
    Tiles stay Perth-focused because tiles aren't shipped outside Perth metro.
  - `seo/keyword_product_titles.py` → `seo/keyword-product-titles.json`: search titles for the
    178 active MELA products that add the everyday term for each type ("Basin Mixer Tap",
    "Shower Mixer", "Wall Hung Vanity", "Bathtub", "Bathroom Mirror"...). Descriptions keep the
    product facts from `product-seo.json` and end with that type's delivery: free shipping
    Australia-wide over $100 (tapware, showers, accessories), Australia Post (basins, mirrors,
    sinks, freestanding bath taps) or Perth delivery with freight quoted Australia-wide (vanities,
    baths, toilets, shower screens). Live ones had been reset to "Shop online at Excellent Tiling
    Services" with no SEO title, so something overwrote the 26 Sep set.
  - Shopify's API clears the meta description if a product's SEO title is sent alone, so
    always send both.
  - Theme: uploaded 1 Oct 2026 to the unpublished "ETS 2026 – Menu fix: baths & toilets (draft)"
    alongside the menu fix; that theme is now live. `meta-tags.liquid` business schema now serves Australia, not just
    Perth, and the " – Excellent Tiling Services" suffix is skipped for any title containing " | ".
- Theme: `snippets/meta-tags.liquid` no longer appends the shop name to titles that already
  end in "| ETS Perth", so titles stay inside Google's display limit.

## Booking form (Shopify Forms)

See [store-content/booking-form-shopify-forms.md](store-content/booking-form-shopify-forms.md) for the exact fields and settings. Adding the Forms block to the booking section replaces the built-in request form.

## Structured data (schema.org)

- `snippets/meta-tags.liquid`: sitewide LocalBusiness (address, hours, contact, product range,
  30-day return policy with 15% restocking fee). Update the return policy block if the refund policy changes.
- `snippets/ets-structured-data.liquid` (rendered at the end of `meta-tags.liquid`): WebSite +
  site search (home), CollectionPage/ItemList (collections), Service (tiling services page),
  BlogPosting (articles).
- `snippets/ets-breadcrumbs.liquid`: BreadcrumbList.
- `snippets/ets-product-schema.liquid`: Product/ProductGroup for every product (images, brand,
  specs and dimensions from the `ets` metafields, price, stock, seller, return policy per offer).
  Barcodes are only output as a GTIN when they are 8/12/13/14 digits, so supplier codes in the
  barcode field no longer produce invalid GTINs.
  **Stock Horizon edit:** in `sections/product-information.liquid` (not stored here), the first
  lines

  ```liquid
  <script type="application/ld+json">
    {{ closest.product | structured_data }}
  </script>
  ```

  are replaced with `{% render 'ets-product-schema', product: closest.product %}` so each
  product page carries one product schema, not two. Redo this after a Horizon update.
- Uploaded 29 Sep 2026 to the unpublished theme "ETS 2026 – Schema for AI + search (preview)"
  (a duplicate of the live theme); publish it from Shopify admin → Online Store → Themes.
