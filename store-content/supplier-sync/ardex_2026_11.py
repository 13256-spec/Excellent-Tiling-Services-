"""ARDEX Australia range -> Shopify productSet inputs (11 Nov 2026).

Owner's instruction (11 Nov 2026): "add all Ardex materials to our website ... live SEO pages and all categories
and catalogues ... not available to sell, out of stock for now".

Source: every product page on ardexaustralia.com (the 'product' sitemap, minus the training-event ticket entries and
two empty AUTO-DRAFT pages), downloaded and parsed with ardex-2026-11/parse_ardex_pages.py into
ardex-2026-11/ardex-catalogue-2026-11-11.json; the category listings into ardex-categories.json; the grout colour
selector into grout-colours.json. The product text, technical data, data-sheet links and photos are ARDEX's own.

What is created:
- status ACTIVE, published to the Online Store channel only (not Google, Shop, Facebook, POS or Inbox: those need a
  real price), so the pages are live for search engines and shoppers.
- price 0.00 on every variant (no ARDEX price list yet); the "Price on request" draft theme shows that instead of $0.
  Tags needs-cost + price-check, trade band 0. SKUs are placeholders (ARDEX-<product>-<size>) until the price list
  gives the real codes; wedi items carry wedi's own article numbers where the site lists them.
- inventory tracked, 0 at Maddington, "stop selling when out of stock": every page shows Sold out / Enquire.
- one product per ARDEX product; pack sizes as a Size option, grout colours as a Colour option.

Usage: python3 ardex_2026_11.py  -> ardex-2026-11/ardex-2026-11-11.json (+ a variant report on stdout)
"""
import html as htmlmod
import json
import os
import re

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ardex-2026-11")
VENDOR = "ARDEX"
SUPPLIER = "ARDEX Australia"
LOCATION = "gid://shopify/Location/77786087487"
CAT = {
    "adhesive": "gid://shopify/TaxonomyCategory/ha-1-5-2",   # Cement, Mortar & Concrete Mixes
    "grout": "gid://shopify/TaxonomyCategory/ha-1-5-3",
    "waterproofing": "gid://shopify/TaxonomyCategory/ha-1-8-6",
    "sealant": "gid://shopify/TaxonomyCategory/ha-1-8",
    "primer": "gid://shopify/TaxonomyCategory/ha-1-6-3",
    "gun": "gid://shopify/TaxonomyCategory/ha-15-6-3",
}
GENERIC_IMG = ("Stockist-Locator", "system-selector", "related-projects")
SKIP = {"wpm-1000", "x-18"}  # AUTO-DRAFT pages
SHIP = {
    "parcel": (["ship-parcel", "ebay-post-15"], "Parcel"),
    "bulky": (["ship-parcel", "ship-bulky", "ebay-post-39"], "Bulky parcel"),
    "local": (["ship-local-only", "ebay-pickup-only"], "Perth only (local delivery / pickup)"),
    "dg": (["ship-dangerous-goods", "ebay-pickup-only"], "Dangerous goods (road only)"),
}
DANGEROUS = {"ardex-wpm-270", "ardex-wa-98-adhesive", "ardex-wa-98-solvent", "ardex-wpm-240", "ardex-ce-300", "ardex-ce-330"}

