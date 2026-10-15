"""Turn finished v3 graphics into short videos with background music.

Usage: python3 make_video.py <date> [<date> ...]   e.g. 2026-10-07
For each date: out3/<date>-story.png -> outvid/<date>-story.mp4 (10 s, 1080x1920)
               out3/<date>-main.png  -> outvid/<date>-main.mp4  (12 s, 1080x1350, posted as a Reel)
Slow 4% zoom, music faded in and out, loudness normalised. Music is CC0 only (music/credits.json),
rotated by date so the same track doesn't repeat two days running.
"""
import datetime
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STORY_TRACKS = ["lofi-epiano.mp3", "lofi-jazz-organ.mp3", "spacey-lofi.mp3", "lofi-guitar.mp3", "aesthetic-lofi.mp3"]
MAIN_TRACKS = ["mellow-chill.mp3", "melodic-deep-house.mp3", "uplifting-ambient.mp3", "acoustic-keys.mp3", "aesthetic-lofi.mp3"]


def render(png, track, out, w, h, secs):
    frames = secs * 30
    vf = (f"[0:v]scale={w*2}:{h*2},zoompan=z='1+0.04*on/{frames}':x='iw/2-(iw/zoom/2)':"
          f"y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps=30,format=yuv420p[v];"
          f"[1:a]atrim=0:{secs},afade=t=in:d=0.8,afade=t=out:st={secs-1.5}:d=1.5,loudnorm=I=-16[a]")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", png, "-i", track,
                    "-filter_complex", vf, "-map", "[v]", "-map", "[a]", "-t", str(secs),
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", out], check=True)


def main(dates):
    os.makedirs(os.path.join(HERE, "outvid"), exist_ok=True)
    used = {}
    for d in dates:
        n = datetime.date.fromisoformat(d).toordinal()
        for slot, tracks, (w, h, secs) in (("story", STORY_TRACKS, (1080, 1920, 10)),
                                            ("main", MAIN_TRACKS, (1080, 1350, 12))):
            png = os.path.join(HERE, "out3", f"{d}-{slot}.png")
            if not os.path.exists(png):
                continue
            track = tracks[n % len(tracks)]
            out = os.path.join(HERE, "outvid", f"{d}-{slot}.mp4")
            render(png, os.path.join(HERE, "music", track), out, w, h, secs)
            used[f"{d}-{slot}"] = track
            print(out, track)
    log = os.path.join(HERE, "outvid", "music-used.json")
    old = json.load(open(log)) if os.path.exists(log) else {}
    old.update(used)
    json.dump(old, open(log, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
