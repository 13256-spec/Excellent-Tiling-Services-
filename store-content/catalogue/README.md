# BAT Trims tools catalogue and the store-wide "what fits what" map

Built 12 Oct 2026 after customer feedback that it is hard to tell which items work with which. The owner
photographed the whole BAT Trims Tools Catalogue (books ONE to SIX, pages 1 to 106) and every tool product
in the store was checked against it: title, description, sizes, and what it suits.

## Files

| File | What it is |
|---|---|
| `bat-tools-catalogue.csv` | The catalogue transcribed, 774 rows: `page, code, brand, name, specs, suits`. Machines carry their accessory and part lists in `suits`. Placeholder codes like `SL-(size)` stand for a size or colour range. Brands: BAT 325, Raimondi 319, Sigma 31, Washboy 26, Unitec 24, Marcrist 22, Battipav 13, Kaufmann 6, ADA 4, Bostik 3, Atika 1. |
| `fitmap_all.py` | The store-wide compatibility map as code, every family in one place: mixers and paddles, grout clean-up systems (Washboy, Maximo, Panther, Siri, Raimondi), drilling, wet-saw and grinder blades, bushes, jolly tools, scrapers and blades, waterproofing rollers, knee pads, silicone guns and silicones, sealers, floor drains, Levtop, the full Sigma cutter and parts map, the product-type fixes and the text corrections. |
| `compatibility-all.csv` | The map as data, 370 products: `product_id, vendor, sku, title, role, fits_models, fits_with_ids, fits_with_titles`. |

`fitmap_all.py` reads a Shopify product export (`products.json`, not committed) and writes
`payload.json` plus `compatibility-all.csv`:

```
python3 -I fitmap_all.py products.json out/
```

The payload was applied with alias-batched `productUpdate` calls (25 products per call for titles, types and
metafields; 12 per call for descriptions). Bulk mutations are blocked for this connector.

## The data on every product

| Metafield | Type | Meaning |
|---|---|---|
| `ets.fits_with` | list of products | on a machine or tool: the accessories, blades, sponges and parts that fit it; on a part: the machines and tools it fits |
| `ets.fits_models` | text | plain words: which models, sizes, threads or handles, including ones we do not stock |
| `ets.fits_role` | text, `parent` or `item` | `parent` = a machine, bucket, gun, frame or tool that takes parts; `item` = a part, blade, sponge, paddle, strap or bit. The theme picks its headings from this. Definition gid://shopify/MetafieldDefinition/214721003583. |

Counts after the 12 Oct run: 370 products in the map (110 parents, 247 items, 13 text-only fixes),
`fits_with` on 326, `fits_models` on 356, 71 titles now say what they suit, 55 product types corrected,
186 descriptions open with a bold "Fits:" line (items) or carry a "What fits:" line (parents).
No links in product descriptions: Marketplace Connect copies them to eBay.

## Where it shows

- **Live now, any theme:** the titles, the "Fits:" and "What fits:" lines, the corrected product types, and
  eight manual or smart collections published to the online store and linked from the Raimondi, BAT, Sigma
  and Panther brand collections:

  | Handle | Products |
  |---|---|
  | `grout-clean-up-systems` | 77 |
  | `mixers-paddles-buckets` | 37 |
  | `sigma-cutter-spares` | 56 |
  | `scrapers-knives-blades` | 30 |
  | `silicone-tools` | 22 |
  | `knee-pads-spares` | 14 |
  | `tile-drilling` | 10 |
  | `washboy` (smart, vendor = Washboy) | 9 |

  The seven Raimondi machine collections from `store-content/raimondi/` stay as they are.
- **Draft theme only, until the owner publishes it:** "ETS 2026 – what fits what (draft, not published)",
  gid://shopify/OnlineStoreTheme/144033579071, a duplicate of the live theme made 12 Oct 21:43 Perth time.
  `sections/ets-product-fits.liquid` shows the `fits_with` products as a card grid ("What fits this one"
  on parents, "What this fits" on items) with a "See the whole range" link to the product's system
  collection (the first collection whose handle contains one of the fragments in the section's
  `system_handles` setting), and `snippets/ets-pdp-fits.liquid` puts the `fits_models` text under the
  title with a "See what fits" jump link. Both product templates carry the `fits` block and section.
  The owner's earlier copy of the live theme (144029417535) was deleted, which also removed the Raimondi
  version of the section; the new draft restores it for the whole range. The live theme is never written to.

## Adding a product

1. Set `ets.fits_role` (`parent` or `item`), `ets.fits_models` (plain words) and `ets.fits_with` (the
   machines it fits, or on a machine everything that fits it). Add it to the machines' `fits_with` lists too.
2. Put "suits …" in the title and a "Fits:" first line (item) or "What fits:" line (parent) in the description.
3. Add it to its system collection (`grout-clean-up-systems`, `mixers-paddles-buckets`, …) and, for
   Raimondi, the `raimondi-*` machine collection.
4. Add an `add(...)` line to `fitmap_all.py` and rerun it so `compatibility-all.csv` stays current.

See `store-content/reports/catalogue-check-2026-10-12.md` for what the catalogue corrected, what it
flagged for the owner and which catalogue items are not stocked.
