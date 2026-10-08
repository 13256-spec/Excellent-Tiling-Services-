"""Write the GraphQL documents that add may2026-additions.json to Shopify.

  python3 build_may2026_mutations.py OUTDIR

OUTDIR/vdocNN.graphql  productVariantsBulkCreate for new variants on existing products
OUTDIR/pdocNN.graphql  productSet for the new products (ACTIVE)
Each document stays under Shopify's 16,384 character limit.
"""
import json
import os
import sys

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
A = json.load(open("may2026-additions.json"))
IDS = json.load(open("shopify-product-ids.json"))
FILES = json.load(open("shopify-file-ids-may2026.json"))
ENUMS = {"DENY", "KILOGRAMS", "ACTIVE", "DEFAULT"}
LIMIT = 15500


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


def write(prefix, calls):
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


calls, k = [], 0
for handle, vs in A["variants"].items():
    opts = list(vs[0]["options"])
    for i in range(0, len(vs), 25):
        chunk = [variant(v, opts) for v in vs[i:i + 25]]
        calls.append(f'v{k}: productVariantsBulkCreate(productId:"{IDS[handle]}",strategy:DEFAULT,variants:{gql(chunk)})'
                     "{productVariants{id sku} userErrors{field message}}")
        k += 1
print(write("vdoc", calls), "variant documents,", k, "calls")

calls = []
for i, p in enumerate(A["products"]):
    opts = p["options"]
    values = {o: [] for o in opts}
    for v in p["variants"]:
        for o in opts:
            if v["options"][o] not in values[o]:
                values[o].append(v["options"][o])
    inp = {
        "handle": p["handle"], "title": p["title"], "vendor": "BAT Trims", "productType": p["productType"],
        "status": "ACTIVE", "descriptionHtml": p["descriptionHtml"], "tags": p["tags"],
        "category": "gid://shopify/TaxonomyCategory/ha-2-11", "seo": p["seo"],
        "metafields": [{"namespace": "mm-google-shopping", "key": "google_product_category",
                        "type": "single_line_text_field", "value": "7112"}],
        "productOptions": [{"name": o, "position": j + 1, "values": [{"name": x} for x in values[o]]}
                           for j, o in enumerate(opts)],
        "files": [{"id": FILES[f]} for f in p["files"]],
        "variants": [dict(variant(v, opts), **{"sku": None}) for v in p["variants"]],
    }
    # productSet takes sku on the variant, not inside inventoryItem
    for vin, v in zip(inp["variants"], p["variants"]):
        vin["sku"] = v["sku"]
        vin["inventoryItem"].pop("sku")
    calls.append(f'p{i}: productSet(synchronous:true,input:{gql(inp)})'
                 "{product{id handle variants(first:50){nodes{id sku}}} userErrors{field message}}")
print(write("pdoc", calls), "product documents")
