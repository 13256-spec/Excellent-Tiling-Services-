#!/usr/bin/env python3
"""Self-check for import_supplier.py: builds a deliberately messy manufacturer workbook and asserts the pipeline's
behaviour (header detection, Chinese/English column aliasing, merged-cell finishes, unit conversion, SKU scheme,
pricing maths, WaterMark/WELS gate, shipping and eBay tags, supplier-name scrubbing). Run: python3 scripts/test_import_supplier.py"""
import json, pathlib, sys, tempfile
import openpyxl

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import import_supplier as imp

cfg = json.loads((imp.ROOT / "scripts/import_config.json").read_text())
cfg["brand"]["name"], cfg["supplier"]["name"], cfg["supplier"]["aliases"] = "Aria Tapware", "Kaiping Sanitary Ware Co., Ltd", ["Kaiping Sanitary", "KPSW"]

wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Price List"
ws.append(["Kaiping Sanitary Ware Co., Ltd  2026 FOB Price List"]); ws.merge_cells("A1:S1")
ws.append([])
ws.append(["型号 Model No.", "品名 Product Name", "类别", "系列 Series", "表面 Finish", "FOB价 (USD)", "材质", "阀芯 Cartridge",
           "工作压力 Max Pressure", "流量 Flow", "WELS Rating", "WELS Reg No.", "WaterMark Licence", "Certifier",
           "出水口长度 Projection", "重量 N.W.", "尺寸 Size", "Warranty", "Images"])
ws.append(["zk 1001", "KPSW Aria Basin Mixer", "Basin Mixer", "Aria", "CP/MB", 23.5, "Brass", "Sedal 35mm", "0.05-0.8MPa", "6L/min", "5", "T12345", "WMKA26123", "SAI Global", "120mm", "1.6kg", "45x180x150mm", "5 years", "https://cdn.example/zk1001-cp.jpg https://cdn.example/zk1001-mb.jpg https://cdn.example/zk1001-bn.jpg"])
ws.append([None, None, None, None, "拉丝镍", 26, None, None, None, None, None, None, None, None, None, None, None, None, None])  # merged row: nickel dearer
ws.append(["ZK-2001", "Aria Wall Mixer", "", "Aria", "CP/MB/BN", 18, "Brass", "Kerox 35 mm", "500kPa", "9 lpm", "", "", "WMKA26124", "SAI Global", "", "1200g", "", "", ""])
ws.append(["ZK-3001", "Aria Bath Spout", "Bath Spout", "Aria", "Gunmetal", 15, "Brass", "", "72 psi", "", "4 star", "T12346", "WMKA26125", "SAI Global", "6 in", "", "", "5", ""])
ws.append(["ZK-4001", "Aria Shower Set", "Shower Set", "Aria", "", 60, "Brass", "", "0.5", "", "3", "T12347", "WMKA26126", "SAI Global", "", "4.5 kg", "1200x250x400mm", "", ""])
tmp = pathlib.Path(tempfile.mkdtemp()); path = tmp / "messy.xlsx"; wb.save(path)

products, skipped, report, _ = imp.run(str(path), cfg, out=tmp / "out", publish=True)
by = {p["key"]: p for p in products}

# header + column detection
assert set(by) == {"ZK-1001", "ZK-2001", "ZK-3001"}, by.keys()
assert skipped == [("ZK-4001", "no recognisable finish on the sheet; add the finish or its alias to import_config.json")], skipped

# finishes from codes, Chinese and merged rows; SKU scheme; finish-specific FOB
p1 = by["ZK-1001"]
assert [v["sku"] for v in p1["input"]["variants"]] == ["ZK-1001-CP", "ZK-1001-MB", "ZK-1001-BN"]
assert [v["optionValues"][0]["name"] for v in p1["input"]["variants"]] == ["Chrome", "Matt Black", "Brushed Nickel"]
pr = {x["finish"]: x for x in p1["pricing"]}
assert pr["Brushed Nickel"]["fob"] == 26 and pr["Chrome"]["fob"] == 23.5 and pr["Brushed Nickel"]["price"] > pr["Chrome"]["price"]

