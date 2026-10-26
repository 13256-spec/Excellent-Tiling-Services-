"""DSA toilet collection (Eternity Tiles, product sheets received 26 Oct 2026) -> Shopify productSet inputs.

Nine toilets plus the Edna Care back rest. Photos and specs come from the sheets Eternity shared
(store-content/supplier-sync/dsa-toilet-sheets/). The Crystal Elite (DSAYC318GE) was already in the
store as "Crystal Smart Toilet with Bidet Seat" and is updated separately (see dsa-toilets-2026-10-26.json).

Pricing (owner, 26 Oct 2026: "record sales price and our cost price"):
- price = DSA RRP inc GST, as for the rest of the DSA range (sell at Eternity's price until a trade list arrives)
- cost  = ESTIMATE: RRP less the 45% "account deal" discount DSA gave on the Malaga vanity packages, ex GST
          (RRP x 0.55 / 1.1 = RRP x 0.5). Tag `cost-estimate` until Eternity confirms the toilet wholesale prices.
Supplier name stays out of customer-facing text; vendor "Excellent Tiling Services".

Usage: dsa_toilets_2026_10.py staged.json out.json
  staged.json: {filename: staged upload URL} for the images in dsa-toilet-sheets/
"""
import json, sys

CAT = "gid://shopify/TaxonomyCategory/ha-10-3-6-2"  # Toilets
PERTH = "ship-local-only"
WELS34 = "WELS 4 Star: 4.5 L full / 3.1 L half / 3.4 L average"
SMART_DESC = (
    "<p>{name} is a one-piece smart toilet with a built-in bidet seat, so washing, drying, flushing and the lid all "
    "work without touching anything. A foot sensor opens and closes the lid, the seat is heated, and a single touch "
    "runs wash, dry and flush in one go. The rimless tornado flush is WaterMark certified and uses 3.4 litres on "
    "average.</p><h3>Features</h3><ul><li>Touch-free automatic lid, foot sensor for flushing</li>"
    "<li>Rear wash, front wash and oscillating wash with adjustable water pressure and nozzle position</li>"
    "<li>Nozzle self-cleans before and after each use</li><li>Heated seat: room temperature, 35, 37 or 39 °C</li>"
    "<li>Wash water: room temperature, 34, 37 or 40 °C, heated instantly with no storage tank</li>"
    "<li>Warm air drying: 35, 45 or 55 °C</li><li>Soft night light and LED temperature display</li>"
    "<li>Handheld remote plus a side button for one-touch flushing</li>"
    "<li>Automatic dual flush: half flush after a short visit, full flush after a longer one</li>"
    "<li>Eight safety protections including seat temperature, leakage, water ingress, power failure and overheating</li>"
    "</ul><h3>Specifications</h3><ul><li>Model: {sku}</li><li>Size: {size}</li>"
    "<li>Colour: white</li><li>Body: ceramic with ABS seat and lid</li><li>Trap: S-trap, set-out adjustable 60 to 280 mm</li>"
    "<li>Flush: rimless tornado, dual flush, {wels}</li><li>WELS standard AS/NZS 6400, licence 1979</li>"
    "<li>WaterMark certified to AS 1172.1 and AS 1172.2</li><li>Power: 220 to 240 V, 50 Hz, rated 1250 W</li>"
    "<li>Splash protection: IPX4</li><li>Weight: about 45 kg</li></ul><h3>Good to know</h3><ul>"
    "<li>Needs a power point beside the toilet and a cold water supply with a minimum of 0.07 MPa dynamic pressure.</li>"
    "<li>Confirm the floor waste position and the S-trap set-out before installation.</li>"
    "<li>Installation by a licensed plumber and electrician.</li></ul>"
)


def smart(name, sku, size):
    return SMART_DESC.format(name=name, sku=sku, size=size, wels=WELS34)


