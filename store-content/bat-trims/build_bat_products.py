"""Build Shopify product data for the BAT Trims 2023/24 catalogue.

Source: "2023-24 BAT Trims Catalogue.pdf" (BAT Trims Pty Ltd, V-06/23), sent by Adam (BAT Perth).
Every product family in the catalogue becomes one Shopify product; sizes, colours and finishes
become variants. SKUs are BAT's own codes with "(Colour)" replaced by the colour code.

Prices are not in the catalogue. Products are created as DRAFT at $0 and tagged `price-needed`
until Adam's trade price list arrives (see README.md).

Run:  python3 build_bat_products.py   -> bat-products.json, bat-variants.csv
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

COLOURS = {
    "ALA": "Alabaster", "AB": "Antique Brass", "BG": "Bright Gold", "BA": "Bronze Ash",
    "BK": "Black", "BS": "Bright Silver", "CP": "Chrome Plated", "GM": "Gunmetal Grey",
    "LB": "Linished Black", "LC": "Linished Copper", "LG": "Linished Gold", "LI": "Linished Iron",
    "LM": "Linished Matt Gold", "LS": "Linished Silver", "MBK": "Matt Black", "MS": "Matt Silver",
    "MW": "Matt White", "MF": "Mill Finish", "MM": "Monument Matt", "WH": "Pearl White",
    "GR": "Grey",
}
# 2023 finishes, only in the sizes BAT lists for them (catalogue p. 6-11).
NEW_COLOUR_SIZES = {
    "AB": ["8", "10", "11", "12"], "LC": ["8", "10", "11", "12"], "LI": ["8", "10", "11", "12"],
    "MM": ["8", "10", "11", "12"], "LM": ["8", "9", "10", "11", "12"], "GM": ["8", "9", "10", "11", "12"],
}

DENSITY = {"aluminium": 2.7, "brass": 8.5, "stainless": 7.9, "pvc": 1.4}
PACK_KG = 0.15  # cardboard / sleeve per length


def length_kg(area_mm2, metres, metal):
    """Weight of one length from its cross-section area (mm2)."""
    return round(area_mm2 * DENSITY[metal] * 1e-3 * metres + PACK_KG, 2)


def box_for(metres, w=8, h=6):
    return f"{int(round(metres * 100)) + 5} x {w} x {h} cm"


def mm(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s


CARE = (
    "<p><strong>Care:</strong> wash finished trims with warm soapy water and a soft cloth. "
    "Don't use acid or alkaline cleaners, scourers or sandpaper on coloured, anodised or plated finishes. "
    "Remove greasy marks with white spirits, then rinse with clean water.</p>"
)
WHY_BAT = (
    "<p>BAT Trims is an Australian family business, making tiling trims in Dandenong, Victoria since 1985. "
    "Order through Excellent Tiling Services in Maddington, Perth.</p>"
)


def desc(intro, specs, extra=""):
    lis = "".join(f"<li>{s}</li>" for s in specs)
    return f"<p>{intro}</p>{extra}<ul>{lis}</ul>{CARE}{WHY_BAT}"


PRODUCTS = []


def add(handle, title, ptype, intro, specs, options, variants, image, metres, ship,
        seo_title, seo_desc, extra_tags=(), extra_html="", gallery=(), variant_images=None):
    """variants: list of dicts {options: {name: value}, sku, weight, box}."""
    tags = ["BAT Trims", "BAT", "Hardware", "Tile Trims + Edging Profiles", "supplier-bat",
            "price-needed", "bat-catalogue-2023-24"] + list(extra_tags)
    if ship == "local":
        tags += ["ship-local-only", "ship-long"]
    else:
        tags += ["ship-parcel"]
    PRODUCTS.append({
        "handle": handle, "title": title, "productType": ptype, "vendor": "BAT Trims",
        "descriptionHtml": desc(intro, specs, extra_html), "tags": tags,
        "seo": {"title": seo_title, "description": seo_desc},
        "options": options, "variants": variants, "image": image, "gallery": list(gallery),
        "variant_images": variant_images or {}, "ship": ship, "metres": metres,
    })


def v(opts, sku, weight, box):
    return {"options": opts, "sku": sku, "weight": weight, "box": box}


# ---------------------------------------------------------------- p.13 Geometric angle
geo_al = [(12, 12, 1.6), (12, 20, 1.6), (12, 40, 1.6), (20, 20, 1.6), (20, 25, 1.6), (20, 32, 1.6),
          (20, 40, 1.6), (25, 25, 1.6), (25, 40, 1.6), (25, 50, 1.6), (32, 32, 1.6), (40, 40, 1.6),
          (40, 50, 1.6), (50, 50, 1.6),
          (20, 20, 3), (20, 25, 3), (20, 32, 3), (25, 25, 3), (25, 32, 3), (25, 40, 3), (25, 50, 3),
          (32, 32, 3), (40, 40, 3), (50, 50, 3), (60, 60, 3)]
vs = []
for a, b, c in geo_al:
    code = f"AA-{a}{b}{'16' if c == 1.6 else '3'}-3"
    for col in ["MF", "BS", "MBK"]:
        vs.append(v({"Size": f"{a} x {b} x {mm(c)}mm", "Colour": COLOURS[col]}, f"{code}-{col}",
                    length_kg((a + b - c) * c, 3, "aluminium"), box_for(3, 8, 8)))
add("bat-aluminium-geometric-angle-3m", "BAT Aluminium Geometric Angle – 3m Lengths", "L Shaped Trim",
    "A plain equal or unequal aluminium angle with no perforated leg. Use it for waterproofing edges, or "
    "fix it over finished tiling to cover chips and damage on an external corner.",
    ["Material: aluminium", "Length: 3m", "Thickness: 1.6mm or 3.0mm",
     "Sizes: 12 x 12mm up to 60 x 60mm (leg A x leg B x thickness)",
     "Finishes: Mill Finish, Bright Silver, Matt Black (anodised or powder coated; other colours on request)"],
    ["Size", "Colour"], vs, "e-013-055.png", 3, "local",
    "BAT Aluminium Geometric Angle 3m | Plain L Angle | ETS Perth",
    "BAT aluminium geometric angle, 3m lengths, 1.6mm and 3mm thick, 12mm to 60mm legs. Mill, silver or matt black. Order in Perth from ETS.")

geo_br = [("BA-1216-36", 12.70, 12.70, 1.59), ("BA-1916-36", 19.05, 19.05, 1.59), ("BA-2516-36", 25.40, 25.40, 1.59),
          ("BA-2532-36", 25.40, 25.40, 3.18), ("BA-25403-36", 25.40, 38.10, 3.18), ("BA-3132-36", 31.75, 31.75, 3.18),
          ("BA-3832-36", 38.10, 38.10, 3.18), ("BA-5032-36", 50.80, 50.80, 3.18)]
geo_ss = [("SSA-203-3", 20, 20, 3), ("SSA-253-3", 25, 25, 3), ("SSA-303-3", 30, 30, 3), ("SSA-403-3", 40, 40, 3),
          ("SSA-503-3", 50, 50, 3), ("SSA-255-3", 25, 25, 5), ("SSA-305-3", 30, 30, 5), ("SSA-405-3", 40, 40, 5),
          ("SSA-505-3", 50, 50, 5), ("SSA-256-3", 25, 25, 6), ("SSA-406-3", 40, 40, 6), ("SSA-506-3", 50, 50, 6)]
vs = []
for code, a, b, c in geo_br:
    vs.append(v({"Material": "Brass (3.6m)", "Size": f"{mm(a)} x {mm(b)} x {mm(c)}mm"}, code,
                length_kg((a + b - c) * c, 3.6, "brass"), box_for(3.6, 8, 8)))
for code, a, b, c in geo_ss:
    vs.append(v({"Material": "Stainless Steel 304 (3m)", "Size": f"{mm(a)} x {mm(b)} x {mm(c)}mm"}, code,
                length_kg((a + b - c) * c, 3, "stainless"), box_for(3, 8, 8)))
add("bat-brass-stainless-geometric-angle", "BAT Brass & Stainless Steel Geometric Angle", "L Shaped Trim",
    "Solid brass and grade 304 stainless steel angle with plain legs, for waterproofing edges, step and "
    "bench edges, and covering damaged corners on finished tiling. Heavier and harder wearing than aluminium.",
    ["Brass: mill finish, 3.6m lengths, 12.7mm to 50.8mm legs, 1.59mm or 3.18mm thick (chrome plated on request)",
     "Stainless steel: grade 304, HRAP mill finish (hot rolled, annealed and pickled), 3m lengths, 20mm to 50mm legs, 3mm, 5mm or 6mm thick",
     "Other sizes available on request"],
    ["Material", "Size"], vs, "e-013-057.png", 3.6, "local",
    "BAT Brass & Stainless Steel Geometric Angle | ETS Perth",
    "Solid brass (3.6m) and 304 stainless steel (3m) plain angle for tiling, waterproofing and corner protection. Order from ETS Perth.",
    gallery=["e-013-056.png"])

# ---------------------------------------------------------------- p.14 Aluminium tiling angle
al_angle = [("4", 4.5, 22, 2.0), ("6", 6.0, 20, 2.5), ("8", 8.0, 20, 2.8), ("9", 9.0, 22, 2.8), ("10", 10, 22, 2.8),
            ("11", 11, 22, 2.8), ("12", 12.5, 23, 2.8), ("13", 13.5, 23, 2.8), ("15", 15, 23, 2.8),
            ("17", 17, 23, 2.8), ("18", 18.5, 23, 2.8), ("20", 20, 23, 2.8), ("22", 22, 23, 2.8),
            ("23", 23, 23, 2.8), ("25", 25.5, 23, 2.8)]
std_cols = ["MF", "BS", "MS", "LS", "BK", "MBK", "LB", "MW", "WH", "ALA", "BG", "LG", "BA"]
new_cols = ["AB", "LC", "LI", "LM", "MM", "GM"]
vs = []
for code, a, b, c in al_angle:
    for col in std_cols + new_cols:
        if col in NEW_COLOUR_SIZES and code not in NEW_COLOUR_SIZES[col]:
            continue
        vs.append(v({"Size": f"{mm(a)}mm", "Colour": COLOURS[col]}, f"AA-{code}-3-{col}",
                    length_kg(b * 1.0 + a * 1.2 + c * 1.0, 3, "aluminium"), box_for(3)))
add("bat-aluminium-tiling-angle-3m", "BAT Aluminium Tiling Angle – 3m Lengths (19 Colours)", "L Shaped Trim",
    "BAT's aluminium L angle protects the exposed edge of wall and floor tiles from chipping, and can be set "
    "between two floor finishes as a border strip. It comes in 15 sizes and 19 finishes, including the 2023 "
    "designer colours Antique Brass, Linished Copper, Linished Iron, Linished Matt Gold, Monument Matt and Gunmetal Grey, "
    "made to match brass, copper, gunmetal and black tapware.",
    ["Material: aluminium, perforated fixing leg", "Length: 3m",
     "Sizes (tile thickness): 4.5, 6, 8, 9, 10, 11, 12.5, 13.5, 15, 17, 18.5, 20, 22, 23 and 25.5mm",
     "Finishes: Mill Finish, Bright Silver, Matt Silver, Linished Silver, Black, Matt Black, Linished Black, Matt White, "
     "Pearl White, Alabaster, Bright Gold, Linished Gold, Bronze Ash",
     "2023 designer finishes: Antique Brass, Linished Copper, Linished Iron, Monument Matt (8, 10, 11, 12.5mm); "
     "Linished Matt Gold, Gunmetal Grey (8, 9, 10, 11, 12.5mm)",
     "Choose the size that matches your tile thickness"],
    ["Size", "Colour"], vs, "e-014-059.png", 3, "local",
    "BAT Aluminium Tile Trim Angle 3m | 19 Colours | ETS Perth",
    "BAT aluminium tile edge angle in 15 sizes and 19 colours incl. Antique Brass, Copper, Gunmetal and Matt Gold. 3m lengths. Order in Perth.",
    extra_tags=["designer-colours"],
    gallery=["e-006-001.png", "e-007-003.png", "e-008-005.png", "e-009-008.png", "e-010-010.png", "e-011-013.png"],
    variant_images={"Antique Brass": "e-006-001.png", "Linished Copper": "e-007-003.png",
                    "Linished Iron": "e-008-005.png", "Linished Matt Gold": "e-009-008.png",
                    "Monument Matt": "e-010-010.png", "Gunmetal Grey": "e-011-013.png"})

# ---------------------------------------------------------------- p.14-15 Brass / CP brass angle
br_angle = [("4", 4.5), ("6", 6), ("8", 8), ("9", 9), ("10", 10), ("11", 11), ("12", 12.5), ("13", 13.5),
            ("15", 15), ("16", 16.5), ("18", 18.5), ("20", 20), ("22", 22), ("23", 23.5), ("25", 25)]
vs = []
for code, a in br_angle:
    w = length_kg(22 * 1.0 + a * 1.2 + 2.8, 3, "brass")
    vs.append(v({"Size": f"{mm(a)}mm", "Finish": "Brass"}, f"NBA-{code}-3", w, box_for(3)))
    vs.append(v({"Size": f"{mm(a)}mm", "Finish": "Chrome Plated"}, f"CPBA-{code}-3", w, box_for(3)))
add("bat-brass-tiling-angle-3m", "BAT Solid Brass Tiling Angle – 3m Lengths (Brass or Chrome)", "L Shaped Trim",
    "Solid brass L angle for tile edges, in natural brass or chrome plated to match chrome tapware. Brass is harder "
    "wearing and more chemical resistant than aluminium, so it suits busy floors, pool surrounds and wet areas.",
    ["Material: solid brass, perforated fixing leg", "Finish: natural brass or chrome plated", "Length: 3m",
     "Sizes: 4.5mm to 25mm (15 sizes)", "Fixing leg: 22mm"],
    ["Size", "Finish"], vs, "e-014-079.png", 3, "local",
    "BAT Brass Tile Trim Angle 3m | Brass or Chrome | ETS Perth",
    "Solid brass tile edge angle, natural brass or chrome plated, 4.5mm to 25mm, 3m lengths. Hard wearing. Order from ETS Perth.",
    gallery=["e-015-082.png"], variant_images={"Chrome Plated": "e-015-082.png"})

# ---------------------------------------------------------------- p.15 Stainless steel angle
vs = []
for code, a in [("3", 3), ("4", 4.5), ("6", 6), ("8", 8), ("10", 10), ("12", 12.5), ("15", 15), ("17", 17.5),
                ("20", 20), ("22", 22)]:
    vs.append(v({"Size": f"{mm(a)}mm"}, f"SSA-{code}-3", length_kg(24 * 0.8 + a * 1.0 + 1.9, 3, "stainless"), box_for(3)))
add("bat-stainless-steel-tiling-angle-3m", "BAT Stainless Steel Tiling Angle 304 – 3m Lengths", "L Shaped Trim",
    "Grade 304 stainless steel L angle with a rolled top edge, for tile edges that need to be tough and corrosion "
    "resistant: commercial kitchens, showers, balconies and pool areas. Marine grade 316 is available to order in 2.7m lengths.",
    ["Material: stainless steel grade 304", "Length: 3m", "Sizes: 3mm to 22mm (10 sizes)", "Fixing leg: 24mm",
     "Marine grade 316 (2.7m) on request"],
    ["Size"], vs, "e-015-083.png", 3, "local",
    "BAT Stainless Steel Tile Angle 304 3m | ETS Perth",
    "BAT 304 stainless steel tile edge angle, 3mm to 22mm, 3m lengths. Tough and rust resistant for wet and commercial areas.")

# ---------------------------------------------------------------- p.15 Notched aluminium angle
vs = []
for code, a, b, c in al_angle:
    if code == "25":
        a = 25  # notched table lists 25.00, the standard angle is 25.50
    for col in ["MF", "MS", "LS", "BK", "MBK", "MW", "WH"]:
        vs.append(v({"Size": f"{mm(a)}mm", "Colour": COLOURS[col]}, f"AA-{code}-3-N-{col}",
                    length_kg(b * 1.0 + a * 1.2 + c, 3, "aluminium"), box_for(3)))
add("bat-notched-aluminium-angle-3m", "BAT Notched Aluminium Tiling Angle – 3m Lengths (Bendable)", "Notched Trim",
    "Aluminium L angle with a notched fixing leg, so it bends around curved walls, round columns, curved steps and "
    "other curved tile edges. Same profile and sizes as BAT's standard tiling angle.",
    ["Material: aluminium, notched fixing leg for curves", "Length: 3m", "Sizes: 4.5mm to 25mm (15 sizes)",
     "Finishes: Mill Finish, Matt Silver, Linished Silver, Black, Matt Black, Matt White, Pearl White"],
    ["Size", "Colour"], vs, "e-015-084.png", 3, "local",
    "BAT Notched Aluminium Tile Angle | Bendable Trim | ETS",
    "Bendable notched aluminium tile trim for curved walls and steps. 15 sizes, 7 colours, 3m lengths. Order from ETS Perth.",
    gallery=["e-015-091.png"])

# ---------------------------------------------------------------- p.16 Flat bar
vs = []
for code, a, b in [("AF-1216-4", 12, 1.6), ("AF-2016-4", 20, 1.6), ("AF-2516-4", 25, 1.6), ("AF-103-4", 10, 3),
                   ("AF-123-4", 12, 3), ("AF-163-4", 16, 3), ("AF-203-4", 20, 3), ("AF-253-4", 25, 3),
                   ("AF-323-4", 32, 3), ("AF-403-4", 40, 3), ("AF-503-4", 50, 3)]:
    vs.append(v({"Material": "Aluminium (4m)", "Size": f"{mm(a)} x {mm(b)}mm"}, code, length_kg(a * b, 4, "aluminium"), box_for(4)))
for code, a, b in [("BF-1216-36", 12.70, 1.59), ("BF-932-36", 9.53, 3.18), ("BF-1232-36", 12.70, 3.18),
                   ("BF-1632-36", 15.88, 3.18), ("BF-1932-36", 19.05, 3.18), ("BF-2532-36", 25.40, 3.18),
                   ("BF-3132-36", 31.75, 3.18), ("BF-3832-36", 38.10, 3.18), ("BF-5032-36", 50.80, 3.18)]:
    vs.append(v({"Material": "Brass (3.6m)", "Size": f"{mm(a)} x {mm(b)}mm"}, code, length_kg(a * b, 3.6, "brass"), box_for(3.6)))
for code, a in [("SSFB-123-4", 12), ("SSFB-203-4", 20), ("SSFB-253-4", 25), ("SSFB-303-4", 30),
                ("SSFB-403-4", 40), ("SSFB-503-4", 50)]:
    vs.append(v({"Material": "Stainless Steel (4m)", "Size": f"{mm(a)} x 3mm"}, code, length_kg(a * 3, 4, "stainless"), box_for(4)))
add("bat-flat-bar-aluminium-brass-stainless", "BAT Flat Bar – Aluminium, Brass & Stainless Steel", "Tile Trims + Edging Profiles",
    "Flat metal bar for finishing a tiled area or making a clean dividing line between two finishes, such as tile to "
    "timber or tile to carpet. Supplied in mill finish; can be polished, anodised or powder coated to order.",
    ["Aluminium: 4m lengths, 10mm to 50mm wide, 1.6mm or 3mm thick",
     "Brass: 3.6m lengths, 9.53mm to 50.8mm wide, 1.59mm or 3.18mm thick",
     "Stainless steel: 4m lengths, 12mm to 50mm wide, 3mm thick",
     "Finish: mill finish (minor surface marks are normal)"],
    ["Material", "Size"], vs, "e-016-103.png", 4, "local",
    "BAT Flat Bar | Aluminium, Brass, Stainless | ETS Perth",
    "BAT flat bar in aluminium (4m), brass (3.6m) and stainless steel (4m) for tile dividers and edges. Order from ETS Perth.",
    gallery=["e-016-107.png", "e-016-105.png"],
    variant_images={"Brass (3.6m)": "e-016-107.png", "Stainless Steel (4m)": "e-016-105.png"})

# ---------------------------------------------------------------- p.17 PVC waterproofing angle, Birds mouth
vs = [v({"Size": s}, code, w, box_for(3, 10, 8)) for code, s, w in
      [("PVC-WPA40502-3", "40 x 50 x 2mm", 0.75), ("PVC-WPA755014-3", "75 x 50 x 1.4mm", 0.7),
       ("PVC-WPA75502-3", "75 x 50 x 2mm", 0.95)]]
add("bat-pvc-waterproofing-angle-3m", "BAT PVC Waterproofing Angle – 3m Lengths (White)", "PVC trim",
    "White PVC angle used as a barrier along the edge of a waterproofing membrane, such as shower hobs, "
    "set-downs and wet-area floor edges.",
    ["Material: PVC", "Colour: white", "Length: 3m", "Sizes: 40 x 50 x 2mm, 75 x 50 x 1.4mm, 75 x 50 x 2mm"],
    ["Size"], vs, "e-017-110.png", 3, "local",
    "BAT PVC Waterproofing Angle 3m | White | ETS Perth",
    "BAT white PVC waterproofing angle for membrane edges in showers and wet areas. 3 sizes, 3m lengths. Order from ETS Perth.")

vs = []
for s, a, c in [(8, 8, 31.2), (10, 10, 33.2), (12, 12.5, 35.7), (15, 15, 41.4), (20, 20, 46.4), (25, 25, 51.4)]:
    for col in ["MF", "MS"]:
        vs.append(v({"Size": f"{mm(a)}mm", "Colour": COLOURS[col]}, f"BMT-{s}-3-{col}",
                    length_kg((c + a * 2) * 1.2, 3, "aluminium"), box_for(3, 8, 8)))
add("bat-birds-mouth-trim-3m", "BAT Birds Mouth Trim – 3m Lengths", "Square edge",
    "Aluminium birds mouth trim gives a crisp square edge on columns and piers without mitring the tiles or stone. "
    "On flat walls it creates a shadow-line feature, and it can hold LED strip lighting for a lit edge.",
    ["Material: aluminium", "Length: 3m", "Sizes: 8, 10, 12.5, 15, 20 and 25mm",
     "Finishes: Mill Finish, Matt Silver (other colours on request)"],
    ["Size", "Colour"], vs, "e-017-111.png", 3, "local",
    "BAT Birds Mouth Trim 3m | Square Corner & LED Edge | ETS",
    "BAT aluminium birds mouth trim for square column corners, shadow lines and LED strip edges. 8mm to 25mm, 3m lengths.")

# ---------------------------------------------------------------- p.18 Mosaic corner angle / guard
vs = []
for s, a in [(4, 4.5), (6, 6.5), (8, 8.5), (10, 10.5), (12, 12.5), (15, 15)]:
    for col in ["MF", "BS", "MS", "LS", "BK", "MBK", "LB", "MW", "WH", "ALA", "BG", "LG", "BA"]:
        vs.append(v({"Size": f"{mm(a)}mm", "Colour": COLOURS[col]}, f"MCA-{s}-3-{col}",
                    length_kg((a * 2 + 28 + 20) * 1.0, 3, "aluminium"), box_for(3, 8, 8)))
add("bat-mosaic-corner-angle-3m", "BAT Mosaic Corner Angle – 3m Lengths (Square Edge)", "Square edge",
    "A square-edge corner trim developed with architects for external corners where the two surfaces are different "
    "thicknesses, such as mosaic on one side and tile on the other. One side is a fixed size; the other can sit "
    "anywhere from flush to about 15mm. Matching pre-made corner pieces are available for 8.5, 10.5 and 12.5mm.",
    ["Material: aluminium", "Length: 3m", "Sizes: 4.5, 6.5, 8.5, 10.5, 12.5 and 15mm",
     "Finishes: Mill Finish, Bright Silver, Matt Silver, Linished Silver, Black, Matt Black, Linished Black, "
     "Matt White, Pearl White, Alabaster, Bright Gold, Linished Gold, Bronze Ash"],
    ["Size", "Colour"], vs, "e-018-114.png", 3, "local",
    "BAT Mosaic Corner Angle 3m | Square Edge Tile Trim | ETS",
    "BAT square edge mosaic corner angle for corners with different tile thicknesses. 6 sizes, 13 colours, 3m lengths.")

vs = []
for s, a in [(4, 4.5), (6, 6.5), (8, 8.5), (10, 10.5), (12, 12.5), (15, 15)]:
    for col in ["MF", "BS", "MS", "BK", "MBK", "MW", "WH", "ALA", "BG"]:
        vs.append(v({"Size": f"{mm(a)}mm", "Colour": COLOURS[col]}, f"MCG-{s}-3-{col}",
                    length_kg((a * 2 + 28 + 40) * 1.0, 3, "aluminium"), box_for(3, 8, 8)))
add("bat-mosaic-corner-guard-3m", "BAT Mosaic Corner Guard – 3m Lengths (Square Edge)", "Square edge",
    "A square-edge external corner trim with two fixing legs, for corners where both surfaces are the same "
    "thickness. Suits vinyl, laminate, glass mosaic, ceramic tile and timber. Pre-made corner pieces are available "
    "for 8.5, 10.5 and 12.5mm.",
    ["Material: aluminium", "Length: 3m", "Sizes: 4.5, 6.5, 8.5, 10.5, 12.5 and 15mm",
     "Finishes: Mill Finish, Bright Silver, Matt Silver, Black, Matt Black, Matt White, Pearl White, Alabaster, Bright Gold",
     "Both surfaces must be the same thickness"],
    ["Size", "Colour"], vs, "e-018-129.png", 3, "local",
    "BAT Mosaic Corner Guard 3m | Square Edge Corner Trim | ETS",
    "BAT square edge corner guard for tile, mosaic, vinyl and timber corners. 6 sizes, 9 colours, 3m lengths. Order from ETS Perth.")

# ---------------------------------------------------------------- p.19 Prefab corners, Y section
vs = []
for s, a in [(8, 8.5), (10, 10.5), (12, 12.5)]:
    for col in ["BS", "MS", "LS", "BK", "MBK", "LB", "MW", "WH", "ALA", "BG", "LG", "BA"]:
        vs.append(v({"Size": f"{mm(a)}mm", "Colour": COLOURS[col]}, f"MCPC-{s}-{col}", 0.05, "8 x 6 x 4 cm"))
add("bat-mosaic-corner-pieces", "BAT Pre-Fabricated Corner Pieces – Mosaic Corner Angle & Guard", "Square edge",
    "Pre-made 3-way corner caps that join BAT Mosaic Corner Angle or Mosaic Corner Guard where two or three edges "
    "meet, such as the top corner of a niche, bench or column. No mitre cutting needed.",
    ["Material: aluminium", "Sizes: 8.5, 10.5 and 12.5mm (to match the trim)", "Sold each",
     "Finishes: Bright Silver, Matt Silver, Linished Silver, Black, Matt Black, Linished Black, Matt White, Pearl White, "
     "Alabaster, Bright Gold, Linished Gold, Bronze Ash"],
    ["Size", "Colour"], vs, "e-019-138.png", 0, "parcel",
    "BAT Mosaic Corner Pieces | Square Edge Trim Corners | ETS",
    "Pre-made aluminium corner pieces for BAT Mosaic Corner Angle and Guard. 8.5, 10.5 and 12.5mm in 12 colours.",
    gallery=["e-019-139.png"])

vs = []
for s, a, b in [(8, 10.3, 14.57), (10, 12.3, 17.39), (12, 14.3, 20.22)]:
    for col in ["MF", "MS"]:
        vs.append(v({"Size": f"{s}mm", "Colour": COLOURS[col]}, f"BDY-{s}-3-{col}",
                    length_kg((a * 2 + 4 * b) * 1.2, 3, "aluminium"), box_for(3, 8, 8)))
add("bat-decorative-y-section-3m", "BAT Decorative Y Section Trim – 3m Lengths", "Square edge",
    "An aluminium corner profile with a 4mm wide visible face, for 90 degree corners on walls, benches and steps. "
    "It protects both tile edges and gives an industrial feature line. Tiles are mitred to meet the Y section.",
    ["Material: aluminium", "Length: 3m", "Sizes: 8, 10 and 12mm", "Visible face: 4mm",
     "Finishes: Mill Finish, Matt Silver"],
    ["Size", "Colour"], vs, "e-019-152.png", 3, "local",
    "BAT Decorative Y Section Trim 3m | Corner Feature | ETS",
    "BAT aluminium Y section corner trim with a 4mm feature line for mitred tile corners. 8, 10 and 12mm, 3m lengths.")

# ---------------------------------------------------------------- p.20 Corner angle
vs = []
for s, a in [(8, 8), (10, 10), (12, 12.5)]:
    w = length_kg((a * 2 + 33 + 22) * 1.3, 3, "brass")
    vs.append(v({"Size": f"{mm(a)}mm", "Finish": "Brass (3m)"}, f"BCA-{s}-3", w, box_for(3)))
    vs.append(v({"Size": f"{mm(a)}mm", "Finish": "Chrome Plated Brass (3m)"}, f"CPBCA-{s}-3", w, box_for(3)))
for s, a in [(8, 8), (10, 10), (12, 12.5), (15, 15)]:
    vs.append(v({"Size": f"{mm(a)}mm", "Finish": "Polished Stainless Steel 304 (2.7m)"}, f"SSCA-{s}-27P",
                length_kg((a * 2 + 33 + 22) * 0.8, 2.7, "stainless"), box_for(2.7)))
add("bat-corner-angle-brass-stainless", "BAT Square Corner Angle – Brass, Chrome & Stainless Steel", "Square edge",
    "A box-section square edge trim in solid metal for tile edges in hard-wearing or harsh areas. Choose natural brass, "
    "chrome plated brass to match chrome tapware, or polished grade 304 stainless steel.",
    ["Brass and chrome plated brass: 3m lengths, 8, 10 and 12.5mm",
     "Stainless steel 304, polished: 2.7m lengths, 8, 10, 12.5 and 15mm",
     "Square box profile with perforated fixing leg"],
    ["Size", "Finish"], vs, "e-020-155.png", 3, "local",
    "BAT Square Edge Corner Angle | Brass, Chrome, Stainless | ETS",
    "BAT square corner angle tile trim in brass, chrome plated brass (3m) or polished 304 stainless steel (2.7m). Order in Perth.",
    gallery=["e-020-156.png"], variant_images={"Polished Stainless Steel 304 (2.7m)": "e-020-156.png"})

# ---------------------------------------------------------------- p.21 External / internal corner
round_cols = ["MF", "BS", "MS", "BK", "MBK", "MW", "WH", "ALA", "BG"]
vs = []
for s, d in [(6, 30.74), (8, 29), (10, 30), (12, 32.5)]:
    for col in round_cols:
        vs.append(v({"Size": f"{s if s != 12 else 12.5}mm", "Colour": COLOURS[col]}, f"BEC-{s}-3-{col}",
                    length_kg((d * 2 + 20) * 1.2, 3, "aluminium"), box_for(3, 8, 8)))
add("bat-external-corner-trim-3m", "BAT External Corner Trim – 3m Lengths (Rounded)", "Round edge",
    "A rounded aluminium external corner for where tiles meet at 90 degrees on walls, benches or step edges. Tiles can "
    "sit level with the top of the profile, or tuck under it to hide a cut edge.",
    ["Material: aluminium", "Length: 3m", "Sizes: 6, 8, 10 and 12.5mm",
     "Finishes: Mill Finish, Bright Silver, Matt Silver, Black, Matt Black, Matt White, Pearl White, Alabaster, Bright Gold"],
    ["Size", "Colour"], vs, "e-021-158.png", 3, "local",
    "BAT External Corner Tile Trim 3m | Rounded Edge | ETS Perth",
    "BAT rounded aluminium external corner tile trim, 6mm to 12.5mm, 9 colours, 3m lengths. Order from ETS Perth.")

vs = []
for s, b in [(8, 35.8), (10, 39.8)]:
    for col in round_cols:
        vs.append(v({"Size": f"{s}mm", "Colour": COLOURS[col]}, f"BIC-{s}-3-{col}",
                    length_kg((b + 20 + 10) * 1.2, 3, "aluminium"), box_for(3, 8, 8)))
add("bat-internal-corner-trim-3m", "BAT Internal Corner Trim – 3m Lengths (Coved)", "Cove Trim",
    "An aluminium internal corner that gives a small coved finish where two tiled surfaces meet at 90 degrees, so the "
    "corner is easy to keep clean. Tiles sit flush or tuck under the lip, then finish with silicone.",
    ["Material: aluminium", "Length: 3m", "Sizes: 8 and 10mm",
     "Finishes: Mill Finish, Bright Silver, Matt Silver, Black, Matt Black, Matt White, Pearl White, Alabaster, Bright Gold"],
    ["Size", "Colour"], vs, "e-021-167.png", 3, "local",
    "BAT Internal Corner Tile Trim 3m | Easy-Clean Corner | ETS",
    "BAT aluminium internal corner trim for easy-clean 90 degree tile corners. 8mm and 10mm, 9 colours, 3m lengths.")

# ---------------------------------------------------------------- p.22 Unicorn, Co-Pro
vs = [v({"Colour": COLOURS[c]}, f"UNI-3-{c}", length_kg(11.5 * 4 * 1.2, 3, "aluminium"), box_for(3))
      for c in ["MF", "BS", "MS", "BK", "MBK", "WH", "ALA", "BG"]]
add("bat-unicorn-universal-corner-3m", "BAT Unicorn Universal Corner Trim – 3m Lengths", "Square edge",
    "BAT's \"Unicorn\" trim works as both an internal and an external corner. Its angled face is easy to clean and "
    "gives a square-edge look, and it suits thin mosaics as well as thicker materials.",
    ["Material: aluminium", "Length: 3m", "Profile: 5 x 11.5 x 11.5mm", "Use: internal or external corners",
     "Finishes: Mill Finish, Bright Silver, Matt Silver, Black, Matt Black, Pearl White, Alabaster, Bright Gold"],
    ["Colour"], vs, "e-022-178.png", 3, "local",
    "BAT Unicorn Universal Corner Trim 3m | Internal & External",
    "BAT Unicorn universal corner tile trim for internal and external corners. Angled easy-clean face, 8 colours, 3m lengths.",
    gallery=["e-022-186.png"])

vs = []
for code, a in [("1010", 10), ("1515", 15), ("2020", 20)]:
    for col in ["BS", "LS", "MBK", "WH"]:
        vs.append(v({"Size": f"{a} x {a}mm", "Colour": COLOURS[col]}, f"BCP-{code}-3-{col}",
                    length_kg(a * 2 * 1.0, 3, "aluminium"), box_for(3, 8, 8)))
add("bat-co-pro-corner-protection-trim-3m", "BAT Co-Pro Stick-On Corner Protection Trim – 3m Lengths", "L Shaped Trim",
    "Co-Pro is an aluminium corner guard that sticks onto corners that are already tiled. Adhesive tape is fitted "
    "inside the angle, so there's no re-grouting or removing tiles. Good for fixing chipped corners in renovations.",
    ["Material: aluminium with adhesive tape", "Length: 3m", "Sizes: 10 x 10, 15 x 15 and 20 x 20mm",
     "Finishes: Bright Silver, Linished Silver, Matt Black, Pearl White", "Fits over finished tiling"],
    ["Size", "Colour"], vs, "e-022-187.png", 3, "local",
    "BAT Co-Pro Stick-On Corner Protector 3m | Tile Corners | ETS",
    "BAT Co-Pro self-adhesive aluminium corner protector for already-tiled corners. 10, 15, 20mm, 4 colours, 3m lengths.")

# ---------------------------------------------------------------- p.23 Half round
vs = []
for s, a, b in [(6, 6, 22), (8, 8, 22), (10, 10, 24), (12, 12, 27.5)]:
    for col in ["MF", "BS", "MS", "LS", "BK", "MBK", "MW", "WH", "ALA", "BG"]:
        vs.append(v({"Size": f"{s}mm", "Colour": COLOURS[col]}, f"HRT-{s}-3-{col}",
                    length_kg((b + a * 1.6) * 1.0, 3, "aluminium"), box_for(3)))
add("bat-half-round-trim-aluminium-3m", "BAT Half Round Tile Trim Aluminium – 3m Lengths", "Round edge",
    "A rounded aluminium edge trim for bath hobs, benchtops, window sills and wall tiling that stops part way up the "
    "wall. It gives a smooth, safe edge and hides cut tile edges.",
    ["Material: aluminium", "Length: 3m", "Sizes: 6, 8, 10 and 12mm",
     "Finishes: Mill Finish, Bright Silver, Matt Silver, Linished Silver, Black, Matt Black, Matt White, Pearl White, Alabaster, Bright Gold"],
    ["Size", "Colour"], vs, "e-023-193.png", 3, "local",
    "BAT Half Round Tile Trim Aluminium 3m | Round Edge | ETS",
    "BAT aluminium half round tile edge trim for hobs, benches and wall edges. 6mm to 12mm, 10 colours, 3m lengths.")

vs = []
for s, b in [(6, 26), (8, 26), (10, 28), (12, 30)]:
    w = length_kg((b + s * 1.6) * 1.0, 3, "brass")
    vs.append(v({"Size": f"{s}mm", "Finish": "Brass (3m)"}, f"HRT-{s}-3B", w, box_for(3)))
    vs.append(v({"Size": f"{s}mm", "Finish": "Chrome Plated Brass (3m)"}, f"CPHRT-{s}", w, box_for(3)))
for s, a, b in [(6, 6, 27), (8, 8, 29), (10, 10, 31), (12, 12.5, 33)]:
    w = length_kg((b + a * 1.6) * 0.8, 2.7, "stainless")
    vs.append(v({"Size": f"{mm(a)}mm", "Finish": "Stainless Steel 304 (2.5m)"}, f"SSHRT-{s}-25", w, box_for(2.5)))
    vs.append(v({"Size": f"{mm(a)}mm", "Finish": "Stainless Steel 316 Marine, Polished (2.7m)"}, f"SSHRTMG-{s}-27", w, box_for(2.7)))
add("bat-half-round-trim-brass-stainless", "BAT Half Round Tile Trim – Brass, Chrome & Stainless Steel", "Round edge",
    "Solid metal half round edge trim for wet areas, pools and commercial jobs. Brass is very durable and chemical "
    "resistant; chrome plated brass matches chrome tapware; stainless steel (304, or 316 marine grade) suits the "
    "harshest environments.",
    ["Brass and chrome plated brass: 3m lengths, 6, 8, 10 and 12mm",
     "Stainless steel grade 304: 2.5m lengths, 6, 8, 10 and 12.5mm",
     "Stainless steel grade 316 marine, polished: 2.7m lengths, 6, 8, 10 and 12.5mm"],
    ["Size", "Finish"], vs, "e-023-203.png", 3, "local",
    "BAT Half Round Trim | Brass, Chrome, 304 & 316 Stainless",
    "BAT half round tile trim in brass, chrome plated brass, 304 and 316 marine stainless steel. 6mm to 12.5mm. Order from ETS Perth.",
    gallery=["e-023-204.png"],
    variant_images={"Stainless Steel 304 (2.5m)": "e-023-204.png",
                    "Stainless Steel 316 Marine, Polished (2.7m)": "e-023-204.png"})

# ---------------------------------------------------------------- p.24 Splash trim, top trim
vs = []
for s, b in [(8, 17.6), (10, 19.6)]:
    for col in ["MF", "BS", "MS", "BK", "MBK", "MW", "WH", "ALA", "BG"]:
        vs.append(v({"Size": f"{s}mm", "Colour": COLOURS[col]}, f"ST-{s}-3-{col}",
                    length_kg((33.5 + b + 20) * 1.3, 3, "aluminium"), box_for(3, 8, 8)))
add("bat-splash-trim-3m", "BAT Splash Trim – 3m Lengths (Bench & Hob Joint)", "Cove Trim",
    "Splash trim makes a curved, easy-clean joint where a tiled wall meets a kitchen benchtop or bath hob, or where a "
    "hob meets a tiled floor, so grime can't build up in a 90 degree corner.",
    ["Material: aluminium", "Length: 3m", "Sizes: 8 and 10mm",
     "Finishes: Mill Finish, Bright Silver, Matt Silver, Black, Matt Black, Matt White, Pearl White, Alabaster, Bright Gold"],
    ["Size", "Colour"], vs, "e-024-206.png", 3, "local",
    "BAT Splash Trim 3m | Benchtop to Splashback Joint | ETS",
    "BAT aluminium splash trim for an easy-clean curved joint between splashback tiles and benchtops or bath hobs. 3m lengths.")

vs = []
for s, a in [(6, 6.5), (8, 8.5), (10, 10.5)]:
    for col in ["MF", "BS", "MS", "BK", "MBK", "MW", "WH", "ALA", "BG"]:
        vs.append(v({"Size": f"{mm(a)}mm", "Colour": COLOURS[col]}, f"BTT-{s}-3-{col}",
                    length_kg((35 + 22) * 1.2, 3, "aluminium"), box_for(3, 8, 8)))
add("bat-top-trim-3m", "BAT Top Trim – 3m Lengths (Concave Wall Capping)", "Tile Trims + Edging Profiles",
    "Top trim caps the top edge of wall tiling with a concave finish that hides cut edges and wipes clean with a cloth. "
    "Also popular as an edge finish for vinyl.",
    ["Material: aluminium", "Length: 3m", "Sizes: 6.5, 8.5 and 10.5mm",
     "Finishes: Mill Finish, Bright Silver, Matt Silver, Black, Matt Black, Matt White, Pearl White, Alabaster, Bright Gold"],
    ["Size", "Colour"], vs, "e-024-215.png", 3, "local",
    "BAT Top Trim 3m | Wall Tile Capping Trim | ETS Perth",
    "BAT aluminium top trim to cap the top edge of wall tiles or vinyl with a concave, easy-clean finish. 3 sizes, 3m lengths.")

# ---------------------------------------------------------------- p.25 Border trim, showerstop bead
vs = []
for s in [8, 10]:
    for col in ["MF", "BS", "MS", "BK", "WH", "ALA"]:
        vs.append(v({"Size": f"{s}mm", "Colour": COLOURS[col]}, f"BT-{s}-3-{col}",
                    length_kg((40 + 12 + s * 2) * 1.2, 3, "aluminium"), box_for(3, 8, 8)))
add("bat-border-trim-3m", "BAT Border Trim – 3m Lengths (Feature Strip)", "T Shaped Trim",
    "A decorative aluminium strip set between wall tiles: a cheaper alternative to ceramic border tiles for homes and "
    "commercial jobs. The 12mm face can sit flush with the tiles, or the tiles can tuck under its lip.",
    ["Material: aluminium", "Length: 3m", "Sizes: 8 and 10mm", "Visible face: 12mm",
     "Finishes: Mill Finish, Bright Silver, Matt Silver, Black, Pearl White, Alabaster"],
    ["Size", "Colour"], vs, "e-025-226.png", 3, "local",
    "BAT Border Trim 3m | Metal Feature Strip for Tiles | ETS",
    "BAT aluminium border trim, a 12mm metal feature strip between wall tiles. 8mm and 10mm, 6 colours, 3m lengths.")

add("bat-showerstop-bead-3m", "BAT Aluminium Showerstop Bead – 3m Length", "Tile Trims + Edging Profiles",
    "A low half-round aluminium bead stuck to the floor at a shower opening to stop water running out of the shower. "
    "Easy to fit on new or existing tiles.",
    ["Material: aluminium", "Colour: Bright Silver", "Length: 3m", "Size: 10mm wide x 5mm high"],
    ["Colour"], [v({"Colour": "Bright Silver"}, "SSB-103-BS", 0.4, box_for(3))], "e-025-233.png", 3, "local",
    "BAT Aluminium Showerstop Bead 3m | Shower Water Stop | ETS",
    "BAT aluminium showerstop bead, 10 x 5mm, 3m length. Stops shower water spilling onto the bathroom floor. Order from ETS Perth.")

# ---------------------------------------------------------------- p.26 Double sided angle, balcony
vs = []
for code, a, b in [("1012", 10, 12.5), ("1030", 10, 30), ("1215", 12.5, 15), ("1230", 12.5, 30)]:
    for col in ["MF", "MS"]:
        vs.append(v({"Size": f"{mm(a)} / {mm(b)}mm", "Colour": COLOURS[col]}, f"DSA-{code}-3-{col}",
                    length_kg((a + b + 25) * 2.0, 3, "aluminium"), box_for(3, 8, 8)))
add("bat-double-sided-angle-3m", "BAT Double Sided Angle – 3m Lengths", "L Shaped Trim",
    "A double sided aluminium angle that covers the end of tiles or substrates, with eight ways to fit it. Good for "
    "tile-over-tile renovations and balcony edges where the front face needs to be hidden.",
    ["Material: aluminium", "Length: 3m", "Sizes (A / B): 10 / 12.5, 10 / 30, 12.5 / 15, 12.5 / 30mm",
     "Finishes: Mill Finish, Matt Silver"],
    ["Size", "Colour"], vs, "e-026-235.png", 3, "local",
    "BAT Double Sided Angle 3m | Tile-Over-Tile Edge Trim | ETS",
    "BAT aluminium double sided angle for tile-over-tile renovations and balcony edges. 4 sizes, 3m lengths. Order from ETS Perth.")

vs = []
for s, a in [(8, 8), (10, 10), (12, 12.5)]:
    for col in ["MF", "MS"]:
        vs.append(v({"Size": f"{mm(a)}mm", "Colour": COLOURS[col]}, f"BET-{s}-3-{col}",
                    length_kg((50 + 62 + 56) * 1.8, 3, "aluminium"), box_for(3, 12, 10)))
add("bat-balcony-edge-trim-3m", "BAT Balcony Edge Trim – 3m Lengths (With Weep Holes)", "Balcony trim",
    "BAT balcony trim finishes the front face of a tiled balcony. The bottom edge is shaped to throw water away from "
    "the slab, so you don't get run lines and staining, and weep holes now come standard. Pre-made internal and "
    "external corners are available.",
    ["Material: aluminium", "Length: 3m", "Sizes: 8, 10 and 12.5mm", "Weep holes included",
     "Finishes: Mill Finish, Matt Silver", "Matching corners: BAT Balcony Edge Trim Corners"],
    ["Size", "Colour"], vs, "e-026-238.png", 3, "local",
    "BAT Balcony Edge Trim 3m | Drip Edge With Weep Holes | ETS",
    "BAT aluminium balcony edge trim with drip edge and weep holes to stop water staining. 8, 10, 12.5mm, 3m lengths.")

# ---------------------------------------------------------------- p.27 Diminishing trims
vs = []
for s, a, b in [(8, 8, 40), (10, 10, 40), (12, 12.5, 45), (15, 15, 50)]:
    for col in ["MF", "MS"]:
        vs.append(v({"Size": f"{mm(a)}mm", "Material": f"Aluminium {COLOURS[col]}"}, f"ADT-{s}-3-{col}",
                    length_kg((b + a + 20) * 1.2, 3, "aluminium"), box_for(3, 8, 8)))
    vs.append(v({"Size": f"{mm(a)}mm", "Material": "Brass"}, f"BDT-{s}-3",
                length_kg((b + a + 20) * 1.5, 3, "brass"), box_for(3, 8, 8)))
add("bat-diminishing-trim-3m", "BAT Diminishing Trim – 3m Lengths (Aluminium or Brass)", "Diminishing trim",
    "A ribbed ramp trim that steps down from a tiled floor to a lower floor, such as carpet, vinyl or timber, to "
    "reduce trip hazards where two floor heights meet in a home.",
    ["Length: 3m", "Sizes (tile height): 8, 10, 12.5 and 15mm",
     "Aluminium: Mill Finish or Matt Silver", "Brass: natural brass (chrome plated on request)", "Ribbed, non-slip top"],
    ["Size", "Material"], vs, "e-027-241.png", 3, "local",
    "BAT Diminishing Trim 3m | Tile to Carpet Ramp | ETS Perth",
    "BAT aluminium or brass diminishing ramp trim for tile-to-carpet or vinyl floor height changes. 8mm to 15mm, 3m lengths.",
    gallery=["e-027-242.png"], variant_images={"Brass": "e-027-242.png"})

vs = []
for s, a, b in [(8, 8, 64), (10, 10, 80), (12, 12.5, 100)]:
    vs.append(v({"Size": f"{mm(a)}mm (ramp {b}mm)"}, f"ADTC-{s}-3-MS",
                length_kg((b + 30) * 1.8, 3, "aluminium"), box_for(3, 12, 6)))
add("bat-commercial-diminishing-trim-3m", "BAT Commercial Diminishing Trim – 3m Lengths (AS1428.1)", "Ramp Trim",
    "A wide, gentle aluminium ramp trim designed to meet the Australian Standard for access and mobility (AS1428.1, "
    "ramped threshold). Use it between floors of different heights in commercial buildings, or at home for "
    "wheelchair and walker access.",
    ["Material: aluminium", "Colour: Matt Silver", "Length: 3m", "Sizes: 8mm (64mm ramp), 10mm (80mm ramp), 12.5mm (100mm ramp)",
     "Complies with AS1428.1 ramped threshold"],
    ["Size"], vs, "e-027-245.png", 3, "local",
    "BAT Commercial Diminishing Trim 3m | AS1428.1 Ramp | ETS",
    "BAT commercial aluminium ramp trim, compliant with AS1428.1 for access and mobility. 8, 10, 12.5mm, 3m lengths.")

# ---------------------------------------------------------------- p.28 Cove trims
cove_cols = ["MF", "BS", "MS", "BK", "MBK", "WH", "ALA"]
cove_sizes = [("88", "8 x 8mm"), ("108", "10 x 8mm"), ("1010", "10 x 10mm"), ("128", "12.5 x 8mm"),
              ("1210", "12.5 x 10mm"), ("1212", "12.5 x 12.5mm")]
vs = []
for code, s in cove_sizes:
    for col in cove_cols:
        vs.append(v({"Size": s, "Colour": COLOURS[col]}, f"CT-{code}-3-{col}",
                    length_kg((56.6 * 2 + 40) * 1.2, 3, "aluminium"), box_for(3, 10, 10)))
add("bat-cove-trim-3m", "BAT Cove Trim – 3m Lengths (Hygienic Wall-Floor Cove)", "Cove Trim",
    "BAT cove trim makes a 25mm radius curve between wall and floor tiles that is easy to clean and doesn't trap dust "
    "or bacteria. Designed with health departments and architects for commercial kitchens, food preparation areas "
    "and anywhere a hygienic wall-floor joint is required. Corners and end caps are available.",
    ["Material: aluminium", "Length: 3m", "Radius: 25mm",
     "Sizes (wall tile x floor tile): 8 x 8, 10 x 8, 10 x 10, 12.5 x 8, 12.5 x 10, 12.5 x 12.5mm",
     "Finishes: Mill Finish, Bright Silver, Matt Silver, Black, Matt Black, Pearl White, Alabaster",
     "Matching parts: BAT Cove Trim Corners, Cove Trim End Caps"],
    ["Size", "Colour"], vs, "e-028-249.png", 3, "local",
    "BAT Cove Trim 3m | Hygienic Wall to Floor Tile Cove | ETS",
    "BAT aluminium cove trim, 25mm radius wall-to-floor cove for commercial kitchens and food areas. 6 sizes, 3m lengths.")

vs = [v({"Colour": COLOURS[c]}, f"APC60-3-{c}", length_kg(95 * 1.5, 3, "aluminium"), box_for(3, 10, 10)) for c in cove_cols]
add("bat-apc60-all-purpose-cove-trim-3m", "BAT APC 60 All Purpose Cove Trim – 3m Lengths", "Cove Trim",
    "A large 60mm radius aluminium cove for a sealed, easy-clean wall-to-floor joint. It can go on top of existing "
    "tiling or under vinyl and other flooring. Designed with health departments and architects. Corners and end caps "
    "are available.",
    ["Material: aluminium", "Length: 3m", "Radius: 60mm", "Size: 50 x 50mm",
     "Finishes: Mill Finish, Bright Silver, Matt Silver, Black, Matt Black, Pearl White, Alabaster",
     "Matching parts: BAT APC 60 Corners, APC 60 End Caps"],
    ["Colour"], vs, "e-028-248.png", 3, "local",
    "BAT APC 60 All Purpose Cove Trim 3m | 60mm Radius | ETS",
    "BAT APC 60 aluminium cove trim, 60mm radius for hygienic wall-to-floor joints over tile or vinyl. 7 colours, 3m lengths.")

vs = []
for s in [8, 10]:
    for col in ["MF", "BS", "MS", "BK", "WH", "ALA"]:
        vs.append(v({"Size": f"{s}mm", "Colour": COLOURS[col]}, f"APCOVCOM{s}-{col}",
                    length_kg((96 + 57 + 21) * 1.5, 3, "aluminium"), box_for(3, 12, 10)))
add("bat-apc60-cove-combination-3m", "BAT APC 60 Cove Combination Trim – 3m Lengths", "Cove Trim",
    "The Cove Combo combines BAT's cove trim and APC 60, for commercial jobs where only the floor is tiled. It forms "
    "a 96mm high coved skirting from the floor tiles up the wall.",
    ["Material: aluminium", "Length: 3m", "Sizes (floor tile): 8 and 10mm", "Height: 96.2mm, radius 25mm",
     "Finishes: Mill Finish, Bright Silver, Matt Silver, Black, Pearl White, Alabaster",
     "Matching parts: BAT Cove Combo Corners, Cove Trim End Caps"],
    ["Size", "Colour"], vs, "e-029-277.png", 3, "local",
    "BAT APC 60 Cove Combination Trim 3m | Coved Skirting | ETS",
    "BAT Cove Combo aluminium coved skirting trim for floors where only the floor is tiled. 8mm and 10mm, 3m lengths.")

# ---------------------------------------------------------------- p.29 Stairnosing
vs = []
for s, a in [(8, 8), (10, 10), (12, 12.5)]:
    for col in ["MF", "BS", "MS", "BK", "MBK", "MW", "WH", "ALA"]:
        for rub in ["Black", "Grey", "Beige", "Brown"]:
            vs.append(v({"Size": f"{mm(a)}mm", "Colour": COLOURS[col], "Rubber Insert": rub},
                        f"BSN-{s}-3-{col}-{rub[:2].upper()}", length_kg((53 + 48.5 + 21.5) * 1.6, 3, "aluminium"),
                        box_for(3, 10, 8)))
add("bat-stairnosing-trim-3m", "BAT Stairnosing Trim – 3m Lengths (Non-Slip Rubber Insert)", "Stair Trim",
    "An aluminium stair nosing with a non-slip rubber insert, set into the tiling on the front edge of each step. It "
    "protects the tile edge and makes stairs safer, and suits indoor and outdoor steps. Choose a rubber colour that "
    "contrasts with your tile so the step edge is easy to see.",
    ["Material: aluminium with rubber insert", "Length: 3m", "Sizes (tile thickness): 8, 10 and 12.5mm",
     "Tread: 53mm with 25mm rubber insert, nose 21.5mm",
     "Trim finishes: Mill Finish, Bright Silver, Matt Silver, Black, Matt Black, Matt White, Pearl White, Alabaster",
     "Rubber insert: Black, Grey, Beige, Brown", "Installed during tiling"],
    ["Size", "Colour", "Rubber Insert"], vs, "e-029-264.png", 3, "local",
    "BAT Stair Nosing Tile Trim 3m | Non-Slip Rubber Insert | ETS",
    "BAT aluminium stair nosing for tiled steps with non-slip rubber insert in 4 colours. 8, 10, 12.5mm, 3m lengths.")

# ---------------------------------------------------------------- p.30 Prefab corners
vs = []
for code, s in cove_sizes:
    for col in cove_cols:
        for typ, pre in [("External", "CTEC"), ("Internal", "CTIC")]:
            vs.append(v({"Type": f"Cove Trim {typ}", "Size": s, "Colour": COLOURS[col]}, f"{pre}-{code}-{col}", 0.2, "15 x 15 x 12 cm"))
for s in [8, 10]:
    for col in ["MF", "BS", "MS", "BK", "WH", "ALA"]:
        for typ, pre in [("External", "APCOVEC"), ("Internal", "APCOVIC")]:
            vs.append(v({"Type": f"Cove Combo {typ}", "Size": f"{s}mm", "Colour": COLOURS[col]}, f"{pre}-{s}-{col}", 0.3, "18 x 18 x 15 cm"))
for col in cove_cols:
    for typ, pre in [("External", "APC60-EC"), ("Internal", "APC60-IC")]:
        vs.append(v({"Type": f"APC 60 {typ}", "Size": "50 x 50mm", "Colour": COLOURS[col]}, f"{pre}-{col}", 0.3, "18 x 18 x 15 cm"))
add("bat-cove-trim-corners", "BAT Cove Trim Corners – Internal & External (Cove, Cove Combo, APC 60)", "Cove Trim",
    "Pre-made internal and external corners for BAT cove trims, so wall-to-floor coves turn corners cleanly without "
    "cutting and filling. Choose the corner type that matches your trim: Cove Trim, Cove Combo or APC 60.",
    ["Material: aluminium", "Sold each",
     "Cove Trim corners: sizes 8 x 8 to 12.5 x 12.5mm (match your Cove Trim size)",
     "Cove Combo corners: 8 and 10mm", "APC 60 corners: 50 x 50mm",
     "Finishes to match the trim: Mill Finish, Bright Silver, Matt Silver, Black, Matt Black (Cove Trim and APC 60 only), Pearl White, Alabaster"],
    ["Type", "Size", "Colour"], vs, "e-030-290.png", 0, "parcel",
    "BAT Cove Trim Corners | Internal & External | APC 60 | ETS",
    "Pre-made internal and external corners for BAT Cove Trim, Cove Combo and APC 60 cove trims. Order from ETS Perth.",
    gallery=["e-030-291.png", "e-030-285.png", "e-030-288.png", "e-030-284.png", "e-030-287.png"],
    variant_images={"Cove Trim Internal": "e-030-291.png", "Cove Combo External": "e-030-285.png",
                    "Cove Combo Internal": "e-030-288.png", "APC 60 External": "e-030-284.png",
                    "APC 60 Internal": "e-030-287.png"})

vs = []
for s, a in [(8, 8), (10, 10), (12, 12.5)]:
    for col in ["MF", "MS"]:
        for typ, pre in [("External", "BETEC"), ("Internal", "BETIC")]:
            vs.append(v({"Type": typ, "Size": f"{mm(a)}mm", "Colour": COLOURS[col]}, f"{pre}-{s}-{col}", 0.25, "18 x 18 x 12 cm"))
add("bat-balcony-edge-trim-corners", "BAT Balcony Edge Trim Corners – Internal & External", "Balcony trim",
    "Pre-made 90 degree internal and external corners for BAT Balcony Edge Trim, so the drip edge runs unbroken "
    "around balcony corners with no mitre cutting.",
    ["Material: aluminium", "Sold each", "Sizes: 8, 10 and 12.5mm (match your balcony trim)",
     "Finishes: Mill Finish, Matt Silver"],
    ["Type", "Size", "Colour"], vs, "e-030-286.png", 0, "parcel",
    "BAT Balcony Edge Trim Corners | Internal & External | ETS",
    "Pre-made internal and external corners for BAT Balcony Edge Trim. 8, 10 and 12.5mm, mill or matt silver.",
    gallery=["e-030-289.png"], variant_images={"Internal": "e-030-289.png"})

# ---------------------------------------------------------------- p.31 End caps
vs = []
for code, t in [("108L", "Cove Trim 10 x 8mm – Left Hand"), ("108R", "Cove Trim 10 x 8mm – Right Hand"),
                ("1010", "Cove Trim 10 x 10mm")]:
    for col in ["GR", "WH"]:
        vs.append(v({"Type": t, "Colour": "Grey" if col == "GR" else "White"}, f"CTCAP-{code}-{col}", 0.1, "15 x 10 x 6 cm"))
for col in ["GR", "WH"]:
    vs.append(v({"Type": "APC 60", "Colour": "Grey" if col == "GR" else "White"}, f"APC60CAP-{col}", 0.15, "18 x 12 x 8 cm"))
add("bat-cove-trim-end-caps-10-pack", "BAT Cove Trim & APC 60 End Caps – Pack of 10", "Cove Trim",
    "Plastic end caps that close off the exposed end of BAT Cove Trim, Cove Combo or APC 60 cove trim where it stops at "
    "a door frame, cupboard or wall end. Note: they don't cover the taper at the top of Cove Combo.",
    ["Material: plastic", "Pack of 10", "Cove Trim caps: 10 x 8mm left hand, 10 x 8mm right hand, 10 x 10mm",
     "APC 60 caps", "Colours: Grey, White"],
    ["Type", "Colour"], vs, "e-031-293.png", 0, "parcel",
    "BAT Cove Trim & APC 60 End Caps 10 Pack | ETS Perth",
    "Plastic end caps for BAT Cove Trim, Cove Combo and APC 60 cove trims, grey or white, pack of 10. Order from ETS Perth.",
    gallery=["e-031-294.png", "e-031-292.png"], variant_images={"APC 60": "e-031-292.png"})

# ---------------------------------------------------------------- p.32 BATEX
def batex(prefix, sizes6, sizes10, metal):
    out = []
    for infill, sizes in [("6mm", sizes6), ("10mm", sizes10)]:
        for code, a in sizes:
            for col in ["BK", "GR"]:
                out.append(v({"Size": f"{mm(a)}mm", "Infill Width": infill, "Insert Colour": COLOURS[col]},
                             f"{prefix}-{code}{infill[:-2]}-3-{col}",
                             length_kg((a * 2 + 50) * 1.2, 3, metal), box_for(3, 8, 8)))
    return out


al_bx = [("8", 8), ("9", 9), ("10", 10), ("11", 11), ("12", 12.5), ("13", 13.5), ("15", 15), ("17", 17),
         ("18", 18.5), ("20", 20), ("22", 22), ("23", 23), ("25", 25)]
br_bx = [("8", 8), ("9", 9), ("10", 10), ("11", 11), ("12", 12.5), ("13", 13.5), ("15", 15), ("18", 18.5),
         ("20", 20), ("22", 22)]
ss_bx = [("8", 8), ("10", 10), ("12", 12.5), ("15", 15), ("18", 18.5), ("22", 22)]
vs = batex("BTXA", al_bx, al_bx, "aluminium")
EXP_INTRO = ("BATEX expansion joints are made from two metal angles bonded to a neoprene rubber infill. They stop "
             "tiles cracking or lifting from thermal expansion and movement in large tiled areas such as shopping "
             "centres, airports, foyers, and large open-plan homes and alfresco areas. Custom versions (curved, full "
             "circle, single sided or wider infill) can be made to order.")
add("bat-batex-expansion-joint-aluminium-3m", "BAT BATEX Expansion Joint Aluminium – 3m Lengths", "Expansion Trim",
    EXP_INTRO,
    ["Material: aluminium angles, neoprene infill", "Length: 3m", "Sizes (tile thickness): 8mm to 25mm",
     "Infill width: 6mm or 10mm", "Insert colour: Black or Grey"],
    ["Size", "Infill Width", "Insert Colour"], vs, "e-032-301.png", 3, "local",
    "BATEX Aluminium Tile Expansion Joint 3m | 6mm or 10mm | ETS",
    "BAT BATEX aluminium movement joint with neoprene infill for large tiled floors. 8mm to 25mm, 3m lengths. Order in Perth.")

vs = batex("BTXB", br_bx, br_bx, "brass")
add("bat-batex-expansion-joint-brass-3m", "BAT BATEX Expansion Joint Brass – 3m Lengths", "Expansion Trim",
    EXP_INTRO,
    ["Material: brass angles, neoprene infill", "Length: 3m", "Sizes (tile thickness): 8mm to 22mm",
     "Infill width: 6mm or 10mm", "Insert colour: Black or Grey"],
    ["Size", "Infill Width", "Insert Colour"], vs, "e-032-300.png", 3, "local",
    "BATEX Brass Tile Expansion Joint 3m | 6mm or 10mm | ETS",
    "BAT BATEX brass movement joint with neoprene infill for large tiled floors. 8mm to 22mm, 3m lengths. Order in Perth.")

vs = batex("BTXS", ss_bx, ss_bx, "stainless")
add("bat-batex-expansion-joint-stainless-3m", "BAT BATEX Expansion Joint Stainless Steel 304 – 3m Lengths", "Expansion Trim",
    EXP_INTRO + " Ask us before choosing stainless steel so we can confirm the right grade for your site.",
    ["Material: stainless steel grade 304 angles, neoprene infill", "Length: 3m",
     "Sizes (tile thickness): 8, 10, 12.5, 15, 18.5 and 22mm", "Infill width: 6mm or 10mm",
     "Insert colour: Black or Grey", "Grade 316 available to order in 8, 10 and 12mm"],
    ["Size", "Infill Width", "Insert Colour"], vs, "e-032-302.png", 3, "local",
    "BATEX Stainless Steel Expansion Joint 304 3m | ETS Perth",
    "BAT BATEX 304 stainless steel movement joint with neoprene infill. 8mm to 22mm, 6 or 10mm infill, 3m lengths.")

# ---------------------------------------------------------------- p.33 Mortarloc
ml_sizes = [("2506", "25 x 6mm"), ("3006", "30 x 6mm"), ("4006", "40 x 6mm"), ("5006", "50 x 6mm"),
            ("2510", "25 x 10mm"), ("3010", "30 x 10mm"), ("4010", "40 x 10mm"), ("5010", "50 x 10mm")]
for pre, metal, mat, img, handle in [("MLSTA", "aluminium", "Aluminium", "e-033-306.png", "bat-mortarloc-expansion-joint-aluminium"),
                                     ("MLSTB", "brass", "Brass", "e-033-308.png", "bat-mortarloc-expansion-joint-brass")]:
    vs = []
    for code, s in ml_sizes:
        h = int(code[:2])
        for col in ["GR", "BK"]:
            vs.append(v({"Size": s, "Insert Colour": COLOURS[col]}, f"{pre}-{code}-{col}",
                        length_kg(h * 2 * 1.2 + h * 4, 3, metal), box_for(3, 8, 8)))
    add(handle, f"BAT MORTARLOC Expansion Joint {mat} – 3m Lengths", "Expansion Trim",
        f"MORTARLOC expansion joints are for thick-bed (mortar bed) tiling, where BATEX is for thin-bed adhesive. "
        f"Two {mat.lower()} side plates (usually 1.2mm) hold a neoprene infill, with anchor tabs that lock into the "
        f"mortar bed. Custom sizes, thicker plates, and stainless steel or zinc versions can be made to order.",
        [f"Material: {mat.lower()} side plates, neoprene infill", "Length: 3m",
         "Sizes (height x joint width): 25, 30, 40 and 50mm high; 6mm or 10mm wide",
         "Insert colour: Grey or Black", "For thick-bed / mortar bed installations"],
        ["Size", "Insert Colour"], vs, img, 3, "local",
        f"BAT MORTARLOC {mat} Expansion Joint 3m | Mortar Bed | ETS",
        f"BAT MORTARLOC {mat.lower()} expansion joint for thick-bed mortar tiling. 25mm to 50mm high, 6 or 10mm wide, 3m lengths.")


def main():
    for p in PRODUCTS:
        assert len(p["seo"]["title"]) <= 70, p["seo"]["title"]
        assert len(p["seo"]["description"]) <= 160, (len(p["seo"]["description"]), p["seo"]["description"])
        skus = [x["sku"] for x in p["variants"]]
        assert len(skus) == len(set(skus)), p["title"]
        combos = [tuple(x["options"][o] for o in p["options"]) for x in p["variants"]]
        assert len(combos) == len(set(combos)), p["title"]
        assert len(p["variants"]) <= 2048
    all_skus = [x["sku"] for p in PRODUCTS for x in p["variants"]]
    assert len(all_skus) == len(set(all_skus)), "duplicate SKU across products"
    with open(os.path.join(HERE, "bat-products.json"), "w") as f:
        json.dump(PRODUCTS, f, indent=1, ensure_ascii=False)
    with open(os.path.join(HERE, "bat-variants.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["handle", "product", "sku", "option1", "option2", "option3", "weight_kg", "box_cm",
                    "shipping", "cost_ex_gst", "price_inc_gst"])
        for p in PRODUCTS:
            for x in p["variants"]:
                o = [x["options"][n] for n in p["options"]] + ["", "", ""]
                w.writerow([p["handle"], p["title"], x["sku"], o[0], o[1], o[2], x["weight"], x["box"],
                            "Perth only" if p["ship"] == "local" else "General", "", ""])
    print(len(PRODUCTS), "products,", len(all_skus), "variants")
    for p in PRODUCTS:
        print(f"{len(p['variants']):4d}  {p['title']}")


if __name__ == "__main__":
    main()
