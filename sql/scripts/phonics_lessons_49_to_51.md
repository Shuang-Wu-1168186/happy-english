# 自然拼读第 49—51 讲提取说明

导入文件：[aliyun_phonics_lessons_49_to_51.sql](aliyun_phonics_lessons_49_to_51.sql)。

依据项目 `video/49.mp4`、`video/50.mp4`、`video/51.mp4` 的课件画面和本地语音转写整理，沿用当前 MySQL `phonics_lesson` 表结构。现有 21 条课程为第 28—48 讲，`priority_order` 为 1—21；本次新增课程使用 22—24，不指定自增 ID。

本文件是课程内容摘要，不是逐字字幕。画面中的单词拼写经人工核对；自动转写中的 `why`、`ran`、`bagger`、`中毒音节` 等误识别分别按画面及语境校正为 `y`、`rain`、`beggar`、`重读音节`。未将片尾学习群推广纳入课程。

## 字段对应

| 字段 | 整理方式 |
| --- | --- |
| `lesson_code` | 沿用现有语义命名方式，新增三个唯一代码 |
| `title`、`subtitle` | 概括主题，并保留视频讲次 |
| `pattern_text`、`sound_text` | 总结发音规律和口型提示 |
| `learning_tip` | 整理讲解、重弱读区别、课后拼读和视频例句 |
| `review_examples_json` | 开头复习或引入例词，沿用前端 WARM UP 区域；无则为 NULL |
| `examples_json` | 本课讲解及自主拼读例词，按首次出现顺序排列 |
| 例词 JSON | 仅包含现有的 `word`、`focus`、`sound` 键 |
| `quiz_*` | 根据本课内容新编一道单选题，不冒充视频原题 |
| `priority_order`、`is_active` | 排在已有第 48 讲之后；导入后启用 |

音标是整理时补充的宽式 IPA，不是逐帧抄录或自动转写结果。采用美式读法，与第 51 讲明确说明的美式示范一致；保留 /r/，弱读 /ər/ 与常见的 /ɚ/ 记法对应。`party`、`waiter` 中 /t/ 的美式闪音属于实际语音变体，此处不另用窄式符号表示。规则描述限定于视频展示的情形，不表示所有含相同字母的单词都没有例外。

## 第 49 讲：弱读词尾 y

- 文件：`video/49.mp4`，时长约 07:22。
- 代码：`weak-final-y`；排序：22。
- 规律：非重读音节的词尾 `y` 通常读 /i/；与词首 `y` 的 /j/ 对比。
- 技巧：咧开嘴角，突出前面的重读音节，词尾轻而干脆。

| 视频位置（约） | 内容 |
| --- | --- |
| 00:32—01:07 | 复习 yoga、yes、you |
| 01:17—01:53 | city |
| 01:54—02:29 | lovely |
| 02:31—02:57 | country |
| 02:57—03:50 | 总结词尾、弱读条件及咧开嘴角的技巧 |
| 03:50—04:37 | candy，说明前重后轻的节奏 |
| 04:39—05:29 | sleepy，与 candy 对照 |
| 05:30—06:04 | 自主拼读 happy |
| 06:04—06:27 | 自主拼读 angry；例句 I am very angry. |
| 06:41—07:14 | 总结本课 |

复习 3 词，正文 7 词。新编小测验：从 yes、city、you 中选出词尾 y 读 /i/ 的词，答案 city。

## 第 50 讲：元音组合 ai

- 文件：`video/50.mp4`，时长约 08:34。
- 代码：`ai-long-a`；排序：23。
- 规律：本课重读音节中的 `ai` 作为整体读 /eɪ/。
- 技巧：口型由扁到更扁，声音从 /e/ 滑向 /ɪ/。

| 视频位置（约） | 内容 |
| --- | --- |
| 00:34—01:03 | 引入 tail、brain、paint |
| 01:21—01:45 | 画面列举 Spain、raise、gain、maid、sail、brain、wait、paint、mail、failure |
| 01:47—02:24 | 说明 ai 是元音字母组合 |
| 02:24—02:45 | rain |
| 02:46—03:40 | nail，提示 ai 作为一个整体拼读 |
| 03:40—04:45 | 对比 rain、nail，总结重读条件和口型 |
| 04:46—05:19 | waitress |
| 05:19—06:14 | snail，与 nail 对比 |
| 06:15—06:43 | 自主拼读 waiter |
| 06:43—07:25 | 自主拼读 train；例句 Let's get on the train. |
| 07:47—08:22 | 总结本课 |

开头的例词列表只用于展示 ai 组合，视频说明当时不逐一讲解词义。将这部分放在 WARM UP 区域，并去掉重复的 brain、paint，得到 11 个引入词；正文 6 词。新编小测验：从 city、card、rain 中选出 ai 读 /eɪ/ 的词，答案 rain。

## 第 51 讲：ar 的三种读音

- 文件：`video/51.mp4`，时长约 09:06。
- 代码：`ar-sounds`；排序：24。
- 规律：重读 /ɑːr/，非重读词尾 /ər/，在 war 中读 /ɔːr/。
- 技巧：重读饱满有力，弱读轻声快速、不拖长。视频明确采用美式示范。

| 视频位置（约） | 内容 |
| --- | --- |
| 00:44—02:09 | party；约 00:47 起说明美式读法，并强调重弱读和 r 音 |
| 02:09—02:41 | card |
| 02:41—03:29 | 总结重读 ar |
| 03:35—04:16 | war；指出 w 后的 ar 发音有变化 |
| 04:16—04:33 | 总结“饱满、有力”的发音技巧 |
| 04:45—05:38 | dollar，词尾 ar 弱读 |
| 05:38—06:39 | beggar；强调弱读轻声快速，口头例句 The beggar is begging dollars. |
| 06:39—07:07 | 自主拼读 sugar |
| 07:08—07:53 | 自主拼读 scarf |
| 08:11—08:59 | 总结三种情况 |

正文 7 词，无独立复习词列表。口头例句保存在本说明，避免过长的学习提示；前两课的短例句同时保存在 `learning_tip` 中。新编小测验：从 party、beggar、scarf 中选出非重读词尾 ar 读 /ər/ 的词，答案 beggar。

补充发音参考：[Cambridge sugar 发音](https://dictionary.cambridge.org/pronunciation/english/sugar)、[有道 war 英美音标](https://dict.youdao.com/w/eng/war/)。课件和语音是课程例词及讲解的主要来源。

## 导入与核查

1. 在 IDEA 数据库控制台选择目标数据库。
2. 执行 `aliyun_phonics_lessons_49_to_51.sql`。文件使用 UTF-8 / utf8mb4 和事务。
3. 查询 `lesson_code IN ('weak-final-y', 'ai-long-a', 'ar-sounds')`，应得到 3 条，排序 22、23、24。
4. 刷新自然拼读页面，课程应排在第 48 讲后面。

SQL 使用唯一键 `lesson_code` 更新这三个课程，重复执行不会新增重复课程，但会覆盖这三个代码对应的课程内容。不会删除课程，也不会改表结构。

已在 MySQL 临时表中连续执行 SQL 两次，验证三条课程的所有内容字段一致且没有重复；现有课程表的 21 条数据保持不变。另在隔离 SQLite 中验证了现有 Repository 的 JSON 解析、课程排序和上一篇/下一篇导航。字段长度、34 个例词的 JSON 结构和三道题的选项均通过检查。

本地抽帧与自动转写保存在未纳入 Git 的 `data/phonics-extraction/`，其中 `49-transcript.txt`、`50-transcript.txt`、`51-transcript.txt` 是未经逐字校对的辅助转写，不能直接用作字幕。
