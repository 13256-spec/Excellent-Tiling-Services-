# Supplier cost check, 12 Oct 2026

Owner's instruction (12 Oct 2026): use the supplier price files he sent (BAT Tools Book 1, Project Trims Book 1, Trims Book 1 and the Raimondi price list, all May 2026; the 2026 SILVER trade-discount sheet; the 2025 MELA catalogue) to double-check every public and trade price, and stay cheaper than other sellers.

What was done: every Shopify unit cost was compared with the files, then the pricing rules (`reprice_2026_10_11.py`) were re-run on a fresh export with today's Bathroom City and B&B Hardware prices. **No price, cost or trade band needed to change.** Master list: `store-pricing-2026-10-12.csv` (same prices as 11 Oct, today's competitor prices).

## Costs by range

| Range (vendor) | Active variants | Cost checked against a supplier file | Cost source |
|---|---|---|---|
| BAT Trims | 1351 | 1171 | Project Trims Book 1 + Trims Book 1 (May 2026) |
| BAT | 423 | 405 | Tools Book 1 + Trims Book 1 (May 2026) |
| Raimondi | 293 | 293 | Raimondi price list (May 2026) |
| Panther | 26 | 24 | Tools Book 1 |
| NICLIS | 25 | 25 | Tools Book 1 |
| Washboy | 9 | 9 | Tools Book 1 |
| Atika | 14 | 14 | Tools Book 1 |
| ADA Instruments | 4 | 4 | Tools Book 1 |
| MELA | 599 | 599 | Bathroom City live list × (1 − SILVER discount) ÷ 1.1, cross-checked with the 2025 MELA catalogue |
| Roberts Designs | 715 | 0 | cost already in Shopify (no file yet) |
| Maxisil | 120 | 0 | cost already in Shopify (no file yet) |
| Excellent Tiling Services | 89 | 89 | Eternity price list 5 Oct 2026 (checked 5 Oct) |
| Sigma | 56 | 0 | cost already in Shopify (no file yet) |
| Siri | 17 | 0 | cost already in Shopify (no file yet) |
| Baron | 10 | 0 | cost already in Shopify (no file yet) |
| Barwalt | 2 | 0 | cost already in Shopify (no file yet) |
| RLA | 1 | 0 | cost already in Shopify (no file yet) |
| Click | 1 | 0 | cost already in Shopify (no file yet) |

Total 3755 active variants; 2633 have a cost confirmed by a supplier file.

### BAT, BAT Trims, Raimondi, Panther, NICLIS, Washboy, Atika, ADA

1948 variants carry exactly the book's net (ex GST) price (`bat-cost-check-2026-10-12.csv`: store cost, book cost, price). Not in any book, so still on the cost that was in Shopify: cove-trim internal/external corners CTEC/CTIC (98 variants, the book only has a placeholder line at $18.20), BSN stair nosings (76), APC60 end caps (16), SA half-rounds (9), the ETS-HW own-coded items (7), SynSafe Acid 20 L (no cost at all). These need BAT Trims Book 2 or the owner's last invoice.

### MELA

The cost basis is Bathroom City's live list price × (1 − SILVER discount) ÷ 1.1; Bathroom City is the supplier. The 2025 catalogue was used as a cross-check (`mela-catalogue-check-2026-10-12.csv`, every active variant):

- 479 variants: Bathroom City list = catalogue RRP.
- 97 variants: Bathroom City's live list is above the 2025 catalogue (CLARK, CLASSIC and BRITTANY vanities +$50–$200, MORRIS screens +$20–$50, FLOVA/PALCO shower sets and RONDO pull-out mixer +$20–$50). The higher live list stays as the cost basis, so these prices are the safe ones. If the owner's MELA invoices show the catalogue prices still apply, re-cost them: prices would drop about 5%.
- 23 variants Bathroom City doesn't list (hoses, shower heads, MORRIS brackets, VINA mirrors, FLOVA 800 rails, RONDO gooseneck, SURI 600 LED...): their cost was an estimate from the SILVER discount off our price; the catalogue RRP equals that price in every case, so the estimate stands as a confirmed cost.
- 0 variants with a cost below what the catalogue implies; 0 not found (vanities, basins, mirrors, mirror cabinets and toilets were read off the catalogue pages by eye because their names are pictures).

Bathroom City list above the 2025 catalogue, by product:

