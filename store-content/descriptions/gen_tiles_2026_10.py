#!/usr/bin/env python3
"""Generate store-content/descriptions/tiles-2026-10-24.json from per-product data.

Facts come only from: the 5 Oct 2026 price list text, our Shopify variants, the old
description, and (for 29 tiles) the supplier's public product page. Looks come from the
product photos / price-list swatches already on our store.
"""
import json, re, html, sys

PL = "store-content/pricing/eternity-price-list-2026-10-05.txt"
CSV = "store-content/pricing/eternity-tiles-2026-10-05.csv"
SW = "store-content/pricing/eternity-swatches/"
SUP = "https://eternitytiles.com.au/products/"

PER_M2 = "Sold per square metre and supplied to the nearest full box."
P3 = "P3 slip rating: fine for bathroom, laundry and other wet-area floors inside the home."
P4 = "P4 slip rating: suits bathroom and laundry floors and covered outdoor areas such as an alfresco."
GLOSS_WALL = "The gloss finish has no slip rating, so use it on walls and dry floors only."
LAPP_WALL = "The lappato finish has no slip rating, so use it on walls and dry floors only."
LAY_600 = "Back-butter the 600 x 600 mm tiles on a flat, primed floor so the adhesive covers the whole back."
LAY_1200 = "The 600 x 1200 mm size needs a flat, level floor and back-buttering; use a levelling system to keep the long edges flush."
LAY_300 = "Lay on a flat, primed substrate with a flexible tile adhesive and a 2 to 3 mm joint."
STONE_CARE = "Natural stone varies from sheet to sheet. Seal it before grouting and again after, and clean with a pH-neutral cleaner, never acid."
STONE_LAY = "Bed the sheet in white flexible adhesive so nothing shows through the lighter stone, and use a non-sanded grout to protect the polished face and metal."
WALL_ONLY = "Wall tile only; it is not rated for floors."
CERAMIC_LAY = "Lay with a wall tile adhesive on a flat, primed substrate and a 2 mm joint."

def old_html(intro, bullets, tail=""):
    return "<p>%s</p><ul>\n%s\n</ul>%s" % (intro, "\n".join("<li>%s</li>" % b for b in bullets), tail)

def build(p):
    parts = ["<p>%s</p>" % p["intro"]]
    for h, items in (("Use it for", p["use"]), ("Specifications", p["specs"]), ("Good to know", p["gtk"])):
        if items:
            parts.append("<h3>%s</h3><ul>%s</ul>" % (h, "".join("<li>%s</li>" % i for i in items)))
    if p.get("tail"):
        parts.append(p["tail"])
    return "".join(parts)

def words(h):
    return len(html.unescape(re.sub(r"<[^>]+>", " ", h)).split())

def porc(sizes, finish, thick="9.5 mm"):
    return ["Material: glazed porcelain", "Sizes: " + sizes, "Finish: " + finish, "Thickness: " + thick]

P = []
def add(**k): P.append(k)

# ---------------- Time Stone (premium, matt P4/R11 or lappato) ----------------
add(handle="time-stone-moon-porcelain-tile", id="gid://shopify/Product/8395795038271", title="Time Stone Moon Porcelain Tile",
    old=old_html("Time Stone Moon porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm and 600x600mm","Matt or Lappato finish","Material: Porcelain","Slip rating: P4/R11","Suitable for dry and wet area applications","Box coverage: 1.44m²","Recommended grout: Ardex Misty Grey 341"]),
    intro="Time Stone Moon is a pale grey stone-look porcelain with soft, cloudy movement and faint veining, so it reads as a light neutral rather than a busy pattern. The matt version carries a P4/R11 slip rating, which makes it one of the few light tiles here you can run straight from the living room into the bathroom floor.",
    use=["Open-plan floors, bathrooms and laundries in the matt finish","Feature walls and dry floors in the lappato (semi-polished) finish","Lightening a room that does not get much natural light"],
    specs=porc("298 x 600 mm and 600 x 600 mm","matt or lappato")+["Slip rating: P4/R11 (matt)","Box coverage: 1.44 m²",PER_M2],
    gtk=[P4, LAPP_WALL, LAY_600, "Recommended grout: Ardex Misty Grey 341."],
    sources=[SUP+"time-stone-moon-premium-range-tile", PL], verified=True,
    notes="Supplier page confirms sizes and finishes. P4/R11, box coverage and grout kept from old description.")

add(handle="time-stone-cinder-porcelain-tile", id="gid://shopify/Product/8395795890239", title="Time Stone Cinder Porcelain Tile",
    old=old_html("Time Stone Cinder porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm and 600x600mm","Matt or Lappato finish","Material: Porcelain"]),
    intro="Time Stone Cinder is a warm beige-grey stone-look porcelain with layered, sedimentary veining running across the face. It is the warm colour in the Time Stone range, and the matt finish carries a P4 slip rating so it works on wet floors as well as dry.",
    use=["Bathroom, laundry and living floors in the matt finish","Walls and dry floors in the lappato (semi-polished) finish","Pairing with timber and warm white joinery"],
    specs=porc("298 x 600 mm and 600 x 600 mm","matt or lappato")+["Slip rating: P4 (matt)",PER_M2],
    gtk=[P4, LAPP_WALL, LAY_600, "Dry-lay a few tiles first and mix from several boxes so the veining spreads evenly."],
    sources=[SUP+"time-stone-cinder-premium-range-tile", PL], verified=True,
    notes="Supplier page confirms sizes and finishes; P4 from price list.")

add(handle="time-stone-charcoal-porcelain-tile", id="gid://shopify/Product/8395796054079", title="Time Stone Charcoal Porcelain Tile",
    old=old_html("Time Stone Charcoal porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm and 600x600mm","Matt or Lappato finish","Material: Porcelain","Slip rating: P4/R11","Suitable for dry and wet area applications","Box coverage: 1.44m²","Recommended grout: Ardex Midnight 302"]),
    intro="Time Stone Charcoal is a dark grey stone-look porcelain with lighter grey veining and a slightly weathered surface. The matt finish is rated P4/R11, so it gives you a dark floor you can carry into a bathroom or laundry without changing tile.",
    use=["Bathroom and laundry floors in the 298 x 600 mm matt finish","Feature walls and dry floors in the 600 x 600 mm lappato finish","Dark floors against white or pale grey walls"],
    specs=porc("298 x 600 mm (matt) and 600 x 600 mm (lappato)","matt or lappato")+["Slip rating: P4/R11 (matt)","Box coverage: 1.44 m²",PER_M2],
    gtk=[P4, LAPP_WALL, LAY_600, "Recommended grout: Ardex Midnight 302.", "Dark matt tiles show grout haze, so wash off thoroughly while grouting."],
    sources=[SUP+"time-stone-charcoal-premium-range-tile", PL], verified=True,
    notes="We sell only 298x600 matt and 600x600 lappato (two variants); description matches the variants rather than the old 'both sizes in both finishes' wording. P4/R11, box coverage and grout kept from old description.")

