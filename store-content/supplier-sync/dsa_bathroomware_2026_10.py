"""DSA bathroomware from Eternity Tiles (vendor "DSA" on eternitytiles.com.au) -> Shopify productSet inputs.

Everything DSA sells that is not a tile (tiles are already in the store): Celine and Chloe tapware and
showers, Malaga vanities and cabinets, basins, kitchen troughs, LED mirrors, wastes and the smart toilet.

No supplier cost sheet exists for these yet, so:
- price = Eternity's listed retail price (what Eternity's own shop charges), no cost recorded
- status DRAFT, tags `supplier-import` + `needs-cost`, until the owner gets DSA trade costs and prices them
  with the playbook rules (store-content/pricing/PRICING-PLAYBOOK.md).
Supplier name stays out of customer-facing text (owner rule): vendor "Excellent Tiling Services",
supplier only in the custom.supplier metafield.

Usage: dsa_bathroomware_2026_10.py et_all.json out.json
  et_all.json: Eternity's public /collections/all/products.json pages, concatenated into one list.
"""
import json, re, sys

CAT = {  # Shopify taxonomy ids already used by the matching MELA / BAT products
    "basin": "gid://shopify/TaxonomyCategory/ha-10-3-5-1", "sink": "gid://shopify/TaxonomyCategory/ha-10-3-5",
    "mirror": "gid://shopify/TaxonomyCategory/hg-3-47-2", "vanity": "gid://shopify/TaxonomyCategory/fr-4-14-1",
    "toilet": "gid://shopify/TaxonomyCategory/ha-10-3-6-2", "drain": "gid://shopify/TaxonomyCategory/ha-10-2-3-1",
    "towel": "gid://shopify/TaxonomyCategory/hg-1-21-3", "mixer": "gid://shopify/TaxonomyCategory/ha-10-3-3-1",
}
FINISH = {"Melamine Antico Oak #43173": "Antico Oak melamine", "Melamine W681-2": "Dark Oak melamine",
          "Ru Bai (Matt White Paint Finish)": "Matt White painted finish"}
PERTH = "ship-local-only"  # delivery profile "Perth only (local delivery / pickup)"; everything else General profile

