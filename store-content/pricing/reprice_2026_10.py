"""Store-wide public and trade pricing plan (3 Oct 2026).

Public prices undercut the competitor that sells the same item; trade prices go lower again
through per-product trade bands. Every price stays above a profit floor based on unit cost.

Competitors (public online prices):
- MELA bathroomware: Bathroom City (sole other MELA stockist), matched via mela-pricing-2026-10-01.csv.
- Tiling hardware: B&B Hardware, Maddington (bbhardware.com.au), matched by hand in BB_MATCH.
  Terweys Total Hardware (Cannington) publishes no prices online, so it can't be compared.
- Eternity tiles: already priced 15% under Eternity's RRP on 2 Oct (eternity_2026_10.py); trade only here.

Rules (costs are ex GST, prices inc GST):
- Public floor = cost x 1.1 x 1.25 (at least 20% margin ex GST). Trade floor = cost x 1.1 x 1.15.
- MELA cost (estimate) = Bathroom City list price x (1 - SLIVER trade discount) / 1.1.
- MELA matched: 5% under Bathroom City's current price, rounded down to the dollar.
- Hardware matched on B&B: 5% under B&B, rounded down to 5c.
- Other hardware with a cost: 10% under our current price (supplier RRP), rounded down to 5c.
- A price is only raised when it is below the public floor, by at most 10% and never to or above the
  competitor; bigger gaps are flagged for the owner. No cost recorded -> left alone.
- Trade band per product = the deepest of 25/20/15/10/5% (tiles: 15% max) that keeps every variant
  above the trade floor.

Usage: reprice_2026_10.py cat.json bc_dir bb_dir out.csv
  cat.json: {"V": [variants with "p" product]} from a bulk export; bc_dir/bb_dir: products.json pages.
"""
import csv, glob, json, math, os, sys

GST, PUB_MARKUP, TRADE_MARKUP = 1.1, 1.25, 1.15
MAX_RAISE = 1.10  # bigger rises below the floor are flagged for the owner, not applied
TILE_BAND_MAX = 15  # trade on tiles: about 15% off public, as approved 2 Oct
BANDS = [25, 20, 15, 10, 5, 0]
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
    "Siri Interchangeable Blue Handle": "SIRI BLUE HANDLE FITS ALL SPONGES AND GROUT ATTACHMENTS",
    "Barwalt KN-1 Ultralight Knee Pad": "BARWALT KNEE PAD PRO ULTRALIGHT - MADE IN USA",
    "Baron E120 Forced Action Mixer": "BARON E 120L FORCED ACTION SCREED MIXER",
}


def feed(d):
    return [p for f in sorted(glob.glob(os.path.join(d, "p*.json"))) for p in json.load(open(f))["products"]]


def down(x, step):
    return math.floor(round(x / step, 6)) * step


