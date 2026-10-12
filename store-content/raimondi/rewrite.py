import json, re
allp = json.load(open('all.json')); compat = json.load(open('compat.json'))
by_id = {n['id'].split('/')[-1]: n for n in allp}
by_sku = {v['sku']: n['id'].split('/')[-1] for n in allp for v in n['variants']['nodes'] if v['sku']}
def tail(pid):
    h = by_id[pid]['descriptionHtml']
    i = h.find('<p>Buy ')
    assert i > 0, pid
    return h[i:]
def head(pid):
    h = by_id[pid]['descriptionHtml']
    return h[:h.find('<p>Buy ')]

U = {}  # pid -> dict(title, descriptionHtml, seo)
def add(sku, title, body, seo_title, seo_desc, keep_head=False):
    pid = by_sku[sku]
    desc = (head(pid) if keep_head else '') + body + tail(pid)
    assert len(seo_title) <= 60, (sku, len(seo_title), seo_title)
    assert len(seo_desc) <= 155, (sku, len(seo_desc), seo_desc)
    U[pid] = {'title': title, 'descriptionHtml': desc, 'seo': {'title': seo_title, 'description': seo_desc}}

ZPS = 'Raimondi Zoe Advanced 85A, 105A, 130A and 155A, Pikus Advanced 85, 105 and 130, and SMS 100 and 125 bridge saws'

add('RAI-ZOE85A', 'Raimondi Zoe Advanced Bridge Wet Saw 3HP - 85A, 105A, 130A, 155A',
 '<p>Raimondi Zoe Advanced bridge wet saw with a 3 HP (2.2 kW) single-phase motor, for straight and 45° mitre cuts in porcelain, granite, marble, bricks and pavers. Four cutting lengths: Zoe 85A (85 cm), 105A (105 cm), 130A (130 cm) and 155A (155 cm, Raimondi\'s ZOE 150 ADV).</p>'
 '<ul><li>Blades: 300 mm or 350 mm diameter, 25.4 mm bore. Raimondi supplies it with a 300 mm porcelain blade.</li>'
 '<li>Depth of cut: 80 mm with a 300 mm blade, 110 mm with a 350 mm blade, up to 235 mm in two passes</li>'
 '<li>Tilting motor assembly for bevel cuts from 0° to 45°, adjustable cutting depth, belt drive</li>'
 '<li>Sliding motor carriage on an extruded aluminium rail with four adjustable double-bearing pulleys</li>'
 '<li>Pivoting, floating blade guard; heavy-duty water pump with two jet nozzles; removable 38 L tank</li>'
 '<li>Telescopic legs with an anti-collapse safety catch; cast and extruded aluminium frame</li>'
 '<li>Diagonal cuts: tiles up to 60 x 60 cm on the 85A and 109 x 109 cm on the 155A</li>'
 '<li>In the box: 300 mm porcelain blade, wheel kit, tile pressure device, key kit, wrench and manual</li>'
 '<li>Weight: 85A 80 kg (98 kg packed), 155A 106 kg (147 kg packed)</li></ul>'
 '<p><strong>What fits this saw:</strong> the folding extension table kit, extension side square, telescopic counter square, 5 roller extension table, 90° and 45°/90° sliding squares and the tile holding device (105A, 130A and 155A sizes) all fit every Zoe Advanced, as do Raimondi\'s 300 mm and 350 mm diamond blades. Spares: aluminium rails (85A, 105A, 130A), switch and overload, switch base and cover, bearing and nylon bush, and a 10 A plug and lead. They are all in our Raimondi wet saw accessories collection.</p>',
 'Raimondi Zoe Advanced Wet Saw 85A to 155A | ETS Perth',
 '3HP Raimondi Zoe Advanced bridge saw, 85 to 155cm cut, 300 or 350mm blades, up to 110mm deep. Extension tables, squares and blades that fit. ETS Perth.')