# units
mf = {m["key"]: m["value"] for m in p1["input"]["metafields"]}
assert mf["max_pressure_kpa"] == "800" and mf["flow_rate"] == "6 L/min" and mf["spout_projection_mm"] == "120"
assert mf["cartridge_brand"] == "Sedal" and mf["cartridge_size_mm"] == "35" and mf["wels_rating"] == "5 Star"
assert mf["width_mm"] == "45" and mf["depth_mm"] == "180" and mf["height_mm"] == "150" and mf["warranty_years"] == "5"
assert json.loads(mf["finish"]) == ["Chrome", "Matt Black", "Brushed Nickel"] and mf["range"] == "Aria" and mf["supplier"] == "Kaiping Sanitary Ware Co., Ltd"
assert {m["key"]: m["value"] for m in by["ZK-2001"]["input"]["metafields"]}["max_pressure_kpa"] == "500"
assert {m["key"]: m["value"] for m in by["ZK-3001"]["input"]["metafields"]}["max_pressure_kpa"] == "496"
assert {m["key"]: m["value"] for m in by["ZK-3001"]["input"]["metafields"]}["spout_projection_mm"] == "152"
assert p1["weight_kg"] == 1.6 and by["ZK-2001"]["weight_kg"] == 1.2 and by["ZK-3001"]["weight_kg"] == 0.9  # 0.9 = type default

# pricing: fob 23.5 USD x 1.55 = 36.425; landed = x (1 + .05 + .12 + .02) = 43.3458; cost inc GST 47.68; price 43.3458 x 2.2 x 1.1 = 104.90 -> 104.95
c = pr["Chrome"]
assert c["cost_inc_gst"] == 47.68 and c["price"] == 104.95 and c["floor"] == 59.6 and c["trade_band"] == 25 and c["trade_price"] == 78.71, c
assert imp.round_price(104.95, "x.95") == 104.95 and imp.round_price(104.96, "x.95") == 105.95 and imp.round_price(59.6, "x.95") == 59.95
v = p1["input"]["variants"][0]
assert v["inventoryPolicy"] == "CONTINUE" and v["inventoryItem"]["tracked"] is True and v["inventoryItem"]["cost"] == 47.68
assert v["file"]["originalSource"].endswith("zk1001-cp.jpg") and p1["input"]["variants"][1]["file"]["originalSource"].endswith("-mb.jpg")
assert "files" not in p1["input"]  # every image matched a finish, nothing left over

# compliance gate
assert p1["gate_missing"] == [] and p1["input"]["status"] == "ACTIVE"
assert by["ZK-2001"]["gate_missing"] == ["wels_registration", "wels_rating"] and by["ZK-2001"]["input"]["status"] == "DRAFT"
assert "needs-compliance" in by["ZK-2001"]["input"]["tags"] and "needs-compliance" not in p1["input"]["tags"]

# tags: shipping + ebay + suite + type
t1 = set(p1["input"]["tags"])
assert {"ship-parcel", "ebay-post-20", "suite-aria", "Basin Mixer", "house-brand", "WELS 5 Star"} <= t1, t1
assert "ebay-post-15" in by["ZK-3001"]["input"]["tags"]
assert imp.ship_tags(4.5, 1200, cfg) == ["ship-local-only", "ebay-pickup-only"] and imp.ship_tags(8, 400, cfg) == ["ship-parcel", "ship-bulky", "ebay-post-39"]

# wall mixer type came from the name, not the empty type column; title never carries the supplier name
assert by["ZK-2001"]["type"] == "Wall Mixer" and p1["input"]["title"] == "Aria Tapware Aria Basin Mixer"
for p in products:
    blob = " ".join([p["input"]["title"], p["input"]["descriptionHtml"], p["input"]["seo"]["title"], p["input"]["seo"]["description"], *p["input"]["tags"]])
    assert not imp.contains_supplier(blob, ["Kaiping", "KPSW"]), blob
    assert len(p["input"]["seo"]["title"]) <= 60 and len(p["input"]["seo"]["description"]) <= 155
assert p1["input"]["handle"] == "aria-tapware-aria-basin-mixer"

# outputs exist and the report names the blocked product
assert (tmp / "out/payload.json").exists() and (tmp / "out/import.csv").exists()
rep = report.read_text()
assert "Blocked by the WaterMark / WELS gate" in rep and "ZK-2001" in rep and "trade-list-25" in rep and "aria-tapware-aria" in rep
print("ok: 3 products, 7 variants, 1 blocked, 1 skipped; report at", report)
