# 通用课时内容结构

`learning_material_lesson` 继续作为课时主表。课时正文统一保存在以下层级中：

```text
learning_material_lesson
  └── learning_lesson_section
        └── learning_lesson_item
```

## 固定区块

每节完整课时发布时必须包含以下七个区块：

| section_code | 内容 | 数量 |
| --- | --- | ---: |
| `core_vocabulary` | Core Vocabulary 核心词汇 | 4–6 |
| `situational_dialogues` | Situational Dialogues 情景对话 | 6–8 组 |
| `key_sentence_patterns` | Key Sentence Patterns 核心句型 | 3–5 |
| `speaking_practice` | Speaking Practice 口语练习 | 至少 1 |
| `mini_exercises` | Mini Exercises 小练习 | 至少 1 |
| `useful_tips` | Useful Tips 实用表达提示 | 至少 1 |
| `extended_reading` | Extended Reading 扩展阅读 | 至少 1 |

每个 `learning_lesson_item.payload_json` 按区块类型保存内容。数据库只负责保存和排序，后端负责按 `section_code` 校验 JSON 结构及数量。情景对话中一条 item 代表一组对话，具体对话轮次放在该 item 的 payload 内。

## 编辑和发布

管理员可以先保存草稿：

```text
PUT /api/admin/learning-material-lessons/{lesson_id}/sections
```

满足七个区块和数量规则后发布：

```text
POST /api/admin/learning-material-lessons/{lesson_id}/publish
```

学习端课时详情统一返回 `sections` 和 `render_payload.content.sections`。旧课时没有新区块时继续走原有来源兼容逻辑，方便分批迁移。

## 首批迁移

`scripts/migrate_dialogue_and_idiomatic_lessons.py` 已将日常口语对话和地道英语系列导入通用表。日常口语的 95 节课已切换为 `lesson_format='structured'`。地道英语日积月累系列保留 `courseware` 渲染和现有前端展示。

```sh
.venv/bin/python scripts/migrate_dialogue_and_idiomatic_lessons.py
.venv/bin/python scripts/migrate_dialogue_and_idiomatic_lessons.py --apply
```

脚本默认跳过已迁移课时；只有显式传入 `--replace --apply` 才会替换该范围内已有的通用区块。

## 日常口语旧表下线

在部署移除旧 `dialogues` API 读取逻辑的版本后，执行
`sql/20260928_drop_daily_spoken_dialogue_item.sql`。脚本会先确认没有课程继续使用
`dialogues`、所有日常口语课时都已切换为结构化内容并已有新区块，然后清除课时主表的旧来源引用，最后删除 `daily_spoken_dialogue_item`。
