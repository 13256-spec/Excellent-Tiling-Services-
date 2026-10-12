"""Premium sales posts (12 Oct 2026): real product photo + a navy caption band with the product
name, one benefit line and the live price. Feed 1080x1350, Story 1080x1920.
Usage: python3 make_premium.py plan.json outdir
plan.json: { "name": {"type": "main"|"story", "image": "src/file", "fit": "cover"|"studio",
             "title": "...", "line": "...", "price": "$189", "price_note": "chrome · from",
             "tag": "Shop · link in bio", "bg": "#F4F5F3" } }
"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
NAVY = (31, 49, 83); DEEP = (22, 36, 62); BLUE = (76, 142, 217); WHITE = (255, 255, 255)
PORCELAIN = (244, 245, 243); GREY = (195, 200, 204); INK = (42, 47, 54)
F = '/usr/share/fonts/opentype/inter/'
def font(name, size): return ImageFont.truetype(F + name, size)
H1 = lambda s: font('InterDisplay-SemiBold.otf', s)
H2 = lambda s: font('InterDisplay-Medium.otf', s)
BODY = lambda s: font('Inter-Regular.otf', s)
MED = lambda s: font('Inter-Medium.otf', s)

def hexrgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def load(path):
    im = Image.open(os.path.join(HERE, path))
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); return im
    return im.convert('RGB')

def cover(im, W, H):
    im = im.convert('RGB'); s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((l, t, l + W, t + H))

def studio(im, W, H, bg):
    """Fit a product shot inside a soft porcelain panel with a drop shadow."""
    canvas = Image.new('RGB', (W, H), bg)
    m = int(W * 0.10)
    if im.mode != 'RGBA':
        # white studio shot: make near-white transparent so it sits on the panel
        rgba = im.convert('RGBA'); px = rgba.load()
        for y in range(rgba.height):
            for x in range(rgba.width):
                r, g, b, a = px[x, y]
                if r > 240 and g > 240 and b > 240: px[x, y] = (r, g, b, 0)
        im = rgba
    bbox = im.split()[3].getbbox()
    if bbox: im = im.crop(bbox)
    im = im.copy(); im.thumbnail((W - 2 * m, H - 2 * m), Image.LANCZOS)
    x, y = (W - im.width) // 2, (H - im.height) // 2
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); sh.paste((20, 28, 45, 110), (0, 0), im.split()[3])
    shadow.paste(sh, (x + 10, y + 26), sh); shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    canvas = Image.alpha_composite(canvas.convert('RGBA'), shadow)
    canvas.paste(im, (x, y), im)
    return canvas.convert('RGB')

def wrap(draw, text, fnt, maxw):
    words = text.split(); lines = []; cur = ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if draw.textlength(t, font=fnt) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def build(p, W, H):
    band_h = 340 if H == 1350 else 380
    bg = hexrgb(p.get('bg', '#F4F5F3'))
    im = load(p['image'])
    z = p.get('zoom')  # keep only the central fraction of the photo before cropping
    if z:
        cw, ch = int(im.width * z), int(im.height * z)
        im = im.crop(((im.width - cw) // 2, (im.height - ch) // 2, (im.width + cw) // 2, (im.height + ch) // 2))
    photo_h = H - band_h
    photo = cover(im, W, photo_h) if p.get('fit', 'cover') == 'cover' else studio(im, W, photo_h, bg)
    out = Image.new('RGB', (W, H), NAVY); out.paste(photo, (0, 0))
    d = ImageDraw.Draw(out)
    # thin tile-blue grout line between photo and band
    d.rectangle([0, photo_h, W, photo_h + 6], fill=BLUE)
    pad = 56; y = photo_h + 6 + 36
    textw = W - 2 * pad - 300
    # title: shrink until it fits on two lines, prefer one
    for size in (50, 46, 42, 38):
        tf = H1(size); lines = wrap(d, p['title'], tf, textw)
        if len(lines) == 1 or size == 38: break
    lh = int(size * 1.16)
    for ln in lines[:2]:
        d.text((pad, y), ln, font=tf, fill=WHITE); y += lh
    # benefit line: shrink until it fits in the space left above the pill
    pill_top = H - 70 - 14
    for bsize in (30, 28, 26, 24):
        bf = BODY(bsize); bl = wrap(d, p['line'], bf, textw)
        if y + 6 + len(bl) * int(bsize * 1.35) <= pill_top - 12: break
    yy = y + 6
    for ln in bl[:3]:
        if yy + int(bsize * 1.35) > pill_top - 8: break
        d.text((pad, yy), ln, font=bf, fill=GREY); yy += int(bsize * 1.35)
    # price block, right
    pf = H1(74); pw = d.textlength(p['price'], font=pf)
    px = W - pad - pw; py = photo_h + 6 + 44
    d.text((px, py), p['price'], font=pf, fill=BLUE)
    nf = MED(24); note = p.get('price_note', '')
    if note:
        nw = d.textlength(note, font=nf); d.text((W - pad - nw, py + 86), note, font=nf, fill=GREY)
    # bottom row: tag pill + site
    tag = p.get('tag', 'Shop · link in bio'); tf2 = MED(26)
    tw = d.textlength(tag, font=tf2); ty = H - 70
    d.rounded_rectangle([pad, ty - 14, pad + tw + 36, ty + 34], radius=24, fill=DEEP, outline=BLUE, width=2)
    d.text((pad + 18, ty - 2), tag, font=tf2, fill=WHITE)
    site = 'excellenttilingservice.com.au'; sf = BODY(24); sw = d.textlength(site, font=sf)
    d.text((W - pad - sw, ty + 2), site, font=sf, fill=GREY)
    return out

if __name__ == '__main__':
    plan = json.load(open(sys.argv[1])); outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
    for name, p in plan.items():
        W, H = (1080, 1920) if p['type'] == 'story' else (1080, 1350)
        build(p, W, H).save(os.path.join(outdir, name + '.jpg'), quality=92)
        print(name)
