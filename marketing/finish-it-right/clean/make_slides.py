"""Clean look (owner approved 11 Oct 2026): real store photos only, no text on images.
Feed slides 1080x1350, Story 1080x1920. Studio shots on white are fitted with margin on white;
room shots are cover-cropped. Usage: python3 make_slides.py plan.json outdir"""
import json, sys, os, io, urllib.request
from PIL import Image

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'v2', 'source', 'img')
_cache = {}

def product_images(handle):
    if handle not in _cache:
        with urllib.request.urlopen(f'https://excellenttilingservice.com.au/products/{handle}.json') as r:
            _cache[handle] = [i['src'] for i in json.load(r)['product']['images']]
    return _cache[handle]

def load(src):
    if src.startswith('local:'):
        return Image.open(os.path.join(IMG, src[6:])).convert('RGB')
    h, i = src.split('#')
    with urllib.request.urlopen(product_images(h)[int(i)]) as r:
        im = Image.open(io.BytesIO(r.read()))
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGBA', im.size, 'white'); bg.alpha_composite(im); im = bg
    return im.convert('RGB')

def is_studio(im):
    w, h = im.size
    pts = [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)]
    return all(min(im.getpixel(p)) > 238 for p in pts)

def slide(im, W, H):
    if is_studio(im):
        c = Image.new('RGB', (W, H), 'white'); m = int(W * 0.08)
        im.thumbnail((W - 2 * m, H - 2 * m), Image.LANCZOS)
        c.paste(im, ((W - im.width) // 2, (H - im.height) // 2)); return c
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((l, t, l + W, t + H))

plan = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
for name, p in plan.items():
    W, H = (1080, 1920) if p['type'] == 'story' else (1080, 1350)
    for n, src in enumerate(p['images'], 1):
        slide(load(src), W, H).save(os.path.join(out, f'{name}-{n}.jpg'), quality=90)
    print(name, len(p['images']))
