"""Build bat-2-2026-10-24.json: rewrites for 89 BAT tools/drains/consumables.
Usage: python3 -I build_bat_2_2026_10.py <current.json from Shopify>
current.json = {handle: {"old": descriptionHtml, "skus": "..."}} fetched via Admin GraphQL on 24 Oct 2026.
Facts come from battrims.com Store API short descriptions (fetched 24 Oct 2026) and the existing descriptions."""
import json, re, sys

HERE = "/home/user/Excellent-Tiling-Services-/store-content/descriptions/"
OUT = HERE + "bat-2-2026-10-24.json"
todo = json.load(open(HERE + "todo-bat-2.json"))
byh = {t["handle"]: t for t in todo}
cur = json.load(open(sys.argv[1]))
BT = "https://battrims.com/product/"
R = []

def words(h): return len(re.sub(r"<[^>]+>", " ", h).split())

def add(handle, new, sources, verified=True, notes=""):
    t = byh[handle]
    src = [BT + s + "/" if not s.startswith("http") and not s.startswith("Shopify") and not s.startswith("existing") else s for s in sources]
    R.append({"id": t["id"], "handle": handle, "title": t["title"], "old": cur[handle]["old"], "new": new,
              "sources": src, "verified": verified, "notes": notes, "words": words(new)})

def ul(*items): return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def sec(title, *items): return f"<h3>{title}</h3>" + ul(*items)

# ---------------- stirrers ----------------
STIR_GTK = sec("Good to know",
    "Run the mixer at low speed to start so the powder does not dust up, then bring the speed up",
    "Rinse the paddle straight after use. Set adhesive is hard to get off the spiral",
    "A worn or bent paddle mixes unevenly, so keep a spare on the truck")

add("bat-liquid-stirrer-to-suit-electric-mixer-140-x-600-x-m14mm",
 "<p>The BAT Liquid Stirrer is a 140 mm double spiral mixing paddle on a 600 mm shaft with an M14 thread. It screws straight onto the BAT Pro 1050 W and 1600 W hand mixers, or any other M14 mixing drill.</p>"
 + sec("Use it for", "Mixing tile adhesive, grout, screed and levelling compound", "Plaster, render, paint and other thick liquids")
 + sec("Features", "Double spiral head folds the mix through for fewer dry lumps", "Bright steel", "Large bottom ring so the paddle does not chew into the bucket", "M14 thread for quick fitting and removal")
 + sec("Specifications", "Head diameter: 140 mm", "Shaft length: 600 mm", "Thread: M14", "Model: BAT-ST140", "Other sizes in the range: 100, 135 and 160 mm heads")
 + sec("Fits", "BAT Pro 1050 W and 1600 W electric hand mixers", "Any mixing drill with an M14 thread")
 + STIR_GTK,
 ["liquid-stirrer-to-suit-electric-mixer-140-x-600-x-m14mm", "https://stonex.com.au/products/bat-mixing-paddle-m14"])

add("bat-em-1600-p-spare-liquid-stirrer-140-x-590-x-m14mm",
 "<p>The BAT EM 1600 P Spare Liquid Stirrer is the replacement paddle for the BAT Pro 1600 W electric mixer. It has the same 140 mm double spiral head the mixer ships with, on a 590 mm shaft with an M14 thread, so it goes on and comes off in seconds.</p>"
 + sec("Use it for", "Replacing a bent, worn or lost paddle on the BAT Pro 1600 W mixer", "Keeping a second paddle for grout so adhesive residue never ends up in the grout mix")
 + sec("Features", "Double spiral head for lump free adhesive, screed and levelling compound", "M14 thread for easy connection and removal")
 + sec("Specifications", "Head diameter: 140 mm", "Shaft length: 590 mm", "Thread: M14", "Model: BAT-EM1600ST")
 + sec("Fits", "BAT Pro 1600 W electric hand mixer (BAT-EM1600P)", "The M14 thread also fits the BAT Pro 1050 W mixer and any other M14 mixing drill")
 + STIR_GTK,
 ["bat-em-1600-p-spare-liquid-stirrer-140-x-590-x-m14mm", "https://adheseal.com.au/products/bat-trims-em1600p-spare-liquid-stirrer-140mm-x-590mm-x-m14-thread"])

add("bat-em-1050p-spare-liquid-stirrer-120-x-590-x-m14mm",
 "<p>The BAT EM 1050P Spare Liquid Stirrer is the replacement paddle for the BAT Pro 1050 W electric mixer. The 120 mm double spiral head is matched to the smaller motor, so it mixes a bucket of adhesive without bogging the drill down.</p>"
 + sec("Use it for", "Replacing a bent, worn or lost paddle on the BAT Pro 1050 W mixer", "A second paddle kept clean for grout or levelling compound")
 + sec("Features", "Double spiral head folds powder through the water for a lump free mix", "M14 thread for easy connection and removal")
 + sec("Specifications", "Head diameter: 120 mm", "Shaft length: 590 mm", "Thread: M14", "Model: BAT-EM1050ST")
 + sec("Fits", "BAT Pro 1050 W electric hand mixer", "The M14 thread also fits the BAT Pro 1600 W mixer and any other M14 mixing drill")
 + STIR_GTK,
 ["bat-em-1050p-spare-liquid-stirrer-120-x-590-x-m14mm", "https://adheseal.com.au/products/bat-em-1050p-spare-liquid-stirrer-120mm-x-590mm-x-m14-thread"])

# ---------------- trowels ----------------
TROWEL_GTK = sec("Good to know",
    "Comb adhesive in straight lines so air can escape when the tile is pressed down",
    "Bright steel rusts if put away wet. Wash it, dry it and wipe it with oil",
    "Check the notch size against your adhesive data sheet before you start")

add("bat-bright-steel-v-notch-trowel-soft-grip",
 "<p>The BAT Bright Steel V Notch Trowel is a carbon steel trowel with a soft grip handle, in nine V notch sizes. V notches lay a thinner bed than square notches, so they suit vinyl, carpet, rubber and timber flooring adhesives as well as thin bed tiling.</p>"
 + sec("Use it for", "1.6 mm (V1): vinyl sheet and vinyl plank", "2.4 mm (V2): direct stick carpet", "3.2 mm (V3): rubber flooring", "4.9 mm V flat (V5 flat): direct stick timber flooring", "6 mm (V6): one step and 3 in 1 flooring adhesives", "3, 5, 8 and 12 mm: thin bed tile adhesive")
 + sec("Features", "Bright (carbon) steel blade", "Soft grip handle", "Pointed V on the 5 and 12 mm, rounded V on the 8 mm")
 + sec("Specifications", "Models: BAT-BSV1-SG (1.6 mm), BAT-BSV2-SG (2.4 mm), BAT-BSV-SG (3 mm), BAT-BSV3-SG (3.2 mm), BAT-BSV5-SG (4.9 mm flat), BAT-BSPV5-SG (5 mm), BAT-BSV6-SG (6 mm), BAT-BSRV8-SG (8 mm), BAT-BSPV12-SG (12 mm)")
 + TROWEL_GTK,
 ["bat-bright-steel-trowel-3mm-v-s-grip", "b-a-t-bright-steel-trowel-1-6mm-v-notch-s-grip", "b-a-t-bright-steel-trowel-4-9mm-v-flat-notch-s-grip", "b-a-t-bright-steel-trowel-6mm-v-notch-s-grip"])

add("bat-bright-steel-square-notch-trowel-soft-grip",
 "<p>The BAT Bright Steel Square Notch Trowel is the everyday tiling trowel: a carbon steel blade with square notches and a soft grip handle, in six notch sizes from 4 to 15 mm. Square notches leave even ridges of adhesive that collapse into a full bed when the tile is pressed in.</p>"
 + sec("Use it for", "4 and 6 mm: wall tiles, small format floor tiles and mosaics on sheets", "8 and 10 mm: standard floor tiles and larger wall tiles", "12 and 15 mm: large format tiles and floors that need a thicker bed")
 + sec("Features", "Bright (carbon) steel blade", "Soft grip handle", "Square notch profile")
 + sec("Specifications", "Notch sizes: 4, 6, 8, 10, 12 and 15 mm", "Models: BAT-BS4-SG, BAT-BS6-SG, BAT-BS8-SG, BAT-BS10-SG, BAT-BS12-SG, BAT-BS15-SG")
 + TROWEL_GTK,
 ["bat-bright-steel-trowel-4mm-s-grip", "bat-bright-steel-trowel-10mm-s-grip", "bat-bright-steel-trowel-15mm-s-grip"])

add("bat-professional-stainless-steel-square-notch-trowel-soft-grip",
 "<p>The BAT Professional Stainless Steel Square Notch Trowel is the step up from bright steel: the blade will not rust, so it stays smooth and clean through years of adhesive and wash water. It has a soft grip handle and comes in five square notch sizes.</p>"
 + sec("Use it for", "4 and 6 mm: wall tiles and mosaics", "8 and 10 mm: standard floor and large wall tiles", "15 mm: large format tiles and thick beds", "Tilers who want a trowel that can be left in the bucket without rust marks")
 + sec("Features", "Stainless steel blade that does not rust or stain light adhesives", "Soft grip handle", "Square notch profile")
 + sec("Specifications", "Notch sizes: 4, 6, 8, 10 and 15 mm", "Models: BAT-SS4-SG, BAT-SS6-SG, BAT-SS8-SG, BAT-SS10-SG, BAT-SS15-SG")
 + sec("Good to know", "Comb adhesive in straight lines so air can escape when the tile is bedded", "Stainless still needs a wash at the end of the day; set adhesive is hard on any blade", "Match the notch to the adhesive data sheet and tile size"),
 ["bat-professional-stainless-steel-trowel-4mm-s-grip", "bat-professional-stainless-steel-trowel-15mm-s-grip"])

add("bat-bright-steel-long-blade-trowel-soft-grip",
 "<p>The BAT Bright Steel Long Blade Trowel has a longer carbon steel blade than a standard trowel, so each pass spreads more adhesive and large format tiles get combed in fewer strokes. Soft grip handle, four notch options including a 15 mm half moon.</p>"
 + sec("Use it for", "Large format floor tiles and panels", "Big floors where a standard blade means too many passes", "15 mm half moon: thick beds under large tiles, with rounded ridges that collapse without trapping air")
 + sec("Features", "Long bright (carbon) steel blade", "Soft grip handle", "Square notches in 8, 10 and 12 mm, half moon in 15 mm")
 + sec("Specifications", "Notch sizes: 8, 10, 12 mm square and 15 mm half moon", "Models: BAT-LBBST-8-SG, BAT-LBBST-10-SG, BAT-LBBST-12-SG, BAT-LBBST-HM15-SG")
 + TROWEL_GTK,
 ["bat-bright-steel-long-blade-trowel-8mm-s-grip", "bat-bright-steel-long-blade-trowel-15mm-h-m-s-grip"])

# ---------------- abrasives ----------------
add("bat-diamond-hand-polishing-pad",
 "<p>The BAT Diamond Hand Polishing Pad takes the sharp, chipped edge off a cut tile by hand, with no grinder and no dust cloud. Work through the four grits and a cut edge on porcelain or stone finishes close to the factory edge.</p>"
 + sec("Use it for", "Dressing cut edges on porcelain, ceramic and stone before they go on the wall", "Exposed cut edges at niches, window sills and external corners", "Softening the arris on a cut edge so it does not chip later")
 + sec("Features", "Diamond grit bonded to a hand sized pad", "Four grits that work as a sequence")
 + sec("Specifications", "60 grit: first pass, removes the rough edge (BAT-DHP060)", "200 grit: refines the edge and starts to smooth it (BAT-DHP200)", "400 grit: creates the fine finish (BAT-DHP400)", "800 grit: smoothest finish, used after the 60, 200 and 400 (BAT-DHP800)")
 + sec("Good to know", "Use it wet. A little water keeps the dust down and makes the diamond last longer", "Hold the pad at a slight angle and work along the edge, not across it", "Start coarse and finish fine; skipping grits leaves scratches the next pad cannot remove"),
 ["bat-diamond-hand-polishing-pad-60-grit", "bat-diamond-hand-polishing-pad-800-grit"])

add("bat-pro-pva-abrasive-wheel-100mm",
 "<p>The BAT Pro PVA Abrasive Wheel is a 100 mm polishing wheel for an angle grinder, made to finish the cut edges of porcelain, stone and concrete. Seven grits take an edge from rough to polished.</p>"
 + sec("Use it for", "Polishing exposed cut edges on porcelain and stone", "Taking saw marks off mitred edges before they are glued", "Dressing concrete edges and small chips")
 + sec("Features", "PVA bonded abrasive wheel", "16 mm bore", "Seven grits so you can work up to the finish you want")
 + sec("Specifications", "Diameter: 100 mm", "Bore: 16 mm", "Recommended speed: 11,400 rpm", "Grits: 36, 60, 120, 220, 320, 400 and 600", "Models: BP-PVA036, BP-PVA060, BP-PVA120, BP-PVA220, BP-PVA320, BP-PVA400, BP-PVA600", "10 packs: BP-PVA060/10 (60 grit) and BP-PVA220/10 (220 grit)")
 + sec("Good to know", "Check the 16 mm bore suits your grinder arbor before fitting", "Keep the wheel moving and use light pressure; let the grit do the work", "Wear eye protection and a dust mask, and keep the grinder guard on"),
 ["bat-pro-pva-abrasive-wheel-100mm-36-grit", "bat-pro-pva-abrasive-wheel-100mm-600-grit"])

