# Branded checkout and customer emails (5 Oct 2026)

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

## 3. Personal wording in the main emails (copy and paste)

For each email below: Settings → Notifications → Customer notifications → open the email →
**Edit code**. Find the line `<p>{{ email_body }}</p>` near the top and paste the block on the
line **directly after it**. Click **Preview**, then **Save**. Leave everything else as Shopify's
default so order details, discounts, pickup and tracking still work.

To undo, open the email and click **Revert to default**.

### Order confirmation

```liquid
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:20px 0;background:#F6F4EF;border-left:4px solid #9C7744;border-radius:8px;">
  <tr><td style="padding:18px 20px;font-family:-apple-system,'Segoe UI',Arial,sans-serif;color:#15213A;font-size:15px;line-height:1.55;">
    <p style="margin:0 0 10px;font-size:17px;font-weight:bold;">Thanks for choosing Excellent Tiling Services{% if customer.first_name %}, {{ customer.first_name }}{% endif %}.</p>
    <p style="margin:0 0 10px;">We're a local tile and bathroom supplier in Maddington, Perth, and a real person is now checking your order {{ order_name }}.</p>
    <p style="margin:0 0 6px;font-weight:bold;">What happens next</p>
    {% if delivery_method == 'pick-up' %}
    <p style="margin:0 0 10px;">We'll email you as soon as your order is ready to collect. Pickup is from 17A Olga Road, Maddington WA 6109, <strong>by appointment</strong>, Monday to Saturday 4:30 pm to 9 pm. Please bring your order number.</p>
    {% elsif delivery_method == 'local' %}
    <p style="margin:0 0 10px;">We'll call or text you to arrange a delivery time in Perth. Please make sure someone can receive large items, and tell us about any stairs or tight access.</p>
    {% else %}
    <p style="margin:0 0 10px;">Some items come straight from our suppliers, so dispatch times can vary. When your parcel is on its way, you'll get a tracking link by email.</p>
    {% endif %}
    <p style="margin:0;">Questions? Call or text <a href="tel:0450960543" style="color:#9C7744;font-weight:bold;">0450 960 543</a> or reply to this email.</p>
  </td></tr>
</table>
```

### Shipping confirmation

```liquid
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:20px 0;background:#F6F4EF;border-left:4px solid #9C7744;border-radius:8px;">
  <tr><td style="padding:18px 20px;font-family:-apple-system,'Segoe UI',Arial,sans-serif;color:#15213A;font-size:15px;line-height:1.55;">
    <p style="margin:0 0 10px;font-size:17px;font-weight:bold;">Good news{% if customer.first_name %}, {{ customer.first_name }}{% endif %}: your order is on its way.</p>
    <p style="margin:0 0 10px;">We packed it by hand in Maddington. Use the tracking button below to follow it with Australia Post.</p>
    <p style="margin:0 0 10px;"><strong>When it arrives:</strong> check the box and contents before you install anything. If something is damaged, missing or wrong, send us your order number and a few photos of the product and packaging, and we'll sort it out.</p>
    <p style="margin:0;">Call or text <a href="tel:0450960543" style="color:#9C7744;font-weight:bold;">0450 960 543</a> or reply to this email.</p>
  </td></tr>
</table>
```

### Ready for local pickup

```liquid
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:20px 0;background:#F6F4EF;border-left:4px solid #9C7744;border-radius:8px;">
  <tr><td style="padding:18px 20px;font-family:-apple-system,'Segoe UI',Arial,sans-serif;color:#15213A;font-size:15px;line-height:1.55;">
    <p style="margin:0 0 10px;font-size:17px;font-weight:bold;">Your order is ready to collect{% if customer.first_name %}, {{ customer.first_name }}{% endif %}.</p>
    <p style="margin:0 0 10px;"><strong>Where:</strong> 17A Olga Road, Maddington WA 6109<br><strong>When:</strong> by appointment, Monday to Saturday 4:30 pm to 9 pm</p>
    <p style="margin:0 0 10px;">Text <a href="sms:0450960543" style="color:#9C7744;font-weight:bold;">0450 960 543</a> with your order number and a time that suits you. For tiles or large items, bring a vehicle with enough room. We'll help you load.</p>
    <p style="margin:0;"><a href="https://excellenttilingservices.com/pages/book-appointment" style="display:inline-block;background:#15213A;color:#ffffff;text-decoration:none;padding:10px 18px;border-radius:6px;font-weight:bold;">Book a pickup time</a></p>
  </td></tr>
</table>
```

### Local delivery: out for delivery

```liquid
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:20px 0;background:#F6F4EF;border-left:4px solid #9C7744;border-radius:8px;">
  <tr><td style="padding:18px 20px;font-family:-apple-system,'Segoe UI',Arial,sans-serif;color:#15213A;font-size:15px;line-height:1.55;">
    <p style="margin:0 0 10px;font-size:17px;font-weight:bold;">We're on our way{% if customer.first_name %}, {{ customer.first_name }}{% endif %}.</p>
    <p style="margin:0 0 10px;">Your order is out for delivery today with the Excellent Tiling Services team. Please keep your phone handy and the driveway clear. Check items before signing, and write any damage on the paperwork.</p>
    <p style="margin:0;">Running late or need to change something? Call <a href="tel:0450960543" style="color:#9C7744;font-weight:bold;">0450 960 543</a>.</p>
  </td></tr>
</table>
```

## 4. Sender details

Settings → Notifications → **Sender email**: `contactus@excellenttilingservices.com`. Shopify asks you to
verify the domain (DNS records). Then emails come from your address, not a shopify.com one,
and are less likely to land in spam.
