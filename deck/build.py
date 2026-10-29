"""Build an animated deck from hand-drawn diagrams: one offline HTML file.

usage: python3 build.py path/to/deck.json [-o out.html]

deck.json lists the diagrams (HTML files made from templates/diagram.html) and the slides
(which diagram, which part of it). Every diagram is opened in Chromium; while its main() runs, each
rough.js stroke and each label is recorded together with the motion identity (id / parent / from / to)
passed to the helper that drew it. The result is inlined with player.html into a single file that
needs no network, no fonts beyond the system serif faces, and no server.

Requires: Python 3.8+, Playwright with Chromium (pip install playwright && playwright install chromium).
Building needs network access for rough.js (the diagrams load it from jsDelivr); the output does not.
"""
import argparse
import base64
import json
import os
import re
import sys

from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
MARK = 'main();\nwindow.__renderDone = true;'
MIME = {'.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.svg': 'image/svg+xml'}

# Injected into the diagram's own script, right before main(): wraps rough.js and the template helpers.
PRE = r"""
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const host = document.createElementNS(NS, 'svg');
  host.setAttribute('width', canvas.width); host.setAttribute('height', canvas.height);
  host.setAttribute('style', 'position:absolute;left:0;top:0;opacity:0;pointer-events:none');
  document.querySelector('.stage').appendChild(host);
  const rs = rough.svg(host);
  let seq = 0, gid = 0, grp = null, depth = 0;
  const idStack = [];                       // identity of the innermost helper call that declared one
  const ident = () => idStack.length ? idStack[idStack.length - 1] : null;
  const ops = window.__deckOps = [], arrows = window.__deckArrows = {};
  // The identity object is the last plain-object argument carrying id / parent / from / to.
  const KEYS = ['id', 'parent', 'from', 'to'];
  const findIdent = a => {
    for (let k = a.length - 1; k >= 0; k--) {
      const v = a[k];
      if (v && typeof v === 'object' && !Array.isArray(v) && KEYS.some(x => v[x] !== undefined))
        return Object.fromEntries(KEYS.filter(x => v[x] !== undefined).map(x => [x, String(v[x])]));
    }
    return null;
  };
  for (const m of ['line', 'rectangle', 'ellipse', 'circle', 'linearPath', 'polygon', 'arc', 'curve', 'path']) {
    const orig = rc[m].bind(rc);
    rc[m] = (...a) => { const r = orig(...a); const g = rs[m](...a); host.appendChild(g);
                        ops.push({ m, g, grp, seq: ++seq, idn: ident() }); return r; };
  }
  const tag = el => { el.dataset.seq = ++seq; el.dataset.grp = grp || ''; const i = ident(); if (i) el.dataset.idn = JSON.stringify(i); };
  const wrap = (name, multi) => {
    const f = window[name]; if (typeof f !== 'function') return;
    window[name] = function (...a) {
      const idn = findIdent(a), outer = multi && depth === 0;
      if (idn) idStack.push(idn);
      if (outer) grp = `${name}:${++gid}`;
      if (multi) depth++;
      if (name === 'arrow' && grp) arrows[grp] = a.slice(0, 4);
      try {
        const n = L.children.length, r = f.apply(this, a);
        for (const el of [...L.children].slice(n)) if (!el.dataset.seq) tag(el);
        return r;
      } finally { if (multi) depth--; if (outer) grp = null; if (idn) idStack.pop(); }
    };
  };
  // Multi-stroke helpers move as one shape; the others only pass identity down.
  for (const name of ['arrow', 'frame', 'timeline', 'taskCard', 'bubble', 'legend']) wrap(name, true);
  for (const name of ['box', 'channel', 'hexagon', 'node', 'lbl', 'plain']) wrap(name, false);
  // title() / subtitle() paint on the canvas; re-issue them as HTML so they become movable text.
  const textAt = (kind, text, x, y, size, weight, family, color, idn) => {
    ctx.font = `${weight} ${size}px ${family}`;
    const m = ctx.measureText(text), A = m.fontBoundingBoxAscent, D = m.fontBoundingBoxDescent;
    const div = document.createElement('div');
    div.className = 'label';
    div.style.cssText = `left:${x}px;top:${y - A}px;width:max-content;white-space:nowrap;` +
      `font-family:${family};font-size:${size}px;font-weight:${weight};line-height:${A + D}px;color:${color}`;
    div.textContent = text;
    if (idn) idStack.push(idn);
    L.appendChild(div); tag(div); div.dataset.grp = kind;
    if (idn) idStack.pop();
  };
  window.title = (text, x, y, size = 44, o = {}) => typeof size === 'object'
    ? window.title(text, x, y, 44, size) : textAt('title', text, x, y, size, 700, FONT_TI, C.title, findIdent([o]));
  window.subtitle = (text, x, y, size = 22, o = {}) => typeof size === 'object'
    ? window.subtitle(text, x, y, 22, size) : textAt('subtitle', text, x, y, size, 400, FONT_BD, C.subtitle, findIdent([o]));
})();
"""