# ---------------- Lava (premium marble look, matt P3, gloss unrated) ----------------
add(handle="lava-etna-porcelain-tile", id="gid://shopify/Product/8395796217919", title="Lava Etna Porcelain Tile",
    old=old_html("Lava Etna porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm and 600x600mm","Matt finish","Material: Porcelain","Slip rating: P3"]),
    intro="Lava Etna is a near-black marble-look porcelain with fine white veins cutting across a dark grey-brown base. It is the darkest tile in the Lava range and, in matt with a P3 slip rating, it works as a bathroom floor as well as a feature wall.",
    use=["Bathroom and ensuite floors and walls","Feature walls behind a vanity or bath","Dark floors in a laundry or powder room"],
    specs=porc("298 x 600 mm and 600 x 600 mm","matt")+["Slip rating: P3",PER_M2],
    gtk=[P3, LAY_600, "Pair with a charcoal grout so the joints disappear, or a light grout to show the grid.", "Dark tiles show water spots in a shower; a squeegee keeps them looking right."],
    sources=[SUP+"lava-etna-premium-range-tile", PL], verified=True,
    notes="We sell matt only; supplier also lists gloss, not included.")

add(handle="lava-ash-porcelain-tile", id="gid://shopify/Product/8395796348991", title="Lava Ash Porcelain Tile",
    old=old_html("Lava Ash porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm and 600x600mm","Material: Porcelain"]),
    intro="Lava Ash is a light warm-grey marble-look porcelain with faint, fine veining, closer to a soft limestone than a bold marble. Choose matt for floors (P3 rated) or gloss for walls where you want the light bounced around.",
    use=["Bathroom floors and walls in matt","Shower and splashback walls in gloss","Living areas where you want a light floor without a strong pattern"],
    specs=porc("298 x 600 mm and 600 x 600 mm","matt or gloss")+["Slip rating: P3 (matt)",PER_M2],
    gtk=[P3, GLOSS_WALL, LAY_600, "Matt and gloss are the same colour, so you can run matt on the floor and gloss up the wall."],
    sources=[SUP+"lava-ash-premium-range-tile", PL], verified=True, notes="")

add(handle="lava-kraka-porcelain-tile", id="gid://shopify/Product/8395796545599", title="Lava Kraka Porcelain Tile",
    old=old_html("Lava Kraka porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm, 600x600mm and 600x1200mm","Material: Porcelain"]),
    intro="Lava Kraka is a warm mid-grey, almost taupe, marble-look porcelain with thin white veins and a mottled stone background. It sits between the pale Ash and the dark Etna in the range, and it is the one to pick when a cool grey feels too cold.",
    use=["Bathroom floors and walls in matt","Large-format walls and dry floors in 600 x 1200 mm gloss","Living and hallway floors in 600 x 600 mm matt"],
    specs=porc("298 x 600 mm and 600 x 600 mm in matt or gloss; 600 x 1200 mm in gloss","matt or gloss")+["Slip rating: P3 (matt)",PER_M2],
    gtk=[P3, GLOSS_WALL, LAY_600, LAY_1200],
    sources=[SUP+"lava-kraka-premium-range-tile", PL], verified=True, notes="600x1200 is gloss only in our variants and on the price list.")

add(handle="lava-vesuv-porcelain-tile", id="gid://shopify/Product/8414127816767", title="Lava Vesuv Porcelain Tile",
    old=old_html("Lava Vesuv porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm, 600x600mm and 600x1200mm","Matt or Gloss finish","Material: Porcelain","Slip rating: P3 (matt)"]),
    intro="Lava Vesuv is a pale greige marble-look porcelain, a soft cream-grey base with fine, scattered veins. It is the lightest and warmest colour in the Lava range and works where you want the marble look without strong contrast.",
    use=["Bathroom floors and walls in matt","Large-format walls and dry floors in 600 x 1200 mm gloss","Open-plan living floors in 600 x 600 mm matt"],
    specs=porc("298 x 600 mm and 600 x 600 mm in matt or gloss; 600 x 1200 mm in gloss","matt or gloss")+["Slip rating: P3 (matt)",PER_M2],
    gtk=[P3, GLOSS_WALL, LAY_600, LAY_1200],
    sources=[PL, SW+"lava-vesuv-tile.png"], verified=False, notes="Not on the supplier's public site; facts from price list and old description, look from price-list swatch.")

# ---------------- Terrazzo ----------------
add(handle="terrazzo-lumina-porcelain-tile", id="gid://shopify/Product/8395796709439", title="Terrazzo Lumina Porcelain Tile",
    old=old_html("Terrazzo Lumina porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm and 600x600mm","Material: Porcelain"]),
    intro="Terrazzo Lumina is a white terrazzo-look porcelain with a fine, even scatter of small dark flecks rather than big chips, so it reads as a speckled white from across the room. It is matt, P4 rated, and hides dust and footprints better than a plain white tile.",
    use=["Bathroom, laundry and kitchen floors","Alfresco and covered patio floors","Walls where you want a bit of texture in a white scheme"],
    specs=porc("298 x 600 mm and 600 x 600 mm","matt")+["Slip rating: P4",PER_M2],
    gtk=[P4, LAY_600, "Grout in a light grey or off-white so the joints blend into the fleck.", "Mix tiles from several boxes so the fleck density stays even."],
    sources=[SUP+"terrazzo-lumina-premium-range-tile", PL], verified=True, notes="")

add(handle="terrazzo-white-porcelain-tile", id="gid://shopify/Product/8395796873279", title="Terrazzo White Porcelain Tile",
    old=old_html("Terrazzo White porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm and 600x600mm","Matt finish","Material: Porcelain"]),
    intro="Terrazzo White is a classic terrazzo-look porcelain: a white base with larger grey and white stone chips and the odd darker fleck, like the poured terrazzo in older Perth homes. It is matt with a P3 slip rating, so it suits bathroom and laundry floors as well as walls.",
    use=["Bathroom and laundry floors","Kitchen splashbacks and feature walls","Floors that need to hide dirt between cleans"],
    specs=porc("298 x 600 mm and 600 x 600 mm","matt")+["Slip rating: P3",PER_M2],
    gtk=[P3, LAY_600, "The chip pattern varies tile to tile; mix boxes as you lay so no two identical faces sit together.", "A mid-grey grout matches the chips and hides joints."],
    sources=[SUP+"terrazzo-white-standard-porcelain-range-tile", PL], verified=True, notes="")

# ---------------- Particle ----------------
add(handle="particle-grey-porcelain-tile", id="gid://shopify/Product/8395797004351", title="Particle Grey Porcelain Tile",
    old=old_html("Particle Grey porcelain tile, sold per sqm to the nearest full box.", ["300x600mm, Matt finish","Material: Porcelain","P Rating: 4"]),
    intro="Particle Grey is a mid-grey porcelain with a fine, granular, salt-and-pepper surface like a honed granite. It is a plain working tile with a P4 slip rating, which makes it a good choice for wet floors, laundries and outdoor areas where a glossy tile would be a hazard.",
    use=["Bathroom, laundry and toilet floors","Alfresco, verandah and covered patio floors","Garages and workshops that get wet"],
    specs=porc("299 x 600 mm","matt")+["Slip rating: P4",PER_M2],
    gtk=[P4, LAY_300, "Textured matt surfaces hold dirt in the grain; a stiff brush and a neutral cleaner bring them back.", "Grey grout keeps the floor low maintenance."],
    sources=[SUP+"particle-grey-standard-porcelain-range-tile", PL], verified=True, notes="Supplier notes a new finish on the new batch; not stated in the description.")

