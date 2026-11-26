"""Turn reports/roberts-price-list-2026-11-18.csv (approved by the owner 26 Nov 2026) into Admin GraphQL requests.

Usage: roberts_apply_2026_11.py OUT_DIR   -> OUT_DIR/NN-kind.graphql, each under 16,000 characters, to run with the
Shopify MCP graphql_mutation tool: prices and costs, trade_band metafields, trade-list collection moves, B2B price list
fixed prices (and deletes where the band is now 0), trade price record metafields. Same maths as
b2b_price_list_2026_11.py and trade_price_metafields_2026_11.py (hardware: to the cent, half up).
"""
import csv, json, os, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); out = sys.argv[1]; os.makedirs(out, exist_ok=True)
PL = "gid://shopify/PriceList/17250287679"
COL = {5: "gid://shopify/Collection/301904298047", 10: "gid://shopify/Collection/301904330815", 15: "gid://shopify/Collection/301904363583", 20: "gid://shopify/Collection/301904396351"}
R = list(csv.DictReader(open(os.path.join(HERE, "reports", "roberts-price-list-2026-11-18.csv")))); f = float
byp = collections.defaultdict(list)
for r in R: byp[r["pid"]].append(r)
files = []
def pack(kind, parts, wrap=lambda body: "mutation {" + body + "}"):
    cur = []
    def flush():
        if cur: files.append((kind, wrap(" ".join(f"a{i}: {p}" for i, p in enumerate(cur)))))
    for p in parts:
        if len(wrap(" ".join(f"a{i}: {x}" for i, x in enumerate(cur + [p])))) > 15500: flush(); cur.clear()
        cur.append(p)
    flush()
chunks = lambda xs, n: [xs[i:i + n] for i in range(0, len(xs), n)]
# 1 prices and costs: only variants whose price or cost changes
parts = []
for pid, rs in byp.items():
    vs = [r for r in rs if abs(f(r["new_price"]) - f(r["old_price"])) > 0.004 or (r["old_cost"] and abs(f(r["new_cost"]) - f(r["old_cost"])) > 0.004)]
    for c in chunks(vs, 100):
        parts.append('productVariantsBulkUpdate(productId: "%s", variants: [%s]) { userErrors { field message } }' % (pid, ", ".join(
            '{id: "%s", price: "%.2f", inventoryItem: {cost: "%.2f"}}' % (r["vid"], f(r["new_price"]), f(r["new_cost"])) for r in c)))
pack("prices", parts)
# 2 bands
moved = [rs[0] for rs in byp.values() if rs[0]["new_band"] != rs[0]["old_band"]]
pack("bands", ['metafieldsSet(metafields: [%s]) { userErrors { field message } }' % ", ".join(
    '{ownerId: "%s", namespace: "ets", key: "trade_band", type: "number_integer", value: "%s"}' % (r["pid"], r["new_band"]) for r in c) for c in chunks(moved, 25)])
# productUpdate collectionsToJoin / collectionsToLeave (collectionAddProducts / collectionRemoveProducts are deprecated in 2026-10)
parts = ['productUpdate(product: {id: "%s"%s%s}) { userErrors { field message } }' % (r["pid"],
    ', collectionsToJoin: ["%s"]' % COL[int(r["new_band"])] if int(r["new_band"]) else "", ', collectionsToLeave: ["%s"]' % COL[int(r["old_band"])] if int(r["old_band"]) else "") for r in moved]
pack("collections", parts)
# 3 B2B price list: fixed price + compare-at for every banded variant whose public or trade price changed; delete where band is now 0
ch = lambda r: abs(f(r["new_price"]) - f(r["old_price"])) > 0.004 or r["new_band"] != r["old_band"]
fixed = [r for r in R if int(r["new_band"]) and ch(r)]
pack("pricelist", ['priceListFixedPricesAdd(priceListId: "%s", prices: [%s]) { userErrors { field message code } }' % (PL, ", ".join(
    '{variantId: "%s", price: {amount: "%.2f", currencyCode: AUD}, compareAtPrice: {amount: "%.2f", currencyCode: AUD}}' % (r["vid"], f(r["trade_price"]), f(r["new_price"])) for r in c)) for c in chunks(fixed, 80)])
gone = [r["vid"] for r in R if not int(r["new_band"]) and int(r["old_band"])]
if gone: pack("pricelist-delete", ['priceListFixedPricesDelete(priceListId: "%s", variantIds: %s) { deletedFixedPriceVariantIds userErrors { field message code } }' % (PL, json.dumps(gone))])
# 4 records: custom.trade_price per variant, ets.trade_price per product (band 0: left as they are, the theme reads the band)
mf = ['{ownerId: "%s", namespace: "custom", key: "trade_price", type: "number_decimal", value: "%.2f"}' % (r["vid"], f(r["trade_price"])) for r in fixed]
for pid, rs in byp.items():
    b = int(rs[0]["new_band"])
    if not b or not any(ch(r) for r in rs): continue
    lo, hi = min(f(r["trade_price"]) for r in rs), max(f(r["trade_price"]) for r in rs)
    txt = f"${lo:,.2f}" if lo == hi else f"${lo:,.2f} – ${hi:,.2f}"
    mf.append('{ownerId: "%s", namespace: "ets", key: "trade_price", type: "single_line_text_field", value: "%s (%d%% off)"}' % (pid, txt, b))
pack("records", ['metafieldsSet(metafields: [%s]) { userErrors { field message } }' % ", ".join(c) for c in chunks(mf, 25)])
for i, (k, q) in enumerate(files, 1):
    assert len(q) < 16000; open(os.path.join(out, f"{i:02d}-{k}.graphql"), "w").write(q)
print(len(files), "requests:", dict(collections.Counter(k for k, _ in files)), "| variants priced", sum(q.count("price:") for k, q in files if k == "prices"), "| band moves", len(moved), "| fixed prices", len(fixed), "| deletes", len(gone), "| metafields", len(mf))
