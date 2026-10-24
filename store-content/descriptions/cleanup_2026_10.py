"""Strip store-operations sentences (delivery, pickup, 'buy online from ETS', stock lines) from descriptions the
writers are not touching. Owner, 24 Oct 2026: descriptions must be customer-facing product copy only."""
import json,re,html,glob,collections
todo=set()
for f in glob.glob('/home/user/Excellent-Tiling-Services-/store-content/descriptions/todo-*.json'):
    todo|={r['id'] for r in json.load(open(f))}
DROP=[r'^\s*Delivery:', r'^\s*Shipping:', r'\bBuy (online|the .{0,80}?)\s.*?from Excellent Tiling Services', r'Order through Excellent Tiling Services',
      r'Available from (our Maddington showroom|Excellent Tiling Services)', r'Perth local delivery or pick', r'Heavy machine: Perth',
      r'Buy online or pick up', r'^\s*Browse more ', r'Contact Excellent Tiling Services for', r'require supplier confirmation',
      r'is in stock at our Maddington showroom', r'Confirm the layout and number of panels for delivery', r'^\s*More details\s*$']
def plain(s): return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',s))).strip()
def drop(t): return any(re.search(p,t,re.I) for p in DROP)
def clean(h):
    removed=[]
    # 1. whole <li> items
    def li(m):
        t=plain(m.group(0))
        if drop(t): removed.append(t); return ''
        return m.group(0)
    h=re.sub(r'<li\b[^>]*>.*?</li>',li,h,flags=re.S)
    # 2. whole <p> / <h3>/<h4> blocks
    def blk(m):
        t=plain(m.group(0))
        if drop(t): removed.append(t); return ''
        # 3. sentences inside a paragraph
        inner=m.group(2); sents=re.split(r'(?<=[.!?])\s+(?=[A-Z])',inner); keep=[]
        for s in sents:
            ps=plain(s)
            if ps and drop(ps): removed.append(ps)
            else: keep.append(s)
        return m.group(1)+' '.join(keep)+m.group(3)
    h=re.sub(r'(<(?:p|h[2-6])\b[^>]*>)(.*?)(</(?:p|h[2-6])>)',blk,h,flags=re.S)
    h=re.sub(r', or see the samples in our Maddington showroom','',h)
    h=re.sub(r'<ul>\s*</ul>|<p>\s*</p>','',h)
    h=re.sub(r'(<h[2-6][^>]*>[^<]*</h[2-6]>)\s*(?=<h[2-6]|$)','',h)  # heading left with nothing under it
    return h.strip(),removed
out=[]
for l in open('dl/products.jsonl'):
    d=json.loads(l)
    if 'id' in d and '/Product/' in d['id'] and d['id'] not in todo and d['descriptionHtml']:
        new,rem=clean(d['descriptionHtml'])
        if rem and new!=d['descriptionHtml']:
            out.append(dict(id=d['id'],handle=d['handle'],title=d['title'],vendor=d['vendor'],old=d['descriptionHtml'],new=new,removed=rem,words_after=len(plain(new).split())))
json.dump(out,open('cleanup-2026-10-24.json','w'),indent=1)
print('products cleaned',len(out),'segments removed',sum(len(o['removed']) for o in out))
print('left under 40 words:',[(o['title'],o['words_after']) for o in out if o['words_after']<40][:15])
leftover=collections.Counter()
for o in out:
    for kw in ['deliver','shipping','showroom','excellent tiling','in stock','pick up','pickup']:
        if kw in plain(o['new']).lower(): leftover[kw]+=1
print('leftover keywords after clean:',leftover)
for o in out[:3]+out[200:202]: print('\n---',o['title'],'\nREMOVED:',o['removed'],'\nNEW:',plain(o['new'])[:400])
# batches of 20 for productUpdate
B=[out[i:i+20] for i in range(0,len(out),20)]
for k,b in enumerate(B):
    q="mutation("+",".join(f"$d{i}:String!" for i in range(len(b)))+") { "+" ".join(f'u{i}: productUpdate(product:{{id:"{o["id"]}", descriptionHtml:$d{i}}}) {{ product {{ id }} userErrors {{ field message }} }}' for i,o in enumerate(b))+" }"
    json.dump({"query":q,"variables":{f"d{i}":o["new"] for i,o in enumerate(b)}},open(f'cl{k}.json','w'))
print('batches',len(B))
