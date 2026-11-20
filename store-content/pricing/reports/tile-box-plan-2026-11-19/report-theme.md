## THEME findings: m2-units today, and what the per-box model needs

Read-only. No Shopify calls, no repo edits. (A PostToolUse hook printed "Theme pushed" after a grep; nothing was pushed.) All paths under `/home/user/Excellent-Tiling-Services-/`.

### 1. How m2-units mode works today, end to end

**Switch.** The product tag `m2-units` is the only switch; every file tests `product.tags contains 'm2-units'` (or `item.product.tags`). Data side (store-content/pricing/tile_m2_units_2026_11.py:36-51): price = $/m² ÷ 100, `showUnitPrice:true`, `unitPriceMeasurement:{quantityValue:0.01, quantityUnit:M2, referenceValue:1, referenceUnit:M2}`, cost ÷100, weight ÷100, plus `tagsAdd "m2-units"`. So Shopify itself already computes `variant.unit_price` = $/m² and shows "$55.00/m²" at checkout (README.md:125).

**Product page calculator** (`theme/snippets/ets-pdp-calc.liquid`, rendered by the custom-liquid block "calc" in theme/templates/product.json:155-160 and product.store-wide.json:158):
- :6-14 `is_tile` = product.type matches `settings.ets_trade_tile_types` (= "Tile", theme/config/settings_data.json:112). Calculator only renders for that type (:15).
- :16 root `<div data-ets-calc data-m2>` (data-m2 only with the tag).
- :19-21 Area (m²) / length / width inputs, step 0.01. :24-31 "Allowance for cuts" `<select data-waste>` 0 / 10 (default) / 15 / 20 %. :33-36 output `<strong data-out>` and `Set quantity` button `[data-apply]`.
- :37-41 note: tagged "sold per m², in steps of 0.01 m²"; untagged "Rounded up to the next whole m²".

**Calculator JS** (`theme/assets/ets-2026.js`, all document-level delegated listeners so Horizon section re-renders keep working, :169):
- :175-193 `calcUpdate`: area = l×w if dims typed (:177-180); `need = area × (1 + waste/100)` (:183); tagged: `qty = ceil(need×100 − 1e-6)/100` to 2 dp, untagged: `Math.ceil(need)` whole m² (:185); writes `calc.dataset.qty`, text "`qty` m²", button "Set quantity to `qty` m²" (:186-189).
- :205-220 apply click: finds `[data-ets-m2-qty]` inside the closest `.shopify-section`, else `input[name="quantity"]` (:210-212); sets value, dispatches input+change (:214-216); button "Quantity set to X m² ✓"; scrolls to the add button (:218-219).
- :222-232 m² box → real quantity: on input, hidden `input[ref="quantityInput"]` = `max(1, round(m2×100))` (:224-228); on change the m² box is normalised to 2 dp (:229-232).

**Quantity selector** (`theme/snippets/quantity-selector.liquid`, used on product page, quick-add modal and cart lines):
- :33-37 `ets_m2` true only when `line_index == null` (product page / quick-add) and tagged.
- :44-57 visible "Area (m²)" `<input data-ets-m2-qty min=0.01 step=0.01 value=1.00>`.
- :58-59 the real `quantity-selector-component` gets `hidden style="display:none"`; :87 its input value is hard-coded `100` for m² products (= 1.00 m²).
- :203-219 CSS for `.ets-m2-qty`.

**Price display** (`theme/snippets/price.liquid`):
- :21-29 `ets_x = 100` when tagged; `price` and `compare_at_price` ×100. :48-51 `price_min/max` ×100 (cards, volume pricing).
- :71-78 `is_ets_tile` from product.type (same type list; NOT the tag).
- :82-93 B2B: trade = variant.price, retail = compare_at, save; all ×ets_x; pct from those.
- :104 trade price gets " / m²" when `is_ets_tile`. :125 retail price gets " / m²" when `is_ets_tile` and no trade pct.
- :126-133 Shopify's native unit price (`render 'unit-price'`, stock Horizon snippet, not in repo) only when `show_unit_price` AND `ets_x == 1`, i.e. suppressed for m² products (it would otherwise print "$55.00/m²" a second time). Only `blocks/_featured-product-price.liquid:51` passes `show_unit_price: true`.

**Product cards / collection "From" price:**
- `theme/blocks/_featured-product-price.liquid:9-12` `product.price_min` ×100 when tagged, used for "From $X" (:19-22, :45-48); otherwise renders `price` (:50-54).
- `theme/snippets/product-card.liquid:25-31` `has_quick_add = false` when tagged. `theme/blocks/_product-card-gallery.liquid:39-44` skips `render 'quick-add'` when tagged (one-click add would add 0.01 m²).

