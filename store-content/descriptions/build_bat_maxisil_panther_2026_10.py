import json, re, html as H

OUT = "/home/user/Excellent-Tiling-Services-/store-content/descriptions/bat-maxisil-panther-2026-10-24.json"
todo = json.load(open("/home/user/Excellent-Tiling-Services-/store-content/descriptions/todo-bat-maxisil-panther.json"))
byh = {t["handle"]: t for t in todo}

BUY = "<p>Buy the {t} online from Excellent Tiling Services in Perth: genuine {b} stock for tilers, builders and DIY renovators.</p>"
DEL = "<p><strong>Delivery:</strong> Ships Australia-wide from Perth, or pick up from our showroom.</p>"
def bat(t, codes, lead="", b="BAT"):
    return lead + BUY.format(t=t, b=b) + f"<p><strong>Code{'s' if ',' in codes else ''}:</strong> {codes}</p>" + DEL

MX = "https://maxisil.com.au/products/"
RD = "https://www.robertsdesigns.com.au/product/"
BT = "https://battrims.com/product/"
GROUT_SRC = ["https://maxisil.com.au/products/grout/", "https://maxisil.com.au/wp-content/uploads/2024/03/Maxisil-Grout-TDS-20.2.2024.pdf"]
GROUT_COLOURS = "Anthracite, Black, Grey, Havana, Light Grey, Mid Grey, Stone, Snow White, Travertine and White"

def grout(kg, water, cov_small, cov_large, old_has_suitable):
    return (f"<p>Maxisil Grout is a flexible, sand-free cement grout made to colour match the Maxisil silicone range, so the joint and the "
            f"corner bead come out the same shade. This {kg} kg bag suits 1 to 15 mm joints on walls and floors, inside and out.</p>"
            "<h3>Use it for</h3><ul><li>Ceramic, porcelain, marble, natural stone, terrazzo, glass and mosaic tiles</li></ul>"
            "<h3>Features</h3><ul><li>Classified CG2, polymer modified</li><li>Sand-free with a smooth finish</li>"
            "<li>Hydrophobic: low water absorption and mould resistant</li><li>Easy to clean off once dry</li></ul>"
            f"<h3>Specifications</h3><ul><li>Joint widths: 1 to 15 mm</li><li>Bag: {kg} kg</li>"
            f"<li>Mixing water: about {water} per bag (guide only)</li><li>Pot life: about 1 hour at 23°C</li>"
            f"<li>Coverage guide: {cov_small}</li>"
            f"<li>Colours: {GROUT_COLOURS}</li></ul>"
            "<h3>Good to know</h3><ul><li>Add powder to water, mix until lump free, stand 3 to 4 minutes and stir again</li>"
            "<li>Grout 5 to 8 m² at a time and sponge off with little water to avoid efflorescence</li>"
            "<li>Allow 24 hours before the final haze clean. Not for movement joints</li>"
            "<li>15 year Maxisil warranty when applied to AS 3958.1 and the data sheet</li></ul>")

R = []
def add(handle, old, new, sources, verified=True, notes=""):
    t = byh[handle]
    R.append({"id": t["id"], "handle": handle, "title": t["title"], "old": old, "new": new,
              "sources": sources, "verified": verified, "notes": notes})

# ---------------- MAXISIL ----------------
add("smoothtex-n",
 '<ul>\n<li class="p1">Features: Increased Workability on silicone</li>\n<li class="p1">Mixing Ratio: Use undiluted</li>\n<li class="p1">Suitable for: Maxisil Natural Stone</li>\n</ul>',
 "<p>Maxisil Smoothtex N is the smoothing agent made for tooling Maxisil Natural Stone silicone on marble, granite and other natural stone. It is formulated to cut the risk of the staining that ordinary soapy smoothing liquids can leave on porous stone.</p>"
 "<h3>Use it for</h3><ul><li>Tooling off fresh silicone beads where the sealant meets natural stone</li><li>Smoothing Maxisil Natural Stone sealant</li></ul>"
 "<h3>Features</h3><ul><li>Increased workability on silicone</li><li>Keeps the shine of the sealant and does not wash the colour pigment out</li><li>Dermatologically tested ingredients</li></ul>"
 "<h3>Specifications</h3><ul><li>Mixing ratio: use undiluted</li><li>Sizes: 250 ml (RDX2019) and 1 litre (RDX2020)</li><li>Store frost free between 0°C and 35°C</li></ul>"
 "<h3>Good to know</h3><ul><li>Use it sparingly: dip the Maxisil Applicator in the liquid rather than wetting the joint</li><li>Rinse any excess off the stone with clean water before it dries</li>"
 "<li>Tool matt colours once only, as repeat passes turn a matt finish glossy</li><li>Very dark stones such as Nero Impala can still mark, so test a small area first</li></ul>",
 [MX+"maxisil-smoothtex-n/", "https://maxisil.com.au/wp-content/uploads/2024/02/Maxisil-Smoothtex-N-Technical-Data-Sheet.pdf", RD+"smoothtex-n/"])

add("maxisil-grout-2kg",
 '<ul>\n<li>Joint widths: 1-15mm</li>\n<li>Mould resistant: Yes</li>\n<li>Features: Hydrophobic, Sand-free and colour-fast, Polymer modified CG2 Grout</li>\n</ul>',
 grout(2, "500 to 800 ml", "100 x 200 mm tiles at a 1.5 mm joint about 8 m²", "400 x 400 mm tiles at a 3 mm joint about 11.75 m²", False)
 .replace("<li>Sand-free with a smooth finish</li>", "<li>Sand-free, colour-fast, smooth finish</li>"),
 GROUT_SRC + [RD+"maxisil-grout-2kg/"])

add("smoothtex-a",
 '<ul>\n<li class="p1">Features: Increased Workability on silicone</li>\n<li class="p1">Mixing Ratio: 2:1 (Smoothtex:Water)</li>\n<li class="p1">Suitable for: Maxisil Wet Area and Maxisil Pool</li>\n</ul>',
 "<p>Maxisil Smoothtex A is the smoothing agent for tooling Maxisil Wet Area and Maxisil Pool silicone. A dip of the applicator in it lets the bead glide to a clean, glossy line without dragging or smearing fresh sealant.</p>"
 "<h3>Use it for</h3><ul><li>Smoothing Maxisil Wet Area and Maxisil Pool sealant in showers, around baths, vanities and pool joints</li><li>Silicone, polyurethane and MS hybrid polymer sealants</li></ul>"
 "<h3>Features</h3><ul><li>Increased workability on silicone</li><li>Keeps the shine of the sealant surface and does not wash out the colour pigment</li><li>Dermatologically tested ingredients that will not dry your skin</li></ul>"
 "<h3>Specifications</h3><ul><li>Mixing ratio: 2 parts Smoothtex A to 1 part water</li><li>Sizes: 250 ml (RDX2000), 1 litre (RDX1999) and 5 litre (RDX2002)</li><li>Store frost free between 0°C and 35°C</li></ul>"
 "<h3>Good to know</h3><ul><li>Not for marble or other natural stone. Use Smoothtex N there</li><li>Wipe off visible water streaks straight after sealing or they can set permanently</li>"
 "<li>Use sparingly. Dried residue on the sealant can leave matt or bright spots</li><li>Pairs with the Maxisil Applicator and 500 ml spray bottle</li></ul>",
 [MX+"maxisil-smoothtex-a/", "https://maxisil.com.au/wp-content/uploads/2024/02/Maxisil-Smoothtex-A-Technical-Data-Sheet.pdf", RD+"smoothtex-a/"])

def primer(num, code, sub_wet, sub_stone, sub_pool, lead):
    return (f"<p>Maxisil Primer {num} is a 250 ml surface primer that gives Maxisil silicone a stronger, longer lasting bond on {lead}. Brush it on before sealing and the sealant grips surfaces it would otherwise struggle on.</p>"
            f"<h3>Use it for</h3><ul><li>With Maxisil Wet Area on {sub_wet}</li><li>With Maxisil Natural Stone on {sub_stone}</li><li>With Maxisil Pool on {sub_pool}</li></ul>"
            "<h3>Features</h3><ul><li>Improves sealant adhesion and durability on hard to bond surfaces</li><li>Part of the Maxisil cleaner, primer and sealant system</li></ul>"
            f"<h3>Specifications</h3><ul><li>Size: 250 ml</li><li>Model: {code}</li></ul>"
            "<h3>Good to know</h3><ul><li>Clean the surface first: Maxisil Cleaner on non-porous surfaces, a wire brush on porous ones</li>"
            "<li>Maxisil data sheets say to let primer dry for about 2 hours before applying sealant</li>"
            "<li>Match the primer number to the surface. Maxisil publishes three primers (1215, 1216 and 1217) for different substrates</li></ul>")

add("maxisil-primer-1217",
 '<ul>\n<li>Size: 250ml</li>\n<li>Suitable for: Maxisil Wet Area (PVC), Maxisil Natural Stone (PVC, Fluorocarbons, Aluminium), Maxisil Pool (PVC, Fibreglass, Polyester)</li>\n</ul>',
 primer("1217", "RDX2016", "PVC", "PVC, fluorocarbons and aluminium", "PVC, fibreglass and polyester", "PVC, fibreglass and other plastics"),
 [MX+"primer-1217/", RD+"primer-1217/", "https://maxisil.com.au/wp-content/uploads/2017/07/Maxisil-Membrane-Technical-Data-Sheet.pdf"])

add("maxisil-primer-1215",
 '<ul>\n<li>Size: 250ml</li>\n<li>Suitable for: Maxisil Wet Area (Mortar, Brick, Untreated Wood), Maxisil Natural Stone (Concrete, Mortar, Brick, Plaster), Maxisil Pool (Chlorinated Rubber, Paint)</li>\n</ul>',
 primer("1215", "RDX2012", "mortar, brick and untreated wood", "concrete, mortar, brick and plaster", "chlorinated rubber paint", "porous surfaces such as mortar, brick, concrete and plaster"),
 [MX+"primer-1215/", RD+"primer-1215/", "https://maxisil.com.au/wp-content/uploads/2017/07/Maxisil-Membrane-Technical-Data-Sheet.pdf"])

add("maxisil-primer-1216",
 '<ul>\n<li>Size: 250ml</li>\n<li>Suitable for: Maxisil Wet Area (Anodised Aluminium, Chrome, Wood), Maxisil Natural Stone (Artificial Stone, Chrome, Stainless Steel), Maxisil Pool (Stainless Steel, Aluminium, Anodised Aluminium)</li>\n</ul>',
 primer("1216", "RDX2014", "anodised aluminium, chrome and wood", "artificial stone, chrome and stainless steel", "stainless steel, aluminium and anodised aluminium", "metals such as chrome, stainless steel and anodised aluminium"),
 [MX+"primer-1216/", RD+"primer-1216/", "https://maxisil.com.au/wp-content/uploads/2017/07/Maxisil-Membrane-Technical-Data-Sheet.pdf"])

