"""RLA Polymers range -> Shopify productSet inputs.

The two catalogues the owner was given (photo, 28 Oct 2026): the RLA TILING Product Range 2026 (V2) and the
GRIPSET Waterproofing Product Guide (V1; Gripset is RLA's waterproofing brand). The RLA Sealants Catalogue 2026 was
also read before the photo arrived; its sealants-only items stay in this file under SEALANTS_ONLY but are NOT created
unless INCLUDE_SEALANTS_CATALOGUE is True.

Sources: the catalogue PDFs (rlapolymers.com.au/catalogues/ and gripset.com/services/), product pages on
rlapolymers.com.au and gripset.com for the long descriptions, photos and the TDS/SDS links. Everything is created as a DRAFT:
nothing is visible to customers until the owner sets a product to Active.

Pricing (owner, 28 Oct 2026: "research market price and go below competition, but not too much"):
- No RLA cost yet (trade account not approved), so every product is tagged `needs-cost` and has no trade band.
- price = a little under the lowest common Australian retail price found online on 28 Oct 2026 (see MARKET in
  each entry and rla-market-prices-2026-10-28.csv). Where B&B Hardware (Maddington) sells the item the
  playbook rule applies: 5% under B&B, rounded down to 5c. Items with no online price are priced from the
  nearest RLA product and tagged `price-check`.
- Once the RLA price list arrives: check every price against the floor (cost x 1.1 x 1.25), set the trade
  band, remove `needs-cost` / `price-check`.

Usage: rla_2026_10.py staged.json out.json [prices.csv]
  staged.json: {filename: staged upload resourceUrl} for the images in rla-images/
"""
import csv, json, sys

VENDOR = "RLA"
SUPPLIER = "RLA Polymers"
CAT = {
    "adhesive": "gid://shopify/TaxonomyCategory/ha-1-5-2",   # Cement, Mortar & Concrete Mixes (as the Sika adhesive)
    "grout": "gid://shopify/TaxonomyCategory/ha-1-5-3",      # Grout
    "waterproofing": "gid://shopify/TaxonomyCategory/ha-1-8-6",  # Waterproofing Coatings
    "sealant": "gid://shopify/TaxonomyCategory/ha-1-8",      # Protective Coatings & Sealants
    "primer": "gid://shopify/TaxonomyCategory/ha-1-6-3",     # Primers
    "gun": "gid://shopify/TaxonomyCategory/ha-15-6-3",       # Caulking Guns
    "cleaner": "gid://shopify/TaxonomyCategory/hg-10-6-11-16-3",  # Grout Cleaners
}
TDS_SDS = "<p><a href=\"{tds}\" target=\"_blank\" rel=\"noopener\">Technical data sheet (PDF)</a> · <a href=\"{sds}\" target=\"_blank\" rel=\"noopener\">Safety data sheet (PDF)</a></p>"
PERTH_LINE = " Buy online or pick up in Maddington, Perth."

# shipping classes -> tags, ets.freight_class, ebay tag
SHIP = {
    "parcel": (["ship-parcel", "ebay-post-15"], "Parcel"),
    "parcel20": (["ship-parcel", "ebay-post-20"], "Parcel"),
    "bulky": (["ship-parcel", "ship-bulky", "ebay-post-39"], "Bulky parcel"),
    "local": (["ship-local-only", "ebay-pickup-only"], "Perth only (local delivery / pickup)"),
}


INCLUDE_SEALANTS_CATALOGUE = False
SEALANTS_ONLY = {"silikon-100", "silikon-200", "silikon-300", "silikon-400", "silikon-600", "roof-gutter", "wet-area",
                 "gap-filler", "ultragrip", "flex-pro-pu", "flex-pro-50fc", "flex-pro-ms", "flex-pro-ms-hd", "firepro-fr",
                 "max-smp-crystal", "max-grab"}


def ul(items):
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def html(intro, uses=None, specs=None, notes=None, tds=None, sds=None, box=None, colours=None):
    out = "".join(f"<p>{p}</p>" for p in intro)
    if uses:
        out += "<h3>Use it for</h3>" + ul(uses)
    if colours:
        out += "<h3>Colours</h3><p>" + ", ".join(colours) + ".</p>"
    if specs:
        out += "<h3>Specifications</h3>" + ul(specs)
    if box:
        out += "<h3>What's in the box</h3>" + ul(box)
    if notes:
        out += "<h3>Good to know</h3>" + ul(notes)
    if tds and sds:
        out += TDS_SDS.format(tds=tds, sds=sds)
    elif tds:
        out += f"<p><a href=\"{tds}\" target=\"_blank\" rel=\"noopener\">Technical data sheet (PDF)</a></p>"
    return out


CEMENT_NOTES = [
    "Prime porous substrates with RLA Porous Primer and existing tiles, paint or sealed concrete with RLA Non-Porous Primer.",
    "Cement based: wear gloves, eye protection and a dust mask when mixing, and read the safety data sheet.",
    "Apply between 5 °C and 35 °C. Keep the bag dry and off the ground; use within the shelf life on the bag.",
]
SIL_NOTES = [
    "Surfaces must be clean, dry and free of soap, grease and old sealant. Mask the joint for a neat line and tool it within the skin time.",
    "Neutral cure: no vinegar smell and safe on metal, stone and mirror backing. Not paintable.",
    "Standard 300 to 310 g cartridge, fits any 300 ml caulking gun. Store below 30 °C.",
]

# ---------------------------------------------------------------------------------------------------
# Products. Each entry: key, title, type, cat, tags (extra), ship, weight_kg (per variant or single),
# price (single) or variants [(option values dict, sku, price, weight)], options [names], desc, seo_title,
# seo_desc, metafields (material, range, warranty), images [(file, alt)], market (note), price_check bool.
# ---------------------------------------------------------------------------------------------------
P = []


def add(**k):
    P.append(k)


# ============================== TILE ADHESIVES (Tiling Catalogue p3-5) ==============================
ADH_TAGS = ["Hardware", "Adhesives & Additives", "Tile Adhesive"]

