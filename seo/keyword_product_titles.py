"""Search titles and descriptions for MELA bathroom products, aimed at shoppers Australia-wide.

Product names like "MELA FLOVA Basin Mixer" only match brand searches. Each SEO title adds
the everyday term for its product type ("Basin Mixer Tap", "Shower Mixer", "Bathroom
Vanity", ...) within Google's ~60 character display limit. Titles carry no city, so the
store isn't pinned to Perth.

Each description keeps the product facts from seo/product-seo.json and ends with how that
product type is delivered, per the shipping policy (store-content/policies/shipping-policy.html):
small items ship Australia-wide, bulky parcels go by Australia Post, and
large items are delivered in Perth with freight quoted elsewhere.

Usage: keyword_product_titles.py products.tsv product-seo.json out.json
  products.tsv: product id, product type, product title (tab separated)
"""
import json, re, sys

TITLE_MAX, DESC_MAX = 60, 155

# Templates tried in order; {t} = product title, {s} = shortened title,
# {w} = title without "Shower/Bath ". First that fits wins.
TEMPLATES = {
    "Basin Mixer": ["{t} Tap | Bathroom Taps | ETS", "{t} Tap | Bathroom Taps", "{t} Tap | ETS"],
    "Wall Mixer": ["{t} | Shower Mixer Tap | ETS", "{t} | Shower Mixer Tap", "{t} | Shower Mixer"],
    "Wall Mixer with Diverter": ["{w} | Shower Mixer | ETS", "{w} | Shower Mixer"],
    "Kitchen Sink Mixer": ["{t} Tap | Kitchen Taps | ETS", "{t} Tap | Kitchen Taps", "{t} | Kitchen Tap"],
    "Wall Spout": ["{t} | Bath & Basin Tap | ETS", "{t} | Bath & Basin Tap"],
    "Bath Spout": ["{t} | Bath Tap | ETS", "{t} | Bath Tap"],
    "Freestanding Bath Spout": ["{t} | Bath Tap | ETS", "{t} | Bath Tap"],
    "Freestanding Bath Mixer": ["{t} | Bath Tap | ETS", "{t} | Bath Tap"],
    "Shower Head": ["{t} | Overhead Shower | ETS", "{t} | Overhead Shower"],
    "Shower Arm": ["{t} | Shower Head Arm | ETS", "{t} | Shower Head Arm", "{t} | Showers"],
    "Ceiling Shower Arm": ["{t} | Shower Head Arm", "{t} | Showers"],
    "Hand Shower Set": ["{t} | Showers | ETS", "{t} | Showers"],
    "Combination Shower Set": ["{t} | Twin Shower", "{s} | Twin Shower"],
    "Wall Hung Vanity": ["{t} | Bathroom Vanity", "{s} | Wall Hung Vanity",
                         "{s} | Bathroom Vanity"],
    "Double Wall Hung Vanity": ["{t} | Double Basin", "{s} | Double Basin Vanity",
                                "{s} | Wall Hung"],
    "Bathroom Tallboy": ["{t} | Bathroom Storage"],
    "Towel Rail": ["{t} | Bathroom Towel Rails", "{t} | Towel Rails"],
    "Hand Towel Rail": ["{t} | Bathroom Towel Rails", "{t} | Towel Rails"],
    "Bath Towel Shelf": ["{t} | Towel Rack | ETS"],
    "Toilet Roll Holder": ["{t} | Toilet Roll Holder"],
    "Bathroom Hook": ["{t} | Robe & Towel Hook | ETS", "{t} | Robe & Towel Hook"],
    "Soap Holder": ["{t} | Bathroom Accessories", "{t} | Shower Shelf"],
    "Shelf Holder": ["{t} | Bathroom Shelf | ETS", "{t} | Bathroom Shelf"],
    "Toilet Brush Holder": ["{t} | Bathroom Accessories"],
    "Pop Up Waste": ["{t} | Basin Plug Waste | ETS", "{t} | Basin Plug Waste"],
    "Freestanding Bath": ["{t} | Freestanding Bathtub", "{t} | Bathtub"],
    "Back to Wall Bath": ["{t} | Bathtub | ETS"],
    "Corner Bath": ["{t} | Bathtub | ETS"],
    "Inset Bath": ["{t} | Built-in Bathtub | ETS", "{t} | Bathtub"],
    "Kitchen Sink": ["{t} | Kitchen & Laundry Sink", "{t} | Kitchen Sink"],
    "Toilet Suite": ["{t} | Toilets | ETS", "{t} | Toilets"],
    "Frameless Shower Panel": ["{t} | Shower Screen"],
    "Mirror": ["{t} | Bathroom Mirror | ETS", "{t} | Bathroom Mirror"],
    "LED Mirror": ["{t} | Bathroom Mirror | ETS", "{t} | Bathroom Mirror"],
    "Mirror Cabinet": ["{t} | Shaving Cabinet | ETS", "{t} | Shaving Cabinet"],
    "Above Counter Basin": ["{t} | Bathroom Basin", "{t} | Basin"],
    "Half Inset Basin": ["{t} | Bathroom Basin | ETS"],
    "Semi Basin": ["{t} | Semi-Recessed Basin"],
    "Undermount Basin": ["{t} | Bathroom Basin | ETS"],
    "Inset Basin": ["{t} | Bathroom Basin | ETS"],
}