add('RAI-SMS100', 'Raimondi SMS Bridge Wet Saw 3HP - SMS 100 (100cm) & SMS 125 (125cm)',
 '<p>Raimondi SMS bridge wet saw with a 3 HP (2.2 kW) motor and a galvanised steel sliding motor housing, for cutting granite, marble, porcelain, bricks and cement products such as pavers. The SMS 100 cuts up to 100 cm, the SMS 125 up to 125 cm.</p>'
 '<ul><li>Blades: 300 mm or 350 mm diameter, 25.4 mm bore. Raimondi supplies it with a 300 mm porcelain blade.</li>'
 '<li>Depth of cut: 60 mm with a 300 mm blade, 100 mm with a 350 mm blade, up to 135 mm in two passes</li>'
 '<li>Tilting motor assembly for bevel cuts from 0° to 45°, adjustable cutting depth</li>'
 '<li>Pivoting blade guard; heavy-duty water pump with two jet nozzles; removable 38 L polypropylene tank</li>'
 '<li>Telescopic legs. In the box: 300 mm porcelain blade, wheel kit, key kit, wrench and manual</li></ul>'
 '<p><strong>What fits this saw:</strong> the folding extension table kit, extension side square, telescopic counter square, 5 roller extension table, 90° and 45°/90° sliding squares and the tile holding device (the SMS 100 takes the 105A size, the SMS 125 the 130A size), plus Raimondi\'s 300 mm and 350 mm diamond blades and the 10 A plug and lead. See our Raimondi wet saw accessories collection.</p>',
 'Raimondi SMS 100 & 125 Bridge Wet Saw 3HP | ETS Perth',
 '3HP Raimondi SMS bridge saw, 100 or 125cm cut, 300 or 350mm blades, up to 100mm deep. Extension tables, squares and blades that fit. ETS Perth.')

add('RAI-SA80', 'Raimondi SA 80 Trolley Wet Saw 3HP - 80cm cut, 120mm depth',
 '<p>Raimondi SA 80 sliding-trolley wet saw with a 3 HP (2.2 kW) motor, for porcelain, marble, granite, brick and cement products. The tile rides on the trolley through a fixed blade, brick-saw style, for straight and 45° mitre cuts.</p>'
 '<ul><li>Cuts up to 80 cm long and 60 cm wide</li>'
 '<li>Depth of cut: 120 mm in a single pass, 170 mm in two passes</li>'
 '<li>Blades: 300 to 350 mm diameter, 25.4 mm bore (Raimondi\'s catalogue lists up to 360 mm). Supplied with a 350 mm segmented blade.</li>'
 '<li>Manually adjustable cut depth; motor tilts 0° to 45°</li>'
 '<li>Heavy-duty water pump and jet nozzles; removable 38 L polypropylene tank</li>'
 '<li>Anti-tip device, trolley lock and telescopic legs. Wheel kit, key kit, wrench and manual included</li></ul>'
 '<p><strong>What fits this saw:</strong> Raimondi 300 mm, 350 mm and 360 mm diamond blades and the 10 A plug and lead. The Zoe and SMS extension tables and squares do not fit the SA 80.</p>',
 'Raimondi SA 80 Trolley Wet Saw 3HP | ETS Perth',
 'Raimondi SA 80 wet saw, 80cm cut, 120mm deep in one pass, 300 to 350mm blades, 45 degree cuts. For porcelain, stone and brick. Buy from ETS Perth.')

add('RAI-FETPIK75', 'Raimondi Folding Extension Table Kit - suits Zoe, Pikus & SMS wet saws',
 f'<p><strong>Fits:</strong> {ZPS} (Raimondi kit 423KITDL).</p>'
 '<p>Optional kit of folding extension tables plus a 90° left square. The tables bolt to the saw frame and fold down for transport, giving large tiles and slabs flat support beside the cutting table so they sit square for the cut. About 5 kg, 71 x 22 x 10 cm packed.</p>',
 'Raimondi Folding Extension Table, Zoe Pikus SMS | ETS Perth',
 'Folding extension table kit with 90° left square. Fits every Raimondi Zoe Advanced, Pikus Advanced and SMS 100/125 wet saw (423KITDL). Buy from ETS Perth.')

