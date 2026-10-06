> **Out of date (6 Oct 2026):** ShipX was replaced by Shopify's built-in shipping profiles. See README "Moved off ShipX".

# ShipX — click by click (Australia Post only)

**Use the "Scenarios" box → Create.** You make 5 scenarios, one at a time.
Don't use "Combined shipping rates" or "Nested" (that one is a paid add-on). You don't need them.

Pickup is NOT set up in ShipX. Shopify's own Local pickup already shows on every order.

Tags are already on every product. You only type them in.

---

## Scenario 1 — Perth only (big items)
**Name:** Perth only

**Conditions** (match ANY of these):
- Product tag **contains** `ship-local-only`
- (if ShipX lets you use SKUs) SKU is one of the big sizes in SHIPX-SETUP.md step 3 (long drains, big mirrors, PORTER cabinets, 20 L acid)

**Plus:** Country = Australia, postcode 6000 to 6199 (Perth metro)

**Rates:**
| Rate name | Price |
| --- | --- |
| Perth local delivery (within 30 km) | $130 |

Turn on **"hide other rates"** / **"stop other scenarios"** if you see it.
Customers outside Perth with these items see no delivery price, only Pickup. That's correct.

---

## Scenario 2 — Dangerous goods (primers, acid)
**Name:** Dangerous goods

**Conditions:** Product tag **contains** `ship-dangerous-goods` AND Country = Australia

**Rates:** one rate called **Australia Post Parcel Post (road)**, by cart weight, using the same prices as Scenario 3 below. No Express Post.

Turn on **"hide other rates"** if you see it.

---

## Scenario 3 — Australia Post (everything else)
**Name:** Australia Post

**Conditions:** Country = Australia AND cart does **not** contain tag `ship-local-only` AND does **not** contain `ship-dangerous-goods`

**Rate name:** Australia Post Standard. Rate type: **by cart weight**

| From kg | To kg | Price |
| --- | --- | --- |
| 0 | 1 | $15 |
| 1 | 3 | $20 |
| 3 | 5 | $29 |
| 5 | 10 | $39 |
| 10 | 22 | $59 |
| 22 | 44 | $109 |
| 44 | 100 | $179 |

**Free shipping:** cart total $1,000 or more → $0

---

## Scenario 4 — New Zealand
**Name:** NZ

**Conditions:** Country = New Zealand AND no tag `ship-local-only` AND no tag `ship-dangerous-goods`

**Rate name:** Australia Post International. **By cart weight:**

| From kg | To kg | Price |
| --- | --- | --- |
| 0 | 1 | $29 |
| 1 | 2 | $39 |
| 2 | 3 | $49 |
| 3 | 5 | $65 |
| 5 | 7 | $85 |
| 7 | 10 | $109 |

Over 10 kg: no rate. No free shipping.

---

## Scenario 5 — US, UK, UAE
**Name:** International

**Conditions:** Country = United States, United Kingdom or United Arab Emirates AND no tag `ship-local-only` AND no tag `ship-dangerous-goods`

**Rate name:** Australia Post International. **By cart weight:**

| From kg | To kg | Price |
| --- | --- | --- |
| 0 | 1 | $45 |
| 1 | 2 | $65 |
| 2 | 3 | $85 |
| 3 | 5 | $119 |
| 5 | 7 | $149 |
| 7 | 10 | $189 |

Over 10 kg: no rate. No free shipping.

---

## Order (top to bottom)
1. Perth only
2. Dangerous goods
3. Australia Post
4. NZ
5. International

Delete or turn off any old ShipX scenarios (the old flat $11.70 / $24.45 ones), so they don't mix in.

## Later (optional)
- Bulky items (`ship-bulky`): add $15. Do this only after the 5 above work.
- Pickup booking app (Pick Easy): only if you want booking times.

**Stuck on a screen?** Send me a screenshot and I'll tell you what to click.
When all 5 are saved, tell me and I'll test them.
