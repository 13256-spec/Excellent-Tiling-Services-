# Trade band proposal under the new rules (5 Nov 2026, waiting for the owner's approval)

Rules (playbook v2): trade floor 25% margin ex GST (MELA 20%), band = deepest of 20/15/10/5 within the cap (hardware 20%,
tiles 15%, MELA 15%) that keeps every variant above the floor. Costs inc GST. Per-product detail:
`trade-band-proposal-2026-11-05.csv` (band now, band proposed, lowest public margin).

| | Products |
|---|---|
| Same band as today | 154 |
| Smaller discount | 707 |
| Bigger discount (mostly MELA, back on a band since the 20 Oct price rise) | 225 |
| Lose the trade discount | 151 (113 Raimondi, 31 BAT, 7 other) |
| Skipped, no cost on a variant | 108 (RLA/Gripset, Click, a few BAT) |

Resulting bands: 5% on 231 products, 10% on 107, 15% on 406, 20% on 98 (no 25% band remains).
Trade margin after the change: hardware median 28.7% (min 25.0), tiles 32.9%, MELA 22.3% (min 21.0).

Worth a separate decision: **Raimondi** sits at a 27% public margin (BAT price-book costs, no competitor on file), so
almost no Raimondi item can carry a trade discount under a 25% floor. Raising Raimondi public prices about 8% would give
most of the range a 10% band. Same for the 31 BAT items.

To apply after approval: move bands (metafield + collections), rerun `b2b_price_list_2026_11.py`, delete the fixed prices
of the 151 products that drop to 0, rerun `trade_price_metafields_2026_11.py`, update the master list, regenerate PDFs.
