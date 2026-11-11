# Product and collection audit (11 Nov 2026)

Every active product was checked against the six department collections and their sub-collections, and each
collection was checked for size and for a place in the menu. Data: 1,425 products (1,415 active, 8 draft, 2 archived)
and 131 collections, exported from Shopify on 11 Nov 2026.

## What was wrong and what was changed (all done in Shopify, owner approved)

| Problem | Fix |
| --- | --- |
| 29 active products sat in no department because their product type was missing from the department rules. | Added the types to the smart collections: Baths & toilets +Bidet Seat, Toilet Flush Button, Toilet Back Rest, Shower Screen, Frameless Shower Panel, Corner Shower Screen, Shower Screen Fitting; Vanities & basins +Ceramic Vanity Top, Vanity Option; Tapware & sinks +Kitchen Sink Accessory; Mirrors & accessories +Heated Towel Rail; Hardware +Core Drills, Utility Knives & Blades, Tile Wedges. |
| 3 "Vanity Option" add-on products were in no collection at all. | Now in Vanities & basins through the type rule. Worth a look: they are add-ons, not vanities. |
| 15 Roberts Designs floor wastes and drains carried the type "Designer Bathroom Accessories". | Type changed to "Floor Drains" (they already sat in Floor drains & wastes by vendor; the type now matches). |
| Spouts & outlets (manual) was missing 3 spouts (Celine swivel bath spout, MELA Bruno wall spout, MELA Rondo wall spout). | Added. Now 8 products. |
| Inset basins (manual) was missing the two MELA half-inset basins (Selva, Debba). | Added. Now 4 products. |
| Accessories (manual) was missing 7 Roberts Designs "Ceramic and Modern Bathroom Fixtures". | Added. Now 60 products. |

Department counts after the fixes: Tiles (manual, unchanged), Vanities & basins 179, Tapware & sinks 88,
Baths & toilets 44, Mirrors & accessories 81, Hardware 982.

## New "On sale" collections (manual, empty until the owner adds products)

One per department, each linked as the first item of its dropdown in both the live menu (`main-menu-2026`) and the
new draft menu (`main-menu-2026-v3`, where Hardware on sale sits under both Adhesives & waterproofing and Tools & trims):

| Department | Collection | URL |
| --- | --- | --- |
| Tiles | Tiles on sale (304302948415) | /collections/tiles-on-sale |
| Vanities & basins | Vanities & basins on sale (304302981183) | /collections/vanities-basins-on-sale |
| Tapware & sinks | Tapware & sinks on sale (304303013951) | /collections/tapware-sinks-on-sale |
| Baths & toilets | Baths & toilets on sale (304303046719) | /collections/baths-toilets-on-sale |
| Mirrors & accessories | Mirrors & accessories on sale (304303079487) | /collections/mirrors-accessories-on-sale |
| Hardware | Hardware on sale (304303112255) | /collections/hardware-on-sale |

To put a product on sale: Shopify admin → Products → open the product → set **Compare-at price** to the old price and
**Price** to the sale price (the theme then shows the Sale badge and the crossed-out price) → under Collections add it to
the department's "on sale" collection. Remove it from the collection when the sale ends. Trade customers still see their
trade price; if the sale price is below the trade price, tell Claude so the trade floor is checked (playbook section 2).

They are manual on purpose: Shopify smart collections cannot mix "department X" AND "has a compare-at price" with the
rest of the department rules, so a rule-based version would have pulled in the whole department.

## Left as is (for the owner to decide)

- Two empty collections deleted on the owner's instruction (11 Nov): "Trade 25% items" (`trade-list-25`, a leftover of
  the old discount-based trade bands, no discount referenced it) and "BAT Tile Trims & Aluminium Angles" (`bat-trims`,
  rule vendor = "BAT Trims" matched nothing). Copies in `store-content/collections/deleted-2026-11-11.json`. The BAT trims
  link was removed from the live Hardware dropdown.
- Clearance stays as its own collection: the owner keeps clearance separate from sale.
- Nine collections with one or two products: inset-baths (1), corner-shower-screens (1), inset-basins (4 after the fix),
  undermount-basins (2), back-to-wall-baths (2), corner-baths (2), tiles-300x300 (2), particle-tiles (2), terrazzo-tiles (2).
  They are real ranges, just thin.
- Collections that are live but not in either menu (reachable from search, the all-collections page and links):
  porcelain-tiles (34), trade-essentials (13), tiling-hand-tools (89), clearance (4), smart-toilets (7), the seven
  Raimondi spares sub-collections, the eleven ARDEX sub-collections and wedi. Clearance (4) could be retired now that
  each department has an "on sale" collection.
- Every other product type maps to exactly the department you would expect; no product sits in a department it does
  not belong to.