POST = r"""
window.__deckExtract = async () => {
  await document.fonts.ready;
  const stage = document.querySelector('.stage'), sr = stage.getBoundingClientRect();
  const q = v => Math.round(v * 10) / 10;
  const R = r => [q(r.left - sr.left), q(r.top - sr.top), q(r.width), q(r.height)];
  const norm = s => s.replace(/\s+/g, ' ').trim();
  const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

  const groups = [], byKey = new Map();
  for (const op of window.__deckOps) {
    const k = op.grp || `op${op.seq}`;
    if (!byKey.has(k)) { const G = { gid: op.grp, seq: op.seq, ms: [], gs: [], idn: op.idn }; byKey.set(k, G); groups.push(G); }
    const G = byKey.get(k); G.ms.push(op.m); G.gs.push(op.g); if (!G.idn && op.idn) G.idn = op.idn;
  }
  const shapes = groups.map(G => {
    let x0 = Infinity, y0 = Infinity, x1 = -Infinity, y1 = -Infinity;
    for (const g of G.gs) {
      const b = g.getBBox();
      x0 = Math.min(x0, b.x); y0 = Math.min(y0, b.y); x1 = Math.max(x1, b.x + b.width); y1 = Math.max(y1, b.y + b.height);
    }
    const p = 5, st = G.gs[0].querySelector('path:not([stroke="none"])');
    return { seq: G.seq, gid: G.gid, ms: G.ms, stroke: st ? st.getAttribute('stroke') : null, idn: G.idn || null,
             ends: G.gid && window.__deckArrows[G.gid] || null,
             r: [q(x0 - p), q(y0 - p), q(x1 - x0 + 2 * p), q(y1 - y0 + 2 * p)],
             svg: G.gs.map(g => g.outerHTML).join('') };
  });

  const Lc = document.getElementById('labels'), texts = [];
  const isBlock = el => getComputedStyle(el).display === 'block';
  const hasInline = el => [...el.childNodes].some(n =>
    (n.nodeType === 3 && n.textContent.trim()) || (n.nodeType === 1 && !isBlock(n)));
  for (const root of Lc.children) {
    const seq = +root.dataset.seq || 0, gid = root.dataset.grp || null, idn = root.dataset.idn ? JSON.parse(root.dataset.idn) : null;
    const emit = leaf => {
      if (!norm(leaf.innerText)) return;
      const cs = getComputedStyle(leaf);
      let op = 1; for (let e = leaf; e && e !== Lc; e = e.parentElement) op *= +getComputedStyle(e).opacity;
      const base = `font-family:${cs.fontFamily};font-size:${cs.fontSize};font-weight:${cs.fontWeight};` +
        `font-style:${cs.fontStyle};line-height:${cs.lineHeight};color:${cs.color};text-align:${cs.textAlign};` +
        `letter-spacing:${cs.letterSpacing};white-space:${cs.whiteSpace}`;
      const br = leaf.getBoundingClientRect();
      const bg = cs.backgroundColor !== 'rgba(0, 0, 0, 0)';
      const segs = [[]];
      for (const n of leaf.childNodes) n.nodeName === 'BR' ? segs.push([]) : segs[segs.length - 1].push(n);
      const lines = segs.filter(s => s.some(n => n.textContent.trim()));
      if (lines.length <= 1 || bg) {
        const rg = document.createRange(); rg.selectNodeContents(leaf);
        texts.push({ seq, gid, idn, r: R(br), t: R(rg.getBoundingClientRect()), txt: norm(leaf.innerText), html: leaf.innerHTML,
                     css: base + `;background:${cs.backgroundColor};padding:${cs.padding}`, op, fs: parseFloat(cs.fontSize) });
        return;
      }
      // One movable atom per <br> line: same width and alignment as the parent, stacked line boxes.
      const pl = parseFloat(cs.paddingLeft), pr = parseFloat(cs.paddingRight), pt = parseFloat(cs.paddingTop), pb = parseFloat(cs.paddingBottom);
      const cx = br.left + pl, cw = br.width - pl - pr, ch = br.height - pt - pb, n = segs.length;
      segs.forEach((s, i) => {
        if (!s.some(nd => nd.textContent.trim())) return;
        const rg = document.createRange(); rg.setStartBefore(s[0]); rg.setEndAfter(s[s.length - 1]);
        texts.push({ seq, gid, idn, r: R({ left: cx, top: br.top + pt + ch * i / n, width: cw, height: ch / n }), t: R(rg.getBoundingClientRect()),
                     txt: norm(s.map(nd => nd.textContent).join('')),
                     html: s.map(nd => nd.nodeType === 3 ? esc(nd.textContent) : nd.outerHTML).join(''),
                     css: base, op, fs: parseFloat(cs.fontSize) });
      });
    };
    const walk = el => {
      const kids = [...el.children].filter(isBlock);
      if (kids.length && !hasInline(el)) kids.forEach(walk); else emit(el);
    };
    walk(root);
  }
  const images = [...Lc.querySelectorAll('img')].map(im => {
    let op = 1; for (let e = im; e && e !== Lc; e = e.parentElement) op *= +getComputedStyle(e).opacity;
    return { r: R(im.getBoundingClientRect()), src: im.getAttribute('src'), op };
  });
  return { w: canvas.width, h: canvas.height, shapes, texts, images };
};
"""