# ---- group = the ARDEX sub-collection (tag ardex-<group>), with the ETS product type and collection tags ----
GROUPS = {
    "adhesives": ("ARDEX tile adhesives", "Adhesives", ["Tile Adhesive", "Adhesives & Additives"], "adhesive"),
    "grouts": ("ARDEX grouts", "Grout", ["Grout"], "grout"),
    "sealants": ("ARDEX silicones & sealants", "Silicone Sealants", ["Silicone & Sealants"], "sealant"),
    "primers": ("ARDEX primers & additives", "Primers & Additives", ["Adhesives & Additives"], "primer"),
    "waterproofing": ("ARDEX waterproofing", "Waterproofing Membranes", ["Waterproofing"], "waterproofing"),
    "levelling": ("ARDEX floor levelling & screeds", "Screeds & Levellers", ["Screeds & Levellers", "Floor Levelling"], "adhesive"),
    "concrete-repair": ("ARDEX concrete repair", "Concrete Repair", ["Concrete Repair"], "adhesive"),
    "civil": ("ARDEX civil engineering", "Civil Engineering", ["Civil Engineering"], None),
    "render": ("ARDEX render", "Render", ["Render"], "adhesive"),
    "flooring-adhesives": ("ARDEX flooring adhesives", "Flooring Adhesives", ["Flooring Adhesives"], "adhesive"),
    "tools": ("ARDEX tools", "Tiling Tools", ["Hand Tools"], None),
    "wedi": ("wedi shower & wet room systems", "Shower Systems", ["wedi"], None),
}
# ARDEX sub-category slug (last part of the products_category URL) -> group, in order of precedence
SUBCAT_GROUP = [
    ("powdered-adhesives", "adhesives"), ("ready-mixed-adhesives", "adhesives"), ("two-part-adhesives", "adhesives"),
    ("tile-adhesives", "adhesives"),
    ("cement-based-grouts", "grouts"), ("epoxy-grouts", "grouts"), ("tile-grouts", "grouts"),
    ("tile-grouts-tile-and-stone-installation-systems", "grouts"), ("epoxy-systems", "grouts"),
    ("silicones", "sealants"), ("construction-sealants", "sealants"),
    ("tiling-primers-bonding-agents-additives", "primers"), ("primers-bonding-agents-additives", "primers"),
    ("render-primers-additives", "primers"),
    ("levelling", "levelling"), ("smoothing", "levelling"), ("screeds", "levelling"), ("patching", "levelling"),
    ("repair-mortars", "levelling"), ("floor-levelling", "levelling"), ("moisture-barrier-systems", "waterproofing"),
    ("sound-deadening", "levelling"), ("uncoupling-crack-isolation-systems", "levelling"),
    ("undertile-waterproofing", "waterproofing"), ("undertile-membranes", "waterproofing"),
    ("external-roof-deck-membrane", "waterproofing"), ("below-grade-membranes", "waterproofing"),
    ("torch-applied-membranes", "waterproofing"), ("weldtec-membranes", "waterproofing"),
    ("external-facade-coatings", "waterproofing"), ("butynol", "waterproofing"), ("drainage-systems", "waterproofing"),
    ("preparatory-products-primers", "waterproofing"), ("waterproofing-roofing-membranes", "waterproofing"),
    ("concrete-repair-mortars", "concrete-repair"), ("construction-grout", "concrete-repair"),
    ("crack-repair-injection", "concrete-repair"), ("structural-grouts-and-mortars", "concrete-repair"),
    ("concrete-repair", "concrete-repair"),
    ("geotechnical", "civil"), ("injection-resins", "civil"), ("civil-engineering", "civil"),
    ("cement-render", "render"), ("render", "render"),
    ("flooring-adhesives", "flooring-adhesives"),
    ("tools", "tools"), ("tool-safety-equipment", "tools"),
    ("building-systems", "wedi"), ("shower-systems", "wedi"), ("system-accessories", "wedi"), ("wedi", "wedi"),
    ("natural-stone-systems", "adhesives"), ("prefab-modular-offsite", "waterproofing"),
]
# per-product type overrides (slug -> (group, type, extra tags))
TYPE_OVERRIDE = {
    # waterproofing accessories (tapes, primers, flashings, outlets, boards) rather than membranes
    **{s: ("waterproofing", "Waterproofing Accessories", []) for s in [
        "ardex-stb-tape", "ardex-deckweb", "ardex-multiprime", "ardex-ca-750", "ardex-wpm-710", "ardex-flashing-tape",
        "ardex-weldtec-corners", "ardex-wa-98-adhesive", "ardex-wa-98-solvent", "ardex-seam-tape", "ardex-butynol-scupper",
        "ardex-construction-detail-bandage", "ardex-cured-flashing", "ardex-uncured-flashing", "ardex-p-9", "ardex-ud-158",
        "ardex-wpm-265", "ardex-wpm-270", "ardex-wpm-299-seam-primer", "ardex-wpm-368", "ardex-wpm-405", "ardex-dropper",
        "ardex-pressure-seal", "ardex-wpm-240", "ardex-fixing-washers", "ardex-protection-board", "ardex-ud-150",
        "wedi-subliner-dry", "wedi-sealing-tape", "wedi-sealing-gaiter-dn10-dn25"]},
    "ardex-wpm-657": ("sealants", "Silicone Sealants", []),
    "ardex-bituminous-roof-sealant": ("sealants", "Silicone Sealants", []),
    "ardex-ra-54": ("sealants", "Silicone Sealants", []),
    "ardex-st-2": ("sealants", "Silicone Sealants", []),
    "ardex-sg-spray": ("sealants", "Silicone Accessories", []),
    "ardex-pmo-450": ("waterproofing", "Waterproofing Membranes", []),
    "ardex-pmo-593": ("levelling", "Screeds & Levellers", []),
    "ardex-af-180-ms": ("flooring-adhesives", "Flooring Adhesives", []),
    "ardex-ds-40": ("levelling", "Uncoupling & Acoustic Mats", []),
    "ardex-ds-60-decoupling-mat": ("levelling", "Uncoupling & Acoustic Mats", []),
    "ardex-ui-740-flexbone": ("levelling", "Uncoupling & Acoustic Mats", []),
    "ardex-a-30": ("levelling", "Screeds & Levellers", []), "ardex-a-45": ("levelling", "Screeds & Levellers", []),
    "ardex-a-46-2": ("levelling", "Screeds & Levellers", []),
    "ardex-e-25-2": ("primers", "Primers & Additives", []), "ardex-abacrete": ("primers", "Primers & Additives", []),
    "ardex-p-38": ("primers", "Primers & Additives", []),
    "ardex-wa-100": ("adhesives", "Adhesives", []), "ardex-x-32": ("adhesives", "Adhesives", []),
    "ardex-quickbond": ("adhesives", "Adhesives", []),
    "ardex-ca-20-p-plus": ("adhesives", "Adhesives", ["Silicone & Sealants"]),
    # tools
    **{s: ("tools", "Tiling Trowels & Floats", ["Trowels"]) for s in [
        "ardex-gt-bullnose-hand-trowel-410mm-301-stainless-steel", "ardex-gt-finishing-trowel-280-x-130mm-420-stainless-steel",
        "ardex-gt-notch-trowel-10mm-280-x-130mm-420-stainless-steel", "ardex-gt-notch-trowel-12mm-280-x-130mm-420-stainless-steel",
        "ardex-gt-notch-trowel-6mm-280-x-130mm-420-stainless-steel", "ardex-gt-notch-trowel-8mm-280-x-130mm-420-stainless-steel",
        "ardex-gt-splash-trowel-180mm-420-stainless-steel"]},
    **{s: ("tools", "Screeding Tools", []) for s in ["ardex-gt-levelling-gauging-rake-600mm", "ardex-gt-smoothing-stand-up-trowel-500mm", "ardex-gt-telescopic-bar-90-200cm"]},
    **{s: ("tools", "Mixers", []) for s in ["gauging-bucket", "graduated-mixing-pail", "grout-mixing-paddle", "mixing-paddle-2"]},
    "micro-sponge": ("tools", "Sponges and Grouting Systems", []),
    "ardex-gt-grout-washboy-system-pro": ("tools", "Grout Clean Up", []),
    **{s: ("tools", "Silicone Accessories", []) for s in ["heavy-duty-caulking-gun", "heavy-duty-dual-cartridge-caulking-gun-21-ratio", "ardex-gt-silicone-applicator-3-pack"]},
    **{s: ("tools", "Waterproofing Tools", []) for s in ["roller-brass", "small-hand-roller"]},
    **{s: ("tools", "Tiling Tools", []) for s in ["ardex-gt-multi-tool-75mm-420-stainless-steel", "ardex-gt-scraper-50mm-420-stainless-steel", "ardex-gt-scraper-75mm-420-stainless-steel", "wedi-putty-knife", "wedi-fastener-kit", "wedi-washers"]},
    **{s: ("tools", "Tile Leveling Systems", ["Tile Spacers"]) for s in ["ardex-gt-ardipegs-levelling-pegs-250-pack", "l-a-s-h"]},
    # wedi
    **{s: ("wedi", "Tile Backer Boards", []) for s in ["wedi-building-board", "wedi-construct-board", "wedi-vapor-85"]},
    "wedi-321": ("wedi", "Adhesives", ["Tile Adhesive"]),
    "wedi-610-adhesive-sealant": ("wedi", "Silicone Sealants", ["Silicone & Sealants"]),
    "wedi-620-sealant": ("wedi", "Silicone Sealants", ["Silicone & Sealants"]),
}
TAXONOMY_BY_TYPE = {"Adhesives": "adhesive", "Grout": "grout", "Silicone Sealants": "sealant", "Primers & Additives": "primer",
                    "Waterproofing Membranes": "waterproofing", "Waterproofing Accessories": "waterproofing",
                    "Screeds & Levellers": "adhesive", "Concrete Repair": "adhesive", "Render": "adhesive",
                    "Flooring Adhesives": "adhesive", "Silicone Accessories": "gun"}

