## Gia's per-box model — reference implementation (read-only findings)

Source files (scratchpad, not repo):
- `/tmp/claude-0/-home-user-Excellent-Tiling-Services-/ac4a4452-2d4f-5624-ba9e-201d16c6b52f/scratchpad/gias/castella.html` (saved PDP, 4,8xx lines)
- `/tmp/claude-0/-home-user-Excellent-Tiling-Services-/ac4a4452-2d4f-5624-ba9e-201d16c6b52f/scratchpad/gias/js/castella-grey-matte.json` (`/products/<handle>.js`)

**Theme correction:** Gia's theme is **Polyform 4.2.0** (`castella.html:55` — `Shopify.theme = {"name":"GBAT - Live Theme - BLACK FRIDAY","schema_name":"Polyform","schema_version":"4.2.0"}`), not Horizon/Dawn. Tailwind-style utility classes, `<product-form>`, `<variant-selects>`, `<cart-drawer>`, `<quantity-input>` custom elements. Our theme is Horizon-based ("ETS Premium", `README.md:7`), so every DOM hook below needs mapping (section 7).

---

### 1. Data model (variant JSON) — `castella-grey-matte.json`

One variant = one box. Shopify `price` = box price. Unit price metadata carries m² per box.

| Variant | `price` (box) | `compare_at_price` | `unit_price` | `unit_price_measurement` | `weight` (g) |
|---|---|---|---|---|---|
| 300×300 (id 43677974659169) | 5040 ($50.40) | 5600 | 5040 | `{"measured_type":"area","quantity_value":"1.0","quantity_unit":"m2","reference_value":1,"reference_unit":"m2"}` | 17800 |
| 300×600 (id 43677974691937) | 7258 ($72.58) | 8064 | 5040 | `quantity_value:"1.44"`, rest identical | 33400 |
| 600×600 (id 43677974724705) | 7258 | 8064 | 5040 | `quantity_value:"1.44"` | 33400 |

- `unit_price` is Shopify-computed: `price / quantity_value * reference_value` → 7258/1.44 = 5040 ($50.40/m²). Storefront shows $/m², cart charges per box.
- `quantity_rule: {min:1, max:null, increment:1}` — plain whole boxes, no quantity rules trick.
- Tags: `["area-selector","Samples","Tiles","trade-program-10"]`. `area-selector` is the product tag that (by name) gates the stepper; the tag string does not appear anywhere in the rendered HTML outside the JSON, so gating is done in Liquid, not JS.
- Weight = kg per box (17.8 kg for 1 m² box, 33.4 kg for 1.44 m² box).
- Across the 180 saved `js/*.json` files: every tile has tag `area-selector`; `quantity_value` is one of `1.0`, `1.2`, `1.44` per variant (varies per size within a product, e.g. `gloss-white-rectified.json` 1.44 and 1.2). Some tiles have `unit_price_measurement: null` (e.g. `bricks-aqua-gloss.json`, `frammenti-nero-brick.json`) — the JS then falls back to 1 m²/box. Non-tiles (tapware, accessories) have no unit price and no tag.

**Admin GraphQL equivalent for us (per variant):** `price` = box price; `unitPriceMeasurement { measuredType: AREA, quantityUnit: M2, quantityValue: <m² per box>, referenceUnit: M2, referenceValue: 1 }`; `inventoryItem.measurement.weight` = kg per box.

---

### 2. PDP price display — `castella.html:3290-3312`

The main price block prints **only the unit price** (per m²), never the box price. Sale shown as struck-through unit compare price:

```html
<div class="mt-16 md:mt-32" id="price-template--21554094080097__main" role="status">
  <div class="price flex flex-wrap gap-12 h4 font-body price-on-sale price-show-badge">
    <div class="price__container"><p class="mt-4 block">
      <span class="visually-hidden">Unit price</span>
      <span class="price-item text-p text-light-subdued">
        <s>$56.00 <span aria-hidden="true">/</span>m<sup>2</sup></s>
      </span>
      <span class="price-item price-item-last">
        <span>$50.40</span>
        <span aria-hidden="true">/</span>
        <span class="visually-hidden">&nbsp;per&nbsp;</span>
        <span>m<sup>2</sup></span>
      </span></p></div>
    <span class="price-badge-sale ...">save 10%</span>
```
- Compare-at unit price is `compare_at_price / quantity_value` ($80.64/1.44 = $56.00), computed in Liquid (Shopify only exposes `unit_price`, not a compare-at unit price).
- Klaviyo "Viewed Product" (`castella.html:387`) sends `Price: "$50.40"` (unit) but `CompareAtPrice: "$80.64"` (box) — a bug on their side, don't copy.

