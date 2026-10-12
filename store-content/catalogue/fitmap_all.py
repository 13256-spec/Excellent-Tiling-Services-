"""Store-wide "what fits what" map (12 Oct 2026).

Reads a Shopify product export (products.json: one object per product with id, title, vendor, productType,
descriptionHtml, variants[{sku}], fitsWith/fitsModels metafields) and produces:
  * payload.json  - per product: the three ets.* metafields (fits_with, fits_models, fits_role) and any
                    title / description / product type change, ready for productUpdate
  * compatibility-all.csv - the map for the repo

Baseline: the Raimondi map already live in ets.fits_with / ets.fits_models (store-content/raimondi/fitmap.py).
Sources for the rest: the BAT Trims Tools Catalogue ONE to SIX (store-content/catalogue/bat-tools-catalogue.csv),
the Sigma parts diagrams in it (pages 18 to 23), and the store's own pages for Siri, Baron, Maxisil, Panther.

Roles: parent = a machine or tool that takes the listed products; item = an accessory, blade, sponge or part.
Usage: python3 -I fitmap_all.py <products.json> <out dir>
"""
import csv, json, re, sys

src, out = sys.argv[1], sys.argv[2]
P = json.load(open(src))
by_sku, by_id = {}, {}
for p in P:
    by_id[p['id']] = p
    for v in p['variants']:
        if v['sku']:
            by_sku.setdefault(v['sku'].strip(), p)


def pid(sku):
    if sku not in by_sku:
        raise KeyError(sku)
    return by_sku[sku]['id']


E = {}  # sku -> entry


def add(sku, role, fits=(), text=None, title=None, type_=None, desc=None, desc_replace=None):
    """fits: SKUs (one per product). desc: how to add the fits line ('prefix' Fits:, 'what' What fits:, None).
    desc_replace: list of (old, new) literal replacements in the description HTML."""
    E[sku] = dict(role=role, fits=(None if fits is None else list(fits)), text=text, title=title, type=type_, desc=desc,
                  desc_replace=desc_replace or [])


M14 = 'M14 thread: BAT Pro 1050 W and 1600 W hand mixers and any other M14 drill mixer'
M14_PADDLES = ['BAT-ST140', 'BAT-EM1050ST', 'BAT-EM1600ST', 'RAI-LSSPSM14', 'RAI-LSSPLM14', 'RAI-LSSPXM14',
               'RAI-LSWSKM14', 'RAI-FLUMIXLSPL']
MIXERS = ['BAT-EM1050P', 'BAT-EM1600P']

# ---------------- mixing ----------------
add('BAT-EM1050P', 'parent', ['BAT-EM1050ST'] + [s for s in M14_PADDLES if s != 'BAT-EM1050ST'] + ['BAT-20LPB', 'RAI-27LB'],
    'Takes M14 thread mixing paddles (its own spare paddle is the 120 x 590 mm BAT-EM1050ST).', desc='what')
add('BAT-EM1600P', 'parent', ['BAT-EM1600ST'] + [s for s in M14_PADDLES if s != 'BAT-EM1600ST'] + ['BAT-20LPB', 'RAI-27LB'],
    'Takes M14 thread mixing paddles (its own spare paddle is the 140 x 590 mm BAT-EM1600ST).', desc='what')
add('BAT-ST140', 'item', MIXERS, M14, title='BAT Liquid Stirrer 140 x 600 x M14mm - suits BAT Pro hand mixers', desc='prefix')
add('BAT-EM1050ST', 'item', MIXERS, 'Spare paddle for the BAT Pro 1050 W mixer; the M14 thread also fits the 1600 W and any other M14 mixer', desc='prefix')
add('BAT-EM1600ST', 'item', MIXERS, 'Spare paddle for the BAT Pro 1600 W mixer; the M14 thread also fits the 1050 W and any other M14 mixer', desc='prefix')
add('LS-SMALL', 'item', [], '10 mm hex shaft for a standard drill chuck (not for M14 mixers)', desc='prefix',
    desc_replace=[('Hand liquid stirrer featuring an 8mm hex shaft and double spiral head of 100mm.',
                   'Hand liquid stirrer with a 10mm hex shaft and a double spiral head of 100, 120 or 150mm.')])
add('RAI-LSWS', 'item', [], '10 mm hex shaft for a standard drill chuck (not for M14 mixers)', desc='prefix')
for s, t in [('RAI-LSSPSM14', 'Raimondi Liquid Stirrer - Small Spiral x M14 - suits BAT Pro & other M14 mixers'),
             ('RAI-LSSPLM14', 'Raimondi Liquid Stirrer - Large Spiral x M14 - suits BAT Pro & other M14 mixers'),
             ('RAI-LSSPXM14', 'Raimondi Liquid Stirrer 160 x 600 x M14 - suits BAT Pro & other M14 mixers'),
             ('RAI-LSWSKM14', 'Raimondi Liquid Stirrer - Whisk Style x M14 - suits BAT Pro & other M14 mixers')]:
    add(s, 'item', MIXERS, M14, title=t, desc='prefix')
add('RAI-FLUMIXLSPL', 'item', ['RAI-FLUMIXSP'] + MIXERS,
    'Raimondi Fluid Mix Special (its standard paddle); M14 thread also fits the BAT Pro and other M14 hand mixers',
    title='Raimondi Liquid Stirrer 140 x 680 x M14 - suits Fluid Mix Special & M14 mixers', desc='prefix')
add('RAI-FLUMIXSP', 'parent', ['RAI-FLUMIXB', 'RAI-FLUMIXLSPL'],
    'Spare 75 L bucket and 3-spiral paddle available. Takes most hand mixers with a 40 to 60 mm neck collar (mixer not included).', desc='what')
add('BAT-20LPB', 'parent', ['BAT-20LPBLID'], 'Snap-on lid sold separately.', desc='what')
add('BAT-20LPBLID', 'item', ['BAT-20LPB'], 'BAT 20 litre bucket', desc='prefix')
add('PAN-20LPB', 'parent', ['PAN-20LPBLID'], 'Orange snap-on lid sold separately.', desc='what')
add('PAN-20LPBLID', 'item', ['PAN-20LPB'], 'Panther 20 litre bucket', desc='prefix')
add('AT-C100-AAI', 'item', [], 'Atika Compact 100 pan mixer', desc='prefix')
add('AT-C140-AAI', 'item', [], 'Atika Compact 140 pan mixer', desc='prefix')
# Baron
add('RDXM50030', 'parent', ['RDXM50443', 'RDXM50421', 'RDXM50340'], 'Spare paddle set (3), mixer head and rubber transport wheel available.', desc='what')
add('RDXM50002', 'parent', ['RDXM50425', 'RDXM50303', 'RDXM50340'], 'Spare mixer head, main switch and rubber transport wheel available.', desc='what')
add('RDXM50003', 'parent', ['RDXM50427', 'RDXM50304'], 'Spare mixer head and main switch available.', desc='what')
add('RDXM50443', 'item', ['RDXM50030'], 'Baron E120 forced action mixer')
add('RDXM50421', 'item', ['RDXM50030'], 'Baron E120 forced action mixer', desc='prefix')
add('RDXM50425', 'item', ['RDXM50002'], 'Baron F200 forced action mixer')
add('RDXM50427', 'item', ['RDXM50003'], 'Baron F300 forced action mixer')
add('RDXM50303', 'item', ['RDXM50002'], 'Baron F200 forced action mixer')
add('RDXM50304', 'item', ['RDXM50003'], 'Baron F300 forced action mixer')
add('RDXM50340', 'item', ['RDXM50002', 'RDXM50030'], 'All Baron forced action mixers except the F300')

