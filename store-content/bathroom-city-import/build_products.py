"""Build Shopify productSet inputs for the Bathroom City MELA products we do not carry (20 Oct 2026).

Inputs: bc-missing-raw.json (Bathroom City feed rows), bc-page-info.json (their "Product information" blocks),
        the scratchpad buckets.json (dedupe against our store).
Output: new-products.json (one productSet input per product, finish families merged into variants, plus
        collections / trade band / delivery flags), new-variants.json (finishes to add to existing products),
        review.txt (one line per product for the owner).
Pricing follows store-content/pricing/PRICING-PLAYBOOK.md: cost = list x (1 - SILVER discount) / 1.1,
price = 5% under Bathroom City rounded down, never below cost x 1.1 x 1.25; trade band = deepest of
25/20/15/10/5 that keeps every variant above cost / 0.8 x 1.1.
"""
import json, re, math, html, sys, os, importlib.util
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(H + '/../..')
S = '/tmp/claude-0/-home-user-Excellent-Tiling-Services-/0767eb1f-0008-58fe-8fc0-a4742ee56fa1/scratchpad/'
spec = importlib.util.spec_from_file_location('seo', ROOT + '/seo/generate_product_seo.py'); seo = importlib.util.module_from_spec(spec); spec.loader.exec_module(seo)

raw = {p['title']: p for p in json.load(open(H + '/bc-missing-raw.json'))}
info = json.load(open(H + '/bc-page-info.json'))
buckets = json.load(open(S + 'buckets.json'))
LOC = "gid://shopify/Location/77786087487"
CARE = {k: f"gid://shopify/Metaobject/{v}" for k, v in dict(vanity=290078097471, basin=290078130239, toilet=290078163007, metal=290078195775, mirror=290078228543, bath=290078261311, screen=290078294079, sink=290078326847).items()}
WARR = {k: f"gid://shopify/Metaobject/{v}" for k, v in dict(mixer=290078359615, spout=290078392383, shower=290078425151, accessory=290078457919, basin=290078490687, bath=290078523455, mirror=290078556223, screen=290078588991, sink=290078621759, toilet=290078654527, vanity=290078687295, waste=290078720063).items()}
FIN = ['Oiled Rubbed Bronze', 'Light Gun Metal', 'Brushed Nickel', 'Brushed Brass', 'Gun Metal', 'Matt Black', 'Matt White', 'Matt Grey', 'Gloss White', 'Black Oak', 'Dracula Oak', 'Sorrento Oak', 'Snafell', 'Walnut', 'Chrome', 'Black', 'White', 'Oak', 'Pink', 'Sage', 'Sand', 'Grey']

def strip_fin(t):
    t = ' ' + t + ' '; found = []
    for f in FIN:
        if re.search(r'(?<![A-Za-z])' + re.escape(f) + r'(?![A-Za-z])', t):
            found.append(f); t = re.sub(r'(?<![A-Za-z])' + re.escape(f) + r'(?![A-Za-z])', ' ', t)
    return re.sub(r'\s+', ' ', t).strip(), ' '.join(found)

def clean_title(t):
    t = t.replace('MELA - ', '').replace('MELA -', '').replace('MELA ', '').strip()
    t = t.replace('PALCO/RONDO', 'PALCO / RONDO').replace('FLOVA/PALCO', 'FLOVA / PALCO').replace(' and ', ' & ')
    t = t.replace('Vanity Basin', 'Basin').replace('Shower or Bath Wall Mixer', 'Shower/Bath Wall Mixer')
    t = re.sub(r'\s+', ' ', t).strip()
    if t.startswith('Amio '): t = 'AMIO ' + t[5:]
    return t

