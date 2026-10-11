"""BAT Tools Book + Raimondi price book (May 2026) -> Shopify products.

  python3 add_tools_raimondi.py TOOLS.json RAIMONDI.json WEB.json OUTDIR [IDS.json]

TOOLS/RAIMONDI.json: rows {sec, code, desc, net} parsed from the two xlsx books.
WEB.json: battrims.com WooCommerce store feed (sku, short_description, images) for photos and copy.
Without IDS.json  -> OUTDIR/tNN.graphql: productSet with the first 20 variants of each product.
With IDS.json     -> OUTDIR/tvNN.graphql: productVariantsBulkCreate for variants past 20 (IDS maps handle -> gid).
Also writes tools-raimondi.json (every product, variant, cost and price).

Sizes, colours and pack counts of one tool become variants of one product; distinct tools stay separate.
SIGMA lines are skipped (the store already sells Sigma through Roberts for less), and codes already
on sale in the store are skipped here and costed in place instead (EXISTING).
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, "pricing")
from price_rule import retail  # noqa: E402
from gqlgen import gql, write_docs  # noqa: E402

tools_f, rai_f, web_f, out = sys.argv[1:5]
ids_f = sys.argv[5] if len(sys.argv) > 5 else None
os.makedirs(out, exist_ok=True)

# store product SKU -> BAT code it is (already live; cost added in place, not duplicated)
EXISTING = {"ETS-HW-001": "BCAL", "ETS-HW-002": "BAT-SS12-SG", "ETS-HW-003": "PAN-SST12", "ETS-HW-006": "BP-DCDB6",
            "X1.5x500": "TC-500", "X1.5x1000": "TC-1000", "W-500": "W-500", "ETS-HW-012": "PAN-TTR-105",
            "BD-MTR-125-R": "BD-MTR-125-R", "BP-PVA036/10": "BP-PVA036/10", "BP-PVA120/10": "BP-PVA120/10",
            "SYNSAFE/1": "BAT-ESS1L", "ETS-HW-016-5L": "BAT-ESS5L"}
SKIP = set(EXISTING.values()) - {"PAN-SST12"}  # the Panther listing doesn't name a notch, keep the full range

# (code regex, product title, option names, desc regex whose groups are the option values)
G = [
    (r"LS-(SMALL|MEDIUM|LARGE)", "BAT Liquid Stirrer - 10mm Shaft", ["Size"], r"Stirrer (.+) x 10mm"),
    (r"PAN-SST\d+", "Panther Stainless Steel Square Notch Trowel - Soft Grip", ["Notch"], r"Trowel (\S+)"),
    (r"BAT-BS[PR]?V\d*-SG", "BAT Bright Steel V Notch Trowel - Soft Grip", ["Notch"], r"Trowel ([\d.]+mm V(?: Flat)?)"),
    (r"BAT-BS\d+-SG", "BAT Bright Steel Square Notch Trowel - Soft Grip", ["Notch"], r"Trowel (\S+)"),
    (r"BAT-SS\d+-SG", "BAT Professional Stainless Steel Square Notch Trowel - Soft Grip", ["Notch"], r"Trowel (\S+)"),
    (r"BAT-LBBST-.*", "BAT Bright Steel Long Blade Trowel - Soft Grip", ["Notch"], r"Trowel (.+?) - S/Grip"),
    (r"BP-GAT\d+", "BAT Pro Gauging Trowel with Swan Neck", ["Size"], r"- (\d+mm)"),
    (r"PS-\d+", "BAT Paint Scraper - Soft Grip", ["Width"], r"- (\d+mm)"),
    (r"BP-TTSQ\d+", "BAT Pro Square Trowel with Swan Neck", ["Size"], r"- (.+mm)"),
    (r"BAT-DHP\d+", "BAT Diamond Hand Polishing Pad", ["Grit"], r"- (\d+ Grit)"),
    (r"BP-PVA\d+(/10)?", "BAT Pro PVA Abrasive Wheel 100mm", ["Grit"], r"- (\d+ Grit(?: \(10 pack\))?)"),
    (r"PRG[BJP]", "Pointed Rubber Grouter", ["Type"], r"- (\w+)"),
    (r"S-(50|100)", "BAT Tiling Sponge 200 x 150mm", ["Thickness"], r"x (\d+mm)$"),
    (r"BL-WPS\d+", "BAT Luxe Waste Pipe Sponge", ["Size"], r"- (.+)$"),
    (r"EPDB-\d+", "BAT Electroplated Diamond Drill Bit", ["Size"], r"Bit (\d+mm)"),
    (r"BP-DCDB\d+", "BAT Pro Dry Cutting Diamond Drill Bit - M14 Thread", ["Size"], r"Bit (\d+mm)"),
    (r"BP-DCDB\d+H", "BAT Pro Dry Cutting Diamond Drill Bit - Hex Shaft", ["Size"], r"Bit (\d+mm)"),
    (r"PAN-TTR-\d+", "Panther Thin Turbo Rim Diamond Blade", ["Size"], r"- (\d+mm)"),
    (r"BD-MTR-.*", "BAT Pro Diamond Mesh Turbo Rim Blade", ["Size"], r"- (\d+mm(?: - Razor)?)"),
    (r"BD-TTR-\d+", "BAT Pro Diamond Thin Turbo Rim Blade", ["Size"], r"- (\d+mm)"),
    (r"BP-DB[BCGP]\d+", "BAT Pro Segmented Diamond Blade for Wet Saws", ["Size", "Material"],
     r"- (\d+mm) - to suit (.+)$"),
    (r"BD-BUSH-.*", "Diamond Blade Reducing Bush", ["Bore"], r"Bush (?:- )?(.+)$"),
    (r"BD-GWSC-\d+", "BAT Super Cluster Diamond Grinding Wheel", ["Size"], r"- (.+)$"),
    (r"BAT-SB-\d+", "BAT Aluminium Screed Bar with Handle 50 x 45mm", ["Length"], r"x (\d+mm)$"),
    (r"BAT-SE72-\d+", "BAT Powder Coated Straight Edge 70 x 20mm", ["Length"], r"x (\d+mm)$"),
    (r"BSE-\d+", "BAT Aluminium Straight Edge 22 x 100mm", ["Length"], r"x (\d+mm)$"),
    (r"SL-\d+", "BAT Spirit Level - 2 Vials", ["Length"], r"- (\d+mm)$"),
    (r"ADA-TM\d+", "ADA Tape Measure", ["Size"], r"Measure (.+)$"),
    (r"BP-BS\d+", "BAT Pro Builders Square", ["Size"], r"- (.+)$"),
    (r"N25BUCK\d+", "BAT Ring Shank Nails 25mm - Bucket", ["Weight"], r"x ([\d.]+kg)"),
    (r"PUF-\d+", "BAT P.U. Float", ["Size"], r"- (.+)$"),
    (r"BAT-SFD50(MB)?", "BAT Chrome Plated Floor Drain 50mm", ["Finish"], r"50mm(?: - (Matt Black))?$"),
    (r"BAT-SFD80(MB)?", "BAT Chrome Plated Floor Drain 80mm", ["Finish"], r"80mm(?: - (Matt Black))?$"),
    (r"BL-SID100(MB)?", "BAT Luxe Square Inspection Drain - 100mm Outlet", ["Finish"], r"Outlet - (.+)$"),
    (r"BL-RPF.*", "BAT Luxe Recessed Round Puddle Flange", ["Size"], r"- (.+)$"),
    (r"KFG-201.*", "NICLIS Grate 85 x 85 x 75mm", ["Finish"], r"75mm (.+)$"),
    (r"KFG-(80[12]|845).*", "NICLIS Square Tile Insert Floor Drain 115 x 115mm", ["Depth", "Finish"],
     r"115 x 115 x (\d+mm) (.+)$"),
    (r"KFG-R902.*", "NICLIS Round Tile Insert Floor Drain 115 x 115 x 75mm", ["Finish"], r"75mm (.+?) \("),
    (r"WPB.*", "NICLIS Waterproofing Bandage", ["Size"], r"Bandage (.+?) \("),
    (r"BAT-PB\d+", "BAT Paint Brush", ["Width"], r"- (\d+mm)"),
    (r"PAN-LSBC.*", "Panther Tile Levelling System Base Clips", ["Clip"], r"System (.+?) x \d+"),
    (r"PAN-LSW\d+", "Panther Tile Levelling System Wedges", ["Pack"], r"x (\d+)"),
    (r"AT-C100-.*", "Atika Replacement Agitation Parts - suit Compact 100", ["Part"], r"Replacement (.+) - suit"),
    (r"AT-C140-.*", "Atika Replacement Agitation Parts - suit Compact 140", ["Part"], r"Replacement (.+) - suit"),
    (r"BSC-\d+", "BATSEAL Pro Ceramic Silicone 310ml", ["Colour"], r"310ml - (.+)$"),
    (r"BSA-\d+", "BATSEAL All-In-One Neutral Cure Silicone 310ml", ["Colour"], r"310ml - (.+)$"),
    (r"S A-APP.*", "BATSEAL Silicone Applicators - Set of 3", ["Profile"], r"Set of 3, (.+)$"),
    (r"S A-BR-\d+", "BATSEAL Backer Rod 6mm", ["Length"], r"6mm x (\d+m)"),
    (r"BC-HPS\d", "BATSEAL HPS High Porosity Sealer", ["Size"], r"- (\dL) Liquid"),
    (r"BC-LPS\d", "BATSEAL LPS Low Porosity Sealer", ["Size"], r"- (\dL) Liquid"),
    (r"BC-MPC\d", "BATSEAL MPC Multi Purpose Cleaner", ["Size"], r"- (\dL) Liquid"),
    (r"BAT-ESS\dL", "BAT SynSafe Acid - 100% Biodegradable", ["Size"], r"(\d Litre)"),
    (r"BC-DSC\d", "BATSEAL De-Scale Phosphoric Acid Cleaner", ["Size"], r"- (\d+ Ltr)"),
    (r"BC-SML\d+", "BATSEAL Matt Look Solvent Based Sealer", ["Size"], r"- (\d+ Ltr)"),
    (r"BC-SPELSB\d", "BATSEAL Silcopel Solvent Based Sealer", ["Size"], r"- (\d+ Ltr)"),
    (r"BC-SWL\d+", "BATSEAL Wet Look Solvent Based Sealer", ["Size"], r"- (\d+ Ltr)"),
    (r"BC-EVSOL\d", "BATSEAL Eversol Solvent", ["Size"], r"- (\d+ Ltr)"),
    # spacers + wedges: one product per type and size, pack size as the variant
    (r"(TC|TS)\d*D?B?-.*|J?W-\d+|J?WB-(?!9)\d+", None, ["Pack"], r"^(.+?) x\s+(\d+ (?:Bag|Bucket).*)$"),
    # Raimondi
    (r"RAI-SMS\d+", "Raimondi SMS Electric Wet Saw 3HP", ["Model"], r"(SMS \d+)"),
    (r"RAI-ZOE\d+A", "Raimondi Zoe Electric Wet Saw 3HP", ["Model"], r"(Zoe \d+A)"),
    (r"RAI-PZ\d+THD", "Raimondi Tile Holding Device", ["Suits"], r"(?:suit|Suit) (.+)$"),
    (r"RAI-ZOE\d+SAR", "Raimondi Zoe Spare Aluminium Rail", ["Model"], r"(Zoe \d+A)"),
    (r"RAI-BDB\d+", "Raimondi Bulldog Polishing Band", ["Grit"], r"Band (D\d+)"),
    (r"RAI-BFW\d+R", "Raimondi Bulldog Finishing Wheel", ["Radius"], r"(R - \d+mm)"),
    (r"RAI-BPW.*", "Raimondi Bulldog Polishing Wheel", ["Radius", "Grit"], r"(R - \d+mm) - (\d+ Grit)"),
    (r"RAI-BSW\d+R(CR)?", "Raimondi Bulldog Shaping Wheel", ["Radius"], r"(R - \d+mm(?: - Continuous Rim)?)"),
    (r"RAI-RFH\d+", "Raimondi Rai-Fix Hooks", ["Pack"], r"Hooks - (.+)$"),
    (r"RAI-WRM\d+", "Raimondi White Rubber Mallet", ["Weight"], r"- (\d+gm)"),
    (r"RAI-BSTSR\d+", "Raimondi Bright Steel Slant Ridge Trowel", ["Notch"], r"(\d+mm)"),
    (r"RAI-LBT\d+", "Raimondi 480mm Long Bladed Trowel", ["Notch"], r"(\d+mm)"),
    (r"RAI-LBTSR\d+", "Raimondi 480mm Long Bladed Slant Ridge Trowel", ["Notch"], r"(\d+mm)"),
    (r"RAI-FRS\d+", "Raimondi Double Foam Rubber Squeegee", ["Width"], r"(\d+mm)"),
    (r"RAI-FRS\d+SR", "Raimondi Foam Rubber Squeegee Spare Rubber", ["Width"], r"(\d+cm)"),
    (r"RAI-AFL\d+G", "Raimondi Berta Anti Foam Liquid", ["Size"], r"- (\d+gm)"),
    (r"RAI-SMART4?", "Raimondi Smart Grout Clean Up System", ["Pack"], r"System (.+)$"),
    (r"RAI-SKIPPER4?", "Raimondi Skipper Grout Clean Up System", ["Pack"], r"System (.+)$"),
    (r"RAI-SPAD[FMH]", "Raimondi Scouring Pad", ["Grade"], r"- (.+)$"),
    (r"RAI-SLEXT\d+", "Raimondi Extending Slab Lifter", ["Suits"], r"Suit (.+)$"),
    (r"RAI-TC.*", "Raimondi Tile Crosses", ["Size"], r"Crosses - (.+)$"),
    (r"RAI-DS\d+", "Raimondi Re-Usable Double Spacer", ["Size"], r"Spacer - (.+)$"),
    (r"RAI-DPK6..", "Raimondi Diamond Pad Kit 100mm - 6 Piece", ["Suits"], r"suit (.+)$"),
    (r"RAI-DPP100\d+", "Raimondi Diamond Polishing Pad 100mm", ["Grit"], r"- (\d+ Grit)"),
    (r"RAI-MAXTFD.", "Raimondi Maxititina Felt Disc", ["Grade"], r"Disc - (.+)$"),
    (r"RAI-IPERFD.", "Raimondi Ipertitina Felt Disc", ["Colour"], r"Ipertitina (\w+) Felt"),
    (r"RAI-IPERPGS\d", "Raimondi Ipertitina Planetary Gear Set", ["Heads"], r"- (\d Head)"),
    (r"RAI-27LB|RAI-45LB", "Raimondi Bucket with Steel Handle", ["Size"], r"(\d+ Litre)"),
]

SIZE_WORDS = {"SMALL": 0, "MEDIUM": 1, "LARGE": 2}


def vendor(code):
    if re.match(r"WB-(PROFI|9\d{3}|HANDSP)", code):
        return "Washboy"
    for p, v in (("PAN-", "Panther"), ("RAI-", "Raimondi"), ("KFG-", "NICLIS"), ("WPB", "NICLIS"),
                 ("AT-", "Atika"), ("ADA-", "ADA Instruments")):
        if code.startswith(p):
            return v
    return "BAT"


def clean(s):
    s = re.sub(r"\s+NEW$", "", s.strip())
    s = s.replace("B.A.T.", "BAT").replace("tickness", "thickness").replace("Mulitlayer", "Multilayer")
    s = s.replace("upto", "up to").replace("MItre", "Mitre").replace("Clean up Up", "Clean Up").replace("  ", " ")
    s = s.replace("S/Grip", "Soft Grip").replace("Lge", "Large").replace("Rep.", "Replacement")
    s = s.replace("Com. Vel.", "Commodore Velcro").replace("Sp. ", "Spare ").replace("Squeez.", "Squeeze")
    s = s.replace("P'Rapid", "Pulirapid").replace("B/Steel", "Bright Steel").replace("suit.", "suit")
    s = s.replace("Rein.", "Reinforced").replace("Inspiection", "Inspection")
    return re.sub(r"\s+", " ", s).strip(" -")


# ---- shop category, Google category, product type, weight and box by keyword --------------------------
KIND = [  # (regex on title, productType, Shopify category, kg, box)
    (r"e-Fox", "Tiling Machines", "ha-15-34", 4.0, "45 x 35 x 20 cm"),
    (r"Roller Plate|Vibrating Plate|Extension Table|Transformer|Planetary Gear|Ballast|Watertank|Tank$|"
     r"Manual Feed Kit|Side Extensions", "Tiling Machine Parts", "ha-15-34", 8.0, "60 x 40 x 30 cm"),
    (r"Squeeze Roller|Bucket Roller|Replacement Roller Set", "Grout Clean Up", "ha-15-34", 0.4, "30 x 15 x 10 cm"),
    (r"Clean Up System|Clean Up Set$|Washboy PROFI", "Grout Clean Up", "ha-15-34", 4.0, "50 x 40 x 40 cm"),
    (r"Electric Wet Saw|Bi-Bulldog", "Tile Saws", "ha-15-62-6", 75.0, "110 x 70 x 60 cm"),
    (r"Bulldog Profiling", "Tiling Machines", "ha-15-34", 12.0, "60 x 40 x 30 cm"),
    (r"Raizor .*Cutting System", "Tile Cutters", "ha-15-11-7", 14.0, "340 x 20 x 15 cm"),
    (r"Easymove|Bigfoot|Trolley|Tyrell|Nelson|Pugiol|OnlyOne|Work ?Bench|Worktable", "Large Format Tile Handling",
     "ha-15-34", 18.0, "140 x 70 x 20 cm"),
    (r"Ipertitina .*Brush|Maxititina Machine|Berta Grout|Rosina|Iperbet Electric|Fluid Mix Special|Mastino|"
     r"Terranova Vibrator|Lupetto Vibrator|BC 45", "Tiling Machines", "ha-15-34", 30.0, "80 x 60 x 60 cm"),
    (r"Screed Bar|Straight Edge", "Screeding Tools", "ha-15-34", 2.5, "LEN x 10 x 8 cm"),
    (r"Spirit Level|Adjustable Level", "Levels", "ha-15-36-17", 1.2, "LEN x 10 x 5 cm"),
    (r"Trowel|Float|Squeegee|Grouter|Scraper|Rake|Beater|Mallet|Rasp", "Tiling Trowels & Floats", "ha-15-34-8", 0.5,
     "35 x 15 x 6 cm"),
    (r"Drill Bit|Drill Set", "Diamond Drill Bits", "ha-14-4-1-1", 0.15, "15 x 6 x 4 cm"),
    (r"Diamond.*Blade|Turbo Rim|Slotted Rim|Segmented|Grinding Wheel|Reducing Bush|Polishing Pad|Abrasive Wheel|Pad Kit|Shaping Wheel|Finishing Wheel|Polishing Wheel|"
     r"Polishing Band|Abrasive Pad|Cutting Wheel", "Diamond Blades & Abrasives", "ha-14-23-2", 0.4, "30 x 30 x 4 cm"),
    (r"Crosses|T Shapes|Wedges|Spacer|Levelling|Clipdozer|Rai-Fix", "Tile Spacers & Levelling", "ha-15-34", 0.6,
     "25 x 20 x 10 cm"),
    (r"Silicone|Sealer|Cleaner|Acid|Solvent|Backer Rod|Applicator|Caulking|Joint Cutter|Nozzle Cutter|Anti Foam",
     "Sealants, Sealers & Cleaners", "ha-1-8", 0.5, "30 x 10 x 10 cm"),
    (r"Drain|Grate|Tile Insert|Puddle Flange|PVC Collar", "Floor Drains", "ha-10-2-3-1", 0.4, "18 x 18 x 12 cm"),
    (r"Waterproofing|Paint|Roller", "Waterproofing Tools", "ha-15-34", 0.4, "35 x 25 x 8 cm"),
    (r"Electric Hand Mixer", "Mixing Tools", "ha-15-21", 5.5, "60 x 30 x 20 cm"),
    (r"Stirrer|Mixer|Iperbet|Fluid Mix", "Mixing Tools", "ha-15-21", 1.5, "65 x 18 x 18 cm"),
    (r"Sponge|Washboy|Maximo|Grout Clean|Sweepex|Scouring|Plastic Grate|Broom", "Grout Clean Up", "ha-15-34", 0.4,
     "35 x 25 x 15 cm"),
    (r"Bucket", "Mixing Tools", "ha-15-34", 1.0, "40 x 35 x 35 cm"),
    (r"Suction Cup|Closer|Closing Tool|Levtop|Medusa|Biventosa|Triventosa|RV 175", "Suction Cups & Lifters",
     "ha-15-34", 1.0, "25 x 20 x 15 cm"),
    (r"Nipper|Cutter|Pliers|Grout Remover|Knife|Compass|Raizor|Blade", "Tile Cutters", "ha-15-11-7", 0.5, "30 x 15 x 6 cm"),
    (r"Tape|Square|Laser|Measure", "Measuring Tools", "ha-15-36", 0.4, "25 x 15 x 6 cm"),
    (r"Knee ?[Pp]ad|Kneepad|Cushion|Shoes|Platform|Hand Support|Tool Bag|Kneeling", "Knee Pads & Workwear", "ha-15-34",
     0.8, "35 x 25 x 12 cm"),
    (r"Nails", "Fixings", "ha-6-14-2-8", 1.0, "15 x 15 x 12 cm"),
]
GOOGLE = {"ha-10-2-3-1": "2216", "ha-1-8": "503743"}  # everything else: Hardware > Tools (1167)


def kind(title):
    for rx, ptype, cat, kg, box in KIND:
        if re.search(rx, title, re.I):
            return ptype, cat, kg, box
    return "Tiling Tools", "ha-15-34", 0.6, "30 x 20 x 10 cm"


def length_mm(desc):
    m = re.search(r"(\d{3,4})\s*mm|(\d+(?:\.\d+)?)\s*m\b|(\d{3})\s*cm", desc)
    if not m:
        return 0
    if m.group(1):
        return int(m.group(1))
    if m.group(2):
        return float(m.group(2)) * 1000
    return int(m.group(3)) * 10


LOCAL = re.compile(r"Electric Wet Saw|Bi-Bulldog|Raizor .*Cutting System|Easymove|Bigfoot|CAM Advanced|"
                   r"Tyrell|Nelson|Ipertitina (110|Plus)|Maxititina Machine|Berta Grout|Rosina|Mastino|Terranova "
                   r"Vibrator|Iperbet Electric|Fluid Mix Special|Spirit Levels - KIT|Floor Scraper 300mm x 1300mm|"
                   r"Pugiol|Sealer - 20 Ltr|Extension Table|5 Roller Extension")


def weight(title, desc, kg, cost):
    if "KIT" in desc:
        return 5.0
    L = length_mm(desc)
    if re.search(r"Screed Bar", title):
        return round(0.9 * L / 1000 + 0.3, 2)
    if re.search(r"Straight Edge", title):
        return round((0.55 if "22 x 100" in desc else 0.45) * L / 1000, 2)
    if re.search(r"Spirit Level", title):
        return round(0.25 + 0.6 * L / 1000, 2)
    if re.search(r"Bucket with", title):
        return 2.0
    if re.search(r"Sealer|Cleaner|Acid|Solvent", title) and (m := re.search(r"(\d+(?:\.\d+)?) ?(?:L|Ltr|Litre)\b", desc)):
        return round(float(m.group(1)) * 1.05 + 0.2, 2)
    if m := re.search(r"x ([\d.]+)kg", desc):
        return round(float(m.group(1)) + 0.1, 2)
    if m := re.search(r"x\s+(\d+) (Bag|Bucket)", desc):
        n = int(m.group(1))
        return round(n * (0.0012 if re.search(r"(?<![\d.])(5|10)mm", desc) else 0.0004) + (0.4 if m.group(2) == "Bucket"
                     else 0.02), 2)
    if re.search(r"Blade", title) and (m := re.search(r"(\d{3})mm", desc)):
        return round((int(m.group(1)) / 100) ** 2 * 0.12, 2)
    if kg >= 14 and cost > 1500:  # big machines: scale by price
        return round(min(110, kg * cost / 2500), 1)
    return kg


def box(title, desc, b):
    if "LEN" in b:
        L = length_mm(desc) or 1800  # the level kit packs to its longest level
        return b.replace("LEN", str(int(L / 10) + 5))
    return b


def slug(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")


# ---- website photos and copy ------------------------------------------------------------------------------
web = json.load(open(web_f))
by_sku, patterns = {}, []
for p in web:
    s = (p.get("sku") or "").strip().upper()
    if not s:
        continue
    if "(" in s:  # e.g. BSA-(COLOUR), BP-DBC(SIZE)
        patterns.append((re.compile(re.sub(r"\\\([^)]*\\\)", ".+", re.escape(s)) + "$"), p))
    else:
        by_sku.setdefault(s, p)


# no listing of their own on battrims.com: borrow the photo of a near-identical sibling
IMG_ALIAS = {"BAT-SFD50": "BAT-SFD100SH", "BAT-SFD50MB": "BAT-SFD100SH", "BAT-SFD80": "BAT-SFD100SH",
             "BAT-SFD80MB": "BAT-SFD100SH", "BAT-LSFD80": "BAT-SFD100SH", "BAT-SFD100MB": "BAT-SFD100SH",
             "BAT-SFD100": "BAT-SFD100SH", "RAI-RAIZOR-SWT": "RAI-RAIZOR-SW", "RAI-RAIZORM2PSW": "RAI-RAIZOR-SW",
             "RAI-RAIZORM2SW": "RAI-RAIZOR-SW", "RAI-IPERTITINAPLUS": "RAI-IPER110"}


def web_for(code):
    c = IMG_ALIAS.get(code, code).upper()
    if c in by_sku:
        return by_sku[c]
    base = re.sub(r"/\d+$", "", c)
    if base in by_sku:
        return by_sku[base]
    for rx, p in patterns:
        if rx.match(c):
            return p
    return None


def text(h):
    h = re.sub(r"<br\s*/?>", "\n", h or "")
    h = re.sub(r"</(p|li)>", "\n", h)
    h = re.sub(r"<[^>]+>", "", h)
    return re.sub(r"[ \t]+", " ", html.unescape(h)).strip()


# ---- build ------------------------------------------------------------------------------------------------
rows = [r for r in json.load(open(tools_f)) if "SIGMA" not in r["sec"]] + json.load(open(rai_f))
products, order = {}, []
for r in rows:
    code = r["code"].strip()
    if code in SKIP or r["net"] is None:
        continue
    desc = re.sub(r"\s+", " ", r["desc"]).strip()
    for rx, title, opts, vrx in G:
        if re.fullmatch(rx, code):
            m = re.search(vrx, desc)
            if not m:
                raise ValueError((code, desc, vrx))
            vals = [g for g in m.groups()]
            if title is None:  # spacers: title from the description, pack size as the value
                title, vals = (("BAT " if not desc.startswith("Raimondi") else "") + m.group(1)), [m.group(2)]
            vals = [clean(v or "Chrome") for v in vals]
            vals = [v + "mm" if re.fullmatch(r"\d+ x \d+", v) else v for v in vals]
            break
    else:
        title, opts, vals = clean(desc), ["Title"], ["Default Title"]
        if vendor(code) == "BAT" and not title.upper().startswith(("BAT", "BATSEAL")):
            title = "BAT " + title
    title = clean(title)
    if title not in products:
        products[title] = {"title": title, "opts": opts, "vendor": vendor(code), "rows": []}
        order.append(title)
    products[title]["rows"].append({"code": code, "desc": desc, "net": float(r["net"]), "vals": vals, "sec": r["sec"]})

out_products = []
for title in order:
    p = products[title]
    ptype, cat, kg, bx = kind(title)
    seen, variants, imgs, blurb = set(), [], [], ""
    for r in p["rows"]:
        key = tuple(r["vals"])
        if key in seen:
            raise ValueError(("duplicate option", title, key))
        seen.add(key)
        w = web_for(r["code"])
        if w:
            for i in w.get("images", [])[:3]:
                if i["src"] not in imgs:
                    imgs.append(i["src"])
            blurb = blurb or text(w.get("short_description") or w.get("description"))
        local = bool(LOCAL.search(r["desc"])) or length_mm(r["desc"]) >= 1800 and re.search(
            r"Screed|Straight Edge|Level", title)
        variants.append({"options": dict(zip(p["opts"], r["vals"])), "sku": r["code"], "cost": r["net"],
                         "price": retail(r["net"]), "weight": weight(title, r["desc"], kg, r["net"]),
                         "box": box(title, r["desc"], bx), "local": bool(local), "desc": r["desc"]})
    local_all = all(v["local"] for v in variants)
    local_any = any(v["local"] for v in variants)
    brand = p["vendor"]
    codes = ", ".join(v["sku"] for v in variants)
    body = "".join(f"<p>{html.escape(x.strip())}</p>" for x in re.split(r"\n+", blurb) if x.strip())
    deliver = ("Large or long item: delivered within Perth metro or collected from our showroom."
               if local_all else
               "Long lengths are Perth delivery or pick-up only; shorter sizes ship Australia-wide." if local_any else
               "Ships Australia-wide from Perth, or pick up from our showroom.")
    desc_html = (f"{body}<p>Buy the {html.escape(title)} online from Excellent Tiling Services in Perth: genuine "
                 f"{html.escape(brand)} stock for tilers, builders and DIY renovators.</p><p><strong>{'Code' if len(variants) == 1 else 'Codes'}:"
                 f"</strong> {html.escape(codes)}</p><p><strong>Delivery:</strong> "
                 f"{deliver}</p>")
    seo_desc = re.sub(r"\s+", " ", blurb or f"{title} for tilers and renovators.").strip()
    seo_desc = (seo_desc[:120].rsplit(" ", 1)[0] + ". Buy online from ETS Perth.") if len(seo_desc) > 120 else \
        seo_desc + " Buy online from ETS Perth."
    tags = [brand, "Tiling Tools", ptype, f"supplier-{'bat' if brand != 'Raimondi' else 'raimondi'}",
            "bat-tools-2026-05" if brand != "Raimondi" else "raimondi-2026-05"]
    if not imgs:
        tags.append("photo-needed")  # kept off Google Shopping until it has a photo
    tags += ["ship-local-only", "ship-long"] if local_all else ["ship-parcel", "ship-long"] if local_any else \
        ["ship-parcel"]
    out_products.append({
        "handle": slug(("" if title.lower().startswith(brand.lower()) else brand + " ") + title),
        "title": title, "vendor": brand, "productType": ptype, "category": f"gid://shopify/TaxonomyCategory/{cat}",
        "google": GOOGLE.get(cat, "1167"), "tags": tags, "options": p["opts"], "images": imgs[:8],
        "seo": {"title": (title if len(title) > 58 else title + " | ETS Perth")[:70], "description": seo_desc[:160]},
        "descriptionHtml": desc_html, "variants": variants})

json.dump(out_products, open("tools-raimondi.json", "w"), indent=1)


def vin(v, opts):
    d = {"optionValues": [{"optionName": o, "name": v["options"][o]} for o in opts],
         "price": f'{v["price"]:.2f}',  # taxable, DENY and requiresShipping are the defaults
         "inventoryItem": {"cost": f'{v["cost"]:.2f}', "tracked": False,
                           "measurement": {"weight": {"value": v["weight"], "unit": "KILOGRAMS"}}},
         "metafields": [
             {"namespace": "shipping", "key": "box_size", "type": "single_line_text_field", "value": v["box"]},
             {"namespace": "mm-google-shopping", "key": "mpn", "type": "single_line_text_field", "value": v["sku"]}]}
    return d


calls = []
if not ids_f:
    for i, p in enumerate(out_products):
        opts = p["options"]
        first = p["variants"][:20]
        values = {o: [] for o in opts}
        for v in p["variants"]:
            for o in opts:
                if v["options"][o] not in values[o]:
                    values[o].append(v["options"][o])
        vs = []
        for v in first:
            d = vin(v, opts)
            d["sku"] = v["sku"]
            vs.append(d)
        inp = {"handle": p["handle"], "title": p["title"], "vendor": p["vendor"], "productType": p["productType"],
               "status": "ACTIVE", "descriptionHtml": p["descriptionHtml"], "tags": p["tags"],
               "category": p["category"], "seo": p["seo"],
               "metafields": [{"namespace": "mm-google-shopping", "key": "google_product_category",
                               "type": "single_line_text_field", "value": p["google"]}],
               "productOptions": [{"name": o, "position": j + 1, "values": [{"name": x} for x in values[o]]}
                                  for j, o in enumerate(opts)],
               "files": [{"originalSource": u, "contentType": "IMAGE", "alt": p["title"]} for u in p["images"]],
               "variants": vs}
        calls.append(f'p{i}: productSet(synchronous:true,input:{gql(inp)})'
                     '{product{id handle variants(first:20){nodes{id sku}}}userErrors{field message}}')
    n = write_docs(out, "t", calls)
else:
    ids = json.load(open(ids_f))
    for i, p in enumerate(out_products):
        rest = p["variants"][20:]
        for k in range(0, len(rest), 20):
            vs = []
            for v in rest[k:k + 20]:
                d = vin(v, p["options"])
                d["inventoryItem"]["sku"] = v["sku"]
                vs.append(d)
            calls.append(f'v{i}_{k}: productVariantsBulkCreate(productId:"{ids[p["handle"]]}",strategy:DEFAULT,'
                         f'variants:{gql(vs)}){{productVariants{{id sku}}userErrors{{field message}}}}')
    n = write_docs(out, "tv", calls)
print(len(out_products), "products", sum(len(p["variants"]) for p in out_products), "variants", n, "docs")