**Cart lines** (`theme/snippets/cart-products.liquid`, cart page + drawer):
- :148-153 `ets_x = 100` per line by tag.
- :158 row class `cart-items__table-row--full-width-variants` unless `item.unit_price_measurement` (drawer grid has a `unit_price` area, CSS :525-560, :827-840).
- :310-344 per-unit price block: `item.final_price`, `item.original_price`, `item.variant.compare_at_price` all `| times: ets_x`; :343 " / m²".
- :363-366 quantity shown as m²: `item.quantity | divided_by: 100` + "." + `modulo: 100` padded → "2.88 m²".
- :367-377 the quantity selector is rendered inside `<div hidden style="display:none">` for m² lines (no +/−; "remove and re-add to change"); kept because Horizon's cart JS finds selectors by line position (:367).
- :413-420 line total = `item.final_line_price` (already correct in any unit). :430-434 native unit price only when `ets_x == 1`.

**Cart count (a tile line counts as 1, not 288):**
- `theme/snippets/cart-drawer.liquid:80-89` (badge :90-100), `theme/snippets/cart-bubble.liquid:13-21` (+ :28), `theme/sections/ets-header.liquid:79-88` (badge :89-92, element `[data-ets-cart-count]`) — Liquid loops by tag.
- `theme/assets/cart-icon.js:60-72` and `theme/assets/ets-2026.js:115-119` — JS refetches `/cart.js` and counts a line as 1 when `unit_price_measurement.quantity_value === 0.01`, else `item.quantity`.

**Schema / SEO** (`theme/snippets/ets-product-schema.liquid:176-185`): tagged branch :180-182 `"price": variant.price × 100 / 100.0` (= $/m²) and `priceSpecification: UnitPriceSpecification … referenceQuantity {value 1, unitCode "MTK"}`; untagged :183-184 price/100.0.

**Not wired / legacy:** `theme/sections/ets-product-story.liquid:1-3` has an older area×waste calculator keyed on collection handle `tiles`; no template references it. `theme/sections/ets-flagship-header.liquid:9` uses raw `cart.item_count`; not in `theme/sections/header-group.json:15` (which uses `ets-header`). Both can be ignored.

### 2. What must change per file for the per-box model

