"""Roberts Designs items that have no photo on robertsdesigns.com.au -> Shopify productSet inputs (21 Oct 2026).

46 Roberts products have no image on their site. 22 are already in the store (photos found elsewhere on 6 Oct),
8 show $0 on Roberts (can't be priced, skipped). These 16 are the rest: 5 were deleted on 6 Oct for having no
photo (backup deleted-no-photo-2-2026-10-06.json), 11 were never imported. Owner's call (21 Oct): list them
without a photo. All tagged `no-photo` so they are easy to find when a photo turns up.

Cost (owner, 21 Oct): the price shown on Roberts' public website IS our cost (ex GST). Sigma / Baron costs are
stored ex GST as usual; the Roberts Designs vendor rows are stored x 1.1 like the rest of that vendor (playbook).
Price: the market was checked (Tile Mart, Victiles, TSP Trims, National Tiles, TradieCart, eBay AU, 21 Oct).
Where an Australian price exists it is at or below our cost (Kera-Cut 50cm bar: Tile Mart $346.40 / Victiles $200
vs cost $332.50; 402 hooks: Tile Mart $146.58 vs $140.75; Kera-Lift carriage kit: Tile Mart $874.90 vs $1,151.10;
14G wheel: eBay $47.06 vs $35.80). The rest have no Australian listing. So every price = the public floor
(cost x 1.1 x 1.25) rounded up to .95, tagged `price-check`. No trade band works at the floor, so trade_band = 0.

Shipping: parcels in the General profile with the eBay post band of their siblings (ebay-post-15 up to 1 kg,
ebay-post-20 above); the 90NE bar is about 1.35 m long, over Australia Post's limit, so it is Perth-only.

Usage: roberts_no_photo_2026_10.py out.json
"""
import json, math, sys

SIGMA_CAT, BARON_CAT, DRAIN_CAT, TRIM_CAT = ("gid://shopify/TaxonomyCategory/ha-15-11-7", "gid://shopify/TaxonomyCategory/ha-15-34-2",
                                             "gid://shopify/TaxonomyCategory/ha-10-2-3", "gid://shopify/TaxonomyCategory/ha-2-11")
BASE = ["no-photo", "price-check", "Roberts Designs", "supplier-import"]
SIGMA_TAGS = BASE + ["Sigma", "Tile Cutters", "Tile Cutting Equipment"]
BARON_TAGS = BASE + ["Baron", "Mixers", "Tiling Tools + Installation Products"]
PERTH = ["ship-local-only", "ship-freight", "shipping-large", "ebay-pickup-only"]  # delivery profile "Perth only (local delivery / pickup)"

def floor_price(cost):  # public floor, rounded up to the next .95
    f = cost * 1.1 * 1.25
    return f"{math.ceil(f - 0.95) + 0.95:.2f}"

def ship(kg, perth=False):
    if perth: return PERTH
    return ["ship-parcel", "shipping-small", "ebay-post-15"] if kg <= 1 else ["ship-parcel", "shipping-large", "ebay-post-20"]

def sigma(sku, part, title, cost, fits, what, kg, perth=False, collections=("sigma-cutter-spares",)):
    return dict(sku=sku, title=title, vendor="Sigma", productType="Tiling Machine Parts", category=SIGMA_CAT, cost=f"{cost:.2f}",
                price=floor_price(cost), kg=kg, tags=sorted(SIGMA_TAGS + ship(kg, perth)), fits=fits, collections=list(collections),
                html=f"<p><strong>Fits:</strong> {fits}</p><p>{what}</p><ul><li><strong>Brand:</strong> Sigma</li><li><strong>Part:</strong> {part}</li>"
                     f"<li><strong>Code:</strong> {sku}</li></ul><p>No product photo yet. Match the Sigma part number to your cutter before ordering.</p>",
                seo=f"{what} Genuine Sigma part {part}. SKU {sku}.")

def baron(sku, part, title, cost, fits, what, kg):
    return dict(sku=sku, title=title, vendor="Baron", productType="Mixers", category=BARON_CAT, cost=f"{cost:.2f}", price=floor_price(cost), kg=kg,
                tags=sorted(BARON_TAGS + ship(kg)), fits=fits, collections=["mixers-paddles-buckets"],
                html=f"<p>{what}</p><ul><li>Fits: {fits}</li><li>Baron part number: {part}</li></ul><p>No product photo yet.</p>",
                seo=f"Baron {title}. Genuine spare part for Baron forced action mixers. SKU {sku}.")