add("maxisil-grout-10kg",
 '<ul>\n<li>Joint widths: 1-15mm</li>\n<li>Mould resistant: Yes</li>\n<li>Features: Hydrophobic, Sand-free and colour-fast Polymer modified CG2 Grout</li>\n<li>Suitable for: Most tile types including ceramic, porcelain, natural stone, glass and mosaics.</li>\n</ul>',
 grout(10, "2.6 litres", "100 x 200 mm tiles at a 1.5 mm joint about 40 m²", "600 x 600 mm tiles at a 5 mm joint about 42.5 m²", True)
 .replace("<li>Sand-free with a smooth finish</li>", "<li>Sand-free, colour-fast, smooth finish</li>"),
 GROUT_SRC + [RD+"maxisil-grout-10kg/"])

add("maxisil-grout-5kg",
 '<ul>\n<li>Joint widths: 1-15mm</li>\n<li>Mould resistant: Yes</li>\n<li>Features: Hydrophobic, Sand-free and colour-fast Polymer modified CG2 Grout</li>\n<li>Suitable for: Most tile types including ceramic, porcelain, natural stone, glass and mosaics.</li>\n</ul>',
 grout(5, "1.3 litres", "100 x 200 mm tiles at a 1.5 mm joint about 20 m²", "450 x 450 mm tiles at a 3 mm joint about 33 m²", True)
 .replace("<li>Sand-free with a smooth finish</li>", "<li>Sand-free, colour-fast, smooth finish</li>"),
 GROUT_SRC + [RD+"maxisil-grout-5kg/"])

add("maxisil-maxigrab-adhesive",
 '<ul>\n<li>\n<strong>Size:</strong> 290ml</li>\n<li>\n<strong>Strength:</strong> 360kg/10cm<sup>2</sup>\n</li>\n<li>\n<strong>Bonding time:</strong> 20min</li>\n<li>\n<strong>Features:</strong> Instant grab, Bonds to wet surfaces</li>\n<li>\n<strong>Suitable for:</strong> Natural stone and ceramics, Window sills, floor and decorative strips. General construction adhesive.</li>\n</ul>',
 "<p>Maxisil Maxigrab is a one part hybrid polymer (STP) construction adhesive with instant grab, so a sill, skirting tile or stone strip stays put without props. It bonds to damp surfaces, even under water, and will not stain natural stone.</p>"
 "<h3>Use it for</h3><ul><li>Bonding natural stone, ceramics, window sills, floor strips, decorative strips and stair treads</li>"
 "<li>Elastic fixing of wood, plastics, metals, glass and mineral surfaces, indoors and out</li><li>General construction adhesive and sealing jobs</li></ul>"
 "<h3>Features</h3><ul><li>Instant grab, bonds to wet surfaces</li><li>Handling strength after 20 minutes, functional strength after 3 hours</li>"
 "<li>Stays elastic to take up movement</li><li>Free of isocyanates and silicone, very low emission (EMICODE EC1 Plus)</li><li>Paintable with water based paints</li></ul>"
 "<h3>Specifications</h3><ul><li>Size: 290 ml cartridge</li><li>Strength: 360 kg per 10 cm²</li><li>Bonding time: 20 minutes</li>"
 "<li>Colours: Original is white (RDX4000), Crystal is clear (RDX4001)</li><li>Apply between +5°C and +40°C; resists -40°C to +90°C once cured</li><li>Skin time about 5 minutes, cures about 2 mm a day</li></ul>"
 "<h3>Good to know</h3><ul><li>Clean non-porous surfaces with Maxisil Cleaner first</li><li>Not for polypropylene, or for copper exposed to UV and heat</li><li>Shelf life 18 months (Original), 12 months (Crystal) from manufacture</li></ul>",
 [MX+"maxisil-maxigrab-adhesive-original/", MX+"maxisil-maxigrab-adhesive-crystal/", "https://maxisil.com.au/wp-content/uploads/2023/07/Maxigrab-Original-Technical-data-sheet-1.pdf", RD+"maxisil-maxigrab-adhesive/", "https://www.bunnings.com.au/brands/m/maxisil"])

add("maxisil-sausage-caulking-gun-600ml",
 '<p>Maxisil alloy sausage caulking gun for 600 ml sausage packs of silicone and sealant, with a high 18:1 thrust ratio for thick sealants.</p><ul>\n<li>Suits: 600 ml sausages</li>\n<li>Thrust ratio: 18:1</li>\n<li>Alloy construction</li>\n</ul>',
 "<p>The Maxisil Sausage Caulking Gun takes 600 ml foil sausage packs of silicone and sealant, the format tilers use on long runs because it holds twice the product of a cartridge and leaves far less packaging. The 18:1 thrust ratio pushes thick, cold sealant without wearing your hand out.</p>"
 "<h3>Use it for</h3><ul><li>600 ml sausage packs of silicone, polyurethane and hybrid sealants</li><li>Long bathroom, pool and expansion joint runs where cartridges run out too fast</li></ul>"
 "<h3>Features</h3><ul><li>Alloy barrel and frame built for daily site use</li><li>High 18:1 thrust ratio for thick sealants</li><li>Fits the Maxisil nozzle range</li></ul>"
 "<h3>Specifications</h3><ul><li>Suits: 600 ml sausages</li><li>Thrust ratio: 18:1</li><li>Construction: alloy</li><li>Model: RDXA3012</li></ul>"
 "<h3>Good to know</h3><ul><li>Snip one end of the sausage, drop it in the barrel and fit the nozzle cap before pumping</li><li>Pull the rod back after each run to stop the bead oozing</li><li>Wipe the barrel out while sealant is still soft</li></ul>",
 [RD+"maxisil-sausage-caulking-gun-600ml/"])

add("20-litre-maxisil-bucket",
 '<p>A 20 litre Maxisil bucket for the job site, handy for mixing, carrying water for clean-up or holding tools and materials.</p><ul>\n<li>Brand: Maxisil</li>\n<li>Size: 20 litre</li>\n<li>Box qty: 1 each</li>\n<li>Code: RDXT987</li>\n</ul>',
 "<p>The 20 Litre Maxisil Bucket is a plain, tough site bucket in the size tilers reach for most: big enough to mix a bag of grout or carry sponge water, small enough to move around a bathroom. It carries the Maxisil name, which also makes it easy to spot in a van full of look alike pails.</p>"
 "<h3>Use it for</h3><ul><li>Mixing grout, adhesive and additives</li><li>Grout wash up and sponge water</li><li>Soaking tools, carrying offcuts or holding spacers and wedges</li></ul>"
 "<h3>Features</h3><ul><li>20 litre capacity</li><li>Plastic construction for everyday site use</li><li>Branded Maxisil</li></ul>"
 "<h3>Specifications</h3><ul><li>Capacity: 20 litres</li><li>Model: RDXT987</li></ul>"
 "<h3>Good to know</h3><ul><li>Rinse out cement based grout before it sets or it will build up on the walls</li><li>Keep one bucket for mixing and a second for clean water so the sponge stays clean</li></ul>",
 [RD+"20-litre-maxisil-bucket-with-lid/"])

add("maxisil-corner-nozzles-3-pack",
 '<p>Maxisil corner nozzles for silicone cartridges, angled to make it easier to run a neat bead of sealant into corners.</p><ul>\n<li>\n<strong>Brand:</strong> Maxisil</li>\n<li>\n<strong>Feature:</strong> 45° angle</li>\n<li>\n<strong>Pack:</strong> 3 nozzles</li>\n<li>\n<strong>Box Qty:</strong> 10 each</li>\n</ul>',
 "<p>Maxisil Corner Nozzles put a 45 degree bend in the nozzle so you can run a bead into internal corners, behind toilets and under vanity lips without twisting the gun. They fit Maxisil cartridges snugly, which stops sealant squeezing out around a loose nozzle.</p>"
 "<h3>Use it for</h3><ul><li>Internal corners of showers and splashbacks</li><li>Tight spots behind cisterns, pipes and fittings</li><li>Any joint where a straight nozzle holds the gun at the wrong angle</li></ul>"
 "<h3>Features</h3><ul><li>45 degree angled tip</li><li>Made to fit all Maxisil sealant cartridges</li><li>Works with the Maxisil Extension Nozzles for extra reach</li></ul>"
 "<h3>Specifications</h3><ul><li>Pack: 3 nozzles</li><li>Model: RDXA2050a</li></ul>"
 "<h3>Good to know</h3><ul><li>Cut the tip at a slight angle to match the joint width before you start</li><li>A blocked nozzle can be cleared with the Maxisil Silicone Nozzle Unblocker rather than thrown away</li></ul>",
 [MX+"maxisil-corner-nozzles/", RD+"maxisil-corner-nozzles/"])

add("maxisil-spray-bottle-500ml",
 '<p>A 500ml Maxisil spray bottle for misting water or tooling solution on the job, such as when finishing sealant or cleaning down.</p><ul>\n<li>Brand: Maxisil</li>\n<li>Size: 500ml</li>\n<li>Box qty: 48 each</li>\n<li>Code: RDXT984</li>\n</ul>',
 "<p>The Maxisil Spray Bottle is a 500 ml trigger sprayer for misting smoothing agent or water over a fresh silicone bead before tooling. A fine mist is far easier to control than pouring, and it keeps the applicator wet without flooding the joint.</p>"
 "<h3>Use it for</h3><ul><li>Misting Maxisil Smoothtex A or Smoothtex N over sealant before smoothing</li><li>Dampening tiles and sponges during grout clean up</li><li>General wash down on the job</li></ul>"
 "<h3>Features</h3><ul><li>500 ml capacity with trigger spray head</li><li>Branded Maxisil so it is not mistaken for a chemical bottle</li></ul>"
 "<h3>Specifications</h3><ul><li>Size: 500 ml</li><li>Model: RDXT984</li></ul>"
 "<h3>Good to know</h3><ul><li>Maxisil recommends using smoothing agent sparingly, so a light mist is all you need</li><li>Label the bottle if you fill it with diluted Smoothtex A (2 parts to 1 part water)</li><li>Rinse after use so the nozzle does not clog</li></ul>",
 [RD+"maxisil-spray-bottle/", "https://maxisil.com.au/wp-content/uploads/2024/02/Maxisil-Smoothtex-A-Technical-Data-Sheet.pdf"])

