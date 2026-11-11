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

## MELA official seller: RRP = Bathroom City, non-MELA bathroomware drafted (11 Nov 2026, live)

ETS is the official MELA seller and MELA-exclusive for bathroomware; RRP must equal Bathroom City (playbook updated). Four
MELA items raised to Bathroom City's price, three shown as sales; 76 non-MELA bathroomware products (DSA, Celine, Chloe
ranges) set to Draft, list in `store-content/mela-exclusive-drafted-2026-11-11.json`. Details and the comparison script:
`store-content/pricing/README.md` and `reports/bathroom-city-match-proposal-2026-11-11.md`. No theme change.

## Product and collection audit, "On sale" per department (11 Nov 2026, live)

Every active product (1,415) and collection (131) was checked for placement; the findings and fixes are in
`store-content/collection-audit-2026-11-11.md`. Fixed in Shopify: 29 products that sat in no department (missing product
types added to the five department smart collections), 15 Roberts Designs drains retyped "Floor Drains", and 12 products
added to the manual Spouts & outlets, Inset basins and Accessories collections. Six new manual **"… on sale"** collections
(tiles-on-sale, vanities-basins-on-sale, tapware-sinks-on-sale, baths-toilets-on-sale, mirrors-accessories-on-sale,
hardware-on-sale) are the first link in each dropdown of both the live menu `main-menu-2026` and the draft menu
`main-menu-2026-v3` (Hardware on sale under both Adhesives & waterproofing and Tools & trims). They are empty until the
owner adds products and sets a compare-at price. No theme change. Same day, on the owner's instruction: the two empty collections
"Trade 25% items" and "BAT trims" were deleted (copies in `store-content/collections/deleted-2026-11-11.json`) and the BAT
trims link dropped from the live Hardware dropdown. Clearance stays separate from sale.

## Menu rethink: materials, tools, brands (11 Nov 2026, draft theme, waiting to be published)

The owner asked whether "Hardware" was the right name for a dropdown that had grown to 22 links mixing adhesives, tools
and brand names. New menu **`main-menu-2026-v3`** (Menu 228292722751; the old `main-menu-2026` is untouched) replaces
"Hardware" with three dropdowns a tiler would look for:
- **Adhesives & waterproofing** (`/collections/adhesives-waterproofing`, new smart collection): tile adhesives, grout,
  waterproofing, levelling / screeds / patching (`levelling-screeds`, new), primers & additives (`primers-additives`, new),
  silicone & sealants, concrete repair & render (`concrete-repair-render`, new), ARDEX range, RLA & Gripset range
  (`rla-gripset`, new, vendor RLA).
- **Tools & trims** (`/collections/tools-trims`, new): trowels, cutters, blades, spacers, grout clean-up, mixers, scrapers,
  silicone guns, large format handling, knee pads, tile drilling, trims, floor drains.
- **Brands** (links to the all-collections page): ARDEX, RLA & Gripset, Raimondi, BAT, Sigma, Maxisil, Roberts Designs,
  Baron, Washboy, Panther, MELA, Eternity tiles. (BAT trims is left out: its collection is empty.)
Tiles, Vanities & basins, Tapware & sinks, Baths & toilets, Mirrors & accessories, Renovations and Trade are unchanged.
The Hardware collection itself stays for its URL and search traffic.

Draft theme **"ETS 2026 – New menu: materials, tools, brands (draft)"** (id 145087791167, a copy of the live
"Price on request" theme) points the header, footer "Shop" column, collection chips, All departments page and page hero
chips at the new menu (`sections/header-group.json`, `sections/footer-group.json`, `templates/collection.json`,
`templates/list-collections.json`, `sections/ets-page-hero.liquid`). Ten top-level items need the whole row, so
`assets/ets-premium.css` hides the nav-row quote button (the hero and footer still have it), tightens the bar (13px, 7px
padding) and switches to the phone drawer under 1200px instead of clipping. Checked in a headless browser with the web fonts
loaded: the bar fits at 1920, 1440, 1280 and 1200px; 1100px shows the burger; the drawer and the three dropdowns render.
The five menu files and `ets-premium.css` were re-synced from the live theme first (the repo copies were behind).
**To go live: Shopify admin → Online Store → Themes → "New menu" draft → Publish.** Preview:
`https://excellenttilingservices.com/?preview_theme_id=145087791167`. The owner published the "Price on request" theme
the same day (now the live theme, id 145086480447).

## ARDEX range live, "Price on request" draft theme (11 Nov 2026)

