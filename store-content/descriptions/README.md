# Product description rewrite (24 Oct 2026)

Owner's request: most product descriptions were too short. Research each product online and write fuller,
customer-facing copy. Remove anything that is not product information (prices, "in stock at our showroom",
trade-account notes, delivery and pickup lines).

Rules every writer followed are in `BRIEF.md`: 90 to 200 words, intro paragraph then "Use it for",
"Features", "Specifications", "What's in the box", "Fits", "Good to know" sections as they apply; no price,
stock, showroom, delivery, pickup or trade wording; never name the tile supplier, the bathroomware importer or
Bathroom City; no hype words, exclamation marks or em dashes; never invent a spec. Each output file
(`<group>-2026-10-24.json`) keeps `old`, `new`, `sources`, `verified` and `notes` for every product, so any
description can be restored or checked.

## Pass 1: thin descriptions (under 60 words), 596 products

| Group | Products | Verified online | Main sources |
| --- | --- | --- | --- |
| roberts | 140 | 140 | Roberts Store API, Roberts catalogue PDF, sealant data sheets |
| raimondi | 91 | 87 | raimondispa.com pages and PDFs, 2026 pocket catalogue |
| sigma-siri-baron | 81 | 77 | sigmaitalia.com and spare-parts sheets, siri.mo.it, Baron UK |
| mela | 119 | 118 | MELA supplier product pages and local spec files |
| bat-maxisil-panther | 58 | 54 | battrims.com Store API, maxisil.com.au data sheets |
| ets-bathroomware-hardware | 60 | 41 | supplier size drawings already on each product |
| tiles | 47 | 27 | supplier product feed, price list, product photos |

## Cleanup of longer descriptions, 482 products

`cleanup_2026_10.py` removed 830 store-operations sentences ("Delivery: ships Australia-wide...",
"Buy ... online from Excellent Tiling Services", "Order through...", "see the samples in our Maddington
showroom", "call the showroom") from descriptions that were already long enough. Before and after for every
product in `cleanup-2026-10-24.json`; result in `cleanup-results-2026-10-24.json` (482 updated, 0 errors).

## Pass 2: thin once the boilerplate was gone, 221 products

| Group | Products | Verified online |
| --- | --- | --- |
| raimondi-2 | 104 | 93 |
| bat-2 | 89 | 76 |
| misc-2 (Panther, Washboy, NICLIS, Atika, ADA, MELA) | 28 | 25 |

## Final check (24 Oct 2026)

A fresh export of all 1,123 active products was compared with the approved text: all 1,078 rewritten or cleaned
descriptions match exactly. A store-wide scan for prices, stock, showroom, Maddington, delivery, pickup, shipping,
trade-account, phone-number, supplier and importer wording found two leftovers (Sika Master Lite pickup line,
Raimondi Rai-Fix Hooks "Buy ... from Excellent Tiling Services"), both fixed (`final-fixes-2026-10-24.json`).
No active product now has a description under 60 words; median is 146 words (was 56).

## Facts the writers found that differ from what we had (check if it matters)

- MELA PALCO/RONDO Shower Head and Hand Shower Set with Rail: old copy said WELS 4 star 7.5 L/min; the
  supplier lists 3 star 9 L/min. Copy now uses the supplier figure.
- Maxisil Membrane: website says 50% joint movement, the data sheet says 25%. Old figure kept.
- Sigma 64B2 mat fits Series 4 cutters (old copy said Kera-Cut/Kera-Lift); 37C fixing kit is for the Jolly
  Edge (old copy said Kera-Cut). Corrected from Sigma's parts sheets.
- Raimondi cellulose sponge is 160 x 90 x 70 mm per Raimondi (title says 190 x 120 mm).
- Baron F200 motor rating left out: Roberts says 3.5 kW, Baron UK says 2.2 kW.
- Tiles: box coverage is only known for Time Stone Moon and Charcoal (1.44 m2). Adding per-box coverage to
  the tile price data would let every tile page show it.
