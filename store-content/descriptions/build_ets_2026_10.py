"""Build ets-bathroomware-hardware-2026-10-24.json from hand-written descriptions."""
import json, re, sys

ROOT = "/home/user/Excellent-Tiling-Services-/store-content"
todo = json.load(open(f"{ROOT}/descriptions/todo-ets-bathroomware-hardware.json"))
sup = {p["title"]: p for p in json.load(open(f"{ROOT}/supplier-sync/dsa-bathroomware-2026-10-14.json"))}
CDN = "https://cdn.shopify.com/s/files/1/0827/3235/1706/files/"
SUP = "store-content/supplier-sync/dsa-bathroomware-2026-10-14.json"

FIN = "<li>Finish: Chrome or Brushed Nickel</li>"
CEL = "Part of the Celine range, so it matches the Celine mixers, showers and accessories in the same finish."
CHL = "Part of the Chloe range, so it matches the Chloe showers and hand pieces in the same finish."
BASIN_GTK = ("<h3>Good to know</h3><ul><li>Takes a standard 32mm basin waste (not included); a pop-up waste in the same "
             "finish as your mixer is the usual pick</li><li>Vitreous china is fired hard and glazed, so it wipes clean "
             "with a soft cloth and non-abrasive cleaner</li><li>Check the dimensions against your vanity top or "
             "wall before you order</li></ul>")

D = {}  # handle -> (html, sources, verified, notes)

def add(handle, html, sources, verified, notes=""):
    D[handle] = (html, sources, verified, notes)

# ---------------- Showers and shower parts ----------------
add("chloe-round-shower-rose-250mm",
    "<p>The Chloe Round Shower Rose is a 250mm slimline overhead rose for a wide, even rain-style spray. It screws onto "
    "any standard half-inch shower arm, so it suits a new install or a quick upgrade of an older, smaller rose.</p>"
    "<h3>Use it for</h3><ul><li>Overhead showers on a wall-mounted or ceiling arm</li><li>Replacing a small or "
    "dated rose without touching the plumbing</li></ul>"
    "<h3>Specifications</h3><ul><li>Diameter: 250mm</li><li>Face plate: 2mm thick, 45mm overall height including the "
    "connector</li><li>Connection: G1/2 (standard half-inch thread)</li>" + FIN +
    "<li>Model: KSR110</li></ul>"
    "<h3>Good to know</h3><ul><li>Shower arm not included; pair it with the Celine Wall Mounted Shower Arm</li>"
    "<li>Wipe the face with a soft cloth to keep the nozzles clear</li><li>" + CHL + "</li></ul>",
    [SUP, CDN + "KSR110-size.jpg"], True, "Dimensions from supplier size diagram.")

add("celine-square-shower-rose-250mm",
    "<p>The Celine Square Shower Rose is a 250 x 250mm slimline overhead rose, only 8mm thick, for a wide rain-style "
    "spray with a clean square look. It fits a standard half-inch shower arm.</p>"
    "<h3>Use it for</h3><ul><li>Overhead showers with square-profile tapware</li><li>Upgrading an existing rose "
    "without re-plumbing</li></ul>"
    "<h3>Specifications</h3><ul><li>Size: 250 x 250 x 8mm</li><li>Connection: standard half-inch (G1/2) shower "
    "arm thread</li>" + FIN + "<li>Model: KSS110</li></ul>"
    "<h3>Good to know</h3><ul><li>Shower arm not included; the Celine Wall Mounted Shower Arm has the matching square "
    "profile</li><li>Rub the soft nozzles with your thumb now and then to clear any build-up</li><li>" + CEL +
    "</li></ul>",
    [SUP, CDN + "KSS110.CR.jpg"], False, "Size from existing description; no diagram online.")

add("celine-wall-mounted-shower-arm",
    "<p>The Celine Wall Mounted Shower Arm is a square-profile gooseneck arm that brings an overhead rose out and "
    "up from the wall, with a square wall flange to cover the pipe entry. Pair it with a Celine or Chloe 250mm rose "
    "for a full overhead shower.</p>"
    "<h3>Use it for</h3><ul><li>Overhead showers where the water comes out of the wall rather than the ceiling</li>"
    "<li>Getting extra height from a rose in a shower with a low outlet</li></ul>"
    "<h3>Specifications</h3><ul><li>Style: square gooseneck arm with square wall flange</li>"
    "<li>Rose connection: standard half-inch (G1/2) thread</li>" + FIN + "<li>Model: SRQ07LF</li></ul>"
    "<h3>Good to know</h3><ul><li>Shower rose sold separately</li><li>Use thread tape on the wall connection and "
    "check for drips before closing up tiles</li><li>" + CEL + "</li></ul>",
    [SUP, CDN + "DSASRQ07LF.CR.png"], False, "No dimensions available; photo only.")

add("celine-round-hand-shower-piece",
    "<p>The Celine Round Hand Shower Piece is a replacement hand shower with a 120mm round face and a push-button "
    "spray selector on the handle. It screws onto any standard half-inch shower hose, so you can swap a worn hand "
    "piece without changing the rail or hose.</p>"
    "<h3>Use it for</h3><ul><li>Replacing the hand piece on a rail shower or twin shower</li>"
    "<li>Matching an existing Celine set when one part needs replacing</li></ul>"
    "<h3>Specifications</h3><ul><li>Face: 120mm diameter</li><li>Length: 262mm</li><li>Depth: 42mm</li>"
    "<li>Spray: multi-function, push-button change on the handle</li><li>Connection: standard half-inch hose "
    "thread</li>" + FIN + "<li>Model: HR002M4</li></ul>"
    "<h3>Good to know</h3><ul><li>Hose and bracket not included</li><li>Rub the soft nozzles to clear scale</li>"
    "<li>" + CEL + "</li></ul>",
    [SUP, CDN + "HR002M4-size_1.jpg"], True, "Dimensions from supplier size diagram.")

add("celine-square-hand-shower-piece",
    "<p>The Celine Square Hand Shower Piece is a replacement hand shower with a 78mm wide square face and a "
    "push-button spray selector on the handle. It fits any standard half-inch shower hose, so a tired hand piece "
    "can be swapped in minutes.</p>"
    "<h3>Use it for</h3><ul><li>Replacing the hand piece on a rail shower or twin shower</li>"
    "<li>Matching square-profile tapware</li></ul>"
    "<h3>Specifications</h3><ul><li>Face: 78mm wide</li><li>Length: 262mm</li><li>Depth: 42mm</li>"
    "<li>Spray: multi-function, push-button change on the handle</li><li>Connection: standard half-inch hose "
    "thread</li>" + FIN + "<li>Model: HS002M4</li></ul>"
    "<h3>Good to know</h3><ul><li>Hose and bracket not included</li><li>Rub the soft nozzles to clear scale</li>"
    "<li>" + CEL + "</li></ul>",
    [SUP, CDN + "HS002M4-size.jpg"], True, "Dimensions from supplier size diagram.")

add("celine-hand-shower-on-bracket",
    "<p>The Celine Hand Shower on Bracket is a square hand shower, flexible hose and fixed wall bracket in one kit. "
    "Lift the hand piece off to rinse down the shower or wash kids and pets, or leave it in the bracket for a normal "
    "wall shower. The spray pattern changes with a push button on the handle.</p>"
    "<h3>Use it for</h3><ul><li>Showers where a full rail is not needed</li><li>A second outlet off a diverter mixer</li>"
    "<li>Replacing a fixed wall shower without re-tiling</li></ul>"
    "<h3>Specifications</h3><ul><li>Hand piece: 78mm wide square face, 262mm long, 42mm deep</li>"
    "<li>Spray: multi-function, push-button change on the handle</li><li>Connection: standard half-inch</li>" + FIN +
    "<li>Model: S028</li></ul>"
    "<h3>What's in the box</h3><ul><li>Hand shower, flexible hose and wall bracket with elbow outlet</li></ul>"
    "<h3>Good to know</h3><ul><li>Needs a half-inch wall outlet at the bracket position</li><li>" + CEL + "</li></ul>",
    [SUP, CDN + "HS002M4-size_f14a1c70-977d-4144-8ddd-2b13eed6cfdd.jpg"], True,
    "Hand piece dimensions from supplier diagram; hose length not shown so left out.")