# ---------------- grout clean-up ----------------
add('WB-PROFI', 'parent', ['WB-9004', 'WB-9005', 'WB-HANDSP', 'BAT-MAXPG'],
    'Comes with the 23 L bucket, rinsing and base rollers and the adhesive float WB-9004. Spare adhesive sponges (WB-9005) glue on. The BAT Maximo grate also fits this bucket.', desc='what')
add('WB-PROFI-A', 'parent', ['WB-9001', 'WB-9002', 'WB-9003', 'BAT-MAXPG'],
    'Comes with the 23 L bucket, rinsing and base rollers and the Velcro float WB-9001 (handle WB-9002 plus sponge WB-9003). Spare Velcro sponges press on. The BAT Maximo grate also fits this bucket.', desc='what')
add('WB-9001', 'item', ['WB-9002', 'WB-9003', 'WB-PROFI-A'], 'Washboy Profi Velcro system. Spare sponge WB-9003, spare handle WB-9002.', desc='prefix')
add('WB-9002', 'parent', ['WB-9003', 'WB-9001', 'WB-PROFI-A'],
    'Takes the Washboy 145 x 290 mm Velcro sponge WB-9003 (and the 140 x 275 mm epoxy and polyester Velcro sponges). The large 185 x 345 mm sponge WB-9003L needs the large handle WB-9002L.',
    desc='what', desc_replace=[('Compatible with the Washboy large velcro sponge (WB-9003L).',
                                'Takes the Washboy Velcro sponge WB-9003 (145 x 290mm). The large sponge WB-9003L needs the large handle WB-9002L.')])
add('WB-9003', 'item', ['WB-9002', 'WB-9001', 'WB-PROFI-A'], 'Washboy Velcro handle WB-9002 (130 x 265 mm) and the Profi Velcro system',
    title='Washboy Velcro Sponge 145 x 290 x 35mm - suits WB-9002 handle', desc='prefix')
add('WB-9003L', 'item', [], 'Washboy large Velcro handle WB-9002L (160 x 315 mm) only; too big for the standard WB-9002 handle',
    title='Washboy Spare Velcro Sponge 185 x 345 x 35mm - suits WB-9002L large handle', desc='prefix')
add('WB-9004', 'item', ['WB-9005', 'WB-PROFI'], 'Washboy Profi system (adhesive float). Spare sponge WB-9005, glued on with Washboy adhesive.', desc='prefix')
add('WB-9005', 'item', ['WB-9004', 'WB-PROFI'], 'Washboy adhesive float WB-9004 and the Profi system; glued on with Washboy adhesive (WB-9008)',
    title='Washboy Spare Adhesive Sponge 145 x 290 x 35mm - suits WB-9004 float', desc='prefix')
add('WB-HANDSP', 'item', [], None, title='Washboy Hand Sponge 165 x 110 x 65mm',
    desc_replace=[('Hand Sponge 165 x 110 x 60mm.', 'Hand Sponge 165 x 110 x 65mm.')])
add('BAT-MAXIMO-C', 'parent', ['BAT-MAXVHC', 'BAT-MAXVSC', 'BAT-MAXPG', 'BAT-MAXRR3', 'BAT-MAXBR2', 'BAT-MAXBUCK'],
    'Spares: Velcro handle, Velcro sponge, plastic grate, top roller set (3), bottom roller set (2) and the 23 L bucket.', desc='what')
add('BAT-MAXVHC', 'item', ['BAT-MAXIMO-C', 'BAT-MAXVSC'], 'BAT Maximo Commodore grout clean-up system; takes the 150 x 320 mm Velcro sponge BAT-MAXVSC',
    title='BAT Maximo Commodore Velcro Handle 130 x 300mm - suits Maximo system', desc='prefix')
add('BAT-MAXVSC', 'item', ['BAT-MAXIMO-C', 'BAT-MAXVHC'], 'BAT Maximo Commodore Velcro handle BAT-MAXVHC',
    title='BAT Maximo Commodore Velcro Sponge 150 x 320mm - suits Maximo Velcro handle', desc='prefix')
add('BAT-MAXPG', 'item', ['BAT-MAXIMO-C', 'WB-PROFI', 'WB-PROFI-A'], 'BAT Maximo bucket and the Washboy Profi bucket (WB-BUCK)',
    title='BAT Maximo Plastic Grate - suits Maximo & Washboy buckets', desc='prefix')
add('BAT-MAXRR3', 'item', ['BAT-MAXIMO-C'], 'BAT Maximo grout clean-up bucket (top roller set, 3 pieces)',
    title='BAT Maximo Replacement Top Roller Set (3 pcs) - suits Maximo bucket', desc='prefix')
add('BAT-MAXBR2', 'item', ['BAT-MAXIMO-C'], 'BAT Maximo grout clean-up bucket (bottom roller set, 2 pieces)',
    title='BAT Maximo Bottom Bucket Roller Set (2 pcs) - suits Maximo bucket', desc='prefix')
add('BAT-MAXBUCK', 'item', ['BAT-MAXIMO-C'], 'BAT Maximo grout clean-up system (23 L bucket with carry handle)', desc='prefix')
add('PAN-QRFH', 'parent', ['PAN-SMSP2814', 'PAN-LGSP3418'], 'Takes the Panther small (280 x 140 mm) and large (335 x 180 mm) sponges with cuts.', desc='what')
add('PAN-SMSP2814', 'item', ['PAN-QRFH'], 'Panther quick release float handle (PAN-QRFH)', title='Panther GCS Small Sponge with Cuts 280 x 140mm - suits quick release handle', desc='prefix')
add('PAN-LGSP3418', 'item', ['PAN-QRFH'], 'Panther quick release float handle (PAN-QRFH)', title='Panther GCS Large Sponge with Cuts 335 x 180mm - suits quick release handle', desc='prefix')
add('PAN-GCSRRS', 'item', [], 'Panther grout clean-up bucket (top roller set); also fits some other wash buckets', desc='prefix')
# Siri
SIRI_SP = ['RDXT610', 'RDXT611', 'RDXT612a']
add('RDXT630', 'parent', ['RDXT609'] + SIRI_SP + ['RDXT617', 'RDXT618', 'RDXT619', 'RDXT611a', 'RDXT611b', 'RDXT612', 'RDXT611c'],
    'Comes with 2 rollers, the RDXT609 handle and the RDXT610 sponge. Spares: roller, bucket handle, grid, clip, sponges and pads.', desc='what')
add('RDXT609', 'parent', SIRI_SP + ['RDXT617', 'RDXT618', 'RDXT619', 'RDXT630'],
    'Takes the Siri yellow and brown sponges, and the white Velcro base plate for the white rinse pad and green clean-up pad.', desc='what')
for s in SIRI_SP:
    add(s, 'item', ['RDXT609', 'RDXT630'], 'Siri RDXT609 handle (the Eco Roller bucket comes with it)')
add('RDXT617', 'item', ['RDXT609', 'RDXT618', 'RDXT619'], 'Siri RDXT609 handle; holds the white rinse pad and the green clean-up pad')
add('RDXT618', 'item', ['RDXT617', 'RDXT609'], 'Siri white Velcro base plate RDXT617 on the RDXT609 handle', desc='prefix')
add('RDXT619', 'item', ['RDXT617', 'RDXT609'], 'Siri white Velcro base plate RDXT617 on the RDXT609 handle', desc='prefix')
for s in ['RDXT611a', 'RDXT611b']:
    add(s, 'item', ['RDXT630'], 'Siri Eco Roller wash-up bucket RDXT630 and the Baby Roller bucket RDXT608')
