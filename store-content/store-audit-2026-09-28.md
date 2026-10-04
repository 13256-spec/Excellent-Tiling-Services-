# Store audit (28 Sep 2026)

## Fixed
- **Checkout, small orders:** a $17 order in Maddington now only shows $20 shipping. The $100 local delivery minimum was set by the owner.
- **Australia Post:** the bulky-items rate now uses the owner's own MyPost Business account, with Parcel Post and Express Post on. Live rates still return nothing, so fixed backup prices were added (see `shipping/README.md`). Basins, mirrors, grout and similar items can now be bought Australia-wide.
- **Google product categories:** 492 products had no category, and all now have one. Tile cutters, vanities, basins, tapware, trims, drains, tools and so on are mapped to the Shopify / Google taxonomy. Google uses this to approve and place listings.
- **Google local listings:** local inventory turned off by the owner. This clears the "Missing local inventory data" error.

## Checked, no problem
- Refund, shipping, privacy, terms and contact policies are all present, filled in with ABN, address and phone, and load on the site.
- Store contact email, address and phone are set.
- Every live product has a vendor, a product type, a price above $0 and a shipping weight.
- There are no duplicate barcodes and no compare-at prices below the selling price.
- 427 of 431 live products are on the Google & YouTube channel.

## Still open (owner)
1. **Google Merchant Center "Not approved" on all products:** the Google & YouTube channel showed "Pending initial review". While Google reviews a new store, every product shows as not approved. That usually clears in 3-5 business days (up to 2 weeks). If products are still not approved after that, open Merchant Center → Products → Needs attention and send the top reasons.
2. **26 live products have no photo** (Sigma cutter spare parts, 2 flanges, 2 trim joiners, Maxisil corner nozzles). Google rejects these. Roberts Designs has no photos for them either. Either photograph them, or exclude them from Google: Products → select → More actions → Exclude from sales channel → Google & YouTube.
3. **Barcodes (GTIN):** 1,534 of 1,539 live variants have none. Google still lists products without them, but they rank lower. Ask Roberts/MELA for a barcode list if one is available.
4. **91 variants have no SKU.**
5. **623 live variants have no cost price** (mostly MELA). Profit reports are incomplete until MELA trade prices are entered.
6. **188 live products have short descriptions** (under 100 characters). These are mainly MELA accessories.
7. **Freight items** (tiles, vanities, baths, toilets, shower screens, 3 m trims) still have no delivery option outside Perth. A freight courier is needed for those.
