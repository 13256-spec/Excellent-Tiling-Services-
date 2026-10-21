"""Roberts Designs items that have no photo on robertsdesigns.com.au -> Shopify productSet inputs (21 Oct 2026).

46 Roberts products have no image on their site. 22 are already in the store (photos found elsewhere on 6 Oct),
8 show $0 on Roberts (can't be priced, skipped). These 16 are the rest: 5 were deleted on 6 Oct for having no
photo (backup deleted-no-photo-2-2026-10-06.json), 11 were never imported. Owner's call (21 Oct): list them
without a photo. All tagged `no-photo` so they are easy to find when a photo turns up.

Price / cost from roberts-designs-pricing.csv. Where that sheet had cost = Roberts list (no trade discount
recorded), cost = list x 0.51 like the sibling Baron / Sigma parts fixed on 6 Oct, tagged `cost-estimated`.

Usage: roberts_no_photo_2026_10.py out.json
"""
import json, sys

SIGMA_CAT, BARON_CAT, DRAIN_CAT, TRIM_CAT = ("gid://shopify/TaxonomyCategory/ha-15-11-7", "gid://shopify/TaxonomyCategory/ha-15-34-2",
                                             "gid://shopify/TaxonomyCategory/ha-10-2-3", "gid://shopify/TaxonomyCategory/ha-2-11")
SIGMA_TAGS = ["no-photo", "Roberts Designs", "ship-parcel", "Sigma", "supplier-import", "Tile Cutters", "Tile Cutting Equipment"]
BARON_TAGS = ["Baron", "cost-estimated", "Mixers", "no-photo", "Roberts Designs", "ship-parcel", "supplier-import", "Tiling Tools + Installation Products"]

def sigma(sku, part, title, price, cost, fits, what, kg, big=False, est=False, collections=("sigma-cutter-spares",)):
    return dict(sku=sku, title=title, vendor="Sigma", productType="Tiling Machine Parts", category=SIGMA_CAT, price=price, cost=cost, kg=kg,
                tags=sorted(SIGMA_TAGS + ["shipping-large" if big else "shipping-small"] + (["cost-estimated"] if est else [])),
                fits=fits, collections=list(collections),
                html=f"<p><strong>Fits:</strong> {fits}</p><p>{what}</p><ul><li><strong>Brand:</strong> Sigma</li><li><strong>Part:</strong> {part}</li>"
                     f"<li><strong>Code:</strong> {sku}</li></ul><p>No product photo yet. Match the Sigma part number to your cutter before ordering.</p>",
                seo=f"{what} Genuine Sigma part {part}. SKU {sku}.")

def baron(sku, part, title, price, cost, fits, what, kg, big=False):
    return dict(sku=sku, title=title, vendor="Baron", productType="Mixers", category=BARON_CAT, price=price, cost=cost, kg=kg,
                tags=sorted(BARON_TAGS + ["shipping-large" if big else "shipping-small"]), fits=fits, collections=["mixers-paddles-buckets"],
                html=f"<p>{what}</p><ul><li>Fits: {fits}</li><li>Baron part number: {part}</li></ul><p>No product photo yet.</p>",
                seo=f"Baron {title}. Genuine spare part for Baron forced action mixers. SKU {sku}.")

