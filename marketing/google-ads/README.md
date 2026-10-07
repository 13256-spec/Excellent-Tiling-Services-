# Google Ads plan ($600 + $600 new-advertiser credit)

Status (7 Oct 2026): planned, not live. Nothing is spent until the owner says yes.

## The offer and its catches

- New Australian advertisers: spend $600 within 60 days of the first ad, get $600 of ad credit.
- The account must be new to Google Ads (a different business's or an old account can disqualify it).
- After the $600 is spent, Google takes up to ~35 days to check the account is new, then adds the credit.
- Check the exact terms and the credit's expiry in Google Ads > Billing > Promotions after sign-up.
- The credit only covers ad clicks. It doesn't pay for anything else and can't be cashed out.

## Is it worth it (the numbers)

- Median profit margin across the store is about 34% (MELA ~31%, Roberts Designs ~38%; from
  `store-content/pricing/store-pricing-2026-10-03.csv`).
- Break-even: every $1 of ads must bring roughly $3 of sales (ROAS 3). Below that, ads lose money.
- With the credit, the first $1,200 of clicks costs $600, so break-even for the whole test is about $1.50
  of sales per $1 of real money (~$1,800 of sales from $1,200 of ads).
- Treat it as a paid test: it tells us which products and searches sell before any more money goes in.

## Budget and timing

| Phase | Days | Daily budget | Money |
| --- | --- | --- | --- |
| 1. Qualify | 60 | $10 | $600 of the owner's money |
| (wait) | up to 35 | $10 keeps running | Google verifies the account |
| 2. Credit | ~60 | $10 | $600 credit |

Keep $10/day. Don't raise it on Google's "budget recommendations"; Google may spend up to 2x on one
day, but averages to the daily budget across the month.

## Campaigns (start small, two only)

1. **Shopping: MELA tapware and vanities** ($6/day). Products show with photo and price in Google.
   - Link the store with the Google & YouTube app in Shopify (free). It creates Merchant Center and
     sends the product feed, and installs purchase tracking.
   - Use a *Standard Shopping* campaign if offered, so we can see which products and searches spend money.
     If only Performance Max is offered, limit it to the Shopping feed and exclude brand terms.
   - Leave out products under ~$60: a click costs too much for the profit on them.
2. **Search: Perth local** ($4/day). Text ads for people near Maddington ready to buy.
   - Keywords (phrase match): "tile shop perth", "tiles maddington", "bathroom vanity perth",
     "tiling tools perth", "tile shop near me", "bathroom tapware perth", "tiler perth", "bathroom tiler perth".
   - Negative keywords from day one: free, jobs, job, course, apprentice, salary, diy video, youtube,
     second hand, used, gumtree, bunnings, ikea, reece, beaumont, how to, wikipedia.

## Settings that waste money if left on (turn them off)

- Search partners: off. Display network expansion: off.
- Locations: Perth metro (or 40 km around Maddington), option "Presence: people in or regularly in
  your locations", NOT "interest in".
- Auto-apply recommendations: off (Google Ads > Recommendations > Auto-apply).
- Don't start with a Smart campaign or "Express" setup; they hide the search terms.
- Bidding: start "Maximise clicks" with a $2.50 max CPC limit. After 15+ sales, switch to
  "Maximise conversion value" or "Target ROAS 300%".

## Tracking (must work before the first dollar)

- Purchases: Google & YouTube app in Shopify (check "Conversion tracking: active").
- Phone calls from ads: add a call asset with 0450 960 543 and count calls over 60 seconds.
- Link Google Business Profile (shows the address and reviews on ads).
- Test: place a real order and check it shows in Google Ads > Goals > Conversions within 24 hours.

## Weekly check (every Monday, 10 minutes)

1. Search terms report: add any junk search as a negative keyword.
2. Products/keywords that spent more than $30 with no sale: pause.
3. Spend vs sales (ROAS) for each campaign. Move money to whatever is above 3.
4. Day 30: if no sales at all, stop and fix the product pages or tracking before spending more.

## Ad text (to be checked by ets-copy-review before use)

- Headlines: "Perth Tile Shop, Maddington", "MELA Tapware, Prices Online", "Bathroom Vanities in Stock",
  "Free Pickup in Maddington", "Evening Showroom, Mon to Sat", "Perth Tilers Since <year>"
- Descriptions: "Every price is on the website. Order online and pick up free in Maddington.",
  "Showroom open 4:30 to 9 pm, Monday to Saturday, by appointment. Call 0450 960 543."
- Same rules as social: never name the tile supplier, no "cheaper than" claims.