# ---- variants: explicit lists where the page text is not a clean size list. (option values dict, sku suffix, kg) ----
V = {}  # slug -> dict(options=[names], variants=[({opt: val}, sku_suffix, kg)])


def grout(slug, code, colours, sizes, only=None, size_only=None):
    """colours x sizes; `only` = {colour: [sizes]} restrictions; size_only = {size: [colours]}."""
    out = []
    for c, _hex in colours:
        for s in sizes:
            if only and c in only and s not in only[c]:
                continue
            if size_only and s in size_only and c not in size_only[s]:
                continue
            out.append(({"Colour": c, "Size": s}, f"{code}-{c}-{s}", kg_of(s)))
    V[slug] = {"options": ["Colour", "Size"], "variants": out}


def kg_of(size):
    m = re.search(r"([\d.]+)\s*(kg|l|ml)\b", size.lower())
    if not m:
        return None
    n = float(m.group(1))
    return {"kg": n, "l": n * 1.1, "ml": n / 1000 * 1.2}[m.group(2)]


GC = json.load(open(os.path.join(HERE, "grout-colours.json")))
grout("ardex-fg-8", "FG8", GC["fg-8"], ["1.5kg", "5kg", "20kg"],
      only={c: ["5kg"] for c in ["Macchiato", "Pewter Blue", "Sandalwood", "Mocha"]})
