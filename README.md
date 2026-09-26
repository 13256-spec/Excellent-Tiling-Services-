# Excellent Tiling Services – Shopify theme

Theme source for [excellenttilingservice.com.au](https://excellenttilingservice.com.au)
(Excellent Tiling Services Pty Ltd, 17A Olga Road, Maddington WA 6109).

`theme/` holds the custom ETS files (sections, snippets, templates, CSS/JS, settings) layered on
Shopify's Horizon theme. Stock Horizon files are not duplicated here.

## 2026 rebuild

A full redesign built in the unpublished theme **"ETS Rebuild 2026 (draft)"**. The live theme
is untouched until the draft is published from Shopify admin → Online Store → Themes.

- **Design system:** `assets/ets-2026.css` (tokens, components, Horizon skin) and
  `assets/ets-2026.js` (mega menu, mobile drawer, cart count, scroll reveal, product tabs,
  tile calculator). Both load from `layout/theme.liquid`. The look is a clean luxury showroom
  with warm stone surfaces, deep ink, brass accents and Instrument Serif with Manrope type.
- **Header / footer:** `sections/ets-header.liquid` and `sections/ets-footer.liquid`. The mega
  menu and mobile drawer are built from the **Main menu** (Online Store → Navigation). Top-level
  items with child links become mega panels, and collection pages use the same menu for their
  category chips.
- **Homepage sections** (all editable in the theme editor): `ets-hero`, `ets-trust`,
  `ets-categories`, `ets-product-tabs`, `ets-split`, `ets-services`, `ets-trade-band`,
  `ets-info-cards`, `ets-faq`, `ets-steps`, `ets-cta`.
- **Inner pages:** `ets-page-hero` + `ets-page-content` (generic pages), `ets-collection-hero`,
  `ets-directory` (all departments), `ets-quote-page`, `ets-trade-apply`, and the `page.delivery`
  and `page.tiling-services` (Renovations & Tiling) templates.
- **Business details** (phone, email, address, hours, Google rating, licence, warranty,
  year founded) live in Theme settings → **ETS business details**. Leave a trust field empty
  to hide it.

## Trade accounts

Tradies apply at `/pages/trade-account` (template `page.trade-account`, section
`ets-trade-apply`). The form uses Shopify's contact form, so each application is emailed to the
store with business name, ABN, trade type, licence, contact, estimated monthly spend, delivery
address and payment preference.

**To approve an applicant:** Shopify admin → Customers → find (or add) the applicant by the
email on the application → add the tag **`trade`** → Save. When they log in with that email:

- every price shows **Trade price** with retail struck through (`snippets/price.liquid` +
  `snippets/ets-trade-rate.liquid`);
- the discount applies automatically in the cart and at checkout.

| Band | Discount | Products | Checkout discount |
| --- | --- | --- | --- |
| Tiles | 20% | Product type `Tile` | "Trade price – Tiles 20%" → collection `trade-band-tiles` |
| Large items | 15% | Vanities, tallboys, baths, toilets, screens/panels, basins, sinks, mirrors, mirror cabinets | "Trade price – Large items 15%" → `trade-band-large` |
| Small items | 10% | Everything else (tapware, showers, accessories, wastes, fittings) | "Trade price – Small items 10%" → `trade-band-small` |

The three automatic discounts are limited to the **Trade customers** segment
(`customer_tags CONTAINS 'trade'`). They combine with shipping discounts only. The `trade-band-*`
smart collections are built from product type and are not published to the online store.
`trade-band-small` is defined as "not a tile or large type", so new product types fall into it
automatically.

**To change a percentage:** update the matching automatic discount in Discounts **and** the
same value in Theme settings → ETS trade pricing (the theme uses it to display the price). If
you add a new large-item product type, add it to both the `trade-band-large` rules and the
"Large item product types" theme setting, and to the NOT_EQUALS rules of `trade-band-small`.

## Showroom bookings

The showroom is open **by appointment only**, Monday to Saturday 4:30 pm to 9 pm (closed Sunday).

- Page: `/pages/book-appointment` (template `page.book-appointment` → section `ets-booking-page`).
- Out of the box the section uses Shopify's native contact form. Each request is emailed to
  the store's sender email with appointment type, preferred date/time, name, phone, email,
  suburb and order number.
- Open days and time slots are editable in the theme editor (Availability settings).
- To use a bookings app instead, add its app block to the "ETS showroom booking" section in
  the theme editor. When an app block is present it replaces the built-in form.

See [store-content/booking-form-shopify-forms.md](store-content/booking-form-shopify-forms.md)
for the Shopify Forms field setup.

## Catalogue clean-up (26 Sep 2026)

- 134 draft products checked (images, collections, description, price) and published. 195 of
  224 products are now live.
- Fixed categories: 7 kitchen mixers added to Kitchen & laundry, 3 half-inset basins to
  Semi-recessed basins, 3 PADDY vanities to Single basin vanities, and the MELA ZONE semi
  basin to Semi-recessed basins.
- Renamed the placeholder "MELA Double Check Clearance Item" to **MELA CASSA Pull Out Sink Mixer
  with Black Hose** (SKU CAS.SM.003); it keeps its "Clearance Item" tag.
- Added supplier photos (Bathroom City) to MELA CLASSIC 600/750/900/1200 2-drawer vanities (one
  per Hampton/Pastel/Shaker style) and the TRITON 1200 double sink.
- Deleted empty collections with no matching products: Hardware, Heated Towel Rails, Bath
  Panels, Floor Standing Vanities.

**Still in draft: no photo could be verified (29).** Add photos in Shopify admin, then set each
one to Active:

- BRITTANY 450, 750, 900, 1200 Double, 1500 Double, 1500 Single and 1800 Single wall-hung
  vanities. The listings don't say which cabinet finish (Oak or Matt White) or layout (drawers
  or cupboard) they are, and the supplier sells several versions of each size.
- CLASSIC Matt White vanities "with Shelves" (900, 1050, 1200, 1500, 1800) and the 1500/1800
  double 4-drawer versions (with and without shelves). The supplier only lists door and drawer
  layouts.
- BRUNO Wall Mixer with Diverter; Bath Pop Up Waste Universal; TRITON 310 sink; FLOVA ABS and
  Brass shower heads; PALCO/RONDO ABS and Brass shower heads; Corrugated and PVC shower hoses;
  MORRIS shower door handle; VINA LED plain mirror; RORY above-counter basin; MELVA half-inset
  basin.

## Deploying

Theme files are uploaded to the unpublished draft theme and previewed with
`?preview_theme_id=143546089535`. Publish from Shopify admin → Online Store → Themes when happy.

## Store content

`store-content/policies/` holds the current policy text. The shipping policy and
contact-information text must be pasted into Shopify admin → Settings → Policies (the API
connector can't write legal policies).

## SEO

- `seo/generate_product_seo.py` builds every product's search title (≤60 chars) and meta
  description (≤155 chars, always mentions Perth) from the product's own specs.
  `seo/product-seo.json` is the exact set written to Shopify on 26 Sep 2026 (224 products).
- `seo/collection-seo.json` holds the titles/descriptions added to 27 collections that had none.
- `snippets/meta-tags.liquid` doesn't append the shop name to titles that already end in
  "| ETS Perth", so titles stay inside Google's display limit.
- New in 2026: FAQ sections output `FAQPage` JSON-LD and product pages output a
  `BreadcrumbList`.