add('RAI-ESSPZ', 'Raimondi Extension Side Square - suits Zoe, Pikus & SMS wet saws',
 f'<p><strong>Fits:</strong> {ZPS} (Raimondi 191CL04A).</p>'
 '<p>Side square that bolts to the saw frame and extends out beside the cutting table, so long tiles and slabs register against a true 90° edge for square, repeatable cuts. About 4.5 kg, 81 x 45 x 13 cm.</p>',
 'Raimondi Extension Side Square, Zoe Pikus SMS | ETS Perth',
 'Bolt-on side square for Raimondi Zoe Advanced, Pikus Advanced and SMS wet saws (191CL04A): a true 90° edge for long tiles and slabs. Buy from ETS Perth.')

add('RAI-PZTCS', 'Raimondi Telescopic Counter Square 90°/45° - suits Zoe, Pikus & SMS',
 f'<p><strong>Fits:</strong> {ZPS} (Raimondi 191CL04A1).</p>'
 '<p>Telescopic set square for 90° and 45° cuts. It extends along the cutting table to support and guide wide tiles and slabs, and locks at the width you need for repeat cuts. About 9 kg, 80 x 33 x 21 cm.</p>',
 'Raimondi Telescopic Counter Square Zoe/Pikus/SMS | ETS Perth',
 'Telescopic 90°/45° set square for Raimondi Zoe Advanced, Pikus Advanced and SMS wet saws (191CL04A1), for wide tiles and repeat cuts. Buy from ETS Perth.')

add('RAI-RETZOE5', 'Raimondi 5 Roller Extension Table - suits Zoe, Pikus & SMS wet saws',
 f'<p><strong>Fits:</strong> {ZPS}, and most other Raimondi bridge saws (Raimondi 374RU5D40I).</p>'
 '<p>Self-standing side bench with five rollers, 705 mm long and 506 mm wide, that stands beside the saw to carry large format tiles and slabs as they feed through the cut. About 20.7 kg.</p>',
 'Raimondi 5 Roller Extension Table, Zoe Pikus SMS | ETS Perth',
 'Self-standing 5 roller side bench (374RU5D40I) for Raimondi Zoe Advanced, Pikus Advanced and SMS wet saws: supports large tiles and slabs through the cut.')

add('RAI-PZ10THD', 'Raimondi Tile Holding Device - suits Zoe 105A/130A/155A, Pikus & SMS',
 '<p><strong>Fits:</strong> choose the size for your saw. Zoe 105A, Pikus 105 and SMS 100 (Raimondi 423BL105ADV); Zoe 130A, Pikus 130 and SMS 125 (423BL130ADV); Zoe 155A (423BL150ADV). New Zoe Advanced saws come with one, so this is the spare, or the longer size if you move to a longer rail.</p>'
 '<p>Pressure bar that clamps the tile firmly on the saw table so it cannot creep during the cut, for clean, accurate edges on long tiles and slabs.</p>',
 'Raimondi Tile Holding Device, Zoe Pikus SMS | ETS Perth',
 'Tile holding device for Raimondi Zoe Advanced, Pikus Advanced and SMS wet saws, in three sizes (423BL105ADV, 130ADV, 150ADV). Buy from ETS Perth.')

add('RAI-SS90', 'Raimondi Sliding Square 90° - suits Zoe, Pikus, SMS, Exploit & Bolt saws',
 '<p><strong>Fits:</strong> Raimondi Zoe Advanced, Pikus Advanced, SMS 100 and 125, Exploit, Bolt and Mistral bridge saws (Raimondi 192SQ03A).</p>'
 '<p>Sliding 90° square that runs in the cutting table groove to hold the tile square to the blade. 42 x 7 x 5 cm, about 900 g.</p>',
 'Raimondi Sliding Square 90°, Zoe Pikus SMS | ETS Perth',
 'Raimondi 90° sliding square (192SQ03A) for Zoe Advanced, Pikus Advanced, SMS, Exploit, Bolt and Mistral bridge saws. Buy online from ETS Perth.')

