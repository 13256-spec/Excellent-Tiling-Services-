"""What people type into Google (Australia) for each product group: Google autocomplete, most popular first.
No volumes (no paid keyword tool connected), but the order and wording are Google's own.
Usage: keyword_suggestions.py > keyword-suggestions-2026-11.json"""
import json, sys, time, urllib.parse, urllib.request
SEEDS = {
 "Floor Drains": ["floor drain", "floor waste", "shower drain", "shower grate", "tile insert", "linear drain", "drain grate", "bathroom floor waste", "puddle flange", "shower waste"],
 "Tile trims": ["tile trim", "tile edge", "tile edging", "aluminium tile trim", "aluminium angle tile", "square edge tile trim", "round edge tile trim", "stair nosing", "tile expansion joint", "cove tile trim", "balcony edge trim", "brass tile trim", "stainless steel tile trim", "black tile trim", "waterstop angle", "shower water stop", "tile ramp trim", "tile transition strip"],
 "Spacers & levelling": ["tile spacers", "tile wedges", "tile levelling", "tile leveling system", "tile levelling clips"],
 "Cutting & drilling": ["tile cutter", "manual tile cutter", "sigma tile cutter", "raimondi tile cutter", "wet tile saw", "tile nippers", "diamond blade tile", "tile drill bit", "diamond core drill", "tile hole saw"],
 "Trowels, grouting, clean up": ["notched trowel", "tiling trowel", "grout float", "grout sponge", "tile sponge", "washboy", "grout", "epoxy grout", "grout cleaner", "grout sealer", "tile sealer", "tile cleaner", "grout haze remover", "grout remover tool"],
 "Adhesives, waterproofing, levellers": ["tile adhesive", "tile glue", "ardex tile adhesive", "ardex", "rla tile adhesive", "waterproofing membrane", "shower waterproofing", "bathroom waterproofing", "waterproofing kit", "ardex waterproofing", "gripset", "waterproofing tape", "bond breaker", "tile primer", "self levelling compound", "floor leveller", "screed", "concrete repair"],
 "Silicone": ["silicone sealant", "bathroom silicone", "coloured silicone", "maxisil", "pool silicone", "caulking gun", "sausage gun", "silicone tool", "backer rod"],
 "Tools": ["tiling tools", "tilers tools", "knee pads tiling", "tile suction cup", "suction lifter", "mixing paddle", "mixing drill", "tile mixer", "spiked roller", "screed bar", "rubber mallet tile", "floor scraper", "raimondi", "large format tile tools"],
 "Bathroom bits": ["shower niche", "niche box", "ceramic soap holder", "tile vent", "tile backer board", "wedi board", "uncoupling membrane"],
 "Tiles & store": ["porcelain tiles", "floor tiles", "bathroom tiles", "tiles perth", "tile shop perth", "tiling supplies", "tiling supplies perth", "tile trim perth", "tile tools perth"],
}
out = {}
for group, seeds in SEEDS.items():
    out[group] = {}
    for s in seeds:
        u = "https://suggestqueries.google.com/complete/search?client=firefox&gl=au&hl=en&q=" + urllib.parse.quote(s)
        out[group][s] = json.loads(urllib.request.urlopen(u, timeout=20).read().decode("latin-1"))[1]
        time.sleep(0.3)
json.dump(out, sys.stdout, indent=1)
