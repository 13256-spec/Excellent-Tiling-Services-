# MELA pricing vs Bathroom City (plan, 1 Oct 2026, not yet applied)

`mela-pricing-2026-10-01.csv` has one row per MELA variant: our current price, Bathroom City's
price and list price, the new price, unit cost, margin and any flag. It doubles as the backup of
the old prices.

Rules:
- **Cost** = Bathroom City list price × (1 − SLIVER trade discount for the category).
  Back to wall and corner baths aren't on the sheet, so they use the lowest bath rate (20%).
- **New price** = 5% under Bathroom City's current price, rounded down to the dollar.
- **Floor**: after our own trade discount (5% small / 10% large items) the price must still be
  5% above cost. Where Bathroom City's sale price is below that, we go $1 under them only if
  trade buyers still break even; otherwise we stay at the floor (flagged).
- Prices are never raised. Variants already below target keep their price; 11 that are below
  the floor (CLASSIC vanities, BRITTANY 600, DAVISSON basin) are flagged for review.
- 79 variants have no Bathroom City equivalent and are left alone.

Scripts: `price.py` (plan), `manual.py` + `fuzzy.py` (name matching for items without a SKU).

# Eternity tiles, price list effective 5 Oct 2026 (applied 2 Oct 2026)

`eternity-price-list-2026-10-05.txt` is the text of Eternity's PDF. `eternity_2026_10.py` turns it
into `eternity-tiles-2026-10-05.csv`: one row per tile variant with the current price, the new
SKU (Eternity renamed ET... codes to DSA...), RRP, cost tiers and the new price.

Rules:
- **Cost** recorded in Shopify = Eternity "non pallet" price ex GST. Pallet (57.6 m² porcelain /
  86.4 m² ceramic) and mixed 3+ pallet (172.8 m²+) prices are in the CSV for quoting big jobs.
- **New price** = 15% under Eternity's RRP, rounded down to 10c ("option B", approved by the
  owner). Eternity's own shop and WA stockists (e.g. Online Flooring WA, Lava $55/m²) sell at RRP.
  Margin is about 35-37% ex GST; the CSV's `trade_price` (15% off public) keeps trade at 24-27%.
- **Floor**: price at least 25% above cost incl. GST.
- Applied in Shopify: 42 variants got the new price and cost; 16 SKUs renamed ET... -> DSA...,
  Lava Kraka 600x1200 Gloss given SKU YW277315.
- Not on the new list (price kept, no cost): Lava Etna Gloss 300x600 and 600x600, Lava Kraka
  600x1200 Matt, Cement White and Cement Grey 300x300. The list prints Time Stone Moon matt as
  YSR...; Eternity's site and our SKUs use YFR..., treated as the same tile.

## Range update to match the 5 Oct 2026 list (2 Oct 2026)

- Removed sizes not on the list: Lava Etna Gloss 300x600 and 600x600, Lava Kraka Matt 600x1200,
  Cement White and Cement Grey 300x300 (tags and descriptions updated to match).
- Added missing sizes: Morgan Hail 600x1200 (DSA126AK661), Morgan Cloud 300x300 (DSA33AK662) and
  300x600 (DSA36AK662), Cement White 300x600 (DSA36MQ01).
- Created 31 products (43 variants) with `eternity_new_products_2026_10.py` -> `eternity-new-products-2026-10.json`:
  Lava Vesuv, Fumosa, Astra White/Greige, Sand White/Beige/Grey, Bianco Greco, Caliza, E-Time Calcare/Chiaro,
  Oak Aube, Subway and Subwave ceramics, White/Eternal Marble/Eternal Carrara/Element Grey/Whisper Grey
  ceramic wall tiles, and 8 natural stone mosaics (sold per sheet). Same pricing rule (15% under RRP),
  cost recorded, published to all channels, added to `tiles`, delivery profile "Local delivery or pickup -
  large items".
- Photos: Eternity's own product photos for the ceramic ranges; swatches cut from the price list PDF
  (`eternity-swatches/`, about 200px, alt text says "indicative swatch") for ranges Eternity's shop doesn't
  list yet. Replace with proper photos when Eternity publishes them.
- New smart collections: `ceramic-wall-tiles` (tag Ceramic + type Tile) and `mosaic-tiles` (tag Mosaic).

# Store-wide public and trade pricing (applied 3 Oct 2026, approved by the owner)

`reprice_2026_10.py` → `store-pricing-2026-10-03.csv`: one row per active variant with the old price
(backup), new public price, trade band and trade price, cost (ex GST), margins, the competitor price it
was compared with, and any flag. Rules are in the script's docstring. In short:

