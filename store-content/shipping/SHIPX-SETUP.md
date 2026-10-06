# Shipx setup — Australia Post only (6 Oct 2026)

Owner's decision: **Australia Post only for now** (no FedEx). Parcels go Australia Post anywhere in Australia and
Australia Post International to NZ, US, UK and UAE. Anything Australia Post can't take is **Perth delivery or pickup only**.

Checkout uses the **ShipX – Shipping Rates & Rules** app (Shopify admin → Apps → ShipX). Its rules can only be changed
inside the app. The products are ready for it:

| On the product | Meaning |
| --- | --- |
| Weight (every variant) | Packed weight (estimated) |
| Metafield `shipping.box_size` (every Roberts variant) | Packed box, e.g. "35 x 15 x 8 cm" |
| Tag `ship-parcel` (215 Roberts products) | Fits Australia Post (up to 22 kg, 105 cm longest side) |
| Tag `ship-local-only` (39 products) | Australia Post can't take it: 3 m and 2.5 m trims, Sigma cutters 95 cm+, Baron mixers and heads, Sigma tables, Kera Cut / Lift, extension pole, floor scraper |
| Tag `ship-dangerous-goods` (4) | Maxisil Primers 1215–1218: road only, no Express, nothing overseas |
| Tag `ship-bulky` (15) | Big box for its weight (buckets, niche boxes, mixers, rollers, backer rod) |

Linear drains (5 products) come in parcel sizes (800 / 900 mm) and long sizes (1200 / 1500 mm), so they are **not**
tagged local-only. The long SKUs are listed in step 3.

## Step 1 — Check Australia Post is connected in ShipX
ShipX already shows "AUS PARCEL REGULAR – Parcel Post" and "AUS PARCEL EXPRESS – Express Post" at checkout, so an
Australia Post connection exists. In ShipX → Carriers, check it is **your MyPost Business account** and that the
ship-from address is Maddington WA 6109. Turn off any FedEx/UPS/other carriers.

## Step 2 — Rule: Perth only (top of the list)
- Condition: cart contains a product tagged `ship-local-only`.
- Rates shown: **Perth local delivery** (your local delivery price) and **Pickup from Maddington** only.
- Hide all Australia Post and international rates.

## Step 3 — Rule: long linear drains (if ShipX can use SKUs)
- Condition: cart contains any of these SKUs (1200 / 1500 mm drains):
  RDXD1075 RDXD1052 RDXD1076 RDXD1053 RDXD1071 RDXD1057 RDXD1072 RDXD1058 RDXD1091 RDXD1087 RDXD1092 RDXD1088
  RDXD1095 RDXD1067 RDXD1063 RDXD1068 RDXD1064 RDXD1098 RDXD1083 RDXD1079 RDXD1099 RDXD1084 RDXD1080
- Same as step 2: Perth delivery / pickup only.

## Step 4 — Rule: dangerous goods
- Condition: cart contains a product tagged `ship-dangerous-goods`.
- Australia only, **Parcel Post only** (no Express Post), no overseas rates.

## Step 5 — Rule: Australia (all states, WA included), by cart weight
Apply to every cart going to Australia that isn't caught by step 2 or 3. Don't require a tag here, so products
without tags still get a price.

| Cart weight | Price |
| --- | --- |
| up to 1 kg | $15 |
| 1 to 3 kg | $20 |
| 3 to 5 kg | $29 |
| 5 to 10 kg | $39 |
| 10 to 22 kg | $59 |
| 22 to 44 kg (2 boxes) | $109 |
| 44 to 100 kg (3–4 boxes) | $179 |
| Order $1,000 or more | Free |

Option instead of the table: **live Australia Post rates** from your MyPost Business account, using product weights
(and box sizes if ShipX can read the `shipping.box_size` metafield). Live rates charge by zone and by box size; the
table is simpler and is what the site and policy say ("from $15, free over $1,000"). If you use the table, add about
**+$15 for `ship-bulky`** items (Australia Post charges these by box size).

## Step 6 — Rule: overseas (NZ, US, UK, UAE) — Australia Post International
- Condition: country is not Australia, and the cart has no `ship-local-only` or `ship-dangerous-goods` product.
- By cart weight, up to 10 kg:

| Cart weight | New Zealand | US, UK, UAE |
| --- | --- | --- |
| up to 0.99 kg | $29 | $45 |
| 1 to 1.99 kg | $39 | $65 |
| 2 to 2.99 kg | $49 | $85 |
| 3 to 4.99 kg | $65 | $119 |
| 5 to 6.99 kg | $85 | $149 |
| 7 to 10 kg | $109 | $189 |

- Over 10 kg: no rate (customer contacts the shop). No free shipping overseas.

## Step 7 — Tell me, and I test
Once saved, tell me. I'll test these carts and then publish the 138 Roberts products:

| Cart | Should show |
| --- | --- |
| Smoothtex A 250 ml (0.35 kg) to Sydney | $15 Australia Post |
| Smoothtex A 250 ml to Auckland | $29 Australia Post International |
| Maxisil grout 10 kg to Darwin | $59 |
| Sigma measuring bar (1.5 kg) to Perth | $20 |
| L Shape Aluminium Trim 3 m | Perth delivery / pickup only |
| Baron E120 mixer | Perth delivery / pickup only |
| Maxisil Primer 1218 to Melbourne | Parcel Post only; nothing to Auckland |
| Any cart $1,000+ in Australia | Free |

## Not covered yet
The other live products (about 48 tiles and 8 BAT / RLA / Click items) have weights but no tags or box sizes. Under
step 5 they'd get the weight price; tiles (about 22 kg per m²) should probably be `ship-local-only`. Ask Claude to
tag them before switching the rules on.
