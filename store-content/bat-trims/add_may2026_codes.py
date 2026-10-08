"""Turn the codes on BAT's May 2026 Trims Book that weren't in the 2023-24 catalogue into
new variants (on existing products) and new products.

Writes may2026-additions.json:
  {"variants": {handle: [variant, ...]}, "products": [product, ...]}
Each variant has options, sku, cost (ex GST), price (inc GST), weight (kg) and box.
"""
import json
import re
import sys

sys.path.insert(0, "pricing")
from price_rule import retail  # noqa: E402

COST = {k: v[0] for k, v in json.load(open("pricing/bat-trims-price-list-2026-05.json")).items()}
P = {p["handle"]: p for p in json.load(open("bat-products.json"))}

# BAT colour suffixes (P = protective film, same finish)
COL = {
    "MF": "Mill Finish", "BS": "Bright Silver", "MS": "Matt Silver", "LS": "Linished Silver", "BK": "Black",
    "MBK": "Matt Black", "LB": "Linished Black", "MW": "Matt White", "WH": "Pearl White", "ALA": "Alabaster",
    "BG": "Bright Gold", "LG": "Linished Gold", "BA": "Bronze Ash", "LC": "Linished Copper",
    "LM": "Linished Matt Gold", "LMG": "Linished Matt Gold", "LN": "Linished Nickel", "SN": "Linished Satin Nickel",
    "LSN": "Linished Satin Nickel", "AW": "Ancient White", "ME": "Medium Grey", "MH": "Manhattan",
    "MO": "Moon White", "GM": "Gunmetal", "LGM": "Linished Gunmetal", "SM": "Surfmist", "MG": "Matt Gold",
    "UP": "Mill Finish (Unpunched)", "GR": "Grey", "DG": "Dark Grey", "SG": "Smokey Grey",
}
ANGLE_MM = {"4": "4.5mm", "12": "12.5mm", "13": "13.5mm", "18": "18.5mm", "25": "25.5mm"}
MCA_MM = {"4": "4.5mm", "6": "6.5mm", "8": "8.5mm", "10": "10.5mm", "12": "12.5mm"}


def col(s):
    s = s[:-1] if s.endswith("P") and s[:-1] in COL else s
    return COL[s]


def num(s):
    m = re.search(r"[\d.]+", s)
    return float(m.group()) if m else 0


def near(handle, size_opt, size):
    """weight and box of the existing variant whose size is closest"""
    vs = P[handle]["variants"]
    v = min(vs, key=lambda x: abs(num(x["options"].get(size_opt, "0")) - num(size)))
    return v["weight"], v["box"]


def var(handle, options, sku, size_opt="Size", weight=None, box=None):
    if sku not in COST:
        raise KeyError(sku)
    if weight is None:
        weight, box = near(handle, size_opt, options[size_opt])
    c = COST[sku]
    return {"options": options, "sku": sku, "cost": c, "price": retail(c), "weight": weight, "box": box}


V = {}


def add(handle, v):
    V.setdefault(handle, []).append(v)


for code in COST:
    m = re.fullmatch(r"AA-(\d+)-3-([A-Z]+)", code)
    if m and code not in ("AA-28-3",):
        size, suf = m.groups()
        if suf not in ("UP", "SNP", "LCP", "LMP", "LNP", "AWP", "MEP", "MHP", "MOP", "GMP", "SMP"):
            continue
        h = "bat-aluminium-tiling-angle-3m"
        name = col(suf)
        exists = any(x["sku"].startswith(f"AA-{size}-3") and x["options"]["Colour"] == name for x in P[h]["variants"])
        if not exists:
            add(h, var(h, {"Size": ANGLE_MM.get(size, size + "mm"), "Colour": name}, code))
add("bat-aluminium-tiling-angle-3m", var("bat-aluminium-tiling-angle-3m", {"Size": "28mm", "Colour": "Mill Finish"}, "AA-28-3"))

