"""Hook Reels (owner asked for Reels that convert, 23 Oct 2026). 1080x1920, 30 fps.

plan.json = {"<name>": {"music": "x.mp3",
   "hook": {"img": "paddy750.jpg", "lines": ["3 vanities", "under $1,000"]},
   "slides": [{"img": "<handle>#<n>" | "file.jpg", "title": "MELA CLARK 600", "line": "$749 · stone top and basin"}, ...],
   "end": ["Every price online", "Free pickup in Maddington"]}}

Look: full-bleed photos (studio shots fitted on porcelain white), 2 s a slide, 0.3 s cuts, 8% push-in.
Hook: big porcelain-white Archivo on a solid navy block, top left, first 2.2 s. Product slides: name and
price on a solid navy strip along the bottom. End card: navy, site name, two lines, "Link in bio".
Brand colours only, no gradients, no stickers. Music CC0 from ../v2/source/music.
"""
import json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
from make_reel import load, is_studio, MUSIC, FONT, W, H, FPS, PORCELAIN, NAVY

HOOK_S, SLIDE_S, END_S, FADE_S = 2.2, 2.0, 2.4, 0.3
WHITE = (244, 245, 243)


def full_bleed(im):
    w2, h2 = W * 2, H * 2
    if is_studio(im):
        c = Image.new('RGB', (w2, h2), 'white'); m = int(w2 * 0.1)
        im = im.copy(); im.thumbnail((w2 - 2 * m, h2 - 2 * m - 700), Image.LANCZOS)
        c.paste(im, ((w2 - im.width) // 2, (h2 - im.height) // 2 - 150)); return c
    s = max(w2 / im.width, h2 / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    l, t = (im.width - w2) // 2, (im.height - h2) // 2
    return im.crop((l, t, l + w2, t + h2))


def hook_layer(lines, path):
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    f = ImageFont.truetype(FONT, 112); y = 300
    for t in lines:
        tw = d.textlength(t, font=f)
        d.rectangle((60, y - 18, 60 + tw + 60, y + 128), fill=NAVY + (255,))
        d.text((90, y), t, font=f, fill=WHITE + (255,)); y += 160
    c.save(path)


def strip_layer(title, line, path):
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rectangle((0, H - 330, W, H), fill=NAVY + (255,))
    f1 = ImageFont.truetype(FONT, 64); f2 = ImageFont.truetype(FONT, 50)
    d.text((72, H - 290), title, font=f1, fill=WHITE + (255,))
    d.text((72, H - 190), line, font=f2, fill=(195, 200, 204, 255))
    c.save(path)


def end_card(lines, path):
    c = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(c)
    f1 = ImageFont.truetype(FONT, 72); f2 = ImageFont.truetype(FONT, 52); f3 = ImageFont.truetype(FONT, 46)
    y = H // 2 - 200
    for i, t in enumerate(['excellenttilingservice.com.au'] + lines + ['Link in bio']):
        f = f1 if i == 0 else (f3 if t == 'Link in bio' else f2)
        tw = d.textlength(t, font=f); d.text(((W - tw) / 2, y), t, font=f, fill=WHITE if i == 0 else (195, 200, 204)); y += 110 if i == 0 else 80
    c.save(path)


def build(name, p, out, tmp):
    items = [(p['hook']['img'], 'hook', HOOK_S)] + [(s['img'], s, SLIDE_S) for s in p['slides']]
    inputs, filters, labels, durs = [], [], [], []
    n_in = 0
    for n, (img, meta, dur) in enumerate(items):
        photo = os.path.join(tmp, f'{name}-{n}-photo.jpg'); layer = os.path.join(tmp, f'{name}-{n}-layer.png')
        full_bleed(load(img)).save(photo, quality=95)
        if meta == 'hook': hook_layer(p['hook']['lines'], layer)
        else: strip_layer(meta['title'], meta['line'], layer)
        frames = round(dur * FPS); i = n_in; n_in += 2
        inputs += ['-loop', '1', '-t', str(dur), '-i', photo, '-loop', '1', '-t', str(dur), '-i', layer]
        filters.append(f"[{i}:v]zoompan=z='1+0.08*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS}[z{n}];"
                       f"[z{n}][{i + 1}:v]overlay=0:0:format=auto,format=yuv420p,setsar=1[s{n}]")
        labels.append(f'[s{n}]'); durs.append(dur)
    endp = os.path.join(tmp, f'{name}-end.png'); end_card(p['end'], endp)
    i = n_in; n_in += 1
    inputs += ['-loop', '1', '-t', str(END_S), '-i', endp]
    filters.append(f'[{i}:v]fps={FPS},format=yuv420p,setsar=1[s{len(items)}]'); labels.append(f'[s{len(items)}]'); durs.append(END_S)
    prev = labels[0]; offset = 0.0
    for n in range(1, len(labels)):
        offset += durs[n - 1] - FADE_S
        o = f'[x{n}]' if n < len(labels) - 1 else '[v]'
        filters.append(f'{prev}{labels[n]}xfade=transition=fade:duration={FADE_S}:offset={offset:.3f}{o}'); prev = o
    total = sum(durs) - FADE_S * (len(durs) - 1)
    inputs += ['-i', os.path.join(MUSIC, p['music'])]; aidx = n_in
    filters.append(f'[{aidx}:a]atrim=0:{total:.3f},afade=t=in:d=0.5,afade=t=out:st={total - 1.5:.3f}:d=1.5,loudnorm=I=-16[a]')
    subprocess.run(['ffmpeg', '-y', '-v', 'error'] + inputs + ['-filter_complex', ';'.join(filters), '-map', '[v]', '-map', '[a]',
                    '-t', f'{total:.3f}', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)
    return total


if __name__ == '__main__':
    plan = json.load(open(sys.argv[1])); outdir = sys.argv[2]
    tmp = os.path.join(outdir, 'tmp'); os.makedirs(tmp, exist_ok=True)
    for name, p in plan.items():
        print(name, f'{build(name, p, os.path.join(outdir, name + ".mp4"), tmp):.1f}s')