grout("ardex-fs-dd", "FSDD", GC["fs-dd"], ["1.5kg", "5kg", "20kg"],
      size_only={"1.5kg": ["Ultra White"], "20kg": ["Ultra White"]})
grout("ardex-wj-50", "WJ50", GC["wj-50"], ["20kg"])
grout("ardex-eg-15", "EG15", GC["eg-15"], ["Kit"])
V["ardex-eg-15"]["variants"] = [({"Colour": c, "Size": "Kit"}, f"EG15-{c}", 7) for c, _ in GC["eg-15"]]
V["ardex-white-grout"] = {"options": ["Size"], "variants": [({"Size": "5kg"}, "WHITE-5KG", 5), ({"Size": "20kg"}, "WHITE-20KG", 20)]}
V["ardex-eg-900-c"] = {"options": ["Size"], "variants": [({"Size": "Kit (1kg A + 0.6kg B + 5kg colour pack)"}, "EG900C-KIT", 7)]}
V["ardex-eg-800-f"] = {"options": ["Size"], "variants": [({"Size": "Kit (8L A + 4L B + 15kg colour pack)"}, "EG800F-KIT", 28)]}
V["ardex-optima"] = {"options": ["Size"], "variants": [({"Size": "Mini kit (1.7kg liquid + 5kg powder)"}, "OPTIMA-MINI", 7), ({"Size": "Large kit (10kg liquid + 6 x 5kg powder)"}, "OPTIMA-LARGE", 40)]}
V["ardex-isoflex"] = {"options": ["Size"], "variants": [({"Size": "Kit (20kg liquid + 2 x 20kg powder)"}, "ISOFLEX-KIT", 60)]}
V["ardex-wpm-002"] = {"options": ["Size"], "variants": [({"Size": "Kit (20kg Part A + 20kg Part B)"}, "WPM002-KIT", 40)]}
V["ardex-wa-100"] = {"options": ["Size"], "variants": [({"Size": "20L kit (2 x 10L)"}, "WA100-20L", 24)]}
V["ardex-ca-20-p-plus"] = {"options": ["Colour", "Size"], "variants": [
    ({"Colour": "White", "Size": "310ml cartridge"}, "CA20P-WHITE-310", 0.5), ({"Colour": "White", "Size": "600ml sausage"}, "CA20P-WHITE-600", 0.9),
    ({"Colour": "Black", "Size": "310ml cartridge"}, "CA20P-BLACK-310", 0.5), ({"Colour": "Grey", "Size": "310ml cartridge"}, "CA20P-GREY-310", 0.5)]}
V["ardex-ra-040"] = {"options": ["Colour", "Size"], "variants": [({"Colour": c, "Size": "600ml sausage"}, f"RA040-{c}-600", 0.9) for c in ["Grey", "White"]]}
V["ardex-x-18"] = {"options": ["Colour", "Size"], "variants": [
    ({"Colour": "White", "Size": "5kg"}, "X18-WHITE-5KG", 5), ({"Colour": "White", "Size": "20kg"}, "X18-WHITE-20KG", 20),
    ({"Colour": "Grey", "Size": "20kg"}, "X18-GREY-20KG", 20)]}
