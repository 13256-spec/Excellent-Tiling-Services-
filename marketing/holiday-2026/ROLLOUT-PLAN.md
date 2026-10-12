# Holiday rollouts 2026 – staged for the owner's approval

Updated 12 Oct 2026. Nothing in this plan is live. The pieces are built and parked in Shopify and Klaviyo so
the owner can look, change, and say yes; the Rollout itself is the switch and only he can press it.

Shopify's new **Rollouts** (Markets → Rollouts, on the Basic plan and up) bundle a theme change, discounts
and catalog changes into one scheduled event that starts and ends on its own and rolls the store back
afterwards. That is what "holiday rollouts" means in the admin.

## The three events

| # | Event | Runs (Perth time) | What changes | Offer |
| --- | --- | --- | --- | --- |
| 1 | **Black Friday to Cyber Monday** | Fri 27 Nov 00:01 → Mon 30 Nov 23:59 | header bar + home hero swap to the Black Friday theme; the Black Friday discount switches on | 15% off 222 products, automatic (no code) |
| 2 | **Christmas post cut-off** | Mon 7 Dec → Fri 18 Dec | header bar only: "Order by Fri 11 Dec for Australia Post delivery before Christmas · Perth pickup until Wed 23 Dec" | none (information) |
| 3 | **Boxing Day to New Year** | Sat 26 Dec 00:01 → Sun 10 Jan 23:59 | header bar + hero: "Summer reno sale"; same 15% discount re-used, or a tiles-only one | to decide after Black Friday numbers |

Only Event 1 is built. Events 2 and 3 are planned so the calendar and content can be prepared in time.

## Event 1: Black Friday 2026 (built, not live)

**Offer.** 15% off, automatic in the cart, on the 222 products that stay above the profit floor
(cost × 1.1 × 1.25) at 15% off. List: `black-friday-2026-eligible-15pct.csv` (lowest price and lowest
profit % after the discount per product). Breakdown:

| Group | Products |
| --- | --- |
| Tiling tools, cutters, blades, spacers, levelling | 64 |
| Tapware, showers, sinks (MELA) | 45 |
| Porcelain tiles | 48 |
| Silicone, grout, cleaners (Maxisil) | 19 |
| Trims and profiles (BAT) | 15 |
| Vanities, basins, mirrors, toilets, niche boxes | 14 |
| Bathroom accessories, wastes, brushes, packaging | 17 |

Lowest profit on any eligible product after 15% off: 20.0% of the sale price (tiles stay above 23.7%). At 15%
off sitewide, 579 of 1,572 variants would have broken the floor and 9 would sell below cost, which is why the
offer is scoped. Trade customers: the Black Friday discount does not combine with the trade automatic
discounts (set to not combine), so a trade customer gets the bigger of the two, never both.

**Built in Shopify (12 Oct 2026):**

- Collection **Black Friday 2026** (`gid://shopify/Collection/302463156287`, handle `black-friday-2026`),
  222 products, unpublished (not visible on the site until published).
- Automatic discount **"Black Friday 2026 – 15% off (rollout only, dates expired on purpose)"**
  (`gid://shopify/DiscountAutomaticNode/1385989865535`), 15% off that collection, combines with shipping
  discounts only. Its own dates are 12 Oct 00:00–00:01, so it shows as Expired and nobody gets it. A Rollout
  that "activates" it turns it on for the rollout's window regardless of those dates (Shopify's documented
  behaviour). If the owner would rather not use Rollouts, he can instead edit the dates to 27–30 Nov.
- Theme **"ETS 2026 – Black Friday rollout (draft, not live)"** (`gid://shopify/OnlineStoreTheme/144032366655`),
  a copy of the live theme with two changes: header bar message "Black Friday · 15% off 220+ tools, tiles,
  tapware & trims · Fri 27 to Mon 30 Nov" and the home hero (eyebrow, heading "15% off tools, tiles, tapware
  and trims. Four days only.", text, button to the Black Friday collection). Files: `theme/`. Preview it from
  Online Store → Themes → … → Preview. **Re-copy it the week before** if the live theme changes between now
  and then (duplicate the live theme again and reapply the two files), otherwise the rollout would publish an
  old theme.

