# Duplicates check, 12 Oct 2026

Owner's instruction: "check for any duplicates and fix". Everything below was checked from fresh Shopify
exports (all 924 products, every variant, every image), the collections, discounts, menus, pages, customers
and the Klaviyo account.

## Products: no duplicates

- 924 products (921 active, 2 archived, 1 draft), 3,755 active variants.
- No two variants share a SKU (3,755 SKUs) or a barcode (1,487 barcodes).
- No two products share a title. The 148 near-identical titles are real size/model siblings (CLARK 600 vs
  CLARK 900, 300 mm vs 350 mm blades, Subway vs Subwave tiles – both ranges are in the Eternity list).
- No product has the same variant twice.
- The draft "Raimondi Bulldog Profiling Machine" ($642.95, no cost) is not a copy of the active Bi-Bulldog;
  it is unpublished because its price looks wrong. The two archived BAT trims (Unicorn corner, APC 60
  combination) have no prices; left archived.

## Fixed

| What | Where | Fix |
|---|---|---|
| Same photo attached twice (or three times) to a product | Time Stone Charcoal, Lava Ash, Lava Kraka tiles; NICLIS square and round tile-insert drains | 9 duplicate image copies deleted; the first copy and all variant images kept |
| Old trade collections `Trade – 5% / 10% / 15%` (tag-based) duplicating the `trade-list-N` collections | Shopify collections | 3 collections deleted (nothing used them: the five automatic trade discounts target `trade-list-N`, the theme reads `ets.trade_band`) |
| Stale `trade-5` / `trade-10` tags on 240 products (left from the old band system; many contradicted the real band) | Shopify product tags | tags removed |
| Second welcome code `ETSWELCOME10` ($10 off $200, 0 uses) next to `WELCOME10` | Shopify discounts | deactivated (not deleted; reactivate in Discounts if wanted) |
| Second free-shipping mechanism: automatic app discount "Free AU standard shipping over $180" (app "Advance Free Shipping Discount", created 10 Oct) on top of the free standard rates added 11 Oct | Shopify discounts | deactivated; the free rates in Settings → Shipping do the job on both parcel profiles. The app can be uninstalled. |
| Test customer "Test Customer" (ets.checkout.test@example.com, from the 11 Oct checkout tests) | Shopify customers | deleted |
| Overlapping product types: generic "Hardware" (8 products), "Tiling Tools + Installation Products" (10), "Diamond Blades" (4) | Shopify product type | 22 products moved to the existing specific types (Tiling Tools, Diamond Blades & Abrasives, Tiling Trowels & Floats, Silicone Accessories, Sealants Sealers & Cleaners, Adhesives); collection rules already covered both names, so no product left a collection |
| Draft Klaviyo flow "ETS Checkout Recovery – 3 Hour Reminder" and its draft template, superseded by the live abandoned-checkout flow | Klaviyo | both deleted |

## Looked at and left alone

- Menus: "Main menu" (Shopify's default, slightly older links) and "Main menu 2026" (what the live header
  uses). The default menu can't be deleted; harmless. Edit "Main menu 2026" when changing navigation.
- 14 BAT Trims photos used on more than one product (same profile in aluminium/brass/stainless, 1 m and
  3 m lengths): range photos, correct.
- Collections "Bathroom Vanities" (28) and "Wall Hung Vanities" (28) hold the same products today because
  every vanity is wall hung; both are in the menu on purpose.
- Klaviyo default segments (VIP, Repeat Buyers, Churn Risks, Engaged 30/90) sit next to the ETS ones;
  the draft campaign template "ETS | Finishing Essentials | Draft | 8 Oct 2026" is a campaign idea, not a copy.
- 20 products still have no photo at all after the 12 Oct photo sourcing (see `photos-sourced-2026-10-11.csv`).
