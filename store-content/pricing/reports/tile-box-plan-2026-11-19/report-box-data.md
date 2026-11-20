## Box data for the 84 `m2-units` tile variants (read-only, 19 Nov 2026)

**Short answer: no source in the repo, in Shopify or on eternitytiles.com.au states m² per box, pieces per box or kg per box for any of our tiles.** The only box figure anywhere is "Box coverage: 1.44 m²" on two products, copied from an old store description of unknown origin. Everything else is UNKNOWN. The supplier figure that does exist is **pallet quantity in m²** (price list), which is consistent with 1.44 m² boxes for the 300x600 / 600x600 / 600x1200 sizes but does not prove it.

### What each source holds

| Source | Box / pcs / kg data? | Notes |
|---|---|---|
| `/home/user/Excellent-Tiling-Services-/store-content/pricing/eternity-price-list-2026-10-05.txt` | **No.** Columns are Product, Pallet QTY (m²), RRP, non-pallet, pallet, mixed 3+ price (header lines 9-13, 71-75 ... 587-591). No box, pcs, m²/box or kg column anywhere (grep `box|pcs|pieces|carton` only hits the header word "pallet"). | Pallet QTY per code: 57.6 m² (all 298/300x600 and 600x600 porcelain), 86.4 m² (300x600 ceramic wall, lines 80-112), 40.32 m² (600x1200 Cement/Morgan, lines 155/223/236), 55.44 m² (299x299 Morgan, lines 162/185), 111.36 m² (100x300 Subway, lines 18/25), 92 m² (75x300 Subwave, lines 32-53), TBC (YW277314 line 320, YW277315 line 341, HSA223111 line 568), n/a (ETSN126631 line 142). |
| `/home/user/Excellent-Tiling-Services-/store-content/pricing/eternity-tiles-2026-10-05.csv` | **No.** Columns (line 1): variant_id, inventory_item, product, variant, sku, price, new_sku, rrp, cost_ex, pallet_ex, mixed3_ex, **pallet_qty**, new_price, margins, note. | pallet_qty only (same values as the price list). |
| `/home/user/Excellent-Tiling-Services-/store-content/pricing/eternity_2026_10.py` | **No.** `LIST` dict lines 17-50: `(RRP, non pallet, pallet, mixed 3+, pallet qty m2)`. | No box fields. |
| `/home/user/Excellent-Tiling-Services-/store-content/supplier-sync/eternity_tile_plan.json` | **No.** Single key `tile_sku`: `[product_id, variant_id, sku, title, variant]` x 84. | ID map only. |
| `/home/user/Excellent-Tiling-Services-/store-content/supplier-sync/drive-eternity-2026-11-10/` | **No.** `README.md` (photos, basins), `photo-plan.json`, `photo_prep.py`, `drafts-created-2026-11-10.json` (5 basins). Zero hits for box/carton/pcs/m2/kg. | README lines 3-6 say the drive's "Product Information zips" and docs were copied to `Eternity/`, but `/home/user/Excellent-Tiling-Services-/Eternity/` in this checkout holds only `README.md` + `eternity-tapware-catalogue-wholesale-2025.pdf`; `Eternity/README.md` lines 29-31 say the tile files (`eternity-porcelain-tile-codes-2026-11-09.xlsx`, test reports) are in the owner's local clone, **not pushed**. |
| `/home/user/Excellent-Tiling-Services-/store-content/pricing/eternity-swatches/` | 20 PNG swatches only (arrow-crystal-white-mosaic ... sand-white-tile). | No data. |
| `/home/user/Excellent-Tiling-Services-/store-content/pricing/store-pricing-2026-10-03.csv` tile rows (lines 601-646, 48 rows) | **No.** flag column says "per m2; sold in 0.01 m2 units ... Shopify price = this / 100 (5 Nov 2026)". | No box columns. |
| `/home/user/Excellent-Tiling-Services-/store-content/descriptions/tiles-2026-10-24.json` lines 6, 36 (old descriptions); `store-content/descriptions/gen_tiles_2026_10.py` lines 54, 72 | **"Box coverage: 1.44m²"** for Time Stone Moon and Time Stone Charcoal only. `store-content/descriptions/README.md:58`: "box coverage is only known for Time Stone Moon and Charcoal (1.44 m2)". | Origin of the 1.44 is not recorded; it was in the pre-October store copy and was applied to the whole product (both 300x600 and 600x600). |
| Shopify (43 products, 84 variants, query `tag:m2-units`, 1 page, hasNextPage false) | **No supplier box data.** Every variant: `unitPriceMeasurement 0.01 M2 / 1 M2`, weight 0.22 kg (porcelain) or 0.15 kg (ceramic) per 0.01 m² unit, variant metafields `shipping.box_size` + `custom.trade_price` only, product metafields ets.supplier / ets.trade_band / ets.trade_price / SEO / google category only. Descriptions: "Sold per square metre and supplied to the nearest full box" on all 43; "Box coverage: 1.44 m²" only on Time Stone Moon and Charcoal. | `shipping.box_size` ("64 x 34 x 6 cm", "64 x 64 x 6 cm", "124 x 64 x 6 cm", "34 x 34 x 6 cm", "124 x 24 x 6 cm", "34 x 14 x 6 cm") is **derived from the tile size**, not supplier data: `/home/user/Excellent-Tiling-Services-/store-content/shipping/estimate_weights.py:55-59` (`tile size + 4 cm`, 6 cm, "~22 kg/m2" estimate); `store-content/shipping/other_products_shipping.py:5` (ceramic wall tiles 15 kg/m²). So the Shopify weights are estimates too (22 kg/m² porcelain, 15 kg/m² ceramic). The four Subwave 75x300 variants carry "64 x 64 x 6 cm", clearly wrong for a 75x300 tile. |
| eternitytiles.com.au (`/products.json?limit=250` pages 1-2, `/products/<handle>.js`, product HTML for astra-white-matt-tile, time-stone-moon-premium-range-tile, cement-white-standard-porcelain-range-tile) | **No.** `unit_price` and `unit_price_measurement` are `null`, `weight`/`grams` 0, `quantity_rule {min 1, increment 1}`, `body_html` = "This product is sold per sqm, to the nearest full box size." Nothing else in the page HTML about box size, pieces or kg. | Eternity's own store sells per whole m² (qty 1 = 1 m² at the RRP), not per box, and publishes no box size. |

