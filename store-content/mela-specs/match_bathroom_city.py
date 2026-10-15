import json,glob,re,html,os,subprocess,sys
S=os.path.dirname(os.path.abspath(__file__))
ours=[n for f in sorted(glob.glob(S+'/ours/page*.json')) for n in json.load(open(f))['data']['products']['nodes']]
sku=json.load(open(S+'/bc/bc_sku_to_handle.json')); bc=json.load(open(S+'/bc/bc_mela.json'))
def norm(s): return (s or '').strip().upper()
def tok(t):
    t=re.sub(r'\bMELA\b|[-–]',' ',t.upper()); t=re.sub(r'\bMIRROR CABINET WITH DOORS\b','MIRROR CABINET',t)
    return tuple(sorted(w for w in re.split(r'[^A-Z0-9]+',t) if w))
bytitle={}
for h,p in bc.items(): bytitle.setdefault(tok(p['title']),[]).append(h)
res=[]
for o in ours:
    hs=[]; how=''
    for v in o['variants']['nodes']:
        k=norm(v['sku'])
        if k in sku and sku[k] not in hs: hs.append(sku[k])
    if hs: how='sku'
    else:
        # title w/ variant option
        for v in o['variants']['nodes']:
            opts='' if v['title'] in ('Default','Default Title') else ' '+v['title'].replace('/',' ')
            m=bytitle.get(tok(o['title']+opts))
            if m and len(m)==1 and m[0] not in hs: hs.append(m[0])
        if hs: how='title'
    res.append({'handle':o['handle'],'title':o['title'],'type':o['productType'],'bc':hs,'how':how})
json.dump(res,open(S+'/match.json','w'),indent=1)
n=len(res); m=sum(1 for r in res if r['bc']); print('ours',n,'matched',m,'by sku',sum(1 for r in res if r['how']=='sku'))
print('UNMATCHED:'); [print('  ',r['type'],'|',r['title']) for r in res if not r['bc']]