- Competitors: Bathroom City for MELA (5% under, to the dollar); B&B Hardware, Maddington, for the ~50
  hardware items it also sells (5% under, to 5c). Terweys Total Hardware has no online prices. Other
  hardware: 10% under our old (supplier RRP) price. Tiles keep the 2 Oct prices.
- Profit floor: public ≥ cost inc GST × 1.25, trade ≥ cost inc GST × 1.15. Prices below the floor rise
  at most 10% and stay under the competitor; bigger gaps are flagged `BELOW PROFIT FLOOR` and left.
- MELA costs are estimates (Bathroom City list × (1 − SLIVER trade discount)); the sheet's discount is off
  the GST-inclusive list, so they're stored ex GST (÷ 1.1).
- 14 Oct 2026: the 694 Roberts Designs rows had their cost multiplied by 1.1 after the owner confirmed the Roberts account prices did not include GST (Maxisil, Sigma, Siri, Baron and Barwalt rows kept their cost on the owner's instruction); `new_price` on all 873 Roberts-supplied rows was refreshed to the live price and both margins recomputed. Prices unchanged. The 48 variants now under the floor are in `reports/roberts-gst-below-floor-2026-10-14.csv`.
- Trade: per-product bands of 5/10/15/20/25% (tiles max 15%), each the deepest that keeps every
  variant above the trade floor. Shopify Basic has no B2B price lists, so each band is a manual (unpublished)
  collection `trade-list-5` ... `trade-list-25` with an automatic discount "Trade price – N%" for the
  "Trade customers" segment (customer tag `trade`). To change one item's trade discount, move it to another
  `trade-list-N` collection in Shopify admin. The old tag-based `trade-band-*` collections are no longer used.
  (A `custom.trade_price` variant metafield definition exists but isn't filled.)
- Applied: 1,388 prices, 599 MELA costs (ex GST), 5 trade discounts. 4 B&B items and 64 MELA items stay above
  the competitor because it sells below our profit floor; ~30 `BELOW PROFIT FLOOR` items left for the owner.
- PDFs: `price_list_pdf.py` -> `price-lists/ETS-price-list-2026-10.pdf` (retail) and
  `price-lists/ETS-trade-price-list-2026-10.pdf` (retail + trade).
- Supplier delivery (SILVER sheet: $80 metro, $120 at 30-50 km) isn't added to costs: the owner confirmed
  (3 Oct) that delivery for bulky items is charged to the customer at checkout.

## On hold: MELA DAVISSON basin, White (4 Oct 2026)

Set to sold out (inventory tracked, 0 stock, "continue selling when out of stock" off) so it can't be
ordered at $199. Its recorded cost ($225.91 ex GST) was copied from the Matt White, because Bathroom City
doesn't list a plain White, so the "below cost" flag may be wrong. Owner to confirm whether MELA supplies
it and at what SILVER cost. To bring it back: set the variant's inventory policy to CONTINUE (or untrack
inventory) and re-price against the real cost. Matt Black and Matt White ($337) are unaffected.

## Eternity "wholesale essentials" list (V27102025.01, received 14 Oct 2026)

`eternity-essentials-2025-10-27.csv`: the 30 lines from Eternity's essentials sheet (cement, Easy Screed, WPA
waterproofing, TPA/Sika adhesives, Ardex FS-DD grout and SE silicone, aluminium angles, LX linear drains, tile
insert and square-plate floor wastes), wholesale ex GST. It does **not** cover the DSA bathroomware (tapware,
showers, vanities, basins, sinks, mirrors, toilet); that request is still `DSA-trade-price-request-2026-10-14.xlsx`.

Applied: BL-TID50 ($38.25) and BL-TID80 ($38.25) recorded as the cost of the two DSA tile insert floor wastes
(50mm given SKU BL-TID50; the 80mm keeps its web code; `needs-cost` removed). The two FLRG-SFD square-plate
drains ($11.01 / $16.11) probably match the Twist Top Floor Drains 80mm/100mm but the sizes don't line up, so
nothing recorded until Eternity confirms. The other 25 items are not stocked; `proposed_price_inc_gst` in the CSV
is cost x 1.1 (GST) / 0.65 (35% margin on the ex-GST sale price), rounded up to 5c, for the owner to approve.

## Eternity vanity packages (sheet "Wholesale Vanity Package Pricing 2025", received 14 Oct 2026)

