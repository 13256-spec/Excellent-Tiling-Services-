# MELA products: extra specs from the supplier (14 Oct 2026)

Follow-up to the mirror rewrite: the owner noticed Bathroom City's pages carry more detail than ours.
Every active MELA product (178) was matched to its Bathroom City page(s) and the supplier's
"Product information" block was merged into our listing where it added something we did not have.

## What was added

- Description: a **More details** list appended under our existing text, with only the facts our
  listing lacked (full wall-hung and freestanding cabinet dimensions, carcass material and hardware,
  kickboard sizes, brass / ceramic / glass material, waste size and overflow, trap and inlet details,
  package contents per size, ceramic tolerance note). Lines the listing already had, in any wording,
  were skipped. An "Approx. dimensions" bullet of ours was removed when the supplier's exact dimensions
  replaced it.
- Metafields (`ets.*`, only where the product had none): `material`, `range`, `wels_rating`,
  `flow_rate`, `cartridge`, `wels_registration`, and `width_mm` / `height_mm` / `depth_mm` for
  single-size items with W/D/H dimensions.

| Result | Products |
| --- | --- |
| Updated (description and/or metafields) | 161 |
| Nothing new on the supplier page | 12 |
| Not on Bathroom City (FLOVA bath spout) or no clean match (3 CLARK shelf vanities whose supplier pages share one code; SURI framed mirror already done) | 5 |

Mirrors were done separately on 13 Oct (`store-content/mirrors/`).

## Files

- `match_bathroom_city.py`, `fetch_bathroom_city_info.py`, `enrich_from_bathroom_city.py`: the pipeline
  (match by product code, with `KIT.` prefix and finish suffix ignored, then by title; fetch each
  supplier page; extract the key/value block; diff against our description).
- `mela-specs-2026-10-14.json`: per product the old description, the appended HTML and the metafields set.
- `bathroom-city-product-info-2026-10-14.json`: the raw supplier key/value blocks per supplier page.

## Not done

Bathroom City also has a spec-sheet drawing per product (375 of them). They were not read for this pass;
the mirror pass showed they add mirror thickness, frame depth and warranty years. Worth a second pass
on vanities and baths if a customer asks for carton or internal dimensions.
