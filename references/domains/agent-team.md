# Agent Team 概念 → 颜色字典

适用：**Agent Team / Multi-Agent / Memory / coding agent / 文档流水线 / 研究流水线** 等主题文章配图。本文件是 `references/domains/` 下的一份领域字典；其他领域见同目录，新领域按 `templates/domain-dictionary.md` 填写。

> **可视化样张**：[`../../examples/concept_palette_cheatsheet.png`](../../examples/concept_palette_cheatsheet.png)
> 把本文档的全部内容渲染成一张 2400×1780 的色卡参考图——9 色 slot × 概念 alias × shape 速查 × 通用色 × 字体 demo × 互斥规则。**画图前先看那张 PNG，再回这份文档查决策树和反例。**

## 为什么需要这份字典

一篇关于 Agent Team 的长文，配图通常 5-10 张：IM 异步执行、coding agent 协作、信息检索研究、文档流水线、Memory 分层、Verifier 协作流、状态机时序、跨厂商对照……

**同一个概念在不同图里必须永远是同一颜色 + 同一形状基线**。否则读者每张图都要重新建立"这个色是谁"的认知，跨图读不通。

这份字典给每个高频概念锁定一个色 slot 和一个 shape 基线。**画图前先查这里，不要凭记忆挑色**。

## 主表 · 9 色 9 类概念

| 颜色 slot | 主义类 | 常见别名 (alias) | 默认 shape |
|---|---|---|---|
| **`C.user`** 钢蓝 | 人 / 决策者 | User · 用户 · 终端用户 · 决策者 · 提问者 · Operator · Human-in-the-loop · 人类签字 · 人类审批 · 责任链中的人 | Box (普通) / Hexagon (人类决策点) |
| **`C.im`** 墨青 | 异步通道 / 状态 | IM Channel · 微信 · Telegram · Feishu · Slack · 通讯通道 · Async Push · Status Bubble · 状态气泡 · 进度通知 · 心跳 · ACK 回执 | Channel (扁长条) / Bubble (状态消息) |
| **`C.agent`** 砖橙 | 唯一主角 / 控制面 | Owner · Orchestrator · 主 Agent · Supervisor · 控制面 · 编排核心 · Coordinator · Planner (负责拆派的那一个) · Plan / Round (Orchestrator 视角的运行单位) | Box (大号 + strokeWidth: 3) / Group Frame (Plan/Round 边框) |
| **`C.subagent`** 焦糖 | 派出去的执行者 / 验证者 | Worker · Sub-Agent · Developer · Writer · Researcher · Formatter · Tool Agent · Doc Worker · Verifier · Tester · Reviewer · Producer · Critic · Synthesizer · 任意被 dispatch 的 task-level agent | Box (普通) / Hexagon (Verifier / 决策语义) / Task Card (Worker 处理的 Task 实体) |
| **`C.llm`** 靛紫 | 推理 / 模型 | LLM · 模型 · Reasoner · GPT · Claude · Gemini · 推理引擎 · 决策模型 · Foundation Model · 基座模型 | Box |
| **`C.tools`** 苔绿 | 可执行能力 / 隔离环境 | Tools · MCP · MCP Server · Skill (作为可执行能力时) · Tool Gateway · CLI · API call (本系统内) · Sandbox · Workspace · Worktree · 沙箱 · 容器 · Agent Harness · 工具链 | Box / Group Frame (Sandbox/Workspace 隔离区，虚线分组框) |
| **`C.memory`** 栗棕 | 记忆 / 持久化 / 交接物 | Memory · User Memory · Agent Memory · Team Memory · Topic Memory · 记忆 · 持久化 · KV / DB / 向量库 · scratchpad · handoff 文档 · 交付物 · session log · archive · AGENTS.md / CLAUDE.md 类记忆文件 · Skills (作为知识沉淀时, vs Tools 维度) | Box / Task Card (单条记忆条目 / 文件) |
| **`C.external`** 墨灰 | 外部 / 第三方 / 行业对照 | External · 第三方 API · 外部服务 · GitHub · OpenAI Agents SDK · Google A2A / ADK · Anthropic Agent Skills · AWS Bedrock AgentCore · 学术论文 / benchmark · 任何"不在本系统内"的依赖或对照参考 | Box (实线) / Box (虚线 strokeLineDash, 表示"行业参照非本系统") |
| **`C.error`** 砖红 | 异常 / 失败 / 阻塞 | Error · Block · Blocker · Stuck · 异常路径 · 失败 · Retry · FAIL · Verifier FAIL · 兜底 · 退回 · Reject · Escalation · 记忆污染 · 上下文污染 · 风险动作 (在被人类审批拦下之前) | Hexagon (异常/决策语义) / Bubble (异常通知, 配 IM 形状但用 Error 色) |

