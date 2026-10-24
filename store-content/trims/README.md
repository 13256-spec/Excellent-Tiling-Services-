# BAT trims checked against BAT's website and price books (24 Oct 2026)

Prompted by the owner holding a bag labelled "BAT Mosaic Corner Angle, Linished Bright Silver, 10.5mm x 3000mm,
Re-Order Code MCA-10-3-LSP, barcode 9325465016702" and not being sure which listing it matched.

**That bag is** `BAT Mosaic Corner Angle – 3m Lengths (Square Edge)` → **10.5mm / Linished Silver** (SKU
MCA-10-3-LSP). BAT's website and price book both call this finish "Linished Silver"; only the bag label says
"Linished Bright Silver". The barcode from the bag is now on that variant.

## How it was checked

- Every active BAT trim variant (46 products, about 1,370 variants) was matched by code to BAT's Premium Trims
  Book (Aug 2026) and Project Trims Book (May 2026), and each product to its battrims.com page (87 pages,
  colour and size tables in `bat-website-attributes-2026-10-24.json`).
- BAT's website rounds sizes down (it lists "4mm", "12mm" for profiles the bags and price books call 4.5mm and
  12.5mm), so sizes were checked against the price book and bag labels, and colours against the website.

## Fixed in Shopify (labels only; codes, prices and stock unchanged)

- **"Black" renamed "Gloss Black"** on 17 products (90 variants). BAT's codes ending BK/BKP are Gloss Black on the
  website, in the price books and on the labels; "Black" was easy to confuse with Matt Black. The stairnosing's
  rubber insert colour "Black" was left alone.
- **Size labels corrected** where every BAT code in the family agrees:
  - Aluminium Tiling Angle: 23mm → 23.5mm (AA-23-3-*), 25.5mm → 25mm (AA-25-3-*)
  - Notched Aluminium Angle: 23mm → 23.5mm (AA-23-3-N)
  - Decorative Y Section: 12mm → 12.5mm (BDY-12-3-*)
  - Half Round, Brass and Chrome: 12mm → 12.5mm (HRT-12-3B, CPHRT-12-3)
  - Marine Grade 316 Stainless Angle: 17.5mm → 17mm (SSAMG-17-3)
  - BATEX Aluminium: 17mm → 17.5mm (BTXA-176-3-*, BTXA-1710-3-*)
- **Barcode** 9325465016702 added to MCA-10-3-LSP.

## Checked and correct (no change)

- Mosaic Corner Angle: same 13 finishes and 6 sizes as BAT.
- Project Aluminium Angle (PA-*) and Project Mosaic Corner Angle (PMCA-*): every code matches the Project Trims
  Book; colours match except "Bronze Ash" on PMCA, which is in the book but missing from BAT's web page.
- Cove trim corners (CTEC/CTIC): sizes and colours match BAT's website.

## Left for the owner

- **APC 60 Internal corners** (APC60-IC-*, 7 variants on "Cove Trim Corners"): BAT's website only has an APC 60
  External corner and neither price book lists an internal one. Confirm with BAT before selling these.
- **Notched angle AA-15-3-N**: price book says 14mm, BAT's website lists 15mm. Left as 15mm; check a label.
- **BATEX Brass BTXB-1110**: the book says "11 x 10mm" for black and "10 x 10mm" for grey under the same code.
  Left as listed.
- Colours BAT makes that we don't list (for example Bright Gold and Matt Black Splash Trim, Gloss Black and Grey
  MORTARLOC) are in `colour-compare-2026-10-24.json` if you want to add them.
- Product photos don't change when a finish is picked on most trim listings, and BAT doesn't publish per-finish
  photos. The variant SKU (BAT re-order code) is in the page data but not shown to shoppers; showing it would let
  anyone match a bag's re-order code to the listing.
