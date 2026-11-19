# Migration plan: tiles from 0.01 m² units to one variant = one box (Gia's model)

Scope: 43 products / 84 variants tagged `m2-units` (81 live, 3 draft). Mosaics untouched. Nothing here has been written to Shopify or the repo. All paths under `/home/user/Excellent-Tiling-Services-/`.

## 0. Blocker: m² per box is not known

No file in the repo, no Shopify field and no Eternity page states m² per box, pieces per box or kg per box for any of the 84 variants (Report 3). The only figure anywhere is "Box coverage: 1.44 m²" in the old descriptions of Time Stone Moon and Time Stone Charcoal (`store-content/descriptions/tiles-2026-10-24.json:6,36`), origin unrecorded. Pallet quantities (57.6 / 86.4 / 40.32 m²) divide by 1.44 but do not prove it; 300x300 (55.44 m²), 100x300, 75x300 and 200x1200 give no clean box size at all.

**Rule 3 applies: nothing is loaded until Eternity sends m²/box, pcs/box and kg/box per code** (same format as `store-content/pricing/DSA-trade-price-request-2026-10-14.txt`). The file `eternity-porcelain-tile-codes-2026-11-09.xlsx` on the owner's drive (`Eternity/README.md:29-31`) may already hold it; check that first. Everything below is built so that the box sheet is the only input; the one worked example uses 1.44 and is marked unverified.

---

## A. Data model per variant

Inputs per SKU (from the box sheet): `m2_per_box` (2 dp), `kg_per_box` (or kg/m² x m²/box if missing), optional `pcs_per_box`.

| Field | Today (0.01 unit) | After (box) | Rule |
|---|---|---|---|
| `price` | $/m² ÷ 100 | `$/m² x m2_per_box`, 2 dp half-up | The owner's whole-dollar $/m² does not change. With m²/box to 2 dp the box price is exact cents, so Shopify's `unit_price` (= price ÷ quantityValue) shows the owner's $/m² exactly. Example: $50 x 1.44 = $72.00, 72.00 ÷ 1.44 = $50.00. |
| `unitPriceMeasurement` | 0.01 M2 per 1 M2 | `{quantityValue: m2_per_box, quantityUnit: M2, referenceValue: 1, referenceUnit: M2}` | Same shape as `tile_m2_units_2026_11.py:49`, only the number changes. `showUnitPrice: true` stays. |
| `inventoryItem.cost` | cost/m² ÷ 100 (Shopify rounds to the cent, so admin margins are off by up to $0.50/m² today) | `cost_m2 x m2_per_box`, 2 dp | Inc GST, from the master list `cost` column. Fixes the rounding problem. |
| weight | kg/m² ÷ 100 | `kg_per_box` from the sheet; else `stored_weight x 100 x m2_per_box` | Stored weights are formula estimates (22 kg/m² porcelain, 15 ceramic, `store-content/shipping/estimate_weights.py:55-59`); prefer the supplier figure. |
| inventory | on hand in 0.01 m² units | boxes = `floor(on_hand ÷ (100 x m2_per_box))` | Only for tracked variants. Read `inventoryQuantity` per variant first (the pre-change snapshot); write with `inventorySetQuantities(input:{reason:"correction", name:"available", quantities:[{inventoryItemId, locationId:"gid://shopify/Location/77786087487", quantity:N}]})`. Report any remainder (part boxes) to the owner. |
| tags | `m2-units` | **remove `m2-units`, add `box-units`** | One tag flip per product, in the same request as the variant update, so theme mode and data never disagree. Theme files gain a `box-units` branch; the `m2-units` branches stay until a cleanup after the switch. |
| `shipping.box_size` | derived from tile size | unchanged | Out of scope; note the Subwave 64x64 error for the shipping pass. |
| `ets.trade_band`, `trade-list-N` collections | unchanged | unchanged | Bands do not move. |
| `custom.trade_price` (variant) | trade per 0.01 unit | trade per box | Same number as the price list (section B). |
| `ets.trade_price` (product) | "$45.00 per m² (10% off)" | same per-m² text, computed as trade per box ÷ m2_per_box | Admin record stays per m². |