add('RAI-SS4590', 'Raimondi Sliding Square 45°/90° Left Hand - suits Zoe, Pikus & SMS',
 '<p><strong>Fits:</strong> Raimondi Zoe Advanced, Pikus Advanced, SMS 100 and 125, Exploit, Bolt and Mistral bridge saws (Raimondi 192SQ07A).</p>'
 '<p>Left-hand sliding square for 45° and 90° cuts. It runs in the cutting table groove and flips between the square and mitre settings. 29 x 22 x 7 cm, about 900 g.</p>',
 'Raimondi Left-Hand 45/90 Sliding Square | ETS Perth',
 'Left-hand 45°/90° sliding square (192SQ07A) for Raimondi Zoe Advanced, Pikus Advanced, SMS, Exploit, Bolt and Mistral saws. Buy from ETS Perth.')

add('RAI-SS4590PZ', 'Raimondi Sliding Square 45°/90° Right Hand - suits Zoe, Pikus & SMS',
 '<p><strong>Fits:</strong> Raimondi Zoe Advanced, Pikus Advanced and SMS bridge saws (the right-hand version of the 45°/90° sliding square).</p>'
 '<p>Right-hand sliding square for 45° and 90° cuts, running in the cutting table groove. Pair it with the left-hand square to work from either side of the blade.</p>',
 'Raimondi Right-Hand 45/90 Sliding Square | ETS Perth',
 'Right-hand 45°/90° sliding square for Raimondi Zoe Advanced, Pikus Advanced and SMS wet saws. Buy online from ETS Perth.')

add('RAI-EXWHK', 'Raimondi Wheels & Handle Kit - suits Exploit, Bolt & Mistral saws',
 '<p><strong>Fits:</strong> Raimondi Exploit, Bolt and Mistral bridge saws (Raimondi 315CR02K). Not needed on the Zoe Advanced, Pikus Advanced, SMS or SA 80, which come with a wheel kit as standard.</p>'
 '<p>Four wheels and two handles that bolt to the saw frame, so the saw can be tipped and wheeled around site like a trolley. About 3.3 kg.</p>',
 'Raimondi Wheels & Handle Kit for Exploit, Bolt | ETS Perth',
 'Four wheels and handles kit (315CR02K) for Raimondi Exploit, Bolt and Mistral bridge saws. Zoe, Pikus and SMS saws already include a wheel kit. ETS Perth.')

add('RAI-SW/EX/PK/ZO', 'Raimondi Switch & Overload - suits Zoe, Pikus & Exploit wet saws',
 '<p><strong>Fits:</strong> Raimondi Zoe Advanced, Pikus Advanced and Exploit wet saws.</p>'
 '<p>Replacement on/off switch with thermal overload for the saw motor. Must be fitted by a licensed electrician.</p>',
 'Raimondi Switch & Overload, Zoe Pikus Exploit | ETS Perth',
 'Replacement switch and overload for Raimondi Zoe Advanced, Pikus Advanced and Exploit wet saws. Fit by a licensed electrician. Buy from ETS Perth.')

add('RAI-SCBEX/PK/ZOE', 'Raimondi Switch Base & Cover - suits Zoe, Pikus & Exploit wet saws',
 '<p><strong>Fits:</strong> Raimondi Zoe Advanced, Pikus Advanced and Exploit wet saws.</p>'
 '<p>Complete switch box: the base and cover that house the switch and overload on the saw frame. Switch sold separately.</p>',
 'Raimondi Switch Base & Cover, Zoe Pikus Exploit | ETS Perth',
 'Switch base and cover for Raimondi Zoe Advanced, Pikus Advanced and Exploit wet saws. Houses the switch and overload. Buy online from ETS Perth.')