def roberts(sku, title, ptype, cat, web_cost, kg, html, seo, tags, collections):
    cost = round(web_cost * 1.1, 2)  # Roberts Designs vendor: cost stored inc GST (playbook)
    return dict(sku=sku, title=title, vendor="Roberts Designs", productType=ptype, category=cat, cost=f"{cost:.2f}", price=floor_price(cost), kg=kg,
                fits=None, collections=collections, tags=sorted(BASE + tags + ship(kg)), html=html, seo=seo)

ITEMS = [
    sigma("RDXA3525B", "90DG swivel measurement bar", "Sigma 90DG Swivel Measurement Bar", 88.20,
          "Sigma cutters that take the 90DG bar; check the part number against your cutter",
          "Genuine Sigma swivel measurement bar: the graduated bar that sets the cut width and angle on the cutter.", 1.5),
    sigma("RDXA3599", "8AEP2 extension bar 50 cm", "Sigma 8AEP2 Kera-Cut Extension Bar 50cm", 332.50,
          "Sigma Kera-Cut large format cutting systems",
          "Genuine Sigma 50 cm extension bar that lengthens the Kera-Cut guide rail for longer cuts in large format tiles and slabs.", 2.0),
    sigma("RDXA3650", "64B2 non-slip magnetic mat", "Sigma 64B2 Non-Slip Magnetic Mat", 198.00,
          "Sigma Kera-Cut and Kera-Lift systems",
          "Genuine Sigma non-slip magnetic mat that holds the tile or slab steady on the work surface while cutting.", 1.5),
    sigma("RDXA3591", "421 carriage kit", "Sigma 421 Carriage Kit (2 Wheel Sets with Slab Support and Angle Support)", 1151.10,
          "Sigma Kera-Cut and Kera-Lift systems",
          "Genuine Sigma carriage kit: two wheel sets with a slab support and an angle support for moving and positioning large format slabs.", 12.0),
    sigma("RDXA3595", "402 work bench storage hooks", "Sigma 402 Work Bench Storage Hooks for Kera-Cut", 140.75,
          "Sigma Kera-Cut work bench",
          "Genuine Sigma storage hooks that mount on the Kera-Cut work bench to hang the rails and accessories when not in use.", 2.0),
    sigma("RDXA3647", "90NE swivel measurement bar 64-0-64 cm", "Sigma 90NE Swivel Measurement Bar 64cm-0-64cm", 387.00,
          "Sigma 4EN and 4FN tile cutters",
          "Genuine Sigma swivel measurement bar graduated 64 cm either side of centre, for setting cut width and angle on the cutter.", 3.0, perth=True),
    sigma("RDXA3492", "37C table fixing kit", "Sigma 37C Table Fixing Kit", 267.30,
          "Sigma Kera-Cut work bench",
          "Genuine Sigma fixing kit for securing the Kera-Cut system to the work table.", 3.0),
    sigma("RDXA3534", "196725 rubber foot", "Sigma 196725 Rubber Foot", 5.40,
          "Sigma tile cutters; check the part number against your cutter",
          "Genuine Sigma replacement rubber foot for the cutter base.", 0.05),
    sigma("RDXA3651", "17A extension bar 500 mm", "Sigma 17A Extension Bar 500mm", 198.00,
          "Sigma Series 4 tile cutters",
          "Genuine Sigma 500 mm extension bar for longer cuts on Sigma tile cutters.", 2.0),
    sigma("RDXA3526", "14G scoring wheel 12 mm", "Sigma 14G Kera-Cut Spare Scoring Wheel 12mm", 35.80,
          "Sigma Kera-Cut",
          "Genuine Sigma 12 mm replacement scoring wheel for the Kera-Cut cutting system.", 0.05),
    sigma("RDXA3580", "108362 M8 square nut", "Sigma 108362 M8 Square Nut for Locking Bolt", 7.60,
          "Sigma swivel measurement bar locking bolts",
          "Genuine Sigma M8 square nut for the measurement bar locking bolt.", 0.1),
    baron("RDXM50444", "50444", "F300 Mixer Paddles Set (3)", 385.00, "Baron F300 forced action mixer",
          "Genuine Baron replacement set of three mixing paddles for the F300 forced action mixer.", 10.0),
    baron("RDXM50101", "50101", "E120 Replacement Power Cable 2m with Plug", 125.19, "Baron E120 forced action mixer",
          "Genuine Baron 2 m replacement power cable with plug for the E120 forced action mixer.", 1.0),
    roberts("RDXT14791", "Recessed Flange Adapter 100 x 100mm", "Designer Bathroom Accessories", DRAIN_CAT, 25.75, 0.4,
            "<p>Adapter for a recessed puddle flange, 100 x 100mm, used at the floor waste penetration so the waterproofing membrane can be sealed to the waste.</p>"
            "<ul><li><strong>Size:</strong> 100 x 100mm</li><li><strong>Code:</strong> RDXT14791</li></ul><p>No product photo yet.</p>",
            "Recessed flange adapter 100 x 100mm from Roberts Designs, for sealing the waterproofing membrane at a floor waste. SKU RDXT14791.",
            ["Designer Bathroom Accessories", "Floor Wastes and Linear Drains"], ["bathroom-wastes"]),
    roberts("RDXT14466", "Flange 50mm Socket Weld", "Designer Bathroom Accessories", DRAIN_CAT, 23.40, 0.3,
            "<p>50mm socket weld flange for connecting a floor waste to 50mm PVC pipe.</p>"
            "<ul><li><strong>Size:</strong> 50mm</li><li><strong>Connection:</strong> Socket weld</li><li><strong>Code:</strong> RDXT14466</li></ul><p>No product photo yet.</p>",
            "50mm socket weld flange from Roberts Designs for connecting a floor waste to 50mm pipe. SKU RDXT14466.",
            ["Designer Bathroom Accessories", "Floor Wastes and Linear Drains"], ["bathroom-wastes"]),
    roberts("RDTT896", "Retro Cove Joiner – 70mm", "Retro Cove Trim", TRIM_CAT, 12.60, 0.05,
            "<p>Joiner for connecting lengths of 70mm retro cove trim, giving a straight, aligned join between pieces.</p>"
            "<ul><li><strong>Size:</strong> 70mm</li><li><strong>Box Qty:</strong> 1</li><li><strong>Code:</strong> RDTT896</li></ul><p>No product photo yet.</p>",
            "Joiner for 70mm retro cove tile trim from Roberts Designs. SKU RDTT896.",
            ["Retro Cove Trim", "Tile Trims + Edging Profiles"], []),
]