add(handle="particle-warm-porcelain-tile", id="gid://shopify/Product/8395797200959", title="Particle Warm Porcelain Tile",
    old=old_html("Particle Warm porcelain tile, sold per sqm to the nearest full box.", ["300x600mm, Matt finish","Material: Porcelain"]),
    intro="Particle Warm is a cream porcelain with a fine, even speckle through the face, like a light sandstone. It has a P4 slip rating, so it works as a bathroom or alfresco floor, and the warm tone suits older brick homes better than a stark grey.",
    use=["Bathroom, laundry and toilet floors","Alfresco and covered outdoor floors","Hallways and living areas in a warm neutral scheme"],
    specs=porc("299 x 600 mm","matt")+["Slip rating: P4",PER_M2],
    gtk=[P4, LAY_300, "Use a beige or sand grout so the joints blend with the speckle.", "Textured matt surfaces hold dirt in the grain; a stiff brush and a neutral cleaner bring them back."],
    sources=[SUP+"particle-warm-standard-porcelain-range-tile", PL], verified=True, notes="P4 from price list (old description had no rating).")

# ---------------- Morgan (standard marble look, P3) ----------------
MORGAN_GTK = [P3, LAY_600, "Marble-look faces repeat, so mix tiles from several boxes and turn some tiles so the veins do not line up."]
add(handle="morgan-dusk-porcelain-tile", id="gid://shopify/Product/8395797364799", title="Morgan Dusk Porcelain Tile",
    old=old_html("Morgan Dusk porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x300mm, 300x600mm and 600x600mm","Material: Porcelain"]),
    intro="Morgan Dusk is a cream marble-look porcelain with soft beige veining, the warm colour in the Morgan range. It is matt, P3 rated, and comes in three sizes, so you can run 300 x 300 mm on a shower floor and 600 x 600 mm through the rest of the bathroom.",
    use=["Bathroom and ensuite floors and walls","Shower floors in the 299 x 299 mm size, which falls to the waste more easily","Living and hallway floors in 600 x 600 mm"],
    specs=["Material: glazed porcelain","Sizes: 299 x 299 mm, 299 x 600 mm and 600 x 600 mm","Finish: matt","Thickness: 9.5 mm (299 x 600 and 600 x 600)","Slip rating: P3",PER_M2],
    gtk=MORGAN_GTK+["A warm white or almond grout suits the cream base."],
    sources=[SUP+"morgan-dusk-standard-porcelain-range-tile", PL], verified=True, notes="Price list gives no thickness for the 299x299 size.")

add(handle="morgan-storm-porcelain-tile", id="gid://shopify/Product/8395797495871", title="Morgan Storm Porcelain Tile",
    old=old_html("Morgan Storm porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm and 600x600mm","Material: Porcelain"]),
    intro="Morgan Storm is a dark grey marble-look porcelain with lighter grey and white veins running through it. It is the darkest Morgan colour, matt with a P3 slip rating, so it gives you a moody bathroom floor without going to a dearer range.",
    use=["Bathroom and ensuite floors and walls","Feature walls behind a bath or vanity","Powder room and laundry floors"],
    specs=porc("299 x 600 mm and 600 x 600 mm","matt")+["Slip rating: P3",PER_M2],
    gtk=MORGAN_GTK+["Charcoal grout hides joints; wash grout haze off dark tiles straight away."],
    sources=[SUP+"morgan-storm-standard-porcelain-range-tile", PL], verified=True, notes="")

add(handle="morgan-cloud-porcelain-tile", id="gid://shopify/Product/8395797659711", title="Morgan Cloud Porcelain Tile",
    old=old_html("Morgan Cloud porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x300mm, 300x600mm and 600x600mm","Material: Porcelain","Slip rating: P3"]),
    intro="Morgan Cloud is a light grey marble-look porcelain with soft white veining and a cloudy background. It is matt and P3 rated, and the three sizes let you use the small 300 x 300 mm tile on a shower floor and the larger sizes on walls and the main floor.",
    use=["Bathroom and ensuite floors and walls","Shower floors in the 299 x 299 mm size","Laundry and toilet floors"],
    specs=["Material: glazed porcelain","Sizes: 299 x 299 mm, 299 x 600 mm and 600 x 600 mm","Finish: matt","Thickness: 9.5 mm","Slip rating: P3",PER_M2],
    gtk=MORGAN_GTK+["A light grey grout keeps the floor looking like one surface."],
    sources=[SUP+"morgan-cloud-standard-porcelain-range-tile", PL], verified=True, notes="")

add(handle="morgan-hail-porcelain-tile", id="gid://shopify/Product/8395797790783", title="Morgan Hail Porcelain Tile",
    old=old_html("Morgan Hail porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm, 600x600mm and 600x1200mm","Material: Porcelain","Slip rating: P3"], '<p>Compare this tile with other <a href="/collections/morgan-tiles">Morgan porcelain tiles</a> or browse our <a href="/collections/tiles-600x1200">600 x 1200 mm tiles</a>.</p>'),
    intro="Morgan Hail is the lightest Morgan colour: a white-grey marble-look porcelain with pale grey veins. It is matt with a P3 slip rating and comes up to 600 x 1200 mm, so you can tile a whole bathroom, floor and walls, in one tile with few joints.",
    use=["Bathroom floors and walls in one tile","Large walls in 600 x 1200 mm with fewer grout lines","Open-plan living floors"],
    specs=porc("299 x 600 mm, 600 x 600 mm and 600 x 1200 mm","matt")+["Slip rating: P3",PER_M2],
    gtk=[P3, LAY_600, LAY_1200, "Mix tiles from several boxes so the veining spreads evenly."],
    tail='<p>Compare this tile with other <a href="/collections/morgan-tiles">Morgan porcelain tiles</a> or browse our <a href="/collections/tiles-600x1200">600 x 1200 mm tiles</a>.</p>',
    sources=[SUP+"morgan-hail-standard-porcelain-range-tile", PL], verified=True,
    notes="Kept the existing internal collection links paragraph at the end. Supplier page lists 300x600 and 600x600 only; the 600x1200 size is on the price list and in our variants.")