# ---- type rules (first match wins) -> (our type, SILVER discount, option name, care, warranty)
RULES = [
    (r'Tallboy', 'Bathroom Tallboy', .25, 'Finish', 'vanity', 'vanity'),
    (r'Ceramic Vanity Top', 'Ceramic Vanity Top', .30, 'Colour', 'basin', 'basin'),
    (r'Mirror Cabinet', 'Mirror Cabinet', .25, 'Finish', 'mirror', 'mirror'),
    (r'LED .*Mirror', 'LED Mirror', .25, 'Finish', 'mirror', 'mirror'),
    (r'Mirror', 'Mirror', .25, 'Frame', 'mirror', 'mirror'),
    (r'Half Inset', 'Half Inset Basin', .30, 'Colour', 'basin', 'basin'),
    (r'Undermount', 'Undermount Basin', .30, 'Colour', 'basin', 'basin'),
    (r'Inset .*Basin', 'Inset Basin', .30, 'Colour', 'basin', 'basin'),
    (r'Wall Mounted .*Basin', 'Wall Hung Basin', .30, 'Colour', 'basin', 'basin'),
    (r'Above Counter', 'Above Counter Basin', .30, 'Colour', 'basin', 'basin'),
    (r'Heated Towel', 'Heated Towel Rail', .30, 'Finish', 'metal', 'accessory'),
    (r'Bath Towel Shelf', 'Bath Towel Shelf', .35, 'Finish', 'metal', 'accessory'),
    (r'Towel Rail', 'Towel Rail', .35, 'Finish', 'metal', 'accessory'),
    (r'Paper Holder', 'Toilet Roll Holder', .35, 'Finish', 'metal', 'accessory'),
    (r'Robe Hook|Hook', 'Bathroom Hook', .35, 'Finish', 'metal', 'accessory'),
    (r'Glass Shelf', 'Shelf Holder', .35, 'Finish', 'metal', 'accessory'),
    (r'Chopping Board|Colander', 'Kitchen Sink Accessory', .35, 'Finish', 'sink', 'accessory'),
    (r'Floor Waste', 'Floor Waste', .40, 'Finish', 'metal', 'waste'),
    (r'Pop Up Waste', 'Pop Up Waste', .40, 'Finish', 'metal', 'waste'),
    (r'Bidet Seat', 'Bidet Seat', .20, 'Finish', 'toilet', 'toilet'),
    (r'Toilet Suite', 'Toilet Suite', .40, 'Finish', 'toilet', 'toilet'),
    (r'Toilet Button|Flush Button', 'Toilet Flush Button', .40, 'Finish', 'metal', 'toilet'),
    (r'Shower Panel|Bath Panel', 'Frameless Shower Panel', .40, 'Finish', 'screen', 'screen'),
    (r'Stainless Steel Sink', 'Kitchen Sink', .40, 'Finish', 'sink', 'sink'),
    (r'Filter Sink Mixer|Sink Mixer|Kitchen Mixer', 'Kitchen Sink Mixer', .40, 'Finish', 'metal', 'mixer'),
    (r'Basin Mixer', 'Basin Mixer', .40, 'Finish', 'metal', 'mixer'),
    (r'Wall Spout & Mixer Set', 'Wall Mixer', .40, 'Finish', 'metal', 'mixer'),
    (r'Wall Mixer', 'Wall Mixer', .40, 'Finish', 'metal', 'mixer'),
    (r'Wall Spout', 'Wall Spout', .40, 'Finish', 'metal', 'spout'),
    (r'Shower Arm Head', 'Shower Head', .40, 'Finish', 'metal', 'shower'),
    (r'Ceiling Arm', 'Ceiling Shower Arm', .40, 'Finish', 'metal', 'shower'),
    (r'Shower Arm', 'Shower Arm', .40, 'Finish', 'metal', 'shower'),
    (r'Shower Head', 'Shower Head', .40, 'Finish', 'metal', 'shower'),
    (r'Combo Shower Set|Combination', 'Combination Shower Set', .40, 'Finish', 'metal', 'shower'),
    (r'Hand Shower Set', 'Hand Shower Set', .40, 'Finish', 'metal', 'shower'),
    (r'Vanity', 'Wall Hung Vanity', .25, 'Colour', 'vanity', 'vanity'),
]
def classify(base, bc):
    for pat, typ, disc, opt, care, warr in RULES:
        if re.search(pat, base, re.I):
            if typ == 'Wall Hung Vanity' and 'double basin vanity' in bc['tags']: typ = 'Double Wall Hung Vanity'
            return typ, disc, opt, care, warr
    raise SystemExit('no rule for ' + base)

VAN_W = {400: 30, 450: 32, 600: 40, 750: 47.5, 900: 55, 1050: 62.5, 1200: 70, 1350: 78, 1500: 85, 1650: 92, 1800: 100}
def size_mm(t):
    m = re.search(r'\b(\d{3,4})(?:mm)?\b', t); return int(m.group(1)) if m else None