# handle: (title, product type, [extra tags], [manual collection handles], category key, ship tag)
P = {
    "bath-pup-up-waste": ("Celine Bath Pop Up Waste", "Pop Up Waste", ["Celine", "Bath Waste"], ["bathroom-wastes", "accessories"], None, "ship-parcel"),
    "bottle-trap-32mm-chrome": ("Celine Bottle Trap 32mm", "Bottle Trap", ["Celine"], ["bathroom-wastes", "accessories"], None, "ship-parcel"),
    "caden-trough-001": ("Caden Single Bowl Sink 610mm", "Kitchen Sink", ["Caden", "Single Bowl", "Stainless Steel"], ["sinks", "kitchen-laundry"], "sink", "ship-bulky"),
    "caden-trough-001-copy": ("Caden Single Bowl Sink with Drainer 660mm", "Kitchen Sink", ["Caden", "Single Bowl", "Drainer", "Stainless Steel"], ["sinks", "kitchen-laundry"], "sink", "ship-bulky"),
    "caden-trough-003": ("Caden Double Bowl Sink with Drainer 1200mm", "Kitchen Sink", ["Caden", "Double Bowl", "Drainer", "Stainless Steel"], ["sinks", "kitchen-laundry"], "sink", "ship-bulky"),
    "callan-trough-001": ("Callan Single Bowl Sink 450mm", "Kitchen Sink", ["Callan", "Single Bowl", "Laundry Sink", "Stainless Steel"], ["sinks", "kitchen-laundry"], "sink", "ship-bulky"),
    "callan-trough-002": ("Callan Single Bowl Sink 580mm", "Kitchen Sink", ["Callan", "Single Bowl", "Laundry Sink", "Stainless Steel"], ["sinks", "kitchen-laundry"], "sink", "ship-bulky"),
    "callan-trough-001-copy": ("Callan Double Bowl Sink 700mm", "Kitchen Sink", ["Callan", "Double Bowl", "Stainless Steel"], ["sinks", "kitchen-laundry"], "sink", "ship-bulky"),
    "capsule-led-oval-back-lit": ("Capsule LED Oval Backlit Mirror 450 x 900mm", "LED Mirror", ["Capsule", "Backlit Mirror", "Oval LED Mirror", "Anti Fog"], ["mirrors", "led-mirrors"], "mirror", "ship-bulky"),
    "celine-2-in-1-shower-type-1": ("Celine Twin Rail Shower", "Combination Shower Set", ["Celine", "Twin Shower", "Rail Shower"], ["tapware", "shower-tapware"], None, "ship-parcel"),
    "celine-basin-mixer": ("Celine Basin Mixer", "Basin Mixer", ["Celine", "Basin Mixer", "Tapware"], ["tapware", "basin-mixers"], "mixer", "ship-parcel"),
    "celine-basin-bath-wall-mixer": ("Celine Wall Basin / Bath Mixer with Spout", "Wall Mixer", ["Celine", "Wall Basin Mixer", "Tapware"], ["tapware", "wall-mixers", "bath-tapware"], "mixer", "ship-parcel"),
    "celine-double-towel-rail-600": ("Celine 600 Double Towel Rail", "Towel Rail", ["Celine", "Double Towel Rail", "600mm", "Accessories"], ["towel-rails", "accessories"], "towel", "ship-parcel"),
    "celine-double-towel-rail-800": ("Celine 800 Double Towel Rail", "Towel Rail", ["Celine", "Double Towel Rail", "800mm", "Accessories"], ["towel-rails", "accessories"], "towel", "ship-parcel"),
    "celine-gooseneck-pull-out-kitchen-mixer": ("Celine Gooseneck Pull Out Kitchen Mixer", "Kitchen Sink Mixer", ["Celine", "Kitchen Mixer", "Pull Out", "Tapware"], ["tapware", "kitchen-tapware", "kitchen-laundry"], None, "ship-parcel"),
    "celine-gooseneck-sink-mixer": ("Celine Gooseneck Sink Mixer", "Kitchen Sink Mixer", ["Celine", "Kitchen Mixer", "Tapware"], ["tapware", "kitchen-tapware", "kitchen-laundry"], None, "ship-parcel"),
    "celine-hand-shower-type-1": ("Celine Hand Shower on Bracket", "Hand Shower Set", ["Celine", "Hand Shower"], ["tapware", "shower-tapware"], None, "ship-parcel"),
    "celine-hand-towel-rail": ("Celine Hand Towel Rail", "Hand Towel Rail", ["Celine", "Hand Towel Rail", "Accessories"], ["towel-rails", "accessories"], "towel", "ship-parcel"),
    "celine-rail-shower": ("Celine Rail Shower", "Hand Shower Set", ["Celine", "Rail Shower", "Hand Shower"], ["tapware", "shower-tapware"], None, "ship-parcel"),
    "celine-robe-hook": ("Celine Robe Hook", "Bathroom Hook", ["Celine", "Robe Hook", "Accessories"], ["bathroom-hooks", "accessories"], None, "ship-parcel"),
    "chloe-round-hand-piece-chrome": ("Celine Round Hand Shower Piece", "Hand Shower", ["Celine", "Hand Shower"], ["tapware", "shower-tapware"], None, "ship-parcel"),
    "celine-shower-mixer": ("Celine Shower Mixer", "Wall Mixer", ["Celine", "Shower Mixer", "Wall Mixer", "Tapware"], ["tapware", "wall-mixers"], None, "ship-parcel"),
    "celine-shower-mixer-with-divertor": ("Celine Shower Mixer with Diverter", "Wall Mixer with Diverter", ["Celine", "Shower Mixer", "Diverter", "Tapware"], ["tapware", "wall-mixers"], None, "ship-parcel"),
    "celine-shower-rose-type-2": ("Celine Square Shower Rose 250mm", "Shower Head", ["Celine", "Shower Head", "Square"], ["tapware", "shower-tapware"], None, "ship-parcel"),
    "celine-single-towel-tail-600": ("Celine 600 Single Towel Rail", "Towel Rail", ["Celine", "Single Towel Rail", "600mm", "Accessories"], ["towel-rails", "accessories"], "towel", "ship-parcel"),
    "celine-single-towel-tail-800": ("Celine 800 Single Towel Rail", "Towel Rail", ["Celine", "Single Towel Rail", "800mm", "Accessories"], ["towel-rails", "accessories"], "towel", "ship-parcel"),
    "celine-sink-mixer": ("Celine Sink Mixer", "Kitchen Sink Mixer", ["Celine", "Kitchen Mixer", "Laundry Mixer", "Tapware"], ["tapware", "kitchen-tapware", "kitchen-laundry"], None, "ship-parcel"),
    "celine-square-hand-piece-chrome": ("Celine Square Hand Shower Piece", "Hand Shower", ["Celine", "Hand Shower"], ["tapware", "shower-tapware"], None, "ship-parcel"),
    "celine-swivel-bath-spout": ("Celine Swivel Bath Spout", "Bath Spout", ["Celine", "Bath Spout", "Tapware"], ["tapware", "bath-tapware", "spouts-outlets"], None, "ship-parcel"),
    "celine-tall-basin-mixer": ("Celine Tall Basin Mixer", "Basin Mixer", ["Celine", "Tall Basin Mixer", "Tapware"], ["tapware", "basin-mixers"], "mixer", "ship-parcel"),
    "celine-toilet-roll-holder": ("Celine Toilet Roll Holder", "Toilet Roll Holder", ["Celine", "Toilet Roll Holder", "Accessories"], ["toilet-roll-holders", "accessories"], None, "ship-parcel"),
    "celine-wall-mount-shower-arm-type-2": ("Celine Wall Mounted Shower Arm", "Shower Arm", ["Celine", "Shower Arm"], ["tapware", "shower-tapware"], None, "ship-parcel"),
    "chloe-hand-shower-type-2": ("Chloe Hand Shower on Bracket", "Hand Shower Set", ["Chloe", "Hand Shower"], ["tapware", "shower-tapware"], None, "ship-parcel"),
    "chloe-shower-rose-type-1": ("Chloe Round Shower Rose 250mm", "Shower Head", ["Chloe", "Shower Head", "Round"], ["tapware", "shower-tapware"], None, "ship-parcel"),
    "chole-compact-round-shower-chrome": ("Chloe Compact Twin Shower", "Combination Shower Set", ["Chloe", "Twin Shower"], ["tapware", "shower-tapware"], None, "ship-parcel"),
    "chole-2-in-1-shower-type-2": ("Chloe Twin Rail Shower", "Combination Shower Set", ["Chloe", "Twin Shower", "Rail Shower"], ["tapware", "shower-tapware"], None, "ship-parcel"),
    "olivia-semi-inset-basin-copy": ("Cosimo Semi Inset Basin", "Semi Basin", ["Cosimo", "Semi Inset Basin", "Basin", "Ceramic", "White"], ["basins", "semi-recessed-basins"], "basin", "ship-bulky"),
    "cosimo-top-mount-basin": ("Cosimo Above Counter Basin", "Above Counter Basin", ["Cosimo", "Above Counter Basin", "Basin", "Ceramic", "White"], ["basins", "above-counter-basins"], "basin", "ship-bulky"),
    "cosimo-undermount-basin": ("Cosimo Undermount Basin", "Undermount Basin", ["Cosimo", "Undermount Basin", "Basin", "Ceramic", "White"], ["basins", "undermount-basins"], "basin", "ship-bulky"),
    "crystal-smart-toilet": ("Crystal Smart Toilet with Bidet Seat", "Toilet Suite", ["Crystal", "Smart Toilet", "Toilet", "Back to Wall", "WELS 3 Star"], ["toilets", "back-to-wall-toilets"], "toilet", PERTH),
    "cube-basin": ("Cube Wall Hung Basin", "Wall Hung Basin", ["Cube", "Wall Hung Basin", "Basin", "Ceramic", "White"], ["basins"], "basin", "ship-bulky"),
    "eclipse-led-round-backlit-mirror": ("Eclipse LED Round Backlit Mirror", "LED Mirror", ["Eclipse", "Backlit Mirror", "Round LED Mirror", "Anti Fog"], ["mirrors", "led-mirrors"], "mirror", "ship-bulky"),
    "malaga-antico-oak-cubby-cabinet-accesory-for-eternity-range-vanity": ("Malaga Antico Oak Cubby Cabinet 300mm", "Bathroom Tallboy", ["Malaga", "Antico Oak", "Vanity Cabinet"], ["bathroom-vanities", "bathroom-storage-tallboys"], "vanity", PERTH),
    "malaga-antico-oak-eternity-range-vanity": ("Malaga Antico Oak Wall Hung Vanity", "Wall Hung Vanity", ["Malaga", "Antico Oak", "Bathroom Vanity", "Wall Hung Vanity"], ["bathroom-vanities", "wall-hung-vanities", "single-vanities"], "vanity", PERTH),
    "malaga-antico-oak-kickboard-cabinet-accesory-for-eternity-range-vanity": ("Malaga Antico Oak Vanity Kickboard", "Vanity Kickboard", ["Malaga", "Antico Oak", "Vanity Cabinet"], ["bathroom-vanities"], "vanity", PERTH),
    "malaga-dark-oak-cubby-cabinet-accesory-for-eternity-range-vanity": ("Malaga Dark Oak Cubby Cabinet 300mm", "Bathroom Tallboy", ["Malaga", "Dark Oak", "Vanity Cabinet"], ["bathroom-vanities", "bathroom-storage-tallboys"], "vanity", PERTH),
    "malaga-dark-oak-eternity-range-vanity": ("Malaga Dark Oak Wall Hung Vanity", "Wall Hung Vanity", ["Malaga", "Dark Oak", "Bathroom Vanity", "Wall Hung Vanity"], ["bathroom-vanities", "wall-hung-vanities", "single-vanities"], "vanity", PERTH),
    "malaga-dark-oak-kickboard-cabinet-accesory-for-eternity-range-vanity": ("Malaga Dark Oak Vanity Kickboard", "Vanity Kickboard", ["Malaga", "Dark Oak", "Vanity Cabinet"], ["bathroom-vanities"], "vanity", PERTH),
    "malaga-element-white-kickboard-cabinet-accesory-for-eternity-range-vanity": ("Malaga Matt White Vanity Kickboard", "Vanity Kickboard", ["Malaga", "Matt White", "Vanity Cabinet"], ["bathroom-vanities"], "vanity", PERTH),
    "malaga-elemental-cubby-cabinet-accesory-for-eternity-range-vanity": ("Malaga Matt White Cubby Cabinet 300mm", "Bathroom Tallboy", ["Malaga", "Matt White", "Vanity Cabinet"], ["bathroom-vanities", "bathroom-storage-tallboys"], "vanity", PERTH),
    "malaga-elemental-eternity-range-vanity": ("Malaga Matt White Wall Hung Vanity", "Wall Hung Vanity", ["Malaga", "Matt White", "Bathroom Vanity", "Wall Hung Vanity"], ["bathroom-vanities", "wall-hung-vanities", "single-vanities"], "vanity", PERTH),
    "malaga-elemental-single-door-cabinet-cabinet-accesory-for-eternity-range-vanity": ("Malaga Matt White Single Door Cabinet 295mm", "Bathroom Tallboy", ["Malaga", "Matt White", "Vanity Cabinet"], ["bathroom-vanities", "bathroom-storage-tallboys"], "vanity", PERTH),
    "mezo-basin": ("Mezo Above Counter Basin", "Above Counter Basin", ["Mezo", "Above Counter Basin", "Basin", "Ceramic", "White"], ["basins", "above-counter-basins"], "basin", "ship-bulky"),
    "olivia-semi-above-counter-basin": ("Olivia Above Counter Basin", "Above Counter Basin", ["Olivia", "Above Counter Basin", "Basin", "Ceramic", "White"], ["basins", "above-counter-basins"], "basin", "ship-bulky"),
    "olivia-semi-inset-basin": ("Olivia Semi Inset Basin", "Semi Basin", ["Olivia", "Semi Inset Basin", "Basin", "Ceramic", "White"], ["basins", "semi-recessed-basins"], "basin", "ship-bulky"),
    "ria-semi-inset-basin": ("Ria Semi Inset Basin", "Semi Basin", ["Ria", "Semi Inset Basin", "Basin", "Ceramic", "White"], ["basins", "semi-recessed-basins"], "basin", "ship-bulky"),
    "ria-top-mount-basin": ("Ria Above Counter Basin", "Above Counter Basin", ["Ria", "Above Counter Basin", "Basin", "Ceramic", "White"], ["basins", "above-counter-basins"], "basin", "ship-bulky"),
    "tiles-insert-floor-waste-50mm-top-100x100mm": ("Tile Insert Floor Waste 50mm, 100 x 100mm", "Floor Drains", ["Floor Waste", "Tile Insert", "Floor Drains"], ["bathroom-wastes"], "drain", "ship-parcel"),
    "tiles-insert-floor-waste-80mm-top-100x100mm": ("Tile Insert Floor Waste 80mm, 100 x 100mm", "Floor Drains", ["Floor Waste", "Tile Insert", "Floor Drains"], ["bathroom-wastes"], "drain", "ship-parcel"),
    "twist-top-floor-drain-100mm-chrome": ("Twist Top Floor Drain 100mm", "Floor Drains", ["Floor Waste", "Floor Drains"], ["bathroom-wastes"], "drain", "ship-parcel"),
    "twist-top-floor-drain-80mm-chrome": ("Twist Top Floor Drain 80mm", "Floor Drains", ["Floor Waste", "Floor Drains"], ["bathroom-wastes"], "drain", "ship-parcel"),
    "universal-pop-up-waste-type-2": ("Celine Universal Pop Up Waste 32/40mm", "Pop Up Waste", ["Celine", "Pop Up Waste", "Basin Waste"], ["bathroom-wastes", "accessories"], None, "ship-parcel"),
}
SKIP = {"sealing-tape-installation-accessory", "under-mount-clip-trough-installation-accessory"}  # $0, no photo

