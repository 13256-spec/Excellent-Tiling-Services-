# Excellent Tiling Services – Shopify theme

Theme source for [excellenttilingservices.com](https://excellenttilingservices.com)
(Excellent Tiling Services Pty Ltd, 17A Olga Road, Maddington WA 6109).

`theme/` holds the custom ETS files (sections, snippets, templates, CSS/JS) from the
Horizon-based "ETS Premium" theme. Stock Horizon files are not duplicated here.

Last synced from the live theme ("ETS 2026 – Seller schema for AI (draft)", the published theme) on
25 Oct 2026 (the 8 domain files; the rest on 4 Oct 2026): every `ets-*` asset, section and snippet, plus `layout/theme.liquid`, `meta-tags`,
`config/settings_data.json`, the header/footer groups and the templates already tracked here.
Third-party Section Store `ss-*` sections and the app-generated `product.store-wide.json` are
left out. Shopify is the source of truth: this repo does not deploy, so re-sync it after editing
the theme in Shopify.

## Product photos and the product-page gallery (26 Oct 2026)

The owner found product pages showing a small product in a huge white square. Two causes, two fixes:

1. **Supplier photos are mostly white space** (the product fills 40-60% of a 2000 px square). The Toilets collection's
   photos (42 images, 10 products) were replaced live with tight square crops of themselves via Shopify's CDN
   `crop=region` parameters, originals saved to Content > Files as `original-<name>`. A plan for the remaining 271
   products / 653 images is ready in `store-content/images/` and waits for the owner's go-ahead. Details and method in
   [store-content/images/README.md](store-content/images/README.md).
2. **The gallery was the full width of the media column and taller than the screen.** Draft theme
   **"ETS 2026 – Product gallery (draft)"** (id 144507338815, a copy of the live theme) adds a block to
   `assets/ets-refine.css`: framed white photo box with rounded corners, gallery column capped at 620 px on desktop,
   frame height capped so the photo fits on screen. Also carries the repo copy of `ets-refine.css` (chat, laptop,
   product-card and cookie-banner rules that were only in Shopify until now). **To go live: Online Store → Themes →
   the "Product gallery" draft → Publish.** The "Call any time" theme is live since 26 Oct.

## DSA toilet collection (26 Oct 2026, live)

Eternity sent the DSA toilet product sheets (SharePoint folders, downloaded by the owner). Ten products created live and the
existing smart toilet updated, via `store-content/supplier-sync/dsa_toilets_2026_10.py` -> `dsa-toilets-2026-10-26.json`:
Eternal Clarice (DSA8080, $660), Edna Care (DSA8081, $1,320) and its back rest (DSA8081-Back rest, $268.99), Eternal Element
(DSA8084, $500), Caleb Aria wall faced with in-wall cistern (DSA8102, $999), Eternal Edge (DSA8202, $550), Eternal Forma
(DSA8203, $550), Eternal Flow (DSA8206, $660), Caleb Vero wall hung with in-wall frame (DSA8305, $1,299), Crystal Prime
(DSAG1FD-E, $3,299) and Crystal Nova (DSAG6FD-E, $3,299) smart toilets. "Crystal Smart Toilet with Bidet Seat" is now
**Crystal Elite Smart Toilet Suite** (DSAYC318GE, $2,999) with the sheet's specs and a second image.

- **Price** = DSA RRP (as for the rest of the DSA range). **Cost** = ESTIMATE, RRP less the 45% account discount DSA gave on
  the Malaga vanity packages, ex GST (= RRP x 0.5), tag `cost-estimate`; the toilets were added to
  `store-content/pricing/DSA-trade-price-request-2026-10-14.txt` so Eternity can confirm. No trade band until the cost is real.
- Full descriptions, SEO title and description, `ets.*` spec metafields (range, material, WELS, sizes), supplier metafields,
  product photos plus the dimension drawings and, for the smart toilets, the feature and specification sheets.
- Collections: Toilets, Back to Wall Toilets (not the wall hung Vero), Baths & Toilets (automatic by type) and the new automatic
  **Smart Toilets** collection (tag `Smart Toilet`, also picks up the MELA smart suites and bidet seats). Perth-only delivery
  profile, published to all six channels. The back rest has only a tiny supplier photo (tag `needs-photo`).
- Videos: the Crystal Prime and Nova installation video (same file, 2 min 46 s) is on both product pages, and the Crystal
  Elite has its features video (1 min 13 s) and installation video (2 min 15 s). The other toilets came with no video.
- Master pricing CSV and the three price-list PDFs regenerated with the 12 rows. Supplier images kept in
  `store-content/supplier-sync/dsa-toilet-sheets/` (the PDFs and videos are too big for the repo; the owner has them).

## "Call any time" on the phone number (26 Oct 2026, draft theme, waiting to be published)

The number was on every page but nothing said when the phone is answered, and it sat next to the showroom hours
(Mon–Sat 4:30–9 pm), so a shopper could assume the phone keeps those hours too. Draft theme
**"ETS 2026 – Call any time (draft)"** (id 144503144511, a copy of the live theme) adds the words: top bar and header
call button ("Call any time · 0450 960 543"), the mobile menu drawer, the contact page Phone row ("Call any time, 7 days.
If we miss you, we'll call back.") and the FAQs intro line. Files: `sections/ets-header.liquid`,
`sections/ets-contact-page.liquid`, `templates/page.faqs.json`. The same draft also sets `ets_email` in
`config/settings_data.json` to contactus@excellenttilingservices.com, because the footer was still showing the old
`.com.au` address (the setting was unset, so the theme fell back to its old default). The "New domain" theme is now the
live theme. **To go live: Shopify admin → Online Store → Themes → the "Call any time" draft → Publish.**

## Supplier on every product (25 Oct 2026)

The pinned product metafield **`ets.supplier`** ("Supplier") now records who ETS buys each product from, on all 1,126
products (it was filled on 136). Values, by vendor: MELA and the MELA vanity add-ons → **Bathroom City**; tiles and the
DSA range (vendor "Excellent Tiling Services") → **Eternity Tiles**; Roberts Designs, Maxisil, Sigma, Siri, Baron and
Barwalt (the `Roberts Designs` / `supplier-import` tags) → **Roberts Designs**; BAT, BAT Trims, Raimondi, Panther,
NICLIS, Washboy, ADA Instruments and Atika (the `supplier-bat` tag; Raimondi is bought through BAT's Raimondi price
book) → **B.A.T. Trims Pty Ltd**; Sika → **Sika Australia**. Two products have no supplier recorded because nothing in
the store or these notes says where they come from: the RLA Quick Set Liquid Additive and the Click Heavy Duty
Powerblock. The older unpinned `custom.supplier` field (Eternity items only) was left as it was; `ets.supplier` is the
one to use. Filter in admin with Products → search `metafields.ets.supplier:"Roberts Designs"` or add the Supplier
column to the product list.

## POS collections (25 Oct 2026)

Only 3 collections were published to the Point of Sale channel, so the POS home screen had nothing to pin. Now every
collection except the `trade-list-*` price lists and `black-friday-2026` is on POS (103 collections), and nine new automated
collections fill the gaps in the tiling-supplies side (all also on Online Store and Shop, each with a cover image):
`grout`, `silicone-sealants` (silicone, hybrid sealants, primers, nozzles, cleaner), `waterproofing`, `trowels-floats`,
`tile-cutters-saws-machines`, `large-format-tile-handling`, `tiling-hand-tools`, `knee-pads-workwear`, `clearance`
(tag `Clearance Item`). `tile-adhesive` is now "Tile Adhesive & Additives" (adds the `Adhesives & Additives` tag),
`tile-spacers-wedges` also takes the `Tile Wedges` type and `diamond-blades-drill-bits` the `Core Drills` type.
Suggested POS smart grid (Shopify POS app → Home → Edit grid): Tiles · Tile Adhesive & Additives · Grout · Silicone & Sealants ·
Waterproofing · Trowels & Floats · Tile Spacers & Wedges · Tile Cutters, Saws & Machines · Diamond Blades & Drill Bits ·
Tile Trims & Edging · Floor Drains & Wastes · Tiling Hand Tools · Vanities & Basins · Tapware & Sinks · Baths & Toilets ·
Mirrors & Accessories, with brand tiles (BAT, Raimondi, Sigma, Maxisil, Roberts Designs, MELA) on a second row.
Collections are all automated by product type/tag, so a new product only needs the right type to land in them.

## New domain excellenttilingservices.com (25 Oct 2026, draft theme, waiting to be published)

Shopify's primary domain, contact email and policies already use **excellenttilingservices.com** /
**contactus@excellenttilingservices.com**; the old `excellenttilingservice.com.au` (and `www.`) 301-redirect to it.
The theme still hardcoded the old email and domain in 8 files, so draft theme
**"ETS 2026 – New domain excellenttilingservices.com (draft)"** (id 144483844159, a copy of the live theme) replaces every
`excellenttilingservice.com.au` with `excellenttilingservices.com` in: `sections/ets-flagship-footer.liquid`,
`ets-flagship-home.liquid`, `ets-contact-page.liquid`, `ets-booking-page.liquid`, `ets-standard-page.liquid` (delivery page),
`snippets/meta-tags.liquid` (LocalBusiness `email`), `templates/llms.txt.liquid` and `templates/llms-full.txt.liquid`
(fallback base URL and email). Everything else in the theme uses `shop.url` / `request.origin`, so it followed the domain change
on its own. The repo copies (and every other repo file: policies, notification templates, agent notes, marketing scripts and copy)
now use the new domain too. **To go live: Shopify admin → Online Store → Themes → the "New domain" draft → Publish.**
Still manual in admin: Settings → Notifications → sender email, and the Shopify Forms / booking notification address.

## Seller schema for AI and search (24 Oct 2026, draft theme, waiting to be published)

The sitewide JSON-LD said who we are but not plainly that we are a shop that sells to the public and to trade. Draft theme
**"ETS 2026 – Seller schema for AI (draft)"** (id 144447766591, a copy of the live theme with two snippets changed) adds:

- `snippets/meta-tags.liquid` (LocalBusiness block): types now `LocalBusiness, HardwareStore, HomeAndConstructionBusiness, OnlineStore`;
  a plain-English description ("tile and bathroom retailer ... sells ... to the public and to trade customers"); `audience`
  (homeowners + trade); `brand` (Sika, Raimondi, BAT, Sigma, Maxisil, Panther, Washboy, Baron, RLA, MELA); `hasOfferCatalog` with the
  eight departments and their collection URLs; `knowsAbout` with tile adhesive, grout, tiling tools, trims and trade supply;
  `potentialAction` = BuyAction, SearchAction, ReserveAction (showroom), RegisterAction (trade account).
- `snippets/ets-product-schema.liquid` (every Offer): `businessFunction` Sell, `eligibleCustomerType` Enduser + Business,
  `availableDeliveryMethod` (pickup + parcel, or pickup only when tagged `ship-local-only`), `availableAtOrFrom` the Maddington
  showroom, `areaServed` (Australia, or Perth for local-only), `shippingDetails` destination.

Both repo copies were first synced to the live theme (checksums matched) and then edited, so the repo matches the draft. The
draft was rendered and every JSON-LD block parsed (home, Sika Master Lite, Time Stone Moon). **To go live: Shopify admin →
Online Store → Themes → "ETS 2026 – Seller schema for AI (draft)" → Publish.** This session cannot publish themes.

## Shop app (Shop sales channel), 12 Oct 2026

The Shop app store was almost empty: 5 of 921 active products and no collections were on the Shop
channel. All 921 active products and all 92 website collections are now published to Shop, and
60 collections that had no cover image (Shop hides those) use their first product's photo, which is
what the website already showed as the fallback. Brand assets, Shop Store navigation and the
collection lists can only be set in admin: the values to paste in are in
[store-content/shop-app-store-setup.md](store-content/shop-app-store-setup.md).

## Storefront filters

Collection and search pages only filter by availability and price because the Search & Discovery app is not
installed. Setup steps and the product fields that feed the filters: [store-content/search-filters-setup.md](store-content/search-filters-setup.md).

## DSA bathroomware (14 Oct 2026)

Eternity's non-tile "DSA" range (Celine/Chloe tapware and showers, Malaga vanities, basins, sinks, LED mirrors,
wastes, smart toilet): 62 products added at Eternity's retail price with no cost, tagged `needs-cost`, in their department collections
and published to all channels. **Live since 14 Oct 2026** (owner's call: sell at Eternity's price until DSA sends a
trade price list; the request to send them is `store-content/pricing/DSA-trade-price-request-2026-10-14.xlsx`). Details in [store-content/supplier-sync/README.md](store-content/supplier-sync/README.md).

## MELA mirror descriptions (13 Oct 2026)

After customer feedback that the LED mirror pages lacked detail, all 17 MELA mirror, LED mirror and
mirror-cabinet listings were rewritten from the supplier's product pages, spec sheets and warranty/care
PDFs (sizes and codes, light, touch dimmer, demister, IP44/SAA, mirror thickness, frame depth, cabinet
box sizes, warranty, cleaning), with matching `ets.*` spec metafields. All four LED ranges are listed as cool white, dimmable.
Records are in [store-content/mirrors/README.md](store-content/mirrors/README.md).

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

## Supplier names (owner rule, 4 Oct 2026)

Never show the tile supplier's name (Eternity) anywhere on the site or in marketing: product and
collection text, vendor, tags, SEO titles/descriptions, image alt text, customer price lists, social
posts. Tiles use vendor "Excellent Tiling Services"; the supplier lives only in the internal
`custom.supplier` metafield and in `store-content/pricing/`. On 4 Oct 2026 "supplied by Eternity Tiles"
was removed from 7 tile collections (porcelain, cement, lava, morgan, particle, terrazzo, time-stone);
before/after text is in `seo/collection-supplier-name-removal.json`. A full export of all 506 products
found no other mentions, and none in menus, blog posts or the live theme's templates.

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

## Design refresh (draft theme, 3 Oct 2026)

Unpublished theme **"ETS 2026 – Design refresh (draft)"** (duplicate of the live theme) tones down the
template look:
- `assets/ets-refine.css` (loaded after `ets-2026.css`): one typeface (Manrope), no italic accent words in
  headings, smaller headings, plain section labels instead of pill "eyebrows", simple rectangular buttons
  without the arrow bubble, flat cards, no fade-in on scroll, vendor label hidden on product cards.
- `templates/index.json`: plain headings, removed the duplicate "What we do" services block, real tile-range
  descriptions (colours, finishes, sizes), best-seller tiles from the 600×600 collection.
- Homepage hero is the new `sections/ets-hero-full.liquid`: full-width rotating room photos with a slow
  zoom, dark gradient, white headline, two buttons, a "Pictured" product link per photo and live counts
  (tile styles, products, trade discount). Own slider script; the old `ets-hero` section is unused.
- Trade discounts now match the per-item bands (`snippets/ets-trade-rates.liquid`, used by
  `ets-trade-band` and `ets-trade-apply`; trust strip says "up to 25%"). The live theme still shows the
  old 20% / 15% / 10% table until this draft is published.

## Landing page boost (draft theme, 3 Oct 2026)

The design refresh above is now live. Unpublished theme **"ETS 2026 – Landing page boost (draft)"**
(id 143765635135, duplicate of the live theme) adds:
- Hero stats on phones as a tidy three-column row (tile styles · products · trade discount).
- Trust strip on phones as one slim swipeable row instead of a tall 2×2 block (`sections/ets-trust.liquid`).
- Sticky phone bar ("Call 0450 960 543" + gold "Free quote") that slides up once the hero is scrolled past
  (in `sections/ets-hero-full.liquid`, hidden on desktop).

## Product page cleanup (draft theme, 5 Oct 2026)

All 506 products use `templates/product.store-wide.json`, which the Section Store app had generated
with invented content: a "4.8 ★ 218 verified reviews" badge, made-up testimonials (Mark T., Helen K.,
James R., Natalie P.), a "30-Day Money-Back Guarantee", a "Receive by" date, a "warehouse pick window"
countdown, and generic AU-wide shipping filler. Fake reviews are a problem under the Australian Consumer Law.

In the unpublished theme **"ETS 2026 – Product page cleanup (draft)"** (gid://shopify/OnlineStoreTheme/143794143295),
`product.store-wide.json` now holds the clean ETS product page (the content of `product.json`) with the
scrolling ticker removed, fonts matched to the theme (DM Sans / Fraunces), and the phone number shown
once. Saved here as `theme/templates/product.store-wide.json`. Publish the draft from Online Store → Themes
to make it live.

Also in the draft: the product-page trade note now says "Trade accounts get 5–25% off, set item by item" (it said "up to 20%", from the tiles setting), and the scrolling ticker on collection pages is turned off. The owner confirmed the licensed team, supply & install and free measure & quote claims (5 Oct 2026).

## Theme recovery (5 Oct 2026)

The owner accidentally published the old "ETS 2026 – Menu fix: baths & toilets (draft)" theme and deleted the
theme that should have gone live. Shopify can't restore a deleted theme, so it was rebuilt from this repo:

- `themeDuplicate` of the (now live) Menu fix theme → unpublished **"ETS 2026 – Restored (5 Oct)"**
  (gid://shopify/OnlineStoreTheme/143796174911), which has all the stock Horizon and Section Store files.
- The 29 files that differed were uploaded from `theme/`: `ets-refine.css`, `ets-hero-full`, the trade sections and
  snippets, `ets-trust`, `layout/theme.liquid` and every template, including the cleaned `product.store-wide.json`.
  Liquid and CSS checksums match the repo exactly. All 37 sections the templates use exist in the theme.
- So the restored theme = the 4 Oct live sync + the 5 Oct product page cleanup. Anything changed only in the
  Shopify theme editor after those dates isn't in the repo and had to be redone by hand.
- Publish it from Online Store → Themes after a preview. Then delete the old Menu fix theme, or keep it as a backup.

## Mobile header fix (draft theme, 5 Oct 2026)

Unpublished theme **"ETS 2026 – Mobile header fix (draft)"** (gid://shopify/OnlineStoreTheme/143802990655), a
duplicate of the live "ETS 2026 – Shipping text fix (draft)" theme, with `sections/ets-header.liquid` and
`assets/ets-menu.css` from this repo (checksums match). Phones and tablets only; desktop is unchanged:
- Top bar (phones): the messages take turns full width (every 4.5 s), so "Australia-wide shipping from $20 · Free on
  orders over $1,000" is no longer cut off at "Fre". A long message wraps to two lines on small phones.
- The phone number moves from the top bar into the header as a call icon (next to account and cart).
- The header slides away while scrolling down and comes back on any scroll up, so it no longer covers about
  a seventh of the screen. It stays put while the menu is open or the search box is in use. Solid background on phones.
- Phones narrower than 375 px: smaller logo, and the account icon moves into the menu drawer ("Log in (trade & retail)").
- Publish it from Online Store → Themes after a preview on a phone.

## Wording cleanup (draft theme, 5 Oct 2026)

Unpublished theme **"ETS 2026 – Wording cleanup (draft)"** (gid://shopify/OnlineStoreTheme/143805218879), a
duplicate of the live "Mobile header fix" theme with 20 files from this repo (Liquid checksums match). Plainer,
customer-facing wording with no unverifiable claims:
- Trade: "set item by item", "a further 5–25%", "trade prices on every product", "our best price" and
  "usually within one business day" are gone. Now "5–25% off, depending on the item" and "the discount comes off in the cart".
- Product page: "Why buy from ETS" → "Why shop with us"; "Trade pricing" → "Trade accounts"; "Advice from a tiling
  team" → "Ask a tiler"; "Buy with confidence" → "Warranty and returns"; ticker says small items (not tiles) ship Australia-wide;
  the Delivery tab no longer says "We deliver within Australia" (tiles are Perth metro only).
- Home "Best sellers" → "Shop the range" (the tabs aren't sorted by sales). 404 no longer says the page "has moved".
- Services page: template slogans ("Renovations, done properly", "Four services, one team", "under one roof",
  "Good to know", "Let's plan your renovation") replaced with plain headings. Same for the delivery page.
- FAQ "Do you deliver?" now says tiles and large items are Perth metro. "1 products" → "1 product" on All departments.
- Not changed (store content, not theme): the Care & Warranty page names "AUS Home Collection Group Pty Ltd (trading as
  Bathroom City)" as the MELA warrantor, and tile descriptions say "sold per sqm to the nearest full box" while the
  calculator rounds to whole m².
