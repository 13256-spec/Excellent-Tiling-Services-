"""Parse downloaded ardexaustralia.com product pages -> ardex-products.json"""
import re, html, json, os, sys
from html.parser import HTMLParser

def clean(s):
    return html.unescape(re.sub(r'\s+', ' ', s)).strip()

def strip_tags(s):
    return clean(re.sub(r'<[^>]+>', ' ', s))

def tab(body, cls):
    m = re.search(r'<div class="product-details tab-' + cls + r'".*?<div class="tab-columns">(.*?)</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</li>', body, re.S)
    return m.group(1).strip() if m else ''

def kv(techhtml):
    """Technical Data tab. Two formats:
    A: <p><strong>Label:</strong></p><ul><li>..</li></ul> (+ <p>note</p>)
    B: <p><strong>LABEL</strong><br /> value<br /> • item<br /> • item</p>"""
    out = []
    parts = re.split(r'<p><strong>', techhtml)
    for p in parts[1:]:
        m = re.match(r'(.*?)</strong>\s*(.*)', p, re.S)
        if not m: continue
        label = strip_tags(m.group(1)).rstrip(':').strip()
        rest = m.group(2)
        items = [strip_tags(x) for x in re.findall(r'<li>(.*?)</li>', rest, re.S)]
        notes = [strip_tags(x) for x in re.findall(r'<p>(.*?)</p>', rest, re.S)]
        if not items:
            head, _, tail = rest.partition('</p>')
            lines = [strip_tags(x).lstrip('•').strip() for x in re.split(r'<br\s*/?>', head)]
            items = [l for l in lines if l]
            notes = [strip_tags(x) for x in re.findall(r'<p>(.*?)</p>', tail, re.S)]
        notes = [n for n in notes if n]
        out.append({'label': label.title() if label.isupper() else label, 'items': items, 'notes': notes})
    return out

def parse(path):
    s = open(path, encoding='utf-8', errors='ignore').read()
    slug = os.path.basename(path)[:-5]
    s = re.sub(r'<(script|style|svg|noscript)[^>]*>.*?</\1>', '', s, flags=re.S)
    m = re.search(r'<main.*?</main>', s, re.S)
    if not m: return {'slug': slug, 'error': 'no main'}
    body = m.group(0)
    d = {'slug': slug, 'url': f'https://ardexaustralia.com/product/{slug}/'}
    m = re.search(r'<h1 itemprop="name">(.*?)</h1>', body, re.S); d['name'] = strip_tags(m.group(1)) if m else ''
    m = re.search(r'<p class="product-description">(.*?)</p>', body, re.S); d['short'] = strip_tags(m.group(1)) if m else ''
    m = re.search(r'<div class="title-box text-right">\s*<a href="([^"]*)">(.*?)</a>', body, re.S)
    d['top_cat'] = strip_tags(m.group(2)) if m else ''; d['top_cat_url'] = m.group(1) if m else ''
    m = re.search(r'<ul class="list-unstyled">(.*?)</ul>', body, re.S)
    d['usps'] = [strip_tags(x) for x in re.findall(r'<li>(.*?)</li>', m.group(1), re.S)] if m else []
    imgs = []
    for u in re.findall(r'<img[^>]+src="(https://i0\.wp\.com/ardexaustralia\.com/wp-content/uploads/[^"?]+)', body):
        u = u.replace('https://i0.wp.com/', 'https://')
        if u not in imgs: imgs.append(u)
    d['images'] = imgs
    d['videos'] = sorted(set(re.findall(r'href="(https://www\.youtube\.com/watch\?v=[^"]+)"', body)))
    info = tab(body, 'information')
    d['info_html'] = info
    d['tech'] = kv(tab(body, 'technical data'))
    dl = tab(body, 'downloads')
    d['downloads'] = [(strip_tags(t), u) for u, t in re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', dl, re.S)]
    m = re.search(r'<p>\s*<a href="(https://ardexaustralia\.com/grout_colour/[^"]+)"', body); d['grout_colour_url'] = m.group(1) if m else ''
    return d

if __name__ == '__main__':
    out = []
    for f in sorted(os.listdir('pages')):
        if f.endswith('.html') and os.path.getsize('pages/' + f) > 0:
            out.append(parse('pages/' + f))
    json.dump(out, open('ardex-products.json', 'w'), indent=1)
    print(len(out), 'parsed;', sum(1 for o in out if not o.get('name')), 'without a name')