for s in ['RDXT612', 'RDXT611c']:
    add(s, 'item', ['RDXT630'], 'Siri Eco Roller wash-up bucket RDXT630')
# Raimondi grout clean-up
SM_SP = ['RAI-SMSPONGE', 'RAI-SMSPONGECUT', 'RAI-SMSPONGECV']
SM_FL = ['RAI-SMFLOAT', 'RAI-SMFLOATCUT']
LG_SP = ['RAI-LGSPONGE', 'RAI-LGSPONGECUT', 'RAI-LGSPONGECV']
LG_FL = ['RAI-LGFLOAT', 'RAI-LGFLOATCUT']
PL_SP = ['RAI-PLSPONGE', 'RAI-PLSPONGECUT', 'RAI-PLSPONGECV']
PL_FL = ['RAI-PLFLOAT', 'RAI-PLFLOATCUT']
add('RAI-SKIPPER', 'parent', ['RAI-SRS2', 'RAI-SPG'] + SM_FL + SM_SP + ['RAI-QCFH'],
    '13 L bucket, supplied with the 13 x 30 cm Sweepex float. Spares: squeeze roller set (2), grate, 13 x 30 cm sponges and floats.', desc='what',
    desc_replace=[('Wash bucket with twin squeeze rollers and sponge float for cleaning grout residue off walls and floors. Single unit or 4 pack.',
                   '13 litre wash bucket with twin squeeze rollers, supplied with the 13 x 30 cm Sweepex sponge float, for cleaning grout residue off walls and floors. Single unit or 4 pack.')])
add('RAI-PULIRAPID', 'parent', ['RAI-SRS3'] + SM_FL + SM_SP + ['RAI-QCFH'],
    '20 L bucket, supplied with the 13 x 30 cm Sweepex float. Spares: squeeze roller set (3), 13 x 30 cm sponges and floats.', desc='what')
add('RAI-PEDALO', 'parent', LG_FL + PL_FL + LG_SP + PL_SP + ['RAI-AHSEC', 'RAI-QCFH'],
    '40 L bucket, supplied with the 17 x 34 cm float, the 13 x 42 cm pole float and the 2-piece aluminium handle. Spares: those sponges, floats and the handle.', desc='what',
    desc_replace=[('High absorption Sweepex sponge with aluminium handle',
                   'Supplied with the 17 x 34 cm Sweepex float, the 13 x 42 cm pole float and the 2-piece aluminium handle')])
add('RAI-SMART', 'parent', ['RAI-SMARTRS2', 'RAI-SPGSM'] + SM_FL + SM_SP + ['RAI-QCFH'],
    'Supplied with a Sweepex sponge float, grate and handle. Spares: roller set (2), grate, 13 x 30 cm sponges and floats.', desc='what')
add('RAI-QCFH', 'parent', SM_SP + LG_SP + ['RAI-SKIPPER', 'RAI-PULIRAPID', 'RAI-PEDALO', 'RAI-SMART'], 'Takes the 13 x 30 cm and 17 x 34 cm Sweepex sponges (plain, cut or carved) with the Easy Lock fitting.', desc='what')
for s, t in [('RAI-SMSPONGE', 'Raimondi Sweepex Sponge 13 x 30cm - suits Easy Lock float (Skipper, Pulirapid, Smart)'),
             ('RAI-SMSPONGECUT', 'Raimondi Sweepex Sponge - Cut - 13 x 30cm - suits Easy Lock float (Skipper, Pulirapid, Smart)'),
             ('RAI-SMSPONGECV', 'Raimondi Sweepex Sponge 13 x 30cm - Carved - suits Easy Lock float (Skipper, Pulirapid, Smart)')]:
    add(s, 'item', ['RAI-QCFH'] + SM_FL + ['RAI-SKIPPER', 'RAI-PULIRAPID', 'RAI-SMART'],
        'Raimondi quick-change float handle (Easy Lock) and the 13 x 30 cm floats supplied with the Skipper, Pulirapid and Smart buckets', title=t, desc='prefix')
for s, t in [('RAI-LGSPONGE', 'Raimondi Sweepex Sponge 17 x 34cm - suits Easy Lock float (Pedalo)'),
             ('RAI-LGSPONGECUT', 'Raimondi Sweepex Sponge - Cut - 17 x 34cm - suits Easy Lock float (Pedalo)'),
             ('RAI-LGSPONGECV', 'Raimondi Sweepex Sponge 17 x 34cm - Carved - suits Easy Lock float (Pedalo)')]:
    add(s, 'item', ['RAI-QCFH'] + LG_FL + ['RAI-PEDALO'],
        'Raimondi quick-change float handle (Easy Lock) and the 17 x 34 cm floats, including the one supplied with the Pedalo', title=t, desc='prefix')
for s, t in [('RAI-PLSPONGE', 'Raimondi Sweepex Sponge 13 x 42cm - suits Pedalo pole float'),
             ('RAI-PLSPONGECUT', 'Raimondi Sweepex Sponge - Cut - 13 x 42cm - suits Pedalo pole float'),
             ('RAI-PLSPONGECV', None)]:
    add(s, 'item', PL_FL + ['RAI-PEDALO', 'RAI-AHSEC'], 'Raimondi 13 x 42 cm pole float (supplied with the Pedalo) on the sectional aluminium handle', title=t, desc='prefix')
for s, t in [('RAI-SMFLOAT', 'Raimondi Sweepex Float 13 x 30cm - suits Skipper, Pulirapid & Smart'),
             ('RAI-SMFLOATCUT', 'Raimondi Sweepex Float - Cut - 13 x 30cm - suits Skipper, Pulirapid & Smart')]:
    add(s, 'item', SM_SP + ['RAI-SKIPPER', 'RAI-PULIRAPID', 'RAI-SMART'],
        'The float supplied with the Skipper, Pulirapid and Smart buckets; takes the 13 x 30 cm Sweepex spare sponges', title=t, desc='prefix')
for s, t in [('RAI-LGFLOAT', 'Raimondi Sweepex Float 17 x 34cm - suits Pedalo'),
             ('RAI-LGFLOATCUT', 'Raimondi Sweepex Float - Cut - 17 x 34cm - suits Pedalo')]:
    add(s, 'item', LG_SP + ['RAI-PEDALO'], 'Supplied with the Pedalo; takes the 17 x 34 cm Sweepex spare sponges', title=t, desc='prefix')
for s, t in [('RAI-PLFLOAT', 'Raimondi Sweepex Sponge & Plate 13 x 42cm - suits Pedalo & aluminium handles'),
             ('RAI-PLFLOATCUT', 'Raimondi Sweepex Sponge Float - Cut - 13 x 42cm - suits Pedalo & aluminium handles')]:
    add(s, 'item', PL_SP + ['RAI-AH', 'RAI-AHSEC', 'RAI-PEDALO'],
        'Pedalo stand-up system on the Raimondi 27 mm aluminium handle; takes the 13 x 42 cm Sweepex spare sponges', title=t, desc='prefix')
add('RAI-BER', 'parent', ['RAI-BERSP', 'RAI-BERSPSW', 'RAI-BERSPEPO', 'RAI-AFL100G', 'RAI-BERWT'],
    'Takes 295 x 400 mm sponge rollers (Avana, Sweepex, cellulose for epoxy), anti-foam liquid and a spare water tray.', desc='what')