# ---------------- Maximo ----------------
add("bat-maximo-grout-clean-up-system-commodore",
 "<p>The BAT Maximo Grout Clean Up System is a complete wash bucket for sponging grout off fresh tiling. The tri-roller system wrings the sponge out with one pass across the bucket, so your hands stay out of the dirty water and the sponge goes back onto the tile just damp, which is what you want for a clean, haze free finish.</p>"
 + sec("What's in the box", "Maximo bucket with carry handle", "Tri-roller wringing system", "Plastic grate", "Maximo Commodore Velcro handle, 130 x 300 mm (BAT-MAXVHC)", "Maximo Commodore Velcro sponge, 150 x 320 mm (BAT-MAXVSC)")
 + sec("Features", "Three rollers wring the sponge evenly and the perforated top rollers separate out lumps of grout", "Velcro backed handle so a worn sponge swaps in seconds", "Rollers underneath so the bucket slides along the floor with you")
 + sec("Specifications", "Model: BAT-MAXIMO-C")
 + sec("Good to know", "Every part is sold as a spare: Velcro handle, Velcro sponge, plastic grate, top roller set (3), bottom roller set (2) and the 23 litre bucket", "Change the water often; dirty water puts the grout haze straight back on the tile", "Rinse the rollers and grate at the end of the day so grout does not set on them"),
 ["bat-maximo-grout-clean-up-system-commodore", "bat-maximo-grout-clean-up-system-spare-bucket-23-ltr"])

add("bat-maximo-plastic-grate",
 "<p>The BAT Maximo Plastic Grate is the replacement grate for the Maximo grout clean up bucket, and it also fits the Washboy Profi bucket. The grate sits in the bucket so the sponge float rests on it rather than in the grout sludge that settles on the bottom.</p>"
 + sec("Use it for", "Replacing a cracked or missing grate in a Maximo bucket", "Fitting a grate to a Washboy bucket (WB-BUCK)")
 + sec("Features", "Plastic construction, so it will not rust in grout water", "Keeps the float and sponge clear of settled grout")
 + sec("Specifications", "Model: BAT-MAXPG")
 + sec("Fits", "BAT Maximo grout clean up system", "Washboy Profi bucket (WB-BUCK)")
 + sec("Good to know", "Rinse it with the bucket at the end of the day; set grout is hard to get off plastic", "Other Maximo spares sold separately: Velcro handle, Velcro sponge, top rollers, bottom rollers and the 23 litre bucket"),
 ["maximo-plastic-grate"])

add("bat-maximo-commodore-velcro-handle-130-x-300mm",
 "<p>The BAT Maximo Commodore Velcro Handle is the float handle from the Maximo grout clean up system, sold on its own. It is a 130 x 300 mm plate with a hook and loop face, so the 150 x 320 mm Velcro sponge presses on and peels off without clips or glue.</p>"
 + sec("Use it for", "Replacing a broken handle from a Maximo Commodore system", "Running a second float so one sponge washes while the other works")
 + sec("Features", "Velcro face holds the sponge flat across the whole plate", "Sponge changes take seconds")
 + sec("Specifications", "Plate size: 130 x 300 mm", "Model: BAT-MAXVHC")
 + sec("Fits", "BAT Maximo Commodore grout clean up system", "Takes the BAT Maximo Commodore Velcro sponge, 150 x 320 mm (BAT-MAXVSC)")
 + sec("Good to know", "Keep grout out of the hook and loop face; rinse it when you change sponges", "Sponge sold separately"),
 ["maximo-com-vel-handle-130-x-300mm"])

add("bat-maximo-commodore-velcro-sponge-150-x-320mm",
 "<p>The BAT Maximo Commodore Velcro Sponge is the replacement sponge for the Maximo grout clean up system. At 150 x 320 mm it overhangs the 130 x 300 mm Velcro handle slightly, so the edges of the handle never touch the tile, and the hook and loop backing means it swaps over in seconds.</p>"
 + sec("Use it for", "Washing grout off fresh tiling with the Maximo system", "Replacing a sponge that has gone hard, torn or filled with grout")
 + sec("Features", "Velcro backing, no clips", "Sized to overhang the handle so the plate cannot scratch the tile")
 + sec("Specifications", "Size: 150 x 320 mm", "Model: BAT-MAXVSC")
 + sec("Fits", "BAT Maximo Commodore Velcro handle (BAT-MAXVHC)")
 + sec("Good to know", "Rinse the sponge well before grout sets in it; a sponge full of hard grout scratches the glaze", "Wring it through the Maximo rollers rather than by hand so it goes back onto the tile just damp", "Keep a spare so a fresh sponge is ready for the final wash"),
 ["maximo-com-vel-sponge-150-x-320mm"])

add("bat-maximo-bucket-roller-set-of-2",
 "<p>The BAT Maximo Bottom Roller Set is the pair of rollers that bolt under the Maximo grout clean up bucket. They let a full bucket of water roll along the floor beside you instead of being lifted every couple of metres.</p>"
 + sec("Use it for", "Replacing worn, cracked or missing bottom rollers on a Maximo bucket")
 + sec("Features", "Hard wearing plastic", "Two piece set")
 + sec("Specifications", "Set of 2 rollers", "Model: BAT-MAXBR2")
 + sec("Fits", "BAT Maximo grout clean up bucket (bottom rollers)")
 + sec("Good to know", "These are the rollers under the bucket. The three wringing rollers inside the bucket are the Top Roller Set (BAT-MAXRR3)", "Knock grout off the rollers before it sets or they stop turning freely", "Other Maximo spares: Velcro handle, Velcro sponge, plastic grate and the 23 litre bucket"),
 ["maximo-bucket-roller-set-of-2"])

add("bat-maximo-grout-clean-up-system-spare-bucket-23-ltr",
 "<p>The BAT Maximo Spare Bucket is the 23 litre bucket from the Maximo grout clean up system, sold on its own. Buy one to replace a cracked bucket, or run two so a clean water bucket is always ready for the final sponge over.</p>"
 + sec("Use it for", "Replacing a damaged Maximo bucket", "A second bucket of clean water for the final wash")
 + sec("Features", "23 litre fluid capacity", "Carry handle")
 + sec("Specifications", "Capacity: 23 litres", "Model: BAT-MAXBUCK")
 + sec("Fits", "BAT Maximo grout clean up system")
 + sec("Good to know", "Bucket only. The rollers, grate, handle and sponge are sold separately as spares", "Empty grout water somewhere it can settle, not down a floor waste; the fines set in the pipe"),
 ["bat-maximo-grout-clean-up-system-spare-bucket-23-ltr"])

add("bat-maximo-grout-clean-up-set-replacement-roller-set",
 "<p>The BAT Maximo Replacement Top Roller Set is the three wringing rollers from the Maximo grout clean up bucket. Drag the sponge across them and they squeeze the dirty water out in one pass, while the perforated rollers let the larger lumps of grout fall through instead of going back onto the tile.</p>"
 + sec("Use it for", "Replacing worn or broken wringing rollers in a Maximo bucket", "Restoring a bucket that has stopped wringing the sponge properly")
 + sec("Features", "Three roller set", "Perforated rollers separate out lumps of grout from the first clean up")
 + sec("Specifications", "Set of 3 rollers", "Model: BAT-MAXRR3")
 + sec("Fits", "BAT Maximo grout clean up bucket (top rollers)")
 + sec("Good to know", "These are the rollers inside the bucket. The two rollers underneath are the Bottom Roller Set (BAT-MAXBR2)", "Rinse the rollers before grout sets on them", "Other Maximo spares: Velcro handle, Velcro sponge, plastic grate and the 23 litre bucket"),
 ["maximo-grout-clean-up-set-replacement-roller-set"])

# ---------------- sponges ----------------
add("bat-sponge-hydro-tilers-and-slaters",
 "<p>The BAT Hydro Tilers and Slaters Sponge is BAT's most popular sponge, made in Germany for maximum water absorption. At 300 x 210 x 35 mm it covers a lot of tile per wipe, and it holds enough water to lift grout haze without flooding the joints.</p>"
 + sec("Use it for", "Washing grout off tiles and slate as you go", "Wiping down adhesive smears before they set", "Wetting down a floor or wall before grouting", "Cleaning tools and buckets")
 + sec("Features", "Hydro sponge for maximum absorption", "Large face for fast coverage", "Made in Germany")
 + sec("Specifications", "Size: 300 x 210 x 35 mm", "Model: SP-TILSLA")
 + sec("Good to know", "Wring it out well before it goes back on the tile; a dripping sponge washes the grout out of the joint", "Rinse it before grout sets in it, and change the water often", "Fits the roller wringers on grout clean up buckets"),
 ["sponge-hydro-tilers-and-slaters"])

add("bat-synthetic-abrasive-sponge-190-x-140-x-50mm",
 "<p>The BAT Pro Synthetic Abrasive Sponge is made for epoxy and urethane grout clean up, where a normal sponge smears the resin around instead of lifting it. The abrasive face scrubs the residue off the tile without scratching tile, stone or the grout joint.</p>"
 + sec("Use it for", "First stage clean up of epoxy and urethane grout", "Scrubbing grout haze off textured or non-slip tiles", "Shifting adhesive smears a plain sponge cannot move")
 + sec("Features", "Synthetic abrasive face", "Will not harm or scratch tile, stone or grout", "Extremely durable and long lasting")
 + sec("Specifications", "Size: 190 x 140 x 50 mm", "Model: SP-RGHAZE")
 + sec("Good to know", "Follow the grout maker's clean up method and timing; epoxy gets much harder to shift once it starts to cure", "Use with clean water and rinse the sponge often", "Finish with a plain hydro sponge for the final wipe"),
 ["synthetic-abrasive-sponge-190-x-140-x-50mm"])

add("bat-luxe-waste-pipe-sponge",
 "<p>The BAT Luxe Waste Pipe Sponge is a plug you push into the floor waste while you grout, so grout and wash water cannot fall down the pipe and set in it. Pull it out when the grout is cleaned off and the waste is clear. Two sizes cover 50 mm wastes and 75 to 100 mm wastes.</p>"
 + sec("Use it for", "Blocking shower and floor wastes during grouting", "Keeping sand, screed and debris out of the pipe while you work around it")
 + sec("Features", "Compresses to fit, then expands to seal the pipe", "Easy to pull out and reuse")
 + sec("Specifications", "60 x 80 mm: suits 50 mm waste pipes (BL-WPS60)", "125 x 120 mm: suits 75 and 100 mm waste pipes (BL-WPS125)")
 + sec("Good to know", "It is a temporary plug, not a permanent seal. Remove it before the waste is used", "Fit it before you start grouting; grout that gets into a pipe is very hard to remove later", "A damp sponge seals better than a bone dry one"),
 ["b-a-t-luxe-waste-pipe-sponge-60-x-80mm", "b-a-t-luxe-waste-pipe-sponge-125-x-120mm"])

# ---------------- drilling ----------------
add("bat-electroplated-diamond-drill-bit",
 "<p>The BAT Electroplated Diamond Drill Bit cuts clean round holes in porcelain, ceramic and stone from a normal electric drill, without the tile cracking the way it does with a masonry bit. It is a wet use bit: a trickle of water keeps the diamond cool and the hole clean.</p>"
 + sec("Use it for", "Holes for tap spindles, shower rails, toilet roll holders and towel rails", "Pipe penetrations in porcelain and stone", "38 mm: holes for waste pipes and larger fittings")
 + sec("Features", "Electroplated diamond cutting edge", "Fits a standard drill chuck", "Wet use only")
 + sec("Specifications", "Diameters: 6, 8, 10, 12 and 38 mm", "Models: EPDB-6, EPDB-8, EPDB-10, EPDB-12, EPDB-38")
 + sec("Fits", "Standard electric drill chuck", "The suction drill guide in the EPDB-5PUK kit, and the BAT Pro suction cup guide, hold the bit on the mark")
 + sec("Good to know", "Start the hole at an angle, then bring the drill upright once the edge has bitten", "Keep water on the bit the whole time and do not force it; let the diamond cut", "Drill with low speed and light pressure through hard porcelain"),
 ["electroplated-diamond-drill-bit-6mm", "electroplated-diamond-drill-bit-38mm"])