## 通用色（不算"角色"，但跨图固定）

| 颜色 | 用途 | 别名 |
|---|---|---|
| **`C.flow`** 暖墨 `#3a3530` | 所有箭头、Timeline 虚线、Workflow / Pipeline 流向 | 流向 · 信息流 · 调用 · 传递 · 转交 · 派发 · 时序 · 轮次推进 |
| **`C.bg`** 暖米白 `#fdfdfa` | 画布底色 | 纸面 · 背景 |
| **`C.title`** `#2a2520` | 大标题 | — |
| **`C.subtitle`** `#5a544f` | 副标 | — |
| **`C.caption`** `#7a746e` | 注释 / Cost / Token / Budget / ROI 小字 / 论文出处 / 时间戳 | 不要为 Cost / 数字 开新色 |

## 形状二级区分（同色下用 shape 拆子类）

每个色 slot 内可能装多个子概念，靠 **shape** 区分而不是新开颜色。

### `C.subagent` 内部分工（最复杂的 slot）

| 子角色 | shape | 说明 |
|---|---|---|
| Worker / Developer / Writer / Researcher / Formatter | Box (普通) | 执行实体 |
| Verifier / Tester / Reviewer | **Hexagon** | 验证语义；和 Worker 形状不同, 一眼看出"这是 verify 节点" |
| Task / Job / Sub-task / Work Unit (被处理的工作包) | Task Card (折角) | 流转物, 不是常驻实体 |

> 关键：**Worker 和 Verifier 通常是 task 级成对的**（一个 task 由一个 worker 执行、另一个 verifier 验收），所以同色 + 不同 shape 一眼配对。不要给 Verifier 单独开色。

### `C.memory` 内部分层

| 子层 | shape | 说明 |
|---|---|---|
| User Memory | Box | "懂用户" 层 |
| Agent Memory | Box | "越来越熟练" 层；可加 Task Card 表示单个记忆文件 |
| Team Memory | Box (**虚线边框** `strokeLineDash: [10,6]`) | 临时态, 用虚线表示"运行时存在" |
| Topic Memory / scratchpad / handoff | Task Card | 单文件实体 |

> User Memory **不要**用 `C.user` 色（user 是角色，user memory 是记忆，分到不同 slot），否则跨图概念会撞。

### `C.tools` 内部分类

| 子类 | shape | 说明 |
|---|---|---|
| Tools / MCP Server / Skill (能力侧) | Box | 普通工具 |
| Sandbox / Workspace / Worktree / Agent Harness 隔离区 | **Group Frame** (4 条 dashed line 围矩形) | 表示"环境隔离"; 内部装 Worker / Tools |

### `C.agent` 内部

| 子类 | shape | 说明 |
|---|---|---|
| 主 Agent / Orchestrator | Box (大号 + strokeWidth: 3) | 唯一主角, 永远比 Worker 大 1.3-1.5× |
| Plan / Round | **Group Frame** (虚线分组框) | 表示"这一组任务由 Orchestrator 协调" |

### `C.user` 内部

| 子类 | shape | 说明 |
|---|---|---|
| User (普通输入) | Box | 输入端 |
| 人类审批 / Human-in-the-loop / 人类签字 | **Hexagon** | 决策节点; 用六边形是因为决策语义 = 和 Verifier 一致, 但用 user 色和 Verifier 区分 |

