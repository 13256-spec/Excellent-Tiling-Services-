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

## Week 2 (25 Oct to 8 Nov 2026)

`plan-week-2026-10-25.json`: one Reel a day at 4:30 pm, 25 Oct to 8 Nov (towel rails, vanities under
$1,000, set-out tools, LED mirrors, kitchen, toilets, light floors, floor wastes, basins, BRITTANY range,
shower sets, mirror cabinets, dark floors, knee pads, the new Celine range). Prices checked against the
live store on 23 Oct 2026 (after the MELA reprice). Videos on Shopify Files as `ets-reel-<date>-<topic>.mp4`;
captions and Metricool ids in `../clean/copy-2026-10-24.json`.

Stories with sound (owner, 23 Oct 2026): `make_story.py plan.json outdir` renders a 7 s 1080x1920 video from one
store photo (slow push-in, CC0 music, no text). `plan-stories-2026-10-24.json` covers 24 to 29 Oct and the
four replaced Stories on 1, 2, 7 and 8 Nov; hosted as `ets-story-<date>.mp4`.

## Hook Reels (owner, 23 Oct 2026: "Reels that convert", less MELA)

`make_reel2.py plan.json outdir`: hook line on a navy block for the first 2.2 s, 2 s full-bleed slides with
name and price on a navy strip, 0.3 s cuts, end card with the website and "Link in bio". 9 to 11 s.
`plan-hook-week-2026-10-25.json` replaced eight MELA Reels in the 4:30 pm slot (25, 26, 28, 29, 30 Oct,
2, 3, 4 Nov) with silicone, trims, Sigma cutters, levelling, blades, grout clean-up and waterproofing.
Hosted as `ets-hook-<date>-<topic>[-v2].mp4`. Hook photos from `marketing/image-library` (stock, mood only)
are copied into `../v2/source/img/lib-*.jpg`. Samples the owner saw: `plan-hook-samples.json`.
