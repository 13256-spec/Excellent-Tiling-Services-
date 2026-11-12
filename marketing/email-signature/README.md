# Email signatures

One command builds the ETS email signature for any staff member: a card with the website logo, name, title,
contact lines (each with an icon and a link), social icons and a diagonal-sliced headshot.
Example: `people/yamen-alsulaiman/preview.png`.

## Make a signature for a new person

You need their full name, job title, company email and a head-and-shoulders photo on a plain background (JPG or PNG).

```
cd marketing/email-signature
node build.js --name "Jane Smith" --title "Showroom Manager" --email jane@excellenttilingservices.com --photo jane.jpg
```

- `--phone "0400 000 000"` if they have their own number. Left out, the shop number 0450 960 543 is used.
- `--photo` left out shows the navy-and-cream stand-in figure (already online). Run it again with `--photo` once they have one.
- The result goes in `people/jane-smith/`: `signature.html`, `name.png`, `preview.png` (and `photo.png`). Check `preview.png`.
- The build ends by listing any images that are not online yet. Until that list is empty the signature is not ready.
- Needs Node with Playwright and Chromium (already present in Claude Code cloud sessions). Nothing else to install:
  fonts, icons and the tile mark are in `assets/`.

## Put it into a mail app

Mail apps only show images that are hosted online, so before anyone can use a signature:

1. The logo and icons are already online (Shopify Files, named `ets-signature-...`), listed in `hosted.json`.
   Only the new person's `name.png` (and `photo.png`) need uploading. This needs the owner's OK.
   How: commit and push the images, then run the Shopify `fileCreate` mutation with `originalSource` set to each
   image's `raw.githubusercontent.com` link (use the commit id, not the branch name) and a `filename` like
   `ets-signature-name-jane-smith.png`. Read the links back with `files(query: "filename:ets-signature*")`.
2. Add each link to `hosted.json` (`"people/jane-smith/name.png": "https://cdn.shopify.com/..."`) and run the build
   again. It should now finish without the "not online yet" list.
3. Open `signature.html` in a browser, select all, copy, and paste into the signature box:
   Gmail: Settings > See all settings > Signature. Outlook.com / Hotmail: gear icon > Account > Signatures
   (older layout: Mail > Compose and reply).
   Apple Mail: Settings > Signatures.

## How the look was made

Everything matches the live website (excellenttilingservices.com, read on 12 Nov 2026). The values sit at the top of `build.js`.

| Part | Choice | Where it comes from |
|---|---|---|
| Text, name | Ink navy `#15213A` | site text colour |
| Icon strip | Dark navy `#0F1A2C`, icons `#E9D6B5` | site top bar |
| Title, contact icons | Brass `#9C7744` | site accent |
| Address | Muted `#6A6862` | site muted text |
| Card | White, 10px corners, 6px on the strip | site cards |
| Logo | Tile icon + EXCELLENT / TILING SERVICES in Manrope | site header |
| Name | Instrument Serif | site headings |
| Text | Manrope, falling back to Arial | site body text |

Rules that keep it working in Gmail, Outlook and Apple Mail:

- Tables and inline styles only. No CSS classes, no flexbox.
- The logo and the name are images, because Gmail and Outlook block custom fonts. The contact lines stay real text,
  so they show in Arial there.
- The photo slices are baked into a see-through PNG, because mail apps cannot clip images.
- Images are saved at 3x size and shown small, so they stay sharp on phones.
- Every icon and line is a link: phone starts a call, emails open a new message, the address opens Google Maps.

If the website's colours, fonts or logo change, update the values at the top of `build.js`, then rebuild each person
with `--shared` added once to refresh the logo and icons.

Icons: Lucide (ISC licence) and Simple Icons (CC0). Fonts: Manrope and Instrument Serif (SIL Open Font Licence).

## Change log

- 2026-11-12: first version. Built for the owner (Yamen Alsulaiman, CEO), with the stand-in figure until he has a photo. With the owner's OK,
  11 images were uploaded to Shopify Files (logo, 8 icons, his name, the stand-in photo figure) and linked in `hosted.json`; his
  `signature.html` is ready to paste. Not yet uploaded (unused so far): `phone-light`, `pin-light`,
  `instagram-brass`, `facebook-brass`.
- Note: the colours were read from the live site, not from `theme/assets/ets-brand.css` in this repo, which still has
  an older palette (`#193247`, Fraunces / DM Sans). The repo theme copy needs a re-sync from Shopify.
