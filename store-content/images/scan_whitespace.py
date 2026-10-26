import json, urllib.request, io, sys, concurrent.futures as cf
from PIL import Image, ImageChops
prods = []
for page in range(1, 10):
    with urllib.request.urlopen(f"https://excellenttilingservices.com/products.json?limit=250&page={page}", timeout=60) as r:
        d = json.load(r)["products"]
    if not d: break
    prods += d
print("products", len(prods), file=sys.stderr)
jobs = [(p["handle"], p["product_type"], p["vendor"], i, im["src"], im["width"], im["height"]) for p in prods for i, im in enumerate(p["images"])]
print("images", len(jobs), file=sys.stderr)
def fill(job):
    handle, ptype, vendor, i, src, w, h = job
    try:
        u = src.split("?")[0] + "?width=300"
        with urllib.request.urlopen(u, timeout=60) as r: im = Image.open(io.BytesIO(r.read()))
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA"); a = im.split()[-1]
            bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=a); im = bg
        im = im.convert("RGB")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        diff = ImageChops.difference(im, bg).convert("L").point(lambda p: 255 if p > 14 else 0)
        box = diff.getbbox()
        if not box: return (handle, ptype, vendor, i, src, w, h, 0, 0, None)
        return (handle, ptype, vendor, i, src, w, h, (box[2]-box[0])/im.size[0], (box[3]-box[1])/im.size[1], box)
    except Exception as e:
        return (handle, ptype, vendor, i, src, w, h, -1, -1, str(e))
with cf.ThreadPoolExecutor(16) as ex: res = list(ex.map(fill, jobs))
json.dump(res, open("scan/fill.json", "w"))
print("done", file=sys.stderr)
