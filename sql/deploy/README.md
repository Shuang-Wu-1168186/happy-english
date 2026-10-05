# 阿里云 MySQL 发布包（2026-10-05）

这个目录用于把当前 Happy English 后端发布到已有的阿里云 RDS for MySQL。发布包按稳定业务编码同步课程内容，不使用本地自增 ID，因此不会把本地用户、密码、学习进度或登录审计带到线上。

线上 RDS 的实际连接信息不在当前工作区，所以无法直接比较它的每一行数据。`20261005_aliyun_preflight.sql` 会在目标库中输出真实的表、列和旧结构状态；本地已核对的当前目标结构和内容基线在下方列出。

## 当前本地基线

| 对象 | 数量 |
| --- | ---: |
| 学习模块 | 6 |
| 学习专题 | 16 |
| 渲染模板 | 8 |
| 教材 | 84 |
| 课程 | 74 |
| 课时 | 2,527 |
| 通用课时区块 | 13,825 |
| 通用课时条目 | 22,955 |
| 课件区块 | 7,767 |
| 课件来源快照 | 38,149 |
| 会员方案 / 权益 | 3 / 2 |

课程内容同步包含旅游英语、购物英语、软件开发职场英语和地铁通勤英语。通勤专题在当前库中有 13 门课程和 92 节课。

已清理一个没有课程、教材或课时的重复空专题：`beginner-english / travel-english`。真实的旅游英语位于 `intermediate-english / travel-english`，发布脚本也会用严格条件清理线上同一遗留项。

## 相对旧阿里云库的已知数据库差异

| 范围 | 变更 |
| --- | --- |
| 账户 | 新增 `login_audit`；`user.contact_number` 需要唯一索引，供小程序手机号登录使用。 |
| 学习目录 | 新增模块、专题、课程、教材、教材课时以及学习进度表。 |
| 课程和教材 | `learning_course` 不再直接存 `topic_id`，改用 `learning_topic_course`；`learning_material` 不再直接存 `topic_id`，改用 `learning_course_material`。 |
| 模板 | 新增 `learning_template` 和 `learning_material.template_id`；新增 `commute` 结构化通勤模板。 |
| 课时正文 | 新增 `learning_lesson_section`、`learning_lesson_item`；课时新增 `lesson_format`、`lesson_schema_version`、`content_status`、`published_at`。 |
| 课件 | 新增 `courseware_block` 和 `courseware_block_source`。 |
| 通勤配图 | `learning_material_lesson` 新增 `illustration_url`。 |
| 笔记筛选 | `english_note_item` 新增语体、场景、标注原因、置信度和来源字段。 |
| 旧日常口语表 | `daily_spoken_dialogue_item` 和 `learning_lesson_item_source` 只在最终清理阶段删除；新代码已从通用课时表读取内容。 |
| 已知内容清理 | 删除无引用的空 `beginner-english / travel-english` 重复专题；保留有 10 门课程的 `intermediate-english / travel-english`。 |

本地还有一张空的 `daily_spoken_dialogue_item_import_check` 表，它只是旧导入过程的检查残留，不是应用模型的一部分，也**不应**发布到阿里云。

日志、Kokoro/Whisper 配置、课程前端页面和接口改动不需要数据库结构变更。

## 文件与执行顺序

1. 先在阿里云目标库执行只读预检：

   ```sh
   mysql --default-character-set=utf8mb4 -h "$MYSQL_HOST" -P 3306 -u "$MYSQL_USER" -p "$MYSQL_DATABASE" \
     < sql/deploy/20261005_aliyun_preflight.sql
   ```

2. 完整备份线上数据库。生产库已有数据时，使用 RDS 备份或 `mysqldump --single-transaction --routines --triggers`；不要用本地开发库直接覆盖线上库。

3. 将本目录、`sql/` 下的增量脚本和 `20261005_learning_catalog_data.sql` 一起上传到服务器，设置连接环境变量后执行：

   ```sh
   export MYSQL_HOST='your-rds-endpoint'
   export MYSQL_USER='your-release-user'
   export MYSQL_DATABASE='happy_english'
   export MYSQL_PWD='your-password'
   ./sql/deploy/20261005_aliyun_schema_release.sh
   ```

   该脚本会建立 `app_schema_migration` 发布账本，先识别目标库是旧结构还是当前结构，只执行仍需要的历史迁移，再同步当前学习目录和会员配置，并执行发布后检查。重复执行时会跳过已记录的阶段。若要重新覆盖当前课程配置，追加 `--force-content`。

4. 部署后端和前端，验证健康检查、登录、课程列表、课程详情和通勤页面。确认无误后再清理已不再被代码读取的旧表：

   ```sh
   ./sql/deploy/20261005_aliyun_schema_release.sh --finalize
   ```

5. 如需单独复查，执行：

   ```sh
   mysql --default-character-set=utf8mb4 -h "$MYSQL_HOST" -P 3306 -u "$MYSQL_USER" -p "$MYSQL_DATABASE" \
     < sql/deploy/20261005_aliyun_postflight.sql
   ```

## 内容同步的边界

`20261005_learning_catalog_data.sql` 是由 `scripts/export_aliyun_learning_catalog.py` 从本地 MySQL 生成的 82 MB 同步脚本。它会更新课程、教材、课时、通用区块、课件区块、模板和会员访问配置；并且只在这些课程范围内重建课程关系及课时子内容。

它明确不导出以下运行期或隐私数据：`user`、`login_audit`、`learning_progress`、`learning_progress_item`、`learning_study_session`、`user_membership`、`learning_user_course`。

部分旧课时仍通过 `source_resource` 指向英文笔记、课本、儿童卡片等基础内容表。已有阿里云旧库会保留这些表和记录。若部署到一个全新的空 RDS，先导入可信的基础库备份或按旧数据导入脚本建立这些基础内容，再运行本发布包；不能只导入课程同步脚本。

## 静态资源不是数据库内容

数据库中的 URL 依赖 `data/static`。本地该目录约 1.2 GB，需单独同步到服务器/Nginx 的 `/static/` 根目录。通勤课时所需的 SVG 位于 `assets/illustrations/commute/`，发布时必须复制到 `data/static/commute-covers/`，否则数据库记录虽然存在，课程配图仍会 404。

## 可再生成内容脚本

当课程内容继续变化时，在连接到确认无误的本地内容库后重新生成，并一并提交新的 SQL 与 manifest：

```sh
PYTHONPATH=. .venv/bin/python scripts/export_aliyun_learning_catalog.py
```

生成后的哈希和行数记录在 `20261005_learning_catalog_manifest.json` 中。不要手改 82 MB 的生成 SQL；修改内容后重新生成即可。
