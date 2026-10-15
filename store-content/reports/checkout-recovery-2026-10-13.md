# Checkout recovery: is the automation set up correctly? (13 Oct 2026)

The owner asked, on the morning of 13 Oct (Perth), whether the checkout-recovery automation is set up
correctly, to delete the old one and keep the working ones. Everything below was checked live in Klaviyo
and Shopify on 12 Oct 23:00 to 23:45 UTC (13 Oct, 7 to 7:45 am Perth).

## What exists

| Where | Automation | Status | What it does |
|---|---|---|---|
| Klaviyo | ETS \| Abandoned checkout (saved checkout + FREEPOST), VU6HcH | live, correct | Shopify "Checkout Started" → 1 h: "Your checkout is saved" (the items with photos, Finish my order button) → 24 h: "Free postage on this order" (FREEPOST). Each step skipped if they ordered since. |
| Klaviyo | ETS \| Abandoned cart (still in your cart), TM9NiE | live, correct | "Added to Cart" → 4 h: "Still in your cart", skipped if they reached checkout or ordered since. |
| Klaviyo | ETS \| Browse abandonment (viewed, no cart), TkVVC9 | live (made 12 Oct, 20:40 Perth) | onsite "Viewed Product" → 2 h: "Still thinking it over?" with the product, skipped if they added to cart, started checkout or ordered. |
| Klaviyo | ETS \| Repeat purchase (day 21), S9w6zL | live (made 12 Oct) | 21 days after an order, 9:30 am: "Finishing the job?" (silicone, trims, taps), skipped if they ordered again. |
| Klaviyo | welcome ×3, post-purchase ×2, win-back, two trade emails | live | unchanged, see `store-content/email/README.md` |
| Shopify | "Abandoned checkout emails by Shopify" (built in) | **on, duplicate** | Shopify's own plain reminder about 10 hours after the checkout, to email subscribers only. Shopify's record for the 11 Oct 14:15 checkout (excellenttiling1@hotmail.com, subscribed) shows "email sent 12 Oct 00:21 UTC"; the two non-subscribed abandoners of 12 Oct got nothing from it. |

The 8 Oct draft flow "ETS | Checkout Recovery – 3 Hour Reminder" was already deleted on 12 Oct. The three
Klaviyo flows are not duplicates of each other: cart, checkout and browse cover different moments, and each
later one is skipped once the customer moves on (cart skipped once they reach checkout, browse skipped once
they add to cart or check out). The only duplicate is Shopify's built-in email, which the owner turns off
(below) once Klaviyo's emails are authenticated.

## What the numbers say (flows live since 11 Oct, 11:56 pm Perth)

- Shopify "Checkout Started" events reaching Klaviyo: 15 since 5 Oct (1, 1, 1, 4, 0, 5, 3 a day from 5 to
  12 Oct Perth), one profile each, so the trigger works. "Added to Cart": 26 events from 6 to 12 Oct.