### 3. Product card price — `castella.html:1162-1172` (recommended-products cards, `.product-card` at :1008/:1113/:1968/:2073)

```html
<p class="block font-bold">
  <span class="visually-hidden">Unit price</span>
  <s class="text-light-subdued font-normal text-caption">$56.00 <span aria-hidden="true">/</span>m<sup>2</sup></s>
  <span>
    <span>$50.40</span>
    <span aria-hidden="true">/</span>
    <span class="visually-hidden">&nbsp;per&nbsp;</span>
    <span>m<sup>2</sup></span>
  </span>
</p>
```
Same pattern: card shows unit price of the first/cheapest variant, "/m²", no box price, no "from".

---

### 4. "Area in m²" stepper markup — `castella.html:3531-3608`

Lives inside the product-info column, outside the `<form>`; all inputs bind to the form via `form="product-form-<section id>"`. Cleaned:

```html
<div class="quick-view-remove mt-32 js-product-form-input">
  <label class="visually-hidden" for="Quantity-{{ section.id }}">Area in m²</label>

  <div class="flex items-center gap-16 flex-wrap"
       data-m2-per-box="{{ m2_per_box }}"            {# 1.0 / 1.2 / 1.44 — current variant's quantity_value #}
       data-section-id="{{ section.id }}">

    <span class="text-p-small font-bold">Area</span>

    <div class="area-m2-stepper inline-flex border rounded-button overflow-hidden">
      <button type="button" class="area-m2-minus" aria-label="Decrease area by 1 m²">−</button>
      <div class="flex items-center gap-4 px-12">
        <input class="area-m2-input" type="number" inputmode="decimal"
               min="0.01" step="0.01" value="{{ m2_per_box }}" aria-label="Area in m²">
        <span>m²</span>
      </div>
      <!-- the real quantity (boxes), hidden, submitted with the form -->
      <input class="area-qty-input" type="number" name="quantity"
             id="Quantity-{{ section.id }}" data-cart-quantity="" data-min="1" min="1" step="1"
             value="1" form="product-form-{{ section.id }}" style="display:none;">
      <button type="button" class="area-m2-plus" aria-label="Increase area by 1 m²">+</button>
    </div>

    <label class="flex items-center gap-8 cursor-pointer select-none" aria-label="Add 15% wastage">
      <div style="position:relative;width:36px;height:20px;flex-shrink:0;">
        <input type="checkbox" class="area-wastage-checkbox"
               style="opacity:0;position:absolute;width:0;height:0;" aria-label="Add 15% wastage">
        <div class="area-wastage-track" style="position:absolute;inset:0;border-radius:999px;background:#ccc;transition:background .2s;"></div>
        <div class="area-wastage-thumb" style="position:absolute;top:2px;left:2px;width:16px;height:16px;border-radius:50%;background:#fff;transition:transform .2s;pointer-events:none;box-shadow:0 1px 3px rgba(0,0,0,.2);"></div>
      </div>
      <span class="text-p-small whitespace-nowrap">Add 15% wastage</span>
    </label>
  </div>

  <p class="mt-8 text-p-small area-m2-note">
    We round up to the nearest full box ({{ m2_per_box }} m² per box).
  </p>
</div>

<div class="quantity__rules caption no-js-hidden"></div>

<!-- hidden line-item properties, posted with /cart/add -->
<input type="hidden" name="properties[_wastage]" id="wastage-property-{{ section.id }}" value="false" form="product-form-{{ section.id }}">
<input type="hidden" name="properties[_area_m2]"  id="area-m2-property-{{ section.id }}"  value="{{ m2_per_box }}" form="product-form-{{ section.id }}">
```
Notes: the minus/plus buttons step by **one box's worth of m²** (aria text says "1 m²" but JS uses `m2PerBox`). The toggle is a hand-rolled switch with inline styles (track colour `#64788c` when on). The `area-wastage-checkbox` has no `name`, so it is not posted — the hidden `_wastage` input carries it.

