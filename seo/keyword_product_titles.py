"""Search titles for MELA bathroom products that include the generic words shoppers type.

Product names like "MELA FLOVA Basin Mixer" only match brand searches. Each SEO title adds
the everyday term for its product type ("Basin Mixer Tap", "Shower Mixer", "Bathroom
Vanity", ...) plus Perth, within Google's ~60 character display limit.

Input: TSV of product id, product type, product title.
Output: seo/keyword-product-titles.json  [{id, title, seo_title}]
"""
import json, re, sys

TITLE_MAX = 60

# Templates tried in order; {t} = product title, {s} = shortened title,
# {w} = title without "Shower/Bath ". First that fits wins.
TEMPLATES = {
    "Basin Mixer": ["{t} Tap | Bathroom Taps Perth", "{t} Tap | Perth"],
    "Wall Mixer": ["{t} | Shower Mixer Tap Perth", "{t} | Shower Mixer Perth"],
    "Wall Mixer with Diverter": ["{w} | Shower Mixer Perth"],
    "Kitchen Sink Mixer": ["{t} Tap | Kitchen Taps Perth", "{t} | Kitchen Tap Perth"],
    "Wall Spout": ["{t} | Bath & Basin Tap Perth", "{t} | Bath Tap Perth"],
    "Bath Spout": ["{t} | Bath Tap Perth"],
    "Freestanding Bath Spout": ["{t} | Bath Tap Perth"],
    "Freestanding Bath Mixer": ["{t} | Bath Tap Perth"],
    "Shower Head": ["{t} | Overhead Shower Perth", "{t} | Showers Perth"],
    "Shower Arm": ["{t} | Shower Head Arm Perth", "{t} | Showers Perth"],
    "Ceiling Shower Arm": ["{t} | Shower Head Arm Perth", "{t} | Showers Perth"],
    "Hand Shower Set": ["{t} | Showers Perth", "{s} | Shower Rail Set Perth"],
    "Combination Shower Set": ["{t} | Perth", "{s} | Perth"],
    "Wall Hung Vanity": ["{t} | Bathroom Vanity Perth", "{s} | Wall Hung Vanity Perth",
                         "{s} | Bathroom Vanity Perth"],
    "Double Wall Hung Vanity": ["{t} | Double Basin Perth", "{s} | Double Basin Vanity Perth",
                                "{s} | Wall Hung Perth"],
    "Bathroom Tallboy": ["{t} | Bathroom Storage Perth"],
    "Towel Rail": ["{t} | Bathroom Towel Rails Perth", "{t} | Towel Rails Perth"],
    "Hand Towel Rail": ["{t} | Bathroom Towel Rails Perth", "{t} | Towel Rails Perth"],
    "Bath Towel Shelf": ["{t} | Towel Rack Perth"],
    "Toilet Roll Holder": ["{t} | Toilet Roll Holder Perth"],
    "Bathroom Hook": ["{t} | Robe & Towel Hook Perth"],
    "Soap Holder": ["{t} | Bathroom Accessories Perth", "{t} | Shower Shelf Perth"],
    "Shelf Holder": ["{t} | Bathroom Shelf Perth"],
    "Toilet Brush Holder": ["{t} | Bathroom Accessories Perth", "{t} | Perth"],
    "Pop Up Waste": ["{t} | Basin Plug Waste Perth"],
    "Freestanding Bath": ["{t} | Freestanding Bathtub Perth", "{t} | Bathtub Perth"],
    "Back to Wall Bath": ["{t} | Bathtub Perth"],
    "Corner Bath": ["{t} | Bathtub Perth"],
    "Inset Bath": ["{t} | Built-in Bathtub Perth", "{t} | Bathtub Perth"],
    "Kitchen Sink": ["{t} | Kitchen & Laundry Sink Perth", "{t} | Kitchen Sink Perth"],
    "Toilet Suite": ["{t} | Toilets Perth", "{t} | Perth"],
    "In Wall Cistern Toilet": ["{t} | Perth", "{s} | Perth"],
    "Frameless Shower Panel": ["{t} | Shower Screen Perth"],
    "Corner Shower Screen": ["{t} | Perth"],
    "Shower Screen Fitting": ["{t} | Perth"],
    "Mirror": ["{t} | Bathroom Mirror Perth"],
    "LED Mirror": ["{t} | Bathroom Mirror Perth", "{t} | Demister Perth"],
    "Mirror Cabinet": ["{t} | Shaving Cabinet Perth"],
    "Above Counter Basin": ["{t} | Bathroom Basin Perth"],
    "Half Inset Basin": ["{t} | Bathroom Basin Perth"],
    "Semi Basin": ["{t} | Semi-Recessed Basin Perth"],
    "Undermount Basin": ["{t} | Bathroom Basin Perth"],
    "Inset Basin": ["{t} | Bathroom Basin Perth"],
}


def shorten(t):
    s = t.replace("Shower/Bath ", "").replace(" without Rail", ", No Rail")
    s = s.replace("Double Wall Hung Vanity", "Double Vanity").replace("Wall Hung Vanity", "Vanity")
    s = s.replace("Matt White ", "").replace("Single Side Shelves", "Single Shelf").replace(" Side Shelves", " Shelves").replace(" Centre Shelves", " Shelves")
    s = s.replace("Wall Faced Rimless Toilet Suite", "Wall Faced Rimless Toilet")
    return re.sub(r"\s+with\s+", ", ", s)


OVERRIDES = {
    "MELA BRITTANY 1200 Oak Fluted Curved Wall Hung Vanity with 2 Drawers":
        "MELA BRITTANY 1200 Oak Fluted Vanity, 2 Drawers | Perth",
}


def seo_title(t, ptype):
    if t in OVERRIDES:
        return OVERRIDES[t]
    s, w = shorten(t), t.replace("Shower/Bath ", "")
    for tpl in TEMPLATES.get(ptype, []) + ["{t} | Perth", "{s} | Perth"]:
        out = tpl.format(t=t, s=s, w=w)
        if len(out) <= TITLE_MAX:
            return out
    return s[:TITLE_MAX].rsplit(" ", 1)[0]


def main(tsv, out):
    rows = []
    for line in open(tsv):
        pid, ptype, title = line.rstrip("\n").split("\t")
        rows.append({"id": f"gid://shopify/Product/{pid}", "title": title,
                     "seo_title": seo_title(title, ptype)})
    json.dump(rows, open(out, "w"), indent=1, ensure_ascii=False)
    return rows


if __name__ == "__main__":
    for r in main(sys.argv[1], sys.argv[2]):
        print(len(r["seo_title"]), r["seo_title"])
