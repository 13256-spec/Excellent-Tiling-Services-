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

## Trade prices on the site + store-wide repricing (11 Oct 2026)

- Prices: every active product repriced to the owner's 11 Oct rule (cheaper than every competitor, 40%
  margin cap on high-margin items, profit floor kept). `store-content/pricing/reports/reprice-2026-10-11.md`
  has the numbers; `store-content/pricing/PRICING-PLAYBOOK.md` the rules.
- Trade accounts: approved customers (tag `trade`) now see their trade price on every product with the
  retail price crossed out, matching the automatic discount in the cart. Per-product band in the
  `ets.trade_band` metafield + `trade-list-N` collections. Guide: `store-content/trade-accounts/README.md`.
- Theme: unpublished **"ETS 2026 – Trade prices on site (draft 11 Oct)"** (gid://shopify/OnlineStoreTheme/143975940159),
  duplicate of the live theme with `snippets/ets-trade-rate.liquid` (reads the metafield instead of the old
  10/15/20%-by-type settings), `ets-pdp-trade.liquid`, `ets-trade-rates.liquid`, `sections/ets-trade-apply.liquid`,
  `ets-trade-band.liquid`. `theme/snippets/price.liquid` is the ETS-modified Horizon price snippet as it is live
  (trade/retail display); it is unchanged by this work. **Published by the owner on 11 Oct 2026** (it is now
  the live theme; the previous live theme "Copy of ETS – $180 shipping wording only" is no longer in the theme list).
  First trade customer approved the same day (tag `trade`).
- New segment "Trade applicants (waiting for approval)" in Customers → Segments.

## Sitewide trade bar (draft theme, 11 Oct 2026)

Logged-in trade customers now get a green bar under the header on every page: "✓ Trade account · Logged in as
<name>. You're seeing your trade prices. Retail prices are crossed out and the discount comes off in the cart ·
Your account · Log out". `snippets/ets-trade-bar.liquid`, rendered from `layout/theme.liquid` right after the
header group. Retail customers and visitors see nothing. `theme/layout/theme.liquid` was re-synced from the live
theme first (it carries a Metricool tracking script the repo copy lacked; checksum verified) and then the one
render line added. Uploaded to the unpublished theme **"ETS 2026 – Trade bar under header (draft 11 Oct)"**
(gid://shopify/OnlineStoreTheme/144004087871), a duplicate of the live theme; publish it from Online Store → Themes.

## Site audit and fixes (11 Oct 2026, evening)

Full crawl and catalogue audit after the day's pricing and shipping work: `store-content/reports/site-audit-2026-10-11.md`.
Every URL and internal link works; breadcrumbs and structured data are in place. Fixed: 336 products that no storefront
collection matched (smart-collection rules extended), 144 new Raimondi products priced and banded, supplier name and stale
"$1,000" wording removed, missing meta descriptions and image alt text added, duplicate Perth delivery rate removed in favour
of Shopify's own Local delivery. Open items (photos for 54 products, local-delivery settings, Search Console access) are in
the report.

## Discount codes, email automations and rollout plan (11 Oct 2026, night)

- Shopify discount codes: `WELCOME10` and `COMEBACK10` (10% off, scoped to the `trade-list-20` and `trade-list-25`
  collections so profit stays above 22%, once per customer, never with trade pricing) and `FREEPOST` (free standard
  post up to $30 on orders of $60 or more). Rules: `store-content/pricing/PRICING-PLAYBOOK.md` → "Discount codes".
- Klaviyo: 11 branded email templates and 7 live flows (welcome ×3, abandoned checkout ×2, abandoned cart,
  post-purchase ×2, win-back, trade application received, trade approved). IDs, timing and how to edit:
  `store-content/email/README.md`; sources in `store-content/email/templates/`, generator `make_emails.py`.
- Checkout: free standard post for WA orders of $100 or more on both parcel profiles
  (`store-content/shipping/README.md`).
- Theme: a draft copy of the live theme, "ETS 2026 – 10% sign-up offer (draft 11 Oct)", has the footer sign-up
  and pop-up promising 10% off a first order and showing `WELCOME10` after sign-up (settings in
  `sections/footer-group.json` only, no code change). The connector can't write to the live theme; the owner
  publishes the draft from Online Store → Themes.
- Plan: `marketing/rollout-2026-10-11.md` (week-by-week posts, owner to-dos, Black Friday proposal date).
- `.claude/agents/ets-copy-review.md`: shipping and discount-code facts updated.
- Photos: 24 of the 54 `photo-needed` products (all Raimondi) now have manufacturer photos, loaded from raimondispa.com and
  BAT Trims; 30 remain without any photo online (`store-content/reports/photos-sourced-2026-10-11.csv`, and the note in
  the audit report).

## Supplier cost check (12 Oct 2026)

- The owner's supplier price files (BAT Tools/Trims books and Raimondi list, May 2026; SILVER discount sheet;
  2025 MELA catalogue) were checked against every Shopify unit cost: all 1,948 BAT-family costs match the books,
  all 599 MELA costs are at or above the catalogue. The pricing rules re-run on a fresh export changed no price,
  cost or trade band. Report: `store-content/pricing/reports/supplier-cost-check-2026-10-12.md`; parsed books:
  `store-content/pricing/supplier-books-2026-05.csv`; master list now `store-pricing-2026-10-12.csv`.
- Playbook: new "Supplier price files on hand" section and the rule that Bathroom City's live list is the MELA
  cost basis, the catalogue the fallback.
- Later the same day the owner relaxed the 20% floor ("sometimes more, sometimes less, depends on the product"):
  `reprice_2026_10_12.py` adds the thin-margin rule (1% under a competitor who is below our 20% price while we
  keep 10%; 5–10% only on owner-named products; never under 5% or cost). 22 prices cut and 15 products moved to
  trade band 0 in Shopify; PDFs regenerated; playbook, agent and monitor updated.

## Duplicates check (12 Oct 2026)

- Fresh exports of every product, variant and image, plus collections, discounts, menus, pages, customers and
  Klaviyo, checked for duplicates: no duplicate products, SKUs, barcodes or variants. Fixed: 9 duplicate image
  copies on 5 products, the 3 old tag-based `trade-band-*` collections and the stale `trade-N` tags on 240
  products, a second welcome code (`ETSWELCOME10`, deactivated), a second free-shipping mechanism (app discount,
  deactivated; the free rates in Settings → Shipping stay), a test customer, 22 products on overlapping product
  types, and a draft Klaviyo flow + template. Report: `store-content/reports/duplicates-check-2026-10-12.md`.

## Product photos, round two (12 Oct 2026)

- On the owner's instruction to use supplier websites, 10 more of the products without photos now have supplier or distributor
  photos (BAT plaster trowel, paint scrapers and BAT Pro square trowel; NICLIS waterproofing bandage and 85 mm grate with one
  photo per variant; Raimondi Clipdozer, two Ipertitina connectors, 250 mm porcelain blade, Power Raizor MK2). 20 remain
  (buckets, BATSEAL sealers, BAT Luxe inspection drain, knives and blades, five Raimondi spares): BAT Trims' site blocks
  automated access and no stockist lists them. Sources and sizes: `store-content/reports/photos-sourced-2026-10-11.csv`.

## Sales review and brand pages (12 Oct 2026)

- 30-day review of where sales come from (`store-content/reports/sales-plan-2026-10-12.md`): about 320 real visits,
  8 orders, 6 of them from Google; the Performance Max campaign spends half its money outside Australia for no sales;
  social brings no orders; email has no sign-ups because the sign-up theme is unpublished.
- Nine smart brand collections created and published (`maxisil`, `sigma`, `raimondi`, `bat-tools`, `bat-trims`,
  `roberts-designs`, `panther`, `baron`, `mela`), each with SEO title, meta description and a delivery-accurate
  description; seven of them added to the Hardware dropdown of `main-menu-2026` and `main-menu`.
- Owner to-dos with click paths (Google Ads location fix, publish the sign-up theme, Search Console, eBay postage,
  reviews app) and two pricing decisions (small-item postage tier, pickup lead time) are in the report.

## Raimondi "what fits what" (12 Oct 2026)

Order #1009 (a Zoe 85A with its extension table, side square and spacers) showed the Raimondi range did not
say which accessories fit which machine. Fixed in three layers, see `store-content/raimondi/README.md` and
`store-content/reports/raimondi-fit-2026-10-12.md`:

- **Data (live):** product metafields `ets.fits_with` (list of products) and `ets.fits_models` (text) on all
  131 Raimondi machines, accessories, blades and parts; seven manual "shop by machine" collections
  (`raimondi-wet-saw-accessories`, `-bulldog-wheels-parts`, `-raizor-spares`, `-grout-clean-up-spares`,
  `-floor-machine-parts`, `-mixer-vibrator-parts`, `-easymove-bigfoot-accessories`) linked from the
  Raimondi collection; 31 wet-saw family products and the Double spacer rewritten from Raimondi's catalogue
  (titles say what they suit, descriptions open with "Fits:"). No links in descriptions (eBay copies them).
- **Theme (draft "ETS 2026 – what fits what (draft, not published)", 144033579071, until the owner publishes it; his earlier copy 144029417535 was deleted):** `sections/ets-product-fits.liquid` (card grid of what fits) and
  `snippets/ets-pdp-fits.liquid` (the "Fits:" line under the title), wired into `templates/product.json`
  and `templates/product.store-wide.json`.
- **Rule for new Raimondi products:** set both metafields, put "suits …" in the title, add the item to its
  `raimondi-*` collection and to the machines' `fits_with` lists, add a row to `fitmap.py`.

## Catalogue check and "what fits what" for the whole range (12 Oct 2026)

Customer feedback: hard to tell which items work with which. The owner photographed the BAT Trims Tools
Catalogue (106 pages); it is transcribed in `store-content/catalogue/bat-tools-catalogue.csv` (774 rows) and
every tool product was checked against it. See `store-content/catalogue/README.md` and
`store-content/reports/catalogue-check-2026-10-12.md`.

- **Data (live):** 370 products across BAT, Raimondi, Washboy, Panther, Siri, Sigma, Baron, Atika, Maxisil and
  Barwalt carry `ets.fits_with`, `ets.fits_models` and the new `ets.fits_role` (`parent` or `item`); 71 titles
  say what they suit, 55 product types corrected, 186 descriptions open with "Fits:" or carry "What fits:";
  the catalogue corrected a dozen facts (Bi-Bulldog wheels, Bulldog feed kit, Washboy sizes, trowel sizes,
  Sigma wheel fitment and more). Map as code: `store-content/catalogue/fitmap_all.py`; as data:
  `compatibility-all.csv`.
- **Collections (live):** eight "shop by system" collections, all brands together, linked from the Raimondi,
  BAT, Sigma and Panther pages: `grout-clean-up-systems`, `mixers-paddles-buckets`, `sigma-cutter-spares`,
  `scrapers-knives-blades`, `silicone-tools`, `knee-pads-spares`, `tile-drilling`, `washboy`.
- **Theme (draft 144033579071 only, until the owner publishes it):** the what-fits section now keys off
  `ets.fits_role` and links to any system collection (`system_handles` setting); headings "What fits this
  one" and "What this fits". The owner deleted his copy of the live theme, so a fresh API duplicate of the live
  theme carries the section; the live theme is never written to.
- **Supplier checks (owner asked for them):** Raimondi's site confirms the Bi-Bulldog ships without a wheel and the
  Bulldog with the 10 mm wheel; the 1050 W mixer has an M14 spindle (page rewritten, no chuck claim); BAT lists
  the Washboy WB-9002L handle but the price book does not, so it needs a cost before it can be listed. Open:
  whether the system collections go in the Hardware menu.

## New look (12 Oct 2026, declined by the owner)

**Declined.** The owner deleted the new-look draft on the evening of 12 Oct ("didn't publish it cause I
don't want it"). `theme/` holds the live (postage) look again; the new-look files survive only in git
history (commit 64e7157) and in `store-content/reports/redesign-2026-10-12.md`. Do not rebuild it unless asked.


- The owner asked for the site's look to be redone. `store-content/reports/redesign-2026-10-12.md` has the audit (blurry
  mosaics leading the Tiles range, a serif that never loaded, pill-and-shadow cards, a crowded phone hero, a product page
  with the buy button nine screens down), the direction ("porcelain and grout": white surfaces, 1 px lines, square corners,
  Archivo, the logo's blue as the one accent) and what was built in the theme copy "ETS 2026 – New look (draft 12 Oct)".
  Changed theme files are in `theme/`; before/after images in `store-content/reports/img/`.
- Live changes made with it: the Tiles collection is sorted by hand (big-format ranges first, mosaics last) with a room
  photo as its banner; the cart-page free-post bar no longer overlaps the order summary on desktop.

## Postage fix (12 Oct 2026, approved by the owner)

- Shopify rates on both parcel profiles and both Australian zones: new tiers up to 250 g $9.95 and up to 500 g $11.95, 3–5 kg cut to
  $24.95; the other tiers unchanged; later the same day the owner also moved the Australia-wide free-post threshold from $180 to $150 (WA stays $100) and the pickup promise to "usually ready in 24 hours". Shopify adds its 100 g default package to the
  cart weight before picking a tier, so every boundary was moved 100 g up to match the item weights (`store-content/shipping/README.md`).
- Draft theme "ETS 2026 – Postage shown before checkout (draft 12 Oct)": product pages show "Australia Post from $X" from the lightest
  variant's weight, the cart drawer and cart page get a free-post progress bar (`snippets/ets-shipping-bar.liquid`), and the top bar,
  trust strip, FAQs, delivery page and product FAQ carry the new tiers. The owner publishes it. `store-content/policies/shipping-policy.html`
  updated for the owner to paste.
