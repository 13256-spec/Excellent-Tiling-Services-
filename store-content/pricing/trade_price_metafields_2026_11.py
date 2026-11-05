"""Write the trade price into Shopify metafields (5 Nov 2026).

Input: pages/p*.json, the saved pages of this Admin GraphQL query (100 products a page, follow endCursor):
  products { id title status tags band: metafield(namespace:"ets",key:"trade_band"){value}
             variants(first:100){ nodes { id title sku price } } }
Output: reqNN.graphql, one metafieldsSet request each (aliases of 25, under 16k chars) to run with the
Shopify MCP graphql_mutation tool, and trade-price-metafields.csv (the report).

Variant  custom.trade_price (number_decimal)      = price x (1 - ets.trade_band/100), to the cent, half up.
Product  ets.trade_price   (single_line_text)      = "$x (N% off)" or "$lo - $hi (N% off)".
Products with band 0 are skipped. Re-run after any price or band change (playbook step 4).
"""

import json, glob
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING
C = Decimal("0.01")
rows, mfs, seen = [], [], set()
for f in sorted(glob.glob("pages/p*.json")):
    for p in json.load(open(f))["data"]["products"]["nodes"]:
        if p["id"] in seen: continue
        seen.add(p["id"])
        band = int((p["band"] or {}).get("value") or 0)
        if not band: continue
        tps = []
        m2 = "m2-units" in p.get("tags", [])   # tiles sold per 0.01 m2: same rounding as b2b_price_list (up)
        for v in p["variants"]["nodes"]:
            price = Decimal(v["price"]); tp = (price * (100 - band) / 100).quantize(C, ROUND_CEILING if m2 else ROUND_HALF_UP)
            tps.append(tp)
            mfs.append({"ownerId": v["id"], "namespace": "custom", "key": "trade_price", "type": "number_decimal", "value": str(tp)})
            rows.append((p["title"], v["title"], v.get("sku",""), p["status"], str(price), band, str(tp)))
        lo, hi = min(tps), max(tps)
        if m2: lo, hi = lo * 100, hi * 100       # show the per-m2 trade price in admin
        txt = f"${lo:,.2f}" if lo == hi else f"${lo:,.2f} – ${hi:,.2f}"
        if m2: txt += " per m²"
        mfs.append({"ownerId": p["id"], "namespace": "ets", "key": "trade_price", "type": "single_line_text_field", "value": f"{txt} ({band}% off)"})
assert all(Decimal(m["value"]) > 0 for m in mfs if m["key"] == "trade_price" and m["namespace"] == "custom")
import csv
with open("trade-price-metafields.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["product", "variant", "sku", "status", "price", "trade_band", "trade_price"]); w.writerows(rows)
# chunk: 25 per metafieldsSet, several aliases per request, < 16k chars
chunks = [mfs[i:i+25] for i in range(0, len(mfs), 25)]
reqs, cur = [], []
def render(groups):
    return "mutation {" + " ".join(f"m{i}: metafieldsSet(metafields: {json.dumps(g).replace(chr(34)+'ownerId'+chr(34), 'ownerId').replace(chr(34)+'namespace'+chr(34),'namespace').replace(chr(34)+'key'+chr(34),'key').replace(chr(34)+'type'+chr(34),'type').replace(chr(34)+'value'+chr(34),'value')}) {{ userErrors {{ field message }} metafields {{ id }} }}" for i, g in enumerate(groups)) + " }"
for c in chunks:
    if len(render(cur + [c])) > 16000:
        reqs.append(render(cur)); cur = []
    cur.append(c)
if cur: reqs.append(render(cur))
for i, r in enumerate(reqs, 1):
    open(f"req{i:02d}.graphql", "w").write(r)
print(len(seen), "products read;", sum(1 for m in mfs if m["namespace"]=="ets"), "trade products;", sum(1 for m in mfs if m["namespace"]=="custom"), "variants;", len(reqs), "requests")