### Mutation shapes (new script `store-content/pricing/tile_box_units_2026_11.py`, `batches()` copied from `tile_m2_units_2026_11.py:38-61`)

Input: `pages/p*.json` (same products query as `trade_price_metafields_2026_11.py:3-5`, plus `inventoryItem{id unitCost{amount} measurement{weight{value unit}}} inventoryQuantity unitPriceMeasurement{quantityValue}`) and `box-sizes.csv` (`sku,m2_per_box,pcs_per_box,kg_per_box`). Any SKU missing from the CSV stops the script with its name printed; nothing is guessed.

One part per product, aliases, chunked under 15,500 chars exactly as today (limit 16,384):

```graphql
mutation {
  p0: productVariantsBulkUpdate(productId: "gid://shopify/Product/…", variants: [
    {id: "gid://shopify/ProductVariant/43966816452671", price: "79.20", showUnitPrice: true,
     unitPriceMeasurement: {quantityValue: 1.44, quantityUnit: M2, referenceValue: 1, referenceUnit: M2},
     inventoryItem: {cost: "51.48", measurement: {weight: {value: 31.68, unit: KILOGRAMS}}}},
    {id: "…", price: "…", …}
  ]) { userErrors { field message } }
  t0: tagsAdd(id: "gid://shopify/Product/…", tags: ["box-units"]) { userErrors { message } }
  u0: tagsRemove(id: "gid://shopify/Product/…", tags: ["m2-units"]) { userErrors { message } }
  p1: … t1: … u1: …
}
```

(Values above are the BS600331 row with 1.44 m²/box: $55 x 1.44 = 79.20, cost 35.75 x 1.44 = 51.48, 22 kg/m² x 1.44 = 31.68; illustrative only until the sheet confirms 1.44.)

Python for the variant string (replaces `tile_m2_units_2026_11.py:49-50`):

```python
box = D(sizes[v["sku"]]["m2_per_box"])                        # KeyError = stop, never invent
price = (m2_price * box).quantize(C, ROUND_HALF_UP)            # m2_price = whole-dollar $/m² = today's price x 100
cost  = (cost_m2 * box).quantize(C, ROUND_HALF_UP)
kg    = sizes[v["sku"]].get("kg_per_box") or round(w["value"] * 100 * float(box), 2)
vs.append('{id:"%s",price:"%s",showUnitPrice:true,unitPriceMeasurement:{quantityValue:%s,quantityUnit:M2,referenceValue:1,referenceUnit:M2},inventoryItem:{cost:"%s",measurement:{weight:{value:%s,unit:%s}}}}'
          % (v["id"], price, box, cost, kg, w["unit"]))
parts.append('p%d: productVariantsBulkUpdate(productId:"%s",variants:[%s]){userErrors{field message}} t%d: tagsAdd(id:"%s",tags:["box-units"]){userErrors{message}} u%d: tagsRemove(id:"%s",tags:["m2-units"]){userErrors{message}}' % (...))
```

Inventory is a second, separate batch file (`inv_NN.graphql`, `inventorySetQuantities`, 100 quantities per call) generated by the same script from the snapshot, so it can be skipped for untracked variants. The script also writes `tile-box-proposal.csv` (section D) and a `rollback_NN.graphql` set from the snapshot (section E). Self-check at the top: `assert box_row(D(55), D("35.75"), D("1.44"), 10) == (D("79.20"), D("51.48"), D("71.28"))`.

---

## B. Trade (B2B price list)

**Rule: trade price per box = box price x (1 − band/100), rounded UP to the cent** (ROUND_CEILING, as the scripts already do for tagged tiles). Rounding up means the discount can never exceed the band, so the 15% tile cap holds; and a trade price that is only ever rounded up cannot fall under the floor if the unrounded one clears it. The per-m² equivalent is `trade_per_m2 x m2_per_box` with trade_per_m2 = $/m² x (1 − band/100).

