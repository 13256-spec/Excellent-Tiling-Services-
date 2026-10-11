"""Build the ETS Klaviyo email templates (HTML + plain text + subject) into an output folder.
Usage: python3 make_emails.py <output dir>
The HTML keeps Klaviyo's {% unsubscribe %} tag (it renders the unsubscribe link itself) and the text
version uses {% unsubscribe_link %}. See store-content/email/README.md.
"""
import os, html, json, sys
OUT=sys.argv[1]
LOGO="https://excellenttilingservice.com.au/cdn/shop/files/Logo_With_Text_87041e11-d8e7-416e-b79f-17249bd17c18.jpg?v=1790680352&width=320"
SITE="https://excellenttilingservice.com.au"
NAVY="#1F3153"; BLUE="#4C8ED9"; PORC="#F4F5F3"; GREY="#C3C8CC"; INK="#2A2F36"
def btn(text,url): return f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:22px 0 6px"><tr><td style="background:{BLUE};border-radius:4px"><a href="{url}" style="display:inline-block;padding:14px 26px;color:#ffffff;font-weight:700;text-decoration:none;font-size:16px">{text}</a></td></tr></table>'
def p(t): return f'<p style="margin:0 0 14px;font-size:16px;line-height:1.55;color:{INK}">{t}</p>'
def h1(t): return f'<h1 style="margin:0 0 16px;font-size:26px;line-height:1.2;color:{NAVY};font-weight:700">{t}</h1>'
def code(c): return f'<p style="margin:18px 0;padding:14px 18px;background:{PORC};border:1px dashed {GREY};font-size:15px;color:{NAVY};text-align:center">Your code: <strong style="font-size:20px;letter-spacing:1px">{c}</strong></p>'
def small(t): return f'<p style="margin:0 0 10px;font-size:14px;line-height:1.5;color:#596069">{t}</p>'
def base(title, body, text):
    htm=f'''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>a.unsubscribe-link{{color:#6B737B !important}}</style></head>
<body style="margin:0;padding:0;background:#EDEFEE;font-family:Arial,Helvetica,sans-serif;color:{INK}">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#EDEFEE"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;background:#ffffff;border:1px solid {GREY}">
<tr><td align="center" style="padding:26px 24px 18px;background:{PORC};border-bottom:4px solid {BLUE}"><a href="{SITE}"><img src="{LOGO}" width="150" alt="Excellent Tiling Services" style="display:block;width:150px;height:auto;border:0"></a></td></tr>
<tr><td style="padding:30px 32px 10px">{body}</td></tr>
<tr><td style="padding:18px 32px 26px;border-top:1px solid {GREY};font-size:13px;line-height:1.6;color:#6B737B">
Excellent Tiling Services Pty Ltd · 17A Olga Road, Maddington WA 6109 · <a href="tel:+61450960543" style="color:#6B737B">0450 960 543</a><br>
Showroom by appointment, Mon to Sat 4:30 to 9 pm · <a href="{SITE}/pages/book-appointment" style="color:{NAVY}">Book a visit</a> · <a href="{SITE}/pages/delivery-pickup" style="color:{NAVY}">Delivery &amp; pickup</a><br>
You're getting this because you shopped with us or signed up at excellenttilingservice.com.au. {{% unsubscribe 'Unsubscribe' %}}
</td></tr></table></td></tr></table></body></html>'''
    return htm, text.strip()+"\n\nExcellent Tiling Services, 17A Olga Road, Maddington WA 6109. 0450 960 543.\nUnsubscribe: {% unsubscribe_link %}"
E={}
# ---------- Welcome 1
E["welcome-1"]=("Your 10% off is inside", base("Your 10% off",
 h1("Thanks for signing up. Here's 10% off your first order.")+
 p("Use the code below at checkout. It works on tiling tools, trims, spacers, grout and bathroom accessories across the store. It doesn't apply to tiles, vanities, baths or toilets, which are already priced as low as we can go.")+
 code("WELCOME10")+
 p("Orders over $180 get free standard shipping anywhere in Australia. In Perth you can also choose local delivery or free pickup from Maddington.")+
 btn("Shop with 10% off", SITE+"/collections/all?utm_source=klaviyo&utm_medium=email&utm_campaign=welcome")+
 small("One use per customer. Can't be combined with trade pricing or other codes. If you're a tiler, builder or plumber, a <a href='"+SITE+"/pages/trade-account' style='color:"+NAVY+"'>trade account</a> gives you more than 10% on most of the range, every order."),
 "Thanks for signing up. Here's 10% off your first order: use WELCOME10 at checkout. It works on tiling tools, trims, spacers, grout and bathroom accessories (not tiles, vanities, baths or toilets). Orders over $180 ship free Australia-wide. Shop: "+SITE))
