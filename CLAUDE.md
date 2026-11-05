# Excellent Tiling Services (Shopify store) - notes for Claude Code

Shopify is the source of truth; this repo does not deploy. It holds the custom theme files, store content, pricing data
and scripts, marketing and SEO work, each with a README that is the change log. Re-sync theme files from Shopify after any
theme edit there.

## Read before touching prices, costs, trade accounts or the theme

- `store-content/pricing/PRICING-PLAYBOOK.md`: the rules book (margins, cost basis, competitor rules, B2B trade pricing,
  the change procedure). Follow it exactly. History and dated decisions: `store-content/pricing/README.md`.
- `README.md` (root): theme changes, draft themes waiting to be published, preview links.
- `store-content/supplier-sync/README.md`: supplier imports. `marketing/`, `seo/`: their own READMEs.

## Hard rules

1. **No price, cost, discount, collection, trade band or company change without the owner's explicit approval of the
   specific change.** Propose in a table first. Reads and reports are always fine.
2. **Floors** (playbook section 2): public 25% margin (price-matched lines 20%); trade 25% (MELA 20%); caps 20/15/15.
   Never price under them. MELA never under Bathroom City's price.
3. **One cost basis**: inc GST. Say when a cost is missing; never invent one.
4. **Theme**: never write to the live theme. Duplicate it, edit the draft, give the owner the preview link and the publish
   steps. Sync the edited files into `theme/` and note the draft in the root README.
5. **After any price or band change**, rerun `b2b_price_list_2026_11.py` and `trade_price_metafields_2026_11.py`, update the
   master list, add a README entry, commit and push to the single branch. Stale trade prices are the main failure mode.
6. **Shopify API**: Admin GraphQL via the Shopify MCP tools. Pages of 100; mutations under 16,384 characters; metafields 25 per
   call, price-list prices 100 per call; `bulkOperationRunMutation` and live-theme writes are blocked. Use current field names
   (`defaultEmailAddress`, `countryCodeV2`, `collectionsToJoin`, `newTheme`).
7. **Destructive actions** (deleting products, companies, themes, discounts) need the owner's explicit instruction naming the
   item. Save a copy in the repo first.
8. Write for the owner: short plain sentences, dollar figures, no jargon, one clear recommendation.

## Shopify IDs that matter

Trade market `gid://shopify/Market/26618265663` · catalog `gid://shopify/MarketCatalog/71173406783` ·
price list `gid://shopify/PriceList/17250287679` · publication `gid://shopify/Publication/163372662847` ·
location `gid://shopify/Location/77786087487` (Maddington) · test company `gid://shopify/Company/6510116927`.
