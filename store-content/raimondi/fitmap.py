"""Raimondi compatibility map: which accessory, blade, consumable or spare part fits which machine.
Sources: Raimondi catalogue A20/A23 (Zoe Advanced pages), A30-A33 (accessories for bridge saw machines,
Jan 2023), raimondispa.com product pages (Oct 2026), the May 2026 Raimondi price list (supplier) and the
store's own descriptions for the non-saw families. Output: compat.json (per product: fits_with product ids,
fits_models text, new title/description/SEO where rewritten) and compatibility.csv for the repo."""
import json, re, csv, html

allp = json.load(open('all.json'))
by_sku = {}
by_id = {}
for n in allp:
    pid = n['id'].split('/')[-1]
    by_id[pid] = n
    for v in n['variants']['nodes']:
        if v['sku']:
            by_sku[v['sku']] = pid

def P(sku):
    return by_sku[sku]

# ---- machines (product ids) ----
ZOE = P('RAI-ZOE85A'); SMS = P('RAI-SMS100'); SA80 = P('RAI-SA80')
BULLDOG = P('RAI-BULLDOG'); BIBULL = P('RAI-BIBULLDOG'); BIBULLM = P('RAI-BIBULLDOGM')
RZ_MK2 = P('RAI-RAIZOR-MK2'); RZ_PLUS = P('RAI-RAIZOR-MK2PLUS'); RZ_MOD = P('RAI-RAIZORMTC2X')
PWR_JIG = P('RAI-PWRRAIZORJIG'); PWR_MK2 = P('RAI-PWRRAIZOR-MK2')
EM_XL = P('RAI-EASYMOVE-XLIGHT10'); EM_4 = P('RAI-EASYMOVE3-4RV'); EM_6 = P('RAI-EASYMOVE3-6RV'); EM_MK4 = P('RAI-EASYMOVE3-2VGMK4')
BF_XL = P('RAI-BIGFOOTXL'); BF_XXL = P('RAI-BIGFOOTXXL')
IPERBET = P('RAI-IPERBET'); FLUMIX = P('RAI-FLUMIXSP')
EFOX = P('RAI-EFOX'); LUPETTO = P('RAI-LUPETTO'); TERRA = P('RAI-TERRA')
IPER110 = P('RAI-IPER110'); IPERPLUS = P('RAI-IPERTITINAPLUS'); MAXIT = P('RAI-MAXIT')
BERTA = P('RAI-BER'); SKIPPER = P('RAI-SKIPPER'); SMART = P('RAI-SMART'); PEDALO = P('RAI-PEDALO'); PULI = P('RAI-PULIRAPID')
RAICUT = P('RAI-RAICUT-JIG')

ZPS = 'Raimondi Zoe Advanced 85A, 105A, 130A and 155A, Pikus Advanced 85, 105 and 130, and SMS 100 and 125 bridge wet saws'
SAWS3 = 'Raimondi Zoe Advanced (all sizes), SMS 100/125 and SA 80 wet saws: any Raimondi saw that takes 300 to 350 mm blades with a 25.4 mm bore'

