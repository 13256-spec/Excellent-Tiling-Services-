# Site audit, 11 Oct 2026

Full check of excellenttilingservice.com.au after the repricing, trade pricing and shipping work. Crawl script:
`scratchpad/scripts/crawl.py` (sitemap, every product URL, all collections, pages, blog, policies, every internal link);
catalogue export via `bulkOperationRunQuery`; checkout tests with Playwright and `draftOrderCalculate`.

## What was checked and found fine

- **Every URL works.** 671 product URLs in the sitemap, 72 collections, 10 pages, 4 blog URLs, 4 policies and 208 distinct
  internal links all return 200. No Liquid errors, no "translation missing", no duplicate titles, no noindex except the
  deliberate one on `/collections/trade-essentials`.
- **Breadcrumbs** render on every product and collection page and on 8 of 10 pages (the quote and trade-account landing
  pages have none by design), with `BreadcrumbList` JSON-LD.
- **Structured data**: `LocalBusiness`/`HomeAndConstructionBusiness` (address, phone, email, map) on every page; `WebSite`
  and `FAQPage` on the home page; `Product` (single variant) or `ProductGroup` (multi-variant) with offers, price, availability,
  image, brand and SKU on product pages; `CollectionPage` on collections; `FAQPage` on the delivery, tiling-services and
  trade pages; `Service` on tiling-services; `BlogPosting` on articles. No JSON-LD parse errors.
- **Titles and meta descriptions** present on every product, collection and page (only Shopify's own blog index, policy
  pages and `/collections/all` have none, which can't be set).
- **Shipping rates** (API and real checkout): $331 tap → free standard shipping + paid Australia Post; $7 knife → $15;
  tiles to NSW/VIC → freight quote only; primers over $180 → free road rate; tiles to Perth → Local delivery $95.
- All 48 tiles, every bath, toilet, vanity, shower screen, 3 m trim, Sigma cutter over 95 cm, Baron mixer and Raimondi
  machine sit in the Perth-only delivery profile (213 products), so none of them gets the free $180 postage.
- Google Shopping: AU feed approved; 115 BAT trim images with a Google-side error that Google retries itself; 1 price
  mismatch (Strip Punched Linear Drain 900 mm) that clears on the next sync; ~400 new products waiting for Google to crawl.

## Fixed today

| Problem | Fix |
|---|---|
| 336 active products (May BAT import, both Raimondi batches) were in no storefront collection: unreachable from menus, only by search | Smart-collection rules extended to the newer product types; `hardware` 335 → 684 products, `trowels-tiling-tools` 97 → 258, `tile-cutters-accessories` 80 → 163, `diamond-blades-drill-bits` 14 → 58, `tile-spacers-wedges` 24 → 48, `silicone-additives-cleaners` 29 → 50, `floor-drains-wastes` 24 → 27 |
| 144 Raimondi products imported today with no price check, no trade band, no trade list | Priced by the playbook (22 variants cut to the 40% cap), bands set, trade lists updated; `store-content/pricing/reports/reprice-2026-10-11-raimondi-batch2.md` |
| Tile supplier named in 3 collection meta descriptions (`matt-tiles`, `tiles-300x300`, `tiles-300x600`) | Rewritten without the supplier |
| "free on orders over $1,000" still in 5 tapware collection descriptions and 7 spacer product descriptions | Changed to $180 |
| 16 spacer/wedge products had no meta description | Written from the first sentence of each description |
| 42 product images on 22 products had no alt text (Sigma cutters, linear drain, Maxisil, trowels, Baron mixers) | Alt text set to the product name |
| Perth tiles checkout showed two $95 options (my "Perth metro delivery" and Shopify's own Local delivery) and the metro rate also appeared for Mandurah/regional WA | Duplicate rates deleted; the WA zone keeps the freight quote, renamed and described for regional WA |
| Legal shipping policy still said free shipping over $1,000 | Owner pasted the rewritten policy (live, dated 11 Oct) |
| No backup theme existed after the trade-bar theme went live | "ETS backup 11 Oct 2026 (trade bar live)" duplicated from the live theme |

## Still open (owner or later work)

- **Photos (updated 11 Oct, night)**: of the 54 products tagged `photo-needed`, 24 Raimondi products now have a manufacturer
  photo (from raimondispa.com or BAT Trims, the official Australian distributor) and the tag was removed. 30 still have none:
  all 15 BAT items (trowels, scrapers, knives, buckets, the BAT Luxe drain), 2 Panther buckets, 2 NICLIS items (grate,
  bandage), 6 BATSEAL sealers and cleaners, and 7 Raimondi spares (Rai-Cut blade, Lupetto plate, transformer, Ipertitina
  skirt and connectors, Clipdozer) that have no photo anywhere online. Four found photos were deliberately not used (a 6-cup
  photo for the 4-cup Easymove set, the Power Raizor unit shown with a grinder that isn't included, the premium disc photo for
  the economy 250 mm blade, a 407 px Lupetto crop). Full list with sources: `photos-sourced-2026-10-11.csv`. The 30 need
  photos from BAT Trims (info@battrims.com) or a phone photo in the showroom.
- **Raimondi Bulldog Profiling Machine** is a draft (hidden); **BAT Bright Steel Long Blade Trowel** is sold out; two archived
  BAT trims have a $0 price (archived, not visible).
- **Local delivery settings** (Shopify admin, not readable by the API): check "free over $2,000" and the minimum order match the
  policy. The $0 freight-quote line is still listed first for Perth customers because Shopify sorts rates by price.
- **Google Search Console is not connected** to the analytics tool, so indexing coverage could not be checked. Connect it in
  HYPD or share access.
- **Sitemap lag**: Shopify's cached sitemap lists 671 of 921 active products; the 250 products created today appear after the
  next regeneration. The collection fix gives them crawlable links in the meantime.
- **Page weight**: the home page HTML is 630 KB (mega menu with product cards on every page, 131 scripts, 28 render-blocking),
  time to interactive 4.1 s on a desktop test, LCP 2.9 s. Worth trimming the menu product cards and app scripts later.
- Homepage/menu images render with empty alt (theme sections drop the file alt); decorative, low priority.