add('RAI-ROS', 'parent', ['RAI-BERSP', 'RAI-BERSPSW', 'RAI-BERSPEPO', 'RAI-AFL100G'],
    'Takes the same 295 x 400 mm sponge rollers as the Berta (Avana, Sweepex, cellulose for epoxy) and anti-foam liquid.', desc='what',
    desc_replace=[('Raimondi Rosina sponge roller machine for fast clean-up of cement-based and epoxy grout residue on large tiled floor areas.',
                   'Raimondi Rosina sponge roller machine for fast clean-up of cement-based and epoxy grout residue on large tiled floor areas.</p><ul><li>0.5 hp motor, two speeds (18 and 22 rpm)</li><li>Cleans about 100 m2 per hour</li><li>56 kg; the heavier, faster sister of the Berta</li></ul><p>')])
for s, t in [('RAI-BERSP', 'Raimondi Sponge Roller - Standard Avana - suits Berta & Rosina'),
             ('RAI-BERSPSW', 'Raimondi Sponge Roller - Long Life Sweepex - suits Berta & Rosina'),
             ('RAI-BERSPEPO', 'Raimondi Sponge Roller - Epoxy Cellulose - suits Berta & Rosina')]:
    add(s, 'item', ['RAI-BER', 'RAI-ROS'], 'Raimondi Berta and Rosina grout clean-up machines (295 x 400 mm roller)', title=t, desc='prefix')
add('RAI-AFL100G', 'item', ['RAI-BER', 'RAI-ROS'], 'Raimondi Berta and Rosina grout clean-up machines', title='Raimondi Anti Foam Liquid - suits Berta & Rosina', desc='prefix')
add('RAI-BERWT', 'item', ['RAI-BER'], 'Raimondi Berta', desc='prefix')
add('RAI-FRS40', 'parent', ['RAI-FRS40SR', 'RAI-AH', 'RAI-AHSEC'], 'Takes the matching spare double foam rubber (40, 50 or 75 cm) and a Raimondi aluminium handle.', desc='what')
add('RAI-FRS40SR', 'item', ['RAI-FRS40'], 'Raimondi double foam rubber squeegee of the same width', desc='prefix')
add('RAI-RGFR', 'parent', ['RAI-RGFRR'], 'Spare blue rubber available.', desc='what')
add('RAI-RGFRR', 'item', ['RAI-RGFR'], 'Raimondi blue grout float with changeable rubber (RAI-RGFR)', title='Raimondi Blue Grout Float Replacement Rubber - suits RAI-RGFR', desc='prefix')
add('RAI-AH', 'parent', ['RAI-BWSB', 'RAI-SCSP', 'RAI-SLGR', 'RAI-FRS40', 'RAI-PLFLOAT', 'RAI-PLFLOATCUT'],
    '27 mm handle for the Raimondi broom head, screed spreader, levelling rake, foam rubber squeegees and the 13 x 42 cm pole floats.', desc='what')
add('RAI-AHSEC', 'parent', ['RAI-BWSB', 'RAI-SCSP', 'RAI-SLGR', 'RAI-FRS40', 'RAI-PLFLOAT', 'RAI-PLFLOATCUT', 'RAI-PEDALO'],
    '27 mm 2-piece handle for the Raimondi broom head, screed spreader, levelling rake, foam rubber squeegees and the 13 x 42 cm pole floats; the Pedalo comes with it.', desc='what')
add('RAI-BWSB', 'item', ['RAI-AH', 'RAI-AHSEC'], 'Raimondi 27 mm aluminium handles', desc='prefix')
add('RAI-SCSP', 'item', ['RAI-AH', 'RAI-AHSEC'], 'Raimondi 27 mm aluminium handles; 500 mm wide spreader head', desc='prefix')
add('RAI-SLGR', 'item', ['RAI-AH', 'RAI-AHSEC'], 'Raimondi 27 mm aluminium handles; 600 mm wide, depth gauge 0 to 20 mm', desc='prefix')
add('RAI-SPADKIT', 'parent', ['RAI-SPADF'], 'Comes with the Velcro handle and one pad of each grade; spare 120 x 250 mm pads sold separately.', desc='what')
add('RAI-SPADF', 'item', ['RAI-SPADKIT'], 'Raimondi scouring pad kit handle (120 x 250 mm Velcro)', desc='prefix')

# ---------------- drilling ----------------
add('EPDB-6', 'item', ['EPDB-5PUK', 'BP-DCDG'], 'Standard drill chuck (wet use); the suction drill guide in the EPDB-5PUK kit and the BAT Pro suction cup guide keep the bit on the mark', desc='prefix')
add('EPDB-5PUK', 'parent', ['EPDB-6'], 'The guide takes 5 to 12 mm electroplated bits; spare bits are sold singly.', desc='what')
add('BP-DCDB5', 'item', ['BP-DBAS1014', 'BP-DCDG'], 'M14 angle grinders (dry); M10 grinders with the BAT Pro M10 to M14 adapter set; start the hole with the suction cup drill guide', desc='prefix')
add('ETS-HW-006', 'item', ['BP-DBAS1014', 'BP-DCDG'], 'M14 angle grinders (dry); M10 grinders with the BAT Pro M10 to M14 adapter set', desc='prefix')
add('BP-DCDB5H', 'item', ['BP-DCDG'], 'Standard drill chuck (hex shaft, dry); start the hole with the suction cup drill guide', desc='prefix')
add('BP-DBAS1014', 'item', ['BP-DCDB5', 'ETS-HW-006'], 'Puts BAT Pro M14 dry diamond drill bits on M10 angle grinders',
    title='BAT Pro Drill Bit Adapter Set M10 to M14 - suits M14 drill bits on M10 grinders', desc='prefix')
add('BP-DCDG', 'parent', ['BP-DCDB5', 'BP-DCDB5H', 'EPDB-6', 'ETS-HW-006'], 'Suction cup guide for starting holes with BAT dry and wet diamond drill bits.', desc='what')
add('RAI-DPP10050', 'item', ['RAI-DPPM14AD'], '100 mm Velcro backing pad with M14 thread (RAI-DPPM14AD) on an angle grinder, 1800 to 4000 rpm', desc='prefix')
add('RAI-DPK6AG', 'item', ['RAI-DPPM14AD'], '100 mm Velcro backing pad with M14 thread (RAI-DPPM14AD) on an angle grinder', desc='prefix')
add('RAI-DPPM14AD', 'parent', ['RAI-DPP10050', 'RAI-DPK6AG'], 'Takes 100 mm Velcro diamond polishing pads and the 6-piece pad kits; M14 angle grinders.', desc='what')
add('RAI-ZAP10080', 'item', ['RAI-IPERPGS3'], 'Planetary heads (free-floating or geared), such as the Raimondi Ipertitina planetary gear set')

# ---------------- wet saw blades and bushes ----------------
SAWS = ['RAI-ZOE85A', 'RAI-SMS100', 'RAI-SA80']
add('BP-DBB250', 'item', SAWS, '300 and 350 mm sizes fit the Raimondi Zoe Advanced, SMS and SA 80 (30/25.4 mm bore); 250 mm fits the Pikus Advanced and other 250 mm saws',
    title='BAT Pro Segmented Diamond Blade for Wet Saws - 250, 300 & 350mm, suits Zoe, SMS & SA 80', desc='prefix')
add('BD-BUSH-2016', 'item', SAWS, 'Brass bush that adapts a blade bore to the saw arbor: 30 to 25.4 mm for the Raimondi Zoe, SMS and SA 80; 22.2 to 20 or 16 mm for angle grinder blades. The reinforced centre sizes suit the BAT Pro TRRC blades.', desc='prefix')