# accessory sku -> (fits_with machine ids, fits_models text, kind)
# kind: acc = accessory, blade = blade/consumable, part = spare part
ACC = {
 # --- wet saw accessories (Raimondi catalogue A30-A31) ---
 'RAI-FETPIK75': ([ZOE, SMS], ZPS + ' (Raimondi kit 423KITDL)', 'acc'),
 'RAI-ESSPZ':    ([ZOE, SMS], ZPS + ' (Raimondi 191CL04A)', 'acc'),
 'RAI-PZTCS':    ([ZOE, SMS], ZPS + ' (Raimondi 191CL04A1)', 'acc'),
 'RAI-RETZOE5':  ([ZOE, SMS], ZPS + ', and most other Raimondi bridge saws (Raimondi 374RU5D40I)', 'acc'),
 'RAI-SS90':     ([ZOE, SMS], 'Raimondi Zoe Advanced, Pikus Advanced, SMS 100/125, Exploit, Bolt and Mistral bridge saws (Raimondi 192SQ03A)', 'acc'),
 'RAI-SS4590':   ([ZOE, SMS], 'Raimondi Zoe Advanced, Pikus Advanced, SMS 100/125, Exploit, Bolt and Mistral bridge saws (Raimondi 192SQ07A)', 'acc'),
 'RAI-SS4590PZ': ([ZOE, SMS], 'Raimondi Zoe Advanced, Pikus Advanced and SMS bridge saws (right-hand version, supplier listing)', 'acc'),
 'RAI-PZ10THD':  ([ZOE, SMS], 'Choose the size for your saw: Zoe 105A / Pikus 105 / SMS 100 (Raimondi 423BL105ADV), Zoe 130A / Pikus 130 / SMS 125 (423BL130ADV), Zoe 155A (423BL150ADV). The Zoe Advanced comes with one; this is the spare or the size-up.', 'acc'),
 'RAI-EXWHK':    ([], 'Raimondi Exploit, Bolt and Mistral bridge saws only (Raimondi 315CR02K). Not for the Zoe, Pikus, SMS or SA 80, which come with a wheel kit.', 'acc'),
 # --- spare parts ---
 'RAI-ZOE85SAR': ([ZOE], 'Raimondi Zoe Advanced: 85A, 105A or 130A rail, choose your saw size', 'part'),
 'RAI-SW/EX/PK/ZO': ([ZOE], 'Raimondi Zoe Advanced, Pikus Advanced and Exploit wet saws', 'part'),
 'RAI-SCBEX/PK/ZOE': ([ZOE], 'Raimondi Zoe Advanced, Pikus Advanced and Exploit wet saws', 'part'),
 'RAI-ZOEBNB':   ([ZOE], 'Raimondi Zoe Advanced and Pikus Advanced wet saws (four per machine)', 'part'),
 'RAI-PL10AMP':  ([ZOE, SMS, SA80], 'Raimondi wet saws on a 10 A single-phase supply: Zoe Advanced, SMS, SA 80, Pikus Advanced', 'part'),
 # --- blades ---
 'RAI-DB12SET300B': ([ZOE, SMS, SA80], SAWS3, 'blade'),
 'RAI-DBCC300':     ([ZOE, SMS, SA80], SAWS3, 'blade'),
 'RAI-DBSET300B':   ([ZOE, SMS, SA80], SAWS3, 'blade'),
 'RAI-DBSET300G':   ([ZOE, SMS, SA80], SAWS3, 'blade'),
 'RAI-DBCC350':     ([ZOE, SMS, SA80], SAWS3, 'blade'),
 'RAI-DBCCT350':    ([ZOE, SMS, SA80], SAWS3, 'blade'),
 'RAI-DBSET350B':   ([ZOE, SMS, SA80], SAWS3, 'blade'),
 'RAI-DBSET350G':   ([ZOE, SMS, SA80], SAWS3, 'blade'),
 'RAI-DBSET360E':   ([ZOE, SMS, SA80], 'Raimondi SA 80, SMS and Zoe Advanced wet saws (14-inch class, 300 to 360 mm per the Raimondi catalogue, 25.4 mm bore)', 'blade'),
 'RAI-DBSET250SP':  ([], 'Raimondi Pikus Advanced 85, 105 and 130 (230 to 250 mm blades) and other 250 mm wet saws with a 25.4 mm bore', 'blade'),
 'RAI-DBSET250BE':  ([], 'Raimondi Pikus Advanced 85, 105 and 130 (230 to 250 mm blades) and other 250 mm wet saws with a 25.4 mm bore', 'blade'),
 'RAI-DBCC200':     ([], 'Raimondi Exploit and other 200 mm bridge saws with a 25.4 mm bore', 'blade'),
 'RAI-DBCC200E':    ([], 'Raimondi Exploit and other 200 mm bridge saws with a 25.4 mm bore', 'blade'),
 # --- Bulldog / Bi-Bulldog profiling ---
 'RAI-BULLMFK':  ([BULLDOG, BIBULL], 'Raimondi Bulldog and Bi-Bulldog profiling machines (already fitted on the Bi-Bulldog with Manual Feed Kit)', 'acc'),
 'RAI-BULLSEPR': ([BULLDOG, BIBULL, BIBULLM], 'Raimondi Bulldog and Bi-Bulldog profiling machines', 'acc'),
 'RAI-BULLCP':   ([BULLDOG, BIBULL, BIBULLM], 'Raimondi Bulldog and Bi-Bulldog, to connect the Back-Finisher', 'acc'),
 'RAI-BDBS':     ([BULLDOG, BIBULL, BIBULLM], 'Raimondi Bulldog and Bi-Bulldog profiling machines', 'blade'),
 'RAI-BDB100':   ([BULLDOG, BIBULL, BIBULLM], 'Raimondi Bulldog and Bi-Bulldog, on the polishing band holder', 'blade'),
 'RAI-BFW8R':    ([BULLDOG, BIBULL, BIBULLM], 'Raimondi Bulldog and Bi-Bulldog; match the radius to your shaping wheel', 'blade'),
 'RAI-BSWFB22R': ([BULLDOG, BIBULL, BIBULLM], 'Raimondi Bulldog and Bi-Bulldog profiling machines', 'blade'),
 'RAI-BPW10R400':([BULLDOG, BIBULL, BIBULLM], 'Raimondi Bulldog and Bi-Bulldog; match the radius to your shaping wheel', 'blade'),
 'RAI-BSW10R':   ([BULLDOG, BIBULL, BIBULLM], 'Raimondi Bulldog and Bi-Bulldog profiling machines', 'blade'),
 'RAI-BSW45':    ([BULLDOG, BIBULL, BIBULLM], 'Raimondi Bulldog and Bi-Bulldog profiling machines', 'blade'),
 'RAI-BSWF':     ([BULLDOG, BIBULL, BIBULLM], 'Raimondi Bulldog and Bi-Bulldog profiling machines', 'blade'),
 # --- Raizor / Power Raizor ---
 'RAI-PWRRAIZOR-MK2': ([RZ_MK2, RZ_PLUS, RZ_MOD], 'Raimondi Raizor MK2, Raizor MK2 PLUS and Raizor modular (MTCX2) rails', 'acc'),
 'RAI-PWRRAIZORJIG':  ([], 'The original Raimondi Raizor cutting guide (for the MK2, MK2 PLUS and modular rails use the Power Raizor MK2 unit)', 'acc'),
 'RAI-PWRRZRDSW': ([PWR_JIG], 'Raimondi Power Raizor cutting jig', 'acc'),
 'RAI-PWRRZRDCD': ([PWR_JIG], 'Raimondi Power Raizor cutting jig', 'acc'),
 'RAI-RAIZORM2SW':  ([RZ_MK2], 'Raimondi Raizor MK2', 'blade'),
 'RAI-RAIZORM2PSW': ([RZ_PLUS], 'Raimondi Raizor MK2 PLUS', 'blade'),
 'RAI-RAIZOR-SW':   ([], 'The original Raimondi Raizor cutting system (16 mm wheel with pin)', 'blade'),
 'RAI-RAIZOR-SWT':  ([], 'The original Raimondi Raizor cutting system (16 mm wheel with pin)', 'blade'),
 'RAI-FREECUTSMP': ([RZ_MK2, RZ_PLUS, RZ_MOD], 'Any score-and-snap rail such as the Raimondi Raizor; panels 3 to 6 mm thick', 'acc'),
 'RAI-LFTSPS':     ([RZ_MK2, RZ_PLUS, RZ_MOD], 'Any score-and-snap rail such as the Raimondi Raizor; panels 3 to 12 mm thick', 'acc'),
 'RAI-FREECUTLGP': ([RZ_MK2, RZ_PLUS, RZ_MOD], 'Any score-and-snap rail such as the Raimondi Raizor; tiles and slabs 6 to 20 mm thick', 'acc'),
 # --- Easymove / Bigfoot / handling ---
 'RAI-VSCRV175B': ([EM_4, EM_6, EM_MK4], 'Raimondi Easymove LFT bars and Easymove Mk4 frames, or hand-held', 'acc'),
 'RAI-ONLYONE':   ([EM_4, EM_6, EM_MK4, EM_XL], 'Raimondi Easymove frames', 'acc'),
 'RAI-TYRELL':    ([EM_4, EM_6, EM_MK4, EM_XL], 'Works with Raimondi Easymove and other carrying frames', 'acc'),
 'RAI-CAMADV':    ([EM_4, EM_6, EM_MK4, EM_XL], 'Holds slabs that are still on a Raimondi Easymove frame', 'acc'),
 'RAI-BIGFOOTXLEXT':  ([BF_XL], 'Raimondi Bigfoot XL', 'acc'),
 'RAI-BIGFOOTXXLEXT': ([BF_XXL], 'Raimondi Bigfoot XXL', 'acc'),
 'RAI-BM180SUP20': ([], 'Raimondi BM 180 and BM 180 Plus work benches', 'acc'),
 # --- mixers ---
 'RAI-IPERBU':  ([IPERBET], 'Raimondi Iperbet mixer', 'part'),
 'RAI-IPERCB':  ([IPERBET], 'Raimondi Iperbet mixer', 'acc'),
 'RAI-IPERDB':  ([IPERBET], 'Raimondi Iperbet mixer', 'part'),
 'RAI-IPERMKF': ([IPERBET], 'Raimondi Iperbet mixer', 'acc'),
 'RAI-FLUMIXB': ([FLUMIX], 'Raimondi Fluid Mix Special', 'part'),
 'RAI-FLUMIXLSPL': ([FLUMIX], 'Raimondi Fluid Mix Special', 'part'),
 # --- vibrators ---
 'RAI-EFOX-SB':    ([EFOX], 'Raimondi e-Fox cordless vibrator', 'part'),
 'RAI-LUPETTO-RA': ([LUPETTO], 'Raimondi Lupetto vibrator', 'acc'),
 'RAI-LUPETTO-VP': ([LUPETTO], 'Raimondi Lupetto vibrator', 'part'),
 'RAI-TERRA-RA':   ([TERRA], 'Raimondi Terranova vibrator', 'part'),
 'RAI-TERRATF':    ([TERRA], 'Raimondi Terranova vibrator', 'part'),
 # --- Ipertitina / Maxititina floor machines ---
 'RAI-IPER6KG':   ([IPER110, IPERPLUS], 'Raimondi Ipertitina 110 and Ipertitina Plus', 'acc'),
 'RAI-IPERDHV':   ([IPER110, IPERPLUS], 'Raimondi Ipertitina 110 and Ipertitina Plus', 'acc'),
 'RAI-IPERFDB':   ([IPER110, IPERPLUS], 'Raimondi Ipertitina 110 and Ipertitina Plus, on the Velcro disc holder', 'blade'),
 'RAI-IPERPGS3':  ([IPER110, IPERPLUS], 'Raimondi Ipertitina 110 and Ipertitina Plus', 'acc'),
 'RAI-IPERSGSK':  ([IPER110, IPERPLUS], 'Raimondi Ipertitina 110 and Ipertitina Plus', 'part'),
 'RAI-IPERTANK':  ([IPER110, IPERPLUS], 'Raimondi Ipertitina 110 and Ipertitina Plus', 'part'),
 'RAI-IPERTINEX': ([IPER110, IPERPLUS], 'Raimondi Ipertitina 110 and Ipertitina Plus', 'blade'),
 'RAI-IPERVAC2':  ([IPER110, IPERPLUS], 'Raimondi Ipertitina 110 and Ipertitina Plus', 'acc'),
 'RAI-IPERVAC3':  ([IPER110, IPERPLUS], 'Raimondi Ipertitina 110 and Ipertitina Plus', 'acc'),
 'RAI-IPERVACFH': ([IPER110, IPERPLUS], 'Raimondi Ipertitina 110 and Ipertitina Plus', 'acc'),
 'RAI-IPERVACSK': ([IPER110, IPERPLUS], 'Raimondi Ipertitina 110 and Ipertitina Plus', 'acc'),
 'RAI-ZAP10080':  ([IPER110, IPERPLUS], 'Planetary heads (free-floating or geared), e.g. the Raimondi Ipertitina planetary gear set', 'blade'),
 'RAI-MAXTANK':   ([MAXIT], 'Raimondi Maxititina', 'part'),
 'RAI-MAXTFDH':   ([MAXIT], 'Raimondi Maxititina, on the Velcro disc holder', 'blade'),
 'RAI-MAXTGP':    ([MAXIT], 'Raimondi Maxititina', 'acc'),
 'RAI-MAXTGPRRS': ([MAXIT], 'Raimondi Maxititina grouting paddle', 'part'),
 'RAI-MAXTINEX':  ([MAXIT], 'Raimondi Maxititina', 'blade'),
 'RAI-MAXTMNB':   ([MAXIT], 'Raimondi Maxititina', 'blade'),
 'RAI-MAXTSNB':   ([MAXIT], 'Raimondi Maxititina', 'blade'),
 'RAI-MAXTSWB':   ([MAXIT], 'Raimondi Maxititina', 'blade'),
 'RAI-MAXTVSDH2': ([MAXIT], 'Raimondi Maxititina', 'acc'),
 # --- grout clean-up ---
 'RAI-BERSP':    ([BERTA], 'Raimondi Berta (295 x 400 mm roller)', 'blade'),
 'RAI-BERSPEPO': ([BERTA], 'Raimondi Berta (295 x 400 mm roller)', 'blade'),
 'RAI-BERSPSW':  ([BERTA], 'Raimondi Berta (295 x 400 mm roller)', 'blade'),
 'RAI-AFL100G':  ([BERTA], 'Raimondi Berta sponge roller machine', 'blade'),
 'RAI-BERWT':    ([BERTA], 'Raimondi Berta', 'part'),
 'RAI-SPG':      ([SKIPPER], 'Raimondi Skipper wash bucket', 'part'),
 'RAI-SRS2':     ([SKIPPER], 'Raimondi Skipper wash bucket', 'part'),
 'RAI-SRS3':     ([PULI], 'Raimondi Pulirapid wash bucket', 'part'),
 'RAI-SMARTRS2': ([SMART], 'Raimondi Smart wash bucket', 'part'),
 'RAI-SPGSM':    ([SMART], 'Raimondi Smart wash bucket', 'part'),
 'RAI-PLSPONGECV': ([PEDALO], 'Raimondi Pedalo (13 x 42 cm carved sponge)', 'blade'),
 'RAI-PLFLOAT':  ([PEDALO], 'Raimondi aluminium handles and the Pedalo stand-up system (13 x 42 cm)', 'blade'),
 # --- Rai-Fix ---
 'RAI-RAICUT-SB': ([RAICUT], 'Raimondi Rai-Cut grooving jig (125 mm)', 'blade'),
 'RAI-RFH5500':   ([RAICUT], 'Slots cut with the Raimondi Rai-Cut jig; choose the hook for the tile thickness', 'acc'),
}

