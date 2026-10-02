"""Eternity Tiles price list effective 5 Oct 2026 -> our tile costs and public prices.

Cost recorded in Shopify = Eternity "non pallet" price ex GST (what we pay per m2 on a normal
order). Pallet and mixed 3+ pallet prices are kept here for quoting bigger jobs.

Public price = 15% under Eternity's RRP (incl. GST), rounded down to 10c, so we sit below
Eternity's own shop and WA stockists that sell at RRP. Trade accounts then get a further
discount (15% off public keeps trade about 24-27% above cost). Every public price must stay
at least 25% above cost incl. GST. Approved by the owner on 2 Oct 2026 ("option B").

Usage: eternity_2026_10.py current.json out.csv
  current.json: [{variant_id, product, variant, sku, price}] from Shopify
"""
import csv, json, math, sys

# code: (RRP inc GST, non pallet ex GST, pallet ex GST, mixed 3+ ex GST, pallet qty m2)
LIST = {
    "ETSN6631": (44, 22, 20, 18, "57.6"), "ETSN126631": (59, 29.5, 26.82, 25, "n/a"),
    "DSA36AK661": (44, 22, 20, 18, "57.6"), "DSA66AK661": (44, 22, 20, 18, "57.6"),
    "DSA126AK661": (59, 29.5, 26.82, 24.14, "40.32"),
    "DSA33AK662": (50, 25, 22.73, 20.45, "55.44"), "DSA36AK662": (44, 22, 20, 18, "57.6"),
    "DSA66AK662": (44, 22, 20, 18, "57.6"),
    "DSA36AK663": (44, 22, 20, 18, "57.6"), "DSA66AK663": (44, 22, 20, 18, "57.6"),
    "DSA33AK666": (50, 25, 22.73, 20.45, "55.44"), "DSA36AK666": (44, 22, 20, 18, "57.6"),
    "DSA66AK666": (44, 22, 20, 18, "57.6"),
    "DSA36MQ01": (44, 22, 20, 18, "57.6"), "DSA66MQ01": (44, 22, 20, 18, "57.6"),
    "DSA126MQ01": (59, 29.5, 26.82, 24.14, "40.32"),
    "DSA36MQ02": (44, 22, 20, 18, "57.6"), "DSA66MQ02": (44, 22, 20, 18, "57.6"),
    "DSA126MQ02": (59, 29.5, 26.82, 24.14, "40.32"),
    "DSA36MQ04": (44, 22, 20, 18, "57.6"), "DSA66MQ04": (44, 22, 20, 18, "57.6"),
    "DSA36CP01N": (44, 22, 20, 18, "57.6"), "DSA66CP01N": (44, 22, 20, 18, "57.6"),
    "ET36SS01": (49.5, 24.75, 22.5, 20.25, "57.6"), "ET36SS03": (49.5, 24.75, 22.5, 20.25, "57.6"),
    "HW637311": (55, 26.5, 25, 22.5, "57.6"), "YW607311": (55, 26.5, 25, 22.5, "57.6"),
    "FG637311": (59, 28.5, 26.82, 24.14, "57.6"), "FG607311": (59, 28.5, 26.82, 24.14, "57.6"),
    "HW637314": (55, 26.5, 25, 22.5, "57.6"), "YW607314": (55, 26.5, 25, 22.5, "57.6"),
    "YW277314": (75, 36.5, 34.09, 30.68, "TBC"),
    "FG637314": (59, 28.5, 26.82, 24.14, "57.6"), "FG607314": (59, 28.5, 26.82, 24.14, "57.6"),
    "HW637315": (55, 26.5, 25, 22.5, "57.6"), "YW607315": (55, 26.5, 25, 22.5, "57.6"),
    "YW277315": (75, 36.5, 34.09, 30.68, "TBC"),
    "FG637315": (59, 28.5, 26.82, 24.14, "57.6"), "FG607315": (59, 28.5, 26.82, 24.14, "57.6"),
    "HW637317": (55, 26.5, 25, 22.5, "57.6"), "YW607317": (55, 26.5, 25, 22.5, "57.6"),
    "YFR632950": (59, 28.5, 26.82, 24.14, "57.6"), "YFR602950": (59, 28.5, 26.82, 24.14, "57.6"),
    # The list prints Moon matt as YSR630331/YSR600331; Eternity's site and our SKUs use YFR.
    "YFR630331": (59, 29.5, 26.82, 24.14, "57.6"), "YFR600331": (59, 29.5, 26.82, 24.14, "57.6"),
    "BS630331": (65, 32.5, 29.55, 26.59, "57.6"), "BS600331": (65, 32.5, 29.55, 26.59, "57.6"),
    "YFR630338": (59, 29.5, 26.82, 24.14, "57.6"), "YFR600338": (59, 29.5, 26.82, 24.14, "57.6"),
    "BS630338": (65, 32.5, 29.55, 26.59, "57.6"), "BS600338": (65, 32.5, 29.55, 26.59, "57.6"),
    "YFR630337": (59, 29.5, 26.82, 24.14, "57.6"), "YFR600337": (59, 29.5, 26.82, 24.14, "57.6"),
    "BS630337": (65, 32.5, 29.55, 26.59, "57.6"), "BS600337": (65, 32.5, 29.55, 26.59, "57.6"),
}
# Codes Eternity renamed (ET... -> DSA...) and variants with no code in Shopify.
RENAME = {f"ET{c}": f"DSA{c}" for c in ["36CP01N", "66CP01N", "36AK661", "66AK661", "66AK662",
          "36AK663", "66AK663", "36AK666", "66AK666", "66MQ01", "126MQ01", "36MQ02", "66MQ02",
          "126MQ02", "36MQ04", "66MQ04"]}
