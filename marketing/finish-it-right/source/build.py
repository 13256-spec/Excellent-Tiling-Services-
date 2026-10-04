import os,subprocess
S=os.path.dirname(os.path.abspath(__file__))
CSS='''
@font-face{font-family:Archivo;src:url(archivo.woff2) format('woff2');font-weight:100 900;font-stretch:62% 125%}
:root{--navy:#1F3153;--deep:#16243E;--blue:#4C8ED9;--porc:#F4F5F3;--grout:#C3C8CC;--ink:#1F3153}
*{box-sizing:border-box;margin:0}
html,body{width:1080px;background:var(--grout)}
body{font-family:Archivo,sans-serif;color:var(--ink);font-variation-settings:"wdth" 100}
.g{position:absolute;inset:0;padding:6px;display:grid;gap:6px;grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(5,1fr)}
.t{position:relative;overflow:hidden;background:var(--porc);padding:40px}
.navy{background:var(--navy);color:#fff}.deep{background:var(--deep);color:#fff}.blue{background:var(--blue);color:#fff}
.ph{padding:0}.ph img{width:100%;height:100%;object-fit:cover;display:block}
.fit{background:#fff}.zoom img{padding:20px 20px 10px 250px}.fit img{object-fit:contain;padding:30px}
h1{font-size:92px;line-height:.95;font-weight:680;font-variation-settings:"wdth" 112;letter-spacing:-.015em}
h2{font-size:64px;line-height:1;font-weight:660;font-variation-settings:"wdth" 110;letter-spacing:-.01em}
p{font-size:31px;line-height:1.3;font-weight:420}
.small{font-size:24px;line-height:1.3;font-weight:450}
.big{font-size:150px;line-height:.85;font-weight:720;font-variation-settings:"wdth" 104;letter-spacing:-.03em}
.code{font-size:182px;line-height:.85;font-weight:760;font-variation-settings:"wdth" 110;letter-spacing:-.02em}
.bot{position:absolute;left:40px;right:40px;bottom:36px}
.logo{display:flex;align-items:center;justify-content:center;background:#fff;padding:18px}.logo img{width:100%;height:100%;object-fit:contain}
.cap{position:absolute;left:24px;bottom:20px;font-size:26px;font-weight:500;color:#fff;text-shadow:0 1px 6px rgba(0,0,0,.35)}
.cap.top{top:20px;bottom:auto}.cap.dark{color:var(--navy);text-shadow:none}
.stack>*+*{margin-top:22px}
table{border-collapse:collapse;font-size:31px;width:100%}td{padding:10px 0;border-bottom:3px solid var(--grout)}td:last-child{text-align:right;font-weight:600}
'''
def a(c,r): return f'style="grid-column:{c};grid-row:{r}"'
def img(f,c,r,cls='',cap='',capcls=''):
    k=f'<div class="t ph {cls}" {a(c,r)}><img src="img/{f}">'+(f'<span class="cap {capcls}">{cap}</span>' if cap else '')+'</div>'
    return k