# ---------------- angle grinder blades and jolly tools ----------------
add('BD-MTR-105-R', 'item', ['RAI-BC45', 'RDXA3477'], '100 and 115 mm angle grinders (22.2/20/16 mm bore); the 115 mm also suits the Raimondi BC 45 jolly tool and Sigma Jolly Edge', desc='prefix',
    desc_replace=[('Bat Pro Diamond Mesh Turbo Rim Blade 105mm (4 inch).', 'BAT Pro Diamond Mesh Turbo Rim Blade, 105mm (4 inch) or 115mm (4.5 inch), 22.2/20/16mm bore.')])
add('BD-TTR-105', 'item', ['RAI-BC45', 'RDXA3477'], '100 to 125 mm angle grinders (22.2/20/16 mm bore); the 115 and 125 mm suit the Raimondi BC 45 jolly tool', desc='prefix')
add('BD-MTR-125-R', 'item', ['RAI-BC45'], '125 mm angle grinders (22.2/20 mm bore) and the Raimondi BC 45 jolly tool', desc='prefix')
add('PAN-TTR-125', 'item', ['RAI-BC45'], '125 mm angle grinders (22.2/20 mm bore) and the Raimondi BC 45 jolly tool', desc='prefix')
add('ETS-HW-012', 'item', [], '100 to 105 mm angle grinders', desc='prefix')
add('RAI-BC45', 'parent', ['BD-MTR-105-R', 'BD-TTR-105', 'BD-MTR-125-R', 'PAN-TTR-125'], 'Takes 115 or 125 mm diamond blades on most 600 to 1100 W angle grinders (grinder not included).', desc='what')
add('RDXA3477', 'parent', ['BD-MTR-105-R', 'BD-TTR-105'], 'Comes with a Sigma 115 mm blade (ART 75B); takes other 115 mm, 22 mm bore blades.', desc='what')

# ---------------- scrapers, knives, blades ----------------
for tool, blade, t in [('FS-412', 'FS-412-RB', 'Takes the 10-pack of 100 mm replacement blades.'),
                       ('FS-125', 'FS-125-RB', 'Takes the 5-pack of 125 mm replacement blades.'),
                       ('FS-300', 'FS-300-SB', 'Takes the 300 mm replacement blade.'),
                       ('GR-DLX-SG', 'GR-DLX-SB', 'Takes the spare blade set (serrated tooth plus tungsten grit).'),
                       ('BP-FKM6', 'BP-FKSB10', 'Takes the 10-piece spare blade set.'),
                       ('S A-DSJC', 'S A-DSJC-SB', 'Takes the spare blade set.'),
                       ('RAI-FPR', 'RAI-FPRBS', 'Takes the 6-piece replacement blade set.')]:
    add(tool, 'parent', [blade], t, desc='what')
add('FS-412-RB', 'item', ['FS-412'], 'BAT FS-412 short handled scraper')
add('FS-125-RB', 'item', ['FS-125'], 'BAT FS-125 floor scraper')
add('FS-300-SB', 'item', ['FS-300'], 'BAT FS-300 long handled floor scraper')
add('GR-DLX-SB', 'item', ['GR-DLX-SG'], 'BAT deluxe grout remover GR-DLX-SG', title='BAT Deluxe Grout Remover Spare Blades - suits GR-DLX-SG')
add('BP-FKSB10', 'item', ['BP-FKM6'], 'BAT Pro folding utility knife', title='BAT Pro Folding Utility Knife Spare Blade Set (10 pce) - suits BAT Pro folding knife')
add('S A-DSJC-SB', 'item', ['S A-DSJC'], 'BATSEAL Delta silicone joint cutter', title='BATSEAL Delta Joint Cutter Spare Blade Set - suits S A-DSJC')
add('RAI-FPRBS', 'item', ['RAI-FPR'], 'Raimondi Fakiro plaster rasp', title='Raimondi Plaster Rasp 6 pce Blade Set - suits Fakiro rasp')
add('UK-1', 'parent', [], 'Takes standard snap-off blades (BAT pack UKSB-10).', desc='what')
add('DWTN', 'parent', [], 'Replacement wheels: BAT-540SW (the same wheel as the BAT 540 and 640 cutters).', desc='what')

# ---------------- waterproofing ----------------
COVERS = ['BAT-3RRS', 'BAT-SRR100']
FRAMES = ['BAT-PRF230HD', 'PAN-PRF230', 'BAT-PRTS', 'BP-WPK1']
for s in FRAMES:
    add(s, 'parent', COVERS + ['BAT-PREP1200'], 'Takes 230 mm roller covers (set of 3 or carton of 100) and the BAT 1.2 to 2.4 m extension pole.', desc='what')
add('BAT-3RRS', 'item', FRAMES, '230 mm roller frames: BAT heavy duty, Panther, the BAT roller and tray set and the BAT Pro waterproofing kit',
    title='BAT Replacement Paint Roller Cover 230mm - Set of 3 - suits 230mm roller frames', desc='prefix')
add('BAT-SRR100', 'item', FRAMES, '230 mm roller frames: BAT heavy duty, Panther, the BAT roller and tray set and the BAT Pro waterproofing kit',
    title='BAT Replacement Roller Cover 230mm - Carton of 100 - suits 230mm roller frames', desc='prefix')
add('BAT-PREP1200', 'item', FRAMES + ['BAT-SR21500'], 'Threaded paint roller frames and the BAT spiked roller', desc='prefix')
add('BAT-SR21500', 'item', ['BAT-PREP1200'], 'Threaded extension poles such as the BAT 1.2 to 2.4 m pole', desc='prefix')

# ---------------- knee pads ----------------
add('KPA', 'parent', ['KP-SB', 'KP-RL', 'KP-ST'], 'Spares: buttons (set of 8), foam liners (pair) and rubber straps (set of 4).', desc='what')
add('KP-SB', 'item', ['KPA'], 'BAT KPA professional knee pads', title='BAT Replacement Buttons (Set of 8) - Suit KPA')
add('KP-RL', 'item', ['KPA'], 'BAT KPA professional knee pads')
add('KP-ST', 'item', ['KPA'], 'BAT KPA professional knee pads')
add('RAI-FFKP', 'parent', ['RAI-FLKP-RST', 'RAI-FLKP-ST'], 'Spares: rubber straps or elastic straps with clips (sets of 2).', desc='what')
add('RAI-FLKP', 'parent', ['RAI-FLKP-RST', 'RAI-FLKP-ST', 'RAI-FLKP-IN'], 'Spares: rubber straps, elastic straps with clips and foam inserts (sets of 2).', desc='what')
add('RAI-FLKP-RST', 'item', ['RAI-FFKP', 'RAI-FLKP'], 'Raimondi flat faced and flexible knee pads', title='Raimondi Replacement Kneepad Straps - Rubber - Set of 2 - suits flat faced & flexible pads', desc='prefix')
add('RAI-FLKP-ST', 'item', ['RAI-FFKP', 'RAI-FLKP'], 'Raimondi flat faced and flexible knee pads', title='Raimondi Knee Pad Strap - Fabric with Clips (Set of 2) - suits flat faced & flexible pads', desc='prefix')
add('RAI-FLKP-IN', 'item', ['RAI-FLKP'], 'Raimondi flexible knee pads', title='Raimondi Flexible Knee Pad Insert (Set of 2) - suits flexible pads', desc='prefix')
add('RDXT415', 'parent', ['RDXT417'], 'Spare liners (pair) available.', desc='what')
add('RDXT417', 'item', ['RDXT415'], 'Barwalt KN-1 ultralight knee pad')

