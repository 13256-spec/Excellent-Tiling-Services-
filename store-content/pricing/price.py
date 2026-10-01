import json,glob,collections,re,math,csv
o=json.load(open('ours.json'))['data']['products']['nodes']
bc=[p for f in sorted(glob.glob('bc_*.json')) for p in json.load(open(f))['products'] if p['vendor'].upper()=='MELA']
norm=lambda s:re.sub(r'[\s\-_.]','',(s or '').upper())
bysku=collections.defaultdict(list)
for p in bc:
    for v in p['variants']:
        if v['sku']: bysku[norm(v['sku'])].append((p,v))
MAN=json.load(open('manual_map.json')) if __import__('os').path.exists('manual_map.json') else {}
BCID={p['id']:p for p in bc}
def find(sku):
    n=norm(sku)
    cands=[n]
    if n.endswith('GM') and not n.endswith('LGM'): cands.append(n[:-2]+'LGM')
    cands+= [n+'CH', n[:-2] if n.endswith('CH') else None]
    for c in cands:
        if c and len(bysku.get(c,[]))==1: return bysku[c][0], c!=n
    return None,None
# supplier trade discount from the SLIVER sheet, by our product type
D={}
for t in ['Wall Hung Vanity','Double Wall Hung Vanity','Bathroom Tallboy']: D[t]=(0.25,'Vanity package')
for t in ['Above Counter Basin','Half Inset Basin','Semi Basin','Undermount Basin','Inset Basin']: D[t]=(0.30,'Basins')
for t in ['Basin Mixer','Kitchen Sink Mixer','Wall Mixer','Wall Mixer with Diverter','Wall Spout','Hand Shower Set','Combination Shower Set','Hand Shower','Shower Arm','Freestanding Bath Spout','Shower Head','Shower Hose','Bath Spout','Ceiling Shower Arm','Freestanding Bath Mixer']: D[t]=(0.40,'Tapware')
for t in ['Towel Rail','Shelf Holder','Soap Holder','Toilet Roll Holder','Bathroom Hook','Hand Towel Rail','Toilet Brush Holder','Bath Towel Shelf']: D[t]=(0.35,'Accessories')
for t in ['Mirror','Mirror Cabinet','LED Mirror']: D[t]=(0.25,'Mirrors / mirror cabinets')
D['Inset Bath']=(0.20,'Inset bath'); D['Freestanding Bath']=(0.40,'Free standing bath')
D['Back to Wall Bath']=(0.20,'Bath not on sheet – used lowest (20%)'); D['Corner Bath']=(0.20,'Bath not on sheet – used lowest (20%)')
for t in ['Shower Screen Fitting','Frameless Shower Panel','Corner Shower Screen']: D[t]=(0.40,'Shower screen')
for t in ['Toilet Suite','In Wall Cistern Toilet']: D[t]=(0.40,'Toilets')
D['Kitchen Sink']=(0.40,'Sinks')
for t in ['Pop Up Waste','Bath Waste']: D[t]=(0.40,'Pop up waste')
LARGE=set(x.strip() for x in "Wall Hung Vanity, Double Wall Hung Vanity, Bathroom Tallboy, Back to Wall Bath, Corner Bath, Freestanding Bath, Inset Bath, Toilet Suite, In Wall Cistern Toilet, Corner Shower Screen, Frameless Shower Panel, Above Counter Basin, Inset Basin, Half Inset Basin, Semi Basin, Undermount Basin, Kitchen Sink, LED Mirror, Mirror, Mirror Cabinet".split(','))
UNDER=0.05; MINMARGIN=0.05
rows=[]
for p in o:
    for v in p['variants']['nodes']:
        r=dict(product=p['title'],variant=v['title'],status=p['status'],type=p['productType'],sku=v['sku'],pid=p['id'],vid=v['id'],inv=v['inventoryItem']['id'],
               old_price=float(v['price']),old_compare=v['compareAtPrice'],old_cost=(v['inventoryItem']['unitCost'] or {}).get('amount'))
        hit,alias=find(v['sku']) if v['sku'] else (None,None)
        if not hit and v['id'] in MAN: hit,alias=(BCID[MAN[v['id']]],BCID[MAN[v['id']]]['variants'][0]),'name'
        d,cat=D.get(p['productType'],(None,None))
        r.update(category=cat,disc=d)
        if not hit or d is None:
            r['action']='no match on Bathroom City' if not hit else 'no discount category'; rows.append(r); continue
        bp,bv=hit; bprice=float(bv['price']); blist=max(bprice,float(bv['compare_at_price'] or 0))
        cost=round(blist*(1-d),2)
        band=0.10 if p['productType'] in LARGE else 0.05
        floor=cost*(1+MINMARGIN)/(1-band)
        target=bprice*(1-UNDER)
        new=math.floor(target) if target>=20 else math.floor(target*2)/2
        flag=''
        if new<floor:
            alt=math.floor(bprice)-1
            if alt>=cost*1.05 and alt*(1-band)>=cost and alt<bprice: new=alt; flag='$1 under BC sale price (thin margin)'
            else: new=math.ceil(floor); flag='BC sale price below our cost – not undercut'
        if new>r['old_price']:
            flag=('kept current price – it is BELOW the safe floor, review' if r['old_price']<floor else 'kept current price (already below target)')
            new=r['old_price']
        r.update(bc_title=bp['title'],bc_sku=bv['sku'],bc_price=bprice,bc_list=blist,alias=bool(alias),cost=cost,new_price=float(new),
                 margin=round((new-cost)/new*100,1),trade_margin=round((new*(1-band)-cost)/(new*(1-band))*100,1),flag=flag,action='update')
        rows.append(r)
json.dump(rows,open('plan.json','w'))
up=[r for r in rows if r['action']=='update']
print('variants',len(rows),'to update',len(up),collections.Counter(r['action'] for r in rows))
print('flags',collections.Counter(r['flag'] for r in up))
print('price changes: down',sum(r['new_price']<r['old_price'] for r in up),'up',sum(r['new_price']>r['old_price'] for r in up),'same',sum(r['new_price']==r['old_price'] for r in up))
print('old revenue-ish sum',round(sum(r['old_price'] for r in up)),'new',round(sum(r['new_price'] for r in up)))
print('margin min/median',min(r['margin'] for r in up),sorted(r['margin'] for r in up)[len(up)//2],'trade margin min',min(r['trade_margin'] for r in up))
for r in sorted(up,key=lambda r:r['new_price']/r['old_price'])[:6]+sorted(up,key=lambda r:-r['new_price']/r['old_price'])[:6]:
    print(f"{r['product'][:40]:40} {r['variant'][:14]:14} ours {r['old_price']:>8} BC {r['bc_price']:>8} list {r['bc_list']:>8} -> {r['new_price']:>8} cost {r['cost']:>8} {r['flag']}")
