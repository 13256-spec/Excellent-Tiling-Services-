"""Estimate shipping weight and packed box size for every Shopify variant.

Input:  P.json - products (id, title, productType, vendor, status, description)
        with a `vs` list of variants (id, sku, title, price, inventoryItem.id),
        exported from Shopify with a bulk query.
Output: product-weights.csv next to this script.

None of our suppliers (Roberts Designs, MELA/Bathroom City, Eternity Tiles)
publish shipping weights, so weights are estimates. The size comes from the
product description or title where it is given; the weight then follows from
the material. `basis` says which one was used.

Shipping method follows Australia Post MyPost Business parcel limits:
22 kg, 105 cm longest side, 0.25 m3. Anything over goes by freight.
"""
import csv
import json
import os
import re
import sys

AUSPOST_MAX_KG = 22
AUSPOST_MAX_CM = 105
AUSPOST_MAX_M3 = 0.25


def num(pattern, text, default=None, cast=float):
    m = re.search(pattern, text, re.I)
    return cast(m.group(1)) if m else default


def desc_dims_mm(desc):
    """First 'A x B x C' size in the description, in mm."""
    m = re.search(r'(\d{2,4})\s*(?:mm)?\s*\(?[A-Z]?\)?\s*[x×]\s*(\d{2,4})\s*(?:mm)?\s*\(?[A-Z]?\)?\s*[x×]\s*(\d{2,4})', desc)
    return tuple(int(x) for x in m.groups()) if m else None


def box_from_mm(dims, pad_cm=8):
    return tuple(round(d / 10 + pad_cm) for d in sorted(dims, reverse=True))


