"""ETS social graphics v2: photo-led, catalogue strip. python3 build2.py [name-prefix...] -> out/<name>.png"""
import os,sys,subprocess
S=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(S,'out'); os.makedirs(OUT,exist_ok=True)
CSS='''@font-face{font-family:A;src:url(archivo.woff2);font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box}
body{width:W;height:H;font-family:A,sans-serif;color:#1F3153;background:#F4F5F3;overflow:hidden;position:relative;-webkit-font-smoothing:antialiased}
.ph{position:absolute;left:0;top:0;width:100%;object-fit:cover}
.strip{position:absolute;left:0;bottom:0;width:100%;background:#F4F5F3;display:flex;justify-content:space-between;align-items:flex-end;padding:0 64px}
.k{font-size:24px;color:#6B7480;letter-spacing:.01em;margin-bottom:12px}
.n{font-size:44px;font-weight:600;line-height:1.08;letter-spacing:-.015em;max-width:640px}
.p{font-size:52px;font-weight:600;letter-spacing:-.02em;text-align:right;white-space:nowrap}
.p small{display:block;font-size:22px;font-weight:400;color:#6B7480;letter-spacing:0;margin-bottom:6px}
.u{font-size:21px;color:#6B7480;text-align:right;margin-top:10px;white-space:nowrap}
.h{font-size:66px;font-weight:600;line-height:1.02;letter-spacing:-.025em}
.s{font-size:30px;line-height:1.35;color:#3D4A60;margin-top:22px;max-width:820px}
.mark{display:inline-block;width:14px;height:14px;background:#4C8ED9;transform:rotate(45deg);margin-right:14px;position:relative;top:-2px}
'''
def product(img,kicker,name,price,pre='',pos='center',W=1080,H=1350,strip=250):
    ph=H-strip
    return W,H,f'''<img class=ph src="img/{img}" style="height:{ph}px;object-position:{pos}">
<div class=strip style="height:{strip}px;padding-bottom:58px"><div><div class=k><span class=mark></span>{kicker}</div><div class=n>{name}</div></div>
<div><div class=p><small>{pre}</small>{price}</div><div class=u>excellenttilingservice.com.au</div></div></div>'''
def statement(img,head,sub,pos='center',W=1080,H=1350,strip=420,foot='excellenttilingservice.com.au'):
    ph=H-strip
    return W,H,f'''<img class=ph src="img/{img}" style="height:{ph}px;object-position:{pos}">
<div class=strip style="height:{strip}px;display:block;padding-top:64px"><div class=h>{head}</div><div class=s>{sub}</div>
<div class=u style="position:absolute;left:64px;bottom:44px;text-align:left"><span class=mark></span>{foot}</div></div>'''
P={}
P['N1-launch']=statement('brittany1200.jpg','Every price is online.','Tiles, tapware and vanities from a Perth tiling business. Order tonight, or see it first in our Maddington showroom.',pos='center 55%')
P['N2-brittany600']=product('brittany600.jpg','MELA · Wall-hung vanity','Brittany 600 fluted, matt white','$1,149.99',pos='center 60%')
P['N3-dusk']=product('dusk2.jpg','Porcelain tile · Matt','Morgan Dusk','$37.40/m²',pre='from',pos='center 70%')
P['N4-shipping']=statement('dusk1.jpg','Free shipping over $1,000','Tapware ships Australia-wide, priced by weight at checkout. Tiles and vanities: Perth delivery or free pickup.',pos='center 60%')
P['S-N2-brittany600']=product('brittany600.jpg','MELA · Wall-hung vanity','Brittany 600 fluted, matt white','$1,149.99',pos='center 55%',H=1920,strip=380)
only=sys.argv[1:]
for name,(W,H,body) in P.items():
    if only and not any(name.startswith(o) for o in only): continue
    f=os.path.join(S,f'_{name}.html'); open(f,'w').write(f'<!doctype html><meta charset=utf-8><style>{CSS.replace("W",str(W)+"px",1).replace("H",str(H)+"px",1)}</style>{body}')
    subprocess.run(['node',os.path.join(S,'shot.js'),f,os.path.join(OUT,name+'.png'),str(W),str(H)],check=True); os.remove(f)
print('done')
