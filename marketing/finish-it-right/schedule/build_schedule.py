"""Builds main-posts.json and stories.json for Metricool (Finish It Right, 6 Oct - 8 Nov 2026)."""
import json, datetime as dt
CDN='https://cdn.shopify.com/s/files/1/0683/0292/9983/files/'
V={'A2-1-cover':'1791211786','A2-2-flova':'1791211785','A2-3-vanities':'1791211786','A2-4-tiles':'1791211786',
'A2-5-delivery':'1791211785','A3-idea':'1791211786','B2-refresh':'1791211785','B3-prices':'1791211785',
'C2-tile-looks':'1791211786','C3-showroom':'1791211785','D2-trade':'1791211785','D3-pickup':'1791211786',
'S-reply':'1791211785','S-shipping':'1791211785','S-showroom':'1791211786','S-trade':'1791211785',
'S-tiles':'1791211786','S-vanity':'1791211786'}
def u(n): return f'{CDN}ets-{n}.png?v={V[n]}'
TAGS='#perthrenovation #perthbathrooms #bathroomrenovation #perthtiler #perthhomes #bathroominspo #maddington #excellenttilingservices'
LINK='Shop at excellenttilingservices.com (link in bio).'
LAUNCH=['A2-1-cover','A2-2-flova','A2-3-vanities','A2-4-tiles','A2-5-delivery']
M=[ # date, graphics, caption (no link/tags; added below). None graphics = owner posts by hand
('2026-10-06',LAUNCH,"Our online store is open. Tiles, tapware and vanities from a Perth tiling business, with every price on the website.\nSwipe for our favourites: MELA FLOVA basin mixer from $189, wall-hung vanities from $1,139 and porcelain tiles from $37.40/m².\nTapware posted Australia-wide from $9.95, Perth delivery, or free pickup from Maddington."),
('2026-10-07',['D3-pickup'],"Order online, pick up free. Choose local pickup at checkout, we'll message you when it's ready, then book a time Monday to Saturday, 4:30 to 9 pm. 17A Olga Road, Maddington. Bring a ute for tiles and vanities."),
('2026-10-08',['A2-5-delivery'],"Three ways to get your order home: tapware and accessories posted Australia-wide from $9.95, Perth delivery for tiles, vanities and baths, or free pickup from our Maddington showroom."),
('2026-10-09',['D2-trade'],"Tiler, builder or plumber? A free ETS trade account takes 5–25% off tapware, vanities, tools and trims, and 15% off all tiles. The discount comes off automatically when you log in. No codes.\nApply in two minutes on our website."),
('2026-10-10',['C2-tile-looks'],"Four quiet floors from our porcelain range: Terrazzo White, Cement Grey, Particle Warm and Lava Ash. Save this for your reno board.\nOrder online for Perth delivery, or book an evening showroom visit to see them in person."),
('2026-10-11',['B3-prices'],"Every price is on our website. No \"call for price\", no waiting on a quote for a mixer. Tiles, tapware, vanities and tools, all buyable tonight.\nTapware posted Australia-wide from $9.95. Perth delivery or free pickup for tiles and vanities."),
('2026-10-12',['A2-3-vanities'],"Wall-hung vanities from $1,139. Shown: the MELA CLARK 900 in walnut, with stone top and basin included.\nDelivered across Perth, or pick up free from our Maddington showroom."),
('2026-10-13',['C3-showroom'],"Work all day? So do we. Our Maddington showroom opens by appointment Monday to Saturday, 4:30 to 9 pm. Bring your plans and measurements and we'll help you work out quantities.\nBook a time online, or call 0450 960 543."),
('2026-10-14',['B2-refresh'],"Not ready for a full reno? Swap four things and the bathroom feels new:\nFLOVA basin mixer $189\nFLOVA hand shower $151\nFLOVA 600 towel rail $94\nFLOVA roll holder $46\n$480 in matching chrome, posted Australia-wide from $9.95."),
('2026-10-15',['A3-idea'],"Bathroom idea: warm oak against a plain wall. The MELA BRITTANY 1200 fluted, curved vanity does the work, so keep the tiles quiet and the tapware simple.\n$1,994, delivered across Perth or picked up free from Maddington. Which would you change first: vanity, tiles or tapware?"),
('2026-10-16',None,"REEL by hand: FLOVA unboxing (see calendar)"),
('2026-10-17',['C2-tile-looks'],"Four quiet floors: Terrazzo White, Cement Grey, Particle Warm and Lava Ash. Which one goes in your bathroom?\nEvery price is online. Perth delivery or free pickup from Maddington."),
('2026-10-18',['B3-prices'],"Sick of \"call for price\"? Every tile, tap and vanity we sell has its price on the website. Check it tonight, order tonight. Tapware posted Australia-wide from $9.95."),
('2026-10-19',['A2-2-flova'],"The MELA FLOVA basin mixer: $189 in chrome, $217 in matt black. 5-star WELS rating, so it saves water without feeling weak. Posted Australia-wide from $9.95."),
('2026-10-20',['D2-trade'],"Tradies: a free ETS trade account takes 15% off tiles and 5–25% off tapware, vanities, tools and trims. It comes off automatically when you're logged in. No codes. Apply on our website."),
('2026-10-21',None,"REEL by hand: vanity install (see calendar)"),
('2026-10-22',['A2-4-tiles'],"Porcelain tiles from $37.40/m². Lava Etna, Morgan Hail, Time Stone Moon and more, sold by the full box with every price online.\nPerth delivery or free pickup from Maddington. Not sure how many boxes? Send us your room size and we'll work it out."),
('2026-10-23',['A2-3-vanities'],"Floating vanities make small bathrooms look bigger and you can mop right under them. Ours start at $1,139 with stone top and basin included.\nDelivered across Perth, or pick up free from Maddington."),
('2026-10-24',['https://cdn.shopify.com/s/files/1/0683/0292/9983/files/mela-suri-700-frameless-mirror.jpg?v=1790229068','https://cdn.shopify.com/s/files/1/0683/0292/9983/files/mela-suri-700-round-mirror-black-frame-7390542.jpg?v=1790401809','https://cdn.shopify.com/s/files/1/0683/0292/9983/files/suri-900-led-round-mirror_799d0a53-d0d3-4672-bf67-63c47279c84d.jpg?v=1790223370','https://cdn.shopify.com/s/files/1/0683/0292/9983/files/mela-mia-450-frameless-oval-mirror.jpg?v=1790170457'],"Round or oval, framed or LED? A new mirror changes a bathroom faster than anything else.\nMELA SURI round: frameless from $189, framed from $236, LED from $349. MELA MIA oval frameless from $189.\nShipped Australia-wide by Australia Post, or pick up free from Maddington."),
('2026-10-25',['A2-5-delivery'],"Three ways to get your order home: tapware and accessories posted Australia-wide from $9.95, Perth delivery for tiles, vanities and baths, or free pickup from our Maddington showroom."),
('2026-10-26',None,"REEL by hand: 3 tiling mistakes (see calendar)"),
('2026-10-27',None,"Customer review or job photo, by hand (see calendar)"),
('2026-10-28',['B2-refresh'],"The easiest bathroom upgrade we sell: four FLOVA pieces in matching chrome for $480, posted Australia-wide from $9.95. No tradie needed for the towel rail and roll holder."),
('2026-10-29',['C2-tile-looks'],"Quiet floors make everything else in the room look better. Terrazzo White, Cement Grey, Particle Warm and Lava Ash, all porcelain, all priced online.\nPerth delivery or free pickup from Maddington."),
('2026-10-30',['C3-showroom'],"Planning a weekend reno? See the tiles and vanities in person first. Our Maddington showroom is open by appointment tonight and tomorrow, 4:30 to 9 pm. Book online or call 0450 960 543."),
('2026-10-31',['https://cdn.shopify.com/s/files/1/0683/0292/9983/files/DSAYFR600331_4.jpg?v=1790332958','https://cdn.shopify.com/s/files/1/0683/0292/9983/files/DSAYFR600331.jpg?v=1790334486','https://cdn.shopify.com/s/files/1/0683/0292/9983/files/DSAYFR600331_2.jpg?v=1790334487'],"Same tile, whole room. Time Stone Moon in 600x600 matt, P4/R11 slip rating so it works in wet areas too. Price per m² on the website, Perth delivery or free pickup."),
('2026-11-01',['D2-trade'],"Tradies: set up your free trade account before Monday's jobs. 15% off tiles and 5–25% off everything else, applied automatically when you're logged in. Apply on our website."),
('2026-11-02',LAUNCH,"Missed it? Our full range is online with every price showing: basin mixers from $189, porcelain tiles from $37.40/m² and wall-hung vanities from $1,139. Tapware posted Australia-wide from $9.95, or pick up free in Maddington."),
('2026-11-03',['B3-prices'],"Every tile, tap and vanity we sell has its price on the website. No quotes, no waiting. Tapware posted Australia-wide from $9.95."),
('2026-11-04',['A3-idea'],"Still thinking about a vanity? The MELA BRITTANY 1200 in fluted oak is $1,994, delivered across Perth or picked up free from Maddington. Book an evening showroom visit to see the finish in person."),
('2026-11-05',['A2-2-flova'],"Tapware and accessories go Australia-wide by tracked Australia Post from $9.95. Mixers, shower sets, towel rails, all priced online."),
('2026-11-06',['D3-pickup'],"Order online, pick up free. Choose local pickup at checkout, we'll message you when it's ready, then book a time Monday to Saturday, 4:30 to 9 pm. 17A Olga Road, Maddington."),
('2026-11-07',['B2-refresh'],"Weekend job: four FLOVA pieces in matching chrome for $480, posted Australia-wide from $9.95. The towel rail and roll holder go up in an afternoon."),
('2026-11-08',['A2-4-tiles'],"Porcelain tiles from $37.40/m², sold by the box with every price online. Lava Etna, Morgan Hail, Time Stone Moon and more. Perth delivery or free pickup from Maddington."),
]
main=[]
for d,g,c in M:
    e={'date':d,'time':'18:30','kind':'main'}
    if g is None: e.update(manual=True,note=c)
    else:
        e['graphics']=g; e['media']=[x if x.startswith('http') else u(x) for x in g]
        e['text']=f"{c}\n{LINK}\n\n{TAGS}"
    main.append(e)
json.dump(main,open('main-posts.json','w'),indent=1,ensure_ascii=False)
rot=['S-shipping','S-tiles','S-reply','S-vanity','S-trade','S-showroom']
st=[]; d=dt.date(2026,10,6); i=0
while d<=dt.date(2026,11,8):
    n=rot[i%6]
    if n=='S-showroom' and d.weekday()==6: n='S-shipping'
    st.append({'date':d.isoformat(),'time':'19:30','kind':'story','graphic':n,'media':[u(n)]}); d+=dt.timedelta(1); i+=1
json.dump(st,open('stories.json','w'),indent=1)
print(len(main),sum(1 for m in main if not m.get('manual')),len(st))