add("chloe-hand-shower-on-bracket",
    "<p>The Chloe Hand Shower on Bracket is a round hand shower, flexible hose and fixed wall bracket in one kit. "
    "Lift the hand piece off to rinse the screen or wash the dog, or leave it in the bracket as a normal wall shower. "
    "A push button on the handle changes the spray pattern.</p>"
    "<h3>Use it for</h3><ul><li>Showers where a full rail is not needed</li><li>A second outlet off a diverter "
    "mixer</li><li>Replacing a fixed wall shower without re-tiling</li></ul>"
    "<h3>Specifications</h3><ul><li>Hand piece: 120mm round face, 262mm long, 42mm deep</li>"
    "<li>Spray: multi-function, push-button change on the handle</li><li>Connection: standard half-inch</li>" + FIN +
    "<li>Model: S027</li></ul>"
    "<h3>What's in the box</h3><ul><li>Hand shower, flexible hose and wall bracket with elbow outlet</li></ul>"
    "<h3>Good to know</h3><ul><li>Needs a half-inch wall outlet at the bracket position</li><li>" + CHL + "</li></ul>",
    [SUP, CDN + "HR002M4-size_1_571a6228-b903-49fc-9797-d314f6caf6c6.jpg"], True,
    "Hand piece dimensions from supplier diagram; hose length not shown so left out.")

add("celine-rail-shower",
    "<p>The Celine Rail Shower puts a square hand shower on a 700mm vertical rail, so the height and angle of the "
    "spray can be set for each person in the house. The hand piece lifts off for rinsing the shower or washing kids "
    "and pets, and a push button on the handle changes the spray pattern.</p>"
    "<h3>Use it for</h3><ul><li>Family bathrooms where users are different heights</li><li>Renovations where the "
    "wall outlet stays in the same spot</li></ul>"
    "<h3>Specifications</h3><ul><li>Rail: 700mm long, 30mm wide, with adjustable slider and 130mm soap dish</li>"
    "<li>Hand piece: 78mm wide square face, 262mm long, 42mm deep</li><li>Hose: 1500mm</li>"
    "<li>Wall elbow: 42 x 40mm with half-inch (G1/2) connection</li>" + FIN + "<li>Model: H614</li></ul>"
    "<h3>What's in the box</h3><ul><li>Rail with slider and soap dish, hand shower, 1500mm hose, wall elbow</li></ul>"
    "<h3>Good to know</h3><ul><li>Needs a half-inch wall outlet; the elbow covers the pipe entry</li><li>" + CEL +
    "</li></ul>",
    [SUP, CDN + "Picture1.png", CDN + "HS002M4-size_f09bc595-5bc5-41a7-9832-734d8836036c.jpg"], True,
    "Rail, hose and elbow dimensions from supplier diagram.")

add("celine-twin-rail-shower",
    "<p>The Celine Twin Rail Shower gives you a 200mm square overhead rose and a square hand shower on a slide rail, "
    "both fed from one wall outlet. Switch between them at the diverter on the rail, so a single set of plumbing "
    "does the job of two showers.</p>"
    "<h3>Use it for</h3><ul><li>Main bathrooms and ensuites that want an overhead rose plus a hand shower</li>"
    "<li>Renovations where only one wall outlet exists</li></ul>"
    "<h3>Specifications</h3><ul><li>Overhead rose: 200 x 200mm square, half-inch connection</li>"
    "<li>Rail: 910mm overall height, 30mm wide, arm reaches 360mm from the rail</li>"
    "<li>Hand piece: 78mm wide square face, 262mm long, on an adjustable slider</li><li>Hose: 1500mm</li>" + FIN +
    "<li>Model: S7121</li></ul>"
    "<h3>What's in the box</h3><ul><li>Rail with overhead arm and rose, hand shower, 1500mm hose, wall fittings</li></ul>"
    "<h3>Good to know</h3><ul><li>Works off a standard shower mixer; a diverter mixer is not needed</li><li>" + CEL +
    "</li></ul>",
    [SUP, CDN + "ETS7121.CR_1.png"], True, "Dimensions from supplier size diagram.")

add("chloe-twin-rail-shower",
    "<p>The Chloe Twin Rail Shower combines a round overhead rose with a round hand shower on a slide rail, both "
    "fed from one wall outlet. A diverter on the rail switches between the two, so you get a rain-style overhead "
    "and an adjustable hand shower from a single set of plumbing.</p>"
    "<h3>Use it for</h3><ul><li>Main bathrooms and ensuites that want both an overhead and a hand shower</li>"
    "<li>Renovations where only one wall outlet exists</li></ul>"
    "<h3>Specifications</h3><ul><li>Overhead rose: 200mm round, half-inch connection</li>"
    "<li>Hand piece: 120mm round face, 262mm long, multi-function spray, on an adjustable slider</li>"
    "<li>Rail: round profile with top-mounted overhead arm</li>" + FIN + "<li>Model: S4902A</li></ul>"
    "<h3>What's in the box</h3><ul><li>Rail with overhead arm and rose, hand shower, hose, wall fittings</li></ul>"
    "<h3>Good to know</h3><ul><li>Works off a standard shower mixer; a diverter mixer is not needed</li><li>" + CHL +
    "</li></ul>",
    [SUP, CDN + "HR002M4C-KSR108-S4902.CR.jpg", CDN + "HR002M4C-KSR108-S703-SIZE_1.jpg"], True,
    "Rose and hand piece sizes taken from the shared KSR108 / HR002M4 component codes in the supplier image names "
    "(same parts as the Chloe Compact Twin Shower diagram). Rail height not shown so left out.")

add("chloe-compact-twin-shower",
    "<p>The Chloe Compact Twin Shower pairs a 200mm round overhead rose with a round hand shower in a fixed bracket, "
    "both off one wall outlet. With no long rail it suits tight showers and lower ceilings while still giving a "
    "rain-style overhead and a hand piece for rinsing.</p>"
    "<h3>Use it for</h3><ul><li>Small showers and ensuites</li><li>Upgrading a single wall shower to overhead plus "
    "hand shower without a second outlet</li></ul>"
    "<h3>Specifications</h3><ul><li>Overhead rose: 200mm round, 2mm face, 45mm overall height</li>"
    "<li>Arm: 370mm reach, 375mm high, 25mm diameter, 85mm wall plate</li>"
    "<li>Hand piece: 120mm round face, 262mm long, multi-function spray</li><li>Hose: 1500mm</li>"
    "<li>Connections: half-inch (G1/2) at the wall and the rose</li>" + FIN + "<li>Model: S703</li></ul>"
    "<h3>What's in the box</h3><ul><li>Wall arm with diverter, overhead rose, hand shower, 1500mm hose, bracket</li></ul>"
    "<h3>Good to know</h3><ul><li>Works off a standard shower mixer</li><li>" + CHL + "</li></ul>",
    [SUP, CDN + "HR002M4C-KSR108-S703-SIZE_1.jpg"], True, "Dimensions from supplier size diagram.")

# ---------------- Mixers and spouts ----------------
add("celine-basin-mixer",
    "<p>The Celine Basin Mixer is a single-lever basin tap with a flat paddle handle and a body that mixes soft "
    "curves with sharp edges. At 164mm high it suits inset, semi-inset and undermount basins, and the lever runs "
    "hot to cold in one easy sweep.</p>"
    "<h3>Use it for</h3><ul><li>Vanity basins with a tap hole in the basin or benchtop</li><li>Powder rooms and "
    "ensuites where a compact tap is wanted</li></ul>"
    "<h3>Specifications</h3><ul><li>Height: 164mm</li><li>Spout reach: 120mm, spout outlet 113mm above the bench</li>"
    "<li>Base: 50mm diameter</li><li>Connection: flexible hoses supplied</li>" + FIN + "<li>Model: HD7020</li></ul>"
    "<h3>Good to know</h3><ul><li>For above-counter basins use the Celine Tall Basin Mixer instead</li>"
    "<li>Pair with a Celine pop-up waste in the same finish</li><li>Wipe with a soft damp cloth; skip abrasive "
    "cleaners on the finish</li></ul>",
    [SUP, CDN + "ETHD7020_1.png"], True, "Dimensions from supplier size diagram.")

