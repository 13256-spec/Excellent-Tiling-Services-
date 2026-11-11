"""Compare our MELA prices with Bathroom City's current (sale) prices. Proposal only; writes nothing to Shopify.
Usage: bc_match_2026_11.py <dir with bc-N.json and ours-N.json from /products.json?limit=250&page=N> <this pricing dir> <out.csv>
Report: reports/bathroom-city-match-proposal-2026-11-11.md (built from the CSV)."""
import csv, glob, json, math, sys, os
from collections import Counter
BC_DIR = sys.argv[1]; PR = sys.argv[2]; OUT = sys.argv[3]
def feed(prefix):
    out = []
    for f in sorted(glob.glob(os.path.join(BC_DIR, prefix + "-*.json")), key=lambda x: int(x.rsplit("-",1)[1].split(".")[0])):
        out += json.load(open(f))["products"]
    return out
bc, ours = feed("bc"), feed("ours")
print("bc products", len(bc), "vendors", Counter(p["vendor"] for p in bc).most_common(8))
bc_by_sku = {}; bc_by_title = {}
for p in bc:
    for v in p["variants"]:
        row = {"title": p["title"], "vtitle": v["title"], "sku": v["sku"] or "", "price": float(v["price"]),
               "cap": float(v["compare_at_price"]) if v["compare_at_price"] else None, "avail": v["available"], "handle": p["handle"]}
        if row["sku"]: bc_by_sku.setdefault(row["sku"].strip().upper(), row)
        bc_by_title[(p["title"], row["sku"])] = row
        bc_by_title.setdefault((p["title"], v["title"]), row)
mela_map = {r["vid"].split("/")[-1]: r for r in csv.DictReader(open(os.path.join(PR, "mela-pricing-2026-10-01.csv")))}
master = {r["vid"].split("/")[-1]: r for r in csv.DictReader(open(os.path.join(PR, "store-pricing-2026-10-03.csv")))}
rows = []
for p in ours:
    if p["vendor"] != "MELA": continue
    for v in p["variants"]:
        vid = str(v["id"]); m = mela_map.get(vid); mr = master.get(vid)
        b = None; how = ""
        if m and m.get("bc_title"):
            b = bc_by_title.get((m["bc_title"], m["bc_sku"])) or (bc_by_sku.get(m["bc_sku"].strip().upper()) if m["bc_sku"] else None); how = "map"
        if b is None and v["sku"]:
            b = bc_by_sku.get(v["sku"].strip().upper()); how = "sku" if b else ""
        cost = float(mr["cost"]) if mr and mr["cost"] else None
        band = int(mr["trade_band"] or 0) if mr else 0
        floor = cost / 0.80 if cost else None
        price = float(v["price"]); cap = float(v["compare_at_price"]) if v["compare_at_price"] else None
        r = {"product": p["title"], "variant": "" if v["title"] == "Default Title" else v["title"], "sku": v["sku"] or "",
             "vid": vid, "pid": str(p["id"]), "our_price": price, "our_cap": cap, "cost": cost, "floor20": floor, "band": band,
             "bc_title": b["title"] if b else "", "bc_price": b["price"] if b else None, "bc_cap": b["cap"] if b else None,
             "bc_avail": b["avail"] if b else None, "match": how}
        if b is None:
            r["action"] = "not on Bathroom City"; r["new_price"] = price; r["new_cap"] = cap
        else:
            target = b["price"]
            if floor and target < floor - 0.005:
                r["new_price"] = math.ceil(floor * 20) / 20; r["action"] = "BC under our floor: stay at floor" if abs(r["new_price"] - price) > 0.005 else "BC under our floor: unchanged"
                if r["new_price"] < price - 0.005: r["action"] = "lower to floor (BC under floor)"
            else:
                r["new_price"] = target
                r["action"] = ("lower" if target < price - 0.005 else "raise" if target > price + 0.005 else "same")
            on_sale = b["cap"] is not None and b["cap"] > r["new_price"] + 0.005
            r["new_cap"] = b["cap"] if on_sale else None
            r["bc_on_sale"] = on_sale
        r["new_margin"] = round((r["new_price"] - cost) / r["new_price"] * 100, 1) if cost and r["new_price"] else None
        r["trade_price"] = round(r["new_price"] * (100 - band) / 100, 2)
        r["trade_margin"] = round((r["trade_price"] - cost) / r["trade_price"] * 100, 1) if cost else None
        rows.append(r)
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
c = Counter(r["action"] for r in rows); print(len(rows), "MELA variants"); print(c)
print("BC on sale among matched:", sum(1 for r in rows if r.get("bc_on_sale")))
print("match how:", Counter(r["match"] for r in rows))
lo = [r for r in rows if r["action"].startswith("lower")]; hi = [r for r in rows if r["action"] == "raise"]
print("lower total $", round(sum(r["our_price"] - r["new_price"] for r in lo), 2), "raise total $", round(sum(r["new_price"] - r["our_price"] for r in hi), 2))
print("trade under 20% after:", sum(1 for r in rows if r["trade_margin"] is not None and r["band"] and r["trade_margin"] < 19.95 and r["action"] != "not on Bathroom City"))
print("no cost:", sum(1 for r in rows if r["cost"] is None))