| Product | Variants | Bathroom City list | 2025 catalogue RRP |
|---|---|---|---|
| MELA BRITTANY 1200 Oak Fluted Curved Wall Hung Vanity with 2 Drawers | 1 | $2,099 | $1,999 |
| MELA BRITTANY 600 Matt White Fluted Wall Hung Vanity with 2 Drawers | 1 | $1,399 | $1,299 |
| MELA CLARK 1050 Wall Hung Vanity with 2 Drawers & Side Shelves | 4 | $1,499 | $1,399 |
| MELA CLARK 1200 Wall Hung Vanity with 2 Drawers & Dual Side Shelves | 4 | $1,699 | $1,599 |
| MELA CLARK 1200 Wall Hung Vanity with 2 Drawers & Single Side Shelves | 4 | $1,699 | $1,599 |
| MELA CLARK 1200 Wall Hung Vanity with Drawers | 4 | $1,499 | $1,399 |
| MELA CLARK 1500 Double Wall Hung Vanity with 4 Drawers & Centre Shelves | 4 | $2,399 | $2,199 |
| MELA CLARK 1500 Double Wall Hung Vanity with Doors | 4 | $1,899 | $1,749 |
| MELA CLARK 1500 Double Wall Hung Vanity with Doors & Drawers | 4 | $2,099 | $1,949 |
| MELA CLARK 1500 Double Wall Hung Vanity with Drawers | 4 | $2,299 | $2,099 |
| MELA CLARK 1500 Wall Hung Vanity with 2 Drawers & Dual Side Shelves | 4 | $2,099 | $1,949 |
| MELA CLARK 1800 Double Wall Hung Vanity with 4 Drawers | 3 | $2,499 | $2,299 |
| MELA CLARK 1800 Double Wall Hung Vanity with 4 Drawers & Centre Shelves | 1 | $2,499 | $2,399 |
| MELA CLARK 1800 Double Wall Hung Vanity with 4 Drawers & Centre Shelves | 3 | $2,599 | $2,399 |
| MELA CLARK 600 Wall Hung Vanity with 2 Drawers | 4 | $999 | $949 |
| MELA CLARK 600 Wall Hung Vanity with Doors | 1 | $749 | $699 |
| MELA CLARK 750 Wall Hung Vanity with 2 Drawers | 4 | $1,099 | $1,049 |
| MELA CLARK 750 Wall Hung Vanity with Doors | 4 | $899 | $849 |
| MELA CLARK 900 Wall Hung Vanity with 2 Drawers | 4 | $1,199 | $1,149 |
| MELA CLARK 900 Wall Hung Vanity with 2 Drawers & Side Shelves | 4 | $1,399 | $1,299 |
| MELA CLASSIC 1200 Matt White Wall Hung Vanity with 2 Drawers | 3 | $1,649 | $1,499 |
| MELA CLASSIC 600 Matt White Wall Hung Vanity with 2 Drawers | 3 | $1,199 | $1,049 |
| MELA CLASSIC 750 Matt White Wall Hung Vanity with 2 Drawers | 3 | $1,299 | $1,149 |
| MELA CLASSIC 900 Matt White Wall Hung Vanity with 2 Drawers | 3 | $1,399 | $1,249 |
| MELA FLOVA Combination Shower Set with Rail | 1 | $549 | $499 |
| MELA MORRIS Frameless Corner Shower Screen | 1 | $1,199 | $1,099 |
| MELA MORRIS Frameless Corner Shower Screen | 1 | $1,249 | $1,199 |
| MELA MORRIS Frameless Corner Shower Screen | 1 | $1,099 | $1,049 |
| MELA MORRIS Frameless Corner Shower Screen | 1 | $1,149 | $1,099 |
| MELA MORRIS Frameless Corner Shower Screen | 1 | $1,049 | $999 |
| MELA MORRIS Frameless Shower Panel | 1 | $569 | $549 |
| MELA MORRIS Frameless Shower Panel | 1 | $359 | $339 |
| MELA MORRIS Frameless Shower Panel | 1 | $369 | $349 |
| MELA MORRIS Frameless Shower Panel | 1 | $379 | $359 |
| MELA MORRIS Frameless Shower Panel | 1 | $419 | $399 |
| MELA MORRIS Frameless Shower Panel | 1 | $439 | $399 |
| MELA MORRIS Frameless Shower Panel | 1 | $429 | $409 |
| MELA MORRIS Frameless Shower Panel | 1 | $449 | $409 |
| MELA PALCO / RONDO Hand Shower Set with Rail | 1 | $379 | $329 |
| MELA RONDO Square Pull-Out Sink Mixer | 1 | $419 | $399 |
| MELA RONDO Square Pull-Out Sink Mixer | 1 | $339 | $319 |
| MELA RONDO Square Pull-Out Sink Mixer | 1 | $449 | $429 |
| MELA RONDO Square Pull-Out Sink Mixer | 1 | $389 | $369 |