add("celine-tall-basin-mixer",
    "<p>The Celine Tall Basin Mixer is the high-rise version of the Celine basin tap, with the spout 250mm above the "
    "bench so it clears an above-counter basin. Same flat paddle lever and mix of curves and angles as the rest of "
    "the range.</p>"
    "<h3>Use it for</h3><ul><li>Above-counter (vessel) basins on a stone or timber top</li><li>Matching the Celine "
    "range across a bathroom</li></ul>"
    "<h3>Specifications</h3><ul><li>Height: 268mm overall, spout outlet 250mm above the bench</li>"
    "<li>Spout reach: 168mm (200mm to the tip of the lever)</li><li>Base: 50mm diameter</li>" + FIN +
    "<li>Model: HD7021</li></ul>"
    "<h3>Good to know</h3><ul><li>Check that the spout reach lands over the centre of your basin; most 400 to 500mm "
    "basins suit it</li><li>Pair with a Celine pop-up waste in the same finish</li><li>Wipe with a soft damp cloth; "
    "skip abrasive cleaners on the finish</li></ul>",
    [SUP, CDN + "hd7021_1_a0247450-685d-4a70-a5b3-eb9ad6648d79.jpg"], True, "Dimensions from supplier size diagram.")

add("celine-wall-basin-bath-mixer-with-spout",
    "<p>The Celine Wall Basin / Bath Mixer with Spout puts the lever and spout on one slim plate, so the tap sits on "
    "the wall and leaves the basin or bath hob clear. One set works for a wall-hung basin, a built-in bath or a "
    "freestanding bath against the wall.</p>"
    "<h3>Use it for</h3><ul><li>Wall-hung and above-counter basins with no tap hole</li><li>Bath fillers on a tiled "
    "hob or wall</li></ul>"
    "<h3>Specifications</h3><ul><li>Plate: 200 x 75mm</li><li>Spout: 180mm reach</li><li>Lever to spout centres: "
    "119.5mm</li><li>Operation: single lever, in-wall mixer body</li>" + FIN + "<li>Model: HD7025</li></ul>"
    "<h3>Good to know</h3><ul><li>The mixer body goes in the wall before tiling; set the height so the spout clears "
    "the basin rim or bath edge</li><li>Pair with a Celine pop-up waste in the same finish</li></ul>",
    [SUP, CDN + "HD7025_1_1_41e2c0d6-8687-4fbb-bfa4-0e17c83695ef.jpg"], True, "Dimensions from supplier size diagram.")

add("celine-shower-mixer",
    "<p>The Celine Shower Mixer is a single-lever wall mixer on a slim rectangular plate. The lever is marked H and C, "
    "and the body sits in the wall so only the plate and handle show on the tiles.</p>"
    "<h3>Use it for</h3><ul><li>Showers with one outlet (rail shower, overhead rose or twin rail with its own "
    "diverter)</li><li>Baths with a separate spout where one outlet is enough</li></ul>"
    "<h3>Specifications</h3><ul><li>Plate: 75 x 160mm</li><li>Operation: single lever, in-wall body</li>" + FIN +
    "<li>Model: HD7023</li></ul>"
    "<h3>Good to know</h3><ul><li>If you need to switch between two outlets (say a bath spout and a shower) use the "
    "Celine Shower Mixer with Diverter instead</li><li>The in-wall body is fitted before tiling, so order the mixer "
    "before the wet area is sheeted</li><li>" + CEL + "</li></ul>",
    [SUP, CDN + "HD7023_1_da563660-e47a-40ae-9e2c-193fea43f124.jpg"], True, "Plate size from supplier diagram.")

add("celine-shower-mixer-with-diverter",
    "<p>The Celine Shower Mixer with Diverter is a single-lever wall mixer with a built-in diverter, so one mixer "
    "runs two outlets, such as a bath spout and a shower, or an overhead rose and a hand shower. Turn the small knob "
    "to send the water the other way.</p>"
    "<h3>Use it for</h3><ul><li>Shower over bath combinations</li><li>Showers with a separate overhead rose and "
    "hand shower on bracket</li></ul>"
    "<h3>Specifications</h3><ul><li>Plate: 85 x 170mm</li><li>Operation: single lever for flow and temperature, "
    "diverter knob below</li><li>Outlets: two</li>" + FIN + "<li>Model: HD7024</li></ul>"
    "<h3>Good to know</h3><ul><li>The in-wall body is fitted before tiling, so have it on site before the wet area "
    "is sheeted</li><li>Pair with the Celine Swivel Bath Spout and a Celine hand shower or rose</li><li>" + CEL +
    "</li></ul>",
    [SUP, CDN + "hd7024_1_ae24c2ad-55e0-4b48-80c6-0fb4842be6aa.jpg"], True, "Plate size from supplier diagram.")

add("celine-swivel-bath-spout",
    "<p>The Celine Swivel Bath Spout is a slim square wall spout that swings out of the way when the bath is not in "
    "use. At 15mm thick it sits flat against the tiles and matches the square profile of the Celine wall mixers.</p>"
    "<h3>Use it for</h3><ul><li>Filling a built-in bath from a wall mixer</li><li>Shower over bath setups with a "
    "diverter mixer</li></ul>"
    "<h3>Specifications</h3><ul><li>Length: 249.5mm from the wall</li><li>Spout: 15mm thick</li>"
    "<li>Wall plate: 60 x 42mm</li><li>Swivels side to side</li>" + FIN +
    "<li>Model: SP18SW (Chrome), SP28SW-BN (Brushed Nickel)</li></ul>"
    "<h3>Good to know</h3><ul><li>Needs a half-inch wall outlet; the spout does not control flow, so pair it with the "
    "Celine Shower Mixer or Shower Mixer with Diverter</li><li>Set the outlet height so the spout clears the bath "
    "rim</li></ul>",
    [SUP, CDN + "CelineSwivelBathSpout-SP28SWsize.jpg"], True, "Dimensions from supplier size diagram.")

add("celine-sink-mixer",
    "<p>The Celine Sink Mixer is a single-lever kitchen or laundry tap with a flat, angled spout and the same mix "
    "of curves and sharp edges as the rest of the Celine range. The spout sits 288mm above the bench, which gives "
    "room to fill tall pots and buckets.</p>"
    "<h3>Use it for</h3><ul><li>Kitchen sinks and laundry troughs with a tap hole</li><li>Matching Celine tapware "
    "through the house</li></ul>"
    "<h3>Specifications</h3><ul><li>Height: 305mm overall, spout outlet 288mm above the bench</li>"
    "<li>Spout reach: 202mm</li><li>Base: 50mm diameter</li><li>Operation: single lever</li>" + FIN +
    "<li>Model: HD7027</li></ul>"
    "<h3>Good to know</h3><ul><li>Check the 202mm reach lands over the bowl, especially on a small single bowl sink</li>"
    "<li>Wipe with a soft damp cloth; skip abrasive cleaners on the finish</li></ul>",
    [SUP, CDN + "hd7027_1_9b2dcd5d-a300-408a-88dd-8e95c4bd5d87.jpg"], True, "Dimensions from supplier size diagram.")

add("celine-gooseneck-sink-mixer",
    "<p>The Celine Gooseneck Sink Mixer is a classic round gooseneck tap for the kitchen or laundry, with a slim pin "
    "lever and a high arch that clears tall pots. It suits kitchens that want a softer look than the square "
    "Celine Sink Mixer.</p>"
    "<h3>Use it for</h3><ul><li>Kitchen sinks and laundry troughs with a tap hole</li><li>Benches where the spout "
    "needs to swing between two bowls</li></ul>"
    "<h3>Specifications</h3><ul><li>Height: 290mm overall, spout outlet 275mm above the bench</li>"
    "<li>Spout reach: 160mm</li><li>Body height: 110mm</li><li>Operation: single pin lever</li>" + FIN +
    "<li>Model: HD4232</li></ul>"
    "<h3>Good to know</h3><ul><li>The 160mm reach suits smaller bowls; for a wide double bowl check the spout lands "
    "where you want it</li><li>Wipe with a soft damp cloth; skip abrasive cleaners on the finish</li></ul>",
    [SUP, CDN + "HD4232_1_dd747fe9-417b-4e9a-a5ac-dbd62b177703.jpg"], True, "Dimensions from supplier size diagram.")

