"""Shipping record for every Roberts Designs variant (6 Oct 2026).

Roberts Designs publishes no weights or carton sizes (weight and dimension
fields on robertsdesigns.com.au are blank for every product), so every number
here is an estimate. Weights and boxes come from product-weights.csv, with the
corrections below applied first (to that file too).

Output: roberts-shipping-2026-10-06.csv next to this script.

Shipping columns:
- chargeable_kg: the higher of the real weight and the Australia Post cubic weight
  (L x W x H / 4000). This is what a carrier bills.
- ship_method:
    parcel  - fits Australia Post (22 kg, 105 cm longest side, 0.25 m3)
    long    - light but over 105 cm (3 m trims, long cutters): needs a courier that
              takes long parcels, or Perth delivery / pickup
    freight - too heavy or big for a parcel: freight quote, or Perth delivery / pickup
- est_ship_au: the owner's Australia-wide small-item prices (5 Oct 2026) applied to
  chargeable_kg, for one item on its own.
- international: small parcels only (chargeable up to 10 kg), not dangerous goods.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WEIGHTS = os.path.join(HERE, 'product-weights.csv')
OUT = os.path.join(HERE, 'roberts-shipping-2026-10-06.csv')

# sku: (weight_kg, box_cm, basis, note)
CORRECTIONS = {
    # Two socket bits, not a carton of 50 (Roberts "Box Qty: 50" is the carton).
    'SOC102': (0.15, '12x10x6', 'pack of 2 bits', ''),
    # Closed-cell PE foam rod. Roberts lists "Length: 250m, 1 roll" for $4.65, which
    # is either a per-metre price or a pricing error: check with Roberts before selling.
    'RDX2303': (0.6, '40x40x20', 'foam rod 10mm x 250m roll', 'check unit with Roberts: per metre or per 250 m roll'),
    'RDX2300': (0.3, '35x35x15', 'foam rod 6mm x 250m roll', 'check unit with Roberts: per metre or per 250 m roll'),
    # One 2.15 m length of open-cell foam, coiled to fit a parcel.
    'RDX2304': (0.15, '30x30x10', 'one 2.15m length, coiled', 'flexible foam, coil to post'),
}

# Product-by-product review against the Roberts product pages (6 Oct 2026, second pass).
# Packed sizes follow the item's own size where Roberts gives it; weight is unchanged
# unless noted. Each rule: (product contains, variant contains or None, kg or None, box).
SPACER_BAGS = {  # pack: (kg or None to keep, box)
    '100 bag': (None, '15x10x3'), '250 bag': (None, '15x10x4'), '500 bag': (None, '20x15x5'),
    '1,000 bag': (None, '25x18x6'), '2,000 bag': (None, '25x20x8'), '5,000 bag': (None, '30x25x10'),
    '10,000 bag': (None, '35x30x15'), '2,000 bucket': (None, '20x20x20'), '3,000 bucket': (None, '22x22x22'),
    '5,000 bucket': (None, '25x25x25'), '10,000 bucket': (None, '30x30x30'), 'Bulk pack': (None, '30x25x10'),
}
WEDGE_BAGS = {'100 bag': '20x15x6', '500 bag': '30x20x10', '1,000 bag': '35x25x15', '2,000 bag': '40x30x20'}
REVIEW = [
    # ceramic shelves / soap holders: box follows the 200x100 / 300x100 / 400x100 / 150 sq size
    ('Ultimate Shelf', None, None, '45x15x10'),
    ('Standard Shelf', None, None, '35x15x10'),
    ('Square Shelf', None, None, '35x15x10'),
    ('Combination Shelf and Soapholder', None, None, '25x15x10'),
    ('Regent Shelf and Soapholder', None, None, '25x15x10'),
    ('Standard Soapholder (Rectangle)', None, None, '25x15x10'),
    ('Standard Soapholder (Square)', None, None, '20x20x10'),
    ('Vents', None, 0.5, '25x15x8'),
    # brushes, rollers, kits
    ('Waterproofing Kit', None, 1.2, '40x35x12'),
    ('3 x Spare Rollers for RDXT232', None, None, '26x15x8'),
    ('3 piece Spare Roller', None, 0.2, '20x12x8'),
    ('Paint Roller Handle – 75mm', None, 0.2, '30x10x5'),
    ('Paint Roller Handle – 230mm', None, None, '40x26x6'),
    # trims: brass trims in step with profile size; 1 m trims fit 104 cm
    ('L Shape Brass Trim', '18.5mm', 3.38, '305x8x6'),
    ('L Shape Brass Trim', '22.5mm', 3.85, '305x8x6'),
    ('L Shape Aluminium Trim – 1m', None, None, '104x6x6'),
    ('Aluminium Stair Trim with Solid Black Carborundum', None, 3.0, '255x10x6'),
    # Baron spares
    ('Main switch', None, 0.5, '20x15x10'),
    # sponges and Siri pads: box follows the stated sponge / pad size
    ('Grout Haze Square Edge Sponge', None, 0.1, '18x13x6'),
    ('Hydra Tilers Round Edge Sponge', None, 0.12, '21x15x6'),
    ('Hydra Tilers Square Edge Sponge', None, 0.12, '21x15x6'),
    ('Hydra Tilers Slater Sponge', None, 0.2, '33x23x5'),
    ('Epoxy Grouting Pad', None, 0.1, '27x12x4'),
    ('Siri Brown Sponge', None, 0.1, '27x12x4'),
    ('Siri Green Clean Up Pad', None, 0.1, '27x12x4'),
    ('Siri White Rinse Pad', None, 0.1, '27x12x4'),
    ('Siri White Velcro Base Plate', None, 0.1, '27x12x3'),
    ('Siri Yellow Sponge', None, 0.12, '29x15x4'),
    ('Siri Interchangeable Blue Handle', None, 0.2, '27x12x8'),
    ('Siri Epoxy Grouting Kit', None, 0.5, '30x15x10'),
    ('Replacement Clip for Eco Roller', None, 0.05, '12x10x4'),
    ('Replacement Plastic Grid for Eco Roller', None, 0.4, '35x25x3'),
    ('Replacement Bucket Handle for Eco Roller', None, 0.15, '40x10x3'),
    ('Replacement Roller for Eco Roller', None, 0.4, '35x10x10'),
    # suction cups: box follows the cup diameter
    ('Aluminium Single Suction Cup', None, 0.6, '20x12x10'),
    ('SIRI Suction Cup', None, 0.8, '22x13x10'),
    ('Kera Flex Aluminium Suction Cup ART51C', None, 1.0, '18x16x12'),
    ('Kera Flex Aluminium Suction Cup ART51P4', None, 1.2, '20x18x12'),
    ('Pro Grip Suction Cup', None, 1.2, '22x20x12'),
    # Sigma parts
    ('Handle', None, 0.6, '35x12x8'),  # Sigma 24-series handles (only Sigma products match below)
    ('Laser for 4 series', None, 0.5, '20x15x10'),
    ('Locking Bolt', None, 0.1, '12x10x4'),
    ('Swivel Measurement Bar', None, 1.5, None),
    # small tools
    ('Barwalt KN-1 Replacement Liners', None, 0.2, '25x20x8'),
    ('Blue Chalk Refill Bottle', None, 0.3, '20x8x6'),
    ('Chalk Line Reel', None, 0.3, '15x10x6'),
    ('Tape Measure', None, 0.35, '12x12x6'),
    ('Splash Trowel', None, 0.4, '30x12x8'),
]


def review_fix(r):
    p, v = r['product'], r['variant']
    if p.startswith('Tile Wedges'):
        for pack, box in WEDGE_BAGS.items():
            if v == pack:
                return None, box
    if r['type'] == 'Tile Spacers' and v in SPACER_BAGS:
        return SPACER_BAGS[v]
    for name, var, kg, box in REVIEW:
        if name == 'Handle' and not p.startswith('Sigma'):
            continue
        if name in p and (var is None or var in v):
            return kg, box
    return None


# Variants deleted from Shopify (found 6 Oct 2026 when writing box sizes); dropped from both CSVs.
DELETED = {
    'gid://shopify/ProductVariant/43993432883263',
    'gid://shopify/ProductVariant/43993432850495',
    'gid://shopify/ProductVariant/43993438060607',
    'gid://shopify/ProductVariant/43993452052543',
    'gid://shopify/ProductVariant/43993440911423',
    'gid://shopify/ProductVariant/43993440878655',
    'gid://shopify/ProductVariant/43993440845887',
    'gid://shopify/ProductVariant/43993438093375',
    'gid://shopify/ProductVariant/43993438027839',
    'gid://shopify/ProductVariant/43993437995071',
    'gid://shopify/ProductVariant/43993437962303',
    'gid://shopify/ProductVariant/43993436487743',
}

DANGEROUS = ('Primer 1215', 'Primer 1216', 'Primer 1217', 'Primer 1218')

AU_BANDS = [(1, 15), (3, 20), (5, 29), (10, 39), (22, 59), (44, 109), (100, 179)]


def au_price(kg):
    for top, price in AU_BANDS:
        if kg <= top:
            return price
    return None


def is_roberts(r):
    return r['vendor'].startswith('Roberts') or r['sku'].upper().startswith(('RD', 'SOC'))


def main():
    with open(WEIGHTS, newline='') as f:
        rows = [r for r in csv.DictReader(f) if r['variant_id'] not in DELETED]
        fields = list(rows[0].keys())

    for r in rows:
        c = CORRECTIONS.get(r['sku'])
        if not c:
            continue
        w, box, basis, note = c
        l, wd, h = (int(x) for x in box.split('x'))
        r['weight_kg'] = f'{w:.2f}'
        r['box_cm'] = box
        r['cubic_kg'] = f'{l * wd * h / 4000:.1f}'
        r['ship_by'] = 'auspost'
        r['basis'] = basis
        r['note'] = note
        r['in_shopify'] = 'yes'  # written to Shopify 6 Oct 2026

    for r in rows:
        if not is_roberts(r):
            continue
        fix = review_fix(r)
        if not fix:
            continue
        kg, box = fix
        if box:
            r['box_cm'] = box
        l, wd, h = (int(x) for x in r['box_cm'].split('x'))
        r['cubic_kg'] = f'{l * wd * h / 4000:.1f}'
        if kg is not None and abs(float(r['weight_kg']) - kg) > 0.001:
            r['weight_kg'] = f'{kg:.2f}'
            r['in_shopify'] = 'yes'  # written to Shopify 6 Oct 2026
        r['basis'] = 'product review 6 Oct (size from Roberts page)'

    with open(WEIGHTS, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    out = []
    for r in rows:
        if not is_roberts(r):
            continue
        kg = float(r['weight_kg'])
        dims = sorted((int(x) for x in r['box_cm'].split('x')), reverse=True)
        cubic = dims[0] * dims[1] * dims[2] / 4000
        m3 = dims[0] * dims[1] * dims[2] / 1e6
        charge = max(kg, cubic)
        if kg <= 22 and dims[0] <= 105 and m3 <= 0.25:
            method = 'parcel'
        elif kg <= 25 and dims[0] > 105 and dims[1] <= 40:
            method = 'long'
        else:
            method = 'freight'
        dg = any(d in r['product'] for d in DANGEROUS)
        price = au_price(charge) if method == 'parcel' else None
        out.append({
            'product': r['product'], 'variant': r['variant'], 'sku': r['sku'], 'type': r['type'],
            'price': r['price'], 'weight_kg': f'{kg:.2f}', 'box_cm': 'x'.join(map(str, dims)),
            'cubic_kg': f'{cubic:.1f}', 'chargeable_kg': f'{charge:.1f}', 'ship_method': method,
            'est_ship_au': f'${price}' if price else ('courier quote / Perth delivery or pickup' if method == 'long'
                                                    else 'freight quote / Perth delivery or pickup'),
            'international': 'yes' if method == 'parcel' and charge <= 10 and not dg else 'no',
            'dangerous_goods': 'yes (road only, no air or overseas)' if dg else '',
            'basis': r['basis'], 'note': r['note'], 'variant_id': r['variant_id'],
            'inventory_item_id': r['inventory_item_id'],
        })
    out.sort(key=lambda o: (o['type'], o['product'], o['variant']))
    with open(OUT, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print(f'{len(out)} Roberts variants -> {os.path.basename(OUT)}')


if __name__ == '__main__':
    main()