# per type: (ship, weight fn, manual collections, family tags)
def conv(typ, base, bc):
    sz = size_mm(base) or 0
    if typ in ('Wall Hung Vanity', 'Double Wall Hung Vanity'):
        return 'local', VAN_W.get(sz, 60), ['bathroom-vanities', 'wall-hung-vanities', 'double-vanities' if typ.startswith('Double') else 'single-vanities'], ['Bathroom Vanity', 'Wall Hung Vanity'] + (['Double Vanity'] if typ.startswith('Double') else [])
    if typ == 'Bathroom Tallboy': return 'local', 32, ['bathroom-storage-tallboys'], ['Bathroom Storage', 'Tallboy', 'Wall Hung']
    if typ == 'Ceramic Vanity Top': return ('local' if sz >= 1200 else 'bulky'), {600: 15, 750: 18, 900: 22, 1200: 30, 1500: 38}.get(sz, 25), ['basins', 'bathroom-vanities'], ['Vanity Top', 'Ceramic', 'Basin']
    if typ.endswith('Basin'):
        sub = {'Above Counter Basin': 'above-counter-basins', 'Inset Basin': 'inset-basins', 'Half Inset Basin': 'inset-basins', 'Undermount Basin': 'undermount-basins', 'Wall Hung Basin': 'basins'}[typ]
        return 'bulky', (12 if 'Concrete' in base else 9), ['basins', sub], ['Basin', 'Concrete' if 'Concrete' in base else 'Ceramic']
    if typ == 'Mirror Cabinet': return 'local', {1500: 35, 1800: 42}.get(sz, 25), ['mirrors', 'mirror-cabinets'], ['Mirror', 'Mirror Cabinet', 'Bathroom Storage', 'Shaving Cabinet']
    if typ == 'LED Mirror': return ('local' if sz >= 1050 else 'bulky'), {1200: 14, 1500: 22, 1800: 28}.get(sz, 10), ['mirrors', 'led-mirrors'], ['Mirror', 'LED Mirror', 'Backlit Mirror', 'Anti Fog', 'Dimmable']
    if typ == 'Mirror': return ('local' if sz >= 1050 else 'bulky'), {700: 8, 750: 8, 800: 9, 900: 10, 1200: 13}.get(sz, 9), ['mirrors', 'plain-mirrors'], ['Mirror', 'Framed Mirror'] + (['Round Mirror'] if 'Round' in base else [])
    if typ == 'Heated Towel Rail': return 'bulky', 8, ['towel-rails', 'accessories'], ['Accessories', 'Towel Rail', 'Heated Towel Rail']
    if typ == 'Towel Rail': return 'parcel', (2.7 if 'Double' in base else 2.2) + (0.4 if sz >= 800 else 0), ['accessories', 'towel-rails'], ['Accessories', 'Towel Rail', 'Double Towel Rail' if 'Double' in base else 'Single Towel Rail']
    if typ == 'Bath Towel Shelf': return 'bulky', 2.2, ['accessories', 'towel-rails'], ['Accessories', 'Towel Rail', 'Bath Towel Shelf']
    if typ == 'Toilet Roll Holder': return 'parcel', 0.5, ['accessories', 'toilet-roll-holders'], ['Accessories', 'Toilet Roll Holder', 'Paper Holder']
    if typ == 'Bathroom Hook': return 'parcel', 0.25, ['accessories', 'bathroom-hooks'], ['Accessories', 'Bathroom Hook', 'Hook']
    if typ == 'Shelf Holder': return 'parcel', 0.7, ['accessories', 'soap-shelf-holders'], ['Accessories', 'Shelf Holder', 'Glass Shelf']
    if typ == 'Kitchen Sink Accessory': return 'parcel', 1, ['kitchen-laundry', 'sinks'], ['Kitchen Sink', 'Sink Accessory', 'Kitchen']
    if typ == 'Floor Waste': return 'parcel', 0.5, ['bathroom-wastes'], ['Bathroom Waste', 'Floor Waste', 'Accessories']
    if typ == 'Pop Up Waste': return 'parcel', 0.35, ['bathroom-wastes', 'accessories'], ['Bathroom Waste', 'Pop Up Waste', 'Accessories']
    if typ == 'Bidet Seat': return 'bulky', 5, ['toilets'], ['Toilet', 'Bidet Seat', 'Smart Toilet']
    if typ == 'Toilet Suite': return 'local', 38, ['toilets'] + (['rimless-toilets'] if 'Rimless' in base else []) + (['wall-faced-toilets'] if 'Wall Face' in base else []), ['Toilet', 'Toilet Suite'] + (['Rimless'] if 'Rimless' in base else []) + (['Smart Toilet'] if 'Smart' in base else [])
    if typ == 'Toilet Flush Button': return 'parcel', 0.4, ['toilets'], ['Toilet', 'Toilet Hardware', 'Flush Button']
    if typ == 'Frameless Shower Panel': return 'local', (18 if 'Bath Panel' in base else 30), ['shower-screens', 'frameless-shower-panels'], ['Shower Screen', 'Frameless Shower Panel', '10mm Glass']
    if typ == 'Kitchen Sink': return 'bulky', (5 if sz < 600 else 11), ['sinks', 'kitchen-laundry'], ['Kitchen Sink', 'Sink', 'Stainless Steel']
    if typ == 'Kitchen Sink Mixer': return 'parcel', (3 if 'Pull Out' in base else 2.4), ['tapware', 'kitchen-tapware', 'kitchen-laundry'], ['Tapware', 'Kitchen Tapware', 'Sink Mixer']
    if typ == 'Basin Mixer': return 'parcel', (2 if 'Tall' in base else 1.4), ['tapware', 'basin-mixers'], ['Tapware', 'Basin Mixer'] + (['Tall Basin Mixer'] if 'Tall' in base else [])
    if typ == 'Wall Mixer': return 'parcel', (2.5 if 'Set' in base else 1.4), ['tapware', 'wall-mixers'], ['Tapware', 'Wall Mixer', 'Shower Mixer', 'Bath Mixer'] + (['Spout & Mixer Set'] if 'Set' in base else [])
    if typ == 'Wall Spout': return 'parcel', 1.1, ['tapware', 'spouts-outlets'], ['Tapware', 'Wall Spout', 'Spout'] + (['Swivel Spout'] if 'Swivel' in base else [])
    if typ in ('Shower Arm', 'Ceiling Shower Arm', 'Shower Head'): return 'parcel', 1.2, ['tapware', 'shower-tapware'], ['Tapware', 'Shower Tapware', typ]
    if typ == 'Hand Shower Set': return 'bulky', 3, ['tapware', 'shower-tapware'], ['Tapware', 'Shower Tapware', 'Hand Shower', 'Shower Set', 'Shower Rail']
    if typ == 'Combination Shower Set': return 'bulky', 4.5, ['tapware', 'shower-tapware'], ['Tapware', 'Shower Tapware', 'Combination Shower Set', 'Shower Rail']
    raise SystemExit('no conv for ' + typ)