V["ardex-protection-board"] = {"options": ["Colour"], "variants": [({"Colour": c}, f"PROTBOARD-{c}", 2) for c in ["Natural", "Black"]]}
V["ardex-wpm-300"] = {"options": ["Colour"], "variants": [({"Colour": c}, f"WPM300-{c}", 20) for c in ["Grey", "Mojo Black"]]}
V["ardex-deckweb"] = {"options": ["Size"], "variants": [({"Size": "100mm x 50m"}, "DECKWEB-100", 2), ({"Size": "190mm x 50m"}, "DECKWEB-190", 3.5)]}
V["ardex-wpm-710"] = {"options": ["Size"], "variants": [({"Size": "300mm x 20m roll"}, "WPM710-300", 6), ({"Size": "100mm x 20m roll"}, "WPM710-100", 2), ({"Size": "Detail patch 150mm"}, "WPM710-PATCH", 0.3)]}
V["ardex-dropper"] = {"options": ["Size"], "variants": [({"Size": "180 x 90mm"}, "DROPPER-90", 0.5), ({"Size": "180 x 110mm"}, "DROPPER-110", 0.6)]}
V["ardex-butynol-scupper"] = {"options": ["Size"], "variants": [({"Size": "100mm"}, "SCUPPER-100", 0.5), ({"Size": "210mm"}, "SCUPPER-210", 0.8)]}
V["ardex-ce-330"] = {"options": ["Size"], "variants": [({"Size": "20L drum"}, "CE330-20L", 22), ({"Size": "Accelerator 1L"}, "CE330-ACC-1L", 1.2)]}
V["ardex-ce-460"] = {"options": ["Size"], "variants": [({"Size": f"{t}mm x {l}"}, f"CE460-{t}-{l}", 10) for t in ["25", "32", "40"] for l in ["6m", "8m", "10m", "11.8m"]]}
V["ardex-ds-40"] = {"options": ["Size"], "variants": [({"Size": "750 x 500 x 4.5mm, carton of 10"}, "DS40-CTN10", 8)]}
V["ardex-p-82"] = {"options": ["Size"], "variants": [({"Size": "2kg kit"}, "P82-2KG", 2.2), ({"Size": "8kg kit"}, "P82-8KG", 8.5)]}
V["ardex-af-171"] = {"options": ["Size"], "variants": [({"Size": "15L pail (18kg)"}, "AF171-15L", 18)]}
V["ardex-af-271"] = {"options": ["Size"], "variants": [({"Size": "15L pail (18kg)"}, "AF271-15L", 18)]}
V["ardex-wpm-157"] = {"options": ["Size"], "variants": [({"Size": "20kg pail (15.4L)"}, "WPM157-20KG", 20)]}
V["ardex-pmo-450"] = {"options": ["Size"], "variants": [({"Size": "30m x 0.99m roll"}, "PMO450-ROLL", 20)]}
V["ardex-ds-60-decoupling-mat"] = {"options": ["Size"], "variants": [({"Size": "20m x 1.4m roll"}, "DS60-ROLL", 12)]}
V["ardex-ui-740-flexbone"] = {"options": ["Size"], "variants": [({"Size": "20m x 1m roll"}, "UI740-ROLL", 10)]}
V["ardex-wpm-3000x"] = {"options": ["Size"], "variants": [({"Size": "1m x 20m roll"}, "WPM3000X-ROLL", 30)]}
V["ardex-wpm-657"] = {"options": ["Size"], "variants": [({"Size": "Cartridge"}, "WPM657-CART", 0.5)]}
V["ardex-ce-425"] = {"options": ["Title"], "variants": [({"Title": "Default Title"}, "CE425", 10)]}

# ---- helpers ----


def strip_tags(s):
    return htmlmod.unescape(re.sub(r"<[^>]+>", " ", s)).replace("\xa0", " ")


def clean_info(h):
    h = re.sub(r'\s(style|data-start|data-end|class)="[^"]*"', "", h)
    h = re.sub(r"</?span[^>]*>", "", h)
    h = re.sub(r"<p>(&nbsp;|\s)*</p>", "", h)
    h = re.sub(r'<a href="https?://(www\.)?ardexaustralia\.com[^"]*"[^>]*>(.*?)</a>', r"\2", h, flags=re.S)
    h = re.sub(r"\s+", " ", h).strip()
    h = h.replace("&#8211;", "–").replace("&#8217;", "’").replace("&#8220;", "“").replace("&#8221;", "”").replace("&amp;", "&")
    return h


def size_value(raw):
    """'20kg triple layered bag' -> '20kg bag'; 'ARDEX CE 330 – 20L steel drum' -> '20L steel drum'; returns (value, code)."""
    s = raw.strip()
    code = None
    m = re.search(r"\((\d{5})\)\s*$", s)
    if m:
        code = m.group(1); s = s[: m.start()].strip()
    s = re.sub(r"^ARDEX [A-Z0-9 ]+ [–-] ", "", s)
    s = re.sub(r"\s*\([^)]*\)", "", s)  # drop notes in brackets
    s = s.replace("triple layered ", "").replace("KG", "kg").replace("mL", "ml").replace(" litre", "L").replace(" Litre", "L")
    s = re.sub(r"\bBag\b", "bag", s).replace("Pail", "pail")
    s = re.sub(r"(\d)\s+(kg|L|ml)\b", r"\1\2", s)
    s = re.sub(r"\s+", " ", s).strip(" .;")
    return s, code