add('RAI-ZOEBNB', 'Raimondi Bearing & Nylon Bush - suits Zoe & Pikus wet saws',
 '<p><strong>Fits:</strong> Raimondi Zoe Advanced and Pikus Advanced wet saws. Each saw uses four; sold singly.</p>'
 '<p>Replacement carriage bearing with its nylon bush. The motor carriage runs on four of these pulleys along the aluminium rail; replace them when the carriage develops play or runs rough.</p>',
 'Raimondi Bearing & Nylon Bush, Zoe & Pikus saws | ETS Perth',
 'Carriage bearing and nylon bush for Raimondi Zoe Advanced and Pikus Advanced wet saws. Four per saw, sold singly. Buy online from ETS Perth.')

add('RAI-PL10AMP', 'Raimondi 10 Amp Plug & 3m Lead - suits Raimondi wet saws',
 '<p><strong>Fits:</strong> Raimondi wet saws on a 10 A single-phase supply, including the Zoe Advanced, SMS, SA 80 and Pikus Advanced.</p>'
 '<p>Pre-wired replacement lead, 3 m long, with a hi-vis 10 A plug. Must be fitted by a licensed electrician.</p>',
 'Raimondi 10 Amp Plug & Lead for Wet Saws | ETS Perth',
 'Pre-wired 3m lead with hi-vis 10 amp plug for Raimondi Zoe, SMS, SA 80 and Pikus wet saws. Fit by a licensed electrician. Buy from ETS Perth.')

add('RAI-ZOE85SAR', 'Raimondi Zoe Spare Aluminium Rail - 85A, 105A or 130A',
 '<p><strong>Fits:</strong> Raimondi Zoe Advanced. Choose the rail for your saw: 85A, 105A or 130A.</p>'
 '<p>Extruded aluminium replacement rail that the motor carriage runs along. Replace a rail that is bent, worn or scored to bring the cut back true.</p>',
 'Raimondi Zoe Spare Rail 85A 105A 130A | ETS Perth',
 'Extruded aluminium replacement rail for the Raimondi Zoe Advanced wet saw, in 85A, 105A and 130A lengths. Buy online from ETS Perth.')

add('RAI-DS13300', 'Raimondi Double Re-Usable Tile Spacer - 1 & 3mm (grey) or 2 & 5mm (red), 300 pack',
 '<p>Raimondi DOUBLE: a removable, reusable spacer that gives two joint widths from one piece. Grey makes 1 mm or 3 mm joints (Raimondi 282D1-3C300), red makes 2 mm or 5 mm (282D2-5C300). Each comes as a resealable bucket of 300.</p>'
 '<ul><li>Two sides of the spacer set one width, the other two sides set the other</li>'
 '<li>Used along the tile edges rather than at the corners, which suits large format tiles</li>'
 '<li>One flat face, so it sits flush against the floor, in corners and on walls</li>'
 '<li>Generous 37 x 37 mm size: easy to grab when placing and pulling out</li>'
 '<li>Most of the spacer sits above the tile and the plastic will not bond to thin-set adhesive, so it pulls out clean and can be used again and again</li></ul>',
 'Raimondi Double Reusable Tile Spacer 1-3mm 2-5mm | ETS Perth',
 'Raimondi DOUBLE reusable edge spacer: grey for 1 and 3mm joints, red for 2 and 5mm, bucket of 300. Pulls out clean, use again. Buy online from ETS Perth.')