### `C.error` 内部

| 子类 | shape | 说明 |
|---|---|---|
| Error / Failure / Block 节点 | Hexagon | 异常终点 |
| 异常状态通知 | Bubble (用 IM 形状, 但填 Error 色) | "C 路异常 · 是否重试?" 这类 push |

## 决策树 · 拿到一个名词怎么定色

```
是不是发起者 / 决策者 / 接收者?
  └ Yes → C.user (人类决策点用 Hexagon)
  └ No
是不是消息通道 / 异步反馈 / 状态推送?
  └ Yes → C.im
  └ No
是不是控制面 / 拆派合并 / 唯一主角 / Plan/Round 单位?
  └ Yes → C.agent
  └ No
是不是被派出去的执行者 / 验证者 / 任务包?
  └ Yes → C.subagent (Verifier 用 Hexagon, Task 用 Task Card)
  └ No
是不是推理 / 模型?
  └ Yes → C.llm
  └ No
是不是工具 / Skill 能力 / 沙箱 / 隔离环境?
  └ Yes → C.tools (隔离环境用 Group Frame)
  └ No
是不是记忆 / 持久化 / 交接物 / 经验沉淀?
  └ Yes → C.memory (Memory 三层全在这, Topic/scratchpad 用 Task Card)
  └ No
是不是第三方 / 外部依赖 / 行业对照?
  └ Yes → C.external (论文/对照用虚线 Box)
  └ No
是不是异常 / 失败 / 阻塞 / 风险动作?
  └ Yes → C.error (节点用 Hexagon, 异常通知用 Bubble + Error 色)
  └ No
是不是 Cost / Token / Budget / ROI / 时间戳 / 数字注释?
  → 不开色, 用 C.caption 灰色小字标注
是不是 Workflow / Pipeline / 流向 / 时序?
  → 不开色, 用 C.flow 箭头 / Timeline 表达

实在归不到? → 优先合并到最近的 slot, 不要开新色; 或者改用形状区分。
```

## 互斥规则（强约束，画图时检查）

1. **`User` 角色 ≠ `User Memory`**——前者 `C.user`，后者 `C.memory`。同色会让"用户"和"关于用户的记忆"在图上混成一团。
2. **`Owner` / `Orchestrator` 不要染成 `C.user`**——它是 Agent (机器)，人类审批 / 签字才是 `C.user`。Orchestrator 永远 `C.agent`。
3. **`Verifier` 不要单独开色**——`C.subagent` + Hexagon 即可。Worker 和 Verifier 同色才能体现"task 级成对"语义。
4. **`Skill` 在不同语境下选不同色**：
   - 作为"可执行能力 / 工具"（Agent Skills 这类可加载能力包）→ `C.tools`
   - 作为"知识沉淀 / 经验"（Agent 自己总结写回的经验文档）→ `C.memory`
   - 一张图里只可能是一种语义，按当前主题选。
5. **`External` 内部进一步分**：
   - 行业对照（OpenAI / Google / Anthropic / AWS）+ 论文 / benchmark → `C.external` + **虚线 Box** 表示"非本系统"
   - 真实被调用的第三方 API（搜索引擎 / OSS / 数据库） → `C.external` + 实线 Box
6. **`Error` 出现时整张图的"异常路径"全部走红色虚线 dashed arrow**——Worker → Verifier FAIL → 人类审批 (Reject) → Retry 这条链是连贯的红，不要中间换色。
7. **颜色按需，不按清单**——9 色是字典，不是清单。只给本图需求里出现的概念上色，没出现的颜色不画；超过 5 种颜色时附颜色图例。

## 反例（常见错误）

