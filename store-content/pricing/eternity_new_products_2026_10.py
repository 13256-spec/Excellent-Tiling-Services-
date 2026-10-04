"""New Eternity tiles from the 5 Oct 2026 price list -> Shopify productSet inputs.

Prices follow eternity_2026_10.py: 15% under Eternity's RRP, rounded down to 10c.
Cost = Eternity "non pallet" price ex GST. Photos are Eternity's own product photos where
their shop has the tile, otherwise the swatch from the price list PDF (marked indicative).

Usage: eternity_new_products_2026_10.py et_all.json staged.json out.json
  et_all.json: Eternity's public products.json pages; staged.json: {filename: staged URL}
"""
import json, math, sys

UNDER_RRP = 0.15
DESC_TAIL = {
    "m2": "sold per sqm to the nearest full box.",
    "sheet": "sold per sheet.",
}


def price(rrp):
    return f"{math.floor(rrp * (1 - UNDER_RRP) * 10) / 10:.2f}"


# title, material, tags, unit, weight kg, photo, [(size, finish, sku, rrp, cost)], extra lines
P = "Porcelain"
PRODUCTS = [
    ("Lava Vesuv Porcelain Tile", P, ["Lava", "P3"], "m2", 22, "lava-vesuv-tile.png",
     [("300x600mm", "Matt", "HW637314", 55, 26.5), ("600x600mm", "Matt", "YW607314", 55, 26.5),
      ("300x600mm", "Gloss", "FG637314", 59, 28.5), ("600x600mm", "Gloss", "FG607314", 59, 28.5),
      ("600x1200mm", "Gloss", "YW277314", 75, 36.5)], ["Slip rating: P3 (matt)"]),
    ("Fumosa Porcelain Tile", P, ["Fumosa", "P3"], "m2", 22, "fumosa-tile.png",
     [("600x600mm", "Matt", "ETSN6631", 44, 22), ("600x1200mm", "Matt", "ETSN126631", 59, 29.5)],
     ["Slip rating: P3"]),
    *[(f"{n} Porcelain Tile", P, [n.split()[0], "P4", "Anti-Slip"], "m2", 22,
       f"{n.lower().replace(' ', '-')}-tile.png",
       [("300x600mm", "Matt", f"DSA36{c}", 55, 26.5), ("600x600mm", "Matt", f"DSA66{c}", 55, 26.5)],
       ["Slip rating: P4"])
      for n, c in [("Astra White", "AW"), ("Astra Greige", "AG"), ("Sand White", "SW"),
                   ("Sand Beige", "SB"), ("Sand Grey", "SG"), ("Bianco Greco", "BG")]],
    ("Caliza Porcelain Tile", P, ["Caliza"], "m2", 22, "caliza-tile.png",
     [("300x600mm", "Matt", "YF637300", 59, 28.5)], []),
    ("E-Time Calcare Porcelain Tile", P, ["E-Time", "P4", "Anti-Slip"], "m2", 22,
     "e-time-calcare-tile.png", [("300x600mm", "Structured", "YW633164", 65, 31.5)],
     ["Structured surface", "Slip rating: P4"]),
    ("E-Time Chiaro Porcelain Tile", P, ["E-Time", "P4", "Anti-Slip"], "m2", 22,
     "e-time-chiaro-tile.png", [("300x600mm", "Structured", "YW633165", 65, 31.5)],
     ["Structured surface", "Slip rating: P4"]),
    ("Oak Aube Timber Look Porcelain Tile", P, ["Timber Look", "P3"], "m2", 22,
     "oak-aube-tile.png", [("200x1200mm", "Matt", "HSA223111", 75, 36.5)],
     ["Timber-look plank, 196 x 1200 x 9mm", "Slip rating: P3"]),
    # Ceramic wall and small-format range (photos from Eternity's shop)
    ("Subway Gloss White Ceramic Tile", "Ceramic", ["Subway", "Wall Tile"], "m2", 15,
     "eternity:subway-gloss-white-ceramic-small-format-tile",
     [("100x300mm", "Gloss", "DSA31001G", 44, 22)], ["8mm thick"]),
    ("Subway Matt White Ceramic Tile", "Ceramic", ["Subway", "Wall Tile"], "m2", 15,
     "eternity:subway-matt-white-ceramic-small-format-range-tile",
     [("100x300mm", "Satin", "DSA31002M", 44, 22)], ["8mm thick"]),
    *[(f"Subwave {n} Ceramic Tile", "Ceramic", ["Subwave", "Wall Tile"], "m2", 15, f"eternity:{h}",
       [("75x300mm", f, s, r, c)], ["Wave-profile wall tile, 8mm thick"])
      for n, h, f, s, r, c in [
          ("Gloss White", "subwave-gloss-white-ceramic-small-format-range-tile", "Gloss", "DSA730WAW1", 55, 25),
          ("Matt White", "subwave-matt-white-ceramic-small-format-range-tile", "Satin", "DSA730WAW1M", 55, 25),
          ("Nude", "subwave-nude-ceramic-small-format-range-tile", "Gloss", "DSA730WBC7", 60, 29),
          ("Grey", "subwave-grey-ceramic-small-format-range-tile", "Gloss", "DSA730WBC6", 60, 29)]],
    ("White Ceramic Wall Tile", "Ceramic", ["Wall Tile"], "m2", 15,
     "eternity:gloss-white-ceramic-wall-range-300x600-tile",
     [("300x600mm", "Gloss", "DSA36001", 40, 13.8), ("300x600mm", "Matt", "DSA36002M", 40, 15.8)],
     ["9.5mm thick"]),
    *[(f"{n} Ceramic Wall Tile", "Ceramic", ["Wall Tile"], "m2", 15, f"eternity:{h}",
       [("300x600mm", "Gloss", s, 40, 20)], ["9.5mm thick"])
      for n, h, s in [("Eternal Marble", "eternal-marble-ceramic-wall-range-300x600-tile", "DSA60822"),
                      ("Eternal Carrara", "eternal-carrara-ceramic-wall-range-300x600-tile", "DSA60602"),
                      ("Element Grey", "element-grey-ceramic-wall-range-300x600-tile", "DSA6049"),
                      ("Whisper Grey", "element-whisper-grey-ceramic-wall-range-300x6", "DSA60871")]],
    # Natural stone mosaics, sold per sheet
    *[(f"{n} Mosaic Tile", "Natural stone", ["Mosaic", "Natural Stone"], "sheet", 2, f"{f}-mosaic.png",
       [(size, "Polished", s, r, 11)], [inlay] if inlay else [])
      for n, f, size, s, r, inlay in [
          ("Hex Crystal White", "hex-crystal-white", "305x330mm", "LAY754", 33, "304 stainless steel inlay"),
          ("Hex Black and White Roots", "hex-black-white-roots", "305x330mm", "LAY754-D", 33, "304 stainless steel inlay"),
          ("Arrow Crystal White", "arrow-crystal-white", "300x260mm", "LAY752", 33, "Aluminium inlay"),
          ("Crystal White Black Jade", "crystal-white-black-jade", "170x295mm", "LAY893", 33, "Stainless steel inlay"),
          ("Crystal White Indian Green", "crystal-white-indian-green", "285x235mm", "LAY761-B", 33, "Stainless steel inlay"),
          ("Herringbone Snow Plum", "herringbone-snow-plum", "Sheet", "LAP625-J", 33, ""),
          ("Pools Red Norwegian", "pools-red-norwegian", "295x300mm", "LAY795-F", 38.5, ""),
          ("Pools Snow Plum", "pools-snow-plum", "295x300mm", "LAY795-D", 38.5, "")]],
]


