# MELA mirrors: fuller product information (13 Oct 2026)

A customer said the LED mirror listings did not say enough (what colour the light is, and so on).
All 17 MELA mirror, LED mirror and mirror-cabinet products were rewritten from the supplier's
own data on bathroom-city.com.au: the "Product information" block on each product page, the MELA
spec-sheet drawings linked under "Product specification", and the MELA warranty and care PDFs.

- `build_mirror_descriptions.py` builds `mirror-descriptions-2026-10-13.json` (per product: new
  description HTML, `ets.*` metafields and tags to add). Written to Shopify on 13 Oct 2026 with
  `productUpdate` + `tagsAdd`; no errors.
- `before-2026-10-13.json` is the description each product had before.
- `ids.json` maps handle to Shopify product id.

## What each listing now says

- **LED mirrors (SURI, MIA 450, VERA, ZOE 600):** sizes and codes, backlit halo, touch on/off and
  dimming, built-in demister, 220–240 V, plug-in or hard-wired (licensed electrician), IP44, SAA,
  3-year mirror warranty, cleaning instructions.
- **Plain and framed mirrors:** sizes and codes, 3.2 mm silver mirror, about 5 mm depth (frameless)
  or 30 mm frame depth, frame finishes, tongue-and-groove mounting, warranty, care.
- **Mirror cabinets:** mirror size, cabinet box size behind it, light grey carcass, shelves,
  mounting, 5-year cabinet / 3-year mirror / 1-year hinges-and-finish warranty, care.
- Metafields the theme shows in the Specifications, Dimensions and Warranty & care panels:
  `ets.range`, `ets.material`, `ets.installation`, `ets.warranty`, `ets.care`, and
  `width_mm` / `height_mm` / `depth_mm` where the product has one size.

## Light colour (confirmed by Bathroom City, 14 Oct 2026)

- ZOE 600 LED: new stock from a new manufacturer, three settings (warm white, natural white, cool white).
- SURI, MIA 450 and VERA LED: original stock, cool white only. Bathroom City ships the original
  stock first; the three-colour version follows once it sells out. When that happens, switch those
  three products to `TRI` in `build_mirror_descriptions.py` and re-send.

## Not added

Bathroom City's spec-sheet drawings (PNG) were used for the numbers but not uploaded as product
images, because they carry Bathroom City's name, phone and address.
