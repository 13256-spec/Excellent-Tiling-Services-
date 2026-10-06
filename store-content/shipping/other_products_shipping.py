"""Shipping record and Shopify upload files for every product that isn't Roberts Designs (6 Oct 2026).

Bathroom City (MELA), tiles, BAT / Panther / RLA / Click. Input: a Shopify bulk export (JSONL) of all products.
Weight and box come from estimate_weights.py (size from title / variant / description, weight from material);
where Shopify already holds a different weight (ceramic wall tiles 15 kg/m2, mosaic sheets 2 kg) the Shopify
weight is kept. Australia Post only (owner, 6 Oct 2026): parcel if it fits Australia Post
(22 kg, 105 cm, 0.25 m3), otherwise Perth delivery / pickup only. Tiles are always Perth delivery / pickup.

Outputs (next to this script): other-products-shipping-2026-10-06.csv, plus JSONL upload files in the
directory given as the second argument.
"""
import csv, html, importlib.util, json, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
DANGEROUS = ('SynSafe Acid',)
AU_BANDS = [(1, 15), (3, 20), (5, 29), (10, 39), (22, 59), (44, 109), (100, 179)]


def au_price(kg):
    return next((p for top, p in AU_BANDS if kg <= top), None)


def main(src, outdir):
    spec = importlib.util.spec_from_file_location('ew', os.path.join(HERE, 'estimate_weights.py'))
    ew = importlib.util.module_from_spec(spec); spec.loader.exec_module(ew)
    P, V = {}, []
    for line in open(src):
        o = json.loads(line)
        (V.append(o) if '__parentId' in o else P.__setitem__(o['id'], o))
    for v in V:
        P[v['__parentId']].setdefault('vs', []).append(v)

    rows, prods = [], collections.OrderedDict()
    for p in sorted(P.values(), key=lambda p: (p['productType'], p['title'])):
        if any(t.startswith('ship-') for t in p['tags']):
            continue  # Roberts products: done by roberts_shipping_record.py
        p['description'] = html.unescape(re.sub('<[^>]+>', ' ', p.get('descriptionHtml') or ''))
        for v in p.get('vs', []):
            kg, box, basis, note = ew.estimate(p, v)
            cur = (v['inventoryItem']['measurement']['weight'] or {}).get('value')
            if cur:
                kg = float(cur)
            dims = sorted(box, reverse=True)
            cubic = dims[0] * dims[1] * dims[2] / 4000
            method = 'parcel' if ew.method(kg, dims, p['productType']) == 'auspost' else 'local'
            dg = any(d in p['title'] for d in DANGEROUS)
            charge = max(kg, cubic)
            rows.append({
                'product': p['title'], 'variant': '' if v['title'] == 'Default Title' else v['title'],
                'sku': v['sku'] or '', 'vendor': p['vendor'], 'type': p['productType'], 'status': p['status'].lower(),
                'price': v['price'], 'weight_kg': f'{kg:.2f}', 'box_cm': 'x'.join(map(str, dims)),
                'cubic_kg': f'{cubic:.1f}', 'chargeable_kg': f'{charge:.1f}',
                'ship_method': method,
                'carrier': 'Australia Post' if method == 'parcel' else 'Perth delivery / pickup only',
                'est_ship_au': f'${au_price(charge)}' if method == 'parcel' else 'Perth delivery / pickup only',
                'international': 'Australia Post International' if method == 'parcel' and charge <= 10 and not dg else 'no',
                'dangerous_goods': 'yes (road only, no air or overseas)' if dg else '',
                'basis': basis, 'note': note, 'product_id': p['legacyResourceId'],
                'variant_id': v['id'], 'inventory_item_id': v['inventoryItem']['id'],
            })
            prods.setdefault(p['id'], []).append(rows[-1])

    with open(os.path.join(HERE, 'other-products-shipping-2026-10-06.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)

    # product tags
    tags_out, mixed = [], []
    for pid, vs in prods.items():
        methods = {v['ship_method'] for v in vs}
        t = []
        if 'parcel' in methods: t.append('ship-parcel')
        if methods == {'local'}: t.append('ship-local-only')
        if methods == {'parcel', 'local'}:
            mixed += [v['sku'] for v in vs if v['ship_method'] == 'local']
        if any(v['dangerous_goods'] for v in vs): t.append('ship-dangerous-goods')
        par = [v for v in vs if v['ship_method'] == 'parcel']
        if par and all(float(v['cubic_kg']) > 1.5 * float(v['weight_kg']) and float(v['cubic_kg']) >= 3 for v in par):
            t.append('ship-bulky')
        tags_out.append((pid, vs[0]['product'], t))
    with open(os.path.join(HERE, 'other-products-shipping-tags.csv'), 'w', newline='') as f:
        w = csv.writer(f, lineterminator='\n'); w.writerow(['product_id', 'product', 'tags'])
        for pid, name, t in tags_out: w.writerow([pid.split('/')[-1], name, ' '.join(t)])

    with open(os.path.join(outdir, 'metafields.jsonl'), 'w') as f:
        for r in rows:
            f.write(json.dumps({'metafields': [{'ownerId': r['variant_id'], 'namespace': 'shipping', 'key': 'box_size',
                                                'type': 'single_line_text_field',
                                                'value': r['box_cm'].replace('x', ' x ') + ' cm'}]}) + '\n')
    with open(os.path.join(outdir, 'tags.jsonl'), 'w') as f:
        for pid, _, t in tags_out:
            f.write(json.dumps({'id': pid, 'tags': t}) + '\n')
    print(len(rows), 'variants,', len(tags_out), 'products')
    print(collections.Counter(' '.join(t) for _, _, t in tags_out))
    print('mixed products, local-only SKUs:', ' '.join(mixed))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