add("celine-gooseneck-pull-out-kitchen-mixer",
    "<p>The Celine Gooseneck Pull Out Kitchen Mixer has a pull-out vege sprayer hidden in the spout, so you can "
    "rinse the whole sink, fill pots on the bench or wash greens without splashing. The tall round gooseneck swings "
    "across the sink and the single lever controls flow and temperature.</p>"
    "<h3>Use it for</h3><ul><li>Kitchen sinks, especially double bowls where a fixed spout does not reach both "
    "sides</li><li>Busy family kitchens that want an easy sink clean-up</li></ul>"
    "<h3>Features</h3><ul><li>Pull-out spray head on a retractable hose</li><li>Gooseneck spout with full swivel</li>"
    "<li>Single-lever mixing</li></ul>"
    "<h3>Specifications</h3><ul>" + FIN + "<li>Model: FE1731</li></ul>"
    "<h3>Good to know</h3><ul><li>Leave clear space under the sink for the hose to drop and retract</li>"
    "<li>Wipe with a soft damp cloth; skip abrasive cleaners on the finish</li></ul>",
    [SUP, CDN + "FE1731_f77e8c28-64e4-4dab-8689-367472d90480.jpg"], False, "No dimensions available; photo only.")

# ---------------- Accessories ----------------
def rail(handle, name, length, kind, model, dims, verified, src, note):
    inner = ("two bars" if kind == "double" else "a single bar")
    html = (f"<p>The {name} is a {length}mm wall-mounted towel rail with {inner} and flat, rounded end posts. "
            "It is sized to hold " + ("two bath towels side by side or a folded towel over each bar" if kind == "double"
            else "a bath towel or a couple of hand towels") + ", and it matches the rest of the Celine accessories.</p>"
            "<h3>Use it for</h3><ul><li>Bathrooms, ensuites and laundries</li><li>Matching a Celine mixer and "
            "shower in the same finish</li></ul>"
            "<h3>Specifications</h3><ul>" + dims + FIN + f"<li>Model: {model}</li></ul>"
            "<h3>Good to know</h3><ul><li>Fix into studs or use proper hollow-wall anchors on plasterboard; a wet "
            "towel is heavier than it looks</li><li>Wipe with a soft damp cloth; skip abrasive cleaners</li>"
            "<li>Also available in " + ("600mm" if length == 800 else "800mm") + " and as a "
            + ("single" if kind == "double" else "double") + " rail</li></ul>")
    add(handle, html, src, verified, note)

rail("celine-800-double-towel-rail", "Celine 800 Double Towel Rail", 800, "double", "HDP302-80",
     "<li>Length: 800mm</li><li>Projection from wall: 120mm</li><li>Bars: two, 8mm thick, 20mm deep</li>"
     "<li>End posts: 38mm wide</li>", True,
     [SUP, CDN + "HDP302-80size_4b7f8aa0-b7a0-42be-be7d-fe89b0a85aad.jpg"], "Dimensions from supplier size diagram.")
rail("celine-600-double-towel-rail", "Celine 600 Double Towel Rail", 600, "double", "HDP302-60",
     "<li>Length: 600mm</li><li>Bars: two</li>", False,
     [SUP, CDN + "HDP302_3_c82fab9c-28ae-401f-8b5e-2bf7590490cf.jpg"],
     "No 600mm diagram; projection figures from the 800mm drawing not applied.")
rail("celine-800-single-towel-rail", "Celine 800 Single Towel Rail", 800, "single", "HDP301-80",
     "<li>Length: 800mm</li><li>Projection from wall: 72mm</li><li>Bar: 8mm thick, 20mm deep</li>"
     "<li>End posts: 38mm wide</li>", True,
     [SUP, CDN + "HDP301-80_cb4195b1-59c7-489a-98fa-cbb2309d12b3.jpg"], "Dimensions from supplier size diagram.")
rail("celine-600-single-towel-rail", "Celine 600 Single Towel Rail", 600, "single", "HDP301-60",
     "<li>Length: 600mm</li>", False,
     [SUP, CDN + "HDP301_2_a871acb6-22b5-470b-b230-a8d20d3a31ff.jpg"],
     "No 600mm diagram; projection figures from the 800mm drawing not applied.")

add("celine-hand-towel-rail",
    "<p>The Celine Hand Towel Rail is a short open-ended rail for a hand towel next to the basin. The towel slides "
    "on from the open end, so there is no ring to fight with, and the flat rounded bracket matches the other "
    "Celine accessories.</p>"
    "<h3>Use it for</h3><ul><li>Powder rooms and ensuites beside the vanity</li><li>Tight spots where a full "
    "towel rail will not fit</li></ul>"
    "<h3>Specifications</h3><ul><li>Style: single open-ended bar on one wall bracket</li>" + FIN +
    "<li>Model: HDP305</li></ul>"
    "<h3>Good to know</h3><ul><li>Fix into a stud or use a proper plasterboard anchor</li><li>Wipe with a soft damp "
    "cloth; skip abrasive cleaners</li><li>Matches the Celine robe hook, toilet roll holder and towel rails</li></ul>",
    [SUP, CDN + "HDP305_1_b816c9ad-53f8-4aa1-a535-392ac6abcfc7.jpg"], False, "No dimensions available; photo only.")

add("celine-robe-hook",
    "<p>The Celine Robe Hook is a single wall hook with a flat, rounded face that matches the Celine towel rails and "
    "toilet roll holder. Use it for a robe or towel behind the bathroom door, or fit two side by side for a "
    "family bathroom.</p>"
    "<h3>Use it for</h3><ul><li>Robes and towels behind doors and beside showers</li><li>Laundries and "
    "powder rooms</li></ul>"
    "<h3>Specifications</h3><ul><li>Style: single hook, solid body</li>" + FIN + "<li>Model: HDP306</li></ul>"
    "<h3>Good to know</h3><ul><li>Fix into a stud or use a proper plasterboard anchor so a wet towel does not pull "
    "it loose</li><li>Wipe with a soft damp cloth; skip abrasive cleaners</li><li>" + CEL + "</li></ul>",
    [SUP, CDN + "HDP306_1_58f473e5-461e-4607-822a-1307d2ab7dfa.jpg"], False, "No dimensions available; photo only.")

add("celine-toilet-roll-holder",
    "<p>The Celine Toilet Roll Holder is an open-ended holder with a flat square arm, so the roll slides on and off "
    "without a spring-loaded spindle. It matches the Celine towel rails and robe hook.</p>"
    "<h3>Use it for</h3><ul><li>Toilets, ensuites and powder rooms</li></ul>"
    "<h3>Specifications</h3><ul><li>Arm: 175mm long, 72mm projection from the wall</li>"
    "<li>Bracket: 38mm tall, 20mm deep</li><li>Base plate: 26mm wide</li>" + FIN + "<li>Model: HDP304</li></ul>"
    "<h3>Good to know</h3><ul><li>Standard rolls slide straight on; fit it with the open end facing the way you "
    "want the roll to hang</li><li>Fix into a stud or use a plasterboard anchor</li><li>Wipe with a soft damp cloth; "
    "skip abrasive cleaners</li></ul>",
    [SUP, CDN + "image_2.png"], True, "Dimensions from supplier size diagram.")

# ---------------- Wastes, traps, drains ----------------
add("celine-bath-pop-up-waste",
    "<p>The Celine Bath Pop Up Waste is a push-button plug for a 40mm bath outlet. Press the 70mm domed cap to seal "
    "the bath and press again to drain, with no chain or plug to lose. Pick the same finish as your bath spout "
    "and mixer.</p>"
    "<h3>Use it for</h3><ul><li>Built-in and freestanding baths with a standard 40mm outlet</li></ul>"
    "<h3>Specifications</h3><ul><li>Cap: 70mm diameter</li><li>Thread: G1 1/2 (40mm)</li><li>Body height: 38mm</li>"
    "<li>Operation: push to close, push to open</li>" + FIN + "<li>Model: BW047</li></ul>"
    "<h3>Good to know</h3><ul><li>Check the bath outlet is 40mm; basin outlets are usually 32mm and take the Celine "
    "Universal Pop Up Waste instead</li><li>Hair catches on the plug stem, so lift it out and clear it now and "
    "then</li></ul>",
    [SUP, CDN + "BW047-SIZE.jpg"], True, "Dimensions from supplier size diagram.")

