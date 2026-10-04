import json,glob,re
rows=json.load(open('plan.json'))
bc=[p for f in sorted(glob.glob('bc_*.json')) for p in json.load(open(f))['products'] if p['vendor'].upper()=='MELA']
bytitle={p['title'].upper().replace('  ',' '):p for p in bc}
def T(t): return bytitle.get(('MELA - '+t).upper())
fz=json.load(open('fuzzy.json'))
REJECT=['Gooseneck Sink Mixer','Wall Mixer with Diverter','FLOVA 800','Corner Glass Shelf','Bath Pop Up Waste','Shower Head','VINA LED','CLARK 750 Wall Hung Vanity with Doors','CLARK 1200 Wall Hung Vanity with Drawers','CLARK 1500 Double Wall Hung Vanity with Doors','CLARK 1500 Double Wall Hung Vanity with Drawers']
m={}
for vid,score,prod,var,bt,_,_ in fz:
    if any(k in prod for k in REJECT[:7]) or prod in ['MELA '+x for x in REJECT[7:]]: continue
    if prod=='MELA CLARK 1800 Double Wall Hung Vanity with 4 Drawers' and var=='Sorrento Oak': continue
    m[vid]=bytitle[bt.upper().replace('  ',' ')]
for r in rows:
    if r['action']=='update' or r['vid'] in m: continue
    p,v=r['product'],r['variant']; hit=None
    mm=re.match(r'MELA CLASSIC (\d+) Matt White Wall Hung Vanity with 2 Drawers',p)
    if mm: hit=T(f"{v.upper()} {mm.group(1)} Matt White Wall Hung Vanity with Drawers")
    lay={'MELA CLARK 750 Wall Hung Vanity with Doors':'CLARK 750 {c} Wall Hung Vanity with 2 Doors','MELA CLARK 1200 Wall Hung Vanity with Drawers':'CLARK 1200 {c} Wall Hung Vanity with 4 Drawers',
         'MELA CLARK 1500 Double Wall Hung Vanity with Doors':'CLARK 1500 {c} Wall Hung Vanity with 4 Doors','MELA CLARK 1500 Double Wall Hung Vanity with Drawers':'CLARK 1500 {c} Wall Hung Vanity with 4 Drawers',
         'MELA CLARK 1200 Wall Hung Vanity with 2 Drawers & Single Side Shelves':'CLARK 1200 {c} Wall Hung Vanity with 2 Drawers and Open Shelves','MELA CLARK 1200 Wall Hung Vanity with 2 Drawers & Dual Side Shelves':'CLARK 1200 {c} Wall Hung Vanity with 2 Drawers and 2 Open Shelves'}
    if p in lay: hit=T(lay[p].format(c=v))
    if p=='MELA CLARK 600 Wall Hung Vanity with Doors': hit=T('CLARK 600 Gloss White Wall Hung Vanity with 2 Doors')
    if p=='MELA MORRIS Frameless Shower Panel':
        mm=re.match(r'(\d+) x 2000mm( Curved)?',v)
        if mm: hit=T(f"MORRIS {mm.group(1)}mm{' Curved' if mm.group(2) else ''} Frameless Shower Panel")
    if p=='MELA MORRIS Shower Screen U Bracket':
        hit=T('Shower Screen U Brackets '+{'Matt Black':'Black'}.get(v,v))
    if p=='MELA PORTER Mirror Cabinet':
        sz=v.split('mm')[0]; hit=T(f'PORTER {sz} Walnut Mirror Cabinet')
    if p=='MELA TRITON 770 Double Sink': hit=T('TRITON 770D Stainless Steel Sink')
    if p=='MELA TRITON 1200 Double Sink': hit=T('TRITON 1200 Polish Stainless Steel Sink with Drainer')
    if hit: m[r['vid']]=hit
json.dump({k:v['id'] for k,v in m.items()},open('manual_map.json','w'))
print('extra matches',len(m))
for r in rows:
    if r['vid'] in m and r['status']=='ACTIVE': pass
missing=[(r['product'],r['variant']) for r in rows if r['action']!='update' and r['vid'] not in m and r['status']=='ACTIVE']
print('still unmatched active',len(missing))
for x in missing: print('  ',x)
