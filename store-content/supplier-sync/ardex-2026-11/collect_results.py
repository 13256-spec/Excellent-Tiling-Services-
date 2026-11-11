"""Collect the productSet responses (scratchpad results/NNN.json) into ardex-created-2026-11-11.json and print the
follow-up payloads: product ids to publish, variant ids per delivery profile."""
import json, os, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
R = sys.argv[1]  # results dir
B = sys.argv[2]  # batches dir
payload = {x['slug']: x for x in json.load(open(os.path.join(HERE, 'ardex-2026-11-11.json')))}
created = {}
errors = []
for f in sorted(glob.glob(os.path.join(R, '*.json'))):
    n = os.path.basename(f)
    batch = json.load(open(os.path.join(B, n)))
    res = json.load(open(f))
    data = res.get('data') or res
    for j, slug in enumerate(batch['slugs']):
        r = data.get(f'p{j}')
        if not r or not r.get('product'):
            errors.append((n, slug, r and r.get('userErrors')))
            continue
        if r.get('userErrors'):
            errors.append((n, slug, r['userErrors']))
        p = r['product']
        created[slug] = {'id': p['id'], 'handle': p['handle'], 'title': p['title'],
                         'variants': [{'id': v['id'], 'sku': v['sku'], 'title': v['title']} for v in p['variants']['nodes']]}
# the two done by hand
extra = json.load(open(os.path.join(HERE, 'manual-created.json'))) if os.path.exists(os.path.join(HERE, 'manual-created.json')) else {}
created.update(extra)
missing = [s for s in payload if s not in created]
out = [{'slug': s, 'group': payload[s]['group'], 'ship': payload[s]['ship'], **created[s]} for s in payload if s in created]
json.dump(out, open(os.path.join(HERE, 'ardex-created-2026-11-11.json'), 'w'), indent=1)
print('created', len(out), 'variants', sum(len(x['variants']) for x in out), 'missing', missing, 'errors', errors)
ids = [x['id'] for x in out]
json.dump(ids, open('/tmp/claude-0/-home-user-Excellent-Tiling-Services-/6ea702dc-bcae-5876-b8d1-0ec2c29c9023/scratchpad/ardex/publish-ids.json', 'w'))
prof = {'local': [], 'dg': []}
for x in out:
    if x['ship'] in prof:
        prof[x['ship']] += [v['id'] for v in x['variants']]
json.dump(prof, open('/tmp/claude-0/-home-user-Excellent-Tiling-Services-/6ea702dc-bcae-5876-b8d1-0ec2c29c9023/scratchpad/ardex/profile-variants.json', 'w'))
print('local', len(prof['local']), 'dg', len(prof['dg']))
