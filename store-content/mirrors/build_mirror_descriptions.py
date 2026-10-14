"""Builds the MELA mirror / LED mirror / mirror-cabinet descriptions and spec metafields
written to Shopify on 13 Oct 2026, after a customer asked for more detail (light colour etc.).

Source: Bathroom City (MELA's distributor) product pages - the "Product information" block,
the MELA spec sheets (PNG drawings) and the MELA warranty and care PDFs linked from each page.
Output: mirror-descriptions-2026-10-13.json (one entry per product: id, handle, tags to add,
metafields, descriptionHtml).
"""
import json, html

CARE = ("Clean with a 30% methylated spirits / 70% water mix on a soft cloth. Keep water off the back and "
        "edges and wipe around the edge to stop salt and calcium build-up. Do not use Windex or similar glass "
        "cleaners, bleach, ammonia, acidic cleaners, alcohol or mineral-based solvents, or abrasive pads.")
CAB_CARE = CARE + " Dry the cabinet with a soft cloth after use; do not let it stay wet."

W_MIRROR = "3 years on the mirror (MELA)"
W_CAB = "5 years cabinet, 3 years mirror, 1 year finish and hinges (MELA)"

LED_COMMON = [
    ("Light", "Backlit LED halo around the full edge of the mirror, giving even, shadow-free light at the vanity"),
    ("Light colour", "{colour}"),
    ("Control", "Touch button on the mirror face for on/off and brightness (dimmable)"),
    ("Anti-fog", "Built-in demister pad keeps the centre of the mirror clear after a hot shower"),
    ("Power", "220–240 V, plug-in or hard-wired; hard-wiring must be done by a licensed electrician"),
    ("Rating", "IP44 splash protection, SAA approved"),
    ("Mounting", "Wall-mounted on the supplied brackets"),
    ("Warranty", "3 years on the mirror (MELA)"),
]
COOL = "Cool white (single colour), dimmable"
TRI = "Three settings: warm white, natural white and cool white, switched from the touch button; dimmable"
WHITE = "Cool white (single colour), dimmable"

def ul(items):
    return "<ul>" + "".join(f"<li><strong>{html.escape(k)}:</strong> {v}</li>" for k, v in items) + "</ul>"

def desc(intro, items, outro=None):
    s = f"<p>{intro}</p>" + ul(items)
    if outro:
        s += f"<p>{outro}</p>"
    return s

CARE_LINE = ("Care", "Clean with 30% methylated spirits in water on a soft cloth. No Windex-type glass cleaners, bleach, ammonia or abrasives, and keep water off the back and edges")

P = {}

# ---------- LED mirrors ----------
def led(colour):
    return [(k, v.format(colour=colour)) for k, v in LED_COMMON]

P["mela-suri-led-round-mirror"] = dict(
    tags=["Anti Fog", "IP44", "Backlit Mirror", "Round LED Mirror"],
    metafields=dict(range="MELA SURI", material="Silver mirror, frameless, backlit LED", installation="Wall-mounted brackets; plug-in or hard-wired (licensed electrician)", warranty=W_MIRROR, care=CARE),
    html=desc(
        "The MELA SURI LED round mirror is a frameless round bathroom mirror with a backlit LED halo, touch dimmer and anti-fog demister. Four diameters cover a powder room up to a double vanity.",
        [("Sizes", "600 mm (SURI.600.LED), 700 mm (SURI.700R.LED), 800 mm (SURI.800R.LED) and 900 mm (SURI.900R.LED) diameter"),
         ("Shape", "Round, frameless with a polished edge")] + led(WHITE) + [CARE_LINE],
        "Pairs with the MELA SURI frameless and framed round mirrors and the SURI 800 round mirror cabinet.")
)

