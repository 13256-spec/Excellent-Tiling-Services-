#!/usr/bin/env python3
"""Manufacturer spreadsheet -> Shopify-ready import for the house-brand tapware.

    python3 scripts/import_supplier.py SHEET.xlsx [--sheet NAME] [--out data/imports/YYYY-MM-DD] [--apply] [--publish]

Dry run by default: reads the (messy) export, maps its columns through scripts/import_config.json, builds one product
per model with one variant per finish, prices from FOB, applies tags and metafields, and writes
  <out>/report.md     what would be created/updated, blocked or skipped, and why
  <out>/payload.json  the productSet inputs exactly as they would be sent
  <out>/import.csv    one row per variant for the owner's spreadsheet
Nothing touches the store unless --apply is given (needs SHOPIFY_STORE and SHOPIFY_ADMIN_TOKEN). Even then every product
is created as DRAFT; --publish sets ACTIVE only for products that pass the WaterMark + WELS gate.

Hard rules enforced here: supplier name never in customer-facing text; no "order on demand" wording; WaterMark + WELS
required before ACTIVE; cost = landed ex GST x 1.1; inventory tracked + continue selling; supplier code in the SKU.
"""
import argparse, csv, datetime, json, math, os, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG_PATH = ROOT / "scripts/import_config.json"
API_VERSION = "2026-10"
FORBIDDEN_PHRASES = ["on demand", "order in", "ordered in", "made to order", "ships from supplier", "drop ship", "dropship"]


# ---------------------------------------------------------------- parsing helpers
def norm_header(h):
    h = str(h or "").strip().lower()
    h = re.sub(r"[\(\)\[\]（）:：/\\\-_.,，。]+", " ", h)
    return re.sub(r"\s+", " ", h).strip()


def parse_number(s):
    """First number in a string: '≈ 1,234.5 kg' -> 1234.5. None when there is none."""
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return float(s)
    m = re.search(r"-?\d+(?:[.,]\d+)?", str(s).replace(",", ""))
    return float(m.group(0)) if m else None


def _numbers(s):
    return [float(x) for x in re.findall(r"\d+(?:\.\d+)?", str(s or "").replace(",", ""))]


def to_mm(s):
    """'150mm' / '15 cm' / '6 in' / '6"' -> 150 / 150 / 152 / 152 (int mm). Default unit mm."""
    n = parse_number(s)
    if n is None:
        return None
    t = str(s).lower()
    if re.search(r'(?<![a-z])(in|inch|inches)(?![a-z])|"', t):
        n *= 25.4
    elif re.search(r"(?<![a-z])cm(?![a-z])", t):
        n *= 10
    elif re.search(r"(?<![a-z])m(?![a-z])", t):
        n *= 1000
    return int(round(n))


def to_kpa(s):
    """'0.05-0.8 MPa' -> 800, '500kPa' -> 500, '5 bar' -> 500, '72 psi' -> 496. Takes the maximum of a range."""
    nums = _numbers(s)
    if not nums:
        return None
    n, t = max(nums), str(s).lower()
    if "mpa" in t:
        n *= 1000
    elif "bar" in t:
        n *= 100
    elif "psi" in t:
        n *= 6.89476
    elif "kpa" not in t and n <= 2:  # a bare 0.5 means MPa on Chinese sheets
        n *= 1000
    return int(round(n))


def to_lpm(s):
    """'6L/min' / '6 lpm' / '1.6 gpm' -> 6.0 / 6.0 / 6.1 (litres per minute)."""
    n = parse_number(s)
    if n is None:
        return None
    if "gpm" in str(s).lower() or "gal" in str(s).lower():
        n *= 3.78541
    return round(n, 1)


def to_kg(s):
    n = parse_number(s)
    if n is None:
        return None
    t = str(s).lower()
    if re.search(r"(?<![a-z])g(ram)?s?(?![a-z])", t) and "kg" not in t:
        n /= 1000
    elif "lb" in t:
        n *= 0.453592
    return round(n, 3)


def parse_dimensions_mm(s):
    """'45x180x150mm' -> [45,180,150]; '18 x 7 in' -> inches converted."""
    nums = _numbers(s)
    if not nums:
        return []
    scale = 25.4 if re.search(r'(?<![a-z])(in|inch)(?![a-z])|"', str(s).lower()) else (10 if re.search(r"(?<![a-z])cm(?![a-z])", str(s).lower()) else 1)
    return [int(round(n * scale)) for n in nums[:3]]