def price_cost(list_price, bc_price, disc):
    cost = round(list_price * (1 - disc) / 1.1, 2)
    floor = cost * 1.1 * 1.25
    price = math.floor(bc_price * 0.95); flag = ''
    if price < floor: price = math.ceil(floor); flag = f'Bathroom City ${bc_price:g} is below our floor; priced at the floor'
    margin = (price / 1.1 - cost) / (price / 1.1) * 100
    return price, cost, round(margin, 1), flag

def band_for(variants):
    for b in (25, 20, 15, 10, 5):
        if all(v['price'] * (1 - b / 100) >= v['cost'] / 0.8 * 1.1 for v in variants): return b
    return 0

def dims_from(kv):
    for k in ('Product Dimensions', 'Dimensions', 'Dimension'):
        for kk, vv in kv:
            if kk == k: return vv
    return None
def wdh(d):
    out = {}
    if not d: return out
    for m in re.finditer(r'(\d{2,4})\s*\(\s*([WDHL])\s*\)', d): out[m.group(2)] = int(m.group(1))
    if not out:
        m = re.search(r'(\d{3,4})\s*[x×\*]\s*(\d{3,4})(?:\s*[x×\*]\s*(\d{2,4}))?\s*mm', d)
        if m: out = {'W': int(m.group(1)), 'H' if not m.group(3) else 'D': int(m.group(2))}; 
        if m and m.group(3): out['H'] = int(m.group(3))
    return out

def tidy(v):
    v = re.sub(r'\s*\*\s*', ' x ', v); v = re.sub(r'\s+', ' ', v).strip(' .;')
    return v

