# Excellent Tiling Services – Shopify theme

Theme source for [excellenttilingservice.com.au](https://excellenttilingservice.com.au)
(Excellent Tiling Services Pty Ltd, 17A Olga Road, Maddington WA 6109).

`theme/` holds the custom ETS files (sections, snippets, templates, CSS/JS) from the
Horizon-based "ETS Premium" theme. Stock Horizon files are not duplicated here.

## Showroom bookings

The showroom is open **by appointment only**.

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
