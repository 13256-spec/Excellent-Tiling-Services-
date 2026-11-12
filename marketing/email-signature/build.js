#!/usr/bin/env node
// Builds an ETS email signature for one person. See README.md.
//   node build.js --name "Jane Smith" --title "Showroom Manager" --email jane@excellenttilingservices.com \
//                 [--phone "0450 960 543"] [--photo headshot.jpg] [--shared]
// Writes people/<name>/signature.html, name.png, photo.png, preview.png.
// --shared also rebuilds the images everyone shares (shared/: logo + icons); only needed after a brand change.
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
const ICONS = ['globe', 'instagram', 'facebook', 'mail', 'phone', 'pin'];
const ICON_SETS = { light: B.brassLight, brass: B.brass }; // light = on the navy strip, brass = beside each contact line

const here = (...p) => path.join(__dirname, ...p);
const b64 = f => fs.readFileSync(here('assets', f)).toString('base64');
const font = (name, file, weight = 400) => `@font-face{font-family:${name};font-weight:${weight};src:url(data:font/woff2;base64,${b64('fonts/' + file)})}`;
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const tel = p => 'tel:' + p.replace(/\s/g, '').replace(/^0/, '+61');

function args() {
  const a = {}, v = process.argv.slice(2);
  for (let i = 0; i < v.length; i++) if (v[i].startsWith('--')) a[v[i].slice(2)] = v[i + 1] && !v[i + 1].startsWith('--') ? v[++i] : true;
  for (const k of ['name', 'title', 'email']) if (typeof a[k] !== 'string') { console.error(`missing --${k}. See the top of build.js.`); process.exit(1); }
  if (a.photo && !fs.existsSync(a.photo)) { console.error(`photo not found: ${a.photo}`); process.exit(1); }
  return a;
}

// Screenshot one element with a see-through background; returns its size in CSS px (images are saved at 3x so they stay sharp).
async function snap(page, html, file) {
  await page.setContent(`<body style="margin:0;background:transparent">${html}`);
  await page.evaluate(() => document.fonts.ready);
  const el = await page.$('#x'), box = await el.boundingBox();
  await el.screenshot({ path: file, omitBackground: true });
  return { w: Math.round(box.width), h: Math.round(box.height) };
}

async function buildShared(page) {
  fs.mkdirSync(here('shared'), { recursive: true });
  // Logo copied from the website header: tile icon + EXCELLENT / TILING SERVICES in Manrope.
  await snap(page, `<style>${font('M7', 'manrope-latin-700-normal.woff2')}${font('M6', 'manrope-latin-600-normal.woff2')}
    #x{display:inline-flex;align-items:center;gap:11px;padding:1px}
    .n{font:17px/1 M7;letter-spacing:1.7px;color:${B.ink}}.s{font:9.5px/1 M6;letter-spacing:3.04px;color:${B.muted};margin-top:5px}</style>
    <div id="x"><img src="data:image/png;base64,${b64('mark.png')}" height="34"><div><div class="n">EXCELLENT</div><div class="s">TILING SERVICES</div></div></div>`,
    here('shared', 'lockup.png'));
  for (const [set, col] of Object.entries(ICON_SETS)) for (const n of ICONS) {
    const svg = fs.readFileSync(here('assets', 'icons', n + '.svg'), 'utf8').replace('<svg', '<svg style="width:24px;height:24px;display:block"');
    await snap(page, `<div id="x" style="width:24px;height:24px;color:${col};fill:${col}">${svg}</div>`, here('shared', `${n}-${set}.png`));
  }
}

// Headshot cut into three leaning slices. Mail apps cannot clip images, so the shape is baked into the PNG.
// Without a photo, a navy-and-cream stand-in figure is used.
async function buildPhoto(page, photo, file) {
  const SIZE = 160, LEAN = 59, GAP = 4.5, WIDTHS = [50, 27, 15]; // widths + gaps must add up to SIZE - LEAN
  console.assert(Math.abs(WIDTHS.reduce((a, b) => a + b) + GAP * (WIDTHS.length - 1) - (SIZE - LEAN)) < 0.01, 'slices must fill the square');
  const inner = photo
    ? `<img src="data:image/${path.extname(photo).slice(1).replace('jpg', 'jpeg')};base64,${fs.readFileSync(photo).toString('base64')}" style="width:100%;height:100%;object-fit:cover;object-position:50% 30%;display:block">`
    : `<div style="width:100%;height:100%;background:linear-gradient(160deg,#3A4556,${B.dark});position:relative"><div style="position:absolute;left:55px;top:30px;width:50px;height:50px;border-radius:50%;background:${B.cream}"></div><div style="position:absolute;left:25px;top:90px;width:110px;height:120px;border-radius:55px 55px 0 0;background:${B.cream}"></div></div>`;
  let x = 0, slices = '';
  for (const w of WIDTHS) {
    slices += `<div style="position:absolute;inset:0;clip-path:polygon(${x}px ${SIZE}px,${x + w}px ${SIZE}px,${x + w + LEAN}px 0,${x + LEAN}px 0)">${inner}</div>`;
    x += w + GAP;
  }
  await snap(page, `<div id="x" style="width:${SIZE}px;height:${SIZE}px;position:relative">${slices}</div>`, file);
}

