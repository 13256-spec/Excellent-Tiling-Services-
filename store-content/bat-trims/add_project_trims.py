"""BAT Project Trims (budget range, May 2026 Project Trims Book) -> two Shopify products.

  python3 add_project_trims.py OUTDIR            -> OUTDIR/projNN.graphql (productSet with the first 20 variants)
  python3 add_project_trims.py OUTDIR IDS.json   -> OUTDIR/projvNN.graphql (productVariantsBulkCreate for the rest;
                                                    IDS.json maps handle -> product gid)

Also writes project-trims.json.
"""
import json
import os
import re
import sys

import openpyxl

sys.path.insert(0, "pricing")
from price_rule import retail  # noqa: E402
from gqlgen import gql, product_set, variant, write_docs  # noqa: E402

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
P = {p["handle"]: p for p in json.load(open("bat-products.json"))}

COL = {"": "Mill Finish", "BAP": "Bronze Ash", "BKP": "Black", "BSP": "Bright Silver", "GMP": "Gunmetal",
       "LGMP": "Linished Gunmetal", "LIP": "Linished Iron", "LMP": "Linished Matt Gold", "LSNP": "Linished Satin Nickel",
       "LSP": "Linished Silver", "MBP": "Matt Black", "MGP": "Matt Gold", "MMP": "Monument Matt", "MSP": "Matt Silver",
       "MWP": "Matt White", "SMP": "Surfmist", "WHP": "Pearl White"}
PA_MM = {"8": "8mm", "9": "9mm", "10": "10mm", "11": "11mm", "12": "12.5mm"}
MCA_MM = {"8": "8.5mm", "10": "10.5mm", "12": "12.5mm"}


def ref(handle, size):
    v = next(x for x in P[handle]["variants"] if x["options"]["Size"] == size)
    return v["weight"], v["box"]


rows = openpyxl.load_workbook("pricing/Project_Trims_Book_1_-_May_2026.xlsx", read_only=True, data_only=True).active
pa, pmca = [], []
for code, desc, cost in rows.iter_rows(min_row=2, values_only=True):
    if not code or cost is None:
        continue
    m = re.fullmatch(r"(PA|PMCA)-(\d+)-3(?:-([A-Z]+))?", code.strip())
    if not m:
        raise ValueError(code)
    kind, s, suf = m.groups()
    cost = float(cost)
    if kind == "PA":
        size = PA_MM[s]
        w, box = ref("bat-aluminium-tiling-angle-3m", size)
        pa.append({"options": {"Size": size, "Colour": COL[suf or ""]}, "sku": code, "cost": cost,
                   "price": retail(cost), "weight": w, "box": box})
    else:
        size = MCA_MM[s]
        w, box = ref("bat-mosaic-corner-angle-3m", size)
        pmca.append({"options": {"Size": size, "Colour": COL[suf]}, "sku": code, "cost": cost,
                     "price": retail(cost), "weight": w, "box": box})

CARE = ("<p><strong>Care:</strong> wash finished trims with warm soapy water and a soft cloth. Don't use acid or alkaline "
        "cleaners, scourers or sandpaper on coloured, anodised or plated finishes. Remove greasy marks with white spirits, "
        "then rinse with clean water.</p><p>BAT Trims is an Australian family business, making tiling trims in Dandenong, "
        "Victoria since 1985. Order through Excellent Tiling Services in Maddington, Perth.</p>")
TAGS = ["BAT Trims", "BAT", "Hardware", "Tile Trims + Edging Profiles", "supplier-bat", "bat-project-trims",
        "bat-price-list-2026-05", "ship-local-only", "ship-long"]
FILES = {"aa": "gid://shopify/MediaImage/30347049599039", "aa-diagram": "gid://shopify/MediaImage/30347049664575",
         "pmca": "gid://shopify/MediaImage/30347648892991", "mca-drawing": "gid://shopify/MediaImage/30347050090559"}