BY_VARIANT = {("Lava Kraka Porcelain Tile", "600x1200mm / Gloss"): "YW277315"}

UNDER_RRP, MIN_MARKUP, TRADE_OFF = 0.15, 1.25, 0.15


def plan(cur):
    rows = []
    for v in cur:
        sku = RENAME.get(v["sku"] or "", v["sku"]) or BY_VARIANT.get((v["product"], v["variant"]))
        row = {**v, "new_sku": sku or "", "rrp": "", "cost_ex": "", "pallet_ex": "", "mixed3_ex": "",
               "pallet_qty": "", "new_price": v["price"], "margin_pct": "", "trade_price": "",
               "trade_margin_pct": "", "note": ""}
        if sku not in LIST:
            row["note"] = "Not on the 5 Oct list - price kept, no cost recorded. Check with Eternity."
            rows.append(row); continue
        rrp, cost, pallet, mixed, qty = LIST[sku]
        price = math.floor(rrp * (1 - UNDER_RRP) * 10) / 10
        floor_price = math.ceil(cost * 1.1 * MIN_MARKUP * 10) / 10
        if price < floor_price:
            price, row["note"] = floor_price, "Raised to the 25% minimum margin."
        if qty == "TBC":
            row["note"] = (row["note"] + " Pallet qty TBC on the list.").strip()
        row.update(rrp=rrp, cost_ex=cost, pallet_ex=pallet, mixed3_ex=mixed, pallet_qty=qty,
                   new_price=f"{price:.2f}",
                   margin_pct=round((price / 1.1 - cost) / (price / 1.1) * 100, 1),
                   trade_price=f"{price * (1 - TRADE_OFF):.2f}",
                   trade_margin_pct=round((price * (1 - TRADE_OFF) / 1.1 - cost)
                                          / (price * (1 - TRADE_OFF) / 1.1) * 100, 1))
        rows.append(row)
    return rows


if __name__ == "__main__":
    rows = plan(json.load(open(sys.argv[1])))
    with open(sys.argv[2], "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    for r in rows:
        print(f'{r["product"][:30]:30} {r["variant"][:20]:20} {r["sku"] or "-":11} {r["new_sku"]:11} '
              f'{r["price"]:>6} -> {r["new_price"]:>6}  cost {r["cost_ex"]!s:>5}  {r["margin_pct"]!s:>5}%  {r["note"]}')