### Per-variant table

Legend: size as in the Shopify variant title (price list nominal size after). `m2_per_box` / `pcs_per_box` / `kg_per_box` = UNKNOWN unless stated. "PL" = `/home/user/Excellent-Tiling-Services-/store-content/pricing/eternity-price-list-2026-10-05.txt`; "pallet" = that line's Pallet QTY column. All 84 variants in Shopify have weight 0.22 kg/unit (porcelain) or 0.15 kg/unit (ceramic) = estimate, not supplier data.

| product | variant | sku | size | m2_per_box | pcs_per_box | kg_per_box | source | confidence |
|---|---|---|---|---|---|---|---|---|
| Time Stone Moon | 300x600mm / Matt | YFR630331 | 298x600x9.5 | 1.44 (claimed) | UNKNOWN | UNKNOWN | descriptions/tiles-2026-10-24.json:6 ("Box coverage: 1.44m²", old copy, origin unrecorded); PL:476 (listed as YSR630331) pallet 57.6 m² | low |
| Time Stone Moon | 600x600mm / Matt | YFR600331 | 600x600x9.5 | 1.44 (claimed) | UNKNOWN | UNKNOWN | same; PL:479 pallet 57.6 m² | low |
| Time Stone Moon | 300x600mm / Lappato | BS630331 | 298x600x9.5 | 1.44 (claimed) | UNKNOWN | UNKNOWN | same; PL:482 pallet 57.6 m² | low |
| Time Stone Moon | 600x600mm / Lappato | BS600331 | 600x600x9.5 | 1.44 (claimed) | UNKNOWN | UNKNOWN | same; PL:486 pallet 57.6 m² | low |
| Time Stone Cinder | 300x600mm / Matt | YFR630338 | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:493 pallet 57.6 m² | - |
| Time Stone Cinder | 600x600mm / Matt | YFR600338 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:496 pallet 57.6 m² | - |
| Time Stone Cinder | 300x600mm / Lappato | BS630338 | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:499 pallet 57.6 m² | - |
| Time Stone Cinder | 600x600mm / Lappato | BS600338 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:503 pallet 57.6 m² | - |
| Time Stone Charcoal | 300x600mm / Matt | YFR630337 | 298x600x9.5 | 1.44 (claimed) | UNKNOWN | UNKNOWN | descriptions/tiles-2026-10-24.json:36; PL:530 pallet 57.6 m² | low |
| Time Stone Charcoal | 600x600mm / Lappato | BS600337 | 600x600x9.5 | 1.44 (claimed) | UNKNOWN | UNKNOWN | same; PL:540 pallet 57.6 m² | low |
| Time Stone Sand | 300x600mm / Lappato | BS630332 | 298x600 | UNKNOWN | UNKNOWN | UNKNOWN | not on PL (drive-eternity-2026-11-10/README.md:16-18) | - |
| Lava Etna | 300x600mm / Matt | HW637317 | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:376 pallet 57.6 m² | - |
| Lava Etna | 600x600mm / Matt | YW607317 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:379 pallet 57.6 m² | - |
| Lava Ash | 300x600mm / Matt | HW637311 | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:297 pallet 57.6 m² | - |
| Lava Ash | 600x600mm / Matt | YW607311 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:300 pallet 57.6 m² | - |
| Lava Ash | 300x600mm / Gloss | FG637311 | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:303 pallet 57.6 m² | - |
| Lava Ash | 600x600mm / Gloss | FG607311 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:307 pallet 57.6 m² | - |
| Lava Kraka | 300x600mm / Matt | HW637315 | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:335 pallet 57.6 m² | - |
| Lava Kraka | 300x600mm / Gloss | FG637315 | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:345 pallet 57.6 m² | - |
| Lava Kraka | 600x600mm / Matt | YW607315 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:338 pallet 57.6 m² | - |
| Lava Kraka | 600x600mm / Gloss | FG607315 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:349 pallet 57.6 m² | - |
| Lava Kraka | 600x1200mm / Gloss | YW277315 | 1200x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:341 pallet TBC | - |
| Lava Vesuv | 300x600mm / Matt | HW637314 | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:314 pallet 57.6 m² | - |
| Lava Vesuv | 600x600mm / Matt | YW607314 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:317 pallet 57.6 m² | - |
| Lava Vesuv | 300x600mm / Gloss | FG637314 | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:324 pallet 57.6 m² | - |
| Lava Vesuv | 600x600mm / Gloss | FG607314 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:328 pallet 57.6 m² | - |
| Lava Vesuv | 600x1200mm / Gloss | YW277314 | 1200x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:320 pallet TBC | - |
| Terrazzo Lumina | 300x600mm / Matt | YFR632950 | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:466 pallet 57.6 m² | - |
| Terrazzo Lumina | 600x600mm / Matt | YFR602950 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:469 pallet 57.6 m² | - |
| Terrazzo White | 300x600mm / Matt | DSA36CP01N | 299x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:253 pallet 57.6 m² | - |
| Terrazzo White | 600x600mm / Matt | DSA66CP01N | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:256 pallet 57.6 m² | - |
| Particle Grey | 300x600mm / Matt | ET36SS03 | 299x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:270 pallet 57.6 m² | - |
| Particle Warm | 300x600mm / Matt | ET36SS01 | 299x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:263 pallet 57.6 m² | - |
| Morgan Dusk | 300x300mm / Matt | DSA33AK666 | 299x299 | UNKNOWN | UNKNOWN | UNKNOWN | PL:185 pallet 55.44 m² | - |
| Morgan Dusk | 300x600mm / Matt | DSA36AK666 | 299x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:188 pallet 57.6 m² | - |
| Morgan Dusk | 600x600mm / Matt | DSA66AK666 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:191 pallet 57.6 m² | - |
| Morgan Storm | 300x600mm / Matt | DSA36AK663 | 299x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:175 pallet 57.6 m² | - |
| Morgan Storm | 600x600mm / Matt | DSA66AK663 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:178 pallet 57.6 m² | - |
| Morgan Cloud | 300x300mm / Matt | DSA33AK662 | 299x299x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:162 pallet 55.44 m² | - |
| Morgan Cloud | 300x600mm / Matt | DSA36AK662 | 299x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:165 pallet 57.6 m² | - |
| Morgan Cloud | 600x600mm / Matt | DSA66AK662 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:168 pallet 57.6 m² | - |
| Morgan Hail | 300x600mm / Matt | DSA36AK661 | 299x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:149 pallet 57.6 m² | - |
| Morgan Hail | 600x600mm / Matt | DSA66AK661 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:152 pallet 57.6 m² | - |
| Morgan Hail | 600x1200mm / Matt | DSA126AK661 | 1200x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:155 pallet 40.32 m² | - |
| Cement Dark Grey | 300x600mm / Matt | DSA36MQ04 | 299x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:243 pallet 57.6 m² | - |
| Cement Dark Grey | 600x600mm / Matt | DSA66MQ04 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:246 pallet 57.6 m² | - |
| Cement White | 300x600mm / Matt | DSA36MQ01 | 299x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:217 pallet 57.6 m² | - |
| Cement White | 600x600mm / Matt | DSA66MQ01 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:220 pallet 57.6 m² | - |
| Cement White | 600x1200mm / Matt | DSA126MQ01 | 1200x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:223 pallet 40.32 m² | - |
| Cement Grey | 300x600mm / Matt | DSA36MQ02 | 299x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:230 pallet 57.6 m² | - |
| Cement Grey | 600x600mm / Matt | DSA66MQ02 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:233 pallet 57.6 m² | - |
| Cement Grey | 600x1200mm / Matt | DSA126MQ02 | 1200x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:236 pallet 40.32 m² | - |
| Fumosa | 600x600mm / Matt | ETSN6631 | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:139 pallet 57.6 m² | - |
| Fumosa | 600x1200mm / Matt | ETSN126631 | 1200x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:142 pallet n/a | - |
| Astra White | 300x600mm / Matt | DSA36AW | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:386 pallet 57.6 m² | - |
| Astra White | 600x600mm / Matt | DSA66AW | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:389 pallet 57.6 m² | - |
| Astra Greige | 300x600mm / Matt | DSA36AG | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:396 pallet 57.6 m² | - |
| Astra Greige | 600x600mm / Matt | DSA66AG | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:399 pallet 57.6 m² | - |
| Sand White | 300x600mm / Matt | DSA36SW | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:406 pallet 57.6 m² | - |
| Sand White | 600x600mm / Matt | DSA66SW | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:409 pallet 57.6 m² | - |
| Sand Beige | 300x600mm / Matt | DSA36SB | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:416 pallet 57.6 m² | - |
| Sand Beige | 600x600mm / Matt | DSA66SB | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:419 pallet 57.6 m² | - |
| Sand Grey | 300x600mm / Matt | DSA36SG | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:426 pallet 57.6 m² | - |
| Sand Grey | 600x600mm / Matt | DSA66SG | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:429 pallet 57.6 m² | - |
| Bianco Greco | 300x600mm / Matt | DSA36BG | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:456 pallet 57.6 m² | - |
| Bianco Greco | 600x600mm / Matt | DSA66BG | 600x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:459 pallet 57.6 m² | - |
| Caliza | 300x600mm / Matt | YF637300 | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:547 pallet 57.6 m² | - |
| E-Time Calcare | 300x600mm / Structured | YW633164 | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:554 pallet 57.6 m² | - |
| E-Time Chiaro | 300x600mm / Structured | YW633165 | 298x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:561 pallet 57.6 m² | - |
| Oak Aube Timber Look | 200x1200mm / Matt | HSA223111 | 196x1200x9 | UNKNOWN | UNKNOWN | UNKNOWN | PL:568 pallet TBC | - |
| Arena Light | 300x600mm / Lappato | BV637544 | 300x600 | UNKNOWN | UNKNOWN | UNKNOWN | not on PL (tagged price-check / needs-photo in Shopify) | - |
| Arena Blonde | 300x600mm / Lappato | BV637541 | 300x600 | UNKNOWN | UNKNOWN | UNKNOWN | not on PL (tagged price-check / needs-photo) | - |
| Subway Gloss White Ceramic | 100x300mm / Gloss | DSA31001G | 100x300x8 | UNKNOWN | UNKNOWN | UNKNOWN | PL:18 pallet 111.36 m² | - |
| Subway Matt White Ceramic | 100x300mm / Satin | DSA31002M | 100x300x8 | UNKNOWN | UNKNOWN | UNKNOWN | PL:25 pallet 111.36 m² | - |
| Subwave Gloss White Ceramic | 75x300mm / Gloss | DSA730WAW1 | 75x300x8 | UNKNOWN | UNKNOWN | UNKNOWN | PL:32 pallet 92 m² | - |
| Subwave Matt White Ceramic | 75x300mm / Satin | DSA730WAW1M | 75x300x8 | UNKNOWN | UNKNOWN | UNKNOWN | PL:39 pallet 92 m² | - |
| Subwave Nude Ceramic | 75x300mm / Gloss | DSA730WBC7 | 75x300x8 | UNKNOWN | UNKNOWN | UNKNOWN | PL:46 pallet 92 m² | - |
| Subwave Grey Ceramic | 75x300mm / Gloss | DSA730WBC6 | 75x300x8 | UNKNOWN | UNKNOWN | UNKNOWN | PL:53 pallet 92 m² | - |
| White Ceramic Wall | 300x600mm / Gloss | DSA36001 | 300x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:80 pallet 86.4 m² | - |
| White Ceramic Wall | 300x600mm / Matt | DSA36002M | 300x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:84 pallet 86.4 m² | - |
| Eternal Marble Ceramic Wall | 300x600mm / Gloss | DSA60822 | 300x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:91 pallet 86.4 m² | - |
| Eternal Carrara Ceramic Wall | 300x600mm / Gloss | DSA60602 | 300x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:98 pallet 86.4 m² | - |
| Element Grey Ceramic Wall | 300x600mm / Gloss | DSA6049 | 300x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:105 pallet 86.4 m² | - |
| Whisper Grey Ceramic Wall | 300x600mm / Gloss | DSA60871 | 300x600x9.5 | UNKNOWN | UNKNOWN | UNKNOWN | PL:112 pallet 86.4 m² | - |