**Built in Klaviyo:** email template "ETS | Black Friday 2026 – 15% off, four days | DRAFT for approval"
(`WsJaAz`) and a Draft campaign of the same name to the email-subscribers segment (trade excluded). Not
scheduled.

**Social (to prepare after approval, `ets-content` + `ets-calendar`):** teaser Story Thu 26 Nov evening,
main carousel Fri 27 Nov 6:30 pm (tools + tiles from the collection, real prices after discount), reminder
Sun 29 Nov, "last day" Story Mon 30 Nov. Marketplace listings that weekend carry the discounted price.

## How the owner creates the Rollout (about 10 minutes, once)

1. Shopify admin → **Markets → Rollouts → Create rollout**. Name: "Black Friday 2026". Type: **Event**.
2. Click **Save** once (needed before theme changes), then **Add changes**.
3. **Theme (Online store)** → under "Replace the current theme" pick "ETS 2026 – Black Friday rollout (draft,
   not live)" → Apply.
4. **Add changes → Discounts** → select "Black Friday 2026 – 15% off…" → set it to **Activated** → Apply.
5. Traffic allocation: leave at **All eligible visitors** (100%).
6. Scheduling: "Event runs from" **27 Nov 2026 12:01 am** → **Set end date** **30 Nov 2026 11:59 pm**
   (store timezone is Perth).
7. Check there are no "Resolve rollout conflicts" messages, then **Save**. Status becomes Scheduled. The store
   switches on Friday and back on Monday night by itself. Pause or End it early from the same page.
8. Publish the collection so the hero button works: Products → Collections → Black Friday 2026 → Sales
   channels → Online Store (the collection page can be published early; the discount only applies while the
   rollout serves).
9. Tell `ets-email` to schedule the campaign for Fri 27 Nov 7:00 am Perth and `ets-calendar` to add the
   social dates.

Rules from Shopify's help pages: a discount can be in only one unended rollout; vintage themes and Liquid code
edits can't be part of a rollout (ours is Horizon-based, JSON settings only, so it qualifies); archiving a
rollout deletes its theme changes; staff need the Markets → Rollouts permission plus Discounts and Themes.

## If the owner wants a different offer

- 10% instead of 15%: 302 products pass; rerun the check in `ets-pricing` (campaign discount check) and
  rebuild the collection. 20%: only 134 products pass.
- Tiles only, or tools only: filter `black-friday-2026-eligible-15pct.csv` by type and give the list to
  `ets-pricing` to rebuild the collection.
- No discount, free shipping instead: a free-shipping automatic discount over $100 Australia-wide for the four
  days is the cheapest alternative; ask `ets-pricing` for the cost on last month's basket sizes.

## Event 2: Christmas post cut-off (plan only)

Header bar message from Mon 7 Dec: "Order by Fri 11 Dec for Australia Post delivery before Christmas ·
Maddington pickup until Wed 23 Dec". Check Australia Post's published 2026 cut-off dates in late November
and adjust. Theme copy only, no discount: duplicate the live theme that week, change `msg_1`, create an Event
rollout 7–18 Dec. Email: one short campaign on Mon 7 Dec to subscribers ("Last post dates").

## Event 3: Boxing Day to New Year (plan only)

Decide on Mon 1 Dec from the Black Friday numbers (orders, discount uses, margin). Same mechanism: a theme
copy, the same or a new discount, an Event rollout 26 Dec – 10 Jan. January is renovation-planning season in
Perth; the hero can lead with "book a free measure and quote" rather than a discount.

## Files here

- `black-friday-2026-eligible-15pct.csv`: the 222 products with lowest price and profit after 15% off.
- `black-friday-2026-eligible-ids.json`: their Shopify product ids (used to build the collection).
- `theme/header-group.json`, `theme/black-friday-theme-changes.json`: the two theme changes.
