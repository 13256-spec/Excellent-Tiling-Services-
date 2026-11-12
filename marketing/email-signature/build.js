#!/usr/bin/env node
// Builds an ETS email signature for one person. See README.md.
//   node build.js --name "Jane Smith" --title "Showroom Manager" --email jane@excellenttilingservices.com \
//                 [--phone "0450 960 543"] [--photo headshot.jpg]
// Writes people/<name>/signature.html, a set of image pieces, and preview.png + preview-dark.png.
//
// The signature is the whole card drawn once, then cut into image pieces, each piece its own link.
// Why images only: Outlook / Hotmail dark mode recolours text and backgrounds (white card turns black, navy text
// vanishes) but leaves images alone, and Gmail / Outlook block the website fonts. Images look the same everywhere.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

// ---- Brand: read from the live website (excellenttilingservices.com). Change here if the site changes. ----
const B = {
  ink: '#15213A', dark: '#0F1A2C', brass: '#9C7744', brassLight: '#E9D6B5', cream: '#EFE6D6', muted: '#6A6862', line: '#DADCE0',
  sans: "Manrope,'Segoe UI',Arial,Helvetica,sans-serif",
};
const SHOP = {
  site: 'https://excellenttilingservices.com', siteText: 'excellenttilingservices.com',
  email: 'contactus@excellenttilingservices.com', phone: '0450 960 543',
  address: '17A Olga Road, Maddington WA 6109',
  maps: 'https://www.google.com/maps/search/?api=1&amp;query=17A+Olga+Road+Maddington+WA+6109',
  instagram: 'https://www.instagram.com/excellent_tiling_services/', facebook: 'https://www.facebook.com/share/1943ueL61k/',
};
const here = (...p) => path.join(__dirname, ...p);
// hosted.json maps a local image ("people/jane-smith/logo.png") to its online link (Shopify Files).
// An image listed there is linked online; one that is not stays a local path and will not show in a mail app.
const HOSTED = fs.existsSync(here('hosted.json')) ? JSON.parse(fs.readFileSync(here('hosted.json'), 'utf8')) : {};
const missing = [];
const hosted = (key, local) => HOSTED[key] || (missing.push(key), local);
const b64 = f => fs.readFileSync(here('assets', f)).toString('base64');
const font = (name, file) => `@font-face{font-family:${name};src:url(data:font/woff2;base64,${b64('fonts/' + file)})}`;
const icon = (n, size) => fs.readFileSync(here('assets', 'icons', n + '.svg'), 'utf8').replace('<svg', `<svg style="width:${size}px;height:${size}px;display:block;flex:none"`);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const tel = p => 'tel:' + p.replace(/\s/g, '').replace(/^0/, '+61');

function args() {
  const a = {}, v = process.argv.slice(2);
  for (let i = 0; i < v.length; i++) if (v[i].startsWith('--')) a[v[i].slice(2)] = v[i + 1] && !v[i + 1].startsWith('--') ? v[++i] : true;
  for (const k of ['name', 'title', 'email']) if (typeof a[k] !== 'string') { console.error(`missing --${k}. See the top of build.js.`); process.exit(1); }
  if (a.photo && !fs.existsSync(a.photo)) { console.error(`photo not found: ${a.photo}`); process.exit(1); }
  return a;
}

// Headshot (or, with no photo, the navy-and-cream stand-in figure) cut into three leaning slices.
function photoHtml(photo) {
  const SIZE = 160, LEAN = 59, GAP = 4.5, WIDTHS = [50, 27, 15]; // widths + gaps must add up to SIZE - LEAN
  console.assert(Math.abs(WIDTHS.reduce((a, b) => a + b) + GAP * (WIDTHS.length - 1) - (SIZE - LEAN)) < 0.01, 'slices must fill the square');
  const inner = photo
    ? `<img src="data:image/${path.extname(photo).slice(1).toLowerCase().replace('jpg', 'jpeg')};base64,${fs.readFileSync(photo).toString('base64')}" style="width:100%;height:100%;object-fit:cover;object-position:50% 30%;display:block">`
    : `<div style="width:100%;height:100%;background:linear-gradient(160deg,#3A4556,${B.dark});position:relative"><div style="position:absolute;left:55px;top:30px;width:50px;height:50px;border-radius:50%;background:${B.cream}"></div><div style="position:absolute;left:25px;top:90px;width:110px;height:120px;border-radius:55px 55px 0 0;background:${B.cream}"></div></div>`;
  let x = 0, slices = '';
  for (const w of WIDTHS) {
    slices += `<div style="position:absolute;inset:0;clip-path:polygon(${x}px ${SIZE}px,${x + w}px ${SIZE}px,${x + w + LEAN}px 0,${x + LEAN}px 0)">${inner}</div>`;
    x += w + GAP;
  }
  return `<div style="width:${SIZE}px;height:${SIZE}px;position:relative">${slices}</div>`;
}