| 错误 | 为什么错 | 正确做法 |
|---|---|---|
| User Memory 染成蓝色 | 跟 User 角色撞色 | User Memory 用 `C.memory` 棕色，配 Box |
| Verifier 用绿色 (好像 "通过 = 绿") | 只有 9 色，不能为单一概念开第 10 色 | `C.subagent` 焦糖 + Hexagon 形状 |
| Orchestrator 用蓝色 (User 蓝, Orchestrator 也算 "主导者") | Orchestrator 是机器, User 是人, 必须分色 | Orchestrator = `C.agent` 砖橙 |
| 把 Cost / Token 数字用大号鲜红 | Cost 不是 Error, 染红会让读者以为预算超了 | 用 `C.caption` 暖灰小字 |
| 给每个 Sub-Worker 换色 (蓝 Developer / 绿 Tester / 紫 Reviewer) | 角色色 = 概念色, 不是个体色; 同一类拆成多色, 读者会以为它们是不同类别 | Developer / Tester / Reviewer 全用 `C.subagent`, 用 sub-label "Developer" / "Tester" / "Reviewer" 文字区分; Verifier 们用 Hexagon |
| Memory 三层各用一个色 (User Memory 蓝, Agent Memory 棕, Team Memory 灰) | 跟 User / External 角色撞色, 字典污染 | 三层都用 `C.memory`, 靠 shape 区分: User Memory Box / Agent Memory Box / Team Memory **虚线 Box** |
| 异常通知气泡用 IM 青色 | 看不出"这是异常"还是"普通进度" | Bubble 形状保留, 但填 `C.error` 红色 |
| Plan/Round 用单独颜色 (灰色框圈一组任务) | Plan/Round 是 Orchestrator 的运行单位 | `C.agent` 色虚线 Group Frame, 标题写 "Round 1" 之类 |
| Sandbox / Workspace 用 external 灰 (好像"不在 prompt 里"算外部) | Sandbox 是工具能力, 不是第三方 | `C.tools` 苔绿 Group Frame |

## 系列文章配图清单（示例）

假设一篇 "Agent Team + Memory" 主题长文要配 5-10 张图，可以这样分配色覆盖：

| 图编号 | 主题 | 颜色 | 关键 shape |
|---|---|---|---|
| 1 | 单 Agent vs Agent Team 对比 | user / agent / subagent / error | Box, Bubble |
| 2 | IM 异步执行 | user / im / agent / subagent | Channel, Bubble, Timeline |
| 3 | Coding agent 协作 (Developer/Tester/Reviewer) | agent / subagent / tools / external | Box, Hexagon, Group Frame (sandbox) |
| 4 | 信息检索研究 | agent / subagent / external / memory | Box, Hexagon (verifier), Task Card (来源卡) |
| 5 | 文档流水线 | agent / subagent / tools / memory | Box, Task Card, Group Frame (workspace) |
| 6 | Orchestrator / Worker / Verifier 协作三角 | agent / subagent / user (decision) | Box, Hexagon (verifier + decision) |
| 7 | Memory 三层 | memory only (+ user / agent / im 引用箭头到对应方) | Box, 虚线 Box (Team Memory) |
| 8 | Plan / Round 状态机 | agent / subagent / error | Group Frame, Hexagon, Timeline |
| 9 | 行业对照 (Google / Anthropic / OpenAI / AWS) | external (虚线 Box) + agent | Box (虚线), 文字标 |
| 10 | Memory 注入与污染 | memory / agent / error | Box, 虚线 Box, Bubble (Error 色) |

每张图都要在 main() 顶部注释里写：

```js
// Concept color binding (this diagram):
//   C.agent    = Orchestrator / Plan
//   C.subagent = Worker (Developer / Writer)
//   C.error    = Verifier FAIL / Reject
//   C.flow     = arrows / timeline
// Concepts NOT in this diagram (but reserved in palette): user, im, llm, tools, memory, external
```

这样每张图自带"色—概念" mapping 注释，跨图 review 时一眼对得上。系列配图 (≥ 2 张) 还要把本表的选择抄进工作目录的 `diagram-binding.md`（模板：`templates/diagram-binding.md`），各图注释与它保持一致。
