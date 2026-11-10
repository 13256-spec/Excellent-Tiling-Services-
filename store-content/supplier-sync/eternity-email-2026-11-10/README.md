# Eternity email flyers (10 Nov 2026)

Eternity emailed "new tile collection" flyers for Bianco Greco, the Sand range (White, Beige, Grey) and the Astra range
(White, Greige). Flyers saved in `Eternity/eternity-flyer-*-2026-11-10.jpg`.

## What the flyers say vs the store

All six products are **already live** (created Oct 2026 from the 5 Oct price list), both sizes each, matching codes:
DSA36/66 BG, SW, SB, SG, AW, AG. 300x600 and 600x600, matt, P4. Flyer RRP $55/m² = price list RRP; store sells at
$46.00/m² (15% under RRP rule), cost $29.15 inc GST, 36.6% margin, trade-5. **No price change needed.**

Only gap: each product shows a 213 px generated "indicative swatch". The flyers carry the real supplier photos.

## Photos cropped from the flyers (this folder)

| Product | Files (px) |
|---|---|
| Bianco Greco | `bianco-greco-room` 784x498, `-tile` 384x384, `-layout` 586x389 |
| Sand White | `sand-white-room` 216x216, `-tile` 217x216, `-layout` 327x216 |
| Sand Beige | `sand-beige-room` 216x216, `-tile` 241x215, `-layout` 290x216 |
| Sand Grey | `sand-grey-room` 216x217, `-tile` 237x217, `-layout` 217x217 |
| Astra White | `astra-white-room` 784x444 (Astra range photo), `-tile` 265x264, `-layout` 265x264 |
| Astra Greige | `astra-greige-tile` 265x257, `-layout` 265x264 |

Status: **not yet on the store**. Upload path (`stagedUploadsCreate` -> curl POST -> `productUpdate(media:)`) was blocked
by the session's permission check at the curl step. Plan once allowed: add the three photos (tile first, then room,
then layout), then delete the old swatch image from each product.

The Sand photos are small (about 220 px). Ask Eternity for the full-size image files; swap them in when they arrive.
