# Excellent Tiling Services – Shopify theme

Theme source for [excellenttilingservice.com.au](https://excellenttilingservice.com.au)
(Excellent Tiling Services Pty Ltd, 17A Olga Road, Maddington WA 6109).

`theme/` holds the custom ETS files (sections, snippets, templates, CSS/JS) from the
Horizon-based "ETS Premium" theme. Stock Horizon files are not duplicated here.

## Showroom bookings

The showroom is open **by appointment only**, Monday to Saturday 4:30 pm to 9 pm (closed Sunday).

- Page: `/pages/book-appointment` (template `page.book-appointment` → section `ets-booking-page`).
- Out of the box the section uses Shopify's native contact form. Each request is emailed to
  the store's sender email with appointment type, preferred date/time, name, phone, email,
  suburb and order number.
- Open days and time slots are editable in the theme editor (Availability settings).
- To use a bookings app instead, add its app block to the "ETS showroom booking" section in
  the theme editor. When an app block is present it replaces the built-in form.

## Header menu

The live header is `sections/ets-header.liquid` (menu: Online Store → Navigation → Main menu).
Desktop behaviour lives in `assets/ets-2026.js` (`initMega`) and `assets/ets-menu.css`:

- Top-level labels are links to their collection; the chevron next to each opens its panel
  (keyboard and touch). With a mouse, resting on an item opens its panel after a short delay,
  so sweeping across the bar doesn't flash panels open.
- Panels are sized to fit the screen below the sticky header. On laptop-height screens
  (≤ 900 px tall) the moving product strip is hidden so the whole panel fits without scrolling.

## Section Store sections

Five sections from the Section Store app live in `sections/ss-*.liquid` (installed by the app;
don't hand-edit them, update them from the app instead). They're placed with ETS content and colours:

| Section | Template | Content |
|---|---|---|
| `ss-scrolling-features` | `product.json`, `collection.json` | Delivery, pickup, trade and showroom selling points |
| `ss-feature-54` | `product.json` | "Why buy from ETS" |
| `ss-collection-16` | `index.json` | Tile ranges (Morgan, Time Stone, Cement, Lava, Particle) |
| `ss-faq-17` | `page.faqs.json` | Tabbed FAQs (assign the FAQs page to the `faqs` template) |
| `ss-testimonial-8` | not placed | Needs real customer reviews first |

## Deploying

Edits are made on an unpublished copy of the live theme, previewed, then published from
Shopify admin → Online Store → Themes.

## Store content

`store-content/policies/` holds the current policy text. `shipping-policy.html` and
`contact-information.html` carry the by-appointment pickup wording and must be pasted into
Shopify admin → Settings → Policies (the API connector used here can't write legal policies).

## SEO

- `seo/generate_product_seo.py` builds every product's search title (≤60 chars) and meta
  description (≤155 chars, always mentions Perth) from the product's own specs.
  `seo/product-seo.json` is the exact set written to Shopify on 26 Sep 2026 (224 products).
- `seo/collection-seo.json` holds the titles/descriptions added to 27 collections that had none.
- Theme: `snippets/meta-tags.liquid` no longer appends the shop name to titles that already
  end in "| ETS Perth", so titles stay inside Google's display limit.

## Booking form (Shopify Forms)

See [store-content/booking-form-shopify-forms.md](store-content/booking-form-shopify-forms.md) for the exact fields and settings. Adding the Forms block to the booking section replaces the built-in request form.
