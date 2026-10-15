# Branded checkout, customer emails, packing slip and tax invoice (updated 8 Oct 2026)

Brand values, taken from the live theme (`theme/assets/ets-2026.css`):

| Use | Colour |
| --- | --- |
| Navy (text, buttons) | `#15213A` |
| Brass (accent) | `#9C7744` |
| Cream (background) | `#F6F4EF` |
| Soft brass (panels) | `#EFE6D6` |

Logo: the same file as the website header (`excellent-tiling-services-logo.jpg`, in Shopify Files).
Fonts on the site: Manrope (text) and Instrument Serif (headings).

These have to be set in Shopify admin. On the Basic plan, the API can't change checkout branding or
email templates. The checkout branding API needs Shopify Plus, and there is no API for notification templates.

## 1. Checkout and thank-you page (about 5 minutes, no code)

Settings → Checkout → **Customize** (opens the checkout editor). Click the paintbrush (Settings) icon:

- **Logo:** upload the ETS logo. Set its position to left and its size to medium.
- **Colours:** accent / buttons `#15213A`, background `#F6F4EF`. Set the main form background to white.
- **Typography:** headings Manrope (or a serif if one is offered), body Manrope.
- **Corner radius:** small, to match the site.

Save. The same branding applies to the thank-you page and the order status page.

Under Settings → Checkout, also check:
- **Customer contact:** email or phone. Phone helps for Perth deliveries.
- **Company name:** optional. Trade customers like having it.
- **Shipping address phone number:** required. Couriers and local delivery need it.
- **Order processing:** "Add a note to the order" stays on, for delivery instructions.

## 2. Email look (2 minutes, no code)

Settings → Notifications → Customer notifications → **Customize email templates**:

- Logo: upload the ETS logo, width **180 px**.
- Accent colour: `#15213A`.

Save. Every customer email now carries the logo and navy buttons.

## 3. Personal wording in every customer email (copy and paste)

The blocks are in `emails/` (built by `build_blocks.py`; edit wording there and re-run it).
For each one: Settings → Notifications → Customer notifications → open the email → **Edit code**.
Find `{{ email_body }}` near the top and paste the block on the line **directly after it**
(if an email has no `{{ email_body }}`, paste it after the heading). Click **Preview**, then **Save**.
Everything else stays Shopify's default, so order details, buttons, pickup and tracking keep working.
To undo, open the email and click **Revert to default**.

| Shopify email | File |
| --- | --- |
| Order confirmation | `emails/order-confirmation.liquid` |
| Order invoice (quotes / draft orders) | `emails/order-invoice.liquid` |
| Order edited | `emails/order-edited.liquid` |
| Order cancelled | `emails/order-cancelled.liquid` |
| Refund notification | `emails/refund-notification.liquid` |
| Shipping confirmation | `emails/shipping-confirmation.liquid` |
| Shipping update | `emails/shipping-update.liquid` |
| Out for delivery | `emails/out-for-delivery.liquid` |
| Delivered | `emails/delivered.liquid` |
| Ready for local pickup | `emails/ready-for-local-pickup.liquid` |
| Picked up by customer | `emails/picked-up-by-customer.liquid` |
| Local delivery: out for delivery | `emails/local-delivery-out-for-delivery.liquid` |
| Local delivery: delivered | `emails/local-delivery-delivered.liquid` |
| Local delivery: missed | `emails/local-delivery-missed.liquid` |
| Abandoned checkout | `emails/abandoned-checkout.liquid` |
| Customer account invite | `emails/customer-account-invite.liquid` |
| Customer account welcome | `emails/customer-account-welcome.liquid` |

Wording follows the owner's rules (8 Oct 2026): no shipping prices or carrier names, no "Perth only"
for products, installation and free measure and quote are Perth services, showroom by appointment
Mon–Sat 4:30–9 pm, trade 5–25% off depending on the item.

## 3a. Packing slip

Settings → Shipping and delivery → **Packing slips** → Edit → replace the whole template with
`packing-slip.liquid` → **Preview** → Save. It adds the ETS header and ABN, a "packed" tick column,
part-shipment note, delivery instructions and the returns summary.

## 3b. Tax invoice (printable / PDF)

Shopify Basic has no built-in tax invoice. Install the free **Shopify Order Printer** app, then
Templates → Create template → "Tax invoice" → paste `tax-invoice-order-printer.liquid` → Preview → Save.
It shows "Tax invoice", the ABN, items, GST included and the total, as the ATO requires. Print or
email it from any order (More actions → Print with Order Printer).

## 3c. Email marketing

Automations and campaigns (Shopify Email): `marketing/email/shopify-email-campaigns.md`.

## 4. Sender details

Settings → Notifications → **Sender email**: `contactus@excellenttilingservice.com.au`. Shopify asks you to
verify the domain (DNS records). Then emails come from your address, not a shopify.com one,
and are less likely to land in spam.
