# 垂直搜索引擎系列配图 · 概念配色绑定

画第一张图之前锁定。后续每张图先读本文件；遇到新概念只能追加，不能改已有行。
概念归类依据：`references/domains/vertical-search.md`。

## 概念 → 颜色 → 形状

| 概念类别 | 包含组件 | 颜色 slot | 形状 |
|---|---|---|---|
| 用户 | 用户 / 搜索框 | `C.user` 钢蓝 | Box |
| 数据源 | 目标网站 · 合作方 Feed · 开放 API | `C.external` 墨灰 | Box (实线, 真实被抓取的来源) |
| 离线建库 | 爬虫 · 解析抽取 · 去重清洗 · 建索引 | `C.subagent` 焦糖 | Box; 多组件时外加同色 `frame()` |
| 在线检索 | Query 理解 · 多路召回 · 排序 · 结果组装 | `C.agent` 砖橙 | Box; 多组件时外加同色 `frame()` |
| 存储 | 倒排索引 · 正排库 · 向量库 (总览图合并为"索引存储") | `C.memory` 栗棕 | Box |
| 模型 | Embedding 模型 · 排序模型 | `C.llm` 靛紫 | Box |
| 队列 | URL 抓取队列 | `C.im` 墨青 | Channel |

## 歧义概念的裁决

- 向量库 → 存储 (`C.memory`)，不是模型。生成向量的 Embedding 模型才是 `C.llm`。
- 建索引 → 离线建库 (`C.subagent`)，不是存储。它是加工动作，索引本身才是存储。
- 离线建库放大图里，离线流水线是主体，但仍用 `C.subagent`，靠 `frame()` 和尺寸突出，不借用 `C.agent`。

## 每张图使用的颜色

| 图 | user | subagent | agent | memory | llm | im | external |
|---|---|---|---|---|---|---|---|
| ① 总体架构 `01_overview` | ● | ● | ● | ● | | | ● |
| ② 离线建库 `02_offline` | | ● | | ● | | ● | ● |
| ③ 在线检索 `03_online` | ● | | ● | ● | ● | | |

## 概念 id（动态 deck 用）

各图 helper 里写的 `{ id, parent }` 以本表为准。`deck.json` 把三张图串成一套动态讲解。

| id | 概念 | parent | 出现在 | 形态变化 |
|---|---|---|---|---|
| `user` | 用户 | | ① ③ | 方框 → 方框 |
| `online-search` | 在线检索 | | ① ③ | ① 方框 → ③ 分组框 |
| `offline-build` | 离线建库 | | ① ② | ① 方框 → ② 分组框 |
| `data-sources` | 数据源 | | ① ② | ① 一个方框 → ② 拆成三个来源 |
| `index-store` | 索引存储 | | ① ② ③ | ① 一个方框 → ②③ 拆成三个库 |
| `site` · `partner-feed` · `open-api` | 目标网站 · 合作方 Feed · 开放 API | `data-sources` | ② | 从「数据源」拆出 |
| `url-queue` | URL 抓取队列 | `offline-build` | ② | 画在分组框外，显式写 parent |
| `crawler` · `parser` · `dedup` · `indexer` | 爬虫 · 解析抽取 · 去重清洗 · 建索引 | `offline-build` | ② | 画在分组框内，parent 自动推断 |
| `query-understanding` · `recall` · `ranking` · `assembly` | Query 理解 · 多路召回 · 排序 · 结果组装 | `online-search` | ③ | 画在分组框内，parent 自动推断 |
| `embedding-model` · `ranking-model` | Embedding 模型 · 排序模型 | | ③ | 只在 ③ 出现 |
| `inverted-index` · `forward-store` · `vector-store` | 倒排索引 · 正排库 · 向量库 | `index-store` | ② ③ | 从「索引存储」拆出；②③ 之间同 id 直接变形 |
