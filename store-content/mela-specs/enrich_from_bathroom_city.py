import json,glob,re,html,os
S=os.path.dirname(os.path.abspath(__file__))
ours=[n for f in sorted(glob.glob(S+'/ours/page*.json')) for n in json.load(open(f))['data']['products']['nodes']]
bc=json.load(open(S+'/bc/bc_mela.json')); info=json.load(open(S+'/bc/info.json'))
MIRRORS=set(json.load(open('/home/user/Excellent-Tiling-Services-/store-content/mirrors/ids.json')))
def key(s): 
    s=re.sub(r'[^A-Z0-9]','',(s or '').upper()); return s[3:] if s.startswith('KIT') else s
bysku={}
for h,p in bc.items():
    for v in p['variants']:
        if v['sku']: bysku.setdefault(key(v['sku']),[]).append(h)
def tok(t): return set(w for w in re.split(r'[^A-Z0-9]+',re.sub(r'\bMELA\b',' ',t.upper())) if w)
MANUAL={'TRITON.7700D':'TRITON.770D'}
def find(sku,title,vtitle):
    k=key(MANUAL.get(sku,sku))
    if k in bysku: return bysku[k][0]
    for kk,hs in bysku.items():
        if k.startswith(kk) and len(k)-len(kk)<=2: return hs[0]
    opts='' if vtitle in ('Default','Default Title') else ' '+vtitle.replace('/',' ')
    t=tok(title+opts); best=(0,None)
    for h,p in bc.items():
        b=tok(p['title']); j=len(t&b)/len(t|b)
        if j>best[0]: best=(j,h)
    return best[1] if best[0]>=0.75 else None