CLOSED = {'rectangle', 'polygon', 'ellipse', 'circle'}
GROUPED = {'taskCard', 'bubble', 'timeline'}
NUM = re.compile(r'(-?\d+\.\d)\d+')


def iou(a, b):
    x0, y0 = max(a[0], b[0]), max(a[1], b[1])
    x1, y1 = min(a[0] + a[2], b[0] + b[2]), min(a[1] + a[3], b[1] + b[3])
    inter = max(0, x1 - x0) * max(0, y1 - y0)
    return inter / (a[2] * a[3] + b[2] * b[3] - inter)


def inside(pt, r, pad=0):
    return r[0] - pad <= pt[0] <= r[0] + r[2] + pad and r[1] - pad <= pt[1] <= r[1] + r[3] + pad


def centre(r):
    return (r[0] + r[2] / 2, r[1] + r[3] / 2)


def structure(d, name):
    """Nodes = closed shape + the text drawn into it; frames keep their label; arrows learn their endpoints."""
    shapes, texts, warn = d['shapes'], d['texts'], []
    for s in shapes:
        s['svg'] = NUM.sub(r'\1', s['svg'])
        s['grp'] = s['gid'].split(':')[0] if s['gid'] else None
        idn = s.pop('idn') or {}
        s.update({k: idn[k] for k in ('id', 'parent', 'from', 'to') if k in idn})
    for t in texts:
        t['grp'] = t['gid'].split(':')[0] if t['gid'] else (t.get('grp') or None)
        idn = t.pop('idn') or {}
        t.update({k: idn[k] for k in ('id', 'parent') if k in idn})

    # nodes: single closed shapes (box / node / channel / hexagon) and the multi-stroke shapes that stand for one
    # thing (taskCard / bubble / timeline); a closed shape drawn right on top of the previous one is a stacked copy
    nodes, prev = [], None
    closed = [i for i, s in enumerate(shapes)
              if (not s['gid'] and len(s['ms']) == 1 and s['ms'][0] in CLOSED) or s['grp'] in GROUPED]
    for i in closed:
        s, p = shapes[i], (shapes[prev] if prev is not None else None)
        if p is not None and not s['gid'] and not p['gid'] and p['seq'] == s['seq'] - 1 and p['stroke'] == s['stroke'] \
                and iou(p['r'], s['r']) > 0.5 and p.get('id') == s.get('id'):
            nodes[p['node']]['shapes'].append(i)
        else:
            nodes.append({'shapes': [i], 'texts': []})
        s['node'] = len(nodes) - 1
        prev = i
    for n in nodes:
        outer = shapes[n['shapes'][-1]]
        n['id'] = next((shapes[k]['id'] for k in n['shapes'] if shapes[k].get('id')), None)
        n['parent'] = next((shapes[k]['parent'] for k in n['shapes'] if shapes[k].get('parent')), None)
        n['r'] = outer['r']
    by_id = {}
    for k, n in enumerate(nodes):
        if n['id']:
            by_id.setdefault(n['id'], k)
    # text → node: same declared id first, else the innermost closed shape drawn before it that contains it
    for j, t in enumerate(texts):
        if t['grp'] in ('legend', 'title', 'subtitle', 'frame'):
            continue
        if t.get('id') in by_id:
            k = by_id[t['id']]
        else:
            c = centre(t['t'])
            own = [i for i in closed if shapes[i]['seq'] < t['seq'] and inside(c, shapes[i]['r'])]
            if not own:
                continue
            k = shapes[max(own, key=lambda i: shapes[i]['seq'])]['node']
            if t.get('id') and nodes[k]['id']:
                continue                       # its own concept drawn inside another one (parent inferred below)
        t['node'] = k
        nodes[k]['texts'].append(j)
        if not nodes[k]['id'] and t.get('id') and not any(texts[x].get('id') for x in nodes[k]['texts'][:-1]):
            nodes[k]['id'] = t['id']           # lbl({ id }) inside a plain box names the box
    # frames: the label drawn by frame() (or a plain() label sitting on the top edge)
    labels = {}
    for j, t in enumerate(texts):
        if t['grp'] == 'frame':
            labels.setdefault(t['gid'], j)
    for s in shapes:
        if s['grp'] != 'frame':
            continue
        j = labels.get(s['gid'])
        if j is None:
            x, y, w, _ = s['r']
            on_edge = [k for k, t in enumerate(texts) if t['grp'] is None and 'node' not in t
                       and x <= centre(t['t'])[0] <= x + w and abs(centre(t['t'])[1] - (y + 5)) < 20]
            j = on_edge[0] if on_edge else None
        if j is not None:
            s['label'] = j
            if not s.get('id') and texts[j].get('id'):
                s['id'] = texts[j]['id']
    frame_labels = {s['label'] for s in shapes if s['grp'] == 'frame' and 'label' in s}
    free = [t for k, t in enumerate(texts) if t.get('id') and 'node' not in t and k not in frame_labels]
    frames = [s for s in shapes if s['grp'] == 'frame' and s.get('id')]
    # a concept drawn inside another one's box or frame belongs to it, unless it says otherwise
    holders = [(n['r'], n['id']) for n in nodes if n['id']] + [(s['r'], s['id']) for s in frames]
    for cid, cr, obj in ([(n['id'], n['r'], n) for n in nodes if n['id']] + [(s['id'], s['r'], s) for s in frames]
                         + [(t['id'], t['t'], t) for t in free]):
        if obj.get('parent'):
            continue
        c, area = centre(cr), cr[2] * cr[3]
        around = [h for h in holders if h[1] != cid and h[0][2] * h[0][3] > area * 1.2 and inside(c, h[0])]
        if around:
            obj['parent'] = min(around, key=lambda h: h[0][2] * h[0][3])[1]
    # arrows: endpoints → the concept they touch (smallest node, else frame, around the point)
    cands = [(n['r'], n['id']) for n in nodes if n['id']] + [(s['r'], s['id']) for s in shapes if s['grp'] == 'frame' and s.get('id')]
    for s in shapes:
        if s['grp'] != 'arrow' or not s.get('ends'):
            continue
        x1, y1, x2, y2 = s['ends']
        for key, pt in (('from', (x1, y1)), ('to', (x2, y2))):
            if s.get(key):
                continue
            hit = [c for c in cands if inside(pt, c[0], 26)]
            if hit:
                s[key] = min(hit, key=lambda c: c[0][2] * c[0][3])[1]
    # one concept, one drawing per diagram: repeated ids are allowed but warned (extra copies split off / merge in)
    seen = {}
    for k in [n['id'] for n in nodes if n['id']] + [s['id'] for s in frames] + [t['id'] for t in free]:
        seen[k] = seen.get(k, 0) + 1
    for k, c in seen.items():
        if c > 1:
            warn.append(f"{name}: id '{k}' is drawn {c} times; extra copies split off / merge into one partner")
    # an id on something that cannot move as a concept (legend, raw rough.js strokes) is ignored: say so
    for s in shapes:
        if s.get('id') and 'node' not in s and s['grp'] not in ('frame', 'arrow'):
            warn.append(f"{name}: id '{s['id']}' on a {s['grp'] or 'rough.js stroke'} is ignored; put it on a shape helper "
                        f"(node / box / channel / hexagon / taskCard / bubble / timeline / frame) or a label")
    for s in shapes:
        for k in ('ms', 'stroke', 'gid'):
            s.pop(k, None)
    for t in texts:
        t.pop('gid', None)
    d['nodes'] = nodes
    return d, warn


