"""Roberts Designs price list effective 18 Nov 2026: proposal only, changes nothing.

Usage: roberts_price_list_2026_11.py LIVE_DIR BB_FEED.json
  LIVE_DIR  saved pages of the Admin productVariants query (vendors Roberts Designs, Maxisil, Sigma, Siri, Baron, Barwalt)
            with id sku title price inventoryItem{unitCost} product{id title vendor status band sup collections}
  BB_FEED   bbhardware.com.au/products.json, all pages, as one list
Reads ../supplier-sync/roberts-price-list-2026-11-18.csv (the supplier PDF, ex GST) and writes
reports/roberts-price-list-2026-11-18.{csv,md}.

Rules (PRICING-PLAYBOOK.md v2): cost = list price x 1.1. Public price = a little under the cheapest competitor on file
(5% under B&B Hardware, 3% under the September web match, else 5% under Roberts' recommended retail inc GST), rounded
down to 5c, never under the floor (30% margin; 25% on lines B&B also sells). Owner's choice 26 Nov 2026 for Roberts lines:
"5% under RRP + 30% floor", "Raise trade floor to 30%" (the playbook's general floors are 25/20). Band = deepest of 20/15/10/5 that keeps
every variant of the product at the trade floor (products with no cost or price change keep their band). Variants not on
the list keep their price and cost. Where the list's RRP leaves no 30% margin the cost is updated and the price is not cut.
"""
import csv, glob, json, math, os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from reprice_2026_10 import BB_MATCH
norm = lambda s: re.sub(r"[^A-Z0-9]", "", (s or "").upper())
dn = lambda x: math.floor(round(x / 0.05, 6)) * 0.05
up = lambda x: math.ceil(round(x / 0.05, 6)) * 0.05
margin = lambda p, c: (p - c) / p * 100 if p else 0
ALIAS = {"RD30W": "RD30"}                                   # our SKU -> list part number
PICK = {"RDXD1016": "long collar"}                          # part number printed twice on the list: which row is ours

pl = collections.defaultdict(list)
for r in csv.DictReader(open(os.path.join(HERE, "..", "supplier-sync", "roberts-price-list-2026-11-18.csv"))): pl[norm(r["sku"])].append(r)
def list_row(sku):
    rs = pl.get(ALIAS.get(norm(sku), norm(sku)), [])
    if len(rs) > 1 and norm(sku) in PICK: rs = [r for r in rs if PICK[norm(sku)] in r["desc"]]
    return rs[0] if rs else None                            # RD6003-0001: first row = single-roll price

V = {}
for f in sorted(glob.glob(os.path.join(sys.argv[1], "*"))):
    for v in json.load(open(f))["data"]["productVariants"]["nodes"]: V[v["id"]] = v
bb = {p["title"]: float(p["variants"][0]["price"]) for p in json.load(open(sys.argv[2]))}
audit = {r["vid"]: r for r in csv.DictReader(open(os.path.join(HERE, "reports", "roberts-price-audit-2026-10-23.csv")))}
sep = {r["sku"].upper(): r for r in csv.DictReader(open(os.path.join(HERE, "..", "supplier-sync", "roberts-designs-pricing.csv")))}

rows = []
for v in V.values():
    p = v["product"]; price = float(v["price"]); uc = v["inventoryItem"]["unitCost"]; cost = float(uc["amount"]) if uc else None
    L = list_row(v["sku"]) if (p["sup"] or {}).get("value") == "Roberts Designs" else None
    new_cost = round(float(L["cost_ex"]) * 1.1 + 1e-9, 2) if L else cost
    a = audit.get(v["id"], {}); old_name = a.get("product", "") + ("" if a.get("variant") == "Default Title" else " / " + a.get("variant", ""))
    key = old_name if old_name in BB_MATCH else a.get("product", "")
    cands = []; bbline = key in BB_MATCH and BB_MATCH[key] in bb
    if bbline: cands.append((bb[BB_MATCH[key]], "B&B Hardware", 0.95))
    s = sep.get((v["sku"] or "").upper(), {})
    if s.get("market_source", "roberts-list") != "roberts-list" and s.get("market_price_used"):
        cands.append((float(s["market_price_used"]), s["market_source"].replace("web:", "").replace("match:", "") + " (Sep)", 0.97))
    rrp = round(float(L["rec_retail_ex"]) * 1.1, 2) if L else None
    if rrp: cands.append((rrp, "Roberts RRP", 0.95))
    fm = 0.75 if bbline else 0.70                           # floor margin, public and trade: lines B&B also sells 25%, else 30%
    floor = up(new_cost / fm) if new_cost else None
    comp = who = target = None; note = ""
    if L and rrp <= floor:                                  # list looks wrong (RRP leaves no 30% margin): cost updated, price not cut
        comp, who = rrp, "Roberts RRP"; proposed = max(price, floor); note = "list RRP at or under our floor: ask Roberts; price kept above RRP"
    elif L:
        comp, who, k = min(cands); target = dn(comp * k); proposed = max(floor, target)
        if target < floor: note = "competitor under our floor: held at floor"
    else:
        proposed = price; note = "not on the new list: unchanged"
        if floor and price < floor - 0.005: note += f"; under floor ${floor:.2f}"
    rows.append(dict(sku=v["sku"], vendor=p["vendor"], product=p["title"], variant=v["title"], status=p["status"], stock=v["inventoryQuantity"],
        list_desc=L["desc"] if L else "", old_cost=cost, new_cost=new_cost, cost_change=round(new_cost - cost, 2) if L and cost is not None else "",
        roberts_rrp=rrp or "", competitor=who or "", comp_price=comp or "", old_price=price, new_price=round(proposed, 2), price_change=round(proposed - price, 2),
        margin=round(margin(proposed, new_cost), 1) if new_cost else "", floor=round(floor, 2) if floor else "", fm=fm, old_band=int((p["band"] or {}).get("value") or 0),
        note=note, vid=v["id"], inv=v["inventoryItem"]["id"], pid=p["id"], collections=" ".join(c["handle"] for c in p["collections"]["nodes"] if c["handle"].startswith("trade-list-"))))