Target data (Gia's model, store-content/supplier-sync/README.md:305-309): variant price = price per box; `unitPriceMeasurement {quantityValue: <m² per box e.g. 1.44>, quantityUnit M2, referenceValue 1, referenceUnit M2}`; Shopify then gives `variant.unit_price` / `item.unit_price` = $/m² (cents) and `variant.unit_price_measurement.quantity_value` = m² per box (Liquid), `item.unit_price_measurement.quantity_value` in `/cart.js`.

Recommended switch (lazy and cut-over safe): key on `unit_price_measurement.quantity_value` being present instead of the `m2-units` tag, and never multiply by 100. Then m² = `quantity × quantity_value` and $/m² = `unit_price` are correct for BOTH today's 0.01 data and tomorrow's 1.44 data, so theme publish and the data switch do not have to be simultaneous. If the tag is kept as the switch, see the ordering risk in section 4.

| File | Change |
|---|---|
| `theme/snippets/ets-pdp-calc.liquid` | :24-31 replace the select with `<label><input type="checkbox" data-waste value="15" checked> Add 15% wastage</label>` (or keep select; owner asked for a tick box). :16 add `data-m2-box="{{ product.selected_or_first_available_variant.unit_price_measurement.quantity_value }}"`. :33-36 output becomes "N boxes · 1.44 m² per box · 2.88 m²"; button "Set quantity to N boxes". :37-41 note: "Sold by the box (1.44 m² per box). We round up to whole boxes; keep a few spare." Multi-size products (84 variants / 43 products) can have a different m² per box per variant, so read the value from the selected variant; Horizon re-renders the section on variant change, which refreshes the attribute. |
| `theme/assets/ets-2026.js` | :183-189 `need = area × (waste checked ? 1.15 : 1)`; `boxes = Math.ceil(need / m2PerBox − 1e-6)`; `m2 = (boxes × m2PerBox).toFixed(2)`; out text "N boxes · X m² per box · Y m²". :205-220 apply: set `input[name="quantity"]` (drop the `[data-ets-m2-qty]` lookup :211-212); button "Quantity set to N boxes ✓". :222-232 delete (m² → ×100 sync). :117-118 cart count: drop the `=== 0.01` special case, use `c.item_count` (boxes are real items) — see count note below. |
| `theme/snippets/quantity-selector.liquid` | Delete the ets_m2 branch (:33-37, :44-59, :87 hard-coded 100, CSS :203-219) so the normal boxes stepper shows. Optionally add one line under it for box products: `{{ variant.unit_price_measurement.quantity_value }} m² per box`. |
| `theme/snippets/price.liquid` | Remove ×100 (:21-29, :48-51, :87-91). Per-m² headline: `selected_variant.unit_price` (+ compare-at per m² = `compare_at_price | divided_by: quantity_value | round`, since Shopify gives no unit compare-at) with " / m²", and a second line "$79.20 per box · 1.44 m²" (`selected_variant.price`, `quantity_value`). Or Shopify-native: box price headline + the existing `unit-price` render (:126-133, drop the `ets_x == 1` guard) — this is what Gia's does. Either way :104 and :125 must stop appending " / m²" to a price that is per box (see risk 4a). B2B block :82-93: use `selected_variant.unit_price` for the trade $/m² and `compare_at_price ÷ quantity_value` for retail $/m²; verify as a trade login that `unit_price` follows the catalog price. |
| `theme/snippets/cart-products.liquid` | :148-153 detect by `item.unit_price_measurement` (or tag). :310-344 show box price (`item.original_price/final_price`, no ×100) and `item.unit_price` " / m²". :363-366 replace with "N boxes · X m² per box · Y m²" where Y = `item.quantity | times: item.unit_price_measurement.quantity_value` (`round: 2`). :367-377 un-hide the quantity selector (+/− now change boxes). :430-434 drop `and ets_x == 1` so the native "$55.00/m²" line renders (drawer grid already has the `unit_price` area, :158, :525-560). |
| `theme/snippets/cart-drawer.liquid:80-89`, `theme/snippets/cart-bubble.liquid:13-21,28`, `theme/sections/ets-header.liquid:79-88`, `theme/assets/cart-icon.js:62-70`, `theme/assets/ets-2026.js:117-118` | Boxes are countable items: delete the special-casing and go back to `cart.item_count` / `cart.totalQuantity` / event count. (Keep "1 per tile line" only if the owner wants that.) Note cart-icon.js:67 and ets-2026.js:118 compare to `0.01` literally, so with 1.44 they already fall through to `item.quantity` — dead but harmless. |
| `theme/snippets/product-card.liquid:29-31`, `theme/blocks/_product-card-gallery.liquid:40-43` | Quick-add can be re-enabled (adds 1 box, sensible). Owner's call; remove the `unless` if so. |
| `theme/blocks/_featured-product-price.liquid:9-12` | Remove ×100. "From" price for `price_varies` products: `product.price_min` is the cheapest BOX; for "From $X / m²" loop `product.variants` and take the min `variant.unit_price`. |
| `theme/snippets/ets-product-schema.liquid:180-182` | `"price"` = `variant.price | divided_by: 100.0` (what is charged per unit sold = box); keep `UnitPriceSpecification` with `"price": variant.unit_price | divided_by: 100.0`, referenceQuantity 1 MTK; optionally `"eligibleQuantity": {"@type":"QuantitativeValue","value": quantity_value, "unitCode":"MTK"}`. |
| Checkout | No change possible (Grow); the "x 288" known limit (README.md:125) disappears — checkout shows "2 × $79.20" and "$55.00/m²". |
| README.md | New entry; also README.md:9 "Last synced…" line is stale (names the Seller-schema theme). |

Stock Horizon files touched by this (`snippets/unit-price.liquid`, `snippets/quick-add-modal.liquid`, `assets/component-cart-quantity-selector.js`) are not in the repo; the drawer/cart JS relies on quantity selectors existing per line (cart-products.liquid:367), which un-hiding satisfies.

### 3. How draft themes were made; which theme is live

- Method (README.md, every "draft theme" entry; explicit at :541): duplicate the live theme with the Admin GraphQL `themeDuplicate` mutation ("a copy of the live theme"), edit files on the copy, preview, owner publishes from Shopify admin → Online Store → Themes → draft → Publish (README.md:390-391). The README names no MCP tool beyond `themeDuplicate`; CLAUDE.md rule 6 says Admin GraphQL via the Shopify MCP tools and that live-theme writes are blocked. Available in this session: `mcp__Shopify__graphql_mutation` / `graphql_query` (themeDuplicate, themeFilesUpsert), and `mcp__Shopify__theme_bash`, `theme_commit`, `theme_publish`, `theme_screenshot` (not used in the README record). Older entries use gid form `gid://shopify/OnlineStoreTheme/<id>` (README.md:528,542,552,565).
- Preview URL pattern: `https://excellenttilingservices.com/<page path>?preview_theme_id=<theme id>` (README.md:38,77-78,95-96,129,154,171,200).
- Theme id chain (README): B2B trade display 144867229759 (published 5 Nov, :151) → no-Sale-badge draft 144868016191 (:152) → "Tiles by exact m2 (draft)" 144880795711, copy of 144868016191 (:114), published 5 Nov (:108) → "Price on request (draft)" 145086480447, copy of the live Tiles-by-m2 theme (:89-90), published 11 Nov (:78-79) → "New menu: materials, tools, brands (draft)" 145087791167 (:69), published 11 Nov per :19-20 → **live theme now (per README, 16 Nov): 145087791167 "ETS 2026 – New menu: materials, tools, brands (draft)"**. Newest draft waiting: "Christmas closure notice (draft)" 145261363263 (:19, publish ~1 Dec, preview :38). Not verified against Shopify in this task; confirm with `themes(first:5, roles:[MAIN])` before duplicating. Suggest duplicating 145261363263 so the per-box theme carries the Christmas notice and the owner does not have to merge two drafts.

### 4. Risks: places that assume quantity×100 = m² or hard-code 0.01

a. **`theme/snippets/price.liquid:104` and :125** append " / m²" for any product whose type is "Tile", independent of the tag. With box prices that labels $79.20 (a box) as "$79.20 / m²". Must be fixed, not just the ×100.
b. ×100 scaling that would show a $79.20 box as "$7,920.00 / m²": price.liquid:24-29, :49-50, :87-91; cart-products.liquid:315,320,322,333,339; _featured-product-price.liquid:11; ets-product-schema.liquid:180-182 (Google would read $7,920).
c. quantity ÷100 assumptions: cart-products.liquid:363-366 (2 boxes → "0.02 m²"); quantity-selector.liquid:87 (value 100 = 100 boxes added!) and :44-56; ets-2026.js:185, :227, :231 (m²×100 into the quantity input → 288 boxes).
d. Hard-coded 0.01: cart-icon.js:67, ets-2026.js:118 (fail-safe: fall through to item.quantity). Count-by-tag in cart-drawer.liquid:84, cart-bubble.liquid:16, ets-header.liquid:83 would show "1" for 3 boxes (cosmetic).
e. **Cut-over ordering.** Today the same tag drives theme and data. If the data switches before the new theme is published, the live theme shows item b. If keyed on the tag and the theme goes first, 0.01 products render as "$0.55 per box · 0.01 m² per box" until the data step (harmless, odd). Keying on `unit_price_measurement` (section 2) removes the ordering problem; otherwise publish theme first, run the data script straight after (as on 5 Nov), or use a new tag.
f. **Rounding.** Shopify's `unit_price` = price ÷ quantity_value, rounded to cents. $79.20 ÷ 1.44 = $55.00 exactly, but boxes of 1.12 / 1.35 / 1.62 m² give uneven $/m² (e.g. $61.60 ÷ 1.12 = $55.00 ok; $74.25 ÷ 1.35 = $55.00 ok; but a $55/m² target × 1.62 = $89.10 fine — the pricing step must set box price = round($/m² × m²/box) and check the displayed $/m² does not drift). Whole-dollar $/m² is no longer required; whole-cent box price is.
g. **B2B.** price.liquid:83-85 uses variant.price/compare_at (contextual catalog price). `variant.unit_price` should follow it; confirm in preview as the test company (gid://shopify/Company/6510116927). No unit compare-at exists: compute retail $/m² as compare_at ÷ quantity_value.
h. **Multi-size products.** m² per box differs per variant; calculator/price must read the selected variant and survive Horizon's section re-render (delegated listeners already do; `calc.dataset.qty` resets, fine).
i. Mosaics (per sheet, no unit measure) are untouched by a measurement-keyed switch; a tag-keyed switch also leaves them alone.
j. Out of theme scope but linked: b2b_price_list_2026_11.py / trade_price_metafields_2026_11.py have m2-units logic (store-content/pricing/README.md:325, rounds trade per 0.01 unit up); order emails / fulfilment now read quantity as boxes, not 0.01 m²; tile_m2_units_2026_11.py:49 must become per-box (price per box, quantityValue = m² per box, cost per box, weight per box).