P["mela-mia-450-led-oval-mirror"] = dict(
    tags=["Backlit Mirror", "Oval LED Mirror"],
    metafields=dict(range="MELA MIA", material="5 mm copper-free silver mirror, acrylic frame, backlit LED", installation="Wall-mounted brackets; plug-in or hard-wired (licensed electrician)", warranty=W_MIRROR, care=CARE, width_mm=450, height_mm=900),
    html=desc(
        "The MELA MIA 450 LED oval mirror is a tall pill-shaped mirror with a backlit LED halo, touch dimmer and anti-fog demister. It suits a single vanity, powder room or ensuite where wall width is tight.",
        [("Size", "450 mm wide × 900 mm high (MIA.450.LED)"),
         ("Shape", "Vertical oval (pill) with a slim acrylic frame"),
         ("Mirror", "5 mm copper-free mirror, anti-fog")] + led(COOL) + [CARE_LINE],
        "Pairs with the MELA MIA 450 frameless and framed oval mirrors and the MIA 450 oval mirror cabinet.")
)

P["mela-vera-led-oval-mirror"] = dict(
    tags=["Anti Fog", "IP44", "Backlit Mirror", "Oval LED Mirror"],
    metafields=dict(range="MELA VERA", material="Silver mirror, frameless, backlit LED", installation="Wall-mounted brackets; plug-in or hard-wired (licensed electrician)", warranty=W_MIRROR, care=CARE),
    html=desc(
        "The MELA VERA LED horizontal oval mirror runs a soft LED halo around the full edge of a wide, frameless oval. The 900 suits a single vanity and the 1200 a double vanity.",
        [("Sizes", "900 mm wide × 600 mm high (VERA.900.LED) and 1200 mm wide × 750 mm high (VERA.1200.LED)"),
         ("Shape", "Horizontal oval, frameless with a polished edge")] + led(WHITE) + [CARE_LINE],
        "Pairs with the MELA VERA plain oval mirror and the VERA oval mirror cabinet.")
)

P["mela-zoe-600-led-arch-mirror"] = dict(
    tags=["Anti Fog", "IP44", "Backlit Mirror", "Arch LED Mirror"],
    metafields=dict(range="MELA ZOE", material="Silver mirror, frameless, backlit LED", installation="Wall-mounted brackets; plug-in or hard-wired (licensed electrician)", warranty=W_MIRROR, care=CARE, width_mm=600, height_mm=900),
    html=desc(
        "The MELA ZOE 600 LED arch mirror traces an LED halo around a frameless arch, with a touch dimmer and anti-fog demister. It gives a single vanity or powder room height without a frame.",
        [("Size", "600 mm wide × 900 mm high (ZOE.600.LED), 300 mm arch radius"),
         ("Shape", "Arch, frameless with a polished edge")] + led(TRI) + [CARE_LINE],
        "Pairs with the MELA ZOE 600 frameless and framed arch mirrors and the ZOE 600 arch mirror cabinet.")
)

# ---------- plain and framed mirrors ----------
TG = ("Mounting", "Tongue-and-groove wall bracket (supplied); hangs flush and level with no visible fixings")
THICK = ("Mirror", "3.2 mm silver mirror, Australian Standard certified")

P["mela-suri-frameless-round-mirror"] = dict(
    tags=["Polished Edge Mirror"],
    metafields=dict(range="MELA SURI", material="3.2 mm silver mirror, frameless, polished edge", installation="Tongue-and-groove wall bracket", warranty=W_MIRROR, care=CARE),
    html=desc(
        "The MELA SURI frameless round mirror is a plain round bathroom mirror with a polished edge and no frame, so it sits almost flat to the wall.",
        [("Sizes", "700 mm (SURI.700R), 800 mm (SURI.800R) and 900 mm (SURI.900R) diameter"),
         ("Depth", "About 5 mm off the wall"), THICK, TG,
         ("Warranty", W_MIRROR), CARE_LINE],
        "Also available with a thin metal frame (MELA SURI framed round mirror), with LED backlighting, or as the SURI 800 round mirror cabinet.")
)

