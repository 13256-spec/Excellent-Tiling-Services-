# Build productUpdate inputs for the DSA porcelain series from the Drive test reports (26 Oct 2026).
# Slipstop Perth wet pendulum (AS 4586, 04/03/2025): Morgan AK P3 (SRV 36), Cement MQ P3 (SRV 35), Particle SS P5 (SRV 55).
# Factory test reports (300x600 / 600x600 / 1200x600, 9.5 mm): water absorption 0.06%, breaking strength 2132 N, stain class 5, frost pass.
import json, re, sys
src = json.load(open(sys.argv[1]))
LAB = '<li>Water absorption: 0.06% (tested)</li>\n<li>Breaking strength: 2,132 N (tested)</li>\n<li>Stain resistance: class 5</li>\n<li>Frost resistant</li>'
P = {
 # key: (id, slip, tags_without_slip, lab_report?)
 "dusk": ("8395797364799","P3",["300x300","300x600","600x600","ebay-pickup-only","Matt","Morgan","Porcelain","ship-local-only","Tile"],True),
 "storm":("8395797495871","P3",["300x600","600x600","ebay-pickup-only","Matt","Morgan","Porcelain","ship-local-only","Tile"],True),
 "cloud":("8395797659711","P3",["300x300","300x600","600x600","ebay-pickup-only","Matt","Morgan","Porcelain","ship-local-only","Tile"],True),
 "hail": ("8395797790783","P3",["300x600","600x1200","600x600","ebay-pickup-only","Matt","Morgan","Porcelain","ship-local-only","Tile"],True),
 "cdg":  ("8395797954623","P3",["300x600","600x600","Cement","ebay-pickup-only","Matt","Porcelain","ship-local-only","Tile"],True),
 "cw":   ("8395798118463","P3",["300x600","600x1200","600x600","Cement","ebay-pickup-only","Matt","Porcelain","ship-local-only","Tile"],True),
 "cg":   ("8395798249535","P3",["300x600","600x1200","600x600","Cement","ebay-pickup-only","Matt","Porcelain","ship-local-only","Tile"],True),
 "pg":   ("8395797004351","P5",["300x600","Anti-Slip","ebay-pickup-only","Matt","Particle","Porcelain","ship-local-only","Tile"],False),
 "pw":   ("8395797200959","P5",["300x600","Anti-Slip","ebay-pickup-only","Matt","Particle","Porcelain","ship-local-only","Tile"],False),
 "tw":   ("8395796873279","P3",["300x600","600x600","ebay-pickup-only","Matt","Porcelain","ship-local-only","Terrazzo","Tile"],True),
}
P5_NOTE = "P5 slip rating, the highest wet pendulum class: suits bathroom and laundry floors, alfresco and verandah floors, pool surrounds and ramps."
out = {}
for k,(pid,slip,tags,lab) in P.items():
    html = src[k]["descriptionHtml"]; seo = src[k]["seo"]["description"]
    if slip == "P5":
        html = re.sub(r"<li>P4 slip rating:[^<]*</li>", "<li>"+P5_NOTE+"</li>", html)
        html = html.replace("P4 slip rating", "P5 slip rating").replace("Slip rating: P4", "Slip rating: P5")
        seo = seo.replace("P Rating: 4", "Slip rating: P5")
        if "P5" not in seo: seo = seo.rstrip(". ") + ". Slip rating: P5 (wet pendulum)."
        assert "P4" not in html
    # tested slip line
    html = html.replace(f"<li>Slip rating: {slip}</li>", f"<li>Slip rating: {slip} (wet pendulum test to AS 4586)</li>") if slip!="P3" or k!="tw" else html
    if lab and "Water absorption" not in html:
        m = re.search(r"<li>Thickness: 9\.5 mm[^<]*</li>", html) or re.search(r"<li>Slip rating: P3[^<]*</li>", html)
        assert m, k
        html = html[:m.end()] + "\n" + LAB + html[m.end():]
    assert f"Slip rating: {slip}" in html, k
    out[k] = {"id": f"gid://shopify/Product/{pid}", "descriptionHtml": html, "tags": sorted(tags+[slip]), "seo": {"description": seo[:320]}}
json.dump(out, open("tile-updates-2026-10-26.json","w"), indent=1)
q = "mutation(" + ", ".join(f"${k}: ProductUpdateInput!" for k in out) + ") {\n" + "\n".join(f'  {k}: productUpdate(product: ${k}) {{ product {{ id }} userErrors {{ field message }} }}' for k in out) + "\n}"
open("mutation.graphql","w").write(q)
print(q); print("====="); print(json.dumps(out, separators=(",",":")))
