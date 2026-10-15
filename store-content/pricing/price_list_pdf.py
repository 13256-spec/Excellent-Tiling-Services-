"""PDF price lists from store-pricing-2026-10-03.csv: a retail list, a trade list (retail + trade price) and
an owner-only list that adds the supplier cost and profit. Never send the owner list to customers.

Usage: price_list_pdf.py store-pricing-2026-10-03.csv out_dir
"""
import csv, os, sys
from collections import defaultdict
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("Sans", f"{FONT_DIR}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", f"{FONT_DIR}/DejaVuSans-Bold.ttf"))

NAVY = colors.HexColor("#1f2a44")
STRIPE = colors.HexColor("#f2f4f7")
SECTIONS = [  # (heading, test on product type / vendor)
    ("Tiles", lambda t, v: t == "Tile"),
    ("Vanities & bathroom storage", lambda t, v: "Vanity" in t or t == "Bathroom Tallboy"),
    ("Basins", lambda t, v: "Basin" in t and "Mixer" not in t),
    ("Tapware", lambda t, v: v == "MELA" and any(k in t for k in ("Mixer", "Spout"))),
    ("Showers", lambda t, v: v == "MELA" and any(k in t for k in ("Shower Head", "Shower Arm", "Shower Set", "Hand Shower", "Shower Hose"))),
    ("Baths", lambda t, v: v == "MELA" and t.endswith("Bath")),
    ("Toilets", lambda t, v: "Toilet" in t and "Holder" not in t),
    ("Shower screens", lambda t, v: "Shower Screen" in t or "Shower Panel" in t),
    ("Mirrors & mirror cabinets", lambda t, v: "Mirror" in t),
    ("Kitchen & laundry sinks", lambda t, v: t == "Kitchen Sink"),
    ("Bathroom accessories & wastes", lambda t, v: v == "MELA"),
    ("Tiling hardware, tools & trims", lambda t, v: True),
]


def money(x):
    return f"${float(x):,.2f}"


def section(row):
    return next(h for h, test in SECTIONS if test(row["type"], row["vendor"]))


def unit(row):
    if row["type"] != "Tile":
        return ""
    return " /sheet" if "Mosaic" in row["product"] else " /m²"


def pct(cost, price):
    return f"{(1 - cost / price) * 100:.0f}%" if price else ""