add(key="tilebond-extra", title="RLA TileBond Extra White Tile Adhesive 20kg", type="Adhesives", cat="adhesive",
    tags=ADH_TAGS + ["C1E", "price-check"], ship="local", weight=20, price=23.95, sku="RL7110-20",
    market="Beaumont Tiles $31.25 (28 Oct 2026); no other online listing. Beaumont runs well above trade shops, so priced as RLA's basic white cement adhesive, under Mastik.",
    material="White cement based tile adhesive, C1E to AS ISO 13007", range="TileBond Extra, 20kg bag (covers about 4 to 5m²)", warranty="RLA 10 year product guarantee when applied to the data sheet",
    images=[("tilebond-extra.jpg", "RLA TileBond Extra 20kg white tile adhesive bag")],
    desc=html(["RLA TileBond Extra is a plain white cement based tile adhesive for rigid fixing: pavers, landscaping and everyday ceramic and stone tiling where the substrate does not move. It is the economical choice in the RLA range and mixes with RLA Plastinex additive when you need flexibility or want to tile over a waterproofing membrane.",
               "A white adhesive, so it will not show through light stone or translucent mosaics."],
              uses=["Walls and floors, internal and external", "Concrete floors and walls, rendered brickwork and blockwork", "Pavers, steps and landscaping", "Ceramic, stone and mosaic tiles (not green marble or moisture sensitive stone)"],
              specs=["Classification: C1E (cementitious, normal strength, extended open time)", "Colour: white", "Bag: 20kg", "Coverage: about 4 to 5m² per bag", "Dry time: 24 hours before grouting", "Low VOC", "RLA 10 year guarantee"],
              notes=["Rigid adhesive: add RLA Plastinex for flexible or membrane applications.", "Not for moisture sensitive stone: use RLA StoneSet."] + CEMENT_NOTES,
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/07/RLA-Tilebond-Extra_TDS-23-7-24.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/rla_tilebond_extra-aust_-_sds-2.pdf"))

add(key="moreflex", title="RLA MoreFlex Flexible Tile Adhesive 20kg Grey", type="Adhesives", cat="adhesive",
    tags=ADH_TAGS + ["C1ETS1", "Flexible Adhesive", "price-check"], ship="local", weight=20, price=27.95, sku="510013",
    market="Beaumont Tiles $34.75 (28 Oct 2026); no trade-shop listing found. Priced just above TileFlex's trade price level.",
    material="Grey rubber modified cement based tile adhesive, C1ETS1 to AS ISO 13007", range="MoreFlex, 20kg bag (covers about 8 to 10m²)", warranty="RLA 10 year product guarantee when applied to the data sheet",
    images=[("moreflex.png", "RLA MoreFlex 20kg grey flexible tile adhesive bag")],
    desc=html(["RLA MoreFlex is a rubber modified, flexible, grey cement based tile adhesive with very good coverage: a 20kg bag spreads 8 to 10m² with a 10mm notched trowel. The rubber filler gives it the flex to take up normal building movement and the non-lipping body tilers want on floors.",
               "An economical everyday adhesive for most ceramic and porcelain tiles, inside or out."],
              uses=["Internal and external walls and floors", "Concrete, plasterboard, fibre cement, rendered brickwork and blockwork", "Ceramic and porcelain tiles (not moisture sensitive stone or marble)", "Over RLA approved waterproofing membranes"],
              specs=["Classification: C1ETS1 (flexible, extended open time, reduced slip)", "Colour: grey", "Bag: 20kg", "Coverage: about 8 to 10m² per bag", "Dry time: 24 hours before grouting", "RLA 10 year guarantee"],
              notes=["Grey adhesive: use a white adhesive such as TileFlex or Mastik under light stone and translucent mosaics."] + CEMENT_NOTES,
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/07/RLA-Moreflex_TDS-23-7-24.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2024/04/Moreflex-Issue-Date-25-08-2023-Code.-RL7166-20.pdf"))

add(key="tileflex", title="RLA TileFlex Premium Flexible Tile Adhesive 20kg White", type="Adhesives", cat="adhesive",
    tags=ADH_TAGS + ["C2TES1", "Flexible Adhesive", "Large Format"], ship="local", weight=20, price=26.95, sku="RL7145-20",
    market="Tilers Direct $27.50 (28 Oct 2026).",
    material="White rubber modified cement based tile adhesive, C2TES1 to AS ISO 13007", range="TileFlex, 20kg bag (covers about 7 to 8m²)", warranty="RLA 10 year product guarantee when applied to the data sheet",
    images=[("tileflex.png", "RLA TileFlex 20kg white premium flexible tile adhesive bag")],
    desc=html(["RLA TileFlex is the premium grade rubber modified adhesive in the RLA range: white, highly flexible, non slump and rated C2TES1. It holds large format wall tiles without slipping and has the improved bond strength porcelain needs.",
               "Use it for internal and external walls and floors over concrete, fibre cement, plasterboard, render and RLA approved membranes."],
              uses=["Large format porcelain and ceramic tiles on walls and floors", "Bathrooms, laundries, kitchens and balconies", "Concrete, fibre cement sheet, plasterboard, rendered brickwork and blockwork", "Over RLA approved waterproofing membranes"],
              specs=["Classification: C2TES1 (improved strength, reduced slip, extended open time, deformable)", "Colour: white", "Bag: 20kg", "Coverage: about 7 to 8m² per bag", "Dry time: 24 hours before grouting", "RLA 10 year guarantee"],
              notes=["Not for moisture sensitive stone or marble: use RLA StoneSet.", "Back butter tiles 400 x 400mm and larger."] + CEMENT_NOTES,
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/07/RLA-Tileflex_TDS-23-7-24.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/RLA_TileFlex-Aust_-_SDS-9.pdf"))

add(key="addflextra", title="RLA AddFlextra Polymer Modified Tile Adhesive 20kg White", type="Adhesives", cat="adhesive",
    tags=ADH_TAGS + ["C2TES1", "Flexible Adhesive", "Large Format"], ship="local", weight=20, price=36.55, sku="RL7550-20",
    market="B&B Hardware Maddington $38.50 -> 5% under = $36.55 (playbook). Tilers Direct $33.85.",
    material="White rubber modified cement based tile adhesive, C2TES1 to AS ISO 13007, respirable silica free", range="AddFlextra, 20kg bag (covers about 10 to 12m²)", warranty="RLA 10 year product guarantee when applied to the data sheet",
    images=[("addflextra.png", "RLA AddFlextra 20kg white polymer modified tile adhesive bag")],
    desc=html(["RLA AddFlextra is a rubber modified, flexible, white cement based tile adhesive with the highest coverage in the range: 10 to 12m² from a 20kg bag. It is strong, non slump and made for large format and low porosity porcelain tiles.",
               "It can also go over existing tiles once they are primed with RLA Non-Porous Primer, so a bathroom can be re-tiled without stripping the old tiles. Free from respirable crystalline silica."],
              uses=["Large format and low porosity porcelain tiles", "Tiling over existing tiles (primed with RLA Non-Porous Primer)", "Internal and external walls and floors", "Concrete, plasterboard, fibre cement sheet, rendered brickwork and blockwork"],
              specs=["Classification: C2TES1 (improved strength, reduced slip, extended open time, deformable)", "Colour: white", "Bag: 20kg", "Coverage: about 10 to 12m² per bag", "Dry time: 24 hours before grouting", "Low VOC, respirable silica free"],
              notes=["Not for moisture sensitive stone or marble: use RLA StoneSet.", "Back butter tiles 400 x 400mm and larger."] + CEMENT_NOTES,
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2025/11/rla-addflextra_tds.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2023/05/addflextra-aust_-_sds-10.pdf"))

add(key="trade-mastik", title="RLA Trade Mastik Polymer Modified Tile Adhesive 20kg White", type="Adhesives", cat="adhesive",
    tags=ADH_TAGS + ["C1TES1", "Flexible Adhesive", "New"], ship="local", weight=20, price=24.75, sku="510020",
    market="Tilers Online $25.00, Turbo Building Group $28.83 (28 Oct 2026).",
    material="White polymer modified cement based tile adhesive, C1TES1 to AS ISO 13007", range="Trade Mastik, 20kg bag (covers about 7m²)", warranty="RLA 10 year product guarantee when applied to the data sheet",
    images=[("trade-mastik.png", "RLA Trade Mastik 20kg white tile adhesive bag")],
    desc=html(["RLA Trade Mastik is the new economy version of RLA Mastik: a smooth, white, polymer modified cement based tile adhesive with good adhesion, flex and non slump properties, rated C1TES1. It suits everyday internal and external wall and floor tiling where a C2 rating is not called for.",
               "Spreads about 7m² per 20kg bag with a 10mm notched trowel."],
              uses=["Everyday wall and floor tiling, internal and external", "Concrete, fibre cement sheeting, plasterboard, rendered brickwork and blockwork", "Ceramic and porcelain tiles (not moisture sensitive stone)", "Over RLA approved waterproofing membranes"],
              specs=["Classification: C1TES1 (reduced slip, extended open time, deformable)", "Colour: white", "Bag: 20kg", "Coverage: about 7m² per bag", "Dry time: 24 hours before grouting", "RLA 10 year guarantee"],
              notes=CEMENT_NOTES,
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/07/RLA-Mastik_TDS-23-7-24.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/rla_mastik-aust_-_sds-10.pdf"))

add(key="mastik", title="RLA Mastik Premium Flexible Tile Adhesive 20kg", type="Adhesives", cat="adhesive",
    tags=ADH_TAGS + ["C2TES1", "Flexible Adhesive", "Large Format", "Green Tag"], ship="local", options=["Colour"],
    variants=[({"Colour": "White"}, "RL7152-20", 25.60, 20), ({"Colour": "Grey"}, "RL7122-20", 25.60, 20)],
    market="B&B Hardware Maddington white $26.95 -> 5% under = $25.60 (playbook). TradieCart $27.23 inc, Tilers Direct $28.60.",
    material="Polymer modified cement based tile adhesive, C2TES1 to AS ISO 13007, respirable silica free, Green Tag certified", range="Mastik, 20kg bag, white or grey (covers about 7m²)", warranty="RLA 10 year product guarantee when applied to the data sheet",
    images=[("mastik.png", "RLA Mastik 20kg white tile adhesive bag")],
    desc=html(["RLA Mastik is the most popular adhesive in the RLA range: a premium, flexible, polymer modified cement based tile adhesive rated C2TES1, Green Tag certified and free from respirable crystalline silica. It has great mastic properties, grabs the tile and does not slump, so it suits large format wall and floor tiles.",
               "Choose white for light stone and mosaics or grey for floors and dark tiles. Bonds most ceramic and porcelain tiles to concrete, render, brick, block, plasterboard, fibre cement and RLA approved membranes."],
              uses=["Large format porcelain and ceramic tiles, walls and floors", "Bathrooms, kitchens, laundries, balconies and living areas", "Concrete, fibre cement sheeting, plasterboard, rendered brickwork and blockwork", "Over RLA approved waterproofing membranes"],
              specs=["Classification: C2TES1 (improved strength, reduced slip, extended open time, deformable)", "Colour: white or grey", "Bag: 20kg", "Coverage: about 7m² per bag", "Dry time: 24 hours before grouting", "Green Tag certified, respirable silica free", "RLA 10 year guarantee"],
              notes=["Not for moisture sensitive stone or marble: use RLA StoneSet.", "Back butter tiles 400 x 400mm and larger."] + CEMENT_NOTES,
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/07/RLA-Mastik_TDS-23-7-24.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/rla_mastik-aust_-_sds-10.pdf"))

add(key="unilite-s1", title="RLA UniLite S1 Lightweight Flexible Tile Adhesive 12.5kg", type="Adhesives", cat="adhesive",
    tags=ADH_TAGS + ["C2TES1", "Lightweight Adhesive", "Flexible Adhesive", "Green Tag", "New"], ship="bulky", options=["Colour"],
    variants=[({"Colour": "White"}, "510005", 31.95, 12.5), ({"Colour": "Grey"}, "510008", 31.95, 12.5)],
    market="Tilers Direct $33.20, Tilers Online $33.50, Mortarmart $33.50 (28 Oct 2026).",
    material="Lightweight polymer modified cement based tile adhesive, C2TES1 to AS ISO 13007, respirable silica free, Green Tag certified", range="UniLite S1, 12.5kg bag, white or grey (covers about 5 to 6m² at 10mm notch; about the yield of a 20kg standard bag)", warranty="RLA product warranty when applied to the data sheet",
    images=[("unilite-s1.png", "RLA UniLite S1 12.5kg lightweight tile adhesive bag")],
    desc=html(["RLA UniLite S1 is a lightweight floor and wall tile adhesive: respirable silica free fillers and advanced polymers give a 12.5kg bag about the same yield as a standard 20kg sand and cement adhesive, so there is less to carry and it spreads more easily. It is flexible, non slip, non slump and has an extended open time.",
               "Rated C2TES1 with high bond strength, it suits large format tiles, porcelain and most ceramic tiles inside and out."],
              uses=["Large format wall and floor tiles", "Bathrooms, kitchens, laundries and balconies", "Concrete, fibre cement sheeting, plasterboard, rendered brickwork and blockwork", "Over RLA approved waterproofing membranes"],
              specs=["Classification: C2TES1 (improved strength, reduced slip, extended open time, deformable)", "Colour: white or grey", "Bag: 12.5kg (lightweight technology)", "Coverage: about 5 to 6m² per bag with a 10mm notched trowel", "Dry time: 24 hours before grouting", "Green Tag certified, respirable silica free"],
              notes=["Lighter bags, same job: budget bags by area, not by weight."] + CEMENT_NOTES,
              tds="https://www.tiledepot.co.nz/data/catalogue/pdf/RLA-Unilite-S1_TDS-23-7-24.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2024/05/RLA-Unilite-S2-Issue-Date-16.11.2023.pdf"))

add(key="unilite-s2", title="RLA UniLite S2 Lightweight Highly Deformable Tile Adhesive 12.5kg", type="Adhesives", cat="adhesive",
    tags=ADH_TAGS + ["C2TES2", "Lightweight Adhesive", "Flexible Adhesive", "Green Tag", "New"], ship="bulky", weight=12.5, price=41.95, sku="510010",
    market="Tilers Online $43.90 (28 Oct 2026).",
    material="Lightweight polymer modified cement based tile adhesive, C2TES2 to AS ISO 13007, respirable silica free, Green Tag certified", range="UniLite S2, 12.5kg bag, white (covers about 5 to 6m² at 10mm notch)", warranty="RLA product warranty when applied to the data sheet",
    images=[("unilite-s2.png", "RLA UniLite S2 12.5kg lightweight highly deformable tile adhesive bag")],
    desc=html(["RLA UniLite S2 is the highly deformable (S2) version of UniLite: a lightweight, high bond strength floor and wall tile adhesive for jobs that move, such as large format porcelain, tiling over timber floors, early age concrete and immersed areas like pools.",
               "Respirable silica free, Green Tag certified, and a 12.5kg bag spreads about as far as a standard 20kg bag."],
              uses=["Large format and thin porcelain panels", "Tiling over timber floors and acoustic underlays (see the data sheet)", "Swimming pools, spas and other immersed areas", "Early age concrete, screeds and render", "Internal and external walls and floors"],
              specs=["Classification: C2TES2 (improved strength, reduced slip, extended open time, highly deformable)", "Colour: white", "Bag: 12.5kg (lightweight technology)", "Coverage: about 5 to 6m² per bag with a 10mm notched trowel", "Dry time: 24 hours before grouting", "Green Tag certified, respirable silica free"],
              notes=CEMENT_NOTES,
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/RLA-Unilite-S2_TDS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2024/05/RLA-Unilite-S2-Issue-Date-16.11.2023.pdf"))

add(key="unigrip", title="RLA UniGrip Premium Highly Flexible Tile Adhesive 15kg White", type="Adhesives", cat="adhesive",
    tags=ADH_TAGS + ["C2S2ET", "Flexible Adhesive", "Large Format", "Pool"], ship="bulky", weight=15, price=36.75, sku="RL7153-15",
    market="B&B Hardware Maddington $38.95 -> 5% under = $37.00; Tilers Direct $36.80, so $36.75.",
    material="White polymer modified cement based tile adhesive, C2S2ET to AS ISO 13007", range="UniGrip, 15kg bag (covers about 6 to 7m²)", warranty="RLA 10 year product guarantee when applied to the data sheet",
    images=[("unigrip.png", "RLA UniGrip 15kg white premium flexible tile adhesive bag")],
    desc=html(["RLA UniGrip is a premium grade, highly flexible (S2) polymer modified white adhesive for the hard jobs: porcelain and vitrified tiles, large format, tile over existing tiles, over most waterproofing membranes and some acoustic mats, and fully immersed pools and spas. It is non slip and non slump and can go over green screeds.",
               "One adhesive for the whole bathroom, balcony or pool surround."],
              uses=["Porcelain, vitrified and large format tiles", "Swimming pools, spas and water features (fully immersed)", "Tiling over existing tiles and over RLA approved membranes", "Green screeds and some acoustic mats (check the data sheet)", "Internal and external walls and floors"],
              specs=["Classification: C2S2ET (improved strength, highly deformable, extended open time, reduced slip)", "Colour: white", "Bag: 15kg", "Coverage: about 6 to 7m² per bag", "Dry time: 24 hours before grouting; pools need the full cure in the data sheet before filling", "RLA 10 year guarantee"],
              notes=["Not for moisture sensitive stone or marble: use RLA StoneSet."] + CEMENT_NOTES,
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/07/RLA-Unigrip_TDS-23-7-24.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/Unigrip-Aust_-_SDS-6.pdf"))

add(key="fastset", title="RLA FastSet Rapid Setting Tile Adhesive 20kg Grey", type="Adhesives", cat="adhesive",
    tags=ADH_TAGS + ["C2S1FTE", "Rapid Set", "Flexible Adhesive", "price-check"], ship="local", weight=20, price=44.95, sku="RL7132-20",
    market="Beaumont Tiles $67.95 (28 Oct 2026); no trade-shop listing found. Beaumont sells Mastik at $47 against $27 elsewhere, so priced at the trade level of a rapid set.",
    material="Grey polymer modified rapid setting cement based tile adhesive, C2S1FTE to AS ISO 13007", range="FastSet, 20kg bag (covers about 5 to 6m²)", warranty="RLA product warranty when applied to the data sheet",
    images=[("fastset.png", "RLA FastSet 20kg grey rapid setting tile adhesive bag")],
    desc=html(["RLA FastSet is a rapid setting, polymer modified grey tile adhesive for jobs that cannot wait: grout after 3 hours, walk on it after 6. It is non slump, so it also handles large format tiles, and it can go over 24 hour green sand and cement screeds.",
               "Bonds porcelain, ceramic, natural stone, terrazzo and mosaics to concrete, render, brick, block, plasterboard and fibre cement, inside or out, and over most waterproofing membranes."],
              uses=["Shop fit-outs, doorways, stairs and repairs that must reopen the same day", "Grouting the same day as fixing", "Over 24 hour green sand and cement screeds", "Low to medium moisture sensitive (Class A) stone", "Internal and external walls and floors"],
              specs=["Classification: C2S1FTE (improved strength, deformable, fast setting, reduced slip, extended open time)", "Colour: grey", "Bag: 20kg", "Coverage: about 5 to 6m² per bag", "Grout after 3 hours, foot traffic after 6 hours", "Polymer modified, non slump"],
              notes=["Short pot life: mix only what you can lay in the working time on the data sheet.", "Dimensionally unstable (curling) stone must be checked for suitability before laying."] + CEMENT_NOTES,
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/07/RLA-Fastset_TDS-23-7-24.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2023/05/RLA-Fast-Set_2022_December_23_AUS_EN.pdf"))

add(key="stoneset", title="RLA StoneSet Rapid Setting Stone Adhesive 20kg White", type="Adhesives", cat="adhesive",
    tags=ADH_TAGS + ["C2S1FTE", "Rapid Set", "Stone Adhesive", "price-check"], ship="local", weight=20, price=64.95, sku="RL7131-20",
    market="Beaumont Tiles $104.75 (28 Oct 2026); TradieCart lists it without a price. Priced from Beaumont's mark-up on the rest of the range.",
    material="White polymer modified rapid setting cement based tile adhesive, C2S1FTE to AS ISO 13007", range="StoneSet, 20kg bag (covers about 5 to 6m²)", warranty="RLA product warranty when applied to the data sheet",
    images=[("stoneset.png", "RLA StoneSet 20kg white rapid setting stone adhesive bag")],
    desc=html(["RLA StoneSet is the adhesive for natural stone that stains, discolours or effloresces when it stays wet: the premium white cement base sets fast (grout in 2 hours, foot traffic in 4), so residual moisture does not sit under the stone. Non slump, so it suits large format slabs, and usable over 24 hour green screeds, most waterproofing membranes and in immersed areas such as pools.",
               "Also a fast white adhesive for porcelain, ceramic, terrazzo and mosaics."],
              uses=["Marble, limestone, travertine and other moisture sensitive (Class A) stone", "Light coloured stone and mosaics that need a white bed", "Pools, spas and water features", "Over 24 hour green screeds and most waterproofing membranes", "Internal and external walls and floors"],
              specs=["Classification: C2S1FTE (improved strength, deformable, fast setting, reduced slip, extended open time)", "Colour: white", "Bag: 20kg", "Coverage: about 5 to 6m² per bag", "Grout after 2 hours, foot traffic after 4 hours", "Polymer modified, non slump"],
              notes=["Short pot life: mix small batches.", "Resin backed and dimensionally unstable stone must be checked for suitability before laying."] + CEMENT_NOTES,
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/07/RLA-Stoneset_TDS-23-7-24.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/RLA_Stone_set-Aust_-_SDS-2.pdf"))

add(key="polymastic", title="RLA PolyMastic Pre-Mixed Wall Tile Adhesive", type="Adhesives", cat="adhesive",
    tags=ADH_TAGS + ["D1E", "Pre-Mixed Adhesive", "Wall Tiles"], options=["Size"],
    variants=[({"Size": "4 L"}, "RL7194-4", 34.95, 5.6, "parcel20"), ({"Size": "15 L"}, "RL7194-15", 94.95, 21, "local")],
    market="15 L: Adheseal $87.39 ex GST ($96.13 inc), $112.91 ex on another listing (28 Oct 2026). 4 L: no listing, priced pro rata (price-check).", price_check_variants=["4 L"],
    material="White acrylic pre-mixed tile adhesive, D1E to AS ISO 13007", range="PolyMastic, 4 L or 15 L pail (covers about 7 to 10m² per 15 L)", warranty="RLA 10 year product guarantee when applied to the data sheet",
    images=[("polymastic-pre-mixed-tile-adhesive.png", "RLA PolyMastic pre-mixed tile adhesive pail")],
    desc=html(["RLA PolyMastic is a ready to use white acrylic wall tile adhesive: open the pail and start spreading, no mixing, no dust. Its superior non slump grab is made for larger internal wall tiles, and it is flexible enough for plasterboard and fibre cement.",
               "Bonds porous ceramic and mosaic tiles to internal walls. Choose the 4 L pail for a splashback or small feature wall and the 15 L pail for a bathroom."],
              uses=["Internal wall tiling: bathrooms, kitchens, laundries and splashbacks", "Porous ceramic, mosaic and glass mosaic tiles", "Plasterboard, fibre cement sheeting, rendered brickwork and blockwork"],
              specs=["Classification: D1E (dispersion adhesive, extended open time)", "Colour: white", "Pail: 4 L or 15 L", "Coverage: about 7 to 10m² per 15 L pail", "Dry time: about 4 hours before grouting on porous tiles", "Low VOC", "RLA 10 year guarantee"],
              notes=["Walls only, internal and dry areas: use a cement based adhesive for floors, wet areas and porcelain.", "Reseal the pail after use; store between 5 °C and 30 °C."],
              tds="https://www.tiledepot.co.nz/data/catalogue/pdf/RLA-Polymastic_TDS-23-7-24.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/rla_mastik-aust_-_sds-10.pdf"))

# ============================== WATERPROOFING (Tiling Catalogue p7-11) ==============================
WP_TAGS = ["Hardware", "Waterproofing", "Waterproofing Membrane"]
WP_TYPE = "Waterproofing Membranes"   # new type: the Waterproofing and Hardware collections were given a rule for it
WP_NOTES = ["Prime with RLA Porous Primer or Non-Porous Primer to suit the substrate, and use a bond breaker (RLA corners, Flex-Pro MS or sealant) at all wall/floor junctions and movement joints.",
            "Two coats at right angles to the dry film thickness in the data sheet; reinforce junctions with RLA Waterproof Tape.",
            "Waterproofing of wet areas in WA must be done by a licensed waterproofer to AS 3740."]

add(key="wpu", title="RLA WPU Class III Internal & External Waterproofing Membrane", type=WP_TYPE, cat="waterproofing",
    tags=WP_TAGS + ["Class III", "UV Stable"], options=["Size"],
    variants=[({"Size": "4 L"}, "14443", 94.05, 5, "parcel20"), ({"Size": "15 L"}, "14442", 166.25, 18, "local")],
    market="B&B Hardware Maddington 15 L $175.00 -> 5% under = $166.25; 4 L $99.00 -> $94.05 (playbook). SealMart 15 L $159.50, GD Building Supplies $134.",
    material="One part water based elastomeric polyurethane/acrylic fibre reinforced membrane, Class III to AS 4858", range="WPU, 4 L or 15 L pail, grey", warranty="RLA product warranty when applied to the data sheet and AS 3740",
    images=[("wpu.png", "RLA WPU Class III waterproofing membrane pail")],
    desc=html(["RLA WPU is the all rounder membrane: a one part, water based, fibre reinforced polyurethane/acrylic membrane rated Class III, CSIRO certified for external use and UV stable, so it works in showers and laundries and on balconies, decks and roofs where it will see sun and occasional foot traffic.",
               "Tough, flexible, fast drying and water clean-up."],
              uses=["Bathrooms, showers, kitchens and laundries", "Balconies, decks and roofs (occasional traffic)", "Internal and external wet areas, residential and commercial", "Concrete (28 days old), render and masonry, cement sheet, wet area plasterboard, structural plywood, brick and Hebel"],
              specs=["Class III membrane to AS 4858:2004, applied to AS 3740", "Colour: grey", "Pail: 4 L or 15 L", "Dry film thickness: 0.5mm walls, 0.9mm floors (two coats)", "CSIRO certified for external use, UV stable", "Low VOC, water based, single pack"],
              notes=WP_NOTES,
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2026/07/rla-wpu_tds.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2026/05/RLA_WPU_Membrane_-Aust_-_SDS.pdf"))

add(key="wpm", title="RLA WPM Class III Wet Area Waterproofing Membrane 15L", type=WP_TYPE, cat="waterproofing",
    tags=WP_TAGS + ["Class III"], ship="local", weight=18, price=129.95, sku="14510",
    market="GD Building Supplies $134.00, SealMart $141.00, Benton & Sons $179 (28 Oct 2026).",
    material="Waterborne SBR flexible fibre reinforced under tile membrane, Class III to AS 4858", range="WPM, 15 L pail, grey", warranty="RLA product warranty when applied to the data sheet and AS 3740",
    images=[("wpm.png", "RLA WPM Class III wet area waterproofing membrane pail")],
    desc=html(["RLA WPM is the internal wet area membrane: a waterborne, permanently flexible, fibre reinforced membrane for under tiled showers, bathrooms, kitchens and laundries. It is a certified Class III membrane to AS 4858:2004 when applied to AS 3740, and it takes the structural movement a house goes through.",
               "Quick drying, low VOC, single pack."],
              uses=["Showers, bathrooms, kitchens and laundries", "Internal wet areas in homes, units and commercial buildings", "Concrete (28 days old), render and masonry, cement sheet, wet area plasterboard, structural plywood, brick and Hebel"],
              specs=["Class III membrane to AS 4858:2004, applied to AS 3740", "Colour: grey", "Pail: 15 L", "Dry film thickness: 0.5mm walls, 0.9mm floors (two coats)", "Low VOC, water based, single pack, fibre reinforced"],
              notes=["Internal use: for balconies, decks and exposed areas use RLA WPU."] + WP_NOTES,
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2026/07/rla-wpm_tds.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/02/RLA_WPM_Membrane-Aust_-_SDS-16.pdf"))

add(key="safe2o", title="RLA Safe2o Solvent Free SMP Waterproofing Membrane 15kg", type=WP_TYPE, cat="waterproofing",
    tags=WP_TAGS + ["Class III", "SMP", "Green Tag"], ship="local", weight=16, price=199.95, sku="RL1003",
    market="Adheseal $202.50 and $209.60 on two listings, $249.19 ex GST on the collection feed (28 Oct 2026).",
    material="One part moisture cured silyl modified polymer (SMP) membrane, non hazardous, Class III to AS 4858 and AS 4654.1, Green Tag certified", range="Safe2o, 15kg pail, grey", warranty="RLA product warranty when applied to the data sheet",
    images=[("safe2o.png", "RLA Safe2o solvent free SMP waterproofing membrane pail")],
    desc=html(["RLA Safe2o is a polyurethane performance membrane without the solvent, isocyanates or smell: a one part, moisture cured SMP (silyl modified polymer) membrane that is non hazardous, Green Tag certified and goes on in a single coat on floors at 1.2mm dry film for Class III compliance.",
               "Made for under screed and other covered, non exposed and below ground work: retaining walls, planter boxes, internal wet areas and covered balconies. Cures to a tough, elastic, non shrinking membrane with a built in root inhibitor for subterranean use."],
              uses=["Under screed on balconies and decks", "Retaining walls, planter boxes and below ground", "Internal wet areas", "Covered balconies and decks (not UV exposed)"],
              specs=["Class III membrane to AS 4858 and AS 4654.1", "Colour: grey", "Pail: 15kg", "One coat on horizontal surfaces to 1.2mm dry film thickness", "Solvent free, isocyanate free, low odour, no shrinkage", "Green Tag certified"],
              notes=["Not for UV exposed areas unless covered: for exposed membrane use RLA PU850 with ATC top coat.", "Use RLA Primer PU on porous substrates.", "Moisture cured: reseal the pail straight after use."] + WP_NOTES[2:],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/05/RLA-SAFE20_TDS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/rla_safe_20-aust_-_sds-6.pdf"))

add(key="2part", title="RLA 2Part UV Stable Cementitious Waterproofing Membrane Kit 40kg", type=WP_TYPE, cat="waterproofing",
    tags=WP_TAGS + ["Class II", "Cementitious", "Pool"], ship="local", weight=42, price=195.95, sku="RL7190-KIT",
    market="Adheseal $198.15 (also $251.23 ex GST on the feed), SealMart $214.50, Beaumont $401.75 (28 Oct 2026).",
    material="Two part cementitious membrane: high alumina fast setting cement powder mixed with high solids pure acrylic, Class II to AS 4858", range="2Part kit: 20 L Part A liquid + 20kg Part B powder (covers about 16m² at two coats, 1.2mm DFT)", warranty="RLA product warranty when applied to the data sheet",
    images=[("2-part-cementitious-waterproofing-membrane.png", "RLA 2Part cementitious waterproofing membrane kit, Part A and Part B pails")],
    desc=html(["RLA 2Part is a two part cementitious membrane: a fast setting high alumina cement powder mixed with a water resistant pure acrylic. You get the fast drying and strong adhesion of a traditional two part membrane with the toughness, elongation and flexibility of a modern acrylic, and it is UV stable.",
               "The classic choice under tiles on balconies and roofs and in swimming pools, inside or out."],
              uses=["Swimming pools and water features", "Under tile on balconies, roofs and podiums", "Internal and external under tile wet areas", "Concrete, render, blockwork and screeds"],
              specs=["Class II membrane to AS 4858", "Colour: off white", "Kit: 20 L Part A (liquid) + 20kg Part B (powder), 40kg total", "Coverage: about 16m² at two coats with a dry film thickness of 1.2mm", "Fast drying, tough, good elongation, excellent adhesion, UV stable"],
              notes=["Mix Part B into Part A with a drill mixer to a lump free slurry; pot life is short, so mix what you can apply.", "Cement based: wear gloves, eye protection and a dust mask."] + WP_NOTES,
              tds="https://cdn.shopify.com/s/files/1/0015/5369/4792/files/RLA-2-PART-TDS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/rla_mastik-aust_-_sds-10.pdf"))

add(key="1komponent", title="RLA 1Komponent One Part Cementitious Waterproofing Membrane 20kg", type=WP_TYPE, cat="waterproofing",
    tags=WP_TAGS + ["Class I", "Cementitious", "Pool", "Negative Pressure"], ship="local", weight=20, price=184.95, sku="999729",
    market="Tilers Online $195.00 (28 Oct 2026).",
    material="One part flexible fibre reinforced cementitious membrane with graded aggregates and polymers, Class I to AS/NZS 4858 and AS 4654.1", range="1Komponent, 20kg bag, light grey (about 1.17kg/m² per mm of thickness)", warranty="RLA product warranty when applied to the data sheet",
    images=[("1komponent.png", "RLA 1Komponent one part cementitious waterproofing membrane bag")],
    desc=html(["RLA 1Komponent is a just add water cementitious membrane: graded aggregates, fibres and polymers in one bag, mixed on site to a brush, roller, spray or trowel consistency. It is highly flexible for a cement membrane and works under both positive and negative water pressure (5 bar positive, 1.5 bar negative), so it suits tanks, pools, retaining walls and areas with hydrostatic pressure.",
               "Can be applied to damp surfaces, which makes it practical on fresh concrete and below ground."],
              uses=["Under tile internal wet areas (AS/NZS 3740)", "Concrete swimming pools and water tanks", "Retaining walls, planter boxes, balconies and podiums (AS/NZS 4654.2)", "Areas subject to hydrostatic or negative pressure", "Damp substrates and fresh concrete"],
              specs=["Class I membrane to AS/NZS 4858:2004 and AS 4654.1", "Colour: light grey", "Bag: 20kg", "Coverage: about 1.17kg per m² per mm of thickness", "Positive pressure up to 5 bar, negative pressure up to 1.5 bar", "Apply by trowel (best), brush, roller or spray"],
              notes=["Versatile mixing ratio: thicker for trowel, thinner for brush; see the data sheet.", "Cement based: wear gloves, eye protection and a dust mask."] + WP_NOTES,
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2026/04/rla-1k_tds.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/RLA_1_Komponent-Aust_-_SDS-5.pdf"))

add(key="pu850", title="RLA PU850 Moisture Cured Polyurethane Waterproofing Membrane 15L", type=WP_TYPE, cat="waterproofing",
    tags=WP_TAGS + ["Class III", "Polyurethane", "ship-dangerous-goods"], ship="local", weight=17, price=204.95, sku="750599",
    market="SealMart $214.50, Tilers Online $299.00 (28 Oct 2026).",
    material="One part moisture cured polyurethane elastomeric membrane, Class III to AS 4858 and AS 4654.1, tar and bitumen free", range="PU850, 15 L pail, grey (about 1.5 L/m² at 1.2mm DFT)", warranty="RLA product warranty when applied to the data sheet",
    images=[("pu850.png", "RLA PU850 polyurethane waterproofing membrane pail")],
    desc=html(["RLA PU850 is a one part, moisture cured polyurethane membrane that cures to a seamless, tough and permanently flexible film with strong adhesion to primed concrete, render and masonry. It is bitumen free, breathable, resists chemicals and stays elastic in the cold, and it suits both above and below ground work.",
               "For exposed rooftops and decks it is over-coated with RLA ATC aliphatic top coat for UV protection."],
              uses=["Retaining walls and planter boxes", "Internal wet areas, balconies and decks", "Rooftops and exposed areas (with RLA ATC top coat)", "Under screed and below ground"],
              specs=["Class III membrane to AS 4858 and AS 4654.1", "Colour: grey", "Pail: 15 L", "Coverage: about 1.5 L per m² at 1.2mm dry film thickness", "Tar and bitumen free, permanently flexible, light foot traffic", "Prime with RLA Primer PU"],
              notes=["Solvent based: ventilate, keep away from flame and read the safety data sheet. Road freight only.", "Moisture cured: reseal the pail straight after use and use within the pot life once opened."] + WP_NOTES[2:],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2025/05/PU850.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/rla_pu850-aust_-_sds-1.pdf"))

add(key="atc", title="RLA ATC Aliphatic Top Coat UV Protective Polyurethane Coating 15L", type=WP_TYPE, cat="waterproofing",
    tags=WP_TAGS + ["Top Coat", "UV Stable", "Polyurethane", "ship-dangerous-goods", "price-check"], ship="local", weight=16, price=229.95, sku="RLA-ATC-15",
    market="No Australian retail listing found (28 Oct 2026); priced a step above PU850, which it goes over.",
    material="One part moisture cured transparent aliphatic polyurethane coating", range="ATC Aliphatic Top Coat, 15 L (about 200 to 300g/m²)", warranty="RLA product warranty when applied to the data sheet",
    images=[("atc.png", "RLA ATC aliphatic top coat tin")],
    desc=html(["RLA ATC is the clear, UV stable aliphatic polyurethane coating that goes over RLA PU850 on rooftops, decks and any membrane left exposed to the sun. It cures to an elastic, durable film with high mechanical, chemical, tensile and tear resistance, a quick tack free time, and it stands up to ponding water and light foot traffic.",
               "Roll, brush or airless spray it on."],
              uses=["Protecting exposed RLA PU850 membrane on roofs and decks", "Exposed balconies, walkways and plant decks", "Areas with ponding water"],
              specs=["Colour: transparent", "Size: 15 L", "Coverage: about 200 to 300g per m²", "Application: roller, brush or airless spray", "External use, UV stable, resists ponding water"],
              notes=["Apply once the PU850 has cured; see the data sheet for the recoat window.", "Solvent based: ventilate, keep away from flame and read the safety data sheet. Road freight only."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2025/01/RLA-ATC_TDS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/01/ATC-Aliphatic-top-Coat.pdf"))

add(key="moisture-seal", title="RLA Moisture Seal Two Part Epoxy Water Vapour Barrier Kit", type=WP_TYPE, cat="waterproofing",
    tags=WP_TAGS + ["Epoxy", "Vapour Barrier", "Primer", "price-check"], options=["Size"],
    variants=[({"Size": "8 L kit"}, "15636", 219.95, 10, "bulky"), ({"Size": "20 L kit"}, "15637", 479.95, 24, "local")],
    market="20 L kit: Adheseal $459.03 ex GST ($504.93 inc), TradieCart lists it without a price (28 Oct 2026). 8 L kit: no listing, priced pro rata.",
    material="Two part water based epoxy water and vapour barrier, 1:1 mix, complies with AS 4020:2005 and ASTM E96", range="Moisture Seal, 8 L or 20 L kit (Part A + Part B), about 4 to 5m² per litre", warranty="RLA product warranty when applied to the data sheet",
    images=[("moisture-seal.png", "RLA Moisture Seal epoxy vapour barrier kit pails")],
    desc=html(["RLA Moisture Seal is a two part, water based epoxy that stops water and water vapour coming up through concrete: a primer and barrier under waterproofing membranes, tiles, vinyl, timber flooring and epoxy floors, and a damp surface primer where rising damp or hydrostatic pressure would lift anything else.",
               "Mixed 1:1, it withstands a 25 metre head of water (250 kPa), complies with AS 4020 for contact with drinking water, can go on green or damp concrete and cleans up with water."],
              uses=["Sealing concrete slabs before vinyl, timber or tile overlays", "Primer for damp surfaces, Scyon sheeting, membranes and RLA tile adhesives", "Basements, retaining walls, planter boxes, lift wells, tanks and underground car parks", "Dust sealing interior concrete floors", "Base coat for seamless epoxy flooring"],
              specs=["Two part epoxy, mixing ratio 1:1 (A:B)", "Kit: 8 L or 20 L", "Coverage: about 4 to 5m² per litre", "Wet film 200 microns, dry film about 100 microns per coat", "Full cure 5 to 7 days at 25 °C and 50% RH", "Withstands 25m head of water (250 kPa); AS 4020:2005 drinking water; ASTM E96 vapour transmission", "Low VOC, water based"],
              notes=["Mix only what you can apply in the pot life; see the data sheet.", "Wear gloves and eye protection; read the Part A and Part B safety data sheets."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2025/10/rla-moisture-seal_tds.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/RLA_moisture_Seal_Part_A-Aust_-_SDS-32.pdf"))

add(key="primer-pu", title="RLA Primer PU Penetrating Waterproofing Primer 15L", type=WP_TYPE, cat="primer",
    tags=WP_TAGS + ["Primer", "Polyurethane", "ship-dangerous-goods"], ship="local", weight=15, price=204.95, sku="730541",
    market="SealMart $214.50 (28 Oct 2026).",
    material="Single pack solvent based penetrating polyurethane primer", range="Primer PU, 15 L (about 4m² per litre per coat)", warranty="RLA product warranty when applied to the data sheet",
    images=[("primerpu.png", "RLA Primer PU penetrating primer tin")],
    desc=html(["RLA Primer PU is the penetrating primer for RLA's polyurethane products: PU850 membrane, Aqua BT and Flex-Pro PU sealant. It soaks into porous substrates, locks down dust and loose material, improves adhesion and makes the membrane spread more easily.",
               "One part, easy to apply, strong on most porous substrates."],
              uses=["Under RLA PU850 membrane and RLA Safe2o", "Under RLA Flex-Pro PU and other polyurethane sealants", "Concrete, cement render, timber, plasterboard, fibre cement, brick and blockwork"],
              specs=["Colour: transparent", "Size: 15 L", "Coverage: about 4m² per litre per coat; very porous substrates may need two coats", "Internal and external use", "Single pack, solvent based"],
              notes=["Solvent based: ventilate, keep away from flame and read the safety data sheet. Road freight only.", "Let the primer dry before applying the membrane; see the data sheet for the recoat window."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/08/FLEX-PRO-MS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/Flex_Pro_PU-Aust_-_SDS-5.pdf"))

add(key="max-smp-25", title="RLA Max SMP 25 Adhesive Sealant", type="Hybrid Sealants", cat="sealant",
    tags=["Hardware", "Silicone & Sealants", "Hybrid Sealants", "SMP", "Adhesive Sealant", "Green Tag"], options=["Size", "Colour"],
    variants=[({"Size": "480g cartridge", "Colour": "Black"}, "620514", 11.95, 0.55, "parcel"), ({"Size": "480g cartridge", "Colour": "Grey"}, "620515", 11.95, 0.55, "parcel"),
              ({"Size": "480g cartridge", "Colour": "White"}, "620516", 11.95, 0.55, "parcel"), ({"Size": "600ml sausage", "Colour": "Black"}, "620521", 11.95, 0.7, "parcel"),
              ({"Size": "600ml sausage", "Colour": "Grey"}, "620520", 11.95, 0.7, "parcel"), ({"Size": "600ml sausage", "Colour": "White"}, "620519", 11.95, 0.7, "parcel")],
    market="TradieCart 600ml sausage grey $12.65 inc GST (28 Oct 2026). Cartridge priced the same.",
    material="Low modulus silyl modified polymer (SMP) hybrid adhesive sealant, solvent and isocyanate free, Green Tag certified", range="Max SMP 25, 480g cartridge or 600ml sausage, black, grey or white", warranty="RLA product warranty when applied to the data sheet",
    images=[("max-smp-25.png", "RLA Max SMP 25 adhesive sealant cartridge")],
    desc=html(["RLA Max SMP 25 is a high performance hybrid adhesive and sealant with superior adhesion to most building materials: brick, stone, concrete, timber, ceramic tiles, steel, aluminium, tin and plaster. It is solvent free and isocyanate free, so it has no odour, does not shrink or stain, and it can be applied to damp surfaces.",
               "Low modulus with ±25% joint movement, paintable, and excellent weather, UV and ageing resistance. The sealant for window and door joints, high sun and high movement areas, skylights and portable buildings, and a bond breaker under RLA membranes."],
              uses=["Window and door perimeter joints", "High movement and high sun exposure joints", "Skylights, roofing and portable building construction", "Bond breaker at wall/floor junctions under RLA waterproofing membranes", "Bonding trims, panels and fixtures without mechanical fixings"],
              specs=["Type: SMP hybrid adhesive sealant, low modulus", "Movement capability: ±25%", "Sizes: 480g cartridge (fits a 300ml gun) or 600ml foil sausage (needs a sausage gun)", "Colours: black, grey, white", "No isocyanates, no solvents, no shrinkage, paintable, non staining", "Internal and external use, can be applied to damp surfaces", "Green Tag certified"],
              notes=["Tool the joint within the skin time; paint once the surface has skinned.", "No primer needed on most surfaces; test on plastics."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/05/MAX-SMP-25_TDS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/max_smp_25-aust_-_sds-4.pdf"))

WPA_TYPE = "Waterproofing Accessories"  # new type, added to the Waterproofing and Hardware collection rules
add(key="wp-tape", title="RLA Waterproof Tape / Gripset RF Fabric Reinforcing Tape 50m", type=WPA_TYPE, cat="waterproofing",
    tags=["Hardware", "Waterproofing", "Waterproofing Tape", "Gripset", "price-check"], options=["Width"],
    variants=[({"Width": "100mm x 50m"}, "730663", 39.95, 0.8, "parcel"), ({"Width": "200mm x 50m"}, "730662", 64.95, 1.5, "parcel20")],
    market="No RLA listing found (28 Oct 2026); Gripset Elastoproof 80mm x 10m is $30.86 inc, so a 50m scrim roll is priced well under that per metre.",
    material="Open weave non woven polyester reinforcing fabric", range="Waterproof Tape, 100mm or 200mm x 50m roll", warranty="RLA product warranty when used with RLA membranes",
    images=[("crop-wp-tape.png", "RLA Waterproof Tape reinforcing fabric rolls")],
    desc=html(["RLA Waterproof Tape (sold as Gripset RF Fabric in the Gripset guide, same codes) is an open weave polyester fabric that is bedded into the wet membrane at junctions, cracks and bond breakers to give the membrane extra strength and build. It stops the membrane sagging over bond breakers and lets you build the film up where it is needed.",
               "About 2 litres of membrane per square metre of tape is needed to saturate and cover it."],
              uses=["Wall/floor junctions and internal corners in showers and wet areas", "Over bond breakers, control joints and substrate abutments", "Cracks and sheet joints before membrane", "Reinforcing RLA WPU, WPM and 2Part membranes"],
              specs=["Material: non woven polyester fabric, open weave", "Widths: 100mm or 200mm", "Roll length: 50m", "Use with RLA liquid membranes; allow about 2 L of membrane per m² of tape"],
              notes=["Lay the tape into the first wet coat, roll it flat with a brush and cover with the second coat.", "Use RLA pre-formed internal and external corners for the corners and collars for pipe penetrations."]))

CORNER_DESC = ["Pre-formed and heat welded from a tough grade of rubber, RLA waterproofing corners line the wall/floor junction at the corner, where most membranes fail. They give an elastic, rupture resistant seal that takes movement, and they are bedded into the membrane like the tape.",
               "Sold as a box of 25."]
add(key="wp-ext-corner", title="RLA Waterproofing External Corners Pre-Formed Rubber, Box of 25", type=WPA_TYPE, cat="waterproofing",
    tags=["Hardware", "Waterproofing", "Waterproofing Corners", "price-check"], ship="parcel20", weight=1.5, price=124.95, sku="730695",
    market="No RLA listing found (28 Oct 2026); Gripset Elastoproof external corner $9.35 inc each, so a box of 25 is priced at about $5 a corner.",
    material="Pre-formed heat welded rubber", range="External corner, box of 25", warranty="RLA product warranty when used with RLA membranes",
    images=[("crop-wp-ext-corner.png", "RLA waterproofing external corner")],
    desc=html(CORNER_DESC, uses=["External wall/floor junctions (hob and step corners)", "Substrate abutments, control joints, movement and expansion joints", "Bond breaker at external corners under RLA membranes"],
              specs=["Type: external corner, pre-formed and heat welded", "Material: rubber, rupture, chemical and water resistant", "Pack: box of 25"],
              notes=["One part, easy to apply: bed into the first membrane coat and cover with the second.", "Use the matching RLA internal corners and RLA Waterproof Tape for the straight runs."]))
add(key="wp-int-corner", title="RLA Waterproofing Internal Corners Pre-Formed Rubber, Box of 25", type=WPA_TYPE, cat="waterproofing",
    tags=["Hardware", "Waterproofing", "Waterproofing Corners", "price-check"], ship="parcel20", weight=1.5, price=124.95, sku="730696",
    market="No RLA listing found (28 Oct 2026); Gripset Elastoproof internal corner $7.46 inc each, so a box of 25 is priced at about $5 a corner.",
    material="Pre-formed heat welded rubber", range="Internal corner, box of 25", warranty="RLA product warranty when used with RLA membranes",
    images=[("crop-wp-int-corner.png", "RLA waterproofing internal corner")],
    desc=html(CORNER_DESC, uses=["Internal wall/floor junctions in showers, bathrooms and laundries", "Substrate abutments, control joints, movement and expansion joints", "Bond breaker at internal corners under RLA membranes"],
              specs=["Type: internal corner, pre-formed and heat welded", "Material: rubber, rupture, chemical and water resistant", "Pack: box of 25"],
              notes=["One part, easy to apply: bed into the first membrane coat and cover with the second.", "Use the matching RLA external corners and RLA Waterproof Tape for the straight runs."]))
add(key="wp-collar", title="RLA Waterproofing Pipe Collars Tap Sleeves, Box of 25", type=WPA_TYPE, cat="waterproofing",
    tags=["Hardware", "Waterproofing", "Waterproofing Collars", "price-check"], ship="parcel20", weight=1.5, price=124.95, sku="730697",
    market="No RLA listing found (28 Oct 2026); priced like the RLA corners, about $5 each in a box of 25.",
    material="Rubber, high strength with excellent tear resistance", range="Collar / tap sleeve, box of 25", warranty="RLA product warranty when used with RLA membranes",
    images=[("crop-wp-collar.png", "RLA waterproofing pipe collar")],
    desc=html(["RLA collars (tap sleeves) seal the membrane around pipes, drainage outlets, cabling and surface fixtures, the penetrations that move, vibrate and crack a plain membrane. The rubber collar gives a permanent, tight, waterproof and vapour proof seal that keeps working through movement.",
               "High strength with excellent tear resistance, and they can be cut on site to suit the pipe. Sold as a box of 25."],
              uses=["Tap and shower breech penetrations", "Floor waste and drainage outlets", "Pipes, conduits and cabling through membranes", "Any penetration that needs long term protection"],
              specs=["Type: pipe collar / tap sleeve", "Material: rubber, waterproof and vapour barrier, tear resistant", "Can be cut on site", "Pack: box of 25"],
              notes=["Bed into the first membrane coat around the penetration and cover with the second coat.", "Seal the pipe to the collar with RLA Max SMP 25 or Flex-Pro MS."]))

# ============================== GROUT (Tiling Catalogue p12-16) ==============================
GROUT_TAGS = ["Hardware", "Grout", "Tile Grout"]
EF_COLOURS = [("White", "LUM02-4"), ("Alabaster", "LUM82-4"), ("Misty Grey", "LUM41-4"), ("Mudberry", "LUM85-4"), ("Light Beige", "LUM21-4"), ("Magellan", "LUM06-4"),
              ("Travertine", "LUM77-4"), ("Havana", "LUM80-4"), ("Salmon", "LUM39-4"), ("Mustard", "LUM30-4"), ("Macchiato", "LUM88-4"), ("Sky", "LUM14-4"),
              ("Forest", "LUM19-4"), ("Slate Grey", "LUM11-4"), ("Charcoal", "LUM54-4"), ("Black", "LUM55-4")]
add(key="luminous-ef", title="RLA Luminous EF Efflorescence Free Coloured Grout 4kg", type="Grout", cat="grout",
    tags=GROUT_TAGS + ["Coloured Grout", "Green Tag", "Luminous"], options=["Colour"],
    variants=[({"Colour": c}, sku, 34.95, 4, "parcel") for c, sku in EF_COLOURS],
    market="Tilers Direct $36.00 a bag, Turbo Building Group $37.05, Beaumont $50.50 (28 Oct 2026).",
    material="Cement based efflorescence free coloured tile grout, respirable silica free, Green Tag certified", range="Luminous EF, 4kg bag, 16 colours, joints up to 20mm", warranty="RLA product warranty when applied to the data sheet",
    images=[("luminous-ef.png", "RLA Luminous EF grout 4kg bag, white"), ("luminous-range.png", "RLA Luminous grout colour range")],
    desc=html(["RLA Luminous EF is a rapid setting coloured tile grout made with efflorescence free technology, so the white bloom that spoils dark cement grouts does not happen. It is silica free, shrinkage compensated, abrasion resistant and colour fast, with a smooth finish that resists dirt and stains, low water absorption and built in water and mould resistance.",
               "Grouts joints up to 20mm wide, inside and out, and in immersed areas like pools. Sixteen colours, matched to RLA Luminous Silicone for the perimeter joints."],
              uses=["Wall and floor tile joints up to 20mm, internal and external", "Bathrooms, kitchens, laundries, balconies and pools", "Porcelain, ceramic, stone and mosaic tiles", "Any job where a dark grout must stay dark"],
              colours=[c for c, _ in EF_COLOURS],
              specs=["Type: cement based coloured grout, efflorescence free, respirable silica free", "Bag: 4kg", "Joint width: up to 20mm", "Rapid setting, extended open time, immersible", "Water and mould resistant, anti fading, shrinkage compensated", "Green Tag certified, extremely low VOC"],
              notes=["Colour chips are a guide; the finished colour depends on mixing water and curing. Mix bags of the same batch for one area.", "Mix with clean water only or with RLA Plastinex for flexibility; wash off within the clean-up time on the bag.", "Seal the perimeter with the matching RLA Luminous Silicone, not grout."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2026/05/rla-luminous-ef-grout_tds.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2024/04/RLA_Luminous_Grouts-Aust_-_SDS.pdf"))

SSG_COLOURS = [("White", "02"), ("Alabaster", "82"), ("Misty Grey", "41"), ("Mudberry", "85"), ("Light Beige", "21"), ("Magellan", "06"),
               ("Travertine", "77"), ("Havana", "80"), ("Macchiato", "88"), ("Slate", "11"), ("Charcoal", "54"), ("Black", "55")]
SSG_CHEAP10 = {"White", "Misty Grey", "Magellan", "Slate"}  # Adheseal 10kg $36.58 ex on these, $55.73 ex on the rest
add(key="luminous-ssg", title="RLA Luminous SSG Smooth Coloured Grout", type="Grout", cat="grout",
    tags=GROUT_TAGS + ["Coloured Grout", "Luminous"], options=["Colour", "Size"],
    variants=[v for c, n in SSG_COLOURS for v in (({"Colour": c, "Size": "4kg"}, f"LUMSSG{n}-4", 28.50, 4, "parcel"),
                                                 ({"Colour": c, "Size": "10kg"}, f"LUMSSG{n}-10", 39.95 if c in SSG_CHEAP10 else 59.95, 10, "bulky"))],
    market="Adheseal 4kg $26.40 ex GST ($29.04 inc); 10kg $36.58 ex ($40.24 inc) for white, misty grey, magellan and slate, $55.73 ex ($61.30 inc) for the other colours (28 Oct 2026).",
    material="Cement based smooth coloured tile grout (CG2W class), water and mould resistant", range="Luminous SSG, 4kg or 10kg bag, 12 colours, joints 1.5 to 15mm", warranty="RLA product warranty when applied to the data sheet",
    images=[("luminous-ssg.png", "RLA Luminous SSG grout bag"), ("luminous-range.png", "RLA Luminous grout colour range")],
    desc=html(["RLA Luminous SSG is a high performance smooth ceramic tile grout for internal and external joints from 1.5 to 15mm. Enhanced workability and a smooth finish make it easy to work into narrow joints and wash off, and the built in water and mould resistance keeps the colour vibrant in showers and kitchens.",
               "Shrinkage compensated so it does not crack, abrasion resistant, with extended colour uniformity and an extended open time. Twelve colours in a 4kg bag for a bathroom or a 10kg bag for floors."],
              uses=["Wall and floor tile joints 1.5 to 15mm, internal and external", "Bathrooms, kitchens, laundries and balconies", "Porcelain, ceramic, stone and mosaic tiles"],
              colours=[c for c, _ in SSG_COLOURS],
              specs=["Type: cement based smooth coloured grout, CG2W", "Bag: 4kg or 10kg", "Joint width: 1.5 to 15mm", "Water resistant, low water absorption, mould resistant", "Shrinkage compensated, abrasion resistant, extended open time"],
              notes=["Colour chips are a guide; mix bags of the same batch for one area and keep the mixing water the same.", "Wash off within the clean-up time on the bag; a haze left overnight is hard to remove.", "Seal the perimeter with the matching RLA Luminous Silicone."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2026/07/LUMSSG_TDS.pdf", sds="https://cdn.bfldr.com/XSLKHZTO/at/hcxf95w3hcs4frk7k833jgj/LUMSSG_SDS.pdf"))

LSIL_COLOURS = [("White", "610702"), ("Alabaster", "610782"), ("Misty Grey", "610741"), ("Mudberry", "610785"), ("Light Beige", "610721"), ("Magellan", "610706"),
                ("Travertine", "610777"), ("Havana", "610780"), ("Macchiato", "610788"), ("Forest", "610719"), ("Slate Grey", "610711"), ("Charcoal", "610754"), ("Black", "610755")]
add(key="luminous-silicone", title="RLA Luminous Silicone Wet Area Sealant 300ml, Grout Matched", type="Silicone Sealants", cat="sealant",
    tags=["Hardware", "Silicone & Sealants", "Silicone Sealants", "Neutral Cure", "Wet Area", "Luminous"], options=["Colour"],
    variants=[({"Colour": c}, sku, 9.75, 0.4, "parcel") for c, sku in LSIL_COLOURS],
    market="Tilers Direct $9.95, Beaumont $12.25 (28 Oct 2026). Codes from the printed RLA Tiling Product Range (V2); the website lists different 13164xx codes.",
    material="100% neutral cure silicone sealant with mould inhibitor", range="Luminous Silicone, 300ml cartridge, 13 grout matched colours", warranty="RLA product warranty when applied to the data sheet",
    images=[("luminous-silicone.png", "RLA Luminous Silicone cartridge")],
    desc=html(["RLA Luminous Silicone is the perimeter sealant for RLA Luminous grouts: a premium neutral cure silicone with a built in mould inhibitor, colour matched to the grout so the shower corners, bath edge and floor/wall joint disappear into the tiling.",
               "Non corrosive, low slump, ±25% movement, UV stable and weatherproof, with a 5 to 12 minute skin time. Excellent adhesion to glass shower screens, aluminium, galvanised steel, cement sheet, concrete, brick, ceramic and wood."],
              uses=["Shower screens, bath and basin perimeters", "Floor/wall and internal corner joints in tiled wet areas", "Kitchens, laundries and toilets", "Glazing and general wet area sealing, inside and out"],
              colours=[c for c, _ in LSIL_COLOURS],
              specs=["Type: 100% silicone, neutral (oxime) cure, sanitary grade with mould inhibitor", "Cartridge: 300ml", "Movement capability: ±25% (total joint movement 50%)", "Skin time: 5 to 12 minutes", "Internal and external use, UV stable"],
              notes=SIL_NOTES,
              tds="https://cdn.bfldr.com/XSLKHZTO/at/xx5kkb2f4mbmsv934pmk3c/RLA_Luminous_Silicone_TDS.pdf", sds="https://cdn.bfldr.com/XSLKHZTO/at/r5h8qnrkr4b45sgf5swbsnn/RA5745_SDS.pdf"))

add(key="epoxy-grout", title="RLA Epoxy Grout Two Part Anti-Acid 5kg Kit", type="Grout", cat="grout",
    tags=GROUT_TAGS + ["Epoxy Grout", "Coloured Grout"], options=["Colour"],
    variants=[({"Colour": c}, sku, 149.95, 5.5, "bulky") for c, sku in [("Arctic", "620400"), ("Mid Grey", "620401"), ("Slate Grey", "620402"), ("Charcoal", "620403")]],
    market="Tilers Direct $154.20, Beaumont $197.95 (28 Oct 2026).",
    material="Two component epoxy mortar grout (Part A resin, aggregates and pigment; Part B catalyst), anti-acid", range="Epoxy Grout, 5kg kit, 4 colours, joints 1 to 15mm", warranty="RLA product warranty when applied to the data sheet",
    images=[("epoxy-grout.jpg", "RLA Epoxy Grout 5kg kit")],
    desc=html(["RLA Epoxy Grout is a two part, anti-acid epoxy mortar for joints that have to stay clean: commercial kitchens, benchtops, pools, shower floors and anywhere exposed to chemicals or heavy cleaning. Mixed, it is a creamy, smooth grout that also holds on vertical joints without slipping; hardened, it is stain proof, does not absorb water and never effloresces.",
               "Grouts joints from 1 to 15mm on walls and floors, internal and external. Four colours in a 5kg kit."],
              uses=["Commercial kitchens, food areas and laboratories", "Swimming pools, spas and shower floors", "Benchtops, splashbacks and high traffic floors", "Surfaces exposed to aggressive chemicals and cleaning", "Ceramic, porcelain, glass and mosaic tiles"],
              colours=["Arctic", "Mid Grey", "Slate Grey", "Charcoal"],
              specs=["Type: two component epoxy grout, anti-acid", "Kit: 5kg (Part A + Part B)", "Joint width: 1 to 15mm", "Walls and floors, internal and external", "Dry time: 24 hours", "No efflorescence, no staining, no water absorption, ultra low VOC", "Coverage: see the RLA grout calculator"],
              notes=["Mix the whole kit (or weigh both parts in ratio) and work in small areas: pot life is limited and clean-up is harder once it starts to set.", "Wash off with water and the grout float/sponge within the time on the data sheet; residue cannot be removed once cured.", "Wear gloves and eye protection; read both safety data sheets."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2021/05/Epoxy-Grout-Technical-Data-Sheet.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2020/07/RLA-Epoxy-Grout-Part-A.pdf"))

add(key="once-over", title="RLA The Once Over Rejuvenating Grout Cleaner 1L", type="Sealants, Sealers & Cleaners", cat="cleaner",
    tags=["Hardware", "Cleaners & Sealers", "Grout Cleaner", "price-check"], ship="parcel", weight=1.1, price=29.95, sku="506210",
    market="No listing found (28 Oct 2026); priced against 1 L tile and grout cleaners in the store.",
    material="Mild acidic grout cleaner, clear liquid", range="The Once Over, 1 L bottle", warranty="RLA product warranty when used to the label",
    images=[("crop-once-over.png", "RLA The Once Over grout cleaner bottle")],
    desc=html(["RLA The Once Over is a mild acidic cleaner that lifts grout haze and stains off a new tiling job and revives the colour of old grout, so the floor looks the way it did the day it was grouted. It works on all grout types, internally and externally, and is easy to use: dilute, apply, scrub, rinse.",
               "Keep a bottle for the end of every job and for maintenance cleans."],
              uses=["Removing grout haze and stains after grouting", "Reviving the colour of old, dull grout", "Maintenance cleaning of tiled floors and walls", "All cement based grouts, internal and external"],
              specs=["Type: mild acidic grout cleaner", "Colour: clear", "Size: 1 L", "Suitable for all grout types, internal and external"],
              notes=["Acidic: test on a small area first and do not leave it on natural stone, marble or polished metal. Rinse well with clean water.", "Wear gloves and eye protection and read the safety data sheet."]))

# ============================== PRIMERS & ADDITIVES (Tiling Catalogue p17) ==============================
PRIM_TAGS = ["Hardware", "Adhesives & Additives"]
add(key="porous-primer", title="RLA Porous Primer Acrylic Tiling Primer", type="Adhesives", cat="primer",
    tags=PRIM_TAGS + ["Primer", "New"], options=["Size"],
    variants=[({"Size": "5 L"}, "RL7175-5", 37.95, 5.3, "parcel20"), ({"Size": "20 L"}, "RL7175-20", 109.95, 21, "local")],
    market="5 L: Render Supply Co $39.00, Tilers Online $49.50, Beaumont $59.25 (28 Oct 2026). 20 L: no listing, priced pro rata (price-check).", price_check_variants=["20 L"],
    material="Water based acrylic primer for porous substrates (replaces RLA UniPrime)", range="Porous Primer, 5 L or 20 L, about 8 to 10m² per litre", warranty="RLA product warranty when applied to the data sheet",
    images=[("porous-primer.png", "RLA Porous Primer 5 L container")],
    desc=html(["RLA Porous Primer is the universal wall and floor primer for porous surfaces before RLA tile adhesives, membranes and repair mortars. It soaks into concrete, render, fibre cement and plasterboard, binds the dust and stops the substrate sucking the water out of the adhesive, so the bond is stronger. Water based, dries clear in about 30 minutes.",
               "It replaces RLA UniPrime."],
              uses=["Porous concrete, screed and render", "Fibre cement sheeting, plasterboard and aerated concrete", "Rendered brickwork and blockwork", "Before RLA tile adhesives, RLA WPU and WPM membranes and repair mortars, walls and floors, internal and external"],
              specs=["Type: water based acrylic primer, porous surfaces", "Colour: dries clear", "Sizes: 5 L or 20 L", "Coverage: about 8 to 10m² per litre", "Dry time: about 30 minutes", "Internal and external use"],
              notes=["Not for existing tiles, paint or sealed concrete: use RLA Non-Porous Primer.", "Apply by brush or roller to a clean, dust free surface and let it dry before tiling."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2025/11/rla-porous-primer_tds.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2024/07/RLA-Porous-Primer_SDS_30_7_24.pdf"))

add(key="non-porous-primer", title="RLA Non-Porous Primer Tile Over Tile Primer", type="Adhesives", cat="primer",
    tags=PRIM_TAGS + ["Primer", "Tile Over Tile", "New"], options=["Size"],
    variants=[({"Size": "5 L"}, "RL8502-5", 87.95, 5.3, "parcel20"), ({"Size": "20 L"}, "RL8502-20", 239.95, 21, "local")],
    market="5 L: Baytina Plus $91.00, Render Supply Co $98.27; B&B Hardware sells the old Universal Primer 5 L at $112.95 and 20 L at $326.50; SealMart Universal Primer 5 L $82.50, 20 L $247.50 (28 Oct 2026).",
    material="Water based acrylic primer for non porous and porous substrates (replaces RLA Universal Primer)", range="Non-Porous Primer, 5 L or 20 L, about 7 to 10m² per litre", warranty="RLA product warranty when applied to the data sheet",
    images=[("rla-non-porous-primer.png", "RLA Non-Porous Primer 5 L container")],
    desc=html(["RLA Non-Porous Primer makes tile over tile possible: a rapid drying, solvent free, low VOC water based acrylic primer that grips existing tiles, old paint, vinyl tiles, vinyl and carpet adhesive residue, metal and sealed or burnished concrete, and gives RLA adhesives something to bond to. Blue, so you can see where you have been, dry in 30 to 60 minutes.",
               "Works on porous substrates too, diluted as the data sheet says. It replaces RLA Universal Primer."],
              uses=["Tiling over existing tiles with RLA AddFlextra, UniGrip or Mastik", "Painted walls (not oil based paint), vinyl tiles and adhesive residue", "Sealed, burnished or smooth concrete and metal surfaces", "Concrete, grout, screed, render and fibre cement (diluted)"],
              specs=["Type: water based acrylic primer, non porous and porous surfaces", "Colour: blue", "Sizes: 5 L or 20 L", "Coverage: about 7 to 10m² per litre", "Dry time: 30 to 60 minutes", "Rapid drying, solvent free, low VOC, can be diluted for porous surfaces", "Internal and external use"],
              notes=["Clean existing tiles with a degreaser and rinse before priming; the primer cannot bond through soap and grease.", "Apply thinly by roller; tile once dry and within the time on the data sheet."],
              tds="https://www.tiledepot.co.nz/data/catalogue/pdf/RLA-Non-Porous-Primer_TDS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2024/07/RLA-Porous-Primer_SDS_30_7_24.pdf"))

add(key="plastinex", title="RLA Plastinex Flexible Acrylic Additive", type="Adhesives", cat="adhesive",
    tags=PRIM_TAGS + ["Additive", "Flexible Additive", "New"], options=["Size"],
    variants=[({"Size": "5 L"}, "RL7950-5", 52.95, 5.3, "parcel20"), ({"Size": "20 L"}, "RL7950-20", 179.95, 21, "local")],
    market="5 L: Tilers Online $54.00, Render Supply Co $54.59, Beaumont $63.75 (28 Oct 2026). 20 L: no listing, priced pro rata (price-check).", price_check_variants=["20 L"],
    material="White high solids flexible acrylic polymer additive (replaces RLA Uniflex)", range="Plastinex, 5 L or 20 L", warranty="RLA product warranty when applied to the data sheet",
    images=[("plastinex.png", "RLA Plastinex 5 L container")],
    desc=html(["RLA Plastinex is a white, high solids, flexible acrylic additive that upgrades RLA's cement based products: mixed into TileBond Extra, Mastik, MoreFlex or AddFlextra it adds flexibility, adhesion and water resistance for tiling over concrete, render, block, membranes and in pools; in grout it adds flex and stain resistance; in sand and cement screeds and render it improves workability, strength and durability.",
               "Internal, external, underground and immersed use. It replaces RLA Uniflex."],
              uses=["Adhesive booster for RLA cement based tile adhesives, including pool tiling", "Grout additive for the RLA grout range", "Additive for sand/cement screeds and render", "Bonding slurries and repair mortars"],
              specs=["Type: flexible acrylic polymer additive, high solids concentrate", "Colour: white", "Sizes: 5 L or 20 L", "Coverage: depends on the application, see the data sheet", "Internal and external use, suitable for underground and immersed environments"],
              notes=["Replace part or all of the mixing water with Plastinex as the data sheet directs for each product.", "Store between 5 °C and 30 °C; do not let it freeze."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/07/RLA-Plastinex_TDS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2024/07/RLA-Plastinex_SDS_31-7-24.pdf"))

# ============================== SILICONES & SEALANTS (Tiling p20; Sealants Catalogue p2-8) ==============================
SIL_TAGS = ["Hardware", "Silicone & Sealants", "Silicone Sealants"]
S700 = [("Almond Ivory", "610600"), ("Bluestone", "610602"), ("Charcoal", "610603"), ("Light Grey", "610605"), ("Mid Grey", "610606"), ("Off White", "610607"), ("Pewter", "610608"),
        ("Stone Beige", "610609"), ("Tile Grey", "610610"), ("Translucent", "610611"), ("Travertine", "610612"), ("Black", "610613"), ("White", "610614"), ("Taupe", "610615")]
add(key="silikon-700", title="RLA Silikon 700 Wet Area Antifungal Silicone 300g", type="Silicone Sealants", cat="sealant",
    tags=SIL_TAGS + ["Neutral Cure", "Wet Area", "Silikon"], options=["Colour"],
    variants=[({"Colour": c}, sku, 9.75, 0.4, "parcel") for c, sku in S700],
    market="Tilers Direct $9.95, Beaumont $12.95, Online Tilers Store $7.60 (28 Oct 2026). 600ml sausages are available to order.",
    material="100% neutral oxime cure silicone sealant with antifungicide", range="Silikon 700 Professional, 300g cartridge, 14 colours", warranty="RLA product warranty when applied to the data sheet",
    images=[("silikon-700.png", "RLA Silikon 700 wet area silicone cartridge"), ("silikon-700-b.png", "RLA Silikon 700 silicone features")],
    desc=html(["RLA Silikon 700 is the tiler's wet area silicone: a premium 100% neutral oxime curing silicone with an antifungicide that stops mould in hot, humid bathrooms, shower screens, kitchens and wash basins. Non corrosive on metal and mirrors, low slump, ±25% movement and UV stable.",
               "Excellent adhesion to glass, aluminium, galvanised steel, concrete, wood, ceramic tiles, baths, vanities and cement sheet. Fourteen colours to match common tile and grout shades."],
              uses=["Shower screens, baths, basins and vanities", "Floor/wall and internal corner joints in tiled wet areas", "Kitchens, laundries and high traffic wash areas", "Glazing and general sealing, inside and out"],
              colours=[c for c, _ in S700],
              specs=["Type: 100% silicone, neutral (oxime) cure, mould inhibited", "Cartridge: 300g (600ml sausage available to order)", "Movement capability: ±25%", "Skin time: 5 to 12 minutes", "UV stable, non corrosive, internal and external use"],
              notes=SIL_NOTES,
              tds="https://cdn.bfldr.com/XSLKHZTO/as/4xp32tkx3mxk9h5j37449v4p/610600_TDSpdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2023/12/Silikon-700.pdf"))

S100 = [("Almond Ivory", "610500"), ("Aluminium", "610501"), ("Black", "610502"), ("Brown", "610504"), ("Classic Cream", "610505"), ("Grey", "610508"), ("Off White", "610510"),
        ("Stone Beige", "610511"), ("Translucent", "610512"), ("White", "610514"), ("Woodland Grey", "610515"), ("Caulfield Green", "610516"), ("Monument", "610517")]
add(key="silikon-100", title="RLA Silikon 100 General Purpose Neutral Cure Silicone 310g", type="Silicone Sealants", cat="sealant",
    tags=SIL_TAGS + ["Neutral Cure", "Roof & Gutter", "Silikon", "price-check"], options=["Colour"],
    variants=[({"Colour": c}, sku, 9.75, 0.4, "parcel") for c, sku in S100],
    market="No online listing found (28 Oct 2026); priced with Silikon 700.",
    material="100% neutral oxime cure silicone sealant, AS 4020 approved for drinking water", range="Silikon 100 Professional, 310g cartridge, 13 colours", warranty="RLA product warranty when applied to the data sheet",
    images=[("silikon-100.png", "RLA Silikon 100 neutral cure silicone cartridge")],
    desc=html(["RLA Silikon 100 is the mechanic in a can: a premium 100% neutral cure silicone for general purpose sealing in plumbing, building, roofing and industrial and automotive work. Glazing, roof and gutter joints, weather sealing, HVAC, caravans and trucks, portable buildings and water tanks (AS 4020 approved for drinking water).",
               "Bonds to glass, wood, timber, concrete, galvanised steel, ceramics, aluminium, some plastics and most painted or powder coated surfaces. UV stable, non corrosive, ±25% movement, in thirteen roofing and trim colours."],
              uses=["Glazing and window frames", "Roofing, guttering, flashings and downpipes", "Weather sealing, HVAC and plumbing", "Caravans, trucks, portable buildings and water tanks"],
              colours=[c for c, _ in S100],
              specs=["Type: 100% silicone, neutral (oxime) cure", "Cartridge: 310g", "Movement capability: ±25%", "UV stable, non corrosive, AS 4020 approved, BS 5889 building approval", "VOC compliant (under 5%), internal and external use"],
              notes=SIL_NOTES,
              tds="https://cdn.bfldr.com/XSLKHZTO/as/cwpthsjwrw3fhjbvjq7nm9tv/610500_TDSpdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2023/12/Silikon-100.pdf"))

add(key="silikon-200", title="RLA Silikon 200 Acetic Cure RTV Silicone 310g Translucent", type="Silicone Sealants", cat="sealant",
    tags=SIL_TAGS + ["Acetic Cure", "Silikon", "price-check"], ship="parcel", weight=0.4, price=9.75, sku="610521",
    market="No online listing found (28 Oct 2026); priced with Silikon 700.",
    material="100% acetic cure RTV silicone sealant", range="Silikon 200 Professional, 310g cartridge, translucent", warranty="RLA product warranty when applied to the data sheet",
    images=[("silikon-200.png", "RLA Silikon 200 acetic cure silicone cartridge")],
    desc=html(["RLA Silikon 200 is a high strength 100% acetic cure RTV silicone for glazing and sealing jobs where long term reliability counts: automotive gaskets, sealing environmental and refrigerated rooms, industrial assembly, waterproofing and aquariums. Superior chemical and temperature performance, UV stable, ±25% movement.",
               "Bonds to glass, wood, timber, ceramics, aluminium, some plastics and most painted or powder coated surfaces."],
              uses=["Glazing and aquariums", "Automotive and appliance gaskets", "Cool rooms, refrigerated and environmental rooms", "Industrial assembly and waterproofing"],
              specs=["Type: 100% silicone, acetic (acetoxy) cure", "Cartridge: 310g", "Colour: translucent", "Movement capability: ±25%", "UV stable, high strength, internal and external use"],
              notes=["Acetic cure releases a vinegar smell while curing and can corrode some metals and mirror backing: use a neutral cure Silikon on those.", "Surfaces must be clean, dry and free of grease; tool within the skin time.", "Standard 310 g cartridge, fits any 300 ml caulking gun."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2023/12/RLA-Silikon-600_TDS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2023/12/Silikon-600.pdf"))

add(key="silikon-300", title="RLA Silikon 300 Low Gloss Matte Neutral Cure Silicone 310g", type="Silicone Sealants", cat="sealant",
    tags=SIL_TAGS + ["Neutral Cure", "Matte", "Glazing", "Silikon", "price-check"], options=["Colour"],
    variants=[({"Colour": c}, sku, 10.95, 0.4, "parcel") for c, sku in [("Matte Black", "610540"), ("Translucent", "610544"), ("Matte Grey", "610545"), ("Matte White", "610546")]],
    market="No online listing found (28 Oct 2026); priced a little above Silikon 700. The catalogue also lists a 420g cartridge; the four codes are listed here as 310g until RLA confirms sizes.",
    material="100% neutral oxime cure silicone sealant, calcium carbonate filled, medium modulus, matte finish", range="Silikon 300 Professional, 310g cartridge, matte black, grey, white and translucent", warranty="RLA product warranty when applied to the data sheet",
    images=[("silikon-300.png", "RLA Silikon 300 matte silicone cartridge"), ("silikon-300-colours.png", "RLA Silikon 300 colours")],
    desc=html(["RLA Silikon 300 is a premium, extra high strength, medium modulus neutral cure silicone formulated for professional glazing, with a low gloss matte finish that sits quietly next to powder coated frames and matte tiles. Superior adhesion and durability for glazing, roofing and guttering, weather sealing, HVAC, caravans, trucks and portable buildings.",
               "Forms a strong weatherproof seal on glass, ceramic, steel, aluminium, brick, concrete and most plastics. Outstanding elongation, UV stable."],
              uses=["Professional glazing and window installation", "Roofing, guttering and weather sealing", "HVAC, caravans, trucks and portable buildings", "Matte finish joints next to powder coated aluminium and matte tiles"],
              colours=["Matte Black", "Translucent", "Matte Grey", "Matte White"],
              specs=["Type: 100% silicone, neutral (oxime) cure, medium modulus", "Cartridge: 310g", "Finish: low gloss matte", "Higher strength, outstanding elongation, UV stable", "Internal and external use"],
              notes=SIL_NOTES,
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2023/12/RLA-Silikon-400LM_TDS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2023/12/Silikon-400.pdf"))

add(key="silikon-400", title="RLA Silikon 400LM Low Modulus Matte Silicone", type="Silicone Sealants", cat="sealant",
    tags=SIL_TAGS + ["Neutral Cure", "Low Modulus", "Matte", "Cladding", "Silikon", "price-check"], options=["Size", "Colour"],
    variants=[({"Size": "400g cartridge", "Colour": "Matte Black"}, "610567", 12.95, 0.5, "parcel"), ({"Size": "400g cartridge", "Colour": "Matte Light Grey"}, "610568", 12.95, 0.5, "parcel"),
              ({"Size": "400g cartridge", "Colour": "Matte White"}, "610570", 12.95, 0.5, "parcel"), ({"Size": "600ml sausage", "Colour": "Matte Black"}, "610566", 14.95, 0.7, "parcel"),
              ({"Size": "600ml sausage", "Colour": "Matte Light Grey"}, "610569", 14.95, 0.7, "parcel"), ({"Size": "600ml sausage", "Colour": "Matte White"}, "610565", 14.95, 0.7, "parcel")],
    market="No online listing found (28 Oct 2026); priced above Silikon 700 for the larger pack.",
    material="100% neutral oxime cure silicone sealant, low modulus, matte finish", range="Silikon 400LM Professional, 400g cartridge or 600ml sausage, matte black, light grey or white", warranty="RLA product warranty when applied to the data sheet",
    images=[("silikon-400.png", "RLA Silikon 400LM low modulus matte silicone cartridge"), ("silikon-400-colours.png", "RLA Silikon 400LM colours")],
    desc=html(["RLA Silikon 400LM is a premium low modulus 100% neutral cure silicone with a matte finish, made for cladding, glazing and facade work where the joint has to move a lot: ±50% movement capability. The soft, discreet matte finish blends with the surrounding panels.",
               "Bonds to glass, cement, concrete, ceramic, steel, aluminium, brick and most plastics for weather sealing, solar panel installation, structural butt joints and colonial bars."],
              uses=["Cladding, facades and curtain walls", "Glazing and structural butt joints", "Solar panel installation", "Weather sealing of high movement joints"],
              colours=["Matte Black", "Matte Light Grey", "Matte White"],
              specs=["Type: 100% silicone, neutral (oxime) cure, low modulus", "Sizes: 400g cartridge or 600ml foil sausage", "Finish: matte", "Movement capability: ±50%", "Skin time: 5 to 10 minutes", "UV stable, internal and external use"],
              notes=["The 600ml sausage needs a barrel (sausage) gun; the 400g cartridge fits a standard gun."] + SIL_NOTES[:2],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2023/12/RLA-Silikon-400LM_TDS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2023/12/Silikon-400.pdf"))

add(key="silikon-600", title="RLA Silikon 600 Fast Cure Neutral Silicone Adhesive Sealant 310g", type="Silicone Sealants", cat="sealant",
    tags=SIL_TAGS + ["Neutral Cure", "Fast Cure", "Silikon", "price-check"], options=["Colour"],
    variants=[({"Colour": c}, sku, 11.95, 0.4, "parcel") for c, sku in [("Black", "610581"), ("Grey", "610583"), ("Translucent", "610584"), ("White", "610586")]],
    market="No online listing found (28 Oct 2026); priced a little above Silikon 700.",
    material="100% neutral oxime cure silicone adhesive sealant, fast curing, high strength", range="Silikon 600 Professional, 310g cartridge, black, grey, translucent or white", warranty="RLA product warranty when applied to the data sheet",
    images=[("silikon-600.png", "RLA Silikon 600 fast cure silicone cartridge"), ("silikon-600-colours.png", "RLA Silikon 600 colours")],
    desc=html(["RLA Silikon 600 is a premium fast curing, high strength neutral silicone adhesive sealant for glazing, industrial and automotive work where the part needs to be moved quickly: extra high body, no slump, excellent adhesion and a 2 to 5 minute skin time, with the long term reliability of a 100% silicone.",
               "Bonds to glass, metals, galvanised steel, aluminium, concrete, plastics and most painted or powder coated surfaces. UV stable, ±25% movement."],
              uses=["Glazing of colonial bars and structural butt joints", "Industrial and automotive sealing and bonding", "Jobs where the item has to be handled soon after sealing"],
              colours=["Black", "Grey", "Translucent", "White"],
              specs=["Type: 100% silicone, neutral (oxime) cure, fast cure", "Cartridge: 310g", "Skin time: 2 to 5 minutes", "Movement capability: ±25%", "No slump, UV stable, internal and external use"],
              notes=["Fast skin: cut the nozzle, gun and tool one joint at a time."] + SIL_NOTES[:2],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2023/12/RLA-Silikon-600_TDS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2023/12/Silikon-600.pdf"))

add(key="roof-gutter", title="RLA Roof & Gutter Silicone Sealant 300ml", type="Silicone Sealants", cat="sealant",
    tags=SIL_TAGS + ["Neutral Cure", "Roof & Gutter"], options=["Colour"],
    variants=[({"Colour": c}, sku, 8.95, 0.4, "parcel") for c, sku in [("Translucent", "610324"), ("White", "610326"), ("Grey", "610319"), ("Black", "610327")]],
    market="Direct Wholesale $6.30 to $6.59 (bulk seller), Valve Warehouse $13.07, Burdens $14.58 (28 Oct 2026).",
    material="100% non diluted neutral cure silicone sealant, mould and fungal resistant, AS/NZS 4020 approved", range="Roof & Gutter Silicone, 300ml cartridge, translucent, white, grey or black", warranty="RLA 10 year manufacturer's warranty when applied to the data sheet",
    images=[("roof-gutter.png", "RLA Roof and Gutter silicone cartridge")],
    desc=html(["RLA Roof & Gutter Silicone is a non diluted, UV resistant, neutral cure silicone made for roofing and plumbing joints: metal and Colorbond roofing, lap joints and flashings, gutters and downpipes, pipe and sprinkler penetrations, air conditioning and window frames. 100% silicone, so it does not shrink as it cures, and it stays flexible through heat, cold and vibration.",
               "Non corrosive neutral cure, AS/NZS 4020 approved for contact with drinking water, mould and fungal resistant, ±25% movement, 10 year manufacturer's warranty."],
              uses=["Metal and Colorbond roof sheeting, lap joints and flashings", "Gutters, downpipes and rainwater tanks", "Pipe, sprinkler and air conditioning penetrations", "Window frames, steel, aluminium, timber, concrete and masonry"],
              colours=["Translucent", "White", "Grey", "Black"],
              specs=["Type: 100% silicone, neutral cure", "Cartridge: 300ml", "Movement capability: ±25%", "AS/NZS 4020 drinking water approved, UV stable, mould and fungal resistant, low VOC", "Internal and external use, 10 year warranty"],
              notes=["Pre-test on plastics and rubbers.", "Not paintable; choose the colour to suit the roof."] + SIL_NOTES[:1],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/01/RLA-ROOF-AND-GUTTER-SILICONE-TDS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2023/05/RLA-Roof-Gutter-Silicone-Translucent-Issue-Date-18.05.2023-Code-610324.pdf"))

add(key="wet-area", title="RLA Wet Area Silicone Sealant 300ml", type="Silicone Sealants", cat="sealant",
    tags=SIL_TAGS + ["Neutral Cure", "Wet Area"], options=["Colour"],
    variants=[({"Colour": c}, sku, 8.75, 0.4, "parcel") for c, sku in [("Translucent", "610316"), ("White", "610318"), ("GP Off White", "610370")]],
    market="Tilers Online $9.00 (white 330g), Burdens $16.82 (28 Oct 2026).",
    material="100% non diluted neutral cure silicone sealant with antifungicide, AS/NZS 4020 approved", range="Wet Area Silicone, 300ml cartridge, translucent, white or GP off white", warranty="RLA 10 year manufacturer's warranty when applied to the data sheet",
    images=[("wet-area.png", "RLA Wet Area silicone cartridge")],
    desc=html(["RLA Wet Area Silicone is the everyday bathroom and kitchen sealant: an antifungal, non diluted, UV resistant neutral cure silicone for the perimeter of baths, basins, shower bases, spas and sinks, around tiles, window frames, exhaust fans and shower frames, anywhere mould would otherwise grow.",
               "100% silicone with no shrinkage, non corrosive, permanently flexible, AS/NZS 4020 approved for drinking water, 10 year manufacturer's warranty. Three colours for white and off white fittings."],
              uses=["Bath, basin, shower base, spa and sink perimeters", "Tile joints, splashbacks and shower frames", "Window frames and exhaust fans in wet rooms", "Kitchens, bathrooms, laundries and toilets"],
              colours=["Translucent", "White", "GP Off White"],
              specs=["Type: 100% silicone, neutral cure, antifungal", "Cartridge: 300ml", "Movement capability: ±25%", "AS/NZS 4020 approved, UV resistant, mould and fungal resistant, low VOC", "Internal and external use, 10 year warranty"],
              notes=SIL_NOTES,
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/01/RLA-WET-AREA-SILICONE-TDS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2023/06/RLA-Wet-Area-Trans-Issue-Date-31.05.2023.pdf"))

HYB_TAGS = ["Hardware", "Silicone & Sealants", "Hybrid Sealants"]
add(key="gap-filler", title="RLA Gap Filler Paintable Acrylic Sealant 300ml White", type="Hybrid Sealants", cat="sealant",
    tags=HYB_TAGS + ["Acrylic", "Gap Filler", "Paintable", "price-check"], ship="parcel", weight=0.4, price=5.95, sku="600395",
    market="No RLA listing found (28 Oct 2026); Soudal gap filler 300ml sells for $4.74 to $5.00, so priced just above.",
    material="Acrylic mastic sealant, paintable", range="Gap Filler, 300ml cartridge, white", warranty="RLA product warranty when applied to the data sheet",
    images=[("gap-filler.jpg", "RLA Gap Filler acrylic sealant cartridge")],
    desc=html(["RLA Gap Filler is a painter's acrylic caulk for sealing cracks and joints in timber and plaster: around door and window frames, wall and ceiling joints, cornices, skirting, masonry, and around baths, sinks and sanitary fittings before painting. Fast drying, sandable, and it can be painted or papered over.",
               "Water wash up, internal and external."],
              uses=["Door and window frames, architraves and skirting", "Wall, ceiling and cornice joints", "Cracks in plaster and render", "Around baths, sinks and sanitary fittings (low movement joints)"],
              specs=["Type: acrylic mastic sealant", "Cartridge: 300ml", "Colour: white", "Paintable and sandable, fast drying, water wash up", "Low movement joints, internal and external"],
              notes=["Not a silicone: for shower screens and wet area joints that flex use RLA Wet Area or Silikon 700.", "Let it dry before painting; deep gaps need two applications."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2022/09/Gap-Filler-TDS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2022/09/RLA-Gap-Filler-Issue-Date-01.08.2022-Code-600395-1.pdf"))

add(key="ultragrip", title="RLA UltraGrip Ultra High Strength Construction Adhesive", type="Hybrid Sealants", cat="sealant",
    tags=HYB_TAGS + ["Construction Adhesive", "Adhesive"], options=["Size"],
    variants=[({"Size": "300ml cartridge"}, "900083", 6.45, 0.45, "parcel"), ({"Size": "850ml cartridge"}, "900033", 14.95, 1.1, "parcel")],
    market="TradieCart 320ml $6.77 inc GST (28 Oct 2026). 850ml: no listing, priced pro rata (price-check).", price_check_variants=["850ml cartridge"],
    material="Synthetic rubber based mastic construction adhesive, conforms to AS 2329", range="UltraGrip, 300ml or 850ml cartridge, light brown", warranty="RLA product warranty when applied to the data sheet",
    images=[("ultragrip.png", "RLA UltraGrip construction adhesive cartridge")],
    desc=html(["RLA UltraGrip is a quality synthetic rubber construction adhesive for fixing flooring sheets and wall panelling: it bonds brick, stone, masonry, cement, polystyrene, wood, timber, ceramic tiles, steel, aluminium, tin and plaster, tolerates moisture in green or damp timber, stays slightly flexible and can be painted.",
               "Polystyrene safe, so it suits foam board and insulation panels. The 850ml cartridge needs a large barrel gun (RLA 850ml caulking gun)."],
              uses=["Wall panels and plasterboard to timber or metal studs", "Flooring sheets, cement sheet and plaster sheet to joists", "Timber trims, skirting and architraves", "Polystyrene and insulation panels", "Metal studs to concrete"],
              specs=["Type: synthetic rubber mastic adhesive, conforms to AS 2329", "Sizes: 300ml (standard gun) or 850ml cartridge (large barrel gun)", "Colour: light brown", "Coverage: about 15 lineal metres per 300ml at a 5mm bead", "Moisture tolerant, polystyrene safe, paintable, internal and external"],
              notes=["Apply in beads, press the panel on, pull it away for a minute and press back for instant grab.", "Solvent based: ventilate and read the safety data sheet."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2023/11/RLA-ULTRAGRIP-ADHESIVE.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2023/03/Ultragrip-Construction-Adhesive-10-3-23.pdf"))

add(key="flex-pro-pu", title="RLA Flex-Pro PU Polyurethane Sealant & Adhesive 600ml Grey", type="Hybrid Sealants", cat="sealant",
    tags=HYB_TAGS + ["Polyurethane", "Construction Joint", "price-check"], ship="parcel", weight=0.75, price=14.95, sku="620542",
    market="No RLA listing found (28 Oct 2026); Tilers Direct sells the fast cure Flex-Pro 50FC at $16.95 and Sikaflex Pro 600ml is $18.13 inc.",
    material="One component moisture curing thixotropic polyurethane sealant and adhesive, Class A (50% total joint movement)", range="Flex-Pro PU, 600ml foil sausage, grey", warranty="RLA product warranty when applied to the data sheet",
    images=[("flex-pro-pu.png", "RLA Flex-Pro PU polyurethane sealant sausage")],
    desc=html(["RLA Flex-Pro PU is a one component, low modulus polyurethane construction joint sealant with high mechanical strength and excellent weathering: expansion and construction joints in precast and tilt-up concrete, perimeter and penetration sealing, bond breakers, fillet joints and marine work.",
               "Non sag in vertical and expansion joints up to 30mm wide, short skinning time, paintable, resists fungal growth, and it bonds to concrete, brick, ceramics, stone, granite, marble, anodised aluminium, steel, glass, dry timber and tiles."],
              uses=["Expansion and construction joints in concrete and tilt panels", "Perimeter sealing around windows and doors; wall and floor penetrations", "Bond breaker under membranes and fillet joints", "Retaining walls, brickwork, stone and tiles", "Marine applications"],
              specs=["Type: one part moisture curing polyurethane, low modulus", "Size: 600ml foil sausage (needs a sausage gun)", "Colour: grey", "Movement capability: ±25% (total joint movement 50%), Class A", "Joints up to 30mm wide, non sag, paintable, low VOC", "Internal and external use"],
              notes=["Prime porous substrates with RLA Primer PU for best adhesion.", "Tool the joint within the skin time; paint once skinned.", "Moisture cured: keep the opened sausage sealed between jobs."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2025/09/rla-flex-pro-pu_tds.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/Flex_Pro_PU-Aust_-_SDS-5.pdf"))

add(key="flex-pro-50fc", title="RLA Flex-Pro 50FC Fast Cure Polyurethane Sealant & Adhesive 600ml", type="Hybrid Sealants", cat="sealant",
    tags=HYB_TAGS + ["Polyurethane", "Fast Cure", "Construction Joint"], options=["Colour"],
    variants=[({"Colour": c}, sku, 15.95, 0.75, "parcel") for c, sku in [("Grey", "A1255"), ("White", "A1256"), ("Black", "A1257")]],
    market="Tilers Direct $16.95 (white) (28 Oct 2026).",
    material="One component fast curing moisture curing polyurethane sealant and adhesive, Class A (50% total joint movement)", range="Flex-Pro 50FC, 600ml foil sausage, grey, white or black", warranty="RLA product warranty when applied to the data sheet",
    images=[("flex-pro-50fc.png", "RLA Flex-Pro 50FC fast cure polyurethane sealant sausage")],
    desc=html(["RLA Flex-Pro 50FC is the fast curing version of Flex-Pro: a one component polyurethane sealant and adhesive for porous and non porous surfaces that reaches strength quickly, with high mechanical strength and resistance to weather, hydrocarbons and jet fuels. It is rated Class A with 50% total joint movement.",
               "Use it for construction and expansion joints in concrete and tilt-up panels, perimeter and penetration sealing, bonding aluminium composite panel to cement sheet and masonry, and trafficable joints in stairs, roads and pavements."],
              uses=["Construction and expansion joints in precast, tilt-up and in situ concrete", "Perimeter sealing around windows, doors and curtain walls; penetrations", "Trafficable joints: stairs, roads, runways and pavements", "Bonding aluminium composite panel to cement sheet, concrete or masonry", "Brickwork, ceramics, stone, granite, marble, steel, glass and dry timber"],
              colours=["Grey", "White", "Black"],
              specs=["Type: one part fast curing polyurethane", "Size: 600ml foil sausage (needs a sausage gun)", "Movement capability: ±25% (total joint movement 50%), Class A", "Resists hydrocarbons, Skydrol and aviation fuels", "Paintable, low VOC, non hazardous classification", "Internal and external use"],
              notes=["Prime porous substrates with RLA Primer PU for best adhesion.", "Tool the joint within the skin time; it skins faster than standard Flex-Pro PU.", "Moisture cured: keep the opened sausage sealed between jobs."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/08/FLEX-PRO-50FC.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/Flex_Pro_50FC_-Aust_-_SDS-3.pdf"))

add(key="flex-pro-ms", title="RLA Flex-Pro MS Hybrid Polymer Sealant & Adhesive 600ml Grey", type="Hybrid Sealants", cat="sealant",
    tags=HYB_TAGS + ["MS Polymer", "SMP", "Bond Breaker"], ship="parcel", weight=0.75, price=14.95, sku="620620",
    market="Tilers Direct $15.95 (28 Oct 2026).",
    material="One component moisture curing silane modified polymer (MS) sealant and adhesive, solvent, isocyanate, silicone and PVC free", range="Flex-Pro MS, 600ml foil sausage, grey", warranty="RLA product warranty when applied to the data sheet",
    images=[("flex-pro-ms.png", "RLA Flex-Pro MS hybrid sealant sausage")],
    desc=html(["RLA Flex-Pro MS is a one component sealant and adhesive based on silane modified polymer: no solvents, isocyanates, silicones or PVC, very low VOC, and it stays elastic after curing. It adheres to most substrates, especially concrete, aluminium, masonry and glass, is compatible with most paint systems and is non staining on stone.",
               "The waterproofer's bond breaker for RLA acrylic membranes, and a sealant for elastic bonding in vibrating constructions, concrete expansion joints, acoustic sealing, window and door perimeters and penetrations."],
              uses=["Bond breaker at wall/floor junctions under RLA WPU and WPM membranes", "Concrete expansion joints and perimeter sealing", "Elastic bonding in vibrating constructions", "Sealing where acoustic properties are required", "Brickwork, ceramics, stone, granite, marble, sanitary ware, anodised aluminium, steel, glass, timber, PVC and plastics"],
              specs=["Type: one part moisture curing MS polymer hybrid", "Size: 600ml foil sausage (needs a sausage gun)", "Colour: grey", "Remains elastic after curing, non staining, paintable", "High weather, temperature and UV resistance, very low VOC", "Internal and external use"],
              notes=["Skin and cure time depend on humidity, temperature and joint depth; see the data sheet.", "Tool the joint within the skin time; paint once skinned."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/08/FLEX-PRO-MS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2024/05/Flex-Pro-MS-sealant.pdf"))

add(key="flex-pro-ms-hd", title="RLA Flex-Pro MS-HD High Modulus Hybrid Sealant & Adhesive 600ml", type="Hybrid Sealants", cat="sealant",
    tags=HYB_TAGS + ["MS Polymer", "SMP", "High Strength", "price-check"], options=["Colour"],
    variants=[({"Colour": c}, sku, 17.95, 0.75, "parcel") for c, sku in [("Grey", "620626"), ("White", "620625"), ("Black", "620627")]],
    market="No online listing found (28 Oct 2026); priced a step above Flex-Pro MS.",
    material="One component moisture curing industrial grade MS polymer sealant and adhesive, high strength, high modulus", range="Flex-Pro MS-HD, 600ml foil sausage, grey, white or black", warranty="RLA product warranty when applied to the data sheet",
    images=[("flex-pro-ms-hd.png", "RLA Flex-Pro MS-HD hybrid sealant sausage")],
    desc=html(["RLA Flex-Pro MS-HD is the industrial grade of the Flex-Pro MS family: a one part, moisture curing MS polymer sealant and adhesive with high strength, high modulus and high green strength, so it holds parts straight away where the bond needs to be fast, carry higher movement or absorb vibration.",
               "Paintable, highly flexible, low VOC and UV stable. Elastic bonding in vibrating constructions, concrete expansion joints, sealing and bonding across building and construction, and body panels on caravans, trucks and trailers."],
              uses=["Elastic bonding in vibrating constructions", "Concrete expansion joints", "Sealing and bonding in the building and construction industry", "Body panel adhesive for caravans, trucks and trailers"],
              colours=["Grey", "White", "Black"],
              specs=["Type: one part moisture curing MS polymer, high modulus", "Size: 600ml foil sausage (needs a sausage gun)", "High strength, high green strength, highly flexible, paintable", "Low VOC, UV stable, internal and external use"],
              notes=["Skin and cure time depend on humidity, temperature and joint depth; see the data sheet.", "Clamp or support heavy parts until green strength develops."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/08/FLEX-PRO-MS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2024/05/Flex-Pro-MS-sealant.pdf"))

add(key="firepro-fr", title="RLA FirePro FR Fire Rated Acrylic Sealant 600ml Grey", type="Hybrid Sealants", cat="sealant",
    tags=HYB_TAGS + ["Fire Rated", "Acrylic", "Intumescent", "price-check"], ship="parcel", weight=0.8, price=24.95, sku="R6841",
    market="No online listing found (28 Oct 2026); priced against other fire rated acrylic sausages.",
    material="Water based intumescent acrylic fire rated sealant, tested to AS 1530.4 and AS 4072.1 (FRL -/240/210)", range="FirePro FR, 600ml foil sausage, grey", warranty="RLA product warranty when applied to the data sheet and the tested system",
    images=[("firepro-fr.png", "RLA FirePro FR fire rated sealant sausage")],
    desc=html(["RLA FirePro FR is a water based intumescent acrylic sealant for internal and external expansion joints and for penetrations that need a fire resistant seal. When exposed to fire it expands to form an inorganic plug in the joint or void, which stops fire passing between the partitions of a building. Tested to AS 1530.4 and AS 4072.1 with a 4 hour fire rating (FRL -/240/210 on 10 to 50mm butt joints).",
               "No priming, flexible, low movement, non hazardous, and it is also an acoustic sealant."],
              uses=["Expansion and control joints in concrete, plasterboard, blockwork and brick walls", "Building services penetrations: pipes, cable trays, conduit and ducts", "Fire and acoustic sealing between partitions"],
              specs=["Type: intumescent acrylic sealant, water based", "Size: 600ml foil sausage (needs a sausage gun)", "Colour: grey", "Fire rating: 4 hours, tested to AS 1530.4 and AS 4072.1 (FRL -/240/210, 10 to 50mm butt joints, 20mm head joint)", "No priming, flexible, low movement, internal and external", "Non hazardous"],
              notes=["Install to the tested system (joint width, depth and backing rod) in the RLA test report; the fire rating only applies to that system.", "Paintable once cured; keep dry until cured."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/08/FLEX-PRO-MS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2024/05/Flex-Pro-MS-sealant.pdf"))

add(key="max-smp-crystal", title="RLA Max SMP Crystal Clear Adhesive Sealant 310g", type="Hybrid Sealants", cat="sealant",
    tags=HYB_TAGS + ["SMP", "Clear", "Adhesive Sealant", "price-check"], ship="parcel", weight=0.4, price=13.95, sku="620510",
    market="No single-unit listing found (28 Oct 2026, only a box of 25 at auction); priced a little above Max SMP 25.",
    material="Crystal clear silyl modified polymer (SMP) hybrid adhesive sealant, solvent and isocyanate free", range="Max SMP Crystal Clear, 310g cartridge, clear", warranty="RLA product warranty when applied to the data sheet",
    images=[("max-smp-crystal-clear.png", "RLA Max SMP Crystal Clear adhesive sealant cartridge")],
    desc=html(["RLA Max SMP Crystal Clear cures to a flexible, crystal clear seal, so the joint disappears: glass shower screens, interior glass, frames to concrete and any interior job where a coloured sealant would show. High bond strength, fast cure, permanently elastic, odourless, paintable, and it can be applied to damp surfaces.",
               "Solvent and isocyanate free, compatible with brick, stone, concrete, timber, ceramic tiles, PVC pipe, aluminium, tin and plaster."],
              uses=["Glass shower screens and interior glass", "Frames to concrete and interior applications", "High movement joints where the sealant must not be seen", "Bonding trims and fixtures to tiles, stone and timber"],
              specs=["Type: SMP hybrid adhesive sealant, crystal clear", "Cartridge: 310g", "Permanently elastic, high bond strength, fast cure", "Odourless, paintable, no isocyanates, no solvents", "Can be applied to damp surfaces; mainly interior use"],
              notes=["Tool within the skin time; the clear finish shows every smear, so mask the joint.", "Fits any 300ml caulking gun."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/05/MAX-SMP-25_TDS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/max_smp_25-aust_-_sds-4.pdf"))

add(key="max-grab", title="RLA Max Grab SMP Instant Grab Adhesive Sealant 440g Grey", type="Hybrid Sealants", cat="sealant",
    tags=HYB_TAGS + ["SMP", "Instant Grab", "Construction Adhesive"], ship="parcel", weight=0.5, price=14.95, sku="620511",
    market="Beaumont Tiles $21.75 (28 Oct 2026).",
    material="High green strength silyl modified polymer (SMP) adhesive sealant, solvent and isocyanate free", range="Max Grab SMP, 440g cartridge, grey", warranty="RLA product warranty when applied to the data sheet",
    images=[("max-grab-smp.png", "RLA Max Grab SMP adhesive cartridge")],
    desc=html(["RLA Max Grab SMP is made for instant grab: its high initial green strength holds materials in place horizontally and vertically without clamping or mechanical fixings, which makes it the adhesive for trims, panels, skirting, mirrors and niche shelves on tiles and masonry. Excellent adhesion to brick, stone, concrete, timber, ceramic tiles, steel, aluminium, tin and plaster with no priming and minimal surface preparation.",
               "No shrinkage, solvent and isocyanate free, odourless, impact resistant, can be applied to damp surfaces, and it repels lime and mould."],
              uses=["Heavy substrate bonding where fixings are not wanted", "An alternative to clamping", "Damp substrates and floor covering adhesion", "Trims, skirting, panels, mirrors and shelves to tiles, stone and masonry"],
              specs=["Type: SMP hybrid adhesive sealant, instant grab", "Cartridge: 440g", "Colour: grey", "No shrinkage, impact resistant, odourless, no isocyanates, no solvents", "Can be applied to damp surfaces, repels lime and mould", "Internal and external use"],
              notes=["Apply in vertical beads and press firmly; heavy items get full strength after cure, see the data sheet.", "Fits any 300ml caulking gun."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/05/MAX-SMP-25_TDS.pdf", sds="https://www.rlapolymers.com.au/wp-content/uploads/2025/03/max_smp_25-aust_-_sds-4.pdf"))

add(key="caulking-gun", title="RLA Heavy Duty Skeleton Caulking Gun", type="Silicone Accessories", cat="gun",
    tags=["Hardware", "Silicone & Sealants", "Silicone Accessories", "Sealant Tools", "Caulking Gun", "price-check"], options=["Size"],
    variants=[({"Size": "300ml"}, "A1380", 14.95, 0.5, "parcel"), ({"Size": "850ml"}, "770502", 29.95, 0.9, "parcel20")],
    market="No RLA listing found (28 Oct 2026); Fuller 300ml gun $15.60 at Bretts. 850ml priced as a large barrel gun.", price_check_variants=["300ml", "850ml"],
    material="Steel skeleton frame caulking gun, black with orange trim", range="Caulking gun, 300ml or 850ml cartridge", warranty="RLA product warranty",
    images=[("crop-caulking-gun.png", "RLA heavy duty skeleton caulking gun")],
    desc=html(["RLA's heavy duty skeleton caulking gun has a steel frame, a handle that combines the plunger and release clip, and a rotating barrel, so you can run a bead round a corner without stopping or repositioning the nozzle. The 300ml gun takes every standard silicone and sealant cartridge; the 850ml gun takes the large RLA UltraGrip cartridge.",
               "Trade quality for fast, efficient caulking."],
              uses=["Silicone, acrylic, SMP and polyurethane cartridges (300ml)", "RLA UltraGrip 850ml construction adhesive cartridges (850ml)", "Everyday tiling, glazing and building sealing"],
              specs=["Type: heavy duty skeleton caulking gun", "Frame: steel", "Sizes: 300ml cartridge or 850ml cartridge", "Rotating barrel, plunger handle with release clip", "Colour: black with orange trim"],
              notes=["For 600ml foil sausages (Flex-Pro, Silikon 400LM, Max SMP sausages) you need a closed barrel sausage gun, not this gun."]))

# ============================== ACOUSTIC ADHESIVES (Tiling Catalogue p22) ==============================
add(key="acoustic-dry", title="RLA Dry Area Acoustic Mat Adhesive 15L", type="Adhesives", cat="adhesive",
    tags=["Hardware", "Adhesives & Additives", "Acoustic", "Flooring Adhesive", "Green Star", "price-check"], ship="local", weight=18, price=189.95, sku="RL-7197-15",
    market="No online listing found (28 Oct 2026); priced against RLA's 15 L resilient flooring adhesives ($230 to $258 at Beaumont).",
    material="Water based synthetic polymer adhesive, solvent free, Green Star compliant (IEQ-13 v2 and IEQ-11 v1.1)", range="Dry Area Acoustic Mat Adhesive, 15 L, beige", warranty="RLA product warranty when applied to the data sheet",
    images=[("dry-area-acoustic-mat-adhesive.png", "RLA Dry Area Acoustic Mat Adhesive pail")],
    desc=html(["RLA Dry Area Acoustic Mat Adhesive is a water based, synthetic polymer adhesive for direct sticking RLA approved acoustic mats to internal concrete subfloors in dry areas, the first step of an acoustic tiled floor in apartments and multi-residential buildings. One part, ready to use, solvent free and low odour, and Green Star compliant.",
               "Tile over the mat with RLA UniGrip or UniLite S2."],
              uses=["Adhering RLA approved acoustic mats to internal concrete subfloors", "Dry areas: living rooms, hallways and bedrooms in apartments", "Acoustic underlay systems under tiles and timber"],
              specs=["Type: water based synthetic polymer adhesive, one part", "Size: 15 L", "Colour: beige", "Substrate: internal concrete, dry areas", "Solvent free, low odour, Green Star compliant (IEQ-13 v2 and IEQ-11 v1.1)"],
              notes=["Dry areas only: use RLA Wet Area Acoustic Mat Adhesive in showers, bathrooms and balconies.", "Concrete must be dry, sound and primed to the data sheet; check moisture before laying."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/08/FLEX-PRO-MS.pdf"))

add(key="acoustic-wet", title="RLA Wet Area Acoustic Mat Adhesive SMP 10L", type="Adhesives", cat="adhesive",
    tags=["Hardware", "Adhesives & Additives", "Acoustic", "Flooring Adhesive", "SMP", "Green Star", "price-check", "needs-photo"], ship="local", weight=12, price=219.95, sku="RL1010-15",
    market="No online listing found (28 Oct 2026); priced against RLA's SMP flooring adhesives (X3 10 L is $260 at Beaumont).",
    material="Single part permanently flexible silyl modified polymer (SMP) adhesive, solvent free, Green Star compliant (IEQ-13 v2 and IEQ-11 v1.1)", range="Wet Area Acoustic Mat Adhesive, 10 L, beige", warranty="RLA product warranty when applied to the data sheet",
    images=[("crop-acoustic-wet.png", "RLA Wet Area Acoustic Mat Adhesive pail")],
    desc=html(["RLA Wet Area Acoustic Mat Adhesive is a single part, permanently flexible SMP adhesive for direct sticking RLA approved acoustic mats in wet areas such as showers, bathrooms and balconies, where a water based adhesive would fail. It also bonds engineered timber, parquet and timber sheet directly to concrete.",
               "Solvent free, low odour, non foaming, no shrinkage, ready to use and easy to spread, and Green Star compliant."],
              uses=["Adhering RLA approved acoustic mats in showers, bathrooms, laundries and balconies", "Engineered timber, parquet and timber sheet directly to concrete", "Wall and floor acoustic underlay systems"],
              specs=["Type: single part SMP adhesive, permanently flexible", "Size: 10 L", "Colour: beige", "Walls and floors, wet areas", "Solvent free, low odour, non foaming, no shrinkage, Green Star compliant (IEQ-13 v2 and IEQ-11 v1.1)"],
              notes=["Prime the concrete to the data sheet; moisture cured, so reseal the pail after use.", "Tile over the mat with RLA UniGrip or UniLite S2 after the adhesive has cured."],
              tds="https://www.rlapolymers.com.au/wp-content/uploads/2024/05/MAX-SMP-25_TDS.pdf"))


# ============================== GRIPSET WATERPROOFING PRODUCT GUIDE (V1) ==============================
# Gripset is RLA's waterproofing brand (gripset.com). Codes from the guide; packaging, coverage and dry times from gripset.com.
GS_TAGS = ["Hardware", "Waterproofing", "Gripset"]
GS_WARR = "Gripset/RLA product warranty when applied to the data sheet and the relevant standard"
GS_NOTES = ["Use the Gripset detailing system (Elastoproof B50 band, corners and collars) as the bond breaker at junctions and penetrations.",
            "Two coats at right angles to the dry film thickness on the data sheet; flood test only after the time stated.",
            "Waterproofing of wet areas in WA must be done by a licensed waterproofer to AS 3740."]
TD = lambda slug, h: f"https://gripset.com/downloads/?fl=tds{h}.pdf&dr=tds"
SD = lambda h: f"https://gripset.com/downloads/?fl=sds{h}.pdf&dr=sds"

add(key="gs-e60", title="Gripset E60 Water Based Epoxy Primer & Moisture Barrier Kit", type=WP_TYPE, cat="primer",
    tags=GS_TAGS + ["Primer", "Epoxy", "Vapour Barrier"], options=["Size"],
    variants=[({"Size": "4 L kit"}, "GWS085", 97.95, 5, "parcel20"), ({"Size": "10 L kit"}, "GWS072", 199.95, 12, "bulky"), ({"Size": "20 L kit"}, "GWS071", 349.95, 24, "local")],
    market="TradieCart 4 L $100.10, 10 L $206.09, 20 L $363.00 inc GST; Adheseal 4 L $106.24 ex, 20 L $391.04 ex (28 Oct 2026).",
    material="Two component water based epoxy primer and moisture/vapour barrier, AS 4020 potable water approved", range="Gripset E60, 4 L, 10 L or 20 L kit (Part A + Part B)", warranty=GS_WARR,
    images=[("gripset-e60.png", "Gripset E60 water based epoxy primer kit")],
    desc=html(["Gripset E60 is a two component water based epoxy that works as both a primer and a protective coating against moisture and rising damp coming through concrete and mineral surfaces. It goes on damp and green concrete, resists up to 25 metres (250 kPa) of hydrostatic pressure and gives Gripset membranes, tile adhesives and floor finishes a surface they can bond to.",
               "Non flammable, odourless, low VOC, with an extended pot life. Complies with AS 4020 for potable water storage."],
              uses=["Vapour and moisture barrier over damp or green concrete before membranes, tiles or flooring", "Primer where substrate moisture is above the limit in the installation standard", "Hydrostatic pressure resistant coating against negative moisture and rising damp", "Sealing water tanks and other potable water structures", "Primer for Gripset membranes, XpressLay and BRW sheet systems"],
              specs=["Type: two part water based epoxy, 1:1 mix", "Kits: 4 L, 10 L or 20 L", "Pot life 2 hours; recoat 4 hours; overcoat with finishes 24 hours; immersion and full cure 7 days", "Colour: Part A light grey, Part B white; dries semi-gloss to matte", "Hydrostatic resistance up to 25 m (250 kPa); AS 4020 potable water approved", "Internal and external use"],
              notes=["Mix the full kit (or both parts in ratio) and apply within the pot life.", "Wear gloves and eye protection; read both safety data sheets."] + GS_NOTES[2:],
              tds=TD("e60", "68b3b536d868d744c29bd0a028eb8502"), sds=SD("19e368e3fa9057e24e1f1d93b518a1d2")))

add(key="gs-gp", title="Gripset GP General Purpose Primer", type=WP_TYPE, cat="primer",
    tags=GS_TAGS + ["Primer"], options=["Size"],
    variants=[({"Size": "5 L"}, "GWS117", 84.95, 5.3, "parcel20"), ({"Size": "15 L"}, "GWS034", 127.95, 16, "local")],
    market="TradieCart 5 L $90.20, 15 L $132.00 inc GST; Adheseal 5 L $87.36 ex, 15 L $190.51 ex; The Waterproofing Shop 5 L $73 (28 Oct 2026).",
    material="Water based acrylic primer for porous substrates", range="Gripset GP, 5 L or 15 L (about 8 to 10m² per litre per coat)", warranty=GS_WARR,
    images=[("gripset-gp.png", "Gripset GP general purpose primer")],
    desc=html(["Gripset GP is the everyday primer for porous surfaces before Gripset membranes and tile adhesives: concrete, block, screed, render, masonry, aerated concrete, compressed fibre cement and plasterboard. Fast drying (about 30 minutes), economical coverage and excellent adhesion.",
               "Milky white wet, clear dry, internal and external."],
              uses=["Priming porous substrates before Gripset 38FC, P39, Xpress Multi Pro, 2P and C-1P", "Before Gripset C-Lite, C-Mastic, C-Stone and C-Rubber tile adhesives", "Before Gripset BRW sheet membranes on porous surfaces"],
              specs=["Type: water based primer for porous surfaces", "Sizes: 5 L or 15 L", "Coverage: 1 litre per 8 to 10m² per coat", "Dry time: about 30 minutes at 23 °C and 50% RH", "Colour: milky white wet, clear dry"],
              notes=["Non porous or smooth surfaces (tiles, metal, dense concrete) need Gripset OP instead.", "Apply by brush or roller to a clean, dust free surface and let it dry before coating."],
              tds=TD("gp", "3a87f35f07dc485b59a3a30690fd1c24"), sds=SD("7b324f6c8c581971a4e630ffb693fd3c")))

add(key="gs-op", title="Gripset OP Non-Porous Surface Primer", type=WP_TYPE, cat="primer",
    tags=GS_TAGS + ["Primer", "Tile Over Tile"], options=["Size"],
    variants=[({"Size": "1 L"}, "GWS106", 27.95, 1.2, "parcel"), ({"Size": "5 L"}, "GWS118", 129.95, 5.5, "parcel20"), ({"Size": "15 L"}, "GWS040", 244.95, 16, "local")],
    market="TradieCart 1 L $28.79, 5 L $135.30, 15 L $256.30 inc GST; B&B Hardware Maddington 1 L $32.80, 5 L $149.95, 15 L $325.00 (28 Oct 2026). Priced under both.",
    material="Solvent free multipurpose primer for non porous, smooth and difficult substrates", range="Gripset OP, 1 L, 5 L or 15 L (minimum 1 litre per 10m² on smooth surfaces)", warranty=GS_WARR,
    images=[("gripset-op.png", "Gripset OP non-porous surface primer")],
    desc=html(["Gripset OP is the solvent free answer to priming the surfaces that nothing sticks to: metal flashings and water stops, existing ceramic tiles and stone, glass reinforced and dense concrete, Scyon and compressed fibre cement, rigid PVC flanges and pipe penetrations. It dries fast to a non tacky, textured blue film that gives Gripset membranes and tile adhesives a mechanical key.",
               "Low VOC, brush or roller application, internal and external."],
              uses=["Priming metal flashings, puddle flanges and water stops before membrane", "Tiling or waterproofing over existing tiles and natural stone", "Dense, smooth or glass reinforced concrete", "Compressed fibre cement and Scyon flooring", "PVC leak control flanges and pipe penetrations"],
              specs=["Type: solvent free multipurpose primer for non porous surfaces", "Sizes: 1 L, 5 L or 15 L", "Coverage: at least 1 litre per 10m² on smooth non porous surfaces", "Dry time: about 30 minutes at 23 °C and 50% RH", "Colour: blue; textured, non tacky finish", "Low VOC, internal and external"],
              notes=["Degrease and rinse existing tiles before priming.", "Coat with the membrane or adhesive within the time on the data sheet."],
              tds=TD("op", "2d21202bb4967cf420df44db433745ee"), sds=SD("237fbf9d152af5803fed51f0c340102b")))

add(key="gs-11y", title="Gripset 11Y Latex Waterproof Additive", type="Adhesives", cat="adhesive",
    tags=["Hardware", "Adhesives & Additives", "Additive", "Gripset", "Waterproofing"], options=["Size"],
    variants=[({"Size": "5 L"}, "GWS116", 89.95, 5.3, "parcel20"), ({"Size": "15 L"}, "GWS015", 204.95, 16, "local")],
    market="TradieCart 5 L $94.60, 15 L $213.62 inc GST; Adheseal 5 L $99.49 ex, 15 L $218.09 ex (28 Oct 2026).",
    material="Concentrated SBR latex polymer admixture for cement based compounds", range="Gripset 11Y, 5 L or 15 L (slurry primer about 1 litre per 3m²)", warranty=GS_WARR,
    images=[("gripset-11y.png", "Gripset 11Y latex waterproof additive")],
    desc=html(["Gripset 11Y is a concentrated SBR latex admixture that upgrades sand and cement screeds, renders and repair mortars: more adhesion, more strength, better water resistance and durability, for general work and for demanding areas exposed to weather, continuous immersion and underground conditions.",
               "Mixed with cement it is also a high bond slurry primer, including under Gripset C-Bed screed, over porous concrete and blockwork, and in immersed and underground areas, or a thin waterproof protective slurry coat."],
              uses=["Additive for screeds, renders and repair mortars", "High bond slurry primer before 11Y enhanced screeds and under Gripset C-Bed", "Primer for immersed and underground areas and porous concrete or blockwork", "Thin build waterproof protective slurry coat"],
              specs=["Type: concentrated SBR latex admixture", "Sizes: 5 L or 15 L", "Slurry primer coverage: about 1 litre of 11Y per 3m²", "Colour: white thin liquid", "Substrates: concrete, masonry, render, screed, blocks, aerated concrete, clay brick, cement sheet, marine ply, asphalt, existing acrylic coatings and Gripset membranes"],
              notes=["Dilution ratios differ by use; see the data sheet.", "Before use over existing paint or coatings check suitability with RLA technical support."],
              tds=TD("11y", "a7e6216412846bda30d5d0140e250d59"), sds=SD("6ffe992d90ae532c84fb53a4e0221ca6")))

add(key="gs-b50", title="Gripset Elastoproof B50 Bond Breaker Joint Band 120mm", type=WPA_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Bond Breaker", "Waterproofing Tape"], options=["Length"],
    variants=[({"Length": "10m roll (B10)"}, "GWS010", 45.95, 1.2, "parcel20"), ({"Length": "50m roll (B50)"}, "GWS011", 164.95, 5, "parcel20")],
    market="TradieCart B10 $47.96, B50 $170.50 inc GST; Adheseal $51.61 / $194.16 ex (28 Oct 2026).",
    material="High grade rubber compound joint band, rupture, chemical and water resistant", range="Elastoproof B50 / B10, 120mm wide, 50m or 10m roll, grey", warranty=GS_WARR,
    images=[("elastoproof-b50.png", "Gripset Elastoproof B50 bond breaker joint band")],
    desc=html(["The Elastoproof B50 Joint Band is Gripset's bond breaker system for every joint, junction and movement zone in a waterproofing job. Made from a high grade rubber compound, it takes longitudinal, lateral and transverse movement with high elongation, rupture resistance and up to 100% elastic recovery, and because the membrane bonds to the band rather than the corner, you do not need to run a sealant bead first.",
               "The waterproofer's favourite for its speed: lay it into the first coat, no drying time for a sealant bond breaker. Pair it with the Elastoproof corners and collars."],
              uses=["Wall/floor junctions in showers, bathrooms, laundries and balconies", "Substrate abutments and sheet joints", "Control joints, movement and expansion joints", "Bond breaker under Gripset 38FC, P39, Xpress Multi Pro, 2P, C-1P and LS"],
              specs=["Type: rubber bond breaker joint band", "Width: 120mm", "Rolls: 10m (B10) or 50m (B50)", "Colour: grey", "Rupture, chemical and water resistant, up to 100% elastic recovery"],
              notes=["Bed into the first membrane coat and cover with the second; keep the band centred on the junction.", "Use Elastoproof CN90 and CN270 corners at the corners."],
              tds=TD("b50", "5619e42f07a2a9b8c884275edd014a4f"), sds=SD("ec9f6a78445277239065767e6da4006c")))

add(key="gs-corners", title="Gripset Elastoproof Prefabricated Corner", type=WPA_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Bond Breaker", "Waterproofing Corners"], options=["Type"],
    variants=[({"Type": "Internal 90° (CN90)"}, "GWS009", 7.95, 0.08, "parcel"), ({"Type": "External 270° (CN270)"}, "GWS006", 9.45, 0.08, "parcel")],
    market="TradieCart CN90 $8.37, CN270 $9.90 inc GST each; Adheseal pack of 10 $90.65 ex (28 Oct 2026). Sold singly.",
    material="Prefabricated rubber corner, 200 x 200mm with 120mm wall/floor returns", range="Elastoproof corners CN90 (internal) and CN270 (external), sold each, grey", warranty=GS_WARR,
    images=[("elastoproof-corners.jpg", "Gripset Elastoproof prefabricated corners")],
    desc=html(["Elastoproof prefabricated corners finish the B50 joint band at the two places a membrane most often fails: the internal 90° corner of a shower and the external 270° corner of a hob, pillar or outside return. Each corner is a seamless, elastic rubber moulding with 120mm wall and floor returns that overlaps the band, so there is no fold, no pin holing and no thick build of membrane drying slowly in the corner.",
               "Sold each, so you buy exactly the number of corners on the job."],
              uses=["Internal CN90: 90° wall/floor corners in showers, bathrooms and laundries", "External CN270: hobs, pillars, columns and outside returns", "With Elastoproof B50 joint band under all Gripset liquid membranes"],
              specs=["Size: 200 x 200mm with 120mm wall/floor returns", "Types: CN90 internal 90°, CN270 external 270°", "Material: rubber, seamless and elastic", "Colour: grey", "Sold each"],
              notes=["Lay the corner first, then run the B50 band over the returns, all bedded in the first membrane coat."],
              tds=TD("corners", "06352f243399e2861b9bd356fdb9c746"), sds=SD("eeb4b458140cdec70b75339017be2e07")))

add(key="gs-collars", title="Gripset Elastoproof Base Collars for Pipes & Penetrations, Pack", type=WPA_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Bond Breaker", "Waterproofing Collars", "price-check"], options=["Pack"],
    variants=[({"Pack": "Small 120 x 120mm, pack of 10 (pipes to 50mm)"}, "GWS064", 89.95, 0.6, "parcel20"), ({"Pack": "Medium 250 x 250mm, pack of 10 (pipes to 110mm)"}, "GWS057", 179.95, 1.5, "parcel20"),
              ({"Pack": "Medium 250 x 250mm, pack of 30 (pipes to 110mm)"}, "GWS148", 499.95, 4.5, "parcel20"), ({"Pack": "Large 350 x 350mm, pack of 10 (pipes to 150mm)"}, "GWS077", 379.95, 3, "parcel20")],
    market="Adheseal small pack of 10 $90.65 ex ($99.72 inc), medium pack $180.50 ex ($198.55), large pack $377.10 ex ($414.81); TradieCart sells singles at $9.35 / $19.31 / $40.70 inc (28 Oct 2026). Medium 30 pack priced pro rata (price-check).", price_check_variants=["Medium 250 x 250mm, pack of 30 (pipes to 110mm)"],
    material="Prefabricated rubber flange seal", range="Elastoproof base collars, small, medium or large, packs of 10 (medium also 30), grey", warranty=GS_WARR,
    images=[("elastoproof-base-collars.png", "Gripset Elastoproof base collars")],
    desc=html(["Elastoproof collars are prefabricated rubber flange seals that go around pipes, drainage outlets, cabling and fixtures to make a permanent, tight elastic seal against water. They protect the membrane at the penetration from movement, vibration and cracking, so a mixer tap or floor waste that moves a little does not open a leak.",
               "Three sizes to suit pipes up to 50mm, 110mm and 150mm, sold in trade packs of 10 (medium also in 30s)."],
              uses=["Tap and shower breech penetrations (small)", "Floor wastes and 100mm drainage outlets (medium)", "Large pipes and outlets on roofs, decks and planters (large)", "Ponds, tanks and water features"],
              specs=["Small: 120 x 120mm, pipes and penetrations up to 50mm, pack of 10", "Medium: 250 x 250mm, up to 110mm, pack of 10 or 30", "Large: 350 x 350mm, up to 150mm, pack of 10", "Material: rubber, rupture resistant", "Colour: grey"],
              notes=["Prime metal or PVC flanges with Gripset OP first; bed the collar into the first membrane coat and cover with the second."],
              tds=TD("collars", "96034e2c6875bc86e7b22e003e7eb039"), sds=SD("1dbdb588502698c0f7b2849871eb23eb")))

add(key="gs-brw-pf-tape", title="Gripset BRW PF Tape Self-Adhesive Butyl Sealing Tape 10m", type=WPA_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Butyl Tape", "Waterproofing Tape", "Bond Breaker"], options=["Width"],
    variants=[({"Width": "80mm x 10m"}, "GWS231", 29.95, 0.9, "parcel20"), ({"Width": "150mm x 10m"}, "GWS146", 53.95, 1.6, "parcel20")],
    market="TradieCart 80mm $31.30, 150mm $55.94 inc GST; Adheseal $33.69 / $60.22 ex (28 Oct 2026).",
    material="Self adhesive butyl rubber tape with white fabric face", range="BRW PF Tape, 80mm or 150mm x 10m roll", warranty=GS_WARR,
    images=[("elastoproof-butyl.png", "Gripset BRW PF Tape butyl sealing tape")],
    desc=html(["Gripset BRW PF Tape is a self adhesive butyl sealing band with a fabric face: it sticks instantly, so there is no drying or curing before you move on, and the fabric face takes Gripset membranes, adhesives, mortars and renders straight over the top. The butyl backing resists moisture, vibration and flexing on internal and external surfaces.",
               "Use it as a bond breaker at wall/floor junctions, to seal puddle flanges, penetrations and water stops, to detail over pipes and flashings, for guttering and roofing, and to patch pin holes in metal before coating."],
              uses=["Bond breaker to wall/floor junctions, joint intersections and transitions", "Sealing puddle flanges, penetrations and water stops", "Detailing over plumbing pipes, PVC and flashings", "Guttering, roofing and patching pitted metal", "General maintenance under surface finishes"],
              specs=["Type: self adhesive butyl rubber tape, fabric faced", "Widths: 80mm or 150mm", "Roll: 10m", "Colour: fabric face white, butyl backing grey", "Rupture and tear resistant, instant seal, internal and external"],
              notes=["Press firmly onto a clean, dry, dust free surface; prime smooth or dusty surfaces with Gripset OP or GP.", "Overcoat with membrane as the data sheet directs."],
              tds=TD("pf", "2354bb6c59857e1eaf21584fbc733d8c"), sds=SD("97c5d08250f8fd59f78fdc4047ab1152")))

add(key="gs-brw-pf-square", title="Gripset BRW PF Square Self-Adhesive Flange Seal 250 x 250mm", type=WPA_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Butyl Tape", "Waterproofing Collars"], ship="parcel", weight=0.1, price=10.45, sku="GWS152",
    market="TradieCart $11.00 inc GST; Adheseal $9.99 ex (28 Oct 2026).",
    material="Self adhesive butyl rubber square with fabric face", range="BRW PF Square, 250 x 250mm, sold each", warranty=GS_WARR,
    images=[("crop-gs-pf-square.png", "Gripset BRW PF Square flange seal")],
    desc=html(["The BRW PF Square is a 250 x 250mm self adhesive butyl square for the fast detailing of leak control flanges, floor wastes and similar penetrations. Peel, press and it has sealed; no drying before the membrane goes over it.",
               "Excellent adhesion, instant sealing, and it simplifies the fiddliest part of a shower floor."],
              uses=["Leak control (puddle) flanges", "Floor wastes and drainage outlets", "Square penetrations through floors"],
              specs=["Size: 250 x 250mm", "Material: self adhesive butyl rubber, fabric faced", "Instant seal, no drying required", "Sold each"],
              notes=["Cut the centre to suit the flange; prime metal and PVC with Gripset OP; overcoat with the membrane."],
              tds=TD("pf", "2354bb6c59857e1eaf21584fbc733d8c"), sds=SD("97c5d08250f8fd59f78fdc4047ab1152")))

add(key="gs-38fc", title="Gripset 38FC SBR Fast Cure Waterproofing Membrane", type=WP_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Class III", "Fast Cure", "Waterproofing Membrane"], options=["Size"],
    variants=[({"Size": "5 L"}, "GWS068", 82.95, 6, "parcel20"), ({"Size": "15 L"}, "GWS065", 149.95, 18, "local")],
    market="TradieCart 5 L $86.52, 15 L $154.55 inc GST; B&B Hardware Maddington 15 L $175.00; Adheseal $93.63 / $189.68 ex (28 Oct 2026). 15 L priced under TradieCart, well under B&B.",
    material="Water based fast curing fibre reinforced SBR latex membrane, AS/NZS 4858 and AS 4654.1 compliant", range="Gripset 38FC, 5 L or 15 L pail, blue", warranty=GS_WARR,
    images=[("gripset-38fc.png", "Gripset 38FC fast cure waterproofing membrane pail")],
    desc=html(["Gripset 38FC is Australia's best known wet area membrane: a water based, fast curing, fibre reinforced SBR latex membrane that can be recoated after 1 hour, tiled over after 4 hours and flood tested after 24, so waterproofing and tiling can be done in one day. It withstands continuously wet conditions and ponding without re-emulsifying, and it is compliant to AS/NZS 4858 and AS 4654.1 for internal and external areas that will be covered with tiles, toppings or overlay finishes.",
               "Flexible, elastomeric, solvent free, non toxic and non flammable; brush, roller or spray."],
              uses=["Showers, bathrooms, laundries and internal wet areas", "Balconies, terraces, decks, roofs and concrete slabs under tiles or toppings", "Residential and commercial jobs with tight turnaround", "Over concrete, render, masonry, fibre cement, wet area plasterboard and primed substrates"],
              specs=["Compliant to AS/NZS 4858 and AS 4654.1, internal and external", "Sizes: 5 L or 15 L pail", "Recoat 1 hour; tiling or toppings 4 hours; flood test 24 hours (23 °C, 50% RH)", "Colour: blue, wet and dry", "Fibre reinforced, low water vapour transmission, will not re-emulsify", "Water based, solvent free, non toxic, non flammable"],
              notes=["Prime with Gripset GP (porous) or OP (non porous); use Gripset E60 or Xpress Primer H2O Plus over damp concrete.", "Not for exposed, UV facing finishes: top coat with Gripset LS where the membrane stays exposed."] + GS_NOTES,
              tds=TD("38fc", "45af3609390928dcca54ed837bae3d7a"), sds=SD("15ab38e45c687acc23b1c0c772a1e5f8")))

add(key="gs-p39", title="Gripset P39 Polyurethane Hybrid Waterproofing Membrane 15L", type=WP_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Class III", "UV Stable", "Waterproofing Membrane"], ship="local", weight=18, price=184.95, sku="GWS131",
    market="TradieCart $190.00 inc GST; Adheseal $232.47 ex (28 Oct 2026).",
    material="Water based fibre enhanced hybrid polyurethane membrane, AS 4858 and AS 4654.1 compliant, solvent free", range="Gripset P39, 15 L pail, light grey", warranty=GS_WARR,
    images=[("gripset-p39.png", "Gripset P39 polyurethane hybrid membrane pail")],
    desc=html(["Gripset P39 is a fibre enhanced membrane built on hybrid polyurethane technology: the performance of a polyurethane with no solvent and no hazardous classification. It has outstanding waterproofing and low vapour transmission, takes early ponding water and permanently wet conditions without re-emulsifying, and has the weather and UV resistance to be left exposed on roofs and decks with light foot traffic, or used under tiles.",
               "Compliant with AS 4858 and AS 4654.1 for internal and external wet areas, fast drying, resistant to fungi and algae, low dirt retention."],
              uses=["Roofs and exposed decks as a light trafficable membrane", "Under tiles on balconies, terraces and podiums", "Internal wet areas", "Any external area that will see sun and rain before it is finished"],
              specs=["Compliant to AS 4858 and AS 4654.1, internal and external", "Size: 15 L pail", "Recoat 2 to 4 hours; dry film 24 hours; tiling or toppings 24 to 48 hours; flood test 72 hours", "Colour: light grey", "Solvent free, non hazardous, highly flexible and elastomeric, UV resistant, light foot traffic"],
              notes=["Prime with Gripset GP, OP or E60 to suit the substrate.", "For heavier foot traffic on exposed areas finish with Gripset LS."] + GS_NOTES,
              tds=TD("p39", "cd28a598f37e3d1783b994f7ff125601"), sds=SD("47abacb632e8f4d96956eceada1166d9")))

add(key="gs-ls", title="Gripset LS External Trafficable Non-Slip Top Coat 15L", type=WP_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Top Coat", "UV Stable", "Non Slip"], ship="local", weight=18, price=204.95, sku="GWS039",
    market="TradieCart $213.73 inc GST; Adheseal $230.09 ex (28 Oct 2026).",
    material="Water based hard wearing non slip top coat for Gripset liquid membranes, solvent free", range="Gripset LS, 15 L pail, light grey (about 8m² per pail at two coats)", warranty=GS_WARR,
    images=[("gripset-ls.png", "Gripset LS external trafficable coating pail")],
    desc=html(["Gripset LS is the hard wearing, non slip top coat that goes over Gripset 38FC, P39 or Xpress Multi Pro on roofs, podiums, balconies and walkways that stay exposed: it protects the membrane from permanent UV, weather and light foot traffic and gives a non slip finish without any sand casting or aggregate.",
               "Solvent free and non hazardous, non shrinking, flexible, resistant to fungi and algae, excellent ponding water resistance, and it can be built up thick for extra durability."],
              uses=["Exposed roofs and rooftop plant and maintenance areas (over a Gripset base membrane)", "Decks, balconies and podiums left exposed", "Walkways as a non slip, water resistant coating"],
              specs=["Type: water based non slip finish coat", "Size: 15 L pail", "Coverage: about 8m² per pail at two coats", "Recoat 4 hours; dry film 24 hours; flood test 10 days", "Colour: light grey", "Solvent free, non hazardous, foot trafficable"],
              notes=["Not a standalone crack bridging membrane: always over a suitable Gripset base membrane on suspended areas.", "Apply once the base membrane has cured as its data sheet directs."],
              tds=TD("ls", "e9481360fab2eefff428d6dac988739f"), sds=SD("3c841287a08961b23de30a7c30dc4514")))

add(key="gs-51", title="Gripset 51 Solvent Free Bitumen Rubber Membrane", type=WP_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Bitumen", "Below Ground", "Waterproofing Membrane"], options=["Size"],
    variants=[({"Size": "5 L"}, "GWS119", 63.95, 6, "parcel20"), ({"Size": "15 L"}, "GWS022", 139.95, 18, "local")],
    market="TradieCart 5 L $66.44, 15 L $144.65 inc GST; Adheseal $71.51 / $155.70 ex (28 Oct 2026).",
    material="Water based solvent free bitumen rubber liquid membrane", range="Gripset 51, 5 L or 15 L pail, black when dry", warranty=GS_WARR,
    images=[("gripset-51.png", "Gripset 51 bitumen rubber membrane pail")],
    desc=html(["Gripset 51 is a water based, solvent free bitumen rubber membrane for underground and external work: retaining walls, cellar and basement walls, planter boxes and garden beds, and as a protective coating over timber and metal against corrosion, rot and salt damp. It bonds to asphalt and bitumen, so it also repairs failed, aged coatings and gutters.",
               "Flexible, crack bridging, withstands continuously damp conditions, user and environmentally safe, and it can be mixed with cement for waterproofing slurries and mortars."],
              uses=["Retaining walls, basements and underground surfaces", "Planter boxes and garden beds", "Gutter repairs and aged bitumen coatings", "Protective coating over metal and timber", "Waterproofing slurries and mortars when mixed with cement"],
              specs=["Type: water based bitumen rubber membrane, solvent free, non toxic, non flammable", "Sizes: 5 L or 15 L pail", "Recoat 2 to 4 hours; dry film 24 hours; backfill 5 days; flood test 10 days", "Colour: charcoal wet, black dry", "Good crack bridging, adhesion to porous and non porous surfaces, sound deadening"],
              notes=["Not for exposed, UV facing areas: cover or backfill once cured.", "Prime porous surfaces as the data sheet directs."],
              tds=TD("51", "1c83bf06ba7069fb085ab3379031bc16"), sds=SD("4f2c6d74d8bb8f0697edcb462b362398")))

add(key="gs-xpress-h2o", title="Gripset Xpress Primer H2O Plus Vapour Barrier Primer 10L", type=WP_TYPE, cat="primer",
    tags=GS_TAGS + ["Primer", "Vapour Barrier", "Xpress"], ship="bulky", weight=11, price=324.95, sku="GWS192",
    market="TradieCart $335.50 inc GST; Adheseal $303.26 to $389.93 ex (28 Oct 2026).",
    material="One component vapour barrier primer for concrete and mineral surfaces", range="Gripset Xpress Primer H2O Plus, 10 L (about 6 to 8m² per litre)", warranty=GS_WARR,
    images=[("gripset-xpress.png", "Gripset Xpress Primer H2O Plus pail")],
    desc=html(["Xpress Primer H2O Plus is a one component vapour barrier primer for concrete, screeds and mineral surfaces that still hold moisture: it stops the blistering and delamination of membranes and coatings that residual dampness causes, without altering the surface profile, so the coating over it bonds as designed. Fast drying, finishes can go on after only 1 hour, and the colour changes to tell you when it is ready.",
               "Also a standalone sealer against carbonation of concrete and, over screeds and renders, a way to reduce efflorescence. Designed to pair with Xpress Multi Pro Membrane and the BRW sheet systems."],
              uses=["Priming damp and green concrete, screeds and renders before Gripset membranes", "Vapour barrier under Xpress Multi Pro, BRW HD and BRW PFN", "Standalone concrete sealer against carbonation", "Reducing efflorescence over screed and render"],
              specs=["Type: one component vapour barrier primer", "Size: 10 L pail", "Coverage: 1 litre per 6 to 8m²", "Dry time: 1 hour at 23 °C and 50% RH; colour changes from milky white through a green tinge to clear when ready", "Water resistant, one part, no mixing"],
              notes=["Apply thinly and evenly; do not leave puddles.", "Overcoat within the window on the data sheet."],
              tds=TD("xpress", "574a6a192f51c3d8288301b8ea896ae9"), sds=SD("ebc13ea2a827e2c9504b3a39ce6d435b")))

add(key="gs-xpress-multi-pro", title="Gripset Xpress Multi Pro Water Based Elastomeric Membrane 15L", type=WP_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Class III", "Fast Cure", "UV Stable", "Xpress", "Waterproofing Membrane"], ship="local", weight=18, price=279.95, sku="GWS191",
    market="TradieCart $284.24 and $344.30 inc GST on two listings; Adheseal $389.93 ex (28 Oct 2026).",
    material="Water based fast cure elastomeric membrane, AS 4858 and AS 4654 compliant, solvent free", range="Gripset Xpress Multi Pro Membrane, 15 L pail, light grey (about 1.5 L/m² under tile at 0.8mm DFT)", warranty=GS_WARR,
    images=[("gripset-xpress-multi-pro-membrane.png", "Gripset Xpress Multi Pro membrane pail")],
    desc=html(["Xpress Multi Pro is Gripset's next generation water based membrane: it cures fast even in cold and humid weather, is rain resistant after 3 hours and recoats after 1, and it stands up to early ponding and washout where ordinary water based membranes re-emulsify. Highly flexible and elastomeric with low vapour transmission and low water absorption, it is a safer alternative to solvent based polyurethanes for both under tile and exposed, UV facing work.",
               "Complies with AS 4858 and AS 4654 for internal and external applications. Use Xpress Primer H2O Plus underneath on damp or green concrete for the fastest turnaround."],
              uses=["Exposed roofs, decks and balconies subject to UV and weather", "Under tiles on balconies and external wet areas", "Internal wet areas", "Cold, damp or humid conditions where other membranes will not dry"],
              specs=["Compliant to AS 4858 and AS 4654, internal and external", "Size: 15 L pail", "Under tile: at least two coats at a total of 1.5 L/m² for a 0.8mm dry film", "Recoat 1 to 2 hours; dry film 1 hour; ponding water resistance 3 hours; full cure 24 hours", "Colour: light grey", "Solvent free, brush or medium nap roller"],
              notes=["Prime with Gripset GP, OP, E60 or Xpress Primer H2O Plus to suit the substrate.", "Finish exposed trafficable areas with Gripset LS."] + GS_NOTES,
              tds=TD("xmp", "c9e760ab58cf6e7b9c4a14e546168255"), sds=SD("c1f53ed9b11d6e8a75a98f1e3ed34910")))

add(key="gs-xpresslay", title="Gripset XpressLay Self-Adhesive Waterproof Anti-Fracture Sheet 1.3 x 10m", type=WP_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Sheet Membrane", "Anti-Fracture", "Xpress"], ship="local", weight=16, price=519.95, sku="GWS234",
    market="TradieCart $534.97 inc GST; Adheseal $578.97 ex (28 Oct 2026).",
    material="High strength reinforced self adhesive PVC sheet", range="Gripset XpressLay, 1.3m x 10m roll (13m²)", warranty=GS_WARR,
    images=[("gripset-xpresslay.png", "Gripset XpressLay self adhesive sheet roll")],
    desc=html(["Gripset XpressLay is a three in one sheet system for under tile floors: waterproof, anti-fracture and decoupling in one self adhesive PVC sheet. The high tack backing bonds to the substrate, the reinforced sheet resists vibration, movement and flexing so cracks in the slab do not telegraph through the tiles, and tile adhesives, membranes and screeds go straight onto its face.",
               "Rapid cold lay installation with no torching, no solvents and no drying time: ideal for shop fit outs, non permanent installations and floors over structural timber or fibre cement."],
              uses=["Waterproofing and anti-fracture underlay for internal wet area floors", "Decoupling tiles from cracked or jointed concrete slabs", "Tiling over structural timber and fibre cement sheet flooring", "Shop fit outs and non permanent installations"],
              specs=["Type: reinforced self adhesive PVC sheet, waterproof, anti-fracture, decoupling", "Roll: 1.3m x 10m (13m²)", "Self adhesive, cold lay, no torching or heat welding", "Excellent performance in cold and humid conditions", "Compatible with Gripset liquid membranes, adhesives and screeds"],
              notes=["Prime with Gripset Xpress SP or OP on non porous substrates and E60 on damp concrete.", "Seal joints and junctions with BRW PF Tape and the Elastoproof system as the data sheet directs."],
              tds=TD("xl", "80d3fbae6ea2e47db4c503667b934917"), sds=SD("f0ba64ec0c9ede8eb25178ce990691bc")))

add(key="gs-2p", title="Gripset 2P Two Part Flexible Cementitious Membrane Kit", type=WP_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Cementitious", "Pool", "Waterproofing Membrane"], ship="local", weight=27, price=179.95, sku="GWS190",
    market="TradieCart $186.73 inc GST; Adheseal $137.14 to $188.44 ex (28 Oct 2026).",
    material="Two component latex cementitious membrane, AS/NZS 4858 and AS 4654 compliant", range="Gripset 2P kit: 10 L Part A liquid in a 20 L pail + 15kg Part B powder", warranty=GS_WARR,
    images=[("gripset-2p.png", "Gripset 2P two part cementitious membrane kit")],
    desc=html(["Gripset 2P is a two component latex cementitious membrane for the broadest range of jobs: internal and external wet areas, feature walls, water features and swimming pools, potable water tanks, planter boxes, retaining walls and general tiled areas. Tough and durable yet flexible with high adhesion, and fast drying, which makes it the choice in cool and humid conditions.",
               "Compliant to AS/NZS 4858 and AS 4654 for internal and external applications. Mix the powder into the liquid in the pail and apply by brush, roller or trowel."],
              uses=["Internal wet areas: bathrooms, laundries and tiled areas", "External wet areas: balconies, decks, podiums and terraces", "Swimming pools, water features and potable water tanks", "Planter boxes, earth shelters and retaining walls", "Concrete, render, masonry, fibre cement, plasterboard and aerated concrete"],
              specs=["Compliant to AS/NZS 4858 and AS 4654, internal and external", "Kit: 10 L Part A liquid (in a 20 L mixing pail) + 15kg Part B powder", "Pot life 1 hour; recoat 2 to 4 hours; tiling or toppings 24 hours; flood test 72 hours; immersion 7 days", "Colour: light grey dry film", "Fast curing, flexible, tough, high adhesion"],
              notes=["Mix with a drill mixer to a lump free slurry; mix only what you can apply in the pot life.", "Cement based: wear gloves, eye protection and a dust mask."] + GS_NOTES,
              tds=TD("2p", "5d75a93979e9d567e3f0eb68fd209f4d"), sds=SD("20c85aae261be54d9eb619414d4d1e54")))

add(key="gs-c-1p", title="Gripset C-1P One Part Flexible Cementitious Membrane 15kg", type=WP_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Cementitious", "Negative Pressure", "Pool", "Waterproofing Membrane"], ship="bulky", weight=15.5, price=154.95, sku="GWS032",
    market="TradieCart $159.50 inc GST; Adheseal $166.30 ex (28 Oct 2026).",
    material="One component fibre reinforced flexible polymer cementitious membrane, AS 4020 potable water approved", range="Gripset C-1P, 15kg bag", warranty=GS_WARR,
    images=[("gripset-c-1p.png", "Gripset C-1P one part cementitious membrane bag")],
    desc=html(["Gripset C-1P is a one part cementitious membrane: graded aggregates, fibres and polymers in a 15kg bag, mixed on site with water. It handles both positive and negative water pressure (5 bar positive, 1.5 bar negative), bridges cracks, goes over damp and green concrete, takes UV exposure and is approved for potable water, which makes it the membrane for tanks, pools, basements, retaining walls and under tile wet areas alike.",
               "Brush, roller, trowel or texture spray on walls and floors without sagging. Non toxic, water based, solvent free."],
              uses=["Negative waterproofing: basements, lift pits and retaining walls from the inside", "Underground and immersed work: tanks, pools and water features", "Under tile internal wet areas", "Damp and green concrete and masonry"],
              specs=["Type: one part fibre reinforced cementitious membrane", "Bag: 15kg", "Resists 5 bar positive and 1.5 bar negative hydrostatic pressure", "Pot life 1 hour; recoat 2 to 4 hours; tiling or toppings 24 hours; water pressure 7 days; immersion 10 days", "Colour: dark grey wet, dark brown dry", "AS 4020 potable water approved, withstands UV"],
              notes=["Stop active leaks with Gripset C-Plug before coating.", "Cement based: wear gloves, eye protection and a dust mask."] + GS_NOTES,
              tds=TD("c1p", "adf878d4d96c0aa9e398c0c2df857066"), sds=SD("8d0e39f634381498560100baae4bfbe7")))

SCREED_TYPE = "Screeds & Levellers"  # new type, added to the Hardware and Tile Adhesive & Additives collection rules
add(key="gs-c-bed", title="Gripset C-Bed Premium Engineered Screed 20kg", type=SCREED_TYPE, cat="adhesive",
    tags=["Hardware", "Adhesives & Additives", "Screed", "Gripset"], ship="local", weight=20, price=26.95, sku="GWS210",
    market="TradieCart $27.72 inc GST; Adheseal $24.93 to $29.09 ex (28 Oct 2026).",
    material="Pre-blended polymer modified engineered screed, over 30 MPa", range="Gripset C-Bed, 20kg bag (about 2m² at 5mm)", warranty=GS_WARR,
    images=[("gripset-c-bed.png", "Gripset C-Bed engineered screed bag")],
    desc=html(["Gripset C-Bed is a ready to use, slump free, shrinkage compensated engineered screed for internal and external floors: select aggregates and polymers give it high strength at low builds, excellent water resistance (less efflorescence than sand and cement) and easy workability. Light foot traffic after 8 hours, tiles after 24.",
               "One pre-blended bag, no site batching, Australian made. Lay from 5mm up to 200mm."],
              uses=["Screeding bathroom and laundry floors to falls before waterproofing and tiling", "Balconies, decks and external floors", "Underlayment for tiles, carpet, vinyl and timber", "New work and remedial repairs"],
              specs=["Type: pre-blended engineered screed, polymer modified", "Bag: 20kg", "Coverage: about 2m² at 5mm thickness", "Thickness: 5mm to 200mm", "Working time 3 hours; set 4 hours; light foot traffic 8 hours; tiles 24 hours; timber floors 5 days", "Strength over 30 MPa; colour grey"],
              notes=["Prime with a Gripset 11Y slurry for the best bond.", "Cement based: wear gloves, eye protection and a dust mask."],
              tds=TD("cbed", "d701d8d1802ac180da31981c10d9cff1"), sds=SD("67a0a144a85d7db2238d30ac58df4e78")))

add(key="gs-c-level", title="Gripset C-Level Fast Set Self-Levelling Compound 20kg", type=SCREED_TYPE, cat="adhesive",
    tags=["Hardware", "Adhesives & Additives", "Leveller", "Gripset", "price-check"], ship="local", weight=20, price=44.95, sku="GWS209",
    market="No online listing found (28 Oct 2026); priced between Gripset C-Bed and the Roberts levellers in the store.",
    material="Rapid drying fibre reinforced cementitious self levelling compound, over 40 MPa", range="Gripset C-Level, 20kg bag (about 2.4m² at 5mm), 3 to 30mm per pour", warranty=GS_WARR,
    images=[("gripset-c-level.png", "Gripset C-Level self levelling compound bag")],
    desc=html(["Gripset C-Level is a rapid drying, fibre reinforced self levelling compound for new or existing concrete floors inside and out, and for internal timber floors. It flows to an ultra smooth finish, pours from 3 to 30mm in one go, needs no additives and reaches over 40 MPa, so it suits domestic, commercial and industrial floors under tile, stone, timber, carpet and vinyl, and even as an exposed finish in light traffic areas.",
               "Works with underfloor heating and the full Gripset waterproofing range."],
              uses=["Levelling concrete floors before tiles, vinyl, timber or carpet", "Levelling internal timber floors", "Floors with underfloor heating", "Light traffic exposed floors"],
              specs=["Type: rapid set fibre reinforced cementitious self leveller", "Bag: 20kg", "Coverage: about 2.4m² at 5mm", "Thickness: 3 to 30mm in a single application", "Open time 30 minutes; vinyl, carpet and tiles after 18 hours; timber 24 hours; coatings 48 hours", "Strength over 40 MPa; colour grey"],
              notes=["Prime the floor with Gripset GP (porous) or OP (non porous) first; mix with a drill mixer and pour within the open time.", "Cement based: wear gloves, eye protection and a dust mask."],
              tds=TD("clevel", "dd98a3b0b2ce2e7dc102921badc1b80e"), sds=SD("4ba6c8d962334c6f3d3812c88d0da0db")))

add(key="gs-c-plug", title="Gripset C-Plug Rapid Set Water Plug", type=SCREED_TYPE, cat="adhesive",
    tags=["Hardware", "Adhesives & Additives", "Repair Mortar", "Gripset", "Waterproofing"], options=["Size"],
    variants=[({"Size": "4kg"}, "GWS056", 54.95, 4.3, "parcel20"), ({"Size": "15kg"}, "GWS055", 164.95, 16, "bulky")],
    market="Adheseal 4kg $51.96 ex ($57.16 inc), 15kg $155.87 ex ($171.46 inc) (28 Oct 2026).",
    material="Rapid setting non shrink cement based water plug", range="Gripset C-Plug, 4kg or 15kg (bag in pail)", warranty=GS_WARR,
    images=[("gripset-c-plug.png", "Gripset C-Plug rapid set water plug pail")],
    desc=html(["Gripset C-Plug stops water that is actively leaking under pressure: a rapid setting, non shrink cement compound that sets in 1 to 3 minutes to form an instant waterproof seal in holes, cracks and openings in concrete and masonry. It cures to the strength of concrete, does not corrode steel reinforcement, is non toxic and non staining, and can be ground back to the existing profile.",
               "Use it with Gripset C-1P in basements and tanks subject to negative water seepage, and for rapid set anchoring of bolts and fixtures."],
              uses=["Active leaks in basements, cellars, lift pits and underground car parks", "Water tanks, retention structures, pipes, tunnels and culverts", "Waterproof, pressure resistant fillets at wall/floor junctions (with Gripset C-1P)", "Rapid set anchoring of bolts and fixtures"],
              specs=["Type: rapid setting non shrink cement based plug", "Sizes: 4kg or 15kg, bag in a pail", "Initial set under 1 minute; final set 2 to 4 minutes", "Cures to the mechanical strength of concrete; does not promote corrosion of reinforcement", "Non toxic, non staining, odour free"],
              notes=["Mix small amounts by hand to a stiff putty and press into the leak; it sets in the hand, so work fast.", "Wear gloves and eye protection."],
              tds=TD("cplug", "4f97c4c01fff6a472143f3f7ddf4907b"), sds=SD("691293e37d5b15ab799f60ec06c433c0")))

add(key="gs-hd-tape", title="Gripset Butyl HD Tape Self-Adhesive Bond Breaker 150mm x 10m", type=WPA_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Butyl Tape", "Bond Breaker", "Sheet Membrane"], ship="parcel20", weight=1.8, price=45.95, sku="GWS228",
    market="TradieCart BRW HD tape 150mm x 10m $47.41 inc GST (28 Oct 2026).",
    material="Self adhesive butyl rubber tape with HDPE face", range="Gripset Butyl HD Tape, 150mm x 10m roll", warranty=GS_WARR,
    images=[("crop-gs-hd-tape.png", "Gripset Butyl HD Tape roll")],
    desc=html(["Gripset Butyl HD Tape is the self adhesive butyl rubber detailing tape for the BRW HD sheet membrane system: it acts as the bond breaker at junctions and corners under BRW HD, and it seals over a wide variety of surfaces with the same high tack adhesion as the sheet.",
               "Cold applied, instant seal, no priming on metal, plastic or glazed surfaces."],
              uses=["System bond breaker for Gripset BRW HD sheet applications", "Detailing junctions, corners and penetrations under BRW HD", "General self adhesive butyl detailing on retaining walls, planters and roofs"],
              specs=["Type: self adhesive butyl rubber tape, HDPE faced", "Size: 150mm x 10m", "Instant seal, cold applied", "Use with Gripset BRW HD"],
              notes=["Press firmly onto a clean, dry surface; prime porous surfaces with Gripset GP or Xpress Primer H2O Plus."],
              tds=TD("brwhd", "0cbb1d6072f2c6bdf7e696ee668bc78d"), sds=SD("b351563fb156513b669ef7e8bfd4e22c")))

add(key="gs-brw-hd", title="Gripset BRW HD HDPE Reinforced Butyl Rubber Sheet Membrane 1m x 10m", type=WP_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Sheet Membrane", "Butyl", "Below Ground"], ship="local", weight=22, price=439.95, sku="GWS197",
    market="TradieCart $451.01 inc GST; Adheseal $462.21 ex (28 Oct 2026).",
    material="Self adhesive butyl rubber sheet membrane with laminated high strength HDPE film face, 1mm", range="Gripset BRW HD, 1mm x 1m x 10m roll (10m²)", warranty=GS_WARR,
    images=[("gripset-brw-hd.png", "Gripset BRW HD butyl rubber sheet membrane roll")],
    desc=html(["Gripset BRW HD is a self adhesive butyl rubber sheet membrane with a high strength HDPE film face for subterranean waterproofing and multi layer sheet membrane work: retaining walls, planter boxes, roof gardens and below ground structures. The high tack butyl backing bonds to porous and non porous surfaces from -30 °C to 80 °C, resists ground salts and chemicals, and forms an instant waterproof seal, so the area is in service as soon as it is laid.",
               "Cold lay, no torching or heat welding, primer-less on metal, plastic and glazed surfaces, and outstanding resistance to vibration, movement and flexing."],
              uses=["Retaining walls, basements and below ground structures", "Planter boxes and roof gardens", "Multi layer sheet membrane systems on roofs and podiums", "Fast track jobs where the membrane must be in service immediately"],
              specs=["Type: self adhesive butyl rubber sheet, HDPE faced", "Roll: 1mm x 1m x 10m (10m²), in a carton", "Service temperature -30 °C to 80 °C", "Colour: black HDPE face, black butyl backing", "Cold lay, instant seal, primer-less on metal, plastic and glazed surfaces"],
              notes=["Prime porous substrates with Gripset GP or Xpress Primer H2O Plus; seal roll ends and laps with Gripset BRW FG Sealing Tape and detail with Butyl HD Tape.", "Protect the membrane before backfilling as the data sheet directs."],
              tds=TD("brwhd", "0cbb1d6072f2c6bdf7e696ee668bc78d"), sds=SD("b351563fb156513b669ef7e8bfd4e22c")))

add(key="gs-brw-pfn", title="Gripset BRW PFN Fibre Reinforced Butyl Rubber Sheet Membrane 1m x 10m", type=WP_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Sheet Membrane", "Butyl", "Anti-Fracture"], ship="local", weight=20, price=409.95, sku="GWS225",
    market="TradieCart $423.50 inc GST; Adheseal $481.10 ex (28 Oct 2026).",
    material="Self adhesive butyl rubber sheet membrane with fabric face lamination, 1mm, AS 4858 and AS 4654 compliant", range="Gripset BRW PFN, 1mm x 1m x 10m roll (10m²)", warranty=GS_WARR,
    images=[("gripset-brw-pfn.png", "Gripset BRW PFN butyl rubber sheet membrane roll")],
    desc=html(["Gripset BRW PFN is a self adhesive butyl rubber sheet membrane for floors, internal and external, that can be tiled or topped directly: the fabric face takes tile adhesive and screed, the butyl backing gives outstanding waterproofing and resistance to vibration, movement and flexing, and the sheet has anti-fracture properties over cracked slabs.",
               "A hybrid system that works with Gripset liquid membranes for more versatility than either on its own. Cold lay, no torching, primer-less on metal, plastic and glazed surfaces, and compliant to AS 4858 and AS 4654 for internal and external wet areas."],
              uses=["Internal wet area floors under tiles", "Balconies, decks and external floors under tiles and toppings", "Anti-fracture layer over cracked or jointed slabs", "Floors over structural timber and fibre cement"],
              specs=["Compliant to AS 4858 and AS 4654, internal and external wet areas", "Roll: 1mm x 1m x 10m (10m²), in a carton", "Service temperature -30 °C to 80 °C", "Colour: white face fabric, grey butyl backing", "Cold lay, instant seal, tile direct onto the face"],
              notes=["Prime porous substrates with Gripset GP, 11Y slurry or E60; detail junctions and laps with BRW PF Tape and the Elastoproof system.", "Tile with Gripset C-Lite, C-Mastic or C-Stone."],
              tds=TD("brwpfn", "4099532eb76052412bc72a4d4a5514cc"), sds=SD("5a838fc3d3f7d5e07da3aa90f57671d6")))

add(key="gs-fg-tape", title="Gripset BRW FG Double Sided Fibreglass Sealing Tape 50mm x 15m", type=WPA_TYPE, cat="waterproofing",
    tags=GS_TAGS + ["Butyl Tape", "Sheet Membrane"], ship="parcel", weight=0.8, price=38.95, sku="GWS229",
    market="TradieCart $40.81 inc GST (28 Oct 2026).",
    material="Double sided fibreglass reinforced butyl strip, 1mm", range="Gripset BRW FG Sealing Tape, 1mm x 50mm x 15m roll", warranty=GS_WARR,
    images=[("crop-gs-fg-tape.png", "Gripset BRW FG sealing tape roll")],
    desc=html(["Gripset BRW FG Sealing Tape is a double sided, fibreglass reinforced butyl strip used at the sheet ends between rolls of BRW HD membrane and at overlaps that have no sealing strip. Double sided high tack, so it bonds both sheets instantly, and it also fixes water stops and other metal or plastic waterproofing accessories without a wet sealant.",
               "Compatible with the full Gripset detailing range."],
              uses=["Sealing sheet ends and laps of Gripset BRW HD", "Instant fixing of water stops and metal or plastic accessories", "Instant bonding alternative to wet applied sealants"],
              specs=["Type: double sided fibreglass reinforced butyl tape", "Size: 1mm x 50mm x 15m", "Colour: black", "Double sided high tack, excellent waterproofing properties"],
              notes=["Apply to clean, dry surfaces and press the lap down firmly with a roller."],
              tds=TD("fg", "2bf2b6931144a786a00526d33475b092"), sds=SD("64c6a01d34681d75fc5b4eef02f75124")))

add(key="gs-c-lite", title="Gripset C-Lite High Performance Lightweight Tile Adhesive 15kg White", type="Adhesives", cat="adhesive",
    tags=ADH_TAGS + ["C2S2TE", "Lightweight Adhesive", "Flexible Adhesive", "Large Format", "Pool", "Gripset"], ship="bulky", weight=15, price=39.95, sku="GWS149",
    market="TradieCart $44.44 and $40.18 inc GST on two listings; Adheseal $35.19 to $45.47 ex (28 Oct 2026).",
    material="White polymer modified lightweight cement based tile adhesive, C2S2TE to AS ISO 13007", range="Gripset C-Lite, 15kg bag (covers about 6 to 7m² with a 10mm notch)", warranty=GS_WARR,
    images=[("gripset-c-lite.png", "Gripset C-Lite tile adhesive bag")],
    desc=html(["Gripset C-Lite is the commercial grade adhesive in the Gripset tile system: white, non slump, highly flexible and rated C2S2TE, with lightweight polymer technology that gives outstanding coverage from a 15kg bag and reduced shrinkage over early age concrete, screeds and renders. Internal, external and immersed use, including pools, spas and large format tiles.",
               "The adhesive to use straight over Gripset membranes and BRW PFN sheet."],
              uses=["Floor and wall tiling to internal and external areas and wet areas", "Porcelain, vitrified tiles, mosaics and natural stone (not moisture sensitive)", "Pools, spas and water features", "Large format tiles and underfloor heating", "Over Gripset waterproofing membranes"],
              specs=["Classification: C2S2TE (improved strength, highly deformable, reduced slip, extended open time)", "Colour: white", "Bag: 15kg", "Coverage: about 6 to 7m² with a 10mm notched trowel", "Open time 30 minutes; adjustment 40 minutes; pot life 2 hours", "Grout and light foot traffic 24 hours; wet area service 3 to 4 days; immersed 7 days"],
              notes=["Prime porous substrates with Gripset GP and non porous with Gripset OP."] + CEMENT_NOTES[1:],
              tds=TD("clite", "8bbe4840ee440f43f75ff445da3e1401"), sds=SD("9eed779912edc1e16a1aaf35aaa996df")))

add(key="gs-c-mastic", title="Gripset C-Mastic High Strength Polymer Modified Tile Adhesive 20kg White", type="Adhesives", cat="adhesive",
    tags=ADH_TAGS + ["C2S1TE", "Flexible Adhesive", "Large Format", "Gripset"], ship="local", weight=20, price=35.95, sku="GWS154",
    market="TradieCart $37.02 inc GST; Adheseal $35.64 ex (28 Oct 2026).",
    material="White polymer modified cement based tile adhesive, C2S1TE to AS ISO 13007, respirable silica free", range="Gripset C-Mastic, 20kg bag (covers about 7m² with a 10mm notch)", warranty=GS_WARR,
    images=[("gripset-c-mastic.png", "Gripset C-Mastic tile adhesive bag")],
    desc=html(["Gripset C-Mastic is a premium grade, respirable silica free, white polymer modified tile adhesive with excellent mastic characteristics: easy to work, non slump, extended open time and economical coverage, for large format tiles and general wall and floor tiling inside and out, and immersed areas. Rated C2S1TE.",
               "Goes directly over Gripset waterproofing membranes and over early age concrete, render and screed."],
              uses=["Floor and wall tiling to internal and external areas", "Porcelain, vitrified tiles, mosaics and natural stone (not moisture sensitive)", "Large format tiles", "Pools and pool surrounds", "Over Gripset waterproofing membranes"],
              specs=["Classification: C2S1TE (improved strength, deformable, reduced slip, extended open time)", "Colour: white", "Bag: 20kg", "Coverage: about 7m² with a 10mm notched trowel", "Open time 30 minutes; adjustment 40 minutes; pot life 1 hour", "Grout and light foot traffic 24 hours; wet area service 3 days; immersed 7 days", "Respirable silica free"],
              notes=["Prime porous substrates with Gripset GP and non porous with Gripset OP."] + CEMENT_NOTES[1:],
              tds=TD("cmastic", "d9c349f56dce51d8d7c45ba8fb3771bc"), sds=SD("e7b533020ddb64963228dea505be4c06")))

add(key="gs-c-stone", title="Gripset C-Stone Fast Set Moisture Sensitive Stone Adhesive 20kg White", type="Adhesives", cat="adhesive",
    tags=ADH_TAGS + ["C2S1FTE", "Rapid Set", "Stone Adhesive", "Gripset", "price-check"], ship="local", weight=20, price=59.95, sku="GWS155",
    market="TradieCart lists it without a price (28 Oct 2026); priced a little under RLA StoneSet.",
    material="White polymer modified fast set high strength tile adhesive, C2S1FTE to AS ISO 13007", range="Gripset C-Stone, 20kg bag (covers about 5 to 6m² with a 10mm notch)", warranty=GS_WARR,
    images=[("gripset-c-stone.png", "Gripset C-Stone stone adhesive bag")],
    desc=html(["Gripset C-Stone is a white, fast set, high strength polymer modified adhesive for Class A moisture sensitive stone: it sets before residual moisture can stain or discolour the stone, with grouting after 2 hours and foot traffic after 4 to 6. Non slip and non slump, commercial grade and cost effective, it also suits any job that needs a fast turnaround, over green screed, render and early age concrete.",
               "Rated C2S1FTE, for internal, external and immersed areas including pools, spas and underfloor heating."],
              uses=["Marble, limestone and other Class A moisture sensitive stone", "Fast turnaround tiling, domestic and commercial", "Porcelain, vitrified tiles and mosaics", "Pools, spas and water features", "Underfloor heating and over Gripset membranes"],
              specs=["Classification: C2S1FTE (improved strength, deformable, fast setting, reduced slip, extended open time)", "Colour: white", "Bag: 20kg", "Coverage: about 5 to 6m² with a 10mm notched trowel", "Open time 30 minutes; adjustment 35 minutes; pot life 1 hour", "Grout 2 hours; light foot traffic 4 to 6 hours; wet area service 3 to 4 days; immersed 7 days"],
              notes=["Short pot life: mix small batches.", "Prime porous substrates with Gripset GP and non porous with Gripset OP."] + CEMENT_NOTES[1:],
              tds=TD("cstone", "25829d09ac940a6f189eccf8a67873c7"), sds=SD("b773df6ef0d997e902946c529bfb1eb2")))

add(key="gs-c-rubber", title="Gripset C-Rubber Economical Rubber Modified Tile Adhesive 20kg", type="Adhesives", cat="adhesive",
    tags=ADH_TAGS + ["C2TES1", "Flexible Adhesive", "Gripset"], ship="local", weight=20, price=32.95, sku="GWS157",
    market="Adheseal $30.98 ex ($34.08 inc) (28 Oct 2026). Code GWS157 from the printed guide V3 (the PDF V1 misprints it as GWS154).",
    material="Off white rubber modified polymer cement based tile adhesive, C2TES1 to AS ISO 13007, respirable silica free", range="Gripset C-Rubber, 20kg bag (covers about 10 to 12m² with a 10mm notch)", warranty=GS_WARR,
    images=[("gripset-c-rubber.png", "Gripset C-Rubber tile adhesive bag")],
    desc=html(["Gripset C-Rubber is the economical adhesive in the Gripset range: a respirable silica free, flexible, rubber modified off white adhesive with outstanding coverage, 10 to 12m² from a 20kg bag, non slump and with an extended open time. Rated C2TES1 for general internal and external wall and floor tiling, including wet areas, over green screed and render and directly over Gripset membranes.",
               "Fixes porcelain, ceramic and vitrified tiles, mosaics and natural stone that is not moisture sensitive."],
              uses=["General floor and wall tiling to internal and external areas", "Internal and external wet areas", "Porcelain, ceramic and vitrified tiles, mosaics and natural stone (not moisture sensitive)", "Over Gripset waterproofing membranes, green screed and render"],
              specs=["Classification: C2TES1 (improved strength, reduced slip, extended open time, deformable)", "Colour: off white", "Bag: 20kg", "Coverage: about 10 to 12m² with a 10mm notched trowel", "Open time 30 minutes; adjustment 40 minutes; pot life 1 hour", "Grout and light foot traffic 24 hours; wet area service 3 to 4 days", "Respirable silica free"],
              notes=["Prime porous substrates with Gripset GP and non porous with Gripset OP."] + CEMENT_NOTES[1:],
              tds=TD("crubber", "2d58b1ce140ee97eaaea519fe330ec8c"), sds=SD("f5a2396f1e472a6b9340ca6e0ecd782b")))

add(key="gs-b26", title="Gripset B26 Asphalt Crack Filler 15L", type=WP_TYPE, cat="sealant",
    tags=GS_TAGS + ["Pavement Protection", "Bitumen"], ship="local", weight=18, price=197.95, sku="GPP008",
    market="TradieCart $203.50 inc GST; Adheseal $187.64 ex (28 Oct 2026).",
    material="Cold applied flexible bitumen crack sealing compound, solvent free", range="Gripset B26, 15 L pail (1 litre fills about 80m of 2mm x 5mm crack)", warranty=GS_WARR,
    images=[("gripset-b26.png", "Gripset B26 asphalt crack filler pail")],
    desc=html(["Gripset B26 is a cold applied crack sealing compound for asphalt and bitumen roads, car parks, driveways and paths: pour it into the crack, no heating, and it is trafficable in 15 to 20 minutes. Flexible, fast drying, water resistant, non tacky when dry, and a safe alternative to heated, solvent based crack sealers.",
               "Also a bitumen sealing compound for horizontal joints and gaps and a pourable joint filler on bitumen and asphalt surfaces."],
              uses=["Cracks in asphalt driveways, car parks, roads and paths", "Horizontal joints and gaps in bitumen surfaces", "Pourable joint filler on asphalt", "Airfield, footpath and bicycle path maintenance"],
              specs=["Type: cold applied bitumen crack sealer, solvent free, non flammable, non toxic", "Size: 15 L pail", "Coverage: 1 litre fills about 80m of crack at 2mm wide and 5mm deep", "Tack free 10 minutes; trafficable 15 to 20 minutes", "Colour: dark brown wet, black dry"],
              notes=["Clean loose material and dust out of the crack before pouring; fill wide cracks in lifts."],
              tds=TD("b26", "368313870e84094be46adea2dddb8ea7"), sds=SD("1a074f614154f6fee2b934a006161b7b")))

add(key="gs-b09", title="Gripset B09 Asphalt Resurfacer & Rejuvenator 15L", type=WP_TYPE, cat="sealant",
    tags=GS_TAGS + ["Pavement Protection", "Bitumen"], ship="local", weight=18, price=199.95, sku="GPP006",
    market="Adheseal $191.42 ex ($210.56 inc) (28 Oct 2026).",
    material="Cold applied polymer modified bitumen surface treatment, solvent free", range="Gripset B09, 15 L pail (about 1 litre per 2m², two coats)", warranty=GS_WARR,
    images=[("gripset-b09.png", "Gripset B09 asphalt resurfacer pail")],
    desc=html(["Gripset B09 is a cold applied bitumen surface treatment that rejuvenates oxidised, pitted asphalt by replenishing the binder in the top layer, so a grey, tired driveway or car park comes back black and weather protected and lasts years longer. Unique polymer technology gives outstanding adhesion and durability, it is non slip and non tacky when dry, and cement can be added for faster rain resistance.",
               "Solvent free, non toxic and free of dangerous odours."],
              uses=["Resurfacing pitted asphalt driveways, car parks and secondary roads", "Footpaths, bicycle paths and laneways", "Repairing asphalt sports surfaces", "Airfields and maintenance areas"],
              specs=["Type: cold applied polymer modified bitumen coating, solvent free, non flammable, non toxic", "Size: 15 L pail", "Coverage: 1 litre per 2m², two coats for best durability", "Tack free 20 minutes; recoat 30 minutes; weatherproof 4 to 6 hours; traffic 24 hours", "Colour: dark charcoal wet, black dry"],
              notes=["Sweep and wash the asphalt first; apply by squeegee or broom in two thin coats."],
              tds=TD("b09", "03753e4367f3597f97945d39d5b765ab"), sds=SD("3a3aea7a082f8a4d4943c4f24eef394a")))

# SEO: search title (<= 60 chars) and meta description (<= 155 chars, always ends with the Perth line)
SEO = {
    "tilebond-extra": ("RLA TileBond Extra 20kg White Tile Adhesive | ETS Perth", "White cement tile adhesive, C1E, 20kg covers 4 to 5m². Walls, floors, pavers and landscaping."),
    "moreflex": ("RLA MoreFlex 20kg Grey Flexible Tile Adhesive | ETS Perth", "Rubber modified flexible tile adhesive, C1ETS1, grey 20kg covers 8 to 10m². Walls and floors in or out."),
    "tileflex": ("RLA TileFlex 20kg White Flexible Tile Adhesive | ETS Perth", "Premium rubber modified white tile adhesive, C2TES1, non slump for large format tiles. 20kg covers 7 to 8m²."),
    "addflextra": ("RLA AddFlextra 20kg White Tile Adhesive C2TES1 | ETS Perth", "Rubber modified white tile adhesive, C2TES1, 20kg covers 10 to 12m². Large format and tile over tile."),
    "trade-mastik": ("RLA Trade Mastik 20kg White Tile Adhesive | ETS Perth", "Smooth white polymer modified tile adhesive, C1TES1, flexible and non slump. 20kg bag covers about 7m²."),
    "mastik": ("RLA Mastik 20kg Tile Adhesive White or Grey | ETS Perth", "Green Tag, silica free flexible tile adhesive, C2TES1. White or grey 20kg covers 7m². Large format tiles."),
    "unilite-s1": ("RLA UniLite S1 12.5kg Lightweight Tile Adhesive | ETS Perth", "Lightweight flexible tile adhesive, C2TES1, silica free. 12.5kg goes as far as a 20kg bag. White or grey."),
    "unilite-s2": ("RLA UniLite S2 12.5kg Tile Adhesive C2TES2 | ETS Perth", "Lightweight highly deformable tile adhesive, C2TES2, silica free. Large format, timber floors, pools. 12.5kg."),
    "unigrip": ("RLA UniGrip 15kg White Tile Adhesive C2S2ET | ETS Perth", "Premium highly flexible white tile adhesive, C2S2ET. Porcelain, large format, tile over tile, pools. 15kg."),
    "fastset": ("RLA FastSet 20kg Rapid Set Tile Adhesive | ETS Perth", "Rapid setting grey tile adhesive, C2S1FTE: grout in 3 hours, walk on in 6. Non slump, over green screeds. 20kg."),
    "stoneset": ("RLA StoneSet 20kg Rapid Set Stone Adhesive | ETS Perth", "Rapid setting white adhesive for moisture sensitive stone and marble, C2S1FTE: grout in 2 hours. 20kg bag."),
    "polymastic": ("RLA PolyMastic Pre-Mixed Wall Tile Adhesive | ETS Perth", "Ready to use white acrylic wall tile adhesive, D1E, non slump for large wall tiles and mosaics. 4 L or 15 L."),
    "wpu": ("RLA WPU Class III Waterproofing Membrane | ETS Perth", "Class III polyurethane/acrylic waterproofing membrane for bathrooms, balconies, decks and roofs. 4 L or 15 L."),
    "wpm": ("RLA WPM Class III Wet Area Membrane 15L | ETS Perth", "Waterborne flexible under tile membrane, Class III to AS 4858, for showers, bathrooms and laundries. 15 L."),
    "safe2o": ("RLA Safe2o Solvent Free SMP Membrane 15kg | ETS Perth", "One part moisture cured SMP waterproofing membrane: solvent free, one coat on floors, Class III. 15kg pail."),
    "2part": ("RLA 2Part Cementitious Membrane Kit 40kg | ETS Perth", "Two part cementitious acrylic waterproofing membrane for pools, balconies and wet areas. 20 L + 20kg kit, 16m²."),
    "1komponent": ("RLA 1Komponent Cementitious Membrane 20kg | ETS Perth", "One part fibre reinforced cementitious membrane: positive and negative pressure, pools and wet areas. 20kg."),
    "pu850": ("RLA PU850 Polyurethane Membrane 15L Grey | ETS Perth", "One part moisture cured polyurethane membrane, Class III: retaining walls, planters, balconies, roofs. 15 L."),
    "atc": ("RLA ATC Aliphatic Top Coat for PU850 15L | ETS Perth", "Transparent aliphatic polyurethane top coat: UV protection for exposed RLA PU850 membrane on roofs and decks."),
    "moisture-seal": ("RLA Moisture Seal Epoxy Vapour Barrier Kit | ETS Perth", "Two part water based epoxy vapour barrier under membranes, tiles, vinyl and timber floors. 8 L or 20 L kit."),
    "primer-pu": ("RLA Primer PU Penetrating Primer 15L | ETS Perth", "Single pack penetrating primer for RLA PU850 membrane and polyurethane sealants. Concrete, render, FC sheet."),
    "max-smp-25": ("RLA Max SMP 25 Adhesive Sealant | ETS Perth", "Solvent and isocyanate free hybrid adhesive sealant: bonds to damp surfaces, paintable, ±25% movement."),
    "wp-tape": ("RLA Waterproof Tape 100mm & 200mm x 50m | ETS Perth", "Polyester reinforcing fabric for RLA membranes at junctions, bond breakers and cracks. 100 or 200mm x 50m."),
    "wp-ext-corner": ("RLA Waterproofing External Corners Box of 25 | ETS Perth", "Pre-formed rubber external corners seal waterproofing membranes at hob and step corners. Box of 25."),
    "wp-int-corner": ("RLA Waterproofing Internal Corners Box of 25 | ETS Perth", "Pre-formed rubber internal corners seal waterproofing membranes at shower and wet area corners. Box of 25."),
    "wp-collar": ("RLA Waterproofing Pipe Collars Box of 25 | ETS Perth", "Rubber collars seal waterproofing membranes around pipes, drains and fixtures. Can be cut on site. Box of 25."),
    "luminous-ef": ("RLA Luminous EF Coloured Grout 4kg, 16 Colours | ETS Perth", "Rapid set efflorescence free tile grout, silica free, joints to 20mm, pools. 16 colours, 4kg bag."),
    "luminous-ssg": ("RLA Luminous SSG Smooth Grout 4kg & 10kg | ETS Perth", "High performance smooth tile grout, water and mould resistant, joints 1.5 to 15mm. 12 colours, 4kg or 10kg."),
    "luminous-silicone": ("RLA Luminous Silicone 300ml Grout Matched | ETS Perth", "Neutral cure mould resistant wet area silicone colour matched to Luminous grout. 13 colours, 300ml cartridge."),
    "epoxy-grout": ("RLA Epoxy Grout 5kg Kit, 4 Colours | ETS Perth", "Two part anti-acid epoxy grout: stain proof, no efflorescence, chemical resistant, joints 1 to 15mm. 5kg kit."),
    "once-over": ("RLA The Once Over Grout Cleaner 1L | ETS Perth", "Mild acidic grout cleaner lifts stains and haze on new tiling and revives old grout colour. All grouts, 1 L."),
    "porous-primer": ("RLA Porous Primer 5L & 20L Tiling Primer | ETS Perth", "Water based acrylic primer for concrete, FC sheet, render and plasterboard before RLA adhesives. Dries fast."),
    "non-porous-primer": ("RLA Non-Porous Primer 5L & 20L Tile Over Tile | ETS Perth", "Rapid drying water based primer for tiling over existing tiles, paint, vinyl and sealed concrete. 5 L or 20 L."),
    "plastinex": ("RLA Plastinex Flexible Additive 5L & 20L | ETS Perth", "High solids acrylic additive: adds flex, adhesion and water resistance to RLA adhesives, grouts and screeds."),
    "silikon-700": ("RLA Silikon 700 Wet Area Silicone 300g | ETS Perth", "Professional 100% neutral cure antifungal silicone for showers, baths, basins and kitchens. 14 colours, 300g."),
    "silikon-100": ("RLA Silikon 100 Neutral Cure Silicone 310g | ETS Perth", "100% neutral cure silicone for glazing, roofing, guttering, plumbing and water tanks (AS 4020). 13 colours."),
    "silikon-200": ("RLA Silikon 200 Acetic Cure RTV Silicone 310g | ETS Perth", "High strength 100% acetic cure RTV silicone for glazing, aquariums, cool rooms and gaskets. Translucent, 310g."),
    "silikon-300": ("RLA Silikon 300 Matte Neutral Cure Silicone | ETS Perth", "Extra high strength neutral cure silicone with a low gloss matte finish for glazing and weather sealing. 310g."),
    "silikon-400": ("RLA Silikon 400LM Low Modulus Matte Silicone | ETS Perth", "Low modulus matte silicone for cladding, glazing, facades and solar panels, ±50% movement. 400g or 600ml."),
    "silikon-600": ("RLA Silikon 600 Fast Cure Silicone 310g | ETS Perth", "Fast curing high strength neutral silicone adhesive sealant, 2 to 5 minute skin, no slump. 4 colours, 310g."),
    "roof-gutter": ("RLA Roof & Gutter Silicone 300ml | ETS Perth", "Neutral cure silicone for metal roofing, Colorbond, gutters and flashings. 4 colours, 10 year warranty."),
    "wet-area": ("RLA Wet Area Silicone 300ml Antifungal | ETS Perth", "Antifungal neutral cure silicone for baths, basins, showers, sinks, tiles and frames. 10 year warranty, 300ml."),
    "gap-filler": ("RLA Gap Filler Acrylic Sealant 300ml White | ETS Perth", "Acrylic caulk for cracks and joints around doors, windows, cornices, skirting and sinks. Paintable, 300ml."),
    "ultragrip": ("RLA UltraGrip Construction Adhesive | ETS Perth", "Synthetic rubber construction adhesive for wall panels, flooring sheets, timber and studs. 300ml or 850ml."),
    "flex-pro-pu": ("RLA Flex-Pro PU Polyurethane Sealant 600ml | ETS Perth", "One part low modulus polyurethane construction joint sealant and adhesive, ±25% movement, paintable. 600ml."),
    "flex-pro-50fc": ("RLA Flex-Pro 50FC Fast Cure PU Sealant 600ml | ETS Perth", "Fast curing polyurethane sealant and adhesive for concrete, tilt panels, stone and trafficable joints. 600ml."),
    "flex-pro-ms": ("RLA Flex-Pro MS Hybrid Sealant 600ml Grey | ETS Perth", "MS polymer sealant and adhesive: solvent and isocyanate free, non staining, bond breaker for RLA membranes."),
    "flex-pro-ms-hd": ("RLA Flex-Pro MS-HD Hybrid Sealant 600ml | ETS Perth", "High modulus MS polymer sealant adhesive with high green strength for vibration and movement. 600ml, 3 colours."),
    "firepro-fr": ("RLA FirePro FR Fire Rated Sealant 600ml | ETS Perth", "Intumescent acrylic sealant, 4 hour fire rating to AS 1530.4 and AS 4072.1, for joints and penetrations. 600ml."),
    "max-smp-crystal": ("RLA Max SMP Crystal Clear Sealant 310g | ETS Perth", "Clear flexible adhesive sealant for glass shower screens, frames and interior joints. Odourless, paintable."),
    "max-grab": ("RLA Max Grab SMP Instant Grab Adhesive 440g | ETS Perth", "Instant grab high strength flexible adhesive sealant: bonds heavy items vertically without clamps. 440g."),
    "caulking-gun": ("RLA Heavy Duty Skeleton Caulking Gun | ETS Perth", "Steel skeleton caulking gun with rotating barrel for silicone and adhesive cartridges. 300ml or 850ml size."),
    "acoustic-dry": ("RLA Dry Area Acoustic Mat Adhesive 15L | ETS Perth", "Water based, solvent free adhesive for direct sticking approved acoustic mats to internal concrete. 15 L."),
    "acoustic-wet": ("RLA Wet Area Acoustic Mat Adhesive 10L | ETS Perth", "Flexible SMP adhesive for acoustic mats, engineered timber and parquet in showers and balconies. 10 L pail."),
    "gs-e60": ("Gripset E60 Water Based Epoxy Primer Kit | ETS Perth", "Two part water based epoxy primer and moisture barrier over damp or green concrete. 4 L, 10 L or 20 L kit."),
    "gs-gp": ("Gripset GP General Purpose Primer 5L & 15L | ETS Perth", "Water based primer for porous concrete, render, FC sheet and plasterboard before Gripset membranes. 5 or 15 L."),
    "gs-op": ("Gripset OP Non-Porous Surface Primer 1L to 15L | ETS Perth", "Solvent free primer for metal, tiles, dense concrete, Scyon and PVC flanges before membranes. 1 L, 5 L, 15 L."),
    "gs-11y": ("Gripset 11Y Latex Waterproof Additive 5L & 15L | ETS Perth", "Concentrated SBR latex additive for screeds, renders and mortars, and a slurry primer under C-Bed. 5 L or 15 L."),
    "gs-b50": ("Gripset Elastoproof B50 Joint Band 10m & 50m | ETS Perth", "Rubber bond breaker joint band for wall/floor junctions and movement joints under Gripset membranes. 120mm."),
    "gs-corners": ("Gripset Elastoproof Corners CN90 & CN270 | ETS Perth", "Prefabricated rubber internal and external corners for the Elastoproof bond breaker system. Sold each."),
    "gs-collars": ("Gripset Elastoproof Base Collars Packs S, M & L | ETS Perth", "Rubber flange seals for taps, floor wastes and pipes up to 150mm under waterproofing membranes. Packs of 10."),
    "gs-brw-pf-tape": ("Gripset BRW PF Tape 80mm & 150mm x 10m | ETS Perth", "Self adhesive butyl sealing tape, fabric faced: instant bond breaker and flange seal under Gripset membranes."),
    "gs-brw-pf-square": ("Gripset BRW PF Square 250mm Flange Seal | ETS Perth", "Self adhesive butyl square for fast sealing of puddle flanges and floor wastes before membrane. 250 x 250mm."),
    "gs-38fc": ("Gripset 38FC Fast Cure Membrane 5L & 15L | ETS Perth", "Fibre reinforced SBR wet area membrane: recoat 1 hour, tile 4 hours, flood test 24. AS 4858, AS 4654.1. Blue."),
    "gs-p39": ("Gripset P39 Polyurethane Hybrid Membrane 15L | ETS Perth", "Solvent free hybrid polyurethane membrane for exposed roofs, decks and under tile wet areas. AS 4858/4654.1."),
    "gs-ls": ("Gripset LS External Trafficable Top Coat 15L | ETS Perth", "Hard wearing non slip UV top coat over Gripset 38FC, P39 and Xpress membranes on roofs, decks and walkways."),
    "gs-51": ("Gripset 51 Bitumen Rubber Membrane 5L & 15L | ETS Perth", "Solvent free bitumen rubber membrane for retaining walls, basements, planters, gutters, timber and metal."),
    "gs-xpress-h2o": ("Gripset Xpress Primer H2O Plus 10L | ETS Perth", "One component vapour barrier primer over damp and green concrete; finishes in 1 hour, colour change when ready."),
    "gs-xpress-multi-pro": ("Gripset Xpress Multi Pro Membrane 15L | ETS Perth", "Fast cure water based elastomeric membrane for exposed and under tile areas, rain resistant in 3 hours. 15 L."),
    "gs-xpresslay": ("Gripset XpressLay Self-Adhesive Sheet 1.3 x 10m | ETS Perth", "Self adhesive waterproof, anti-fracture and decoupling PVC sheet for under tile floors. Cold lay, 13m² roll."),
    "gs-2p": ("Gripset 2P Cementitious Membrane Kit 10L + 15kg | ETS Perth", "Two part latex cementitious membrane for wet areas, balconies, pools and tanks. Fast curing. AS 4858, AS 4654."),
    "gs-c-1p": ("Gripset C-1P One Part Cementitious Membrane 15kg | ETS Perth", "One part fibre reinforced cementitious membrane: positive and negative pressure, pools, basements, wet areas."),
    "gs-c-bed": ("Gripset C-Bed Engineered Screed 20kg | ETS Perth", "Pre-blended polymer modified screed, 5 to 200mm, foot traffic 8 hours, tile in 24. Internal and external. 20kg."),
    "gs-c-level": ("Gripset C-Level Fast Set Self Leveller 20kg | ETS Perth", "Rapid drying fibre reinforced self levelling compound, 3 to 30mm, over 40 MPa, concrete and timber floors."),
    "gs-c-plug": ("Gripset C-Plug Rapid Set Water Plug 4kg & 15kg | ETS Perth", "Non shrink cement plug that stops active water leaks in 1 to 3 minutes. Basements, tanks, pipes. 4kg or 15kg."),
    "gs-hd-tape": ("Gripset Butyl HD Tape 150mm x 10m | ETS Perth", "Self adhesive HDPE faced butyl tape, the bond breaker and detailing tape for the BRW HD sheet membrane."),
    "gs-brw-hd": ("Gripset BRW HD Butyl Sheet Membrane 1m x 10m | ETS Perth", "Self adhesive HDPE reinforced butyl rubber sheet for retaining walls, planters and roof gardens. 10m² roll."),
    "gs-brw-pfn": ("Gripset BRW PFN Butyl Sheet Membrane 1m x 10m | ETS Perth", "Self adhesive fabric faced butyl sheet membrane to tile straight over, anti-fracture. AS 4858, AS 4654. 10m²."),
    "gs-fg-tape": ("Gripset BRW FG Sealing Tape 50mm x 15m | ETS Perth", "Double sided fibreglass reinforced butyl tape for BRW HD sheet laps and fixing water stops. 1mm x 50mm x 15m."),
    "gs-c-lite": ("Gripset C-Lite 15kg Tile Adhesive C2S2TE | ETS Perth", "Commercial grade white lightweight tile adhesive, C2S2TE, highly flexible, large format, pools. 15kg bag."),
    "gs-c-mastic": ("Gripset C-Mastic 20kg Tile Adhesive C2S1TE | ETS Perth", "High strength white polymer modified tile adhesive, C2S1TE, silica free, non slump, extended open time. 20kg."),
    "gs-c-stone": ("Gripset C-Stone 20kg Fast Set Stone Adhesive | ETS Perth", "Fast set white adhesive for moisture sensitive stone, C2S1FTE: grout in 2 hours, foot traffic in 4. 20kg."),
    "gs-c-rubber": ("Gripset C-Rubber 20kg Tile Adhesive C2TES1 | ETS Perth", "Economical rubber modified flexible tile adhesive, C2TES1, silica free, 20kg covers 10 to 12m². Walls, floors."),
    "gs-b26": ("Gripset B26 Asphalt Crack Filler 15L | ETS Perth", "Cold applied flexible crack sealer for asphalt driveways, car parks and paths. Trafficable in 20 minutes. 15 L."),
    "gs-b09": ("Gripset B09 Asphalt Resurfacer 15L | ETS Perth", "Cold applied bitumen resurfacer that rejuvenates oxidised asphalt driveways and car parks. Solvent free. 15 L."),
}


# ---------------------------------------------------------------------------------------------------
def build(staged):
    out, rows = [], []
    for p in P:
        if p["key"] in SEALANTS_ONLY and not INCLUDE_SEALANTS_CATALOGUE:
            continue
        options = p.get("options")
        if options:
            variants = p["variants"]
        else:
            options = ["Title"]
            variants = [({"Title": "Default Title"}, p["sku"], p["price"], p["weight"], p["ship"])]
        ships = {v[4] if len(v) > 4 else p["ship"] for v in variants}
        # product level shipping tags: the heaviest class wins for tags; ets.freight_class names the mix
        order = ["parcel", "parcel20", "bulky", "local"]
        heaviest = max(ships, key=order.index)
        ship_tags, freight = SHIP[heaviest]
        if len(ships) > 1:
            freight = " / ".join(SHIP[s][1] for s in sorted(ships, key=order.index)) + " (by size)"
        tags = sorted(set(p["tags"] + ship_tags + ["RLA", "supplier-import", "needs-cost", "rla-2026-10"]))
        pc = p.get("price_check_variants")
        if pc and "price-check" not in tags:
            tags.append("price-check")
        metafields = [
            {"namespace": "ets", "key": "supplier", "type": "single_line_text_field", "value": SUPPLIER},
            {"namespace": "custom", "key": "supplier", "type": "single_line_text_field", "value": SUPPLIER},
            {"namespace": "ets", "key": "material", "type": "single_line_text_field", "value": p["material"]},
            {"namespace": "ets", "key": "range", "type": "single_line_text_field", "value": p["range"]},
            {"namespace": "ets", "key": "warranty", "type": "single_line_text_field", "value": p["warranty"]},
            {"namespace": "ets", "key": "freight_class", "type": "single_line_text_field", "value": freight},
            {"namespace": "ets", "key": "lead_time", "type": "single_line_text_field", "value": "Order in from the supplier: usually 3 to 7 business days to Maddington, Perth"},
            {"namespace": "ets", "key": "trade_band", "type": "number_integer", "value": "0"},
        ]
        vin = []
        for v in variants:
            opt, sku, price, kg = v[0], v[1], v[2], v[3]
            vin.append({"optionValues": [{"optionName": k, "name": val} for k, val in opt.items()],
                        "price": f"{price:.2f}", "inventoryPolicy": "CONTINUE", "taxable": True,
                        "inventoryItem": {"sku": sku, "tracked": True, "measurement": {"weight": {"value": kg, "unit": "KILOGRAMS"}}}})
            rows.append({"product": p["title"], "variant": " / ".join(opt.values()), "sku": sku, "price": f"{price:.2f}",
                         "ship": v[4] if len(v) > 4 else p["ship"], "market": p["market"],
                         "price_check": "yes" if ("price-check" in p["tags"] or (pc and list(opt.values())[0] in pc)) else ""})
        seo_title, seo_desc = SEO[p["key"]]
        seo_desc += PERTH_LINE
        assert len(seo_title) <= 60, (p["key"], len(seo_title))
        assert len(seo_desc) <= 155, (p["key"], len(seo_desc))
        opt_values = {o: [] for o in options}
        for v in variants:
            for k, val in v[0].items():
                if val not in opt_values[k]:
                    opt_values[k].append(val)
        out.append({
            "title": p["title"], "descriptionHtml": p["desc"], "vendor": VENDOR, "productType": p["type"],
            "status": "DRAFT", "category": CAT[p["cat"]], "tags": tags,
            "seo": {"title": seo_title, "description": seo_desc},
            "metafields": metafields,
            "productOptions": [{"name": o, "values": [{"name": v} for v in opt_values[o]]} for o in options],
            "files": [{"originalSource": staged[f], "alt": alt, "contentType": "IMAGE"} for f, alt in p["images"] if f in staged],
            "variants": vin,
        })
    return out, rows


if __name__ == "__main__":
    staged = json.load(open(sys.argv[1])) if len(sys.argv) > 1 and sys.argv[1] != "-" else {}
    products, rows = build(staged)
    if len(sys.argv) > 2:
        json.dump(products, open(sys.argv[2], "w"), indent=1)
    if len(sys.argv) > 3:
        with open(sys.argv[3], "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
    print(f"{len(products)} products, {len(rows)} variants")
    for pr in products:
        prices = sorted({float(v['price']) for v in pr['variants']})
        print(f"{pr['title'][:70]:70} {pr['productType'][:24]:24} {len(pr['variants']):3} var  ${prices[0]:.2f}" + (f"-{prices[-1]:.2f}" if len(prices) > 1 else "") + f"  {len(pr['descriptionHtml'].split())} words  {len(pr['files'])} img")
