---
name: handdrawn-diagram
description: "Render hand-drawn (rough.js sketch-style) architecture, flow and process diagrams with a fixed 9-color palette, serif print typography (Chinese 宋体 / 中宋 + Latin Times New Roman) and no emoji, keeping a whole series of figures in one visual language. Output is static PNGs for articles, docs and slides, or an animated walkthrough (offline HTML slides, optional MP4) that zooms from an overview into detail diagrams and morphs every concept shown on both instead of letting it vanish — for software, business processes, physical or natural systems alike. Triggers: 画架构图 / 画流程图 / 手绘风 / 手绘流程图 / 草图风 / 白板风 / 配色统一 / 架构图样张 / 动态讲解 / 动画演示 / 讲解视频 / 神奇移动 / draw architecture diagram / hand-drawn flowchart / sketch-style diagram / whiteboard-style diagram / consistent color palette across diagrams / animated diagram slides / Magic Move / diagram walkthrough video."
license: MIT
compatibility: Needs a Chromium-based browser (headless Chrome or Playwright) to rasterize HTML to PNG, and network access to load rough.js from jsDelivr and Noto Serif SC from Google Fonts. Animated decks additionally need Python 3.8+ with Playwright (Chromium); Pillow is optional (contact sheets); MP4 export needs ffmpeg.
---

# Hand-drawn Diagram

Render hand-drawn, sketch-style diagrams with a fixed palette, locked typography, and a no-emoji rule. Use this skill whenever the user wants multiple architecture / flow diagrams that share a unified visual language (e.g. one 微信 article with 5 figures).

Two outputs, same drawings:

- **Static figures** (default): one PNG per diagram.
- **Animated deck**: the diagrams of a series played as slides — an overview, camera moves onto one part, that part morphs into its detail diagram, and back. A concept on both diagrams moves and reshapes instead of fading out and in. Delivered as one offline `deck.html`, optionally recorded to MP4. Each diagram is still a normal static figure; it only declares a stable id for every concept that appears on more than one diagram.

## When to load

- User asks to "画架构图 / 画流程图 / 来一张样张 / 手绘风 / 草图风 / 白板风"
- User wants visual consistency across multiple diagrams in one document/article
- User asks to render a diagram and shows preference for hand-drawn style
- Follow-up requests to extend / re-render a diagram in this style
- User wants to walk an audience through a system or process on screen — slides, a talk, a screen recording, a video — or asks for animation / 动态 / Magic Move between diagrams

Do NOT load for: simple Markdown table diagrams, Mermaid (use Mermaid directly), photorealistic illustrations.

## Hard rules (read before drawing)