The owner asked for every ARDEX Australia product on the site, live for search engines but not for sale yet. **206 ARDEX
products / 361 variants** are now Active on the Online Store channel only, at price $0.00, stock 0 and "stop selling when
out of stock", in 13 new ARDEX collections (`/collections/ardex` plus one per range), under Hardware in the main menu, with a
catalogue and data-sheet page. Details, ids and the activation steps: `store-content/supplier-sync/README.md`, "ARDEX
Australia range".

A $0.00 price looks like a free product, so draft theme **"ETS 2026 – Price on request (draft)"** (id 145086480447, a copy
of the live "Tiles by exact m2" theme) shows **Price on request** wherever a variant's price is $0: `snippets/price.liquid`
(product page, cards, quick view), `blocks/_featured-product-price.liquid` (no "From $0.00" on multi-variant products) and
`snippets/ets-product-schema.liquid` (the JSON-LD offer carries no price, only the currency and OutOfStock availability, so
Google is not told the product costs $0). Priced products render exactly as before. Tested in preview on the ARDEX SG Spray
page: "Price on request", Sold out button, no $0.00 anywhere, offer without a price.
**To go live: Shopify admin → Online Store → Themes → "ETS 2026 – Price on request (draft)" → Publish.** Preview:
`https://excellenttilingservices.com/products/ardex-sg-spray-silicone-smoothing-agent?preview_theme_id=145086480447`.
Until it is published the ARDEX pages show $0.00.

## Eternity supplier photos from the flash drive (10 Nov 2026, live)

The owner's external drive (`D:\Eternity`) has every file Eternity has sent. Applied live in Shopify: the generated "indicative
swatch" images on Lava Vesuv and Caliza replaced with the supplier's real tile photos; 26 supplier photos added across 14 tiles
(Lava, Time Stone, Caliza, ceramic wall tiles, Terrazzo Lumina); Time Stone Sand published with its first photos; Cement White /
Grey / Dark Grey featured images switched to the clean single-tile shot. Five basins that have no RRP in the supplier PDF were
created as drafts tagged `price-check`. Supplier documents (basin and kitchen catalogues, warranties, tile code sheets, test and
slip reports) are now in `Eternity/`. Record and the still-unpriced items: `store-content/supplier-sync/drive-eternity-2026-11-10/README.md`.

## Tiles sold by exact m² (5 Nov 2026, published the same day; tile prices switched the same day)

Owner chose "Option 2": tiles (not mosaics, which are sold by the sheet) are sold in 0.01 m² units, so 2.88 m² is
quantity 288. Shopify carts only take whole numbers, so each variant's price becomes price per 0.01 m² (whole-dollar
price per m², approved: `store-content/pricing/reports/tile-m2-units-proposal-2026-11-05.csv`). The product tag
**`m2-units`** switches a product into m² mode in the theme; untagged products render exactly as before.
Draft theme **"ETS 2026 – Tiles by exact m2 (draft)"** (id 144880795711, a copy of the live theme 144868016191):
- `snippets/price.liquid`: all prices x100 with " / m²" for m2 products (retail, trade, retail crossed out, save).
- `snippets/quantity-selector.liquid` + `assets/ets-2026.js`: "Area (m²)" box (step 0.01) on the product page and quick-add
  modal; the real quantity input is hidden and set to m² x 100. The calculator gives exact m² rounded up to 0.01 and fills the box.
- `snippets/ets-pdp-calc.liquid`: note text for m2 products.
- `snippets/cart-products.liquid`: cart lines show "2.88 m²" and the per-m² price; +/- hidden (remove and re-add to change).
- `blocks/_product-card-gallery.liquid`, `snippets/product-card.liquid`: no quick-add for m2 products.
- `blocks/_featured-product-price.liquid`, `snippets/ets-product-schema.liquid`: per-m² price, JSON-LD UnitPriceSpecification (MTK).
Tested in preview with the tag on one tile (then removed): calculator 12.5 m² +10% -> 13.75 m², 2.88 m² added as 288,
cart shows "2.88 m²". Cart count: a tile line counts as 1 (`sections/ets-header.liquid`, `assets/ets-2026.js`, and Horizon's
`snippets/cart-bubble.liquid`, `snippets/cart-drawer.liquid`, `assets/cart-icon.js`); tested 2.88 m² tile -> 1, plus 2 mirrors -> 3.
Known limit: checkout (not editable on Grow)
shows "x 288" with the unit price line "$55.00/m²".
**To go live: Shopify admin → Online Store → Themes → "Tiles by exact m2" draft → Publish**, then the price step
(`store-content/pricing/tile_m2_units_2026_11.py ... batches`: prices, costs, weights, unit price measure and the tag
together), then both trade scripts. Preview: `https://excellenttilingservices.com/products/time-stone-moon-porcelain-tile?preview_theme_id=144880795711`

