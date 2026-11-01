"""Median Lighthouse metrics per label and form factor, and the before/after diff.
Usage: python3 lighthouse/diff.py <before-label> [after-label]"""
import json, statistics, sys, glob, os
HERE = os.path.dirname(os.path.abspath(__file__))
METRICS = [  # (label, audit id or category, unit, lower is better)
    ("Performance", "cat:performance", "score", False),
    ("Accessibility", "cat:accessibility", "score", False),
    ("Best practices", "cat:best-practices", "score", False),
    ("SEO", "cat:seo", "score", False),
    ("First Contentful Paint", "first-contentful-paint", "ms", True),
    ("Largest Contentful Paint", "largest-contentful-paint", "ms", True),
    ("Total Blocking Time", "total-blocking-time", "ms", True),
    ("Cumulative Layout Shift", "cumulative-layout-shift", "", True),
    ("Speed Index", "speed-index", "ms", True),
    ("DOM elements", "dom-size-insight", "", True),
    ("Page weight", "total-byte-weight", "KB", True),
]

def value(r, key):
    if key.startswith("cat:"):
        s = r["categories"].get(key[4:], {}).get("score")
        return None if s is None else round(s * 100)
    a = r["audits"].get(key, {})
    v = a.get("numericValue")
    if v is None:
        return None
    return v / 1024 if key == "total-byte-weight" else v

def medians(label, ff):
    runs = [json.load(open(p)) for p in sorted(glob.glob(f"{HERE}/{label}/{ff}-*.json"))]
    runs = [r for r in runs if not r.get("runtimeError")]
    out = {}
    for name, key, *_ in METRICS:
        vals = [v for v in (value(r, key) for r in runs) if v is not None]
        out[name] = statistics.median(vals) if vals else None
    return out, len(runs)

def fmt(v, unit):
    if v is None: return "n/a"
    if unit == "ms": return f"{v/1000:.2f} s" if v >= 1000 else f"{v:.0f} ms"
    if unit == "KB": return f"{v:,.0f} KB"
    if unit == "score": return f"{v:.0f}"
    return f"{v:.3f}" if v < 1 else f"{v:,.0f}"

def main():
    before = sys.argv[1]; after = sys.argv[2] if len(sys.argv) > 2 else None
    for ff in ("mobile", "desktop"):
        b, nb = medians(before, ff)
        if after:
            a, na = medians(after, ff)
            print(f"\n### {ff.title()} (median of {nb} before / {na} after runs)\n")
            print("| Metric | Before | After | Change |\n|---|---|---|---|")
            for name, key, unit, lower in METRICS:
                bv, av = b[name], a[name]
                if bv is None or av is None: ch = "n/a"
                else:
                    d = av - bv
                    better = (d < 0) == lower if d else None
                    ch = ("+" if d > 0 else "") + fmt(abs(d), unit).replace("n/a", "0") if unit != "score" else f"{d:+.0f}"
                    if unit != "score" and d < 0: ch = "-" + fmt(abs(d), unit)
                    ch += "" if better is None else (" better" if better else " worse")
                print(f"| {name} | {fmt(bv, unit)} | {fmt(av, unit)} | {ch} |")
        else:
            print(f"\n### {ff.title()} (median of {nb} runs)\n")
            print("| Metric | Value |\n|---|---|")
            for name, key, unit, lower in METRICS:
                print(f"| {name} | {fmt(b[name], unit)} |")

if __name__ == "__main__":
    main()
