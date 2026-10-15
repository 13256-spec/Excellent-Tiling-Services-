"""Second pass over the tNN.graphql batches from add_tools_raimondi.py.

Replaces the per-type default weight and box size with realistic values per product,
fixes product types the keyword table got wrong (spare grates, Ipertitina brush),
and marks the Ipertitina 110 as Perth delivery only.

Usage: python3 patch_tools_shipping.py BATCH_DIR   (writes BATCH_DIR/fixed/tNN.graphql)
"""
import re,glob,sys,os
D=sys.argv[1] if len(sys.argv)>1 else 'out'
# title regex -> (weight kg, box)
T=[
(r'Bulldog (45|Flat) Shaping',1.0,'20 x 20 x 10 cm'),
(r'Raizor MK2 Rail|MK2 PLUS Rail',14,'340 x 20 x 15 cm'),
(r'Raizor Modular',9,'160 x 20 x 15 cm'),
(r'Spare Cutting Wheel',0.05,'10 x 10 x 3 cm'),
(r'Compass Cutting',1.5,'60 x 15 x 10 cm'),
(r'Power Raizor Cutting Apparatus|Power Raizor - MK2',6,'50 x 30 x 20 cm'),
(r'Dust Suppression|Dust Containment',1.0,'30 x 20 x 10 cm'),
(r'Small Pliers',0.5,'25 x 10 x 5 cm'),
(r'Snapping Pliers|Large Pliers',1.2,'35 x 15 x 8 cm'),
(r'Bigfoot XL Large',25,'140 x 70 x 20 cm'),(r'Bigfoot XXL Large',30,'170 x 80 x 20 cm'),
(r'Support Cylinders',2,'30 x 20 x 15 cm'),
(r'OnlyOne',10,'60 x 40 x 30 cm'),(r'Tyrell',15,'100 x 60 x 30 cm'),
(r'Corner Protector',0.3,'20 x 15 x 5 cm'),
(r'Levtop',2.5,'40 x 30 x 15 cm'),
(r'Medusa',0.4,'20 x 20 x 10 cm'),(r'Triventosa',1.2,'40 x 20 x 12 cm'),
(r'RV 175',1.5,'30 x 30 x 15 cm'),
(r'Grooving Tool - Jig',2.0,'40 x 20 x 10 cm'),(r'Grooving Tool Spare',0.1,'15 x 10 x 3 cm'),
(r'Rasp',0.3,'30 x 10 x 5 cm'),(r'Screed Bar Handles',0.3,'20 x 15 x 5 cm'),
(r'Tile Beater',1.0,'40 x 18 x 8 cm'),(r'Skirting Trowel',0.3,'30 x 10 x 5 cm'),
(r'Gauging Rake',1.0,'60 x 30 x 10 cm'),
(r'Iperbet Spare 45L',2.0,'50 x 50 x 50 cm'),(r'Clump Breaker',0.5,'30 x 10 x 10 cm'),
(r'Double Bladed Mix',1.5,'70 x 15 x 15 cm'),(r'Fluid Mixing Kit',3,'70 x 20 x 20 cm'),
(r'Liquid Stirrer',1.0,'70 x 15 x 15 cm'),(r'Bucket with Steel',1.0,'35 x 35 x 30 cm'),
(r'Lupetto Vibrator',8,'50 x 40 x 30 cm'),
(r'Spare Lithium',0.8,'20 x 15 x 10 cm'),
(r'Lupetto (11 Row|Flat)',3,'40 x 30 x 10 cm'),(r'Terranova 11 Row',5,'50 x 40 x 10 cm'),
(r'Transformer',5,'30 x 25 x 20 cm'),(r'Screed Spreader',1.0,'50 x 15 x 10 cm'),
(r'Maxititina 12L',2,'40 x 30 x 30 cm'),(r'Felt Disc',0.3,'35 x 35 x 5 cm'),
(r'Grouting Paddle',2,'40 x 40 x 10 cm'),(r'Replacement Rubber Set',0.5,'40 x 10 x 5 cm'),
(r'Maxititina (Abrasive|Medium|Stiff|Steel)',1.5,'35 x 35 x 10 cm'),
(r'Velcro Disc',1.2,'35 x 35 x 8 cm'),(r'Ballast',6,'30 x 20 x 10 cm'),
(r'Splash Guard|Suction Skirt',1.0,'50 x 50 x 10 cm'),(r'16 Ltr Watertank',2,'40 x 30 x 30 cm'),
(r'Ipertitina Abrasive Brush',3,'50 x 50 x 15 cm'),(r'Vacuum Connector',0.3,'20 x 10 x 10 cm'),
(r'Vacuum Hose',0.5,'30 x 30 x 10 cm'),
(r'Polishing Pad|Pad Kit|Pad Adapter',0.3,'15 x 15 x 5 cm'),(r'Zirconium',0.05,'15 x 15 x 2 cm'),
(r'Pedalo',8,'60 x 40 x 40 cm'),
(r'Aluminium Handle - 1330',0.6,'140 x 8 x 8 cm'),
(r'Spare Plastic Grate',0.3,'40 x 30 x 5 cm'),
(r'Tip Top',1.5,'30 x 20 x 10 cm'),(r'Elia',6,'60 x 40 x 20 cm'),
(r'Straps|Strap',0.1,'20 x 10 x 3 cm'),(r'Knee Pad Insert',0.2,'20 x 15 x 5 cm'),
(r'Husky',1.2,'35 x 25 x 12 cm'),(r'Isola',1.5,'40 x 30 x 10 cm'),
(r'Nelson',6,'50 x 40 x 30 cm'),(r'Pugiol',10,'90 x 50 x 15 cm'),
(r'Paver / Slab Lifter',2,'60 x 20 x 10 cm'),(r'Extending Slab',4,'100 x 20 x 10 cm'),
(r'Tool Bag',1.0,'50 x 30 x 20 cm'),(r'Waffled Shoes',1.0,'35 x 25 x 12 cm'),
(r'Wedges - 28mm',1.5,'30 x 20 x 15 cm'),(r'Clipdozer',0.8,'30 x 15 x 8 cm'),
]
SKU={'RAI-RFH870':(0.5,'20 x 15 x 10 cm'),'RAI-RFH6120':(1.0,'25 x 20 x 10 cm'),'RAI-RFH8120':(1.0,'25 x 20 x 10 cm'),
     'RAI-RFH5500':(4,'40 x 30 x 20 cm'),'RAI-RFH6500':(4,'40 x 30 x 20 cm'),'RAI-RFH8500':(4,'40 x 30 x 20 cm')}
