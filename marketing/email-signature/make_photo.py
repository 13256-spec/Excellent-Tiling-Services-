"""Cut a headshot into the diagonal-slice shape used in the email signature.

Usage: python3 make_photo.py photo.jpg [img/photo.png]
Email clients cannot do this with CSS, so the slices are baked into a transparent PNG.
"""
import sys
from PIL import Image, ImageDraw, ImageOps

SIZE = 320          # output is SIZE x SIZE px (shown at 160 in the signature, so it stays sharp)
SHEAR = 118         # how far the top of each slice leans right
GAP = 9             # see-through gap between slices
WIDTHS = (100, 54, 30)  # slice widths, left to right; with gaps they fill SIZE - SHEAR


def mask(size=SIZE, ss=4):
    assert sum(WIDTHS) + GAP * (len(WIDTHS) - 1) == size - SHEAR, "slices must fill the square"
    m = Image.new("L", (size * ss, size * ss), 0)
    d = ImageDraw.Draw(m)
    x = 0
    for w in WIDTHS:
        d.polygon([(x * ss, size * ss), ((x + w) * ss, size * ss),
                   ((x + w + SHEAR) * ss, 0), ((x + SHEAR) * ss, 0)], fill=255)
        x += w + GAP
    return m.resize((size, size), Image.LANCZOS)


def make(src, dst):
    img = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    img = ImageOps.fit(img, (SIZE, SIZE), Image.LANCZOS, centering=(0.5, 0.35))  # keep the face, not the chest
    img.putalpha(mask())
    img.save(dst, optimize=True)


if __name__ == "__main__":
    m = mask()
    assert m.getpixel((2, 2)) == 0 and m.getpixel((SIZE - 10, 3)) == 255 and m.getpixel((10, SIZE - 3)) == 255
    if len(sys.argv) < 2:
        sys.exit("mask ok. usage: make_photo.py photo.jpg [out.png]")
    make(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "img/photo.png")