SKIP_NOTE = re.compile(r'\$|Bathroom City|Please Note|Upgrade to|Warranty|Delivery|choice of', re.I)
def build_desc(base, typ, members, group_kv, notes, finishes, cols):
    bc0 = members[0]['bc']
    intro = html.unescape(re.sub(r'<[^>]+>', ' ', (bc0['body_html'] or '').split('</p>')[0]))
    intro = re.sub(r'\s+', ' ', intro).strip()
    intro = re.sub(r'^\s*(Mela|MELA)\s+', '', intro)
    if len(intro) > 650: intro = intro[:650].rsplit('. ', 1)[0] + '.'
    if 'MWS' in intro or len(intro) < 40: intro = ''
    li = []
    codes = sorted({m['sku'] for m in members if m['sku']})
    if codes and len(codes) <= 3: li.append('Model: ' + ', '.join(codes))
    order = ['Product Dimensions', 'Dimensions', 'Dimension', 'Material', 'Materials', 'Hardware', 'Kickboard', 'Kickboard Size (optional extra)', 'WELS Star Rating', 'WELS Rating', 'Litres Per Minute', 'Cartridge Size (mm)', 'Cartridge Size', 'WELS Registration No', 'Registration No', 'Compatibility', 'Type & Mount', 'Mounting Way', 'Installation', 'Voltage', 'Output', 'Rater Power', 'IP Rating', 'IP Rate', 'Lead Length', 'Number of Bars', 'Wiring Type', 'Wiring Position', 'Colour Temperature', 'Light Colour', 'Switch Type', 'Memory Function', 'CRI', 'Outlet', 'Seat', 'Trap Type', 'S Trap', 'P Trap', 'Bottom Inlet', 'Rear Entry', 'Water Inlet', 'Water Pressure Requirement']
    label = {'Product Dimensions': 'Dimensions', 'Dimension': 'Dimensions', 'Materials': 'Material', 'WELS Star Rating': 'WELS rating', 'WELS Rating': 'WELS rating', 'Litres Per Minute': 'Flow rate', 'Cartridge Size (mm)': 'Cartridge', 'Cartridge Size': 'Cartridge', 'WELS Registration No': 'WELS registration', 'Registration No': 'WELS registration', 'Kickboard Size (optional extra)': 'Kickboard (optional extra)', 'Rater Power': 'Rated power', 'IP Rate': 'IP rating', 'Type & Mount': 'Type and mounting', 'Mounting Way': 'Mounting', 'Colour Temperature': 'Colour temperature', 'Light Colour': 'Light colour', 'Switch Type': 'Switch', 'Memory Function': 'Memory function', 'Number of Bars': 'Bars', 'Wiring Type': 'Wiring', 'Wiring Position': 'Wiring position', 'Lead Length': 'Lead length', 'Trap Type': 'Trap', 'Water Inlet': 'Water inlet', 'Water Pressure Requirement': 'Water pressure', 'Bottom Inlet': 'Bottom inlet', 'Rear Entry': 'Rear entry'}
    seen = set()
    for k in order:
        for kk, vv in group_kv:
            if kk == k and label.get(k, k) not in seen:
                val = tidy(vv)
                if k == 'Litres Per Minute' and 'min' not in val.lower(): val += ' L/min'
                val = val.replace('L / MIN', 'L/min').replace('L/MIN', 'L/min')
                if k in ('Cartridge Size (mm)', 'Cartridge Size') and 'mm' not in val: val += ' mm'
                li.append(f'{label.get(k, k)}: {val}'); seen.add(label.get(k, k)); break
    if finishes: li.append(('Colours: ' if cols in ('vanity', 'basin') else 'Finishes: ') + ', '.join(finishes))
    inc = []; take = False
    for n in notes:
        if re.match(r'Package includes', n, re.I): take = True; continue
        if re.match(r'Please Note', n, re.I): take = False
        if take and not SKIP_NOTE.search(n):
            line = n.strip()
            if finishes: line, _ = strip_fin(line)
            inc.append('Includes ' + line)
    li += inc
    if typ in ('Wall Hung Vanity', 'Double Wall Hung Vanity') and any('Stone' in n for n in notes):
        li.append('Matt White, coloured or fluted basin upgrade available on request')
        li.append('Stone cutting, tapware and waste are not included')
    for n in notes:
        if re.search(r'licensed electrician', n, re.I) and not any('electrician' in x for x in li): li.append(n.strip().rstrip('.'))
    links = {'vanity': '<p>Browse more <a href="/collections/wall-hung-vanities">wall-hung bathroom vanities</a> or explore our <a href="/collections/bathroom-vanities">bathroom vanity collection</a>.</p>',
             'basin': '<p>Browse more <a href="/collections/basins">bathroom basins</a>.</p>', 'mirror': '<p>Browse more <a href="/collections/mirrors">bathroom mirrors</a>.</p>',
             'metal': '<p>Browse more <a href="/collections/tapware">bathroom tapware</a> and <a href="/collections/accessories">accessories</a>.</p>',
             'toilet': '<p>Browse more <a href="/collections/toilets">toilets</a>.</p>', 'screen': '<p>Browse more <a href="/collections/shower-screens">shower screens</a>.</p>', 'sink': '<p>Browse more <a href="/collections/sinks">kitchen sinks</a>.</p>'}
    html_out = (f'<p>{html.escape(intro)}</p>' if intro else f'<p>MELA {html.escape(base)}.</p>') + '<ul>' + ''.join(f'<li>{html.escape(x)}</li>' for x in li) + '</ul>' + links.get(cols, '')
    if typ in ('Wall Hung Vanity', 'Double Wall Hung Vanity'):
        html_out += '<h4>More details</h4><ul><li>Choose your stone colour, basin, stone cutting and kickboard above. Tell us anything else when you order, or see the samples in our Maddington showroom.</li></ul>'
    return html_out, li

def seo_for(title, li, typ, d=None):
    first = title + '.'
    bits = []
    if d and 'W' in d: bits.append(' x '.join(str(d[k]) for k in ('W', 'D', 'H') if k in d) + ' mm')
    bits += [x for x in li if re.match(r'(WELS rating|Flow rate|Material|Colours|Finishes):', x)][:2]
    d = first + (' ' + '. '.join(bits) + '.' if bits else '')
    d = re.sub(r'\s+', ' ', d)
    return seo.seo_title(title), seo.fit(d)

def range_of(base):
    w = base.split()[0]
    if re.fullmatch(r'[A-Z]{3,}(?: / [A-Z]{3,})?', ' '.join(base.split()[:3]).split(' Wall')[0]) or re.fullmatch(r'[A-Z]{3,}', w): 
        return (base.split(' / ')[0].split()[0] + (' / ' + base.split(' / ')[1].split()[0] if ' / ' in base.split(' Wall')[0][:20] else '')) if '/' in base[:20] else w
    return None