# ---------------- silicone and sealers ----------------
GUNS = ['S A-CGP', 'ETS-HW-001', 'S A-CGT', 'S A-CGA']
BAT_SIL = ['BSC-11', 'BSA-11']
MAX_SIL = ['RDX1000mw', 'RDX1001v', 'RDX1004b', 'RDX1007']
SIL_TOOLS = ['S A-APP45', 'S A-BR-20', 'SA-CNC']
for g in ['S A-CGP', 'ETS-HW-001']:
    add(g, 'parent', BAT_SIL + MAX_SIL + SIL_TOOLS, 'Takes standard 300 and 310 ml cartridges: BATSEAL and Maxisil silicones.', desc='what')
for g in ['S A-CGT', 'S A-CGA']:
    add(g, 'parent', BAT_SIL + MAX_SIL + SIL_TOOLS, 'Takes standard 300 and 310 ml cartridges (BATSEAL and Maxisil silicones) and 600 ml sausage packs.', desc='what')
for s in BAT_SIL:
    add(s, 'item', GUNS + SIL_TOOLS + ['RDXA3000', 'RDXA2050a', 'RDXA2051', 'RDXA3010'], 'Any standard caulking gun. Finish the bead with the BATSEAL applicators; use backer rod in deep joints.', desc='prefix')
for s in MAX_SIL:
    add(s, 'item', GUNS + ['RDXA3000', 'RDXA2050a', 'RDXA2051', 'RDXA3010', 'S A-APP45', 'S A-BR-20'] +
        (['RDX2000'] if s in ('RDX1000mw', 'RDX1004b') else ['RDX2020'] if s == 'RDX1001v' else []),
        'Any standard caulking gun; Maxisil applicator, corner and extension nozzles' + (', Smoothtex A' if s in ('RDX1000mw', 'RDX1004b') else ', Smoothtex N' if s == 'RDX1001v' else ''))
add('S A-APP45', 'item', BAT_SIL + MAX_SIL, 'Any silicone or sealant bead', desc='prefix')
add('S A-BR-20', 'item', BAT_SIL + MAX_SIL, 'Deep joints before any silicone or sealant', desc='prefix')
add('SA-CNC', 'item', BAT_SIL + MAX_SIL, 'Any silicone cartridge', desc='prefix')
add('RDXA3000', 'item', MAX_SIL + BAT_SIL, 'Any silicone bead')
add('RDXA2050a', 'item', MAX_SIL + BAT_SIL, 'Standard silicone cartridges')
add('RDXA2051', 'item', MAX_SIL + BAT_SIL, 'Standard silicone cartridges')
add('RDXA3010', 'item', MAX_SIL + BAT_SIL, 'Standard silicone cartridge nozzles')
add('RDX2000', 'item', ['RDX1000mw', 'RDX1004b'], 'Maxisil Wet Area and Maxisil Pool silicone')
add('RDX2020', 'item', ['RDX1001v'], 'Maxisil Natural Stone silicone')
SOLV = ['BC-SML1', 'BC-SWL1', 'BC-SPELSB1']
add('BC-EVSOL1', 'item', SOLV, 'Thins the BATSEAL Matt Look, Wet Look and Silcopel solvent-based sealers and cleans up after them', desc='prefix')
for s in SOLV:
    add(s, 'parent', ['BC-EVSOL1'], 'Thin and clean up with BATSEAL Eversol solvent.', desc='what')

# ---------------- floor drains ----------------
add('BAT-SFDPVCC', 'item', ['BAT-SFD100', 'BAT-SFD100SH'], 'BAT chrome plated square floor drains with a 100 mm outlet that take a PVC collar', desc='prefix')
DRAINS = ['BAT-SFD100', 'BAT-SFD100SH', 'BAT-SFD100MB', 'BAT-SFD80', 'BAT-LSFD80', 'BAT-SFD50']
add('BL-RPF100100R', 'item', DRAINS, 'Sits under the floor waste: 100 x 100 for 100 mm drains, 80 x 80 for 80 mm drains, 80 x 50 for 50 mm drains', desc='prefix')
for s in ['BAT-SFD100', 'BAT-SFD100SH']:
    add(s, 'parent', ['BAT-SFDPVCC', 'BL-RPF100100R'], 'Spare PVC collar and a recessed puddle flange (100 x 100) available.', desc='what')
for s in ['BAT-SFD100MB', 'BAT-SFD80', 'BAT-LSFD80', 'BAT-SFD50']:
    add(s, 'parent', ['BL-RPF100100R'], 'Recessed puddle flange available to match the outlet size.', desc='what')

# ---------------- large format handling ----------------
add('RAI-LEVTOP-PLUS', 'parent', ['RAI-VSCRV175B'], 'Uses two RV175 battery suction cups (included); spares available.', desc='what')

# ---------------- Sigma ----------------
S4UP = ['RDXA3614', 'RDXA3615', 'RDXA3616']
S4NEX = ['RDXA3642', 'RDXA3643', 'RDXA3644', 'RDXA3617', 'RDXA3618']
S4COMMON = ['RDXA3634', 'RDXA3635', 'RDXA3628']
add('RDXA3510', 'parent', ['RDXA3516C', 'RDXA3511', 'RDXA3512', 'RDXA3552', 'RDXA3649'], 'Takes the 12 mm scoring wheel 14A (titanium 14T). Spares: 19C square, 108616 clamping knob and nut.', desc='what')
add('RDXA3503', 'parent', ['RDXA3525C', 'RDXA3516', 'RDXA3520', 'RDXA3512', 'RDXA3552'], 'Takes the 12 mm scoring wheel 14A (titanium 14T). Spares: 90D3 swivel bar, 19B3 square, 24C handle.', desc='what')
add('RDXA3498', 'parent', ['RDXA3512', 'RDXA3552'], 'Takes the 12 mm scoring wheel 14A (titanium 14T).', desc='what')
for s, bar in [('RDXA3614', 'RDXA3631'), ('RDXA3615', 'RDXA3632'), ('RDXA3616', 'RDXA3633')]:
    add(s, 'parent', [bar, 'RDXA3625'] + S4COMMON + ['RDXA3619', 'RDXA3620'], 'Takes the 12 mm scoring wheel 14U (titanium 14UT). Spares: swivel measurement bar, 24U handle, 483/484 support arms, ART022 laser.', desc='what')
for s in S4NEX:
    add(s, 'parent', ['RDXA3626'] + S4COMMON + ['RDXA3621', 'RDXA3622'], 'Takes the 16 mm scoring wheel 14N (titanium 14NT). Spares: 24N handle, 483/484 support arms, ART022 laser.', desc='what')
