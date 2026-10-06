# Shipx rules to enter (Roberts Designs products) — 6 Oct 2026

Checkout uses one rate source: the **Shipx – Shipping Rates & Rules** app (General profile, zone Global: AU, NZ, US, GB, AE).
Its rules can only be changed inside the app (Shopify admin → Apps → Shipx). Everything Shipx needs is now on the products:

| On the product | What it is |
| --- | --- |
| Weight (every variant) | Packed weight, estimated (Roberts publishes none) |
| Metafield `shipping.box_size` (every variant) | Packed box, e.g. "35 x 15 x 8 cm" |
| Tag `ship-parcel` (215 products) | Fits Australia Post: up to 22 kg, 105 cm longest side |
| Tag `ship-long` (33 products) | Over 105 cm (2.5 m / 3 m trims, cutters 95 cm+, extension pole, floor scraper). Australia Post won't take these |
| Tag `ship-fedex` (44 products) | Goes by FedEx (owner, 6 Oct: anything Australia Post can't take) = all `ship-long` + `ship-freight` |
| Tag `ship-fedex-freight` (26 products) | Too big even for a FedEx parcel (over 274 cm or over 68 kg): 3 m trims, Baron mixers, Sigma tables, Kera Cut / Lift |
| Tag `ship-freight` (11 products) | Baron mixers and heads, Sigma tables and workbench, Kera Cut, Kera Lift |
| Tag `ship-bulky` (15 products) | Light but big box: Australia Post charges cubic weight (buckets, niche boxes, mixers, rollers, backer rod) |
| Tag `ship-dangerous-goods` (4 products) | Maxisil Primers 1215, 1216, 1217, 1218: road only, no Express Post, no overseas |

## Problems found at checkout today
- Every state pays the same price (1.2–2.3 kg items are $24.45 to Perth, Sydney and Darwin alike).
- Maxisil grout 5 kg and 10 kg get **no shipping option at all**, even in Perth.
- Some light parcels (Sigma support arm 1.8 kg, Sigma measuring bar 2 kg) get no option, or only Perth delivery.

## Rules to set, in this order

**1. FedEx items (anything Australia Post can't take)** — condition: product tag is `ship-fedex` (44 products)
- Rate: FedEx. If Shipx can connect your FedEx account, use live FedEx rates with the `shipping.box_size` metafield
  for dimensions. If not, use a fixed FedEx price table by cart weight (get it from your FedEx account rate card).
- Also show Perth local delivery and pickup from Maddington.
- Hide Australia Post rates for these items.
- Two kinds:
  - `ship-fedex` only (18 products): fit a FedEx parcel (up to 68 kg, 274 cm long, length + girth 330 cm). Linear
    drains 1200/1500 mm, 2.5 m PVC and stair trims, Sigma cutters 95 cm and up, Baron mixer heads, extension pole,
    floor scraper.
  - `ship-fedex-freight` (26 products): too big for a FedEx parcel, so they need FedEx freight (pallet or long-freight
    booking): every **3 m trim** (305 cm box, over FedEx's 274 cm parcel limit), Baron E120/F200/F300 mixers, Sigma
    table and workbench, Kera Cut 332 cm, Kera Lift. If Shipx can't price FedEx freight, show "Freight – we'll
    contact you with a quote" or Perth delivery / pickup only.
- Linear drains have short and long sizes. If Shipx can use SKUs, apply FedEx only to the long (1200 / 1500 mm)
  SKUs and let 800 / 900 mm use the Australia Post rule:
  RDXD1075 RDXD1052 RDXD1076 RDXD1053 RDXD1071 RDXD1057 RDXD1072 RDXD1058 RDXD1091 RDXD1087 RDXD1092 RDXD1088
  RDXD1095 RDXD1067 RDXD1063 RDXD1068 RDXD1064 RDXD1098 RDXD1083 RDXD1079 RDXD1099 RDXD1084 RDXD1080
- Overseas: see rule 5 (FedEx International for everything that can go overseas).

**2. (removed — long and freight items are both covered by the FedEx rule above)**

**3. Dangerous goods** — condition: product tag is `ship-dangerous-goods`
- Australia only, Parcel Post (road). Hide Express Post and every overseas rate.

**4. Parcels in Australia** — condition: product tag is `ship-parcel`, country Australia, by cart weight
(your prices from 5 Oct, all states including WA):

| Cart weight | Price |
| --- | --- |
| up to 1 kg | $15 |
| 1 to 3 kg | $20 |
| 3 to 5 kg | $29 |
| 5 to 10 kg | $39 |
| 10 to 22 kg | $59 |
| 22 to 44 kg (2 boxes) | $109 |
| 44 to 100 kg (3–4 boxes) | $179 |
| order $1,000 or more | Free |

If Shipx can use live Australia Post prices with product dimensions, use those instead and point it at the
`shipping.box_size` metafield. Otherwise add a surcharge for `ship-bulky` (about +$15), because Australia Post charges these
by box size (the 20 L bucket is charged as about 12 kg and the SIRI Eco Roller bucket as about 26 kg).

**5. Overseas (NZ, US, UK, UAE): FedEx International only** (owner, 6 Oct 2026)
- Condition: country is not Australia. Hide **all** Australia Post rates (Parcel Post, Express, MyPost International).
- Only FedEx International. Best: live FedEx rates from your FedEx account, using item weight and the
  `shipping.box_size` metafield. If Shipx can't do live FedEx, use this fixed table (your 5 Oct overseas prices) and
  check it against your first real FedEx invoices:

| Cart weight | New Zealand | US, UK, UAE |
| --- | --- | --- |
| up to 0.99 kg | $29 | $45 |
| 1 to 1.99 kg | $39 | $65 |
| 2 to 2.99 kg | $49 | $85 |
| 3 to 4.99 kg | $65 | $119 |
| 5 to 6.99 kg | $85 | $149 |
| 7 to 10 kg | $109 | $189 |

- Over 10 kg: live FedEx rate, or "contact us for a quote".
- No overseas rate for `ship-dangerous-goods` (primers can't fly) or `ship-fedex-freight` (3 m trims, Baron mixers,
  Sigma tables, Kera Cut / Lift).
- Customs: FedEx needs a commercial invoice (item description, value, HS code) on every overseas shipment.

## After saving the rules — test these carts (Sydney 2000, Darwin 0800, Perth 6109, Auckland)
| Cart | Should show |
| --- | --- |
| Smoothtex A 250 ml (0.35 kg) | AU $15 (Australia Post); NZ and US/UK/UAE: FedEx only, no Australia Post option |
| Maxisil grout 10 kg | AU $59 (WA too); no overseas rate |
| Sigma measuring bar (1.5 kg) | AU $20 |
| L Shape Aluminium Trim 3 m | FedEx freight (or quote), Perth delivery, pickup — no Australia Post |
| Sigma Tile Cutter ART 4EN 125 cm | FedEx rate, no Australia Post |
| Baron E120 mixer | FedEx freight (or quote), Perth delivery, pickup |
| Maxisil Primer 1218 | AU Parcel Post only; nothing overseas |
| Any cart $1,000+ in Australia | Free |

Then tell me Shipx is done and I'll set the Roberts products back to Active (list in `roberts-ready-to-publish.txt`)
and re-run these tests.