# ---------------- Cement ----------------
add(handle="cement-dark-grey-porcelain-tile", id="gid://shopify/Product/8395797954623", title="Cement Dark Grey Porcelain Tile",
    old=old_html("Cement Dark Grey porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm and 600x600mm","Material: Porcelain"]),
    intro="Cement Dark Grey is a charcoal concrete-look porcelain with soft, cloudy tonal variation and no veining. It is matt with a P3 slip rating, so it works as a bathroom or laundry floor, and the plain face suits modern and industrial-style fit-outs.",
    use=["Bathroom, laundry and toilet floors","Walls in a shower or behind a vanity","Hallways and entries that take a lot of foot traffic"],
    specs=porc("299 x 600 mm and 600 x 600 mm","matt")+["Slip rating: P3",PER_M2],
    gtk=[P3, LAY_600, "Charcoal grout gives a near-seam-free concrete look; a lighter grout shows the grid.", "Wash grout haze off dark tiles straight away."],
    sources=[SUP+"cement-dark-grey-standard-porcelain-range-tile", PL], verified=True, notes="")

add(handle="cement-grey-porcelain-tile", id="gid://shopify/Product/8395798249535", title="Cement Grey Porcelain Tile",
    old=old_html("Cement Grey porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm, 600x600mm and 600x1200mm","Matt finish","Material: Porcelain","Slip rating: P3"]),
    intro="Cement Grey is a light-to-mid grey concrete-look porcelain with gentle cloudy variation across the face. It is matt, P3 rated, and comes in three sizes up to 600 x 1200 mm, which makes it a safe all-rounder for floors and walls through a whole renovation.",
    use=["Bathroom, laundry and kitchen floors","Large walls in 600 x 1200 mm with fewer joints","Living areas and hallways"],
    specs=porc("299 x 600 mm, 600 x 600 mm and 600 x 1200 mm","matt")+["Slip rating: P3",PER_M2],
    gtk=[P3, LAY_600, LAY_1200, "A mid-grey grout keeps the concrete look continuous."],
    sources=[SUP+"cement-grey-standard-porcelain-range-tile", PL], verified=True, notes="")

# ---------------- Fumosa ----------------
add(handle="fumosa-porcelain-tile", id="gid://shopify/Product/8414127849535", title="Fumosa Porcelain Tile",
    old=old_html("Fumosa porcelain tile, sold per sqm to the nearest full box.", ["Available in 600x600mm and 600x1200mm","Material: Porcelain","Slip rating: P3"]),
    intro="Fumosa is a bright white marble-look porcelain with bold grey veins, in the style of statuario marble. It is matt with a P3 slip rating, and the 600 x 1200 mm size lets the veins run long across a wall or floor the way real slab does.",
    use=["Bathroom floors and walls","Feature walls behind a bath or vanity in 600 x 1200 mm","Kitchen floors and living areas"],
    specs=porc("600 x 600 mm and 600 x 1200 mm","matt")+["Slip rating: P3",PER_M2],
    gtk=[P3, LAY_600, LAY_1200, "Dry-lay first and plan where the bold veins fall; a white grout keeps the slab look."],
    sources=[PL, SW+"fumosa-tile.png"], verified=False, notes="Not on the supplier's public site; facts from price list, look from price-list swatch.")

# ---------------- Astra, Sand, Bianco Greco (premium, P4) ----------------
add(handle="astra-white-porcelain-tile", id="gid://shopify/Product/8414127882303", title="Astra White Porcelain Tile",
    old=old_html("Astra White porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm and 600x600mm","Material: Porcelain","Slip rating: P4"]),
    intro="Astra White is a soft ivory-white porcelain with a gentle limestone texture and very little pattern. It is matt and P4 rated, so you can take a light tile through a bathroom, laundry and out to a covered alfresco without swapping to a rougher floor tile.",
    use=["Bathroom and laundry floors","Alfresco and covered outdoor floors","Open-plan living floors in a light neutral scheme"],
    specs=porc("298 x 600 mm and 600 x 600 mm","matt")+["Slip rating: P4",PER_M2],
    gtk=[P4, LAY_600, "Use a white or ivory grout to keep the floor looking like one surface.", "A P4 matt surface is slightly textured; a neutral cleaner and a soft brush keep it clean."],
    sources=[PL, SW+"astra-white-tile.png"], verified=False, notes="Not on the supplier's public site; facts from price list, look from price-list swatch.")

add(handle="astra-greige-porcelain-tile", id="gid://shopify/Product/8414127915071", title="Astra Greige Porcelain Tile",
    old=old_html("Astra Greige porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm and 600x600mm","Material: Porcelain","Slip rating: P4"]),
    intro="Astra Greige is a light grey-beige porcelain with a soft, cloudy stone look and faint veins. It is matt and P4 rated, which makes it a good inside-to-outside floor: bathroom, living room and alfresco in the same tile.",
    use=["Bathroom and laundry floors","Alfresco and covered patio floors","Living and hallway floors where grey feels too cold and beige too warm"],
    specs=porc("298 x 600 mm and 600 x 600 mm","matt")+["Slip rating: P4",PER_M2],
    gtk=[P4, LAY_600, "A greige or light grey grout blends with the base; white grout will show the grid.", "Mix tiles from several boxes so the cloudy variation spreads evenly."],
    sources=[PL, SW+"astra-greige-tile.png"], verified=False, notes="Not on the supplier's public site; facts from price list, look from price-list swatch.")

SAND_GTK = [P4, LAY_600, "Mix tiles from several boxes so the stone movement spreads evenly across the floor."]
add(handle="sand-white-porcelain-tile", id="gid://shopify/Product/8414127980607", title="Sand White Porcelain Tile",
    old=old_html("Sand White porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm and 600x600mm","Material: Porcelain","Slip rating: P4"]),
    intro="Sand White is a white-grey sandstone-look porcelain with soft diagonal movement across the face, like a sawn stone slab. It is matt and P4 rated, so it suits wet floors and covered outdoor areas as well as living rooms.",
    use=["Bathroom and laundry floors","Alfresco, verandah and covered patio floors","Living areas in a pale coastal scheme"],
    specs=porc("298 x 600 mm and 600 x 600 mm","matt")+["Slip rating: P4",PER_M2],
    gtk=SAND_GTK+["A white or light grey grout keeps the stone look continuous."],
    sources=[PL, SW+"sand-white-tile.png"], verified=False, notes="Not on the supplier's public site; facts from price list, look from price-list swatch.")

add(handle="sand-beige-porcelain-tile", id="gid://shopify/Product/8414128013375", title="Sand Beige Porcelain Tile",
    old=old_html("Sand Beige porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm and 600x600mm","Material: Porcelain","Slip rating: P4"]),
    intro="Sand Beige is a cream sandstone-look porcelain with soft, layered movement and a slightly textured matt face. It is P4 rated, so it is a good pick for a warm-toned floor that runs from the living room through to a covered alfresco.",
    use=["Alfresco, verandah and covered patio floors","Bathroom and laundry floors","Living and hallway floors in a warm neutral scheme"],
    specs=porc("298 x 600 mm and 600 x 600 mm","matt")+["Slip rating: P4",PER_M2],
    gtk=SAND_GTK+["Use a beige or sand grout so the joints blend in."],
    sources=[PL, SW+"sand-beige-tile.png"], verified=False, notes="Not on the supplier's public site; facts from price list, look from price-list swatch.")