add("bat-electroplated-diamond-drill-set-5pce-universal-kit",
 "<p>The BAT Electroplated Diamond Drill Set is a wet drilling kit for porcelain, ceramic and stone. Five bits cover the common fixing sizes, the suction guide holds the bit exactly where you want the hole, and the pressure bottle feeds water onto the cut so the diamond stays cool.</p>"
 + sec("What's in the box", "Electroplated diamond drill bits: 5, 6, 8, 10 and 12 mm", "0.9 litre water pressure bottle", "5 hole universal suction drill guide", "1.8 m of flexible hose")
 + sec("Use it for", "Holes for taps, towel rails, shower screens and bathroom accessories", "Drilling finished tiles on the wall without chipping the glaze")
 + sec("Features", "Suction guide locks onto the tile so the bit cannot wander", "Water fed from the bottle for wet drilling", "All bits fit a standard drill chuck")
 + sec("Specifications", "Model: EPDB-5PUK", "The guide takes 5 to 12 mm electroplated bits; spare bits are sold singly")
 + sec("Good to know", "Wet use only. Pump the bottle up and keep water on the bit the whole time", "Low speed, light pressure; forcing the bit glazes the diamond", "The suction cup needs a smooth, clean tile face to grip"),
 ["electroplated-diamond-drill-set-5pce-universal-kit", "https://stonex.com.au/products/bat-electroplated-diamond-core-drill-set"])

add("bat-pro-drill-bit-adapter-set-m10-to-m14",
 "<p>The BAT Pro Drill Bit Adapter Set lets you run M14 threaded diamond drill bits on an angle grinder with an M10 spindle. If your grinder is the smaller thread, this is the piece that opens up the whole BAT Pro dry cutting drill bit range to it.</p>"
 + sec("Use it for", "Fitting BAT Pro vacuum brazed dry drill bits (M14) to M10 angle grinders", "Any M14 threaded accessory on an M10 grinder")
 + sec("Specifications", "Thread: M10 to M14", "Model: BP-DBAS1014")
 + sec("Fits", "M10 angle grinders", "BAT Pro dry cutting drill bits 50, 55, 65, 88 and 110 mm (M14 thread)")
 + sec("Good to know", "Check the thread on your grinder spindle before ordering; most 100 and 125 mm grinders in Australia are M14, some compact models are M10", "Tighten the adapter firmly and check it before each use", "Follow the drill bit's speed rating, not the grinder's maximum"),
 ["bat-pro-drill-bit-adapter-set-m10-to-m14", "bat-pro-dry-cutting-drill-bit-50mm-m14-thread"])

add("bat-pro-dry-cutting-drill-bit-guide-with-suction-cup",
 "<p>The BAT Pro Dry Cutting Drill Bit Guide is a template on a suction cup. Stick it to the tile, line up the hole, and the guide holds the diamond bit on the mark while it bites. It is the difference between a clean round hole and a bit that skates across the glaze.</p>"
 + sec("Use it for", "Starting holes with BAT Pro dry cutting drill bits on an angle grinder", "Guiding wet electroplated bits in a drill", "Holes close to tile edges where a wandering bit would chip the corner")
 + sec("Features", "Suction cup fixing, no drilling or taping", "Template lies flat on the tile for accurate placement")
 + sec("Specifications", "Model: BP-DCDG")
 + sec("Fits", "BAT dry cutting (vacuum brazed) diamond drill bits", "BAT electroplated wet drill bits")
 + sec("Good to know", "The cup needs a smooth, clean, dry tile face to grip; it will not hold on heavily textured tiles", "Start the bit at a slight angle, then bring it upright", "Dry drilling makes fine dust: wear a mask and eye protection, and use water where you can to prolong the life of the diamond"),
 ["bat-pro-dry-cutting-drill-bit-guide-with-suction-cup", "bat-pro-dry-cutting-drill-bit-50mm-m14-thread"])

add("bat-super-cluster-diamond-grinding-wheel",
 "<p>The BAT Super Cluster Diamond Grinding Wheel is a diamond grinding wheel for the angle grinder that takes old adhesive, paint and high spots off a concrete floor fast. The clustered diamond segments are aggressive enough for set adhesive, which is the job most tilers buy it for.</p>"
 + sec("Use it for", "Grinding off old tile adhesive before retiling", "Knocking down high spots and laitance on new concrete", "General floor preparation before screed or adhesive")
 + sec("Features", "Clustered diamond segments for fast removal", "Two sizes: 100 mm for a standard grinder, 180 mm for a large grinder")
 + sec("Specifications", "Diameters: 100 mm and 180 mm", "Bore: 22.2/20 mm", "Models: BD-GWSC-100 (100 mm), BD-GWSC-180 (180 mm)")
 + sec("Good to know", "Always wear eye protection, hearing protection and a dust mask, and use a dust shroud and vacuum where you can", "Keep the wheel moving and flat; leaning on one edge gouges the slab", "Check the slab is sound and dry before grinding; damp adhesive clogs the segments"),
 ["bat-super-cluster-grinding-wheel-100mm-x-22-2-20mm", "bat-super-cluster-grinding-wheel-180mm-x-22-2-20mm"])

# ---------------- screeding and setting out ----------------
add("bat-aluminium-screed-bar-with-handle-50-x-45mm",
 "<p>The BAT Aluminium Screed Bar is a 50 x 45 mm powder coated box section with a handle, for cutting and levelling sand and cement screed and concrete. The two working edges are different, and the bar flips over so you can cut the screed down with one edge and smooth it with the other. Ten lengths from 1.2 to 5 m.</p>"
 + sec("Use it for", "Screeding bathroom and laundry floors to falls before tiling", "Levelling bedding mortar and concrete toppings", "Straightening long runs where a float is too short")
 + sec("Features", "Dual reversible working edges", "Powder coated aluminium that is light enough to pull all day", "Handle for control; the 4200 and 5000 mm bars have double handles")
 + sec("Specifications", "Section: 50 x 45 mm", "Lengths: 1200, 1500, 1800, 2100, 2400, 2700, 3000, 3600, 4200 and 5000 mm", "Models: BAT-SB-1200, BAT-SB-1500, BAT-SB-1800, BAT-SB-2100, BAT-SB-2400, BAT-SB-2700, BAT-SB-3000, BAT-SB-3600, BAT-SB-4200, BAT-SB-5000")
 + sec("Good to know", "Pick a bar longer than the gap between your screed rails so it rides on both", "Wash the screed off straight after use; set mortar ruins the edge", "Store it flat or hung so it stays straight"),
 ["bat-screed-bar-with-handle-50-x-45-x-1200mm", "bat-screed-bar-with-double-handle-50-x-45-x-5000mm"])

add("bat-powder-coated-straight-edge-70-x-20mm",
 "<p>The BAT Powder Coated Straight Edge is a 70 x 20 mm aluminium rule in bright yellow, so it stands out among the tools on a busy site. Use it to mark out, set lines and check that a floor, wall or run of tiles is straight. Seven lengths from 1.2 to 3 m.</p>"
 + sec("Use it for", "Marking out tile layouts and setting lines", "Checking screeds and walls for straightness before tiling", "Running a straight edge over laid tiles to find lippage")
 + sec("Features", "Vibrant yellow powder coat for easy identification on site", "Light aluminium section", "Seven lengths")
 + sec("Specifications", "Section: 70 x 20 mm", "Lengths: 1200, 1500, 1800, 2100, 2400, 2700 and 3000 mm", "Models: BAT-SE72-1200, BAT-SE72-1500, BAT-SE72-1800, BAT-SE72-2100, BAT-SE72-2400, BAT-SE72-2700, BAT-SE72-3000")
 + sec("Good to know", "For a heavier rule that doubles as a screeding straight edge, see the BAT 22 x 100 mm anodised straight edge", "Store it flat or hung by one end so it stays true", "Wipe adhesive off before it sets; a lump on the edge throws every check"),
 ["bat-straight-edge-powder-coated-70-x-20-x-1200mm", "bat-straight-edge-powder-coated-70-x-20-x-3000mm"])

add("bat-aluminium-straight-edge-22-x-100mm",
 "<p>The BAT Aluminium Straight Edge is the heavy duty option: a 22 x 100 mm section in hard wearing matt silver anodised aluminium, wider, thicker and stiffer than the 70 x 20 mm BAT-SE72 rule. The extra stiffness is what you want for checking long floors and screeds, where a light rule can flex and lie to you. Seven lengths up to 4 m.</p>"
 + sec("Use it for", "Checking screeds, slabs and large format tile floors for flatness", "Marking and setting out long lines", "Ruling off levelling compound and bedding")
 + sec("Features", "Matt silver anodised finish that resists scratches and adhesive", "Wider, thicker and sturdier than the BAT-SE72 straight edge", "Seven lengths")
 + sec("Specifications", "Section: 22 x 100 mm", "Lengths: 1500, 1800, 2100, 2400, 2700, 3000 and 4000 mm", "Models: BSE-1500, BSE-1800, BSE-2100, BSE-2400, BSE-2700, BSE-3000, BSE-4000")
 + sec("Good to know", "Set the edge on the floor and look for daylight under it; a 2 m length is the usual check for a tiled floor", "Store it flat or hung so it stays true", "Clean adhesive off before it sets"),
 ["bat-straight-edge-22-x-100-x-1500mm", "bat-straight-edge-22-x-100-x-4000mm"])

add("bat-spirit-level-2-vials",
 "<p>The BAT Spirit Level is a straightforward aluminium level with two vials, one for level and one for plumb, in seven lengths from 400 mm to 1.8 m. Shock resistant end caps take the knocks of being dropped on a tiled floor.</p>"
 + sec("Use it for", "Setting out level lines for wall tiling", "Checking tiles are plumb at corners, niches and shower screens", "Checking falls across a floor by sliding a packer under one end", "Long levels for setting screed rails and shelf angles")
 + sec("Features", "Durable aluminium body", "Two vials: horizontal (level) and vertical (plumb)", "Shock resistant end caps")
 + sec("Specifications", "Lengths: 400, 600, 800, 1000, 1200, 1500 and 1800 mm", "Models: SL-40, SL-60, SL-80, SL-100, SL-120, SL-150, SL-180")
 + sec("Good to know", "Check a level by reading it, turning it end for end and reading again; the bubble should sit in the same place", "The short lengths suit niches and single tiles, the long ones suit setting out whole walls", "A kit with one of each length is also available (SL-KITS)"),
 ["spirit-level-2-vials-400mm", "spirit-level-2-vials-1800mm"])

add("bat-spirit-levels-kit-1-of-each-size",
 "<p>The BAT Spirit Levels Kit gives you one of every length in the BAT range, from a 400 mm level for a niche up to 1.8 m for setting out a whole wall. Each level has two vials, a durable aluminium body and shock resistant end caps.</p>"
 + sec("What's in the box", "BAT spirit levels in 400, 600, 800, 1000, 1200, 1500 and 1800 mm", "Each level has 2 vials: horizontal (level) and vertical (plumb)")
 + sec("Use it for", "Setting up a new tiler or renovator with a full set of levels in one go", "Having the right length on hand for niches, single tiles, screen frames, screed rails and full walls")
 + sec("Features", "Durable aluminium construction", "Shock resistant end caps")
 + sec("Specifications", "Model: SL-KITS", "Individual levels: SL-40, SL-60, SL-80, SL-100, SL-120, SL-150, SL-180")
 + sec("Good to know", "Check each level now and then by reading it, flipping it end for end and reading again", "Store levels flat or hung; a level left standing on its end in a wet bucket will not stay true"),
 ["spirit-levels-kit-1-of-each-size"])

add("bat-pro-builders-square",
 "<p>The BAT Pro Builders Square is a set square for marking and checking right angles. Tilers use it to square up the first tiles off a wall, to mark 90 degree cuts and to lay out a room before the adhesive comes out. Two sizes: 200 x 300 mm for tiles and 400 x 600 mm for floors.</p>"
 + sec("Use it for", "Marking square cuts on tiles before scoring or sawing", "Checking a room, hob or niche is square before setting out", "Laying out tile lines and measuring off a wall")
 + sec("Features", "Right angle with a long and a short arm", "Two sizes for tile work and floor layout")
 + sec("Specifications", "200 x 300 mm (BP-BS2030)", "400 x 600 mm (BP-BS4060)")
 + sec("Good to know", "Few rooms are truly square. Set your tile lines off the square, not the walls, and let the cuts take up the difference", "Check the square now and then by drawing a line, flipping the square and drawing again", "Keep it clean of adhesive so it sits flat on the tile"),
 ["bat-pro-builders-square-200-x-300mm", "bat-pro-builders-square-400-x-600mm"])

# ---------------- spacers ----------------
def spacer(handle, size, shape, packs, models, use, extra_gtk, slugs, deep=False):
    name = "Deep Tile Crosses" if deep else ("Tile Crosses" if shape == "cross" else "T Shapes")
    intro = {
     "cross": f"<p>BAT Tile Crosses in {size} are plastic cross spacers that hold every grout joint at the same {size} width while the adhesive sets. Sit one at each corner where four tiles meet and the lines stay straight across the whole floor or wall.</p>",
     "deep": f"<p>BAT Deep Tile Crosses in {size} are cross spacers with taller legs than a standard cross. The extra depth keeps them upright in a thick adhesive bed under heavy floor tiles, and gives you something to grab when it is time to pull them out.</p>",
     "tee": f"<p>BAT T Shapes in {size} are T spacers for brick bond, offset and other staggered layouts, where three tiles meet in a T instead of four in a cross. They hold the joint at {size} without a cross leg sticking into the middle of a tile.</p>",
    }[shape]
    return add(handle, intro
     + sec("Use it for", *use)
     + sec("Features", f"{size} joint width", "Plastic, so they do not stain the grout", "Bags for small jobs, buckets for site work")
     + sec("Specifications", f"Joint width: {size}", f"Pack sizes: {packs}", f"Models: {models}")
     + sec("Good to know", "Pull the spacers out before grouting. Spacers left under the grout show through as weak spots and can crack the joint", *extra_gtk),
     [s for s in slugs])

