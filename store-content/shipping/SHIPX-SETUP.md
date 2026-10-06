# Shipx rules to enter (Roberts Designs products) — 6 Oct 2026

Checkout uses one rate source: the **Shipx – Shipping Rates & Rules** app (General profile, zone Global: AU, NZ, US, GB, AE).
Its rules can only be changed inside the app (Shopify admin → Apps → Shipx). Everything Shipx needs is now on the products:

| On the product | What it is |
| --- | --- |
| Weight (every variant) | Packed weight, estimated (Roberts publishes none) |
| Metafield `shipping.box_size` (every variant) | Packed box, e.g. "35 x 15 x 8 cm" |
| Tag `ship-parcel` (215 products) | Fits Australia Post: up to 22 kg, 105 cm longest side |
| Tag `ship-long` (33 products) | Over 105 cm (2.5 m / 3 m trims, cutters 95 cm+, extension pole, floor scraper). Australia Post won't take these |
| Tag `ship-freight` (11 products) | Baron mixers and heads, Sigma tables and workbench, Kera Cut, Kera Lift |
| Tag `ship-bulky` (15 products) | Light but big box: Australia Post charges cubic weight (buckets, niche boxes, mixers, rollers, backer rod) |
| Tag `ship-dangerous-goods` (4 products) | Maxisil Primers 1215, 1216, 1217, 1218: road only, no Express Post, no overseas |

## Problems found at checkout today
- Every state pays the same price (1.2–2.3 kg items are $24.45 to Perth, Sydney and Darwin alike).
- Maxisil grout 5 kg and 10 kg get **no shipping option at all**, even in Perth.
- Some light parcels (Sigma support arm 1.8 kg, Sigma measuring bar 2 kg) get no option, or only Perth delivery.

## Rules to set, in this order

**1. Freight items** — condition: product tag is `ship-freight`
- Show only: Perth local delivery (your local delivery price) and free pickup from Maddington.
- Hide all parcel and international rates. Customers outside Perth should contact the shop for a freight quote.

**2. Long items** — condition: product tag is `ship-long`
- Show only: Perth local delivery and pickup.
- Hide parcel and international rates.
- Linear drains have short and long sizes, so they carry both tags. If Shipx can use SKUs, apply this rule only to the
  long (1200 mm and 1500 mm) SKUs and let the 800 / 900 mm sizes use the parcel rule:
  RDXD1075 RDXD1052 RDXD1076 RDXD1053 RDXD1071 RDXD1057 RDXD1072 RDXD1058 RDXD1091 RDXD1087 RDXD1092 RDXD1088
  RDXD1095 RDXD1067 RDXD1063 RDXD1068 RDXD1064 RDXD1098 RDXD1083 RDXD1079 RDXD1099 RDXD1084 RDXD1080

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

**5. Parcels overseas** — condition: product tag is `ship-parcel` and NOT `ship-dangerous-goods`, by cart weight, up to 10 kg

| Cart weight | New Zealand | US, UK, UAE |
| --- | --- | --- |
| up to 0.99 kg | $29 | $45 |
| 1 to 1.99 kg | $39 | $65 |
| 2 to 2.99 kg | $49 | $85 |
| 3 to 4.99 kg | $65 | $119 |
| 5 to 6.99 kg | $85 | $149 |
| 7 to 10 kg | $109 | $189 |

Over 10 kg: no rate (contact the shop).

## After saving the rules — test these carts (Sydney 2000, Darwin 0800, Perth 6109, Auckland)
| Cart | Should show |
| --- | --- |
| Smoothtex A 250 ml (0.35 kg) | AU $15; NZ $29; US/UK/UAE $45 |
| Maxisil grout 10 kg | AU $59 (WA too); no overseas rate |
| Sigma measuring bar (1.5 kg) | AU $20 |
| L Shape Aluminium Trim 3 m | Perth delivery / pickup only |
| Baron E120 mixer | Perth delivery / pickup only |
| Maxisil Primer 1218 | AU Parcel Post only; nothing overseas |
| Any cart $1,000+ in Australia | Free |

Then tell me Shipx is done and I'll set the Roberts products back to Active (list in `roberts-ready-to-publish.txt`)
and re-run these tests.