add(handle="sand-grey-porcelain-tile", id="gid://shopify/Product/8414128078911", title="Sand Grey Porcelain Tile",
    old=old_html("Sand Grey porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm and 600x600mm","Material: Porcelain","Slip rating: P4"]),
    intro="Sand Grey is a light grey sandstone-look porcelain with soft diagonal veining and a slightly textured matt surface. It is P4 rated, so it handles bathroom and laundry floors and covered outdoor areas, and it pairs well with the Sand White and Sand Beige tiles in the same range.",
    use=["Bathroom and laundry floors","Alfresco and covered outdoor floors","Living and hallway floors"],
    specs=porc("298 x 600 mm and 600 x 600 mm","matt")+["Slip rating: P4",PER_M2],
    gtk=SAND_GTK+["A light grey grout keeps the joints quiet."],
    sources=[PL, SW+"sand-grey-tile.png"], verified=False, notes="Not on the supplier's public site; facts from price list, look from price-list swatch.")

add(handle="bianco-greco-porcelain-tile", id="gid://shopify/Product/8414128111679", title="Bianco Greco Porcelain Tile",
    old=old_html("Bianco Greco porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm and 600x600mm","Material: Porcelain","Slip rating: P4"]),
    intro="Bianco Greco is a white porcelain with scattered pale stone chips, like a light terrazzo or ceppo stone. It is matt and P4 rated, so you get a bright, slip-resistant floor that hides the dust and sand that a plain white tile would show.",
    use=["Bathroom, laundry and kitchen floors","Alfresco and covered outdoor floors","Walls where you want a little texture in a white scheme"],
    specs=porc("298 x 600 mm and 600 x 600 mm","matt")+["Slip rating: P4",PER_M2],
    gtk=[P4, LAY_600, "Mix tiles from several boxes so the chip pattern stays even.", "An off-white grout blends with the base; a grey grout shows the grid."],
    sources=[PL, SW+"bianco-greco-tile.png"], verified=False, notes="Not on the supplier's public site; facts from price list, look from price-list swatch.")

# ---------------- Caliza, E-Time, Oak Aube ----------------
add(handle="caliza-porcelain-tile", id="gid://shopify/Product/8414128930879", title="Caliza Porcelain Tile",
    old=old_html("Caliza porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm","Material: Porcelain"]),
    intro="Caliza is a white marble-look porcelain with fine grey veins in the style of carrara marble, in a matt finish. No slip rating is listed for this tile, so treat it as a wall tile or a dry-area floor tile.",
    use=["Bathroom and ensuite walls","Kitchen splashbacks","Dry floors such as a hallway or bedroom"],
    specs=porc("298 x 600 mm","matt")+["Slip rating: not listed",PER_M2],
    gtk=["No slip rating has been supplied, so keep it off shower and other wet-area floors.", LAY_300, "Stack-bond or brick-bond with a white grout to keep the marble look continuous."],
    sources=[PL, SW+"caliza-tile.png"], verified=False, notes="Not on the supplier's public site; price list gives no slip rating.")

add(handle="e-time-calcare-porcelain-tile", id="gid://shopify/Product/8414128963647", title="E-Time Calcare Porcelain Tile",
    old=old_html("E-Time Calcare porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm","Material: Porcelain","Structured surface","Slip rating: P4"]),
    intro="E-Time Calcare is a sand-coloured limestone-look porcelain with soft horizontal banding and a structured (textured) surface you can feel underfoot. The texture gives it a P4 slip rating, which is why it is the one to reach for on an alfresco, pool surround or outdoor step.",
    use=["Alfresco, verandah and covered patio floors","Bathroom and laundry floors","Outdoor steps and entries"],
    specs=porc("298 x 600 mm","structured")+["Slip rating: P4",PER_M2],
    gtk=[P4, LAY_300, "A structured surface holds dirt in the texture; hose or scrub with a neutral cleaner rather than letting it build up.", "Use a sand-coloured grout outside so the joints do not show marks."],
    sources=[PL, SW+"e-time-calcare-tile.png"], verified=False, notes="Not on the supplier's public site; facts from price list and old description.")

add(handle="e-time-chiaro-porcelain-tile", id="gid://shopify/Product/8414129029183", title="E-Time Chiaro Porcelain Tile",
    old=old_html("E-Time Chiaro porcelain tile, sold per sqm to the nearest full box.", ["Available in 300x600mm","Material: Porcelain","Structured surface","Slip rating: P4"]),
    intro="E-Time Chiaro is a mid-grey stone-look porcelain with faint layered banding and a structured (textured) surface. The texture gives it a P4 slip rating, so it suits outdoor and wet floors where a smooth matt tile would be risky.",
    use=["Alfresco, verandah and covered patio floors","Bathroom and laundry floors","Outdoor steps, entries and paths under cover"],
    specs=porc("298 x 600 mm","structured")+["Slip rating: P4",PER_M2],
    gtk=[P4, LAY_300, "A structured surface holds dirt in the texture; hose or scrub with a neutral cleaner rather than letting it build up.", "Grey grout keeps outdoor joints looking clean."],
    sources=[PL, SW+"e-time-chiaro-tile.png"], verified=False, notes="Not on the supplier's public site; facts from price list and old description.")

add(handle="oak-aube-timber-look-porcelain-tile", id="gid://shopify/Product/8414129061951", title="Oak Aube Timber Look Porcelain Tile",
    old=old_html("Oak Aube Timber Look porcelain tile, sold per sqm to the nearest full box.", ["Available in 200x1200mm","Material: Porcelain","Timber-look plank, 196 x 1200 x 9mm","Slip rating: P3"]),
    intro="Oak Aube is a pale oak timber-look porcelain plank with a fine, straight grain and a light, washed colour. It gives you the look of a blonde timber floor in a bathroom, laundry or alfresco where real timber would not last, and the matt face carries a P3 slip rating.",
    use=["Bathroom and laundry floors with a timber look","Living areas and hallways","Covered alfresco floors where timber would weather"],
    specs=["Material: glazed porcelain","Size: 196 x 1200 x 9 mm plank","Finish: matt","Slip rating: P3",PER_M2],
    gtk=[P3, "Lay planks in a random or one-third stagger, not a half stagger, so any slight bow in the long tiles does not lip.", "Back-butter every plank on a flat floor and use a levelling system on the long edges.", "A beige or light brown grout in a narrow joint keeps the timber look."],
    sources=[PL, SW+"oak-aube-tile.png"], verified=False, notes="Not on the supplier's public site; facts from price list and old description, look from price-list swatch.")

# ---------------- Ceramic small format ----------------
SUBWAY_SPEC = lambda fin: ["Material: glazed ceramic","Size: 100 x 300 x 8 mm","Finish: "+fin,"Wall tile",PER_M2]
add(handle="subway-gloss-white-ceramic-tile", id="gid://shopify/Product/8414129127487", title="Subway Gloss White Ceramic Tile",
    old=old_html("Subway Gloss White ceramic tile, sold per sqm to the nearest full box.", ["Available in 100x300mm","Material: Ceramic","8mm thick"]),
    intro="A plain white gloss subway tile, 100 x 300 mm, with a flat face and a bright white glaze. It is the standard splashback and shower wall tile: cheap to buy, easy to lay, easy to wipe down, and it goes with every colour of grout and tapware.",
    use=["Kitchen splashbacks","Shower and bathroom walls","Laundry walls behind the trough"],
    specs=SUBWAY_SPEC("gloss"),
    gtk=[WALL_ONLY, CERAMIC_LAY, "Lay it in brick bond, stack bond or herringbone; a dark grout shows the pattern, a white grout hides it.", "Gloss glaze shows adhesive and grout haze, so wipe tiles down as you go."],
    sources=[SUP+"subway-gloss-white-ceramic-small-format-tile", PL], verified=True, notes="")