add_spacer = spacer
add_spacer("bat-tile-crosses-1-5mm", "1.5 mm", "cross",
 "bags of 100, 500 (no header card), 2000, 3000, 5000, 10,000, 15,000 and 20,000; buckets of 2000, 3000, 5000, 10,000, 15,000 and 20,000",
 "TC-100, TC-500-ECON, TC-2000, TC-3000, TC-5000, TC-10000, TC-15000, TC-20000, TCB-2000, TCB-3000, TCB-5000, TCB-10000, TCB-15000, TCB-20000",
 ["Rectified porcelain and large format tiles laid with a tight joint", "Wall tiles where a fine grout line is wanted", "Mosaic sheets and feature strips"],
 ["1.5 mm is a tight joint that needs rectified tiles and a flat substrate", "A thick bed? Use the Deep Tile Crosses in 1.5 mm"],
 ["tile-crosses-1-5mm-x-500-bag-no-header-card", "deep-tile-crosses-1-5mm-x-100-bag"])
add_spacer("bat-deep-tile-crosses-1-5mm", "1.5 mm", "deep",
 "bags of 100, 250, 500, 1000, 2000, 5000 and 10,000; buckets of 1000, 2000, 5000, 10,000 and 20,000",
 "TCD-100, TCD-250, TCD-500, TCD-1000, TCD-2000, TCD-5000, TCD-10000, TCDB-1000, TCDB-2000, TCDB-5000, TCDB-10000, TCDB-20000",
 ["Large format and heavy floor tiles on a thick adhesive bed", "Rectified tiles laid with a 1.5 mm joint", "Any job where standard spacers keep sinking into the adhesive"],
 ["1.5 mm is a tight joint that needs rectified tiles and a flat substrate", "For wall tiles on a thin bed the standard BAT Tile Crosses do the same job"],
 ["deep-tile-crosses-1-5mm-x-100-bag", "deep-tile-crosses-1-5mm-x-20000-bucket"], deep=True)
add_spacer("bat-tile-crosses-2mm", "2 mm", "cross",
 "bags of 100, 500, 1000, 2000, 3000, 5000, 10,000 and 20,000; buckets of 1000, 2000, 5000, 10,000 and 20,000",
 "TC2-100, TC2-500, TC2-1000, TC2-2000, TC2-3000, TC2-5000, TC2-10000, TC2-20000, TC2B-1000, TC2B-2000, TC2B-5000, TC2B-10000, TC2B-20000",
 ["Rectified porcelain floor and wall tiles", "Subway and feature wall tiles with a fine grout line", "Most modern bathroom tiling where a 1.5 mm joint is too tight for the tile tolerance"],
 ["2 mm is the common joint for rectified porcelain; non rectified tiles usually need 3 mm", "A thick bed? Use the Deep Tile Crosses in 2 mm"],
 ["tile-crosses-2mm-x-100-bag", "tile-crosses-2mm-x-20000-bucket"])
add_spacer("bat-deep-tile-crosses-2mm", "2 mm", "deep",
 "bags of 500, 1000, 2000, 5000 and 10,000; buckets of 2000, 5000 and 10,000",
 "TC2D-500, TC2D-1000, TC2D-2000, TC2D-5000, TC2D-10000, TC2DB-2000, TC2DB-5000, TC2DB-10000",
 ["Large format and heavy floor tiles on a thick adhesive bed", "Rectified porcelain laid with a 2 mm joint", "Floors where standard spacers sink into the adhesive and are lost"],
 ["2 mm is the common joint for rectified porcelain", "For wall tiles on a thin bed the standard BAT Tile Crosses in 2 mm do the same job"],
 ["deep-tile-crosses-2mm-x-10000-bucket"], deep=True)
add_spacer("bat-tile-crosses-3mm", "3 mm", "cross",
 "bags of 100, 500, 500 (no header card), 1000, 2000, 5000, 10,000 and 15,000; buckets of 2000, 5000, 10,000 and 15,000",
 "TC3-100, TC3-500, TC3-500-ECON, TC3-1000, TC3-2000, TC3-5000, TC3-10000, TC3-15000, TC3B-2000, TC3B-5000, TC3B-10000, TC3B-15000",
 ["Non rectified ceramic floor and wall tiles", "Standard bathroom, kitchen and laundry tiling", "Floors where a slightly wider joint hides small size differences between tiles"],
 ["3 mm is the usual joint for pressed edge (non rectified) tiles, which vary a little in size", "Also made in 1.5, 2, 5 and 10 mm, and as T shapes for brick bond layouts"],
 ["tile-crosses-3mm-x-100-bag", "tile-crosses-3mm-x-15000-bucket"])
add_spacer("bat-tile-crosses-5mm", "5 mm", "cross",
 "bags of 100, 250, 500, 1000, 5000 and 10,000; buckets of 1000, 5000 and 10,000",
 "TC5-100, TC5-250, TC5-500, TC5-1000, TC5-5000, TC5-10000, TC5B-1000, TC5B-5000, TC5B-10000",
 ["Pavers and outdoor tiles", "Rustic, handmade and terracotta tiles that vary in size", "Quarry tiles and other floors where a wide grout line is part of the look"],
 ["Wide joints need a grout rated for the width; check the bag before you buy", "Also made in 1.5, 2, 3 and 10 mm"],
 ["tile-crosses-5mm-x-100-bag", "tile-crosses-5mm-x-10000-bucket"])
add_spacer("bat-tile-crosses-10mm", "10 mm", "cross",
 "bags of 100, 250 and 500; bucket of 500",
 "TC10-100, TC10-250, TC10-500, TC10B-500",
 ["Pavers, slate and outdoor stone", "Crazy paving and random stone where joints are wide", "Any floor where the design calls for a 10 mm grout line"],
 ["A 10 mm joint needs a wide joint grout or a sand and cement mix rated for it", "Also made in 1.5, 2, 3 and 5 mm"],
 ["tile-crosses-10mm-x-100-bag", "tile-crosses-10mm-x-500-bucket"])
add_spacer("bat-t-shapes-1-5mm", "1.5 mm", "tee",
 "bags of 100, 500, 1000, 2000, 5000 and 10,000; buckets of 2000, 5000 and 10,000",
 "TS-100, TS-500, TS-1000, TS-2000, TS-5000, TS-10000, TSB-2000, TSB-5000, TSB-10000",
 ["Brick bond and one third offset layouts in rectified tile", "Subway tiles and plank tiles laid staggered", "Edges and borders where a cross would stick out"],
 ["1.5 mm needs rectified tiles and a flat substrate", "Use BAT Tile Crosses where four tiles meet and T shapes where three meet"],
 ["t-shapes-1-5mm-x-100-bag", "t-shapes-1-5mm-x-10000-bucket"])
add_spacer("bat-t-shapes-2mm", "2 mm", "tee",
 "bags of 500, 1000, 2000, 5000 and 10,000; buckets of 1000, 2000, 5000 and 10,000",
 "TS2-500, TS2-1000, TS2-2000, TS2-5000, TS2-10000, TS2B-1000, TS2B-2000, TS2B-5000, TS2B-10000",
 ["Brick bond and offset layouts in rectified porcelain", "Staggered plank tiles and subway tiles", "Edges and borders where a cross would stick out"],
 ["2 mm is the common joint for rectified porcelain", "Use BAT Tile Crosses where four tiles meet and T shapes where three meet"],
 ["t-shapes-2mm-x-500-bag", "t-shapes-2mm-x-10000-bucket"])
add_spacer("bat-t-shapes-3mm", "3 mm", "tee",
 "bags of 100, 500, 1000, 2000, 5000 and 10,000; buckets of 1000, 2000, 5000 and 10,000",
 "TS3-100, TS3-500, TS3-1000, TS3-2000, TS3-5000, TS3-10000, TS3B-1000, TS3B-2000, TS3B-5000, TS3B-10000",
 ["Brick bond and offset layouts in non rectified ceramic tile", "Staggered subway and plank tiles with a standard joint", "Edges and borders where a cross would stick out"],
 ["3 mm is the usual joint for pressed edge (non rectified) tiles", "Use BAT Tile Crosses where four tiles meet and T shapes where three meet"],
 ["t-shapes-3mm-x-100-bag", "t-shapes-3mm-x-10000-bucket"])

# ---------------- hand tools ----------------
add("bat-dual-wheel-nipper",
 "<p>The BAT Dual Wheel Nipper is a mosaic nipper with two rotating tungsten carbide wheels instead of flat jaws. The wheels score and snap small tiles and glass mosaics cleanly, which is far easier than trying to fit a 20 mm mosaic piece into a bench cutter.</p>"
 + sec("Use it for", "Cutting glass, ceramic and stone mosaic pieces on a sheet", "Trimming small tiles around taps, pipes and corners", "Nibbling curves into tile edges")
 + sec("Features", "Dual rotating tungsten carbide wheels", "Wheels turn to present a fresh edge as they wear", "Hand held, no power or water needed")
 + sec("Specifications", "Model: DWTN", "Replacement wheels: BAT-540SW, the same wheel used on the BAT 540 and 640 tile cutters")
 + sec("Good to know", "Hold the tile so the wheels sit about a third of the way across the piece and squeeze; the tile snaps along the line", "Wear eye protection, as glass mosaic throws sharp chips", "Smooth the cut edge with a diamond hand pad before fixing"),
 ["dual-wheel-nipper"])

add("bat-deluxe-grout-remover-soft-grip",
 "<p>The BAT Deluxe Grout Remover is a hand tool for raking old or stained grout out of joints before regrouting. It comes with two blades: a serrated tooth blade that cuts through cement grout, and a tungsten grit blade that files the joint clean, and a soft grip handle for a job that is hard on the hands.</p>"
 + sec("Use it for", "Removing mouldy or cracked grout in showers before regrouting", "Cleaning out a joint before a repair tile goes in", "Taking down grout haze left high in a joint")
 + sec("What's in the box", "1 x serrated tooth blade", "1 x tungsten grit blade", "Soft grip handle")
 + sec("Specifications", "Model: GR-DLX-SG", "Spare blade set (serrated tooth plus tungsten grit): GR-DLX-SB")
 + sec("Good to know", "Work along the joint with light, repeated strokes rather than digging in; a slip scratches the glaze", "Vacuum the joint out and wipe it damp before new grout goes in", "Epoxy grout is much harder to rake out than cement grout; expect it to take a while"),
 ["deluxe-grout-remover-soft-grip", "deluxe-grout-remover-spare-blade"])

add("bat-side-nipper-single-curved-jaw",
 "<p>The BAT Side Nipper with a single curved jaw is for nibbling curves and notches into tile that a straight cutter cannot make: around a pipe, a toilet flange or a tap. One jaw is straight and one is curved, both tipped in tungsten carbide, and the spring loaded handles open themselves between bites.</p>"
 + sec("Use it for", "Cutting round holes and curves for pipes and wastes", "Nibbling notches for door frames and skirting", "Trimming cut edges that came out a little long")
 + sec("Features", "Offset single curved jaw: 1 x straight and 1 x curved jaw", "Tungsten carbide tipped cutting edges", "Spring loaded handles with soft grip")
 + sec("Specifications", "Model: SN-SCJ")
 + sec("Good to know", "Take small bites from the edge in towards the line; big bites crack the tile", "Score the line first with a tile scriber so the nipper has something to follow", "Wear eye protection and smooth the finished edge with a diamond hand pad"),
 ["side-nipper-single-curved-jaw", "side-nipper-curved-jaw"])

add("bat-pro-folding-utility-knife-with-5-blades-6-pack-counter-display",
 "<p>The BAT Pro Folding Utility Knife is a steel bodied folding knife with a soft grip handle and a belt clip, supplied with five blades. This is the 6 pack: six individually packaged knives in a counter display box, for a crew, a shop counter or anyone who keeps losing knives on site.</p>"
 + sec("Use it for", "Cutting waterproofing membrane, bond breaker and reinforcing fabric", "Trimming backer rod, underlay and packaging", "Opening adhesive bags and silicone cartridges")
 + sec("What's in the box", "6 x BAT Pro folding utility knives, individually packaged", "5 blades with each knife", "Counter display box")
 + sec("Features", "Sturdy steel design", "Soft grip handle", "Belt clip", "Folds closed so the blade is covered in a pocket or tool bag")
 + sec("Specifications", "Model: BP-FKM6", "Takes the 10 piece spare blade set")
 + sec("Good to know", "Change the blade when it starts to drag; a blunt blade is the one that slips", "Keep the pivot clean of adhesive and dust so it folds freely"),
 ["bat-pro-folding-utility-knife-with-5-blades-6-pack-counter-display", "https://adheseal.com.au/products/b-a-t-pro-folding-utility-knife"])