DESC = {  # fallback when Eternity's page has no text: by product type, then by source-handle word
    "Pop Up Waste": "Pop up waste with a push-button plug; match the finish to your tapware.",
    "Bottle Trap": "32mm bottle trap for exposed basin plumbing; match the finish to your tapware.",
    "Combination Shower Set": "Twin shower: an overhead rose plus a hand shower on a slide rail, run off one set of plumbing.",
    "Basin Mixer": "Single-lever basin mixer from the Celine range, a modern mix of curves and angles.",
    "Towel Rail": "Wall-mounted towel rail from the Celine accessories range.",
    "Bathroom Hook": "Wall-mounted robe hook from the Celine accessories range.",
    "Hand Shower": "Replacement hand shower piece; fits standard shower hoses.",
    "Wall Mixer": "Single-lever shower and wall mixer from the Celine range.",
    "Wall Mixer with Diverter": "Single-lever wall mixer with a built-in diverter to switch between two outlets.",
    "Bath Spout": "Swivel bath spout from the Celine range.",
    "Toilet Roll Holder": "Wall-mounted toilet roll holder from the Celine accessories range.",
    "Shower Arm": "Wall-mounted shower arm from the Celine range, for use with a shower rose.",
    "Vanity Kickboard": "Kickboard that sits under a Malaga wall hung vanity to make it floor-standing.",
    "cubby": "Open cubby side cabinet that matches the Malaga vanity range.",
    "single-door": "Single door side cabinet that matches the Malaga vanity range.",
    "tiles-insert": "Tile insert floor waste with a square 100 x 100mm top, so the floor tile runs through the grate.",
    "twist-top": "Twist-top floor drain with a removable grate.",
}