add(handle="subway-matt-white-ceramic-tile", id="gid://shopify/Product/8414129160255", title="Subway Matt White Ceramic Tile",
    old=old_html("Subway Matt White ceramic tile, sold per sqm to the nearest full box.", ["Available in 100x300mm","Material: Ceramic","8mm thick"]),
    intro="A plain white subway tile, 100 x 300 mm, with a satin (low-sheen) glaze instead of gloss. It gives the same classic subway layout with less reflection, which suits a room with downlights or a lot of glass where gloss tiles glare.",
    use=["Kitchen splashbacks","Shower and bathroom walls","Laundry and toilet walls"],
    specs=SUBWAY_SPEC("satin (listed as matt)"),
    gtk=[WALL_ONLY, CERAMIC_LAY, "Lay it in brick bond, stack bond or herringbone; a grey grout makes the pattern read, white keeps it quiet.", "Satin glazes mark more easily than gloss; use a non-scratch cleaner."],
    sources=[SUP+"subway-matt-white-ceramic-small-format-range-tile", PL], verified=True, notes="Price list and variant call the finish Satin; title says Matt.")

SUBWAVE_SPEC = lambda fin: ["Material: glazed ceramic","Size: 75 x 300 x 8 mm","Finish: "+fin,"Wall tile with a gently rippled face",PER_M2]
SUBWAVE_GTK = [WALL_ONLY, CERAMIC_LAY, "The rippled face catches light differently across each tile; stack bond or brick bond both work.", "Use a matching grout colour so the wave, not the joint, is what you see."]
add(handle="subwave-gloss-white-ceramic-tile", id="gid://shopify/Product/8414129193023", title="Subwave Gloss White Ceramic Tile",
    old=old_html("Subwave Gloss White ceramic tile, sold per sqm to the nearest full box.", ["Available in 75x300mm","Material: Ceramic","Wave-profile wall tile, 8mm thick"]),
    intro="Subwave Gloss White is a slim 75 x 300 mm white wall tile with a gently rippled, hand-made style face. The gloss glaze picks up the ripple as soft highlights, so a plain white wall gets texture without adding a colour.",
    use=["Kitchen splashbacks","Shower and bathroom walls","Feature walls behind a vanity or bath"],
    specs=SUBWAVE_SPEC("gloss"),
    gtk=SUBWAVE_GTK,
    sources=[SUP+"subwave-gloss-white-ceramic-small-format-range-tile", PL], verified=True, notes="")

add(handle="subwave-matt-white-ceramic-tile", id="gid://shopify/Product/8414129225791", title="Subwave Matt White Ceramic Tile",
    old=old_html("Subwave Matt White ceramic tile, sold per sqm to the nearest full box.", ["Available in 75x300mm","Material: Ceramic","Wave-profile wall tile, 8mm thick"]),
    intro="Subwave Matt White is a slim 75 x 300 mm white wall tile with a gently rippled face and a satin (low-sheen) glaze. The ripple gives a plain white wall some texture, and the satin finish keeps it soft rather than shiny.",
    use=["Kitchen splashbacks","Shower and bathroom walls","Feature walls in a white-on-white scheme"],
    specs=SUBWAVE_SPEC("satin (listed as matt)"),
    gtk=SUBWAVE_GTK+["Satin glazes mark more easily than gloss; use a non-scratch cleaner."],
    sources=[SUP+"subwave-matt-white-ceramic-small-format-range-tile", PL], verified=True, notes="Price list and variant call the finish Satin; title says Matt.")

add(handle="subwave-nude-ceramic-tile", id="gid://shopify/Product/8414129815615", title="Subwave Nude Ceramic Tile",
    old=old_html("Subwave Nude ceramic tile, sold per sqm to the nearest full box.", ["Available in 75x300mm","Material: Ceramic","Wave-profile wall tile, 8mm thick"]),
    intro="Subwave Nude is a slim 75 x 300 mm wall tile in a warm, creamy off-white with a gently rippled face and gloss glaze. It is the warm colour in the Subwave range and suits brass or brushed nickel tapware and timber vanities.",
    use=["Kitchen splashbacks","Shower and bathroom walls","Feature walls behind a vanity"],
    specs=SUBWAVE_SPEC("gloss"),
    gtk=SUBWAVE_GTK,
    sources=[SUP+"subwave-nude-ceramic-small-format-range-tile", PL], verified=True, notes="")

add(handle="subwave-grey-ceramic-tile", id="gid://shopify/Product/8414129848383", title="Subwave Grey Ceramic Tile",
    old=old_html("Subwave Grey ceramic tile, sold per sqm to the nearest full box.", ["Available in 75x300mm","Material: Ceramic","Wave-profile wall tile, 8mm thick"]),
    intro="Subwave Grey is a slim 75 x 300 mm wall tile in a mid grey with soft concrete-style variation, a gently rippled face and gloss glaze. It gives a splashback or shower wall some depth without the dark, flat look of a plain grey tile.",
    use=["Kitchen splashbacks","Shower and bathroom walls","Feature walls in a grey or black-and-white scheme"],
    specs=SUBWAVE_SPEC("gloss"),
    gtk=SUBWAVE_GTK,
    sources=[SUP+"subwave-grey-ceramic-small-format-range-tile", PL], verified=True, notes="")

# ---------------- Ceramic 300x600 wall ----------------
CW_SPEC = lambda fin: ["Material: glazed ceramic","Size: 300 x 600 x 9.5 mm","Finish: "+fin,"Wall tile",PER_M2]
CW_GTK = [WALL_ONLY, "Lay with a wall tile adhesive on a flat, primed substrate; a levelling system keeps the 600 mm edges flush.", "Ceramic cuts cleanly with a manual tile cutter, which keeps the job quick."]
add(handle="white-ceramic-wall-tile", id="gid://shopify/Product/8414129881151", title="White Ceramic Wall Tile",
    old=old_html("White ceramic tile, sold per sqm to the nearest full box.", ["Available in 300x600mm","Gloss or Matt finish","Material: Ceramic","9.5mm thick"]),
    intro="A plain white 300 x 600 mm ceramic wall tile in your choice of gloss or matt glaze. It is the basic bathroom wall tile: bright, flat and quick to lay, and it lets the floor tile, vanity and tapware do the talking.",
    use=["Bathroom, ensuite and toilet walls","Shower walls","Laundry and kitchen walls"],
    specs=CW_SPEC("gloss or matt"),
    gtk=CW_GTK+["Gloss wipes clean and bounces light; matt hides water spots better in a shower.", "White grout keeps it quiet; grey grout shows the grid."],
    sources=[SUP+"gloss-white-ceramic-wall-range-300x600-tile", SUP+"matt-white-ceramic-wall-range-300x600-tile", PL], verified=True, notes="Supplier lists gloss and matt as two products; ours is one product with a finish option.")