LOGO=lambda c,r: f'<div class="t logo" {a(c,r)}><img src="img/logo-white.jpg"></div>'
URL='excellenttilingservice.com.au'
posts={
'A2-1-cover':
 img('brittany2.jpg','1/5','1/4')+
 f'<div class="t" {a("1/4","4/6")}><h1>Our online store is open</h1><p class="bot">Tiles, tapware and vanities from a Perth tiling business, at the prices we pay to fit them out.</p></div>'+
 f'<div class="t navy" {a("4/5","4/5")}><h2 style="font-size:86px">10%</h2><p class="small bot">off your first order over $150</p></div>'+
 LOGO('4/5','5/6'),
'A2-2-flova':
 img('flova.png','1/5','1/4','fit')+
 f'<div class="t navy" {a("1/3","4/6")}><div class="big">$189</div><p class="bot">MELA FLOVA basin mixer in chrome. WELS 5 star.</p></div>'+
 img('flova-black.png','3/5','4/5','fit zoom','Also in matt<br>black, $217','dark top')+
 f'<div class="t blue" {a("3/5","5/6")}><p>Free shipping anywhere in Australia on tapware orders over $100</p></div>',
'A2-3-vanities':
 img('clark-walnut.webp','1/5','1/4')+
 f'<div class="t" {a("1/4","4/6")}><h2>Wall-hung vanities</h2><p class="bot">Delivered across Perth, or pick up free from our Maddington showroom. Shown: MELA CLARK 900 in walnut.</p></div>'+
 f'<div class="t navy" {a("4/5","4/6")}><p>From</p><h2 class="bot" style="font-size:52px">$1,139</h2></div>',
'A2-4-tiles':
 img('etna-room.jpg','1/3','1/3','','Lava Etna')+
 img('hail-room2.jpg','3/5','1/3','','Morgan Hail','dark')+
 img('moon-room.jpg','1/3','3/5','','Time Stone Moon','dark')+
 img('moon-room2.jpg','3/5','3/5','','Time Stone Moon, laid','dark')+
 f'<div class="t" {a("1/4","5/6")}><h2 style="font-size:52px">Porcelain tiles from $37.40/m²</h2><p class="small" style="margin-top:14px">Perth delivery or free pickup. Sold by the full box.</p></div>'+
 f'<div class="t blue" {a("4/5","5/6")}></div>',
'A2-5-code':
 f'<div class="t deep" {a("1/5","1/4")}><p>Use code</p><div class="code" style="margin-top:30px">YAMEN10</div><p class="bot" style="font-size:40px">10% off your first order over $150</p></div>'+
 f'<div class="t" {a("1/4","4/6")}><h2>Ends Sunday 8&nbsp;November</h2><p class="bot">{URL}</p></div>'+
 f'<div class="t blue" {a("4/5","4/5")}></div>'+LOGO('4/5','5/6'),
'C3-showroom':
 f'<div class="t navy" {a("1/5","1/4")}><h1 style="font-size:132px">Work all day?<br>So do we.</h1><p class="bot" style="font-size:38px">Our Maddington showroom opens in the evening, by appointment.</p></div>'+
 f'<div class="t" {a("1/3","4/6")}><table><tr><td>Mon to Sat</td><td>4:30–9 pm</td></tr><tr><td>Sunday</td><td>Closed</td></tr></table><p class="small bot">Bring your plans and measurements. We\'ll help you work out quantities.</p></div>'+
 f'<div class="t blue" {a("3/5","4/5")}><h2 style="font-size:52px">Book a time online</h2></div>'+
 f'<div class="t" {a("3/4","5/6")}><p class="small">17A Olga Road, Maddington<br><br>0450 960 543</p></div>'+LOGO('4/5','5/6'),
'D3-last-call':
 img('hail-room.jpg','1/5','1/3')+
 f'<div class="t deep" {a("1/5","3/5")}><p>Last call</p><div class="code" style="margin-top:24px">YAMEN10</div><h2 class="bot" style="font-size:58px">Ends Sunday 8 November</h2></div>'+
 f'<div class="t" {a("1/4","5/6")}><p>10% off your first order over $150, tiles to tapware.</p><p class="small" style="margin-top:12px">{URL}</p></div>'+LOGO('4/5','5/6'),
}

