# Google Drive "DSA" folder sync (26 Oct 2026)

Source: the owner's Google Drive folder `DSA` (root id 1q8gHoFtBqXr_7tUsN6ClBwLtdbyHhlnE), read through the
Google Drive connector. `drive-dsa-inventory.json` is the full tree (169 entries, 144 files).

## What was applied to the store

**Porcelain tiles (10 products, all already in the store)**
- Slip ratings from the Slipstop Perth wet pendulum reports (AS 4586, tested 4 Mar 2025):
  Morgan AK = P3 (SRV 36), Cement MQ = P3 (SRV 35), Particle SS = P5 (SRV 55).
  Particle Grey and Particle Warm were listed as P4 and are now P5 (tags, description, SEO).
  The supplier's `Porcelain Tile Slip Stop Test.xlsx` says Cement is P5, but the lab PDF says P3; the lab PDF wins.
  Terrazzo White has no lab report yet (the sheet says a retest is pending), so its P3 claim is unchanged.
- Factory test report figures added to the Specifications list of Morgan, Cement and Terrazzo White
  (9.5 mm, water absorption 0.06%, breaking strength 2,132 N, stain resistance class 5, frost resistant).
  `tile_updates.py` + `tile-updates-2026-10-26.json` are the exact productUpdate inputs.
- 34 photos attached to the 10 tile products (face variation sheets, single tiles, room renders) and 3 showroom
  photos saved to Content > Files. `tile_photos_prep.py` / `tile-photos-plan.json` map each Drive file id to
  the Shopify filename and alt text. Files over about 6 MB cannot come through the Drive connector, so the
  largest JPEGs (the 10 to 27 MB ones) were skipped; the store already had equivalent hero photos for those.

**Basins and sinks**
- New: Chet Wall Hung Basin (ETK311B, $198) and Mezzo Above Counter Basin (ET847, $179), live, with photos
  pulled from `Chet_and_Mezzo.pdf` (`basin-pdf/`), in the Basins / Above Counter Basins collections and on
  all sales channels.
- Olivia Semi Inset and Olivia Above Counter already existed; the two duplicate drafts created by mistake were deleted.
- All 10 ceramic basins now carry `ets.warranty` = "5 years on the ceramic basin"; the 6 stainless sinks carry
  "10 years on the stainless steel sink; 2 years on basket wastes, rubbers, overflow and seals" (from the two
  warranty PDFs). `needs-cost` replaced by `cost-estimate` with cost = RRP x 0.5 (see `basins-sinks-costs-2026-10-26.csv`).

## Not added, and why
- Particle Dark RSS06: the supplier sheet says "Not available for now". Photos are in the Drive folder if it is released.
- Terrazzo Middi: five showroom photos only, no code or price in any sheet.
- Morgan Dawn AK666: same code and image as Morgan Dusk (already in the store); nothing extra to add.
- Snow White YF/FG 1240 (298x600 matt, 600x600 gloss, 600x1200 honed): listed in `Porcelain Tile.xlsx` with codes
  but no price, photos or spec sheet. Ask Eternity for RRP and photos before listing.
- Toilets: the 10 zips in `DSA/Toilets` are the same files the owner uploaded on 26 Oct and were already processed.