add(handle="eternal-marble-ceramic-wall-tile", id="gid://shopify/Product/8414129913919", title="Eternal Marble Ceramic Wall Tile",
    old=old_html("Eternal Marble ceramic tile, sold per sqm to the nearest full box.", ["Available in 300x600mm","Material: Ceramic","9.5mm thick"]),
    intro="Eternal Marble is a 300 x 600 mm gloss ceramic wall tile with a bright white base and bold grey veins, in the style of calacatta marble. It gives a bathroom wall the slab-marble look at a wall-tile price, and the gloss glaze wipes clean.",
    use=["Bathroom and ensuite walls","Shower walls and niches","Feature walls behind a vanity or bath"],
    specs=CW_SPEC("gloss"),
    gtk=CW_GTK+["Dry-lay and plan where the bold veins fall; a white grout keeps the marble look continuous."],
    sources=[SUP+"eternal-marble-ceramic-wall-range-300x600-tile", PL], verified=True, notes="")

add(handle="eternal-carrara-ceramic-wall-tile", id="gid://shopify/Product/8414129946687", title="Eternal Carrara Ceramic Wall Tile",
    old=old_html("Eternal Carrara ceramic tile, sold per sqm to the nearest full box.", ["Available in 300x600mm","Material: Ceramic","9.5mm thick"]),
    intro="Eternal Carrara is a 300 x 600 mm gloss ceramic wall tile with a white base and soft, fine grey veining, in the style of carrara marble. It is the quieter of the two marble-look wall tiles and suits a whole bathroom rather than just a feature wall.",
    use=["Bathroom, ensuite and toilet walls","Shower walls","Kitchen splashbacks"],
    specs=CW_SPEC("gloss"),
    gtk=CW_GTK+["Mix tiles from several boxes so the veining spreads evenly; white grout keeps it looking like one surface."],
    sources=[SUP+"eternal-carrara-ceramic-wall-range-300x600-tile", PL], verified=True, notes="")

add(handle="element-grey-ceramic-wall-tile", id="gid://shopify/Product/8414129979455", title="Element Grey Ceramic Wall Tile",
    old=old_html("Element Grey ceramic tile, sold per sqm to the nearest full box.", ["Available in 300x600mm","Material: Ceramic","9.5mm thick"]),
    intro="Element Grey is a 300 x 600 mm gloss ceramic wall tile in a light grey-green stone look with soft white veining. It is a mid-tone wall that sits well with white floors and either chrome or black tapware.",
    use=["Bathroom and ensuite walls","Shower walls","Laundry walls"],
    specs=CW_SPEC("gloss"),
    gtk=CW_GTK+["A light grey grout blends in; white grout shows the grid."],
    sources=[SUP+"element-grey-ceramic-wall-range-300x600-tile", PL], verified=True, notes="")

add(handle="whisper-grey-ceramic-wall-tile", id="gid://shopify/Product/8414130012223", title="Whisper Grey Ceramic Wall Tile",
    old=old_html("Whisper Grey ceramic tile, sold per sqm to the nearest full box.", ["Available in 300x600mm","Material: Ceramic","9.5mm thick"]),
    intro="Whisper Grey is a 300 x 600 mm gloss ceramic wall tile in a pale, warm grey stone look with fine veining. It is lighter and warmer than Element Grey and works as an all-over bathroom wall where plain white feels too stark.",
    use=["Bathroom, ensuite and toilet walls","Shower walls","Kitchen splashbacks"],
    specs=CW_SPEC("gloss"),
    gtk=CW_GTK+["A light grey or warm white grout keeps the wall looking like one surface."],
    sources=[SUP+"element-whisper-grey-ceramic-wall-range-300x600-tile", PL], verified=True, notes="Supplier lists it as Element Whisper Grey.")

# ---------------- Natural stone mosaics (per sheet) ----------------
def mosaic(sheet, inlay):
    s = ["Material: natural stone, polished", "Sheet size: " + sheet]
    if inlay: s.append("Inlay: " + inlay)
    s.append("Sold per sheet.")
    return s
MOS_GTK_METAL = [STONE_CARE, STONE_LAY, "Walls and dry floors; polished stone and metal are slippery when wet, so keep it off shower floors."]
MOS_GTK = [STONE_CARE, STONE_LAY.replace(" and metal", ""), "Walls and dry floors; polished stone is slippery when wet, so keep it off shower floors."]

add(handle="hex-crystal-white-mosaic-tile", id="gid://shopify/Product/8414130044991", title="Hex Crystal White Mosaic Tile",
    old=old_html("Hex Crystal White natural stone mosaic, sold per sheet.", ["Available in 305x330mm","Material: Natural stone","304 stainless steel inlay"]),
    intro="Hex Crystal White is a polished white marble hexagon mosaic with small triangular 304 stainless steel inlays set into some of the pieces, so a plain white hex wall gets a few metallic flashes. It comes mesh-mounted on a 305 x 330 mm sheet.",
    use=["Feature walls behind a vanity or in a shower niche","Kitchen splashbacks","Bathroom walls where you want a little metal to match the tapware"],
    specs=mosaic("305 x 330 mm", "304 stainless steel"),
    gtk=MOS_GTK_METAL,
    sources=[PL, SW+"hex-crystal-white-mosaic.png"], verified=False, notes="Not on the supplier's public site; facts from price list and old description, look from price-list swatch.")

add(handle="hex-black-and-white-roots-mosaic-tile", id="gid://shopify/Product/8414130798655", title="Hex Black and White Roots Mosaic Tile",
    old=old_html("Hex Black and White Roots natural stone mosaic, sold per sheet.", ["Available in 305x330mm","Material: Natural stone","304 stainless steel inlay"]),
    intro="Hex Black and White Roots is a polished dark marble hexagon mosaic, near-black with fine white veins, with small triangular 304 stainless steel inlays set into some pieces. It is the dark version of the Hex Crystal White sheet and comes mesh-mounted at 305 x 330 mm.",
    use=["Feature walls behind a vanity or bath","Shower niches","Powder room walls where a small area can carry a dark tile"],
    specs=mosaic("305 x 330 mm", "304 stainless steel"),
    gtk=MOS_GTK_METAL+["Use a charcoal grout so the hexagons read as one dark surface."],
    sources=[PL, SW+"hex-black-white-roots-mosaic.png"], verified=False, notes="Not on the supplier's public site; facts from price list and old description, look from price-list swatch.")

