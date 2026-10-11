"""Store-wide public and trade pricing plan, 11 Oct 2026 (replaces reprice_2026_10.py).

Goal set by the owner on 11 Oct 2026: cheaper than every competitor on every item, cheaper again on
high-margin items, and approved trade accounts cheaper still. Profit floor still applies.

Inputs
- Shopify bulk export of every ACTIVE product/variant (bulk/catalog.jsonl): price, unit cost (ex GST),
  vendor, type, tags.
- Public product feeds: Bathroom City (MELA) and B&B Hardware, Maddington (tiling hardware).
- mela-pricing-2026-10-01.csv: which Bathroom City product/SKU each MELA variant is.
- BB_MATCH (below): our product [/ variant] -> B&B title, checked by hand.
- tradelists.json: which trade-list-N collection each product is in today (for the change list).

Rules (prices inc GST, costs ex GST)
- Public floor  = cost x 1.1 x 1.25  (20% of the sale price is profit, ex GST).
- Trade floor   = cost x 1.1 x 1.15.
- Margin cap    = 40%: any item earning more than 40% is cut to 40% (price = cost x 1.1 / 0.6).
  This is the "high-margin items get cheaper" rule.
- Competitor    = 5% under the competitor's current price; 10% under when we'd still make 40%+ at
  5% under. Never below the floor: if the competitor is below our floor we sit at the floor and the
  item is flagged "competitor below our floor".
- Prices are only raised when the current price is below the floor, and never to or above the
  competitor (those stay and are flagged BELOW PROFIT FLOOR for the owner).
- Rounding: MELA down to the dollar, tiles down to 10c, everything else down to 5c. Floors round up.
- No cost recorded -> price left alone. Same cost on every size of a product whose prices differ by
  25%+ -> cost treated as unverified: price kept, trade band 5%, flagged COST CHECK.
- Trade band per product = deepest of 25/20/15/10/5% that keeps every variant above the trade floor
  (tiles max 15%). Products with a variant that has no cost get 5%.

Usage: reprice_2026_10_11.py catalog.jsonl bc_dir bb_dir tradelists.json out.csv
"""
import csv, glob, json, math, os, sys, collections

GST, PUB_MARKUP, TRADE_MARKUP = 1.1, 1.25, 1.15
MARGIN_CAP = 0.40
TILE_BAND_MAX = 15
BANDS = [25, 20, 15, 10, 5]
HERE = os.path.dirname(os.path.abspath(__file__))