- Emails the flows sent: "Your checkout is saved" to 3 people on 12 Oct (02:07, 05:12 and 07:35 UTC, each
  about 1 h after their checkout); "Still in your cart" to 1 (the owner's own account). Opens 0, clicks 0,
  orders 0, bounces 0, no skipped sends. The FREEPOST follow-ups are due 24 h after each checkout (the first
  at 01:07 UTC on 13 Oct), so none had gone out yet at the time of the check.
- Shopify abandoned checkouts since 12 Sep: 6. Three are real and recent: a $128.65 SIRI wash-up bucket to
  Panania NSW, abandoned at the payment step with $39 postage showing (5.5 kg, so the $39 tier); a $28.90
  floor scraper to Charleville QLD; and a $63.96 checkout (Klaviyo saw it, Shopify's list did not keep it).
  The other three are the owner's own Zoe checkout (the items of order #1009) and two test checkouts from
  the 2 and 11 Oct shipping tests (their test customers were deleted on 12 Oct).
- Orders 5 to 12 Oct: 9 (#1001 to #1009; 7 web, 1 eBay, 1 quick sale). Three web orders on 10 and 11 Oct
  match "Checkout Started" events to the second, so completed checkouts are counted correctly and never
  emailed.

## Why nobody opened them: the emails fail DMARC

`excellenttilingservice.com.au` publishes `v=DMARC1; p=quarantine`. Klaviyo has **no sending domain set up**,
so every flow email goes out through Klaviyo's shared domain (`kocruj.shared.klaviyomail.com`) with the From
address contactus@excellenttilingservice.com.au. Neither the SPF nor the DKIM domain matches the From
domain, DMARC fails, and the domain's own policy tells Gmail, Outlook and Hotmail to quarantine: the emails
land in junk. All four recipients so far use Gmail, Hotmail or Live. The welcome, post-purchase and win-back
emails have the same problem; none has had a recipient yet.

**Fix, started 13 Oct:** a branded sending domain `send.excellenttilingservice.com.au` was created in Klaviyo
(id 3434342, status pending). It needs four DNS records at the domain's DNS host, which is Hosting Platform
(nameservers ns1/ns2.syd7.hostingplatform.net.au; the company email is hosted there too):

| Type | Host / name | Value |
|---|---|---|
| CNAME | `send` | `3847965137100592943.klaviyodns.com` |
| CNAME | `mtd1._domainkey` | `mtd1._domainkey.3847965137100592943.klaviyodns.com` |
| CNAME | `mtd2._domainkey` | `mtd2._domainkey.3847965137100592943.klaviyodns.com` |
| TXT | `@` (the domain itself) | `klaviyo-site-verification=WNnVDh` |

If the DNS editor wants full names: `send.excellenttilingservice.com.au`,
`mtd1._domainkey.excellenttilingservice.com.au`, `mtd2._domainkey.excellenttilingservice.com.au` and
`excellenttilingservice.com.au`. Nothing else in the zone changes (the existing SPF, MX and the mail host stay
as they are). Once the records are in, Klaviyo's verification job is run and the domain activated
(`POST /api/sending-domain-verification-jobs`, then `/api/sending-domain-activation-jobs`); after that the
emails are signed by the shop's own domain and pass DMARC. Until then, assume every Klaviyo email is in junk.

## Fixes applied on 13 Oct

1. **Smart sending off** on the two checkout emails and the cart email (flow actions 120142375, 120142378,
   120142389). With it on, a checkout reminder is skipped whenever any other email went to that person in
   the previous 16 hours, including the cart reminder or a campaign. Still on for the browse, welcome,
   post-purchase and repeat emails.
2. **Browse flow condition** (action 120232850) changed from "no add-to-cart / checkout / order since the flow
   started" to "none in the last 24 hours". Product views are back-filled into Klaviyo at the moment a
   visitor identifies themselves at checkout, so the old condition could have sent "Still thinking it over?"
   two hours after someone had already checked out.
3. **FREEPOST email corrected.** The code only applies to standard post rates up to $30 (parcels to 5 kg);
   the email promised free postage "whatever the order size", which would have failed for the $39 bucket
   order above. New wording in `make_emails.py` and master Y8JnzV; the live copy is now TpVBWu. The plain-text
   versions of both checkout emails now keep the checkout link unescaped (`|safe`); live copy of the first
   email is Wx2R3B.
4. **Checked the saved-checkout email renders** with a real Shopify payload (`event.extra.line_items`,
   `event.extra.checkout_url`): items with photo, variant, quantity and price, and the Finish my order button
   pointing at the recovery link.

## For the owner (superseded by the decision below)

1. Add the four DNS records above at Hosting Platform (or forward the table to their support and ask them
   to add it), then say so: verification and activation take a minute from here.
2. After that, turn off Shopify's built-in reminder so subscribers stop getting two: Shopify admin → Apps →
   Messaging → Automations → "Abandoned checkout emails by Shopify" → the actions menu → turn off (it is not
   reachable through the API). Keep it on until the DNS records are in, so subscribers get at least one
   email that reaches the inbox.
3. The three abandoned checkouts are in Shopify admin → Orders → Abandoned checkouts. The $167.65 bucket
   order (NSW) is worth a phone call: postage was the sticking point and the FREEPOST code will not cover a
   $39 rate.
4. Not touched, say if they should go: the 8 Oct draft campaign "ETS | Finishing Essentials | REVIEW ONLY"
   and its template (never sent), and the 12 Oct Black Friday draft campaign and template "for approval".

## Decision, 13 Oct 8:30 am Perth: Shopify's own automations, Klaviyo parked

The owner's answer to the above: "Not Klaviyo, I don't wanna use that for now, use Shopify ones." Done at
23:50 UTC on 12 Oct (7:50 am Perth):

- **All nine Klaviyo flows set to draft** (off): abandoned checkout, abandoned cart, browse abandonment,
  repeat purchase, welcome series, post-purchase, win-back, trade application received, trade account
  approved. Nothing was deleted; each is one status change away from live. The Klaviyo app stays installed
  (customer sync and onsite tracking still run; the owner can uninstall it from Apps if he wants it gone).
  The Klaviyo sending domain created earlier stays "pending" and unused; its DNS records are not needed.
- **Shopify's built-in "Abandoned checkout emails by Shopify" is now the only recovery email.** It already
  works: Shopify's record for the 11 Oct checkout shows the email sent, and Shopify delivers even without
  domain authentication (the From address shows "via shopifyemail.com", it is not quarantined like Klaviyo's
  was). Two settings make it recover more than it does today, both in Shopify admin → Apps → Messaging →
  Automations → "Abandoned checkout emails by Shopify":
  1. *Edit email* → the **To:** field → **All customers**. Shopify's default is email subscribers only, which
     is why the 12 Oct abandoners (not subscribed) got nothing while the subscribed 11 Oct one did.
  2. *Edit settings* → **Send after: 1 hour** instead of the current 10 hours (the 11 Oct email went 10 h after
     the checkout). One hour is when the customer is still at the device.
  The email's wording and logo are edited in the same place; the default template already lists the items
  and carries the "Complete your purchase" link.
- **Other Shopify automations the owner can turn on** in the same place (Create automation): Recover abandoned
  cart, Convert abandoned product browse, Welcome new subscribers with a discount (pick the existing
  WELCOME10 code), Win back customers (COMEBACK10), Thank customers after they purchase. Each defaults to
  subscribers only. Automations can be created on desktop; on the phone only the three recovery ones show.
- **Sender authentication (optional, recommended):** Settings → Notifications → Sender email → "Authenticate
  your domain" shows store-specific CNAME records to add at Hosting Platform; once in, Shopify's emails come
  from contactus@excellenttilingservice.com.au without the "via shopifyemail.com" label. The domain has no
  Shopify DKIM records today.
- Not applicable any more: the Klaviyo DNS records above, and "turn off Shopify's reminder" (it is the one to
  keep).
