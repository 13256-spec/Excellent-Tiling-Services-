# Excellent Tiling Services – working notes for Claude

Read this before touching anything. The owner is busy and not technical: answer in plain English, short sentences.

## The business

**Excellent Tiling Services Pty Ltd** (ABN 63 150 082 054), 17A Olga Road, Maddington WA 6109. A WA tiling trade
supplier run by working tilers, trading since 2011. Live Shopify store **excellenttilingservices.com**
(`0mthrd-hk.myshopify.com`, Shopify plan, AUD, AWST): tiles, tile adhesive/grout/tools, bathroomware, tapware,
vanities, mirrors, heated towel rails. Positioning: trade-first, bathroom/renovation range second. Showroom is
**by appointment only**, Mon–Sat 4:30–9 pm. Phone 0450 960 543 (answered any time).

**House brand** (name in `brand/tokens.json` -> `brand.name`; vendor on every product): our own label of bathroom
tapware (basin mixers, wall mixers, bath spouts, shower sets) made for us by a Chinese manufacturer and sold through the
existing store as our own brand, the way Bathroom City sells MELA. It is an addition to the live store, never a new build.

## Hard rules (non-negotiable, every file, every write)

1. **Never show or reference supplier or manufacturer names** anywhere a customer can see: product copy, titles, vendor,
   tags, SEO titles/descriptions, image alt text, knowledge base, price lists, social posts, JSON-LD. The only exception
   is Roberts Designs on its own-label products. Supplier names live only in the internal `ets.supplier` metafield and
   in `store-content/`. (Eternity for tiles is the long-standing example of this rule.)
2. **Never say publicly that we order stock on demand**, or any "order in", "made to order", "ships from supplier" wording.
3. **No product goes live without WaterMark and WELS data.** `ets.watermark_licence_number`, `ets.wels_registration`
   and `ets.wels_rating` must all be filled before a plumbing product is set Active. This is a hard gate in
   `scripts/import_supplier.py`; a product missing any of them stays Draft and is reported to the owner. Don't work
   around it, and if supplier data contradicts a compliance requirement, stop and tell the owner.
4. **Cost per item in Shopify is recorded with GST added**: supplier ex-GST (landed) price x 1.1.
5. **All products track inventory and continue selling when out of stock** (`inventoryPolicy: CONTINUE`, `tracked: true`).
6. **Every listing carries the supplier's product code in the SKU field**, normalised (`scripts/import_supplier.py`).
7. **Never push to the live theme or write to live products without telling the owner first.** All theme work happens on
   an unpublished dev theme; the owner publishes from Online Store -> Themes. The Shopify MCP connector blocks writes to
   the MAIN theme anyway.
8. **Ask before anything expensive to reverse**: SKU scheme, metafield namespace, URL structure, collection handles.
9. **Commit at each milestone** with a clear message.

Pricing rules (public floor cost x 1.1 x 1.25, trade floor 20 % margin ex GST, MELA never under Bathroom City) are in
`store-content/pricing/PRICING-PLAYBOOK.md` and apply to the house brand too.

## Repo map

| Path | What |
| --- | --- |
| `theme/` | Custom files of the live Horizon-based theme ("ETS 2026 – Premium"): every `ets-*` asset/section/snippet, layout, templates, settings. Stock Horizon files are not duplicated. Synced from live 2 Nov 2026. |
| `brand/` | Design tokens (`tokens.json`) and `build.py` -> `theme/assets/ets-tokens.css` + `brand/email.css`. |
| `data/metafields/` | Product metafield definitions (`definitions.json`) and generated `mutations.graphql`. |
| `scripts/` | `import_supplier.py` (manufacturer spreadsheet -> Shopify import, dry-run by default), `metafield_mutations.py`, tests. |
| `store-content/` | Pricing playbook and price lists, supplier sync records, policies, shipping, SEO notes. |
| `seo/`, `marketing/`, `lighthouse/` | SEO scripts and data, marketing assets, Lighthouse baselines. |
| `.claude/agents/` | Marketing, pricing, social, calendar agents. |

## Theme workflow

- Live theme: "ETS 2026 – Premium (draft)" (`gid://shopify/OnlineStoreTheme/144742973503`, role MAIN). Do not write to it.
- Work on an unpublished duplicate (Shopify admin -> Themes -> ... -> Duplicate, or `themeDuplicate`), upload files with
  `themeFilesUpsert` or `shopify theme push --theme <id>`, preview, then the owner publishes.
- Local development: `shopify theme dev --store 0mthrd-hk.myshopify.com --path theme` serves a **development theme**
  (never the live one). See README "Theme on GitHub and Shopify CLI".
- Re-sync `theme/` from the live theme after anyone edits in the theme editor (compare `checksumMd5` from the Admin API).
- Match the existing design language: tokens in `brand/tokens.json`, serif display (Instrument Serif), Manrope body,
  ink/brass/stone palette, hairlines not boxes. No second visual system.

## Metafield schema (namespace `ets`, owner PRODUCT)