P["mela-suri-framed-round-mirror"] = dict(
    tags=["Metal Frame Mirror"],
    metafields=dict(range="MELA SURI", material="3.2 mm silver mirror with thin metal frame", installation="Tongue-and-groove wall bracket", warranty=W_MIRROR, care=CARE, depth_mm=30),
    html=desc(
        "The MELA SURI framed round mirror adds a thin metal frame to the SURI round mirror. The frame colours match MELA tapware and accessories, so the mirror ties in with the rest of the bathroom.",
        [("Sizes", "700 mm, 800 mm and 900 mm diameter"),
         ("Frame finishes", "Matt Black (SURI.700RF.BK / 800RF.BK / 900RF.BK), Gun Metal (…RF.GM) and Brushed Brass (…RF.BB)"),
         ("Frame", "Thin metal frame, 30 mm deep"), THICK, TG,
         ("Warranty", W_MIRROR), CARE_LINE],
        "Also available frameless, with LED backlighting, or as the SURI 800 round mirror cabinet.")
)

P["mela-mia-450-frameless-oval-mirror"] = dict(
    tags=["Polished Edge Mirror"],
    metafields=dict(range="MELA MIA", material="3.2 mm silver mirror, frameless, polished edge", installation="Tongue-and-groove wall bracket", warranty=W_MIRROR, care=CARE, width_mm=450, height_mm=900),
    html=desc(
        "The MELA MIA 450 frameless oval mirror is a tall pill-shaped mirror with a polished edge and no frame. At 450 mm wide it fits a narrow vanity or powder room wall.",
        [("Size", "450 mm wide × 900 mm high (MIA.450), 225 mm end radius"),
         ("Depth", "About 5 mm off the wall"), THICK, TG,
         ("Warranty", W_MIRROR), CARE_LINE],
        "Also available with a thin metal frame, with LED backlighting, or as the MIA 450 oval mirror cabinet.")
)

P["mela-mia-450-framed-oval-mirror"] = dict(
    tags=["Metal Frame Mirror"],
    metafields=dict(range="MELA MIA", material="3.2 mm silver mirror with thin metal frame", installation="Tongue-and-groove wall bracket", warranty=W_MIRROR, care=CARE, width_mm=450, height_mm=900, depth_mm=30),
    html=desc(
        "The MELA MIA 450 framed oval mirror outlines the tall MIA pill shape with a thin metal frame in a finish that matches MELA tapware.",
        [("Size", "450 mm wide × 900 mm high"),
         ("Frame finishes", "Matt Black (MIA.450F.BK), Brushed Brass (MIA.450F.BB) and Gun Metal (MIA.450F.GM)"),
         ("Frame", "Thin metal frame, 30 mm deep"), THICK, TG,
         ("Warranty", W_MIRROR), CARE_LINE],
        "Also available frameless, with LED backlighting, or as the MIA 450 oval mirror cabinet.")
)

P["mela-zoe-600-frameless-arch-mirror"] = dict(
    tags=["Polished Edge Mirror"],
    metafields=dict(range="MELA ZOE", material="3.2 mm silver mirror, frameless, polished edge", installation="Tongue-and-groove wall bracket", warranty=W_MIRROR, care=CARE, width_mm=600, height_mm=900),
    html=desc(
        "The MELA ZOE 600 frameless arch mirror is a plain arch-top mirror with a polished edge and no frame. The arch gives a single vanity some height without a heavy frame.",
        [("Size", "600 mm wide × 900 mm high (ZOE.600), 300 mm arch radius"),
         ("Depth", "About 5 mm off the wall"), THICK, TG,
         ("Warranty", W_MIRROR), CARE_LINE],
        "Also available with a thin metal frame, with LED backlighting, or as the ZOE 600 arch mirror cabinet.")
)

P["mela-zoe-600-framed-arch-mirror"] = dict(
    tags=["Metal Frame Mirror"],
    metafields=dict(range="MELA ZOE", material="3.2 mm silver mirror with thin metal frame", installation="Tongue-and-groove wall bracket", warranty=W_MIRROR, care=CARE, width_mm=600, height_mm=900, depth_mm=30),
    html=desc(
        "The MELA ZOE 600 framed arch mirror puts a thin metal frame around the ZOE arch, in a finish that matches MELA tapware and accessories.",
        [("Size", "600 mm wide × 900 mm high, 300 mm arch radius"),
         ("Frame finishes", "Matt Black (ZOE.600F.BK), Gun Metal (ZOE.600F.GM) and Brushed Brass (ZOE.600F.BB)"),
         ("Frame", "Thin metal frame, 30 mm deep"), THICK, TG,
         ("Warranty", W_MIRROR), CARE_LINE],
        "Also available frameless, with LED backlighting, or as the ZOE 600 arch mirror cabinet.")
)

