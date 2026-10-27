# Finish It Right social campaign (12 Oct – 8 Nov 2026)

Ready-to-post graphics. Feed posts are 1080×1350 (Instagram/Facebook portrait); files starting
`S-` (Stories) and `R-` (Reel covers) are 1080×1920.

| File | Use |
| --- | --- |
| A2-1 … A2-5 | Store launch carousel (post in order; A2-5 is "three ways to get it home") |
| A3-idea | Bathroom idea: BRITTANY oak vanity |
| B2-refresh | $480 FLOVA bathroom refresh |
| B3-prices | Every price is online |
| C2-tile-looks | Four porcelain floors |
| C3-showroom | Evening showroom hours |
| D2-trade | Trade accounts |
| D3-pickup | Order online, pick up free in Maddington |
| R-B1 / R-C1 / R-D1 | Reel covers: unboxing, vanity install, tiling mistakes |
| S-poll / S-shipping / S-showroom / S-trade | Story frames (add the poll sticker in Instagram) |

## No discount code (decided 5 Oct 2026)

A YAMEN10 code (10% off, $150 minimum) was set up and then cancelled before launch: at 10% off, 349 of
1,572 product options would have dropped below the 20% profit floor and 9 would have sold below cost.
The campaign leads with every price online, small items posted Australia-wide from $9.95 (free shipping ended 17 Oct 2026), Perth delivery, free
pickup in Maddington and the evening showroom instead. Don't claim "cheaper than" competitors: 62 of 574
MELA prices are above Bathroom City's.

The posting schedule and captions are in the owner's Google Calendar. Prices are as of 4 Oct 2026;
re-check before reposting after a price change. Never name the tile supplier.

To edit or add a post: `cd source && python3 build.py [name-prefix]` (needs Node + Playwright with
Chromium). Layout is a 4-column tile grid with 6 px grout lines; colours from the logo (navy #1F3153,
tile blue #4C8ED9), type is Archivo (bundled).

## New plan and Metricool queue (updated 5 Oct 2026)

The campaign now starts **Tue 6 Oct** (launch carousel) and runs to 8 Nov. Metricool (brand 7234377,
Facebook + Instagram @excellent_tiling_services) auto-publishes three slots a day:

| Time | Slot | Source |
| --- | --- | --- |
| 12:15 pm | Product of the day (store photos, live price, link) | `schedule/lunch-products.json` |
| 6:30 pm | Main post (brand graphic) | `schedule/main-posts.json` (`manual: true` = Reels 16/21/26 Oct and review post 27 Oct, posted by hand) |
| 7:30 pm | Story | `schedule/stories.json` |

Everything sent to Metricool is in `schedule/metricool-queue.json`; Metricool ids in `schedule/results-*.json`.
`schedule/build_schedule.py` rebuilds the main-post and Story files. Graphics are hosted on Shopify Files
(`cdn.shopify.com/.../files/ets-<name>.png`) so Metricool can fetch them.

New Stories for auto-posting (no stickers, which Metricool can't add): `S-reply` (chrome or black, reply
with your pick), `S-tiles` (from $37.40/m²), `S-vanity` (from $1,139). `S-shipping` now says "Shop via
the link in our bio". `S-poll` still needs a poll sticker, so it is for posting by hand only.

By hand each day (Google Calendar): 7 am real Story, 8:30 am Marketplace, 3:30 pm groups + Google, 9 pm
replies. Team agents: `ets-marketing` (lead), `ets-content`, `ets-social`, `ets-community`,
`ets-analytics`, `ets-calendar`, `ets-pricing` (`.claude/agents/`).

## Queue rewrite, 28 Oct – 8 Nov (27 Oct 2026)

The owner found the posts repetitive. Metricool reach backed it: feed posts fell from 44–55 people (6–10 Oct)
to 9–37 after the catalogue template took over on 14 Oct, while Reels did 50–123. Every pending 12:15 pm and
6:30 pm post and 4:30 pm Reel caption from 28 Oct to 8 Nov was rewritten in place (same Metricool uuids) with
a different angle and call to action each day, the delivery line taken out of the caption, prices re-checked
and eight parked drafts made live. Six products were swapped for ones never posted (smart toilet, Eternal
Element toilet, Malaga package, niche box, BRITTANY 750, powder-room combo). Record and new captions:
`schedule/rewrite-2026-10-28.json`. Known gap: the 1 Nov floor-waste Reel video still shows $16.05 (live
$18.99); caption corrected, video not re-rendered.
