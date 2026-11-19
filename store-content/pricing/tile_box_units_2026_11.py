"""Tiles from 0.01 m2 units to one variant = one BOX (Gia's model), 19 Nov 2026.

Inputs (all by SKU):
  reports/tile-box-plan-2026-11-19/pages/p*.json   Shopify snapshot (products tagged m2-units, with band metafield)
  store-pricing-2026-10-03.csv                     master list: new_price ($/m2), cost ($/m2 inc GST), trade_price ($/m2)
  box-sizes-2026-11.csv                            supplier box data: sku,m2_per_box,pcs_per_box,kg_per_box  (UNKNOWN = blank)
Output: reports/tile-box-proposal-2026-11-19.csv (the owner's approval table). With "batches": box_batches/
  pl_NN.graphql (price list fixed prices per box, RUN FIRST), box_NN.graphql (variants + tag flip), inv_NN.graphql
  (inventory in boxes), rollback_NN.graphql. Batches refuse to build while any box size is UNKNOWN or a floor fails.
Rules: price per box = master $/m2 x m2/box; cost per box = master cost x m2/box; trade per box = master trade $/m2
x m2/box (today's whole-dollar trade price kept; band formula shown as an option only). Nothing is invented.
"""
import json, glob, csv, sys, os
from decimal import Decimal as D, ROUND_HALF_UP
C = D("0.01"); REP = "reports/tile-box-plan-2026-11-19"; LOC = "gid://shopify/Location/77786087487"
PRICE_LIST = "gid://shopify/PriceList/17250287679"; CAP = {"Tile": 15}; KG_M2 = {"Porcelain": D(22), "Ceramic": D(15)}

def box_row(m2_price, cost_m2, trade_m2, box):
    """All per-box figures from per-m2 figures. box is Decimal m2 per box, 2 dp."""
    assert box > 0 and box == box.quantize(C), box
    q = lambda x: (x * box).quantize(C, ROUND_HALF_UP)
    return q(m2_price), q(cost_m2), q(trade_m2)
assert box_row(D(55), D("35.75"), D(50), D("1.44")) == (D("79.20"), D("51.48"), D("72.00"))