def product(i):
    mf = [{"namespace": "ets", "key": "trade_band", "type": "number_integer", "value": "0"}]
    if i["fits"]:
        mf += [{"namespace": "ets", "key": "fits_models", "type": "single_line_text_field", "value": i["fits"]},
               {"namespace": "ets", "key": "fits_role", "type": "single_line_text_field", "value": "item"}]
    return {"title": i["title"], "descriptionHtml": i["html"], "vendor": i["vendor"], "productType": i["productType"], "category": i["category"],
            "status": "ACTIVE", "tags": i["tags"], "seo": {"title": f"{i['title']} | ETS", "description": i["seo"]}, "metafields": mf,
            "productOptions": [{"name": "Title", "values": [{"name": "Default Title"}]}],
            "variants": [{"optionValues": [{"optionName": "Title", "name": "Default Title"}], "price": i["price"], "inventoryPolicy": "CONTINUE", "taxable": True,
                          "inventoryItem": {"sku": i["sku"], "tracked": True, "cost": i["cost"],
                                            "measurement": {"weight": {"value": i["kg"], "unit": "KILOGRAMS"}}}}],
            "_collections": i["collections"]}

if __name__ == "__main__":
    assert floor_price(100) == "137.95" and floor_price(5.40) == "7.95"
    out = [product(i) for i in ITEMS]
    assert len({p["variants"][0]["inventoryItem"]["sku"] for p in out}) == 16
    for p in out:  # profit floor: price >= cost x 1.1 (GST) x 1.25
        v = p["variants"][0]; assert float(v["price"]) >= float(v["inventoryItem"]["cost"]) * 1.375 - 1e-9, p["title"]
    json.dump(out, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
    for i in ITEMS: print(f"{i['sku']:10} {i['cost']:>8} -> {i['price']:>8}  {i['kg']:>5}kg  {[t for t in i['tags'] if t.startswith(('ship','ebay'))]}")
