# 许可证说明

本项目采用**分开授权**：文档与规则用 CC BY 4.0，代码用 MIT。

| 许可 | 适用文件 | 正文 |
|---|---|---|
| **CC BY 4.0** | 除 `scripts/` 外的全部内容 | [`LICENSE-DOCS`](LICENSE-DOCS) |
| **MIT** | `scripts/due_review.py`、`scripts/backup_data.py` | [`LICENSE-CODE`](LICENSE-CODE) |

版权所有者：**99999vvain**（2026）

> **发布状态**：授权文本与内容来源说明（第四节）均已就位，维护者已于 2026-10-22 确认来源。
> 仓库已建立并推送至 https://github.com/99999vvain/kaoyan-calculus-learning-cycle，**当前为私有**；转为公开由维护者决定（计划在第三方实装测试完成后）。

---

## 一、覆盖范围（逐文件对应）

| 文件 / 目录 | 许可 |
|---|---|
| `SKILL.md` | CC BY 4.0 |
| `README.md` | CC BY 4.0 |
| `CONTRIBUTING.md` | CC BY 4.0 |
| `TESTING.md` | CC BY 4.0 |
| `CHANGELOG.md` | CC BY 4.0 |
| `LICENSE.md`（本文件） | CC BY 4.0 |
| `LICENSE-DOCS` | CC BY 4.0 |
| `docs/LIMITATIONS.md` | CC BY 4.0 |
| `references/` 下全部 8 个 `.md` | CC BY 4.0 |
| `assets/snapshot-template.md` | CC BY 4.0 |
| `assets/templates/` 下 4 个 `.md` | CC BY 4.0 |
| `scripts/due_review.py` | MIT |
| `scripts/backup_data.py` | MIT |
| `LICENSE-CODE` | MIT |
| `.gitignore`、`.gitattributes` | 不单独授权（无著作性内容） |

## 二、为什么 CC BY 4.0 的正文是"声明 + 链接"

`LICENSE-CODE` 里是 MIT 的**完整原文**——它足够短，可以逐字内置，不会有偏差。

`LICENSE-DOCS` 里没有内嵌 CC BY 4.0 的完整法律文本（约 7000 词），只给了规范声明、必须遵守的条件、以及指向官方法律文本的固定链接。原因是：**手抄一份长法律文本，抄错一个词就是新问题**。Creative Commons 官方认可用"声明 + 链接"的方式标注许可状态，链接指向的 `legalcode` 才是唯一权威版本。

代价：GitHub 的自动许可识别可能无法把本仓库标为 "CC BY 4.0"。如果你希望出现那个徽标，可以把 `LICENSE-DOCS` 换成官方全文（仓库体积约增加 40KB）。这只是取舍，不影响授权效力。

## 三、署名要求

CC BY 4.0 要求署名（BY）。复用或改编时，请照 `LICENSE-DOCS` 末尾的格式标注：

```
基于「考研高数学习闭环 / Kaoyan-Calculus-Learning-Cycle」
（作者 99999vvain，许可 CC BY 4.0，原仓库 https://github.com/99999vvain/kaoyan-calculus-learning-cycle）改编，并作出了修改。
```

**不得暗示原作者为你的使用行为背书。** 这一点在许可文本里有明文。

## 四、内容来源与权属说明

本节是**事实说明**，不是待办事项。维护者已就下列四项作出确认（2026-10-22）。

| 内容 | 来源 | 权属判断 |
|---|---|---|
| `SKILL.md`、`references/` 下的规则文本 | 维护者定方向、逐条讨论与验收，AI 起草成文 | 维护者所有 |
| `references/knowledge-map.md` | 八章骨架对应公开考纲板块（公开体例，无独创性）；99 个知识点的拆分、`K-章.节.序` 编号、前置依赖、「数一要求」等级由 AI 生成 | 本项目自拟，无第三方来源可对照 |
| `scripts/due_review.py`、`scripts/backup_data.py` | AI 编写，仅用 Python 标准库，无引入第三方代码 | 维护者所有 |
| `README.md`、`TESTING.md`、`CONTRIBUTING.md`、`CHANGELOG.md`、`docs/`、`assets/` 模板 | AI 起草，维护者验收 | 维护者所有 |

**明确排除在仓库之外的**：课程讲义原文与截图、教材摘录、角色设定图。这三样不随本项目发布，因此不在授权范围内。

**两个必须保留的限定**：

1. `knowledge-map.md` **不是官方大纲的转录**，也未逐条对照大纲原文校核；它没有从任何讲义的目录结构搬来。准确度按"未经整体校核的草稿"对待，而非"权威考点清单"。
2. "AI 参与生成"是**披露**问题，不是**授权**问题。版权与最终责任在维护者本人；声明 AI 参与，是为了让复用者知道内容的实际来历，不改变许可效力。

结论：本仓库所含内容不含第三方享有著作权的材料，维护者有权按 `LICENSE-DOCS` / `LICENSE-CODE` 授权。

---

## 附：三个容易混淆的点

1. **MIT 和 CC BY 4.0 都不禁止商业使用。** 想让别人不能拿去卖，这两份许可都做不到。标准开放许可里没有"禁止商用"这一档。
2. **"非商用"自定义条款通常不被认可为开放许可。** 一旦写进仓库，GitHub 的许可识别、各类开放内容清单、部分平台的收录都会受影响。
3. **本项目选了许可，不等于第三方材料自动获得授权。** 这是两件事。所以角色图和讲义才被排除在外。