add("bat-professional-knee-pads",
 "<p>The BAT Professional Knee Pads are the flexible concertina style pad that tilers wear all day. The rubber face grips the floor and does not scratch tiles, the soft foam inlay takes the pressure off the knee, and the rubber straps hold them in place when you shuffle along a wall.</p>"
 + sec("Use it for", "Floor tiling, screeding and grouting", "Flooring, waterproofing and any job spent kneeling on hard floors")
 + sec("Features", "Flexible concertina design that bends with the knee", "Rubber face that will not mark tiles", "Soft foam inlay for support", "Rubber straps")
 + sec("Specifications", "Model: KPA", "Spares: buttons (set of 8), foam liners (pair) and rubber straps (set of 4)")
 + sec("Good to know", "Every wearing part is replaceable, so a broken strap or flattened liner does not mean a new pair", "Knock the grit off the rubber face before kneeling on a finished floor", "Hose them off; grout left on the straps makes them brittle"),
 ["professional-knee-pads"])

add("bat-ring-shank-nails-25mm-bucket",
 "<p>BAT Ring Shank Nails are 25 mm nails for fixing fibre cement sheet over an existing timber floor before tiling. The ringed shank bites into the timber and does not work loose the way a smooth nail can, which matters when a tiled floor is riding on top of it. Sold by the bucket in 1, 2.5 and 5 kg.</p>"
 + sec("Use it for", "Nailing cement sheet underlay to timber floors", "Fixing sheet flooring and underlay where screws are too slow")
 + sec("Features", "Ring shank for grip in timber", "25 mm length", "Sold by the bucket")
 + sec("Specifications", "Length: 25 mm", "1 kg bucket, about 720 nails (N25BUCK1)", "2.5 kg bucket, about 1800 nails (N25BUCK25)", "5 kg bucket, about 3600 nails (N25BUCK5)")
 + sec("Good to know", "Follow the sheet maker's nailing pattern, usually a close grid with nails along every edge", "Punch heads flush or just below the surface so they do not show through the adhesive bed", "A 30 mm version is made for thicker sheet"),
 ["ring-shank-nails-25mm-x-1kg-bucket", "ring-shank-nails-25mm-x-5kg-bucket"])

add("bat-floor-scraper-125-x-500mm",
 "<p>The BAT Floor Scraper 125 x 500 mm is the mid size scraper for lifting tiles, vinyl and old adhesive. The 125 mm blade gets under a tile edge, the 500 mm handle gives you two hands and some leverage, and the butt head on the end is made to be hit with a hammer when a tile will not come.</p>"
 + sec("Use it for", "Lifting floor tiles and vinyl during a strip out", "Scraping old adhesive and levelling compound off a slab", "Working behind toilets and in cupboards where a long pole cannot swing")
 + sec("Features", "125 mm replaceable blade", "500 mm handle for grip and leverage", "Butt head for striking with a hammer")
 + sec("Specifications", "Blade width: 125 mm", "Handle length: 500 mm", "Model: FS-125", "Takes the 5 pack of 125 mm replacement blades")
 + sec("Good to know", "Keep the blade angle low so it slides under the tile rather than digging into the slab", "Wear eye protection and gloves; tile shards are sharp", "Swap the blade as soon as it rolls over; a blunt blade is twice the work"),
 ["floor-scraper-125-x-500mm", "https://adheseal.com.au/products/floor-wall-scraper-125mm"])

add("bat-floor-scraper-300mm-x-1300mm",
 "<p>The BAT Floor Scraper 300 x 1300 mm is the stand up scraper for big strip outs. The 300 mm steel blade clears a wide strip of adhesive or vinyl in each pass, and the 1.3 m wooden handle lets you put your weight behind it from standing instead of on your knees.</p>"
 + sec("Use it for", "Stripping vinyl, carpet glue and old adhesive from large floors", "Lifting loose tiles and levelling compound", "Clearing a slab before grinding or screeding")
 + sec("Features", "300 mm wide steel blade, replaceable", "1300 mm wooden handle for stand up work", "Sturdy steel design")
 + sec("Specifications", "Blade width: 300 mm", "Handle length: 1300 mm", "Model: FS-300", "Takes the 300 mm replacement blade")
 + sec("Good to know", "Keep the blade angle low and push in long strokes; chopping at adhesive just bounces", "A blunt blade makes the job twice as hard, so change it when it stops biting", "For tight spots use the 125 x 500 mm or 100 x 300 mm BAT scrapers"),
 ["floor-scraper-300mm-x-1300mm"])

add("bat-short-handled-scraper-100mm-x-300mm",
 "<p>The BAT Short Handled Scraper is the one handed scraper for small jobs and tight spots: a 100 mm blade on a 300 mm handle. It gets into corners, behind pipes and along skirtings where the long handled scrapers cannot reach.</p>"
 + sec("Use it for", "Scraping adhesive and grout off small areas", "Cleaning up around pipes, corners and door frames", "Lifting the odd loose tile or a patch of vinyl")
 + sec("Features", "100 mm replaceable blade", "300 mm handle for one handed control")
 + sec("Specifications", "Blade width: 100 mm", "Handle length: 300 mm", "Model: FS-412", "Takes the 10 pack of 100 mm replacement blades")
 + sec("Good to know", "Keep the blade angle low so it slides under the muck rather than gouging the surface", "Change blades often; small blades blunt quickly on set adhesive", "For whole floors step up to the 125 x 500 mm or 300 x 1300 mm BAT scrapers"),
 ["short-handled-scraper-100mm-x-300mm"])

add("bat-20-ltr-promotional-bucket",
 "<p>The BAT 20 Ltr Bucket is a strong plastic site bucket with the BAT logo on the side. Twenty litres is the size that suits a full bag of adhesive or grout with room to mix, and it doubles as a water bucket, a tool carrier and a seat.</p>"
 + sec("Use it for", "Mixing tile adhesive, grout and levelling compound", "Carrying water for sponges and clean up", "Storing spacers, trowels and small tools between jobs")
 + sec("Features", "Strong plastic construction", "20 litre capacity", "BAT branded")
 + sec("Specifications", "Capacity: 20 litres", "Model: BAT-20LPB", "Snap on lid sold separately")
 + sec("Good to know", "Rinse it out before adhesive sets; set adhesive flakes off into the next mix", "Keep one bucket for adhesive and one for grout so the colours stay clean", "Buy the lid if you want to keep mixed grout or wash water covered between coats"),
 ["Shopify product title and options", "existing description"], False,
 "BAT-20LPB is not listed on battrims.com, adheseal.com.au or stonex.com.au. Written from the title and the existing description plus general bucket use.")

# ---------------- floats ----------------
PU_INTRO = "Polyurethane is lighter than timber or steel and does not soak up water, so the float stays the same weight all day and does not warp."
add("bat-p-u-float-pointed-260-x-80mm",
 f"<p>The BAT P.U. Float Pointed is a 260 x 80 mm polyurethane rendering float with a pointed nose for getting into corners, around pipes and behind fittings where a rectangular float cannot reach. {PU_INTRO}</p>"
 + sec("Use it for", "Finishing render and screed in internal corners", "Working around pipes, brackets and window reveals", "Small patch repairs in render")
 + sec("Features", "Pointed float for hard to reach areas", "Extremely lightweight and durable polyurethane construction", "For smooth finishing of rendered surfaces")
 + sec("Specifications", "Size: 260 x 80 mm", "Model: PPUF-2680")
 + sec("Good to know", "Wait until the render has stiffened enough to take a thumb print before floating, then work in overlapping circles", "Wash the float off before render sets on it", "Pair it with a standard BAT P.U. Float for the open areas"),
 ["p-u-float-pointed-260-x-80mm"])

add("bat-p-u-float",
 f"<p>The BAT P.U. Float is a rectangular polyurethane rendering float in five sizes, from 240 x 120 mm for patching up to 420 x 220 mm for big walls. {PU_INTRO} It leaves a smooth, even finish on render and screed.</p>"
 + sec("Use it for", "Rubbing up render on walls and hobs", "Closing and smoothing sand and cement screed", "Floating levelling and bedding mortar before tiling")
 + sec("Features", "Extremely lightweight and durable polyurethane construction", "For smooth finishing of rendered surfaces", "Five sizes to suit the job and the hand")
 + sec("Specifications", "240 x 120 mm (PUF-2412)", "280 x 140 mm (PUF-2814)", "320 x 180 mm (PUF-3218)", "360 x 200 mm (PUF-3620)", "420 x 220 mm (PUF-4222)")
 + sec("Good to know", "Let the render stiffen before floating; too early and it drags, too late and it will not close", "Work in overlapping circles with light pressure", "Hose the float off before the mix sets on the face", "A pointed version and a Dutch oblong version are also made for corners and detail work"),
 ["p-u-float-240-x-120mm", "p-u-float-420-x-220mm"])

add("bat-p-u-float-dutch-340-x-140-120mm",
 f"<p>The BAT P.U. Float Dutch is a 340 mm polyurethane rendering float with an oblong shape that tapers from 140 mm to 120 mm. The taper lets the narrow end work into corners and around fittings while the wide end still covers open wall. {PU_INTRO}</p>"
 + sec("Use it for", "Rendering and patching around windows, doors and pipes", "Floating hobs, niches and other narrow sections", "General render finishing where one float has to do everything")
 + sec("Features", "Dutch style oblong shape, 140 mm tapering to 120 mm", "Extremely lightweight and durable polyurethane construction", "For smooth finishing of rendered surfaces")
 + sec("Specifications", "Size: 340 x 140/120 mm", "Model: PUFD-3414")
 + sec("Good to know", "Float once the render has stiffened enough to take a thumb print", "Rinse the face before render sets on it", "For big open walls the rectangular BAT P.U. Float in 360 or 420 mm is quicker"),
 ["p-u-float-dutch-340-x-140-120mm"])

# ---------------- floor drains ----------------
DRAIN_GTK_PLUMB = "Floor wastes are fitted by the plumber and the tiler together: the collar goes into the pipe, the waterproofing is dressed into the puddle flange, and the grate finishes flush with the tile"
DRAIN_GTK_FALL = "Screed the floor with fall to the drain so water does not pond on the tile"
DRAIN_GTK_CLEAN = "Wipe grout off the plated finish before it dries; dried grout dulls chrome and marks matt black"
NOTE_DRAIN = "This drain is not listed on battrims.com (only the 100 mm chrome short and ultra short collar drains are). Written from the title, options and the existing description plus general floor waste guidance."

add("bat-chrome-plated-floor-drain-50mm",
 "<p>The BAT Chrome Plated Floor Drain 50mm is a square floor waste grate with a 50 mm outlet, for the smaller waste pipes found in some laundries, balconies and older bathrooms. The square grate sits flush in the tiled floor and comes in chrome plate or matt black to match your tapware.</p>"
 + sec("Use it for", "Bathrooms, laundries and other wet areas with a 50 mm waste pipe", "Replacing a dated round grate with a square one")
 + sec("Features", "Square grate", "Chrome plated or matt black finish", "50 mm outlet")
 + sec("Specifications", "Outlet: 50 mm", "Finishes: Chrome (BAT-SFD50), Matt Black (BAT-SFD50MB)")
 + sec("Fits", "50 mm waste pipes", "Pairs with the BAT Luxe recessed round puddle flange in 80 x 50 mm")
 + sec("Good to know", DRAIN_GTK_PLUMB, DRAIN_GTK_FALL, DRAIN_GTK_CLEAN),
 ["Shopify product title and options", "existing description", "bat-luxe-recessed-round-puddle-flange-80-x-50mm"], False, NOTE_DRAIN)

add("bat-chrome-plated-floor-drain-80mm",
 "<p>The BAT Chrome Plated Floor Drain 80mm is a square floor waste grate with an 80 mm outlet, the size used on many bathroom and laundry wastes. It sits flush in the tiled floor and comes in chrome plate or matt black to match the rest of the room.</p>"
 + sec("Use it for", "Bathroom, shower and laundry floors with an 80 mm waste pipe", "Replacing a worn or dated grate on an existing 80 mm waste")
 + sec("Features", "Square grate", "Chrome plated or matt black finish", "80 mm outlet")
 + sec("Specifications", "Outlet: 80 mm", "Finishes: Chrome (BAT-SFD80), Matt Black (BAT-SFD80MB)")
 + sec("Fits", "80 mm waste pipes", "Pairs with the BAT Luxe recessed round puddle flange in 80 x 80 mm", "For deep floor builds, see the BAT long collar 80 mm drain")
 + sec("Good to know", DRAIN_GTK_PLUMB, DRAIN_GTK_FALL, DRAIN_GTK_CLEAN),
 ["Shopify product title and options", "existing description", "bat-luxe-recessed-round-puddle-flange-80-x-80mm"], False, NOTE_DRAIN)