for code in ["AA-6-3-BSP-N", "AA-8-3-BSP-N", "AA-8-3-LGP-N", "AA-10-3-BSP-N", "AA-10-3-LGP-N",
             "AA-11-3-BSP-N", "AA-11-3-LGP-N", "AA-12-3-BSP-N", "AA-12-3-LGP-N"]:
    s, c = re.fullmatch(r"AA-(\d+)-3-(\w+)-N", code).groups()
    add("bat-notched-aluminium-angle-3m",
        var("bat-notched-aluminium-angle-3m", {"Size": ANGLE_MM.get(s, s + "mm"), "Colour": col(c)}, code))

# geometric angle: AA-aabbtt-3[-COL], tt = 16 (1.6mm) or a single 3 (3mm)
GEO = "bat-aluminium-geometric-angle-3m"
for code in COST:
    m = re.fullmatch(r"AA-(\d{5,6})-3(?:-([A-Z]+))?", code)
    if not m:
        continue
    d, suf = m.groups()
    a, b, t = (d[:2], d[2:4], "1.6") if len(d) == 6 else (d[:2], d[2:4], "3")
    size = f"{int(a)} x {int(b)} x {t}mm"
    colour = COL[suf] if suf else "Mill Finish"
    if any(x["options"] == {"Size": size, "Colour": colour} for x in P[GEO]["variants"]):
        continue
    same = [x for x in P[GEO]["variants"] if x["options"]["Size"] == size]
    if same:
        w, box = same[0]["weight"], same[0]["box"]
    else:  # scale the closest profile by cross-section
        ref = min(P[GEO]["variants"], key=lambda x: abs(sum(map(num, x["options"]["Size"].split("x"))) - (int(a) + int(b) + float(t))))
        ra, rb, rt = [num(p) for p in ref["options"]["Size"].split("x")]
        w = round(ref["weight"] * ((int(a) + int(b)) * float(t)) / ((ra + rb) * rt), 2)
        box = ref["box"]
    add(GEO, var(GEO, {"Size": size, "Colour": colour}, code, weight=w, box=box))

for s in ("6", "8", "10", "12"):
    add("bat-mosaic-corner-angle-3m", var("bat-mosaic-corner-angle-3m", {"Size": MCA_MM[s], "Colour": "Linished Matt Gold"}, f"MCA-{s}-3-LMP"))
for s in ("10", "15", "20"):
    add("bat-co-pro-corner-protection-trim-3m",
        var("bat-co-pro-corner-protection-trim-3m", {"Size": f"{s} x {s}mm", "Colour": "Linished Matt Gold"}, f"BCP-{s}{s}-LMG"))
for s in ("10", "12"):
    add("bat-decorative-y-section-3m", var("bat-decorative-y-section-3m", {"Size": f"{s}mm", "Colour": "Bright Silver"}, f"BDY-{s}-3-BS"))
add("bat-birds-mouth-trim-3m", var("bat-birds-mouth-trim-3m", {"Size": "8mm", "Colour": "Pearl White"}, "BMT-8-3-WH"))
add("bat-birds-mouth-trim-3m", var("bat-birds-mouth-trim-3m", {"Size": "10mm", "Colour": "Black"}, "BMT-10-3-BK"))
BS = {"8": "8mm", "10": "10mm", "12": "12.5mm"}
for s in ("8", "10", "12"):
    for c in ("GM", "MBK"):
        add("bat-balcony-edge-trim-3m", var("bat-balcony-edge-trim-3m", {"Size": BS[s], "Colour": COL[c]}, f"BET-{s}-3-{c}"))
        for t, pre in (("External", "BETEC"), ("Internal", "BETIC")):
            add("bat-balcony-edge-trim-corners",
                var("bat-balcony-edge-trim-corners", {"Type": t, "Size": BS[s], "Colour": COL[c]}, f"{pre}-{s}-{c}"))