def generic_variants(p):
    raw = []
    for t in p["tech"]:
        if t["label"].lower() in ("packaging", "pack size", "pack sizes", "sizes", "size", "dimensions", "mat size"):
            raw += t["items"]
    vals = []
    for r in raw:
        v, code = size_value(r)
        if not v or len(v) > 45 or v.lower().startswith(("ardex", "wedi", "available", "cartons", "pallets", "pack of", "1 roll")):
            continue
        if v.lower() in ("various",):
            continue
        if (v, code) not in vals:
            vals.append((v, code))
    if not vals:
        return {"options": ["Title"], "variants": [({"Title": "Default Title"}, "", None)]}
    out = []
    for v, code in vals:
        out.append(({"Size": v}, code or re.sub(r"[^A-Z0-9]+", "", v.upper())[:12], kg_of(v)))
    return {"options": ["Size"], "variants": out}


def product_code(p):
    s = re.sub(r"^(ardex-|wedi-)", "", p["slug"])
    s = re.sub(r"-\d$", "", s)  # WordPress duplicate suffixes (ardex-a-46-2)
    return re.sub(r"[^A-Z0-9]+", "", s.upper())[:24]


def ship_class(slug, group, ptype, variants):
    if slug in DANGEROUS:
        return "dg"
    kgs = [v[2] for v in variants if v[2]]
    mx = max(kgs) if kgs else None
    text = " ".join(v[0].get("Size", "") for v in variants).lower()
    if ptype in ("Tile Backer Boards", "Shower Systems") or any(w in text for w in ("roll", "board", "x 20m", "x 50m", "drum", "sheet")) or group == "civil":
        return "local"
    if mx is None:
        return "parcel" if group == "tools" else "bulky"
    if mx >= 15:
        return "local"
    if mx >= 4:
        return "bulky"
    return "parcel"


def default_kg(group, ptype, v):
    if v[2]:
        return round(v[2], 2)
    return {"tools": 0.6, "wedi": 8.0}.get(group, 5.0)


TITLE = {
    "ardex-ds-60-decoupling-mat": "ARDEX DS 60 Decoupling Mat",
    "ardex-pressure-seal": "ARDEX Pressure Seal Termination Bar",
    "ardex-ca-20-p-plus": "ARDEX CA 20 P Plus Silane Modified Polymer Adhesive & Sealant",
    "roller-brass": "ARDEX Brass Roller",
    "small-hand-roller": "ARDEX Small Hand Roller",
    "gauging-bucket": "ARDEX Gauging Bucket",
    "graduated-mixing-pail": "ARDEX Graduated Mixing Pail 20L",
    "grout-mixing-paddle": "ARDEX Grout Mixing Paddle",
    "mixing-paddle-2": "ARDEX Mixing Paddle",
    "micro-sponge": "ARDEX Micro Sponge",
    "heavy-duty-caulking-gun": "ARDEX Heavy Duty Caulking Gun",
    "heavy-duty-dual-cartridge-caulking-gun-21-ratio": "ARDEX Heavy Duty Dual-Cartridge Caulking Gun (2:1 Ratio)",
    "l-a-s-h": "ARDEX L.A.S.H Tile Levelling System",
    "concrete-crack-lock": "ARDEX Concrete Crack Lock Carbon-Fibre Crack Bridging Stitch",
    "butynol": "ARDEX Butynol Sheet Applied Membrane",
    "fundo-click-and-seal-height-adjustment-kit": "wedi Fundo Click and Seal Height Adjustment Kit",
    "wedi-washers": "wedi Washers (1000 per box)",
    "wedi-fastener-kit": "wedi Fastener Kit, Screws and Washers (100 per box)",
    "wedi-shower-drain-cover-set-tileable": "wedi Tileable Shower Drain Cover Set",
    "wedi-standard-shower-drain-cover-and-frame": "wedi Standard Shower Drain Cover and Frame",
    "wedi-putty-knife": "wedi Corner Putty Knife",
    "wedi-comoda-base": "wedi Comoda Base Curved Wellness Bench",
    "wedi-comoda-bench": "wedi Comoda Bench Curved Wellness Bench",
    "ardex-stb-tape": "ARDEX STB / STA Self-Adhesive Butynol Tape",
    "wedi-click-and-seal-drain-kit-dn80-and-dn100": "wedi Click and Seal Drain Kit DN80 / DN100 for Fundo Shower Bases",
    "wedi-fundo-click-and-seal-drain-kit-dn50": "wedi Fundo Click and Seal Point Drain Kit DN50",
    "wedi-riolito-shower-drain-kit-standard": "wedi Riolito Shower Drain Kit Standard",
    "ardex-wpm-330-facade": "ARDEX WPM 330 Facade Anti-Carbonation Protection Coating",
    "ardex-x-52-improved-glue": "ARDEX X 52 Improved Glue Economical Flexible Rubber Modified Tile Adhesive",
}


