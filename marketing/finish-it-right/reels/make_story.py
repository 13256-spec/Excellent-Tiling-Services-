"""Story videos (1080x1920, 7 s): one store photo, slow push-in, CC0 music, no text (owner, 23 Oct 2026).
Usage: python3 make_story.py plan.json outdir   plan = {"<name>": {"img": "<handle>#<n>" | "file.jpg", "music": "x.mp3"}}"""
import json, os, subprocess, sys
from PIL import Image
from make_reel import load, is_studio, MUSIC, W, H, FPS

DUR = 7.0

def build(name, p, out, tmp):
    im = load(p['img']); w2, h2 = W * 2, H * 2
    if is_studio(im):  # product render on white: fit it, don't crop into the white
        c = Image.new('RGB', (w2, h2), 'white'); m = int(w2 * 0.08)
        im.thumbnail((w2 - 2 * m, w2 - 2 * m), Image.LANCZOS)
        c.paste(im, ((w2 - im.width) // 2, (h2 - im.height) // 2)); im = c
    else:
        s = max(w2 / im.width, h2 / im.height)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        l, t = (im.width - w2) // 2, (im.height - h2) // 2
        im = im.crop((l, t, l + w2, t + h2))
    photo = os.path.join(tmp, f'{name}-photo.jpg'); im.save(photo, quality=95)
    frames = round(DUR * FPS)
    vf = (f"zoompan=z='1+0.06*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS},"
          f"format=yuv420p,setsar=1")
    af = f"atrim=0:{DUR},afade=t=in:d=0.8,afade=t=out:st={DUR - 1.5}:d=1.5,loudnorm=I=-18"
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-loop', '1', '-t', str(DUR), '-i', photo, '-i', os.path.join(MUSIC, p['music']),
                    '-vf', vf, '-af', af, '-t', str(DUR), '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
                    '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], check=True)

if __name__ == '__main__':
    plan = json.load(open(sys.argv[1])); outdir = sys.argv[2]
    tmp = os.path.join(outdir, 'tmp'); os.makedirs(tmp, exist_ok=True)
    for name, p in plan.items():
        build(name, p, os.path.join(outdir, f'{name}.mp4'), tmp); print(name, p['music'])