byp = collections.defaultdict(list)
for r in rows: byp[r["pid"]].append(r)
for rs in byp.values():
    ok = lambda b: all(r["new_cost"] and round(r["new_price"] * (1 - b / 100) + 1e-9, 2) >= r["new_cost"] / r["fm"] - 0.005 for r in rs)
    band = next((b for b in (20, 15, 10, 5) if ok(b)), 0)
    if all(abs(r["new_price"] - r["old_price"]) < 0.005 and (r["new_cost"] or 0) == (r["old_cost"] or 0) for r in rs): band = rs[0]["old_band"]  # untouched product
    for r in rs:
        r["new_band"] = band; r["trade_price"] = round(r["new_price"] * (1 - band / 100) + 1e-9, 2)
        r["trade_margin"] = round(margin(r["trade_price"], r["new_cost"]), 1) if r["new_cost"] else ""; del r["fm"]
assert all(r["new_price"] >= r["floor"] - 0.005 for r in rows if r["list_desc"])
fn = list(rows[0]); w = csv.DictWriter(open(os.path.join(HERE, "reports", "roberts-price-list-2026-11-18.csv"), "w", newline=""), fieldnames=fn); w.writeheader(); w.writerows(rows)

on = [r for r in rows if r["list_desc"]]; m = lambda x: f"${x:,.2f}"
cu = [r for r in on if r["cost_change"] > 0.004]; cd = [r for r in on if r["cost_change"] < -0.004]
pu = [r for r in on if r["price_change"] > 0.004]; pd = [r for r in on if r["price_change"] < -0.004]
bc = {r["pid"]: r for r in rows if r["new_band"] != r["old_band"]}
nm = lambda r: f"{r['product']}" + ("" if r["variant"] == "Default Title" else f" / {r['variant']}") + f" ({r['sku']})"
line = lambda r: f"| {nm(r)} | {m(r['old_cost'])} -> {m(r['new_cost'])} | {r['competitor']} {m(r['comp_price'])} | {m(r['old_price'])} -> {m(r['new_price'])} | {r['margin']}% | {r['old_band']}% -> {r['new_band']}% | {m(r['trade_price'])} ({r['trade_margin']}%) | {r['note']} |"
H = "| Item | Cost inc GST | Competitor | Price | Margin | Band | Trade price (margin) | Note |\n|---|---|---|---|---|---|---|---|\n"
top = lambda rs, k, n=25: H + "\n".join(line(r) for r in sorted(rs, key=k)[:n]) + "\n"
md = ["# Roberts Designs price list effective 18 Nov 2026: proposal\n",
 f"{len(rows)} live variants from Roberts ({len(byp)} products). {len(on)} are on the new list; {len(rows) - len(on)} are not and stay as they are. **Nothing has been changed in Shopify.**\n",
 "| What | Variants |\n|---|---|\n" + f"| Cost up | {len(cu)} |\n| Cost down | {len(cd)} |\n| Cost the same | {len(on) - len(cu) - len(cd)} |\n| Price up | {len(pu)} |\n| Price down | {len(pd)} |\n| Price the same | {len(on) - len(pu) - len(pd)} |\n"
 f"| Held at our floor because the competitor is cheaper | {sum(1 for r in on if r['note'])} |\n| Products changing trade band | {len(bc)} |\n",
 "## Biggest price rises\n", top(pu, lambda r: -r["price_change"]), "## Biggest price cuts\n", top(pd, lambda r: r["price_change"]),
 "## Held at our floor (competitor is cheaper than we can go)\n", top([r for r in on if r["note"]], lambda r: -r["new_price"], 200),
 "## Trade band changes\n", "| Product | Now | Proposed |\n|---|---|---|\n" + "\n".join(f"| {r['product']} | {r['old_band']}% | {r['new_band']}% |" for r in sorted(bc.values(), key=lambda r: r["product"])) + "\n",
 "## Not on the new list (unchanged)\n", "| Item | Price | Cost | Note |\n|---|---|---|---|\n" + "\n".join(f"| {nm(r)} | {m(r['old_price'])} | {m(r['old_cost']) if r['old_cost'] else 'none'} | {r['note']} |" for r in rows if not r["list_desc"]) + "\n",
 "Every variant: `roberts-price-list-2026-11-18.csv`.\n"]
open(os.path.join(HERE, "reports", "roberts-price-list-2026-11-18.md"), "w").write("\n".join(md))
print(f"{len(rows)} variants, on list {len(on)}; cost up {len(cu)} down {len(cd)}; price up {len(pu)} down {len(pd)}; floor-held {sum(1 for r in on if r['note'])}; band changes {len(bc)}")