def title_of(p):
    if p["slug"] in TITLE:
        return TITLE[p["slug"]]
    name, short = p["name"].strip(), p["short"].strip()
    name = name.replace("ARDEX Root Repell™", "ARDEX Root Repell").replace("ARDEX STB Tape ARDEX STA Tape", "ARDEX STB / STA Tape")
    if not short or name.lower() in short.lower() or short.lower().startswith(name.lower()):
        return name
    short = re.sub(r"\s*\(.*?\)\s*", " ", short).strip()
    short = short.replace("WeldTec TM", "WeldTec").replace("TM ", "")
    if short.lower().startswith("ardex ") or len(short) > 90:
        short = short.split(".")[0]
        if len(short) > 90:
            return name
    return f"{name} {short}"


def seo(p, title, group):
    label = GROUPS[group][0]
    t = title if len(title) <= 58 else p["name"]
    seo_title = f"{t} | ETS Perth"
    short = p["short"].strip() or title
    usp = p["usps"][0].rstrip(".") if p["usps"] else ""
    d = f"{p['name']}: {short.rstrip('.')}."
    if usp and len(d) + len(usp) < 110:
        d += f" {usp}."
    d += f" ARDEX stockist in Maddington, Perth. Enquire for price and availability."
    if len(d) > 160:
        d = f"{p['name']}: {short.rstrip('.')[:95]}. ARDEX stockist in Maddington, Perth. Enquire for price and stock."
    return seo_title[:70], d[:160]


def description(p, title, group):
    out = []
    if p["short"] and p["short"].lower() not in title.lower():
        out.append(f"<p><strong>{htmlmod.escape(p['short'])}</strong></p>")
    info = clean_info(p["info_html"])
    if info:
        out.append(info)
    if p["usps"]:
        out.append("<h3>Key features</h3><ul>" + "".join(f"<li>{htmlmod.escape(u)}</li>" for u in p["usps"]) + "</ul>")
    tech = [t for t in p["tech"] if t["items"] or t["notes"]]
    if tech:
        out.append("<h3>Technical data</h3>")
        for t in tech:
            items = t["items"]
            if len(items) <= 2:
                out.append(f"<p><strong>{htmlmod.escape(t['label'])}:</strong> {htmlmod.escape('; '.join(items))}</p>")
            else:
                out.append(f"<p><strong>{htmlmod.escape(t['label'])}:</strong></p><ul>" + "".join(f"<li>{htmlmod.escape(i)}</li>" for i in items) + "</ul>")
            for n in t["notes"]:
                out.append(f"<p>{htmlmod.escape(n)}</p>")
    dl = [(n, u) for n, u in p["downloads"] if u.lower().endswith(".pdf")]
    if dl:
        out.append("<h3>Data sheets</h3><p>" + " · ".join(f'<a href="{htmlmod.escape(u)}" target="_blank" rel="noopener">{htmlmod.escape(n)} (PDF)</a>' for n, u in dl) + "</p>")
    if group == "grouts" and p["slug"] in ("ardex-fg-8", "ardex-fs-dd", "ardex-wj-50", "ardex-eg-15"):
        out.append("<p>Choose the colour and pack size above. Colours on screen are a guide only: see the ARDEX colour chart in our Maddington showroom before you order.</p>")
    out.append("<p>Genuine ARDEX Australia product, supplied by Excellent Tiling Services in Maddington, Perth. Call 0450 960 543 or send an enquiry for price, stock and lead time; trade accounts welcome.</p>")
    return "".join(out)


def group_of(p, cats):
    slug = p["slug"]
    if slug in TYPE_OVERRIDE:
        g, t, extra = TYPE_OVERRIDE[slug]
        return g, t, extra
    subs = [k.split("__")[-1] for k, c in cats.items() if slug in c["products"]]
    for sub, g in SUBCAT_GROUP:
        if sub in subs:
            return g, GROUPS[g][1], []
    return "tools" if "tool" in slug else "waterproofing", GROUPS["tools"][1] if "tool" in slug else GROUPS["waterproofing"][1], []


