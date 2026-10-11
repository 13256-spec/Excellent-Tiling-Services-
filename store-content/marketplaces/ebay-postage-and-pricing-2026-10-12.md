# eBay (Marketplace Connect): charge postage and cover eBay fees

Written 12 Oct 2026 after the first eBay order (#1008, caulking sticks, $7.95 to QLD, postage $0).

## Why eBay orders arrive with free postage

Shopify's shipping rates ($15 standard, free over $180, free over $100 in WA) only run at the website
checkout. eBay listings take their postage from an **eBay postage business policy** that Marketplace Connect
assigns to each listing, and the policy in use is "free postage / Standard Parcel Delivery". The eBay price is
the Shopify price +8% (Marketplace Connect price adjustment), which doesn't cover eBay's final value fee
(about 13% of item + postage, plus 30c), let alone the postage.

Order #1008 as an example: sale $7.95, eBay fee about $1.40, Perth → QLD parcel about $11, sticks cost about
$5 → roughly $9 lost.

## Fix A: make the eBay postage policy charge $15 (phone browser, not the eBay app)

The eBay app can only pick policies, not edit them. Use Safari or Chrome in desktop mode.

1. Open https://www.ebay.com.au/bp/manage and log in.
2. If the page is cramped: Safari → tap "AA" in the address bar → "Request Desktop Website";
   Chrome → three dots → "Desktop site".
3. On "Manage business policies" find the **postage** policy the listings use (highest "Listings" count,
   currently free "Standard Parcel Delivery"). Tap **Edit**.
4. Domestic postage: cost type **Flat: same cost to all buyers**; service **Australia Post Standard**
   (Standard Parcel Delivery); cost **15.00**; each additional item **0.00**; untick **Free postage**;
   handling time 1–2 business days.
5. **Save**. eBay updates every listing that uses the policy. Repeat for any other postage policy that is free.
   Listings with a sale pending get a "Copy of …" policy and update later; that's normal.

Calculated postage (by weight and the buyer's postcode) is the more accurate option later; every parcel
product in Shopify already has a weight.

## Fix B (optional): free postage over $180, like the website

1. https://www.ebay.com.au/ship/prf → **Combined postage rules** → **Edit** → **Promotional postage rule** →
   free postage when the buyer spends $180 or more → **Save**.
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

- eBay says business policies become a Pro-plan feature from 1 December 2026; revisit before then.
- Shopify/eBay settings can't be changed through the Claude connector (Marketplace Connect has no API).
- Sources: eBay help "Business policies" (id 4212) and "Postage discounts" (id 4168); Shopify Help Center,
  Marketplace Connect → "Setting up and managing eBay listings" and "Listing and editing your products".
