# Prepare the DSA porcelain photos from Drive for Shopify (26 Oct 2026): rename, convert BMP, cap at 20 MP.
import json, os
from PIL import Image
done = json.load(open('drive-done.json'))
# (drive id, new name, product key, alt)
PLAN = [
 ("13de4_iHNaHMcDWVPAX1ZdI_W1h_lkAo7","morgan-cloud-face-variations.jpg","cloud","Morgan Cloud porcelain tile, face variations"),
 ("1UCJHkccXR6swTIKX_EqDOMJAavgPUNeg","morgan-cloud-600x600-variations.png","cloud","Morgan Cloud 600 x 600 mm tiles laid out"),
 ("1PQCxngYWAJQsj5TGkgC_ORlLyiqIj1W_","morgan-cloud-room.jpg","cloud","Morgan Cloud porcelain tile in a bathroom"),
 ("1-uCp0UDN_4X9M8P2fdb_5hkPui8N3u4w","morgan-dusk-room.jpg","dusk","Morgan Dusk porcelain tile in a living room"),
 ("1G9hDLjkzrYyuXu-K8Kft4ks8b8YcWhUj","morgan-storm-face-variations.jpg","storm","Morgan Storm porcelain tile, face variations"),
 ("18m7M-gPW3dF6KUOAV6O-Nc5vOldT88lk","morgan-storm-room.png","storm","Morgan Storm porcelain tile on a loft floor"),
 ("1bZNeVuEVWuORc35nP68YAc7jzcnIhzax","morgan-hail-face-variations.jpg","hail","Morgan Hail porcelain tile, face variations"),
 ("19-9_ZJG8wPjMJGgE4OBGFgtRLuH2Cn0m","morgan-hail-face-variations-2.png","hail","Morgan Hail porcelain tiles laid out"),
 ("11at_D7NQmgVJ-h-b8LFy875_NYj2A3dA","morgan-hail-room.png","hail","Morgan Hail porcelain tile in a bathroom"),
 ("1EL8aKxn5seWkxdm3siV1D44Ib6L0hG0P","cement-dark-grey-tile.jpg","cdg","Cement Dark Grey porcelain tile, single tile"),
 ("1oa3l7GW-YznrlKN3N_C1Y3Yd_XTqXoGQ","cement-dark-grey-room.png","cdg","Cement Dark Grey porcelain tile in a living room"),
 ("1rOMEkTTkxp75W9XzfAMevUprYqtxHljz","cement-dark-grey-600x600-variations.png","cdg","Cement Dark Grey 600 x 600 mm tiles, face variations"),
 ("1UkW3YigDF4xyDPilgAl9ZGgTwO2vwaH-","cement-dark-grey-300x600-variations.png","cdg","Cement Dark Grey 300 x 600 mm tiles, face variations"),
 ("1f3-7l1vO9Wb9ZVJoN8r2ToYSy2QAAqDV","cement-white-tile.jpg","cw","Cement White porcelain tile, single tile"),
 ("1X7bZVvb5zvmqcFqvzrncuUIAwZqOZE4s","cement-white-room.jpg","cw","Cement White porcelain tile in a bedroom"),
 ("10j75JPX2gKklM1SYcBvPwdmG8-quvroB","cement-white-600x600-variations.png","cw","Cement White 600 x 600 mm tiles, face variations"),
 ("19iwYgj1-rbnx6SF19vZaKtLaoUWIlmvh","cement-white-300x600-variations.png","cw","Cement White 300 x 600 mm tiles, face variations"),
 ("1zyFaMLT8JkkZPAyq2s7y4-1AzG9jo2Cq","cement-range-white-grey-dark-grey.jpg","cw cg cdg","Cement White, Grey and Dark Grey porcelain tiles together"),
 ("1P5ENLQq8U9iUCkayiaCp9C1EHZUfZmir","cement-range-white-grey-dark-grey-2.jpg","cw cg cdg","Cement White, Grey and Dark Grey porcelain tiles stacked"),
 ("1_WxuWc53hbQOeZkrJFs4lIy3e8Pis393","cement-grey-tile.jpg","cg","Cement Grey porcelain tile, single tile"),
 ("1PsEhtZC4W5mqHzinSMl_rDTZypp5Wxg3","cement-grey-room.png","cg","Cement Grey porcelain tile in a kitchen"),
 ("1T8cVKPxrzP0ZO_bym_0wD0YalIBZbl-G","cement-grey-600x600-variations.png","cg","Cement Grey 600 x 600 mm tiles, face variations"),
 ("1U6TMv7GEz3KneTcTywlMARXm453eS-ND","cement-grey-300x600-variations.png","cg","Cement Grey 300 x 600 mm tiles, face variations"),
 ("1fvCdlLNriBa1GYTTeHFnr4Cf0x7wq3w9","cement-grey-tile-2.jpg","cg","Cement Grey porcelain tile close up"),
 ("1KFoyTZ1tGM9fSsYW6wRGK-4ldH_cTjix","particle-grey-tile.jpg","pg","Particle Grey porcelain tile, single tile"),
 ("1jFAjBelwNYsYG8aiURzd_upwGaqNAKn3","particle-grey-tile-2.jpg","pg","Particle Grey porcelain tile close up"),
 ("1CUNkZRvkDG0CaY0UeaWuDHx5nBHQBBXw","particle-grey-room.png","pg","Particle Grey porcelain tile around a pool"),
 ("1mH8_cyMniuKPGp7rl9xtfQeMfDdba5v1","particle-grey-face-variations.png","pg","Particle Grey 300 x 600 mm tiles, face variations"),
 ("1A1nj1cf0xdEUuAffqsqcbqsGBJC3o4Ls","particle-grey-room-2.jpg","pg","Particle Grey porcelain tile in a shower"),
 ("1Bf-CkYPtR1T-Gq4Ju--vhQmAT_JbgPcM","particle-warm-room.png","pw","Particle Warm porcelain tile on a lobby floor"),
 ("1uzGHrWEo8yO8-ERJqckBWVFoR335i6zI","particle-warm-face-variations.png","pw","Particle Warm 300 x 600 mm tiles, face variations"),
 ("1M8CfiX8cg_Pjw7w2iaUdKbHLoAMlFp37","terrazzo-white-room.png","tw","Terrazzo White porcelain tile in a bathroom"),
 ("1eL012ar2jncIsy3kAW9Wi9Iao-8QAFhB","terrazzo-white-600x600-variations.png","tw","Terrazzo White 600 x 600 mm tiles, face variations"),
 ("1YnnLov8ekbELEjVbtK8u2SN6VT8fRF-s","terrazzo-white-300x600-variations.png","tw","Terrazzo White 300 x 600 mm tiles, face variations"),
 ("1HQvPg65E-foU2PLBlrqX4f_gokxFu4h9","porcelain-showroom-1.jpg","files","Porcelain tile samples on the showroom display"),
 ("1WwacZbIeGtVds9jAkC_JLTO8pGso344t","porcelain-showroom-2.jpg","files","Porcelain tile samples on the showroom display"),
 ("1D9LWWmWfSCZjJgfrSqm5xtLYOMRep57x","porcelain-showroom-3.jpg","files","Porcelain tile samples on the showroom display"),
]
out=[]
for fid,name,key,alt in PLAN:
    im=Image.open(done[fid]); 
    if im.width*im.height > 19_500_000:
        s=(19_500_000/(im.width*im.height))**0.5; im=im.resize((int(im.width*s),int(im.height*s)), Image.LANCZOS)
    p='tilesup/prep/'+name
    if name.endswith('.jpg'): im.convert('RGB').save(p,quality=90)
    else: im.save(p,optimize=True)
    out.append({"name":name,"key":key,"alt":alt,"size":os.path.getsize(p),"mime":"image/jpeg" if name.endswith('.jpg') else "image/png","px":im.size})
json.dump(out,open('tilesup/plan.json','w'),indent=1)
print(json.dumps([{"filename":o["name"],"mimeType":o["mime"],"resource":"IMAGE","httpMethod":"POST","fileSize":str(o["size"])} for o in out],separators=(',',':')))
print(sum(o['size'] for o in out)/1e6,'MB',len(out))