def extract(browser, src):
    html = open(src, encoding='utf-8').read()
    if html.count(MARK) != 1:
        sys.exit(f'{src}: expected exactly one "main();\\nwindow.__renderDone = true;" (copy templates/diagram.html)')
    html = html.replace(MARK, PRE + MARK + '\n' + POST)
    tmp = os.path.join(os.path.dirname(os.path.abspath(src)), '.deck_extract_' + os.path.basename(src))
    open(tmp, 'w', encoding='utf-8').write(html)   # next to the source, so relative image paths still resolve
    try:
        m = re.search(r'<canvas id="c" width="(\d+)" height="(\d+)"', html)
        page = browser.new_page(viewport={'width': int(m.group(1)), 'height': int(m.group(2))})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto('file://' + tmp)
        try:
            page.wait_for_function('window.__renderDone === true && window.__deckExtract', timeout=60000)
        except Exception:
            sys.exit(f'{src}: diagram did not finish rendering. Page errors: {errors or "none (is rough.js reachable?)"}')
        d = page.evaluate('window.__deckExtract()')
        page.close()
    finally:
        os.remove(tmp)
    for im in d['images']:
        f = os.path.join(os.path.dirname(os.path.abspath(src)), im['src'])
        im['src'] = f"data:{MIME[os.path.splitext(f)[1].lower()]};base64," + base64.b64encode(open(f, 'rb').read()).decode()
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('deck', help='deck.json')
    ap.add_argument('-o', '--out', help='output HTML (default: deck.html next to deck.json)')
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.deck))
    spec = json.load(open(a.deck, encoding='utf-8'))
    diagrams = spec.get('diagrams') or {}
    slides = spec.get('slides') or []
    if not diagrams or not slides:
        sys.exit('deck.json needs "diagrams" {name: file.html} and "slides" [{"diagram": name, ...}]')
    for i, sl in enumerate(slides):
        if sl.get('diagram') not in diagrams:
            sys.exit(f'slide {i + 1}: unknown diagram {sl.get("diagram")!r}')
    data, warns, known = {}, [], {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for key, rel in diagrams.items():
            d, w = structure(extract(browser, os.path.join(base, rel)), key)
            data[key] = d
            warns += w
            ids = sorted({n['id'] for n in d['nodes'] if n['id']} | {s['id'] for s in d['shapes'] if s.get('id')}
                         | {t['id'] for t in d['texts'] if t.get('id')})
            known[key] = {n['id'] for n in d['nodes'] if n['id']} | {t['id'] for t in d['texts'] if t.get('id') and 'node' not in t} \
                | {s['id'] for s in d['shapes'] if s['grp'] == 'frame' and s.get('id')}
            arrows = [s for s in d['shapes'] if s['grp'] == 'arrow']
            linked = sum(1 for s in arrows if s.get('from') and s.get('to'))
            print(f'{key}: {d["w"]}x{d["h"]}  shapes={len(d["shapes"])} texts={len(d["texts"])} nodes={len(d["nodes"])} '
                  f'ids={len(ids)} arrows={len(arrows)} (linked {linked})')
        browser.close()
    for w in warns:
        print('warning:', w)
    for i, sl in enumerate(slides):          # a mistyped focus id would silently show the whole diagram
        f = sl.get('focus')
        f = [f] if isinstance(f, str) else f
        if isinstance(f, list) and f and isinstance(f[0], str):
            miss = [x for x in f if x not in known[sl['diagram']]]
            if miss:
                sys.exit(f'slide {i + 1}: focus id(s) {miss} not found in diagram "{sl["diagram"]}" '
                         f'(it has: {", ".join(sorted(known[sl["diagram"]])) or "no ids"})')
    payload = {'spec': {k: v for k, v in spec.items() if k != 'diagrams'}, 'data': data}
    js = 'window.DECK = ' + json.dumps(payload, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + ';'
    player = open(os.path.join(HERE, 'player.html'), encoding='utf-8').read()
    tag = '<script id="deck-data"></script>'
    assert player.count(tag) == 1
    title = spec.get('title') or 'Deck'
    esc = title.replace('&', '&amp;').replace('<', '&lt;')
    out = a.out or os.path.join(base, 'deck.html')
    html = player.replace(tag, '<script>' + js + '</script>').replace('<title>Deck</title>', f'<title>{esc}</title>')
    open(out, 'w', encoding='utf-8').write(html)
    print(f'wrote {out} ({os.path.getsize(out) // 1024} KB, {len(slides)} slides)')


if __name__ == '__main__':
    main()