add("celine-universal-pop-up-waste-32-40mm",
    "<p>The Celine Universal Pop Up Waste is a push-button basin plug that fits 32mm and 40mm outlets. Press the cap "
    "to seal the basin and press again to drain, with a 62mm flange that covers the outlet neatly.</p>"
    "<h3>Use it for</h3><ul><li>Above-counter, semi-inset, undermount and wall-hung basins</li><li>Matching the "
    "finish of a Celine basin mixer</li></ul>"
    "<h3>Specifications</h3><ul><li>Suits: 32mm and 40mm outlets</li><li>Flange: 62mm diameter, 37.5mm cap</li>"
    "<li>Thread: G1 1/4</li><li>Height: 78mm overall; suits basin thickness from 30 to 65mm</li>"
    "<li>Operation: push to close, push to open</li>" + FIN + "<li>Model: K81</li></ul>"
    "<h3>Good to know</h3><ul><li>This waste does not include an overflow slot; if your basin has an overflow, "
    "check the waste type with your plumber</li><li>Lift the plug out to clear hair when it drains slowly</li></ul>",
    [SUP, CDN + "K80-SIZE_1_1bad27f5-7288-4bbe-bac4-5b44d9beef3f.jpg"], True,
    "Dimensions from supplier size diagram (drawing is labelled K80; same listing).")

add("celine-bottle-trap-32mm",
    "<p>The Celine Bottle Trap is a 32mm exposed trap for a wall-hung or vessel basin where the plumbing is on show. "
    "It replaces the usual plastic trap with a slim metal bottle and a straight wall tube, finished to match your "
    "mixer.</p>"
    "<h3>Use it for</h3><ul><li>Wall-hung basins and open vanities</li><li>Pedestal and console basins</li></ul>"
    "<h3>Specifications</h3><ul><li>Inlet: G1 1/4 (32mm) with 0 to 85mm adjustable tail</li>"
    "<li>Body: 50mm diameter, 133mm high</li><li>Wall tube: 320mm long, 31.75mm outside diameter</li>"
    "<li>Wall flange: 70mm diameter</li>" + FIN + "<li>Model: B186</li></ul>"
    "<h3>Good to know</h3><ul><li>Cut the wall tube to suit; the flange covers the pipe entry</li><li>The bottle "
    "unscrews from below to clear a blockage</li><li>Pair with the Celine Universal Pop Up Waste</li></ul>",
    [SUP, CDN + "B186.jpg"], True, "Dimensions from supplier size diagram.")

add("twist-top-floor-drain-80mm",
    "<p>The Twist Top Floor Drain is a square 85 x 85mm floor waste grate for an 80mm outlet. The round slotted "
    "grate twists out for cleaning, so hair and grit can be cleared without tools.</p>"
    "<h3>Use it for</h3><ul><li>Shower floors and bathroom floor wastes on 80mm pipe</li><li>Laundries and "
    "balconies</li></ul>"
    "<h3>Specifications</h3><ul><li>Top: 85 x 85mm square</li><li>Body: 75mm diameter, 17mm deep</li>"
    "<li>Grate: round, slotted, twist to remove</li><li>Outlet: 80mm</li>" + FIN + "<li>Model: BD073</li></ul>"
    "<h3>Good to know</h3><ul><li>Measure the outlet pipe before ordering; a 100mm version is listed separately</li>"
    "<li>For a grate that the tile runs through, see the Tile Insert Floor Waste</li><li>Set the grate flush with "
    "the finished tile and fall the floor towards it</li></ul>",
    [SUP, CDN + "BD073-SIZE_1_a2166569-6b81-43cc-954a-d739eafa7d00.jpg"], True,
    "Dimensions from supplier size diagram.")

add("twist-top-floor-drain-100mm",
    "<p>The Twist Top Floor Drain 100mm is a square floor waste grate for a 100mm outlet. The round slotted grate "
    "twists out for cleaning, so hair and grit can be cleared without tools.</p>"
    "<h3>Use it for</h3><ul><li>Shower floors and bathroom floor wastes on 100mm pipe</li><li>Laundries, garages "
    "and balconies</li></ul>"
    "<h3>Specifications</h3><ul><li>Outlet: 100mm</li><li>Grate: round, slotted, twist to remove</li>"
    "<li>Top: square</li>" + FIN + "<li>Model: BD078</li></ul>"
    "<h3>Good to know</h3><ul><li>Measure the outlet pipe before ordering; an 80mm version is listed separately</li>"
    "<li>For a grate that the tile runs through, see the Tile Insert Floor Waste</li><li>Set the grate flush with "
    "the finished tile and fall the floor towards it</li></ul>",
    [SUP, CDN + "BD073.CR_ddc95546-542f-4a2a-8675-ef256854a8d9.jpg"], False,
    "No 100mm diagram; listing uses the 80mm photo, so top dimensions left out.")

add("tile-insert-floor-waste-80mm-100-x-100mm",
    "<p>This Tile Insert Floor Waste has a square 100 x 100mm frame with a recessed tray, so a cut piece of your "
    "floor tile sits in the grate and the drain all but disappears. It suits an 80mm outlet and gives a shower "
    "floor the clean, continuous look of a tile-in drain.</p>"
    "<h3>Use it for</h3><ul><li>Shower floors and wet rooms on 80mm pipe</li><li>Large-format tiles where a "
    "standard grate would break the pattern</li></ul>"
    "<h3>Specifications</h3><ul><li>Frame: 100 x 100mm</li><li>Tile recess: 80 x 80mm</li>"
    "<li>Height: 35mm overall (20mm frame plus 15mm spigot)</li><li>Outlet: 80mm</li><li>Finish: Chrome</li>"
    "<li>Model: SQT101-100D-80</li></ul>"
    "<h3>Good to know</h3><ul><li>The tray lifts out so the drain can be cleaned</li><li>Have the tiler cut and "
    "glue the tile insert at the same time as the floor so the grout lines run through</li><li>A 50mm outlet "
    "version is listed separately</li></ul>",
    [SUP, CDN + "SQTI01-100D-80.BS_-_Size.jpg"], True, "Dimensions from supplier size diagram.")

add("tile-insert-floor-waste-50mm-100-x-100mm",
    "<p>This Tile Insert Floor Waste has a square 100 x 100mm frame with a recessed tray, so a cut piece of your "
    "floor tile sits in the grate and the drain all but disappears. It suits a 50mm outlet and gives a shower "
    "floor the clean, continuous look of a tile-in drain.</p>"
    "<h3>Use it for</h3><ul><li>Shower floors and wet rooms on 50mm pipe</li><li>Large-format tiles where a "
    "standard grate would break the pattern</li></ul>"
    "<h3>Specifications</h3><ul><li>Frame: 100 x 100mm</li><li>Outlet: 50mm</li><li>Finish: Chrome</li>"
    "<li>Model: TID50</li></ul>"
    "<h3>Good to know</h3><ul><li>The tray lifts out so the drain can be cleaned</li><li>Have the tiler cut and "
    "glue the tile insert at the same time as the floor so the grout lines run through</li><li>An 80mm outlet "
    "version is listed separately</li></ul>",
    [SUP, CDN + "SQTI01-100D-80.BS_8428515b-1680-471b-821a-f56d1ba10421.jpg"], False,
    "Listing uses the 80mm photo; only the 100 x 100mm top and 50mm outlet are certain.")