add("maxisil-extension-nozzles-6-pk",
 '<p>Maxisil extension nozzles fit on sealant cartridges to reach into tight or deep spots when applying silicone and sealant.</p><ul>\n<li>Brand: Maxisil</li>\n<li>Feature: 100mm extension</li>\n<li>Pack: 6 nozzles</li>\n<li>Box qty: 10</li>\n<li>Code: RDXA2051</li>\n</ul>',
 "<p>Maxisil Extension Nozzles add 100 mm of reach to a sealant cartridge so the bead lands where you want it: behind a bath lip, down the back of a vanity or into a deep niche. They fit the Maxisil cartridge thread properly, so there is no leaking at the join.</p>"
 "<h3>Use it for</h3><ul><li>Deep or recessed joints a standard nozzle cannot reach</li><li>Sealing behind fixtures without pulling them out</li><li>Pairing with the Maxisil Corner Nozzles for reach and angle together</li></ul>"
 "<h3>Features</h3><ul><li>100 mm extension</li><li>Fits all Maxisil sealant cartridges and the Maxisil Corner Nozzles</li></ul>"
 "<h3>Specifications</h3><ul><li>Pack: 6 nozzles</li><li>Model: RDXA2051</li></ul>"
 "<h3>Good to know</h3><ul><li>Cut the tip to suit the joint width before starting</li><li>Clear a hardened nozzle with the Maxisil Silicone Nozzle Unblocker and reuse it</li></ul>",
 [MX+"maxisil-extension-nozzles/", RD+"maxisil-extension-nozzles/"])

add("maxisil-silicone-nozzle-unblocker",
 '<p>The Maxisil silicone nozzle unblocker clears blocked silicone cartridge nozzles so you can reuse partly used tubes instead of throwing them away.</p><ul>\n<li>\n<strong>Brand:</strong> Maxisil</li>\n<li>\n<strong>Use:</strong> Clearing blocked silicone cartridge nozzles</li>\n<li>\n<strong>Box qty:</strong> 25 each</li>\n<li>\n<strong>Code:</strong> RDXA3010</li>\n</ul>',
 "<p>The Maxisil Silicone Nozzle Unblocker rescues part used cartridges. Drive its screw into the plug of cured silicone in the nozzle, twist, and pull the plug out in one piece, so the tube you opened last week is good to go again.</p>"
 "<h3>Use it for</h3><ul><li>Clearing blocked silicone and sealant cartridge nozzles</li><li>Saving part used tubes between jobs</li></ul>"
 "<h3>Features</h3><ul><li>Screw action grips the hardened silicone and pulls it clear</li><li>Reusable, nothing to wear out</li><li>Small enough to live in the gun case</li></ul>"
 "<h3>Specifications</h3><ul><li>Model: RDXA3010</li></ul>"
 "<h3>Good to know</h3><ul><li>Works on the Maxisil Corner and Extension Nozzles too</li><li>If the silicone has cured deep into the cartridge, fit a fresh nozzle after unblocking</li></ul>",
 [MX+"maxisil-silicone-nozzle-unblocker/", RD+"maxisil-silicone-nozzle-unblocker/"])

add("maxisil-applicator",
 '<p>Maxisil applicator for tooling and shaping silicone beads in corners and around fixtures after the sealant is applied.</p><ul>\n<li>\n<strong>Material:</strong> High-quality silicone rubber</li>\n<li>\n<strong>Shape:</strong> Multi-shaped, for different bead profiles</li>\n<li>\n<strong>Features:</strong> Easy clean</li>\n<li>\n<strong>Box Qty:</strong> 10</li>\n<li>\n<strong>Code:</strong> RDXA3000</li>\n</ul>',
 "<p>The Maxisil Applicator is the rubber finishing tool Maxisil recommends for tooling its silicone. Dip it in Smoothtex, draw it along the bead and it strips the excess while leaving a smooth, even fillet in one pass.</p>"
 "<h3>Use it for</h3><ul><li>Shaping silicone beads in corners, around baths, basins and fixtures</li><li>Removing excess sealant before it skins</li></ul>"
 "<h3>Features</h3><ul><li>Flexible silicone rubber with a smooth edge</li><li>Multi-shaped: different edges give different bead profiles</li><li>Easy to grip, easy to clean</li></ul>"
 "<h3>Specifications</h3><ul><li>Material: silicone rubber</li><li>Model: RDXA3000</li></ul>"
 "<h3>Good to know</h3><ul><li>Dip the applicator in Smoothtex A (wet areas, pools) or Smoothtex N (natural stone) rather than wetting the joint</li>"
 "<li>Tool matt colours in a single pass, as repeated passes bring up a gloss</li><li>Wipe it clean straight after use so cured silicone does not build up on the edge</li></ul>",
 [MX+"maxisil-applicator/", RD+"maxisil-applicator/", "https://maxisil.com.au/wp-content/uploads/2024/02/Maxisil-Smoothtex-N-Technical-Data-Sheet.pdf"])

add("maxisil-cleaner-250ml",
 '<p>Set your job up for success with a clean foundation. The Maxisil cleaner is the first step, removing residues and dirt from the surface before primer and sealant are applied.</p>\n<p>The Maxisil Cleaner is compatible with the entire Maxisil sealant range.</p>\n<ul>\n<li>Size: 250ml</li>\n<li>Features: Acetone-based cleaner that removes contaminants and oils</li>\n<li>Suitable for: All Maxisil Products</li>\n</ul>',
 "<p>Maxisil Cleaner is the first step of a silicone job: an acetone based cleaner that lifts oils, soap residue and dust off tiles, glass and stainless steel so the primer and sealant bond to the surface rather than the grime on it. It suits the whole Maxisil sealant range.</p>"
 "<h3>Use it for</h3><ul><li>Cleaning non-porous surfaces before Maxisil primer and silicone</li><li>Tile and stainless steel cleaning around joints</li><li>Wiping fresh, uncured silicone smears off tiles</li></ul>"
 "<h3>Features</h3><ul><li>Acetone based, removes contaminants and oils</li><li>Flashes off in about a minute</li><li>Compatible with all Maxisil products</li></ul>"
 "<h3>Specifications</h3><ul><li>Size: 250 ml</li><li>Model: RDX2004</li></ul>"
 "<h3>Good to know</h3><ul><li>Apply with a clean, lint free cotton cloth and allow about 1 minute airing time before priming or sealing</li>"
 "<li>Highly flammable: keep away from flames and sparks, ventilate the room and wear gloves and eye protection</li><li>Porous surfaces such as mortar are cleaned with a wire brush instead</li></ul>",
 [MX+"maxisil-cleaner/", "https://maxisil.com.au/wp-content/uploads/2023/08/MAXISIL-CLEANER.pdf", "https://maxisil.com.au/wp-content/uploads/2017/07/Maxisil-Membrane-Technical-Data-Sheet.pdf", RD+"maxisil-cleaner/"])

add("maxisil-membrane-silicone",
 '<ul>\n<li>Neutral cure, Highly flexible</li>\n<li>Size: 310ml</li>\n<li>Temperature resistance: -40ºC to +180ºC</li>\n<li>Wait time: No waiting required. Membrane material can be immediately applied over Maxisil Membrane</li>\n<li>Suitable for: Bond breaker/fillet applications, and Joint sealer prior to waterproofing</li>\n<li>Low modulus, 50% joint movement capability</li>\n<li>Can be used for interior and exterior areas</li>\n<li>Easy to apply with good tooling properties</li>\n</ul>',
 "<p>Maxisil Membrane is a neutral cure silicone made for the bond breaker and fillet work that goes under a liquid waterproofing membrane. There is no waiting: you can roll the membrane straight over the fresh bead, which takes a day out of a bathroom program.</p>"
 "<h3>Use it for</h3><ul><li>Bond breaker and fillet joints at wall to floor and hob junctions before waterproofing</li><li>Sealing joints prior to membrane in showers, niches and wet areas</li><li>Movement joints in bathrooms, interior and exterior</li></ul>"
 "<h3>Features</h3><ul><li>Neutral cure, non-corrosive, highly flexible, low modulus</li><li>50% joint movement capability</li><li>Contains fungicides for mould resistance</li>"
 "<li>Easy to apply with good tooling properties</li><li>Tested to EN 15651 Part 1 (F EXT-INT CC 25 LM) and conforms to AS 3740</li></ul>"
 "<h3>Specifications</h3><ul><li>Size: 310 ml cartridge</li><li>Temperature resistance: -40°C to +180°C</li><li>Skin time about 5 to 15 minutes, cures about 2 mm in 24 hours</li>"
 "<li>Apply between +5°C and +35°C</li><li>Wait time: none, membrane can go on immediately</li><li>Model: RDX1007</li></ul>"
 "<h3>Good to know</h3><ul><li>Clean non-porous surfaces with Maxisil Cleaner first; porous ones with a wire brush</li><li>Not paintable. Keep it away from bitumen, butyl, EPDM and neoprene</li><li>Check the fillet size your membrane maker specifies</li></ul>",
 [MX+"maxisil-membrane/", "https://maxisil.com.au/wp-content/uploads/2017/07/Maxisil-Membrane-Technical-Data-Sheet.pdf", RD+"maxisil-membrane/"])

# ---------------- BAT trowels, floats, scrapers ----------------
add("bat-pro-12-mm-square-notch-trowel",
 '<p>BAT Pro square notch trowel with a 12 mm notch and a comfortable soft-grip handle. Spreads an even adhesive bed for large-format floor and wall tiles.</p>',
 "<p>The BAT Pro 12 mm Square Notch Trowel lays the thick, even adhesive bed that large format floor and wall tiles need. Square notches comb full ribs that collapse evenly under the tile, pushing air out and lifting adhesive coverage, which is where most bond failures start.</p>"
 "<h3>Use it for</h3><ul><li>Large format porcelain and stone on floors and walls</li><li>Uneven substrates that need more adhesive depth</li><li>Back buttering heavy tiles</li></ul>"
 "<h3>Features</h3><ul><li>12 mm square notch</li><li>Soft grip handle for long stretches of combing</li><li>Part of the BAT Pro trowel range, which runs from 4 mm to 15 mm notches</li></ul>"
 "<h3>Specifications</h3><ul><li>Notch: 12 mm square</li><li>Handle: soft grip</li></ul>"
 "<h3>Good to know</h3><ul><li>Match the notch to the adhesive data sheet and tile size; 12 mm is a common call for tiles 600 mm and larger</li>"
 "<li>Comb in one direction and lay the tile across the ribs so air can escape</li><li>Wash the blade before adhesive sets so the notches stay true</li></ul>",
 ["https://battrims.com/product/bat-professional-stainless-steel-trowel-12mm-s-grip/", "https://adheseal.com.au/products/bat-professional-stainless-steel-trowel"],
 True, "Range-level verification: BAT Pro soft grip square notch trowels come in 4 to 15 mm. Blade material not stated on our listing so not claimed.")

