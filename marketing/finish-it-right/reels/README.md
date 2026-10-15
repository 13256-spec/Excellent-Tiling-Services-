# Photo Reels (from 13 Oct 2026)

Owner asked on 13 Oct 2026 for videos and more posts to lift sales. These are 11-14 second photo Reels
built from the store's own photos (Shopify product images and the room shots in `../v2/source/img/`):
one photo per slide on porcelain white, product name and price in navy Archivo under it, slow push-in,
0.6 s dissolves, CC0 music from `../v2/source/music/`, and an end card with the website and the
delivery line. No AI images, no stock photos, no cards or gradients.

- `make_reel.py plan.json outdir` renders them (ffmpeg + Pillow; `Archivo.ttf` is the bundled brand font).
- `plan-2026-10-13.json`: today's two Reels (tiles 4:30 pm, vanities 8:30 pm).
- `plan-week-2026-10-14.json`: one Reel a day, 14-19 Oct, 4:30 pm (tools, basin mixers, tiles, mirrors,
  showers, vanities under $1,350).
- `metricool-2026-10-13.json`: what was booked in Metricool (ids, CDN video URLs, captions, copy-review
  verdicts). Videos are hosted on Shopify Files as `ets-reel-<date>-<topic>.mp4`.

Slot: 4:30 pm Instagram + Facebook Reel (showReelOnFeed), on top of the 12:15 pm product post, 6:30 pm
carousel and 7:30 pm Story. Prices were checked against the live store on 13 Oct 2026; re-check before
reposting.
