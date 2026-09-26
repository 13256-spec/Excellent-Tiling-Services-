import json,glob,re
from collections import Counter
ours=[o for o in json.load(open('ours.json'))['data']['products']['nodes'] if o['vendor']=='MELA']
bc=[p for f in sorted(glob.glob('bc_*.json')) for p in json.load(open(f))['products'] if p['vendor'].upper()=='MELA']
SYN=[(r'\bmela\b',''),(r'\bmatt black\b','black'),(r'\blight gun metal\b','gunmetal'),(r'\bgun metal\b','gunmetal'),(r'\brobe hook\b','hook'),
     (r'\bfree standing\b','freestanding'),(r'\btwin combo\b','combination'),(r'\bpull-out\b','pull out'),(r'\bwith diverter\b','diverter'),
     (r'\bceiling shower arm\b','ceiling arm'),(r'\bbrackets\b','bracket'),(r'[()]',' '),(r'/',' '),(r'&',' and '),(r'-',' '),(r'\s+',' ')]
def toks(s):
    s=' '+s.lower()+' '
    for a,b in SYN: s=re.sub(a,b,s)
    return tuple(sorted(s.split()))
idx={}
for p in bc: idx.setdefault(toks(p['title']),[]).append(p)
res=[];st=Counter()
for o in ours:
    for v in o['variants']['nodes']:
        opts=[x['value'] for x in v['selectedOptions'] if x['value'] not in ('Default Title','Default')]
        k=toks(o['title']+' '+' '.join(opts))
        m=idx.get(k)
        if (not m) and not opts: m=None
        if m and len(m)>1: st['ambig']+=1; m=None
        st['match' if m else 'none']+=1
        m=m[0] if m else None
        res.append({'pid':o['id'],'vid':v['id'],'title':o['title'],'var':v['title'],'status':o['status'],'our_sku':v['sku'],'media':o['mediaCount']['count'],
                    'bc':m['title'] if m else None,'bc_sku':(m['variants'][0]['sku'] if m else None),'bc_imgs':[i['src'] for i in m['images']] if m else [],
                    'bc_alt':[i.get('alt') for i in m['images']] if m else []})
json.dump(res,open('mela_strict.json','w'))
print(st)
# products with 0 media: coverage
nomedia={}
for r in res:
    if r['media']==0: nomedia.setdefault((r['pid'],r['title'],r['status']),[]).append(r)
print('no-media products',len(nomedia))
for (pid,t,s),rs in nomedia.items():
    got=[r for r in rs if r['bc_imgs']]
    print(f"  {s[:1]} {t} | variants {len(rs)} matched {len(got)}", '' if got else ' <-- none')
live_nosku=[r for r in res if r['status']=='ACTIVE' and not r['our_sku']]
print('live variants missing sku',len(live_nosku),'fixable',sum(1 for r in live_nosku if r['bc_sku']))
for r in live_nosku: print('   ',r['title'],'|',r['var'],'=>',r['bc'],r['bc_sku'])