## Prices and trade bands re-run today

- 3755 active variants, 57 price changes needed.
- 666 variants have a competitor price today (Bathroom City or B&B Hardware); 592 are cheaper than it. The rest sit at our 20% profit floor because the competitor is selling below it (table below).
- Trade bands (products): 25% × 322, 20% × 223, 15% × 227, 10% × 20, 5% × 127, 0% × 2. The `ets.trade_band` metafield and the `trade-list-N` collections match the rules on every one of the 921 products.
- Two MORRIS curved panels (895 and 995 × 2000) are no longer on Bathroom City; prices kept.

## For the owner

### Competitor sells below our profit floor (we stay at the floor)

| Item | Our price | Profit % | Competitor | Their price |
|---|---|---|---|---|
| MELA PALCO/RONDO Soap Holder / Gun Metal | $130.00 | 20.5% | Bathroom City | $111.30 |
| MELA PALCO/RONDO Toilet Brush Holder / Gun Metal | $130.00 | 20.5% | Bathroom City | $111.30 |
| MELA FLOVA Combination Shower Set without Rail / Chrome | $300.00 | 20.2% | Bathroom City | $229.00 |
| MELA FLOVA Combination Shower Set without Rail / Matt Black | $375.00 | 20.2% | Bathroom City | $329.00 |
| MELA FLOVA Combination Shower Set with Rail / Chrome | $412.00 | 20.0% | Bathroom City | $299.00 |
| MELA FLOVA Combination Shower Set with Rail / Matt Black | $450.00 | 20.1% | Bathroom City | $399.00 |
| MELA PALCO / RONDO Hand Shower Set without Rail / Gun Metal | $202.00 | 20.1% | Bathroom City | $188.30 |
| MELA PALCO / RONDO Combination Shower Set without Rail / Chrome | $300.00 | 20.2% | Bathroom City | $229.00 |
| MELA PALCO / RONDO Combination Shower Set without Rail / Matt Black | $375.00 | 20.2% | Bathroom City | $329.00 |
| MELA PALCO / RONDO Combination Shower Set without Rail / Gun Metal | $525.00 | 20.1% | Bathroom City | $489.30 |
| MELA PALCO / RONDO Combination Shower Set with Rail / Chrome | $412.00 | 20.0% | Bathroom City | $299.00 |
| MELA PALCO / RONDO Combination Shower Set with Rail / Matt Black | $450.00 | 20.1% | Bathroom City | $399.00 |
| MELA PALCO Wall Mixer with Diverter / Gun Metal | $262.00 | 20.1% | Bathroom City | $244.30 |
| MELA PALCO / RONDO Free Standing Bath Spout / Gun Metal | $345.00 | 20.2% | Bathroom City | $321.30 |
| MELA PALCO / RONDO Free Standing Bath Mixer / Gun Metal | $555.00 | 20.1% | Bathroom City | $517.30 |
| MELA PALCO Gooseneck Kitchen Mixer / Gun Metal | $375.00 | 20.2% | Bathroom City | $349.30 |
| MELA RONDO Gooseneck Sink Mixer / Gun Metal | $225.00 | 20.3% | Bathroom City | $209.30 |
| MELA RONDO Square Gooseneck Sink Mixer / Gun Metal | $225.00 | 20.3% | Bathroom City | $209.30 |
| MELA CASSA Pull Out Sink Mixer with Black Hose / Chrome | $300.00 | 20.2% | Bathroom City | $199.50 |
| MELA RONDO Square Pull-Out Sink Mixer / Chrome | $255.00 | 20.2% | Bathroom City | $135.60 |
| MELA RONDO Square Pull-Out Sink Mixer / Matt Black | $292.00 | 20.1% | Bathroom City | $155.60 |
| MELA RONDO Square Pull-Out Sink Mixer / Brushed Nickel | $315.00 | 20.2% | Bathroom City | $167.60 |
| MELA RONDO Square Pull-Out Sink Mixer / Gun Metal | $337.00 | 20.1% | Bathroom City | $179.60 |
| MELA FLOVA Bath Towel Shelf / Chrome | $154.00 | 20.2% | Bathroom City | $94.50 |
| MELA FLOVA Bath Towel Shelf / Matt Black | $195.00 | 20.3% | Bathroom City | $119.50 |
| MELA FLOVA Bath Towel Shelf / Brushed Nickel | $219.00 | 20.2% | Bathroom City | $134.50 |
| MELA PALCO / RONDO Bath Towel Shelf / Chrome | $154.00 | 20.2% | Bathroom City | $94.50 |
| MELA PALCO / RONDO Bath Towel Shelf / Matt Black | $195.00 | 20.3% | Bathroom City | $119.50 |
| MELA PALCO / RONDO Bath Towel Shelf / Brushed Nickel | $219.00 | 20.2% | Bathroom City | $134.50 |
| MELA PALCO / RONDO Bath Towel Shelf / Gun Metal | $243.00 | 20.0% | Bathroom City | $149.50 |
| MELA PALCO / RONDO Bath Towel Shelf / Brushed Brass | $243.00 | 20.0% | Bathroom City | $149.50 |
| MELA PALCO / RONDO 600 Single Towel Rail / Gun Metal | $138.00 | 20.4% | Bathroom City | $118.30 |
| MELA PALCO / RONDO 600 Double Towel Rail / Gun Metal | $162.00 | 20.2% | Bathroom City | $139.30 |
| MELA PALCO / RONDO 800 Single Towel Rail / Gun Metal | $162.00 | 20.2% | Bathroom City | $139.30 |
| MELA PALCO / RONDO Hand Towel Rail / Gun Metal | $122.00 | 20.6% | Bathroom City | $104.30 |
| MELA PALCO / RONDO Shelf Holder / Gun Metal | $203.00 | 20.3% | Bathroom City | $174.30 |
| MELA CALLA Free Standing Bath / 1500mm | $1,200.00 | 20.1% | Bathroom City | $999.00 |
| MELA CALLA Free Standing Bath / 1700mm | $1,275.00 | 20.0% | Bathroom City | $1,099.00 |
| MELA MAYA Free Standing Bath / 1500mm | $1,200.00 | 20.1% | Bathroom City | $1,099.00 |
| MELA MAYA Free Standing Bath / 1700mm | $1,275.00 | 20.0% | Bathroom City | $1,199.00 |
| MELA TAYLOR Free Standing Bath / 1500mm | $1,275.00 | 20.0% | Bathroom City | $1,179.00 |
| MELA TAYLOR Free Standing Bath / 1700mm | $1,350.00 | 20.0% | Bathroom City | $1,279.00 |
| MELA MIZO Back to Wall Bath / 1700mm | $2,199.00 | 20.0% | Bathroom City | $1,499.00 |
| MELA NOOK Corner Bath (Right) / 1700mm | $1,799.00 | 20.0% | Bathroom City | $1,299.00 |
| MELA NOOK Corner Bath (Left) / 1700mm | $1,799.00 | 20.0% | Bathroom City | $1,299.00 |
| MELA KASTEN Inset Bath / 1525mm | $399.00 | 20.0% | Bathroom City | $399.00 |
| MELA KASTEN Inset Bath / 1675mm | $479.00 | 20.0% | Bathroom City | $479.00 |
| MELA CALLA Rimless Toilet Suite | $450.00 | 20.1% | Bathroom City | $399.00 |
| MELA PASSA Rimless Toilet Suite Extra Height | $450.00 | 20.1% | Bathroom City | $399.00 |
| MELA ELLIS Wall Faced Rimless Toilet Suite | $675.00 | 20.1% | Bathroom City | $599.00 |
| MELA FELLI Wall Faced Rimless Toilet Suite | $675.00 | 20.1% | Bathroom City | $599.00 |
| MELA MIA 450 Framed Oval Mirror / Gun Metal | $375.00 | 20.2% | Bathroom City | $199.50 |
| MELA SURI Framed Round Mirror / 700mm / Gun Metal | $328.00 | 20.2% | Bathroom City | $174.50 |
| MELA SURI Framed Round Mirror / 800mm / Gun Metal | $375.00 | 20.2% | Bathroom City | $199.50 |
| MELA SURI Framed Round Mirror / 900mm / Gun Metal | $421.00 | 20.0% | Bathroom City | $224.50 |
| MELA ZOE 600 Framed Arch Mirror / Gun Metal | $375.00 | 20.2% | Bathroom City | $199.50 |
| MELA MARCIE 440 Above Counter Basin | $175.00 | 20.4% | Bathroom City | $125.30 |
| Sigma 19N Square 260mm | $61.90 | 20.0% | B&B Hardware | $59.95 |
| Sigma Tile Cutter ART 4FN – 155cm | $2,281.55 | 20.0% | B&B Hardware | $1,750.00 |
| Sigma Tile Cutter ART 4EN – 125cm | $1,763.75 | 20.0% | B&B Hardware | $1,499.00 |
| Sigma Tile Cutter ART 4DU – 103cm | $1,050.80 | 20.0% | B&B Hardware | $945.00 |
| Sigma Tile Cutter ART 4BU – 70cm | $825.55 | 20.0% | B&B Hardware | $745.00 |
| Sigma Handle ART 24N for ART 4 Push series | $275.45 | 20.0% | B&B Hardware | $275.00 |
| Barwalt KN-1 Ultralight Knee Pad | $51.40 | 20.1% | B&B Hardware | $49.95 |
| Raimondi Zoe Electric Wet Saw 3HP / Zoe 85A | $4,798.75 | 20.0% | B&B Hardware | $4,389.00 |