def estimate(p, v):
    t = p['title']
    tl = t.lower()
    vt = v['title'] if v['title'] not in ('Default Title', 'Default') else ''
    vl = vt.lower()
    typ = p['productType']
    desc = re.sub(r'\s+', ' ', p.get('description') or '')
    full = f'{tl} {vl}'

    def r(kg, box, basis='type estimate', note=''):
        return round(kg, 2), tuple(int(round(b)) for b in box), basis, note

    # ---------- tiles: one variant = 1 m2 ----------
    if typ == 'Tile':
        size = re.search(r'(\d{3,4})x(\d{3,4})', vl)
        a, b = (int(size.group(1)), int(size.group(2))) if size else (600, 600)
        return r(22.0, (b / 10 + 4, a / 10 + 4, 6), 'tile size + 9.5mm porcelain (~22 kg/m2)',
                 'per m2; orders are several m2, so freight')

    # ---------- MELA bathroom ware ----------
    if 'vanity' in tl:
        w = num(r'\b(450|600|750|900|1050|1200|1500|1800)\b', tl, 750)
        kg = 10 + w * 0.05
        return r(kg, (w / 10 + 8, 55, 70), 'vanity width from title',
                 'cabinet + 20mm stone top + basin')
    if 'tallboy' in tl:
        return r(32, (168, 48, 48))
    if 'bath' in tl and typ in ('Freestanding Bath', 'Back to Wall Bath', 'Corner Bath', 'Inset Bath'):
        length = num(r'(\d{4})', vl or tl, 1500)
        kg = 30 + (length - 1300) * 0.02 + (8 if 'free standing' in tl or typ == 'Freestanding Bath' else 0)
        return r(kg, (length / 10 + 10, 85, 65), 'bath length from variant', 'acrylic')
    if 'toilet' in tl and typ in ('Toilet Suite', 'In Wall Cistern Toilet'):
        d = desc_dims_mm(desc)
        box = box_from_mm(d, 10) if d else (90, 50, 70)
        return r(38 if typ == 'Toilet Suite' else 32, box,
                 'description dimensions' if d else 'type estimate', 'vitreous china, usually 2 boxes')
    if typ in ('Corner Shower Screen', 'Frameless Shower Panel'):
        sizes = [int(x) for x in re.findall(r'(\d{3,4})', vt)]
        area = sum(s for s in sizes if s < 2000) / 1000 * 2.0 if sizes else 1.8
        return r(area * 25 + 3, (210, max(sizes or [900]) / 10 + 10, 12), 'glass size from variant',
                 '10mm toughened glass')
    if 'u channel 2000' in tl:
        return r(2.5, (205, 8, 6), 'title length')
    if typ in ('Above Counter Basin', 'Half Inset Basin', 'Inset Basin', 'Semi Basin', 'Undermount Basin'):
        d = desc_dims_mm(desc)
        box = box_from_mm(d, 12) if d else (60, 48, 30)
        kg = 9 if not d else min(11, max(6, d[0] * d[1] / 1e6 * 55))
        return r(kg, box, 'description dimensions' if d else 'type estimate', 'ceramic - fragile')
    if typ == 'Kitchen Sink':
        w = num(r'triton (\d{3,4})', tl)
        litres = num(r'(\d{2})l\b', tl)
        if litres:
            w = 550 if litres >= 45 else 450
        w = w or 600
        kg = 4 + w * 0.009
        return r(kg, (w / 10 + 8, 55, 30), 'sink width from title', 'stainless steel')
    if typ == 'Mirror Cabinet':
        w = num(r'(\d{3,4})mm', vl) or num(r'\b(450|600|750|800|900|1200)\b', tl, 600)
        kg = 8 + w * 0.02
        return r(kg, (max(w / 10 + 10, 85), 20, 80 if w < 800 else w / 10 + 10), 'width from title/variant',
                 'glass - fragile')
    if typ in ('Mirror', 'LED Mirror'):
        w = num(r'(\d{3,4})mm', vl) or num(r'\b(450|600|700|800|900|1200)\b', tl, 600)
        h = 900 if w <= 600 and ('arch' in tl or 'oval' in tl) else (w if 'round' in tl else 800)
        if 'vina' in tl:
            h = 800
        area = w * h / 1e6 * (0.8 if ('round' in tl or 'oval' in tl or 'arch' in tl) else 1)
        kg = area * 13 + (2.5 if typ == 'LED Mirror' else 0) + (1.5 if 'framed' in tl else 0) + 1.5
        return r(kg, (max(w, h) / 10 + 10, min(w, h) / 10 + 10, 10), 'width from title/variant', 'glass - fragile')

    # ---------- tapware and accessories ----------
    if typ in ('Basin Mixer',):
        return r(2.0 if 'tall' in tl or 'high' in tl else 1.4, (30, 20, 10))
    if typ in ('Wall Mixer', 'Wall Mixer with Diverter'):
        return r(1.4, (22, 18, 12))
    if typ in ('Wall Spout', 'Bath Spout'):
        return r(1.1, (32, 15, 10))
    if typ == 'Kitchen Sink Mixer':
        return r(3.0 if 'pull' in tl else 2.4, (45, 25, 12))
    if typ == 'Freestanding Bath Mixer':
        return r(9.0, (105, 25, 20), 'type estimate', 'floor-standing, ~1m tall')
    if typ == 'Freestanding Bath Spout':
        return r(6.0, (100, 25, 20), 'type estimate', 'floor-standing')
    if typ == 'Combination Shower Set':
        return r(4.5 if 'without rail' not in tl else 3.0, (100 if 'without rail' not in tl else 60, 35, 15))
    if typ in ('Hand Shower Set',):
        return r(1.8 if 'without rail' in tl else 3.0, (40 if 'without rail' in tl else 100, 20, 12))
    if typ in ('Shower Head',):
        return r(1.2, (32, 32, 10))
    if typ == 'Hand Shower':
        return r(0.5, (30, 12, 8))
    if typ in ('Shower Arm', 'Ceiling Shower Arm'):
        return r(1.2, (45, 12, 10))
    if typ == 'Shower Hose':
        return r(0.4, (25, 20, 6))
    if typ == 'Towel Rail':
        w = num(r'\b(600|800|900)\b', tl, 600)
        return r(1.4 + w / 1000 * (2.2 if 'double' in tl else 1.2), (w / 10 + 10, 15, 10), 'rail width from title')
    if typ == 'Hand Towel Rail':
        return r(0.7, (30, 12, 10))
    if typ == 'Bath Towel Shelf':
        return r(2.2, (68, 28, 12), 'description dimensions')
    if typ in ('Bathroom Hook',):
        return r(0.25, (12, 10, 8))
    if typ in ('Toilet Roll Holder',):
        return r(0.5, (20, 15, 10))
    if typ in ('Soap Holder', 'Shelf Holder'):
        return r(0.7, (25, 15, 10))
    if typ == 'Toilet Brush Holder':
        return r(1.2, (45, 15, 15))
    if typ in ('Pop Up Waste', 'Bath Waste'):
        return r(0.5 if 'bath' in tl else 0.35, (20, 12, 10))
    if typ == 'Shower Screen Fitting':
        return r(0.6, (20, 15, 8))

    # ---------- Roberts / trade ----------
    if 'baron f200' in tl:
        return r(180, (110, 85, 125), 'supplier spec (180 kg empty)')
    if 'baron f300' in tl:
        return r(200, (145, 105, 130), 'supplier spec (180 kg+)')
    if 'mixer head' in tl:
        return r(25 if 'e120' in tl else 30, (70, 50, 50))
    if 'paddles set' in tl:
        return r(10, (60, 40, 20))
    if 'baron e120' in tl and 'mixer' in tl:
        return r(85, (100, 70, 110))
    if 'main switch' in tl:
        return r(1.5, (25, 20, 15))
    if 'rubber wheel' in tl:
        return r(3.0, (35, 35, 12))
    if 'power cable' in tl:
        return r(1.0, (30, 25, 8))
    if 'electric glue mixer' in tl:
        return r(6.0, (70, 30, 20))
    if 'spiral head' in tl or ('mixer' in tl and 'shaft' in tl):
        return r(1.3, (65, 16, 16))

    if typ == 'Tile Cutters' or 'sigma' in tl or 'kera' in tl:
        if any(k in tl for k in (' nut ', 'bolt', 'wheel', 'rubber foot')) or tl.endswith(' nut'):
            return r(0.1, (12, 10, 4), 'type estimate', 'small spare part')
        if 'suction cup' in tl:
            return r(1.5, (25, 25, 15))
        if 'kera cut kit' in tl:
            return r(45, (345, 25, 20), 'title length 332cm')
        if 'kera lift' in tl:
            return r(60, (180, 60, 40), 'title size 340 x 160cm', 'ships as a kit')
        if 'workbench art 63e' in tl:
            return r(40, (190, 105, 20), 'title size 180 x 100cm')
        if 'table with legs' in tl:
            return r(60, (200, 80, 25))
        cm = num(r'(\d{2,3})\s*cm', tl)
        if cm and ('cutter' in tl):
            return r(3 + cm * 0.15, (cm + 18, 30, 16), 'cutter length from title')
        if 'measurement bar' in tl:
            return r(2.0, (70 if '90n' in tl else 60, 15, 8), 'type estimate', 'length not published')
        if 'extension bar' in tl:
            return r(1.5, (58, 12, 8))
        if 'support arm' in tl:
            return r(1.8, (50, 20, 10))
        if 'jolly edge' in tl:
            return r(4.5, (45, 30, 20))
        if 'laser' in tl or 'carriage kit' in tl or 'fixing kit' in tl or 'clamps' in tl or 'hooks' in tl:
            return r(1.5, (35, 25, 12))
        if 'magnetic map' in tl:
            return r(1.0, (60, 30, 3))
        if 'suction cup' in tl:
            return r(1.5, (25, 25, 15))
        if 'handle' in tl or 'square' in tl:
            return r(0.9, (35, 20, 8))
        return r(0.1, (12, 10, 4), 'type estimate', 'small spare part')

    if 'grout' in tl and typ == 'Grout':
        kg = num(r'(\d+)\s*kg', tl, 5)
        box = {2: (22, 15, 12), 5: (30, 22, 20), 10: (40, 30, 25)}.get(int(kg), (40, 30, 25))
        return r(kg + 0.3, box, 'pack size from title')
    if 'eco synsafe acid' in tl or 'liquid additive' in tl:
        l = num(r'(\d+)\s*l\b', vl or tl, 5)
        return r(l * 1.1 + 0.3, (20 + l, 20 + l / 2, 25 + l / 2), 'volume from title/variant', 'liquid')
    if typ in ('Silicone Sealants', 'Hybrid Sealants', 'Adhesives') or 'maxisil 100% pure silicone' in tl:
        return r(0.85 if '600ml' in desc.lower() or 'sausage' in tl else 0.45, (30, 8, 8))
    if 'bucket' in tl and 'litre' in tl:
        return r(1.3, (35, 35, 40))
    if 'backer rod' in tl:
        return r(2.5, (55, 55, 30 if '20mm' in tl else 20), 'type estimate', 'light but bulky reel')
    if typ == 'Silicone Accessories' or 'smoothtex' in tl or 'primer' in tl:
        l = num(r'(\d+)\s*litre', vl or tl)
        ml = num(r'(\d+)\s*ml', vl or tl)
        if l:
            return r(l * 1.05 + 0.3, (25 if l >= 5 else 15, 20 if l >= 5 else 10, 30 if l >= 5 else 25), 'volume from variant', 'liquid')
        if ml:
            return r(ml / 1000 + 0.1, (20, 8, 8), 'volume from title', 'liquid')
        return r(0.2, (20, 10, 5))

    if 'niche box' in tl:
        d = [int(x) for x in re.findall(r'(\d{3})', tl)[:2]]
        qty = num(r'^(\d+)$', vt, 1, int)
        return r(3.5 * qty, (d[0] / 10 + 5, d[1] / 10 + 5, 10 * qty + 2), 'size from title', f'{qty} per pack')
    if 'linear drain' in tl:
        mm = num(r'(\d{3,4})mm', vt, 900)
        return r(1.5 + mm / 1000 * 2.5, (mm / 10 + 8, 15, 10), 'length from variant')
    if 'floor waste' in tl:
        return r(1.2 if '100mm' in tl else 0.9, (20, 20, 12))
    if 'flange' in tl:
        return r(0.4, (20, 20, 10))

    # trims: 3m / 2.5m / 1m lengths, corners and joiners
    if 'length' in tl and ('trim' in tl or 'stair' in tl):
        length_m = num(r'(\d(?:\.\d)?)\s*m\s*lengths?', tl) or num(r'x\s*(\d(?:\.\d)?)m\b', tl, 3)
        size = num(r'(\d{1,2})\s*mm', vl or tl, 10)
        per_m = 0.12 + size * 0.012
        if 'brass' in tl:
            per_m *= 3.2
        elif 's/steel' in tl or 'stainless' in tl:
            per_m *= 2.6
        elif 'pvc' in tl:
            per_m *= 0.6
        elif 'stair' in tl:
            per_m = 0.9
        return r(per_m * length_m + 0.1, (length_m * 100 + 5, 8, 6), 'length from title, profile size from variant')
    if 'stair trim' in tl:
        return r(2.4, (255, 10, 6), 'title size 2.5m')
    if any(k in tl for k in ('corner', 'joiner')) and typ not in ('Mirror',):
        return r(0.1, (12, 10, 6))

    if typ == 'Diamond Blades' or 'diamond blade' in tl:
        mm = num(r'(\d{3})mm', vl or tl, 125)
        return r(0.15 + (mm / 100) ** 2 * 0.08, (mm / 10 + 4, mm / 10 + 4, 3), 'blade diameter')
    if typ in ('Drill Bits', 'Core Drills') or 'drill' in tl:
        mm = num(r'(\d{1,2})mm', vl or tl, 10)
        return r(0.1 + mm * 0.006, (18, 8, 6))
    if typ == 'Grinding Wheels and Polishing Pads' or 'abrasive' in tl or 'hand pads' in tl:
        return r(0.4 if '10 pack' in tl else 0.15, (15, 15, 6))

    if typ in ('Tile Spacers', 'Tile Leveling Systems', 'Tile Wedges') or 'spacer' in tl or 'wedges' in tl:
        count = num(r'([\d,]+)\s*(?:bag|bucket|pack)', vl or tl, None, lambda s: int(s.replace(',', '')))
        if not count:
            count = num(r'([\d,]+)\s*pack', tl, 100, lambda s: int(s.replace(',', '')))
        each = 0.0004 if ('spacer' in tl and 'plate' not in tl) else (0.003 if 'wedge' in tl else (0.004 if 'plate' in tl else 0.008))
        if 'x spacer – 10mm' in tl:
            each, count = 0.01, 100
        kg = count * each + (0.4 if 'bucket' in vl else 0.05)
        box = (30, 25, 25) if kg > 3 or 'bucket' in vl else (25, 18, 8)
        return r(max(kg, 0.1), box, 'pack count from variant')

    if 'trowel' in tl or 'spreader' in tl or 'float' in tl:
        return r(0.25 if 'plastic' in tl else (0.9 if 'large' in tl else 0.6), (35, 15, 8))
    if 'scraper' in tl:
        if 'floor scraper' in tl:
            return r(2.5 if '300' in vl else 2.0, (125, 32 if '300' in vl else 18, 10), 'type estimate', 'long handle')
        return r(0.3, (28, 12, 5))
    if 'extension pole' in tl:
        return r(1.2, (125, 8, 8), 'description size 1.2-2.4m')
    if 'roller and tray' in tl:
        return r(0.8, (40, 35, 10))
    if 'eco roller wash up bucket' in tl:
        return r(5.5, (65, 40, 40), 'type estimate', 'bulky')
    if typ == 'Sponges and Grouting Systems' or 'sponge' in tl or 'pad' in tl and 'knee' not in tl:
        return r(1.2 if 'kit' in tl else 0.25, (30, 20, 12))
    if typ == 'Brushes and Rollers' or 'roller' in tl or 'brush' in tl:
        return r(0.9 if 'waterproofing kit' in tl else 0.3, (30, 15, 10))
    if 'caulking gun' in tl or 'cylinder gun' in tl:
        return r(1.4 if 'cylinder' in tl else (0.9 if 'sausage' in tl or '600' in tl else 0.6), (45 if 'sausage' in tl or 'cylinder' in tl else 35, 18, 8))
    if 'suction cup' in tl:
        return r(1.5 if '50kg' in tl else 1.0, (25, 15, 15))
    if 'knee pad' in tl or 'liners' in tl:
        return r(0.8 if 'pad' in tl else 0.3, (30, 25, 15))
    if 'gloves' in tl:
        return r(0.8, (25, 13, 9), 'type estimate', 'box of 100')
    if 'mallet' in tl or 'nipper' in tl or 'rake' in tl or 'tape measure' in tl or 'chalk' in tl:
        return r(0.7 if 'mallet' in tl else 0.35, (30, 12, 8))
    if 'pallet wrap roll' in tl:
        return r(3.0, (52, 12, 12))
    if 'pallet wrap dispenser' in tl:
        return r(1.5, (55, 15, 15))
    if 'tape' in tl:
        return r(0.3, (12, 12, 6))
    if 'surface protection' in tl:
        return r(7.0, (98, 16, 16), 'size from description (915mm roll)')
    if 'powerblock' in tl:
        return r(2.5, (35, 25, 15))
    if 'knife' in tl:
        return r(0.25, (18, 10, 4))
    if typ == 'Designer Bathroom Accessories':
        return r(0.8, (25, 20, 12))
    if typ == 'Ceramic and Modern Bathroom Fixtures' or 'soapholder' in tl or 'shelf' in tl:
        return r(1.2 if 'shelf' in tl else 0.8, (35, 20, 12), 'type estimate', 'ceramic - fragile')
    if 'vent' in tl:
        return r(0.4, (25, 25, 8))
    return r(1.0, (30, 20, 15), 'default', 'check')


