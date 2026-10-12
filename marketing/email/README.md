# Customer email (Klaviyo) – what is live and what the owner still has to switch on

Updated 12 Oct 2026. Klaviyo account `WNnVDh`, sender "Excellent Tiling Services"
<contactus@excellenttilingservice.com.au>, timezone Australia/Perth. Owned by the `ets-email` agent
(`.claude/agents/ets-email.md`). Nothing here names the tile supplier.

## Why email

First 8 days of the store (4–12 Oct): 1,599 visits, 9 orders, 6 abandoned checkouts, 0 email subscribers.
The seven buyers all left the marketing box unticked. Email is the only channel that brings a visitor back
without paying for it, so the flows below run on their own; the list has to be grown by the pop-up and the
checkout opt-in (owner to-dos at the end).

## Flows (all live)

| Flow (Klaviyo id) | Who enters | What they get | Code | Stops if |
| --- | --- | --- | --- | --- |
| Welcome series `TYrj9X` | anyone who becomes subscribed to email (segment `TuL3a7`), not trade | now: "Your 10% off is inside" (WELCOME10); day 3: three ways to get it home; day 7: code reminder | WELCOME10 | they order before day 7 |
| Browse abandonment `TkVVC9` (new 12 Oct) | viewed a product (onsite metric `TgJERy`) | 2 h later: "Still thinking it over?" with the product, price, image and a tiler's-opinion offer. Once per 7 days | none | added to cart, started checkout or ordered |
| Abandoned cart `TM9NiE` | added to cart (`TrZbyk`) | 4 h later: "Still in your cart". Once per 7 days | none | started checkout or ordered |
| Abandoned checkout `VU6HcH` | started checkout (`RDzi3R`) | 1 h: "Your checkout is saved" with the items and a Finish-my-order button; 24 h: "Free postage on this order". Once per 3 days | FREEPOST | they order |
| Post-purchase `R7P79n` | placed order (`UG3gMA`) | day 2: what happens next (post, Perth delivery, pickup); day 14: Google review ask. Once per 30 days | none | |
| Repeat purchase `S9w6zL` (new 12 Oct) | placed order | day 21 at 9:30 am: "Finishing the job?" (Maxisil, trims, MELA, trade account, quote). Once per 30 days | none | they order again first |
| Win-back `VUFXf5` | ordered before, nothing in 60 days (segment `Rrg8ud`), not trade | next morning: "It's been a while. Here's 10% off" | COMEBACK10 | |
| Trade application received `Uxqmty` | Shopify tag `trade-applicant` (segment `SWneSS`) | "We've got your trade application" | | |
| Trade account approved `TK8Na9` | Shopify tag `trade` (segment `TE2xQT`) | "Your trade account is live" | | |

Already sent by 12 Oct: 3 abandoned-checkout emails, 1 abandoned-cart email (no opens yet, the flows are a day old).

## Discount codes (Shopify, email-only, created 11 Oct 2026)

| Code | What | Where it applies | Who |
| --- | --- | --- | --- |
| WELCOME10 | 10% off, one use per customer | collections `trade-list-20` (223 products) and `trade-list-25` (322): tools, trims, tapware, accessories | pop-up + welcome flow |
| COMEBACK10 | 10% off, one use per customer | same collections | win-back flow |
| FREEPOST | free standard post, orders over $60, shipping rates under $30, Australia | all products | abandoned checkout email 2 |

The two 10% codes are scoped to the products with the deepest trade band because those are the ones that
stay above the profit floor (cost × 1.1 × 1.25) at 10% off; 349 of 1,572 variants would not. Tiles,
vanities, baths and toilets are excluded on purpose. ETSWELCOME10 (an earlier $10 code) is expired.

The codes are never printed on social, Marketplace or in group replies. Social may say "sign up for 10% off
your first order of tools, trims and accessories".

## Templates (Klaviyo, CODE editor)

Library templates: Welcome 1–2, Welcome 3 (code reminder), Abandoned cart, Abandoned checkout 1–2,
Post-purchase 1–2, Trade received/approved, Browse abandonment `UGrMgA`, Repeat purchase `VthAtQ`,
Black Friday 2026 draft `WsJaAz`. Each flow holds its own copy (the id in the flow differs).

Frame: 600 px white card on `#EDEFEE`, porcelain `#F4F5F3` header band with the logo from the store CDN and a
tile-blue `#4C8ED9` rule, navy `#1F3153` headings, Arial, grey `#C3C8CC` rules, footer with address, hours,
Book-a-visit and Delivery links and `{% unsubscribe %}`. Shipping lines in every template match the live
site on 12 Oct 2026: post from $9.95, free on WA orders over $100 and Australia-wide over $150; tiles and
large items Perth delivery or free Maddington pickup. If the site's shipping changes, the templates must
change the same day.

## Segments

`TuL3a7` Email subscribers (consent = subscribed) · `TE2xQT` Trade customers (Shopify tag `trade`) ·
`SWneSS` Trade applicants · `Rrg8ud` Lapsed customers (no order in 60 days) · Klaviyo's own: Engaged 30/90
days, Potential purchasers, Repeat buyers, VIP, Churn risks.

List "Email List" `Srnmin` was double opt-in; changed to single opt-in on 12 Oct 2026 so nobody is lost at a
confirmation email. The welcome flow triggers on consent, not on the list.

## Owner to-dos (each is a few minutes in a settings page; the agents can't do these)

1. **Shopify → Klaviyo subscriber sync.** In Klaviyo: Integrations → Shopify → turn on "Sync Shopify email
   subscribers to Klaviyo" and pick "Email List". Why: the one Shopify subscriber so far
   (excellenttiling1@hotmail.com, 11 Oct) shows in Klaviyo as never subscribed, so the welcome flow has had
   nobody to send to. Until this is on, pop-up sign-ups get the code on screen but no welcome emails.
2. **Checkout opt-in box.** Shopify admin → Settings → Checkout → Marketing options → Email: tick "Show a
   sign-up option at checkout". Leave it unticked by default (Australian Spam Act wants a real yes). Every
   buyer so far was not asked.
3. **Branded sending domain.** Klaviyo → Settings → Email → Sending domains → add
   `excellenttilingservice.com.au` and paste the DNS records at the domain host. Without it, emails go out
   from a shared Klaviyo domain and land in spam more often. (Klaviyo reports no sending domain set up.)
4. **Review link.** The day-14 review email links to Google; confirm the Google Business Profile review link
   is the one in the template (`ets-community` can check).
5. **Decide on Black Friday**: `marketing/holiday-2026/ROLLOUT-PLAN.md`.

## Weekly check (Monday, `ets-analytics` + `ets-email`)

Flow report (last 7 days): recipients, clicks, orders, revenue per flow · subscribers now and added ·
abandoned checkouts started vs recovered · one change for the week.