for code, size, mat in [("ADT-8-3-BG", "8mm", "Aluminium Bright Gold"), ("ADT-15-3-BG", "15mm", "Aluminium Bright Gold"),
                        ("ADT-8-3-MBK", "8mm", "Aluminium Matt Black"), ("ADT-10-3-MBK", "10mm", "Aluminium Matt Black"),
                        ("ADT-12-3-MBK", "12.5mm", "Aluminium Matt Black"), ("ADT-15-3-MBK", "15mm", "Aluminium Matt Black"),
                        ("CPDT-8-3", "8mm", "Chrome Plated Brass"), ("CPDT-10-3", "10mm", "Chrome Plated Brass"),
                        ("CPDT-12-3", "12.5mm", "Chrome Plated Brass"), ("CPDT-15-3", "15mm", "Chrome Plated Brass")]:
    add("bat-diminishing-trim-3m", var("bat-diminishing-trim-3m", {"Size": size, "Material": mat}, code))
for code, size in [("DSA-1012-3-MBK", "10 / 12.5mm"), ("DSA-1030-3-MBK", "10 / 30mm"),
                   ("DSA-1215-3-MBK", "12.5 / 15mm"), ("DSA-1230-3-MBK", "12.5 / 30mm")]:
    add("bat-double-sided-angle-3m", var("bat-double-sided-angle-3m", {"Size": size, "Colour": "Matt Black"}, code))
add("bat-stainless-steel-tiling-angle-3m", var("bat-stainless-steel-tiling-angle-3m", {"Size": "18.5mm"}, "SSAMG-18-3"))
add("bat-brass-stainless-geometric-angle",
    var("bat-brass-stainless-geometric-angle", {"Material": "Brass (3.6m)", "Size": "19.05 x 19.05 x 3.18mm"}, "BA-1932-36"))
for code, size in [("AF-803-4", "80 x 3mm"), ("AF-1003-4", "100 x 3mm")]:
    w, box = near("bat-flat-bar-aluminium-brass-stainless", "Size", "50 x 3mm")
    add("bat-flat-bar-aluminium-brass-stainless",
        var("bat-flat-bar-aluminium-brass-stainless", {"Material": "Aluminium (4m)", "Size": size}, code,
            weight=round(w * num(size) / 50, 2), box="405 x 12 x 4 cm"))
add("bat-pvc-waterproofing-angle-3m", var("bat-pvc-waterproofing-angle-3m", {"Size": "45 x 45 x 4mm"}, "PVC-WPA45454-3"))
for s, size in (("8", "8mm"), ("10", "10mm"), ("12", "12.5mm"), ("15", "15mm")):
    ref = next(x for x in P["bat-corner-angle-brass-stainless"]["variants"] if x["sku"] == f"SSCA-{s}-27P")
    add("bat-corner-angle-brass-stainless",
        var("bat-corner-angle-brass-stainless", {"Size": size, "Finish": "Commercial Grade Stainless Steel, Polished (2.7m)"},
            f"SSCCA-{s}-27P", weight=ref["weight"], box=ref["box"]))
add("bat-half-round-trim-aluminium-3m", var("bat-half-round-trim-aluminium-3m", {"Size": "12mm", "Colour": "Bright Gold"}, "HRT-12-3BGP"))
for code in COST:
    m = re.fullmatch(r"BTX([BS])-(\d+?)(6|10)-3-(BK|GR)", code)
    if not m:
        continue
    mat, s, inf, c = m.groups()
    h = "bat-batex-expansion-joint-brass-3m" if mat == "B" else "bat-batex-expansion-joint-stainless-3m"
    size = {"17": "17.5mm", "18": "18.5mm", "12": "12.5mm", "13": "13.5mm"}.get(s, s + "mm")
    opts = {"Size": size, "Infill Width": inf + "mm", "Insert Colour": COL[c]}
    if any(x["options"] == opts for x in P[h]["variants"]):
        continue
    add(h, var(h, opts, code))