add("panther-stainless-steel-square-notch-trowel-280-x-120-mm",
 '<p>Panther stainless steel square notch trowel, 280 x 120 mm blade with an ergonomic two-tone grip. Rust-resistant blade for spreading tile adhesive evenly on floors and walls.</p>',
 "<p>The Panther Stainless Steel Square Notch Trowel has a 280 x 120 mm blade, wider than a standard notch trowel, so each pass covers more floor. Stainless steel will not rust or pit against cement adhesives, which keeps the notch profile true for the life of the tool.</p>"
 "<h3>Use it for</h3><ul><li>Spreading tile adhesive evenly on floors and walls</li><li>Tiling and plastering work</li></ul>"
 "<h3>Features</h3><ul><li>Stainless steel blade with spot rivet weld construction</li><li>Ergonomic two-tone soft grip handle</li><li>Rust resistant, easy to wash clean</li></ul>"
 "<h3>Specifications</h3><ul><li>Blade: 280 x 120 mm</li><li>Material: stainless steel</li><li>Notch: square</li></ul>"
 "<h3>Good to know</h3><ul><li>Panther makes this trowel in 4, 6, 8, 10, 12 and 15 mm square notches; pick the size your adhesive data sheet calls for the tile</li>"
 "<li>Comb the ribs in one direction and bed the tile across them so air can escape</li><li>Rinse before adhesive hardens on the blade</li></ul>",
 ["https://battrims.com/product/panther-stainless-steel-trowel-12mm-s-grip/", "https://adheseal.com.au/products/panther-stainless-steel-trowel"])

add("panther-diamond-blade",
 '<p><strong>Fits:</strong> 100 to 105 mm angle grinders</p><p>Panther thin turbo diamond blade, 105 mm (4"), for angle grinders. Cuts porcelain, ceramic and stone tiles cleanly with minimal chipping.</p>',
 "<p>The Panther Thin Turbo Diamond Blade is a 105 mm (4 inch) grinder blade for cutting porcelain, ceramic and stone with minimal chipping. The thin turbo rim takes a smaller bite per pass, which is what keeps the edge of an expensive tile clean, and the reinforced core keeps the blade running true.</p>"
 "<h3>Use it for</h3><ul><li>Ceramic, porcelain, slate, marble and granite</li><li>Notches, L cuts and trimming on site where the bench saw cannot go</li></ul>"
 "<h3>Features</h3><ul><li>Thin turbo rim for fast, clean cuts</li><li>Reinforced core</li><li>Wet or dry cutting</li></ul>"
 "<h3>Specifications</h3><ul><li>Diameter: 105 mm (4 inch)</li><li>Also made in 125 mm</li></ul>"
 "<h3>Fits</h3><ul><li>100 to 105 mm angle grinders</li></ul>"
 "<h3>Good to know</h3><ul><li>Not designed for side grinding; incorrect use can delaminate the rim</li><li>Let the blade do the work and cool it between dry cuts</li><li>Wear eye, ear and dust protection</li></ul>",
 ["https://battrims.com/product/panther-thin-turbo-rim-diamond-blade-105mm/", "https://adheseal.com.au/products/panther-thin-turbo-diamond-blade"])

add("bat-paint-scraper-soft-grip",
 bat("BAT Paint Scraper - Soft Grip", "PS-50, PS-75, PS-100"),
 "<p>The BAT Paint Scraper is a stiff steel blade on a soft grip handle for stripping paint, adhesive and dried grout off walls and floors before tiling. Pick the width to suit the job: 50 mm for corners and tight spots, 75 mm for general work, 100 mm for wide flat areas.</p>"
 "<h3>Use it for</h3><ul><li>Scraping old paint, flaking render and adhesive ridges before tiling</li><li>Lifting dried grout, silicone and membrane drips</li><li>Cleaning down trowels, floats and buckets</li></ul>"
 "<h3>Features</h3><ul><li>Steel blade</li><li>Soft grip handle</li><li>Three widths</li></ul>"
 "<h3>Specifications</h3><ul><li>Widths: 50 mm (PS-50), 75 mm (PS-75), 100 mm (PS-100)</li></ul>"
 "<h3>Good to know</h3><ul><li>Keep the edge square with a file so it lifts rather than gouges</li><li>Use a floor scraper with a long handle for whole floors</li></ul>",
 ["https://stonex.com.au/collections/bat-trims", BT], True, "BAT paint scraper sets on stonex.com.au confirm steel blade and soft grip handle in this range; singles PS-50/75/100 not listed on battrims.com.")

add("bat-pro-square-trowel-with-swan-neck",
 bat("BAT Pro Square Trowel with Swan Neck", "BP-TTSQ160, BP-TTSQ200"),
 "<p>The BAT Pro Square Trowel with Swan Neck is a flat square trowel for scooping adhesive and grout out of the bucket and laying it onto the wall or hawk. The swan neck in the handle hooks over the bucket rim between loads, so the blade never sinks into the mix and the handle stays clean.</p>"
 "<h3>Use it for</h3><ul><li>Loading adhesive from bucket to trowel or wall</li><li>Spreading a flat bed before combing with a notch trowel</li><li>Buttering the back of tiles and filling low spots</li></ul>"
 "<h3>Features</h3><ul><li>Steel blade that holds its edge against abrasive mortar</li><li>Swan neck handle rests on the bucket rim</li><li>Two blade sizes</li></ul>"
 "<h3>Specifications</h3><ul><li>160 x 110 mm (BP-TTSQ160)</li><li>200 x 125 mm (BP-TTSQ200)</li></ul>"
 "<h3>Good to know</h3><ul><li>Pairs with the BAT Pro gauging trowel from the same range for mixing small batches</li><li>Rinse before the adhesive sets</li></ul>",
 ["https://adheseal.com.au/products/bat-pro-square-trowel-with-swan-neck", "https://battrims.com/product/bat-pro-gauging-trowel-with-swan-neck-200mm/"])

add("bat-bright-steel-trowel-plaster-soft-grip",
 bat("BAT Bright Steel Trowel - Plaster - Soft Grip", "BAT-BSPL-SG"),
 "<p>The BAT Bright Steel Plaster Trowel is a flat finishing trowel for rendering, patching and skimming the walls you are about to tile. The bright carbon steel blade is stiff enough to pull render flat, and the soft grip handle takes the sting out of a long day of floating.</p>"
 "<h3>Use it for</h3><ul><li>Rendering and skimming walls before tiling</li><li>Patching and flattening screed and render</li><li>Pressing bedding compound flat on hobs and niches</li></ul>"
 "<h3>Features</h3><ul><li>Flat bright steel blade</li><li>Soft grip handle</li><li>From the BAT bright steel soft grip trowel range</li></ul>"
 "<h3>Specifications</h3><ul><li>Blade: bright (carbon) steel</li><li>Handle: soft grip</li><li>Model: BAT-BSPL-SG</li></ul>"
 "<h3>Good to know</h3><ul><li>Carbon steel will rust if put away wet: wipe it dry and give it a light oil</li><li>For combing adhesive, use a notched BAT trowel instead</li></ul>",
 ["https://battrims.com/product/bat-bright-steel-trowel-12mm-s-grip/"], False, "Plaster trowel BAT-BSPL-SG not found online; written from title, BAT bright steel soft grip range and general plastering trowel use.")

add("bat-plastic-float-280-x-140-x-3mm",
 bat("BAT Plastic Float - 280 x 140 x 3mm", "PRF-28143", "<p>Plastic Coarse Float</p><p>280 x 140 x 3mm thick</p><p>ABS Plastic Construction</p>"),
 "<p>The BAT Plastic Float is a 280 x 140 mm coarse float in ABS plastic for rubbing up render and screed before tiling. Plastic does not drag fines to the surface the way steel does, so it leaves an open, even texture that adhesive keys into.</p>"
 "<h3>Use it for</h3><ul><li>Floating freshly laid screed and render flat</li><li>Opening up the surface of a screed so adhesive bonds</li><li>Working bedding into hobs and shower bases</li></ul>"
 "<h3>Features</h3><ul><li>Coarse face</li><li>ABS plastic construction, light and rust free</li><li>Easy to hose clean</li></ul>"
 "<h3>Specifications</h3><ul><li>Size: 280 x 140 mm</li><li>Thickness: 3 mm</li><li>Material: ABS plastic</li><li>Model: PRF-28143</li></ul>"
 "<h3>Good to know</h3><ul><li>Float in overlapping circles once the screed has stiffened enough to take weight</li><li>For a finer finish, follow with a steel trowel</li></ul>",
 [BT+"plastic-float-280-x-140-x-3mm/"])

add("bat-plaster-float-coarse-195-x-125mm",
 bat("BAT Plaster Float - Coarse - 195 x 125mm", "PFC-1219", "<p>Plaster Float – Plastic</p><p>Diamond Pattern Underside</p><p>195 x 125mm</p><p>For the smoothing off of freshly screeded surfaces</p>"),
 "<p>The BAT Plaster Float is a compact 195 x 125 mm plastic float with a diamond pattern underside for smoothing off freshly screeded surfaces. The small face gets into shower bases, hobs and niches where a full size float will not fit.</p>"
 "<h3>Use it for</h3><ul><li>Smoothing fresh screed and render</li><li>Shower bases, hobs, steps and niches</li><li>Patching and small repairs</li></ul>"
 "<h3>Features</h3><ul><li>Diamond pattern underside</li><li>Coarse plastic face</li><li>Light, rust free and easy to clean</li></ul>"
 "<h3>Specifications</h3><ul><li>Size: 195 x 125 mm</li><li>Material: plastic</li><li>Model: PFC-1219</li></ul>"
 "<h3>Good to know</h3><ul><li>Work in overlapping circles once the screed has firmed enough to take weight</li><li>The larger BAT 280 x 140 mm plastic float suits open floors</li></ul>",
 [BT+"plaster-float-coarse-195-x-125mm/"])

add("bat-pointed-rubber-grouter",
 bat("Pointed Rubber Grouter", "PRGB, PRGJ, PRGP", "<p>BAT Pointed Rubber Grouter with 240mm long base.</p><p>For the easy spread and application of Grout.</p><p>A high quality trade based product.</p>"),
 "<p>The BAT Pointed Rubber Grouter pushes grout into corners and narrow joints a flat float cannot reach. The 240 mm pointed base compacts the grout along the joint, then strikes off the excess in the same pass.</p>"
 "<h3>Use it for</h3><ul><li>Grouting ceramic, porcelain, stone and mosaic tiles on walls and floors</li><li>Corners, edges and narrow joints</li><li>Spreading and applying grout</li></ul>"
 "<h3>Features</h3><ul><li>Pointed rubber blade on a 240 mm base</li><li>Rubber blade on a timber handle</li><li>Three blade options</li></ul>"
 "<h3>Specifications</h3><ul><li>BAT (PRGB): standard BAT rubber blade with a timber handle</li>"
 "<li>Japanese (PRGJ): softer, more flexible Japanese rubber for a smoother finish on soft or polished tiles</li><li>Plastic (PRGP): plastic bladed version</li><li>Base length: 240 mm</li></ul>"
 "<h3>Good to know</h3><ul><li>Light pressure on the final pass shapes the joint</li><li>Rinse the blade often so dried grout does not scratch the tile</li><li>Keep one for dark grout and one for light, as rubber holds pigment</li></ul>",
 [BT+"pointed-rubber-grouter-bat-trade/", "https://adheseal.com.au/products/pointed-rubber-grouter", "https://adheseal.com.au/products/premium-pointed-rubber-grouter-japanese-rubber"])

