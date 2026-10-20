"""After the products exist: print the GraphQL mutation documents that publish them to every channel, add them to
their manual collections (incl. trade-list-N) and put Perth-only items in the local delivery profile.
Usage: python3 post_import.py  -> writes post-mutations.json (list of {name, query, variables}) and prints a summary."""
import json, glob, os
H = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(H + '/new-products.json'))
res = {}
for f in sorted(glob.glob(H + '/results/results-*.json')):
    for r in json.load(open(f)):
        if 'product_id' in r: res[r['index']] = r
COL = {'bathroom-vanities': 301478707263, 'wall-hung-vanities': 301478740031, 'single-vanities': 301310804031, 'double-vanities': 301310836799, 'bathroom-storage-tallboys': 301478805567,
       'basins': 301310967871, 'above-counter-basins': 301479034943, 'inset-basins': 301479067711, 'undermount-basins': 301479100479, 'mirrors': 301310869567, 'led-mirrors': 301479428159,
       'mirror-cabinets': 301479460927, 'towel-rails': 301479657535, 'accessories': 301475954751, 'toilet-roll-holders': 301479690303, 'bathroom-hooks': 301479755839, 'soap-shelf-holders': 301479723071,
       'kitchen-laundry': 301479854143, 'sinks': 301479886911, 'bathroom-wastes': 301479788607, 'toilets': 301310935103, 'rimless-toilets': 301479362623, 'wall-faced-toilets': 301479329855,
       'shower-screens': 301479526463, 'frameless-shower-panels': 301479559231, 'tapware': 301310771263, 'kitchen-tapware': 301478969407, 'basin-mixers': 301478838335, 'wall-mixers': 301478871103,
       'spouts-outlets': 301479002175, 'shower-tapware': 301478936639, 'bath-tapware': 301478903871, 'trade-list-5': 301904298047, 'trade-list-10': 301904330815, 'trade-list-15': 301904363583,
       'trade-list-20': 301904396351, 'trade-list-25': 301904429119}
PUBS = [157691969599, 157692002367, 157692035135, 158454186047, 158458609727, 159373983807]
muts = []
pids = [res[i]['product_id'] for i in range(len(P)) if i in res]
# publish: 20 products per call
for k in range(0, len(pids), 20):
    q = 'mutation($pubs:[PublicationInput!]!){' + ' '.join(f'p{j}: publishablePublish(id:"{pid}", input:$pubs){{userErrors{{message}}}}' for j, pid in enumerate(pids[k:k+20])) + '}'
    muts.append({'name': f'publish-{k//20+1}', 'query': q, 'variables': {'pubs': [{'publicationId': f'gid://shopify/Publication/{p}'} for p in PUBS]}})
# collections
bycol = {}
for i, p in enumerate(P):
    if i not in res: continue
    for c in p['collections']: bycol.setdefault(c, []).append(res[i]['product_id'])
items = list(bycol.items())
for k in range(0, len(items), 8):
    q = 'mutation{' + ' '.join(f'c{j}: collectionAddProducts(id:"gid://shopify/Collection/{COL[c]}", productIds:{json.dumps(ids)}){{userErrors{{message}}}}' for j, (c, ids) in enumerate(items[k:k+8])) + '}'
    muts.append({'name': f'collections-{k//8+1}', 'query': q, 'variables': {}})
# delivery profile for local items
local = [vid for i, p in enumerate(P) if i in res and p['ship'] == 'local' for vid in res[i]['variant_ids'].values()]
for k in range(0, len(local), 80):
    muts.append({'name': f'delivery-{k//80+1}', 'query': f'mutation{{ deliveryProfileUpdate(id:"gid://shopify/DeliveryProfile/94703747135", profile:{{variantsToAssociate:{json.dumps(local[k:k+80])}}}){{profile{{id}} userErrors{{field message}}}} }}', 'variables': {}})
json.dump(muts, open(H + '/post-mutations.json', 'w'), indent=1)
print('products with results', len(pids), 'of', len(P), '| mutations:', [(m['name'], len(m['query'])) for m in muts])
print('collections:', {c: len(v) for c, v in bycol.items()}, '| local variants', len(local))