# ---------- new products ----------
CARE = ("<p><strong>Care:</strong> wash finished trims with warm soapy water and a soft cloth. Don't use acid or alkaline "
        "cleaners, scourers or sandpaper on coloured, anodised or plated finishes. Remove greasy marks with white spirits, "
        "then rinse with clean water.</p><p>BAT Trims is an Australian family business, making tiling trims in Dandenong, "
        "Victoria since 1985. Order through Excellent Tiling Services in Maddington, Perth.</p>")
LONG = ["BAT Trims", "BAT", "Hardware", "Tile Trims + Edging Profiles", "supplier-bat", "bat-price-list-2026-05",
        "ship-local-only", "ship-long"]
PARCEL = ["BAT Trims", "BAT", "Hardware", "Tile Trims + Edging Profiles", "supplier-bat", "bat-price-list-2026-05",
          "ship-parcel"]
NEW = []

ch = []
for s in ("8", "10", "12"):
    for c in ("MF", "BSP", "MSP", "MBKP", "WHP"):
        k = f"AC-{s}-3-{c}"
        ch.append({"options": {"Size": s + "mm", "Colour": col(c)}, "sku": k, "cost": COST[k], "price": retail(COST[k]),
                   "weight": round(0.36 + 0.01 * (int(s) - 8), 2), "box": "305 x 8 x 6 cm"})
NEW.append({
    "handle": "bat-aluminium-channel-trim-3m", "title": "BAT Aluminium Channel Trim (U Channel) – 3m Lengths",
    "productType": "Square edge", "tags": LONG, "files": ["channel", "channel-profile"],
    "seo": {"title": "BAT Aluminium Channel Trim U Channel 3m | ETS Perth",
            "description": "BAT aluminium U channel tile trim, 8, 10 and 12mm, 3m lengths. Mill, bright silver, matt silver, matt black or pearl white. Perth."},
    "descriptionHtml": "<p>A U-shaped aluminium channel that caps the edge of tile, stone, glass or panels with a clean square finish on both faces. Use it on benchtop and splashback edges, niches, shelves and feature panels.</p><ul>\n<li>Material: aluminium</li>\n<li>Length: 3m</li>\n<li>Sizes (internal width): 8, 10 and 12mm</li>\n<li>Finishes: Mill Finish, Bright Silver, Matt Silver, Matt Black, Pearl White (coloured finishes come with protective film)</li>\n</ul>" + CARE,
    "options": ["Size", "Colour"], "variants": ch, "ship": "local"})

one_al, one_br = [], []
for code in COST:
    m = re.fullmatch(r"(N?BA|AA)-(\d+)-1", code)
    if not m:
        continue
    kind, s = m.groups()
    if kind == "AA":
        w3, _ = near("bat-aluminium-tiling-angle-3m", "Size", ANGLE_MM.get(s, s + "mm"))
        size = {"4": "4.5mm", "12": "12.5mm", "13": "13.5mm", "18": "18.5mm"}.get(s, s + "mm")
        one_al.append({"options": {"Size": size}, "sku": code, "cost": COST[code], "price": retail(COST[code]),
                       "weight": round(w3 / 3, 2), "box": "105 x 6 x 4 cm"})
    else:
        size = {"4": "4.5mm", "12": "12.5mm", "13": "13.5mm", "16": "16.5mm", "18": "18.5mm", "23": "23.5mm"}.get(s, s + "mm")
        w3, _ = near("bat-brass-tiling-angle-3m", "Size", size)
        one_br.append({"options": {"Size": size}, "sku": code, "cost": COST[code], "price": retail(COST[code]),
                       "weight": round(w3 / 3, 2), "box": "105 x 6 x 4 cm"})