# ---------- Welcome 2
E["welcome-2"]=("Three ways to get your order home", base("Three ways to get it home",
 h1("Three ways to get your order home")+
 p("<strong>Posted.</strong> Tapware, shower sets, towel rails, tools and other boxed items go by tracked Australia Post. Free on orders over $180, otherwise from $15.")+
 p("<strong>Delivered in Perth.</strong> Tiles, vanities, baths, toilets and other big items are delivered by our own ute within about 30 km of Maddington for $95, free on orders over $2,000. We call you to set a time.")+
 p("<strong>Picked up free.</strong> Collect from 17A Olga Road, Maddington. We're open by appointment Monday to Saturday, 4:30 to 9 pm, so you can come after work.")+
 btn("See delivery and pickup", SITE+"/pages/delivery-pickup?utm_source=klaviyo&utm_medium=email&utm_campaign=welcome")+
 small("Want to see tiles and vanities in person before you buy? <a href='"+SITE+"/pages/book-appointment' style='color:"+NAVY+"'>Book an evening showroom visit</a>. Your WELCOME10 code still works."),
 "Three ways to get your order home: tracked Australia Post (free over $180), Perth delivery within about 30 km of Maddington ($95, free over $2,000), or free pickup from Maddington by appointment Mon to Sat 4:30 to 9 pm. Details: "+SITE+"/pages/delivery-pickup"))
# ---------- Welcome 3
E["welcome-3"]=("Your 10% off is still waiting", base("Still 10% off",
 h1("Your 10% off is still waiting")+
 p("No rush, but WELCOME10 is sitting there unused. A few places people start:")+
 "<ul style='margin:0 0 14px 20px;padding:0;font-size:16px;line-height:1.7;color:"+INK+"'>"+
 f"<li><a href='{SITE}/collections/tapware' style='color:{NAVY}'>Tapware</a>: basin, wall and kitchen mixers in chrome, black, brushed nickel and brass.</li>"+
 f"<li><a href='{SITE}/collections/mirrors-accessories' style='color:{NAVY}'>Towel rails, hooks and holders</a>: finish the room in a matching set.</li>"+
 f"<li><a href='{SITE}/collections/hardware' style='color:{NAVY}'>Tiling tools and trims</a>: trowels, spacers, levelling clips, grout and 3 m trims.</li></ul>"+
 code("WELCOME10")+
 btn("Use my code", SITE+"/collections/all?utm_source=klaviyo&utm_medium=email&utm_campaign=welcome")+
 small("Not sure what you need for your bathroom? Reply to this email with a photo and a rough size and we'll point you in the right direction."),
 "Your WELCOME10 code is still unused. Tapware: "+SITE+"/collections/tapware. Accessories: "+SITE+"/collections/mirrors-accessories. Tools and trims: "+SITE+"/collections/hardware"))
