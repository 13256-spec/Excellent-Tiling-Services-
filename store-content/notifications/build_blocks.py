"""Builds the branded paste-in blocks for Shopify customer notifications.

Each block goes directly after `{{ email_body }}` in the matching email
(Settings -> Notifications -> Customer notifications -> email -> Edit code).
Shopify's own order details, buttons and tracking stay untouched.

Run: python3 build_blocks.py   (writes emails/*.liquid)
Edit the wording here, not in the generated files.
"""
from pathlib import Path

NAVY, BRASS, CREAM = "#15213A", "#9C7744", "#F6F4EF"
PHONE = '<a href="tel:0450960543" style="color:%s;font-weight:bold;">0450 960 543</a>' % BRASS
HI = "{% if customer.first_name %}, {{ customer.first_name }}{% endif %}"
ADDRESS = "17A Olga Road, Maddington WA 6109"
HOURS = "by appointment, Monday to Saturday, 4:30 pm to 9 pm"
SITE = "https://excellenttilingservice.com.au"


def button(label, url):
    return (f'<p style="margin:14px 0 0;"><a href="{url}" style="display:inline-block;background:{NAVY};'
            f'color:#ffffff;text-decoration:none;padding:10px 18px;border-radius:6px;font-weight:bold;">{label}</a></p>')


def block(title, *paras):
    body = "\n".join(p if p.lstrip().startswith(("<p", "{%")) else f'    <p style="margin:0 0 10px;">{p}</p>'
                     for p in paras)
    return f"""<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:20px 0;background:{CREAM};border-left:4px solid {BRASS};border-radius:8px;">
  <tr><td style="padding:18px 20px;font-family:-apple-system,'Segoe UI',Arial,sans-serif;color:{NAVY};font-size:15px;line-height:1.55;">
    <p style="margin:0 0 10px;font-size:17px;font-weight:bold;">{title}</p>
{body}
  </td></tr>
</table>
"""


HELP = f"Questions? Call or text {PHONE}, or reply to this email."

