"""Photo Reels for Instagram + Facebook (1080x1920, 30 fps) from the store's own photos.

Usage: python3 make_reel.py plan.json outdir

plan.json = {"<name>": {"music": "mellow-chill.mp3",
                        "slides": [{"img": "moon.jpg" | "p/x.jpg" | "<handle>#<n>",
                                    "title": "Time Stone Moon", "line": "Matt $50.10/m2 . 300x600 or 600x600"}, ...],
                        "end": ["excellenttilingservices.com", "Perth delivery . Free pickup in Maddington"]}}

Look: porcelain-white canvas, one photo per slide (room shots cover-cropped, studio shots on white),
slow 5% push-in, 0.6 s dissolve between slides, product name and price in navy Archivo under the photo.
No cards, no gradients, no stickers. Music is CC0 (../v2/source/music/credits.json), faded in and out.
"""
import io
import json
import os
import subprocess
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'v2', 'source')
IMG = os.path.join(SRC, 'img')
MUSIC = os.path.join(SRC, 'music')
FONT = os.path.join(HERE, 'Archivo.ttf')
W, H, FPS = 1080, 1920, 30
SLIDE_S, FADE_S, END_S = 3.4, 0.6, 2.6
PORCELAIN, NAVY, GREY = (244, 245, 243), (31, 49, 83), (120, 128, 136)
_cache = {}


def product_images(handle):
    if handle not in _cache:
        with urllib.request.urlopen(f'https://excellenttilingservices.com/products/{handle}.json') as r:
            _cache[handle] = [i['src'] for i in json.load(r)['product']['images']]
    return _cache[handle]


def load(src):
    if '#' in src:
        h, i = src.split('#')
        with urllib.request.urlopen(product_images(h)[int(i)]) as r:
            im = Image.open(io.BytesIO(r.read()))
    else:
        im = Image.open(os.path.join(IMG, src))
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGBA', im.size, 'white'); bg.alpha_composite(im); im = bg
    return im.convert('RGB')


def is_studio(im):
    w, h = im.size
    return all(min(im.getpixel(p)) > 238 for p in [(2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)])


def photo_box(im):
    """Photo zone on the canvas: full width, height from the photo's own shape (max 4:5), centred."""
    ph = min(1350, round(W * im.height / im.width))
    if is_studio(im):
        ph = 1080
    return ph


def render_photo(im, ph, path):
    """2x-size photo for zoompan, cover-cropped (room shots) or fitted on white (studio shots)."""
    w2, h2 = W * 2, ph * 2
    if is_studio(im):
        c = Image.new('RGB', (w2, h2), 'white'); m = int(w2 * 0.07)
        im = im.copy(); im.thumbnail((w2 - 2 * m, h2 - 2 * m), Image.LANCZOS)
        c.paste(im, ((w2 - im.width) // 2, (h2 - im.height) // 2))
    else:
        s = max(w2 / im.width, h2 / im.height)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        l, t = (im.width - w2) // 2, (im.height - h2) // 2
        c = im.crop((l, t, l + w2, t + h2))
    c.save(path, quality=95)


def text_layer(ph, title, line, path):
    """Canvas with the photo zone left transparent and the caption under it."""
    c = Image.new('RGBA', (W, H), PORCELAIN + (255,))
    top = (H - ph) // 2 - 60
    d = ImageDraw.Draw(c)
    d.rectangle((0, top, W, top + ph), fill=(0, 0, 0, 0))
    f1 = ImageFont.truetype(FONT, 58); f2 = ImageFont.truetype(FONT, 42)
    y = top + ph + 54
    d.text((72, y), title, font=f1, fill=NAVY + (255,))
    d.text((72, y + 84), line, font=f2, fill=GREY + (255,))
    c.save(path)
    return top


def end_card(lines, path):
    c = Image.new('RGB', (W, H), PORCELAIN)
    d = ImageDraw.Draw(c)
    f1 = ImageFont.truetype(FONT, 64); f2 = ImageFont.truetype(FONT, 42)
    y = H // 2 - 70
    for i, t in enumerate(lines):
        f = f1 if i == 0 else f2
        tw = d.textlength(t, font=f)
        d.text(((W - tw) / 2, y), t, font=f, fill=NAVY if i == 0 else GREY)
        y += 96 if i == 0 else 60
    c.save(path)


def build(name, p, out, tmp):
    slides = p['slides']
    inputs, filters, labels = [], [], []
    n_in = 0  # number of ffmpeg inputs added so far
    frames = round(SLIDE_S * FPS)
    for n, s in enumerate(slides):
        im = load(s['img']); ph = photo_box(im)
        photo = os.path.join(tmp, f'{name}-{n}-photo.jpg'); layer = os.path.join(tmp, f'{name}-{n}-text.png')
        render_photo(im, ph, photo); top = text_layer(ph, s['title'], s['line'], layer)
        i = n_in; n_in += 2
        inputs += ['-loop', '1', '-t', str(SLIDE_S), '-i', photo, '-loop', '1', '-t', str(SLIDE_S), '-i', layer]
        filters.append(
            f"[{i}:v]zoompan=z='1+0.05*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{ph}:fps={FPS}[z{n}];"
            f"color=c=0xF4F5F3:s={W}x{H}:r={FPS}:d={SLIDE_S}[bg{n}];[bg{n}][z{n}]overlay=0:{top}[c{n}];"
            f"[c{n}][{i + 1}:v]overlay=0:0:format=auto,format=yuv420p,setsar=1[s{n}]")
        labels.append(f'[s{n}]')
    endp = os.path.join(tmp, f'{name}-end.png'); end_card(p['end'], endp)
    i = n_in; n_in += 1
    inputs += ['-loop', '1', '-t', str(END_S), '-i', endp]
    filters.append(f'[{i}:v]fps={FPS},format=yuv420p,setsar=1[s{len(slides)}]'); labels.append(f'[s{len(slides)}]')
    # dissolve chain
    prev = labels[0]; offset = 0.0; durs = [SLIDE_S] * len(slides) + [END_S]
    for n in range(1, len(labels)):
        offset += durs[n - 1] - FADE_S
        o = f'[x{n}]' if n < len(labels) - 1 else '[v]'
        filters.append(f'{prev}{labels[n]}xfade=transition=fade:duration={FADE_S}:offset={offset:.3f}{o}')
        prev = o
    total = sum(durs) - FADE_S * (len(durs) - 1)
    music = os.path.join(MUSIC, p['music'])
    inputs += ['-i', music]; aidx = n_in; n_in += 1
    filters.append(f'[{aidx}:a]atrim=0:{total:.3f},afade=t=in:d=1,afade=t=out:st={total - 2:.3f}:d=2,loudnorm=I=-18[a]')
    cmd = ['ffmpeg', '-y', '-v', 'error'] + inputs + ['-filter_complex', ';'.join(filters), '-map', '[v]', '-map', '[a]',
           '-t', f'{total:.3f}', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
           '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True)
    return total


if __name__ == '__main__':
    plan = json.load(open(sys.argv[1])); outdir = sys.argv[2]
    tmp = os.path.join(outdir, 'tmp'); os.makedirs(tmp, exist_ok=True)
    for name, p in plan.items():
        out = os.path.join(outdir, f'{name}.mp4')
        secs = build(name, p, out, tmp)
        print(name, f'{secs:.1f}s', p['music'])