`eternity-vanity-packages-2025.csv`: RRP and the three wholesale tiers (account 45% off, COD / 5-buy account 50%,
5-buy COD 55%) for the Malaga all-in-one packages. Two products created live at RRP (owner: sell at Eternity's
price for now), `malaga_packages_2026_10.py` -> `supplier-sync/malaga-packages-2026-10-14.json`:
China Top (3 colours x 750/900/1200) and Stone Top (3 colours x 750/900/1200/1500/1800). Stone colour (White Burst /
Blanco Bliss) and basin shape are taken in the order notes, not as variants. Cost = the sheet's **account deal 45%** column (owner, 14 Oct 2026), stored ex GST (÷ 1.1):
china top $590.00 / $771.82 / $953.64, stone top $734.55 / $852.73 / $1,052.73 / $1,416.36 / $1,680.00. Margin 46-50%
at RRP; both products in `trade-list-25`; 24 rows appended to the master CSV. Package photos are the sheet's own images (`supplier-sync/malaga-package-images/`).

## Trade bands re-set to a 20% floor (14 Oct 2026)

The owner found the trade prices too cheap: the 3 Oct bands were the deepest discount that kept about 13% margin, so the median margin after the trade discount was 16%, and the Roberts Designs cost correction pushed 141 of those products under even that floor. On the owner's instruction the trade floor is now **20% margin ex GST** (trade price ≥ cost ÷ 0.8 × 1.1) and every product on a trade list was re-banded to the deepest of 25/20/15/10/5% that keeps all its variants above it (tiles still max 15%).

- 906 products checked, 840 moved between the `trade-list-N` collections. Bands now: 25% → 17 products, 20% → 233, 15% → 235, 10% → 65, 5% → 231; 123 products (72 MELA, 25 Roberts Designs, 26 other) come off the trade lists because no band keeps 20%. Two products with no cost (Click powerblock, RLA additive) were left where they were.
- Median margin after the trade discount is now 22.8% (minimum 19.9%).
- `store-pricing-2026-10-03.csv`: `trade_band`, `trade_price` and `trade_margin_pct` refreshed on every trade-listed row. `reports/trade-price-check-2026-10-14.csv` is the before/after check with the band each floor would give. Price-list PDFs regenerated.

## Maxisil costs and trade bands (15 Oct 2026)

The owner confirmed Maxisil costs from the Roberts trade account were ex GST, and that trade customers were getting Maxisil too cheap. The 120 Maxisil variants now carry cost x 1.1, and each Maxisil product was re-banded to the deepest trade discount that keeps a 20% margin. **Public prices were left unchanged on the owner's instruction.**

- 18 products moved to a smaller discount (mostly 15% to 5%, grout 5/10kg and Natural Stone to 10%, primers 1215-1217 and the caulking gun to 15%). Pool silicone no longer gets a trade discount. Wet Area silicone and Maxigrab already had none.
- Wet Area silicone ($16.25, 12% margin on the new cost) and Maxigrab ($15.99 / $18.85, 14% and 23%) now sit under the 20% profit floor at the public price. Online they sell for about $18.50 and $22.12, so there is room to raise them if the owner wants.


## Trade price label fixed (15 Oct 2026)

The product page showed trade customers the old discount (e.g. Maxisil Natural Stone: "25% off, $20.99" while the cart gave 10%, $25.19). The theme reads `ets.trade_band`, which had not been updated when products moved between `trade-list-N` collections on 14-15 Oct. All 840 out-of-sync products were reset so `ets.trade_band` matches their `trade-list-N` collection (0 when in none). Step 4 of the playbook now says to update both.

## MELA matched to Bathroom City's price (20 Oct 2026)

Bathroom City supplies our MELA range and does not allow us to advertise below its price. On the owner's
instruction every MELA variant priced under Bathroom City's current price was raised to exactly that price
(734 variants, 278 products); nothing was lowered. 50 variants stay above Bathroom City because its clearance
price is under our profit floor; 25 are not on Bathroom City's site and were left alone. Full list:
`reports/bathroom-city-price-match-2026-10-20.md`. `monitor_competitors.py` now reports any MELA variant
priced below Bathroom City as a breach (section 1a) instead of suggesting 5% under. 213 MELA variants added
after 3 Oct were appended to the master CSV (cost from `mela-estimated-costs-2026-10-06.csv` where it has one); `mela-pricing-2026-10-01.csv`
now carries a Bathroom City match for all 786 matched variants. Trade bands were not changed.

## Roberts selling-price audit (23 Oct 2026)

