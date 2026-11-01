# Google Merchant Center fixes (30 Oct 2026)

Done from the Merchant Center "product attribute improvements" report. The report itself needs the owner's Google login; the fixes below are the store-side gaps it flags, checked against the live catalogue (1,205 live products, 3,945 variants).

## Fixed

- **75 products with photos were not on the Google & YouTube channel** (new Raimondi, Sigma, BAT, Baron, Roberts, NICLIS, Maxisil and Panther lines added since the September audit). All published to Google. The four MELA vanity add-on products (stone top, basin upgrade, top cutting, kickboard) were left off on purpose, they are options, not products.
- **Colour sent to Google on 2383 variants** (334 products). Google reads a variant option only when it is called "Color"; the store uses "Colour", "Finish" and "Insert Colour", so the value is now also written to the Google `color` field on each variant (Chrome, Matt Black, Brushed Nickel, Mill Finish, Bright Silver, and so on). Values that are a texture not a colour (Matt, Gloss, Satin, Polished, Structured, Lappato) were skipped. Google uses colour for filtering and for the "attribute improvements" score.
- **SKUs on the last variants without one** (Google uses the SKU as the MPN). Celine Bottle Trap 32mm Brushed Nickel: ETB186.BN (sibling pattern). MELA RONDO Wall Spout & Mixer Set: KIT.RON.WS.CH / .BK / .BN / .BB. MELA PALCO Wall Spout & Mixer Set: KIT.PAL.WS.CH / .BK / .BN / .GM / .BB. These two sets are ETS bundles, so the KIT.* convention already used for vanity kits applies.

## Still open (owner)

1. **17 products have no photo but are on the Google channel.** Google disapproves them. Removing a product from a channel is blocked for this tool, so in Shopify: Products → filter "Google & YouTube" → select these → More actions → Exclude from sales channel → Google & YouTube. Or add a photo.
   - BATSEAL De-Scale Phosphoric Acid Cleaner
   - Sigma 90DG Swivel Measurement Bar
   - Sigma 8AEP2 Kera-Cut Extension Bar 50cm
   - Sigma 64B2 Non-Slip Magnetic Mat
   - Sigma 421 Carriage Kit (2 Wheel Sets with Slab Support and Angle Support)
   - Sigma 402 Work Bench Storage Hooks for Kera-Cut
   - Sigma 90NE Swivel Measurement Bar 64cm-0-64cm
   - Sigma 37C Table Fixing Kit
   - Sigma 196725 Rubber Foot
   - Sigma 17A Extension Bar 500mm
   - Sigma 14G Kera-Cut Spare Scoring Wheel 12mm
   - Sigma 108362 M8 Square Nut for Locking Bolt
   - F300 Mixer Paddles Set (3)
   - E120 Replacement Power Cable 2m with Plug
   - Recessed Flange Adapter 100 x 100mm
   - Flange 50mm Socket Weld
   - Retro Cove Joiner – 70mm
2. **19 more products have no photo** and are already off Google. They still sell poorly on the website without one.
   - BAT Pro Folding Utility Knife Spare Blade Set (10 pce) - suits BAT Pro folding knife
   - BAT Utility Knife
   - BAT Floor Scraper 300mm Replacement Blade
   - BAT 20 Ltr Bucket
   - BAT 20 Ltr Bucket Lid
   - Panther 20 Ltr Bucket
   - Panther 20 Ltr Bucket Lid - Orange
   - BAT Luxe Square Inspection Drain - 100mm Outlet
   - BATSEAL Matt Look Solvent Based Sealer
   - BATSEAL Silcopel Solvent Based Sealer
   - BATSEAL Wet Look Solvent Based Sealer
   - BATSEAL Pristine - Water Based Sealer - 1 Ltr
   - BATSEAL Eversol Solvent
   - Raimondi Easymove LFT Carrying Bar Set with 4 RV175 Suction Cups
   - Raimondi Rai-Cut Grooving Tool Spare Blade
   - Raimondi Lupetto 11 Row Roller Plate Assembly
   - Raimondi Lupetto Flat Vibrating Plate
   - Raimondi 300W / 42V Transformer for Terranova
   - Raimondi Ipertitina Splash Guard Skirt
3. **Barcodes (GTIN): 2,489 of 3,945 variants have none.** Google still lists them with brand + MPN (vendor + SKU) but ranks them lower. Needs supplier barcode lists (MELA, BAT, Raimondi, Sigma, RLA).
4. **Two MELA MORRIS curved panel products (895mm and 995mm) have no SKU.** Their codes (MORRIS.895*2000.CURVED, MORRIS.995*2000.CURVED) are already used by the variants of "MELA MORRIS Frameless Shower Panel", so the standalone products are duplicates. Delete one or the other.
5. **Read the Merchant Center report directly** next time: select the Merchant Center account in HYPD at https://app.hypd.ai/sources, or export the report as CSV.

## Checked, no problem

- Every live product has a Google product category and a description over 100 characters.
- Every variant has a weight; brand (vendor) and product type are set on all products.