Source of truth: `data/metafields/definitions.json`. Reused existing definitions: `wels_registration`, `wels_rating`
(text, "5 Star"), `flow_rate` (text, "6 L/min"), `material`, `warranty` (legacy text), `cartridge` (legacy "35mm"),
`range` (suite name), `supplier` (internal), `lead_time`, `trade_band`, `width_mm`/`height_mm`/`depth_mm`.

New for the house brand (all storefront `PUBLIC_READ`):

| Key | Type | Notes |
| --- | --- | --- |
| `watermark_licence_number` | single_line_text | mandatory (gate), pinned |
| `watermark_certifier` | single_line_text | mandatory in practice, pinned |
| `finish` | list.single_line_text | choices: Chrome, Matt Black, Brushed Nickel, Brushed Brass, Gunmetal |
| `cartridge_brand` | single_line_text | |
| `cartridge_size_mm` | number_integer | 10–60 |
| `max_pressure_kpa` | number_integer | 50–2000 |
| `installation_type` | single_line_text | Deck mounted, Wall mounted, In-wall, ... |
| `spout_projection_mm`, `spout_height_mm` | number_integer | |
| `warranty_years` | number_integer | theme shows it when `warranty` text is empty |
| `spec_sheet`, `installation_guide` | file_reference (PDF) | Downloads panel on the product page |

Where the theme reads them: `sections/ets-product-specs.liquid` (spec table, compliance panel, downloads),
`snippets/ets-pdp-compliance.liquid` (WELS stars + WaterMark badge under the price),
`snippets/ets-product-schema.liquid` (JSON-LD `hasCertification`, `additionalProperty`).

## House-brand conventions

- **Vendor** = brand name. **Collection** `/collections/<brand-handle>` (smart: vendor equals brand) uses
  `templates/collection.brand.json` (landing page). **Suites**: one smart collection per range, handle
  `<brand-handle>-<range-handle>` (vendor equals brand AND tag equals `suite-<range-handle>`), template
  `collection.suite.json`. Product metafield `ets.range` = the range name; the theme derives the suite handle from it.
- **Finishes are variants** (option `Finish`), one product per model, so one URL per mixer: no finish-level pages to
  cannibalise each other. `canonical_url` already drops `?variant=`. Finish spelling follows the store ("Matt Black").
  Variant images carry the finish; the Horizon variant picker shows swatches once the Finish option is linked to a
  metaobject with a colour (standard `shopify--color-pattern`), which the import creates.
- **SKU** = `[prefix]<MODEL>-<FINISH CODE>` where MODEL is the supplier's model code upper-cased with spaces and
  punctuation removed, finish codes CP/MB/BN/BB/GM (`scripts/import_config.json`). Raw supplier code stays in the SKU
  body as required by the owner.
- **Tags**: `house-brand`, `<Type>`, `WELS <n> Star`, `suite-<range>`, `ship-parcel|ship-bulky|ship-local-only`,
  `ebay-post-15|20|29|39|59` or `ebay-pickup-only` (Marketplace Connect; untagged = Local Pickup only).
- **Pricing** per `scripts/import_config.json`: landed AUD ex GST = FOB x FX x (1 + duty) + freight + other; unit cost
  = landed x 1.1; price = landed x markup x 1.1 rounded to x.95, never under cost_inc x 1.25; trade band = deepest of
  25/20/15/10/5 that keeps 20 % margin ex GST; `ets.trade_band` set and the product listed for the `trade-list-N` collection.

## Brand tokens (`brand/tokens.json`)

Colour: bg `#FFFFFF`, bg-2 `#F5F2EC`, ink `#15213A`, ink-soft `#3A4556`, muted `#6A6862`, brass `#9C7744`,
brass-soft `#EFE6D6`, trade `#1F6149`, dark `#0F1A2C`, line `rgba(21,33,58,.12)`. Finish swatches: chrome `#C9CDD2`,
matt-black `#1C1C1E`, brushed-nickel `#A9AAA6`, brushed-brass `#B5945C`, gunmetal `#4B5057`.
Type: Instrument Serif 400 for display/h1/h2 (display `clamp(40px,5vw,72px)`, h2 `clamp(32px,3.4vw,50px)`), Manrope for
everything else (body 16px/1.6, small 13px, eyebrow 11.5px tracked .16em uppercase). Space: section `clamp(72px,8vw,128px)`,
gutter `clamp(16px,4vw,48px)`, max width 1360px, scale 4/8/12/16/24/32/48/64. Radius 6/10/14/pill.
`python3 brand/build.py` regenerates `theme/assets/ets-tokens.css` (loaded last in `layout/theme.liquid`) and
`brand/email.css` (paste into Shopify notification / Klaviyo templates so emails match the site).

## Supplier import

`python3 scripts/import_supplier.py <sheet.xlsx> [--out data/imports/<date>]` is a **dry run**: writes `report.md`,
`payload.json` (productSet inputs) and `import.csv`, and prints what would change. `--apply` writes to Shopify
(needs `SHOPIFY_STORE` and `SHOPIFY_ADMIN_TOKEN`); products are created as Draft; `--publish` sets Active only
for products that pass the WaterMark/WELS gate. Self-check: `python3 scripts/test_import_supplier.py`.