`reports/roberts-price-audit-2026-10-23.md` (+ `.csv` with a proposed price per variant) audits all 935 Roberts-supplied variants against today's costs, the B&B Hardware feed, the September market matches and Roberts' own retail price, using the playbook floor (cost inc GST x 1.25). Built by `audit_roberts_2026_10.py`. Nothing was changed; the owner decides.

## Roberts selling prices applied (23 Oct 2026)

Owner approved the whole audit ("make money but a tiny bit cheaper than the competitor"). Applied to Shopify on 23 Oct:
- 913 variant prices set to the audit's proposed price (722 up, 191 down): 5% under B&B Hardware, 3% under the September market match, or 10% under Roberts' own retail, never under cost inc GST x 1.25. The 12 below-cost and 6 below-floor items (Baron mixers and parts, Sigma bars and cutters, 1500mm linear drain) now sit at the floor, so they are dearer than the competitor; ask Roberts for a trade discount on them.
- Biggest cuts: Expansion Aluminium Trim (all 28 sizes were $61 to $117; Roberts lists every size at $43.20 retail / $23.99 trade, so now $38.85). Biggest rises: L-shape trims and floor wastes that were 35 to 50% under Roberts retail.
- 227 products moved to the deepest trade band that keeps every variant at 20% margin ex GST at the new price (`ets.trade_band` metafield and `trade-list-N` collection both updated).
- `store-pricing-2026-10-03.csv` and `../supplier-sync/roberts-designs-pricing.csv` refreshed; `audit_roberts_2026_10.py` produced the proposals, `reports/roberts-price-audit-2026-10-23.csv` is the exact list applied.

## BAT / Raimondi costs from the May 2026 price books (23 Oct 2026)

Owner supplied three BAT price books (Tools Book 1, Raimondi Price Book, Project Trims Book 1, all May 2026, NET prices ex GST), flattened into `bat-price-books-2026-05.csv`. Applied by `bat_fix_2026_10.py`:
- 883 variants matched by SKU (BAT tools, Raimondi, Panther, Washboy, NICLIS, Project trims): unit cost set to NET x 1.1. The costs already in Shopify were the NET figures without GST.
- Selling prices left as they were except one: Raimondi Zoe 85A wet saw raised from $4,345.10 to $4,798.75 to clear the 20% floor. Every matched variant is now at 20% margin ex GST or better (median 37.5%). No competitor price is on file for BAT, so prices were not cut.
- 10 trade bands changed (8 products 25% to 20%, one 15% to 20%, one 0% to 5%); metafield and collections updated.
- `reports/bat-cost-price-update-2026-10-23.csv` has every matched variant; `reports/bat-not-in-may-2026-books.csv` lists the 1,280 variants these books do not cover: 1,253 BAT Trims profiles priced from the 2023-24 catalogue (GST basis of those costs still unconfirmed), 7 BAT items on ETS-HW internal SKUs, 20 archived trim variants.

Re-checked 25 Oct 2026 on the owner's query, against the original Project Trims Book 1 (May 2026) spreadsheet. All 98 PA-/PMCA- codes match, and every Shopify cost = NET x 1.1. The selling prices already include GST (PA-8-3: $3.30 NET / 0.6 = $5.50 + GST = $6.05, a 40% margin ex GST; PMCA 37-39%). The owner chose to keep the prices.

Note on margins: the margin columns in the 23 Oct Roberts reports and this one are (price - cost) / price with both inc GST, which equals the margin ex GST. An earlier version of the Roberts reports divided by the ex-GST price, understating margin by about 8 points; those files were regenerated.

## BAT Trims costs from Trims Book 1, August 2026 (24 Oct 2026)

Owner supplied the BAT Premium Trims price book (Trims Book 1, August 2026 v2, NET prices ex GST), parsed from the PDF into `bat-trims-book-2026-08.csv` (1,102 codes). Applied with the same rules as the May books (`bat_fix_2026_10.py` pointed at this CSV, then `bat_trims_stairnosing_2026_10.py`):
- 1,155 BAT Trims variants on 43 products now carry unit cost = book NET x 1.1. Every cost went up: the figures already in Shopify were the 2023-24 NET prices without GST.
- Stairnosing (76 variants) is sold with the non-slip rubber insert, so its cost is bar + insert (`BSN-8-3-MF-BL` = `BSN-8-3-MF` $34.35 + `RSI-BL` $22.90), x 1.1. The old cost was exactly that sum without GST.
- No selling price changed: every variant stays at 26.7% margin ex GST or better (median 37.5%), so no floor raise was needed and no trade band moved. No competitor price is on file for BAT Trims.
- `reports/bat-trims-cost-update-2026-10-24.csv` has every variant (old/new cost, price, floor, margin, band). All 1,155 were added to `store-pricing-2026-10-03.csv`.
- `reports/bat-not-in-any-price-book-2026-10-24.csv` supersedes the 23 Oct "not in May books" list: 125 variants remain without a book price. 98 active cove-trim and APC 60 corner pieces (`CTEC-*`, `CTIC-*`, `APC60-*`, one product) are not in any of the four books; 7 BAT items on internal ETS-HW SKUs need a manual code; 20 archived Unicorn and APC cove combination variants were left alone.