1. **9 fixed roles, 9 fixed colors — low-saturation warm palette on ivory `#fdfdfa`.** See `references/palette.md`. Never invent a new color for a single diagram. Same role = same color in every figure. Node-internal text color **must** equal the node's `stroke` color (same hue, deeper); every pair already meets WCAG AA (≥ 4.5:1) against its `fill`.
2. **No emoji anywhere.** Use red + hexagon for warnings; bold stroke + main color for emphasis. See `references/typography.md`.
3. **Chinese = Songti / 中宋 (serif print). Latin = Times New Roman.** Both are the most conventional print fonts in their respective scripts. Never use sans-serif (PingFang / Heiti / Noto Sans), never script/handwritten (Caveat / Patrick Hand / Ma Shan Zheng / 楷书 / 行书). The contrast — hand-drawn shapes + engraved print text — is the whole point. See `references/typography.md`.
4. **Arrows are always warm ink `C.flow` (`#3a3530`).** Never color the arrows; only nodes carry color. The single exception is the red dashed error path (rule 5).
5. **Red is for exceptions only.** If you find yourself using red on the happy path, stop.
6. **Color count follows the brief.** Use one color per concept category the brief actually mentions, up to all 9. More than 5 colors → add a compact color legend with `legend()` listing only the colors used (the one exception to Rule 7's no-legend default). Every node carries a text label, so color is never the only cue: several palette pairs (Agent / Sub-Agent, User / LLM, IM / External) are hard to tell apart under red-green color blindness. If a diagram gets too dense to read, split it into an overview + zoom-in diagrams.
7. **Only draw what the user's text actually mentions.** The 9-color palette is a *vocabulary*, not a checklist. If the user's brief does not mention LLM / Tools / External / Memory / IM Channel / Error / status bubbles / timelines, do **not** add them. No "system completion", no "let me also show the underlying stack", no shape-glossary, and no legend unless Rule 6 requires one. When in doubt, list every noun/verb in the user's text first; anything outside that list needs explicit user permission to draw.
8. **Color follows the concept, not the diagram.** In a series of 2+ diagrams, lock every concept's color in `diagram-binding.md` before drawing the first one, and never re-color a locked concept in later diagrams.

## Workflow

### Step 0 — Choose the output

| The reader | Output |
|---|---|
| Reads it in an article, a document, or on paper; one figure answers the question | **Static figures** (default) — Steps 1–6 below |
| Is walked through it on a screen (talk, lesson, recording, video), or one diagram is too dense and they must see where each zoom-in comes from | **Animated deck** — read `references/motion.md` first; it adds a storyboard and concept ids, then uses Steps 1–5 below for every diagram before building the deck |
| Asks explicitly for slides, animation, video, Magic Move | **Animated deck** |

When unsure, deliver static figures. They can become a deck later, usually by adding concept ids, sometimes with small layout changes so details keep their place and nothing collides in flight (`references/motion.md` §1.4, §1.6).

### Step 1 — Read references first

Always skim before drawing:

- `references/palette.md` — the 9 colors, each slot's **abstract meaning** (use this column to map non-Agent domains), and color-count / legend rules
- `references/typography.md` — fonts, punctuation, no-emoji policy
- `references/shapes.md` — shape semantics (box / channel / taskCard / bubble / hexagon / timeline / group frame)
- `references/motion.md` — **animated deck only**: overview vs detail, object constancy, concept ids, camera and pacing, `deck.json`, build / check / record
- `references/domains/` — per-domain concept→color dictionaries (alias table, shape sub-classification, decision tree, exclusion rules). **MUST READ the matching one if it exists:**
  - `domains/agent-team.md` — Agent Team / Multi-Agent / Memory / coding-agent / document-pipeline / research-pipeline
  - `domains/vertical-search.md` — search engines / crawling / indexing / retrieval & ranking
  - No match: map concepts by the abstract-meaning column in `palette.md`; for a reusable dictionary, fill `templates/domain-dictionary.md`

### Step 2 — Plan the diagram on paper (mentally)

Before writing code, decide:

- **First, extract the brief.** List every concrete noun (roles / entities) and verb (actions / transitions) in the user's text. Draw **only** these. If the brief does not name LLM / Tools / External / Memory / IM Channel / Error / 状态气泡 / Timeline, leave them out — see Hard Rule #7.
- **Series of 2+ diagrams: write the binding file first.** Copy `templates/diagram-binding.md` into the working directory, walk every concept of the whole series through the domain dictionary's decision tree (or the abstract-meaning column), and fill in: concept → slot → shape, rulings for ambiguous concepts, and which colors each diagram uses. Before every later diagram, re-read it; new concepts are appended, existing rows never change. Worked example: `examples/vertical-search/`. A single standalone diagram may skip the file.
- **Every diagram**: write the binding into `main()` as a comment block (`// Concept color binding: C.agent = 在线检索 ...`). In a series it must match `diagram-binding.md`. Don't pick colors by gut.
- Which roles appear → which colors
- Who is the main subject → that node gets `strokeWidth: 3`, oversized box (1.3-1.5× others)
- Layout: rows × columns, where the main flow goes (usually left → right)
- Where exceptions branch off (only red path)
- **Resist completion bias.** A 5-noun brief should produce a 5-node diagram, not a 12-node "complete system architecture". A shape glossary belongs to one master reference figure, not every diagram; a color legend appears only when Rule 6 requires it.

### Step 3 — Copy the template

Copy `templates/diagram.html` (path relative to this skill's directory) into the working directory:

```bash
cp <skill-dir>/templates/diagram.html <workdir>/<your_diagram>.html
```

The template provides:

- Font stacks (Times New Roman + Songti SC / STZhongsong / SimSun system fonts; Noto Serif SC web fallback)
- `C` palette constant (9 role colors + flow / bg / title / subtitle / caption)
- `opts(color, override)` — rough.js style baseline: bold 2.4px stroke, roughness 1.6, bowing 1.4, solid light fill
- Shape helpers: `box / channel / taskCard / bubble / hexagon / timeline / frame` (`frame` = dashed group boundary with a title on its top edge)
- Composite helper: `node(x, y, w, h, color, text, sub, opts)` — box + vertically centered label in the stroke color; use it for most entity nodes
- Arrow helper: `arrow(x1, y1, x2, y2, options)` (pass `strokeLineDash` for dashed; pass `stroke: C.error.stroke` for red exception)
- Label helpers: `lbl({...})` (two-line CN+EN), `plain({...})` (single line). Both inject `text` as HTML so `<b>` / `<br>` work; escape literal `<` and `&` as `&lt;` / `&amp;`.
- Legend helper: `legend(x, y, items, cols, colW)` — color key, required only when a diagram uses more than 5 colors
- Title helpers: `title(text, x, y)`, `subtitle(text, x, y)`; `LABEL_BG` — ivory label background for labels that sit on a line
- Motion identity: every helper except `legend` takes an optional last argument `{ id, parent, from, to }`; optional arguments in front of it may be skipped, and `node` / `box` / `arrow` / `lbl` / `plain` take the fields inside the option object they already have. Static rendering ignores it; an animated deck uses it to morph the same concept between diagrams. See `references/motion.md` §4

Edit only the `main()` function. Leave helpers untouched so all diagrams share identical visual baseline, and keep the closing `main();` / `window.__renderDone = true;` lines as they are (the deck builder hooks in there).

### Step 4 — Render to PNG

The template is a static HTML page; rasterize it with a headless browser. It sets `window.__renderDone = true` after drawing.

**Option A — headless Chrome CLI (no extra dependencies).** `file://` works directly. Set `--window-size` to the canvas size; `--virtual-time-budget` gives web fonts and rough.js time to load.

```bash
# macOS: CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# Linux: CHROME=google-chrome   (or chromium)
"$CHROME" --headless=new --disable-gpu --hide-scrollbars \
  --window-size=1720,1240 --force-device-scale-factor=2 \
  --virtual-time-budget=8000 \
  --screenshot=/absolute/path/output.png \
  "file:///absolute/path/<your_diagram>.html"
```

`--force-device-scale-factor=2` gives a 2× PNG for crisp text on phones; drop it for 1×.

**Option B — Playwright / any browser-automation tool.** Set the viewport to the canvas size, open the file, wait for fonts and the render flag, then take a full-page screenshot:

```js
await page.setViewportSize({ width: 1720, height: 1240 });
await page.goto('file:///absolute/path/<your_diagram>.html');
await page.evaluate(async () => { await document.fonts.ready; });
await page.waitForFunction(() => window.__renderDone === true);
await page.screenshot({ path: '/absolute/path/output.png', fullPage: true });
```

The same in Python (the deck scripts use Python Playwright, so this needs nothing extra); `device_scale_factor=2` gives a 2× PNG:

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    page = p.chromium.launch().new_page(viewport={'width': 1720, 'height': 1240}, device_scale_factor=2)
    page.goto('file:///absolute/path/<your_diagram>.html')
    page.evaluate('document.fonts.ready')
    page.wait_for_function('window.__renderDone === true')
    page.screenshot(path='/absolute/path/output.png', full_page=True)
```

Adjust canvas size in the template's `<div class="stage" style="width: ...; height: ...;">` and `<canvas width=... height=...>` to match diagram needs (default 1720 × 1240), and keep the browser window / viewport the same size.

### Step 5 — Self-check before delivery

Open the PNG and look at it. Then run through the typography checklist (`references/typography.md` bottom):

- [ ] No emoji anywhere
- [ ] Chinese is all Songti / 中宋 serif (no Heiti / sans-serif / script / kaiti / handwritten)
- [ ] Latin is all Times New Roman (no Caveat / Patrick Hand / Helvetica / Arial)
- [ ] **No hachure (斜线填充) behind any text label.** Default fill is `solid`. Hachure only on shapes with NO text inside (decorative blocks, legend swatches without overlay text). On phones, hachure lines eat small text.
- [ ] **Background is `#fdfdfa` ivory, not `#ffffff` pure white.** Set on body, .stage, and any label `bg`.
- [ ] **Node text color = node `stroke` color, contrast ≥ 4.5:1 vs `fill`** (palette already verified; don't override with neutral gray or contrasting hue).
- [ ] Every color maps to a category in the brief; more than 5 colors → compact color legend present; every node has a text label
- [ ] Main subject is visibly larger / bolder, not just brighter
- [ ] All arrows are `C.flow` (`#3a3530`) except the Error branch (red dashed)
- [ ] No label overlaps a line, arrow, or another label
- [ ] `main()` has the `// Concept color binding` comment block
- [ ] **Series of 2+ diagrams**: every color used matches `diagram-binding.md`; no locked concept is re-colored; new concepts were appended to the file, not improvised
- [ ] **Every node and arrow on the canvas maps to a noun/verb in the user's brief.** No "system completion", no shape-glossary unless asked, legend only when Rule 6 requires it.

### Step 6 — Deliver

Deliver the PNG itself using whatever attachment / image mechanism the host agent supports, not just a printed path. Keep the `.html` next to it so the figure can be re-rendered or edited later.

## Examples

- `examples/vertical-search/` — **worked multi-diagram series**: `diagram-binding.md` + overview / offline indexing / online retrieval, built with `node()` and `frame()`. Follow this when a request needs several diagrams, or when one diagram would get too dense to read. The same three diagrams also carry concept ids and form an 11-slide animated deck (`deck.json` → `deck.html`): the advanced deck reference, with one → three splits, an explicit `parent`, and concepts travelling across three diagrams.
- `examples/water-supply/` — **first animated deck to read**: city water supply, not software. Overview → camera on the plant → the plant box opens into a frame with four treatment steps → back. Two diagrams, five slides, `diagram-binding.md` with its concept-id table, `deck.json`, built `deck.html`. The code excerpts in `references/motion.md` come from here.
- `examples/concept_palette_cheatsheet.html` + `.png` — **Agent Team color cheatsheet.** All 9 palette slots with Agent-domain aliases, shape sub-classifications, common colors, font/background demo, and exclusion rules in one 2400×1780 reference image. Look at this PNG before starting any Agent Team themed diagram.
- `examples/coding_agent.html` + `.png` — **single dense diagram**: a coding agent handling an issue (orchestrator → developer in a sandbox → verifier → PR, with a red retry path). 8 colors with `legend()`, `frame()` for the sandbox, `hexagon()` for verify / failure. Built by copying the template and editing only `main()`, so its helpers are identical to `templates/diagram.html`.

## Adding new shapes / colors

Don't, unless absolutely needed across multiple diagrams. If you do:

1. Add the color to `references/palette.md` with its abstract meaning and a verified WCAG ratio
2. Add the shape helper to `templates/diagram.html`
3. Update `references/shapes.md` with usage guidance
4. Copy the updated helper block into every `examples/**/*.html` (they are full template copies), re-render them, and check the PNGs
5. Give the new helper the optional last argument `o = {}` like the others, and add its name to one of the two wrap lists in `deck/build.py` (helpers that draw several strokes, or helpers that only pass identity on). A multi-stroke helper that draws one thing (like `taskCard`) also goes into `GROUPED` there, so it can be a concept. Then rebuild both example decks (`python3 deck/build.py examples/<name>/deck.json`) and run `deck/check.py` on each