What changes for trade customers: today the ceiling is applied to a 1-cent unit, which pushed several lines above the band (a $37 tile at band 10 is $34/m² today, 8.1% off, not $33.30). Per box the true band applies: $37 x 1.44 = $53.28 → $47.96 a box = $33.31/m². Trade prices move down by up to $0.70/m² on the $37, $42, $46 and $55 lines; the $50/$45/$63 lines are unchanged. Margins per m² (unchanged by the box multiplier) after the change, lowest first: $63 band 15 → $53.55 vs cost $40.15 = 25.0% (holds, just); $46 band 15 → 25.4%; all others 26% or better. No variant breaks the 25% trade floor or the 25% public floor (public margins are untouched: 34.5% to 39.3%).

If the owner would rather keep today's whole-dollar trade $/m² exactly (nothing moves for trade customers), the script takes `trade_per_m2` from the master list instead of the band formula; same mutation, same rounding. Recommendation: use the band formula (it is the playbook formula, section 4) and let the small drop happen.

Script changes:

- `store-content/pricing/b2b_price_list_2026_11.py:27`: `"m2-units"` → `"box-units"` (keeps ROUND_CEILING for box tiles; half-up for everything else). Docstring line 7 add "box tiles: rounded up". Output unchanged: `priceListFixedPricesAdd`, 90 prices per file (< 100 cap), `assert len(q) < 16000`, compareAtPrice = box price. 84 prices → 1 file.
- `store-content/pricing/trade_price_metafields_2026_11.py`: line 5 query adds `unitPriceMeasurement{quantityValue}` to the variant fields; line 25 `"m2-units"` → `"box-units"`; line 27 unchanged (ceiling); line 32 becomes `if m2: lo, hi = (lo / qv).quantize(C), (hi / qv).quantize(C)` with `qv = Decimal(v["unitPriceMeasurement"]["quantityValue"])` collected per variant (use min/max of `tp/qv`, not `tp` min ÷ one qv, because sizes in one product can have different box sizes); line 34 " per m²" stays. `custom.trade_price` = per-box trade price (number). 25 metafields per `metafieldsSet`, < 16,000 chars, unchanged.
- Verify with `contextualPricing` for `gid://shopify/CompanyLocation/7315980351` on three variants (one per box size), as playbook 5.3.5.

---

## C. Theme (draft only; CLAUDE.md rule 4)

Mode switch: `product.tags contains 'box-units'` (products) / `item.product.tags contains 'box-units'` (cart). The `m2-units` branches stay in place so the live theme keeps working for untouched products until the data flip; delete them in a follow-up sync once no product carries `m2-units`. The box size is read from `variant.unit_price_measurement.quantity_value` (Liquid) / `item.unit_price_measurement.quantity_value` (cart.js), never hard-coded, because sizes in one product can differ per variant. Never multiply by 100 in box mode.

