# <领域名> 概念 → 颜色字典

<!--
  新领域的可复用字典模板。和 diagram-binding.md 的区别:
  - 字典 (本文件) = 一个领域的通用约定, 跨文章复用, 放进 references/domains/。
  - 绑定表 (diagram-binding.md) = 一个系列配图的具体锁定, 只服务这一组图, 放在工作目录。
  填写规则:
  - 只从 references/palette.md 的 9 个 slot 里选, 按"抽象语义"列对应, 不新增颜色。
  - 一个类别一个 slot; 同类别内的子概念用形状区分, 不拆颜色。
  - 填好的例子: references/domains/agent-team.md, references/domains/vertical-search.md
-->

适用：<哪类文章 / 系统的配图>。

## 主表

| 颜色 slot | 本领域类别 | 常见别名 (alias) | 默认 shape |
|---|---|---|---|
| **`C.<slot>`** <色名> | <类别> | <别名 · 别名> | Box |

## 形状二级区分（同色下用 shape 拆子类）

| slot | 子概念 | shape | 说明 |
|---|---|---|---|
| `C.<slot>` | <子概念> | <shape> | <为什么用这个形状> |

## 决策树 · 拿到一个名词怎么定色

```
是不是 <类别 A 的判断条件>?
  └ Yes → C.<slot>
  └ No
是不是 <类别 B 的判断条件>?
  └ Yes → C.<slot>
  └ No
...
实在归不到? → 优先合并到最近的 slot, 不要开新色; 或者改用形状区分。
```

## 互斥规则

1. **<概念 X> ≠ <概念 Y>**——<各自归属和理由>。

## 系列配图色覆盖建议

| 图 | 主题 | 颜色 | 关键 shape |
|---|---|---|---|
| 1 | <总览> | <slot / slot> | <shape> |