P["mela-vera-oval-mirror"] = dict(
    tags=["Polished Edge Mirror", "Frameless Mirror"],
    metafields=dict(range="MELA VERA", material="Silver mirror, frameless, polished edge", installation="Tongue-and-groove wall bracket", warranty=W_MIRROR, care=CARE),
    html=desc(
        "The MELA VERA horizontal oval mirror is a wide, frameless oval with a polished edge. The 900 suits a single vanity and the 1200 a double vanity.",
        [("Sizes", "900 mm wide × 600 mm high (VERA.900) and 1200 mm wide × 750 mm high (VERA.1200)"),
         ("Shape", "Horizontal oval, frameless, polished edge"), TG,
         ("Warranty", W_MIRROR), CARE_LINE],
        "Also available with LED backlighting (MELA VERA LED oval mirror) or as the VERA oval mirror cabinet.")
)

P["mela-vina-plain-mirror"] = dict(
    tags=["Frameless Mirror", "Rectangular Mirror"],
    metafields=dict(range="MELA VINA", material="Silver mirror, frameless, polished edge, rounded corners", installation="Tongue-and-groove wall bracket", warranty=W_MIRROR, care=CARE, height_mm=750),
    html=desc(
        "The MELA VINA plain mirror is a frameless rectangular bathroom mirror with a polished edge and softly rounded polished corners. Six widths run from a powder room to an 1800 mm double vanity.",
        [("Widths", "600 mm (VIN.600P), 750 mm (VIN.750P), 900 mm (VIN.900P), 1200 mm (VIN.1200P), 1500 mm (VIN.1500P) and 1800 mm (VIN.1800P)"),
         ("Height", "750 mm for every width"),
         ("Edge", "Polished edge with curved polished corners"), TG,
         ("Warranty", W_MIRROR), CARE_LINE])
)

# ---------- mirror cabinets ----------
CAB_MAT = "3.2 mm silver mirror door on a moisture-resistant particle board carcass, light grey inside"
SCREW = ("Mounting", "Screws to the wall through the back of the cabinet")
CAB_W = ("Warranty", W_CAB)
CAB_CARE_LINE = ("Care", "Clean the mirror with 30% methylated spirits in water; no Windex-type cleaners, bleach, ammonia or abrasives. Dry the cabinet with a soft cloth after use")

P["mela-mia-450-oval-mirror-cabinet"] = dict(
    tags=["Shaving Cabinet"],
    metafields=dict(range="MELA MIA", material=CAB_MAT, installation="Screw to wall", warranty=W_CAB, care=CAB_CARE, width_mm=450, height_mm=900, depth_mm=116),
    html=desc(
        "The MELA MIA 450 oval mirror cabinet is the MIA pill-shaped mirror with a storage cabinet behind it. The mirror door hides a light grey cabinet with adjustable shelves and a small internal mirror.",
        [("Mirror", "450 mm wide × 900 mm high, 116 mm off the wall (MIA.450.MC.1)"),
         ("Cabinet behind", "420 mm wide × 480 mm high × 104 mm deep, light grey carcass"),
         ("Storage", "Adjustable shelves plus a small round mirror inside the door"),
         ("Material", CAB_MAT), SCREW, CAB_W, CAB_CARE_LINE],
        "Also available as the MIA 450 frameless, framed and LED oval mirrors.")
)