add(handle="arrow-crystal-white-mosaic-tile", id="gid://shopify/Product/8414130864191", title="Arrow Crystal White Mosaic Tile",
    old=old_html("Arrow Crystal White natural stone mosaic, sold per sheet.", ["Available in 300x260mm","Material: Natural stone","Aluminium inlay"]),
    intro="Arrow Crystal White is a polished white marble mosaic cut into chevron (arrow) pieces, with thin aluminium strips running down the point of each arrow. The metal lines turn a white wall into a pattern, and the sheet is mesh-mounted at 300 x 260 mm.",
    use=["Feature walls behind a vanity or in a shower niche","Kitchen splashbacks","Bathroom walls in a white and metallic scheme"],
    specs=mosaic("300 x 260 mm", "aluminium"),
    gtk=MOS_GTK_METAL+["Check the arrow direction on every sheet before it goes on the wall."],
    sources=[PL, SW+"arrow-crystal-white-mosaic.png"], verified=False, notes="Not on the supplier's public site; facts from price list and old description, look from price-list swatch.")

add(handle="crystal-white-black-jade-mosaic-tile", id="gid://shopify/Product/8414130896959", title="Crystal White Black Jade Mosaic Tile",
    old=old_html("Crystal White Black Jade natural stone mosaic, sold per sheet.", ["Available in 170x295mm","Material: Natural stone","Stainless steel inlay"]),
    intro="Crystal White Black Jade is a polished marble mosaic that mixes white and dark grey-black stone in angled, chevron-style pieces with thin stainless steel strips between them. It is a graphic, two-tone pattern for a small feature area, mesh-mounted on a 170 x 295 mm sheet.",
    use=["Feature strips and shower niches","Behind a vanity or bar","Kitchen splashbacks in a black-and-white scheme"],
    specs=mosaic("170 x 295 mm", "stainless steel"),
    gtk=MOS_GTK_METAL+["The sheet is small, so plan the layout and count sheets carefully before cutting."],
    sources=[PL, SW+"crystal-white-black-jade-mosaic.png"], verified=False, notes="Not on the supplier's public site; facts from price list and old description, look from price-list swatch.")

add(handle="crystal-white-indian-green-mosaic-tile", id="gid://shopify/Product/8414130929727", title="Crystal White Indian Green Mosaic Tile",
    old=old_html("Crystal White Indian Green natural stone mosaic, sold per sheet.", ["Available in 285x235mm","Material: Natural stone","Stainless steel inlay"]),
    intro="Crystal White Indian Green is a polished marble mosaic of white and deep green stone cut into arched, scalloped pieces with thin stainless steel strips between them. The green marble gives a bathroom or splashback a strong colour, and the sheet is mesh-mounted at 285 x 235 mm.",
    use=["Feature walls and shower niches","Kitchen splashbacks","Powder room walls"],
    specs=mosaic("285 x 235 mm", "stainless steel"),
    gtk=MOS_GTK_METAL+["Green marble varies a lot from sheet to sheet; lay sheets out and shuffle them before fixing."],
    sources=[PL, SW+"crystal-white-indian-green-mosaic.png"], verified=False, notes="Not on the supplier's public site; facts from price list and old description, look from price-list swatch.")

add(handle="herringbone-snow-plum-mosaic-tile", id="gid://shopify/Product/8414130962495", title="Herringbone Snow Plum Mosaic Tile",
    old=old_html("Herringbone Snow Plum natural stone mosaic, sold per sheet.", ["Material: Natural stone"]),
    intro="Herringbone Snow Plum is a polished natural stone mosaic in a herringbone layout, cut from a white marble with grey and plum-grey veining. The herringbone pattern comes pre-set on a mesh sheet, so you get the look without cutting hundreds of small pieces.",
    use=["Feature walls behind a vanity or bath","Shower niches and splashbacks","Bathroom walls in a grey and white scheme"],
    specs=mosaic("not listed", None),
    gtk=MOS_GTK+["Sheet size is not listed; measure a sheet before you work out quantities.", "A light grey grout blends with the veining."],
    sources=[PL, SW+"herringbone-snow-plum-mosaic.png"], verified=False, notes="Price list gives no sheet size. Not on the supplier's public site.")

add(handle="pools-red-norwegian-mosaic-tile", id="gid://shopify/Product/8414130995263", title="Pools Red Norwegian Mosaic Tile",
    old=old_html("Pools Red Norwegian natural stone mosaic, sold per sheet.", ["Available in 295x300mm","Material: Natural stone"]),
    intro="Pools Red Norwegian is a polished natural stone mosaic of elongated, rounded-end pieces in a pink-red marble with grey-green veining. It is a warm, colourful stone for a small feature area, mesh-mounted on a 295 x 300 mm sheet.",
    use=["Feature walls behind a vanity or bath","Shower niches","Powder room and splashback walls"],
    specs=mosaic("295 x 300 mm", None),
    gtk=MOS_GTK+["Colour varies a lot from sheet to sheet; lay sheets out and shuffle them before fixing.", "A warm grey or pink-beige grout keeps the pieces reading as stone."],
    sources=[PL, SW+"pools-red-norwegian-mosaic.png"], verified=False, notes="Not on the supplier's public site; facts from price list and old description, look from price-list swatch.")

add(handle="pools-snow-plum-mosaic-tile", id="gid://shopify/Product/8414131060799", title="Pools Snow Plum Mosaic Tile",
    old=old_html("Pools Snow Plum natural stone mosaic, sold per sheet.", ["Available in 295x300mm","Material: Natural stone"]),
    intro="Pools Snow Plum is a polished natural stone mosaic of elongated, rounded-end pieces cut from a white marble with grey and plum-grey veining, laid in a staggered brick pattern on the sheet. It is the same stone as the Herringbone Snow Plum sheet in a softer shape, mesh-mounted at 295 x 300 mm.",
    use=["Feature walls behind a vanity or bath","Shower niches","Bathroom and splashback walls in a grey and white scheme"],
    specs=mosaic("295 x 300 mm", None),
    gtk=MOS_GTK+["Mix sheets from the box so the heavier-veined pieces spread out.", "A light grey grout blends with the veining."],
    sources=[PL, SW+"pools-snow-plum-mosaic.png"], verified=False, notes="Not on the supplier's public site; facts from price list and old description, look from price-list swatch.")

# ---------------- output ----------------
BAD = re.compile(r"\$|\btrade\b|in stock|stock|showroom|Maddington|deliver|pick up|shipping|Eternity|DSA|Bathroom City|elevate|stunning|seamless|!|curated|timeless|discover|unlock|premium quality|look no further|perfect for any|transform|—|–", re.I)
out = []
bad = []
for p in P:
    new = build(p)
    n = words(new)
    hits = [m.group(0) for m in BAD.finditer(new)]
    if hits or not (90 <= n <= 200):
        bad.append((p["handle"], n, hits))
    out.append({"id": p["id"], "handle": p["handle"], "title": p["title"], "old": p["old"], "new": new,
                "sources": p["sources"], "verified": p["verified"], "notes": p["notes"], "words": n})
json.dump(out, open("store-content/descriptions/tiles-2026-10-24.json", "w"), indent=1, ensure_ascii=False)
print(len(out), "products;", sum(1 for o in out if o["verified"]), "verified")
for b in bad: print("CHECK", b)
assert len(out) == 47 and len({o["handle"] for o in out}) == 47, "expected 47 unique products"
