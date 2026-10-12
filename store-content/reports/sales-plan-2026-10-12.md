# Where the sales are coming from, and what to do next (12 Oct 2026)

Written for the owner after the question "what can we work on, we need more sales". Numbers are the 30 days to
12 Oct 2026 from Shopify Analytics, Google Analytics 4 (property 556035910), Google Ads (account 6204790591),
Google Merchant Center (5858979511) and Klaviyo.

## The numbers

| | 30 days to 12 Oct |
|---|---|
| Visits Shopify counts | 1,505 (about 800 of them are bots from one US data centre, "Iowa") |
| Real visits (Google Analytics, bots removed) | about 320, so roughly 10 a day |
| Orders | 8, first one 4 Oct, $685 in total, average $80 |
| Orders that came from Google | 6 of 8 (4 from the paid Shopping campaign, 2 from free search results) |
| Orders from Instagram, Facebook, YouTube | 0 from 84 visits (average visit 11 seconds) |
| Orders from email | 0 (12 people on the list, no new sign-ups: the sign-up offer theme is still a draft) |
| Checkouts started vs finished | about 1 in 6 finishes (41 started, 7 finished in the best week) |
| Google Ads since 7 Oct | $64.60 spent, 193 clicks, 3 sales worth $375.71 |
| Google Ads spent outside Australia | $30.29 of the $64.60 (NZ $18.68, USA $8.89, UAE $1.96, UK $0.76): 0 sales |
| Google Shopping listings | 4,828 variants approved for Australia; the only rejections are in the UAE feed |
| What Google sends people to | product pages: Maxisil silicone (natural stone, wet area, pool), square grate floor wastes, Sigma cutter parts, Maxigrab, backer rod, Panther clips, X spacers |

What this says: the shop converts fine when a buyer with a product in mind arrives from Google (about 2.5 in 100
Google visitors buy). The problem is volume: too few of those visitors, and nearly half the ad money is going to
countries that don't buy.

## Done today (no owner action needed)

1. **Brand pages.** Google was already sending brand searches (Maxisil, Sigma, Roberts Designs floor wastes) to single
   product pages, but the shop had no brand pages. Nine smart collections now exist, each with a search title, meta
   description and a short plain description with the right delivery rule:
   `/collections/maxisil` (22 products), `/collections/sigma` (56), `/collections/raimondi` (223), `/collections/bat-tools` (145),
   `/collections/bat-trims` (48), `/collections/roberts-designs` (142), `/collections/panther` (14), `/collections/baron` (10),
   `/collections/mela` (178). They fill themselves by vendor (Baron also by title), so new products land in them automatically.
2. **Menu.** Seven of them (Maxisil, Sigma, Raimondi, BAT tools, BAT trims, Roberts Designs, Baron) are now links in the
   Hardware dropdown of `main-menu-2026` (the live header) and `main-menu`, after "Floor drains & wastes". The dropdown
   lists them as text links, the same as the existing items.

## For the owner: five minutes each, in order of money

1. **Stop the ad spend leaking overseas (biggest).** ads.google.com → Campaigns → "ETS | AU + NZ | Shopping" →
   Settings → Locations: remove New Zealand (48 clicks, $18.68, no sales; postage to NZ kills the sale) → open
   "Location options" → choose **"Presence: People in or regularly in your targeted locations"** (today it also shows
   ads to people merely *interested* in Australia, which is where the US, UAE and UK clicks come from) → Save.
   Then Goals → Conversions → Summary → **"Local actions – Directions"** → Edit settings → set to **Secondary** →
   Save, so Google optimises for purchases, not map clicks. Leave the budget at $30 a day; it only spends about $13
   now, and after this change the whole amount reaches Australian shoppers. Give it two weeks before judging it.
2. **Publish the sign-up offer theme.** Online Store → Themes → "ETS 2026 – 10% sign-up offer (draft 11 Oct)" → ⋯ →
   Publish. It is a copy of the live theme plus the footer box and pop-up that promise 10% off and show WELCOME10.
   Without it the welcome emails never get anyone to send to. Then sign up yourself with a fresh address to see the
   first email arrive.
3. **Connect Google Search Console** so we can see which searches bring people and ask Google to index new pages.
   search.google.com/search-console → Add property → **URL prefix** → `https://excellenttilingservice.com.au/` →
   verify with **Google Analytics** (same Google login as the ads) → Verify. Then in HYPD (the analytics tool) →
   Connect → Ad Platforms → Google Search Console.
4. **eBay postage.** Order #1008 (caulking sticks, $7.95 to Queensland) shipped free and lost about $9. Every eBay
   sale under about $20 loses money until the postage policies are fixed. Steps:
   `store-content/marketplaces/ebay-postage-and-pricing-2026-10-12.md`. If there's no time this week, pause the eBay
   listings in Marketplace Connect instead.
5. **Reviews.** The product pages show no reviews (the fake ones were removed on 5 Oct). Install the free plan of
   Judge.me (Apps → Shopify App Store → "Judge.me Product Reviews" → Install) and the next session will place the
   review stars on product pages in a draft theme and turn on the review-request email. Real reviews lift conversion more
   than anything else on the page.

Two decisions that need a yes or no (not done, they change what customers pay):

- **Cheaper postage for small items.** Today a $15 tube of Maxisil costs $15 to post. Australia Post's small satchel
  (up to 500 g) costs about $10 through MyPost Business. A $9.95 rate for carts under 500 g would make the most-searched
  products (silicone, cleaner, spacers, caulking sticks) buyable. Say yes and it goes into Settings → Shipping as a
  weight tier on the General and Dangerous goods profiles; free over $100 in WA and over $180 elsewhere stay.
- **Pickup lead time.** Checkout promises pickup "in 2 to 4 days", by appointment. A Perth tiler who needs it tomorrow
  goes to Bunnings. If orders can be packed by the next evening, change it to "Usually ready in 24 hours"
  (Settings → Shipping and delivery → Local pickup → Maddington → Expected pickup time).

## Next for the agents (no decision needed)

- Weekly: Google Ads results by country and product, Merchant Center rejections, the `monitor_competitors.py` price
  check, Klaviyo flow numbers (`ets-analytics`, `ets-pricing`).
- Once Search Console is connected: short, factual help articles for the searches that already bring buyers (Maxisil
  colour guide, choosing a floor waste outlet size, Sigma cutter sizes and spare parts) that link to the brand pages.
- Home page speed: 630 KB of HTML and 28 render-blocking scripts; 5 of 7 web orders came from phones. Trim the
  mega-menu product cards and app scripts in a draft theme, measure before and after.
- Black Friday proposal by Sat 8 Nov (`marketing/rollout-2026-10-11.md`).
- Trade outreach: one approved trade account so far. A plain email and the public trade price list to Perth tiling,
  plumbing and building firms is the fastest route to repeat orders; proposal to follow.

## Not worth time right now

- Social posting as a sales channel: 84 visits, 0 sales, 11-second visits. Keep the calendar going for the brand, but
  don't expect orders from it this month.
- The 121 Merchant Center rejections: they are the UAE feed only (image error on the BAT 316 stainless angle, one
  price mismatch on a linear drain); the Australian listings for the same products are approved.