def build(rows, path, mode):
    trade, owner = mode in ("trade", "owner"), mode == "owner"
    title = {"retail": "Price list", "trade": "Trade price list", "owner": "Cost & price list (owner only)"}[mode]
    page = landscape(A4) if owner else A4
    styles = {
        "h1": ParagraphStyle("h1", fontName="Sans-Bold", fontSize=18, leading=22, textColor=NAVY, spaceAfter=4),
        "sub": ParagraphStyle("sub", fontName="Sans", fontSize=8.5, leading=11, textColor=colors.HexColor("#555555")),
        "h2": ParagraphStyle("h2", fontName="Sans-Bold", fontSize=12, textColor=NAVY, spaceBefore=8, spaceAfter=4),
        "cell": ParagraphStyle("cell", fontName="Sans", fontSize=7.5, leading=9),
    }
    story = [
        Paragraph(f"Excellent Tiling Services – {title}", styles["h1"]),
        Paragraph("17A Olga Road, Maddington WA 6109 · 0450 960 543 · contactus@excellenttilingservice.com.au · "
                  "excellenttilingservice.com.au", styles["sub"]),
        Paragraph("Prices in AUD including GST, effective 3 October 2026 and subject to change without notice. "
                  "Tiles are priced per m² (sold to the nearest full box) and mosaics per sheet. Delivery is extra; "
                  "see our shipping policy." + (
                      " Trade prices apply when you're logged in to an approved trade account and don't combine "
                      "with other discounts." if trade else "") + (
                      " CONFIDENTIAL – not for customers. Supplier cost is shown inc GST so it compares directly "
                      "with the selling price. Profit = share of the selling price you keep after the supplier cost "
                      "(both inc GST). Eternity tile costs are the non-pallet price; MELA costs are Bathroom City's "
                      "list price less your SILVER trade discount; other costs are as recorded in Shopify." if owner
                      else ""), styles["sub"]),
        Spacer(1, 4 * mm),
    ]
    groups = defaultdict(list)
    for r in rows:
        groups[section(r)].append(r)
    if owner:
        head = ["Product", "Option", "SKU", "Supplier cost", "Price", "Profit", "Trade", "Trade profit"]
        widths = [mm * w for w in (76, 46, 34, 26, 24, 16, 24, 26)]
    else:
        head = ["Product", "Option", "SKU", "Price"] + (["Trade", "Save"] if trade else [])
        widths = [72 * mm, 40 * mm, 30 * mm, 22 * mm] + ([22 * mm, 12 * mm] if trade else [])
    if mode == "retail":
        widths[0] += 20 * mm
        widths[1] += 14 * mm
    for heading, _ in SECTIONS:
        rs = sorted(groups.get(heading, []), key=lambda r: (r["product"], r["variant"]))
        if not rs:
            continue
        data = [head]
        for r in rs:
            line = [Paragraph(r["product"], styles["cell"]),
                    Paragraph("" if r["variant"] == "Default Title" else r["variant"], styles["cell"]),
                    Paragraph(r["sku"], styles["cell"]),
                    money(r["new_price"]) + unit(r)]
            if owner:
                band = int(r["trade_band"] or 0)
                cost = float(r["cost"]) * 1.1 if r["cost"] else None
                price, tp = float(r["new_price"]), float(r["trade_price"] or 0)
                line = line[:3] + [money(cost) if cost else "–", line[3], pct(cost, price) if cost else "",
                                   money(tp) if band else "–", pct(cost, tp) if cost and band else ""]
            elif trade:
                band = int(r["trade_band"] or 0)
                line += [money(r["trade_price"]) + unit(r) if band else "–", f"{band}%" if band else ""]
            data.append(line)
        t = Table(data, colWidths=widths, repeatRows=1)
        t.setStyle(TableStyle([
            ("FONT", (0, 0), (-1, 0), "Sans-Bold", 8),
            ("FONT", (0, 1), (-1, -1), "Sans", 7.5),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, STRIPE]),
            ("ALIGN", (3, 0), (-1, -1), "RIGHT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ] + ([("FONT", (4, 1), (4, -1), "Sans-Bold", 7.5)] if trade else [])
          + ([("TEXTCOLOR", (3, 1), (3, -1), colors.HexColor("#9a3412"))] if owner else [])))
        story += [Paragraph(f"{heading} ({len(rs)})", styles["h2"]), t]

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Sans", 7)
        canvas.setFillColor(colors.HexColor("#777777"))
        canvas.drawString(15 * mm, 10 * mm, f"Excellent Tiling Services Pty Ltd · {title} · 14 October 2026")
        canvas.drawRightString(page[0] - 15 * mm, 10 * mm, f"Page {doc.page}")
        canvas.restoreState()

    SimpleDocTemplate(path, pagesize=page, leftMargin=12 * mm, rightMargin=12 * mm, topMargin=12 * mm,
                      bottomMargin=16 * mm, title=f"ETS {title} – October 2026",
                      author="Excellent Tiling Services").build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    rows = list(csv.DictReader(open(sys.argv[1])))
    os.makedirs(sys.argv[2], exist_ok=True)
    build(rows, os.path.join(sys.argv[2], "ETS-price-list-2026-10.pdf"), "retail")
    build(rows, os.path.join(sys.argv[2], "ETS-trade-price-list-2026-10.pdf"), "trade")
    build(rows, os.path.join(sys.argv[2], "ETS-OWNER-cost-and-price-list-2026-10.pdf"), "owner")
    print("sections:", {h: sum(section(r) == h for r in rows) for h, _ in SECTIONS})