P["mela-suri-800-round-mirror-cabinet"] = dict(
    tags=["Shaving Cabinet"],
    metafields=dict(range="MELA SURI", material=CAB_MAT, installation="Screw to wall", warranty=W_CAB, care=CAB_CARE, width_mm=800, height_mm=800, depth_mm=143),
    html=desc(
        "The MELA SURI 800 round mirror cabinet looks like a plain 800 mm round mirror but opens to a light grey storage cabinet with adjustable shelves.",
        [("Mirror", "800 mm diameter, 143 mm off the wall (SURI.800.MC.1)"),
         ("Cabinet behind", "550 mm wide × 500 mm high × 128 mm deep, light grey carcass"),
         ("Storage", "Three adjustable shelves; the door is hinged on the left"),
         ("Material", CAB_MAT), SCREW, CAB_W, CAB_CARE_LINE],
        "Also available as the SURI frameless, framed and LED round mirrors.")
)

P["mela-zoe-600-arch-mirror-cabinet"] = dict(
    tags=["Shaving Cabinet"],
    metafields=dict(range="MELA ZOE", material=CAB_MAT, installation="Screw to wall", warranty=W_CAB, care=CAB_CARE, width_mm=600, height_mm=900, depth_mm=116),
    html=desc(
        "The MELA ZOE 600 arch mirror cabinet is the ZOE arch mirror with a storage cabinet behind the lower part of the mirror, so the arch stays clean while toiletries stay hidden.",
        [("Mirror", "600 mm wide × 900 mm high, 116 mm off the wall (ZOE.600.MC.1)"),
         ("Cabinet behind", "580 mm wide × 608 mm high × 102 mm deep, light grey carcass"),
         ("Storage", "Adjustable shelves"),
         ("Material", CAB_MAT), SCREW, CAB_W, CAB_CARE_LINE],
        "Also available as the ZOE 600 frameless, framed and LED arch mirrors.")
)

P["mela-vera-oval-mirror-cabinet"] = dict(
    tags=["Shaving Cabinet"],
    metafields=dict(range="MELA VERA", material=CAB_MAT, installation="Tongue-and-groove wall mounting", warranty=W_CAB, care=CAB_CARE, depth_mm=140),
    html=desc(
        "The MELA VERA oval mirror cabinet is the wide VERA oval mirror with storage behind it. The 900 suits a single vanity and the 1200 a double vanity, with a light grey interior and adjustable shelves.",
        [("Sizes", "900 mm wide × 600 mm high (VERA.900.MC) and 1200 mm wide × 750 mm high (VERA.1200.MC), both 140 mm deep"),
         ("Doors", "Two- or three-door layout depending on size"),
         ("Storage", "Adjustable shelves, light grey carcass"),
         ("Material", CAB_MAT), ("Mounting", "Tongue-and-groove wall mounting"), CAB_W, CAB_CARE_LINE],
        "Also available as the VERA plain and LED oval mirrors.")
)

P["mela-porter-mirror-cabinet"] = dict(
    tags=["Shaving Cabinet"],
    metafields=dict(range="MELA PORTER", material="High-moisture-resistant (HMR) timber laminate with 18 mm backing board, mirrored doors", installation="Wall-mounted on cabinet brackets; arrives fully assembled", warranty=W_CAB, care=CAB_CARE, height_mm=720, depth_mm=140),
    html=desc(
        "The MELA PORTER mirror cabinet is a square-edged mirror cabinet with handle-free mirrored doors, made from high-moisture-resistant board. Four widths and four finishes match the MELA vanity range.",
        [("Widths", "600 mm and 750 mm (two doors), 900 mm (two doors) and 1200 mm (three doors)"),
         ("Height and depth", "About 720 mm high × 140 mm deep; internal shelf depth 94 mm"),
         ("Finishes", "Gloss White (POR.xxx.GW), Snafell (…SF), Sorrento Oak (…SO) and Walnut (…WN)"),
         ("Storage", "Adjustable shelves behind each door"),
         ("Doors", "Handle-free square-edge mirror doors on integrated European (DTC) hinges"),
         ("Material", "High-moisture-resistant timber laminate, 18 mm backing board"),
         ("Delivery", "Comes fully assembled with wall-mounting brackets"),
         CAB_W, CAB_CARE_LINE])
)

json.dump(P, open(__file__.replace("build_mirror_descriptions.py", "mirror-descriptions-2026-10-13.json"), "w"), indent=1, ensure_ascii=False)
print(len(P), "products")
for h, p in P.items():
    print(h, len(p["html"]))
