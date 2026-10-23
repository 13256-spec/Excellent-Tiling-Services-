"""Audit selling prices of Roberts-supplied variants. Rules (PRICING-PLAYBOOK.md + owner 23 Oct: make money, a bit under competitors):
floor = cost(inc GST) x 1.25 (20% margin ex GST); target = 5% under B&B if they sell it, else 10% under Roberts retail; never below floor.
Trade: price x (1 - band) must also be >= floor. Writes roberts-price-audit-2026-10-23.{md,csv}. Changes nothing."""
import csv, json, math, sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from reprice_2026_10 import BB_MATCH
MARKUP, BANDS = 1.25, [25, 20, 15, 10, 5, 0]
def dn(x): return math.floor(round(x / 0.05, 6)) * 0.05
def up(x): return math.ceil(round(x / 0.05, 6)) * 0.05
def margin(price, cost): return (price - cost) / price * 100 if price else 0  # price and cost both inc GST, so this is the margin ex GST
L = [json.loads(l) for l in open("products.jsonl")]
P = {l["id"]: l for l in L if "id" in l and "/Product/" in l["id"]}
V = [l for l in L if "id" in l and "/ProductVariant/" in l["id"]]
pub = {r["sku"].upper(): float(r["public_inc_gst"]) for r in csv.DictReader(open("roberts-public.csv")) if r["sku"]}
sep = {r["sku"].upper(): r for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "supplier-sync", "roberts-designs-pricing.csv")))}
bb = {}
for f in sorted(os.listdir("bb")):
    for p in json.load(open(f"bb/{f}"))["products"]: bb[p["title"]] = float(p["variants"][0]["price"])
rows = []
for v in V:
    p = P[v["__parentId"]]; price = float(v["price"]); cost = float(v["inventoryItem"]["unitCost"]["amount"]); sku = v["sku"].upper()
    name = p["title"] + ("" if v["title"] == "Default Title" else " / " + v["title"])
    floor = up(cost * MARKUP)
    key = name if name in BB_MATCH else p["title"]
    # cheapest known competitor wins: B&B live (5% under), Sep market match Tile Mart/National Tiles etc. (3% under), Roberts retail (10% under)
    s = sep.get(sku, {}); cands = []
    if key in BB_MATCH and BB_MATCH[key] in bb: cands.append((bb[BB_MATCH[key]], "B&B", 0.95))
    if s.get("market_source", "roberts-list") != "roberts-list" and s.get("market_price_used"):
        cands.append((float(s["market_price_used"]), s["market_source"].replace("web:", "").replace("match:", "") + " (Sep price)", 0.97))
    if sku in pub: cands.append((pub[sku], "Roberts retail", 0.90))
    comp, who, target = None, "", None
    if cands: comp, who, k = min(cands); target = dn(comp * k)
    web = s.get("market_price_used") if s.get("market_source", "").startswith("web:") else ""
    proposed = max(floor, target) if target is not None else max(floor, price)
    if target is not None and target < floor: note = "competitor below our floor: hold at floor"
    elif target is None: note = "no competitor price"
    else: note = ""
    band = int((p.get("tradeBand") or {}).get("value") or 0)
    rows.append(dict(sku=v["sku"], vendor=p["vendor"], product=p["title"], variant=v["title"], pid=p["id"], vid=v["id"], stock=v["inventoryQuantity"],
        price=price, cost=cost, margin=round(margin(price, cost), 1), floor=round(floor, 2), competitor=who, comp_price=comp, target=target,
        sep_web_market=web, proposed=round(proposed, 2), change=round(proposed - price, 2), band=band, trade_price=round(price * (1 - band / 100), 2),
        trade_margin=round(margin(price * (1 - band / 100), cost), 1), note=note))
# recommended band per product at proposed prices
byp = collections.defaultdict(list)
for r in rows: byp[r["pid"]].append(r)
for pid, rs in byp.items():
    rec = next((b for b in BANDS if all(r["proposed"] * (1 - b / 100) >= r["floor"] - 0.005 for r in rs)), 0)
    for r in rs: r["rec_band"] = rec