def build(et_all, staged):
    by_handle = {p["handle"]: p for p in et_all}
    out = []
    for title, material, tags, unit, kg, photo, variants, extra in PRODUCTS:
        if photo.startswith("eternity:"):
            src = by_handle[[h for h in by_handle if h.startswith(photo[9:])][0]]["images"][0]["src"]
            alt = title
        else:
            src, alt = staged[photo], f"{title} (indicative swatch)"
        sizes = sorted({v[0] for v in variants}, key=lambda s: [int(x) for x in s[:-2].split("x")] if s != "Sheet" else [0])
        finishes = list(dict.fromkeys(v[1] for v in variants))
        size_tags = [s[:-2] for s in sizes if s != "Sheet"]
        finish_tags = ["Matt" if f == "Satin" else f for f in finishes if f != "Polished"]
        name = title.rsplit(" Porcelain", 1)[0].rsplit(" Ceramic", 1)[0].rsplit(" Mosaic", 1)[0]
        lines = ([f"Available in {', '.join(sizes[:-1]) + ' and ' + sizes[-1] if len(sizes) > 1 else sizes[0]}"]
                 if sizes != ["Sheet"] else [])
        if len(finishes) > 1:
            lines.append(f"{' or '.join(finishes)} finish")
        lines += [f"Material: {material}"] + extra
        desc = (f"<p>{name} {material.lower()} {'mosaic' if unit == 'sheet' else 'tile'}, "
                f"{DESC_TAIL[unit]}</p><ul>\n" + "".join(f"<li>{l}</li>\n" for l in lines) + "</ul>")
        out.append({
            "title": title, "descriptionHtml": desc, "vendor": "Excellent Tiling Services",
            "productType": "Tile", "status": "ACTIVE", "category": "gid://shopify/TaxonomyCategory/ha-2-5",
            "tags": sorted(set(tags + size_tags + finish_tags + [material if material != "Natural stone" else "Natural Stone", "Tile", "trade-5"])),
            "metafields": [{"namespace": "custom", "key": "supplier", "type": "single_line_text_field",
                            "value": "Eternity Tiles"}],
            "productOptions": [{"name": "Size", "values": [{"name": s} for s in sizes]},
                               {"name": "Finish", "values": [{"name": f} for f in finishes]}],
            "files": [{"originalSource": src, "alt": alt, "contentType": "IMAGE"}],
            "variants": [{"optionValues": [{"optionName": "Size", "name": s}, {"optionName": "Finish", "name": f}],
                          "price": price(rrp), "inventoryPolicy": "CONTINUE", "taxable": True,
                          "inventoryItem": {"sku": sku, "cost": str(cost), "tracked": False,
                                            "measurement": {"weight": {"value": kg, "unit": "KILOGRAMS"}}}}
                         for s, f, sku, rrp, cost in variants],
        })
    return out


if __name__ == "__main__":
    rows = build(json.load(open(sys.argv[1])), json.load(open(sys.argv[2])))
    json.dump(rows, open(sys.argv[3], "w"), indent=1)
    for r in rows:
        print(f'{r["title"]:42} {len(r["variants"])} var  {", ".join(v["price"] for v in r["variants"]):30} {" ".join(r["tags"])}')
