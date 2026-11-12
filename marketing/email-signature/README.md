# Email signatures

One command builds the ETS email signature for any staff member: a card with the website logo, name, title,
contact lines (each with an icon and a link), social icons and a diagonal-sliced headshot.
Example: `people/yamen-alsulaiman/preview.png` (and `preview-dark.png` for a dark-mode email).

## Make a signature for a new person

You need their full name, job title, company email and a head-and-shoulders photo on a plain background (JPG or PNG).

```
cd marketing/email-signature
node build.js --name "Jane Smith" --title "Showroom Manager" --email jane@excellenttilingservices.com --photo jane.jpg
```

- `--phone "0400 000 000"` if they have their own number. Left out, the shop number 0450 960 543 is used.
- `--photo` left out shows the navy-and-cream stand-in figure. Run it again with `--photo` once they have one.
- The result goes in `people/jane-smith/`: `signature.html`, about 12 image pieces, `preview.png`, `preview-dark.png`.
  Check both previews.
- The build ends by listing any images that are not online yet. Until that list is empty the signature is not ready.
- Needs Node with Playwright and Chromium (already present in Claude Code cloud sessions). Nothing else to install:
  fonts, icons and the tile mark are in `assets/`.

## Put it into a mail app

Mail apps only show images that are hosted online, so before anyone can use a signature:

1. Upload the person's image pieces (`people/jane-smith/*.png`, not the previews) to Shopify Files. This needs the
   owner's OK. How: commit and push, then run the Shopify `fileCreate` mutation with `originalSource` set to each
   image's `raw.githubusercontent.com` link (use the commit id, not the branch name), `contentType: IMAGE` and a
   `filename` like `ets-sig-jane-smith-logo.png`. Read the links back with `nodes(ids: [...])` on the ids it returns.
2. Add each link to `hosted.json` (`"people/jane-smith/logo.png": "https://cdn.shopify.com/..."`) and run the build
   again. It should now finish without the "not online yet" list.
3. Open `signature.html` in a browser, select all, copy, and paste into the signature box:
   Gmail: Settings > See all settings > Signature. Outlook.com / Hotmail: gear icon > Account > Signatures
   (older layout: Mail > Compose and reply). Apple Mail: Settings > Signatures.

Any change to a person's details or photo means new pieces. Replace the existing files in place with the Shopify
`fileUpdate` mutation (`id` + new `originalSource`), read back the links (the `?v=` number changes), update
`hosted.json`, rebuild, and paste again.

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
| Text | Manrope | site body text |

How it is built, and why:

- `build.js` draws the whole card once as a web page, then cuts it into image pieces. `signature.html` is just a
  table that puts the pieces back together, each piece wrapped in its own link.
- Images only, no live text. The first version used real text and coloured table cells; in Hotmail dark mode the
  white card turned black, the navy strip turned pale and the navy text vanished. Dark mode recolours text and
  backgrounds but leaves images alone. It also means the website fonts show everywhere (Gmail and Outlook block them).
- The trade-off: the text cannot be selected and copied, and if a reader's mail app blocks images they see the
  plain details instead (each piece carries its text as a fallback).
- Pieces are saved at 3x size and shown small, so they stay sharp on phones.
- Every icon and line is a link: phone starts a call, emails open a new message, the address opens Google Maps.

If the website's colours, fonts or logo change, update the values at the top of `build.js` and rebuild each person.

Icons: Lucide (ISC licence) and Simple Icons (CC0). Fonts: Manrope and Instrument Serif (SIL Open Font Licence).

## Change log

- 2026-11-12: first version, built for the owner (Yamen Alsulaiman, CEO) with the stand-in figure until he has a photo.
  After a Hotmail dark-mode test showed the card recoloured, rebuilt as image pieces. With the owner's OK his 12
  pieces are on Shopify Files (`ets-sig-yamen-alsulaiman-*.png`) and linked in `hosted.json`.
- 2026-11-12: card shrunk to 80% (415px wide, `SCALE` at the top of `build.js`) after the owner found 518px too big
  in Outlook. His 12 files were replaced in place.
- 2026-11-12: made narrower again at the owner's request (370px wide): tighter side spacing and a smaller photo
  panel (`K` in `photoHtml`). Note: the preview loads the online images, so after a size change it looks stretched
  until the new pieces are uploaded and `hosted.json` is updated.
- Leftovers on Shopify Files from the first version, no longer used: 11 files named `ets-signature-*.png`
  (logo, icons, name, placeholder). Safe to delete, but only on the owner's instruction.
- Note: the colours were read from the live site, not from `theme/assets/ets-brand.css` in this repo, which still has
  an older palette (`#193247`, Fraunces / DM Sans). The repo theme copy needs a re-sync from Shopify.
