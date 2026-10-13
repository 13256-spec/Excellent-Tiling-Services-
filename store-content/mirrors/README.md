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

## Light colour: the one gap

Bathroom City only publishes a colour temperature for the AERI LED arch mirrors (3000–6000 K,
warm / natural / cool white, which we do not stock). For SURI, VERA and ZOE LED it lists no
colour temperature at all, and its copy says "soft, warm glow" while its product photos show a
cool-white halo. The MIA 450 LED keeps "cool white" because our earlier catalogue-based
description already said so.

So the SURI, VERA and ZOE LED listings say "White LED, dimmable. Need a particular colour
temperature? Ask us before you order and we will confirm it with the supplier." Once Bathroom City
(08 9244 2168) confirms the Kelvin figure and whether it is single-colour or switchable, replace
that line in `build_mirror_descriptions.py` (`WHITE`) and re-send the four LED products.

## Not added

Bathroom City's spec-sheet drawings (PNG) were used for the numbers but not uploaded as product
images, because they carry Bathroom City's name, phone and address.