MALAGA_EXTRA = {  # title -> extra description lines
    "Wall Hung Vanity": ["Sizes: 600, 750, 900 and 1200mm wide, 630mm high, 455mm deep", "Finger-pull doors and drawers, no handles",
                         "Supplied as cabinet; add a basin or top to suit"],
    "Vanity Kickboard": ["Sizes: 750, 900 and 1200mm wide, 425mm high, 200mm deep", "Turns a Malaga wall hung vanity into a floor-standing one"],
    "Bathroom Tallboy": ["630mm high, 455mm deep", "Matches the Malaga vanity range"],
}


def clean_html(html):
    html = re.sub(r"<img[^>]*>", "", html or "")
    html = re.sub(r"<p>\s*(<br>)?\s*</p>", "", html)
    html = re.sub(r"\bEternity\b ?(Range)?", "", html).replace(" our ", " the ").replace("--", "-")
    html = html.replace("<p><br>", "<p>").replace("suites either", "suits either")
    html = re.sub(r"\s+", " ", html).strip()
    return html


def size_mm(label):
    m = re.match(r"\s*(\d+)\(", label)  # "590(w) x630(H) x 455mm(D)" -> 600 class
    return {"590": "600mm", "740": "750mm", "890": "900mm", "1190": "1200mm"}.get(m.group(1), label) if m else label