NEW.append({
    "handle": "bat-aluminium-tiling-angle-1m", "title": "BAT Aluminium Tiling Angle – 1m Lengths (Mill Finish)",
    "productType": "L Shaped Trim", "tags": PARCEL, "files": ["aa-gold", "aa-diagram"],
    "seo": {"title": "BAT Aluminium Tile Trim Angle 1m | Small Jobs | ETS Perth",
            "description": "BAT mill finish aluminium tile edge angle in handy 1m lengths, 4.5mm to 25mm. Ideal for niches, small repairs and shower hobs. Ships Australia wide."},
    "descriptionHtml": "<p>The same BAT aluminium L angle as the 3m range, cut to 1m. Handy for niches, shower hobs, window sills, small repairs and anywhere a full 3m length would be wasted. Short enough to post.</p><ul>\n<li>Material: aluminium, mill finish, perforated fixing leg</li>\n<li>Length: 1m</li>\n<li>Sizes (tile thickness): 4.5, 6, 8, 9, 10, 11, 12.5, 13.5, 15, 17, 18.5, 20, 22 and 25mm</li>\n<li>Choose the size that matches your tile thickness</li>\n</ul>" + CARE,
    "options": ["Size"], "variants": one_al, "ship": "parcel"})
NEW.append({
    "handle": "bat-brass-tiling-angle-1m", "title": "BAT Solid Brass Tiling Angle – 1m Lengths",
    "productType": "L Shaped Trim", "tags": PARCEL, "files": ["brass-angle", "aa-diagram"],
    "seo": {"title": "BAT Solid Brass Tile Trim Angle 1m | ETS Perth",
            "description": "BAT solid brass tile edge angle in 1m lengths, 4.5mm to 25mm. Hard wearing, ages to a warm patina. Ships Australia wide from Perth."},
    "descriptionHtml": "<p>Solid brass L angle in 1m lengths, for feature edges, niches, steps and small jobs. Brass is much harder wearing than aluminium and ages to a warm patina, or can be polished back to bright.</p><ul>\n<li>Material: solid brass</li>\n<li>Length: 1m</li>\n<li>Sizes (tile thickness): 4.5mm to 25mm</li>\n<li>Choose the size that matches your tile thickness</li>\n</ul>" + CARE,
    "options": ["Size"], "variants": one_br, "ship": "parcel"})

jo = [{"options": {"Type": t}, "sku": k, "cost": COST[k], "price": retail(COST[k]), "weight": 0.05, "box": "12 x 8 x 3 cm"}
      for t, k in (("Cove Trim Joiners", "CTJ-6"), ("APC 60 Cove Trim Joiners", "APC60J-6"), ("Balcony Trim Joiners", "BETJ-6"))]
NEW.append({
    "handle": "bat-trim-joiners-6-pack", "title": "BAT Trim Joiners – Pack of 6 (Cove Trim, APC 60, Balcony Trim)",
    "productType": "Tile Trims + Edging Profiles", "tags": PARCEL, "files": ["cove", "balcony"],
    "seo": {"title": "BAT Trim Joiners Pack of 6 | Cove, APC 60, Balcony | ETS",
            "description": "Joiners for BAT Cove Trim, APC 60 cove trim and Balcony Trim. Pack of 6 for neat, aligned joints between lengths. Ships Australia wide."},
    "descriptionHtml": "<p>Joiners that slot into the back of BAT trims so two lengths line up perfectly, with no step or gap at the joint. Choose the joiner that matches your trim.</p><ul>\n<li>Pack of 6</li>\n<li>Cove Trim joiners: suit BAT Cove Trim</li>\n<li>APC 60 joiners: suit BAT APC 60 All Purpose Cove Trim</li>\n<li>Balcony Trim joiners: suit BAT Balcony Edge Trim</li>\n</ul>" + CARE,
    "options": ["Type"], "variants": jo, "ship": "parcel"})

vi = []
for s, h in (("256", "2.5mm"), ("556", "5.5mm")):
    for c in ("BK", "DG", "SG"):
        k = f"BTXV-{s}-33-{c}"
        vi.append({"options": {"Height": h, "Insert Colour": COL[c]}, "sku": k, "cost": COST[k], "price": retail(COST[k]),
                   "weight": 0.45, "box": "335 x 8 x 6 cm"})