add("bat-chrome-plated-long-collar-square-floor-drain-80mm",
 "<p>The BAT Chrome Plated Long Collar Square Floor Drain 80mm is the 80 mm square waste for floors with a deep build up. The longer collar reaches down through a thick screed and tile bed to the pipe, where a standard collar would come up short and leave the grate sitting proud.</p>"
 + sec("Use it for", "Bathrooms and laundries where the screed is built up to fall", "Floors over timber or sheet flooring with a thick bedding", "Any 80 mm waste where the standard collar does not reach")
 + sec("Features", "Long collar for deeper floor builds", "Square chrome plated grate", "80 mm outlet")
 + sec("Specifications", "Outlet: 80 mm", "Finish: chrome plated", "Model: BAT-LSFD80")
 + sec("Fits", "80 mm waste pipes", "Pairs with the BAT Luxe recessed round puddle flange in 80 x 80 mm")
 + sec("Good to know", "Measure from finished tile level down to the pipe before choosing between the standard and long collar", DRAIN_GTK_PLUMB, DRAIN_GTK_CLEAN),
 ["Shopify product title and options", "existing description"], False, NOTE_DRAIN)

add("bat-chrome-plated-floor-drain-100mm",
 "<p>The BAT Chrome Plated Floor Drain 100mm is a square chrome plated waste grate for a 100 mm outlet, the common size for shower and bathroom floor wastes. The square grate sits flush in the tiled floor and looks a lot neater than the old round chrome grate it usually replaces.</p>"
 + sec("Use it for", "Shower floors, bathrooms and wet areas with a 100 mm waste", "Replacing a round or corroded grate on an existing 100 mm waste")
 + sec("Features", "Square chrome plated grate", "100 mm outlet")
 + sec("Specifications", "Outlet: 100 mm", "Finish: chrome plated", "Model: BAT-SFD100SH")
 + sec("Fits", "100 mm waste pipes", "Spare PVC collar (BAT-SFDPVCC) available to extend the outlet", "Pairs with the BAT Luxe recessed round puddle flange in 100 x 100 mm")
 + sec("Good to know", "Matt black, ultra short collar and PVC collar versions are also made", DRAIN_GTK_PLUMB, DRAIN_GTK_CLEAN),
 ["chrome-plated-floor-drain-100mm", "pvc-collar-shower-floor-drain"])

add("bat-chrome-plated-floor-drain-100mm-matt-black",
 "<p>The BAT Floor Drain 100mm in matt black is the square 100 mm waste grate finished to match black tapware, shower fittings and accessories. It sits flush in the tiled floor and, on a dark tile, all but disappears.</p>"
 + sec("Use it for", "Shower floors, bathrooms and laundries with a 100 mm waste", "Bathrooms fitted out in matt black tapware")
 + sec("Features", "Square grate", "Matt black finish", "100 mm outlet")
 + sec("Specifications", "Outlet: 100 mm", "Finish: matt black", "Model: BAT-SFD100MB")
 + sec("Fits", "100 mm waste pipes", "Pairs with the BAT Luxe recessed round puddle flange in 100 x 100 mm")
 + sec("Good to know", "Also made in chrome plate, and in an ultra short collar version for shallow floors", DRAIN_GTK_PLUMB, "Clean matt black with a soft cloth and mild detergent; abrasive pads and acid cleaners mark it"),
 ["Shopify product title and options", "existing description"], False, NOTE_DRAIN)

add("bat-chrome-plated-floor-drain-100mm-with-pvc-collar",
 "<p>The BAT Chrome Plated Floor Drain 100mm with PVC Collar is the square 100 mm chrome waste grate supplied with its PVC collar in the box. The collar glues into the waste pipe and the grate sits in it.</p>"
 + sec("Use it for", "Shower, bathroom and laundry floors with a 100 mm waste")
 + sec("What's in the box", "Square chrome plated 100 mm floor drain grate", "PVC collar")
 + sec("Specifications", "Outlet: 100 mm", "Finish: chrome plated", "Model: BAT-SFD100")
 + sec("Fits", "100 mm PVC waste pipes", "Spare PVC collar (BAT-SFDPVCC) sold separately", "Pairs with the BAT Luxe recessed round puddle flange in 100 x 100 mm")
 + sec("Good to know", DRAIN_GTK_PLUMB, DRAIN_GTK_FALL, DRAIN_GTK_CLEAN),
 ["Shopify product title and options", "existing description", "pvc-collar-shower-floor-drain"], False, NOTE_DRAIN)

add("bat-chrome-plated-floor-drain-100mm-ultra-short-collar",
 "<p>The BAT Chrome Plated Floor Drain 100mm Ultra Short Collar is the square 100 mm waste for shallow floors. The very short collar suits a thin screed or a tile laid close to the slab, where a standard collar would hit the pipe fitting before the grate sat flush.</p>"
 + sec("Use it for", "Shower and bathroom floors with little depth between slab and tile", "Renovations where the old waste sits high in the floor")
 + sec("Features", "Ultra short collar", "Square chrome plated grate", "100 mm outlet")
 + sec("Specifications", "Outlet: 100 mm", "Finish: chrome plated", "Model: BAT-SFD100-USC", "Also made in matt black (BAT-SFD100-USCMB)")
 + sec("Fits", "100 mm waste pipes", "Pairs with the BAT Luxe recessed round puddle flange in 100 x 100 mm")
 + sec("Good to know", "Measure from finished tile level to the pipe before choosing between the ultra short, short and long collar drains", DRAIN_GTK_PLUMB, DRAIN_GTK_CLEAN),
 ["chrome-plated-floor-drain-100mm-ultra-short-collar"])

add("bat-stainless-steel-316-tile-insert-floor-drain-110mm",
 "<p>The BAT Stainless Steel Tile Insert Floor Drain is a 110 x 110 mm floor waste with a recessed tray in the top. Cut a piece of your floor tile, bed it into the tray, and the drain all but disappears, leaving a thin stainless line around a square of tile. Marine grade 316 stainless steel will not rust or pit in a shower.</p>"
 + sec("Use it for", "Shower floors where you do not want a chrome grate in the middle of the tile", "Bathrooms and wet rooms in large format or stone tile")
 + sec("Features", "Tile insert tray takes a cut piece of the floor tile", "Water drains through the slot around the insert", "Marine grade 316 stainless steel")
 + sec("Specifications", "Size: 110 x 110 mm", "Material: 316 stainless steel", "Model: BAT-SSFD110")
 + sec("Good to know", "Cut the insert tile a touch smaller than the tray so grout or silicone can seal around it", DRAIN_GTK_PLUMB),
 ["stainless-steel-316-tile-insert-floor-drain-110mm"])

add("bat-chrome-plated-floor-drain-100mm-ultra-short-collar-matt-black",
 "<p>The BAT Floor Drain 100mm Ultra Short Collar in matt black is the square 100 mm waste for shallow floors, finished to match black tapware. The very short collar suits a thin screed or a tile laid close to the slab, where a standard collar would hit the pipe fitting before the grate sat flush.</p>"
 + sec("Use it for", "Shower and bathroom floors with little depth between slab and tile", "Bathrooms fitted out in matt black tapware")
 + sec("Features", "Ultra short collar", "Square grate", "Matt black finish")
 + sec("Specifications", "Outlet: 100 mm", "Finish: matt black", "Model: BAT-SFD100-USCMB", "Also made in chrome plate (BAT-SFD100-USC)")
 + sec("Fits", "100 mm waste pipes", "Pairs with the BAT Luxe recessed round puddle flange in 100 x 100 mm")
 + sec("Good to know", "Measure from finished tile level to the pipe before choosing between the ultra short, short and long collar drains", DRAIN_GTK_PLUMB, "Clean matt black with a soft cloth and mild detergent; abrasive pads and acid cleaners mark it"),
 ["chrome-plated-floor-drain-100mm-ultra-short-collar-matt-black"])

add("bat-pvc-collar-shower-floor-drain",
 "<p>The BAT PVC Collar is the plastic collar that sits between a BAT chrome plated square floor drain and the 100 mm waste pipe. Buy it as a spare when the original collar is cracked or lost, or to extend the outlet so the grate reaches tile level on a deeper floor build.</p>"
 + sec("Use it for", "Replacing a damaged collar on a BAT 100 mm square floor drain", "Extending the drain outlet to suit a thicker screed and tile build", "Fitting a drain bought without a collar")
 + sec("Features", "PVC, solvent welds to standard PVC waste pipe", "Allows for drain outlet extension")
 + sec("Specifications", "Model: BAT-SFDPVCC", "An 80 mm version is also made (BAT-SFDPVCC80)")
 + sec("Fits", "BAT chrome plated square floor drains with a 100 mm outlet that take a PVC collar")
 + sec("Good to know", "Check the collar against the drain before the plumber glues it in; collar only, grate not included", "Use PVC priming fluid and solvent cement to join it to the pipe"),
 ["pvc-collar-shower-floor-drain", "pvc-collar-shower-floor-drain-80mm"])

add("bat-luxe-square-inspection-drain-100mm-outlet",
 "<p>The BAT Luxe Square Inspection Drain is a square floor grate for a 100 mm outlet that is made to come out. Lift the grate and a plumber has access to the waste below the tiled floor to clear a blockage or run a camera, without cutting the tiles. Chrome plated or matt black.</p>"
 + sec("Use it for", "Bathrooms and laundries where the waste needs to stay accessible", "Floors over an inspection opening or a waste that is prone to blocking", "Matching other BAT Luxe drains and grates in the same finish")
 + sec("Features", "Removable square grate for inspection access", "Chrome plated or matt black finish", "100 mm outlet")
 + sec("Specifications", "Outlet: 100 mm", "Finishes: Chrome Plated (BL-SID100), Matt Black (BL-SID100MB)")
 + sec("Fits", "100 mm waste pipes", "Pairs with the BAT Luxe recessed round puddle flange in 100 x 100 mm")
 + sec("Good to know", DRAIN_GTK_PLUMB, DRAIN_GTK_CLEAN),
 ["Shopify product title and options", "existing description"], False,
 "BL-SID100 is not listed on battrims.com or the stockist feeds. Written from the title, options and the existing description plus general floor waste guidance.")

add("bat-luxe-recessed-round-puddle-flange",
 "<p>The BAT Luxe Recessed Round Puddle Flange is the plastic flange that sits under the floor waste and gives the waterproofing membrane something to bond to. The membrane is dressed into the recess and sealed to the flange, so water under the tile is led into the waste, not the slab. Three sizes to suit 50, 80 and 100 mm drains.</p>"
 + sec("Use it for", "Shower and bathroom floors being waterproofed before tiling", "Any floor waste in a wet area that needs the membrane tied in")
 + sec("Features", "Recessed round flange that the membrane laps into", "Plastic, so it will not corrode in the slab")
 + sec("Specifications", "100 x 100 mm, for 100 mm drains (BL-RPF100100R)", "80 x 80 mm, for 80 mm drains (BL-RPF8080R)", "80 x 50 mm, for 50 mm drains (BL-RPF8050R)")
 + sec("Fits", "Sits under the floor waste on the pipe: match the second number to your drain outlet size")
 + sec("Good to know", "Fit the flange before waterproofing, level with or just below the screed", "Follow the membrane maker's instructions for dressing the membrane into the flange and use bond breaker where they call for it", "Puddle flanges are part of the waterproofing system in Australian wet areas"),
 ["bat-luxe-recessed-round-puddle-flange-100-x-100mm", "bat-luxe-recessed-round-puddle-flange-80-x-50mm"])

# ---------------- waterproofing rollers ----------------
ROLLER_FITS = sec("Fits", "230 mm roller covers: set of 3 (BAT-3RRS) or carton of 100 (BAT-SRR100)", "BAT paint roller extension pole 1.2 to 2.4 m (BAT-PREP1200)")
add("bat-heavy-duty-paint-roller-frame-230mm",
 "<p>The BAT Heavy Duty Paint Roller Frame is a 230 mm roller frame built for liquid waterproofing membrane, which is thicker and heavier than paint. A light frame bends and the roller skips; this one holds its shape under the load, so the membrane goes on at an even thickness.</p>"
 + sec("Use it for", "Rolling liquid waterproofing membrane on floors and walls", "Primers, sealers and thick coatings", "Paint, when you want a frame that will last")
 + sec("Features", "Heavy duty construction that will not bend during application", "230 mm width", "Threaded handle for an extension pole")
 + sec("Specifications", "Roller length: 230 mm", "Model: BAT-PRF230HD")
 + ROLLER_FITS
 + sec("Good to know", "Frame only; roller covers are sold separately", "Membrane sets hard on a cover, so budget on a fresh cover for each coat", "Wash the frame before membrane dries on it"),
 ["bat-heavy-duty-paint-roller-frame-230mm"])