OVERRIDES = {
    "MELA BRITTANY 1200 Oak Fluted Curved Wall Hung Vanity with 2 Drawers":
        "MELA BRITTANY 1200 Oak Fluted Vanity, 2 Drawers | ETS",
}

# Delivery wording per shipping-policy class, longest first; the first that fits is used.
SMALL = [" Shipped Australia-wide by Australia Post.", " Ships Australia-wide."]
PARCEL = [" Shipped Australia-wide by Australia Post.", " Shipped Australia-wide."]
LARGE = [" Delivered in Perth, freight quoted Australia-wide.", " Freight quoted Australia-wide."]
NEUTRAL = [" Buy online from Excellent Tiling Services.", " Buy online at ETS."]
DELIVERY = {
    **dict.fromkeys(["Basin Mixer", "Wall Mixer", "Wall Mixer with Diverter", "Kitchen Sink Mixer",
                     "Wall Spout", "Bath Spout", "Shower Head", "Shower Arm", "Ceiling Shower Arm",
                     "Hand Shower Set", "Combination Shower Set", "Towel Rail", "Hand Towel Rail",
                     "Bath Towel Shelf", "Toilet Roll Holder", "Bathroom Hook", "Soap Holder",
                     "Shelf Holder", "Toilet Brush Holder", "Pop Up Waste"], SMALL),
    **dict.fromkeys(["Freestanding Bath Spout", "Freestanding Bath Mixer", "Kitchen Sink", "Mirror",
                     "LED Mirror", "Mirror Cabinet", "Above Counter Basin", "Half Inset Basin",
                     "Semi Basin", "Undermount Basin", "Inset Basin"], PARCEL),
    **dict.fromkeys(["Wall Hung Vanity", "Double Wall Hung Vanity", "Bathroom Tallboy",
                     "Freestanding Bath", "Back to Wall Bath", "Corner Bath", "Inset Bath",
                     "Toilet Suite", "In Wall Cistern Toilet", "Frameless Shower Panel",
                     "Corner Shower Screen"], LARGE),
}

# Closing calls to action left by the earlier Perth-only pass.
OLD_CTA = re.compile(r"\s*(?:Buy online or (?:see it at|visit) our Maddington showroom, Perth|"
                     r"Shop online from ETS Maddington, Perth|Shop online, Perth|"
                     r"Buy online, Maddington, Perth)\.$")

DESC_OVERRIDES = {
    "MELA CASSA Pull Out Sink Mixer with Black Hose":
        "MELA CASSA pull-out kitchen sink mixer with black hose. 5 Star WELS, 6L/min. "
        "Chrome, Matt Black or Brushed Nickel.",
}


def shorten(t):
    s = t.replace("Shower/Bath ", "").replace(" without Rail", ", No Rail")
    s = s.replace("Double Wall Hung Vanity", "Double Vanity").replace("Wall Hung Vanity", "Vanity")
    s = s.replace("Matt White ", "").replace("Single Side Shelves", "Single Shelf")
    s = s.replace(" Side Shelves", " Shelves").replace(" Centre Shelves", " Shelves")
    s = s.replace("Wall Faced Rimless Toilet Suite", "Wall Faced Rimless Toilet")
    return re.sub(r"\s+with\s+", ", ", s)


def seo_title(t, ptype):
    if t in OVERRIDES:
        return OVERRIDES[t]
    s, w = shorten(t), t.replace("Shower/Bath ", "")
    for tpl in TEMPLATES.get(ptype, []) + ["{t} | ETS", "{s} | ETS", "{t}", "{s}"]:
        out = tpl.format(t=t, s=s, w=w)
        if len(out) <= TITLE_MAX:
            return out
    return s[:TITLE_MAX].rsplit(" ", 1)[0]


def seo_desc(t, ptype, old):
    base = DESC_OVERRIDES.get(t) or OLD_CTA.sub(".", old).replace("..", ".")
    for cta in DELIVERY.get(ptype, NEUTRAL):
        if len(base) + len(cta) <= DESC_MAX:
            return base + cta
    parts = re.split(r"(?<=\.)\s+", base)
    while len(parts) > 1 and len(" ".join(parts)) + len(cta) > DESC_MAX:
        parts.pop()
    return " ".join(parts) + cta


def main(tsv, seo_json, out):
    old = {r["id"]: r["seo_desc"] for r in json.load(open(seo_json))}
    rows = []
    for line in open(tsv):
        pid, ptype, title = line.rstrip("\n").split("\t")
        gid = f"gid://shopify/Product/{pid}"
        rows.append({"id": gid, "title": title, "seo_title": seo_title(title, ptype),
                     "seo_desc": seo_desc(title, ptype, old[gid])})
    json.dump(rows, open(out, "w"), indent=1, ensure_ascii=False)
    return rows


if __name__ == "__main__":
    for r in main(*sys.argv[1:4]):
        print(len(r["seo_title"]), r["seo_title"], "||", len(r["seo_desc"]), r["seo_desc"])
