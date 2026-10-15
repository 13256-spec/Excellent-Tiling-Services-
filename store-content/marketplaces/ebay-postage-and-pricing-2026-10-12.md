# eBay (Marketplace Connect): charge postage and cover eBay fees

Written 12 Oct 2026 after the first eBay order (#1008, caulking sticks, $7.95 to QLD, postage $0).

## Why eBay orders arrive with free postage

Shopify's shipping rates ($15 standard, free over $150, free over $100 in WA) only run at the website
checkout. eBay listings take their postage from an **eBay postage business policy** that Marketplace Connect
assigns to each listing, and the policy in use is "free postage / Standard Parcel Delivery". The eBay price is
the Shopify price +8% (Marketplace Connect price adjustment), which doesn't cover eBay's final value fee
(about 13% of item + postage, plus 30c), let alone the postage.

Order #1008 as an example: sale $7.95, eBay fee about $1.40, Perth → QLD parcel about $11, sticks cost about
$5 → roughly $9 lost.

## Fix A: charge the same postage as the website (five eBay postage policies)

The website charges Australia Post by total weight, the same table for WA and the other states (General and
Dangerous goods profiles), free over $150 anywhere and free over $100 in WA:

| Weight | Website postage | eBay policy to create | Shopify tag (added 12 Oct) | Products |
|---|---|---|---|---|
| up to 1 kg | $15 | ETS Post A – up to 1 kg – $15 | `ebay-post-15` | 410 |
| 1 to 3 kg | $20 | ETS Post B – 1 to 3 kg – $20 | `ebay-post-20` | 164 |
| 3 to 5 kg | $29 | ETS Post C – 3 to 5 kg – $29 | `ebay-post-29` | 40 |
| 5 to 10 kg | $39 | ETS Post D – 5 to 10 kg – $39 | `ebay-post-39` | 67 |
| 10 to 22 kg | $59 | ETS Post E – 10 to 22 kg – $59 | `ebay-post-59` | 27 |

Every parcel product (708, General and Dangerous goods profiles) now carries one of these tags, chosen by its
heaviest variant (60 products have variants in more than one tier; the heaviest wins so postage is never short).
eBay can't do weight tiers inside one policy and calculated postage needs package dimensions Shopify doesn't send,
so one flat policy per tier is the way to mirror the website. eBay also can't give WA a different free threshold,
so eBay gets free postage over $150 only.

### A1. Create the five policies on eBay (phone browser in desktop mode, not the eBay app)

1. Open https://www.ebay.com.au/bp/manage and log in. Safari: tap "AA" → "Request Desktop Website";
   Chrome: three dots → "Desktop site".
2. First fix the existing free policy ("Standard Parcel Delivery", the one with the most listings): **Edit** →
   Domestic postage: **Flat: same cost to all buyers**, service **Australia Post Standard** (Standard Parcel
   Delivery), cost **15.00**, each additional item **0.00**, untick **Free postage**, handling time 2 business days,
   **no international postage** → rename it "ETS Post A – up to 1 kg – $15" → **Save**. Every listing now charges
   $15 from this moment; the heavier ones get their own policy in A3.
3. **Create policy** → **Postage** → name "ETS Post B – 1 to 3 kg – $20", same settings with cost **20.00** → **Save**.
   Repeat for C ($29), D ($39) and E ($59).

### A2. Free postage over $150, like the website

1. https://www.ebay.com.au/ship/prf → **Combined postage rules** → **Edit** → **Promotional postage rule** →
   free postage when the buyer spends $150 or more → **Save**.
2. Back at https://www.ebay.com.au/bp/manage, open each of the five policies → **Combined postage discounts** →
   tick the promotional rule → **Save**.

### A3. Put each listing on the right policy (Shopify app)

Shopify → **Apps** → **Marketplace Connect** → **Listings** → marketplaces drop-down → **eBay** → **Bulk edit**.
1. **Filters** → **Tag** → `ebay-post-20` → select all → **Columns** → add the eBay shipping/postage policy column →
   choose "ETS Post B – 1 to 3 kg – $20" → **Update** → **Save**.
2. Repeat with tag `ebay-post-29` → policy C, `ebay-post-39` → policy D, `ebay-post-59` → policy E.
3. `ebay-post-15` products already use policy A (the edited one), nothing to do.
4. **Settings** → **Accounts** → eBay → **New listings** → **Manage** → **Shipping**: set policy A as the default for
   future listings, and remember to move heavier new products to B–E by their tag.

## Fix B (optional): free postage over $150, like the website

1. https://www.ebay.com.au/ship/prf → **Combined postage rules** → **Edit** → **Promotional postage rule** →
   free postage when the buyer spends $150 or more → **Save**.
2. https://www.ebay.com.au/bp/manage → open the postage policy → **Combined postage discounts** → tick the
   rule → **Save**.

## Fix C: lift the eBay price adjustment to cover fees (Shopify app)

1. Shopify → **Apps** → **Marketplace Connect** → **Settings** → **Accounts** → the eBay account →
   **New listings** → **Manage** → **Adjustments** → **Price** → **Edit** → increase by **15%** → **Save** → **Save**.
   This only changes future listings.
2. Existing listings: **Listings** → marketplaces drop-down → **eBay** → **Bulk edit** → select all →
   **Columns** → add the price column → set Shopify price +15% → **Update** → **Save**.

## Fix D: keep Perth-only items off eBay

**Listings** → **eBay** → **Bulk edit** → **Filters** → **Tag** = `ship-local-only` (tiles) and the vanities,
baths, toilets → select all → set to not listed → **Save**. These are Perth delivery or pickup only.

## Notes

- 12 Oct 2026, later: the website now charges $9.95 up to 250 g and $11.95 up to 500 g (and $24.95 for 3–5 kg). The eBay policies
  above keep $15 as the minimum on purpose: eBay's final value fee (about 13% of item + postage) eats the difference, and the
  `ebay-post-15` tag already covers every product under 1 kg. Add an "ETS Post A0 – up to 500 g – $11.95" policy later only if light
  items sell on eBay in volume.

- eBay says business policies become a Pro-plan feature from 1 December 2026; revisit before then.
- Shopify/eBay settings can't be changed through the Claude connector (Marketplace Connect has no API).
- Sources: eBay help "Business policies" (id 4212) and "Postage discounts" (id 4168); Shopify Help Center,
  Marketplace Connect → "Setting up and managing eBay listings" and "Listing and editing your products".