def parse_wels_rating(s):
    n = parse_number(s)
    return "%d Star" % int(n) if n is not None and 0 <= n <= 6 else ""


def parse_years(s):
    n = parse_number(s)
    return int(n) if n is not None else None


def parse_finishes(s, cfg):
    """'CP/MB, 拉丝镍' -> (['Chrome','Matt Black','Brushed Nickel'], [])."""
    found, unknown = [], []
    for part in re.split(r"[\/,;|、&+]+|\band\b", str(s or "")):
        p = part.strip().lower()
        if not p:
            continue
        hit = next((name for name, f in cfg["finishes"].items() if not name.startswith("_") and p in [a.lower() for a in f["aliases"]] or p == name.lower()), None)
        if hit and hit not in found:
            found.append(hit)
        elif not hit:
            unknown.append(part.strip())
    return found, unknown


def detect_type(*texts, cfg):
    blob = " ".join(str(t or "") for t in texts).lower()
    for ptype, words in cfg["types"].items():
        if ptype.startswith("_"):
            continue
        if any(w.lower() in blob for w in words):
            return ptype
    return ""


def normalise_model(model):
    m = re.sub(r"[^A-Za-z0-9]+", "-", str(model or "").upper()).strip("-")
    return m


def handleize(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", str(s).lower())).strip("-")


def contains_supplier(text, names):
    t = str(text or "").lower()
    return any(n and n.lower() in t for n in names)


def scrub_supplier(text, names):
    for n in sorted((n for n in names if n), key=len, reverse=True):
        text = re.sub(re.escape(n), "", text, flags=re.I)
    return re.sub(r"\s{2,}", " ", text).strip(" -–,")


# ---------------------------------------------------------------- pricing / tags
def round_price(x, rule):
    if rule == "x.95":
        c = math.ceil(x)
        cand = c - 0.05
        return round(cand if cand >= x else c + 0.95, 2)
    if rule == "x.00":
        return float(math.ceil(x))
    return round(x, 2)


def price_product(fob, weight_kg, ptype, cfg):
    cur, land, pr = cfg["currency"], cfg["landed"], cfg["pricing"]
    fob_aud = fob * cur["aud_per_unit"]
    landed = fob_aud * (1 + land["duty_pct"] / 100) + fob_aud * land["freight_pct_of_fob"] / 100 \
        + (weight_kg or 0) * land["freight_per_kg_aud"] + fob_aud * land["other_pct"] / 100
    cost_inc = round(landed * 1.1, 2)
    markup = pr["markup_on_landed"].get(ptype, pr["markup_on_landed"]["default"])
    price = round_price(landed * markup * 1.1, pr["round"])
    floor = round(cost_inc * pr["floor_multiplier_on_cost_inc_gst"], 2)
    flags = []
    if price < floor:
        price, flags = round_price(floor, pr["round"]), ["raised-to-floor"]
    trade_floor = cost_inc / (1 - pr["trade_floor_margin_ex_gst"])
    band = next((b for b in pr["trade_bands"] if price * (1 - b / 100) >= trade_floor), 0)
    return {"fob": fob, "fob_aud": round(fob_aud, 2), "landed_ex_gst": round(landed, 2), "cost_inc_gst": cost_inc,
            "price": price, "floor": floor, "markup": markup, "trade_band": band,
            "trade_price": round(price * (1 - band / 100), 2), "flags": flags}


def ship_tags(weight_kg, longest_mm, cfg):
    sh = cfg["shipping"]
    if longest_mm and longest_mm > sh["local_only_if_longest_side_over_mm"]:
        return list(sh["over_max"])
    for band in sh["bands"]:
        if weight_kg <= band["max_kg"]:
            return list(band["tags"])
    return list(sh["over_max"])


# ---------------------------------------------------------------- workbook reading
def find_header_row(ws, cfg, scan=25):
    aliases = {a for v in cfg["columns"].values() if isinstance(v, list) for a in v}
    best, best_score = None, 0
    for r in range(1, min(ws.max_row, scan) + 1):
        cells = [norm_header(c.value) for c in ws[r]]
        score = sum(1 for c in cells if c and (c in aliases or any(a == c or (len(a) > 2 and a in c) for a in aliases)))
        if score > best_score:
            best, best_score = r, score
    if best_score < 3:
        raise SystemExit("Could not find a header row (need at least 3 recognised headers in the first %d rows). "
                         "Add the sheet's headers to scripts/import_config.json -> columns." % scan)
    return best


def map_columns(headers, cfg):
    """headers: list of raw header strings by column index. Returns ({field: index}, [unmapped headers])."""
    normed = [norm_header(h) for h in headers]
    mapping, used = {}, set()
    cols = {k: v for k, v in cfg["columns"].items() if isinstance(v, list)}
    # pass 1 exact, pass 2 containment with the longest alias first
    for exact in (True, False):
        for field, aliases in cols.items():
            if field in mapping:
                continue
            for a in sorted(aliases, key=len, reverse=True):
                for i, h in enumerate(normed):
                    if i in used or not h:
                        continue
                    if (exact and h == a) or (not exact and len(a) > 1 and re.search(r"(^|\s)%s(\s|$)" % re.escape(a), h)):
                        mapping[field], used = i, used | {i}
                        break
                if field in mapping:
                    break
    unmapped = [headers[i] for i in range(len(headers)) if i not in used and normed[i]]
    return mapping, unmapped


def read_rows(ws, header_row, mapping):
    rows, carry = [], {}
    for r in ws.iter_rows(min_row=header_row + 1, values_only=True):
        rec = {f: ("" if r[i] is None else str(r[i]).strip()) for f, i in mapping.items() if i < len(r)}
        if not any(rec.values()):
            continue
        # merged cells: a row with a finish but no model continues the model above
        if not rec.get("model") and rec.get("finish") and carry:
            for f in ("model", "name", "type", "range", "material", "cartridge", "pressure", "flow", "wels_rating",
                      "wels_registration", "watermark_licence", "watermark_certifier", "weight", "dimensions", "warranty",
                      "spout_projection", "spout_height", "image"):
                rec[f] = rec.get(f) or carry.get(f, "")
            rec["fob"] = rec.get("fob") or carry.get("fob", "")
        if not rec.get("model"):
            continue
        carry = rec
        rows.append(rec)
    return rows


# ---------------------------------------------------------------- product building
def build_products(rows, cfg, publish=False):
    brand, supplier_names = cfg["brand"]["name"], [cfg["supplier"]["name"], *cfg["supplier"]["aliases"]]
    groups, order = {}, []
    for rec in rows:
        key = normalise_model(rec["model"])
        if key not in groups:
            groups[key], order = [], order + [key]
        groups[key].append(rec)

    products, skipped, unknown_finishes = [], [], {}
    for key in order:
        recs = groups[key]
        first = {f: next((r[f] for r in recs if r.get(f)), "") for f in recs[0]}
        ptype = detect_type(first.get("type"), first.get("name"), cfg=cfg)
        rng = scrub_supplier(first.get("range", ""), supplier_names).strip().title()
        # finishes: each row may carry several; a finish-specific FOB (black often dearer) wins over the group's
        finishes = {}
        for r in recs:
            names, unk = parse_finishes(r.get("finish"), cfg)
            for u in unk:
                unknown_finishes.setdefault(key, []).append(u)
            fob = parse_number(r.get("fob")) or parse_number(first.get("fob"))
            for n in names:
                finishes.setdefault(n, fob)
        if not finishes:
            skipped.append((key, "no recognisable finish on the sheet; add the finish or its alias to import_config.json"))
            continue
        if not any(finishes.values()):
            skipped.append((key, "no FOB price"))
            continue
        weight = to_kg(first.get("weight")) or cfg["shipping"]["default_weight_kg_by_type"].get(ptype, 1.5)
        dims = parse_dimensions_mm(first.get("dimensions"))
        width = to_mm(first.get("width")) or (dims[0] if len(dims) == 3 else None)
        depth = to_mm(first.get("depth")) or (dims[1] if len(dims) == 3 else None)
        height = to_mm(first.get("height")) or (dims[2] if len(dims) == 3 else None)
        longest = max([d for d in (width, depth, height) if d] or [0])

        cart_brand, cart_size = first.get("cartridge", ""), to_mm(first.get("cartridge_size"))
        m = re.search(r"(\d{2})\s*mm", cart_brand)
        if m and not cart_size:
            cart_size = int(m.group(1))
        cart_brand = re.sub(r"\d{2}\s*mm|ceramic|cartridge|阀芯", "", cart_brand, flags=re.I).strip(" ,/-") or cfg["defaults"]["cartridge_brand"]

        mf = {
            "range": rng,
            "material": first.get("material") or cfg["defaults"]["material"],
            "finish": list(finishes),
            "cartridge_brand": cart_brand,
            "cartridge_size_mm": cart_size,
            "max_pressure_kpa": to_kpa(first.get("pressure")),
            "flow_rate": ("%s L/min" % ("%g" % to_lpm(first["flow"]))) if first.get("flow") and to_lpm(first["flow"]) else "",
            "wels_rating": parse_wels_rating(first.get("wels_rating")),
            "wels_registration": first.get("wels_registration", "").strip(),
            "watermark_licence_number": first.get("watermark_licence", "").strip(),
            "watermark_certifier": first.get("watermark_certifier", "").strip(),
            "installation_type": cfg["defaults"]["installation_type_by_type"].get(ptype, ""),
            "spout_projection_mm": to_mm(first.get("spout_projection")),
            "spout_height_mm": to_mm(first.get("spout_height")),
            "warranty_years": parse_years(first.get("warranty")) or cfg["defaults"]["warranty_years"],
            "width_mm": width, "height_mm": height, "depth_mm": depth,
            "supplier": cfg["supplier"]["name"],
        }
        missing = [k for k in cfg["publish_gate"] if not mf.get(k)]
        type_label = ptype or "Tapware"
        clean_name = scrub_supplier(first.get("name", ""), supplier_names)
        title = " ".join(x for x in [brand, rng, type_label] if x) if ptype else " ".join(x for x in [brand, clean_name] if x)
        tags = sorted({cfg["brand"]["tag"], type_label, "Tapware", *ship_tags(weight, longest, cfg),
                       *(["WELS %s" % mf["wels_rating"]] if mf["wels_rating"] else []),
                       *(["suite-" + handleize(rng)] if rng else []), *(["needs-compliance"] if missing else [])})
        variants, pricing_rows = [], []
        for finish, fob in finishes.items():
            pr = price_product(fob, weight, ptype, cfg)
            code = cfg["finishes"][finish]["code"]
            sku = "%s%s-%s" % (cfg["brand"]["sku_prefix"], key, code)
            v = {"optionValues": [{"optionName": "Finish", "name": finish}], "sku": sku, "price": pr["price"],
                 "inventoryPolicy": "CONTINUE",
                 "inventoryItem": {"tracked": True, "cost": pr["cost_inc_gst"],
                                   "measurement": {"weight": {"unit": "KILOGRAMS", "value": weight}}}}
            if first.get("barcode"):
                v["barcodes"] = [{"value": first["barcode"]}]
            img = _image_for(first.get("image", ""), finish, cfg)
            if img:
                v["file"] = {"originalSource": img, "alt": "%s in %s" % (title, finish), "contentType": "IMAGE"}
            variants.append(v)
            pricing_rows.append({"finish": finish, "sku": sku, **pr})
        band = min(p["trade_band"] for p in pricing_rows)  # one band per product (playbook), the safest variant decides
        mf["trade_band"] = band
        description = _description(title, type_label, rng, mf, list(finishes), cfg)
        seo_title = ("%s %s | %s" % (rng, type_label, brand) if rng else title)[:60].rstrip(" |")
        ship_line = "Free shipping Australia-wide on orders over $100" if "ship-parcel" in tags and "ship-bulky" not in tags else "Perth delivery or pickup from Maddington"
        seo_desc = "%s %s%s in %s. %s%s. %s from ETS, Perth." % (
            brand, (rng + " ") if rng else "", type_label.lower(), ", ".join(finishes),
            ("WELS %s, " % mf["wels_rating"]) if mf["wels_rating"] else "", "WaterMark certified" if mf["watermark_licence_number"] else "solid brass",
            ship_line)
        seo_desc = seo_desc[:155].rsplit(" ", 1)[0] if len(seo_desc) > 155 else seo_desc
        for text in (title, description, seo_title, seo_desc, " ".join(tags)):
            assert not contains_supplier(text, supplier_names), "supplier name leaked into customer text for %s" % key
            assert not any(p in text.lower() for p in FORBIDDEN_PHRASES), "forbidden stock wording in %s" % key
        product = {
            "handle": handleize(title + ("" if ptype else " " + key)),
            "title": title, "vendor": brand, "productType": type_label, "tags": tags,
            "status": "ACTIVE" if publish and not missing else "DRAFT",
            "descriptionHtml": description,
            "seo": {"title": seo_title, "description": seo_desc},
            "productOptions": [{"name": "Finish", "position": 1, "values": [{"name": f} for f in finishes]}],
            "variants": variants,
            "metafields": _metafields(mf),
        }
        files = [u for u in _urls(first.get("image", "")) if u not in {v.get("file", {}).get("originalSource") for v in variants}]
        if files:
            product["files"] = [{"originalSource": u, "alt": title, "contentType": "IMAGE"} for u in files]
        products.append({"key": key, "input": product, "pricing": pricing_rows, "gate_missing": missing,
                         "weight_kg": weight, "longest_mm": longest, "range": rng, "type": type_label,
                         "flags": sorted({f for p in pricing_rows for f in p["flags"]} | ({"unknown-type"} if not ptype else set())),
                         "spec_sheet": first.get("spec_sheet", ""), "installation_guide": first.get("installation_guide", "")})
    return products, skipped, unknown_finishes


_MF_TYPES = {"finish": "list.single_line_text_field", "cartridge_size_mm": "number_integer", "max_pressure_kpa": "number_integer",
             "spout_projection_mm": "number_integer", "spout_height_mm": "number_integer", "warranty_years": "number_integer",
             "width_mm": "number_integer", "height_mm": "number_integer", "depth_mm": "number_integer", "trade_band": "number_integer"}


def _metafields(mf):
    out = []
    for k, v in mf.items():
        if v in ("", None, []):
            continue
        t = _MF_TYPES.get(k, "single_line_text_field")
        out.append({"namespace": "ets", "key": k, "type": t, "value": json.dumps(v) if t.startswith("list.") else str(v)})
    return out


def _urls(cell):
    return re.findall(r"https?://\S+", str(cell or ""))


def _image_for(cell, finish, cfg):
    f = cfg["finishes"][finish]
    keys = [finish.lower().replace(" ", "-"), finish.lower().replace(" ", ""), f["code"].lower()] + [a.lower() for a in f["aliases"] if a.isascii()]
    for u in _urls(cell):
        name = u.rsplit("/", 1)[-1].lower()
        if any(re.search(r"(^|[-_.])%s([-_.]|$)" % re.escape(k), name) for k in keys):
            return u
    return None


def _description(title, ptype, rng, mf, finishes, cfg):
    intro = {
        "Basin Mixer": "A single-lever basin mixer with a solid brass body and a ceramic disc cartridge, so the lever stays smooth and drip-free.",
        "Wall Mixer": "A wall mixer for showers and baths with a solid brass body and a ceramic disc cartridge. The in-wall body sits behind the tiles; only the plate and handle show.",
        "Bath Spout": "A wall-mounted bath spout in solid brass, sized to clear the rim of a standard bath and match the rest of the suite.",
        "Shower Set": "A complete shower set: overhead rain shower, handheld shower on a rail, and the hoses and fittings to connect them.",
        "Shower Head": "An overhead shower in solid brass with easy-clean silicone nozzles.",
        "Shower Rail": "A shower rail with an adjustable handset holder, in solid brass.",
    }.get(ptype, "Solid brass tapware with a ceramic disc cartridge.")
    specs = []
    if mf["material"]: specs.append("Body: %s" % mf["material"])
    if finishes: specs.append("Finishes: %s" % ", ".join(finishes))
    if mf["cartridge_brand"] or mf["cartridge_size_mm"]:
        specs.append("Cartridge: %s" % " ".join(x for x in [mf["cartridge_brand"], ("%d mm" % mf["cartridge_size_mm"]) if mf["cartridge_size_mm"] else ""] if x))
    if mf["max_pressure_kpa"]: specs.append("Max working pressure: %d kPa" % mf["max_pressure_kpa"])
    if mf["wels_rating"]: specs.append("WELS: %s%s" % (mf["wels_rating"], (", %s" % mf["flow_rate"]) if mf["flow_rate"] else ""))
    if mf["wels_registration"]: specs.append("WELS registration: %s" % mf["wels_registration"])
    if mf["watermark_licence_number"]: specs.append("WaterMark licence: %s%s" % (mf["watermark_licence_number"], (" (%s)" % mf["watermark_certifier"]) if mf["watermark_certifier"] else ""))
    if mf["spout_projection_mm"]: specs.append("Spout projection: %d mm" % mf["spout_projection_mm"])
    if mf["spout_height_mm"]: specs.append("Spout height: %d mm" % mf["spout_height_mm"])
    dims = [d for d in (mf["width_mm"], mf["depth_mm"], mf["height_mm"]) if d]
    if len(dims) == 3: specs.append("Size: %d x %d x %d mm (W x D x H)" % tuple(dims))
    if mf["installation_type"]: specs.append("Installation: %s" % mf["installation_type"])
    if mf["warranty_years"]: specs.append("Warranty: %d years" % mf["warranty_years"])
    suite = ("<p>Part of the %s suite: basin mixer, wall mixer, bath spout and shower set in matching finishes, so the whole bathroom matches.</p>" % rng) if rng else ""
    return ("<p>%s</p>%s<h3>Specifications</h3><ul>%s</ul><h3>Good to know</h3><ul>"
            "<li>Installation by a licensed plumber. The installation guide is under Downloads.</li>"
            "<li>Australian plumbing rules limit new installations to 500 kPa; fit a pressure limiting valve if your supply is higher.</li>"
            "<li>Clean with a soft cloth and mild soap only. Abrasives and acidic cleaners mark the finish and void the warranty.</li></ul>"
            % (intro, suite, "".join("<li>%s</li>" % s for s in specs)))


# ---------------------------------------------------------------- outputs
def write_outputs(out, products, skipped, unknown, mapping, unmapped, headers, cfg, sheet_name, publish):
    out.mkdir(parents=True, exist_ok=True)
    (out / "payload.json").write_text(json.dumps([p["input"] for p in products], indent=2, ensure_ascii=False))
    with (out / "import.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["handle", "title", "type", "range", "finish", "sku", "fob", "fob_aud", "landed_ex_gst", "cost_inc_gst", "price", "floor", "trade_band", "trade_price", "status", "gate_missing", "tags"])
        for p in products:
            for pr in p["pricing"]:
                w.writerow([p["input"]["handle"], p["input"]["title"], p["type"], p["range"], pr["finish"], pr["sku"], pr["fob"], pr["fob_aud"], pr["landed_ex_gst"], pr["cost_inc_gst"], pr["price"], pr["floor"], p["input"]["metafields"] and next(m["value"] for m in p["input"]["metafields"] if m["key"] == "trade_band"), pr["trade_price"], p["input"]["status"], ";".join(p["gate_missing"]), " ".join(p["input"]["tags"])])
    blocked = [p for p in products if p["gate_missing"]]
    ok = [p for p in products if not p["gate_missing"]]
    lines = ["# Supplier import, dry run %s" % datetime.date.today().isoformat(), "",
             "Sheet `%s`: %d products built (%d variants), %d pass the WaterMark/WELS gate, %d blocked, %d skipped." % (
                 sheet_name, len(products), sum(len(p["pricing"]) for p in products), len(ok), len(blocked), len(skipped)),
             "Mode: %s. Products are written as DRAFT%s." % ("apply" if publish is not None else "dry run", "; --publish sets gate-passing products ACTIVE" if not publish else " except gate-passing ones, which go ACTIVE"), "",
             "## Columns", "", "| Field | Sheet header |", "| --- | --- |"]
    lines += ["| %s | %s |" % (f, headers[i]) for f, i in sorted(mapping.items())]
    if unmapped:
        lines += ["", "Headers not used (add an alias in import_config.json if one matters): " + ", ".join("`%s`" % h for h in unmapped)]
    lines += ["", "## Products", "", "| Handle | Type | Range | Finishes | Cost inc GST | Price | Trade | Status | Tags | Flags |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for p in products:
        costs = "–".join(sorted({"$%.2f" % x["cost_inc_gst"] for x in p["pricing"]}))
        prices = "–".join(sorted({"$%.2f" % x["price"] for x in p["pricing"]}))
        band = next(m["value"] for m in p["input"]["metafields"] if m["key"] == "trade_band")
        lines.append("| %s | %s | %s | %s | %s | %s | %s%% | %s | %s | %s |" % (
            p["input"]["handle"], p["type"], p["range"], ", ".join(x["finish"] for x in p["pricing"]), costs, prices, band,
            p["input"]["status"] + (" (blocked: %s)" % ", ".join(p["gate_missing"]) if p["gate_missing"] else ""),
            " ".join(t for t in p["input"]["tags"] if t.startswith(("ship-", "ebay-"))), ", ".join(p["flags"])))
    if blocked:
        lines += ["", "## Blocked by the WaterMark / WELS gate (stay Draft until the data arrives)", ""]
        lines += ["- **%s** (%s): missing %s" % (p["input"]["title"], p["key"], ", ".join(p["gate_missing"])) for p in blocked]
    if skipped:
        lines += ["", "## Skipped (not in the payload)", ""] + ["- **%s**: %s" % s for s in skipped]
    if unknown:
        lines += ["", "## Finish values not recognised", ""] + ["- %s: %s" % (k, ", ".join(sorted(set(v)))) for k, v in unknown.items()]
    suites = sorted({(p["range"], "suite-" + handleize(p["range"])) for p in products if p["range"]})
    if suites:
        lines += ["", "## Collections needed", "", "- `%s` (vendor equals %s), template `collection.brand`" % (handleize(cfg["brand"]["name"]), cfg["brand"]["name"])]
        lines += ["- `%s-%s` (vendor equals %s AND tag equals `%s`), template `collection.suite`" % (handleize(cfg["brand"]["name"]), handleize(r), cfg["brand"]["name"], t) for r, t in suites]
    trade = {}
    for p in products:
        trade.setdefault(next(m["value"] for m in p["input"]["metafields"] if m["key"] == "trade_band"), []).append(p["input"]["handle"])
    lines += ["", "## Trade lists (add each product to its trade-list-N collection; ets.trade_band is set in the payload)", ""]
    lines += ["- trade-list-%s: %s" % (b, ", ".join(h)) for b, h in sorted(trade.items(), key=lambda x: -int(x[0])) if b != "0"]
    docs = [(p["input"]["handle"], p["spec_sheet"], p["installation_guide"]) for p in products if p["spec_sheet"] or p["installation_guide"]]
    if docs:
        lines += ["", "## Documents to upload (Content -> Files, then set ets.spec_sheet / ets.installation_guide)", ""] + ["- %s: %s %s" % d for d in docs]
    (out / "report.md").write_text("\n".join(lines) + "\n")
    return out / "report.md"


# ---------------------------------------------------------------- Shopify writes
def gql(query, variables=None):
    import requests  # only needed with --apply
    store, token = os.environ.get("SHOPIFY_STORE"), os.environ.get("SHOPIFY_ADMIN_TOKEN")
    if not store or not token:
        raise SystemExit("--apply needs SHOPIFY_STORE (x.myshopify.com) and SHOPIFY_ADMIN_TOKEN in the environment")
    r = requests.post("https://%s/admin/api/%s/graphql.json" % (store, API_VERSION), json={"query": query, "variables": variables or {}},
                      headers={"X-Shopify-Access-Token": token, "Content-Type": "application/json"}, timeout=60)
    r.raise_for_status()
    data = r.json()
    if data.get("errors"):
        raise SystemExit("GraphQL errors: %s" % json.dumps(data["errors"], indent=1))
    return data["data"]


def _finish_metaobjects(cfg):
    """Make sure a shopify--color-pattern entry exists per finish (handle = finish handleized) and return {finish: gid}.
    The Horizon variant picker shows a swatch for an option value linked to a metaobject with a colour field."""
    tokens = json.loads((ROOT / "brand/tokens.json").read_text())["finish"]
    gids = {}
    for finish in cfg["finishes"]:
        if finish.startswith("_"):
            continue
        handle = handleize(finish)
        hexval = tokens.get(handle, {}).get("hex", "#CCCCCC")
        data = gql("""mutation($h: MetaobjectHandleInput!, $m: MetaobjectUpsertInput!) { metaobjectUpsert(handle: $h, metaobject: $m) {
                       metaobject { id } userErrors { field message } } }""",
                   {"h": {"type": "shopify--color-pattern", "handle": handle},
                    "m": {"fields": [{"key": "label", "value": finish}, {"key": "color", "value": hexval}]}})["metaobjectUpsert"]
        if data["userErrors"]:
            print("swatch metaobject for %s not created: %s" % (finish, data["userErrors"]))
            return {}
        gids[finish] = data["metaobject"]["id"]
    return gids


def _link_swatches(inp, gids):
    """Point the product's Finish option and each variant's option value at the colour-pattern entries."""
    if not gids:
        return
    for opt in inp.get("productOptions", []):
        if opt["name"] == "Finish":
            opt["linkedMetafield"] = {"namespace": "shopify", "key": "color-pattern", "values": [gids[v["name"]] for v in opt["values"]]}
    for v in inp.get("variants", []):
        for ov in v["optionValues"]:
            if ov.get("optionName") == "Finish":
                ov["linkedMetafieldValue"] = gids[ov["name"]]


def apply(products, cfg, publish):
    """Create or update each product with productSet (matched by handle), then make sure the collections exist."""
    results = []
    pubs = [n["id"] for n in gql("{ publications(first: 20) { nodes { id } } }")["publications"]["nodes"]] if publish else []
    gids = _finish_metaobjects(cfg) if cfg.get("swatches", {}).get("link_finish_to_color_pattern", True) else {}
    for p in products:
        inp = json.loads(json.dumps(p["input"]))
        _link_swatches(inp, gids)
        existing = gql('query($q: String!) { products(first: 1, query: $q) { nodes { id } } }', {"q": "handle:%s" % inp["handle"]})["products"]["nodes"]
        if existing:
            inp["id"] = existing[0]["id"]
        data = gql("""mutation($input: ProductSetInput!) { productSet(synchronous: true, input: $input) {
                       product { id handle status } userErrors { field message code } } }""", {"input": inp})["productSet"]
        if data["userErrors"]:
            results.append((inp["handle"], "ERROR", data["userErrors"]))
            continue
        pid = data["product"]["id"]
        if publish and not p["gate_missing"] and pubs:
            gql("""mutation($id: ID!, $input: [PublicationInput!]!) { publishablePublish(id: $id, input: $input) { userErrors { message } } }""",
                {"id": pid, "input": [{"publicationId": x} for x in pubs]})
        results.append((inp["handle"], "updated" if existing else "created", pid))
    _ensure_collections(products, cfg)
    return results


def _ensure_collections(products, cfg):
    brand, bh = cfg["brand"]["name"], handleize(cfg["brand"]["name"])
    wanted = [(bh, brand, [{"column": "VENDOR", "relation": "EQUALS", "condition": brand}], "brand")]
    for rng in sorted({p["range"] for p in products if p["range"]}):
        wanted.append((bh + "-" + handleize(rng), "%s %s suite" % (brand, rng),
                       [{"column": "VENDOR", "relation": "EQUALS", "condition": brand}, {"column": "TAG", "relation": "EQUALS", "condition": "suite-" + handleize(rng)}], "suite"))
    for handle, title, rules, suffix in wanted:
        if gql('query($h: String!) { collectionByHandle(handle: $h) { id } }', {"h": handle})["collectionByHandle"]:
            continue
        gql("""mutation($input: CollectionInput!) { collectionCreate(input: $input) { collection { id handle } userErrors { message } } }""",
            {"input": {"handle": handle, "title": title, "templateSuffix": suffix, "ruleSet": {"appliedDisjunctively": False, "rules": rules}}})


# ---------------------------------------------------------------- main
def run(sheet_path, cfg, sheet=None, out=None, apply_changes=False, publish=False):
    import openpyxl
    wb = openpyxl.load_workbook(sheet_path, data_only=True, read_only=False)
    ws = wb[sheet] if sheet else wb.worksheets[0]
    hr = find_header_row(ws, cfg)
    headers = [("" if c.value is None else str(c.value)) for c in ws[hr]]
    mapping, unmapped = map_columns(headers, cfg)
    for need in ("model", "finish", "fob"):
        if need not in mapping:
            raise SystemExit("No column for `%s` found. Headers seen: %s" % (need, headers))
    rows = read_rows(ws, hr, mapping)
    products, skipped, unknown = build_products(rows, cfg, publish=publish)
    out = pathlib.Path(out or (ROOT / "data/imports" / datetime.date.today().isoformat()))
    report = write_outputs(out, products, skipped, unknown, mapping, unmapped, headers, cfg, ws.title, publish if apply_changes else None)
    results = apply(products, cfg, publish) if apply_changes else []
    return products, skipped, report, results


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sheet"); ap.add_argument("--sheet", dest="sheet_name"); ap.add_argument("--out")
    ap.add_argument("--config", default=str(CFG_PATH))
    ap.add_argument("--apply", action="store_true", help="write to Shopify (drafts)"); ap.add_argument("--publish", action="store_true", help="with --apply: set ACTIVE and publish products that pass the gate")
    a = ap.parse_args()
    cfg = json.loads(pathlib.Path(a.config).read_text())
    if cfg["brand"]["name"].endswith("_TBC") and a.apply:
        raise SystemExit("Set brand.name and supplier.name in scripts/import_config.json before --apply")
    products, skipped, report, results = run(a.sheet, cfg, a.sheet_name, a.out, a.apply, a.publish)
    print(report.read_text())
    for r in results:
        print(*r)
