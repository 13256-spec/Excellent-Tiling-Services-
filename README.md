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
- Theme: `snippets/meta-tags.liquid` gives every template its own title (≤60 chars, shop name
  only when it fits) and meta description (≤160 chars, cut at a word), fills in the pages
  Shopify leaves blank (all products, departments, blog, search, cart, 404), and outputs
  LocalBusiness + WebSite JSON-LD and HTTPS Open Graph images.
- Breadcrumbs: `snippets/ets-breadcrumbs.liquid` renders the visible trail and matching
  BreadcrumbList JSON-LD on pages, collections, articles, contact, booking, quote and trade pages
  (products use `sections/ets-product-breadcrumbs.liquid`).
- Shopify serves `sitemap.xml`, `robots.txt` and `llms.txt` itself on the custom domain; they are
  not theme files.
- The homepage tile ranges use `sections/ets-ranges.liquid` (native scroll-snap) instead of the
  Section Store slider, which pulled in the 155 KB Swiper bundle from jsDelivr.

## Booking form (Shopify Forms)

See [store-content/booking-form-shopify-forms.md](store-content/booking-form-shopify-forms.md) for the exact fields and settings. Adding the Forms block to the booking section replaces the built-in request form.