add('RDXA3598', 'parent', ['RDXA3584', 'RDXA3479', 'RDXA3623', 'RDXA3637', 'RDXA3594'], 'Takes the 19 mm wheel 14K and the Kera Flex suction cups 51C and 51P4; the ART 63G table has hooks for it.', desc='what')
add('RDXA3540', 'parent', ['RDXA3629', 'RDXA3630'], 'Spare Pro Grip cups: 51M3 for the straight bar, 51M4 for the cross bar.', desc='what')
add('RDXA3594', 'parent', ['RDXA3593', 'RDXA3598'], 'Takes the ART 400 clamp pair; a stand for the Kera Cut.', desc='what', type_='Large Format Tile Handling')
add('RDXA3637', 'item', ['RDXA3598'], 'Sigma Kera Cut (hooks on the table); clamps included', desc='prefix', type_='Large Format Tile Handling')
TMP = 'Tiling Machine Parts'
add('RDXA3516C', 'item', ['RDXA3510'], 'Sigma Tecnica 2G', title='Sigma 19C Square - suits Tecnica 2G', desc='prefix', type_=TMP)
add('RDXA3516', 'item', ['RDXA3503'], 'Sigma Tecnica 2A3, 2B3 and 2D4', title='Sigma 19B3 Square - suits Tecnica 2A3, 2B3 & 2D4', type_=TMP)
add('RDXA3516B', 'item', [], 'Sigma Series 3: 3G, 3L, 3B2, 3C2, 3D2 and the Max 3B3M to 3F3M', title='Sigma 19D Square - suits Series 3 cutters', desc='prefix', type_=TMP)
add('RDXA3646', 'item', [], '260 mm square; check the part number against your cutter', type_=TMP)
add('RDXA3518', 'item', [], 'Sigma 3C2, 3D2 and 4A', title='Sigma 24AE Handle - suits 3C2, 3D2 & 4A', desc='prefix', type_=TMP)
add('RDXA3520', 'item', ['RDXA3503'], 'Sigma Tecnica 2A3 and 2B3', title='Sigma 24C Handle - suits Tecnica 2A3 & 2B3', desc='prefix', type_=TMP)
add('RDXA3517', 'item', [], 'Sigma 3L, 3B2, 5B and 6', title='Sigma 24E Handle - suits 3L, 3B2, 5B & 6', desc='prefix', type_=TMP)
add('RDXA3519', 'item', [], 'Sigma Max 3C3M, 3D3M and 3P3M', title='Sigma 24M10X Handle - suits Max 3C3M, 3D3M & 3P3M', desc='prefix', type_=TMP)
add('RDXA3528', 'item', [], 'Sigma Max 3E3M and 3F3M', title='Sigma 24M15X Handle - suits Max 3E3M & 3F3M', desc='prefix', type_=TMP)
add('RDXA3539', 'item', [], 'Sigma Max series; check the part number against your cutter', desc='prefix', type_=TMP)
add('RDXA3525C', 'item', ['RDXA3503'], 'Sigma Tecnica 2A3, 2B3 and 2D4', title='Sigma 90D3 Swivel Measurement Bar - suits Tecnica 2A3, 2B3 & 2D4', type_=TMP)
add('RDXA3560', 'item', [], 'Sigma 3B2 and 3B3M', title='Sigma 90LB Swivel Measurement Bar - suits 3B2 & 3B3M', desc='prefix', type_=TMP)
add('RDXA3561', 'item', [], 'Sigma 3C2 and 3C3M', title='Sigma 90LC Swivel Measurement Bar - suits 3C2 & 3C3M', desc='prefix', type_=TMP)
add('RDXA3562', 'item', [], 'Sigma 3D, 3D2, 3DK, 3D2K, 3DM, 3D2M, 3D3M, 3P, 3P2, 3P2M and 3P3M', title='Sigma 90LD Swivel Measurement Bar - suits 3D & 3P series', type_=TMP)
add('RDXA3585', 'item', [], 'Sigma 3E2M, 3E3M, 3F2M and 3F3M', title='Sigma 90LE Swivel Measurement Bar - suits 3E & 3F Max', type_=TMP)
add('RDXA3511', 'item', ['RDXA3510', 'RDXA3649'], 'Sigma Tecnica 2G swivel bar clamping knob (M8 x 25); takes the 108362 nut', type_=TMP)
add('RDXA3544', 'item', ['RDXA3649'], 'Sigma Series 3: 3G, 3L, 3B2, 3C2, 3D2 and the Max 3B3M to 3F3M', title='Sigma 108621 Locking Bolt M8 x 40 - suits Series 3 cutters', type_=TMP)
add('RDXA3649', 'item', ['RDXA3511', 'RDXA3544'], 'Sigma M8 locking bolts 108616 and 108621', type_=TMP)
add('RDXA3548', 'item', [], 'Sigma Max 3B3M, 3C3M, 3D3M, 3P3M, 3E3M and 3F3M (19 mm wheel)', title='Sigma Cutting Wheel ART14MX 19mm - suits Series 3 Max cutters', type_=TMP)
add('RDXA3535', 'item', [], 'Sigma Tecnica 2D4 and Series 3 Klick Klock cutters (15 mm wheel)', type_=TMP)
WHEEL12 = 'Sigma 2G, 2A3, 2B3, 7F, Series 3 (not Max), 4A, 5B and 6: every cutter with a 12 mm standard wheel'
add('RDXA3512', 'item', ['RDXA3510', 'RDXA3503', 'RDXA3498'], WHEEL12, title='Sigma Spare Wheel with axle ART14A 12mm - suits 2G, 2B3, 7F & Series 3', type_=TMP)
add('RDXA3552', 'item', ['RDXA3510', 'RDXA3503', 'RDXA3498'], WHEEL12, title='Sigma Titanium Wheel with axle ART14T 12mm - suits 2G, 2B3, 7F & Series 3', type_=TMP)
add('RDXA3619', 'item', S4UP, 'Sigma Series 4 Up: 4BU, 4CU and 4DU', title='Sigma Spare Wheel with axle ART14U 12mm - suits Series 4 Up (4BU, 4CU, 4DU)', type_=TMP)
add('RDXA3620', 'item', S4UP, 'Sigma Series 4 Up: 4BU, 4CU and 4DU', title='Sigma Titanium Wheel with axle ART14UT 12mm - suits Series 4 Up (4BU, 4CU, 4DU)', type_=TMP)
add('RDXA3621', 'item', S4NEX, 'Sigma Series 4 NEX: 4BN, 4CN, 4DN, 4EN and 4FN', title='Sigma Spare Wheel with axle ART14N 16mm - suits Series 4 NEX', type_=TMP)
add('RDXA3622', 'item', S4NEX, 'Sigma Series 4 NEX: 4BN, 4CN, 4DN, 4EN and 4FN', title='Sigma Titanium Wheel with axle ART14NT 16mm - suits Series 4 NEX', type_=TMP)
add('RDXA3625', 'item', S4UP, 'Sigma Series 4 Up: 4BU, 4CU and 4DU', type_=TMP)
add('RDXA3626', 'item', S4NEX, 'Sigma Series 4 NEX: 4BN, 4CN, 4DN, 4EN and 4FN', type_=TMP)
for s in ['RDXA3634', 'RDXA3635', 'RDXA3628']:
    add(s, 'item', S4UP + S4NEX, 'Sigma Series 4 (Up and NEX)', type_=TMP)
add('RDXA3631', 'item', ['RDXA3614'], 'Sigma 4BU', type_=TMP)
add('RDXA3632', 'item', ['RDXA3615'], 'Sigma 4CU', type_=TMP)
add('RDXA3633', 'item', ['RDXA3616'], 'Sigma 4DU', type_=TMP)
add('RDXA3584', 'item', ['RDXA3598'], 'Sigma Kera Cut', type_=TMP)
add('RDXA3593', 'item', ['RDXA3594'], 'Sigma ART 63E aluminium workbench', type_=TMP)
add('RDXA3479', 'item', ['RDXA3598'], 'Sigma Kera Cut', type_='Suction Cups & Lifters')
add('RDXA3623', 'item', ['RDXA3598'], 'Sigma Kera Cut', type_='Suction Cups & Lifters')
add('RDXA3629', 'item', ['RDXA3540'], 'Sigma Kera Lift 1A6 to 1D3 (straight bar)', type_='Suction Cups & Lifters')
add('RDXA3630', 'item', ['RDXA3540'], 'Sigma Kera Lift (cross bar)', type_='Suction Cups & Lifters')

