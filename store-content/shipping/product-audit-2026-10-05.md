# Product shipping audit (5 Oct 2026)

Every variant in the store (1,685, of which 1,572 active) was pulled live from Shopify: price, shipping weight, delivery profile and status. The full list, with what each one costs to ship to Australia, NZ and US/UK/UAE and any warnings, is in `product-shipping-audit-2026-10-05.csv`.

## Checks that passed
- Every active variant has a shipping weight (none at 0 kg).
- Shopify weights match `product-weights.csv` for every variant in it.
- Every item that fits Australia Post is in a parcel profile; every item that doesn't is in "Local delivery or pickup", apart from the 3 fixed below.

## Fixed today
| Problem | Fix |
| --- | --- |
| Maxisil grout 5 kg ($30) charged $79 and 10 kg ($47) charged $99. It sat in the bulky (cubic-weight) profile, but grout is a dense, compact box. | 20 grout variants, Primer 1218 and the pallet wrap moved to the General (small items) profile. Grout now ships for $39 (5 kg) and $59 (10 kg). |
| Heavy Duty Floor Scrapers come in 125 cm boxes, longer than Australia Post's 105 cm limit. | Moved to Perth delivery or pickup. |
| BAT Eco SynSafe Acid 20 L: 22 kg of acid in the parcel profile. | Moved to Perth delivery or pickup. |
| Small-item prices were padded above what Australia Post charges. | New Australia-wide (WA included) prices: up to 1 kg $15, 1–3 kg $20, 3–5 kg $29, 5–10 kg $39, 10–22 kg $59, 22–44 kg $109, 44–100 kg $179. Free from $1,000. |
| International 5–10 kg band was A$279. | Reduced to smaller steps (see shipping README). |

## Competitor delivery (web check, 5 Oct 2026)
| Store | Free delivery from | Under that |
| --- | --- | --- |
| Bathroom City (Perth, same MELA range) | $1,000 | Perth metro by quote; interstate not listed |
| Yabby | $1,000 (bulky items excluded) | |
| The Tapware Outlet | $500 | |
| The Blue Space | $500 (metro) | |
| MYTAP | $150 | |
| Designer Bathware | $100 on tapware | |
| Adheseal (grout, silicone) | | $17.95 + GST flat, metro only, bulky excluded |
| RJ Bathroom | Perth $3,200, Sydney $2,000 | |

ETS: $15 (under 1 kg) / $20 (1–3 kg) for small items anywhere in Australia, WA included, cheaper than Adheseal's flat $19.75 incl. GST. Free over $1,000, the same as Bathroom City and Yabby. Tapware-only stores (MYTAP, Designer Bathware) give free delivery from $100–150. Matching that would cost $15–30 an order.

## Still open (owner's call)
- **626 active variants are Perth delivery or pickup only** (tiles, vanities, baths, toilets, screens, 2.5–3 m trims). Interstate customers can't check out with them. A courier that takes long parcels (e.g. Couriers Please, Aramex, Sendle Pro) would open up trims; a freight account (e.g. Border Express, TNT) would open up vanities and baths.
- **Dangerous goods:** Maxisil Primers 1215–1218 and BAT acid can't go by air, so not by Express Post or internationally. Australia Post road parcels need a dangerous-goods declaration. Don't post these overseas; refund or contact the customer if one is ordered.
- **47 tile variants added after 28 Sep** have no box size recorded (weights 15–22 kg per m² look right). They're Perth delivery only, so this doesn't change checkout.
- **165 cheap items** (spacers, brushes, silicone) cost more to deliver alone than the item. That's normal, and customers usually buy several.
- Weights are still estimates. Weighing a few best sellers (a pull-out sink mixer, an 800 mm towel rail, a 10 kg grout bag) would make checkout prices exact.
- Product prices vs competitors weren't part of this check. Use the pricing playbook / pricing agent for that.
- Theme and page text says small items ship "from $20". It's now from $15, so customers pay less than the site says. Update on the next theme edit. The policy text in `store-content/policies/shipping-policy.html` already has the new prices.

## Supplier weight check (5 Oct 2026, later)
- **Bathroom City (MELA):** the public product feed (1,721 products, 936 MELA) has no weights (7 of 258 variants on the first page had any) and no carton sizes in the descriptions. Real MELA weights need the PDF Bathroom City sent the owner. It wasn't in the repo or Drive, and Gmail needed signing in again.
- **Roberts Designs:** the public WooCommerce feed (276 products) has a weight field, but it's 0 or empty for every product and variation, and dimensions are blank. The only weights stated are in the text for the Baron mixers: E120 90 kg, F200 180 kg, F300 180 kg. E120 (was 85) and F300 (was 200) were corrected in Shopify and in `product-weights.csv`. Both are drafts and freight-only, so checkout isn't affected.
- Every other Roberts and MELA weight stays an estimate from the product's size and material.

## Bathroom City documents from the owner (5 Oct 2026, evening)
Checked: `2025 MELA CATALOGUE (FINAL)`, `2026 NEW SILVER TRADE PRICE`, `Product Care and Warranty Procedure`, `Trade Returns Policy`, `MELA Care Guide`. **None has product weights or carton sizes.** The catalogue's text is font-obfuscated (each character shifted by 31) and decodes to names, codes, finishes and RRPs only. Product dimensions are drawings (images). MELA weights stay estimates. Ask the Bathroom City rep for a "product data sheet / logistics sheet" with carton dimensions and gross weights (most suppliers have one for freight).

### MELA prices vs Bathroom City online (live feed, matched by SKU)
- 330 active MELA variants matched. **279 are 5% cheaper than Bathroom City** (the playbook rule).
- **51 are dearer.** Every one is on sale at Bathroom City (compare-at price set): gun-metal accessories, pull-out sink mixers, bath towel shelves, combination shower sets, NOOK/KORI/MIZO/CALLA baths, CALLA/PASSA toilets, MIA/ZOE gun-metal mirrors, MARCIE basin. All 51 are already at the public floor (cost × 1.1 × 1.25), and most of Bathroom City's sale prices are below our cost. Matching them would mean selling at a loss, so prices were not changed. Re-check when their sale ends.