def variants_of(p):
    """-> (option names, [(option values, sku, price)], finishes) with Eternity's junk options removed."""
    names = [o["name"] for o in p["options"]]
    rows = []
    for v in p["variants"]:
        vals = [x for x in [v["option1"], v["option2"], v["option3"]] if x is not None]
        rows.append((dict(zip(names, vals)), (v["sku"] or "").replace(" -", "-").strip() or None, v["price"]))
    real = {n: list(dict.fromkeys(r[0][n] for r in rows if r[0][n] not in ("Default Title", "See Diagram"))) for n in names}
    finishes = [FINISH.get(f, f.title()) for f in real.get("Colour", [])]
    keep = [n for n in names if len(real[n]) > 1]
    if not keep:
        return ["Title"], [({"Title": "Default Title"}, s, pr) for _, s, pr in rows], finishes
    out = []
    for vals, s, pr in rows:
        ov = {}
        for n in keep:
            val = vals[n]
            if n in ("Colour", "Taphole"):
                val = val.title()
            elif n == "Size" and "(" in val:
                val = size_mm(val)
            ov[{"Colour": "Finish"}.get(n, n)] = val
        out.append((ov, s, pr))
    return [{"Colour": "Finish"}.get(n, n) for n in keep], out, finishes


def build(et_all):
    out = []
    for p in et_all:
        if p["vendor"] != "DSA" or p["handle"] in SKIP or p["handle"] not in P:
            continue
        title, ptype, extra, colls, cat, ship = P[p["handle"]]
        names, rows, finishes = variants_of(p)
        if names == ["Size"]:
            rows.sort(key=lambda r: int(re.sub(r"\D", "", r[0]["Size"]) or 0))
        values = {n: list(dict.fromkeys(r[0][n] for r in rows)) for n in names}
        desc = clean_html(p["body_html"])
        lines = list(MALAGA_EXTRA.get(ptype, [])) if title.startswith("Malaga") else []
        if finishes:
            lines.append("Finish: " + " or ".join(finishes))
        if not desc:
            key = next((k for k in DESC if k in p["handle"]), ptype)
            desc = f"<p>{DESC[key]}</p>"
        if lines:
            desc += "<ul>" + "".join(f"<li>{l}</li>" for l in lines) + "</ul>"
        tags = sorted(set(extra + [f for f in finishes if f in ("Chrome", "Brushed Nickel")] + [ship, "supplier-import", "needs-cost"]))
        prod = {
            "title": title, "descriptionHtml": desc, "vendor": "Excellent Tiling Services", "productType": ptype,
            "status": "DRAFT", "tags": tags,
            "metafields": [{"namespace": "custom", "key": "supplier", "type": "single_line_text_field", "value": "Eternity Tiles"}],
            "productOptions": [{"name": n, "values": [{"name": v} for v in values[n]]} for n in names],
            "files": [{"originalSource": img["src"].split("?")[0], "alt": title, "contentType": "IMAGE"} for img in p["images"]],
            "variants": [{"optionValues": [{"optionName": n, "name": ov[n]} for n in names], "price": pr,
                          "inventoryPolicy": "CONTINUE", "taxable": True,
                          "inventoryItem": {**({"sku": s} if s else {}), "tracked": False}}
                         for ov, s, pr in rows],
            "_collections": colls, "_source": p["handle"],  # stripped before sending
        }
        if cat:
            prod["category"] = CAT[cat]
        out.append(prod)
    missing = set(P) - {r["_source"] for r in out}
    assert not missing, missing
    return out


if __name__ == "__main__":
    rows = build(json.load(open(sys.argv[1])))
    json.dump(rows, open(sys.argv[2], "w"), indent=1)
    for r in rows:
        print(f'{r["title"]:48} {r["productType"]:24} {len(r["variants"])} var  {", ".join(v["price"] for v in r["variants"])}')
    print(len(rows), "products", sum(len(r["variants"]) for r in rows), "variants")
