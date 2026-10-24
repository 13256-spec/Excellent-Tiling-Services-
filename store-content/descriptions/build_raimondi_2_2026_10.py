#!/usr/bin/env python3
"""Build raimondi-2-2026-10-24.json from the two data modules and check the hard rules.

Usage: python3 build_raimondi_2_2026_10.py            # write JSON + report
       python3 build_raimondi_2_2026_10.py batches    # also write mutation variable files
"""
import json, re, sys, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from raimondi2_data_a import A
from raimondi2_data_b import B

OUT = os.path.join(HERE, "raimondi-2-2026-10-24.json")
TODO = os.path.join(HERE, "todo-raimondi-2.json")

BANNED = [r"\$", r"\btrade\b", r"\bstock\b", r"showroom", r"Maddington", r"\bdeliver", r"pick up",
          r"shipping", r"Eternity", r"\bDSA\b", r"Bathroom City", r"elevate", r"stunning", r"seamless",
          r"!", r"—", r"curated", r"timeless", r"discover", r"unlock", r"premium quality",
          r"look no further", r"perfect for any", r"\bMOQ\b", r"supplier", r"cheaper than", r"best price"]

def words(h):
    return len(re.findall(r"\b\w+\b", html.unescape(re.sub(r"<[^>]+>", " ", h))))

def main():
    recs = A + B
    todo = {r["id"]: r for r in json.load(open(TODO))}
    ids = [r["id"] for r in recs]
    assert len(ids) == len(set(ids)), "duplicate ids"
    missing = [t for t in todo if t not in ids]
    extra = [i for i in ids if i not in todo]
    assert not missing and not extra, (missing, extra)
    problems = []
    for r in recs:
        r["words"] = words(r["new"])
        if not 90 <= r["words"] <= 200:
            problems.append((r["handle"], "words", r["words"]))
        for pat in BANNED:
            if re.search(pat, r["new"], re.I):
                problems.append((r["handle"], "banned", pat))
        if "style=" in r["new"] or "<img" in r["new"] or "<script" in r["new"]:
            problems.append((r["handle"], "html", "style/img/script"))
        # keep codes from old: every RAI- or Art number in old should still... codes are internal, skipped by design
    json.dump(recs, open(OUT, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {OUT}: {len(recs)} records, verified={sum(r['verified'] for r in recs)}")
    for p in problems:
        print("PROBLEM", p)
    if len(sys.argv) > 1 and sys.argv[1] == "batches":
        bdir = os.path.join(os.environ.get("RAI2_BATCH_DIR", HERE), "rai2_batches")
        os.makedirs(bdir, exist_ok=True)
        for i in range(0, len(recs), 8):
            chunk = recs[i:i+8]
            q = "mutation(" + ", ".join(f"$p{j}: ProductUpdateInput!" for j in range(len(chunk))) + ") {\n"
            for j in range(len(chunk)):
                q += f"  u{j}: productUpdate(product: $p{j}) {{ product {{ id handle }} userErrors {{ field message }} }}\n"
            q += "}"
            vars_ = {f"p{j}": {"id": r["id"], "descriptionHtml": r["new"]} for j, r in enumerate(chunk)}
            json.dump({"query": q, "variables": vars_}, open(os.path.join(bdir, f"b{i//8}.json"), "w"), ensure_ascii=False)
        print("batches in", bdir)
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main())