## Trade (B2B) display: trade price next to crossed-out retail, corner badge, no "apply" links (5 Nov 2026, published the same day)

Trade pricing now runs on Shopify's native B2B (see `store-content/pricing/PRICING-PLAYBOOK.md`): a trade customer is a
company contact, and the B2B catalog gives every banded variant a fixed trade price with the retail price as compare-at.
Draft theme **"ETS 2026 – B2B trade display (draft)"** (id 144867229759, a copy of the live theme) makes the storefront
match, keyed on `customer.b2b?` instead of the old `trade` customer tag:

- `snippets/price.liquid` (customised Horizon file, now tracked here): for a B2B login the existing "Trade $x / Save $y (N%) /
  Retail $z" block is driven by the variant's catalog price and compare-at price. The old `ets-trade-rate` snippet (band x tag)
  is deleted.
- `sections/ets-header.liquid`: "Trade" chip shows the company name; a small fixed pill bottom-right ("Trade account · company ·
  trade prices shown"); the "Trade" menu item, top-bar link and drawer "Apply" button are hidden for B2B logins.
- `sections/ets-footer.liquid`: the trade CTA button and the "Trade account" footer link are hidden for B2B logins.
- `snippets/ets-pdp-trade.liquid`, `sections/ets-trade-band.liquid`, `sections/ets-trade-apply.liquid`, `snippets/ets-trade-rates.liquid`:
  B2B check and copy ("that is what you pay at checkout" instead of "the discount comes off in the cart"); the trade page shows
  "your account is active" to B2B logins instead of the form.
- `blocks/_product-card-gallery.liquid` (customised Horizon file, now tracked here) and `snippets/ets-card.liquid`: no "Sale" badge for
  B2B logins, since every discounted item carries the retail price as compare-at for them.
- Re-synced from the live theme ("ETS 2026 – Premium v2 (draft)", the published theme) on 5 Nov 2026: the files above.

The owner published this theme on 5 Nov 2026 (it is now the live theme, id 144867229759; the older drafts were removed). The
"Sale" badge fix came after publishing, so it sits in a new copy, **"ETS 2026 – no Sale badge for trade (draft)"** (id 144868016191).
**To go live: Shopify admin → Online Store → Themes → that draft → Publish.** Preview as a trade login:
`https://excellenttilingservices.com/collections/hardware?preview_theme_id=144868016191`. Theme settings
"ETS trade pricing" (tag, three rates) are no longer used by these files and can be ignored.

## Google "Add to preferred sources" button on blog posts (2 Nov 2026, draft theme, waiting to be published)

Google's Preferred Sources lets a reader pick sites to see more of in Top Stories and AI Overviews
(developers.google.com/search/docs/appearance/preferred-sources). Draft theme **"ETS 2026 – Google preferred source (draft)"**
(id 144771973183, a copy of the live theme) adds Google's standard button under every blog post, in
`sections/ets-article-page.liquid`: a one-line caption, `<div google-add-preferred-source-btn data-lang="en">`, Google's
`publisher.js` loaded async at the end of the section (blog posts only, not the rest of the site), and a plain deeplink
(`google.com/preferences/source?q=excellenttilingservices.com`) for readers without JavaScript. Same deeplink works in
social posts and emails.

**Check first:** the button only works for sites already in Google's source tool. Open
`https://www.google.com/preferences/source?q=excellenttilingservices.com` signed in to Google; if the site is not listed,
the button shows but does nothing. Google lists domains, not subfolders, so the blog counts as part of the site.
**To go live: Shopify admin → Online Store → Themes → the "Google preferred source" draft → Publish.** Preview:
`https://excellenttilingservices.com/blogs/news/how-much-tile-do-i-need?preview_theme_id=144771973183`.

## Premium look, after Bathroom City (2 Nov 2026, draft theme, waiting to be published)

The owner asked what makes Bathroom City's site (bathroom-city.com.au, Osborne Park; Shopify "Concept" theme) feel premium, and
for the same on ours. Both sites were screenshotted page by page (home, collection, product; desktop and phone). The difference
is restraint, not features: one light editorial typeface instead of heavy bold headings; photography that leads, with one headline
and one button over it; a white base with hairlines instead of boxed cards; a quiet header; nothing competing with the products.
(They also have things we do not: a Google rating badge with 208 reviews, a testimonials block, a brand-logo strip, a project
gallery and "book a consultation" in the main menu.)

Draft theme **"ETS 2026 – Premium (draft)"** (id 144742973503, a copy of the live theme) applies the same restraint in the ETS
brand rather than copying theirs:

- `assets/ets-premium.css` (new, loaded last from `layout/theme.liquid`, which now also loads Instrument Serif): serif display
  headings at weight 400 everywhere, including product titles, with the brass italic accent word back; white page background with
  the warm paper kept for alternating sections; pill buttons with small tracked capitals; a slimmer white header; a taller hero
  with a light shade and no "48 tile styles / 1200+ products / 5–25%" row; product cards on one soft tile with no border
  (`mix-blend-mode: multiply` hides the white photo backgrounds); the collection header without the render box and the moving strip;
  the product gallery without its frame; Shopify's purple "Buy with Shop" wallet button hidden, so "Add to cart" is the solid
  navy button again ("More payment options" stays).
- `snippets/ets-card.liquid`: the brand line above a card title is hidden when it is only the store's own name.
- The draft also carries the mega-menu change from the previous commit (6 still products per panel instead of 16 looping) and the
  touch-screen fix for the product strip.
- Re-synced from the live theme: `layout/theme.liquid`, `sections/ets-hero-full.liquid`, `sections/ets-categories.liquid` (the
  live theme had moved on since 25 Oct). `templates/product.json` and `config/settings_data.json` also differ live and are not
  yet re-synced here.

**To go live: Shopify admin → Online Store → Themes → "ETS 2026 – Premium (draft)" → Publish.** Preview first:
`https://excellenttilingservices.com/?preview_theme_id=144742973503`. Not in the theme, but worth the owner's call: the floating
"Shop Best Sellers / Shop with AI / Explore this product" bubbles come from an app and sit on top of the hero and product columns on
every page; Bathroom City has nothing like them.

## Clarity "dead clicks" on Vanities & basins (2 Nov 2026, repo only, not yet in Shopify)

Microsoft Clarity's summary reported dead clicks around "Vanities & basins" and quick back-clicks from product and
category pages. Every step of that path was clicked in a headless browser on the live site (desktop, iPad-size touch
and phone): the menu label and chevron, the mega-panel links, the phone drawer, the collection chips, product cards,
the colour filters (desktop dropdown and phone drawer), "Load more products" with and without filters, sort and the
page links. All of them navigate or update the page. The one thing a click can miss is the **moving product strip in
the collection hero**: with a mouse it pauses on hover, but on a touch screen it never stops, so a tap can land on
a card that has already moved on (the automation could not click it either). Fix in
`snippets/ets-product-marquee.liquid`: on screens with no mouse (`hover: none`) the strip is the same still,
swipeable row it already becomes under reduced motion. One CSS media-query line; copy it into the live theme's
snippet. The quick back-clicks from product pages are the whitespace-photo problem already covered above
(the crop plan in `store-content/images/` is still waiting for the owner's go-ahead).

## Google Merchant Center attribute fixes (30 Oct 2026, live)

From the Merchant Center "product attribute improvements" report. 75 products with photos that were missing from the
Google & YouTube channel are now on it; the variant colour/finish (Chrome, Matt Black, Mill Finish and so on) is now
sent to Google's `color` field on 2,289 variants; the last 9 variants without a SKU have one. Still for the owner:
17 no-photo products to exclude from Google (the tool cannot unpublish), and supplier barcode lists. Details in
[store-content/merchant-center-2026-10-30.md](store-content/merchant-center-2026-10-30.md).

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

## RLA Polymers range (28 Oct 2026, live)

A new supplier's two catalogues (RLA Tiling Product Range 2026 and the Gripset Waterproofing Product Guide) are in
Shopify as **69 live products / 165 variants** with full descriptions, SEO, photos, metafields, delivery profiles,
collections and channels set up, tagged `rla-2026-10`, `needs-cost`. Stock is 0 and the variants stop selling
at zero, so they are visible but show as sold out until costs and stock arrive. Prices are proposals a little under AU retail; there is no
cost until the RLA trade account is approved. The Waterproofing collection now
also matches the `Waterproofing` tag and the new "Waterproofing Membranes" / "Waterproofing Accessories" types.
Details, codes and the activation steps: `store-content/supplier-sync/README.md`, "RLA Polymers range".

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

## Google Drive DSA folder (26 Oct 2026)

The supplier's Google Drive folder was read through the Drive connector and applied to the store: lab slip
ratings and test-report specs on the 10 porcelain tile products (Particle Grey and Warm corrected from P4 to P5),
34 new tile photos, 2 new basins (Chet, Mezzo) with photos, warranties and estimated costs on all basins and
sinks. Details, scripts and what was deliberately not added are in
`store-content/supplier-sync/drive-dsa-2026-10-26/README.md`.
