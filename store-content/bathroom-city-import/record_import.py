"""Write the created products into the master price list, the SEO record and a JSON log."""
import json, csv, glob, os
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(H + '/../..')
P = json.load(open(H + '/new-products.json'))
res = {}
for f in sorted(glob.glob(H + '/results/results-*.json')):
    for r in json.load(open(f)):
        if 'product_id' in r: res[r['index']] = r
rows = list(csv.reader(open(ROOT + '/store-content/pricing/store-pricing-2026-10-03.csv')))
have = {(r[0], r[1]) for r in rows[1:]}
seo = json.load(open(ROOT + '/seo/product-seo.json')); seo_ids = {s['id'] for s in seo}
log = []
n = 0
for i, p in enumerate(P):
    if i not in res: continue
    inp = p['input']; r = res[i]
    for k, (m, v) in enumerate(zip(p['members'], inp['variants'])):
        vt = v['optionValues'][0]['name'] if v['optionValues'][0]['name'] != 'Default Title' else 'Default'
        if (inp['title'], vt) in have: continue
        vid = r['variant_ids'].get(v.get('sku')) or r['variant_ids'].get(vt) or r['variant_ids'].get(str(k+1)) or ''
        rows.append([inp['title'], vt, v.get('sku', ''), 'MELA', inp['productType'], '', str(m['price']), str(p['band']) if p['band'] else '', f"{m['price']*(1-p['band']/100):.2f}" if p['band'] else '', f"{m['cost']:.2f}", 'estimate: list x (1 - SLIVER discount) / 1.1', f"{m['margin']:.1f}", '', 'Bathroom City', f"{m['bc_price']:g}", 'new 20 Oct 2026' + ('; ' + m['flag'] if m['flag'] else ''), vid, '', r['product_id'], ' '.join(inp['tags'])]); n += 1
    if r['product_id'] not in seo_ids:
        seo.append({'id': r['product_id'], 'title': inp['title'], 'status': 'ACTIVE', 'old_title': None, 'old_desc': None, 'seo_title': inp['seo']['title'], 'seo_desc': inp['seo']['description']})
    log.append({'id': r['product_id'], 'handle': r['handle'], 'title': inp['title'], 'type': inp['productType'], 'trade_band': p['band'], 'ship': p['ship'], 'collections': p['collections'], 'members': p['members']})
nv = json.load(open(H + '/new-variants.json'))
for v in nv:
    if (v['our_product'], v['finish']) in have: continue
    vt = (v['size'] + ' / ' if v.get('size') else '') + v['finish']
    rows.append([v['our_product'], vt, v['sku'], 'MELA', v['type'], '', str(v['price']), '', '', f"{v['cost']:.2f}", 'estimate: list x (1 - SLIVER discount) / 1.1', f"{v['margin']:.1f}", '', 'Bathroom City', f"{v['bc_price']:g}", 'new variant 20 Oct 2026', v.get('variant_id', ''), '', v['pid'], '']); n += 1
csv.writer(open(ROOT + '/store-content/pricing/store-pricing-2026-10-03.csv', 'w', newline='')).writerows(rows)
json.dump(seo, open(ROOT + '/seo/product-seo.json', 'w'), indent=1, ensure_ascii=False)
json.dump(log, open(H + '/created-products-2026-10-20.json', 'w'), indent=1, ensure_ascii=False)
print('price list rows added', n, '| products logged', len(log))