function signatureHtml(p, nameSize) {
  const img = n => `../../shared/${n}.png`;
  const strip = (icon, alt, href, pad) => `        <tr><td style="padding:${pad};"><a href="${href}"><img src="${img(icon + '-light')}" width="18" height="18" alt="${alt}" style="display:block;border:0;"></a></td></tr>\n`;
  const row = (icon, alt, href, text, color = B.ink) => `        <tr><td style="padding:2px 8px 2px 0;vertical-align:middle;"><a href="${href}"><img src="${img(icon + '-brass')}" width="13" height="13" alt="${alt}" style="display:block;border:0;"></a></td>` +
    `<td style="font-size:12px;line-height:18px;vertical-align:middle;"><a href="${href}" style="color:${color};text-decoration:none;">${text}</a></td></tr>\n`;
  const mail = 'mailto:' + esc(p.email);
  return `<!-- ETS email signature for ${esc(p.name)}. Made by build.js - edit there, not here.
     Tables + inline styles only, so Gmail / Outlook / Apple Mail keep it intact. -->
<table cellpadding="0" cellspacing="0" border="0" style="font-family:${B.sans};color:${B.ink};border:1px solid ${B.line};border-radius:10px;background:#ffffff;">
  <tr>
    <td style="padding:16px 0 16px 16px;vertical-align:middle;">
      <table cellpadding="0" cellspacing="0" border="0" bgcolor="${B.dark}" style="border-radius:6px;background:${B.dark};">
${strip('globe', 'Website', SHOP.site, '10px 10px 6px')}${strip('instagram', 'Instagram', SHOP.instagram, '6px 10px')}${strip('facebook', 'Facebook', SHOP.facebook, '6px 10px')}${strip('mail', 'Email', mail, '6px 10px 10px')}      </table>
    </td>
    <td style="padding:16px 20px;vertical-align:middle;">
      <a href="${SHOP.site}"><img src="${img('lockup')}" width="173" height="36" alt="Excellent Tiling Services" style="display:block;border:0;margin-bottom:12px;"></a>
      <img src="name.png" width="${nameSize.w}" height="${nameSize.h}" alt="${esc(p.name)}" style="display:block;border:0;font-family:Georgia,serif;font-size:26px;color:${B.ink};">
      <table cellpadding="0" cellspacing="0" border="0" style="margin-top:2px;"><tr>
        <td style="vertical-align:middle;padding-right:8px;"><div style="width:22px;height:1px;line-height:1px;font-size:1px;background:${B.brass};">&nbsp;</div></td>
        <td style="font-size:11px;font-weight:bold;line-height:16px;letter-spacing:2px;text-transform:uppercase;color:${B.brass};vertical-align:middle;">${esc(p.title)}</td>
      </tr></table>
      <table cellpadding="0" cellspacing="0" border="0" style="margin-top:9px;">
${row('phone', 'Phone', tel(p.phone), esc(p.phone))}${row('mail', 'Email', mail, esc(p.email))}${p.email === SHOP.email ? '' : row('mail', 'Email', 'mailto:' + SHOP.email, SHOP.email)}${row('globe', 'Website', SHOP.site, SHOP.siteText)}${row('pin', 'Address', SHOP.maps, SHOP.address, B.muted)}      </table>
    </td>
    <td style="padding:16px 18px 16px 0;vertical-align:middle;">
      <img src="photo.png" width="160" height="160" alt="" style="display:block;border:0;">
    </td>
  </tr>
</table>
`;
}

(async () => {
  const a = args();
  const p = { name: a.name, title: a.title, email: a.email, phone: typeof a.phone === 'string' ? a.phone : SHOP.phone };
  const dir = here('people', p.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''));
  fs.mkdirSync(dir, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({ deviceScaleFactor: 3 });
  if (a.shared || !fs.existsSync(here('shared', 'lockup.png'))) await buildShared(page);

  // Name in the website's heading font (Instrument Serif), as an image so every mail app shows it.
  const nameSize = await snap(page, `<style>${font('IS', 'instrument-serif-latin-400-normal.woff2')}</style>
    <div id="x" style="display:inline-block;white-space:nowrap;font:30px/1.1 IS;color:${B.ink};letter-spacing:-.3px;padding:0 2px 2px 0">${esc(p.name)}</div>`, path.join(dir, 'name.png'));
  await buildPhoto(page, a.photo, path.join(dir, 'photo.png'));
  fs.writeFileSync(path.join(dir, 'signature.html'), signatureHtml(p, nameSize));

  // Preview picture, with Manrope loaded the way font-capable mail apps (Apple Mail) show it.
  const prev = await browser.newPage({ deviceScaleFactor: 2, viewport: { width: 760, height: 300 } });
  await prev.goto('file://' + path.join(dir, 'signature.html'));
  await prev.addStyleTag({ content: `body{margin:24px;background:#fff;display:inline-block}${font('Manrope', 'manrope-latin-500-normal.woff2', 400)}${font('Manrope', 'manrope-latin-700-normal.woff2', 700)}` });
  await prev.evaluate(() => document.fonts.ready);
  await (await prev.$('body')).screenshot({ path: path.join(dir, 'preview.png') });
  await browser.close();
  console.log('built', path.relative(process.cwd(), dir));
})();