# ---------------- Basins ----------------
add("cosimo-above-counter-basin",
    "<p>The Cosimo Above Counter Basin is a soft-rectangle vessel basin in gloss white vitreous china, 460mm wide "
    "and 170mm high. It sits on top of the vanity, so it suits a stone or timber bench with a tall basin mixer.</p>"
    "<h3>Use it for</h3><ul><li>Vanities with a stone or solid top</li><li>Pairing with the Celine Tall Basin "
    "Mixer</li></ul>"
    "<h3>Specifications</h3><ul><li>Size: 460 x 325 x 170mm</li><li>Shape: rectangular with rounded corners</li>"
    "<li>Material: vitreous china</li><li>Finish: gloss white</li><li>Tap hole: none (use a tall or wall mixer)</li>"
    "<li>Model: BA207CT</li></ul>" + BASIN_GTK,
    [SUP, CDN + "895.jpg"], False,
    "Size from existing description. Supplier photo is captioned 455x325x135mm, which conflicts, so not used.")

add("cosimo-semi-inset-basin",
    "<p>The Cosimo Semi Inset Basin drops into a cut-out in the vanity top with the front of the bowl sitting proud "
    "of the cabinet. It is the fix for shallow vanities (under 400mm deep) where a full inset basin will not fit, "
    "and it keeps the bench top clear.</p>"
    "<h3>Use it for</h3><ul><li>Narrow vanities in ensuites and powder rooms</li><li>Replacing a semi-recessed "
    "basin in a renovation</li></ul>"
    "<h3>Specifications</h3><ul><li>Size: 520 x 340 x 150mm</li><li>Bowl: 500 x 320mm, 100mm deep</li>"
    "<li>Material: vitreous china</li><li>Finish: gloss white</li><li>Model: E408D</li></ul>" + BASIN_GTK,
    [SUP, CDN + "E408D_1.png"], True, "Bowl size from supplier diagram.")

add("cosimo-undermount-basin",
    "<p>The Cosimo Undermount Basin fixes under a stone or solid-surface top, so the bench runs clean to the edge "
    "of the bowl and wipes straight into it. It has a built-in overflow and a rectangular bowl that makes the "
    "most of a narrow vanity.</p>"
    "<h3>Use it for</h3><ul><li>Stone-top vanities, with a wall mixer or a bench-mounted mixer</li>"
    "<li>Kitchens and laundries that want a small hand basin under stone</li></ul>"
    "<h3>Specifications</h3><ul><li>Size: 455 x 325 x 180mm</li><li>Shape: rectangular</li><li>Overflow: built "
    "in</li><li>Material: vitreous china</li><li>Finish: gloss white</li><li>Model: BSN6018</li></ul>"
    "<h3>Good to know</h3><ul><li>The stonemason cuts and polishes the top to suit this basin, so supply the basin "
    "before the top is made</li><li>Takes a standard 32mm overflow waste (not included)</li><li>Wipe with a soft "
    "cloth and non-abrasive cleaner</li></ul>",
    [SUP, CDN + "DSABSN6018.png"], False, "Size from existing description; photo only.")

add("cube-wall-hung-basin",
    "<p>The Cube Wall Hung Basin is a compact 455 x 255mm hand basin that bolts straight to the wall, with the tap "
    "hole on a flat deck to one side. At only 255mm deep it suits a small toilet or powder room where a vanity "
    "would get in the way. Choose the tap hole on the left or the right.</p>"
    "<h3>Use it for</h3><ul><li>Toilets, powder rooms and laundries</li><li>Tight spaces next to a door</li></ul>"
    "<h3>Specifications</h3><ul><li>Size: 455 x 255 x 120mm</li><li>Tap hole: one, on the left or the right</li>"
    "<li>Material: vitreous china</li><li>Finish: gloss white</li><li>Model: BSN4228L (left), BSN4229R (right)</li></ul>"
    "<h3>Good to know</h3><ul><li>Takes a standard 32mm overflow waste (not included)</li><li>A bottle trap "
    "finishes the exposed plumbing underneath</li><li>Fix to studs or noggins; the wall carries the full weight</li>"
    "</ul>",
    [SUP, CDN + "DSABSN4229L.png"], False, "Size from existing description; photo only.")

add("mezo-above-counter-basin",
    "<p>The Mezo Above Counter Basin is a small oval vessel basin in gloss white vitreous china. At 410mm wide it "
    "fits a narrow vanity or a powder room bench and sits on top of the bench with a tall or wall mixer.</p>"
    "<h3>Use it for</h3><ul><li>Powder rooms and ensuites with a narrow bench</li><li>Pairing with the Celine Tall "
    "Basin Mixer or Celine wall mixer</li></ul>"
    "<h3>Specifications</h3><ul><li>Size: 410 x 340 x 150mm</li><li>Shape: oval, sloped sides</li>"
    "<li>Material: vitreous china</li><li>Finish: gloss white</li><li>Tap hole: none</li><li>Model: 847</li></ul>"
    + BASIN_GTK,
    [SUP, CDN + "847.jpg"], False,
    "Size from existing description. Supplier photo is captioned 405x330x140mm, which conflicts, so not used.")

add("olivia-above-counter-basin",
    "<p>The Olivia Above Counter Basin is a wide pill-shaped vessel basin, 490mm long with soft rounded ends and "
    "a shallow 135mm profile that does not tower over the bench. It sits on top of the vanity with a tall or "
    "wall-mounted mixer.</p>"
    "<h3>Use it for</h3><ul><li>Stone and timber vanity tops</li><li>Pairing with the Celine Tall Basin Mixer or "
    "Celine wall mixer</li></ul>"
    "<h3>Specifications</h3><ul><li>Size: 490 x 360 x 135mm</li><li>Shape: oval with straight sides</li>"
    "<li>Material: vitreous china</li><li>Finish: gloss white</li><li>Tap hole: none</li><li>Model: BA8025CT</li></ul>"
    + BASIN_GTK,
    [SUP, CDN + "10001.png"], False, "Size from existing description; photo only.")

add("olivia-semi-inset-basin",
    "<p>The Olivia Semi Inset Basin drops into a cut-out in the vanity top with the oval front sitting proud of the "
    "cabinet, so it works on shallow vanities where a full inset basin will not fit. It has an overflow slot and "
    "a deep 165mm bowl.</p>"
    "<h3>Use it for</h3><ul><li>Narrow vanities in ensuites and powder rooms</li><li>Replacing an older "
    "semi-recessed basin</li></ul>"
    "<h3>Specifications</h3><ul><li>Size: 485 x 330 x 165mm</li><li>Shape: oval</li><li>Overflow: yes</li>"
    "<li>Material: vitreous china</li><li>Finish: gloss white</li><li>Model: BSN4302S</li></ul>"
    "<h3>Good to know</h3><ul><li>Takes a standard 32mm overflow waste (not included)</li><li>The vanity top is cut "
    "to the basin template, so have the basin on site before the top is cut</li><li>Wipe with a soft cloth and "
    "non-abrasive cleaner</li></ul>",
    [SUP, CDN + "4302S.png"], False, "Size from existing description; overflow visible in supplier photo.")

add("ria-above-counter-basin",
    "<p>The Ria Above Counter Basin is a round, straight-sided vessel basin, 360mm across and 120mm high, in gloss "
    "white vitreous china. Its small footprint suits a narrow vanity or a powder room, and the low height keeps a "
    "tall mixer from looking out of scale.</p>"
    "<h3>Use it for</h3><ul><li>Powder rooms and small ensuites</li><li>Pairing with the Celine Tall Basin Mixer or "
    "Celine wall mixer</li></ul>"
    "<h3>Specifications</h3><ul><li>Size: 360 x 360 x 120mm</li><li>Shape: round, straight sides</li>"
    "<li>Material: vitreous china</li><li>Finish: gloss white</li><li>Tap hole: none</li><li>Model: BA222CT</li></ul>"
    "<h3>Good to know</h3><ul><li>Takes a standard 32mm waste (not included); a pop-up waste in the same finish as "
    "your mixer is the usual pick</li><li>Wipe with a soft cloth and non-abrasive cleaner</li><li>A semi inset "
    "version of the Ria is listed separately</li></ul>",
    [SUP, CDN + "4201.png"], False, "Size from existing description; photo only.")

