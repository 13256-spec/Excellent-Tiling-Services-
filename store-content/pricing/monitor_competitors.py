"""Weekly pricing check: our live prices vs Bathroom City (MELA) and B&B Hardware, against our profit floors.

MELA rule since 20 Oct 2026: our price must equal Bathroom City's current price, never below it (supplier condition).
B&B rule: 5% under.

Reads only public product feeds (no Shopify login needed) plus store-pricing-2026-10-03.csv for costs and
trade bands. Changes nothing; writes a Markdown report for the owner to approve.

Usage: monitor_competitors.py [report.md]
"""
import csv, json, math, os, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from reprice_2026_10 import BB_MATCH, GST, PUB_MARKUP  # noqa: E402

FEEDS = {"ours": "https://excellenttilingservice.com.au", "bc": "https://bathroom-city.com.au",
         "bb": "https://bbhardware.com.au"}
PLAN = os.path.join(HERE, "store-pricing-2026-10-03.csv")
MELA_MAP = os.path.join(HERE, "mela-pricing-2026-10-01.csv")


def feed(base):
    out, page = [], 1
    while True:
        req = urllib.request.Request(f"{base}/products.json?limit=250&page={page}",
                                     headers={"User-Agent": "Mozilla/5.0 (ETS price check)"})
        products = json.load(urllib.request.urlopen(req, timeout=60))["products"]
        if not products:
            return out
        out += products
        page += 1
        time.sleep(0.5)


def target(comp, dollar):
    t = comp * 0.95
    return math.floor(t) if dollar and t >= 20 else math.floor(t * 20) / 20


def main(report_path):
    plan = {r["vid"].split("/")[-1]: r for r in csv.DictReader(open(PLAN))}
    mela = {r["vid"].split("/")[-1]: r for r in csv.DictReader(open(MELA_MAP))}
    ours = {str(v["id"]): (p, v) for p in feed(FEEDS["ours"]) for v in p["variants"]}
    bc = {(p["title"], v["sku"]): float(v["price"]) for p in feed(FEEDS["bc"]) for v in p["variants"]}
    bb = {p["title"]: float(p["variants"][0]["price"]) for p in feed(FEEDS["bb"])}

    undercut, drift, floor_breach, unplanned, gone, below_bc, bc_cheaper = [], [], [], [], [], [], []
    for vid, (p, v) in ours.items():
        price = float(v["price"])
        name = p["title"] + ("" if v["title"] == "Default Title" else " / " + v["title"])
        r = plan.get(vid)
        if not r:
            unplanned.append(f"| {name} | {v.get('sku') or ''} | ${price:.2f} |")
            continue
        if abs(price - float(r["new_price"])) > 0.004:
            drift.append(f"| {name} | ${float(r['new_price']):.2f} | ${price:.2f} |")
        cost = float(r["cost"]) * GST if r["cost"] else None
        if cost and price < cost * PUB_MARKUP - 0.01:
            floor_breach.append(f"| {name} | ${price:.2f} | ${cost:.2f} | ${math.ceil(cost * PUB_MARKUP * 20) / 20:.2f} |")
        comp, who, dollar = None, "", False
        m = mela.get(vid)
        if m and m["bc_title"]:
            comp, who, dollar = bc.get((m["bc_title"], m["bc_sku"])), "Bathroom City", True
            if comp is None:
                gone.append(f"| {name} | Bathroom City: {m['bc_title']} |")
        else:
            key = name if name in BB_MATCH else p["title"]
            if key in BB_MATCH:
                comp, who = bb.get(BB_MATCH[key]), "B&B Hardware"
                if comp is None:
                    gone.append(f"| {name} | B&B: {BB_MATCH[key]} |")
        band = r["trade_band"] or "0"
        if who == "Bathroom City" and comp is not None and price < comp - 0.004:
            # MELA may not be advertised below Bathroom City (owner, 20 Oct 2026): raise to match.
            below_bc.append(f"| {name} | ${comp:.2f} | ${price:.2f} | {'$%.2f' % cost if cost else '–'} | {band}% |")
        elif who == "Bathroom City" and comp is not None and price > comp + 0.004:
            floor = cost * PUB_MARKUP if cost else 0
            bc_cheaper.append(f"| {name} | ${comp:.2f} | ${price:.2f} | {'$%.2f' % cost if cost else '–'} | "
                              f"{'can match' if comp >= floor else 'below our profit floor, stay'} |")
        elif who == "B&B Hardware" and comp is not None and price >= comp:
            want = target(comp, dollar)
            floor = cost * PUB_MARKUP if cost else 0
            ok = want >= floor
            undercut.append(f"| {name} | {who} ${comp:.2f} | ${price:.2f} | "
                            f"{'$%.2f' % want if ok else 'can’t beat profitably'} | "
                            f"{'$%.2f' % cost if cost else '–'} | {band}% |")

    def table(head, rows):
        return (head + "\n" + "|" + "---|" * head.count("|", 1) + "\n" + "\n".join(rows) + "\n") if rows else "None.\n"

    md = [f"# ETS weekly price check – {time.strftime('%d %b %Y')}\n",
          f"Checked {len(ours)} of our variants, {len(bc)} Bathroom City and {len(bb)} B&B products. "
          "Nothing was changed; the owner approves any price change.\n",
          "## 1a. MELA priced BELOW Bathroom City (not allowed: raise to their price)\n",
          table("| Item | Bathroom City | Our price | Cost inc GST | Trade band |", below_bc),
          "## 1b. Bathroom City now cheaper than us on MELA (match only if above our profit floor)\n",
          table("| Item | Bathroom City | Our price | Cost inc GST | Action |", bc_cheaper),
          "## 1c. B&B Hardware is now as cheap or cheaper than us\n",
          table("| Item | Competitor | Our price | Suggested (5% under, above profit floor) | Cost inc GST | Trade band |", undercut),
          "## 2. Selling below the profit floor (cost inc GST × 1.25)\n",
          table("| Item | Our price | Cost inc GST | Floor price |", floor_breach),
          "## 3. Live price differs from the approved price list\n",
          table("| Item | Approved | Live now |", drift),
          "## 4. New products with no cost or trade band yet\n",
          table("| Item | SKU | Price |", unplanned),
          "## 5. Competitor no longer lists the matched item\n",
          table("| Item | Was matched to |", gone)]
    os.makedirs(os.path.dirname(report_path) or ".", exist_ok=True)
    open(report_path, "w").write("\n".join(md))
    print(f"below BC {len(below_bc)}, BC cheaper {len(bc_cheaper)}, undercut {len(undercut)}, below floor {len(floor_breach)}, drift {len(drift)}, "
          f"unplanned {len(unplanned)}, gone {len(gone)} -> {report_path}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "reports", time.strftime("price-check-%Y-%m-%d.md")))