def method(kg, box, typ=''):
    if typ == 'Tile':
        return 'freight'
    vol = box[0] * box[1] * box[2] / 1e6
    if kg <= AUSPOST_MAX_KG and max(box) <= AUSPOST_MAX_CM and vol <= AUSPOST_MAX_M3:
        return 'auspost'
    return 'freight'


def main(src, out):
    P = json.load(open(src))
    rows = []
    for p in sorted(P.values(), key=lambda p: (p['productType'], p['title'])):
        for v in p.get('vs', []):
            kg, box, basis, note = estimate(p, v)
            cubic = box[0] * box[1] * box[2] / 4000
            rows.append({
                'product': p['title'],
                'variant': '' if v['title'] in ('Default Title', 'Default') else v['title'],
                'sku': v['sku'] or '',
                'vendor': p['vendor'],
                'type': p['productType'],
                'status': p['status'].lower(),
                'price': v['price'],
                'weight_kg': f'{kg:.2f}',
                'box_cm': 'x'.join(str(b) for b in box),
                'cubic_kg': f'{cubic:.1f}',
                'ship_by': method(kg, box, p['productType']),
                'basis': basis,
                'note': note,
                'variant_id': v['id'],
                'inventory_item_id': v['inventoryItem']['id'],
            })
    with open(out, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    return rows


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    main(sys.argv[1], os.path.join(here, 'product-weights.csv'))
