# Product description rewrite brief (24 Oct 2026)

Owner's instruction: "most product descriptions are so little. Search online for the product and add more about it to help
customers shop. Keep language appropriate." He also flagged that lines like "Price: $29.95 per bag. In stock at our
Maddington showroom. Trade accounts get their discount at checkout." are NOT customer-facing and must not appear.

## What a finished description looks like

HTML only (no inline styles, no scripts, no images). 90 to 200 words. Structure:

1. `<p>` One or two sentences a Perth renovator or tiler would want first: what it is, what it is for, the one thing that
   makes it worth buying (benefit, then the fact behind it). Name the brand and model naturally.
2. `<h3>` sections as they apply (use only the ones with real content): "Use it for", "Features", "Specifications",
   "What's in the box", "Fits" / "Compatible with", "Good to know" (limits, care, prep, pairing items).
   `<ul><li>` bullets, short, one fact each.
3. Keep every true fact that is already in the old description (sizes, finishes, materials, codes, pack sizes).
4. Finish with nothing: no price, no shipping promise, no call to action. The page already shows price, stock and delivery.

## Voice (from .claude/agents/ets-copy-review.md)

Plain Aussie English, short sentences, contractions fine. Specific and real. No hype: never "elevate", "transform",
"stunning", "seamless", "curated", "timeless", "discover", "unlock", "premium quality", "look no further", "perfect for
any", three adjectives in a row. No exclamation marks. No em dashes.

## Hard rules

- NEVER put a price, "trade", "trade account", "in stock", "showroom", "Maddington", "we deliver", "pick up", "shipping",
  "link in bio" or any internal note (SKU codes as the subject, "MOQ", "supplier", "profile", "needs cost") in a description.
  A manufacturer code is fine inside a Specifications bullet ("Model: PAL.SA.001").
- NEVER name the tile supplier (Eternity / Eternity Tiles) or the bathroomware importer (DSA) or Bathroom City. Brand names
  that customers know (MELA, Sika, Raimondi, Sigma, BAT, Maxisil, Roberts Designs, Panther, Washboy, Baron, Siri, Barwalt,
  Celine, Chloe) are fine.
- NEVER invent a spec. Every size, rating, material, warranty, capacity, coverage or compatibility must come from the
  manufacturer or distributor website, a data sheet, the existing description, or the product title/options. If you cannot
  verify a detail, leave it out. If you can verify nothing new online, still rewrite for a customer using only what is
  certain (title, options, type, old description) and general use guidance for that product category, and mark the record
  `"verified": false`.
- No "cheaper than", "best price", review claims, stock-level or delivery-speed claims, no warranty length unless sourced.
- Keep the product title, price, tags, SEO fields, images and metafields untouched. Change `descriptionHtml` only.

## Research

- WebSearch / WebFetch / curl are available. Manufacturer first, then the Australian distributor, then a reputable retailer.
- Roberts Designs (also stocks Raimondi, Sigma, Siri, Baron, Barwalt, Panther, Washboy): the public Store API returns the
  full description without login:
  `curl -s "https://robertsdesigns.com.au/wp-json/wc/store/v1/products?search=<sku or name>&per_page=5"` (fields
  `description`, `short_description`, `attributes`). Product pages: robertsdesigns.com.au/product/<slug>/.
- Raimondi: raimondispa.com (product pages have specs, PDFs). Sigma: sigmaitalia.com / sigma.it. Siri: siri.it.
  Baron mixers: baronmixers (via Roberts). BAT trims and tools: battrims.com.au. Maxisil: maxisil.com.au. Panther:
  panther levelling (via Roberts). Sika: aus.sika.com.
- MELA: bathroom-city.com.au/products/<handle>. Local copies already fetched:
  `store-content/mela-specs/mela-specs-2026-10-14.json` (field `bc` = Bathroom City handles) and
  `store-content/mela-specs/bathroom-city-product-info-2026-10-14.json` (kv pairs and notes per handle), plus the MELA
  warranty/care facts in `store-content/mirrors/README.md`.
- Celine / Chloe bathroomware, kitchen sinks, floor drains, tallboys sold under vendor "Excellent Tiling Services":
  `store-content/supplier-sync/dsa-bathroomware-2026-10-14.json` has what we were given; search the web for the model
  name for more (Celine and Chloe are DSA ranges, do not name DSA).
- Tiles (vendor "Excellent Tiling Services", type Tile): `store-content/pricing/eternity-tiles-2026-10-05.csv` and
  `store-content/pricing/eternity-price-list-2026-10-05.txt` have sizes, finishes, slip ratings, box coverage. Search the
  tile name online for the range description. Never name the supplier. Tiles are sold per m² to the nearest full box:
  keep that sentence.

## Output and apply

1. Write `store-content/descriptions/<group>-2026-10-24.json`: a list of
   `{"id", "handle", "title", "old", "new", "sources": [urls or local file names], "verified": true|false, "notes"}`.
   Write it incrementally (every 10 products) so nothing is lost if you are interrupted.
2. Check every `new` against the hard rules (a script that greps for "$", "trade", "stock", "showroom", "Maddington",
   "deliver", "pick up", "shipping", "Eternity", "DSA", "Bathroom City", "elevate", "stunning", "seamless", "!" is the
   minimum). Fix before applying.
3. Apply to Shopify with `mcp__Shopify__graphql_mutation` (load it with ToolSearch `select:mcp__Shopify__graphql_mutation`):
   aliased `productUpdate(product:{id, descriptionHtml})` calls, about 8 products per mutation, and check `userErrors`.
   Pass the HTML as a GraphQL variable or escape it properly. Record any failures in the JSON (`"applied": false`).
4. Do not run git. Report back: how many rewritten, how many verified online, how many applied, anything you could not
   find, and three example before/after pairs.
