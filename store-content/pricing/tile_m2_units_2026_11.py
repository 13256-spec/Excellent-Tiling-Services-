"""Option 2: tiles sold in 0.01 m2 units. Price per m2 must be a whole dollar so the unit price is whole cents."""
import json, sys, csv, math
from decimal import Decimal as D, ROUND_HALF_UP, ROUND_CEILING
C=D("0.01")
def plan(price, cost, band):
    new = D(math.floor(price))                     # round DOWN to whole dollar (playbook: public rounds down)
    if cost and (new - cost) / new < D("0.25"):    # never under the public floor
        new = D(math.ceil(price))
    unit = (new / 100).quantize(C)
    tunit = (unit * (100 - band) / 100).quantize(C, ROUND_CEILING) if band else unit  # ceiling: discount never above the band cap
    return new, unit, tunit
assert plan(D("55.20"), D("35.75"), 10) == (D(55), D("0.55"), D("0.50"))
rows=[]
for p in json.load(open(sys.argv[1]))["data"]["products"]["nodes"]:
    if "Mosaic" in p["title"]: continue
    band=int((p["band"] or {}).get("value") or 0)
    for v in p["variants"]["nodes"]:
        price=D(v["price"]); c=v["inventoryItem"]["unitCost"]; cost=D(c["amount"]) if c else None
        new,unit,tunit=plan(price,cost,band)
        cu = cost/100 if cost else None
        rows.append(dict(product=p["title"],status=p["status"],variant=v["title"],sku=v["sku"],variant_id=v["id"],inventory_item=None,
            band=band,cost_m2=cost,old_m2=price,new_m2=new,change=new-price,unit_price=unit,
            public_margin=round(float((new-cost)/new*100),1) if cost else "",
            trade_unit=tunit,trade_m2=tunit*100,eff_disc=round(float((1-tunit/unit)*100),1),
            trade_margin=round(float((tunit-cu)/tunit*100),1) if cost else ""))
w=csv.DictWriter(open("tile-m2-proposal.csv","w"),fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(len(rows),"variants,",len({r['product'] for r in rows}),"products")
print("missing cost:",[r['sku'] for r in rows if r['cost_m2'] is None])
print("trade margin <25:",[(r['sku'],r['trade_margin']) for r in rows if r['trade_margin']!="" and r['trade_margin']<25])
print("eff disc > 15 (cap):",[(r['sku'],r['eff_disc']) for r in rows if r['eff_disc']>15])
print("rounded UP for floor:",[(r['sku'],str(r['old_m2']),str(r['new_m2'])) for r in rows if r['change']>0])
from collections import Counter
print(Counter((str(r['old_m2']),str(r['new_m2']),r['band'],str(r['trade_m2'])) for r in rows))
