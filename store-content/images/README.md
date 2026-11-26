# Product photo white space (26 Oct 2026)

Supplier product photos (MELA from Bathroom City above all) come as 2000 x 2000 px files with the product in the middle
and white all round it, so on the product page the gallery showed a small product in a huge white square.

`scan_whitespace.py` reads the public products.json feed, downloads every product image at 300 px and measures how much of
the frame the product actually fills (anything not near-white). Result on 26 Oct 2026: 2,739 images; 695 of them (281
products) fill less than 70% of the frame. `crop-plan-all-2026-10-26.json` has a square crop region for each of those,
centred on the product with a 7% margin.

Applied so far (`crop-applied-toilets-2026-10-26.json`): the Toilets collection, 42 images on 10 products (MELA MIRO,
ELIO, AMIO, ELLIS, FELLI, the three paper holders, the two brush holders). Method, all through the Admin API with no
re-upload: a new media item is created from the original's CDN URL with Shopify's `crop=region` parameters, variant
swatches are re-linked to the new media, and the old media is deleted. The original full-frame file is first copied into
Content > Files as `original-<name>` (alt text "ORIGINAL before crop: ...") so any crop can be undone. Images whose crop
would come out under 800 px (the flush buttons, the Clarice photo, the Caleb Aria photo) are left alone.

The remaining 271 products (653 images) are in the plan but not applied; the owner decides.

The product page gallery itself was tidied in the theme (`assets/ets-refine.css`, draft "ETS 2026 - Product gallery"):
framed white photo box with rounded corners, gallery column capped at 620 px on desktop so the details column gets its
share, and the frame height capped so the photo is never cut off at the bottom of the screen.

# Maxisil Wet Area Silicone: a photo and colour code for every colour (23 Nov 2026)

Product 8403247857727 had 41 colours but only 5 colour photos, none linked to a colour. Now every colour has its own
tube-and-colour photo (36 added from the Roberts Designs site, same series as the 5 already there) and picking a colour
shows its photo. The colour names now carry the Maxisil code, for example "White A2", "Mocha A60", "Matte Black A85",
so customers can search or ask by code. Codes were checked against maxisil.com.au. Photo alt text reads
"Maxisil Wet Area Silicone A2 White". No price, SKU or stock change.

`maxisil-wet-area-colours-2026-11-23.json` lists each variant, SKU, old name, code, new name, photo and source URL. To
undo the names, set each option value back to the `colour` field.

The trade price list PDF still prints the old colour names until `b2b_price_list_2026_11.py` is next rerun. Not done:
Natural Stone (N codes) and Pool (P codes) have the photos already but they are not linked to colours or coded.
