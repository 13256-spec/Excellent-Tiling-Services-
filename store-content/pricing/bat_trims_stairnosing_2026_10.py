"""Second trims pass: stairnosing SKUs = bar code + rubber-insert colour (BSN-8-3-MF-BL = BSN-8-3-MF bar + RSI-BL insert).
Cost = (bar NET + insert NET) x 1.1. Match by dropping the trailing segment; the dropped segment picks the RSI-<colour> insert.
Same floor/band rules as bat_fix.py."""
import csv, json, math, os, collections
os.chdir(os.path.dirname(os.path.abspath(__file__)))
BANDS = [25, 20, 15, 10, 5, 0]
def up(x): return math.ceil(round(x / 0.05, 6)) * 0.05
def margin(price, cost): return (price - cost) / price * 100 if price else 0
L = [json.loads(l) for l in open("bat-products.jsonl")]
P = {l["id"]: l for l in L if "id" in l and "/Product/" in l["id"]}
V = [l for l in L if "id" in l and "/ProductVariant/" in l["id"]]
B = {r["code"].upper(): r for r in csv.DictReader(open("bat-price-books-2026-05.csv"))}
done = {r["sku"].upper() for r in csv.DictReader(open("bat-fix-2026-10-23.csv"))} | {r["sku"].upper() for r in csv.DictReader(open("../bat-fix-2026-10-23.csv"))}
def strip_match(sku):
    parts = sku.split("-")
    for k in range(len(parts) - 1, 1, -1):
        c = "-".join(parts[:k]); ins = "RSI-" + "-".join(parts[k:])
        if c in B and ins in B: return c, ins
rows, un = [], []
for v in V:
    p = P[v["__parentId"]]; sku = (v["sku"] or "").strip().upper()
    if sku in done: continue
    hit = strip_match(sku) if sku else None
    old_cost = float(v["inventoryItem"]["unitCost"]["amount"]) if v["inventoryItem"]["unitCost"] else None
    price = float(v["price"]); band = int((p.get("tradeBand") or {}).get("value") or 0)
    if not hit:
        un.append([v["sku"], p["vendor"], p["title"], v["title"], price, old_cost, p["status"]]); continue
    code, ins = hit; b = B[code]; net = round(float(b["net_ex_gst"]) + float(B[ins]["net_ex_gst"]), 2)
    cost = round(net * 1.1 + 1e-9, 2); floor = round(up(cost * 1.25), 2)
    new_price = max(price, floor) if price > 0 else floor
    rows.append(dict(sku=v["sku"], vendor=p["vendor"], product=p["title"], variant=v["title"], status=p["status"], pid=p["id"], vid=v["id"],
                     book=b["book"] + " (" + code + " + " + ins + ")", net_ex_gst=net, old_cost=old_cost, new_cost=cost, old_price=price, floor=floor,
                     new_price=new_price, price_change=round(new_price - price, 2), old_margin=round(margin(price, cost), 1),
                     new_margin=round(margin(new_price, cost), 1), band=band))
byp = collections.defaultdict(list)
for r in rows: byp[r["pid"]].append(r)
for pid, rs in byp.items():
    matched_skus = {r["sku"].upper() for r in rs} | done
    all_matched = all((v["sku"] or "").upper() in matched_skus for v in V if v["__parentId"] == pid)
    rec = next((b for b in BANDS if all(r["new_price"] * (1 - b / 100) >= r["floor"] - 0.005 for r in rs)), 0) if all_matched else rs[0]["band"]
    for r in rs: r["rec_band"] = rec; r["all_variants_matched"] = all_matched
with open("bsn-fix-2026-10-24.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
with open("bat-still-unmatched-2026-10-24.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["sku", "vendor", "product", "variant", "price", "cost", "status"]); w.writerows(un)
batches, cur, i = [], [], 0
for pid, rs in byp.items():
    for j in range(0, len(rs), 40):
        vs = ",".join('{id:"%s",price:"%.2f",inventoryItem:{cost:"%.2f"}}' % (r["vid"], r["new_price"], r["new_cost"]) for r in rs[j:j + 40])
        cur.append('b%d: productVariantsBulkUpdate(productId:"%s", variants:[%s]) { productVariants { id price } userErrors { field message } }' % (i, pid, vs)); i += 1
        if sum(len(c) for c in cur) > 11000: batches.append("mutation { " + " ".join(cur) + " }"); cur = []
if cur: batches.append("mutation { " + " ".join(cur) + " }")
for k, b in enumerate(batches): open(f"bsn{k}.graphql", "w").write(b)
moves = {pid: (rs[0]["band"], rs[0]["rec_band"]) for pid, rs in byp.items() if rs[0]["rec_band"] != rs[0]["band"]}
raised = [r for r in rows if r["price_change"] > 0]
print(f"matched {len(rows)} on {len(byp)} products; raised {len(raised)}; batches {len(batches)} {[len(b) for b in batches]}; band moves {moves}")
print(f"still unmatched {len(un)}:", collections.Counter((r[6], r[1]) for r in un))
for r in rows[:6]: print(r["sku"], r["book"], r["old_cost"], r["new_cost"], r["old_price"], r["floor"], r["new_margin"], r["band"], r["rec_band"])
for r in un: print("  UN", r)