add("bat-paint-roller-extension-pole-1-2-2-4m",
 "<p>The BAT Paint Roller Extension Pole extends from 1.2 to 2.4 m and screws onto a threaded roller frame, so you can roll membrane across a floor or up a wall from standing. It also fits the BAT spiked roller used over self levelling compound.</p>"
 + sec("Use it for", "Rolling waterproofing membrane on floors without kneeling in it", "Reaching high walls and ceilings", "Running the BAT spiked roller over levelling compound")
 + sec("Features", "Telescopic, 1.2 to 2.4 m", "Standard threaded end for roller frames", "Can be easily fitted to paint roller frames and the BAT spiked roller")
 + sec("Specifications", "Length: 1.2 to 2.4 m", "Model: BAT-PREP1200")
 + sec("Fits", "Threaded paint roller frames, including the BAT heavy duty 230 mm frame", "BAT spiked roller")
 + sec("Good to know", "Lock the pole at the shortest length that reaches; a fully extended pole flexes and makes it harder to keep the coat even", "Wipe membrane off the thread before it sets or the frame will not come off"),
 ["bat-paint-roller-extension-pole-1-2-2-4m"])

add("bat-paint-roller-and-tray-set",
 "<p>The BAT Paint Roller and Tray Set is the basic kit for rolling on waterproofing membrane, primer or paint: a 230 mm roller frame, one roller cover and a tray to load it from. Open the box and start rolling.</p>"
 + sec("What's in the box", "Paint tray", "230 mm roller frame", "1 x roller cover")
 + sec("Use it for", "Rolling liquid waterproofing membrane in showers, bathrooms and laundries", "Primers and sealers before tiling", "General painting")
 + sec("Specifications", "Roller length: 230 mm", "Model: BAT-PRTS")
 + ROLLER_FITS
 + sec("Good to know", "Membrane sets hard in a roller cover, so buy spare covers if you are doing more than one coat", "A brush for corners is sold separately; the BAT Pro Waterproofing Kit includes one", "Wash the tray and frame before membrane dries on them"),
 ["bat-paint-roller-and-tray-set"])

add("bat-pro-waterproofing-kit",
 "<p>The BAT Pro Waterproofing Kit has everything you need to roll and brush on a liquid waterproofing membrane: a roller frame, two roller covers for two coats, a tray and a brush for the corners and junctions where the roller does not reach. One box, one bathroom.</p>"
 + sec("What's in the box", "230 mm roller frame", "2 x roller covers", "Paint tray", "Brush")
 + sec("Use it for", "Waterproofing shower recesses, bathroom floors and laundries before tiling", "Applying primer and membrane in two coats as the membrane maker specifies")
 + sec("Specifications", "Roller length: 230 mm", "Model: BP-WPK1")
 + ROLLER_FITS
 + sec("Good to know", "Brush the membrane into internal corners and around pipes first, then roll the open areas", "Use a fresh cover for each coat; membrane sets hard in the first one", "Follow the membrane data sheet for coat thickness and drying time between coats"),
 ["bat-pro-waterproofing-kit"])

add("bat-replacement-paint-roller-cover-set-of-3-pcs",
 "<p>The BAT Replacement Paint Roller Cover is a 230 mm roller cover for waterproofing membrane, primer and paint, sold in a set of 3. Membrane sets hard in a cover between coats, so a set of three covers a bathroom: primer, first coat, second coat.</p>"
 + sec("Use it for", "Rolling liquid waterproofing membrane", "Primers, sealers and paint")
 + sec("Features", "230 mm length", "Set of 3")
 + sec("Specifications", "Length: 230 mm", "Pack: 3 covers", "Model: BAT-3RRS")
 + sec("Fits", "230 mm roller frames: BAT heavy duty, Panther, the BAT roller and tray set and the BAT Pro waterproofing kit")
 + sec("Good to know", "Throw the cover out when the coat is done rather than trying to wash membrane out of it", "For a crew doing bathrooms every week there is also a carton of 100 (BAT-SRR100)"),
 ["bat-replacement-paint-roller-cover-set-of-3-pcs"])

add("bat-replacement-roller-cover-set-carton-of-100-pcs",
 "<p>The BAT Replacement Roller Cover carton is 100 of the 230 mm covers used for waterproofing membrane, primer and paint. It is the bulk pack for waterproofers and tiling crews who go through a cover every coat and do not want to run out mid job.</p>"
 + sec("Use it for", "Rolling liquid waterproofing membrane", "Primers, sealers and paint")
 + sec("Features", "230 mm length", "Bulk carton of 100")
 + sec("Specifications", "Length: 230 mm", "Pack: carton of 100 covers", "Model: BAT-SRR100")
 + sec("Fits", "230 mm roller frames: BAT heavy duty, Panther, the BAT roller and tray set and the BAT Pro waterproofing kit")
 + sec("Good to know", "Use a fresh cover for each coat; membrane sets hard in the first one", "Keep the carton dry and off the floor of the van so the covers stay clean", "A set of 3 (BAT-3RRS) suits a single bathroom"),
 ["bat-replacement-roller-cover-set-carton-of-100-pcs"])

# ---------------- BATSEAL silicone tools ----------------
add("batseal-silicone-applicators-set-of-3",
 "<p>The BATSEAL Silicone Applicators are a set of three non-stick finishing tools for tooling off a silicone bead in one pass, with the same profile every time. Choose the 45 degree set for a flat angled fillet from 3 to 10 mm, or the radius set for a concave bead from 4 to 14 mm, with a different radius at each end of each applicator.</p>"
 + sec("Use it for", "Finishing silicone in shower corners, along bath and vanity edges and at floor to wall junctions", "Internal corners between tiles and around windows and splashbacks")
 + sec("Features", "Non-stick, so cured and uncured silicone wipes off", "Three applicators per set covering a range of joint sizes", "Radius set: each applicator has a different radius at either end")
 + sec("Specifications", "45 degree profile, 3 to 10 mm (S A-APP45)", "Radius profile, 4 to 14 mm (S A-APPRAD)")
 + sec("Fits", "Any silicone or sealant bead")
 + sec("Good to know", "Pick the applicator size that matches the joint so the tool rides on both tile faces", "Dip the tool in a smoothing agent such as Maxisil Smoothtex rather than soapy water on natural stone", "Tool matt silicones once only; repeat passes polish them glossy"),
 ["batseal-applicators-set-of-3-45-degree-3-10mm", "batseal-applicators-set-of-3-radius-4-14mm"])

add("batseal-backer-rod-6mm",
 "<p>BATSEAL Backer Rod is a 6 mm closed cell foam rod pressed into a joint before it is sealed. It sets the depth of the bead and stops the sealant bonding to the bottom of the joint, so the silicone sticks to the two sides only and can stretch as the joint moves. Sold in 20 m and 100 m rolls.</p>"
 + sec("Use it for", "Movement joints in tiled floors before silicone or polyurethane sealant", "Deep gaps at floor to wall junctions, bath edges and around hobs", "Filling behind a bead so a cartridge is not wasted filling a cavity")
 + sec("Features", "Closed cell foam, does not soak up water", "6 mm diameter", "Compresses to fit joints a little narrower than 6 mm")
 + sec("Specifications", "Diameter: 6 mm", "Roll lengths: 20 m (S A-BR-20) and 100 m (S A-BR-100)")
 + sec("Fits", "Deep joints before any silicone or sealant")
 + sec("Good to know", "Choose a rod about 25 percent wider than the joint so it stays put", "Push it in with a blunt tool, not a knife; a punctured rod can bubble the sealant", "Sealant depth over the rod is usually about half the joint width; check the sealant data sheet"),
 ["batseal-backer-rod-6mm-x-20m", "batseal-backer-rod-6mm-x-100m"])

GUN_GTK = sec("Good to know", "Cut the nozzle at 45 degrees to a width just under the joint size", "Release the pressure as soon as you stop the bead or the gun keeps pushing sealant out", "Wipe the plunger and frame before silicone cures on them")
add("batseal-caulking-gun-air",
 "<p>The BATSEAL Caulking Gun Air runs off a site compressor and pushes the sealant out with air pressure instead of your hand. Squeeze the trigger and the bead flows at a constant rate, so long runs of silicone come out even and your forearm is not cooked after a day of showers and splashbacks.</p>"
 + sec("Use it for", "High volume silicone work: whole bathrooms, commercial wet areas and expansion joints", "Firm sealants such as polyurethane that are hard work in a hand gun", "Long, consistent beads along floor to wall junctions")
 + sec("Features", "Air fed, with trigger control over flow", "Even bead at a steady speed", "Takes cartridges and sausage packs")
 + sec("Specifications", "Model: S A-CGA", "Air supply: site compressor")
 + sec("Fits", "Standard 300 and 310 ml cartridges, including BATSEAL and Maxisil silicones", "600 ml sausage packs")
 + GUN_GTK,
 ["batseal-caulking-gun-air"])

add("batseal-caulking-gun-professional",
 "<p>The BATSEAL Caulking Gun Professional is a heavy duty hand gun with a complete holding frame for 310 ml cartridges. Built for everyday use, the full frame supports the cartridge along its length so it does not split or kick, and the smooth drive puts out a steady bead with less effort than a skeleton gun.</p>"
 + sec("Use it for", "Silicone in showers, around baths and vanities and along splashbacks", "Acrylic gap filler, polyurethane and construction adhesive in standard cartridges", "Daily use by tilers, plumbers and waterproofers")
 + sec("Features", "Complete heavy duty holding frame", "Smooth, steady drive", "For professional everyday use")
 + sec("Specifications", "Cartridge size: 310 ml", "Model: S A-CGP")
 + sec("Fits", "Standard 300 and 310 ml cartridges, including BATSEAL and Maxisil silicones")
 + GUN_GTK,
 ["batseal-caulking-gun-professional"])

add("batseal-caulking-gun-cartridge-and-sausage",
 "<p>The BATSEAL Caulking Gun Cartridge and Sausage is an aluminium barrel gun with a 600 ml capacity. It takes the foil sausage packs that polyurethane and some silicones come in, and it also takes a standard cartridge, so one gun covers both.</p>"
 + sec("Use it for", "Polyurethane and MS polymer sealants sold in 600 ml sausages", "Movement joints in floors and large tiled areas where a 310 ml cartridge runs out too fast", "Standard 300 and 310 ml silicone cartridges")
 + sec("Features", "Large 600 ml capacity", "Aluminium construction", "Barrel takes foil packed sausages or cartridges")
 + sec("Specifications", "Capacity: 600 ml", "Material: aluminium", "Model: S A-CGT")
 + sec("Fits", "600 ml sausage packs", "Standard 300 and 310 ml cartridges, including BATSEAL and Maxisil silicones")
 + sec("Good to know", "Snip the end off the sausage after it is loaded, then fit the nozzle cap", "Release the pressure when you stop the bead or sealant keeps flowing", "Clean the barrel and plunger before sealant cures in them"),
 ["batseal-caulking-gun-cartridge-and-sausage"])

add("batseal-delta-silicone-joint-cutter",
 "<p>The BATSEAL Delta Silicone Joint Cutter is an angled blade tool for cutting old silicone out of a joint before resealing. The blade reaches in at 45 degrees, so it runs along both faces of the joint and slices the bead free in a strip instead of leaving smears of old silicone behind that new sealant will not stick to.</p>"
 + sec("Use it for", "Stripping old or mouldy silicone from shower, bath and vanity joints", "Cleaning sealant off tile edges without scratching the glaze", "Cutting out failed beads before regrouting or resealing")
 + sec("Features", "45 degree angled cutter", "Replaceable blades")
 + sec("Specifications", "Model: S A-DSJC", "Spare blade set: S A-DSJC-SB")
 + sec("Good to know", "Cut down both sides of the bead, then peel the strip out", "Wipe the joint with a silicone remover or methylated spirits so the new bead bonds", "Dispose of used blades in a sealed container"),
 ["delta-silicone-joint-cutter", "delta-silicone-joint-cutter-spare-blade-set"])

add("batseal-cartridge-nozzle-cutter",
 "<p>The BATSEAL Cartridge and Nozzle Cutter is a two in one tool for getting a silicone cartridge ready to use. One end pierces the foil seal on the cartridge; the other cuts the nozzle to a clean 45 degree angle at the width you want. It replaces the utility knife and the guesswork.</p>"
 + sec("Use it for", "Opening and preparing silicone, acrylic and polyurethane cartridges", "Cutting nozzles to a consistent angle and size for a matching bead every time")
 + sec("Features", "Seal remover at one end", "Angled nozzle cutter at the other", "Works with any standard cartridge")
 + sec("Specifications", "Model: SA-CNC")
 + sec("Fits", "Any silicone cartridge")
 + sec("Good to know", "Cut the nozzle opening a little smaller than the joint; you can always cut more off", "Keep the cutter in the caulking gun bag so it is there when you need it", "Wipe silicone off the blade before it cures"),
 ["batseal-cartridge-nozzle-cutter"])

