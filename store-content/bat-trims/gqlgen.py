"""Shared helpers: Python values -> Shopify GraphQL input literals, split into <16k documents."""
import json

ENUMS = {"DENY", "KILOGRAMS", "ACTIVE", "DRAFT", "DEFAULT"}
LIMIT = 15500
CATEGORY = "gid://shopify/TaxonomyCategory/ha-2-11"  # Hardware > Building Materials > Molding


def gql(x):
    """Python value -> GraphQL input literal"""
    if isinstance(x, dict):
        return "{" + ",".join(f"{k}:{gql(v)}" for k, v in x.items()) + "}"
    if isinstance(x, list):
        return "[" + ",".join(gql(v) for v in x) + "]"
    if isinstance(x, bool):
        return "true" if x else "false"
    if isinstance(x, (int, float)):
        return repr(x)
    if x in ENUMS:
        return x
    return json.dumps(x, ensure_ascii=False)


def variant(v, opts):
    return {
        "optionValues": [{"optionName": o, "name": v["options"][o]} for o in opts],
        "price": f'{v["price"]:.2f}', "taxable": True, "inventoryPolicy": "DENY",
        "inventoryItem": {"sku": v["sku"], "cost": f'{v["cost"]:.2f}', "tracked": False, "requiresShipping": True,
                          "measurement": {"weight": {"value": v["weight"], "unit": "KILOGRAMS"}}},
        "metafields": [
            {"namespace": "shipping", "key": "box_size", "type": "single_line_text_field", "value": v["box"]},
            {"namespace": "mm-google-shopping", "key": "mpn", "type": "single_line_text_field", "value": v["sku"]},
            {"namespace": "mm-google-shopping", "key": "condition", "type": "single_line_text_field", "value": "new"},
        ],
    }


def product_set(p, files, vendor="BAT Trims", category=CATEGORY, google_category="7112"):
    """productSet input for a product dict (handle, title, productType, tags, seo, descriptionHtml, options, variants)"""
    opts = p["options"]
    values = {o: [] for o in opts}
    for v in p["variants"]:
        for o in opts:
            if v["options"][o] not in values[o]:
                values[o].append(v["options"][o])
    variants = []
    for v in p["variants"]:
        vin = variant(v, opts)
        vin["sku"] = vin["inventoryItem"].pop("sku")  # productSet takes sku on the variant
        variants.append(vin)
    return {
        "handle": p["handle"], "title": p["title"], "vendor": vendor, "productType": p["productType"],
        "status": "ACTIVE", "descriptionHtml": p["descriptionHtml"], "tags": p["tags"],
        "category": category, "seo": p["seo"],
        "metafields": [{"namespace": "mm-google-shopping", "key": "google_product_category",
                        "type": "single_line_text_field", "value": google_category}],
        "productOptions": [{"name": o, "position": j + 1, "values": [{"name": x} for x in values[o]]}
                           for j, o in enumerate(opts)],
        "files": [{"id": files[f]} for f in p["files"]],
        "variants": variants,
    }


def write_docs(out, prefix, calls):
    docs, cur = [], []
    for c in calls:
        if cur and sum(map(len, cur)) + len(c) > LIMIT:
            docs.append(cur)
            cur = []
        cur.append(c)
    if cur:
        docs.append(cur)
    for i, d in enumerate(docs):
        with open(f"{out}/{prefix}{i:02d}.graphql", "w") as f:
            f.write("mutation {\n" + "\n".join(d) + "\n}\n")
    return len(docs)
