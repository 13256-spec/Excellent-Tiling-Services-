"""Search-term pass for tiling hardware (Nov 2026): put the words people type into Google on the product pages.

Product names follow the supplier ("Square Grate Shower Floor Waste"), shoppers type other words ("floor drain grate",
"shower drain"). Terms come from keyword-suggestions-2026-11.json (Google autocomplete, Australia). Per product:
  seo_title  the product name plus the main search phrase its name lacks (max 65 chars), else unchanged
  aka        a visible last line on the description: <p class="ets-aka">Also known as: ...</p> (Google ranks on page
             text, not hidden tags); rerunning replaces the line
The meta description is re-sent unchanged (Shopify clears it if the SEO title is sent alone).

Usage: hardware_search_terms.py products.json out.json
  products.json: Admin products (id title vendor productType status seo{title description} descriptionHtml), non-MELA
"""
import json, re, sys
MAX = 65
# (product type, regex on title or None) -> (phrase for the title or None, also-known-as terms). First match wins.
RULES = [
 ("Floor Drains", r"linear", ("Linear Shower Drain", ["linear shower drain", "strip drain", "shower channel drain", "linear floor waste", "long shower grate"])),
 ("Floor Drains", r"flange", ("Puddle Flange", ["puddle flange", "floor waste flange", "leak control flange", "shower puddle flange"])),
 ("Floor Drains", r"tile insert", ("Tile Insert Shower Grate", ["tile insert floor waste", "tile insert drain", "tile insert shower grate", "tile insert shower drain", "smart tile floor waste"])),
 ("Floor Drains", r"collar$|pvc collar", (None, ["floor waste collar", "floor drain riser", "shower drain extension"])),
 ("Floor Drains", r"waste", ("Floor Drain Grate", ["floor drain", "floor drain grate", "shower drain", "shower grate", "bathroom floor waste grate"])),
 ("Floor Drains", None, ("Floor Waste Grate", ["floor waste", "floor waste grate", "shower drain grate", "shower waste", "bathroom floor drain"])),
 ("Shower Systems", r"drain", (None, ["shower drain", "shower drain cover", "shower waste"])),
 (None, r"waterstop|waterproofing angle|water stop", ("Shower Waterstop Angle", ["waterstop angle", "shower water stop", "shower water stop angle", "shower hob angle"])),
 ("L Shaped Trim", None, ("Tile Edge Trim", ["tile trim", "tile edge trim", "tile edging strip", "aluminium tile angle", "L angle tile trim"])),
 ("Notched Trim", None, ("Curved Tile Edge Trim", ["bendable tile trim", "curved tile trim", "flexible tile angle", "tile edge trim for curves"])),
 ("Square edge", None, ("Square Edge Tile Trim", ["square edge tile trim", "box edge tile trim", "tile edging", "tile edge trim"])),
 ("Round edge", None, ("Round Edge Tile Trim", ["round edge tile trim", "bullnose tile trim", "quadrant tile edging", "tile edge trim"])),
 ("Cove Trim", None, ("Cove Tile Trim", ["cove trim", "cove tile trim", "coved skirting trim", "hygienic floor to wall trim"])),
 ("Retro Cove Trim", None, ("Cove Tile Trim", ["retro fit cove trim", "cove trim for tiles already installed", "coved skirting trim"])),
 ("Retro Fit Angle", None, ("Retro Fit Tile Trim", ["retro fit tile trim", "tile trim for tiles already installed", "tile edging after install"])),
 ("Expansion Trim", None, ("Tile Expansion Joint", ["tile expansion joint", "tile expansion joint trim", "movement joint", "control joint profile"])),
 ("Balcony trim", None, ("Balcony Edge Trim", ["balcony edge trim", "balcony tile edge trim", "balcony drip edge trim"])),
 ("Stair Trim", None, ("Stair Nosing", ["stair nosing", "stair nosing trim", "tile stair nosing", "step edge trim"])),
 ("Diminishing trim", None, ("Tile Transition Strip", ["tile transition strip", "tile reducer strip", "tile threshold strip", "tile to floor ramp edge"])),
 ("Ramp Trim", None, ("Tile Transition Ramp", ["tile ramp trim", "tile transition strip", "tile threshold ramp", "tile edge ramp"])),
 ("T Shaped Trim", None, ("Tile Transition Strip", ["T bar tile trim", "tile transition strip", "tile divider strip", "feature strip"])),
 ("Tile Trims + Edging Profiles", r"joiner|corner", (None, ["tile trim corners", "tile trim joiners", "tile trim end caps"])),
 ("Tile Spacers", None, ("Tile Spacers", ["tile spacers", "tiling spacers", "tile cross spacers", "grout spacers"])),
 ("Tile Wedges", None, ("Tile Wedges", ["tile wedges", "tiling wedges", "tile wedges and spacers"])),
 ("Tile Leveling Systems", None, ("Tile Levelling System", ["tile levelling system", "tile levelling clips", "tile leveling system", "tile lippage clips and wedges"])),
 ("Tile Spacers & Levelling", r"level|clip|wedge|cap|strap", ("Tile Levelling System", ["tile levelling system", "tile levelling clips", "tile leveling system", "tile levelling wedges"])),
 ("Tile Spacers & Levelling", None, ("Tile Spacers", ["tile spacers", "tiling spacers", "grout spacers"])),
 ("Tile Cutters", r"tile cutter", ("Manual Tile Cutter", ["tile cutter", "manual tile cutter", "tile cutting machine", "porcelain tile cutter"])),
 ("Tile Saws", None, ("Wet Tile Saw", ["wet tile saw", "tile saw", "bridge tile saw", "wet tile cutter"])),
 ("Diamond Blades & Abrasives", r"^(?!.*(bush|spare blade|grooving)).*blade", ("Diamond Tile Blade", ["diamond blade", "tile cutting blade", "diamond tile blade", "porcelain cutting disc"])),
 ("Diamond Blades & Abrasives", r"pad", (None, ["diamond polishing pads", "tile polishing pad", "tile edge polishing pad"])),
 ("Grinding Wheels and Polishing Pads", None, (None, ["diamond polishing pads", "tile polishing pad", "tile edge polisher"])),
 ("Drill Bits", r"^(?!.*(adapter|adaptor|guide))", ("Tile Drill Bit", ["tile drill bit", "diamond drill bit", "diamond core drill bit", "tile hole saw", "porcelain drill bit"])),
 ("Diamond Drill Bits", r"^(?!.*(adapter|adaptor|guide)).*bit", ("Tile Drill Bit", ["tile drill bit", "diamond core drill bit", "tile hole saw", "porcelain drill bit"])),
 ("Core Drills", None, ("Tile Drill Bit", ["tile drill bit", "diamond core drill bit", "tile hole saw", "porcelain drill bit"])),
 ("Tiling Trowels & Floats", r"notch", ("Notched Tiling Trowel", ["notched trowel", "tiling trowel", "tile adhesive trowel"])),
 ("Tiling Trowels & Floats", r"^(?!.*handle).*(grout float|rubber float|gum float|sweepex|washboy)", ("Grout Float", ["grout float", "rubber grout float", "tiling float"])),
 (None, r"sponge", (None, ["grout sponge", "tile sponge", "tiling sponge"])),
 ("Grout Clean Up", r"washboy|bucket|system|maximo", (None, ["grout clean up bucket", "grout wash bucket", "washboy grout bucket"])),
 ("Grout", r"epoxy", ("Epoxy Tile Grout", ["epoxy grout", "epoxy tile grout", "epoxy grout for showers"])),
 ("Grout", None, ("Tile Grout", ["tile grout", "coloured grout", "floor and wall grout"])),
 ("Adhesives", r"tile adhesive|tile glue", ("Tile Adhesive", ["tile adhesive", "tile glue", "tile cement"])),
 ("Waterproofing Membranes", r"^(?!.*(primer|asphalt|top coat)).*(membrane|wpm|waterproof)", ("Waterproofing Membrane", ["waterproofing membrane", "shower waterproofing", "bathroom waterproofing membrane"])),
 ("Waterproofing Accessories", r"tape|band", ("Waterproofing Tape", ["waterproofing tape", "waterproofing bandage", "sealing tape"])),
 ("Screeds & Levellers", r"level", ("Self Levelling Compound", ["self levelling compound", "floor leveller", "floor levelling compound"])),
 ("Screeds & Levellers", r"screed", (None, ["floor screed", "sand cement screed", "tile bedding screed"])),
 ("Primers & Additives", r"prim", (None, ["tile primer", "tiling primer", "waterproofing primer"])),
 ("Silicone Sealants", r"pool", ("Pool Silicone Sealant", ["pool silicone", "pool silicone sealant", "swimming pool sealant"])),
 ("Silicone Sealants", r"silicone", ("Silicone Sealant", ["silicone sealant", "bathroom silicone", "coloured silicone"])),
 ("Hybrid Sealants", None, (None, ["hybrid sealant", "polyurethane sealant", "paintable sealant"])),
 ("Silicone Accessories", r"gun", ("Caulking Gun", ["caulking gun", "silicone gun", "sausage gun"])),
 ("Silicone Accessories", r"backer", (None, ["backer rod", "foam backing rod", "caulking backer rod"])),
 ("Silicone Accessories", r"smooth|applicator|nozzle|stick", (None, ["silicone tool", "silicone smoothing tool", "silicone tooling"])),
 ("Sealants, Sealers & Cleaners", r"sealer", (None, ["tile sealer", "grout sealer", "stone sealer"])),
 ("Sealants, Sealers & Cleaners", r"clean|acid|haze|remov", (None, ["tile cleaner", "grout cleaner", "grout haze remover"])),
 ("Knee Pads & Workwear", r"knee pads?(?!.*(strap|liner|button))", ("Tilers Knee Pads", ["knee pads for tiling", "tilers knee pads", "work knee pads"])),
 ("Suction Cups & Lifters", r"suction", ("Tile Suction Cup", ["tile suction cup", "suction lifter", "slab and glass suction lifter"])),
 ("Mixing Tools", r"paddle|stirrer", ("Mixing Paddle", ["mixing paddle", "mixing paddle for drill", "tile adhesive mixer paddle"])),
 ("Mixers", r"^(?!.*not including).*paddle", ("Mixing Paddle", ["mixing paddle", "mixing paddle for drill", "tile adhesive mixer paddle"])),
 ("Waterproofing Tools", r"spiked", (None, ["spiked roller", "spiked roller for self levelling compound"])),
 ("Screeding Tools", None, (None, ["screed bar", "screeding level", "floor levelling tools"])),
 ("Bathroom Niche Boxes", None, ("Shower Niche", ["shower niche", "niche box for shower", "shower niche insert", "recessed shower shelf"])),
 ("Ceramic and Modern Bathroom Fixtures", r"soap", ("Ceramic Soap Holder", ["ceramic soap holder", "tile-in soap dish", "shower soap holder"])),
 ("Ceramic and Modern Bathroom Fixtures", r"shelf", ("Ceramic Shower Shelf", ["ceramic shower shelf", "tile-in shower shelf", "shower corner shelf"])),
 ("Tile Backer Boards", None, ("Tile Backer Board", ["tile backer board", "wedi board", "waterproof tile backer board"])),
 ("Uncoupling & Acoustic Mats", None, (None, ["uncoupling membrane", "decoupling mat", "tile underlay mat"])),
]
words = lambda s: set(re.findall(r"[a-z0-9]+", s.lower().replace("levelling", "leveling").replace("tiling", "tile").replace("tilers", "tile")))
stem = lambda ws: {w[:-1] if w.endswith("s") and len(w) > 3 else w for w in ws}
has = lambda title, phrase: stem(words(phrase)) <= stem(words(title))
AKA = re.compile(r'\s*<p class="ets-aka">.*?</p>', re.S)

