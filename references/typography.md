# Typography · 字体 / 标点 / Emoji 约束

整套图的视觉一致性，2/3 靠字体和标点。**emoji 一律禁止**。

## 风格定位

**手绘形状 + 印刷字体**。形状走 rough.js 的抖动笔触 + bowing 笔锋 + 浅色实填（`fillStyle: 'solid'`），文字走最常规的衬线印刷字体（中文宋体 / 西文 Times）。这种"草图骨架 + 正文字"的反差，是本风格的核心识别度——像教授在白板上画图、底下贴正经课件，或者教科书插图配印刷版字注。

不是手写体。不是黑体。不是楷体。不是 Comic Sans 也不是 Caveat。

## Emoji

**全图禁止使用 emoji**。包括但不限于：

- 节点标题、副标题
- 连线标签、箭头说明
- 图例、Legend
- 标题、副标题、脚注

替代方案：

| 想表达的语义 | 用什么替代 |
|---|---|
| ⚠️ 警告 / 异常 | `C.error` 砖红 (`#a52928`) + 六边形 + 文字 "Error" / "异常" |
| ✅ 完成 / 成功 | 文字 "Done" / "完成" + 描边收尾或对话气泡 |
| ❗ 重点 | 加粗描边 (strokeWidth 3+) + 大字号 + 主角色 |
| 💡 提示 / 说明 | 灰色小字注释，独立成行，不混在节点内 |
| 🔄 循环 / 重试 | 双向箭头 / 回路弧线 + 文字 "retry" |
| ⏰ 时间 / 等待 | Timeline 虚线 + 时间刻度 |

理由：emoji 在不同平台（iOS / Android / 微信 PC / 微信 Mac）渲染差异巨大；和印刷字质感冲突；多图统一时极易破功。

## 字体

### 西文 (Latin)

| 用途 | 首选 | 备选 | 字号区间 |
|---|---|---|---|
| 大标题 | **Times New Roman**（粗体）| Times / Liberation Serif | 36-48px |
| 节点标题 | **Times New Roman**（粗体）| Times | 22-32px |
| 节点副标题 / 标签 | **Times New Roman**（常规）| Times | 14-19px |
| 备注小字 | **Times New Roman**（常规）| Times | 13-16px |

Windows 和 macOS 都自带 Times New Roman；Linux 通常没有，会落到 `Liberation Serif`（度量兼容 Times）或 `serif`。英文不走 Web 字体。

```css
font-family: 'Times New Roman', Times, 'Liberation Serif', serif;
```

### 中文 (CJK)

| 用途 | 首选 | 备选 | 严禁 |
|---|---|---|---|
| 大标题 / 节点主标 | **STZhongsong**（华文中宋）| Songti SC Bold / SimSun Bold / Noto Serif SC weight 700 | 黑体 / 楷体 / 行书 / 手写体 |
| 节点副标 / 正文 | **Songti SC**（宋体-简）| STSong / SimSun / 宋体 / Noto Serif SC | 同上 |
| 备注小字 | **Songti SC** | STSong / SimSun / Noto Serif SC | 同上 |

中宋（**STZhongsong** / 华文中宋）是宋体家族里中等粗细的成员，介于 Regular 和 Bold 之间，适合标题和强调。它是商业字体，**macOS 和 Windows 都不预装**（通常随 Microsoft Office 中文环境安装），所以字体栈里排在它后面的 `Songti SC`（macOS 自带）/ `SimSun`（Windows 自带）+ `font-weight: 700` 才是大多数机器上的实际效果。没有任何宋体的环境（多数 Linux、容器）落到 Web fallback 思源宋体 SC（**Noto Serif SC**，SIL OFL，Google Fonts 托管）。

CSS 字体栈推荐（按"中宋-宋体-思源宋体-serif"顺序）：

```css
/* 标题 / 主标 — 走中宋 */
font-family: 'STZhongsong', '华文中宋', 'Songti SC', 'SimSun', '宋体', 'Noto Serif SC', serif;
font-weight: 700;

/* 正文 / 副标 — 走宋体 */
font-family: 'Songti SC', 'STSong', 'SimSun', '宋体', 'Noto Serif SC', serif;
font-weight: 400;
```

Web 加载（仅中文兜底，英文不需要 Web 字体）：

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### 为什么是宋体 + Times 而不是手写体或黑体

