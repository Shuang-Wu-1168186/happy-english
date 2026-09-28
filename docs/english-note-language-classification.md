# 学习笔记语体与场景标注

范围：`english_note_item` 的 1,588 条现有词条。

本次标注基于卡片原有的英文内容、中文讲解、例句和关键词。`常用口语`表示适合自然对话使用，**不表示外部语料库中的全球频率排名**；单独词汇或术语没有足够语境时会保留为“中性表达”或“术语/知识点”，避免把它们误说成口语或书面语。

| 语体 | 条数 | 占比 | 使用含义 |
| --- | ---: | ---: | --- |
| 常用口语 | 1,021 | 64.3% | 日常对话、自然短语、缩略形式和非正式表达 |
| 正式口语 | 58 | 3.7% | 礼貌请求、会议、面试、客户和商务沟通 |
| 书面语 | 14 | 0.9% | 报告、学术、法律、政策和正式写作 |
| 多语体对照 | 90 | 5.7% | 一张卡同时比较日常、正式或书面替代说法 |
| 中性表达 | 362 | 22.8% | 单词本身可用于口语和书面语 |
| 术语/知识点 | 43 | 2.7% | 语法、专业词汇或需要看搭配的知识卡 |

例如，`gonna`、`run around`、`show up` 会归为常用口语；礼貌请求和会议表达会归为正式口语；`hence`、`retrieve`、`conversely` 会归为书面语；`enough / sufficient` 这类比较卡会归为多语体对照。

每条卡片还带有一个到三个适用场景标签。现有标签覆盖最多的是日常生活（610）、职场沟通（352）、技术沟通（253）、报告写作（167）、客户服务（142）、会议/演示（124）、朋友社交（86）和求职面试（74）。同一张卡可以同时适用于例如“会议/演示”和“职场沟通”。

## 数据字段

`english_note_item` 新增以下字段：

| 字段 | 含义 |
| --- | --- |
| `language_register` | `common_spoken`、`formal_spoken`、`written`、`mixed`、`neutral`、`reference` |
| `usage_scenarios_json` | 适用场景编码的 JSON 数组 |
| `register_reason` | 简短的中文判断说明 |
| `classification_confidence` | 自动判断置信度，0–100 |
| `classification_source` | `auto_rule_v1` 或 `manual` |

接口支持按语体和场景查询：

```text
GET /api/content/note-items?language_register=common_spoken
GET /api/content/note-items?scenario=meeting_presentation
```

Web 学习笔记页可以按语体筛选，卡片会显示语体和场景标签。小程序卡片也会显示相同标签。后台编辑学习笔记卡片时可修改语体、场景和判断说明；保存人工修改后，`classification_source` 会变为 `manual`，后续自动重跑不会覆盖它。

## 发布顺序

先执行结构迁移，再执行标注数据迁移：

```bash
mysql happy_english < sql/20260926_classify_english_note_items.sql
mysql happy_english < sql/20260926_seed_english_note_item_language_labels.sql
```

`scripts/classify_english_note_items.py` 是可重复运行的分类器。它默认只输出统计；加 `--apply` 会写入当前数据库，加 `--write-sql <path>` 会生成可发布的数据迁移文件。除非显式添加 `--overwrite`，它会保留人工标注。