NEW.append({
    "handle": "bat-batex-expansion-joint-vinyl-3-3m", "title": "BAT BATEX Expansion Joint for Vinyl – 3.3m Lengths",
    "productType": "Expansion Trim", "tags": LONG, "files": ["vinyl", "batex"],
    "seo": {"title": "BAT BATEX Vinyl Expansion Joint 3.3m | 2.5 & 5.5mm | ETS Perth",
            "description": "BAT BATEX aluminium expansion joint made for vinyl and hybrid floors. 2.5mm or 5.5mm high, 6mm infill, 3.3m lengths. Black, dark or smokey grey."},
    "descriptionHtml": "<p>A low-profile BATEX movement joint made for vinyl, hybrid and LVT floors. Aluminium side profiles hold a 6mm flexible infill that takes up floor movement and stops cracking and lifting across large areas and doorways.</p><ul>\n<li>Material: aluminium profiles, flexible infill</li>\n<li>Length: 3.3m</li>\n<li>Heights: 2.5mm or 5.5mm (match your floor thickness)</li>\n<li>Infill width: 6mm</li>\n<li>Insert colour: Black, Dark Grey or Smokey Grey</li>\n</ul>" + CARE,
    "options": ["Height", "Insert Colour"], "variants": vi, "ship": "local"})

ss = []
for code in COST:
    m = re.fullmatch(r"MLSTSS-(\d\d)(06|10)-(BK|GR)", code)
    if m:
        h, w, c = m.groups()
        ref = next(x for x in P["bat-mortarloc-expansion-joint-aluminium"]["variants"] if x["sku"].startswith(f"MLSTA-{h}{w}"))
        ss.append({"options": {"Size": f"{int(h)} x {int(w)}mm", "Insert Colour": COL[c]}, "sku": code, "cost": COST[code],
                   "price": retail(COST[code]), "weight": round(ref["weight"] * 0.6 * 2.9, 2), "box": "185 x 8 x 8 cm"})
NEW.append({
    "handle": "bat-mortarloc-expansion-joint-stainless", "title": "BAT MORTARLOC Expansion Joint Stainless Steel – 1.8m Lengths",
    "productType": "Expansion Trim", "tags": LONG, "files": ["mortarloc", "mortarloc-drawing"],
    "seo": {"title": "BAT MORTARLOC Stainless Steel Expansion Joint 1.8m | ETS Perth",
            "description": "BAT MORTARLOC stainless steel expansion joint for thick-bed mortar tiling. 25mm to 50mm high, 6 or 10mm wide, 1.8m lengths. Perth."},
    "descriptionHtml": "<p>MORTARLOC expansion joints are for thick-bed (mortar bed) tiling, where BATEX is for thin-bed adhesive. Two stainless steel side plates hold a neoprene infill, with anchor tabs that lock into the mortar bed. Stainless steel suits commercial kitchens, wet areas and outdoor paving.</p><ul>\n<li>Material: stainless steel side plates, neoprene infill</li>\n<li>Length: 1.8m</li>\n<li>Sizes (height x joint width): 25, 30, 40 and 50mm high; 6mm or 10mm wide</li>\n<li>Insert colour: Grey or Black</li>\n<li>For thick-bed / mortar bed installations</li>\n</ul>" + CARE,
    "options": ["Size", "Insert Colour"], "variants": ss, "ship": "local"})

out = {"variants": V, "products": NEW}
json.dump(out, open("may2026-additions.json", "w"), indent=1, ensure_ascii=False)
n = sum(len(v) for v in V.values())
print(n, "new variants on", len(V), "products;", len(NEW), "new products with", sum(len(p["variants"]) for p in NEW), "variants")
used = {v["sku"] for vs in V.values() for v in vs} | {v["sku"] for p in NEW for v in p["variants"]}
print("total codes used:", len(used))
