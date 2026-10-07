# Excellent Tiling Services – Shopify theme

Theme source for [excellenttilingservice.com.au](https://excellenttilingservice.com.au)
(Excellent Tiling Services Pty Ltd, 17A Olga Road, Maddington WA 6109).

`theme/` holds the custom ETS files (sections, snippets, templates, CSS/JS) from the
Horizon-based "ETS Premium" theme. Stock Horizon files are not duplicated here.

Last synced from the live theme ("ETS 2026 – Landing page boost (draft)", the published theme) on
4 Oct 2026: every `ets-*` asset, section and snippet, plus `layout/theme.liquid`, `meta-tags`,
`config/settings_data.json`, the header/footer groups and the templates already tracked here.
Third-party Section Store `ss-*` sections and the app-generated `product.store-wide.json` are
left out. Shopify is the source of truth: this repo does not deploy, so re-sync it after editing
the theme in Shopify.

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

## Shopify Inbox chat

The Inbox chat button and window are styled from the theme in `assets/ets-refine.css` (bottom of
the file) through the variables and `::part(activator)` / `::part(dialog)` hooks Shopify exposes:
navy pill button with a brass ring, Manrope font, solid cream chat window with a brass top edge. On phones the button sits above the sticky
"Call / Free quote" bar, and the bar slides away while the chat is open so the message box isn't
covered. `assets/ets-2026.js` holds back the email sign-up pop-up while a chat is open. Button text,
position (left/right), greeting and AI settings are set in Shopify admin → Inbox → Chat settings;
those admin colours are overridden by the theme CSS.

## Laptop sizing

The desktop layout was sized for large monitors, so on laptops (990-1600px wide) the site felt
zoomed in. `assets/ets-refine.css` (bottom of the file) trims it for that range only: slimmer sticky
header (about 107px instead of 130px once scrolled), smaller headings, department tiles four across
instead of two, a shorter collection banner and smaller product titles. Phones and wider screens are
unchanged. Two rules use `!important` to beat an inline banner shape and an earlier `!important`
product-title size. Product breadcrumbs also show on one line instead of as a numbered list.

## Product cards

Collection, search and carousel product cards (`assets/ets-refine.css`, "Product cards"): a white
rounded square with a real border, the photo inset inside it (product photos have their own white
backgrounds, so without this the edges vanished and the grid looked patchy), bolder two-line names,
bold prices and a small lift on hover. The collection grid shows five per row from 1200px wide.

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