# blades: keep the existing text, add a Fits line and a clearer title
SAW3 = 'Raimondi Zoe Advanced (all sizes), SMS 100 and 125, and SA 80 wet saws, and any other saw that takes a 300 to 350 mm blade with a 25.4 mm bore.'
BL = [
 ('RAI-DB12SET300B', 'Raimondi Diamond Blade 300mm Porcelain Continuous Rim - suits Zoe, SMS & SA 80', SAW3, 'Raimondi 300mm Porcelain Blade, Zoe SMS SA 80 | ETS Perth'),
 ('RAI-DBCC300', 'Raimondi Diamond Blade 300mm Continuous Rim - suits Zoe, SMS & SA 80', SAW3, 'Raimondi 300mm Continuous Rim Blade, Zoe SMS | ETS Perth'),
 ('RAI-DBSET300B', 'Raimondi Diamond Blade 300mm Segmented Porcelain - suits Zoe, SMS & SA 80', SAW3, 'Raimondi 300mm Segmented Blade, Zoe SMS SA 80 | ETS Perth'),
 ('RAI-DBSET300G', 'Raimondi Segmented Diamond Blade 300mm Granite - suits Zoe, SMS & SA 80', SAW3, 'Raimondi 300mm Granite Blade, Zoe SMS SA 80 | ETS Perth'),
 ('RAI-DBCC350', 'Raimondi Diamond Blade 350mm Continuous Rim - suits Zoe, SMS & SA 80', SAW3, 'Raimondi 350mm Continuous Rim Blade, Zoe SMS | ETS Perth'),
 ('RAI-DBCCT350', 'Raimondi Diamond Blade 350mm Turbo - suits Zoe, SMS & SA 80', SAW3, 'Raimondi 350mm Turbo Blade, Zoe SMS SA 80 | ETS Perth'),
 ('RAI-DBSET350B', 'Raimondi Segmented Diamond Blade 350mm Porcelain - suits Zoe, SMS & SA 80', SAW3, 'Raimondi 350mm Porcelain Blade, Zoe SMS SA 80 | ETS Perth'),
 ('RAI-DBSET350G', 'Raimondi Segmented Diamond Blade 350mm Granite - suits Zoe, SMS & SA 80', SAW3, 'Raimondi 350mm Granite Blade, Zoe SMS SA 80 | ETS Perth'),
 ('RAI-DBSET360E', 'Raimondi Diamond Blade 360mm Segmented Economy - suits SA 80, SMS & Zoe', 'Raimondi SA 80, SMS and Zoe Advanced wet saws (the 14-inch class: Raimondi\'s catalogue lists 300 to 360 mm blades for them), 25.4 mm bore.', 'Raimondi 360mm Economy Blade, SA 80 SMS Zoe | ETS Perth'),
 ('RAI-DBSET250SP', 'Raimondi Multilayer Slotted Rim Porcelain Blade 250mm - suits Pikus', 'Raimondi Pikus Advanced 85, 105 and 130 (230 to 250 mm blades) and other 250 mm wet saws with a 25.4 mm bore. Too small for the Zoe, SMS and SA 80.', 'Raimondi 250mm Slotted Porcelain Blade, Pikus | ETS Perth'),
 ('RAI-DBSET250BE', 'Raimondi Segmented Diamond Blade 250mm Porcelain Economy - suits Pikus', 'Raimondi Pikus Advanced 85, 105 and 130 (230 to 250 mm blades) and other 250 mm wet saws with a 25.4 mm bore. Too small for the Zoe, SMS and SA 80.', 'Raimondi 250mm Economy Porcelain Blade, Pikus | ETS Perth'),
 ('RAI-DBCC200', 'Raimondi Diamond Blade 200mm Continuous Rim - suits Exploit & 200mm saws', 'Raimondi Exploit and other 200 mm bridge saws with a 25.4 mm bore. Too small for the Zoe, Pikus, SMS and SA 80.', 'Raimondi 200mm Continuous Rim Blade, Exploit | ETS Perth'),
 ('RAI-DBCC200E', 'Raimondi Diamond Blade 200mm Economy Continuous Rim - suits 200mm saws', 'Raimondi Exploit and other 200 mm bridge saws with a 25.4 mm bore. Too small for the Zoe, Pikus, SMS and SA 80.', 'Raimondi 200mm Economy Blade for 200mm saws | ETS Perth'),
]
for sku, title, fits, seo_t in BL:
    pid = by_sku[sku]
    old_seo = by_id[pid]['seo']['description'] or ''
    add(sku, title, f'<p><strong>Fits:</strong> {fits}</p>', seo_t, old_seo[:155], keep_head=True)

json.dump(U, open('updates.json', 'w'), indent=1)
print(len(U), 'products to rewrite')
for pid, u in U.items():
    print('\n##', pid, '|', u['title'], '\n  SEO:', u['seo'])
    print('  ', re.sub(r'<[^>]+>', ' ', u['descriptionHtml'])[:260].replace('\n', ' '), '...')