**Line-item properties: yes, posted.** `properties[_wastage]` = "true"/"false", `properties[_area_m2]` = the entered m² (before wastage, e.g. "12.5"). Underscore prefix hides them from the cart/checkout UI but they land on the order line. The product form itself (`castella.html:3726`) is standard: `<form method="post" action="/cart/add" id="product-form-…" data-type="add-to-cart-form">` with `name="id"` hidden input + `product-id` + `section-id`.

---

### 5. PDP inline JS (m² → boxes) — `castella.html:3610-3717`, cleaned

```js
(function () {
  var wrapper = document.querySelector('.area-m2-stepper');
  if (!wrapper) return;

  var container   = wrapper.closest('[data-m2-per-box]');
  var m2PerBox    = parseFloat(container.getAttribute('data-m2-per-box')) || 1;
  var m2Input     = wrapper.querySelector('.area-m2-input');
  var qtyInput    = wrapper.querySelector('.area-qty-input');      // name="quantity", hidden
  var minusBtn    = wrapper.querySelector('.area-m2-minus');
  var plusBtn     = wrapper.querySelector('.area-m2-plus');
  var wastageChk  = document.querySelector('.area-wastage-checkbox');
  var track       = document.querySelector('.area-wastage-track');
  var thumb       = document.querySelector('.area-wastage-thumb');
  var note        = document.querySelector('.area-m2-note');
  var wastageProp = document.getElementById('wastage-property-SECTION_ID');
  var areaProp    = document.getElementById('area-m2-property-SECTION_ID');

  // Liquid: {{ product.variants | json }} — needs unit_price_measurement.quantity_value per variant
  var productVariants = PRODUCT_VARIANTS_JSON;

  function getWastage() { return wastageChk && wastageChk.checked ? 1.15 : 1; }

  function m2ToBoxes(m2) { return Math.ceil((m2 * getWastage()) / m2PerBox); }

  function updateNote(m2) {
    if (!note) return;
    var b = m2ToBoxes(m2);
    var txt = 'We round up to the nearest full box (' + m2PerBox + ' m² per box) — '
            + b + ' box' + (b !== 1 ? 'es' : '') + ' needed.';
    if (wastageChk && wastageChk.checked) txt += ' (incl. 15% wastage)';
    note.textContent = txt;
  }

  function update() {
    var m2 = Math.max(0.01, parseFloat(m2Input.value) || m2PerBox);
    qtyInput.value = m2ToBoxes(m2);
    if (areaProp) areaProp.value = m2;
    updateNote(m2);
  }

  function updateToggleUI() {
    var on = wastageChk && wastageChk.checked;
    if (track) track.style.background = on ? '#64788c' : '#ccc';
    if (thumb) thumb.style.transform  = on ? 'translateX(16px)' : 'translateX(0)';
    if (wastageProp) wastageProp.value = on ? 'true' : 'false';
  }

  function onVariantChange(variantId) {
    var variant = productVariants.find(function (v) { return v.id === parseInt(variantId); });
    if (!variant) return;
    var newM2PerBox = 0;
    if (variant.unit_price_measurement && variant.unit_price_measurement.quantity_value) {
      newM2PerBox = parseFloat(variant.unit_price_measurement.quantity_value);
    }
    if (!newM2PerBox) newM2PerBox = 1;
    m2PerBox = newM2PerBox;
    container.setAttribute('data-m2-per-box', m2PerBox);
    m2Input.value = m2PerBox;   // reset area to one box
    m2Input.step  = m2PerBox;
    update();
  }

  minusBtn.addEventListener('click', function () {
    var current = parseFloat(m2Input.value) || m2PerBox;
    m2Input.value = Math.max(0.01, Math.round((current - m2PerBox) * 100) / 100);
    update();
  });
  plusBtn.addEventListener('click', function () {
    var current = parseFloat(m2Input.value) || m2PerBox;
    m2Input.value = Math.round((current + m2PerBox) * 100) / 100;
    update();
  });
  m2Input.addEventListener('change', update);
  m2Input.addEventListener('input', update);
  if (wastageChk) wastageChk.addEventListener('change', function () { updateToggleUI(); update(); });

  // belt-and-braces: recompute boxes on submit (capture phase, before product-form.js reads the form)
  var form = document.getElementById('product-form-SECTION_ID');
  if (form) form.addEventListener('submit', function () {
    var m2 = Math.max(0.01, parseFloat(m2Input.value) || m2PerBox);
    qtyInput.value = m2ToBoxes(m2);
    if (areaProp) areaProp.value = m2;
  }, true);

  // variant switch: Polyform's variant-selects fires 'change' on the hidden input[name="id"]
  var variantInput = document.querySelector('[name="id"]');
  if (variantInput) variantInput.addEventListener('change', function () { onVariantChange(this.value); });

  update();
})();
```
Behaviour summary: boxes = ceil(m² × (1.15 if wastage) ÷ m²PerBox); `quantity` posted = boxes; `_area_m2` = raw m²; `_wastage` = "true"/"false"; note text becomes "We round up to the nearest full box (1.44 m² per box) — 9 boxes needed. (incl. 15% wastage)". Changing variant resets area to one box and changes the stepper step. The displayed price never changes with quantity (no line total on PDP).

