# Email signature

`signature.html` is the owner's email signature (card with logo, contact details, social icons and a diagonal-sliced headshot).
`preview.png` shows how it looks.

- 2026-11-12: first draft, then restyled to the LIVE website look: ink #15213A, dark navy #0F1A2C, brass #9C7744,
  Manrope text, Instrument Serif name, header-style logo (tile icon + EXCELLENT / TILING SERVICES). Icon and link on
  every line, both emails (yamen@ and contactus@). Name set to Yamen; `img/photo.png` is still a placeholder.
- Note: the colours were read from the live site, not from `theme/assets/ets-brand.css` in this repo, which still has
  the older palette (#193247, Fraunces / DM Sans). The repo theme copy needs a re-sync from Shopify.
- To put in the real headshot: `python3 make_photo.py headshot.jpg img/photo.png`.
- Still to do before it can be pasted into Gmail/Outlook: the images in `img/` must be hosted online
  (Shopify Files) and the `src` links in `signature.html` pointed at them. Mail apps drop images that only exist on a computer.