ITEMS = [
    sigma("RDXA3525B", "90DG swivel measurement bar", "Sigma 90DG Swivel Measurement Bar", "84.95", "44.98",
          "Sigma cutters that take the 90DG bar; check the part number against your cutter",
          "Genuine Sigma swivel measurement bar: the graduated bar that sets the cut width and angle on the cutter.", 1.5, big=True, est=True),
    sigma("RDXA3599", "8AEP2 extension bar 50 cm", "Sigma 8AEP2 Kera-Cut Extension Bar 50cm", "321.95", "169.75",
          "Sigma Kera-Cut large format cutting systems",
          "Genuine Sigma 50 cm extension bar that lengthens the Kera-Cut guide rail for longer cuts in large format tiles and slabs.", 2.0, big=True),
    sigma("RDXA3650", "64B2 non-slip magnetic mat", "Sigma 64B2 Non-Slip Magnetic Mat", "191.95", "110.00",
          "Sigma Kera-Cut and Kera-Lift systems",
          "Genuine Sigma non-slip magnetic mat that holds the tile or slab steady on the work surface while cutting.", 1.5),
    sigma("RDXA3591", "421 carriage kit", "Sigma 421 Carriage Kit (2 Wheel Sets with Slab Support and Angle Support)", "1115.95", "587.30",
          "Sigma Kera-Cut and Kera-Lift systems",
          "Genuine Sigma carriage kit: two wheel sets with a slab support and an angle support for moving and positioning large format slabs.", 8.0, big=True),
    sigma("RDXA3595", "402 work bench storage hooks", "Sigma 402 Work Bench Storage Hooks for Kera-Cut", "135.95", "71.80",
          "Sigma Kera-Cut work bench",
          "Genuine Sigma storage hooks that mount on the Kera-Cut work bench to hang the rails and accessories when not in use.", 2.0),
    sigma("RDXA3647", "90NE swivel measurement bar 64-0-64 cm", "Sigma 90NE Swivel Measurement Bar 64cm-0-64cm", "374.95", "215.00",
          "Sigma cutters that take the 90NE bar; check the part number against your cutter",
          "Genuine Sigma swivel measurement bar graduated 64 cm either side of centre, for setting cut width and angle on the cutter.", 3.0, big=True),
    sigma("RDXA3492", "37C table fixing kit", "Sigma 37C Table Fixing Kit", "258.95", "148.50",
          "Sigma Kera-Cut work bench",
          "Genuine Sigma fixing kit for securing the Kera-Cut system to the work table.", 3.0),
    sigma("RDXA3534", "196725 rubber foot", "Sigma 196725 Rubber Foot", "5.20", "3.00",
          "Sigma tile cutters; check the part number against your cutter",
          "Genuine Sigma replacement rubber foot for the cutter base.", 0.05),
    sigma("RDXA3651", "17A extension bar 500 mm", "Sigma 17A Extension Bar 500mm", "191.95", "110.00",
          "Sigma cutters that take the 17A bar; check the part number against your cutter",
          "Genuine Sigma 500 mm extension bar for longer cuts on Sigma tile cutters.", 2.0, big=True),
    sigma("RDXA3526", "14G scoring wheel 12 mm", "Sigma 14G Kera-Cut Spare Scoring Wheel 12mm", "33.95", "18.30",
          "Sigma Kera-Cut",
          "Genuine Sigma 12 mm replacement scoring wheel for the Kera-Cut cutting system.", 0.05),
    sigma("RDXA3580", "108362 M8 square nut", "Sigma 108362 M8 Square Nut for Locking Bolt", "7.35", "3.88",
          "Sigma swivel measurement bar locking bolts",
          "Genuine Sigma M8 square nut for the measurement bar locking bolt.", 0.1, est=True),
    baron("RDXM50444", "50444", "F300 Mixer Paddles Set (3)", "372.95", "196.35", "Baron F300 forced action mixer",
          "Genuine Baron replacement set of three mixing paddles for the F300 forced action mixer.", 10.0, big=True),
    baron("RDXM50101", "50101", "E120 Replacement Power Cable 2m with Plug", "120.95", "63.85", "Baron E120 forced action mixer",
          "Genuine Baron 2 m replacement power cable with plug for the E120 forced action mixer.", 1.0),
    dict(sku="RDXT14791", title="Recessed Flange Adapter 100 x 100mm", vendor="Roberts Designs", productType="Designer Bathroom Accessories",
         category=DRAIN_CAT, price="23.95", cost="15.73", kg=0.4, fits=None, collections=["bathroom-wastes"],
         tags=["Designer Bathroom Accessories", "Floor Wastes and Linear Drains", "no-photo", "Roberts Designs", "ship-parcel", "shipping-small", "supplier-import"],
         html="<p>Adapter for a recessed puddle flange, 100 x 100mm, used at the floor waste penetration so the waterproofing membrane can be sealed to the waste.</p>"
              "<ul><li><strong>Size:</strong> 100 x 100mm</li><li><strong>Code:</strong> RDXT14791</li></ul><p>No product photo yet.</p>",
         seo="Recessed flange adapter 100 x 100mm from Roberts Designs, for sealing the waterproofing membrane at a floor waste. SKU RDXT14791."),
    dict(sku="RDXT14466", title="Flange 50mm Socket Weld", vendor="Roberts Designs", productType="Designer Bathroom Accessories",
         category=DRAIN_CAT, price="21.95", cost="14.30", kg=0.3, fits=None, collections=["bathroom-wastes"],
         tags=["Designer Bathroom Accessories", "Floor Wastes and Linear Drains", "no-photo", "Roberts Designs", "ship-parcel", "shipping-small", "supplier-import"],
         html="<p>50mm socket weld flange for connecting a floor waste to 50mm PVC pipe.</p>"
              "<ul><li><strong>Size:</strong> 50mm</li><li><strong>Connection:</strong> Socket weld</li><li><strong>Code:</strong> RDXT14466</li></ul><p>No product photo yet.</p>",
         seo="50mm socket weld flange from Roberts Designs for connecting a floor waste to 50mm pipe. SKU RDXT14466."),
    dict(sku="RDTT896", title="Retro Cove Joiner – 70mm", vendor="Roberts Designs", productType="Retro Cove Trim",
         category=TRIM_CAT, price="12.20", cost="7.15", kg=0.05, fits=None, collections=[],
         tags=["no-photo", "Retro Cove Trim", "Roberts Designs", "ship-parcel", "shipping-small", "supplier-import", "Tile Trims + Edging Profiles"],
         html="<p>Joiner for connecting lengths of 70mm retro cove trim, giving a straight, aligned join between pieces.</p>"
              "<ul><li><strong>Size:</strong> 70mm</li><li><strong>Box Qty:</strong> 1</li><li><strong>Code:</strong> RDTT896</li></ul><p>No product photo yet.</p>",
         seo="Joiner for 70mm retro cove tile trim from Roberts Designs. SKU RDTT896."),
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
    out = [product(i) for i in ITEMS]
    assert len({p["variants"][0]["inventoryItem"]["sku"] for p in out}) == 16
    for p in out:  # profit floor: price >= cost x 1.1 (GST) x 1.25
        v = p["variants"][0]; assert float(v["price"]) >= float(v["inventoryItem"]["cost"]) * 1.375, p["title"]
    json.dump(out, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
    print(len(out), "products")