def fixvars(block,w,box):
    block=re.sub(r'weight:\{value:[\d.]+,',f'weight:{{value:{w},',block)
    block=re.sub(r'(key:"box_size",type:"single_line_text_field",value:)"[^"]*"',lambda m:m.group(1)+f'"{box}"',block)
    return block
for f in sorted(glob.glob(D+'/t*.graphql')):
    n=int(os.path.basename(f)[1:3])
    if n<39: continue
    s=open(f).read()
    parts=re.split(r'(?=\np\d+: productSet)',s)
    out=[]
    for p in parts:
        m=re.search(r'title:"(.*?)",vendor',p)
        if m:
            t=m.group(1)
            for rx,w,box in T:
                if re.search(rx,t): p=fixvars(p,w,box); break
            for sku,(w,box) in SKU.items():
                p=re.sub(r'(\{optionValues:(?:(?!\{optionValues).)*?sku:"%s"\})'%re.escape(sku),lambda mm:fixvars(mm.group(1),w,box),p)
            if 'Spare Plastic Grate' in t:
                p=p.replace('productType:"Floor Drains"','productType:"Grout Clean Up"').replace('"Floor Drains"','"Grout Clean Up"').replace('ha-10-2-3-1','ha-15-34').replace('value:"2216"','value:"1167"')
            if 'Ipertitina Abrasive Brush' in t:
                p=p.replace('"Tiling Machines"','"Tiling Tools"')
            if 'Ipertitina Electric Brush 110' in t and 'ship-local-only' not in p:
                p=p.replace('"ship-parcel"','"ship-local-only","ship-long"').replace('Ships Australia-wide from Perth, or pick up from our showroom.','Large item: delivered within Perth metro or collected from our showroom.')
            p=p.replace('Large or long item:','Large item:')
            p=p.replace('variants(first:20){nodes{id sku}}','handle')
        out.append(p)
    open(D+'/fixed/'+os.path.basename(f),'w').write(''.join(out))
print('ok')