# ---- dedupe against the master price list (finish families: our products carry finishes as variants)
import csv
ALIAS = [(r'^(PALCO / RONDO) Ceiling Arm$', r'\1 Ceiling Shower Arm'), (r'Robe Hook$', 'Hook'), (r'Twin Combo Shower Set with Rail', 'Combination Shower Set with Rail'),
         (r'^BRUNO Shower/Bath Wall Mixer$', 'BRUNO Wall Mixer'), (r'^Corner Glass Shelf$', 'BRUNO Corner Glass Shelf Holder'), (r'^SURI (\d+) Round Mirror Frame$', r'SURI Framed Round Mirror'),
         (r'^PORTER (\d+) Mirror Cabinet$', 'PORTER Mirror Cabinet')]
def alias(base):
    for a, b in ALIAS: base = re.sub(a, b, base)
    return base
ours = {}
for r in csv.DictReader(open(ROOT + '/store-content/pricing/store-pricing-2026-10-03.csv')):
    if r['vendor'] != 'MELA': continue
    k, _ = strip_fin(clean_title(r['product'])); k = re.sub(r'[^A-Z0-9&]+', ' ', k.upper()).strip()
    o = ours.setdefault(k, {'title': r['product'], 'variants': set(), 'pid': r['pid']}); o['variants'].add(r['variant'].upper())
# existing products that take new finishes: option name(s)
TARGET_OPTS = {'MELA BAYLEE Above Counter Basin': ['Colour'], 'MELA CLARK 400 Wall Hung Tallboy': ['Finish'], 'MELA CLARK 600 Wall Hung Vanity with 2 Drawers': ['Finish'], 'MELA DAVISSON Above Counter Basin': ['Colour'],
    'MELA FLOVA / PALCO Swivel Wall Spout': ['Colour'], 'MELA FLOVA / PALCO Wall Spout': ['Colour'], 'MELA PALCO / RONDO 800 Double Towel Rail': ['Colour'], 'MELA PALCO / RONDO Hand Shower Set with Rail': ['Colour'],
    'MELA PALCO / RONDO Paper Holder': ['Colour'], 'MELA PALCO / RONDO Shower Arm': ['Colour'], 'MELA PALCO / RONDO Shower Head': ['Colour'], 'MELA PALCO / RONDO Straight Shower Arm': ['Colour'], 'MELA PALCO Medium Basin Mixer': ['Colour'],
    'MELA PALCO Tall Basin Mixer': ['Colour'], 'MELA PORTER Mirror Cabinet': ['Size', 'Finish'], 'MELA RONDO Pull Out Sink Mixer': ['Finish'], 'MELA RONDO Swivel Wall Spout': ['Finish'], 'MELA PALCO / RONDO Ceiling Shower Arm': ['Colour'],
    'MELA PALCO / RONDO Hook': ['Colour'], 'MELA BRUNO Hook': ['Colour'], 'MELA BRUNO Wall Mixer': ['Colour'], 'MELA PALCO / RONDO Combination Shower Set with Rail': ['Colour'], 'MELA SURI Framed Round Mirror': ['Size', 'Finish']}
groups = {}; porter = []; have = []
for title, _ in buckets['new'] + [(t, None) for t, *_ in buckets['new_variant']]:
    base, fin = strip_fin(clean_title(title)); base = alias(base)
    k = re.sub(r'[^A-Z0-9&]+', ' ', base.upper()).strip()
    if k in ours:
        o = ours[k]; f = fin or ('White' if 'Basin' in base else '')
        size = (str(size_mm(clean_title(title))) + 'mm') if 'Size' in TARGET_OPTS.get(o['title'], []) else None
        vt = f.upper() if not size else f'{size} / {f}'.upper()
        if 'Black' == f and 'MATT BLACK' in o['variants'] and 'Mirror' in base: vt = 'MATT BLACK'
        if vt in o['variants'] or (not f and 'DEFAULT' in o['variants']) or (size and any(v.startswith(size.upper()) and v.endswith(f.upper()) for v in o['variants'])):
            have.append((title, o['title'])); continue
        porter.append((title, o['title'], f, size)); continue
    groups.setdefault(base, []).append({'fin': fin, 'title': title, 'bc': raw[title]})