# Our product title [/ variant] -> B&B product title (same item, checked by hand)
BB_MATCH = {
    **{f"Vacuum Brazed Diamond Drill Bits / {s}mm": f"ROBERTS VACUUM BRAZED {s}MM DIAMOND DRILL BIT"
       for s in (6, 8, 10, 12, 25, 35, 38, 45, 50)},
    **{f"Stainless Steel Square Notched Maxi Grip Trowel / {s}mm": f"ROBERTS S/S {s}mm SQUARE NOTCH TROWEL"
       for s in (4, 6, 8, 10, 12, 15)},
    "Smoothtex A / 250ml": "MAXISIL A SMOOTHTEX CERAMIC HANDLING 250ML",
    "Smoothtex A / 1 litre": "MAXISIL A SMOOTHTEX CERAMIC HANDLING 1 LITRE",
    "Maxisil Wet Area Silicone": "MAXISIL A #02 WHITE   COLOURED SILICONE 310ML",
    "Tile Insert Floor Waste – 50mm Outlet / Brushed Copper": "ROBERTS DESIGNS TILE INSERT BRUSHED COPPER 50MM",
    "Tile Insert Floor Waste – 50mm Outlet / Matte Black": "ROBERTS DESIGN FLOOR DRAIN 50MM T/INSERT MATTE BLACK",
    "Tile Insert Floor Waste – 80mm Outlet / Matte Black": "ROBERTS DESIGN FLOOR DRAIN 80MM T/INSERT MATTE BLACK",
    "Sigma 24E Handle": "SIGMA HANDLE SIG-24E SUITS 3B4",
    "Sigma 24C Handle": "SIGMA HANDLE SIG 24C SUIT 2A3 2B3",
    "Sigma 24AE Handle": "SIGMA HANDLE SIG-24AE SUITS 3C2 3D2",
    "Sigma 19C Square": "SIGMA SLIDING SQUARE SUPPORT  ART-19C",
    "Sigma 19D Square": "SIGMA SLIDING SQUARE SUPPORT ART-19D SUIT 3 SERIES CUTTERS",
    "Sigma 19N Square 260mm": "SIGMA SLIDING SQUARE SUPPORT ART-19N SUIT 4 SERIES CUTTERS",
    "Sigma Swivel Measurement Bar for 4DU ART90ND": "SIGMA CALIBRATED SUPPORT ARM SIG-90NC SUITS 4DU CUTTER",
    "Sigma Swivel Measurement Bar for 4CU ART90NC": "SIGMA CALIBRATED SUPPORT ARM SIG-90NC SUITS 4CU CUTTER",
    "Sigma Swivel Measurement Bar for 4BU ART90NB": "SIGMA CALIBRATED SUPPORT ARM SIG-90NB SUITS 4BU CUTTER",
    "Sigma Handle ART 24N for ART 4 Push series": 'SIGMA 24N "NEX" PUSH HANDLE TO SUIT 4B, 4C, 4D, 4E, FN CUTTERS',
    "Sigma Handle ART 24U for ART 4 Up series": 'SIGMA 24U PULL "UP" HANDLE TO SUIT 4B, 4C, 4D, 4E, FN CUTTERS',
    "Sigma Spare Wheel with axle ART14N – 16mm dia": "SIGMA REPLACEMENT SCORING WHEEL NEX SERIES ART14N",
    "Sigma Spare Wheel with axle ART14U – 12mm dia": "SIGMA REPLACEMENT SCORING WHEEL UP SERIES ART14U",
    "Sigma Titanium Wheel with axle ART14UT – 12mm dia": "SIGMA REPLACEMENT TITANIUM SCORING WHEEL UP SERIES ART14U",
    "Sigma Tile Cutter ART 4FN – 155cm": 'TILE CUTTER DRY SIGMA 155CM ART 4FN WITH "NEX" PUSH HANDLE',
    "Sigma Tile Cutter ART 4EN – 125cm": 'TILE CUTTER DRY SIGMA 125CM ART 4EN WITH "NEX" PUSH HANDLE',
    "Sigma Tile Cutter ART 4DU – 103cm": 'TILE CUTTER DRY SIGMA 103CM ART 4DU WITH "UP" PULL HANDLE',
    "Sigma Tile Cutter ART 4CU – 84cm": 'TILE CUTTER DRY SIGMA 84CM ART 4CU WITH "UP" PULL HANDLE',
    "Sigma Tile Cutter ART 4BU – 70cm": 'TILE CUTTER DRY SIGMA 70CM ART 4BU WITH "UP" PULL HANDLE',
    "Siri Interchangeable Blue Handle": "SIRI BLUE HANDLE FITS ALL SPONGES AND GROUT ATTACHMENTS",
    "Siri Yellow Sponge No Cuts – Fits RDXT609 Handle": "SIRI REPLACEMENT SMALL YELLOW SPONGE (NO CUTS)",
    "Barwalt KN-1 Ultralight Knee Pad": "BARWALT KNEE PAD PRO ULTRALIGHT - MADE IN USA",
    "Baron E120 Forced Action Mixer": "BARON E 120L FORCED ACTION SCREED MIXER",
    # added 11 Oct 2026 (BAT / Raimondi range)
    "BAT Parrot Nipper": "BAT PARROT NIPPER",
    "BAT Straight Nipper": "BAT STRAIGHT NIPPER INLINE",
    "BAT Dual Suction Cup - 4 inch": "BAT DUAL SUCTION CUP 4 INCH",
    "BAT Paint Brush 100mm": "BAT TRIMS PAINT BRUSH 100MM",
    "BAT Pro Diamond Mesh Turbo Rim Blade 115mm": "BAT TURBO MESH DIAMOND BLADE 115MM",
    "BAT Tile Crosses 1.5mm 100 Bag": "BAT TILE CROSSES 1.5MM PK 100",
    "BAT T Shapes 1.5mm 500 Bag": "BAT T SPACER 1.5MM 500 BAG",
    "BAT Cross Tile Spacers 1.5mm – 500 Pack": "BAT TILE CROSSES 1.5MM PK 500",
    "BAT Chrome Plated Floor Drain - 100mm with PVC Collar": "BAT TRIMS FLOOR WASTE 100MM SQUARE CHROME WITH PVC COLLAR",
    "Raimondi Folding Extension Table - Suit Pikus": "RAIMONDI FOLDING EXTENSION TABLE- SUIT PIKUS",
    "Raimondi Zoe Electric Wet Saw 3HP / Zoe 85A": "RAIMONDI ZOE 85A ELECTRIC WET SAW",
    "Raimondi 5 Roller Extension Table - Zoe": "RAIMONDI 5 ROLLER EXTENSION TABLE - SUIT ZOE & PIKUS",
}