# buckets
below_cost = [r for r in rows if r["price"] < r["cost"]]
below_floor = [r for r in rows if r["price"] < r["floor"] - 0.005 and r["price"] >= r["cost"]]
above_comp = [r for r in rows if r["comp_price"] and r["price"] > r["comp_price"] + 0.005 and r["price"] >= r["floor"] - 0.005]
leaving_money = [r for r in rows if r["target"] is not None and r["price"] >= r["floor"] - 0.005 and r["price"] <= r["comp_price"] and r["proposed"] - r["price"] >= max(1, 0.05 * r["price"])]
trade_breach = [r for r in rows if r["band"] and r["trade_price"] < r["floor"] - 0.005 and r["price"] >= r["floor"] - 0.005]
band_change = {r["pid"]: r for r in rows if r["rec_band"] != r["band"]}
ok = len(rows) - len(below_cost) - len(below_floor) - len(above_comp) - len(leaving_money)
fn = list(rows[0].keys())
w = csv.DictWriter(open("roberts-price-audit-2026-10-23.csv", "w", newline=""), fieldnames=fn); w.writeheader(); w.writerows(rows)
def money(x): return f"${x:,.2f}" if x not in (None, "") else "–"
def table(head, rs, fmt):
    return head + "\n|" + "---|" * head.count("|", 1) + "\n" + "\n".join(fmt(r) for r in rs) + "\n" if rs else "None.\n"
def nm(r): return r["product"] + ("" if r["variant"] == "Default Title" else " / " + r["variant"])
def comp(r): return f"{r['competitor']} {money(r['comp_price'])}" if r["competitor"] else "–"
std = lambda r: f"| {nm(r)} | {money(r['price'])} | {money(r['cost'])} | {r['margin']}% | {comp(r)} | {money(r['proposed'])} | {r['band']}% | {r['note']} |"
HEAD = "| Item | Our price | Cost inc GST | Margin | Competitor | Proposed | Trade band | Note |"
md = [f"# Roberts Designs selling-price audit – 23 Oct 2026\n",
f"{len(rows)} variants on {len(byp)} products (vendors Roberts Designs, Maxisil, Sigma, Siri, Baron, Barwalt). Costs are today's trade prices inc GST. "
f"Competitor = the cheapest known seller: B&B Hardware live price ({sum(1 for r in rows if r['competitor']=='B&B')} variants), the Tile Mart / National Tiles / Port Kembla / Western Distributors / Builders Centre price recorded in September ({sum(1 for r in rows if 'Sep price' in r['competitor'])} variants, worth a re-check), or Roberts' own retail price today ({sum(1 for r in rows if r['competitor']=='Roberts retail')} variants). "
"Rule: a little under the competitor (5% under B&B, 3% under the September market price, 10% under Roberts retail) but never under the profit floor (cost × 1.25 = 20% margin ex GST). Nothing was changed.\n",
"| Bucket | Variants |\n|---|---|\n"
f"| Selling below cost | {len(below_cost)} |\n| Above cost but below the 20% floor | {len(below_floor)} |\n| Dearer than the competitor | {len(above_comp)} |\n"
f"| Leaving money on the table (more than 5% or $1 under the target) | {len(leaving_money)} |\n| Priced right | {ok} |\n| Trade price below the floor | {len(trade_breach)} |\n| Products whose trade band should change | {len(band_change)} |\n",
"## 1. Selling below cost (raise now)\n", table(HEAD, sorted(below_cost, key=lambda r: r["margin"]), std),
"## 2. Below the 20% profit floor (raise to the floor, or to just under the competitor if that is higher)\n", table(HEAD, sorted(below_floor, key=lambda r: r["margin"]), std),
"## 3. Dearer than the competitor (drop to just under them, floor allowing)\n", table(HEAD, sorted(above_comp, key=lambda r: r["price"] - r["comp_price"], reverse=True), std),
"## 4. Leaving money on the table (we are well under the competitor; raise to just under them)\n", table(HEAD, sorted(leaving_money, key=lambda r: r["change"], reverse=True), std),
"## 5. Trade price below the floor at the current band\n", table("| Item | Our price | Band | Trade price | Floor | Recommended band |", trade_breach,
    lambda r: f"| {nm(r)} | {money(r['price'])} | {r['band']}% | {money(r['trade_price'])} | {money(r['floor'])} | {r['rec_band']}% |"),
"## 6. Trade band changes at the proposed prices (deepest of 25/20/15/10/5 that keeps every variant above the floor)\n",
 table("| Product | Now | Recommended |", sorted(band_change.values(), key=lambda r: r["product"]), lambda r: f"| {r['product']} | {r['band']}% | {r['rec_band']}% |"),
"Full detail per variant: `roberts-price-audit-2026-10-23.csv` (proposed price, change, target, Sep web market price where one was recorded).\n"]
open("roberts-price-audit-2026-10-23.md", "w").write("\n".join(md))
tot = sum(r["change"] for r in rows); print(f"below cost {len(below_cost)}, below floor {len(below_floor)}, above comp {len(above_comp)}, leaving money {len(leaving_money)}, trade breach {len(trade_breach)}, band changes {len(band_change)}, no comp {sum(1 for r in rows if not r['competitor'])}")
assert all(r["proposed"] >= r["floor"] - 0.005 for r in rows)
