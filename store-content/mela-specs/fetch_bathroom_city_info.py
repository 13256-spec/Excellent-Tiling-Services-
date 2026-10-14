import json,re,html,os,subprocess
S=os.path.dirname(os.path.abspath(__file__))
res=json.load(open(S+'/match.json'))
hs=sorted({h for r in res for h in r['bc']})
os.makedirs(S+'/bc/pages',exist_ok=True)
info={}
def clean(t):
    t=re.sub(r'<(script|style|noscript|svg)[^>]*>.*?</\1>','',t,flags=re.S)
    t=re.sub(r'<(br|/p|/li|/tr|/h\d|/div|/summary|/details|/dd|/dt)[^>]*>','\n',t); t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(t)
    t=re.sub(r'[ \t\xa0]+',' ',t); return re.sub(r'\n\s*\n+','\n',t)
for h in hs:
    fn=f'{S}/bc/pages/{h}.html'
    if not os.path.exists(fn) or os.path.getsize(fn)<20000:
        subprocess.run(['curl','-sS','-A','Mozilla/5.0',f'https://bathroom-city.com.au/products/{h}','-o',fn])
    raw=open(fn,encoding='utf-8',errors='ignore').read()
    t=clean(raw)
    i=t.find('Product Information'); j=t.find('FAQs',i) if i>=0 else -1
    blk=t[i:j] if i>=0 else ''
    blk=blk.replace('Product Information \n Product information\n','').replace(' Warranty \n Warranty','')
    lines=[l.strip() for l in blk.split('\n') if l.strip()]
    kv=[];notes=[]
    for l in lines:
        m=re.match(r'([A-Za-z /&()-]{2,40}):\s*(.+)',l)
        if m: kv.append([m.group(1).strip(),m.group(2).strip()])
        else: notes.append(l)
    # spec sheet image under Product Specification
    k=raw.find('Product Specification'); sheet=None
    if k>=0:
        mm=re.search(r'(?:href|src)="(//bathroom-city\.com\.au/cdn/shop/files/[^"]+)"',raw[k:k+4000])
        if mm and 'Warranty' not in mm.group(1): sheet='https:'+mm.group(1)
    info[h]={'kv':kv,'notes':notes,'sheet':sheet}
json.dump(info,open(S+'/bc/info.json','w'),indent=1,ensure_ascii=False)
print('pages',len(hs),'with info',sum(1 for v in info.values() if v['kv']),'with sheet',sum(1 for v in info.values() if v['sheet']))
from collections import Counter
c=Counter(k for v in info.values() for k,_ in v['kv']); print(c.most_common(60))
