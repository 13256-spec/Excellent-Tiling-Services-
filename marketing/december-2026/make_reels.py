#!/usr/bin/env python3
"""Weekly photo Reels from the Canva Story PNGs: slow push-in, dissolves, CC0 music.
Usage: python3 make_reels.py   (needs ffmpeg; reads REELS below, writes reels/<name>.mp4)"""
import os, subprocess
D = os.path.dirname(os.path.abspath(__file__))
MUSIC = os.path.join(D, "..", "finish-it-right", "v2", "source", "music")
S, F, FPS = 3.2, 0.6, 30  # seconds per slide, dissolve, frame rate
REELS = {  # name: (music, story pages)
    "2026-11-29-reel-bathroom-picks": ("mellow-chill.mp3", [2, 1, 5, 7]),
    "2026-12-06-reel-vanities": ("lofi-epiano.mp3", [8, 14, 2, 20]),
    "2026-12-13-reel-mirrors-and-taps": ("acoustic-keys.mp3", [16, 5, 13, 17]),
    "2026-12-20-reel-tiles-and-basins": ("uplifting-ambient.mp3", [3, 9, 24, 27]),
}
def build(name, music, pages):
    ins, flt = [], []
    for i, n in enumerate(pages):
        ins += ["-loop", "1", "-t", str(S), "-i", f"{D}/stories/{n:02d}.png"]
        fr = round(S * FPS)
        flt.append(f"[{i}:v]scale=2160:3840,zoompan=z='1+0.04*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps={FPS},format=yuv420p,setsar=1[s{i}]")
    prev, off = "[s0]", 0.0
    for i in range(1, len(pages)):
        off += S - F; o = "[v]" if i == len(pages) - 1 else f"[x{i}]"
        flt.append(f"{prev}[s{i}]xfade=transition=fade:duration={F}:offset={off:.2f}{o}"); prev = o
    total = S * len(pages) - F * (len(pages) - 1); a = len(pages)
    flt.append(f"[{a}:a]atrim=0:{total:.2f},afade=t=in:d=1,afade=t=out:st={total-2:.2f}:d=2,loudnorm=I=-18[a]")
    os.makedirs(f"{D}/reels", exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-i", f"{MUSIC}/{music}", "-filter_complex", ";".join(flt),
                    "-map", "[v]", "-map", "[a]", "-t", f"{total:.2f}", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", f"{D}/reels/{name}.mp4"], check=True)
if __name__ == "__main__":
    for name, (music, pages) in REELS.items():
        build(name, music, pages); print(name)