def build():
    prods = json.load(open(os.path.join(HERE, "ardex-catalogue-2026-11-11.json")))
    cats = json.load(open(os.path.join(HERE, "ardex-categories.json")))
    out = []
    for p in prods:
        if p["slug"] in SKIP or p["name"] == "AUTO-DRAFT":
            continue
        group, ptype, extra = group_of(p, cats)
        label, _, gtags, _ = GROUPS[group]
        title = title_of(p)
        vdef = V.get(p["slug"]) or generic_variants(p)
        variants = vdef["variants"]
        ship = ship_class(p["slug"], group, ptype, variants)
        ship_tags, freight = SHIP[ship]
        code = product_code(p)
        tags = sorted(set(["Hardware", "ARDEX", "ardex-2026-11", f"ardex-{group}", "supplier-import", "needs-cost", "price-check"]
                          + gtags + extra + ship_tags + (["wedi"] if p["name"].lower().startswith("wedi") or p["slug"].startswith("wedi") else [])))
        seo_title, seo_desc = seo(p, title, group)
        images = [u for u in p["images"] if not any(g in u for g in GENERIC_IMG)]
        files = [{"originalSource": u, "alt": title if i == 0 else f"{title} ({i + 1})", "contentType": "IMAGE"} for i, u in enumerate(images)]
        files += [{"originalSource": v, "alt": f"{title} video", "contentType": "EXTERNAL_VIDEO"} for v in p["videos"][:2]]
        option_names = vdef["options"]
        values = {o: [] for o in option_names}
        for ov, _, _ in variants:
            for o in option_names:
                if ov[o] not in values[o]:
                    values[o].append(ov[o])
        vin = []
        for ov, suffix, kg in variants:
            sku = f"ARDEX-{code}" + (f"-{re.sub(r'[^A-Z0-9.]+', '-', suffix.upper()).strip('-')}" if suffix else "")
            if suffix.isdigit() and len(suffix) == 5:
                sku = f"WEDI-{suffix}"
            vin.append({
                "optionValues": [{"optionName": o, "name": ov[o]} for o in option_names],
                "price": "0.00",
                "inventoryPolicy": "DENY",
                "taxable": True,
                "inventoryQuantities": [{"locationId": LOCATION, "name": "available", "quantity": 0}],
                "inventoryItem": {"sku": sku[:50], "tracked": True,
                                  "measurement": {"weight": {"value": default_kg(group, ptype, (ov, suffix, kg)), "unit": "KILOGRAMS"}}},
            })
        taxo = CAT.get(TAXONOMY_BY_TYPE.get(ptype, ""))
        inp = {
            "title": title,
            "descriptionHtml": description(p, title, group),
            "vendor": VENDOR,
            "productType": ptype,
            "status": "ACTIVE",
            "tags": tags,
            "seo": {"title": seo_title, "description": seo_desc},
            "metafields": [
                {"namespace": "ets", "key": "supplier", "type": "single_line_text_field", "value": SUPPLIER},
                {"namespace": "custom", "key": "supplier", "type": "single_line_text_field", "value": SUPPLIER},
                {"namespace": "ets", "key": "material", "type": "single_line_text_field", "value": (p["short"] or title)[:255]},
                {"namespace": "ets", "key": "range", "type": "single_line_text_field", "value": label},
                {"namespace": "ets", "key": "warranty", "type": "single_line_text_field", "value": "ARDEX Australia manufacturer warranty when installed to the technical data sheet"},
                {"namespace": "ets", "key": "freight_class", "type": "single_line_text_field", "value": freight},
                {"namespace": "ets", "key": "lead_time", "type": "single_line_text_field", "value": "Order in from ARDEX Australia's Perth warehouse: enquire for lead time"},
                {"namespace": "ets", "key": "trade_band", "type": "number_integer", "value": "0"},
            ],
            "productOptions": [{"name": o, "values": [{"name": v} for v in values[o]]} for o in option_names],
            "files": files,
            "variants": vin,
        }
        if taxo:
            inp["category"] = taxo
        out.append({"slug": p["slug"], "source": p["url"], "group": group, "ship": ship, "input": inp})
    return out


if __name__ == "__main__":
    prods = build()
    json.dump(prods, open(os.path.join(HERE, "ardex-2026-11-11.json"), "w"), indent=1, ensure_ascii=False)
    nv = sum(len(x["input"]["variants"]) for x in prods)
    print(f"{len(prods)} products, {nv} variants")
    for x in prods:
        i = x["input"]
        vs = [" / ".join(o["name"] for o in v["optionValues"]) for v in i["variants"]]
        print(f"{x['group']:18s} {i['productType']:28s} {x['ship']:6s} {i['title'][:60]:60s} | {len(vs)}: {'; '.join(vs)[:110]}")
    # self-check
    assert all(v["price"] == "0.00" and v["inventoryPolicy"] == "DENY" for x in prods for v in x["input"]["variants"])
    assert len({x["input"]["title"] for x in prods}) == len(prods), "duplicate titles"
    skus = [v["inventoryItem"]["sku"] for x in prods for v in x["input"]["variants"]]
    assert len(set(skus)) == len(skus), "duplicate SKUs: " + str([s for s in skus if skus.count(s) > 1][:10])