add("ria-semi-inset-basin",
    "<p>The Ria Semi Inset Basin is a round 360mm basin that drops into a cut-out in the vanity top with the front "
    "sitting proud of the cabinet, so it fits a shallow vanity where a full inset basin will not. Gloss white "
    "vitreous china, 120mm high.</p>"
    "<h3>Use it for</h3><ul><li>Narrow vanities in ensuites and powder rooms</li><li>Pairing with a Celine basin "
    "mixer or wall mixer</li></ul>"
    "<h3>Specifications</h3><ul><li>Size: 360 x 360 x 120mm</li><li>Shape: round</li>"
    "<li>Material: vitreous china</li><li>Finish: gloss white</li><li>Model: BSN4201</li></ul>"
    "<h3>Good to know</h3><ul><li>Takes a standard 32mm overflow waste (not included)</li><li>The vanity top is cut "
    "to the basin template, so have the basin on site before the top is cut</li><li>Wipe with a soft cloth and "
    "non-abrasive cleaner</li><li>An above counter version of the Ria is listed separately</li></ul>",
    [SUP, CDN + "4201.png"], False, "Size from existing description; photo only.")

# ---------------- Kitchen sinks ----------------
SINK_GTK = ("<h3>Good to know</h3><ul><li>Stainless steel marks less if you rinse and wipe it dry after use</li>"
            "<li>Measure the cabinet width and the benchtop cut-out before ordering</li></ul>")

add("caden-single-bowl-sink-610mm",
    "<p>The Caden Single Bowl Sink is a 610 x 500mm stainless steel top-mount sink with one deep 200mm bowl and a "
    "single tap hole on the rear ledge. It drops into a benchtop cut-out and comes with the basket waste, so it is "
    "ready to plumb.</p>"
    "<h3>Use it for</h3><ul><li>Kitchens and laundries with a 600mm sink cabinet</li><li>Replacing an old "
    "top-mount sink without changing the tap position</li></ul>"
    "<h3>Specifications</h3><ul><li>Overall: 610 x 500mm, 200mm deep</li><li>Bowl: 534 x 424mm</li>"
    "<li>Tap holes: one</li><li>Overflow: none</li><li>Installation: top mount (above mount)</li>"
    "<li>Material: stainless steel</li><li>Model: LS-6150</li></ul>"
    "<h3>What's in the box</h3><ul><li>Sink and basket waste</li></ul>" + SINK_GTK,
    [SUP, CDN + "LS-6150.png"], True,
    "Old text said 'Inner 610x500x200'; the supplier diagram shows 610 x 500 overall with a 534 x 424 bowl.")

add("caden-single-bowl-sink-with-drainer-660mm",
    "<p>The Caden Single Bowl Sink with Drainer is a compact 660 x 420mm stainless steel top-mount sink with one "
    "bowl and a ribbed drainer beside it. It suits a small kitchen, laundry or outdoor bench where a full-width "
    "sink will not fit, and it comes with the basket waste.</p>"
    "<h3>Use it for</h3><ul><li>Small kitchens, granny flats and laundries</li><li>Outdoor and bar benches</li></ul>"
    "<h3>Specifications</h3><ul><li>Overall: 660 x 420mm, 200mm deep</li><li>Bowl: 365 x 335mm</li>"
    "<li>Drainer: one side</li><li>Tap holes: one</li><li>Overflow: none</li><li>Installation: top mount "
    "(above mount)</li><li>Material: stainless steel</li><li>Model: LS-7642S</li></ul>"
    "<h3>What's in the box</h3><ul><li>Sink and basket waste</li></ul>" + SINK_GTK,
    [SUP, CDN + "LS-7642S_2.jpg"], False, "Sizes from existing description; supplier image is a photo.")

add("caden-double-bowl-sink-with-drainer-1200mm",
    "<p>The Caden Double Bowl Sink with Drainer is a full 1200mm stainless steel top-mount sink with two matching "
    "bowls and a ribbed drainer on the right. Two bowls let you wash in one and rinse in the other, and it comes "
    "with the basket wastes.</p>"
    "<h3>Use it for</h3><ul><li>Family kitchens with a 1200mm sink cabinet</li><li>Replacing a 1200mm top-mount "
    "sink in a renovation</li></ul>"
    "<h3>Specifications</h3><ul><li>Overall: 1200 x 500mm, 200mm deep</li><li>Bowls: two, 350 x 390mm each</li>"
    "<li>Drainer: one side</li><li>Tap holes: one</li><li>Overflow: none</li><li>Installation: top mount "
    "(above mount)</li><li>Material: stainless steel</li><li>Model: LS-12050A</li></ul>"
    "<h3>What's in the box</h3><ul><li>Sink and basket waste</li></ul>" + SINK_GTK,
    [SUP, CDN + "LS-12050A.png"], True, "Dimensions confirmed against supplier diagram.")

add("callan-single-bowl-sink-450mm",
    "<p>The Callan Single Bowl Sink is a 450 x 400mm square-cornered stainless steel sink with a deep 230mm bowl. "
    "It can be top mounted or fitted under a stone bench, and it comes with the basket waste. With no tap hole it "
    "pairs with a bench-mounted mixer.</p>"
    "<h3>Use it for</h3><ul><li>Laundries and small kitchens</li><li>Bar and butler's pantry sinks under stone</li></ul>"
    "<h3>Specifications</h3><ul><li>Overall: 450 x 400mm, 230mm deep</li><li>Bowl: 400 x 350mm</li>"
    "<li>Waste hole: 114mm</li><li>Overflow: none</li><li>Installation: top mount or undermount</li>"
    "<li>Material: stainless steel</li><li>Model: LS-4045</li></ul>"
    "<h3>What's in the box</h3><ul><li>Sink and basket waste</li></ul>" + SINK_GTK,
    [SUP, CDN + "LS-4045.jpg"], True, "Dimensions from supplier diagram.")

add("callan-single-bowl-sink-580mm",
    "<p>The Callan Single Bowl Sink is a 580 x 450mm square-cornered stainless steel sink with one large 530mm "
    "bowl, 230mm deep. It can be top mounted or fitted under a stone bench, and the underside has a sound-deadening "
    "pad to cut the clatter of dishes. Basket waste included.</p>"
    "<h3>Use it for</h3><ul><li>Kitchens with a 600mm sink cabinet</li><li>Undermount under stone or solid "
    "surface tops</li></ul>"
    "<h3>Specifications</h3><ul><li>Overall: 580 x 450mm, 230mm deep</li><li>Bowl: 530 x 350mm</li>"
    "<li>Overflow: none</li><li>Installation: top mount or undermount</li><li>Material: stainless steel</li>"
    "<li>Model: LS-5845</li></ul>"
    "<h3>What's in the box</h3><ul><li>Sink and basket waste</li></ul>" + SINK_GTK,
    [SUP, CDN + "ETLS5845_3.jpg"], False, "Sizes from existing description; sound pad visible in supplier photo.")

add("callan-double-bowl-sink-700mm",
    "<p>The Callan Double Bowl Sink is a 700 x 400mm square-cornered stainless steel sink with two equal bowls, "
    "240mm deep. It can be top mounted or fitted under a stone bench, and it comes with the basket wastes. With no "
    "tap hole it pairs with a bench-mounted mixer.</p>"
    "<h3>Use it for</h3><ul><li>Kitchens that want two bowls in a 700mm cabinet</li><li>Undermount under stone "
    "or solid surface tops</li></ul>"
    "<h3>Specifications</h3><ul><li>Overall: 700 x 400mm, 240mm deep</li><li>Bowls: two, 350 x 310mm each</li>"
    "<li>Waste holes: 114mm</li><li>Overflow: none</li><li>Installation: top mount or undermount</li>"
    "<li>Material: stainless steel</li><li>Model: LS-7040</li></ul>"
    "<h3>What's in the box</h3><ul><li>Sink and basket waste</li></ul>" + SINK_GTK,
    [SUP, CDN + "LS-7040.jpg"], True, "Dimensions from supplier diagram.")

# ---------------- Malaga vanities and cabinets ----------------
MAL_FIN = {"Antico Oak": "Antico Oak melamine", "Dark Oak": "Dark Oak melamine", "Matt White": "Matt White painted finish"}
MAL_SRC = [SUP, CDN + "ETOJS106-1200AO_1.png", CDN + "ETOJS106-600W_1.png"]

