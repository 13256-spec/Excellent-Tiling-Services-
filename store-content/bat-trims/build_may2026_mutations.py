"""Write the GraphQL documents that add may2026-additions.json to Shopify.

  python3 build_may2026_mutations.py OUTDIR

OUTDIR/vdocNN.graphql  productVariantsBulkCreate for new variants on existing products
OUTDIR/pdocNN.graphql  productSet for the new products (ACTIVE)
Each document stays under Shopify's 16,384 character limit.
"""
import json
import os
import sys

from gqlgen import gql, product_set, variant, write_docs

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
A = json.load(open("may2026-additions.json"))
IDS = json.load(open("shopify-product-ids.json"))
FILES = json.load(open("shopify-file-ids-may2026.json"))

calls, k = [], 0
for handle, vs in A["variants"].items():
    opts = list(vs[0]["options"])
    for i in range(0, len(vs), 25):
        chunk = [variant(v, opts) for v in vs[i:i + 25]]
        calls.append(f'v{k}: productVariantsBulkCreate(productId:"{IDS[handle]}",strategy:DEFAULT,variants:{gql(chunk)})'
                     "{productVariants{id sku} userErrors{field message}}")
        k += 1
print(write_docs(out, "vdoc", calls), "variant documents,", k, "calls")

calls = []
for i, p in enumerate(A["products"]):
    calls.append(f'p{i}: productSet(synchronous:true,input:{gql(product_set(p, FILES))})'
                 "{product{id handle variants(first:50){nodes{id sku}}} userErrors{field message}}")
print(write_docs(out, "pdoc", calls), "product documents")
