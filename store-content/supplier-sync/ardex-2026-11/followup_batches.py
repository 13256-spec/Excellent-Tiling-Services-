"""After collect_results.py: write the follow-up mutation files (unpublish from POS/Shop/Copilot, delivery profiles)."""
import json, os
S = '/tmp/claude-0/-home-user-Excellent-Tiling-Services-/6ea702dc-bcae-5876-b8d1-0ec2c29c9023/scratchpad/ardex/'
ids = json.load(open(S + 'publish-ids.json'))
prof = json.load(open(S + 'profile-variants.json'))
UNPUB = ["gid://shopify/Publication/157692002367", "gid://shopify/Publication/157692035135", "gid://shopify/Publication/159206998079"]
os.makedirs(S + 'followup', exist_ok=True)
n = 0
for i in range(0, len(ids), 25):
    chunk = ids[i:i + 25]
    q = "mutation(" + ", ".join(f"$i{j}: ID!" for j in range(len(chunk))) + ", $pubs: [PublicationInput!]!) { " + " ".join(
        f"u{j}: publishableUnpublish(id: $i{j}, input: $pubs) {{ userErrors {{ field message }} }}" for j in range(len(chunk))) + " }"
    v = {f"i{j}": pid for j, pid in enumerate(chunk)}
    v["pubs"] = [{"publicationId": p} for p in UNPUB]
    json.dump({"query": q, "variables": v}, open(S + f'followup/unpub-{n:02d}.json', 'w')); n += 1
for key, pid in (("local", "gid://shopify/DeliveryProfile/94703747135"), ("dg", "gid://shopify/DeliveryProfile/94703714367")):
    vs = prof[key]
    for i in range(0, len(vs), 100):
        json.dump({"query": "mutation($id: ID!, $profile: DeliveryProfileInput!) { deliveryProfileUpdate(id: $id, profile: $profile) { profile { id } userErrors { field message } } }",
                   "variables": {"id": pid, "profile": {"variantsToAssociate": vs[i:i + 100]}}},
                  open(S + f'followup/profile-{key}-{i // 100}.json', 'w'))
print('unpublish batches', n, 'local variants', len(prof['local']), 'dg', len(prof['dg']))
