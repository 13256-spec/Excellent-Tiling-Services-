# Storefront filters

**2 Nov 2026:** Search & Discovery is now installed (seen in the app list). The filters below are set only in the app
(there is no API for them). For the house-brand tapware add, Apps -> Search & Discovery -> Filters -> Add filter:

| Filter | Source | Label |
| --- | --- | --- |
| Finish | variant option `Finish` | Finish |
| Product type | product type | Type (group values: Basin Mixer, Wall Mixer, Bath Spout, Shower Set, Shower Head, Shower Rail) |
| WELS rating | product metafield `ets.wels_rating` | WELS rating |
| Installation type | product metafield `ets.installation_type` | Installation |
| Range | product metafield `ets.range` | Range / suite |
| Brand | vendor | Brand |

The metafields must be storefront-readable first: `data/metafields/mutations.graphql` sets `access.storefront: PUBLIC_READ`
on every definition the theme and the filters use. The theme's finish swatches on the brand collection page link to
`?filter.v.option.finish=<name>`, which only works once the Finish filter exists.

---

# Storefront filters (14 Oct 2026, original note)

The website's collection and search pages show only **Availability** and **Price** as filters. The theme has
filtering switched on (`templates/collection.json` and `search.json`, block `filters`), but the list of filters
comes from Shopify's free **Search & Discovery** app, which is **not installed** on the store. Until it is, no
product data can add a filter. This can only be done in Shopify admin (there is no API for it).

## Install and set up (owner, about 10 minutes)

1. Shopify admin → **Apps** → search "Search & Discovery" (by Shopify, free) → **Install**.
2. Open the app → **Filters** → **Add filter**. Add, in this order:
   - **Product type** (label it "Type")
   - **Finish** (variant option; label "Finish")
   - **Colour** (variant option; label "Colour")
   - **Size** (variant option; label "Size")
   - **Range** (product metafield `ets.range`; label "Range")
   - **Material** (product metafield `ets.material`; label "Material")
   - **Price** and **Availability** (keep)
3. Optional, for the Product type filter: use **Group values** so similar types show as one choice
   (e.g. "Basin Mixer" + "Tall Basin Mixer" → "Basin mixers"; "Hand Shower" + "Hand Shower Set" + "Combination
   Shower Set" → "Showers"; "Wall Mixer" + "Wall Mixer with Diverter" → "Wall mixers").
4. Save. Filters appear on every collection page and on search results within a few minutes.

## Product data that feeds those filters

All MELA and DSA products use the same option names (`Finish`, `Size`, `Colour`) and the same `ets` metafields,
so the filters work across both ranges. On 14 Oct 2026 the 64 new DSA products (62 items + 2 Malaga packages) were
given `ets.supplier`, `ets.range`, `ets.material` and, where the supplier gives them, `ets.width_mm`,
`ets.height_mm`, `ets.depth_mm` (`supplier-sync/dsa-metafields-2026-10-14.json`). The definitions for
`ets.range`, `ets.material`, `ets.width_mm`, `ets.height_mm`, `ets.depth_mm` and `ets.wels_rating` were set to
storefront access **Public read** so the app (and the theme) can use them.