def feed(d):
    return [p for f in sorted(glob.glob(os.path.join(d, "p*.json"))) for p in json.load(open(f))["products"]]


def down(x, step):
    return round(math.floor(round(x / step, 6)) * step, 2)


def up(x, step):
    return round(math.ceil(round(x / step, 6)) * step, 2)


def load_catalog(path):
    P, V = {}, []
    for line in open(path):
        o = json.loads(line)
        if "__parentId" in o:
            o["pid"] = o.pop("__parentId")
            V.append(o)
        else:
            P[o["id"]] = o
    return P, V


def main(cat, bc_dir, bb_dir, tl_path, out):
    P, V = load_catalog(cat)
    bc = {(p["title"], v["sku"]): float(v["price"]) for p in feed(bc_dir) for v in p["variants"]}
    bb = {}
    for p in feed(bb_dir):
        for v in p["variants"]:
            t = p["title"] + ("" if v["title"] == "Default Title" else " / " + v["title"])
            bb[t] = float(v["price"])
            bb.setdefault(p["title"], float(p["variants"][0]["price"]))
    mela = {r["vid"]: r for r in csv.DictReader(open(os.path.join(HERE, "mela-pricing-2026-10-01.csv")))}
    tl = json.load(open(tl_path))
    band_now = {pid: int(h.split("-")[-1]) for h, ids in tl.items() for pid in ids}
    # Cost sanity check: a product whose variants all carry the same cost while their prices differ by
    # more than 25% (sizes of trim, lengths of drain...) has a cost that was copied across sizes, not
    # looked up. Those prices are kept and flagged; only a verified cost can lower them.
    suspect = set()
    byp = collections.defaultdict(list)
    for v in V:
        byp[v["pid"]].append(v)
    for pid, vs in byp.items():
        costs = {(x["inventoryItem"]["unitCost"] or {}).get("amount") for x in vs}
        prices = [float(x["price"]) for x in vs if float(x["price"]) > 0]
        if len(vs) >= 3 and len(costs) == 1 and None not in costs and prices and max(prices) > min(prices) * 1.25:
            suspect.add(pid)
    rows = []
    for v in V:
        p = P[v["pid"]]
        name = p["title"] + ("" if v["title"] == "Default Title" else " / " + v["title"])
        price = float(v["price"])
        cost = (v["inventoryItem"]["unitCost"] or {}).get("amount")
        is_tile = p["productType"] == "Tile"
        step = 1 if p["vendor"] == "MELA" else (0.1 if is_tile else 0.05)
        r = dict(product=p["title"], variant=v["title"], sku=v["sku"], vendor=p["vendor"], type=p["productType"],
                 old_price=price, competitor="", comp_price="", vid=v["id"], inv=v["inventoryItem"]["id"],
                 pid=p["id"], band_now=band_now.get(p["id"], 0), tags=" ".join(p["tags"]))
        comp, flag = None, ""
        if p["vendor"] == "MELA":
            m = mela.get(v["id"])
            if m and m["bc_title"]:
                comp = bc.get((m["bc_title"], m["bc_sku"]))
                if comp is None:
                    flag = "no longer on Bathroom City"
                else:
                    r.update(competitor="Bathroom City", comp_price=comp)
        else:
            key = name if name in BB_MATCH else p["title"]
            if key in BB_MATCH and BB_MATCH[key] in bb:
                comp = bb[BB_MATCH[key]]
                r.update(competitor="B&B Hardware", comp_price=comp)
        if not cost:
            r.update(cost="", cost_src="", new_price=price, margin_pct="", flag="no cost recorded; price left as is", rule="no cost")
            rows.append(r)
            continue
        cost = float(cost)
        if p["id"] in suspect:
            r.update(cost=cost, cost_src="Shopify (unverified: same cost on every size)", new_price=price, rule="kept (cost unverified)",
                     margin_pct=round((1 - cost * GST / price) * 100, 1),
                     flag="COST CHECK: every size has the same cost but prices differ; price kept until the supplier cost is confirmed")
            rows.append(r)
            continue
        floor = up(cost * GST * PUB_MARKUP, step)
        cap = down(cost * GST / (1 - MARGIN_CAP), step)
        cands = {"kept": price, "margin cap 40%": cap}
        if comp is not None:
            c5 = down(comp * 0.95, step)
            cands["5% under competitor"] = c5
            if 1 - cost * GST / c5 >= MARGIN_CAP:
                cands["10% under competitor"] = down(comp * 0.90, step)
        rule, new = min(cands.items(), key=lambda kv: kv[1])
        if new < floor:
            if comp is not None and floor >= comp:
                flag = f"{r['competitor']} ${comp:.2f} is below our floor ${floor:.2f}; not undercut"
            if price < floor:
                # current price is below the floor: raise to the floor unless that puts us at/above the competitor
                if comp is not None and floor >= comp:
                    flag = f"BELOW PROFIT FLOOR: needs ${floor:.2f}+, {r['competitor']} is ${comp:.2f}; kept ${price:.2f} for owner review"
                    rule, new = "kept (below floor, owner review)", price
                else:
                    rule, new = "raised to profit floor", floor
            else:
                rule, new = "profit floor", floor
        r.update(cost=cost, cost_src="Shopify", new_price=round(new, 2), rule=rule,
                 margin_pct=round((1 - cost * GST / new) * 100, 1), flag=flag)
        rows.append(r)
    by_p = collections.defaultdict(list)
    for r in rows:
        by_p[r["pid"]].append(r)
    for pid, rs in by_p.items():
        if any(r["cost"] == "" or r["rule"] == "kept (cost unverified)" for r in rs):
            band = 5
        else:
            cap_b = TILE_BAND_MAX if rs[0]["type"] == "Tile" else 100
            band = next((b for b in BANDS if b <= cap_b and all(
                r["new_price"] * (1 - b / 100) >= r["cost"] * GST * TRADE_MARKUP for r in rs)), 0)
        for r in rs:
            tp = round(r["new_price"] * (1 - band / 100), 2)
            r.update(trade_band=band, trade_price=tp,
                     trade_margin_pct=round((1 - r["cost"] * GST / tp) * 100, 1) if r["cost"] != "" and tp else "")
    cols = ["product", "variant", "sku", "vendor", "type", "old_price", "new_price", "rule", "trade_band", "band_now",
            "trade_price", "cost", "cost_src", "margin_pct", "trade_margin_pct", "competitor", "comp_price", "flag",
            "vid", "inv", "pid", "tags"]
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return rows


if __name__ == "__main__":
    rows = main(*sys.argv[1:6])
    ch = [r for r in rows if r["new_price"] != r["old_price"]]
    print("variants", len(rows), "price changes", len(ch), "down", sum(r["new_price"] < r["old_price"] for r in ch),
          "up", sum(r["new_price"] > r["old_price"] for r in ch))
    print("rules", collections.Counter(r["rule"] for r in rows).most_common())
    print("flags", collections.Counter((r["flag"] or "")[:40] for r in rows).most_common())
    bands = {r["pid"]: (r["trade_band"], r["band_now"]) for r in rows}
    print("band changes (products)", sum(1 for b, n in bands.values() if b != n), "of", len(bands))
    print("bands", collections.Counter(b for b, n in bands.values()).most_common())
    beat = [r for r in rows if r["comp_price"] != ""]
    print("matched to a competitor", len(beat), "cheaper than them", sum(r["new_price"] < r["comp_price"] for r in beat))
