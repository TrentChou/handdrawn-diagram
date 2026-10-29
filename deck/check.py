"""Check a built deck: does every shared concept morph, does text collide in flight, is everything readable?

usage: python3 check.py deck.html [--strips DIR] [--min-px 12]

Prints one block per slide and per transition, then a summary. With --strips it also saves, for every
transition between two different diagrams, a contact sheet of frames at fixed progress points
(strip_<i>_<j>.png) to look at: the numbers find suspects, the pictures decide.

Findings
  LOST       a concept id drawn on both diagrams did not move into its new form (it faded out and in)
  REAPPEARS  the same words fade out on one side and fade in on the other: give both the same id
  COLLIDES   two different text lines overlap mid-flight by more than half a line height (worst moment
             and how many of the sampled frames it lasts); fix the layout first, a "timing" entry in
             deck.json only as a last resort
  SMALL      lines on a resting slide smaller than --min-px on screen (the deck's stage, 1920x1080 by default)
  ERROR      the page threw a JavaScript error
"""
import argparse
import os
import sys

from playwright.sync_api import sync_playwright

PS = [i / 20 for i in range(1, 20)]
STRIP = [0, .2, .35, .5, .65, .8, 1]


def overlap(a, b):
    w = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
    h = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
    return (w, h) if w > 2 and h > 2 else None


def collisions(page, i, j, calm):
    """Worst overlap between two different text lines while transition i → j runs.

    Skipped: the two copies of one morphing line, pairs that already overlap on a resting slide (`calm`),
    and grazes smaller than half the shorter line's height in either direction (edges touching, not
    glyphs on glyphs). Returns (area, p, text_a, text_b, (w, h), sampled frames the pair collided in)."""
    page.evaluate(f'__deck.freeze({i}, {j}, 0)')
    worst, frames = None, {}
    for p in PS:
        page.evaluate(f'__deck.freeze({i}, {j}, {p})')
        bs = page.evaluate('__deck.textBoxes()')
        for x in range(len(bs)):
            for y in range(x + 1, len(bs)):
                a, b = bs[x], bs[y]
                if a['pair'] is not None and a['pair'] == b['pair']:
                    continue
                if (a['txt'], b['txt']) in calm or (b['txt'], a['txt']) in calm:
                    continue
                o = overlap(a['r'], b['r'])
                if not o or min(a['op'], b['op']) <= .45 or min(o) < .5 * min(a['r'][3], b['r'][3]):
                    continue
                key = tuple(sorted((a['txt'], b['txt'])))
                frames[key] = frames.get(key, 0) + 1
                area = o[0] * o[1]
                if not worst or area > worst[0]:
                    worst = (area, p, a['txt'], b['txt'], o)
    page.evaluate(f'__deck.freeze({i}, {j}, 1)')
    return worst and worst + (frames[tuple(sorted(worst[2:4]))],)


def resting_overlaps(page, i):
    page.evaluate(f'__deck.setState({i})')
    bs = page.evaluate('__deck.textBoxes()')
    return {(a['txt'], b['txt']) for x, a in enumerate(bs) for b in bs[x + 1:] if overlap(a['r'], b['r'])}


