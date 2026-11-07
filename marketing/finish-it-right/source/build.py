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
URL='excellenttilingservices.com'
posts={
'A2-1-cover':
 img('brittany2.jpg','1/5','1/4')+
 f'<div class="t" {a("1/4","4/6")}><h1>Our online store is open</h1><p class="bot">Tiles, tapware and vanities from a Perth tiling business. Every price is online.</p></div>'+
 f'<div class="t navy" {a("4/5","4/5")}><h2 style="font-size:40px">Free<br>pickup</h2><p class="small bot">in Maddington, or posted from $9.95</p></div>'+
 LOGO('4/5','5/6'),
'A2-2-flova':
 img('flova.png','1/5','1/4','fit')+
 f'<div class="t navy" {a("1/3","4/6")}><div class="big">$189</div><p class="bot">MELA FLOVA basin mixer in chrome. WELS 5 star.</p></div>'+
 img('flova-black.png','3/5','4/5','fit zoom','Also in matt<br>black, $217','dark top')+
 f'<div class="t blue" {a("3/5","5/6")}><p>Posted Australia-wide from $9.95, or pick up free in Maddington</p></div>',
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
'C3-showroom':
 f'<div class="t navy" {a("1/5","1/4")}><h1 style="font-size:132px">Work all day?<br>So do we.</h1><p class="bot" style="font-size:38px">Our Maddington showroom opens in the evening, by appointment.</p></div>'+
 f'<div class="t" {a("1/3","4/6")}><table><tr><td>Mon to Sat</td><td>4:30–9 pm</td></tr><tr><td>Sunday</td><td>Closed</td></tr></table><p class="small bot">Bring your plans and measurements. We\'ll help you work out quantities.</p></div>'+
 f'<div class="t blue" {a("3/5","4/5")}><h2 style="font-size:52px">Book a time online</h2></div>'+
 f'<div class="t" {a("3/4","5/6")}><p class="small">17A Olga Road, Maddington<br><br>0450 960 543</p></div>'+LOGO('4/5','5/6'),
}
posts.update({
'B2-refresh':
 f'<div class="t navy" {a("1/5","1/3")}><h1 style="font-size:104px">Bathroom refresh for $480</h1><p class="bot">Four swaps in one matching chrome finish. Posted from $9.95.</p></div>'+
 img('flova.png','1/3','3/5','fit','Basin mixer $189','dark')+
 img('handshower.jpg','3/4','3/5','fit','Hand shower $151','dark')+
 img('towelrail.png','4/5','3/4','fit','Towel rail $94','dark')+
 img('paper.png','4/5','4/5','fit','Roll holder $46','dark')+
 f'<div class="t" {a("1/4","5/6")}><p>All MELA FLOVA. Also available in matt black and brushed nickel.</p></div>'+LOGO('4/5','5/6'),
'B3-prices':
 f'<div class="t" {a("1/5","1/3")}><h1 style="font-size:112px">Every price is on the website</h1></div>'+
 f'<div class="t navy" {a("1/3","3/5")}><h2>No “call for price”</h2><p class="bot">Tiles, tapware, vanities and tools, all priced online, all buyable tonight.</p></div>'+
 img('flova-black.png','3/5','3/4','fit zoom','FLOVA basin mixer, matt black, $217','dark top')+
 f'<div class="t blue" {a("3/5","4/5")}><p>Tapware posted from $9.95. Perth delivery for tiles and vanities.</p></div>'+
 f'<div class="t" {a("1/4","5/6")}><p>excellenttilingservices.com</p></div>'+LOGO('4/5','5/6'),
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
 f'<div class="t navy" {a("1/5","5/8")}><h1 style="font-size:120px">Unboxing the FLOVA basin mixer</h1><p class="bot" style="font-size:40px">$189 in chrome. Posted Australia-wide from $9.95.</p></div>',
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

posts.update({
'A2-5-delivery':
 f'<div class="t deep" {a("1/5","1/3")}><h1 style="font-size:112px">Three ways to get it home</h1></div>'+
 f'<div class="t" {a("1/3","3/5")}><h2 style="font-size:58px">Posted from $9.95</h2><p class="bot">Tapware and accessories, tracked Australia Post, anywhere in Australia.</p></div>'+
 f'<div class="t" {a("3/5","3/5")}><h2 style="font-size:58px">Perth delivery</h2><p class="bot">Tiles, vanities and baths, priced at checkout.</p></div>'+
 f'<div class="t blue" {a("1/4","5/6")}><h2 style="font-size:54px">Free pickup in Maddington</h2></div>'+LOGO('4/5','5/6'),
'D3-pickup':
 img('hail-room.jpg','1/5','1/3')+
 f'<div class="t deep" {a("1/5","3/5")}><p>Order online</p><h1 style="font-size:150px;margin-top:24px">Pick up free</h1><h2 class="bot" style="font-size:58px">17A Olga Road, Maddington</h2></div>'+
 f'<div class="t" {a("1/4","5/6")}><p>We message you when it\'s ready. Book a pickup time, Monday to Saturday, 4:30 to 9 pm.</p></div>'+LOGO('4/5','5/6'),
'S-shipping':
 f'<div class="t deep" {a("1/5","1/5")}><p style="font-size:40px">Tapware and accessories</p><h1 style="font-size:150px;margin-top:40px">Posted Australia-wide from $9.95</h1><p class="bot" style="font-size:44px">or pick up free in Maddington</p></div>'+
 img('flova.png','1/5','5/7','fit')+
 f'<div class="t blue" {a("1/4","7/8")}><h2 style="font-size:52px">Shop via the link in our bio</h2></div>'+LOGO('4/5','7/8'),
})

posts.update({
'S-reply':
 img('flova.png','1/3','1/4','fit')+img('flova-black.png','3/5','1/4','fit')+
 f'<div class="t navy" {a("1/5","4/7")}><h1 style="font-size:116px">Chrome or matt black?</h1><p class="bot" style="font-size:40px">Same MELA FLOVA mixer, $189 or $217. Reply with your pick.</p></div>'+
 f'<div class="t blue" {a("1/4","7/8")}><h2 style="font-size:52px">Shop via the link in our bio</h2></div>'+LOGO('4/5','7/8'),
'S-tiles':
 img('moon-room.jpg','1/5','1/4')+
 f'<div class="t navy" {a("1/5","4/6")}><p style="font-size:40px">Porcelain tiles</p><h1 style="font-size:150px;margin-top:30px">From $37.40/m²</h1></div>'+
 f'<div class="t" {a("1/5","6/7")}><p style="font-size:38px">Perth delivery or free pickup from Maddington. Every price online.</p></div>'+
 f'<div class="t blue" {a("1/4","7/8")}><h2 style="font-size:52px">Shop via the link in our bio</h2></div>'+LOGO('4/5','7/8'),
'S-vanity':
 img('clark-walnut.webp','1/5','1/4')+
 f'<div class="t navy" {a("1/5","4/6")}><p style="font-size:40px">Wall-hung vanities</p><h1 style="font-size:150px;margin-top:30px">From $1,139</h1></div>'+
 f'<div class="t" {a("1/5","6/7")}><p style="font-size:38px">Stone top and basin included. Delivered across Perth or free pickup.</p></div>'+
 f'<div class="t blue" {a("1/4","7/8")}><h2 style="font-size:52px">Shop via the link in our bio</h2></div>'+LOGO('4/5','7/8'),
})

# Mirror clearance, Nov 2026 (photos live in marketing/mirror-clearance-2026-11)
MC='img/../../../mirror-clearance-2026-11/'
def mcrow(rows): return ''.join(f'<tr><td>{a}</td><td style="text-align:right;color:#7a828b;font-weight:420"><s>RRP {b}</s></td><td>{c}</td></tr>' for a,b,c in rows)
def mctext(c,r,name,rows):
    return f'<div class="t" {a(c,r)} style="padding:28px 36px"><h2 style="font-size:40px">{name}</h2><table style="font-size:30px;margin-top:10px;table-layout:fixed"><col style="width:42%"><col style="width:33%"><col style="width:25%">{mcrow(rows)}</table></div>'
def mcbody(o):
    R=lambda n: f'{n+o}/{n+o+1}'
    return (
     f'<div class="t ph" {a("1/2",R(2))}><img src="{MC}eclipse-stick-on-mirror.jpg"></div>'+
     mctext('2/5',R(2),'Eclipse round stick-on mirror, 5 mm',[('600 mm','$99','$63.00'),('800 mm','$109','$69.35')])+
     f'<div class="t ph" {a("1/2",R(3))}><img src="{MC}capsule-stick-on-mirror.jpg"></div>'+
     mctext('2/5',R(3),'Capsule stick-on mirror',[('450 x 900 mm','$109','$69.35')])+
     f'<div class="t ph" {a("1/2",R(4))}><img style="object-fit:contain;background:#7d7d7d" src="{MC}rectangular-mirror.jpg"></div>'+
     mctext('2/5',f'{4+o}/{6+o}','Rectangular framed mirror, 750 mm high, 34 mm thick',[('600 mm','$89.10','$56.70'),('750 mm','$99','$63.00'),('900 mm','$109','$69.35'),('1200 mm','$129','$82.10')])+
     f'<div class="t blue" {a("1/2",R(5))} style="padding:26px"><p class="small">Prices inc GST. Pick up free in Maddington, or we deliver.</p></div>')
posts.update({
'MC-mirror-clearance':
 f'<div class="t navy" {a("1/4","1/2")}><h1 style="font-size:84px">Mirror clearance</h1><p class="bot">Up to 36% off RRP. Limited stock, while stocks last.</p></div>'+LOGO('4/5','1/2')+mcbody(0),
'S-mirror-clearance':
 f'<div class="t navy" {a("1/5","1/3")}><h1 style="font-size:150px">Mirror clearance</h1><p class="bot" style="font-size:40px">Up to 36% off RRP. Limited stock, while stocks last.</p></div>'+mcbody(1)+
 f'<div class="t deep" {a("1/4","7/8")}><h2 style="font-size:44px">Clearance section at excellenttilingservices.com</h2></div>'+LOGO('4/5','7/8'),
})

# Week of 9 Nov 2026 (photos live in marketing/week-2026-11-09/img)
W='img/../../../week-2026-11-09/img/'
def wimg(f,c,r,cls='',cap='',capcls=''):
    return f'<div class="t ph {cls}" {a(c,r)}><img src="{W}{f}">'+(f'<span class="cap {capcls}">{cap}</span>' if cap else '')+'</div>'
BIO=lambda r: f'<div class="t blue" {a("1/4",r)}><h2 style="font-size:52px">Shop via the link in our bio</h2></div>'+LOGO('4/5',r)
def step(n,r,txt): return f'<div class="t" {a("1/5",r)} style="display:flex;align-items:center;gap:44px"><div class="big" style="color:var(--blue);min-width:110px">{n}</div><p style="font-size:40px">{txt}</p></div>'
posts.update({
'W1-big-tiles':
 wimg('hail-big.jpg','1/5','1/4','','Morgan Hail')+
 f'<div class="t navy" {a("1/4","4/6")}><h1 style="font-size:84px">Small bathroom? Go bigger on the tiles.</h1><p class="bot">Fewer grout lines, so the floor reads as one surface.</p></div>'+
 f'<div class="t blue" {a("4/5","4/5")}><p class="small">600x1200</p><h2 class="bot" style="font-size:50px">$50/m²</h2></div>'+LOGO('4/5','5/6'),
'W2-toilets':
 f'<div class="t navy" {a("1/5","1/2")}><h1 style="font-size:96px">New in: toilets</h1></div>'+
 wimg('element.jpg','1/2','2/4','fit','Element<br>$500','dark')+wimg('edge.png','2/3','2/4','fit','Edge<br>$550','dark')+
 wimg('forma.png','3/4','2/4','fit','Forma<br>$550','dark')+wimg('clarice.jpg','4/5','2/4','fit','Clarice<br>$660','dark')+
 wimg('flow.png','1/2','4/5','fit','Flow $660','dark')+wimg('vero.png','2/3','4/5','fit','Vero $1,299','dark')+
 f'<div class="t" {a("3/5","4/5")}><p>Rimless bowls. Every price online.</p></div>'+
 f'<div class="t blue" {a("1/4","5/6")}><p>Perth delivery, or pick up free in Maddington</p></div>'+LOGO('4/5','5/6'),
'W3-measure':
 f'<div class="t navy" {a("1/5","1/2")}><h1 style="font-size:84px">How much tile do you need?</h1></div>'+
 step(1,'2/3','Measure length x width of each part of the room, in metres.')+
 step(2,'3/4','Add them up.')+
 step(3,'4/5','Add 10% for cuts. 15% for herringbone or diagonal.')+
 f'<div class="t blue" {a("1/4","5/6")}><p>Our tile calculator on every tile page does steps 2 and 3 for you.</p></div>'+LOGO('4/5','5/6'),
'W4-smart':
 wimg('elite.png','1/3','1/4','fit')+
 f'<div class="t navy" {a("3/5","1/4")}><h2 style="font-size:70px">What does a smart toilet do?</h2><p class="bot">A built-in bidet wash. Less paper, and a cleaner feel.</p></div>'+
 f'<div class="t" {a("1/3","4/5")}><p class="small">Crystal Elite</p><h2 class="bot" style="font-size:64px">$2,999</h2></div>'+
 f'<div class="t" {a("3/5","4/5")}><p class="small">Crystal Prime</p><h2 class="bot" style="font-size:64px">$3,299</h2></div>'+
 f'<div class="t blue" {a("1/4","5/6")}><p>Install video on the product page. Perth delivery.</p></div>'+LOGO('4/5','5/6'),
'W6-rimless':
 wimg('flow.png','1/3','1/4','fit')+
 f'<div class="t navy" {a("3/5","1/4")}><h1 style="font-size:96px">Why rimless?</h1></div>'+
 f'<div class="t" {a("1/5","4/5")}><p style="font-size:38px">No hidden rim under the bowl, so there\'s nowhere for grime to hide. One wipe and it\'s clean.</p></div>'+
 f'<div class="t blue" {a("1/4","5/6")}><h2 style="font-size:46px">Every Eternal toilet we sell is rimless. From $500.</h2></div>'+LOGO('4/5','5/6'),
'W7-photo':
 img('brittany2.jpg','1/5','1/3')+
 f'<div class="t navy" {a("1/5","3/5")}><h1 style="font-size:100px">Send us a photo of your bathroom</h1><p class="bot" style="font-size:36px">We\'ll reply with the one change we\'d make first, and what it costs.</p></div>'+
 f'<div class="t blue" {a("1/4","5/6")}><h2 style="font-size:50px">DM us, or comment “photo”</h2></div>'+LOGO('4/5','5/6'),
'S-W1-big-tiles':
 wimg('hail-big.jpg','1/5','1/4')+
 f'<div class="t navy" {a("1/5","4/6")}><p style="font-size:40px">600x1200 porcelain tiles</p><h1 style="font-size:150px;margin-top:30px">$50/m²</h1></div>'+
 f'<div class="t" {a("1/5","6/7")}><p style="font-size:38px">Fewer grout lines, a bigger-looking room. Morgan Hail, Cement White, Cement Grey, Fumosa.</p></div>'+BIO('7/8'),
'S-W2-toilets':
 wimg('element.jpg','1/3','1/4','fit')+wimg('vero.png','3/5','1/4','fit')+
 f'<div class="t navy" {a("1/5","4/7")}><h1 style="font-size:140px">New in: toilets from $500</h1><p class="bot" style="font-size:40px">Rimless bowls. Perth delivery or free pickup.</p></div>'+BIO('7/8'),
'S-W3-sketch':
 f'<div class="t navy" {a("1/5","1/5")}><h1 style="font-size:140px">Odd-shaped room?</h1><p class="bot" style="font-size:48px">Send us a sketch with the measurements. We\'ll work out how much tile you need.</p></div>'+
 img('moon-room.jpg','1/5','5/7')+f'<div class="t blue" {a("1/4","7/8")}><h2 style="font-size:52px">DM us your sketch</h2></div>'+LOGO('4/5','7/8'),
'S-W4-smart':
 wimg('elite.png','1/5','1/4','fit')+
 f'<div class="t navy" {a("1/5","4/7")}><p style="font-size:40px">Smart toilets</p><h1 style="font-size:150px;margin-top:30px">From $2,999</h1><p class="bot" style="font-size:40px">Built-in bidet wash. Perth delivery.</p></div>'+BIO('7/8'),
'S-W6-rimless':
 wimg('flow.png','1/5','1/4','fit')+
 f'<div class="t navy" {a("1/5","4/7")}><h1 style="font-size:140px">Rimless. One wipe, clean.</h1><p class="bot" style="font-size:40px">Eternal toilets from $500.</p></div>'+BIO('7/8'),
'S-W7-photo':
 f'<div class="t navy" {a("1/5","1/5")}><h1 style="font-size:140px">Send us a photo of your bathroom</h1><p class="bot" style="font-size:48px">We\'ll reply with the one change we\'d make first, and what it costs.</p></div>'+
 img('brittany2.jpg','1/5','5/7')+f'<div class="t blue" {a("1/4","7/8")}><h2 style="font-size:52px">DM us a photo</h2></div>'+LOGO('4/5','7/8'),
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