# key: (title, type, rrp, tags, metafields, seo_desc, description, images [(file, alt)], width, depth, height)
P = {
    "dsa8080": ("Eternal Clarice Toilet Suite", "Toilet Suite", 660,
        ["Eternal", "Rimless", "Back to Wall", "Toilet", "Toilet Suite"],
        {"range": "Eternal", "material": "Ceramic"},
        "Eternal Clarice rimless back to wall toilet suite, 645 x 385 x 860 mm, S-trap 100 to 250 mm or P-trap, 475 mm seat height.",
        "<p>The Eternal Clarice is a back to wall toilet suite with a rimless bowl and a clean, boxy cistern. The seat sits at "
        "475 mm, a little higher than a standard suite, which makes it easier to get up from without going to a full care "
        "height.</p><h3>Use it for</h3><ul><li>Main bathrooms, ensuites and powder rooms</li>"
        "<li>Replacing an older suite where the waste is 100 to 250 mm from the wall</li>"
        "<li>Anyone who finds a standard 400 to 430 mm seat a bit low</li></ul><h3>Specifications</h3><ul>"
        "<li>Model: DSA8080</li><li>Size: 645 x 385 x 860 mm</li><li>Seat height: 475 mm</li>"
        "<li>Trap: S-trap 100 to 250 mm set-out, or P-trap 180 mm</li><li>Flush: rimless</li>"
        "<li>Finish: white ceramic</li><li>Soft close seat included</li></ul><h3>Good to know</h3><ul>"
        "<li>Rimless bowls have no hidden rim underneath, so there is nowhere for grime to build up.</li>"
        "<li>Measure from the finished wall to the centre of the waste before ordering so the trap suits.</li>"
        "<li>Installation by a licensed plumber.</li></ul>",
        [("dsa8080-eternal-clarice-toilet-suite.jpg", "Eternal Clarice Toilet Suite"),
         ("dsa8080-eternal-clarice-dimensions.png", "Eternal Clarice Toilet Suite dimensions")], 385, 645, 860),
    "dsa8081": ("Edna Care Toilet Suite", "Toilet Suite", 1320,
        ["Care", "Accessible", "Ambulant", "Rimless", "Back to Wall", "Toilet", "Toilet Suite"],
        {"range": "Care", "material": "Ceramic"},
        "Edna Care rimless toilet suite with grey contrast seat, 800 x 385 x 860 mm, 470 mm seat height, S-trap 115 to 200 mm or P-trap. Optional back rest.",
        "<p>The Edna Care is a care toilet suite: a longer 800 mm pan, a 470 mm seat height and a grey seat that stands out "
        "against the white bowl for people with low vision. It suits accessible bathrooms in homes, aged care and "
        "commercial buildings.</p><h3>Use it for</h3><ul><li>Accessible and ambulant bathrooms</li>"
        "<li>Home modifications for people with limited mobility</li><li>Aged care, clinics and community buildings</li></ul>"
        "<h3>Specifications</h3><ul><li>Model: DSA8081</li><li>Size: 800 x 385 x 860 mm</li><li>Seat height: 470 mm</li>"
        "<li>Trap: S-trap 115 to 200 mm set-out, or P-trap 180 mm</li><li>Flush: rimless</li>"
        "<li>Finish: white ceramic, grey contrast seat</li></ul><h3>Good to know</h3><ul>"
        "<li>The matching back rest (model DSA8081-Back rest) is sold separately.</li>"
        "<li>The longer pan sits further from the wall, so check the room has space for grab rails and transfer.</li>"
        "<li>Installation by a licensed plumber.</li></ul>",
        [("dsa8081-edna-care-toilet-suite.jpg", "Edna Care Toilet Suite with grey contrast seat"),
         ("dsa8081-edna-care-dimensions.png", "Edna Care Toilet Suite dimensions")], 385, 800, 860),
    "dsa8081-br": ("Edna Care Toilet Back Rest", "Toilet Back Rest", 268.99,
        ["Care", "Accessible", "Ambulant", "Toilet", "Toilet Hardware", "Back Rest", "needs-photo"],
        {"range": "Care", "material": "Steel"},
        "Back rest for the Edna Care toilet suite. Padded rest on a steel frame for accessible and care bathrooms. Sold separately from the suite.",
        "<p>The back rest for the Edna Care toilet suite gives a padded support behind the user, which care and accessible "
        "bathroom designs usually call for. It mounts to the wall behind the suite.</p><h3>Use it for</h3><ul>"
        "<li>Completing an Edna Care suite in an accessible bathroom</li><li>Care homes, clinics and home modifications</li></ul>"
        "<h3>Specifications</h3><ul><li>Model: DSA8081-Back rest</li><li>Fits: Edna Care Toilet Suite (DSA8081)</li>"
        "<li>Padded rest on a steel frame, wall mounted</li></ul><h3>Good to know</h3><ul>"
        "<li>Sold separately from the suite.</li><li>Fix into solid blocking or masonry so it takes a person's weight.</li></ul>",
        [("dsa8081-edna-care-back-rest.jpg", "Edna Care Toilet Back Rest")], None, None, None),
    "dsa8084": ("Eternal Element Toilet Suite", "Toilet Suite", 500,
        ["Eternal", "Rimless", "Back to Wall", "Toilet", "Toilet Suite"],
        {"range": "Eternal", "material": "Ceramic"},
        "Eternal Element rimless back to wall toilet suite, 610 x 385 x 815 mm, S-trap 55 to 175 mm or P-trap 180 mm, 430 mm seat height.",
        "<p>The Eternal Element is a compact back to wall toilet suite with a rimless bowl. At 610 mm deep it is one of the "
        "shorter suites around, and the S-trap set-out starts at 55 mm, so it fits tight rooms and older plumbing where the "
        "waste is close to the wall.</p><h3>Use it for</h3><ul><li>Small bathrooms, ensuites and powder rooms</li>"
        "<li>Renovations where the waste sits close to the wall</li><li>Budget-conscious bathroom updates</li></ul>"
        "<h3>Specifications</h3><ul><li>Model: DSA8084</li><li>Size: 610 x 385 x 815 mm</li><li>Seat height: 430 mm</li>"
        "<li>Trap: S-trap 55 to 175 mm set-out, or P-trap 180 mm</li><li>Flush: rimless</li>"
        "<li>Finish: white ceramic</li><li>Soft close seat included</li></ul><h3>Good to know</h3><ul>"
        "<li>Rimless bowls are easier to keep clean because there is no rim for grime to hide under.</li>"
        "<li>Measure from the finished wall to the centre of the waste before ordering.</li>"
        "<li>Installation by a licensed plumber.</li></ul>",
        [("dsa8084-eternal-element-toilet-suite.jpg", "Eternal Element Toilet Suite"),
         ("dsa8084-eternal-element-dimensions.png", "Eternal Element Toilet Suite dimensions")], 385, 610, 815),
    "dsa8102": ("Caleb Aria Wall Faced Toilet with In-Wall Cistern", "In Wall Cistern Toilet", 999,
        ["Caleb", "Rimless", "Wall Faced", "In Wall Cistern Toilet", "Toilet", "WELS 4 Star"],
        {"range": "Caleb", "material": "Ceramic", "wels_rating": WELS34},
        "Caleb Aria wall faced floor pan with in-wall cistern, rimless tornado flush, WELS 4 star 3.4 L average, 545 x 360 x 410 mm, S-trap 100 to 125 mm.",
        "<p>The Caleb Aria is a wall faced floor pan that hides the cistern inside the wall, leaving only the pan and a flush "
        "plate on show. The rimless tornado flush washes the whole bowl with 3.4 litres on average, and the pan sits hard "
        "against the wall with no gap behind it to clean.</p><h3>Use it for</h3><ul>"
        "<li>New bathrooms and renovations where the wall is being opened up</li>"
        "<li>Minimal, easy-clean bathrooms with a flat wall behind the toilet</li>"
        "<li>Pairing with a wall hung vanity for a floating look</li></ul><h3>Specifications</h3><ul>"
        "<li>Model: DSA8102</li><li>Pan size: 545 x 360 x 410 mm</li><li>Trap: S-trap, 100 to 125 mm set-out</li>"
        "<li>Flush: rimless tornado, dual flush, " + WELS34 + "</li><li>WaterMark certified to AS 1172.1 and AS 1172.2</li>"
        "<li>Finish: white ceramic</li><li>Soft close seat included</li></ul><h3>What's in the box</h3><ul>"
        "<li>Pan, seat and the matching in-wall cistern (DSA8102-CISTERN) with flush plate</li></ul><h3>Good to know</h3><ul>"
        "<li>The cistern needs a framed wall cavity; plan it before the wall is lined and tiled.</li>"
        "<li>Installation by a licensed plumber.</li></ul>",
        [("dsa8102-caleb-aria-toilet.png", "Caleb Aria Wall Faced Toilet"),
         ("dsa8102-caleb-aria-dimensions.png", "Caleb Aria Wall Faced Toilet dimensions"),
         ("dsa8102-caleb-aria-cistern.png", "Caleb Aria in-wall cistern DSA8102-CISTERN")], 360, 545, 410),
    "dsa8202": ("Eternal Edge Toilet Suite", "Toilet Suite", 550,
        ["Eternal", "Rimless", "Back to Wall", "Toilet", "Toilet Suite", "WELS 4 Star"],
        {"range": "Eternal", "material": "Ceramic", "wels_rating": WELS34},
        "Eternal Edge rimless back to wall toilet suite, WELS 4 star 3.4 L average, 630 x 360 x 850 mm, S-trap 70 to 150 mm (70 to 250 mm with extra pipes).",
        "<p>The Eternal Edge is a two-piece back to wall toilet suite with a rimless bowl and a dual flush that averages "
        "3.4 litres. The cistern has square edges and a flat top, and the pan sits flush to the wall so there is no gap to "
        "clean behind.</p><h3>Use it for</h3><ul><li>Main bathrooms, ensuites and powder rooms</li>"
        "<li>Renovations: the S-trap set-out covers 70 to 250 mm with the optional pipe kit</li>"
        "<li>Square-edged bathroom schemes</li></ul><h3>Specifications</h3><ul><li>Model: DSA8202</li>"
        "<li>Size: 630 x 360 x 850 mm</li><li>Seat height: 415 mm</li>"
        "<li>Trap: S-trap 70 to 150 mm set-out as supplied (140 mm recommended); 70 to 250 mm with additional pipes, sold separately</li>"
        "<li>Flush: rimless, dual flush, " + WELS34 + "</li><li>WaterMark certified to AS 1172.1 and AS 1172.2</li>"
        "<li>Finish: white ceramic</li><li>Soft close seat included</li></ul><h3>Good to know</h3><ul>"
        "<li>Measure from the finished wall to the centre of the waste; over 150 mm needs the extension pipes.</li>"
        "<li>Installation by a licensed plumber.</li></ul>",
        [("dsa8202-eternal-edge-toilet-suite.png", "Eternal Edge Toilet Suite"),
         ("dsa8202-eternal-edge-dimensions.png", "Eternal Edge Toilet Suite dimensions")], 360, 630, 850),
    "dsa8203": ("Eternal Forma Toilet Suite", "Toilet Suite", 550,
        ["Eternal", "Rimless", "Back to Wall", "Toilet", "Toilet Suite", "WELS 4 Star"],
        {"range": "Eternal", "material": "Ceramic", "wels_rating": WELS34},
        "Eternal Forma rimless back to wall toilet suite, WELS 4 star 3.4 L average, 630 x 360 x 850 mm, S-trap 70 to 150 mm (70 to 250 mm with extra pipes).",
        "<p>The Eternal Forma is a two-piece back to wall toilet suite with a rimless bowl and a dual flush that averages "
        "3.4 litres. It shares its footprint and plumbing with the Eternal Edge; the difference is the softer, rounded "
        "cistern and seat profile.</p><h3>Use it for</h3><ul><li>Main bathrooms, ensuites and powder rooms</li>"
        "<li>Renovations: the S-trap set-out covers 70 to 250 mm with the optional pipe kit</li>"
        "<li>Bathrooms with rounded basins and tapware</li></ul><h3>Specifications</h3><ul><li>Model: DSA8203</li>"
        "<li>Size: 630 x 360 x 850 mm</li><li>Seat height: 415 mm</li>"
        "<li>Trap: S-trap 70 to 150 mm set-out as supplied (140 mm recommended); 70 to 250 mm with additional pipes, sold separately</li>"
        "<li>Flush: rimless, dual flush, " + WELS34 + "</li><li>WaterMark certified to AS 1172.1 and AS 1172.2</li>"
        "<li>Finish: white ceramic</li><li>Soft close seat included</li></ul><h3>Good to know</h3><ul>"
        "<li>Measure from the finished wall to the centre of the waste; over 150 mm needs the extension pipes.</li>"
        "<li>Installation by a licensed plumber.</li></ul>",
        [("dsa8203-eternal-forma-toilet-suite.png", "Eternal Forma Toilet Suite"),
         ("dsa8203-eternal-forma-dimensions.png", "Eternal Forma Toilet Suite dimensions")], 360, 630, 850),
    "dsa8206": ("Eternal Flow Toilet Suite", "Toilet Suite", 660,
        ["Eternal", "Rimless", "Back to Wall", "Toilet", "Toilet Suite", "WELS 4 Star"],
        {"range": "Eternal", "material": "Ceramic", "wels_rating": WELS34},
        "Eternal Flow rimless tornado back to wall toilet suite, WELS 4 star 3.4 L average, 605 x 360 x 840 mm, S-trap 100 to 170 mm (60 to 220 mm with pipe kits).",
        "<p>The Eternal Flow is a two-piece back to wall toilet suite with a rimless tornado flush: water enters from one "
        "point and spins around the bowl, which cleans the whole surface quietly on 3.4 litres average. The pan is a touch "
        "shorter than the Edge and Forma at 605 mm.</p><h3>Use it for</h3><ul><li>Main bathrooms, ensuites and powder rooms</li>"
        "<li>Renovations with a waste anywhere from 60 to 220 mm off the wall, using the right pipe kit</li>"
        "<li>Quieter flushing in bathrooms next to bedrooms</li></ul><h3>Specifications</h3><ul><li>Model: DSA8206</li>"
        "<li>Size: 605 x 360 x 840 mm</li><li>Seat height: 400 mm</li>"
        "<li>Trap: S-trap 100 to 170 mm set-out as supplied (140 mm recommended); pipe A 60 to 125 mm, pipe B 100 to 170 mm, pipe C 150 to 220 mm, sold separately</li>"
        "<li>Flush: rimless tornado, dual flush, " + WELS34 + "</li><li>WaterMark certified to AS 1172.1 and AS 1172.2</li>"
        "<li>Finish: white ceramic</li><li>Soft close seat included</li></ul><h3>Good to know</h3><ul>"
        "<li>Measure from the finished wall to the centre of the waste and pick the pipe kit to suit.</li>"
        "<li>Installation by a licensed plumber.</li></ul>",
        [("dsa8206-eternal-flow-toilet-suite.png", "Eternal Flow Toilet Suite"),
         ("dsa8206-eternal-flow-dimensions.png", "Eternal Flow Toilet Suite dimensions")], 360, 605, 840),
    "dsa8305": ("Caleb Vero Wall Hung Toilet with In-Wall Cistern", "In Wall Cistern Toilet", 1299,
        ["Caleb", "Rimless", "Wall Hung", "In Wall Cistern Toilet", "Toilet", "WELS 4 Star"],
        {"range": "Caleb", "material": "Ceramic", "wels_rating": WELS34},
        "Caleb Vero wall hung toilet with in-wall cistern and frame, rimless tornado flush, WELS 4 star 3.4 L average, 520 x 360 x 330 mm pan, P-trap.",
        "<p>The Caleb Vero is a wall hung toilet: the pan floats off the floor on a steel frame hidden in the wall, with the "
        "cistern behind the wall lining and only a flush plate showing. The floor runs clean underneath, and the rimless "
        "tornado flush uses 3.4 litres on average.</p><h3>Use it for</h3><ul>"
        "<li>New bathrooms and renovations where the wall is being framed and opened up</li>"
        "<li>Easy-clean bathrooms with nothing on the floor</li><li>Matching a wall hung vanity</li></ul>"
        "<h3>Specifications</h3><ul><li>Model: DSA8305</li><li>Pan size: 520 x 360 x 330 mm</li>"
        "<li>Trap: P-trap, wall hung</li><li>Flush: rimless tornado, dual flush, " + WELS34 + "</li>"
        "<li>WaterMark certified to AS 1172.1 and AS 1172.2</li><li>Finish: white ceramic</li>"
        "<li>Soft close seat included</li></ul><h3>What's in the box</h3><ul>"
        "<li>Pan, seat and the in-wall body: steel frame, cistern and flush plate</li></ul><h3>Good to know</h3><ul>"
        "<li>The frame needs a wall cavity about 1140 mm high and is fixed to the floor and wall; plan it before lining and tiling.</li>"
        "<li>Pan height is set on the frame during installation, so it can be raised for easier use.</li>"
        "<li>Installation by a licensed plumber.</li></ul>",
        [("dsa8305-caleb-vero-wall-hung-toilet.png", "Caleb Vero Wall Hung Toilet"),
         ("dsa8305-caleb-vero-dimensions.png", "Caleb Vero Wall Hung Toilet dimensions and in-wall frame")], 360, 520, 330),
    "dsag1fd-e": ("Crystal Prime Smart Toilet Suite", "Toilet Suite", 3299,
        ["Crystal", "Smart Toilet", "Bidet", "Rimless", "Back to Wall", "Toilet", "Toilet Suite", "WELS 4 Star"],
        {"range": "Crystal", "material": "Ceramic", "wels_rating": WELS34, "wels_registration": "1979"},
        "Crystal Prime smart toilet suite with bidet wash, heated seat, warm air dryer, auto lid and foot sensor flush. WELS 4 star 3.4 L, 705 x 390 x 460 mm.",
        smart("The Crystal Prime", "DSAG1FD-E", "705 x 390 x 460 mm"),
        [("dsag1fd-e-crystal-prime-smart-toilet.png", "Crystal Prime Smart Toilet Suite"),
         ("dsag1fd-e-crystal-prime-features.jpg", "Crystal Prime Smart Toilet Suite features"),
         ("dsag1fd-e-crystal-prime-specifications.png", "Crystal Prime Smart Toilet Suite specifications")], 390, 705, 460),
    "dsag6fd-e": ("Crystal Nova Smart Toilet Suite", "Toilet Suite", 3299,
        ["Crystal", "Smart Toilet", "Bidet", "Rimless", "Back to Wall", "Toilet", "Toilet Suite", "WELS 4 Star"],
        {"range": "Crystal", "material": "Ceramic", "wels_rating": WELS34, "wels_registration": "1979"},
        "Crystal Nova smart toilet suite with bidet wash, heated seat, warm air dryer, auto lid and foot sensor flush. WELS 4 star 3.4 L, 705 x 390 x 440 mm.",
        smart("The Crystal Nova", "DSAG6FD-E", "705 x 390 x 440 mm"),
        [("dsag6fd-e-crystal-nova-smart-toilet.png", "Crystal Nova Smart Toilet Suite"),
         ("dsag6fd-e-crystal-nova-features.jpg", "Crystal Nova Smart Toilet Suite features"),
         ("dsag6fd-e-crystal-nova-specifications.png", "Crystal Nova Smart Toilet Suite specifications")], 390, 705, 440),
}
WEIGHT = {"Toilet Suite": 35, "In Wall Cistern Toilet": 30, "Toilet Back Rest": 4}


