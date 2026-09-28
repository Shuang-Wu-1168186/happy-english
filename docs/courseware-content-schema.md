# 面向课件的内容模型建议

## 目标

`english_note_item` 继续保存原始学习笔记，不把它改造成页面布局表。以 `put aside`（`english_note_item.id = 1514`）为例，一条卡片中的 `raw_text`、`chinese_text`、`explanation` 与 `examples` 是可追溯的内容来源；课件负责把这些来源编排成“记忆画面、三种用法、情景对话、对比、输出练习、回顾”等可学习的区块。

现有的 `learning_material`、`learning_material_lesson` 和 `learning_course` 已经解决了教材目录、课时、课程权限和学习进度问题。建议在 `learning_material_lesson` 下增加课件区块，而不是新建另一套课程、教材或课时主表。

```text
learning_course ──< learning_course_material >── learning_material → learning_material_lesson
                                                                         │
                                                                         ├── courseware_block
                                                                         │       └── courseware_block_source
                                                                         │
english_note / english_note_item ───────────────────────────────────────┘
```

这样，课程、会员权益、试看和进度仍按现有课时工作；课件只负责该课时如何呈现。

## 三层职责

| 层级     | 使用现有表或新表                              | 负责什么                                             |
| -------- | --------------------------------------------- | ---------------------------------------------------- |
| 原始内容 | `english_note_item`                           | 保存笔记原文及其来源，不因页面版式而重复或拆散。     |
| 课时目录 | `learning_material_lesson`                    | 标题、排序、发布和所属教材。                         |
| 课件编排 | `courseware_block`、`courseware_block_source` | 定义学习顺序、区块类型、页面数据和每段文本从哪里来。 |

对于视觉和教学方式会持续变化的内容，不建议为“对话第几句”“三个释义的第几张卡”等各自建表。把可查询、可排序、要关联的字段放在列中；一个区块内部的句子、角色、强调词、填空位置等放进 `payload_json`。前端按 `block_type` 渲染，后台保存时按该类型校验 JSON 结构。

## 对现有课时表的最小扩展

增加一个用于选择前端渲染方式的字段。原有课时默认 `source`，不改变已有接口行为；新课件课时使用 `courseware`。

```sql
ALTER TABLE `learning_material_lesson`
    ADD COLUMN `lesson_format` VARCHAR(50) NOT NULL DEFAULT 'source'
        COMMENT 'source：按既有内容表读取；courseware：按课件区块读取'
        AFTER `content_json`,
    ADD KEY `idx_learning_material_lesson_format`
        (`lesson_format`, `is_published`);
```

`content_json` 可以保留给旧的自包含课时，不应同时承载新的可编辑课件正文。新课件正文放在下方区块表中，避免一次修改整段 JSON，也能独立排序和追溯来源。

## 新表

### `courseware_block`

每一行是课时中的一个教学区块。`block_code` 是稳定标识，供进度、埋点和前端定位使用；`block_type` 决定前端读取 `payload_json` 的方式。

```sql
CREATE TABLE `courseware_block` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '课件区块主键ID',
    `material_lesson_id` BIGINT UNSIGNED NOT NULL COMMENT '所属教材课时ID',
    `block_code` VARCHAR(120) NOT NULL COMMENT '课时内稳定区块编码',
    `block_type` VARCHAR(50) NOT NULL COMMENT 'hero、usage_group、dialogue、comparison、output、recap 等',
    `title` VARCHAR(255) DEFAULT NULL COMMENT '区块标题；为空时由前端按类型决定是否显示',
    `payload_json` LONGTEXT NOT NULL COMMENT '按 block_type 校验的课件内容 JSON',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '课时内排序',
    `status` VARCHAR(20) NOT NULL DEFAULT 'draft' COMMENT 'draft、published、archived',
    `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建管理员ID',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '最后修改管理员ID',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',

    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_courseware_block_lesson_code` (`material_lesson_id`, `block_code`),
    KEY `idx_courseware_block_lesson_status_order`
        (`material_lesson_id`, `status`, `sort_order`),
    CONSTRAINT `fk_courseware_block_lesson`
        FOREIGN KEY (`material_lesson_id`) REFERENCES `learning_material_lesson` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_courseware_block_created_by`
        FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
    CONSTRAINT `fk_courseware_block_updated_by`
        FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课件教学区块表';