65 variants.

### Below the floor, kept for the owner's decision

| Item | Our price | Needs | Cost ex GST | Competitor | Their price |
|---|---|---|---|---|---|
| MELA KORI Back to Wall Bath / 1500mm | $1,599.00 | $1600.00 | $1,162.91 | Bathroom City | $1,099.00 |
| MELA KORI Back to Wall Bath / 1700mm | $1,699.00 | $1700.00 | $1,235.64 | Bathroom City | $1,199.00 |
| MELA MIZO Back to Wall Bath / 1500mm | $2,099.00 | $2100.00 | $1,526.55 | Bathroom City | $1,399.00 |
| MELA NOOK Corner Bath (Right) / 1300mm | $1,699.00 | $1700.00 | $1,235.64 | Bathroom City | $1,199.00 |
| MELA NOOK Corner Bath (Right) / 1500mm | $1,699.00 | $1700.00 | $1,235.64 | Bathroom City | $1,199.00 |
| MELA NOOK Corner Bath (Left) / 1300mm | $1,699.00 | $1700.00 | $1,235.64 | Bathroom City | $1,199.00 |
| MELA NOOK Corner Bath (Left) / 1500mm | $1,699.00 | $1700.00 | $1,235.64 | Bathroom City | $1,199.00 |
| Sigma Tile Cutter ART 4CU – 84cm | $800.00 | $900.65 | $655.00 | B&B Hardware | $799.00 |
| Baron E120 Forced Action Mixer | $4,799.99 | $5018.75 | $3,650.00 | B&B Hardware | $4,295.00 |