| File | Change |
|---|---|
| `theme/snippets/ets-pdp-calc.liquid` | :16 add `{% if product.tags contains 'box-units' %} data-box="{{ product.selected_or_first_available_variant.unit_price_measurement.quantity_value }}"{% endif %}` (Horizon re-renders the section on variant change, so the attribute follows the selected size). :24-31 replace the `<select data-waste>` with `<label class="ets-calc__waste"><input type="checkbox" data-waste value="15" checked> Add 15% wastage</label>` (owner's ask, Gia's default). :33-36 output text and button come from JS. :37-41 add a `box-units` branch first: `Sold by the box ({{ product.selected_or_first_available_variant.unit_price_measurement.quantity_value }} m² per box). We round up to the nearest full box. Keep a few spare for future repairs.` |
| `theme/assets/ets-2026.js` | :183 `const waste = c.waste.type === 'checkbox' ? (c.waste.checked ? 15 : 0) : parseFloat(c.waste.value); const need = a * (1 + waste / 100);` :185-189 add box branch: `if (calc.dataset.box) { const box = parseFloat(calc.dataset.box) || 1; const boxes = Math.ceil(need / box - 1e-6); const m2 = (boxes * box).toFixed(2); calc.dataset.qty = boxes; c.out.textContent = `${boxes} box${boxes === 1 ? '' : 'es'} · ${box} m² per box · ${m2} m²`; c.apply.textContent = `Set quantity to ${boxes} box${boxes === 1 ? '' : 'es'}`; }` else the existing two branches. :208 `const qty = 'm2' in calc.dataset ? calc.dataset.qty : parseInt(calc.dataset.qty, 10);` already gives an integer for box mode; :211 the `[data-ets-m2-qty]` lookup finds nothing for box products (the m² input only renders for `m2-units`), so `input[name="quantity"]` is used: no change. :217 button text: `${qty} ${calc.dataset.box ? 'box' + (qty == 1 ? '' : 'es') : 'm²'}`. :222-232 and :117-118 unchanged now (they key on `data-ets-m2-qty` and `=== 0.01`, both absent for box products, so boxes count as real items); delete in the cleanup. Port of Gia's logic (Report 4 section 5) is this one `Math.ceil(need / box)` line; the rest of Gia's script (global selectors, variant-change listener, toggle styling) is not needed because Horizon re-renders and our listeners are delegated. |
| `theme/snippets/quantity-selector.liquid` | Box products fall through to the normal stepper (ets_m2 is false). Add after :60's component on the product page only: `{% if line_index == null and product.tags contains 'box-units' and variant.unit_price_measurement %}<span class="ets-box-hint">{{ variant.unit_price_measurement.quantity_value }} m² per box</span>{% endif %}`. Remove :33-37, :44-59, :87 `100` and CSS :203-219 in the cleanup. |
| `theme/snippets/price.liquid` | After :29 add: `assign ets_box = false if product_resource.tags contains 'box-units' and selected_variant.unit_price_measurement: assign ets_box = true; assign ets_box_m2 = selected_variant.unit_price_measurement.quantity_value; assign price = selected_variant.unit_price | money (currency variant as :26); if compare_at_price: assign compare_at_price = selected_variant.compare_at_price | divided_by: ets_box_m2 | round | money`. :48-51 for cards: `if ets_box and price_min: loop product_resource.variants, take min variant.unit_price → price_min/price_max` (so "From" shows the cheapest $/m², not the cheapest box). :82-93 B2B: `if ets_box: ets_trade = selected_variant.unit_price; ets_retail = selected_variant.compare_at_price | divided_by: ets_box_m2 | round; ets_save = ets_retail − ets_trade` (confirm in preview as the test company that `unit_price` follows the catalog price; if it does not, use `selected_variant.price | divided_by: ets_box_m2 | round`). :104 and :125 " / m²" now label a per-m² figure in box mode, so they stay; they are only wrong if the ×100 and per-m² assignments are skipped, which is why the ets_box block must run before them. After :125 add, product page only: `{% if ets_box and is_product_card != true %}<span class="ets-price__box">{{ selected_variant.price | money }} per box · {{ ets_box_m2 }} m²</span>{% endif %}`. :126 guard becomes `and ets_x == 1 and ets_box == false` (we already print $/m²; Shopify's own line would duplicate it). |
| `theme/blocks/_featured-product-price.liquid` | :9-12 add `elsif product.tags contains 'box-units'`: loop `product.variants`, `ets_price_min` = smallest `variant.unit_price`. |
| `theme/snippets/cart-products.liquid` | :148-153 add `assign ets_box = false; if item.product.tags contains 'box-units' and item.unit_price_measurement: assign ets_box = true; assign ets_box_m2 = item.unit_price_measurement.quantity_value`. :310-344 in box mode: price shown = `item.unit_price | money` + " / m²" (sale/compare-at: `item.variant.compare_at_price | divided_by: ets_box_m2 | round | money`), then a second line `{{ item.original_price | money }} per box`. :363-366 add box branch: `<span class="ets-m2-cartqty cart-primary-typography">{{ item.quantity }} box{% if item.quantity != 1 %}es{% endif %} · {{ ets_box_m2 }} m² per box · {{ item.quantity | times: ets_box_m2 | round: 2 }} m²</span>` (this is Gia's drawer text done in Liquid; Horizon re-renders the drawer on every quantity change, so no JS or MutationObserver). :367-377 quantity selector stays visible for box lines (+/− change boxes). :413 line total unchanged. :430-434 native unit-price block: add `and ets_box == false` (same duplication reason). Drawer grid CSS :525-560 already has the `unit_price` area. |
| `theme/snippets/cart-drawer.liquid:80-89`, `theme/snippets/cart-bubble.liquid:13-21,28`, `theme/sections/ets-header.liquid:79-88`, `theme/assets/cart-icon.js:62-70` | No change now: box lines are not tagged `m2-units` and have quantity_value ≠ 0.01, so they count as boxes already. Delete the special cases in the cleanup. |
| `theme/snippets/product-card.liquid:25-31`, `theme/blocks/_product-card-gallery.liquid:39-44` | No change: the quick-add block is keyed on `m2-units`, so box products get quick add (adds 1 box, which is sensible). |
| `theme/snippets/ets-product-schema.liquid:176-185` | Add `elsif product.tags contains 'box-units'` before the m2-units branch: `"price": {{ variant.price | divided_by: 100.0 | json }}` (what one unit sold costs = a box), `"priceSpecification": { "@type": "UnitPriceSpecification", "price": {{ variant.unit_price | divided_by: 100.0 | json }}, "priceCurrency": …, "referenceQuantity": { "@type": "QuantitativeValue", "value": 1, "unitCode": "MTK" } }, "eligibleQuantity": { "@type": "QuantitativeValue", "value": {{ variant.unit_price_measurement.quantity_value }}, "unitCode": "MTK" }`. |
| Checkout | No theme control (Grow). It shows "2 x $79.20" and Shopify's "$55.00/m²". The "x 288" oddity from README.md:125 goes away. |
| `README.md` (root) | New dated entry; fix the stale "Last synced" line (:9). |

Not touched: `theme/sections/ets-product-story.liquid` (old calculator, not in any template), `theme/sections/ets-flagship-header.liquid` (not in `header-group.json`). Stock Horizon files (`snippets/unit-price.liquid`, `quick-add-modal.liquid`, cart quantity JS) are not in the repo and need no edit.

Line-item properties `_area_m2` / `_wastage` (Gia's) are skipped: nothing reads them. Add later if the owner wants the customer's typed area on the order.

---

## D. Owner's approval table (built by the script, nothing written until "yes")

One row per variant, 84 rows, in `store-content/pricing/reports/tile-box-proposal-2026-11.csv`:

`product,variant,sku,vid,m2_per_box,pcs_per_box,kg_per_box,price_m2,old_unit_price,new_box_price,cost_m2,new_box_cost,public_margin_pct,band,old_trade_m2,new_trade_box,new_trade_m2,trade_margin_pct,eff_discount_pct,on_hand_units,on_hand_boxes,remainder_units,flag`

Rows whose SKU is missing from the box sheet get `m2_per_box = UNKNOWN` and empty price columns; the batch is not generated while any row is UNKNOWN.

What the owner sees (plain words): the $/m² a customer pays does not change. The cart now charges per box. Example rows **if Eternity confirms 1.44 m² per box** (unverified today):

| Tile | $/m² today | Box | Box price | Box cost | Public margin | Band | Trade per box | Trade per m² (today) | Trade margin |
|---|---|---|---|---|---|---|---|---|---|
| Time Stone Moon 600x600 Lappato (BS600331) | $55.00 | 1.44 m² | $79.20 | $51.48 | 35.0% | 10% | $71.28 | $49.50 ($50.00) | 27.8% |
| Time Stone Moon 300x600 Matt (YFR630331) | $50.00 | 1.44 m² | $72.00 | $46.73 | 35.1% | 10% | $64.80 | $45.00 ($45.00) | 27.9% |
| Cement White 600x600 (DSA66MQ01) | $37.00 | 1.44 m² | $53.28 | $34.85 | 34.6% | 10% | $47.96 | $33.31 ($34.00) | 27.3% |
| Lava Vesuv 600x1200 Gloss (YW277314) | $63.00 | 1.44 m² | $90.72 | $57.82 | 36.3% | 15% | $77.12 | $53.56 ($54.00) | 25.0% |

Every one of the 84 variants clears both floors (public 25%, trade 25%) because the margin per m² is unchanged; the lowest is the three $63 lines at 25.0% trade. Trade band cap 15% holds by the round-up rule. Owner approves the CSV as a whole or strikes rows.

---

## E. Order of operations, preview, publish, rollback

1. **Box sheet.** Ask Eternity (or open `eternity-porcelain-tile-codes-2026-11-09.xlsx` on the owner's drive) for m²/box, pcs/box, kg/box per code. Save as `store-content/pricing/box-sizes-2026-11.csv`. Note the SKU differences in Report 3 (ET- vs DSA- prefixes, DSA365G vs DSA36SG, Astra codes swapped on Eternity's site) when matching.
2. **Snapshot.** Query the 43 products (price, cost, weight, unitPriceMeasurement, tags, inventoryQuantity, inventoryItem id) into `pages/p*.json`; commit as the rollback source.
3. **Proposal.** Run `tile_box_units_2026_11.py pages/p1.json` → `tile-box-proposal-2026-11.csv`. Any UNKNOWN row stops here.
4. **Draft theme.** Confirm the live theme with `themes(first:5, roles:[MAIN]){nodes{id name}}`; duplicate the newest draft **145261363263** ("Christmas closure notice") with `themeDuplicate(id:"gid://shopify/OnlineStoreTheme/145261363263", name:"ETS 2026 – Tiles by the box (draft)")` so the owner does not merge two drafts. Apply section C with `themeFilesUpsert` on the copy only. Sync the edited files into `theme/`.
5. **Preview on today's data.** `https://excellenttilingservices.com/products/<any live tile handle>?preview_theme_id=<new id>` must look exactly as live (m2-units branches untouched). Check cart drawer and cart page with a tile line.
6. **One-tile test (owner approves this single row first).** Use the DRAFT product Time Stone Sand (BS630332, status DRAFT, not for sale): run its one `productVariantsBulkUpdate` + tag flip. Open the theme preview once (sets the preview cookie), then Shopify admin → Products → Time Stone Sand → Preview. Check: price "$55.00 / m²" with "$79.20 per box · 1.44 m²" under it (numbers per the sheet), the calculator (12.5 m² with wastage ticked → 10 boxes · 1.44 m² per box · 14.40 m²), add to cart, drawer line "10 boxes · 1.44 m² per box · 14.40 m²", +/− works, header count = 10, checkout shows $/m², schema JSON, and the test company login (`gid://shopify/Company/6510116927`) sees the trade price per m². If the draft product 404s in preview, do the test on one live tile in the 15 minutes before step 8 instead. Screenshot 1440 and 390.
7. **Owner approves the full CSV** (rule 1).
8. **Publish the draft theme** (owner: Shopify admin → Online Store → Themes → "ETS 2026 – Tiles by the box (draft)" → Publish). The m2-units branches keep the live products correct while step 9 runs.
9. **Variants.** Run the `box_NN.graphql` batches straight after (`graphql_mutation`, check every `userErrors`). Then `inv_NN.graphql` for tracked variants.
10. **Trade.** Re-query pages → `b2b_price_list_2026_11.py` → run `pl/pl01.graphql`; `trade_price_metafields_2026_11.py` → run `reqNN.graphql`; verify three variants with `contextualPricing` as `CompanyLocation/7315980351`.
11. **Records.** Master list `store-content/pricing/store-pricing-2026-10-03.csv`: keep per-m² `new_price`/`trade_price`/`cost`, add columns `m2_per_box, box_price, box_cost, trade_box`, rewrite the tile `flag` text to "per m2; sold by the box (tag box-units), Shopify price = this x m2_per_box (date)"; add the 3 draft rows if they go live. Rerun `price_list_pdf.py` (no code change; footer already says "sold to the nearest full box"). Rewrite `PRICING-PLAYBOOK.md:31-32` and `store-content/pricing/README.md:314-347` ("New tiles from now on": price per m² whole dollars x m²/box, cost x m²/box, kg/box, unit price measure m²/box M2 / 1 M2, tag `box-units`, then both trade scripts). Dated entries in root `README.md` and `store-content/pricing/README.md`. Commit, push.
12. **Cleanup (later, separate draft):** delete the `m2-units` branches and the cart-count special cases once `products(query:"tag:m2-units")` returns nothing.

Preview URL pattern: `https://excellenttilingservices.com/products/<handle>?preview_theme_id=<theme id>` (cart: `/cart?preview_theme_id=…`).

**Rollback.** Theme: Online Store → Themes → publish the previous theme again (the one that was live before step 8). Data: the script writes `rollback_NN.graphql` from the step-2 snapshot (price, unitPriceMeasurement 0.01, cost, weight, `tagsAdd m2-units` + `tagsRemove box-units`, and `inventorySetQuantities` back to the snapshot units); run them, then rerun both trade scripts. Because the theme is keyed on the tag, data rollback alone is safe even under the new theme.

---

## F. Risks

1. **Carts in flight.** A cart holding 288 x $0.55 units at the moment of step 9 becomes 288 boxes x $79.20. Shopify reprices lines at checkout from the current variant price. Mitigation: run step 9 in a quiet hour, check `draftOrders`/abandoned checkouts created in the previous 48 h for tile lines, and email those customers; orders already placed are unaffected.
2. **Order history and reports.** Past orders keep quantity in 0.01 units (288 = 2.88 m²); new ones are boxes. Sales-by-quantity reports mix units across 5 Nov to the switch date. Note it in the README; fulfilment must read quantity as boxes from the switch.
3. **Inventory.** On hand is in 0.01 units today. If tracking is on, the figure must be converted (A) or oversells/undersells follow. Part boxes are reported, not rounded silently. If tracking is off ("continue selling"), nothing to do. Confirm per variant from the snapshot.
4. **Google Shopping feed / Merchant Center.** The feed takes `price` = box price; the title/description must say "per box (1.44 m²)" or the ad shows $79.20 against competitors' $/m². Check which feed app or channel is installed and whether it supports `unit_pricing_measure` (Shopify's channel sends unit price when `showUnitPrice` is set). Expect a reprice flag on 84 offers.
5. **eBay listings.** Tag `ebay-pickup-only` exists on some products; if any tile is synced to eBay, the listing quantity and price flip to boxes and need their own title/quantity fix in the eBay app. List them first (`products(query:"tag:ebay-pickup-only tag:m2-units")`).
6. **Shopify unit price rounding.** `unit_price` = price ÷ quantityValue to the cent. Whole-dollar $/m² x m²/box with 2-dp box sizes is exact; a box size with more decimals (e.g. 1.0368 m²) would show a $/m² a few cents off. The script asserts `price / box == m2_price` and flags any SKU where it does not.
7. **B2B unit price.** Whether `variant.unit_price` follows the catalog price for trade logins is unverified; price.liquid has the fallback (compute from `price ÷ quantity_value`). Test in step 6.
8. **Trade price moves.** Section B: trade $/m² drops by up to $0.70 on several lines. The owner must see this in the table before saying yes.
9. **Draft-product preview.** If Shopify will not show the DRAFT test tile in theme preview, the test moves to one live tile for a few minutes (step 6 fallback).
10. **Cut-over window.** Theme published before data: box branches idle, nothing changes. Data before theme: impossible by order of steps; if it happened, the live theme would show "$79.20 / m²" (price.liquid:104/125 suffix on a box price). Keep steps 8 and 9 within minutes of each other.
11. **Descriptions.** All 43 say "Sold per square metre and supplied to the nearest full box" (fine). Time Stone Moon/Charcoal say "Box coverage: 1.44 m²"; if the sheet gives a different size, fix those two lines.
12. **Weights.** Stored weights are estimates; shipping rates by weight change by the box multiplier only if kept, or to supplier kg/box if provided. Either way check one shipping quote after the switch.

One recommendation: get the box sheet from Eternity first; until it arrives nothing can be priced per box, and the theme draft (steps 4 and 5) is the only work that can start now.