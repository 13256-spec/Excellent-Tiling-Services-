# Eternity flash drive sync (10 Nov 2026)

Source: the owner's external drive, folder `D:\Eternity` (339 files: Caliza, Ceramic, DSA basin collection, DSA kitchen &
laundry, Lava, Porcelain, Product Information zips, Time stone, Terrazzo Lumina). It is the same material as the Google Drive
"DSA" folder synced on 26 Oct 2026 plus newer folders dated 9-10 Nov (Caliza, Ceramic, Lava, Time stone, Terrazzo Lumina).
Documents are copied into `Eternity/`; the photos (about 300 MB) stay on the drive.

## Applied to the store (live)

- **Placeholder swatches replaced with real supplier photos.** Lava Vesuv (`lava-vesuv-tile.png`, "indicative swatch") and
  Caliza (`caliza-tile.png`) now show the supplier's own tile photo; the two swatch files were deleted from Files.
- **26 supplier photos added** (list, alt text and source file in `photo-plan.json`; resize/convert script `photo_prep.py`):
  Lava Vesuv 4, Lava Kraka 3, Lava Etna 1, Lava Ash 2, Time Stone Sand 2, Time Stone Moon 2, Time Stone Charcoal 2, Caliza 1,
  Element Grey 1, Whisper Grey 1, Eternal Carrara 2, Eternal Marble 1, White Ceramic Wall Tile 2, Terrazzo Lumina 2.
  Upload path: `stagedUploadsCreate` -> curl POST -> `productUpdate(media:)` (`productCreateMedia` is rejected on API 2026-10).
- **Time Stone Sand (BS630332)** had no photo and was a draft. Photos added, `needs-photo` removed, set **Active** at its
  existing $55/m² lappato price. Not in `eternity-tiles-2026-10-05.csv`, so no cost is recorded; the owner can set it back
  to draft if it was waiting on a price.
- **Cement White / Grey / Dark Grey**: the clean single-tile photo moved to position 1 (the collection grid was showing a framed
  sample board and thin strips).
- **5 draft basins created** (`drafts-created-2026-11-10.json`), tagged `price-check`, `needs-photo`, price $0.00, `ets.supplier`
  = Eternity Tiles. They are the models in the basin folder that have no RRP in the Basin Collection PDF. Their supplier
  photos are 135-200 px, so none were attached.

## Not added, and why

- Snow White YF/FG 1240 (five codes in `eternity-porcelain-tile-codes-2026-11-09.xlsx`): still no price or photos.
- Caliza 600x600 (FG607300) and 600x1200 gloss (FG277300): photos on the drive, no price; the store lists 300x600 matt only.
- Particle Dark RSS06: still "Not available for now".
- Time Stone Sand 600x600 and matt: not in any price list; the Time Stone Series PDF (92 MB) is image-only.
- Supplier codes DSABA207CT / DSABA222CT (folders) vs ETBSN895 / ETBSN4202 (store, from the Basin Collection PDF): same names,
  sizes within 5 mm. Confirm with Eternity which code is current before changing SKUs.
- Test reports, slip reports and warranties are in `Eternity/test-reports/`; the store has no `ets.spec_sheet` file metafield,
  so nothing links to them yet.
- Toilet spec PDFs and videos (35 MB+) are the same files processed on 26 Oct; not copied again.
- Products still on generated swatches with no supplier photo on the drive: Astra White/Greige, Sand White/Beige/Grey,
  Bianco Greco, Fumosa, E-Time Calcare/Chiaro, Oak Aube, Subway and Subwave ceramics, the eight mosaics.
