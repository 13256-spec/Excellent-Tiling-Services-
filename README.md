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

## Structured data (schema.org)

- `snippets/meta-tags.liquid`: sitewide LocalBusiness (address, hours, contact, product range,
  30-day return policy with 15% restocking fee). Update the return policy block if the refund policy changes.
- `snippets/ets-structured-data.liquid` (rendered at the end of `meta-tags.liquid`): WebSite +
  site search (home), CollectionPage/ItemList (collections), Service (tiling services page),
  BlogPosting (articles).
- `snippets/ets-breadcrumbs.liquid`: BreadcrumbList.
- `snippets/ets-product-schema.liquid`: Product/ProductGroup for every product (images, brand,
  specs and dimensions from the `ets` metafields, price, stock, seller, return policy per offer).
  Barcodes are only output as a GTIN when they are 8/12/13/14 digits, so supplier codes in the
  barcode field no longer produce invalid GTINs.
  **Stock Horizon edit:** in `sections/product-information.liquid` (not stored here), the first
  lines

  ```liquid
  <script type="application/ld+json">
    {{ closest.product | structured_data }}
  </script>
  ```

  are replaced with `{% render 'ets-product-schema', product: closest.product %}` so each
  product page carries one product schema, not two. Redo this after a Horizon update.
- Uploaded 29 Sep 2026 to the unpublished theme "ETS 2026 – Schema for AI + search (preview)"
  (a duplicate of the live theme); publish it from Shopify admin → Online Store → Themes.