# ---------- Checkout 1 (dynamic)
items='''{% if event.extra.line_items %}<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:6px 0 18px;border-top:1px solid #C3C8CC">{% for item in event.extra.line_items %}<tr><td style="padding:12px 0;border-bottom:1px solid #C3C8CC;width:72px;vertical-align:top">{% if item.product.images.0.src %}<img src="{{ item.product.images.0.src }}" width="64" alt="" style="display:block;width:64px;height:64px;object-fit:cover;border:1px solid #C3C8CC">{% endif %}</td><td style="padding:12px 10px;border-bottom:1px solid #C3C8CC;font-size:15px;line-height:1.4;color:#2A2F36;vertical-align:top"><strong>{{ item.product.title }}</strong>{% if item.variant_title and item.variant_title != "Default Title" %}<br><span style="color:#596069">{{ item.variant_title }}</span>{% endif %}<br><span style="color:#596069">Qty {{ item.quantity }}</span></td><td align="right" style="padding:12px 0;border-bottom:1px solid #C3C8CC;font-size:15px;color:#2A2F36;vertical-align:top;white-space:nowrap">${{ item.line_price|floatformat:2 }}</td></tr>{% endfor %}</table>{% endif %}'''
E["checkout-1"]=("Your checkout is saved", base("Your checkout is saved",
 h1("Your checkout is saved")+
 p("You started an order with us and didn't quite finish. Nothing's lost: your items are still there.")+items+
 btn("Finish my order", "{{ event.extra.checkout_url }}")+
 p("Not sure about delivery? Posted orders over $180 ship free anywhere in Australia. Tiles and large items are delivered in Perth or picked up free from Maddington, and the options show at checkout.")+
 small("Questions? Reply to this email or call 0450 960 543 (Mon to Sat, 4:30 to 9 pm)."),
 "You started an order with us and didn't finish. Your items are saved here: {{ event.extra.checkout_url }}  Questions about delivery? Reply to this email or call 0450 960 543."))
# ---------- Checkout 2
E["checkout-2"]=("Free postage on this order", base("Free postage on this order",
 h1("We'll cover the postage on this one")+
 p("Still thinking it over? Use the code below and standard Australia Post shipping on your saved order is free, whatever the order size.")+
 code("FREEPOST")+items+
 btn("Finish my order", "{{ event.extra.checkout_url }}")+
 small("One use per customer, Australian addresses, orders of $60 or more. Covers tracked standard post. Tiles and large items are Perth delivery or pickup and aren't posted. Already over $180? Then postage was free anyway, and this code just makes sure."),
 "Still thinking it over? Use FREEPOST at checkout and standard Australia Post shipping on your saved order is free (Australian addresses, orders $60+). Finish here: {{ event.extra.checkout_url }}"))
# ---------- Cart
E["cart-1"]=("Still in your cart", base("Still in your cart",
 h1("Still in your cart")+
 p("You added something to your cart at Excellent Tiling Services and left it there. It's saved on this device whenever you're ready.")+
 btn("Back to my cart", SITE+"/cart?utm_source=klaviyo&utm_medium=email&utm_campaign=cart")+
 p("Orders over $180 ship free anywhere in Australia by tracked post. In Perth, tiles and large items are delivered by us or picked up free from Maddington.")+
 small("Want a second opinion on sizes or finishes before you buy? Reply with a photo of the room. We do this every day."),
 "You left something in your cart at Excellent Tiling Services. Back to your cart: "+SITE+"/cart  Orders over $180 ship free Australia-wide."))
# ---------- Post-purchase 1
E["post-1"]=("Thanks for your order, here's what happens next", base("Thanks for your order",
 h1("Thanks for your order")+
 p("<strong>Posted items</strong> leave Maddington by tracked Australia Post. You'll get the tracking number by email when it's on its way.")+
 p("<strong>Perth delivery</strong>: we call to arrange a time that suits you (we deliver Monday to Saturday).")+
 p("<strong>Pickup</strong>: wait for the ready-for-pickup email, then <a href='"+SITE+"/pages/book-appointment' style='color:"+NAVY+"'>book a time</a> or call 0450 960 543. Bring your order number.")+
 p("Before you install, have a quick read of our <a href='"+SITE+"/pages/product-care' style='color:"+NAVY+"'>care and warranty notes</a>. Two minutes now saves a callback later.")+
 btn("Finishing supplies: grout, silicone, trims", SITE+"/collections/hardware?utm_source=klaviyo&utm_medium=email&utm_campaign=post-purchase")+
 small("Anything wrong with the order when it arrives? Reply with a photo straight away and we'll sort it."),
 "Thanks for your order. Posted items go by tracked Australia Post (tracking emailed). Perth delivery: we call to arrange a time. Pickup: wait for the ready email, then book at "+SITE+"/pages/book-appointment or call 0450 960 543. Care notes: "+SITE+"/pages/product-care"))