```

`block_type` 建议先固定为以下有限集合，并在服务层对每类 JSON 做校验：

| `block_type`  | 用途                                   | 典型 `payload_json`                                        |
| ------------- | -------------------------------------- | ---------------------------------------------------------- |
| `hero`        | 课件首屏、核心短语、核心释义、记忆线索 | `phrase`、`meaning`、`memory`、`key_sentence`              |
| `usage_group` | 一个或多个含义及例句                   | `uses[]`，每项含 `title`、`examples[]`                     |
| `dialogue`    | 情景对话                               | `scene`、`lines[]`，每行含 `speaker`、`english`、`chinese` |
| `comparison`  | 易混表达比较                           | `items[]`，含表达、语气、例句                              |
| `output`      | 跟读、替换、填空或造句                 | `patterns[]`、`instruction`                                |
| `recap`       | 最后回顾和关键句                       | `summary`、`key_sentence`                                  |

`dialogue` 必须呈现一个具体的真实情境：第一句交代人物正在面对的事件、地点或后果，第二句要自然回应并推进该事件。不能用“发生了什么？”、“这个词是什么意思？”或“这个词指……”这类释义问答充当情景对话；释义应留在首屏或用法卡，情景卡只保留人在真实场景中的交流。

例如，`put aside` 的通用协作场景对话区块可以保存为：

```json
{
  "scene": "情景练习",
  "lines": [
    {
      "speaker": "人物 A",
      "english": "Let’s put that discussion aside for now.",
      "chinese": "那件事我们现在先放一放。"
    },
    {
      "speaker": "人物 B",
      "english": "Good idea. We can put aside some time tomorrow.",
      "chinese": "好主意。我们明天可以留出一些时间。"
    }
  ]
}
```

### `courseware_block_source`

一段课件可能来自同一张笔记卡的不同字段，也可能未来来自课文、对话或题库。此表记录每个区块使用的原始片段及其快照，避免原始笔记被修改后无法还原已经发布的课件。

```sql
CREATE TABLE `courseware_block_source` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '课件区块来源主键ID',
    `courseware_block_id` BIGINT UNSIGNED NOT NULL COMMENT '所属课件区块ID',
    `source_resource` VARCHAR(80) NOT NULL COMMENT '来源类型，例如 english_note_item、dialogue_line',
    `source_reference_id` BIGINT UNSIGNED NOT NULL COMMENT '来源记录主键ID',
    `source_field` VARCHAR(80) NOT NULL COMMENT '来源字段，例如 raw_text、explanation、examples',
    `source_locator_json` LONGTEXT DEFAULT NULL COMMENT '字段内定位信息，如标题、句子或数组下标',
    `source_snapshot_text` MEDIUMTEXT NOT NULL COMMENT '发布时使用的原文快照',
    `source_hash` CHAR(64) DEFAULT NULL COMMENT '原文快照 SHA-256，用于变更检测',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '同一课件区块内的来源顺序',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',

    PRIMARY KEY (`id`),
    KEY `idx_courseware_block_source_block_order`
        (`courseware_block_id`, `sort_order`),
    KEY `idx_courseware_block_source_reference`
        (`source_resource`, `source_reference_id`, `source_field`),
    CONSTRAINT `fk_courseware_block_source_block`
        FOREIGN KEY (`courseware_block_id`) REFERENCES `courseware_block` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课件区块内容来源表';