products = [
    {"handle": "bat-project-aluminium-tiling-angle-3m",
     "title": "BAT Project Aluminium Tiling Angle – 3m Lengths (Budget Range)",
     "productType": "L Shaped Trim", "tags": TAGS, "files": ["aa", "aa-diagram"],
     "seo": {"title": "BAT Project Aluminium Tile Angle 3m | Budget Trim | ETS Perth",
             "description": "BAT Project aluminium tile edge angle from $7.30. 8mm to 12.5mm, 3m lengths, 16 colours incl. matt gold, gunmetal and matt black. Perth."},
     "descriptionHtml": "<p>BAT's Project range is a lighter-gauge aluminium L angle made for volume jobs: apartments, builds and rentals where you need a lot of metres of trim at a sharp price. Same perforated fixing leg and colour range as the standard angle, in the most popular tile thicknesses.</p><ul>\n<li>Material: aluminium (project gauge), perforated fixing leg</li>\n<li>Length: 3m</li>\n<li>Sizes (tile thickness): 8, 9, 10, 11 and 12.5mm</li>\n<li>Finishes: Mill Finish, Bright Silver, Matt Silver, Linished Silver, Black, Matt Black, Matt White, Pearl White, Surfmist, Bronze Ash, Matt Gold, Linished Matt Gold, Gunmetal, Linished Gunmetal, Linished Iron, Linished Satin Nickel, Monument Matt</li>\n<li>Coloured finishes come with protective film</li>\n<li>Need a heavier gauge or other sizes? See the standard BAT Aluminium Tiling Angle</li>\n</ul>" + CARE,
     "options": ["Size", "Colour"], "variants": pa},
    {"handle": "bat-project-mosaic-corner-angle-3m",
     "title": "BAT Project Mosaic Corner Angle – 3m Lengths (Budget Range)",
     "productType": "Square edge", "tags": TAGS, "files": ["pmca", "mca-drawing"],
     "seo": {"title": "BAT Project Mosaic Corner Angle 3m | Budget Square Edge | ETS",
             "description": "BAT Project mosaic corner angle, square-edge tile trim from $17.45. 8.5, 10.5 and 12.5mm, 3m lengths, 5 colours. Order in Perth."},
     "descriptionHtml": "<p>A budget version of BAT's mosaic corner angle: a square-edge aluminium trim that gives external corners and tile edges a crisp, modern finish. Made for volume jobs where the look matters but the budget is tight.</p><ul>\n<li>Material: aluminium (project gauge), perforated fixing leg</li>\n<li>Length: 3m</li>\n<li>Sizes (tile thickness): 8.5, 10.5 and 12.5mm</li>\n<li>Finishes: Bright Silver, Matt Silver, Matt Black, Matt White, Bronze Ash (with protective film)</li>\n</ul>" + CARE,
     "options": ["Size", "Colour"], "variants": pmca},
]
json.dump(products, open("project-trims.json", "w"), indent=1, ensure_ascii=False)
FIRST = 20
if len(sys.argv) < 3:
    calls = [f'p{i}: productSet(synchronous:true,input:{gql(product_set(dict(p, variants=p["variants"][:FIRST]), FILES))})'
             "{product{id handle} userErrors{field message}}" for i, p in enumerate(products)]
    print(len(pa), "PA,", len(pmca), "PMCA;", write_docs(out, "proj", calls), "productSet documents")
else:
    ids = json.load(open(sys.argv[2]))
    calls, k = [], 0
    for p in products:
        rest = p["variants"][FIRST:]
        for j in range(0, len(rest), 20):
            chunk = [variant(v, p["options"]) for v in rest[j:j + 20]]
            calls.append(f'v{k}: productVariantsBulkCreate(productId:"{ids[p["handle"]]}",strategy:DEFAULT,variants:{gql(chunk)})'
                         "{productVariants{id sku} userErrors{field message}}")
            k += 1
    print(write_docs(out, "projv", calls), "variant documents,", k, "calls")