# ---------- Post-purchase 2
E["post-2"]=("How did it go?", base("How did it go?",
 h1("How did it go?")+
 p("Your order should be in and, hopefully, installed by now. We're a small Perth business and a short Google review makes a real difference to us.")+
 btn("Leave a Google review", "https://www.google.com/maps/search/?api=1&query=Excellent+Tiling+Services+17A+Olga+Road+Maddington+WA+6109")+
 p("Opens our listing in Google Maps. Tap <em>Write a review</em>. If something wasn't right, reply to this email first and we'll fix it.")+
 p("Send us a photo of the finished room too. With your okay we'll share it, and it helps the next person picture what they're buying.")+
 small("Tiler, builder or plumber? A <a href='"+SITE+"/pages/trade-account' style='color:"+NAVY+"'>trade account</a> takes 5 to 25% off most of the range and 15% off tiles on every order."),
 "Your order should be in by now. A short Google review helps us a lot: https://www.google.com/maps/search/?api=1&query=Excellent+Tiling+Services+Maddington  If something wasn't right, reply to this email first."))
# ---------- Winback
E["winback-1"]=("It's been a while. Here's 10% off", base("It's been a while",
 h1("It's been a while. Here's 10% off.")+
 p("It's been a couple of months since your last order. If there's another room on the list, this takes 10% off tiling tools, trims, spacers, grout and bathroom accessories.")+
 code("COMEBACK10")+
 p("Since you last looked: more Raimondi and BAT tools and trims, Perth delivery for tiles and large items at a flat $95, and free standard shipping over $180.")+
 btn("Shop with 10% off", SITE+"/collections/all?utm_source=klaviyo&utm_medium=email&utm_campaign=winback")+
 small("One use per customer. Not on tiles, vanities, baths or toilets. Can't be combined with trade pricing."),
 "It's been a couple of months since your last order. COMEBACK10 takes 10% off tools, trims, spacers, grout and bathroom accessories. Shop: "+SITE))
# ---------- Trade applicant
E["trade-applied"]=("We've got your trade application", base("Trade application received",
 h1("We've got your trade application")+
 p("Thanks for applying for a trade account with Excellent Tiling Services. We check the ABN and usually approve accounts within one business day. You'll get an email the moment it's live.")+
 p("What you get once approved:")+
 "<ul style='margin:0 0 14px 20px;padding:0;font-size:16px;line-height:1.7;color:"+INK+"'><li>15% off tiles and 5 to 25% off tools, trims, tapware and bathroomware, taken off automatically when you're logged in.</li><li>Your trade price shown on every product page, with the retail price crossed out.</li><li>Free pickup from Maddington, Monday to Saturday until 9 pm, or Perth delivery.</li></ul>"+
 btn("Browse the range", SITE+"/collections/hardware?utm_source=klaviyo&utm_medium=email&utm_campaign=trade")+
 small("Need something urgently before approval? Call 0450 960 543 and we'll sort it over the phone."),
 "Thanks for applying for a trade account. We check the ABN and usually approve within one business day; you'll get an email when it's live. Trade pricing: 15% off tiles, 5 to 25% off the rest, applied automatically when you're logged in."))
# ---------- Trade approved
E["trade-approved"]=("Your trade account is live", base("Your trade account is live",
 h1("Your trade account is live")+
 p("You're approved. Log in with this email address and every product page shows your trade price with the retail price crossed out. The discount comes off automatically in the cart; there's no code to type.")+
 "<ul style='margin:0 0 14px 20px;padding:0;font-size:16px;line-height:1.7;color:"+INK+"'><li>Tiles: 15% off. Tools, trims, tapware and bathroomware: 5 to 25% off depending on the item.</li><li>Trade pricing can't be combined with discount codes.</li><li>Pickup from Maddington Monday to Saturday until 9 pm, Perth delivery for tiles and large items, tracked post for the rest.</li></ul>"+
 btn("Log in and see your prices", SITE+"/account/login?utm_source=klaviyo&utm_medium=email&utm_campaign=trade")+
 small("Big job coming up? Send us the quantities and we'll price pallets and bulk tool orders directly. Reply to this email or call 0450 960 543."),
 "Your trade account is approved. Log in with this email and your trade prices show automatically (15% off tiles, 5 to 25% off the rest). Log in: "+SITE+"/account/login"))
for k,(subject,(htm,txt)) in E.items():
    open(os.path.join(OUT,k+".html"),"w").write(htm); open(os.path.join(OUT,k+".txt"),"w").write(txt)
    open(os.path.join(OUT,k+".subject"),"w").write(subject)
print({k:len(v[1][0]) for k,v in E.items()})
