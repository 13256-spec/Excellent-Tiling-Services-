# Raimondi compatibility ("what fits what")

Set up 12 Oct 2026 after order #1009 (a Zoe 85A with the folding extension table, side square and Double
spacers): the customer had trouble working out which accessories fit the saw. Every Raimondi machine,
accessory, blade, consumable and spare part now carries two product metafields, and the site uses them.

**Superseded the same evening** by the store-wide map in `store-content/catalogue/` (`fitmap_all.py`,
`compatibility-all.csv`), which covers every Raimondi product plus BAT, Washboy, Panther, Siri, Sigma and the
rest, and adds `ets.fits_role`. This folder is kept for the Raimondi sources and the wet-saw rewrite.

## The data

| Metafield | Type | On a machine | On an accessory, blade or part |
|---|---|---|---|
| `ets.fits_with` | list of products | its accessories, blades and spare parts (accessories first, then blades, then parts) | the machines we sell that it fits |
| `ets.fits_models` | text | what it takes (blade sizes, consumables) | every model it fits in plain words, including ones we don't stock (Pikus Advanced, Exploit, Bolt, Mistral) and the Raimondi article number where known |

`compatibility.csv` is the full map (131 products). `fitmap.py` holds the map as code and writes the CSV
and the Shopify payloads; `rewrite.py` holds the new titles, descriptions and SEO text for the wet-saw
family and the Double spacer. Both read `all.json`, a Shopify export of the Raimondi products (not committed:
it contains costs). To rebuild: export the products, run `fitmap.py`, then set the metafields with
`metafieldsSet` (25 per call).

Sources: Raimondi catalogue pages A20 (Zoe 85 Advanced), A23 (Zoe 150 Advanced) and A30–A33 (accessories for
bridge saw machines, with the fit matrix), the current raimondispa.com product pages (Zoe 85/130 Advanced,
Pikus 85 Advanced, SMS 100/125, SA 80, DOUBLE spacer), the supplier's May 2026 Raimondi price list, and the
store's own descriptions for the non-saw families (Bulldog, Raizor, Easymove, mixers, vibrators, Ipertitina,
Maxititina, grout clean-up, Rai-Fix).

## What the catalogue settled

- The folding extension table kit (Raimondi 423KITDL, SKU RAI-FETPIK75, "suit Pikus" in the supplier list)
  fits every Zoe Advanced, Pikus Advanced and SMS. So do the side square (191CL04A), the telescopic counter
  square (191CL04A1), the 5-roller bench (374RU5D40I) and the sliding squares (192SQ03A, 192SQ07A).
- Tile holding device: 423BL105ADV fits Zoe 105A, Pikus 105 and SMS 100; 423BL130ADV fits Zoe 130A, Pikus
  130 and SMS 125 (the SMS 125 was missing from the variant name, now added); 423BL150ADV fits Zoe 155A.
  New Zoe Advanced saws include one.
- The wheels and handle kit (315CR02K, RAI-EXWHK) fits Exploit, Bolt and Mistral only. The Zoe, Pikus, SMS
  and SA 80 come with a wheel kit. The old description said "for Raimondi wet saws".
- Blades: Zoe Advanced, SMS and SA 80 take 300 to 350 mm (Raimondi's 2021 catalogue says up to 360 mm),
  25.4 mm bore; Pikus Advanced takes 230 to 250 mm; 200 mm blades are for the Exploit.
- Raimondi's current pages say the Zoe Advanced and SMS ship with a 300 mm porcelain blade (the 2021
  catalogue said 350 mm). The product pages now say 300 mm; the owner can confirm against what BAT ships.
- The SA 80 is a sliding-trolley saw, 80 cm cut, 120 mm depth in one pass, 3 HP; it does not take the Zoe
  and SMS extension tables and squares.
- Raimondi calls the Zoe 155A the "ZOE 150 ADV" (155 cm cut). The variant keeps the supplier's name.
- The Double spacer: grey 1 and 3 mm (282D1-3C300), red 2 and 5 mm (282D2-5C300), bucket of 300, 37 x 37 mm.

## Where it shows

- Live now (any theme): 31 wet-saw family products and the Double spacer have new titles that name the saws
  they suit, a bold "Fits:" first line in the description, and the three saws list "What fits this saw".
  No links in descriptions: Marketplace Connect copies descriptions to eBay, and eBay removes listings with
  off-eBay links.
- Live now: seven manual collections, one per machine family, linked from the Raimondi collection's
  "Shop by machine" line: `raimondi-wet-saw-accessories`, `raimondi-bulldog-wheels-parts`,
  `raimondi-raizor-spares`, `raimondi-grout-clean-up-spares`, `raimondi-floor-machine-parts`,
  `raimondi-mixer-vibrator-parts`, `raimondi-easymove-bigfoot-accessories`.
- Live theme "ETS 2026 – what fits what (live from 12 Oct)" (gid://shopify/OnlineStoreTheme/144033579071,
  a duplicate of the previous live theme made 12 Oct after the owner deleted his own copy 144029417535, and
  published by the owner that night): `sections/ets-product-fits.liquid` renders the `fits_with` products as a card grid
  ("What fits this one" on machines, "What this fits" on everything else, with a "See the whole range" link
  to the product's system or machine collection), and `snippets/ets-pdp-fits.liquid` puts the `fits_models`
  text under the product title with a "See what fits" jump link. Both product templates carry the `fits`
  block and section.

## Adding a new Raimondi product

1. Set `ets.fits_models` (plain words, name the models) and `ets.fits_with` (pick the machines it fits, or on
   a machine, everything that fits it). Add the new item to the machines' `fits_with` lists too.
2. Put "suits …" in the title and a "Fits:" first line in the description.
3. Add it to the right `raimondi-*` collection (they are manual).
4. Add a row to `fitmap.py` and rerun it so `compatibility.csv` stays current.