// The pieces the card is cut into: [column, file name, link, text shown if images are blocked].
function pieces(p) {
  const mail = 'mailto:' + p.email;
  return [
    [0, 'strip-website', SHOP.site, 'Website'], [0, 'strip-instagram', SHOP.instagram, 'Instagram'],
    [0, 'strip-facebook', SHOP.facebook, 'Facebook'], [0, 'strip-email', mail, 'Email'],
    [1, 'logo', SHOP.site, 'Excellent Tiling Services'], [1, 'name', null, `${p.name}, ${p.title}`],
    [1, 'phone', tel(p.phone), p.phone], [1, 'email', mail, p.email],
    ...(p.email === SHOP.email ? [] : [[1, 'shop-email', 'mailto:' + SHOP.email, SHOP.email]]),
    [1, 'website', SHOP.site, SHOP.siteText], [1, 'address', SHOP.maps, SHOP.address],
    [2, 'photo', null, ''],
  ];
}

// The card as a normal web page (never sent to anyone - it is only drawn and cut up). data-s marks each piece.
function designHtml(p, photo) {
  const strip = (s, ic, pad) => `<div data-s="strip-${s}" style="padding:${pad};color:${B.brassLight};fill:${B.brassLight}">${icon(ic, 18)}</div>`;
  const row = (s, ic, text, color = B.ink) => `<div data-s="${s}" style="display:flex;align-items:center;gap:8px;height:22px;font-size:12px;color:${color};white-space:nowrap"><span style="color:${B.brass};fill:${B.brass}">${icon(ic, 13)}</span>${esc(text)}</div>`;
  return `<style>${font('M5', 'manrope-latin-500-normal.woff2')}${font('M6', 'manrope-latin-600-normal.woff2')}${font('M7', 'manrope-latin-700-normal.woff2')}${font('IS', 'instrument-serif-latin-400-normal.woff2')}
    body{margin:0;background:transparent}</style>
<div id="card" style="display:inline-flex;align-items:center;box-sizing:border-box;border:1px solid ${B.line};border-radius:10px;background:#fff;font-family:M5;color:${B.ink}">
  <div style="padding:16px 0 16px 16px"><div style="border-radius:6px;background:${B.dark}">
    ${strip('website', 'globe', '10px 10px 6px')}${strip('instagram', 'instagram', '6px 10px')}${strip('facebook', 'facebook', '6px 10px')}${strip('email', 'mail', '6px 10px 10px')}
  </div></div>
  <div data-col="1" style="padding:16px 20px">
    <div data-s="logo" style="display:flex;align-items:center;gap:11px;margin-bottom:12px"><img src="data:image/png;base64,${b64('mark.png')}" height="34">
      <div><div style="font:17px/1 M7;letter-spacing:1.7px">EXCELLENT</div><div style="font:9.5px/1 M6;letter-spacing:3.04px;color:${B.muted};margin-top:5px">TILING SERVICES</div></div></div>
    <div data-s="name"><div style="font:30px/1.1 IS;letter-spacing:-.3px;white-space:nowrap">${esc(p.name)}</div>
      <div style="display:flex;align-items:center;gap:8px;margin-top:4px"><div style="width:22px;height:1px;background:${B.brass}"></div>
        <div style="font:11px/16px M7;letter-spacing:2px;text-transform:uppercase;color:${B.brass};white-space:nowrap">${esc(p.title)}</div></div></div>
    <div style="margin-top:9px">
      ${row('phone', 'phone', p.phone)}${row('email', 'mail', p.email)}${p.email === SHOP.email ? '' : row('shop-email', 'mail', SHOP.email)}${row('website', 'globe', SHOP.siteText)}${row('address', 'pin', SHOP.address, B.muted)}
    </div>
  </div>
  <div data-col="2" style="padding:16px 18px 16px 0">${photoHtml(photo)}</div>
</div>`;
}