Totals: 84 variants, 43 products. m²/box stated for 6 variants (low confidence, same 1.44 figure for both sizes of two products), UNKNOWN for 78. pcs/box and kg/box UNKNOWN for all 84.

### Inferences from the pallet column (not data, flagged as inference)

- 57.6 m² = 40 x 1.44; 86.4 m² = 60 x 1.44; 40.32 m² = 28 x 1.44. All three pallet sizes divide exactly by 1.44 m², consistent with (but not proof of) 1.44 m² boxes for 300x600 (8 pcs), 600x600 (4 pcs) and 600x1200 (2 pcs).
- 55.44 m² (299x299) does not divide by 1.44; it divides by 0.99 (56 boxes of 11 pcs) or 1.26 (44 boxes of 14 pcs), so the 300x300 box size cannot be inferred.
- 111.36 m² (100x300) and 92 m² (75x300) give no clean box size; 92 is probably rounded.

### Common industry defaults (ASSUMPTIONS, not data; confirm with Eternity before loading)

| Size | pcs/box | m²/box | kg/box (porcelain ~22 kg/m², ceramic ~15 kg/m², both estimates from `store-content/shipping/estimate_weights.py:58` and `store-content/shipping/other_products_shipping.py:5`) |
|---|---|---|---|
| 300x600 (298/299x600) | 8 | 1.44 | ~31.7 porcelain / ~21.6 ceramic (Gia's CTS 300x600 boxes: 1.44 m², 33.4 kg, `store-content/supplier-sync/gias-2026-11/gias-tiles-2026-11-19.csv:2`) |
| 600x600 | 4 | 1.44 | ~31.7 |
| 600x1200 | 2 | 1.44 | ~31.7 |
| 300x300 | 11 (0.99 m²) or 10 (0.90) or 14 (1.26) | varies; Gia's CTS 300x300 = 1.0 m², 17.8 kg (`gias-tiles-2026-11-19.csv:8`) | ~22 |
| 200x1200 (196x1200) | 5 or 6 | 1.2 or 1.44 | ~26-32 |
| 100x300 | 32-50 | 0.96-1.5 | ~15-22 |
| 75x300 | 44-50 | ~1.0-1.125 | ~15-17 |

### Other things worth knowing before the switch

- Shopify box sizes (`shipping.box_size`) and weights on all 84 variants are **formula estimates** from tile size (`/home/user/Excellent-Tiling-Services-/store-content/shipping/estimate_weights.py:55-59`), not supplier figures; `store-content/shipping/product-audit-2026-10-05.md:36` already notes the tile weights as estimates that "look right". Subwave 75x300 variants carry a 64 x 64 cm box, which is wrong.
- SKU differences between our store and eternitytiles.com.au (from `/products.json`): Eternity still uses ET-prefix codes for Terrazzo White / Morgan / Cement (ET36CP01N etc.) where we use DSA; Eternity lists Sand Grey as DSA365G/DSA665G (ours DSA36SG/DSA66SG), Bianco Greco as DSA36BGS/DSA66BGS (ours DSA36BG/DSA66BG), White ceramic as 36001/36002M (ours DSA36001/DSA36002M), Subway as 31001G/31002M (ours DSA31001G/DSA31002M), and has the Astra White/Greige codes swapped against their titles. Matters if box data is later matched by code.
- The files most likely to carry box data (`eternity-porcelain-tile-codes-2026-11-09.xlsx`, Product Information zips, test reports) are on the owner's drive / local clone and are **not in this repo** (`/home/user/Excellent-Tiling-Services-/Eternity/README.md:29-31`, `store-content/supplier-sync/drive-eternity-2026-11-10/README.md:3-6`).
- Gia's model reference for comparison: `/home/user/Excellent-Tiling-Services-/store-content/supplier-sync/README.md:305-309` and `store-content/supplier-sync/gias-2026-11/gias-tiles-2026-11-19.csv` (m2_per_box, box_kg columns).

**Recommendation:** ask Eternity for one sheet with m²/box, pcs/box and kg/box per code (same format as the 14 Oct DSA trade price request, `/home/user/Excellent-Tiling-Services-/store-content/pricing/DSA-trade-price-request-2026-10-14.txt`). Nothing can be loaded per box until that arrives; treat the 1.44 m² figure on Time Stone Moon/Charcoal as unverified.