add("bat-floor-scraper-300mm-replacement-blade",
 bat("BAT Floor Scraper 300mm Replacement Blade", "FS-300-SB", "<p>Replacement 300mm steel blade for the BAT FS-300 long handled floor scraper.</p>"),
 "<p>This is the replacement 300 mm steel blade for the BAT FS-300 long handled floor scraper. A fresh edge is what makes the scraper lift adhesive and old floor coverings in one pass instead of skating over them.</p>"
 "<h3>Fits</h3><ul><li>BAT FS-300 floor scraper: 300 mm blade width on a 1300 mm wooden handle</li></ul>"
 "<h3>Use it for</h3><ul><li>Stripping old tile adhesive, vinyl and carpet residue from floors</li><li>Removing floor coverings from a stand up position</li></ul>"
 "<h3>Features</h3><ul><li>Steel blade</li><li>Full 300 mm width</li></ul>"
 "<h3>Specifications</h3><ul><li>Blade width: 300 mm</li><li>Model: FS-300-SB</li></ul>"
 "<h3>Good to know</h3><ul><li>Swap the blade when the edge rounds over; a dull blade needs twice the effort</li><li>Keep the blade flat to the floor so it slides under residue rather than digging in</li></ul>",
 [BT+"floor-scraper-300mm-x-1300mm/"])

add("bat-floor-scraper-replacement-blades-to-suit-fs-125-5-pk",
 bat("BAT Floor Scraper Replacement Blades to suit FS-125 (5 pk)", "FS-125-RB", "<p>Replacement Blade set to suit FS-125 ( 5 pcs )</p>"),
 "<p>A 5 pack of replacement blades for the BAT FS-125 floor scraper. Keep a pack in the van and a dull edge costs you a minute, not an afternoon of chipping at adhesive.</p>"
 "<h3>Fits</h3><ul><li>BAT FS-125 floor scraper: 125 mm blade width on a 500 mm handle, with a butt head that can be struck with a hammer for forced tile removal</li></ul>"
 "<h3>Use it for</h3><ul><li>Lifting tiles, adhesive and floor coverings in tight spaces: behind toilets, in cupboards, along skirtings</li><li>Cleaning up ridges of set adhesive</li></ul>"
 "<h3>Specifications</h3><ul><li>Blade width: 125 mm</li><li>Pack: 5 blades</li><li>Model: FS-125-RB</li></ul>"
 "<h3>Good to know</h3><ul><li>Change the blade as soon as the edge rounds over</li><li>Wear gloves and eye protection when chipping tiles</li></ul>",
 [BT+"replacement-blade-to-suit-fs-125-5-pk/", BT+"floor-scraper-125-x-500mm/"])

add("bat-replacement-blade-to-suit-fs-412-10-pk",
 bat("BAT Replacement Blade to suit FS-412 (10 pk)", "FS-412-RB", "<p>Replacement blade pack to suit the FS-412 short handled floor scraper (10 pcs).</p>"),
 "<p>A 10 pack of replacement blades for the BAT FS-412 short handled scraper, the one handed tool for small adhesive and grout clean up jobs. Fresh blades keep it lifting cleanly instead of smearing.</p>"
 "<h3>Fits</h3><ul><li>BAT FS-412 short handled scraper: 100 mm blade width on a 300 mm handle</li></ul>"
 "<h3>Use it for</h3><ul><li>Scraping adhesive ridges and grout haze off small areas</li><li>Cleaning up around fixtures and in corners</li></ul>"
 "<h3>Specifications</h3><ul><li>Blade width: 100 mm</li><li>Pack: 10 blades</li><li>Model: FS-412-RB</li></ul>"
 "<h3>Good to know</h3><ul><li>Swap the blade when it rounds over or chips</li><li>For whole floors, step up to the BAT FS-125 or FS-300 scrapers</li></ul>",
 [BT+"replacement-blade-to-suit-fs-412-10-pk/", BT+"short-handled-scraper-100mm-x-300mm/"])

# ---------------- Spacers ----------------
def spacer_tail(code_list):
    return f"<li>Codes: {code_list}</li></ul>"

add("bat-t-shapes-10mm",
 bat("BAT T Shapes 10mm", "TS10-250, TS10-500, TS10-1000", "<p>T-Shapes 10mm x 250 pce Bag</p>"),
 "<p>BAT T Shape spacers hold a 10 mm joint where tiles meet in a T, which is every joint on a brick bond, offset or staggered layout. A 10 mm joint suits outdoor pavers, rustic stone and any job where a wide grout line is part of the look.</p>"
 "<h3>Use it for</h3><ul><li>Brick bond and offset layouts on floors and walls</li><li>Wide grout joints on pavers, quarry tiles and natural stone</li><li>Lining up the first course against a wall</li></ul>"
 "<h3>Features</h3><ul><li>T shape sits in three way joints without fouling the fourth tile</li><li>Plastic, reusable if pulled before the adhesive sets</li></ul>"
 "<h3>Specifications</h3><ul><li>Joint width: 10 mm</li><li>Packs: 250 bag (TS10-250), 500 bag (TS10-500), 1000 bag (TS10-1000)</li></ul>"
 "<h3>Good to know</h3><ul><li>Pull spacers before grouting; left in, they leave a hollow in the joint</li><li>BAT also makes T shapes in 1.5, 2, 3 and 5 mm</li></ul>",
 [BT+"t-shapes-10mm-x-250-bag/", "https://stonex.com.au/collections/bat-trims"])

add("bat-t-shapes-5mm",
 bat("BAT T Shapes 5mm", "TS5-250, TS5-500, TS5-2000, TS5-5000, TS5B-2000, TS5B-5000", "<p>T-Shapes 5mm x 250 pce Bag</p>"),
 "<p>BAT T Shape spacers hold a 5 mm joint at the three way junctions of a brick bond, offset or staggered layout. 5 mm is a common floor joint for handmade look tiles, pavers and any tile with a rustic edge that needs room.</p>"
 "<h3>Use it for</h3><ul><li>Brick bond and offset layouts on floors and walls</li><li>Pavers, quarry tiles and uneven edged stone</li><li>Setting out the first course</li></ul>"
 "<h3>Features</h3><ul><li>T shape sits in three way joints without fouling the fourth tile</li><li>Plastic, reusable if pulled before the adhesive sets</li><li>Bags for small jobs, buckets for whole floors</li></ul>"
 "<h3>Specifications</h3><ul><li>Joint width: 5 mm</li><li>Bags: 250 (TS5-250), 500 (TS5-500), 2000 (TS5-2000), 5000 (TS5-5000)</li><li>Buckets: 2000 (TS5B-2000), 5000 (TS5B-5000)</li></ul>"
 "<h3>Good to know</h3><ul><li>Pull spacers before grouting</li><li>BAT also makes T shapes in 1.5, 2, 3 and 10 mm, and deep versions for thick adhesive beds</li></ul>",
 [BT+"t-shapes-5mm-x-250-bag/", "https://stonex.com.au/collections/bat-trims"])

add("bat-deep-t-shapes-1-5mm",
 bat("BAT Deep T Shapes 1.5mm", "TSD-500, TSD-2000, TSDB-2000", "<p>BAT deep 1.5mm T-shape spacers with taller legs for thicker adhesive beds on offset and brick-bond layouts.</p>"),
 "<p>BAT Deep T Shapes hold a tight 1.5 mm joint on brick bond and offset layouts. The deep version has taller legs than a standard T, so it stays put in a thick adhesive bed under large format and heavy tiles instead of sinking and disappearing.</p>"
 "<h3>Use it for</h3><ul><li>Rectified porcelain and large format tiles laid in offset or brick bond</li><li>Thick adhesive beds on floors and walls</li><li>Minimal joints on polished and rectified edges</li></ul>"
 "<h3>Features</h3><ul><li>1.5 mm joint</li><li>Taller legs for deep adhesive beds</li><li>Plastic, reusable if pulled before the adhesive sets</li></ul>"
 "<h3>Specifications</h3><ul><li>Joint width: 1.5 mm</li><li>Bags: 500 (TSD-500), 2000 (TSD-2000)</li><li>Bucket: 2000 (TSDB-2000)</li></ul>"
 "<h3>Good to know</h3><ul><li>Pull spacers before grouting</li><li>A 1.5 mm joint needs flat tiles and a flat substrate; add a levelling system on big tiles</li><li>Also made in 2 mm</li></ul>",
 [BT+"deep-t-shapes-1-5mm-x-500-bag/"])

add("bat-deep-t-shapes-2mm",
 bat("BAT Deep T Shapes 2mm", "TS2D-500, TS2D-2000, TS2D-5000, TS2DB-2000, TS2DB-5000", "<p>BAT deep 2mm T-shape spacers with taller legs for thicker adhesive beds on offset and brick-bond layouts.</p>"),
 "<p>BAT Deep T Shapes hold a 2 mm joint on brick bond and offset layouts. Taller legs than a standard T keep them upright in the thick adhesive bed under large format tiles, so the joint stays even from the first tile to the last.</p>"
 "<h3>Use it for</h3><ul><li>Rectified porcelain and large format tiles laid offset or brick bond</li><li>Thick adhesive beds on floors and walls</li><li>Subway and plank tiles with a fine joint</li></ul>"
 "<h3>Features</h3><ul><li>2 mm joint</li><li>Taller legs for deep adhesive beds</li><li>Plastic, reusable if pulled before the adhesive sets</li><li>Bags for small jobs, buckets for whole floors</li></ul>"
 "<h3>Specifications</h3><ul><li>Joint width: 2 mm</li><li>Bags: 500 (TS2D-500), 2000 (TS2D-2000), 5000 (TS2D-5000)</li><li>Buckets: 2000 (TS2DB-2000), 5000 (TS2DB-5000)</li></ul>"
 "<h3>Good to know</h3><ul><li>Pull spacers before grouting</li><li>Also made in 1.5 mm</li></ul>",
 [BT+"deep-t-shapes-2mm-x-500-bag/"])

add("bat-tile-crosses-4mm",
 bat("BAT Tile Crosses 4mm", "TC4-500", "<p>BAT 4mm tile cross spacers in a 500 piece bag, for wider grout joints on floor and feature tiles.</p>"),
 "<p>BAT Tile Crosses hold a 4 mm joint at every four way corner of a straight stacked or grid layout. 4 mm is a common floor joint for outdoor tiles, quarry tiles and anything with a slightly irregular edge.</p>"
 "<h3>Use it for</h3><ul><li>Grid and stack bond layouts on floors and walls</li><li>Wider grout joints on floor and feature tiles</li><li>Outdoor and rustic tiles that need room for size variation</li></ul>"
 "<h3>Features</h3><ul><li>Cross shape sits at the corner of four tiles</li><li>Plastic, reusable if pulled before the adhesive sets</li></ul>"
 "<h3>Specifications</h3><ul><li>Joint width: 4 mm</li><li>Pack: 500 piece bag</li><li>Model: TC4-500</li></ul>"
 "<h3>Good to know</h3><ul><li>Stand a cross on its edge in a joint and you can pull it out before grouting without leaving a hollow</li><li>BAT also makes tile crosses in 1.5, 2 and 3 mm, plus deep versions</li></ul>",
 [BT+"tile-crosses-4mm-x-500-bag/", "https://adheseal.com.au/products/bat-trims-tile-crosses"])

