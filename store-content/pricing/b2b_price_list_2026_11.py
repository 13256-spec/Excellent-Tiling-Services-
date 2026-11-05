"""Fixed trade prices for the B2B price list (5 Nov 2026).

Shopify Grow has native B2B (companies, one B2B market, up to 3 catalogs). The trade scheme lives in ONE catalog:
  market      "Trade accounts (B2B)"  gid://shopify/Market/26618265663   (all company locations)
  catalog     "Trade price list"      gid://shopify/MarketCatalog/71173406783  (publication: all products, auto-publish)
  price list  "Trade prices"          gid://shopify/PriceList/17250287679  (base adjustment 0%, fixed price per variant)
Fixed price = public price x (1 - ets.trade_band/100), to the cent, half up: the same number as the variant
metafield custom.trade_price. Compare-at = the public price (shown crossed out to trade logins). Products with band 0 have no fixed price, so trade accounts pay the public price.

Input: pages/p*.json, saved pages of the products query in trade_price_metafields_2026_11.py (include `tags`).
Output: pl/plNN.graphql, one priceListFixedPricesAdd per file (90 prices, < 16k chars), to run with the
Shopify MCP graphql_mutation tool. Re-run after any price or band change. To remove a price that no longer
applies (band dropped to 0) use priceListFixedPricesDelete with the variant ids.
"""
import json, glob, os
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING
PRICE_LIST = "gid://shopify/PriceList/17250287679"
C = Decimal("0.01"); prices = []; seen = set()
for f in sorted(glob.glob("pages/p*.json")):
    for p in json.load(open(f))["data"]["products"]["nodes"]:
        if p["id"] in seen: continue
        seen.add(p["id"])
        band = int((p["band"] or {}).get("value") or 0)
        if not band: continue
        for v in p["variants"]["nodes"]:
            # m2-units tiles (price per 0.01 m2): round UP so the whole-cent rounding never gives more than the band
            rnd = ROUND_CEILING if "m2-units" in p.get("tags", []) else ROUND_HALF_UP
            tp = (Decimal(v["price"]) * (100 - band) / 100).quantize(C, rnd)
            # compareAtPrice = the public price, so trade logins see it crossed out next to their price
            prices.append('{variantId: "%s", price: {amount: "%s", currencyCode: AUD}, compareAtPrice: {amount: "%s", currencyCode: AUD}}' % (v["id"], tp, Decimal(v["price"]).quantize(C)))
os.makedirs("pl", exist_ok=True)
chunks = [prices[i:i+90] for i in range(0, len(prices), 90)]
for i, c in enumerate(chunks, 1):
    q = 'mutation { priceListFixedPricesAdd(priceListId: "%s", prices: [%s]) { prices { variant { id } } userErrors { field message code } } }' % (PRICE_LIST, ", ".join(c))
    assert len(q) < 16000, len(q)
    open(f"pl/pl{i:02d}.graphql", "w").write(q)
print(len(prices), "prices,", len(chunks), "files")