```

这里使用 `source_resource + source_reference_id`，与现有 `learning_material_lesson` 的多态来源方式一致，因此不能建立统一外键；服务层在保存时校验来源记录存在且有权限读取。对学习笔记，来源可写为 `english_note_item:1514`，并保存字段名和实际使用的原文片段。

## `put aside` 的落库方式

课时头仍是已有的 `learning_material_lesson`：

```text
lesson_code: phrase-put-aside
title: put aside
source_resource: notes
source_reference_id: 21
lesson_format: courseware
```

然后创建以下区块及来源映射：

| `block_code`         | `block_type`  | 来自 `english_note_item.id = 1514` 的字段                     |
| -------------------- | ------------- | ------------------------------------------------------------- |
| `hero`               | `hero`        | `raw_text`、`chinese_text`、`examples` 中的记忆法和一句话记忆 |
| `three-uses`         | `usage_group` | `explanation` 中的三段用法和对应例句                          |
| `scene-dialogue`     | `dialogue`    | 从各项核心用法选出的通用情景例句                              |
| `put-vs-set-aside`   | `comparison`  | `examples` 中的对比说明和两句例句                             |
| `say-it`             | `output`      | 从原有例句抽取出的可替换句型                                  |
| `recap`              | `recap`       | `examples` 中的“一句话记”                                     |

静态样稿中的所有英语、中文释义和例句都可以在这些来源快照中找到。诸如“同事 A / B”、区块标题和空格样式属于课件编排元数据，不作为新的词义或例句写入原始笔记。

## 发布和编辑流程

1. 管理员选择一个 `english_note_item`，系统提取原文字段，生成草稿区块和来源快照。
2. 管理员在区块编辑器中调整排序、选择要展示的原句、为对话指定角色、配置填空位置。
3. 服务端校验每个面向学习者的原文片段都有 `courseware_block_source`，并对 `payload_json` 按区块类型校验。
4. 发布时将所有区块切为 `published`，再将 `learning_material_lesson.is_published` 置为 `1`。学习端只读取已发布区块。
5. 原笔记以后修改时，按 `source_hash` 标记“来源已变更”；管理员选择重新生成草稿或保留已发布快照，不会静默改写课件。

批量整理一份笔记时，可先创建目标教材，再逐条调用 `POST /api/admin/courseware/from-note-item`。请求中的 `material_id` 为可选字段；传入后，课时会写入该教材，并校验该教材属于所选专题。例如可把同一专题下的不同月份分别放入“地道英语日积月累【8月】”“地道英语日积月累【9月】”等教材，避免混入同一个课时目录。

当一个笔记词条的 `english_text` 用 `/` 或 `|` 并列多个独立表达，且原笔记逐项提供了中文释义（可以是 `表达 = 中文释义`，也可以是“中文场景标题 + 对应表达”的分组）时，预览和生成会自动拆为多个课时。例如 `scraggly / scraggle / straggly` 会生成三条独立课时，而不是一张合并卡片。每条课时仍引用同一个 `english_note_item`，并在 `courseware_block_source.source_locator_json` 记录拆分后的表达和位置。

没有足够逐项释义的并列表达不会再生成一张合并卡，预览和生成会返回 `422`，提示先拆分笔记或补齐逐项释义。可运行 `scripts/audit_courseware_multi_expression_entries.py --apply` 清理已生成的历史课时：能可靠拆分的会重建成独立课时，单词后的 IPA 音标会从标题移除，无法可靠拆分的合集课时会从教材中移除；原始笔记不会删除。

## 专题维护管理

专题对应 `learning_topic`，用于组织教材、课程和课件课时。后台管理接口提供以下能力：

| 操作 | 接口 | 说明 |
| ---- | ---- | ---- |
| 分页查询 | `GET /api/admin/learning-topics` | 支持 `q`、`module_id`、`is_published`、`page`、`page_size`；每项带教材、课时和课程的发布统计。 |
| 查看详情 | `GET /api/admin/learning-topics/{topic_id}` | 返回专题、教材、课程和统计，供课程管理窗口展示；课程带 `materials`、`material_ids` 与兼容字段 `material_title`，用于显示关联教材。 |
| 新建／编辑 | `POST /api/admin/learning/topics`、`PUT /api/admin/learning/topics/{topic_id}` | 维护所属学习区域、稳定编码、标题、简介、封面、排序与发布状态。 |
| 关联课程 | `POST /api/admin/learning-topics/{topic_id}/courses` | 从课程库选择已有课程并写入 `learning_topic_course` 映射；同一课程可关联多个专题，此操作不会新建课程。 |
| 保存课程顺序 | `PUT /api/admin/learning-topics/{topic_id}/course-order` | 请求体为 `{ "course_ids": [课程 ID, ...] }`，必须完整且不重复地提交该专题的全部课程；系统按提交顺序写入课程排序。 |
| 解除课程关联 | `DELETE /api/admin/learning-topics/{topic_id}/courses/{course_id}` | 只删除该专题与课程的映射；课程、教材、课时和其他专题关联都会保留。 |
| 学习端专题详情 | `GET /api/learning/topics/{topic_id}` | 返回的 `courses` 按 `sort_order`、`id` 排序；Web 和小程序都按该顺序展示专题下的课程。 |
| 快速上下架 | `PUT /api/admin/learning/topics/{topic_id}/publication` | 请求体为 `{ "is_published": 0 或 1 }`。 |
| 删除 | `DELETE /api/admin/learning/topics/{topic_id}` | 专题下仍有教材或课程时返回 `409`，避免误删内容。 |

管理端在 `happy-english-ui` 的“内容管理”菜单下提供“专题维护”入口（前端路由为 `/admin/content/topics`，兼容 `/admin/learning/topics`）。专题列表的操作区提供“课程管理”：可在窗口中从课程库关联已有课程，拖住课程左侧手柄调整该专题内的课程顺序。课程表本身不保存专题 ID；课程的创建和教材配置仍在“课程开发”中完成。保存排序后，学习端专题目录和课程列表会立即按专题映射顺序展示。`GET /api/admin/management-menu` 同步返回该菜单信息。前端页面仅允许管理员访问，并调用上述管理 API 完成筛选、新建、编辑、课程管理、发布、下架和删除。

“课程管理”窗口中将鼠标悬浮在课程上即可显示“移除”操作。确认后只解除该课程与当前专题的关联，不会删除课程、教材、课时或该课程在其他专题中的关联。

## 教材开发、课程开发与访问策略

管理端的“内容管理”菜单分成两个前端开发页面，页面代码位于 `happy-english-ui`；本服务只提供其调用的 API：

- **教材开发**（`/admin/content/materials`，兼容前端路由为 `/admin/learning/materials`）维护 `learning_material`，并在同一页面的“课时开发”窗口中为一本教材新增、编辑、排序、发布或删除多个 `learning_material_lesson`。
- **课程开发**（`/admin/content/courses`，兼容前端路由为 `/admin/learning/courses`）维护 `learning_course`。课程创建时不绑定专题，只配置课程自身和教材；之后在“专题维护”中通过 `learning_topic_course` 关联已有课程。编辑课程时可多选整本教材，系统将课程内教材顺序写入 `learning_course_material.sort_order`；学习端按这个顺序串联各教材的课时。

同一系列的月份内容应保留为多本教材、一个课程。例如“地道英语日积月累”只保留一条 `learning_course` 记录，按月份通过 `learning_course_material` 关联“地道英语日积月累【2025年3月】”至后续各月教材；不再为每本教材创建重复课程。

课程是否免费在“课程开发”的“是否免费”字段设置，对应 `learning_course.access_policy`：

- `free`：免费学习，登录学习者可直接学习。
- `benefit`：需要有效会员权益；保存后还要在会员管理的“课程权益绑定”中将该课程加入相应权益。

课件首次从笔记生成时会新建一门默认免费的课程。以后重新生成同一教材的课件会更新课时和课程基础信息，但保留管理员已经选择的访问策略，避免把会员课意外改回免费。

这套设计不需要改动现有课程、会员权益或学习进度表。等样稿确认后，再补充迁移 SQL、SQLAlchemy 模型、后台区块编辑接口和学习端渲染器即可。