1. **形状已经"手绘"了**——rough.js 的抖动笔触 + bowing 弯曲本身就是 noise。文字再叠手写感，视觉信息密度爆表，看着累。
2. **宋体 + Times 是中文出版物 / 学术论文 / 严肃报告的默认字体**，几十年视觉沉淀，识别成本接近零。读者注意力会落在内容上而不是字体本身。
3. **手写体（Caveat / Ma Shan Zheng / 楷书 / 行书）字符宽度不稳定、可读性差**。节点标签密集时，14-16px 的小字会糊。宋体 / Times 同字号下识别率明显更高。
4. **黑体（PingFang / 苹方 / Heiti）和 rough.js 手绘形状不搭**——黑体太"工业 UI"、太"App 设计稿"，手绘草图配 App UI 字体会显得错位。
5. **印刷体 + 手绘形状 = "草图笔记"质感**，像教授白板课件、读书笔记 marginalia、技术博客插图——稳重又有人味，多图并排时不抢戏。
6. **Times New Roman 和宋体在视觉密度、笔画粗细对比上是亲戚**，混排不打架；中英混排 0 违和感。

### 严禁手写体 / 黑体 fallback

Canvas `ctx.font` 和 CSS `font-family` 兜底必须是 `serif`，**不要写 `cursive` 或 `sans-serif`**。一旦走到 `cursive`，macOS / iOS 会渲染成系统楷体或手写体；走到 `sans-serif` 就是黑体。两种都破坏整体风格。

```js
// BAD — 兜底是 cursive 或 sans-serif，跨设备会跑偏
ctx.font = `700 44px 'Times New Roman', cursive`;
ctx.font = `700 44px 'STZhongsong', sans-serif`;

// GOOD — 兜底是 serif
ctx.font = `700 44px 'Times New Roman', 'STZhongsong', '华文中宋', 'Songti SC', 'SimSun', 'Noto Serif SC', serif`;
```

CSS 同理：

```css
/* BAD */
.ti { font-family: 'Times New Roman', cursive; }
.bd { font-family: 'Songti SC', sans-serif; }

/* GOOD */
.ti { font-family: 'Times New Roman', 'STZhongsong', '华文中宋', 'Songti SC', 'SimSun', 'Noto Serif SC', serif; }
.bd { font-family: 'Times New Roman', 'Songti SC', 'STSong', 'SimSun', 'Noto Serif SC', serif; }
```

注意字体栈里**先放西文（Times New Roman），再放中文**。浏览器会按字符逐个匹配：英文字符落到 Times，中文字符跳过 Times 落到 Songti / 中宋。这样一段中英混排文本里，英文是 Times、中文是宋体，自动分工，无需手动切。

### 字体使用纪律

1. **整张图字体家族 ≤ 2 种** —— 一种走中宋（标题、节点主标）；一种走宋体（副标、正文、注释）。Times New Roman 自动随中宋 / 宋体的字体栈生效，不算独立家族。
2. **同一标签内中英文分工自动完成** —— 字体栈里 Times 在前、Songti 在后，浏览器逐字符匹配。不要手动 `<span>` 切。
3. **加粗用 `font-weight: 700` 让宋体变粗体**，效果和中宋接近；但首选写真正的中宋（`STZhongsong`），更准。
4. **不要叠多种 font-style**——不用斜体（`italic`），宋体的斜体在浏览器里是机械倾斜，丑且不专业。

## 填充与文字可读性

模板默认 `fillStyle: 'solid'`（浅色实填）+ 暖米白底 `#fdfdfa`。**hachure（斜线填充）默认禁用，仅在节点内部不放任何文字时才允许 override**。

### 颜色对比度门槛

节点内文字色必须用对应角色的 `stroke` 色（同色相深色），不要换中性灰、不要换对比色。整套 9 色已按 **WCAG 2.1 AA**（≥ 4.5:1）调过，详见 `references/palette.md` 对比度表。