master = {r["sku"]: r for r in csv.DictReader(open("store-pricing-2026-10-03.csv"))}
sizes = {r["sku"]: r for r in csv.DictReader(open("box-sizes-2026-11.csv"))} if os.path.exists("box-sizes-2026-11.csv") else {}
rows, seen = [], set()
for f in sorted(glob.glob(f"{REP}/pages/p*.json")):
    for p in json.load(open(f))["data"]["products"]["nodes"]:
        if p["id"] in seen or "Mosaic" in p["title"]: continue
        seen.add(p["id"]); band = int((p["band"] or {}).get("value") or 0)
        for v in p["variants"]["nodes"]:
            sku, m = v["sku"], master.get(v["sku"]); s = sizes.get(v["sku"], {})
            r = dict(product=p["title"], status=p["status"], variant=v["title"], sku=sku, variant_id=v["id"], product_id=p["id"],
                     inventory_item=v["inventoryItem"]["id"], band=band, flag=[])
            unit_price = D(v["price"])
            if not m: r["flag"].append("NOT IN MASTER LIST: no exact cost"); m2_price = unit_price * 100; cost_m2 = trade_m2 = None
            else:
                m2_price, cost_m2 = D(m["new_price"]), D(m["cost"]); trade_m2 = D(m["trade_price"]) if band else m2_price
                if m2_price != unit_price * 100 or m2_price != m2_price.to_integral_value(): r["flag"].append(f"MASTER/SHOPIFY MISMATCH {m2_price} vs {unit_price*100}")
            r.update(m2_price=m2_price, cost_m2=cost_m2, trade_m2_today=trade_m2, trade_m2_band_formula=(m2_price * (100 - band) / 100).quantize(C) if band else "")
            box = D(s["m2_per_box"]) if s.get("m2_per_box") else None
            r.update(m2_per_box=box or "UNKNOWN", pcs_per_box=s.get("pcs_per_box", ""), kg_per_box=s.get("kg_per_box", ""))
            r.update(old_unit_price=unit_price, old_stock_units=v["inventoryQuantity"], tracked=v["inventoryItem"]["tracked"])
            if box and cost_m2 is not None:
                pb, cb, tb = box_row(m2_price, cost_m2, trade_m2, box)
                kg = D(s["kg_per_box"]) if s.get("kg_per_box") else (KG_M2["Ceramic" if "Ceramic" in p["tags"] else "Porcelain"] * box).quantize(C)
                if not s.get("kg_per_box"): r["flag"].append("kg per box estimated")
                units = int(round(box * 100)); stock = v["inventoryQuantity"]
                r.update(price_per_box=pb, cost_per_box=cb, trade_per_box=tb, kg_per_box=kg,
                         margin_pct=round(float((pb - cb) / pb * 100), 1), trade_margin_pct=round(float((tb - cb) / tb * 100), 1),
                         eff_discount_pct=round(float((1 - tb / pb) * 100), 1),
                         new_stock_boxes=int(stock / units), stock_remainder_units=stock - int(stock / units) * units)
                if r["margin_pct"] < 25: r["flag"].append("UNDER PUBLIC FLOOR")
                if band and r["trade_margin_pct"] < 25: r["flag"].append("UNDER TRADE FLOOR")
                if band and r["eff_discount_pct"] > CAP["Tile"]: r["flag"].append("OVER BAND CAP")
                if stock < 0:  # owner, 19 Nov 2026: negative stock (past sales never received) resets to zero boxes
                    r.update(new_stock_boxes=0, stock_remainder_units=0); r["flag"].append(f"negative stock {stock} units reset to 0 boxes (owner 19 Nov)")
                if r["stock_remainder_units"]: r["flag"].append(f"part box in stock: {r['stock_remainder_units']} units")
                # a customer example line for the approval table: 3 m2 job
                import math; n = math.ceil(3 / float(box) - 1e-6); r["example_3m2"] = f"{n} box{'es' if n > 1 else ''} = ${pb * n:.2f} (today ${m2_price * 3:.2f})"
            r["flag"] = "; ".join(r["flag"]); rows.append(r)
cols = ["product", "status", "variant", "sku", "band", "m2_per_box", "pcs_per_box", "kg_per_box", "m2_price", "cost_m2", "trade_m2_today",
        "trade_m2_band_formula", "price_per_box", "cost_per_box", "trade_per_box", "margin_pct", "trade_margin_pct", "eff_discount_pct",
        "example_3m2", "old_unit_price", "old_stock_units", "new_stock_boxes", "stock_remainder_units", "tracked", "flag", "variant_id", "product_id", "inventory_item"]