def main(cat, bc_dir, bb_dir, out):
    V = [v for v in json.load(open(cat))["V"] if v["p"]["status"] == "ACTIVE"]
    bc = {(p["title"], v["sku"]): float(v["price"]) for p in feed(bc_dir) for v in p["variants"]}
    bb = {p["title"]: float(p["variants"][0]["price"]) for p in feed(bb_dir)}
    mela = {r["vid"]: r for r in csv.DictReader(open(os.path.join(HERE, "mela-pricing-2026-10-01.csv")))}
    rows = []
    for v in V:
        p = v["p"]
        name = p["title"] + ("" if v["title"] == "Default Title" else " / " + v["title"])
        price = float(v["price"])
        cost = (v["inventoryItem"]["unitCost"] or {}).get("amount")
        cost_src = "Shopify" if cost else ""
        r = dict(product=p["title"], variant=v["title"], sku=v["sku"], vendor=p["vendor"], type=p["productType"],
                 old_price=price, competitor="", comp_price="", vid=v["id"], inv=v["inventoryItem"]["id"],
                 pid=p["id"], tags=" ".join(p["tags"]))
        target, step, flag = None, 0.05, ""
        if p["vendor"] == "MELA":
            m = mela.get(v["id"])
            # The SLIVER sheet gives a trade discount off the GST-inclusive list price, so the
            # estimate includes GST; store it ex GST like every other cost. (The 34 MELA costs
            # already in Shopify are the same inc-GST estimate.)
            if m and m["cost"]:
                cost, cost_src = round(float(m["cost"]) / GST, 2), "estimate: list x (1 - SLIVER discount) / 1.1"
            if m and m["bc_title"]:
                bp = bc.get((m["bc_title"], m["bc_sku"]))
                if bp is None:
                    flag = "no longer on Bathroom City"
                else:
                    r.update(competitor="Bathroom City", comp_price=bp)
                    target, step = bp * 0.95, 1
        elif p["productType"] == "Tile":
            flag = "tile: public price set 2 Oct (15% under Eternity RRP)"
        else:
            key = name if name in BB_MATCH else p["title"]
            if key in BB_MATCH and BB_MATCH[key] in bb:
                bp = bb[BB_MATCH[key]]
                r.update(competitor="B&B Hardware", comp_price=bp)
                target = bp * 0.95
            elif cost:
                target = price * 0.90
        if cost:
            cost = float(cost)
            floor = cost * GST * PUB_MARKUP
            new = price
            if target is not None:
                new = min(price, down(target, step) if target >= 20 or step < 1 else down(target, 0.5))
            if new < floor:
                new = math.ceil(floor * 20) / 20 if step < 1 else math.ceil(floor)
                if r["comp_price"] and new >= r["comp_price"]:
                    flag = f"{r['competitor']} is below our profit floor; not undercut"
                if new > price:
                    if new > price * MAX_RAISE or (r["comp_price"] and new >= r["comp_price"]):
                        flag, new = f"BELOW PROFIT FLOOR: needs {new:.2f}+, kept {price:.2f} for owner review", price
                    else:
                        flag = "raised slightly: old price was below the profit floor"
            r.update(cost=cost, cost_src=cost_src, new_price=round(new, 2),
                     margin_pct=round((1 - cost * GST / new) * 100, 1), flag=flag)
        else:
            r.update(cost="", cost_src="", new_price=price, margin_pct="", flag=flag or "no cost recorded; price left as is")
        rows.append(r)
    # trade band per product
    by_p = {}
    for r in rows:
        by_p.setdefault(r["pid"], []).append(r)
    for pid, rs in by_p.items():
        if any(r["cost"] == "" for r in rs):
            band = 5 if "trade-5" in rs[0]["tags"].split() else 0
        else:
            cap = TILE_BAND_MAX if rs[0]["type"] == "Tile" else 100
            band = next((b for b in BANDS if b <= cap and all(r["new_price"] * (1 - b / 100) >= r["cost"] * GST * TRADE_MARKUP for r in rs)), 0)
        for r in rs:
            tp = round(r["new_price"] * (1 - band / 100), 2)
            r.update(trade_band=band, trade_price=tp,
                     trade_margin_pct=round((1 - r["cost"] * GST / tp) * 100, 1) if r["cost"] != "" and tp else "")
    cols = ["product", "variant", "sku", "vendor", "type", "old_price", "new_price", "trade_band", "trade_price",
            "cost", "cost_src", "margin_pct", "trade_margin_pct", "competitor", "comp_price", "flag", "vid", "inv", "pid", "tags"]
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    return rows


if __name__ == "__main__":
    import collections
    rows = main(*sys.argv[1:5])
    ch = [r for r in rows if r["new_price"] != r["old_price"]]
    print("variants", len(rows), "price changes", len(ch), "down", sum(r["new_price"] < r["old_price"] for r in ch),
          "up", sum(r["new_price"] > r["old_price"] for r in ch))
    print("flags", collections.Counter(r["flag"] for r in rows).most_common())
    bands = {}
    for r in rows:
        bands[r["pid"]] = (r["trade_band"], r["vendor"] if r["vendor"] in ("MELA",) else ("Tile" if r["type"] == "Tile" else "Hardware"))
    print("trade bands (products)", collections.Counter(bands.values()).most_common())
    beat = [r for r in rows if r["comp_price"] != ""]
    print("matched to a competitor", len(beat), "cheaper than them", sum(r["new_price"] < r["comp_price"] for r in beat))