skipped = []
products = []; review = []
for base, members in groups.items():
    bc0 = members[0]['bc']
    typ, disc, optname, care, warr = classify(base, bc0)
    ship, weight, mcols, fam = conv(typ, base, bc0)
    for m in members:
        v = m['bc']['variants'][0]
        m['sku'] = (v['sku'] or '').strip()
        listp = float(v['compare_at_price'] or v['price']); bcp = float(v['price'])
        m['bc_list'] = listp; m['bc_price'] = bcp
        m['price'], m['cost'], m['margin'], m['flag'] = price_cost(listp, bcp, disc)
        if not m['fin']: m['fin'] = 'White' if typ.endswith('Basin') or typ == 'Ceramic Vanity Top' else ('Standard' if len(members) > 1 else '')
    keep = []
    for m in members:
        if m['flag'] and m['price'] > m['bc_price'] * 1.02 or 'CLEARANCE' in (m['bc']['body_html'] or '').upper():
            skipped.append({'bc_title': m['title'], 'bc_handle': m['bc']['handle'], 'bc_list': m['bc_list'], 'bc_price': m['bc_price'], 'our_floor_price': m['price'], 'cost': m['cost'], 'why': 'Bathroom City clearance price is below our profit floor; not matched (playbook)'})
        else: keep.append(m)
    members = keep
    if not members: continue
    members.sort(key=lambda m: (m['price'], m['fin']))
    band = band_for(members)
    multi = len(members) > 1
    finishes = [m['fin'] for m in members] if multi else ([members[0]['fin']] if members[0]['fin'] else [])
    kv = []; notes = []
    for m in members:
        pi = info.get(m['bc']['handle']) or {'kv': [], 'notes': []}
        for k, v in pi['kv']:
            if k not in [x for x, _ in kv]: kv.append([k, v])
        for n in pi['notes']:
            if n not in notes: notes.append(n)
    desc, li = build_desc(base, typ, members, kv, notes, finishes if multi else [], care)
    title = 'MELA ' + base
    d = wdh(dims_from(kv))
    seo_t, seo_d = seo_for(title, li, typ, d)
    rng = range_of(base)
    sz = size_mm(base)
    tags = ['MELA'] + fam + ([rng.replace(' / ', '/').split('/')[0]] if rng else []) + ([f'{sz}mm'] if sz and typ not in ('Floor Waste',) else []) + finishes
    tags += {'local': ['ship-local-only', 'ebay-pickup-only'], 'bulky': ['ship-bulky', 'ship-parcel'], 'parcel': ['ship-parcel']}[ship]
    if rng and ' / ' in rng: tags.append(rng.split(' / ')[1])
    if 'Fluted' in base: tags.append('Fluted Vanity')
    if 'Curved' in base: tags.append('Curved Vanity')
    if any(f['flag'] for f in members): tags.append('bc-sale-below-floor')
    tags = sorted(set(t for t in tags if t))
    mf = [('supplier', 'single_line_text_field', 'Bathroom City'), ('trade_band', 'number_integer', str(band)), ('care_guide', 'metaobject_reference', CARE[care]), ('warranty_terms', 'metaobject_reference', WARR[warr])]
    if rng: mf.append(('range', 'single_line_text_field', rng))
    mat = next((v for k, v in kv if k in ('Material', 'Materials')), None)
    if mat: mf.append(('material', 'single_line_text_field', tidy(mat)[:250]))
    for key, k in (('width_mm', 'W'), ('depth_mm', 'D'), ('height_mm', 'H')):
        if k in d: mf.append((key, 'number_integer', str(d[k])))
    for key, k in (('wels_rating', 'WELS Star Rating'), ('wels_rating', 'WELS Rating'), ('flow_rate', 'Litres Per Minute'), ('cartridge', 'Cartridge Size (mm)'), ('cartridge', 'Cartridge Size'), ('wels_registration', 'WELS Registration No'), ('wels_registration', 'Registration No')):
        v = next((v for kk, v in kv if kk == k), None)
        if v and key not in [x for x, _, _ in mf]:
            if key == 'flow_rate' and 'min' not in v.lower(): v = v + ' L/min'
            v = v.replace('L / MIN', 'L/min').replace('L/MIN', 'L/min')
            mf.append((key, 'single_line_text_field', tidy(v)))
    if typ in ('Wall Hung Vanity', 'Double Wall Hung Vanity') and members[0]['sku'].startswith('KIT.'):
        mf.append(('lead_time', 'single_line_text_field', 'Made to order: allow about 2 weeks for the stonemason to cut the top'))
    files = []; seen_img = set()
    for m in members:
        for i, im in enumerate(m['bc']['images']):
            if im['src'] in seen_img: continue
            seen_img.add(im['src']); files.append({'originalSource': im['src'], 'alt': title + (f' in {m["fin"]}' if multi and m['fin'] else '') + (f', view {i+1}' if i else ''), 'contentType': 'IMAGE'})
    variants = []
    for m in members:
        vv = {'optionValues': [{'optionName': optname if multi else 'Title', 'name': m['fin'] if multi else 'Default Title'}], 'price': str(m['price']), 'inventoryPolicy': 'CONTINUE', 'taxable': True,
              'inventoryItem': {'tracked': True, 'cost': str(m['cost']), 'requiresShipping': True, 'measurement': {'weight': {'value': weight, 'unit': 'KILOGRAMS'}}},
              'inventoryQuantities': [{'locationId': LOC, 'name': 'available', 'quantity': 0}]}
        if m['sku']: vv['sku'] = m['sku'] if len([x for x in members if x['sku'] == m['sku']]) == 1 else m['sku'] + '.' + ''.join(w[0] for w in m['fin'].split())
        if multi and m['bc']['images']: vv['file'] = {'originalSource': m['bc']['images'][0]['src'], 'alt': title + f' in {m["fin"]}', 'contentType': 'IMAGE'}
        variants.append(vv)
    inp = {'title': title, 'descriptionHtml': desc, 'vendor': 'MELA', 'productType': typ, 'tags': tags, 'status': 'ACTIVE', 'seo': {'title': seo_t, 'description': seo_d},
           'metafields': [{'namespace': 'ets', 'key': k, 'type': t, 'value': v} for k, t, v in mf], 'files': files,
           'productOptions': [{'name': optname if multi else 'Title', 'values': [{'name': m['fin'] if multi else 'Default Title'} for m in members]}], 'variants': variants}
    products.append({'input': inp, 'collections': mcols + ([f'trade-list-{band}'] if band else []), 'ship': ship, 'band': band, 'members': [{'bc_handle': m['bc']['handle'], 'bc_title': m['title'], 'fin': m['fin'], 'sku': m['sku'], 'bc_list': m['bc_list'], 'bc_price': m['bc_price'], 'price': m['price'], 'cost': m['cost'], 'margin': m['margin'], 'flag': m['flag']} for m in members]})
    review.append(f"{title} | {typ} | {len(members)}v | BC {'/'.join(f'{m['bc_price']:g}' for m in members)} | ours {'/'.join(str(m['price']) for m in members)} | cost {'/'.join(f'{m['cost']:g}' for m in members)} | margin {'/'.join(f'{m['margin']:g}' for m in members)}% | band {band} | {ship} | {' ; '.join(sorted({m['flag'] for m in members if m['flag']}))}")