for col in ["Antico Oak", "Dark Oak", "Matt White"]:
    h = "malaga-" + col.lower().replace(" ", "-") + "-wall-hung-vanity"
    add(h,
        f"<p>The Malaga {col} Wall Hung Vanity is a handle-free cabinet with finger-pull doors and drawers, in four "
        "widths from 600 to 1200mm. It is supplied as the cabinet only, so you choose the top and basin to suit, "
        "and the wall-hung design keeps the floor clear for easy mopping.</p>"
        "<h3>Use it for</h3><ul><li>Bathrooms and ensuites that want a clean, minimal vanity</li><li>Pairing with "
        "a stone top and above counter basin, or a ceramic top</li></ul>"
        "<h3>Specifications</h3><ul><li>Widths: 600, 750, 900 and 1200mm (cabinet measures 590, 740, 890 and "
        "1190mm wide)</li><li>Height: 630mm</li><li>Depth: 455mm</li><li>Doors and drawers with finger pulls, no "
        "handles</li><li>600mm: two drawers; 1200mm: four drawers with room for two basins</li>"
        f"<li>Finish: {MAL_FIN[col]}</li><li>Model: OJS106</li></ul>"
        "<h3>Good to know</h3><ul><li>Supplied as cabinet; add a basin or top to suit</li><li>Fix to studs or a "
        "noggin; a wall hung vanity carries the top, basin and water on the wall</li><li>Matching kickboard, "
        "cubby cabinet and single door cabinet are listed separately</li></ul>",
        MAL_SRC, True, "Actual cabinet widths and drawer layout from supplier diagrams (600 and 1200 drawn).")

for col in ["Antico Oak", "Dark Oak", "Matt White"]:
    h = "malaga-" + col.lower().replace(" ", "-") + "-vanity-kickboard"
    add(h,
        f"<p>The Malaga {col} Vanity Kickboard closes the gap under a Malaga wall hung vanity, so the cabinet reads as "
        "floor-standing without losing the wall-hung fixing. It comes in 750, 900 and 1200mm to match the vanity "
        "widths, in the same finish as the cabinet.</p>"
        "<h3>Use it for</h3><ul><li>Hiding plumbing or a rough floor under a wall hung vanity</li><li>Bathrooms "
        "where a built-in look is wanted</li></ul>"
        "<h3>Specifications</h3><ul><li>Sizes: 750, 900 and 1200mm wide (board measures 740, 890 and 1190mm)</li>"
        "<li>Height: 425mm</li><li>Depth: 200mm</li><li>Board: 16mm</li>"
        f"<li>Finish: {MAL_FIN[col]}</li><li>Model: KB-750, KB-900, KB-1200</li></ul>"
        "<h3>Good to know</h3><ul><li>Turns a Malaga wall hung vanity into a floor-standing one</li><li>Order the "
        "same width as your vanity</li><li>Seal the bottom edge where it meets the floor in a wet area</li></ul>",
        [SUP, CDN + "ETKB-750AO_1.png"], True, "Board width and thickness from supplier diagram.")

for col in ["Antico Oak", "Dark Oak", "Matt White"]:
    h = "malaga-" + col.lower().replace(" ", "-") + "-cubby-cabinet-300mm"
    add(h,
        f"<p>The Malaga {col} Cubby Cabinet is a 300mm open shelf unit that sits beside a Malaga wall hung vanity "
        "for towels and baskets. Three open compartments and the same height, depth and finish as the vanity, so "
        "the two read as one piece.</p>"
        "<h3>Use it for</h3><ul><li>Extra storage next to a vanity</li><li>Filling a gap between the vanity and the "
        "wall</li></ul>"
        "<h3>Specifications</h3><ul><li>Width: 300mm (264mm clear inside)</li><li>Height: 630mm</li>"
        "<li>Depth: 455mm</li><li>Two fixed shelves, three open compartments</li>"
        f"<li>Finish: {MAL_FIN[col]}</li><li>Model: CUB</li></ul>"
        "<h3>Good to know</h3><ul><li>Matches the Malaga vanity range</li><li>Wall hung; fix to studs or a "
        "noggin</li><li>A single door version is listed separately in Matt White</li></ul>",
        [SUP, CDN + "ETCUB_20AO_1.png"], True, "Dimensions from supplier diagram.")

add("malaga-matt-white-single-door-cabinet-295mm",
    "<p>The Malaga Matt White Single Door Cabinet is a 295mm wide side cabinet with one finger-pull door and a shelf "
    "inside, made to sit beside a Malaga wall hung vanity. It hides the bits you do not want on show and matches "
    "the vanity in height, depth and finish.</p>"
    "<h3>Use it for</h3><ul><li>Closed storage next to a vanity</li><li>Filling a gap between the vanity and the "
    "wall</li></ul>"
    "<h3>Specifications</h3><ul><li>Width: 295mm (259mm clear inside)</li><li>Height: 630mm</li>"
    "<li>Depth: 450mm</li><li>One door with finger pull, one internal shelf</li>"
    "<li>Finish: Matt White painted finish</li><li>Model: SDC</li></ul>"
    "<h3>Good to know</h3><ul><li>Matches the Malaga vanity range</li><li>Wall hung; fix to studs or a noggin</li>"
    "<li>An open cubby version is listed separately</li></ul>",
    [SUP, CDN + "ETSDC_20W_1.png"], True, "Dimensions from supplier diagram.")

# ---------------- Mirror ----------------
add("capsule-led-oval-backlit-mirror-450-x-900mm",
    "<p>The Capsule LED Oval Backlit Mirror is a 450 x 900mm pill-shaped mirror with LED light behind the glass, so "
    "it throws a soft halo onto the wall instead of glaring at you. Touch the sensor to change between three light "
    "tones, and the built-in demister keeps the glass clear after a shower.</p>"
    "<h3>Use it for</h3><ul><li>Vanities in ensuites and main bathrooms</li><li>Powder rooms where a tall narrow "
    "mirror suits the wall</li></ul>"
    "<h3>Features</h3><ul><li>Backlit LED with three light tones, changed at the touch sensor</li>"
    "<li>Built-in demister with its own touch sensor</li><li>Can be hung portrait or landscape</li></ul>"
    "<h3>Specifications</h3><ul><li>Size: 450 x 900mm</li><li>Power: 220-240V AC 50/60Hz</li>"
    "<li>Model: MIRBLEDOVAL</li></ul>"
    "<h3>What's in the box</h3><ul><li>Mirror, wall mounting screws and anchor plugs, in extra strong packaging</li></ul>"
    "<h3>Good to know</h3><ul><li>Must be installed by a licensed electrician in accordance with local "
    "regulations</li><li>Allow for a power point or hard-wired connection behind the mirror</li></ul>",
    [SUP, "https://eternitytiles.com.au/products/capsule-led-oval-back-lit", CDN + "2.jpg"], True,
    "Features confirmed on distributor product page; orientation listed both ways there.")

# ---------------- assemble ----------------
BAD = re.compile(r"\$|\btrade\b|stock|showroom|Maddington|deliver|pick up|shipping|Eternity|\bDSA\b|Bathroom City|"
                 r"elevate|stunning|seamless|!|—|curated|timeless|discover|unlock|premium quality|look no further|"
                 r"perfect for any|transform|\bMOQ\b|supplier|link in bio", re.I)
out, errs = [], []
for t in todo:
    h = t["handle"]
    if h not in D:
        errs.append(f"MISSING {h}"); continue
    html, src, ver, notes = D[h]
    words = len(re.sub(r"<[^>]+>", " ", html).split())
    if not 90 <= words <= 200:
        errs.append(f"WORDS {words} {h}")
    m = BAD.search(re.sub(r"<[^>]+>", " ", html))
    if m:
        errs.append(f"BAD '{m.group()}' {h}")
    old = sup.get(t["title"], {}).get("descriptionHtml", "")
    out.append({"id": t["id"], "handle": h, "title": t["title"], "old": old, "new": html,
                "sources": src, "verified": ver, "notes": notes, "words": words})
print(len(out), "records;", sum(o["verified"] for o in out), "verified")
for e in errs: print(e)
json.dump(out, open(f"{ROOT}/descriptions/ets-bathroomware-hardware-2026-10-24.json", "w"), indent=1, ensure_ascii=False)
sys.exit(1 if errs else 0)
