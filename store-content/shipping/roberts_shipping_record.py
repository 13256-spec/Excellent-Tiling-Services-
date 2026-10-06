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

DANGEROUS = ('Primer 1215', 'Primer 1216', 'Primer 1217', 'Primer 1218')

AU_BANDS = [(1, 15), (3, 20), (5, 29), (10, 39), (22, 59), (44, 109), (100, 179)]


def au_price(kg):
    for top, price in AU_BANDS:
        if kg <= top:
            return price
    return None


def is_roberts(r):
    return r['vendor'] == 'Roberts Designs' or r['sku'].upper().startswith(('RD', 'SOC'))


def main():
    with open(WEIGHTS, newline='') as f:
        rows = list(csv.DictReader(f))
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
