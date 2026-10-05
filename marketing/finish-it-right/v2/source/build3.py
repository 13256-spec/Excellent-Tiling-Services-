"""ETS v3 graphics: full-bleed photo, text on the quiet part of the photo, navy pill button.
python3 build3.py <config.json> -> out3/<name>.png   (config: list of posts, see week1-v3.json)"""
import json,os,sys,subprocess
S=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(S,'out3'); os.makedirs(OUT,exist_ok=True)
CSS='''@font-face{font-family:A;src:url(archivo.woff2);font-weight:100 900}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:A,sans-serif;position:relative;overflow:hidden;-webkit-font-smoothing:antialiased}
.ph{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.cut{position:absolute;object-fit:contain}
.box{position:absolute}
.k{font-size:26px;margin-bottom:22px;opacity:.85}
.mark{display:inline-block;width:14px;height:14px;background:#4C8ED9;transform:rotate(45deg);margin-right:14px;position:relative;top:-3px}
h1{font-weight:600;letter-spacing:-.03em;line-height:1}
.s{font-size:32px;line-height:1.32;margin-top:24px}
.price{font-size:64px;font-weight:600;letter-spacing:-.02em;margin-top:26px}
.price small{font-size:26px;font-weight:400;margin-right:10px;opacity:.8}
.pill{position:absolute;font-size:28px;font-weight:500;padding:20px 32px;border-radius:999px;white-space:nowrap}
'''
def page(p):
    W,H=(1080,1920) if p.get('story') else (1080,1350)
    col=p.get('color','#1F3153'); sub=p.get('subcolor',col)
    if p.get('cutout'):
        bg=p.get('bg','#EFECE7')
        imgtag=f'<div style="position:absolute;inset:0;background:{bg}"></div><img class=cut src="img/{p["img"]}" style="{p.get("cutstyle","left:140px;top:380px;width:800px;height:800px")};mix-blend-mode:multiply">'
    else:
        imgtag=f'<img class=ph src="img/{p["img"]}" style="object-position:{p.get("pos","center")}">'
    b=p['box']; style=';'.join(f'{k}:{v}px' if isinstance(v,(int,float)) else f'{k}:{v}' for k,v in b.items())
    if p.get('card'): style+=';background:rgba(244,245,243,.92);padding:46px 48px 50px;border-radius:30px'
    k=f'<div class=k style="color:{sub}"><span class=mark></span>{p.get("kicker","Excellent Tiling Services · Perth")}</div>'
    h=f'<h1 style="font-size:{p.get("hs",88)}px;color:{col}">{p["head"]}</h1>'
    s=f'<div class=s style="color:{sub}">{p["sub"]}</div>' if p.get('sub') else ''
    pr=f'<div class=price style="color:{col}"><small>{p.get("pre","")}</small>{p["price"]}</div>' if p.get('price') else ''
    pl=p.get('pill','Shop now · link in bio'); pc=p.get('pillpos',{'left':72,'bottom':(230 if p.get('story') else 72)})
    pst=';'.join(f'{a}:{v}px' for a,v in pc.items())
    pb,pf=(('#fff','#1F3153') if p.get('pilllight') else ('#1F3153','#fff'))
    pill=f'<div class=pill style="{pst};background:{pb};color:{pf}">{pl}</div>' if pl else ''
    return W,H,f'<!doctype html><meta charset=utf-8><style>{CSS}body{{width:{W}px;height:{H}px}}</style>{imgtag}<div class=box style="{style}">{k}{h}{s}{pr}</div>{pill}'
cfg=json.load(open(sys.argv[1])); only=sys.argv[2:]
for p in cfg:
    if only and not any(p['name'].startswith(o) for o in only): continue
    W,H,html=page(p); f=os.path.join(S,f"_{p['name']}.html"); open(f,'w').write(html)
    subprocess.run(['node',os.path.join(S,'shot.js'),f,os.path.join(OUT,p['name']+'.png'),str(W),str(H)],check=True); os.remove(f)
    print(p['name'])