(async () => {
  const a = args();
  const p = { name: a.name, title: a.title, email: a.email, phone: typeof a.phone === 'string' ? a.phone : SHOP.phone };
  const slug = p.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  const dir = here('people', slug);
  fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 3, viewport: { width: 1000, height: 500 } }); // 3x so pieces stay sharp on phones
  await page.setContent(designHtml(p, a.photo));
  await page.evaluate(() => document.fonts.ready);
  // Measure where to cut (whole px): columns at the start of the text and photo columns, rows halfway between neighbours.
  const list = pieces(p);
  const m = await page.evaluate(names => {
    const card = document.getElementById('card'), r = card.getBoundingClientRect();
    card.style.width = Math.ceil(r.width) + 'px'; card.style.height = Math.ceil(r.height) + 'px';
    const box = el => { const b = el.getBoundingClientRect(); return { top: b.top, bottom: b.bottom, left: b.left }; };
    return { w: Math.ceil(r.width), h: Math.ceil(r.height), cols: [1, 2].map(c => Math.round(box(document.querySelector(`[data-col="${c}"]`)).left)),
      boxes: Object.fromEntries(names.map(n => [n, box(document.querySelector(`[data-s="${n}"]`) || document.querySelector('[data-col="2"]'))])) };
  }, list.map(x => x[1]));
  const xs = [0, ...m.cols, m.w];
  const cols = [0, 1, 2].map(c => {
    const items = list.filter(x => x[0] === c);
    const cuts = [0, ...items.slice(1).map((x, i) => Math.round((m.boxes[items[i][1]].bottom + m.boxes[x[1]].top) / 2)), m.h];
    return items.map(([, file, href, alt], i) => ({ file, href, alt, x: xs[c], y: cuts[i], w: xs[c + 1] - xs[c], h: cuts[i + 1] - cuts[i] }));
  });
  for (const s of cols.flat()) await page.screenshot({ path: path.join(dir, s.file + '.png'), omitBackground: true, clip: { x: s.x, y: s.y, width: s.w, height: s.h } });
  console.assert(cols.every(c => c.reduce((t, s) => t + s.h, 0) === m.h), 'each column must add up to the card height');

  const img = s => `<img src="${hosted(`people/${slug}/${s.file}.png`, s.file + '.png')}" width="${s.w}" height="${s.h}" alt="${esc(s.alt)}" style="display:block;border:0;outline:none;">`;
  fs.writeFileSync(path.join(dir, 'signature.html'), `<!-- ETS email signature for ${esc(p.name)}. Made by build.js - edit there, not here. -->
<table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;"><tr>
${cols.map(c => `<td style="padding:0;vertical-align:top;font-size:0;line-height:0;">${c.map(s => s.href ? `<a href="${esc(s.href)}" style="text-decoration:none;">${img(s)}</a>` : img(s)).join('')}</td>`).join('\n')}
</tr></table>
`);

  // Preview pictures: on a white email and on a dark-mode email.
  const prev = await browser.newPage({ deviceScaleFactor: 2, viewport: { width: m.w + 48, height: m.h + 48 } });
  await prev.goto('file://' + path.join(dir, 'signature.html'), { waitUntil: 'networkidle' });
  for (const [file, bg] of [['preview.png', '#fff'], ['preview-dark.png', '#1f1f1f']]) {
    await prev.addStyleTag({ content: `body{margin:24px;background:${bg}}` });
    await prev.screenshot({ path: path.join(dir, file) });
  }
  await browser.close();
  console.log('built', path.relative(process.cwd(), dir), `(${m.w} x ${m.h} px, ${list.length} pieces)`);
  if (missing.length) console.log('NOT ready for a mail app - these images are not online yet (add them to hosted.json):\n  ' + missing.join('\n  '));
})();