# machine -> fits_models text (what it takes)
MACHINE_TEXT = {
 ZOE: 'Takes 300 mm and 350 mm diamond blades, 25.4 mm bore. Shares its extension tables and squares with the Pikus Advanced and SMS.',
 SMS: 'Takes 300 mm and 350 mm diamond blades, 25.4 mm bore. Shares its extension tables and squares with the Zoe Advanced and Pikus Advanced.',
 SA80: 'Takes 300 to 350 mm diamond blades, 25.4 mm bore (Raimondi\'s catalogue lists up to 360 mm).',
 BULLDOG: 'Takes Raimondi Bulldog shaping, finishing and polishing wheels and polishing bands.',
 BIBULL: 'Takes Raimondi Bulldog shaping, finishing and polishing wheels and polishing bands.',
 BIBULLM: 'Takes Raimondi Bulldog shaping, finishing and polishing wheels and polishing bands.',
 RZ_MK2: 'Takes the Raizor MK2 spare wheel and the Power Raizor MK2 cutting unit.',
 RZ_PLUS: 'Takes the Raizor MK2 PLUS spare wheel and the Power Raizor MK2 cutting unit.',
 RZ_MOD: 'Takes the Power Raizor MK2 cutting unit.',
 PWR_JIG: 'Runs on the original Raizor cutting guide. Add the dust suppression or dust containment device.',
 PWR_MK2: 'Fits the Raizor MK2, MK2 PLUS and modular (MTCX2) rails.',
 EM_XL: 'Add the OnlyOne wheels device, a Tyrell cart or a CAM trolley.',
 EM_4: 'Uses RV175 battery suction cups. Add the OnlyOne wheels device, a Tyrell cart or a CAM trolley.',
 EM_6: 'Uses RV175 battery suction cups. Add the OnlyOne wheels device, a Tyrell cart or a CAM trolley.',
 EM_MK4: 'Uses RV175 battery suction cups. Add the OnlyOne wheels device, a Tyrell cart or a CAM trolley.',
 BF_XL: 'Takes the Bigfoot XL extension table.',
 BF_XXL: 'Takes the Bigfoot XXL extension table.',
 IPERBET: 'Spare 45 L bucket, clump breaker, double-bladed mix tool and fluid mixing kit available.',
 FLUMIX: 'Spare 75 L bucket and 3-spiral liquid stirrer available.',
 EFOX: 'Spare lithium-ion battery available.',
 LUPETTO: 'Takes the 11-row roller plate and the flat vibrating plate.',
 TERRA: 'Takes the 11-row roller plate; runs from the 300 W / 42 V transformer.',
 IPER110: 'Takes tools 49 to 60 cm: felt discs on the Velcro holder, abrasive brush, planetary gear set, ballast, tank, vacuum fittings.',
 IPERPLUS: 'Takes tools 49 to 60 cm: felt discs on the Velcro holder, abrasive brush, planetary gear set, ballast, tank, vacuum fittings.',
 MAXIT: 'Takes tools 45 to 60 cm: felt discs on the Velcro holder, nylon, abrasive and wire brushes, grouting paddle, 12 L tank.',
 BERTA: 'Takes 295 x 400 mm sponge rollers (Avana, cellulose for epoxy, Sweepex) and anti-foam liquid.',
 SKIPPER: 'Spare grate and squeeze rollers available.',
 SMART: 'Spare grate and rollers available.',
 PEDALO: 'Takes 13 x 42 cm Sweepex sponges (carved) on its pole float.',
 PULI: 'Spare squeeze roller set available.',
 RAICUT: 'Cuts the slot for Rai-Fix hooks; takes a 125 mm spare blade.',
}

