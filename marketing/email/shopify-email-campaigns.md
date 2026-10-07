# Shopify Email: automations and campaigns (8 Oct 2026)

Shopify has no API for Shopify Email, so these are set up in Shopify admin → **Marketing**.
Each email uses the **ETS brand**: logo at the top, navy buttons `#15213A`, brass accents `#9C7744`,
cream background `#F6F4EF`. Set these once under Marketing → Automations/Campaigns → any email →
**Edit** → **Theme settings** (logo, colours, font: Arial/Helvetica), then they apply to every email.

Rules for every email (owner and copy-review rules):
- No discount codes. The owner decided not to run one (5 Oct 2026); propose one only if he asks.
- Don't quote shipping prices or free-shipping thresholds. Use: "We deliver, or pick up free in Maddington. Shipping options show at checkout."
- Never name the tile supplier. MELA can be named.
- Prices must match the live store on the day the email goes out. Prices below are from 8 Oct 2026.
- One clear next step per email. Max one exclamation mark.

The store has only 2 real customers so far, so the **automations** matter most: they run by
themselves for every new customer from now on. Turn them on first.

---

## Automations (Marketing → Automations → Create automation)

### 1. Abandoned checkout (template: "Recover abandoned checkout")
Send 4 hours after the checkout is abandoned. One email.

- **Subject:** Your items are saved
- **Preview text:** Finish your order when you're ready, or ask us first.
- **Heading:** Still planning your project?
- **Body:** Your items are still in your cart. If you're unsure about sizes, quantities or finishes, call or text 0450 960 543. You'll be talking to a Perth tiling team, not a call centre. You can also see products in person at our Maddington showroom, by appointment, Monday to Saturday, 4:30 to 9 pm.
- **Button:** Finish my order

(Also paste `store-content/notifications/emails/abandoned-checkout.liquid` into the Abandoned checkout notification, so the default Shopify email matches.)

### 2. Welcome new subscriber (template: "Welcome new subscribers")
Send straight after someone subscribes.

- **Subject:** Welcome to Excellent Tiling Services
- **Preview text:** Tiles, MELA bathroomware and tiling tools from a Perth tiling team.
- **Heading:** Thanks for joining us
- **Body:** We're a Perth tiling business in Maddington that sells the products we install: porcelain tiles, MELA vanities and tapware, and tiling tools. Every price is on the website. Want to see something in person? Book an evening showroom visit, Monday to Saturday, 4:30 to 9 pm.
- **Product block:** 3 products. Suggested: MELA basin mixers (from $189), MELA wall hung vanities (from $703), porcelain tiles.
- **Button:** Shop the range

### 3. Thank you + Google review (template: "Thank customers after purchase")
Send 7 days after the order is fulfilled.

- **Subject:** How did we go?
- **Preview text:** One minute, and it helps a local business a lot.
- **Heading:** Thanks for your order
- **Body:** We hope everything arrived in good shape. If anything isn't right, reply to this email and we'll sort it out. If you're happy, a quick Google review helps other Perth renovators find us.
- **Button:** Leave a Google review → link: https://search.google.com/local/writereview?placeid=ChIJJ1zzJya-MioR2YywWzXHAJo
  (Google Business Profile "Excellent Tiling Services PTY LTD"; it asks the customer to sign in to Google first.)

### 4. Win-back (template: "Win back customers")
Send 90 days after the last order.

- **Subject:** Ready for the next room?
- **Preview text:** Tiles, vanities and tapware, with every price online.
- **Heading:** Planning another job?
- **Body:** Whether it's the laundry, an ensuite or a splashback, we've got the tiles, tapware and tools, and our licensed team can do the work too, starting with a free measure and quote in Perth.
- **Buttons:** Shop now · Get a free quote (`/pages/request-a-quote`)

---

## Campaigns (Marketing → Create campaign → Shopify Email)

Send only to customers who have subscribed to email marketing.

### A. "We're online" launch (send once)
For past tiling customers and contacts. Import them first: Customers → Import, and only include people who agreed to receive emails from you.

- **Subject:** You can now shop our range online
- **Preview text:** Tiles, MELA bathroomware and tiling tools, with every price shown.
- **Heading:** Our range is online
- **Body:** You know us for tiling. Now you can shop the products we use on our jobs: porcelain tiles, MELA vanities, basins and tapware, and tiling tools and trims. Every price is on the website. Order online and pick up free in Maddington, or choose delivery at checkout.
- **Product block:** 4 products, one from each range (a tile, a MELA vanity, a MELA basin mixer, a Sigma tile cutter).
- **Button:** Shop online

### B. Trade accounts (for tilers, builders and plumbers)
Send to customers tagged `trade`, or to trade contacts you import.

- **Subject:** Trade pricing for tilers, builders and plumbers
- **Preview text:** 5–25% off, depending on the item. Apply with your ABN.
- **Heading:** Get your trade account
- **Body:** Approved trade accounts get 5–25% off, depending on the item (tiles up to 15%). Apply once with your ABN, then log in and the discount comes off in the cart. Stock up on Sigma tile cutters, Maxisil silicone and grout, tile trims, spacers and floor wastes, with free pickup in Maddington.
- **Button:** Apply for a trade account (`/pages/trade-account`)

### C. Monthly product pick (once a month, short)
- **Subject:** example: "Brushed nickel or matt black?"
- **Body:** One product or one idea, the real price from the live store, one photo, one link. Example: the MELA basin mixer range from $189 in chrome, matt black, brushed nickel, brushed brass and gun metal.
- **Button:** See the range

### D. Black Friday (27 Nov 2026)
Plan by 8 Nov with the `ets-marketing` and `ets-pricing` agents. Any discount must be checked against the 20% profit floor first.