posts.update({
'B2-refresh':
 f'<div class="t navy" {a("1/5","1/3")}><h1 style="font-size:104px">Bathroom refresh for $480</h1><p class="bot">Four swaps, one matching chrome finish, delivered free anywhere in Australia.</p></div>'+
 img('flova.png','1/3','3/5','fit','Basin mixer $189','dark')+
 img('handshower.jpg','3/4','3/5','fit','Hand shower $151','dark')+
 img('towelrail.png','4/5','3/4','fit','Towel rail $94','dark')+
 img('paper.png','4/5','4/5','fit','Roll holder $46','dark')+
 f'<div class="t" {a("1/4","5/6")}><p>All MELA FLOVA. Add code YAMEN10 for another 10% off orders over $150.</p></div>'+LOGO('4/5','5/6'),
'B3-prices':
 f'<div class="t" {a("1/5","1/3")}><h1 style="font-size:112px">Every price is on the website</h1></div>'+
 f'<div class="t navy" {a("1/3","3/5")}><h2>No “call for price”</h2><p class="bot">Tiles, tapware, vanities and tools, all priced online, all buyable tonight.</p></div>'+
 img('flova-black.png','3/5','3/4','fit zoom','FLOVA basin mixer, matt black, $217','dark top')+
 f'<div class="t blue" {a("3/5","4/5")}><p>Free shipping on tapware over $100. Perth delivery for tiles and vanities.</p></div>'+
 f'<div class="t" {a("1/4","5/6")}><p>excellenttilingservice.com.au</p></div>'+LOGO('4/5','5/6'),
'A3-idea':
 img('brittany2.jpg','1/5','1/4')+
 f'<div class="t" {a("1/4","4/6")}><h2>Bathroom idea: warm oak against a plain wall</h2><p class="bot">A fluted, curved vanity does the work. Keep the tiles quiet and the tapware simple.</p></div>'+
 f'<div class="t navy" {a("4/5","4/6")}><p class="small">MELA BRITTANY 1200 oak vanity</p><h2 class="bot" style="font-size:52px">$1,994</h2></div>',
'C2-tile-looks':
 img('terrazzo.jpg','1/3','1/3','','Terrazzo White','dark')+
 img('cement.jpg','3/5','1/3','','Cement Grey','dark')+
 img('particle.jpg','1/3','3/5','','Particle Warm','dark')+
 img('lava-ash.jpg','3/5','3/5','','Lava Ash','dark')+
 f'<div class="t navy" {a("1/4","5/6")}><h2 style="font-size:52px">Four quiet floors. Save this for your reno.</h2></div>'+LOGO('4/5','5/6'),
'D2-trade':
 f'<div class="t navy" {a("1/5","1/3")}><h1 style="font-size:104px">Tiler, builder or plumber?</h1><p class="bot">A free ETS trade account takes the discount off at checkout. No codes.</p></div>'+
 f'<div class="t" {a("1/3","3/5")}><div class="big" style="color:var(--blue)">15%</div><p class="bot">off all tiles</p></div>'+
 f'<div class="t" {a("3/5","3/5")}><div class="big" style="font-size:120px;color:var(--blue)">5–25%</div><p class="bot">off tapware, vanities, tools and trims, set item by item</p></div>'+
 f'<div class="t blue" {a("1/4","5/6")}><h2 style="font-size:52px">Apply on our website in two minutes</h2></div>'+LOGO('4/5','5/6'),
'R-B1-unboxing':
 img('flova.png','1/5','1/5','fit')+
 f'<div class="t navy" {a("1/5","5/8")}><h1 style="font-size:120px">Unboxing the FLOVA basin mixer</h1><p class="bot" style="font-size:40px">$189 in chrome. Free shipping over $100.</p></div>',
'R-C1-vanity':
 img('clark-walnut.webp','1/5','1/5')+
 f'<div class="t navy" {a("1/5","5/8")}><h1 style="font-size:120px">Wall-hung vanity, start to finish</h1><p class="bot" style="font-size:40px">30 seconds. One install. Delivered across Perth.</p></div>',
'R-D1-mistakes':
 img('hail-room2.jpg','1/5','1/4')+
 f'<div class="t navy" {a("1/5","4/8")}><h1 style="font-size:132px">3 tiling mistakes we fix every week</h1><p class="bot" style="font-size:40px">And the tool that stops each one.</p></div>',
'S-poll':
 img('flova.png','1/3','1/4','fit')+img('flova-black.png','3/5','1/4','fit')+
 f'<div class="t navy" {a("1/5","4/6")}><h1 style="font-size:116px">Chrome or matt black?</h1><p class="bot" style="font-size:38px">Same mixer, $189 or $217. Vote below.</p></div>'+
 f'<div class="t" {a("1/5","6/8")}><p style="font-size:34px;color:#8a919a">Poll sticker goes here</p></div>',
'S-countdown':
 f'<div class="t deep" {a("1/5","1/5")}><p style="font-size:40px">Last day tomorrow</p><div class="code" style="margin-top:40px">YAMEN10</div><p class="bot" style="font-size:44px">10% off your first order over $150</p></div>'+
 f'<div class="t" {a("1/5","5/7")}><p style="font-size:34px;color:#8a919a">Countdown sticker goes here</p></div>'+
 f'<div class="t blue" {a("1/4","7/8")}><h2 style="font-size:52px">Tap the link to shop</h2></div>'+LOGO('4/5','7/8'),
'S-showroom':
 f'<div class="t navy" {a("1/5","1/4")}><h1 style="font-size:132px">Open tonight, 4:30 to 9</h1></div>'+
 img('brittany2.jpg','1/5','4/6')+
 f'<div class="t" {a("1/5","6/7")}><p style="font-size:38px">17A Olga Road, Maddington. By appointment, Monday to Saturday.</p></div>'+
 f'<div class="t blue" {a("1/4","7/8")}><h2 style="font-size:52px">Book a time</h2></div>'+LOGO('4/5','7/8'),
'S-trade':
 f'<div class="t navy" {a("1/5","1/4")}><h1 style="font-size:124px">Trade prices for trades</h1></div>'+
 f'<div class="t" {a("1/3","4/6")}><div class="big" style="color:var(--blue)">15%</div><p class="bot">off tiles</p></div>'+
 f'<div class="t" {a("3/5","4/6")}><div class="big" style="font-size:120px;color:var(--blue)">5–25%</div><p class="bot">off everything else</p></div>'+
 f'<div class="t blue" {a("1/4","6/8")}><h2 style="font-size:60px">Free account. Apply on the website.</h2></div>'+LOGO('4/5','6/8'),
})

os.makedirs(f'{S}/out',exist_ok=True)
import sys
only=sys.argv[1:]
for name,body in posts.items():
    if only and not any(name.startswith(o) for o in only): continue
    tall=name[:2] in ('S-','R-')
    H=1920 if tall else 1350; rows=7 if tall else 5
    h=f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} html,body{{height:{H}px}} .g{{grid-template-rows:repeat({rows},1fr)}}</style></head><body><div class="g">{body}</div></body></html>'
    p=f'{S}/{name}.html';open(p,'w').write(h)
    subprocess.run(['node',f'{S}/shot.js',p,f'{S}/out/{name}.png','1080',str(H)],check=True)
print('done')
