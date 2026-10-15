"""Turn bat-products.json into productSet inputs (JSONL) for a Shopify bulk mutation."""
import json

P = json.load(open("bat-products.json"))
names = json.load(open("image-files.json"))      # catalogue image -> uploaded filename
ids = json.load(open("shopify-file-ids.json"))   # uploaded filename -> MediaImage gid
CATEGORY = "gid://shopify/TaxonomyCategory/ha-2-11"  # Hardware > Building Materials > Molding


def fid(img):
    return ids[names[img]]


lines = []
for p in P:
    files = []
    for img in [p["image"]] + p["gallery"] + list(p["variant_images"].values()):
        if fid(img) not in files:
            files.append(fid(img))
    opts = p["options"]
    values = {o: [] for o in opts}
    for x in p["variants"]:
        for o in opts:
            if x["options"][o] not in values[o]:
                values[o].append(x["options"][o])
    variants = []
    for x in p["variants"]:
        var = {
            "sku": x["sku"],
            "price": "0.00",
            "taxable": True,
            "inventoryPolicy": "DENY",
            "optionValues": [{"optionName": o, "name": x["options"][o]} for o in opts],
            "inventoryItem": {"tracked": False, "requiresShipping": True,
                              "measurement": {"weight": {"value": x["weight"], "unit": "KILOGRAMS"}}},
            "metafields": [
                {"namespace": "shipping", "key": "box_size", "type": "single_line_text_field", "value": x["box"]},
                {"namespace": "mm-google-shopping", "key": "mpn", "type": "single_line_text_field", "value": x["sku"]},
                {"namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
            ],
        }
        img = next((p["variant_images"][v] for v in x["options"].values() if v in p["variant_images"]), p["image"])
        var["file"] = {"id": fid(img)}
        variants.append(var)
    lines.append({"input": {
        "handle": p["handle"], "title": p["title"], "vendor": p["vendor"], "productType": p["productType"],
        "status": "DRAFT", "descriptionHtml": p["descriptionHtml"], "tags": p["tags"], "category": CATEGORY,
        "seo": p["seo"],
        "metafields": [
            {"namespace": "mm-google-shopping", "key": "google_product_category", "type": "single_line_text_field", "value": "7112"},
        ],
        "productOptions": [{"name": o, "position": i + 1, "values": [{"name": v} for v in values[o]]}
                           for i, o in enumerate(opts)],
        "files": [{"id": f} for f in files],
        "variants": variants,
    }, "synchronous": True})

with open("bat-productset.jsonl", "w") as f:
    for l in lines:
        f.write(json.dumps(l, ensure_ascii=False) + "\n")
print(len(lines), "lines")