Edge cases they left: `querySelector('.area-m2-stepper')` is global (breaks with two product forms / quick-view); `[name="id"]` is also global; wastage percent is hard-coded 1.15; the m² input accepts 0.01 (= 1 box).

---

### 6. Cart drawer script — `castella.html:4792-4826`, cleaned

```js
(function () {
  function initDrawerAreaSteppers() {
    document.querySelectorAll('quantity-input[data-m2-per-box]').forEach(function (qInput) {
      if (qInput.dataset.drawerInitialized) return;
      qInput.dataset.drawerInitialized = 'true';

      var m2PerBox = parseFloat(qInput.getAttribute('data-m2-per-box')) || 1;
      var qtyInput = qInput.querySelector('.drawer-area-qty');        // the line's quantity <input>
      var row      = qInput.closest('.drawer-area-row');
      var display  = row ? row.querySelector('.drawer-area-display') : null;  // m² figure
      var noteEl   = row ? row.nextElementSibling : null;               // "N boxes · 1.44 m² per box"

      function updateDisplay() {
        var boxes = parseInt(qtyInput.value) || 1;
        var m2    = Math.round(boxes * m2PerBox * 100) / 100;
        if (display) display.textContent = m2;
        if (noteEl) noteEl.textContent = boxes + ' box' + (boxes !== 1 ? 'es' : '') + ' · ' + m2PerBox + ' m² per box';
      }
      qtyInput.addEventListener('change', updateDisplay);
      updateDisplay();
    });
  }
  initDrawerAreaSteppers();
  // drawer re-renders its items via section rendering; re-init on every DOM swap
  var observer = new MutationObserver(initDrawerAreaSteppers);
  var drawerContents = document.querySelector('#CartDrawer-CartItems .js-contents');
  if (drawerContents) observer.observe(drawerContents, { childList: true, subtree: true });
})();
```
**Caveat:** the saved page has an empty cart ("Your cart is empty", `castella.html:4747`), so the drawer line-item Liquid markup is NOT in the file. From the JS the implied markup per line is:
```html
<div class="drawer-area-row">
  … <span class="drawer-area-display">2.88</span> m² …
  <quantity-input data-m2-per-box="{{ item.variant.unit_price_measurement.quantity_value }}">
    <input class="drawer-area-qty" type="number" value="{{ item.quantity }}" …>
  </quantity-input>
</div>
<p>2 boxes · 1.44 m² per box</p>   <!-- nextElementSibling of .drawer-area-row -->
```
Cart quantity stays in boxes (the stepper +/- changes boxes, the m² label is derived). Line price = boxes × box price, computed by Shopify.

Also present: the drawer has a `.gbat-cart-preorder-*` CSS block (`castella.html:4740-4790`) for pre-order dates — unrelated, ignore.

---

### 7. What depends on Polyform and needs a different hook in our Horizon theme

