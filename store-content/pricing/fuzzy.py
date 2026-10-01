import json,glob,re,collections
rows=json.load(open('plan.json'))
bc=[p for f in sorted(glob.glob('bc_*.json')) for p in json.load(open(f))['products'] if p['vendor'].upper()=='MELA' and 'OPTION SET' not in p['title'].upper()]
SYN=[(r'\bmela\b',' '),(r'\bmatt black\b','black'),(r'\blight gun metal\b','gunmetal'),(r'\bgun metal\b','gunmetal'),(r'\bmatt white\b','white'),
 (r'\bfree standing\b','freestanding'),(r'\binsert\b','inset'),(r'(\d+)\s*mm\b',r'\1'),(r'(\d+)\s*x\s*(\d+)',r'\1x\2'),(r'\bframed\b','frame'),(r'\bframe\b','frame'),
 (r'\bdoors?\b','door'),(r'\bdrawers?\b','drawer'),(r'\bshelves\b','shelf'),(r'\bpolished edge\b',' '),(r'\bwith\b',' '),(r'\band\b',' '),(r'&',' '),(r'[()/,\-–]',' ')]
COL={'black','white','gunmetal','chrome','nickel','brass','copper','walnut','snafell','sorrento','oak','dracula','gloss','brushed','polished','hampton','pastel','shaker','stainless','steel'}
def toks(s):
    s=' '+s.lower()+' '
    for a,b in SYN: s=re.sub(a,b,s)
    return set(s.split())
bct=[(p,toks(p['title'])) for p in bc]
out=[]
for r in rows:
    if r['action']=='update': continue
    t=toks(r['product']+' '+(r['variant'] if r['variant'] not in ('Default','Default Title') else ''))
    nums={x for x in t if re.fullmatch(r'[\dx]+',x)}; cols=t&COL
    best=[]
    for p,bt in bct:
        bn={x for x in bt if re.fullmatch(r'[\dx]+',x)}
        if bn!=nums or (bt&COL)!=cols: continue
        j=len(t&bt)/len(t|bt)
        best.append((j,p))
    best.sort(key=lambda x:-x[0])
    if best and best[0][0]>=0.6 and (len(best)==1 or best[1][0]<best[0][0]):
        out.append((r['vid'],round(best[0][0],2),r['product'],r['variant'],best[0][1]['title'],best[0][1]['variants'][0]['price'],best[0][1]['variants'][0]['compare_at_price']))
for x in out: print(x[1],'|',x[2],'|',x[3],'=>',x[4],x[5],x[6])
print(len(out))
json.dump(out,open('fuzzy.json','w'))
