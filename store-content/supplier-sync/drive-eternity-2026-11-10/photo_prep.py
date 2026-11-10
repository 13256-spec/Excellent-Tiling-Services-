"""Resize and convert the supplier photos listed in photo-plan.json for upload to Shopify.

Usage: python photo_prep.py <output folder>   (reads D:/Eternity, the owner's external drive)
Each entry becomes <handle>-<n>.jpg at most 2400 px (PNG kept only when it has transparency).
Upload afterwards with stagedUploadsCreate -> curl POST -> productUpdate(media:).
"""
import os, sys, json
from PIL import Image

E = "D:/Eternity"
OUT = sys.argv[1]
plan = json.load(open(os.path.join(os.path.dirname(__file__), "photo-plan.json")))
for p in plan:
    src = os.path.join(E, p["source"])
    if not os.path.exists(src):
        print("MISSING", src); continue
    im = Image.open(src)
    keep_png = im.mode in ("RGBA", "LA", "P") and src.lower().endswith(".png")
    im = im.convert("RGBA" if keep_png else "RGB")
    im.thumbnail((2400, 2400))
    out = os.path.join(OUT, p["file"] if not keep_png else p["file"][:-4] + ".png")
    im.save(out, quality=88) if not keep_png else im.save(out, optimize=True)
    print(im.width, im.height, out)