def strip(page, i, j, path):
    try:
        from PIL import Image
    except ImportError:
        Image = None
    shots = []
    for p in STRIP:
        if p == 0:
            page.evaluate(f'__deck.setState({i})')
        else:
            page.evaluate(f'__deck.freeze({i}, {j}, {p})')
        shots.append(page.screenshot(type='png'))
    page.evaluate(f'__deck.setState({j})')
    if Image is None:                       # no Pillow: keep the frames as separate files
        for p, b in zip(STRIP, shots):
            open(path.replace('.png', f'_p{int(p * 100):03d}.png'), 'wb').write(b)
        return
    import io
    ims = [Image.open(io.BytesIO(b)).convert('RGB') for b in shots]
    w, h = ims[0].width // 2, ims[0].height // 2
    cols = 2
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (w * cols, h * rows), 'white')
    for k, im in enumerate(ims):
        sheet.paste(im.resize((w, h)), ((k % cols) * w, (k // cols) * h))
    sheet.save(path)


def main():
    ap = argparse.ArgumentParser(description='Check a built deck.')
    ap.add_argument('deck')
    ap.add_argument('--strips', help='directory for transition contact sheets')
    ap.add_argument('--min-px', type=float, default=12)
    a = ap.parse_args()
    if a.strips:
        os.makedirs(a.strips, exist_ok=True)
    issues = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto('file://' + os.path.abspath(a.deck))
        page.wait_for_function('window.__ready === true', timeout=60000)
        w, h = page.evaluate('[__deck.W, __deck.H]')
        page.set_viewport_size({'width': w, 'height': h})      # one stage pixel = one screen pixel
        page.evaluate(f'window.DECK.spec.minFontPx = {a.min_px}')
        slides = page.evaluate('__deck.SLIDES.map(s => ({ d: s.d, focus: !!s.focus, note: s.note }))')
        n = len(slides)
        print(f'{n} slides')
        for i, sl in enumerate(slides):
            st = page.evaluate(f'__deck.stats({i})')
            where = f'{sl["d"]}{" (focus)" if sl["focus"] else ""}'
            print(f'\nslide {i + 1:2d}  {where:22s} lines={st["lines"]:3d} to read={st["newLines"]:3d} '
                  f'min={st["minPx"]}px  {sl["note"]}')
            if st['small']:
                issues.append(f'SMALL      slide {i + 1}: {len(st["small"])} line(s) under {a.min_px:g}px, e.g. {st["small"][0]}')
                print(f'  SMALL     {len(st["small"])} line(s) under {a.min_px:g}px, e.g. {st["small"][:3]}')
            if i + 1 == n:
                continue
            r = page.evaluate(f'__deck.inspect({i}, {i + 1})')
            if r['camera']:
                print(f'  → {i + 2}: camera move')
                continue
            print(f'  → {i + 2}: morph  shared ids={len(r["sharedIds"])} ({", ".join(r["sharedIds"]) or "none"})  '
                  f'paired lines={r["pairedTexts"]} arrows morphed={r["morphedArrows"]} '
                  f'lines out={r["goneTexts"]} in={r["newTexts"]}')
            for id_ in r['lostIds']:
                issues.append(f'LOST       {i + 1}→{i + 2}: id "{id_}" is on both diagrams but did not morph')
                print(f'  LOST      "{id_}"')
            for t in r['reappearingText']:
                issues.append(f'REAPPEARS  {i + 1}→{i + 2}: "{t}" fades out and back in')
                print(f'  REAPPEARS "{t}"')
            calm = resting_overlaps(page, i) | resting_overlaps(page, i + 1)
            w = collisions(page, i, i + 1, calm)
            if w:
                msg = (f'"{w[2]}" × "{w[3]}" {w[4][0]:.0f}x{w[4][1]:.0f}px at p={w[1]:.2f}, '
                       f'in {w[5]}/{len(PS)} sampled frames')
                issues.append(f'COLLIDES   {i + 1}→{i + 2}: {msg}')
                print(f'  COLLIDES  {msg}')
            if a.strips:
                strip(page, i, i + 1, os.path.join(a.strips, f'strip_{i + 1:02d}_{i + 2:02d}.png'))
        browser.close()
    for e in errors:
        issues.append(f'ERROR      {e}')
    print('\n' + ('\n'.join(issues) if issues else 'no findings'))
    if a.strips:
        print(f'contact sheets (frames at p = {", ".join(map(str, STRIP))}) in {a.strips}')
    sys.exit(1 if any(x.startswith(('ERROR', 'LOST')) for x in issues) else 0)


if __name__ == '__main__':
    main()