# ---------------- BATSEAL sealers and cleaners ----------------
SEALER_TEST = "Test on a spare tile or a hidden corner first and check the surface is clean and dry before sealing"
add("batseal-aero-high-porosity-sealer-350gm-aerosol",
 "<p>BATSEAL Aero is a penetrating sealer for porous stone and grout in a 350 g aerosol. Spray it on, let it soak in and wipe off the excess: no roller, no tray and no clean up, which makes it the easy way to seal a small area or re-seal grout lines in an existing bathroom.</p>"
 + sec("Use it for", "Sealing grout lines after they have cured", "Limestone, sandstone, terracotta and slate", "Concrete and brick", "Small areas and touch ups where a tin of sealer is overkill")
 + sec("Features", "Penetrating sealer that soaks into the surface rather than sitting on top", "Long lasting protection", "Aerosol application")
 + sec("Specifications", "Size: 350 g aerosol", "Model: BC-A350", "Part of the BATSEAL Pro range")
 + sec("Good to know", "Let new grout cure before sealing; check the grout bag for the waiting time", "Spray in a well ventilated room and wipe up any sealer left on the surface before it dries", SEALER_TEST, "For whole floors the same sealer comes as BATSEAL HPS in 1 and 4 litre tins"),
 ["batseal-aero-high-porosity-sealer-350gm-aerosol"])

add("batseal-hps-high-porosity-sealer",
 "<p>BATSEAL HPS is a solvent based penetrating sealer for porous stone and grout. It soaks into the surface and gives excellent protection against both water based and oil based stains, without changing the look of the stone or leaving a film to wear off. In 1 and 4 litre tins.</p>"
 + sec("Use it for", "Grout", "Sandstone, limestone, terracotta and slate", "Concrete and brick", "Porous stone floors, splashbacks and outdoor paving")
 + sec("Features", "Solvent based penetrating sealer", "Protects against water and oil based stains", "Natural look finish")
 + sec("Specifications", "Sizes: 1 litre (BC-HPS1) and 4 litre (BC-HPS4)", "Part of the BATSEAL Pro range")
 + sec("Good to know", "For dense surfaces such as porcelain, marble and granite use BATSEAL LPS instead", "Apply with a lambswool applicator, brush or roller and wipe off any excess before it dries; dried excess leaves a sheen", "Work in a ventilated area away from flames, and keep the room clear while it cures", SEALER_TEST),
 ["batseal-hps-high-porosity-sealer-1l-liquid", "batseal-hps-high-porosity-sealer-4l-liquid"])

add("batseal-lps-low-porosity-sealer",
 "<p>BATSEAL LPS is a solvent based penetrating sealer made for dense, low porosity surfaces: porcelain, marble, granite, bluestone and terrazzo. These take in very little liquid, so a general sealer sits on top and streaks. LPS is formulated to get into the tight pores and protect against water and oil based stains without changing the look of the surface. In 1 and 4 litre tins.</p>"
 + sec("Use it for", "Polished and honed porcelain", "Marble, granite and bluestone", "Terrazzo", "Grout on dense tile floors")
 + sec("Features", "Solvent based penetrating sealer for dense surfaces", "Protects grout, tile and stone against water and oil based stains", "Natural look finish")
 + sec("Specifications", "Sizes: 1 litre (BC-LPS1) and 4 litre (BC-LPS4)", "Part of the BATSEAL Pro range")
 + sec("Good to know", "For porous stone, terracotta and brick use BATSEAL HPS instead", "Apply thinly and buff off all excess before it dries; dense surfaces hold very little, so a thin coat is correct", "Work in a ventilated area away from flames", SEALER_TEST),
 ["batseal-lps-low-porosity-sealer-1l-liquid", "batseal-lps-low-porosity-sealer-4l-liquid"])

add("batseal-mpc-multi-purpose-cleaner",
 "<p>BATSEAL MPC is an industrial strength, water based cleaner for grout, tiles, floors and hard surfaces. It shifts grease, grime, dirt and general building muck without acid or solvent, so it is safe on sealed stone and is the everyday cleaner to reach for before and after tiling. Low foaming, eco friendly, in 1 and 5 litre bottles.</p>"
 + sec("Use it for", "Cleaning floors before tiling and before sealing", "Lifting grime out of grout lines", "Kitchen, bathroom and laundry tiles", "General hard surface cleaning on site and at home")
 + sec("Features", "Heavy duty, industrial strength cleaner", "Water based, eco friendly and low foaming", "Removes grease, grime, dirt and other contaminants")
 + sec("Specifications", "Sizes: 1 litre (BC-MPC1) and 5 litre (BC-MPC5)", "Part of the BAT Eco range")
 + sec("Good to know", "Dilute for routine cleaning, use neat on heavy grease; follow the label", "Rinse with clean water and let the surface dry fully before sealing", "For cement haze and efflorescence use an acid based cleaner such as BATSEAL De-Scale instead"),
 ["batseal-mpc-multi-purpose-cleaner-1l-liquid", "batseal-mpc-multi-purpose-cleaner-5l-liquid"])

NOTE_SEALER = "Not listed on battrims.com or the stockist feeds. Written from the title, options and the existing description plus general guidance for this product type; no coverage or drying figures given."
add("batseal-de-scale-phosphoric-acid-cleaner",
 "<p>BATSEAL De-Scale is a phosphoric acid cleaner for the mess that cement leaves behind: grout haze, efflorescence, lime scale and mineral deposits on acid resistant tiles and grout. It is the after tiling clean that takes a floor from dull and cloudy to the finish you laid. In 1 and 4 litre bottles.</p>"
 + sec("Use it for", "Removing cement and grout haze after installation", "Efflorescence (white salts) on tiles, pavers and grout", "Lime scale and mineral deposits in showers and laundries", "Cleaning tiles before sealing")
 + sec("Features", "Phosphoric acid based, milder than hydrochloric acid cleaners", "Works on acid resistant tiles and cement grout")
 + sec("Specifications", "Sizes: 1 litre (BC-DSC1) and 4 litre (BC-DSC4)")
 + sec("Good to know", "Not for marble, limestone, travertine or other acid sensitive stone; it will etch them", "Test on a small hidden area first", "Wet the floor before applying so the acid works on the haze and not the grout, then rinse well with clean water", "Wear gloves and eye protection and ventilate the room"),
 ["Shopify product title and options", "existing description"], False, NOTE_SEALER)

add("batseal-matt-look-solvent-based-sealer",
 "<p>BATSEAL Matt Look is a solvent based topical sealer that leaves a natural, low sheen finish. It protects concrete, pavers, brick and natural stone from stains and weathering, indoors and out, without the shine of a wet look sealer. In 1, 4 and 20 litre tins.</p>"
 + sec("Use it for", "Outdoor pavers, paths and alfresco areas", "Concrete floors and exposed slabs", "Brick and natural stone where you want protection but not gloss")
 + sec("Features", "Solvent based topical sealer", "Natural matt finish", "Protects against stains and weathering")
 + sec("Specifications", "Sizes: 1 litre (BC-SML1), 4 litre (BC-SML4) and 20 litre (BC-SML20)", "Thin and clean up with BATSEAL Eversol solvent")
 + sec("Good to know", "A topical sealer sits on the surface, so it wears with traffic and will need recoating in time", "Surfaces must be clean, dry and free of efflorescence before sealing", "Work in a ventilated area away from flames and keep the area clear while it cures", SEALER_TEST),
 ["Shopify product title and options", "existing description"], False, NOTE_SEALER)

add("batseal-silcopel-solvent-based-sealer",
 "<p>BATSEAL Silcopel is a solvent based siloxane water repellent for porous masonry. It soaks into render, brick and stone and lines the pores so water beads off, while the surface keeps its natural look and still breathes. In 1 and 4 litre tins.</p>"
 + sec("Use it for", "Rendered and bagged walls", "Face brick and blockwork", "Sandstone, limestone and other porous stone", "Retaining walls and garden walls that stay damp")
 + sec("Features", "Solvent based siloxane", "Penetrates porous masonry rather than forming a film", "Repels water without changing the look of the surface")
 + sec("Specifications", "Sizes: 1 litre (BC-SPELSB1) and 4 litre (BC-SPELSB4)", "Thin and clean up with BATSEAL Eversol solvent")
 + sec("Good to know", "It is a water repellent, not a stain sealer; for oil and stain protection on stone use BATSEAL HPS", "Surfaces must be clean and dry; let new render cure first", "Work in a ventilated area away from flames", SEALER_TEST),
 ["Shopify product title and options", "existing description"], False, NOTE_SEALER)

add("batseal-wet-look-solvent-based-sealer",
 "<p>BATSEAL Wet Look is a solvent based topical sealer that deepens the colour of concrete, pavers, exposed aggregate and natural stone and leaves a rich, glossy wet look finish. It is the sealer for a driveway or pool surround you want to look freshly hosed all year. In 1, 4 and 20 litre tins.</p>"
 + sec("Use it for", "Exposed aggregate and coloured concrete driveways", "Pavers, paths and pool surrounds", "Natural stone where you want the colour brought out")
 + sec("Features", "Solvent based topical sealer", "Enhances colour and leaves a wet look gloss", "Protects against stains and weathering")
 + sec("Specifications", "Sizes: 1 litre (BC-SWL1), 4 litre (BC-SWL4) and 20 litre (BC-SWL20)", "Thin and clean up with BATSEAL Eversol solvent")
 + sec("Good to know", "A gloss topical sealer can be slippery when wet; consider an anti slip additive around pools and on ramps", "A topical sealer wears with traffic and will need recoating in time", "Surfaces must be clean, dry and free of efflorescence; work in a ventilated area away from flames", SEALER_TEST),
 ["Shopify product title and options", "existing description"], False, NOTE_SEALER)

add("batseal-pristine-water-based-sealer-1-ltr",
 "<p>BATSEAL Pristine is a water based penetrating sealer for tile, grout and natural stone. It has low odour and cleans up with water, so it suits sealing indoors in a finished bathroom, kitchen or living room where a solvent sealer would clear the house. 1 litre bottle.</p>"
 + sec("Use it for", "Sealing grout lines in bathrooms, kitchens and laundries", "Natural stone floors, benchtops and splashbacks indoors", "Porous tile and stone in living areas")
 + sec("Features", "Water based penetrating sealer", "Low odour", "Easy clean up with water")
 + sec("Specifications", "Size: 1 litre", "Model: BC-PRISWB1")
 + sec("Good to know", "Let new grout cure before sealing; check the grout bag for the waiting time", "Apply thinly and wipe off any excess before it dries", "Test on a small hidden area first", "For outdoor and heavy duty stone sealing the solvent based BATSEAL HPS and LPS give stronger stain protection"),
 ["Shopify product title and options", "existing description"], False, NOTE_SEALER)

add("batseal-eversol-solvent",
 "<p>BATSEAL Eversol is the solvent that goes with the BATSEAL solvent based sealers. Use it to thin Matt Look, Wet Look and Silcopel for the first coat on a very porous surface, and to clean rollers, brushes and sprayers before the sealer sets in them. In 1 and 4 litre tins.</p>"
 + sec("Use it for", "Thinning BATSEAL Matt Look, Wet Look and Silcopel sealers", "Cleaning rollers, brushes and sprayers after sealing", "Wiping up sealer drips and overspray before they cure")
 + sec("Features", "Matched to the BATSEAL solvent based sealers", "Clean up and thinning in one tin")
 + sec("Specifications", "Sizes: 1 litre (BC-EVSOL1) and 4 litre (BC-EVSOL4)")
 + sec("Fits", "BATSEAL Matt Look, Wet Look and Silcopel solvent based sealers")
 + sec("Good to know", "Flammable: use in a ventilated area away from flames and sparks, and store with the lid tight", "Follow the sealer label for how much to thin; too much solvent weakens the coat", "Not for water based sealers such as BATSEAL Pristine, which clean up with water"),
 ["Shopify product title and options", "existing description"], False, NOTE_SEALER)

# ---------------- flooring cutter ----------------
add("bat-pro-laminate-and-vinyl-flooring-cutter",
 "<p>The BAT Pro Laminate and Vinyl Flooring Cutter is a guillotine for plank flooring. Set the plank, pull the handle and the board is cut square: no saw, no dust and no noise, so you can cut inside the room you are laying instead of walking to a saw bench outside. It cuts material up to 12 mm thick and the blade never needs sharpening.</p>"
 + sec("Use it for", "Laminate flooring", "Vinyl plank and hybrid flooring", "End cuts at walls and doorways while laying")
 + sec("Features", "Fast, clean, precise cuts", "No dust and no noise, so it can be used in occupied homes and apartments", "Blade never needs sharpening")
 + sec("Specifications", "Cutting capacity: material up to 12 mm thick", "Model: BP-LVFC")
 + sec("Good to know", "Mark the cut line on the face and cut with the decorative face up for the cleanest edge", "Guillotine cutters make straight cuts; use a jigsaw for notches around pipes and door frames", "Check your plank thickness and width against the 12 mm capacity before buying"),
 ["bat-pro-laminate-and-vinyl-flooring-cutter"])

json.dump(R, open(OUT, "w"), indent=1, ensure_ascii=False)
print(len(R), "records;", [(r["handle"][:30], r["words"]) for r in R if not 90 <= r["words"] <= 200])