### No cost recorded (price left alone, trade band 5%)

- BAT Eco SynSafe Acid / 20 L at $485.00
- RLA Quick Set Liquid Additive – Cement Accelerator 5 L / Default Title at $47.00
- Click Heavy Duty Powerblock – 4 Outlet with RCBO Protection / Default Title at $75.00

The seven MELA baths are $1 under the floor only because the floor rounds up to the next dollar (profit 19.99%); Bathroom City clears them far lower, so there is nothing to undercut. Sigma ART 4CU and Baron E120: B&B Hardware sells below our floor; to beat them we would earn 11% and 12% instead of 20% – the owner's call.

## Still missing

- Roberts Designs price list (Roberts Designs, Maxisil, Sigma, Siri, Baron, Barwalt: 920 variants priced on the costs already in Shopify; one Roberts item, Expansion Aluminium Trim 3 m, has the same cost on every size and is flagged COST CHECK).
- BAT Trims Book 2 (or last invoice) for the cove corners, stair nosings, APC60 caps, half-rounds and ETS-HW items.
- A cost for BAT Eco SynSafe Acid 20 L, RLA Quick Set Liquid Additive 5 L and the Click Heavy Duty Powerblock.
- SILVER sheet has no line for back-to-wall and corner baths (KORI, MIZO, NOOK): 20% is assumed.