| Gia's (Polyform) | Ours (Horizon "ETS Premium") — where to hook |
|---|---|
| Stepper sits outside `<form>` and binds via `form="product-form-{{ section.id }}"` | Horizon's buy-buttons block already has `<product-form-component>` + `form id="product-form-{{ section.id }}"`; same trick works, or put the stepper inside `snippets/quantity-selector.liquid` where our `ets_m2` branch already renders an "Area (m²)" input (`theme/snippets/quantity-selector.liquid:44-58`, `data-ets-m2-qty`) and hides the real `<quantity-selector-component>` (`:59-60`). |
| `document.querySelector('[name="id"]')` `change` event for variant switch | Horizon re-renders the section via `variant:update` / `VariantUpdate` events from `variant-picker` (section rendering replaces the buy-buttons DOM). Must re-init after re-render or read `quantity_value` from the re-rendered `data-m2-per-box`. Our `theme/assets/ets-2026.js` already uses delegated listeners (`:197-230`) which survive re-renders — keep that pattern. |
| `productVariants` inlined in JS | Use `{{ product.variants | json }}` or re-render with Liquid; Horizon's product-information section already re-renders on variant change, so simplest is to emit `data-m2-per-box="{{ variant.unit_price_measurement.quantity_value }}"` in Liquid and let the re-render carry it. |
| `quantity-input` custom element + `#CartDrawer-CartItems .js-contents` MutationObserver | Horizon: `<cart-drawer-component>` (`theme/snippets/cart-drawer.liquid:53`), items rendered by `snippets/cart-products.liquid` (`:147-158`, already has an `ets_x` m2-units branch per line) and `<cart-items-component>` (`cart-drawer.liquid:135`). Hook `data-m2-per-box` on the row in Liquid and listen for Horizon's `cart:update` event instead of a MutationObserver; or compute "N boxes · 1.44 m² per box" purely in Liquid (`item.quantity | times: item.variant.unit_price_measurement.quantity_value`) since Horizon re-renders the drawer on every quantity change — no JS needed. |
| Price block prints unit price only, compare-at unit price computed in Liquid | Our `theme/snippets/price.liquid:21-28` currently multiplies by 100 for `m2-units`; replace with: show `selected_variant.unit_price` (+ `compare_at_price | divided_by: quantity_value` for sale) and suffix "/m²". Existing unit-price branch at `price.liquid:126-132` (`render 'unit-price'`) is gated by `show_unit_price` — can reuse. |
| Card price "$50.40 /m²" | `theme/snippets/product-card.liquid:29` (m2-units gate), `blocks/_product-card-gallery.liquid`, `snippets/ets-card.liquid` — switch to `product.selected_or_first_available_variant.unit_price`. |
| Tag `area-selector` gates the stepper | We gate on `m2-units` tag / `settings.ets_trade_tile_types` (`theme/snippets/ets-pdp-calc.liquid:6-14`). Keep one tag; rename or reuse. |
| Line-item properties `_wastage`, `_area_m2` | Theme-agnostic: two hidden inputs with `form=` attribute; Horizon's product-form-component serialises the whole form so they post unchanged. |
| Existing ETS calculator (`ets-pdp-calc.liquid`, `ets-2026.js:172-230`: area / length×width / 0-20% waste select, "Set quantity") | Overlaps Gia's feature. Either delete it and port Gia's stepper, or keep ours and change its output from m² (×100 units) to `ceil(m² × (1+waste) / m2PerBox)` boxes — the smaller diff. Our note text at `ets-pdp-calc.liquid:37-40` ("sold per m², in steps of 0.01 m²") must change to the box wording. |
| Cart count: our header counts a tile line as 1 (`README.md:123`) | With boxes as quantity the stock Horizon count is correct again; the override can be removed. |

**Data changes implied for our 84 variants (owner approval needed, not done):** price → price per box (= $/m² × m² per box), cost → per box, weight → kg per box, `unitPriceMeasurement.quantityValue` → m² per box (we need m² per box per variant — currently not stored; supplier data or box-size metafield required), trade price list → per box, and `b2b_price_list_2026_11.py` / `trade_price_metafields_2026_11.py` reworked from "per 0.01 m² rounded up" to "per box".