def rule(p):
    t = p["title"].lower()
    for typ, rx, val in RULES:
        if (typ is None or typ == p["productType"]) and (rx is None or re.search(rx, t)): return val
    return None

def plan(p):
    r = rule(p)
    if not r: return None
    kw, aka = r
    old = p["seo"]["title"] or p["title"]
    base = re.sub(r"\s*\|.*$", "", old).strip()            # drop the old "| ETS Perth" tail
    new = old
    plain_tail = re.fullmatch(r"[^|]*(\|\s*ETS( Perth)?\s*)?", old)      # leave titles that already carry a hand-written phrase
    if kw and plain_tail and not has(p["title"], kw) and not has(old, kw):
        new = next((c for c in (f"{base} | {kw} | ETS", f"{base} | {kw}") if len(c) <= MAX), old)
    terms = [a for a in aka if not has(p["title"], a)] or aka[:2]
    line = '<p class="ets-aka">Also known as: %s.</p>' % ", ".join(terms)
    body = AKA.sub("", p["descriptionHtml"] or "").rstrip() + "\n" + line
    return dict(id=p["id"], title=p["title"], type=p["productType"], old_seo_title=p["seo"]["title"], seo_title=new,
                seo_desc=p["seo"]["description"], aka=", ".join(terms), descriptionHtml=body,
                changed_title=new != old, changed_body=body != (p["descriptionHtml"] or ""))

def demo():
    p = dict(id="x", title="Roberts Designs Square Grate Shower Floor Waste - 80mm Outlet", productType="Floor Drains",
             seo=dict(title="Square Grate Shower Floor Waste 80mm Outlet | ETS Perth", description="d"), descriptionHtml="<p>Solid brass.</p>")
    r = plan(p)
    assert r["seo_title"] == "Square Grate Shower Floor Waste 80mm Outlet | Floor Drain Grate", r["seo_title"]
    assert "floor drain grate" in r["aka"] and r["descriptionHtml"].startswith("<p>Solid brass.</p>")
    p["descriptionHtml"] = r["descriptionHtml"]; assert plan(p)["descriptionHtml"] == r["descriptionHtml"]   # rerun is stable
    assert plan(dict(p, productType="Tiling Machine Parts", title="Sigma M8 Nut")) is None

if __name__ == "__main__":
    demo()
    rows = [r for p in json.load(open(sys.argv[1])) if p["status"] != "ARCHIVED" for r in [plan(p)] if r]
    json.dump(rows, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
    print(len(rows), "products;", sum(r["changed_title"] for r in rows), "search titles change;", sum(r["changed_body"] for r in rows), "descriptions get the line")
