# Email signature

`signature.html` is the owner's email signature (card with logo, contact details, social icons and a diagonal-sliced headshot).
`preview.png` shows how it looks.

- 2026-11-12: first draft. Name set to Yamen; `img/photo.png` is still a grey placeholder.
- To put in the real headshot: `python3 make_photo.py headshot.jpg img/photo.png`.
- Still to do before it can be pasted into Gmail/Outlook: the images in `img/` must be hosted online
  (Shopify Files) and the `src` links in `signature.html` pointed at them. Mail apps drop images that only exist on a computer.
