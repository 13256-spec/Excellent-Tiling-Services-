// ETS: box-units calculator maths check (kept out of theme/ so it is not synced to Shopify). Run: node store-content/pricing/ets-box-math.test.js
// Copy of the box branch in theme/assets/ets-2026.js calcUpdate (keep them in step); requires nothing from the theme.
const assert = require('assert');

function boxesNeeded(areaM2, wastePct, m2PerBox) {
  const need = areaM2 * (1 + wastePct / 100);
  const box = parseFloat(m2PerBox) || 1;
  // the 1e-6 guard stops float noise (4.32 / 1.44 = 3.0000000000000004) adding a box
  return Math.ceil(need / box - 1e-6);
}

assert.strictEqual(boxesNeeded(4.32, 0, '1.44'), 3);
assert.strictEqual(boxesNeeded(8.64, 0, '1.44'), 6);
assert.strictEqual(boxesNeeded(1.44, 0, '1.44'), 1);
assert.strictEqual(boxesNeeded(12.5, 15, '1.44'), 10);
assert.strictEqual(boxesNeeded(12.5, 0, '1.44'), 9);
// without the guard the exact multiples would be wrong
assert.strictEqual(Math.ceil(4.32 / 1.44), 4);
// result text pieces: m² per box and total m² print with two decimals
assert.strictEqual((1.4).toFixed(2), '1.40');
assert.strictEqual((3 * 1.44).toFixed(2), '4.32');
// missing/invalid box size falls back to 1 m² per box
assert.strictEqual(boxesNeeded(2.5, 0, ''), 3);

console.log('ets-box-math: all checks pass');
