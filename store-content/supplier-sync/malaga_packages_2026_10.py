"""Malaga all-in-one vanity packages (Eternity "Wholesale Vanity Package Pricing 2025") -> Shopify productSet inputs.

Two products, priced at Eternity's RRP inc GST (owner, 14 Oct 2026: sell at Eternity's price until costs are agreed):
- China top package: vanity + ceramic top with integrated basin + low basin mixer + pop-up waste. 750/900/1200mm.
- Stone top package: vanity + 20mm polished stone top (White Burst or Blanco Bliss) + above-counter basin
  (rectangular or round) + tall basin mixer + pop-up waste. 750/900/1200mm single, 1500/1800mm double.
Colours: Matt White, Antico Oak, Dark Oak (the Malaga cabinet already in the store).
Wholesale tiers on the sheet: account 45% off RRP, COD / 5-buy account 50%, 5-buy COD 55%. Cost is recorded once
the owner says which tier applies.

Usage: malaga_packages_2026_10.py out.json
"""
import json, sys

STAGED = "https://shopify-staged-uploads.storage.googleapis.com/tmp/68302929983/files/"
IMG = {
    "china-top": STAGED + "31f23a4a-5660-49b2-9e7f-7042fd975c19/malaga-package-china-top.png",
    "low-mixer": STAGED + "db91df30-77f6-47da-b3fb-eb85a5a0680c/malaga-package-low-mixer-waste.png",
    "tall-mixer": STAGED + "ad0872e0-8dd1-42d3-a176-8b5a4bc04756/malaga-package-tall-mixer.png",
    "pop-up-waste": STAGED + "133ebce5-0dc0-4bfb-9d28-d9ffaf9dbae8/malaga-package-pop-up-waste.png",
    "white-burst": STAGED + "69f7e61a-d0ad-4e66-92b2-853e62c13f9c/malaga-package-stone-white-burst.png",
    "blanco-bliss": STAGED + "0099b7c5-35be-472d-ac16-f340285ba06b/malaga-package-stone-blanco-bliss.png",
    "basin-rect": STAGED + "deb8031b-8c8d-4219-a899-aec936efa404/malaga-package-basin-rectangle.png",
    "basin-round": STAGED + "00c39cfe-502e-4aca-b6ed-1dab542698bf/malaga-package-basin-round.png",
}
CDN = "https://cdn.shopify.com/s/files/1/0827/3235/1706/files/"  # Eternity's own Malaga cabinet photos
VANITY = {"Matt White": CDN + "ETOJS106-1200W.png", "Antico Oak": CDN + "ETOJS106-1200AO.png",
          "Dark Oak": CDN + "ETOJS106750DO-1_1_e5c6af31-a27a-4d8f-8b12-ed23eff13c59.jpg"}
CODE = {"Matt White": "W", "Antico Oak": "AO", "Dark Oak": "DO"}
COLOURS = list(CODE)
CABINET = {"750mm": "740 x 630 x 455mm", "900mm": "890 x 630 x 455mm", "1200mm": "1190 x 630 x 455mm",
           "1500mm": "1490 x 630 x 455mm", "1800mm": "1790 x 630 x 455mm"}

PACKAGES = [
    ("Malaga All-in-One Vanity Package with China Top", "CT",
     {"750mm": 1215, "900mm": 1525, "1200mm": 1935},
     "<p>Everything for a finished vanity in one box: the Malaga wall hung vanity, a ceramic top with built-in basin, "
     "a chrome basin mixer and a pop-up waste. Single basin.</p><ul>"
     "<li>Vanity: Malaga wall hung cabinet with finger-pull doors and drawers, 630mm high, 455mm deep</li>"
     "<li>Top: gloss white ceramic top with integrated basin, one tap hole</li>"
     "<li>Tapware: chrome low basin mixer and chrome pop-up waste</li>"
     "<li>Sizes: 750mm, 900mm and 1200mm wide</li>"
     "<li>Colours: Matt White, Antico Oak melamine, Dark Oak melamine</li></ul>",
     ["china-top", "low-mixer", "pop-up-waste"]),
    ("Malaga All-in-One Vanity Package with Stone Top", "ST",
     {"750mm": 1478, "900mm": 1718, "1200mm": 2118, "1500mm": 2848, "1800mm": 3358},
     "<p>Everything for a finished vanity in one box: the Malaga wall hung vanity, a 20mm polished stone top, an "
     "above-counter basin, a chrome tall basin mixer and a pop-up waste. 750, 900 and 1200mm have one basin; "
     "1500 and 1800mm have two basins, two mixers and two wastes.</p><ul>"
     "<li>Vanity: Malaga wall hung cabinet with finger-pull doors and drawers, 630mm high, 455mm deep</li>"
     "<li>Stone top: 20mm polished, in White Burst or Blanco Bliss</li>"
     "<li>Basin: gloss white above-counter basin, rectangular or round</li>"
     "<li>Tapware: chrome tall basin mixer and chrome pop-up waste</li>"
     "<li>Sizes: 750, 900 and 1200mm (single basin), 1500 and 1800mm (double basin)</li>"
     "<li>Colours: Matt White, Antico Oak melamine, Dark Oak melamine</li></ul>"
     "<p>Tell us your stone colour and basin shape in the order notes at checkout, or we will call to confirm before "
     "it is ordered in.</p>",
     ["white-burst", "blanco-bliss", "basin-rect", "basin-round", "tall-mixer", "pop-up-waste"]),
]


def build():
    out = []
    for title, code, prices, desc, imgs in PACKAGES:
        sizes = list(prices)
        files = [{"originalSource": VANITY[c], "alt": f"{title}, {c}", "contentType": "IMAGE"} for c in COLOURS]
        files += [{"originalSource": IMG[i], "alt": f"{title}: {i.replace('-', ' ')}", "contentType": "IMAGE"} for i in imgs]
        out.append({
            "title": title, "descriptionHtml": desc, "vendor": "Excellent Tiling Services",
            "productType": "Wall Hung Vanity", "status": "ACTIVE",
            "category": "gid://shopify/TaxonomyCategory/fr-4-14-1",
            "tags": sorted(set(COLOURS + sizes + ["Malaga", "Vanity Package", "Bathroom Vanity", "Wall Hung Vanity",
                                                  "ship-local-only", "supplier-import", "needs-cost"])),
            "metafields": [{"namespace": "custom", "key": "supplier", "type": "single_line_text_field", "value": "Eternity Tiles"}],
            "productOptions": [{"name": "Colour", "values": [{"name": c} for c in COLOURS]},
                               {"name": "Size", "values": [{"name": s} for s in sizes]}],
            "files": files,
            "variants": [{"optionValues": [{"optionName": "Colour", "name": c}, {"optionName": "Size", "name": s}],
                          "price": f"{prices[s]:.2f}", "inventoryPolicy": "CONTINUE", "taxable": True,
                          "inventoryItem": {"sku": f"ETPKG-{code}-{s[:-2]}-{CODE[c]}", "tracked": False}}
                         for c in COLOURS for s in sizes],
        })
    return out


if __name__ == "__main__":
    rows = build()
    json.dump(rows, open(sys.argv[1], "w"), indent=1)
    for r in rows:
        print(r["title"], len(r["variants"]), "variants", [v["price"] for v in r["variants"][:5]])