add("bat-wedges",
 bat("BAT Wedges", "W-100, W-1000, W-2000, W-5000, WB-1000, WB-2000, WB-5000, WB-10000", "<p>Wedges x 100 pce Bag</p>"),
 "<p>BAT Wedges adjust spacing where a cross or T will not fit. The taper runs from 5 mm down to a fine point, so you slide one under a tile edge to lift it level or push one into a joint to nudge two tiles apart. They are the go to for wall tiling off a batten and for the first course over a bath or floor.</p>"
 "<h3>Use it for</h3><ul><li>Levelling and spacing wall tiles</li><li>Holding the first course off a floor, bath or hob</li><li>Fine tuning joints on floors with ceramic, porcelain or natural stone</li></ul>"
 "<h3>Features</h3><ul><li>Tapered plastic wedge, 5 mm to a fine point</li><li>Reusable: wash the adhesive off before it hardens</li><li>Bags for small jobs, buckets for big jobs</li></ul>"
 "<h3>Specifications</h3><ul><li>Bags: 100 (W-100), 1000 (W-1000), 2000 (W-2000), 5000 (W-5000)</li><li>Buckets: 1000 (WB-1000), 2000 (WB-2000), 5000 (WB-5000), 10000 (WB-10000)</li></ul>"
 "<h3>Good to know</h3><ul><li>As a rough guide, allow about 100 wedges per 2 m² depending on tile size and how much levelling is needed</li><li>Pull them out once the adhesive has taken, before grouting</li></ul>",
 [BT+"wedges-x-100-bag/", "https://adheseal.com.au/products/bat-trims-tile-wedges"])

add("bat-jumbo-wedges",
 bat("BAT Jumbo Wedges x 100 Bag", "JW-100", "<p>Jumbo Wedges x 100 pce Bag</p>"),
 "<p>BAT Jumbo Wedges are the bigger brother of the standard tile wedge, made for adjusting thick tiles and stone where a small wedge bottoms out. Slide one under a paver or 20 mm porcelain to lift the edge level, or push one into a joint to spread two slabs apart.</p>"
 "<h3>Use it for</h3><ul><li>Levelling thick pavers, stone and 20 mm outdoor porcelain</li><li>Holding heavy wall tiles and slabs off a floor or hob while the adhesive takes</li><li>Wide joints where a standard wedge is too small</li></ul>"
 "<h3>Features</h3><ul><li>Larger taper than the standard BAT wedge</li><li>Reusable plastic: wash the adhesive off before it sets</li><li>Bags for small jobs, a bucket for big jobs</li></ul>"
 "<h3>Specifications</h3><ul><li>Bags: 100 (JW-100), 250 (JW-250), 500 (JW-500), 1000 (JW-1000)</li><li>Bucket: 1000 (JWB-1000)</li></ul>"
 "<h3>Good to know</h3><ul><li>Pull wedges out once the adhesive has taken, before grouting</li><li>For standard thickness tiles, the regular BAT Wedges taper from 5 mm to a point</li></ul>",
 [BT+"jumbo-wedges-x-100-bag/", "https://tsptrims.com.au/shop/jumbo-tile-wedges-500-pack/"])

# ---------------- Nippers ----------------
NIP_GOOD = "<h3>Good to know</h3><ul><li>Nibble small bites from the edge of the cut line; big bites crack the tile</li><li>Smooth the nibbled edge with a rubbing stone or diamond pad</li><li>Wear eye protection, as chips fly</li></ul>"
add("bat-heavy-duty-tile-nipper",
 bat("BAT Heavy Duty Tile Nipper", "HDTN", "<p>Heavy Duty Tile Nipper</p><p>Straight Jaw design</p><p>Ergonomic Handle</p>"),
 "<p>The BAT Heavy Duty Tile Nipper is the big nipper for thick, hard tile. Straight jaws take a square bite out of porcelain, quarry tile and stone, and the ergonomic handles give the leverage to do it without jarring your hands.</p>"
 "<h3>Use it for</h3><ul><li>Nibbling curves, notches and irregular shapes in thick tile</li><li>Trimming around pipes, taps and floor wastes</li><li>Shaping offcuts too small or awkward for the cutter</li></ul>"
 "<h3>Features</h3><ul><li>Heavy duty build</li><li>Straight jaw design</li><li>Ergonomic handle</li></ul>"
 "<h3>Specifications</h3><ul><li>Jaw: straight</li><li>Model: HDTN</li></ul>" + NIP_GOOD,
 [BT+"heavy-duty-tile-nipper/"])

add("bat-straight-nipper",
 bat("BAT Straight Nipper", "STN", "<p>Straight Nipper</p><p>Straight cutting Tungsten Carbide Tipped Jaws</p><p>Spring Loaded Handle with comfort Soft Grip</p>"),
 "<p>The BAT Straight Nipper has tungsten carbide tipped jaws that stay sharp through porcelain and glazed tile long after plain steel jaws would have rounded off. The spring loaded handles open themselves between bites, so one hand does the work while the other holds the tile.</p>"
 "<h3>Use it for</h3><ul><li>Nibbling curves, notches and irregular shapes</li><li>Cutting around pipes, taps and fittings</li><li>Trimming mosaics and small offcuts</li></ul>"
 "<h3>Features</h3><ul><li>Straight cutting tungsten carbide tipped jaws</li><li>Spring loaded handles</li><li>Comfort soft grip</li></ul>"
 "<h3>Specifications</h3><ul><li>Jaw: straight, tungsten carbide tipped</li><li>Model: STN</li></ul>" + NIP_GOOD,
 [BT+"straight-nipper/"])

add("bat-side-nipper",
 bat("BAT Side Nipper", "SN", "<p>Side Nipper with Offset Jaw</p><p>Straight cutting Tungsten Carbide Tipped Jaws</p><p>Spring Loaded Handle with comfort Soft Grip</p>"),
 "<p>The BAT Side Nipper puts the jaws out to the side on an offset head, so you can nibble along a cut line while your hand and the tool stay clear of the tile face. Tungsten carbide tips keep the edge sharp through porcelain, and the spring opens the handles between bites.</p>"
 "<h3>Use it for</h3><ul><li>Small insets and notches in tiles</li><li>Trimming a scored line that did not snap clean</li><li>Nibbling around pipes and fittings</li></ul>"
 "<h3>Features</h3><ul><li>Offset jaw for a clear view of the cut</li><li>Straight cutting tungsten carbide tipped jaws</li><li>Spring loaded handles with comfort soft grip</li></ul>"
 "<h3>Specifications</h3><ul><li>Jaw: offset, straight cutting, tungsten carbide tipped</li><li>Model: SN</li></ul>" + NIP_GOOD,
 [BT+"side-nipper/", "https://www.tilestonepaver.com.au/BAT-Trims-Tile-Side-Nipper"])

add("bat-side-nipper-curved-jaw",
 bat("BAT Side Nipper - Curved Jaw", "SN-CJ", "<p>Side Nipper with Curved Jaws</p><p>Curved cutting Tungsten Carbide Tipped Jaws</p><p>Spring Loaded Handle with comfort Soft Grip</p>"),
 "<p>The BAT Side Nipper with Curved Jaw is made for round cuts: tap holes, waste outlets and the curved edge around a pipe. The curved tungsten carbide tips follow the arc instead of flattening it, and the offset head keeps your hand clear of the tile face.</p>"
 "<h3>Use it for</h3><ul><li>Enlarging and finishing round holes in tiles</li><li>Curved cuts around pipes, taps and wastes</li><li>Shaping mosaics and small pieces</li></ul>"
 "<h3>Features</h3><ul><li>Curved cutting tungsten carbide tipped jaws</li><li>Side (offset) jaw for a clear view</li><li>Spring loaded handles with comfort soft grip</li></ul>"
 "<h3>Specifications</h3><ul><li>Jaw: offset, curved, tungsten carbide tipped</li><li>Model: SN-CJ</li></ul>" + NIP_GOOD,
 [BT+"side-nipper-curved-jaw/"])

add("bat-parrot-nipper",
 bat("BAT Parrot Nipper", "PN", "<p>Parrot Beak Nipper</p><p>Used for enlarging holes in tiles from a pre-existing cut.</p><p>Unique Parrot Head design allows for easy reach into a cut hole.</p>"),
 "<p>The BAT Parrot Nipper has a hooked parrot beak head that reaches into a hole you have already drilled or cut and nibbles it bigger from the inside. It is the tool for opening up a core drilled hole to clear a tap body or waste without cracking the tile.</p>"
 "<h3>Use it for</h3><ul><li>Enlarging holes in tiles from an existing cut or drilled hole</li><li>Fitting tiles around tap bodies, mixers and floor wastes</li><li>Internal curves a straight nipper cannot reach</li></ul>"
 "<h3>Features</h3><ul><li>Parrot head design reaches into a cut hole</li><li>Compact jaws for controlled bites</li></ul>"
 "<h3>Specifications</h3><ul><li>Jaw: parrot beak</li><li>Model: PN</li></ul>"
 "<h3>Good to know</h3><ul><li>Drill or cut a starter hole first; the parrot nipper enlarges, it does not start a hole</li><li>Take small bites and smooth the edge with a diamond pad</li><li>Wear eye protection</li></ul>",
 [BT+"parrot-nipper/"])

# ---------------- Knee pads ----------------
KPA = "<h3>Fits</h3><ul><li>BAT KPA Professional Knee Pads: flexible concertina style, rubber faced, with a soft foam inlay and rubber straps</li></ul>"
add("bat-replacement-liners-pair-suit-kpa",
 bat("BAT Replacement Liners (Pair) - Suit KPA", "KP-RL", "<p>Replacement Foam Liners to suit KPA Kneepads ( 2 pce set )</p>"),
 "<p>A pair of replacement foam liners for the BAT KPA Professional Knee Pads. The foam inlay is the part that compresses after months of kneeling on tile; swap it and the pads feel new again without replacing the shell.</p>"
 + KPA +
 "<h3>What's in the box</h3><ul><li>2 foam liners (one pair)</li></ul>"
 "<h3>Specifications</h3><ul><li>Model: KP-RL</li></ul>"
 "<h3>Good to know</h3><ul><li>Replacement straps (KP-ST) and buttons (KP-SB) for the KPA are also available, so the whole pad can be kept in service</li>"
 "<li>Replace liners when they stay flat after you stand up</li></ul>",
 [BT+"replacement-liners-pair-suit-kpa/", BT+"professional-knee-pads/"])