json.dump(products, open(H + '/new-products.json', 'w'), indent=1, ensure_ascii=False)
open(H + '/review.txt', 'w').write('\n'.join(review) + '\n')
# ---- new finish variants for existing products
nv = []
for bc_title, ourt, fin, size in porter:
    p = raw[bc_title]; v = p['variants'][0]
    base, _ = strip_fin(clean_title(bc_title)); typ, disc, *_ = classify(base, p)
    ship, weight, mcols, fam = conv(typ, base, p)
    listp = float(v['compare_at_price'] or v['price']); bcp = float(v['price'])
    price, cost, margin, flag = price_cost(listp, bcp, disc)
    if flag and price > bcp * 1.02 or 'CLEARANCE' in (p['body_html'] or '').upper():
        skipped.append({'bc_title': bc_title, 'bc_handle': p['handle'], 'bc_list': listp, 'bc_price': bcp, 'our_floor_price': price, 'cost': cost, 'why': 'Bathroom City clearance price is below our profit floor; not matched (playbook)'}); continue
    opts = TARGET_OPTS[ourt]; ov = ([{'optionName': opts[0], 'name': size}] if size else []) + [{'optionName': opts[-1], 'name': fin}]
    nv.append({'our_product': ourt, 'pid': ours[re.sub(r'[^A-Z0-9&]+', ' ', alias(strip_fin(clean_title(bc_title))[0]).upper()).strip()]['pid'], 'optionValues': ov, 'weight': weight, 'finish': fin, 'size': size, 'bc_title': bc_title, 'bc_handle': p['handle'], 'sku': v['sku'], 'bc_list': listp, 'bc_price': bcp, 'price': price, 'cost': cost, 'margin': margin, 'flag': flag, 'image': p['images'][0]['src'] if p['images'] else None, 'type': typ})
json.dump(nv, open(H + '/new-variants.json', 'w'), indent=1, ensure_ascii=False)
json.dump(skipped, open(H + '/skipped-clearance.json', 'w'), indent=1, ensure_ascii=False)
print('already ours', len(have), 'skipped clearance variants', len(skipped))
print('products', len(products), 'variants', sum(len(p['input']['variants']) for p in products), 'new finish variants', len(nv))
from collections import Counter
print(Counter(p['input']['productType'] for p in products).most_common())
print('bands', Counter(p['band'] for p in products)); print('flags', sum(1 for p in products for m in p['members'] if m['flag']))
print('payload chars', sum(len(json.dumps(p['input'])) for p in products), 'max', max(len(json.dumps(p['input'])) for p in products))