# BAT hand tools wrongly typed as cutters
for s in ['GR-DLX-SG', 'GR-DLX-SB', 'DWTN', 'HDTN', 'PN', 'BP-FKSB10', 'BP-FKM6', 'BP-LVFC', 'SN', 'SN-CJ', 'SN-SCJ', 'STN', 'UK-1']:
    E.setdefault(s, dict(role=None, fits=[], text=None, title=None, type=None, desc=None, desc_replace=[]))
    E[s]['type'] = 'Tiling Tools'

# ---------------- Raimondi corrections on top of the live map ----------------
add('RAI-BULLMFK', 'item', ['RAI-BULLDOG'], 'Raimondi Bulldog (RAI-BULLDOG). The Bi-Bulldog takes its own kit, RAI-BIBULLMFK, available to order.',
    title='Raimondi Manual Feed Kit - suits Bulldog (Bi-Bulldog kit to order)',
    desc_replace=[('Optional manual feed kit for the Raimondi Bulldog and Bi-Bulldog profiling machines.',
                   'Optional manual feed kit for the Raimondi Bulldog profiling machine (the Bi-Bulldog takes its own kit, RAI-BIBULLMFK, available to order).')])
add('RAI-BULLCP', 'item', None, 'Raimondi Bulldog and Bi-Bulldog, to run machines in line',
    desc_replace=[('Pair of guides that connect the Raimondi Back-Finisher to the Bulldog profiling machine.',
                   'Pair of attachment arms that connect Raimondi Bulldog and Bi-Bulldog machines (or the Back-Finisher) in line, so longer pieces run through more than one machine.')])
BIB_FIX = [('Supplied with 10mm radius shaping wheel, universal table and dressing stone',
            'Supplied with universal table and dressing stone; profiling wheels sold separately (choose the shaping, finishing and polishing wheels you need)')]
add('RAI-BIBULLDOG', 'parent', None, None, desc_replace=BIB_FIX)
add('RAI-BIBULLDOGM', 'parent', None, None, desc_replace=BIB_FIX)
add('RAI-BSTSR6', None, None, None, title='Raimondi Stainless Steel Slant Ridge Trowel')
add('RAI-ZOE85A', 'parent', ['BP-DBB250'], 'Takes 300, 350 or 360 mm diamond blades, 25.4 mm bore. Shares its extension tables and squares with the Pikus Advanced and SMS.',
    desc_replace=[('Blades: 300 mm or 350 mm diameter, 25.4 mm bore.', 'Blades: 300, 350 or 360 mm diameter, 25.4 mm bore.'),
                  ('110 mm with a 350 mm blade, up to 235 mm in two passes', '110 mm with a 350 mm blade, 120 mm with a 360 mm blade, up to 235 mm in two passes')])
add('RAI-SMS100', 'parent', ['BP-DBB250'], None)
add('RAI-SA80', 'parent', ['BP-DBB250'], None,
    desc_replace=[('The Zoe and SMS extension tables and squares do not fit the SA 80.',
                   'The Zoe and SMS extension tables and squares do not fit the SA 80. Optional Raimondi extras made for the SA 80, available to order: extension side square (RAI-ESSSA80), adjustable square (RAI-SSSA80), foot pedal (RAI-FPSA80) and extension bench (RAI-EBSA80).')])
add('RAI-RGFS', None, None, None, desc_replace=[('Rectangular grout float with soft rubber, suited to epoxy grouting.', 'Rectangular grout float, 115 x 250mm, with soft blue rubber, suited to epoxy grouting.')])
add('RAI-RGFH', None, None, None, desc_replace=[('Rectangular grout float with hard rubber, suited to epoxy grouting.', 'Rectangular grout float, 115 x 250mm, with hard green rubber, suited to epoxy grouting.')])
add('RAI-VSCRV175B', 'item', ['RAI-EASYMOVE3-4RV', 'RAI-EASYMOVE3-6RV', 'RAI-EASYMOVE3-2VGMK4', 'RAI-LEVTOP-PLUS'],
    'Raimondi Easymove LFT bars, Easymove Mk4 frames and the Levtop Plus, or hand-held')
# BAT text fixes without fits
add('BAT-SS4-SG', None, None, None, desc_replace=[('including 4mm, 6mm, 8mm, 10mm, 12mm and 15mm.', 'including 4mm, 6mm, 8mm, 10mm and 15mm.')])
add('BAT-BS4-SG', None, None, None, desc_replace=[('4mm, 6mm, 8mm, 10mm, 12mm and 15mm halfmoon.', '4mm, 6mm, 8mm, 10mm, 12mm and 15mm.')])
add('BAT-SB-1200', None, None, None, desc_replace=[('Used to level and smooth out materials such as concrete and screed.',
                                                      'Used to level and smooth out materials such as concrete and screed. The 4200mm and 5000mm bars have double handles.')])

# ---------------- build payload ----------------
def existing(p):
    fw = json.loads(p['fitsWith']['value']) if p.get('fitsWith') else []
    fm = p['fitsModels']['value'] if p.get('fitsModels') else None
    return fw, fm


MACHINE_TYPES = {'Tile Saws', 'Tiling Machines', 'Tile Cutters', 'Large Format Tile Handling'}
payload = {}
for sku, e in E.items():
    p = by_sku[sku]
    fw0, fm0 = existing(p)
    fits = fw0 if e['fits'] is None else [pid(s) for s in e['fits']]
    if e['fits'] is not None and fw0 and sku in ('RAI-ZOE85A', 'RAI-SMS100', 'RAI-SA80', 'RAI-VSCRV175B'):
        fits = fw0 + [g for g in fits if g not in fw0]
    text = e['text'] if e['text'] is not None else fm0
    role = e['role']
    if role is None and (fits or text):
        role = 'parent' if p['productType'] in MACHINE_TYPES else 'item'
    payload[p['id']] = dict(sku=sku, title=e['title'], type=e['type'], fits=fits, text=text, role=role,
                            desc=e['desc'], desc_replace=e['desc_replace'])
# every other product that already has fits data (Raimondi baseline) gets a role
for p in P:
    fw0, fm0 = existing(p)
    if p['id'] in payload or not (fw0 or fm0):
        continue
    payload[p['id']] = dict(sku=p['variants'][0]['sku'], title=None, type=None, fits=fw0, text=fm0,
                            role='parent' if p['productType'] in MACHINE_TYPES else 'item', desc=None, desc_replace=[])
# Bi-Bulldogs: drop the Bulldog-only manual feed kit from their lists
for s in ('RAI-BIBULLDOG', 'RAI-BIBULLDOGM'):
    g = pid(s); payload[g]['fits'] = [x for x in payload[g]['fits'] if x != pid('RAI-BULLMFK')]
# machine role for the Raimondi machines that were role-less by type (e.g. Berta is Tiling Machines: ok)
json.dump(payload, open(out + '/payload.json', 'w'), indent=1)

with open(out + '/compatibility-all.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['product_id', 'vendor', 'sku', 'title', 'role', 'fits_models', 'fits_with_ids', 'fits_with_titles'])
    for g, d in sorted(payload.items(), key=lambda kv: (by_id[kv[0]]['vendor'], by_id[kv[0]]['title'])):
        p = by_id[g]
        w.writerow([g.split('/')[-1], p['vendor'], d['sku'], d['title'] or p['title'], d['role'], d['text'] or '',
                    ' '.join(x.split('/')[-1] for x in d['fits']), ' | '.join(by_id[x]['title'] for x in d['fits'] if x in by_id)])
print(len(payload), 'products in the map;', sum(1 for d in payload.values() if d['title']), 'title changes;',
      sum(1 for d in payload.values() if d['type']), 'type changes;', sum(1 for d in payload.values() if d['desc'] or d['desc_replace']), 'description edits')