KIND_ORDER = {'acc': 0, 'blade': 1, 'part': 2}
# expand multi-variant products: ACC is keyed by one sku per product
acc_by_pid = {}
for sku, (machines, text, kind) in ACC.items():
    pid = P(sku)
    acc_by_pid[pid] = (machines, text, kind)

machine_lists = {}
for pid, (machines, text, kind) in acc_by_pid.items():
    for m in machines:
        machine_lists.setdefault(m, []).append((KIND_ORDER[kind], by_id[pid]['title'], pid))
for m in machine_lists:
    machine_lists[m] = [pid for _, _, pid in sorted(machine_lists[m])]

out = {}
for pid, (machines, text, kind) in acc_by_pid.items():
    out[pid] = {'fits_with': machines, 'fits_models': text, 'kind': kind}
for m, lst in machine_lists.items():
    out.setdefault(m, {'fits_with': [], 'fits_models': MACHINE_TEXT.get(m, ''), 'kind': 'machine'})
    out[m]['fits_with'] = lst
    out[m]['kind'] = 'machine'
for m, t in MACHINE_TEXT.items():
    out.setdefault(m, {'fits_with': [], 'fits_models': t, 'kind': 'machine'})
    out[m]['fits_models'] = t
    out[m]['kind'] = 'machine'

json.dump(out, open('compat.json', 'w'), indent=1)
with open('compatibility.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['product_id', 'title', 'skus', 'kind', 'fits_models', 'fits_with_ids', 'fits_with_titles'])
    for pid, d in sorted(out.items(), key=lambda x: (x[1]['kind'] != 'machine', by_id[x[0]]['title'])):
        n = by_id[pid]
        w.writerow([pid, n['title'], ' '.join(v['sku'] or '' for v in n['variants']['nodes']), d['kind'], d['fits_models'], ' '.join(d['fits_with']), ' | '.join(by_id[x]['title'] for x in d['fits_with'])])
print('products with data:', len(out))
for m, lst in machine_lists.items():
    print(f"\n{by_id[m]['title']} ({len(lst)}):")
    for x in lst:
        print('   -', by_id[x]['title'])