with open(f"reports/tile-box-proposal-2026-11-19.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
unknown = [r["sku"] for r in rows if r["m2_per_box"] == "UNKNOWN"]; bad = [(r["sku"], r["flag"]) for r in rows if "FLOOR" in r["flag"] or "CAP" in r["flag"] or "MISMATCH" in r["flag"] or "MASTER" in r["flag"]]
print(len(rows), "variants,", len(seen), "products;", len(unknown), "box size UNKNOWN;", len(bad), "flagged")
for b in bad: print("  ", *b)

if len(sys.argv) > 1 and sys.argv[1] == "batches":
    assert not bad, f"fix these first: {bad}"
    # a product flips to box mode as a whole (the tag is per product), so hold back any product with a variant still UNKNOWN
    held = {r["product_id"] for r in rows if r["m2_per_box"] == "UNKNOWN"}
    for pid in held: print("  held back (box size UNKNOWN on a variant):", next(r["product"] for r in rows if r["product_id"] == pid))
    rows = [r for r in rows if r["product_id"] not in held]
    print(len(rows), "variants in the batches")
    out = "box_batches"; os.makedirs(out, exist_ok=True)
    def chunk(parts, head, tail, name, limit=15500):
        reqs, cur = [], []
        for part in parts:
            if len(head + " ".join(cur + [part]) + tail) > limit: reqs.append(head + " ".join(cur) + tail); cur = []
            cur.append(part)
        reqs.append(head + " ".join(cur) + tail)
        for n, r in enumerate(reqs, 1): open(f"{out}/{name}_{n:02d}.graphql", "w").write(r.replace("%02d", f"{n:02d}") if "%02d" in r else r)
        return len(reqs)
    # 1. price list first (never a window where the fixed price is per unit and the variant price is per box)
    pl = ['{variantId: "%s", price: {amount: "%s", currencyCode: AUD}, compareAtPrice: {amount: "%s", currencyCode: AUD}}' % (r["variant_id"], r["trade_per_box"], r["price_per_box"]) for r in rows if r["band"]]
    n_pl = chunk(pl, 'mutation { priceListFixedPricesAdd(priceListId: "%s", prices: [' % PRICE_LIST, ']) { prices { variant { id } } userErrors { field message code } } }', "pl")
    # 2. variants + tag flip, one product per alias group
    by_p = {}
    for r in rows: by_p.setdefault(r["product_id"], []).append(r)
    parts, back = [], []
    for i, (pid, rs) in enumerate(by_p.items()):
        vs = ",".join('{id:"%s",price:"%s",showUnitPrice:true,unitPriceMeasurement:{quantityValue:%s,quantityUnit:M2,referenceValue:1,referenceUnit:M2},inventoryItem:{cost:"%s",measurement:{weight:{value:%s,unit:KILOGRAMS}}}}'
                      % (r["variant_id"], r["price_per_box"], r["m2_per_box"], r["cost_per_box"], r["kg_per_box"]) for r in rs)
        parts.append('p%d: productVariantsBulkUpdate(productId:"%s",variants:[%s]){userErrors{field message}} t%d: tagsAdd(id:"%s",tags:["box-units"]){userErrors{message}} u%d: tagsRemove(id:"%s",tags:["m2-units"]){userErrors{message}}' % (i, pid, vs, i, pid, i, pid))
        vb = ",".join('{id:"%s",price:"%s",showUnitPrice:true,unitPriceMeasurement:{quantityValue:0.01,quantityUnit:M2,referenceValue:1,referenceUnit:M2},inventoryItem:{cost:"%s",measurement:{weight:{value:%s,unit:KILOGRAMS}}}}'
                      % (r["variant_id"], r["old_unit_price"], (r["cost_m2"] / 100).quantize(C), (r["kg_per_box"] / r["m2_per_box"] / 100).quantize(D("0.0001"))) for r in rs)
        back.append('p%d: productVariantsBulkUpdate(productId:"%s",variants:[%s]){userErrors{field message}} t%d: tagsAdd(id:"%s",tags:["m2-units"]){userErrors{message}} u%d: tagsRemove(id:"%s",tags:["box-units"]){userErrors{message}}' % (i, pid, vb, i, pid, i, pid))
    n_box = chunk(parts, "mutation{", "}", "box"); n_back = chunk(back, "mutation{", "}", "rollback")
    # 3. inventory in boxes, guarded by the snapshot quantity so a sale in between fails loudly
    inv = ['{inventoryItemId: "%s", locationId: "%s", quantity: %d, changeFromQuantity: %d}' % (r["inventory_item"], LOC, r["new_stock_boxes"], r["old_stock_units"]) for r in rows if r["tracked"]]
    n_inv = chunk(inv, 'mutation { inventorySetQuantities(input: {reason: "correction", name: "available", quantities: [', ']}) @idempotent(key: "ets-box-units-inv-%02d") { userErrors { field message code } } }', "inv", 15000)
    print(f"batches: {n_pl} price-list, {n_box} variant, {n_inv} inventory, {n_back} rollback files in {out}/ (run in that order; rollback = variants back to 0.01 units, then rerun both trade scripts)")
