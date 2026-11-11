"""Build the HTML for the Shopify page "ARDEX catalogues, data sheets & grout colours" from the created products.
Usage: python3 catalogue_page.py > ardex-catalogue-page.html
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
cat = {p["slug"]: p for p in json.load(open(os.path.join(HERE, "ardex-catalogue-2026-11-11.json")))}
created = json.load(open(os.path.join(HERE, "ardex-created-2026-11-11.json")))
gc = json.load(open(os.path.join(HERE, "grout-colours.json")))

GROUPS = [
    ("adhesives", "Tile adhesives", "/collections/ardex-tile-adhesives"),
    ("grouts", "Grouts", "/collections/ardex-grouts"),
    ("waterproofing", "Waterproofing membranes and accessories", "/collections/ardex-waterproofing"),
    ("levelling", "Floor levelling, screeds and smoothing compounds", "/collections/ardex-floor-levelling"),
    ("primers", "Primers, bonding agents and additives", "/collections/ardex-primers-additives"),
    ("sealants", "Silicones and sealants", "/collections/ardex-silicones-sealants"),
    ("concrete-repair", "Concrete repair, construction grouts and crack injection", "/collections/ardex-concrete-repair"),
    ("civil", "Civil engineering", "/collections/ardex-civil-engineering"),
    ("render", "Render", "/collections/ardex-render"),
    ("flooring-adhesives", "Flooring adhesives", "/collections/ardex-flooring-adhesives"),
    ("tools", "ARDEX GT tools", "/collections/ardex-tools"),
    ("wedi", "wedi shower and wet room systems", "/collections/wedi"),
]
LABEL = {"Technical Datasheet": "TDS", "Safety Datasheet": "SDS", "Spec Sheet": "Spec sheet", "VOC": "VOC", "VOC Content Certificate": "VOC"}


def esc(s):
    return html.escape(s, quote=True)


out = []
out.append("<p>Every ARDEX Australia product we list carries ARDEX's own technical data sheet (TDS) and safety data sheet (SDS). "
           "This page collects them in one place, with the grout colour charts and ARDEX's catalogues and selectors. "
           "Prices and stock for the ARDEX range are being loaded: call 0450 960 543 or <a href=\"/pages/request-a-quote\">send an enquiry</a> for a price.</p>")
out.append("<h2>ARDEX catalogues and selectors</h2><ul>"
           "<li><a href=\"https://ardexaustralia.com/literature-library/\" target=\"_blank\" rel=\"noopener\">ARDEX literature library</a>: brochures, system guides and specification sheets</li>"
           "<li><a href=\"https://ardexaustralia.com/calculators-and-downloads/\" target=\"_blank\" rel=\"noopener\">ARDEX calculators and downloads</a>: coverage calculators and every spec sheet</li>"
           "<li><a href=\"https://ardexaustralia.com/tools/grout-colour-selector/\" target=\"_blank\" rel=\"noopener\">ARDEX grout colour selector</a>: see each grout colour against a tile colour</li>"
           "<li><a href=\"https://ardexaustralia.com/tools/technical-bulletins/\" target=\"_blank\" rel=\"noopener\">ARDEX technical bulletins</a>: tiling, flooring and waterproofing systems</li>"
           "<li><a href=\"https://ardexaustralia.com/ardex-australia-warranty/\" target=\"_blank\" rel=\"noopener\">ARDEX Australia system warranty</a></li></ul>")

out.append("<h2>Grout colour charts</h2><p>On-screen colours are a guide only. Check the ARDEX colour chart in our Maddington showroom before you order.</p>")
charts = [("fg-8", "ARDEX FG 8 (flexible coloured grout, 1 to 8mm joints)", "ardex-fg-8"),
          ("fs-dd", "ARDEX FS-DD (non-sanded grout)", "ardex-fs-dd"),
          ("wj-50", "ARDEX WJ 50 (wide joint grout, 2 to 50mm)", "ardex-wj-50"),
          ("eg-15", "ARDEX EG 15 (epoxy grout)", "ardex-eg-15")]
handles = {x["slug"]: x["handle"] for x in created}
for key, label, slug in charts:
    link = f"/products/{handles[slug]}" if slug in handles else "#"
    cells = "".join(
        f'<span style="display:inline-block;width:120px;margin:0 8px 10px 0;text-align:center;font-size:13px">'
        f'<span style="display:block;height:48px;border:1px solid #ccc;border-radius:6px;background:#{hx}"></span>{esc(name)}</span>'
        for name, hx in gc[key])
    out.append(f"<h3><a href=\"{link}\">{esc(label)}</a></h3><p>{cells}</p>")

out.append("<h2>Data sheets by product</h2>")
for g, label, url in GROUPS:
    rows = []
    for x in sorted((c for c in created if c["group"] == g), key=lambda c: c["title"].lower()):
        p = cat[x["slug"]]
        links = []
        for name, u in p["downloads"]:
            if u.lower().endswith(".pdf"):
                links.append(f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(LABEL.get(name, name))}</a>')
        rows.append(f'<li><a href="/products/{x["handle"]}">{esc(x["title"])}</a>' + (": " + " · ".join(links) if links else "") + "</li>")
    out.append(f"<h3><a href=\"{url}\">{esc(label)}</a></h3><ul>" + "".join(rows) + "</ul>")

out.append("<p>Data sheets open on ardexaustralia.com and are the current versions published by ARDEX Australia. Always install to the data sheet; ARDEX technical services: 1800 224 070.</p>")
print("".join(out))
