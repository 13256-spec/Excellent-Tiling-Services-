"""BAT / Raimondi fix from the May 2026 price books (owner, 23 Oct 2026).
Matched SKUs: cost = book NET ex GST x 1.1; price raised to the floor (cost x 1.25, up to 5c) where under 20% margin ex GST,
otherwise left alone (no competitor price on file). Trade band per product = deepest of 25/20/15/10/5 that keeps every
variant above the floor. Writes: bat-fix-2026-10-23.csv (every matched variant), pm*.graphql (price+cost per product),
mf*.graphql (ets.trade_band), coll-moves.json. Unmatched variants are listed in bat-unmatched-2026-10-23.csv."""
import csv, json, math, os, collections
os.chdir(os.path.dirname(os.path.abspath(__file__)))
BANDS = [25, 20, 15, 10, 5, 0]
def up(x): return math.ceil(round(x / 0.05, 6)) * 0.05
def margin(price, cost): return (price - cost) / price * 100 if price else 0  # both inc GST = margin ex GST
L = [json.loads(l) for l in open("bat-products.jsonl")]
P = {l["id"]: l for l in L if "id" in l and "/Product/" in l["id"]}
V = [l for l in L if "id" in l and "/ProductVariant/" in l["id"]]
B = {r["code"]: r for r in csv.DictReader(open("bat-price-books-2026-05.csv"))}
rows, un = [], []
for v in V:
    p = P[v["__parentId"]]; sku = (v["sku"] or "").strip().upper(); b = B.get(sku)
    old_cost = float(v["inventoryItem"]["unitCost"]["amount"]) if v["inventoryItem"]["unitCost"] else None
    price = float(v["price"]); band = int((p.get("tradeBand") or {}).get("value") or 0)
    if not b:
        un.append([v["sku"], p["vendor"], p["title"], v["title"], price, old_cost, p["status"]]); continue
    cost = round(float(b["net_ex_gst"]) * 1.1 + 1e-9, 2); floor = round(up(cost * 1.25), 2)
    new_price = max(price, floor) if price > 0 else floor
    rows.append(dict(sku=v["sku"], vendor=p["vendor"], product=p["title"], variant=v["title"], status=p["status"], pid=p["id"], vid=v["id"],
                     book=b["book"], net_ex_gst=b["net_ex_gst"], old_cost=old_cost, new_cost=cost, old_price=price, floor=floor,
                     new_price=new_price, price_change=round(new_price - price, 2), old_margin=round(margin(price, cost), 1),
                     new_margin=round(margin(new_price, cost), 1), band=band))
byp = collections.defaultdict(list)
for r in rows: byp[r["pid"]].append(r)
for pid, rs in byp.items():
    all_matched = len(rs) == sum(1 for v in V if v["__parentId"] == pid)
    rec = next((b for b in BANDS if all(r["new_price"] * (1 - b / 100) >= r["floor"] - 0.005 for r in rs)), 0) if all_matched else rs[0]["band"]
    for r in rs: r["rec_band"] = rec; r["all_variants_matched"] = all_matched
with open("bat-fix-2026-10-23.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
with open("bat-unmatched-2026-10-23.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["sku", "vendor", "product", "variant", "price", "cost", "status"]); w.writerows(un)
# price + cost batches
batches, cur, i = [], [], 0
for pid, rs in byp.items():
    for j in range(0, len(rs), 40):
        vs = ",".join('{id:"%s",price:"%.2f",inventoryItem:{cost:"%.2f"}}' % (r["vid"], r["new_price"], r["new_cost"]) for r in rs[j:j + 40])
        cur.append('p%d: productVariantsBulkUpdate(productId:"%s", variants:[%s]) { productVariants { id price } userErrors { field message } }' % (i, pid, vs)); i += 1
        if sum(len(c) for c in cur) > 11000: batches.append("mutation { " + " ".join(cur) + " }"); cur = []
if cur: batches.append("mutation { " + " ".join(cur) + " }")
for k, b in enumerate(batches): open(f"pm{k}.graphql", "w").write(b)
moves = {pid: (rs[0]["band"], rs[0]["rec_band"]) for pid, rs in byp.items() if rs[0]["rec_band"] != rs[0]["band"]}
mf = ['{ownerId:"%s",namespace:"ets",key:"trade_band",type:"number_integer",value:"%d"}' % (pid, b) for pid, (a, b) in moves.items()]
mfb = ["mutation { metafieldsSet(metafields:[%s]) { metafields { ownerType } userErrors { field message } } }" % ",".join(mf[k:k + 25]) for k in range(0, len(mf), 25)]
for k, b in enumerate(mfb): open(f"mf{k}.graphql", "w").write(b)
out = collections.defaultdict(list); into = collections.defaultdict(list)
for pid, (a, b) in moves.items():
    if a: out[a].append(pid)
    if b: into[b].append(pid)
json.dump({"out": out, "into": into}, open("coll-moves.json", "w"))
raised = [r for r in rows if r["price_change"] > 0]
print(f"matched {len(rows)} variants on {len(byp)} products; unmatched {len(un)}; cost changes {sum(1 for r in rows if r['old_cost'] is None or abs(r['old_cost'] - r['new_cost']) > 0.005)}")
print(f"prices raised to floor: {len(raised)} (max x{max((r['new_price'] / r['old_price'] for r in raised if r['old_price']), default=1):.2f}); unchanged {len(rows) - len(raised)}")
print(f"price batches {len(batches)} {[len(b) for b in batches]}; band changes {len(moves)} {collections.Counter(f'{a}->{b}' for a, b in moves.values()).most_common(6)}; metafield batches {len(mfb)}")
print("out:", {k: len(v) for k, v in out.items()}, "into:", {k: len(v) for k, v in into.items()})
assert all(r["new_price"] >= r["floor"] - 0.005 for r in rows)