def normv(s): s=s.lower().replace('*','x').replace('×','x'); return re.sub(r'\s+|mm','',s)
def txt(h): return html.unescape(re.sub(r'<[^>]+>',' ',h or ''))
SKIP_KEYS={'Model Name','Model Number','Please Note'}
SKIP_LABELS={'mela-morris-frameless-corner-shower-screen':{'Dimensions'}}  # BC's 900x900 page carries the 900x1000 dims
LABEL={'Materials':'Material','Product Dimensions':'Dimensions','Product DImensions':'Dimensions','Dimension':'Dimensions','WELS Star Rating':'WELS rating','WELS Rating':'WELS rating','Litres Per Minute':'Flow rate','Cartridge Size (mm)':'Cartridge','Cartridge Size':'Cartridge','WELS Registration No':'WELS registration','IP Rate':'IP rating','Type & Mount':'Type and mount','Bottom Inlet':'Bottom inlet','Rear Entry':'Rear entry','S Trap':'S trap','P Trap':'P trap'}
NOTE_OK=re.compile(r'include|tolerance|waste|overflow|pre-assembled|flush',re.I)
NOTE_BAD=re.compile(r'colour variation|screen settings|team is always|check your items|prior to purchase|sold separately\.$',re.I)
out=[]
for o in ours:
    if o['id'] in MIRRORS: continue
    pairs=[]
    for v in o['variants']['nodes']:
        h=find(v['sku'],o['title'],v['title'])
        if h and h not in [p[1] for p in pairs]: pairs.append((v['title'],h))
    if not pairs: out.append({'handle':o['handle'],'title':o['title'],'status':'unmatched'}); continue
    ourtxt=normv(txt(o['descriptionHtml']))
    def overlap(n):
        w=[x for x in re.findall(r'[a-z0-9]+',n.lower()) if len(x)>2]
        return sum(1 for x in w if x in ourtxt)/max(1,len(w))
    def seen(v): return normv(v) in ourtxt or normv(re.sub(r'\b(gloss|matt)\s+','',v,flags=re.I)) in ourtxt or overlap(v)>=0.7
    merged={}  # label -> {value: [variant titles]}
    notes=[]
    for vt,h in pairs:
        if h not in info: continue
        for k,val in info[h]['kv']:
            if k in SKIP_KEYS: continue
            lab=LABEL.get(k,k); val=val.replace('*',' × ').replace('  ',' ').strip()
            merged.setdefault(lab,{}).setdefault(val,[]).append(vt)
        ns=info[h]['notes']; i=0
        while i<len(ns):
            n=ns[i]; i+=1
            if re.search(r'includes?( the following)?:?$',n,re.I):
                items=[]
                while i<len(ns) and not re.search(r'^(important|please|warranty|note|water inlet)',ns[i],re.I) and len(ns[i])<120:
                    items.append(ns[i].strip()); i+=1
                if items:
                    n='Package includes: '+'; '.join(items)
                else: continue
            if NOTE_OK.search(n) and not NOTE_BAD.search(n) and n not in [x[0] for x in notes] and len(n)<400: notes.append((n,vt))
    lines=[]
    nvar=len(o['variants']['nodes'])
    for lab,vals in merged.items():
        if lab in SKIP_LABELS.get(o['handle'],()): continue
        new={v:vt for v,vt in vals.items() if not seen(v)}
        if not new: continue
        if len(vals)==1 or lab=='Colour':
            v=', '.join(new) if lab=='Colour' else list(new)[0]
            if lab=='Colour' and len(vals)>1: lab='Colours'
            lines.append((lab,v))
        else:
            for v,vt in new.items():
                lines.append((lab,f"{v} ({', '.join(t for t in vt if t not in ('Default','Default Title'))})" if nvar>1 else v))
    pk=[x for x in notes if x[0].startswith('Package includes')]
    notes=[(f"Package includes ({vt}): {n[len('Package includes: '):]}" if len(pk)>1 and n.startswith('Package includes') else n) for n,vt in notes]
    notes=[n for n in notes if normv(n) not in ourtxt and overlap(n)<0.7]
    add='' if not lines and not notes else '<h4>More details</h4><ul>'+''.join(f'<li><strong>{html.escape(l)}:</strong> {html.escape(v)}</li>' for l,v in lines)+''.join(f'<li>{html.escape(n)}</li>' for n in notes)+'</ul>'
    # metafields
    have={m['key'] for m in o['metafields']['nodes']}
    mf={}
    single=lambda lab: list(merged[lab]) [0] if lab in merged and len(merged[lab])==1 else None
    for lab,k in [('Material','material'),('WELS rating','wels_rating'),('Flow rate','flow_rate'),('Cartridge','cartridge'),('WELS registration','wels_registration')]:
        v=single(lab)
        if v and k not in have: mf[k]=v
    d=single('Dimensions')
    if d and not {'width_mm','height_mm','depth_mm'}&have:
        m=re.findall(r'(\d{2,4})\s*\((W|D|H|L)\)',d)
        axes={a for _,a in m}
        if m and len(d)<40 and not ({'L','W'}<=axes):
            for n,a in m: mf[{'W':'width_mm','L':'width_mm','D':'depth_mm','H':'height_mm'}[a]]=int(n)
    if 'range' not in have:
        m=re.match(r'MELA\s+([A-Z]+)',o['title'])
        if m and m.group(1) not in ('POP',): mf['range']='MELA '+m.group(1)
    if not add and not mf: out.append({'handle':o['handle'],'title':o['title'],'status':'nothing-new','bc':[h for _,h in pairs]}); continue
    old_html=o['descriptionHtml']
    if any(l=='Dimensions' for l,_ in lines): old_html=re.sub(r'<li>\s*Approx\.[^<]*</li>\s*','',old_html)
    out.append({'handle':o['handle'],'id':o['id'],'title':o['title'],'status':'update','bc':[h for _,h in pairs],'old':old_html,'add':add,'metafields':mf})
json.dump(out,open(S+'/enrich.json','w'),indent=1,ensure_ascii=False)
from collections import Counter; print(Counter(r['status'] for r in out))
print('unmatched:',[r['title'] for r in out if r['status']=='unmatched'])
print('nothing-new:',[r['title'] for r in out if r['status']=='nothing-new'])