add("bat-replacement-buttons-set-of-4-suit-kpa",
 bat("BAT Replacement Buttons (Set of 4) - Suit KPA", "KP-SB", "<p>Replacement Button Set to suit KPA Kneepads ( 8 pce set )</p>"),
 "<p>A set of 8 replacement buttons for the BAT KPA Professional Knee Pads. The buttons are the studs the rubber straps hook over; when one breaks the strap will not hold, and a new set costs far less than new pads.</p>"
 + KPA +
 "<h3>What's in the box</h3><ul><li>8 replacement buttons</li></ul>"
 "<h3>Specifications</h3><ul><li>Model: KP-SB</li></ul>"
 "<h3>Good to know</h3><ul><li>Replacement straps (KP-ST) and foam liners (KP-RL) for the KPA are also available</li><li>Check buttons when you change straps; a worn button wears the new strap</li></ul>",
 [BT+"replacement-buttons-set-suit-kpa/", BT+"professional-knee-pads/"])

add("bat-replacement-straps-set-of-4-suit-kpa",
 bat("BAT Replacement Straps (Set of 4) - Suit KPA", "KP-ST", "<p>Replacement Rubber Strap Set to suit KPA Kneepads ( 4 pce set )</p>"),
 "<p>A set of 4 replacement rubber straps for the BAT KPA Professional Knee Pads. Straps stretch and crack long before the shell wears out, so a fresh set keeps the pads sitting under your knee instead of sliding down your shin.</p>"
 + KPA +
 "<h3>What's in the box</h3><ul><li>4 rubber straps (two per pad)</li></ul>"
 "<h3>Specifications</h3><ul><li>Model: KP-ST</li></ul>"
 "<h3>Good to know</h3><ul><li>Replacement buttons (KP-SB) and foam liners (KP-RL) for the KPA are also available</li><li>Fit the strap snug over work pants, not tight behind the knee</li></ul>",
 [BT+"replacement-straps-set-of-4-suit-kpa/", BT+"professional-knee-pads/"])

# ---------------- Sponges, suction, misc ----------------
add("bat-tiling-sponge-200-x-150mm",
 bat("BAT Tiling Sponge 200 x 150mm", "S-50, S-100", "<p>A general-purpose sponge predominantly used in Grout Clean Up.</p><p>Dimensions are 200 x 150 x 50mm.</p>"),
 "<p>The BAT Tiling Sponge is a 200 x 150 mm general purpose sponge for washing grout off tiles. It holds enough water to clean the joint and tile face, and the big flat face covers ground quickly on floors and walls.</p>"
 "<h3>Use it for</h3><ul><li>Grout clean up on ceramic, porcelain and stone</li><li>Wiping adhesive smears off tile faces</li><li>General wash down</li></ul>"
 "<h3>Features</h3><ul><li>Large 200 x 150 mm face</li><li>Two thicknesses</li></ul>"
 "<h3>Specifications</h3><ul><li>50 mm thick: 200 x 150 x 50 mm (S-50)</li><li>100 mm thick: 200 x 150 x 100 mm (S-100)</li></ul>"
 "<h3>Good to know</h3><ul><li>Wring it well: too much water pulls pigment out of the grout and leaves a patchy colour</li><li>Rinse often and change the water when it clouds</li><li>For a denser sponge on fine finishes, see the BAT Deluxe Cellulose Sponge</li></ul>",
 [BT+"sponge-200-x-150-x-50mm/"])

add("bat-sponge-deluxe-cellulose",
 bat("BAT Sponge - Deluxe Cellulose", "SP-DLXCELL", "<p>A premium Cellulose based Sponge best suited for grouting Clean Up</p><p>Sponge dimensions are 190 x 135 x 55mm.</p>"),
 "<p>The BAT Deluxe Cellulose Sponge is the dense natural cellulose sponge for grout clean up. Cellulose holds water evenly and releases it slowly, so it lifts grout haze without flooding the joints or dragging pigment out.</p>"
 "<h3>Use it for</h3><ul><li>Grout clean up on walls and floors</li><li>Final wipe over before the haze clean</li><li>Polished and delicate tile faces where a coarse sponge scratches</li></ul>"
 "<h3>Features</h3><ul><li>Cellulose based</li><li>Dense, even texture</li><li>Hand sized block</li></ul>"
 "<h3>Specifications</h3><ul><li>Size: 190 x 135 x 55 mm</li><li>Material: cellulose</li><li>Model: SP-DLXCELL</li></ul>"
 "<h3>Good to know</h3><ul><li>Wet before first use; cellulose is stiff when dry</li><li>Wring well and rinse often so you are not spreading grout back over the tile</li><li>Let it dry fully between jobs</li></ul>",
 [BT+"sponge-deluxe-cellulose/"])

add("bat-suction-cup-4",
 bat("BAT Suction Cup - 4 inch Single Cup", "BATSC-4", "<p>Aluminium Bodied Suction Cup – 4 inch Single Cup</p><p>100mm diameter with Black Rubber base</p><p>40kg capacity.</p>"),
 "<p>The BAT Suction Cup is a single 100 mm (4 inch) lifter rated to 40 kg for moving and placing tiles, glass and stone slabs without touching the edges. One cup gives a tiler a handle on a large format tile so it can be set down flat instead of dropped on a corner.</p>"
 "<h3>Use it for</h3><ul><li>Lifting and placing large format tiles and glass splashbacks</li><li>Lifting a laid tile back up to add adhesive</li><li>Carrying polished stone without fingerprints on the face</li></ul>"
 "<h3>Features</h3><ul><li>Aluminium body</li><li>100 mm black rubber base</li><li>40 kg capacity</li></ul>"
 "<h3>Specifications</h3><ul><li>Cup: 100 mm (4 inch), single</li><li>Capacity: 40 kg</li><li>Model: BATSC-4</li></ul>"
 "<h3>Good to know</h3><ul><li>Suction cups need a smooth, clean, non-porous surface; they will not hold on textured or dusty tile</li><li>For heavier slabs, the BAT Dual Suction Cup is rated to 80 kg</li></ul>",
 [BT+"suction-cup-4/", "https://stonex.com.au/collections/bat-trims"])

add("bat-dual-suction-cup-4",
 bat("BAT Dual Suction Cup - 4 inch", "BATSC-D4", "<p>Aluminium Bodied Suction Cup – Dual 4 inch Cup</p><p>100mm diameter cups with Black Rubber base</p><p>80kg capacity.</p>"),
 "<p>The BAT Dual Suction Cup puts two 100 mm (4 inch) cups on one aluminium handle for an 80 kg rating, enough for big porcelain panels, stone slabs and glass. Two cups also stop the load swinging, so a long tile can be carried and set down level.</p>"
 "<h3>Use it for</h3><ul><li>Lifting and placing large format and 20 mm porcelain</li><li>Glass splashbacks, shower screens and stone benchtop offcuts</li><li>Lifting a laid tile back out to add adhesive</li></ul>"
 "<h3>Features</h3><ul><li>Aluminium body</li><li>Two 100 mm black rubber cups</li><li>80 kg capacity</li></ul>"
 "<h3>Specifications</h3><ul><li>Cups: 2 x 100 mm (4 inch)</li><li>Capacity: 80 kg</li><li>Model: BATSC-D4</li></ul>"
 "<h3>Good to know</h3><ul><li>Suction cups need a smooth, clean, non-porous surface; wipe dust off the tile first</li><li>Two people and two lifters make 20 mm pavers a lot safer</li><li>The single BAT Suction Cup is rated to 40 kg</li></ul>",
 [BT+"dual-suction-cup-4/", "https://stonex.com.au/collections/bat-trims"])

add("bat-paint-brush",
 bat("BAT Paint Brush", "BAT-PB50, BAT-PB75, BAT-PB100", "<p>Paint brush for applying liquid waterproofing membrane into corners, around penetrations and along wall-floor junctions. Available in 50mm, 75mm and 100mm widths.</p>"),
 "<p>The BAT Paint Brush is a waterproofing brush for working liquid membrane into the places a roller misses: internal corners, around pipe penetrations and along wall to floor junctions. Three widths cover tight niches through to full wall and floor junction runs.</p>"
 "<h3>Use it for</h3><ul><li>Applying liquid waterproofing membrane in corners and around penetrations</li><li>Bedding bond breaker tape and reinforcing fabric into membrane</li><li>Cutting in along wall-floor junctions before rolling</li></ul>"
 "<h3>Features</h3><ul><li>Sized for waterproofing work</li><li>Three widths</li></ul>"
 "<h3>Specifications</h3><ul><li>50 mm (BAT-PB50)</li><li>75 mm (BAT-PB75)</li><li>100 mm (BAT-PB100)</li></ul>"
 "<h3>Good to know</h3><ul><li>Membrane sets hard in the bristles, so wash out straight after use or treat the brush as disposable</li><li>Follow your membrane maker's coat thickness and drying times</li></ul>",
 [BT+"bat-paint-brush-50mm/"])

add("bat-utility-knife",
 bat("BAT Utility Knife", "UK-1", "<p>A general purpose snap-blade utility knife for cutting membrane, cardboard, backer rod and sealant.</p><p><strong>What fits:</strong> Takes standard snap-off blades (BAT pack UKSB-10).</p>"),
 "<p>The BAT Utility Knife is a general purpose snap blade knife for the cutting a tiling job throws up: trimming membrane, slicing backer rod, opening adhesive bags and cutting out old sealant. Snap off a dull segment and you have a fresh edge in a second.</p>"
 "<h3>Use it for</h3><ul><li>Cutting waterproofing membrane, bond breaker tape and backer rod</li><li>Trimming cured sealant and opening packaging</li><li>Scoring plasterboard and cement sheet</li></ul>"
 "<h3>Features</h3><ul><li>Snap-off blade for a fresh edge without changing blades</li><li>Retractable for safe carry</li></ul>"
 "<h3>Fits</h3><ul><li>Standard snap-off blades (BAT pack UKSB-10)</li></ul>"
 "<h3>Specifications</h3><ul><li>Model: UK-1</li></ul>"
 "<h3>Good to know</h3><ul><li>Snap blades with pliers, not fingers</li><li>Retract the blade before it goes in a pocket or tool bag</li></ul>",
 [BT], False, "UK-1 not listed on battrims.com or stockists; written from title and old description.")

add("bat-pro-folding-utility-knife-spare-blade-set-10-pce",
 bat("BAT Pro Folding Utility Knife Spare Blade Set (10 pce)", "BP-FKSB10", "<p>A 10 piece set of spare blades for the BAT Pro folding utility knife.</p>"),
 "<p>A 10 piece set of spare blades for the BAT Pro Folding Utility Knife. Membrane, backer rod and packaging dull a blade fast, and a sharp blade tracks true under load so cuts stay where you put them.</p>"
 "<h3>Fits</h3><ul><li>BAT Pro Folding Utility Knife: a steel bodied folding knife with soft grip handle and belt clip</li></ul>"
 "<h3>Use it for</h3><ul><li>Replacing worn blades in the BAT Pro folding knife</li><li>Keeping a sharp edge for membrane, expansion joint filler, backer rod and packaging</li></ul>"
 "<h3>What's in the box</h3><ul><li>10 trapezoid utility blades</li></ul>"
 "<h3>Specifications</h3><ul><li>Model: BP-FKSB10</li></ul>"
 "<h3>Good to know</h3><ul><li>Change the blade when it starts tearing membrane rather than slicing it</li><li>Dispose of used blades in a sealed container</li></ul>",
 [BT+"bat-pro-folding-utility-knife-with-5-blades-6-pack-counter-display/", "https://adheseal.com.au/products/b-a-t-pro-folding-utility-knife"])

