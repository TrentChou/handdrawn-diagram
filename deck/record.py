"""Record a built deck to MP4, frame by frame, at the deck's own transition timing.

usage: python3 record.py deck.html [-o deck.mp4] [--scale 2] [--fps 60]

Each slide is one screenshot held for its reading time; each transition is stepped with
__deck.freeze(i, j, p), so the motion is exact however slow the machine is. Frames are piped into
ffmpeg (H.264, yuv420p, bt709). The video has the deck's stage size (1920x1080 by default);
--scale 2 doubles it (3840x2160).

Hold time per slide: the slide's "hold" (seconds) from deck.json if set, otherwise 2 s + 0.2 s for
every line to read (new on this slide, or just brought into focus), kept within 2-6 s. The video
fades in from and out to paper colour (0.8 s / 1.5 s); the last slide is held 1.5 s longer for it.
"""
import argparse
import os
import subprocess
import sys

from playwright.sync_api import sync_playwright

PAPER = '0xfdfdfa'
FADE_IN, FADE_OUT = 0.8, 1.5


def hold_seconds(slide, new_lines, last):
    t = slide.get('hold') or min(6.0, max(2.0, 2.0 + 0.2 * new_lines))
    return t + (FADE_OUT if last else 0)


def ffmpeg(out, fps, total):
    vf = (f'scale=out_color_matrix=bt709,fade=t=in:d={FADE_IN}:color={PAPER},'
          f'fade=t=out:st={max(0, total - FADE_OUT):.3f}:d={FADE_OUT}:color={PAPER},'
          'format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv')
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(fps), '-c:v', 'png', '-i', '-',
           '-vf', vf, '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-movflags', '+faststart', out]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)


def main():
    ap = argparse.ArgumentParser(description='Record a built deck to MP4.')
    ap.add_argument('deck')
    ap.add_argument('-o', '--out')
    ap.add_argument('--fps', type=int, default=60)
    ap.add_argument('--scale', type=float, default=1, help='2 = 3840x2160')
    a = ap.parse_args()
    out = a.out or os.path.splitext(a.deck)[0] + '.mp4'

    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--force-color-profile=srgb'])
        page = browser.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=a.scale)
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.goto('file://' + os.path.abspath(a.deck))
        page.wait_for_function('window.__ready === true', timeout=60000)
        w, h = page.evaluate('[__deck.W, __deck.H]')
        page.set_viewport_size({'width': w, 'height': h})      # the video is exactly the stage
        slides = page.evaluate('__deck.SLIDES.map(s => ({ hold: s.hold, note: s.note }))')
        n = len(slides)
        holds = [round(hold_seconds(s, page.evaluate(f'__deck.stats({i}).newLines'), i == n - 1) * a.fps)
                 for i, s in enumerate(slides)]
        trans = [round(page.evaluate(f'__deck.freeze({i}, {i + 1}, 0)') / 1000 * a.fps) for i in range(n - 1)]
        page.evaluate('__deck.setState(0)')
        total = (sum(holds) + sum(k - 1 for k in trans)) / a.fps   # frame k of a transition = next slide's hold
        ff = ffmpeg(out, a.fps, total)
        frames = 0
        for i in range(n):
            page.evaluate(f'__deck.setState({i})')
            png = page.screenshot(type='png')
            for _ in range(holds[i]):
                ff.stdin.write(png)
            frames += holds[i]
            print(f'slide {i + 1:2d}  hold {holds[i] / a.fps:4.1f}s  {slides[i]["note"]}', flush=True)
            if i + 1 < n:
                k = trans[i]
                for f in range(1, k):
                    page.evaluate(f'__deck.freeze({i}, {i + 1}, {f / k})')
                    ff.stdin.write(page.screenshot(type='png'))
                page.evaluate(f'__deck.freeze({i}, {i + 1}, 1)')
                frames += k - 1
        ff.stdin.close()
        if ff.wait() != 0:
            sys.exit('ffmpeg failed')
        browser.close()
    if errors:
        sys.exit('page errors: ' + '; '.join(errors))
    print(f'{frames} frames, {frames / a.fps:.2f}s → {out}')


if __name__ == '__main__':
    main()