新增颜色或自定义调色时，**必须**先用 WCAG 公式验算 `stroke` 对 `fill` 的对比度，未达 4.5:1 直接不要用。在线工具：[contrast-ratio.com](https://contrast-ratio.com/) / [webaim.org/resources/contrastchecker](https://webaim.org/resources/contrastchecker/)。

反面教材（直接拿 [Open Color](https://yeun.github.io/open-color/) 高饱和色当 stroke + fill）：

| 角色 | stroke | fill | 对比度 | 后果 |
|---|---|---|---|---|
| Sub-Agent | `#f08c00` 亮橙 | `#ffe066` 鲜黄 | **1.9:1** | 黄底橙字, 几乎不可读 |
| Agent | `#e8590c` 鲜橙 | `#ffd8a8` 浅橙 | **2.7:1** | 同色异度, 字浮在背景上糊 |
| User | `#1971c2` 电蓝 | `#a5d8ff` 鲜浅蓝 | **3.3:1** | 不到 AA, 长时间看眼累 |

本套色卡全部 ≥ 4.5:1（多数 5-7:1），文字稳得住。

### 为什么 hachure 必须禁用

1. **手机 / 微信图片预览缩到 350-400px 宽**时，hachure 斜线和 14-18px 的小字会糊到一起，文字被斜线截断，读者得放大才能看清。
2. **宋体 / Times 是衬线字体**，本身笔画就细腻；衬线遇到 hachure 的斜杠形成"斜线密集区"的负向干扰，比黑体 + hachure 更糟。
3. **solid 浅色实填 + rough 描边** = "草图笔记里贴了一张便利贴"的视觉，干净、稳重、印刷感；这是 rough.js 内置的填充模式之一，不是降级。

什么时候可以 hachure：

- **图例 / Legend 的小色块**且色块旁边才放文字（文字不在色块内）—— 此时 hachure 反而强化"这是个色样"的语义
- **纯装饰元素**：分组背景、底纹、不承载关键信息的填充区域
- **强调主角**且主角内不放正文（极少用，一般用 strokeWidth + 加大尺寸即可强调）

写法：

```js
// 默认 — 文字背后干净, stroke 就是文字色
box(120, 200, 200, 110, C.user);

// override 为 hachure (节点内不放文字时才用)
box(SX, SY, 50, 30, C.subagent, { fillStyle: 'hachure', hachureGap: 6, hachureAngle: -41 });
```

### 底色不用纯白

整图背景设为 `#fdfdfa` 暖米白（253/253/250），不要 `#ffffff`：

- 纯白 + 低饱和填充 = 节点像漂浮在屏幕上, 没着陆感
- 暖米白和暖色系填充同色温, 整体协调
- 长时间阅读时, 暖米白比纯白伤眼少
- 印刷出来 / 微信图片预览里, 米白比纯白更显"纸面感"

`body { background: #fdfdfa; }` + `.stage { background: #fdfdfa; }` 都要写, 别只写 body。

## 标点

### 中英混排

- 中英文之间留**半角空格**（盘古之白）：`Agent · 编排核心` 而不是 `Agent·编排核心`
- 数字和中文之间也留：`已派出 3 路` 而不是 `已派出3路`

### 节点标签内

- 分隔符用 `·` (中点) 或 `/` (斜杠)：`Tools · MCP` / `章节 / 版本 1`
- **禁用** `、` `,` `；` 作为节点内分隔
- 节点标签短到不需要句号 — 不加任何句号

### 序号

- 用圈数字 `① ② ③ ④ ⑤ ⑥ ⑦ ⑧ ⑨ ⑩`
- 不用 `1. 2. 3.` 或 `(1) (2) (3)`
- 圈数字紧凑，宋体下也清晰

### 括号 / 引号

- 括号统一英文 `( )`，**禁用**中文 `（ ）`
- 引号统一弯引号 `" "` 或直引号 `" "`，全图选一种到底，不混用
- 单引号同理

### 符号

| 用途 | 用 | 不用 |
|---|---|---|
| 破折号 | `—` (em dash) | `--` `~` `~~` |
| 省略号 | `…` | `...` |
| 连接 / 流向 | `→` | `->` `=>` |
| 双向 | `⇄` 或 `↔` | `<->` `<=>` |
| 区间分隔 | `—` 或 `-` (en dash) | 中文破折号 `——` |

### 大小写

- 英文专有名词保持原样：`LLM` / `MCP` / `IM` / `Agent` / `Sub-Agent`
- 缩写不要加点：`API` 不写 `A.P.I.`
- Title Case 仅用于一级标题；副标题、标签都用 sentence case

## 自检清单

提交一张图前过一遍：

- [ ] 没有 emoji
- [ ] 中文都是宋体 / 中宋 (无黑体 / 楷体 / 行书 / 手写体 / sans-serif fallback)
- [ ] 西文都是 Times New Roman (无 Caveat / Patrick Hand / Helvetica / Arial / Comic Sans)
- [ ] 字体家族 ≤ 2 种 (中宋 + 宋体，西文随字体栈自动落到 Times)
- [ ] 字体栈兜底是 `serif` 不是 `cursive` 也不是 `sans-serif`
- [ ] 字体栈把英文 Times 放在中文宋体之前 (canvas font 和 CSS 都查)
- [ ] **填充默认 solid，文字背后没有 hachure 斜线**
- [ ] **底色 #fdfdfa 暖米白，不是纯白 #ffffff**
- [ ] **节点内文字色 = 节点 stroke 色，对自家 fill 对比度 ≥ 4.5:1 (WCAG AA)**
- [ ] 中英文之间有空格
- [ ] 没有中文括号 `（）`
- [ ] 没有斜体 (没用 `italic` / `font-style: italic`)
- [ ] 引号风格全图一致
- [ ] 序号用圈数字
- [ ] 节点标签没有句号
- [ ] 破折号用 `—`，省略号用 `…`
