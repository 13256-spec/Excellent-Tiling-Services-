"""Build consistent, Perth-targeted SEO titles/descriptions for every product.

Input: JSON list of products (id, title, status, productType, seo, descriptionHtml?).
Output: seo/product-seo.json  [{id, title, old_title, old_desc, seo_title, seo_desc}]
Rules: title <= 60 chars, description 120-155 chars, no "Default" variant leakage,
       every description names Perth, and one closing call to action.
"""
import html, json, re, sys

TITLE_MAX, DESC_MAX = 60, 155
CTAS = [
    " Buy online or see it at our Maddington showroom, Perth.",
    " Buy online or visit our Maddington showroom, Perth.",
    " Shop online from ETS Maddington, Perth.",
    " Shop online, Perth.",
]
# Case-sensitive: truncated fragments left in the original supplier copy.
CASE_STRIP = [
    r"(?<=[\w)])\s+Available in [A-Z][a-z]+(?: [A-Z][a-z]+)?\.",
    r"(?<=[\w)/])\s+Cartridge\.",
]
STRIP = [
    r"(?:(?<=\.)|^)\s*(?:Shop|Available|Buy|Order)\b[^.]*(?:Excellent Tiling Services|ETS)[^.]*\.",
    r",?\s+(?:through|from|at) (?:ETS|Excellent Tiling Services)(?: in)?,? Maddington(?=\.)",
    r"\s*Available in\.",
    r",?\s*[Ss]old per sqm (?:to|by) the (?:nearest )?full box\.",
    r"(?<=\.)\s*MELA [A-Z]+\.(?=\s|$)",
    r"\s*Shop at Excellent Tiling Services, Maddington\.?",
    r"\s*Available (?:through|from|at) ETS(?: in)? Maddington\.?",
    r"\s*(?:through|from|at) ETS Maddington\.?",
    r"\s*Shop online,? (?:from )?Maddington,? Perth\.?",
    r"\s*Buy online,? Maddington,? Perth\.?",
    r"\s*Buy online from Maddington\.?",
    r"\s*(?:from|at) our Maddington showroom,? Perth(?: WA)?\.?",
    r"\s*Perth\.?$",
]


def seo_title(t):
    t = re.sub(r"\s+", " ", t).strip()
    for suffix in (" | ETS Perth", " | Perth"):
        if len(t) + len(suffix) <= TITLE_MAX:
            return t + suffix
    if len(t) <= TITLE_MAX:
        return t
    # Drop trailing qualifiers ("with 2 Drawers & Shelves") before cutting words.
    short = re.split(r"\s+(?:with|&|-)\s+", t)[0]
    for suffix in (" | ETS Perth", " | Perth", ""):
        if len(short) + len(suffix) <= TITLE_MAX:
            return short + suffix
    cut = short[:TITLE_MAX].rsplit(" ", 1)[0]
    return re.sub(r"\s+(?:with|and|&|in|for|the|of)$", "", cut.rstrip(" -|/,"))


def text_bits(desc_html):
    s = html.unescape(re.sub(r"<[^>]+>", "\n", desc_html or ""))
    lines = [l.strip(" .") for l in s.split("\n") if l.strip()]
    skip = re.compile(r"catalogue|not included|RRP|as shown|optional|^model:", re.I)
    return [l for l in lines if not skip.search(l)]


TITLE_OVERRIDES = {
    # Shopify discards an SEO title identical to the product title, so these need a variant.
    "MELA PALCO / RONDO Combination Shower Set without Rail": "MELA PALCO / RONDO Combination Shower Set, No Rail | Perth",
    "MELA CLARK 1500 Double Wall Hung Vanity with Doors & Drawers": "MELA CLARK 1500 Double Vanity, Doors & Drawers | ETS Perth",
    "MELA CLARK 1800 Double Wall Hung Vanity with 4 Drawers": "MELA CLARK 1800 Double Vanity, 4 Drawers | ETS Perth",
    "MELA CLASSIC 600 Matt White Wall Hung Vanity with 2 Drawers": "MELA CLASSIC 600 Wall Hung Vanity, 2 Drawers | ETS Perth",
    "MELA CLASSIC 750 Matt White Wall Hung Vanity with 2 Drawers": "MELA CLASSIC 750 Wall Hung Vanity, 2 Drawers | ETS Perth",
    "MELA CLASSIC 900 Matt White Wall Hung Vanity with 2 Drawers": "MELA CLASSIC 900 Wall Hung Vanity, 2 Drawers | ETS Perth",
    "MELA CLASSIC 1200 Matt White Wall Hung Vanity with 2 Drawers": "MELA CLASSIC 1200 Wall Hung Vanity, 2 Drawers | ETS Perth",
    "MELA CLARK 1200 Wall Hung Vanity with 2 Drawers & Single Side Shelves": "MELA CLARK 1200 Vanity, 2 Drawers & Single Shelf | ETS Perth",
    "MELA CLARK 1200 Wall Hung Vanity with 2 Drawers & Dual Side Shelves": "MELA CLARK 1200 Vanity, 2 Drawers & Dual Shelves | ETS Perth",
    "MELA CLASSIC 1500 Matt White Double Wall Hung Vanity with 4 Drawers": "MELA CLASSIC 1500 Double Vanity, 4 Drawers | ETS Perth",
    "MELA CLASSIC 1500 Matt White Double Wall Hung Vanity with 4 Drawers & Shelves": "MELA CLASSIC 1500 Double Vanity, Drawers & Shelves | Perth",
    "MELA CLASSIC 1800 Matt White Double Wall Hung Vanity with 4 Drawers": "MELA CLASSIC 1800 Double Vanity, 4 Drawers | ETS Perth",
    "MELA CLASSIC 1800 Matt White Double Wall Hung Vanity with 4 Drawers & Shelves": "MELA CLASSIC 1800 Double Vanity, Drawers & Shelves | Perth",
}