BLOCKS = {
    # Orders
    "order-confirmation": ("Order confirmation", block(
        f"Thanks for your order{HI}.",
        "We've got order {{ order_name }} and we're getting it ready.",
        "{% if delivery_method == 'pick-up' %}",
        f"<p style=\"margin:0 0 10px;\"><strong>Pickup:</strong> we'll email you when it's ready. Collect from {ADDRESS}, {HOURS}. Bring your order number.</p>",
        "{% elsif delivery_method == 'local' %}",
        "<p style=\"margin:0 0 10px;\"><strong>Perth delivery:</strong> we'll call or text to book a delivery time. Let us know about stairs or tight access for large items.</p>",
        "{% else %}",
        "<p style=\"margin:0 0 10px;\"><strong>Delivery:</strong> some items come straight from our suppliers, so dispatch times vary. You'll get a tracking link as soon as it's on its way.</p>",
        "{% endif %}",
        HELP)),
    "order-invoice": ("Order invoice (quotes and draft orders)", block(
        f"Your quote from Excellent Tiling Services{HI}.",
        "Here are the items and prices we discussed. All prices include GST.",
        "Happy to go ahead? Use the button below to pay securely online. If you'd like to change anything first, just reply or give us a call.",
        HELP)),
    "order-edited": ("Order edited", block(
        f"We've updated your order{HI}.",
        "The changes we discussed are below, with your new total. If anything doesn't look right, let us know before we send it out.",
        HELP)),
    "order-cancelled": ("Order cancelled", block(
        f"Your order has been cancelled{HI}.",
        "If you paid, the refund goes back to your original payment method. Your bank may take a few business days to show it.",
        f"Didn't expect this email? Call or text {PHONE} and we'll sort it out.")),
    "refund-notification": ("Refund notification", block(
        f"Your refund is on its way{HI}.",
        "We've processed the refund shown below. It goes back to your original payment method, and your bank may take a few business days to show it.",
        HELP)),
    # Shipping
    "shipping-confirmation": ("Shipping confirmation", block(
        f"Your order is on its way{HI}.",
        "Use the tracking button below to follow your delivery.",
        "<p style=\"margin:0 0 10px;\"><strong>When it arrives:</strong> check the box and contents before you install anything. If something is damaged, missing or wrong, send us your order number with a few photos of the product and packaging.</p>",
        HELP)),
    "shipping-update": ("Shipping update", block(
        f"There's an update on your delivery{HI}.",
        "The latest tracking details are below.",
        HELP)),
    "out-for-delivery": ("Out for delivery", block(
        f"Your order is out for delivery today{HI}.",
        "Please keep your phone handy. For large items, make sure someone is home and the access is clear.",
        HELP)),
    "delivered": ("Delivered", block(
        f"Your order has been delivered{HI}.",
        "Please check everything before you install it. Something damaged, missing or wrong? Send us your order number and a few photos and we'll fix it.",
        f"Need a hand with the job? Our licensed team does tiling and bathroom work across Perth, starting with a free measure and quote.",
        button("Get a free quote", f"{SITE}/pages/request-a-quote"))),
    # Local pickup
    "ready-for-local-pickup": ("Ready for local pickup", block(
        f"Your order is ready to collect{HI}.",
        f"<p style=\"margin:0 0 10px;\"><strong>Where:</strong> {ADDRESS}<br><strong>When:</strong> {HOURS}</p>",
        f"Book a time below or text {PHONE} with your order number. For tiles or large items, bring a vehicle with enough room and we'll help you load.",
        button("Book a pickup time", f"{SITE}/pages/book-appointment"))),
    "picked-up-by-customer": ("Picked up by customer", block(
        f"Thanks for picking up your order{HI}.",
        "If anything isn't right once you open it, send us your order number and a few photos and we'll sort it out.",
        HELP)),
    # Local delivery
    "local-delivery-out-for-delivery": ("Local delivery: out for delivery", block(
        f"We're on our way{HI}.",
        "Your order is out for delivery today with the Excellent Tiling Services team. Please keep your phone handy and the driveway clear, and check items before signing.",
        f"Running late or need to change something? Call {PHONE}.")),
    "local-delivery-delivered": ("Local delivery: delivered", block(
        f"Your order has been delivered{HI}.",
        "Please check everything before you install it. If something is damaged or missing, send us your order number and a few photos.",
        HELP)),
    "local-delivery-missed": ("Local delivery: missed", block(
        f"Sorry we missed you{HI}.",
        f"We tried to deliver your order today but couldn't drop it off. Call or text {PHONE} and we'll book a new time.")),
    # Checkout and accounts
    "abandoned-checkout": ("Abandoned checkout", block(
        f"Still planning your project{HI}?",
        "Your items are saved. Use the button below to finish your order whenever you're ready.",
        f"Not sure about sizes, quantities or finishes? Call or text {PHONE}. You're talking to a Perth tiling team, and you can also see products in person at our Maddington showroom, {HOURS}.")),
    "customer-account-invite": ("Customer account invite", block(
        f"Your Excellent Tiling Services account{HI}.",
        "Set a password below to see your orders and check out faster next time.",
        "Tiler, builder or plumber? Approved trade accounts get 5–25% off, depending on the item.",
        button("Apply for a trade account", f"{SITE}/pages/trade-account"))),
    "customer-account-welcome": ("Customer account welcome", block(
        f"Welcome to Excellent Tiling Services{HI}.",
        "Your account is ready. Log in any time to see your orders and check out faster.",
        "Tiler, builder or plumber? Approved trade accounts get 5–25% off, depending on the item.",
        button("Apply for a trade account", f"{SITE}/pages/trade-account"))),
}

if __name__ == "__main__":
    out = Path(__file__).with_name("emails")
    out.mkdir(exist_ok=True)
    for slug, (name, html) in BLOCKS.items():
        (out / f"{slug}.liquid").write_text(f"{{% comment %}} ETS block for: {name} {{% endcomment %}}\n{html}")
    print(f"wrote {len(BLOCKS)} blocks to {out}")