def build(staged):
    out = []
    for key, (title, ptype, rrp, tags, mf, seo_desc, desc, images, w, d, h) in P.items():
        sku = key.upper().replace("-BR", "-Back rest")
        kg = 45 if "Smart" in title else WEIGHT[ptype]
        metafields = [{"namespace": "custom", "key": "supplier", "type": "single_line_text_field", "value": "Eternity Tiles"},
                      {"namespace": "ets", "key": "supplier", "type": "single_line_text_field", "value": "Eternity Tiles"}]
        for k, v in mf.items():
            metafields.append({"namespace": "ets", "key": k, "type": "single_line_text_field", "value": v})
        for k, v in (("width_mm", w), ("depth_mm", d), ("height_mm", h)):
            if v:
                metafields.append({"namespace": "ets", "key": k, "type": "number_integer", "value": str(v)})
        out.append({
            "title": title, "descriptionHtml": desc, "vendor": "Excellent Tiling Services", "productType": ptype,
            "status": "ACTIVE", "category": CAT,
            "tags": sorted(set(tags + [PERTH, "ebay-pickup-only", "supplier-import", "cost-estimate"])),
            "seo": {"title": f"{title} | Toilets | ETS Perth"[:60] if len(title) <= 36 else f"{title} | ETS Perth", "description": seo_desc},
            "metafields": metafields,
            "productOptions": [{"name": "Title", "values": [{"name": "Default Title"}]}],
            "files": [{"originalSource": staged[f], "alt": alt, "contentType": "IMAGE"} for f, alt in images],
            "variants": [{"optionValues": [{"optionName": "Title", "name": "Default Title"}],
                          "price": f"{rrp:.2f}", "inventoryPolicy": "CONTINUE", "taxable": True, "barcode": sku,
                          "inventoryItem": {"sku": sku, "cost": f"{rrp * 0.5:.2f}", "tracked": False,
                                            "measurement": {"weight": {"value": kg, "unit": "KILOGRAMS"}}}}],
        })
    return out


if __name__ == "__main__":
    rows = build(json.load(open(sys.argv[1])))
    json.dump(rows, open(sys.argv[2], "w"), indent=1)
    for r in rows:
        v = r["variants"][0]
        print(f'{r["title"]:52} {v["inventoryItem"]["sku"]:20} ${v["price"]:>8}  cost ${v["inventoryItem"]["cost"]:>7}  {len(r["files"])} img  {len(r["descriptionHtml"].split())} words')