DESC_OVERRIDES = {
    "Time Stone Moon Porcelain Tile": "Time Stone Moon porcelain tile, 300x600 or 600x600mm, Matt or Lappato. P4/R11 slip rating for wet areas. Shop online from ETS Maddington, Perth.",
    "Time Stone Charcoal Porcelain Tile": "Time Stone Charcoal porcelain tile, 300x600 or 600x600mm, Matt or Lappato. P4/R11 slip rating for wet areas. Shop online from ETS Maddington, Perth.",
}


def sentences_clean(d, title):
    """Drop fragment sentences and ones that just restate the title."""
    tw = set(title.lower().split())
    keep = []
    for i, sent in enumerate(re.split(r"(?<=\.)\s+", d)):
        words = sent.strip(" .").split()
        if len(words) <= 3 and not re.search(r"\d", sent):
            continue
        if i > 0 and (sent[:1].islower() or re.search(r"catalogue", sent, re.I)):
            continue
        sent = re.sub(r"(?<=[A-Za-z]{2})\s+\d{3,4}mm(?: Pearl)?(?=\.$)|(?<=\d)mm Pearl(?=\.$)", lambda m: "mm" if m.group(0).startswith("mm") else "", sent.strip())
        if re.fullmatch(r"\d+mm\.", sent):
            continue
        # Supplier copy was cut off mid-phrase ("Easy to.", "from 600mm to.").
        if re.search(r"\b(?:to|the|and|of|with|for|from|in|a|tiled)\.$", sent.strip()):
            continue
        lw = [re.sub(r"\W", "", w.lower()) for w in words]
        prev = tw | set(re.findall(r"[a-z0-9]+", " ".join(keep).lower()))
        if i > 0 and sum(w in prev for w in lw) / len(lw) >= 0.5:
            continue
        keep.append(sent.strip())
    return " ".join(keep)


def base_desc(p):
    d = (p["seo"].get("description") or "").strip()
    bug = "Default" in d
    d = re.sub(r"\s+in Default\.?", "", d)
    for pat in STRIP:
        d = re.sub(pat, "", d, flags=re.I).strip()
    d = re.sub(r"(?<=/min)\s+WELS\.", ".", d)
    for pat in CASE_STRIP:
        d = re.sub(pat, "", d).strip()
    d = re.sub(r"\s{2,}", " ", d).strip()
    d = re.sub(r"(?<=[\w)%])\s+(?=(?:Flow rate|Cartridge|Colour|Material|Manufacturing tolerance|WELS)\b:)", ", ", d)
    d = sentences_clean(d, p["title"])
    if bug or len(d) < 100:
        bits = text_bits(p.get("descriptionHtml", ""))
        first = d if (d and not bug) else p["title"] + "."
        if not first.endswith("."):
            first += "."
        seen = set(re.findall(r"[a-z0-9]+", first.lower()))
        extra = []
        for b in bits[1:6]:
            bw = re.findall(r"[a-z0-9]+", b.lower())
            if len(b) >= 80 or not bw or sum(w in seen for w in bw) / len(bw) >= 0.5:
                continue
            if b[:1].islower() or len(bw) <= 3 and not re.search(r"\d", b):
                continue
            value = re.sub(r"\s", "", b.split(":", 1)[-1].lower())
            if value and value in re.sub(r"\s", "", first.lower()):
                continue
            extra.append(b); seen.update(bw)
        d = first + (" " + ". ".join(extra) + "." if extra else "")
    d = re.sub(r"[,;:\s]+\.", ".", d)
    if d and not d.endswith("."):
        d += "."
    return d


def fit(d):
    for cta in CTAS:
        if len(d) + len(cta) <= DESC_MAX:
            return d + cta
    # trim trailing sentences until the shortest CTA fits
    parts = re.split(r"(?<=\.)\s+", d)
    while len(parts) > 1 and len(" ".join(parts)) + len(CTAS[-1]) > DESC_MAX:
        parts.pop()
    d = " ".join(parts)
    if len(d) + len(CTAS[-1]) > DESC_MAX:
        d = d[: DESC_MAX - len(CTAS[-1]) - 1].rsplit(" ", 1)[0].rstrip(",;:") + "."
    return d + CTAS[-1]


def main(paths, out):
    prods, seen = [], set()
    for path in paths:
        data = json.load(open(path))
        data = data.get("data", data)
        conns = data.values() if isinstance(data, dict) else [data]
        for c in conns:
            nodes = c["nodes"] if isinstance(c, dict) and "nodes" in c else c
            for n in nodes:
                if n["id"] not in seen:
                    seen.add(n["id"]); prods.append(n)
    rows = []
    for p in prods:
        rows.append({
            "id": p["id"], "title": p["title"], "status": p["status"],
            "old_title": p["seo"].get("title"), "old_desc": p["seo"].get("description"),
            "seo_title": TITLE_OVERRIDES.get(p["title"]) or seo_title(p["title"]), "seo_desc": DESC_OVERRIDES.get(p["title"]) or fit(base_desc(p)),
        })
    json.dump(rows, open(out, "w"), indent=1, ensure_ascii=False)
    return rows


if __name__ == "__main__":
    rows = main(sys.argv[1:-1], sys.argv[-1])
    print(len(rows), "products")
