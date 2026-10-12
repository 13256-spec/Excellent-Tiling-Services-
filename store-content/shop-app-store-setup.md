# Shop app store: matching the website (12 Oct 2026)

The Shop app ("Shop" sales channel) builds its store page from three things: the catalogue
published to the Shop channel, the collections' cover images, and the store's brand assets.
The first two were done through the API connector on 12 Oct 2026. The brand assets and the
Shop Store home-page layout can only be set in Shopify admin, so this file holds the exact
values to paste in.

## Done through the connector

- **Products:** all 921 active products are now published to the Shop channel (only 5 were
  before: three Sigma cutters and two BAT trims). New products still need "Shop" ticked under
  Sales channels when they are created.
- **Collections:** all 92 collections that are on the Online Store are now on Shop too. The five
  internal "Trade N% items" lists and "Black Friday 2026" stay off, as on the website.
- **Cover images:** Shop only shows a collection that has a cover image. 60 collections had
  none (every tile size, finish and range; the hardware brands and Raimondi sub-ranges; double
  vanities, sinks, bath taps, shower sets, wastes, the MELA range, Trade Essentials and a few
  others). Each now uses the featured photo of its first product, which is exactly what the website
  header, category tiles and collection heroes were already falling back to, so nothing changes on
  the website. The only collections still without an image are the internal trade lists and
  Black Friday 2026, which are not on Shop or the website.

## To set in admin (API cannot write these)

### Settings → General → Brand assets → Manage

Values come from the live theme (`theme/assets/ets-2026.css`, `theme/config/settings_data.json`,
`theme/templates/index.json`).

| Field | Value |
|---|---|
| Primary colour | `#15213A` (navy ink, used for headings, buttons, header text) |
| Primary contrasting colour | `#FFFFFF` |
| Secondary colour | `#9C7744` (brass accent, used for section labels and highlights) |
| Secondary contrasting colour | `#FFFFFF` |
| Slogan (≤ 80 chars) | `Your bathroom, from the first tile to the last tap.` |
| Short description (≤ 150 chars) | `Porcelain tiles, vanities, tapware and tiling tools. Shop online, visit our Maddington showroom, or let our licensed team handle the whole job.` |
| Default logo | The website logo, `excellent-tiling-services-logo.jpg` (Content → Files). Needs to be PNG or JPEG, ≥ 512 px wide. |
| Square logo | A square crop of the logo mark on a transparent background, PNG, ≥ 512 × 512 px. This is what the Shop app shows as the store avatar. |
| Cover image | One of the homepage hero room photos, exported at 1920 × 1080 px JPEG. The hero uses `DSA66AK666_3_…jpg`, `DSA66AK661_2.jpg`, `DSA66SS06_2.jpg`, `DSA36MQ02_3.jpg`, `DSAYFR600331_2.jpg`, `DSAFG607311.jpg` (Content → Files). |
| Social links | Same as the footer. |

The website body font is Manrope. The Shop app does not allow custom fonts, so the match is
colours, logo, photos and wording only.

### Sales channels → Shop → Store → Customize → Shop Store home

**Header**
- Logo: the square transparent PNG above (SVG, PNG or WEBP, ≥ 512 px, square).
- Background: a hero room photo at 1080 × 1170 px, or leave plain.
- Primary colour: `#15213A`.

**Navigation (up to 12 collections)**, in the website's menu order:
1. Tiles
2. Vanities & Basins (`vanities-basins`)
3. Tapware & Sinks (`tapware-sinks`)
4. Baths & Toilets (`baths-toilets`)
5. Mirrors & Accessories (`mirrors-accessories`)
6. Hardware
7. 600 x 600 mm Tiles
8. 300 x 600 mm Tiles
9. Bathroom Vanities
10. Bathroom Taps & Tapware
11. Trowels & Tiling Tools
12. Trade Essentials

**Collection lists (up to 5 lists, 10 collections each)**, mirroring the homepage sections:

| List heading (website section) | Collections |
|---|---|
| Shop by department | Tiles · Vanities & Basins · Tapware & Sinks · Baths & Toilets · Mirrors & Accessories · Hardware |
| Tile ranges | Morgan Tiles · Time Stone Tiles · Cement Tiles · Lava Tiles · Terrazzo Tiles · Particle Tiles · Ceramic & Wall Tiles · Mosaic Tiles |
| Tiles by size and finish | 600 x 600 mm · 300 x 600 mm · 600 x 1200 mm · 300 x 300 mm · Matt · Gloss · Lappato · Anti-Slip |
| Bathroom | Wall Hung Vanities · Double Vanities · Basins · Basin Mixers & Basin Taps · Shower Heads & Shower Sets · Freestanding Baths · Rimless Toilets · Shower Screens · LED Mirrors · Towel Rails |
| Tiling tools and hardware | Trowels & Tiling Tools · Sigma Tile Cutters & Spare Parts · Diamond Blades & Drill Bits · Tile Trims & Edging · Silicone, Additives & Cleaners · Grout Clean-Up Buckets, Floats & Sponges · Floor Drains & Wastes · Raimondi Tiling Tools & Machines · BAT Tiling Tools · Knee Pads & Replacement Straps |

A collection can sit in only one list, so the lists above do not repeat any collection.

**Announcement banner**: appears automatically whenever an automatic discount is active.

**Filters**: come from Search & Discovery and are the same as the website's.

## Checking it

Open the Shop app, search "Excellent Tiling Services", and confirm the store page shows the logo,
the six departments and the product count. Product delivery rules are the website's: tiles and
large items Perth metro, small items Australia-wide, applied at checkout.
