# Shapes · 形状语义

新概念优先**换形状**而非新增颜色。所有图共用同一套形状语义。

## 形状对应表

| 形状 | 用途 | helper 函数 |
|---|---|---|
| **矩形 Box** | 实体 / Service / Agent / Resource | `box(x, y, w, h, color, override?)` |
| **长条 Channel** | 通道 / 传输层 / Bus / Queue / IM | `channel(x, y, w, h, color)` |
| **折角卡片 Task Card** | 任务 / Job / Work Unit | `taskCard(x, y, w, h, color)` |
| **对话气泡 Bubble** | 状态消息 / 通知 / IM 推送 | `bubble(x, y, w, h, color, tailSide)` |
| **六边形 Hexagon** | 异常 / 决策 / 兜底 / 终态 | `hexagon(cx, cy, w, h, color)` |
| **虚线时间线 Timeline** | 时序 / 阶段 / 长周期 | `timeline(x1, y, x2, marks)` |
| **虚线分组框 Group Frame** | 子系统 / Sandbox / Workspace / Plan / 临时分组 | `frame(x, y, w, h, color, label?, labelW?)` |

组合 helper：`node(x, y, w, h, color, text, sub?, { box?, size?, subSize? })` = `box()` + 垂直居中的两行标签（文字色自动取 `color.stroke`）。大多数实体节点直接用 `node()`，只有需要自定义标签位置时才分开调 `box()` + `lbl()`。

## 何时用哪种

### 实体 → Box

最常用。任何"是个东西"的角色（用户、Agent、模型、工具、资源）都用矩形。

主角的 Box 加大 + 加粗：

```js
node(770, 195, 340, 150, C.agent, '主 Agent', 'Orchestrator', { box: { strokeWidth: 3 }, size: 30 });
```

### 通道 → Channel (扁长条)

任何"消息流过的地方"用扁长条。和 Box 形状区分（高度只有 60-80px，远扁于 Box）。

适用：IM Channel、Event Bus、Queue、Stream、Pub/Sub topic。

### 任务 → Task Card (折角卡片)

被派发出去的工作单元。折角让它一眼就和"实体 Box"区分开 — 实体是常驻的，任务是流转的。

适用：Sub-task、Job、章节包、版本、独立可并行的工作单元。

### 状态通知 → Bubble (对话气泡)

主 Agent 主动 push 给用户的状态消息。气泡的尾巴 (`tailSide`) 指向消息来源。

```js
bubble(1190, 200, 460, 70, C.im, 'left');
// 尾巴在左 = 消息从左侧的 Agent 飞出来
```

颜色：常规通知用 IM 青色；异常通知用 Error 红色（描边和填充都换）。

### 异常 / 决策 → Hexagon

任何"非正常路径"或"二选一岔口"。形状本身有 caution 含义，配合红色更强烈。

也可用于 Decision 决策节点（菱形 in classical flowchart 也行，但六边形和手绘风更搭）。

### 时序 → Timeline

需要表达"先后顺序"或"长周期"时，画一根横向虚线，标 5 个左右关键时点。

```js
timeline(80, 152, 1620, [
  { x: 200, text: '① 接收' },
  { x: 530, text: '② 拆派' },
  { x: 820, text: '③ 并行' },
  { x: 1130, text: '④ 汇报' },
  { x: 1500, text: '⑤ 完成' },
]);
```

时间刻度用圈数字，文字通过 `plain()` 单独渲染。

## 形状组合范式

### 单 Agent 同步流

`User (Box) → Agent (Box, 主角) → LLM/Tools/Memory (Box) → External (Box)`

线性流，全用 Box，箭头串联。

### 多 Agent 异步协作

```
User (Box) ⇄ IM Channel (长条) ⇄ 主 Agent (大 Box, 主角)
                                          ↓ 拆派
              Sub-Agent A/B/C (浅橙 Box) + Task Card (折角)
                          ↓ 调用
              LLM / Tools / Memory / External (Box)
                          ↓ 异常
                      Error (六边形)
                          ↓ 状态回流
                  Bubble × N (对话气泡)
                          → IM Channel → User
```

没有对应的示例图；按上面的组合自行排布。

### Agent 执行 + 验收 + 失败重试

```
User (Box) ⇄ 主 Agent (大 Box, 主角) → 代码仓库 / External (Box)
                 ↓ 派发
   ┌ Sandbox (tools 色 frame) ─────────────┐
   │ Tools (Box × N) ← Developer (Box)     │ → Verifier (Hexagon) → PASS 回主 Agent
   └───────────────────────────────────────┘          ↓ FAIL (红色虚线)
                 ↓ 调用 (细虚线)                 验收失败 (红 Hexagon)
          LLM (Box) · Memory (Box)                     ↓ 退回 (红色虚线折线) → Developer
```

参见 `examples/coding_agent.html`（8 色 + `legend()`；红色虚线用折线绕开 frame，避免穿过其他节点）。

### 多子系统架构（系列配图）

总览图每个子系统画成一个 Box；放大图把子系统拆成多个同色 Box，外面用同色 `frame()` 圈起来、标题写子系统名。子系统内部的步骤靠名称和序号区分，不拆颜色。

参见 `examples/vertical-search/`（总览 + 离线建库 + 在线检索三张图，共用一份 `diagram-binding.md`）。

### 长周期 + 关键节点

横轴用 Timeline (虚线 + 刻度) 贯穿，纵向放 Agent 和资源。每个时点对应一个状态变化。

## 不要做的事

- 不要用圆形 Circle — 和手绘 Box 的视觉重量不对等
- 不要用云朵 Cloud — 容易让人想到 SaaS 产品 logo
- 不要用 3D 立方体 — 和手绘风彻底冲突
- 不要给同一个角色换形状 — 主 Agent 永远是大 Box，不要某图换六边形
- 不要在 Hexagon 里塞多行文字或带英文短词的标签 — Hexagon 两端是斜 ear（约 `w * 0.18`），文字横向有效宽度只有 `w - 2*ear`。要列文字标签（接口名 / 卡片）一律用 Box，不要用 Hexagon。Hexagon 仅用于决策 / 异常 / 终态等单点语义节点。

## 虚线分组框为什么不用 `rc.rectangle`

`frame()` 内部用 4 条 dashed line 围成矩形，**不要自己用 `rc.rectangle` 画分组框**：模板默认填充是 `solid`，
即使传 `fill: 'none'`，rough.js 在带笔触模式下仍可能渲染出实色或额外笔画，把内部节点遮死。

```js
frame(340, 280, 1330, 210, C.agent, '在线检索');   // 标题自动带 LABEL_BG 底色, 不会被虚线穿过
```

标题宽度默认 160px，标题较长时传第 7 个参数 `labelW`。分组框和内部节点之间留 ≥ 28px 空隙，避免虚线贴着节点边框。