add("bat-deluxe-grout-remover-spare-blade",
 bat("BAT Deluxe Grout Remover - Spare Blade", "GR-DLX-SB", "<p>Replacement Blades to suit Deluxe Grout Remover (GR-DLX-SG).</p><p>Includes 1 x Serrated tooth blade and 1 x Tungsten grit blade.</p>"),
 "<p>Replacement blades for the BAT Deluxe Grout Remover (GR-DLX-SG). The set gives you both cutting styles the tool uses: a serrated tooth blade that saws out soft or sanded grout, and a tungsten grit blade that grinds through hard, old grout and epoxy.</p>"
 "<h3>Fits</h3><ul><li>BAT Deluxe Grout Remover with soft grip handle (GR-DLX-SG)</li></ul>"
 "<h3>What's in the box</h3><ul><li>1 x serrated tooth blade</li><li>1 x tungsten grit blade</li></ul>"
 "<h3>Use it for</h3><ul><li>Raking out failed or mouldy grout before regrouting</li><li>Cleaning hardened grout out of joints before silicone</li></ul>"
 "<h3>Specifications</h3><ul><li>Model: GR-DLX-SB</li></ul>"
 "<h3>Good to know</h3><ul><li>Work the blade along the centre of the joint and let the grit do the cutting; pressing sideways chips glazed edges</li><li>Vacuum the joint out before new grout goes in</li></ul>",
 [BT+"deluxe-grout-remover-spare-blade/", BT+"deluxe-grout-remover-soft-grip/"])

add("batseal-delta-silicone-joint-cutter-spare-blade-set",
 bat("BATSEAL Delta Silicone Joint Cutter Spare Blade Set", "S A-DSJC-SB", "<p>Spare Blade set to suit Delta Silicone Joint Cutter</p>"),
 "<p>A spare blade set for the BAT Delta Silicone Joint Cutter, the angled tool for cutting old silicone out of shower and bath joints. The cutter reaches in at 45 degrees so the blade runs along both faces of the joint, and a fresh set of blades is what keeps it slicing rather than tearing.</p>"
 "<h3>Fits</h3><ul><li>BAT Delta Silicone Joint Cutter (S A-DSJC)</li></ul>"
 "<h3>Use it for</h3><ul><li>Stripping old or mouldy silicone from wet area joints before resealing</li><li>Cleaning sealant off tile edges without scratching the glaze</li></ul>"
 "<h3>Specifications</h3><ul><li>Model: S A-DSJC-SB</li></ul>"
 "<h3>Good to know</h3><ul><li>Cut both sides of the bead, then peel the strip out</li><li>Clean the joint with Maxisil Cleaner before new silicone goes in</li><li>Dispose of used blades in a sealed container</li></ul>",
 [BT+"delta-silicone-joint-cutter-spare-blade-set/", BT+"delta-silicone-joint-cutter/"])

add("bat-20-ltr-promotional-bucket-lid",
 '<p><strong>Fits:</strong> BAT 20 litre bucket</p><p>Snap-on lid for the BAT 20 litre bucket.</p>' + BUY.format(t="BAT 20 Ltr Bucket Lid", b="BAT") + "<p><strong>Code:</strong> BAT-20LPBLID</p>" + DEL,
 "<p>The BAT 20 Ltr Bucket Lid snaps onto the BAT 20 litre bucket to keep water, part mixed material and tools covered between jobs. With a lid on, a bucket of spacers or wedges rides in the van without tipping out, and sponge water does not slop over the floor.</p>"
 "<h3>Fits</h3><ul><li>BAT 20 litre bucket</li></ul>"
 "<h3>Use it for</h3><ul><li>Covering clean up water and tools in transit</li><li>Keeping dust and grit out of clean water</li><li>Stacking buckets of spacers, wedges and small tools</li></ul>"
 "<h3>Features</h3><ul><li>Snap-on fit</li><li>Plastic, easy to rinse</li></ul>"
 "<h3>Specifications</h3><ul><li>Suits: 20 litre BAT bucket</li><li>Model: BAT-20LPBLID</li></ul>"
 "<h3>Good to know</h3><ul><li>Lid only; the bucket is sold separately</li><li>Do not seal a bucket of cement based mix and expect it to keep; grout and adhesive go off within the pot life either way</li></ul>",
 [BT], False, "Lid not listed on battrims.com or stockists; written from title and old description.")

# ---------------- Panther ----------------
PANSYS = ("<h3>Good to know</h3><ul><li>Panther base clips come in 1, 1.5, 2 and 3 mm joint widths for tiles 3 to 12 mm thick, with large base clips for 11 to 20 mm tiles and stone clips for 23 to 32 mm</li>"
          "<li>Clips are single use and snap off at the base once the adhesive has set; the wedges are reused</li>"
          "<li>A levelling system does not fix a bad substrate or thin adhesive coverage</li></ul>")
add("panther-levelling-spacers-adjustable-traction-pliers-floor",
 "<p>Adjustable traction pliers for driving Panther levelling wedges on floor tiling installations.</p>" + BUY.format(t="Panther Levelling System Adjustable Traction Pliers - Floor", b="Panther") + "<p><strong>Code:</strong> PAN-LSATPF</p>" + DEL,
 "<p>The Panther Adjustable Traction Pliers drive the wedge into a Panther levelling clip with one squeeze, pulling two tile edges level while the adhesive cures. The adjustable stop sets how far the wedge goes in, so every clip gets the same tension and you are not snapping clips on thin tiles or under tightening on thick ones.</p>"
 "<h3>Use it for</h3><ul><li>Floor tiling with the Panther Levelling System clips and wedges</li><li>Large format and rectified porcelain where lippage shows</li><li>Thin, flexible or heavy tiles that will not sit flat on their own</li></ul>"
 "<h3>Features</h3><ul><li>Adjustable tension so wedge depth is repeatable</li><li>Floor pattern for working down onto the tile</li><li>Fits the Panther levelling wedges</li></ul>"
 "<h3>Specifications</h3><ul><li>Suits: Panther Levelling System wedges and base clips</li><li>Model: PAN-LSATPF</li></ul>" + PANSYS,
 [BT+"panther-levelling-spacers-adjustable-traction-pliers-floor/", BT+"panther-levelling-system-wedges-x-250s/", "https://adheseal.com.au/products/panther-levelling-system-base-clips"])

add("panther-tile-levelling-system-wedges",
 "<p>Panther levelling system wedges, reusable, in bags of 250 or 500.</p><p>Strong Reinforced Wedge Base avoids distortion of the Wedge when inserting</p>" + BUY.format(t="Panther Tile Levelling System Wedges", b="Panther") + "<p><strong>Codes:</strong> PAN-LSW250, PAN-LSW500</p>" + DEL,
 "<p>Panther Levelling System Wedges are the reusable half of the Panther tile levelling system. Pushed through a base clip, the wedge pulls two tile edges flush while the adhesive sets, so large format floors come up without lippage. A reinforced base stops the wedge bending as the pliers drive it in.</p>"
 "<h3>Use it for</h3><ul><li>Floor and wall tiling with Panther base clips</li><li>Large format, rectified and thin porcelain</li><li>Any job where tile lippage would show</li></ul>"
 "<h3>Features</h3><ul><li>Reusable: pull the wedge after the clip snaps off and use it on the next job</li><li>Strong reinforced wedge base avoids distortion when inserting</li><li>Fits all Panther base clips and the Panther traction pliers</li></ul>"
 "<h3>Specifications</h3><ul><li>Bags: 250 (PAN-LSW250), 500 (PAN-LSW500)</li><li>Base clips sold separately</li></ul>" + PANSYS,
 [BT+"panther-levelling-system-wedges-x-250s/", "https://adheseal.com.au/products/panther-levelling-system-wedges"])

add("panther-20-ltr-promotional-bucket-lid-orange",
 '<p><strong>Fits:</strong> Panther 20 litre bucket</p><p>Orange snap-on lid for the Panther 20 litre bucket.</p>' + BUY.format(t="Panther 20 Ltr Bucket Lid - Orange", b="Panther") + "<p><strong>Code:</strong> PAN-20LPBLID</p>" + DEL,
 "<p>The Panther 20 Ltr Bucket Lid is an orange snap-on lid for the Panther 20 litre bucket. It keeps clean up water, part mixed material and small tools covered in the van and on site, and the orange colour makes the Panther bucket easy to pick out of a stack.</p>"
 "<h3>Fits</h3><ul><li>Panther 20 litre bucket</li></ul>"
 "<h3>Use it for</h3><ul><li>Covering sponge water and tools in transit</li><li>Keeping grit out of clean water</li><li>Stacking buckets of spacers, wedges and levelling clips</li></ul>"
 "<h3>Features</h3><ul><li>Snap-on fit</li><li>Orange plastic, easy to rinse</li></ul>"
 "<h3>Specifications</h3><ul><li>Suits: 20 litre Panther bucket</li><li>Colour: orange</li><li>Model: PAN-20LPBLID</li></ul>"
 "<h3>Good to know</h3><ul><li>Lid only; the bucket is sold separately</li><li>Cement based mixes go off within their pot life even with a lid on</li></ul>",
 [BT], False, "Lid not listed on battrims.com or stockists; written from title and old description.")

assert len(R) == 58, len(R)
assert set(r["handle"] for r in R) == set(byh), set(byh) - set(r["handle"] for r in R)
R.sort(key=lambda r: todo.index(byh[r["handle"]]))
json.dump(R, open(OUT, "w"), indent=1, ensure_ascii=False)

# ---- hard-rule check ----
BAD = ["$", "trade", "stock", "showroom", "maddington", "deliver", "pick up", "shipping", "eternity", "dsa", "bathroom city",
       "elevate", "stunning", "seamless", "!", "transform", "curated", "timeless", "discover", "unlock", "premium", "look no further",
       "perfect for any", "—", "–", "link in bio", "moq", "supplier", "cheaper", "best price", "in stock"]
fail = 0
for r in R:
    txt = H.unescape(re.sub("<[^>]+>", " ", r["new"])).lower()
    words = len(txt.split())
    hits = [b for b in BAD if b in txt]
    if hits or not (90 <= words <= 200):
        fail += 1
        print("CHECK", r["handle"], words, hits)
print("records", len(R), "fails", fail, "verified", sum(r["verified"] for r in R))