## SikaTile-305 Master Lite 15kg (new product, 24 Oct 2026)

Owner's cost $20 ex GST, recorded as $22.00 inc GST. Floor = $27.50. No Australian retailer lists Master Lite online yet (Sika released the data sheet in May 2026), so the market check used Sika's other 20kg adhesives: Prohesive Promaxset $26.61 (TradieCart), Proflex $27.50 and Evo Pro $28.60-31.46 (Kims Tiling Supplies), Davco SMP Evo $33.95 (Mitre 10), Megapro $34.10-37.51 (Kims). A 15kg Master Lite covers about what a 20kg standard bag does, so it was priced at **$29.95** (26.5% margin ex GST), trade band 5% ($28.45, 22.7%). SKU `SIKA-305-ML-15`, product `gid://shopify/Product/8458228629567`, published to every channel, tagged `Hardware` + `Adhesives & Additives` + `ship-parcel` (15kg fits Australia Post). Stock is tracked with "continue selling": the owner still has to enter the on-hand count.

## Eternity tile samples, invoice SI-00036787 (added 26 Oct 2026)

Five lappato 300x600 samples (`eternity-samples-invoice-SI-00036787.pdf`, 100% discounted, unit prices are the
non-pallet ex GST cost). Decisions in `eternity-samples-2026-10-26.csv`. Time Stone Moon and Cinder lappato were
already listed. Three products created as **drafts** (no photo yet, tag `needs-photo`): Time Stone Sand (BS630332,
$55.20, cost $32.00, same tier as the other Time Stone lappatos), Arena Light (BV637544) and Arena Blonde (BV637541)
($50.10, cost $28.00, tag `price-check`: neither is on the Oct 2026 list or Eternity's site, so the RRP is assumed to be
the $59 tier their cost sits in). All three: trade-list-15, "Perth only (local delivery / pickup)" profile, published to
every channel so they go live the moment the status is set to Active. Eternity's SharePoint folders (Time stone, Lava,
Caliza, Terrazzo Lumina, porcelain/ceramic standard range, DSA toilet/kitchen/basin collections) need a login, so the
product sheets and photos still have to be downloaded by the owner and added by hand.


## Trade prices recorded as metafields (5 Nov 2026)

The owner asked to see each product's trade price inside Shopify. `trade_price_metafields_2026_11.py` read every
product's `ets.trade_band` and variant prices and wrote, for the 837 products on a trade list (3,320 variants):
variant metafield `custom.trade_price` (the definition existed, unfilled) = price x (1 - band/100), and a new pinned
product metafield `ets.trade_price` showing "$x (N% off)" or the range across variants. Products with band 0 got
nothing. `reports/trade-price-metafields-2026-11-05.csv` lists every value written. These fields are a record for
reading, not what the checkout discount uses; rerun the script after any price or band change (playbook step 4).

## Sigma 108362 nut: duplicate removed (5 Nov 2026)

Roberts Designs lists the same Sigma part (art. 108362, M8 square nut for the swivel-bar locking lever) under two codes,
RDXA3649 ($11.70 retail, $6.50 trade ex GST) and RDXA3580 ($7.60 retail), both with only a placeholder photo on Roberts' site.
The import made two products. The RDXA3580 one ("M8 Square Nut", `no-photo`, no trade band) had been deleted on 6 Oct for having
no photo and came back with the 21 Oct Roberts re-import; it was deleted again on the owner's instruction
(`../deleted-duplicate-sigma-108362-2026-11-05.json` is the backup). Kept: "Sigma 108362 M8 Nut for Locking Bolt"
(`gid://shopify/Product/8403243204671`, RDXA3649, $10.50, trade band 10%, photo from BAT's SIG-108362 listing), with all three
supplier codes now in its description. BAT also sells it: SIG-108362 at $5.85 NET ex GST (Tools Book 1, May 2026), cheaper than
Roberts, so buy it there; the recorded cost ($7.15, Roberts) was left for the owner to decide. Its stock reads -2 (oversold).
