# Lighthouse: trust sections draft, before vs after (1 Nov 2026)

Both sides measured on the same unpublished theme "ETS 2026 – Trust sections (draft)" (id 144719740991) through its preview link: `before-draft` right after it was duplicated from the live theme, `after-draft` after the 14 files were uploaded. Lighthouse 13.6.0, headless Chromium, default throttling, median of 3 runs each. Preview pages carry Shopify's preview bar, which is why accessibility reads 94-95 here and 100 on the live site. Mobile run-to-run spread is wide (before LCP 2.97-4.82 s, TBT 2.83-4.50 s), so the DOM count is the firm number.

### Mobile (median of 3 before / 3 after runs)

| Metric | Before | After | Change |
|---|---|---|---|
| Performance | 55 | 56 | +1 better |
| Accessibility | 94 | 95 | +1 better |
| Best practices | 77 | 77 | +0 |
| SEO | 100 | 100 | +0 |
| First Contentful Paint | 1.49 s | 1.50 s | +11 ms worse |
| Largest Contentful Paint | 3.10 s | 3.24 s | +139 ms worse |
| Total Blocking Time | 2.99 s | 2.49 s | -505 ms better |
| Cumulative Layout Shift | 0.009 | 0.008 | -0.001 better |
| Speed Index | 10.48 s | 10.35 s | -124 ms better |
| DOM elements | 4,093 | 2,673 | -1,420 better |
| Page weight | 5,446 KB | 5,374 KB | -71 KB better |

### Desktop (median of 3 before / 3 after runs)

| Metric | Before | After | Change |
|---|---|---|---|
| Performance | 71 | 78 | +7 better |
| Accessibility | 94 | 95 | +1 better |
| Best practices | 77 | 77 | +0 |
| SEO | 100 | 100 | +0 |
| First Contentful Paint | 696 ms | 666 ms | -31 ms better |
| Largest Contentful Paint | 1.77 s | 1.66 s | -110 ms better |
| Total Blocking Time | 320 ms | 204 ms | -116 ms better |
| Cumulative Layout Shift | 0.004 | 0.003 | -0.000 better |
| Speed Index | 4.53 s | 4.04 s | -491 ms better |
| DOM elements | 4,090 | 2,670 | -1,420 better |
| Page weight | 6,002 KB | 6,017 KB | +15 KB worse |
