"""Render v2 graphics from a copy file: python3 from_copy.py ../copy-week1.json -> out/<date>-<slot>.png
Photos: LIFE maps product-name keywords to a room photo in img/; otherwise the product's first store photo."""
import json,sys,os,re,subprocess,importlib.util
S=os.path.dirname(os.path.abspath(__file__))
spec=importlib.util.spec_from_file_location('b',os.path.join(S,'build2.py')); b=importlib.util.module_from_spec(spec)
sys.argv_saved=sys.argv; sys.argv=[sys.argv[0],'__none__']; spec.loader.exec_module(b); sys.argv=sys.argv_saved
CAT=json.load(open(os.path.join(S,'catalogue.json')))
LIFE=[('morgan dusk porcelain tile (living','dusk1.jpg','center 60%'),('brittany 1200','brittany1200.jpg','center 55%'),('brittany 600','brittany600.jpg','center 60%'),
('mia 450 oval mirror cabinet','miacab.jpg','center 40%'),('morgan dusk','dusk2.jpg','center 70%'),('time stone cinder','cinder.jpg','center'),
('time stone moon','moon.jpg','center'),('particle warm','particle.jpg','center'),('lava ash','ash.jpg','center'),
('porter','porter.jpg','center'),('mia 450 frameless','miaoval.jpg','center'),('morgan storm','storm.jpg','center'),
('paddy 750','paddy750.jpg','center'),('vera','vera.jpg','center'),('time stone charcoal','charcoal.jpg','center'),('cement grey','cementgrey.jpg','center'),('lava etna','etna.jpg','center'),('dusk porcelain tile (living','dusk1.jpg','center 60%')]
def photo(name):
    n=(name or '').lower()
    for k,f,pos in LIFE:
        if k in n and os.path.exists(os.path.join(S,'img',f)): return f,pos
    # fall back: product's own first image (or a named index "#2")
    best=None
    for p in CAT:
        t=p['title'].lower()
        if t and t in n or n and n in t: best=p; break
    if not best:
        words=[w for w in re.findall(r'[a-z0-9]+',n) if len(w)>2]
        sc=sorted(CAT,key=lambda p:-sum(w in p['title'].lower() for w in words)); best=sc[0]
    fn=f"p/{best['handle']}.jpg"
    if not os.path.exists(os.path.join(S,'img',fn)):
        os.makedirs(os.path.join(S,'img','p'),exist_ok=True)
        u=best['images'][0]['src']; subprocess.run(['curl','-s','-o',os.path.join(S,'img',fn),u+('&' if '?' in u else '?')+'width=1600'])
    return fn,'center'
def render(name,W,H,body):
    f=os.path.join(S,f'_{name}.html'); css=b.CSS.replace('W',str(W)+'px',1).replace('H',str(H)+'px',1)
    open(f,'w').write(f'<!doctype html><meta charset=utf-8><style>{css}</style>{body}')
    subprocess.run(['node',os.path.join(S,'shot.js'),f,os.path.join(S,'out',name+'.png'),str(W),str(H)],check=True); os.remove(f)
d=json.load(open(sys.argv[1])); made=[]
for e in d.get('main',[]):
    img,pos=photo(e.get('photo_product'))
    if e.get('layout')=='product':
        W,H,body=b.product(img,e.get('kicker',''),e.get('name',''),e.get('price',''),pre=e.get('pre',''),pos=pos)
    else:
        W,H,body=b.statement(img,e.get('headline',''),e.get('sub',''),pos=pos)
    n=f"{e['date']}-main"; render(n,W,H,body); made.append(n)
for e in d.get('stories',[]):
    img,pos=photo(e.get('photo_product'))
    W,H,body=b.statement(img,e.get('headline',''),e.get('sub',''),pos=pos,H=1920,strip=600,foot='Link in bio')
    body=body.replace('class=h>','class=h style="font-size:86px">').replace('class=s>','class=s style="font-size:40px;max-width:940px">').replace('class=u ','class=u style="font-size:30px" ',0)
    n=f"{e['date']}-story"; render(n,W,H,body); made.append(n)
print('\n'.join(made))
for e in d.get('lunch',[]):
    h=e['url'].rstrip('/').rsplit('/',1)[1]; p=next((x for x in CAT if x['handle']==h),None)
    if not p: print('NO PRODUCT',h); continue
    pr=sorted({float(v['price']) for v in p['variants'] if v['available']})
    price=f"${pr[0]:,.2f}".replace('.00','')+('/m²' if p['product_type']=='Tile' else '')
    name=re.sub(r'^MELA\s+','',p['title']); name=re.sub(r'\s+(Porcelain )?Tile$','',name) if p['product_type']=='Tile' else name
    pt=p['product_type'] if p['product_type']!='Tile' else 'Porcelain tile'; pt=pt[:1]+pt[1:].lower().replace('led','LED')
    kicker=('MELA · ' if p['vendor']=='MELA' else '')+pt
    OVR={'mela-clark-600-wall-hung-vanity-with-doors':'p/clark600-alt.jpg'}
    fn=OVR.get(h) or (f"p/{h}.jpg" if os.path.exists(os.path.join(S,'img',f"p/{h}.jpg")) else f"p/{h}.png")
    if p['product_type']=='Tile':
        lf,lpos=photo(p['title'])
        if not lf.startswith('p/'): fn=lf
    long=len(name)>30
    W,H,body=b.product(fn,kicker,name,price,pre='from' if len(pr)>1 else '',pos='center',strip=300 if long else 250)
    if long: body=body.replace('class=n>','class=n style="font-size:36px">')
    body=body.replace('class=ph ','class=ph style="background:#fff;object-fit:contain;padding:40px" ',1) if fn.endswith('.png') else body
    n=f"{e['date']}-lunch"; render(n,W,H,body); made.append(n)
print('\n'.join(made[-len(d.get('lunch',[])):]))
