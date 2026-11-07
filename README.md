# happy-english

Happy English 独立后端，使用 **Python 3.12 + FastAPI + SQLAlchemy 2 + MySQL**。前端位于同级 `happy-english-ui`，通过 JSON API 通信。后端不渲染 Jinja 页面，也不依赖原来的 HappyEnglish 目录或前端源码。

## 本机启动

本次迁移已经安装依赖，并将原项目的本地 MySQL 连接配置写入本项目 `.env`，生成了独立会话密钥。数据库结构和已有数据保持原样，可使用原账户登录。

```sh
cd /Users/wushuang/projects/happy-english
sh scripts/dev.sh
```

- API：<http://127.0.0.1:8000/api/health>
- 数据库连接检查：<http://127.0.0.1:8000/api/health/ready>
- Swagger：<http://127.0.0.1:8000/docs>
- 前端：另开终端，在 `../happy-english-ui` 执行 `npm run dev`。

不要在启动时导入 SQL 备份。当前配置直接使用原数据库，所以通过新页面保存、删除内容也会影响原应用读取的数据。

## 在另一台机器安装

```sh
python3.12 -m venv .venv
.venv/bin/pip install -r requirements-lock.txt
cp .env.example .env
# 编辑数据库连接信息，生成 SECRET_KEY：
.venv/bin/python -c 'import secrets; print(secrets.token_hex(32))'
sh scripts/dev.sh
```

基础依赖是 `requirements.txt`，开发依赖是 `requirements-dev.txt`；`requirements-lock.txt` 记录已验证的依赖版本。使用已有 MySQL 8 数据库；如需新建空数据库，可使用 `app.models.metadata.create_all(engine)` 或参考原 SQL 脚本。`sql/` 保存了迁移时复制的旧导出和增量脚本，不会自动执行；部分脚本包含已有数据，导入前应选择正确的目标数据库。

## 已迁移功能

- 登录、退出、注册、个人资料、修改密码；兼容原 bcrypt 密码。
- 登录审计：记录成功与失败的登录尝试、账号、IP、时间和浏览器信息；仅管理员可查看。
- 管理员创建用户、修改角色、停用账户。
- 日常英语、儿童英语、自然拼读、课本、情景对话、学习笔记、专业词汇、面试英语、数学卡片。
- 关键词搜索、分类筛选、分页、详情、卡片前后导航及关联例句。
- 日常英语和笔记卡片学习进度，保存和恢复个人学习位置。
- 日常英语、笔记、笔记卡片、专业词汇和面试英语的管理；面试回答分段管理。
- 图片上传、原图片资源；其他模块沿用 SQL 导入维护方式。
- Kokoro 中英文朗读和 Whisper 跟读文本匹配评分接口。

`share_status` 保留原系统的内容标记语义；和旧学习页面一样，学习内容面向已登录用户，内容修改只允许管理员。跟读分数为转写文本相似度，不是专业音素发音评分。

## 项目结构

```text
app/
  main.py                  # 应用工厂、中间件、异常处理、路由
  api/                     # 账号、学习内容、音频 API
  core/                    # 环境配置、数据库连接、会话安全
  repositories/            # SQLAlchemy 查询和数据访问
  services/                # 账号业务逻辑
  audio/                   # 从旧项目迁入的音频与评分代码
  models.py                # 映射现有数据库表
  schemas.py               # 输入校验
scripts/dev.sh             # 本地启动
sql/                       # 原有 SQL 备份及增量脚本
data/static/              # 图片和上传文件（本地数据，不提交 Git）
tests/                     # 使用独立 SQLite 数据库的接口测试
```

网页登录使用签名 HttpOnly Cookie，所有写入接口校验 `X-CSRF-Token`。调用顺序：

1. `GET /api/auth/session` 获取匿名 Cookie 和 `csrf_token`。
2. 发送 `POST /api/auth/login`，带 Cookie、`X-CSRF-Token` 和 `{ "username": "...", "password": "..." }`。
3. 登录后使用新返回的 token；退出和修改密码也会返回新 token。

API 浏览器请求需携带凭据。开发前端的 Vite 代理已配置；不同端口直接访问时，在 `CORS_ORIGINS` 设置明确的前端来源。参考 [FastAPI CORS 文档](https://fastapi.tiangolo.com/tutorial/cors/)。

### 微信小程序手机号登录

小程序调用 `wx.login` 和 `getPhoneNumber`，将两个一次性 code 提交到 `POST /api/auth/miniprogram/login`：

```json
{
  "login_code": "wx.login 返回的 code",
  "phone_code": "getPhoneNumber 返回的 code"
}
```

后端使用微信服务端接口校验 code 并取得手机号，先按 `user.contact_number` 查找账户，找不到时自动创建一个 `learner` 账户。手机号不会由小程序直接提交。响应沿用 `user`、`csrf_token`，并带 `created` 标识；小程序应保存响应头 `X-Happy-English-Session`，后续每次请求将它作为同名 Header 发回。该 Header 形式的签名会话适用于小程序不稳定的 Cookie 存储，和网页登录的账户状态、角色检查及密码变更失效机制相同。

部署前在 `.env` 配置微信小程序的服务端凭据，不能将 `AppSecret` 放入小程序代码：

```sh
WECHAT_MINIPROGRAM_APP_ID=wx...
WECHAT_MINIPROGRAM_APP_SECRET=...
WECHAT_REQUEST_TIMEOUT_SECONDS=10
```

已有数据库还需要先执行一次 [20260925_add_miniprogram_phone_login.sql](sql/20260925_add_miniprogram_phone_login.sql)。该脚本会将空联系方式转为 `NULL` 并为手机号建立唯一索引；执行前先处理脚本查询出的重复手机号。

### DeepSeek 复习出题

`POST /api/learning/review-sessions` 从学习者近期学习过的 English Note 和已完成教材课时中抽取双语例句。请求中的 `source_types` 可设为 `["notes"]`、`["textbooks"]` 或两者并存。服务端启用 DeepSeek 后，由模型选择更有代表性的例句并提供等价答案与解析；标准答案仍取自原始笔记或教材，模型故障会自动回退到本地抽题。

密钥只配置在后端 `.env`，不要放入 Android、网页或提交到代码库：

```sh
DEEPSEEK_API_KEY=sk-...
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_REVIEW_MODEL=deepseek-chat
DEEPSEEK_REQUEST_TIMEOUT_SECONDS=20
DEEPSEEK_REVIEW_MAX_CANDIDATES=40
```

留空 `DEEPSEEK_API_KEY` 时仍可使用确定性的本地复习流程。配置了密钥时，只有拥有 `ai-review-generation` 功能权益的活跃会员会调用 DeepSeek；其余用户继续使用确定性的本地复习流程。服务只发送当前学习者近期已学习内容中的有限双语例句，不发送用户 ID、账号或会话信息；日志只记录模型请求失败类型，不记录提示词、例句或密钥。首次部署会话式复习前需执行 [20261103_add_learning_review_sessions.sql](sql/20261103_add_learning_review_sessions.sql) 和 [20261106_add_ai_review_membership_benefit.sql](sql/20261106_add_ai_review_membership_benefit.sql)。

### 登录审计表升级

已有数据库在部署本功能前，需要执行一次 [20260920_add_login_audit.sql](sql/20260920_add_login_audit.sql)。前端 Nginx 会覆盖并转发 `X-Forwarded-For`，因此生产环境应只让 Nginx 对外暴露后端服务，避免客户端伪造登录来源地址。

## 可选服务器音频

配置模板默认 `AUDIO_ENABLED=false`；关闭时 React 页面使用浏览器语音。本机已安装音频依赖，并在 `.env` 设置 `AUDIO_ENABLED=true`，复用原系统缓存的 Kokoro 模型。新环境启用本地朗读和跟读评分时执行：

```sh
.venv/bin/pip install -r requirements-audio.txt
# 按操作系统安装 espeak-ng，并准备 Kokoro / Whisper 模型。
# 在 .env 中设置 AUDIO_ENABLED=true，随后重启。
```

Kokoro 模型与 WAV 缓存在 `~/.cache/happyenglish/kokoro`，可通过 `KOKORO_HOME`、`HF_HOME`、`KOKORO_AUDIO_CACHE_DIR` 覆盖。沿用原系统的 `hexgrad/Kokoro-82M-v1.1-zh` 模型，英语使用 `bf_vale`、中文使用 `zf_001`。音频依赖中包含英语音素转换所需的 `en_core_web_sm`，避免首次朗读时临时安装。已在禁用 Hugging Face 网络访问的情况下，通过 `/api/audio/tts` 验证英语及中英混合文本实际生成 24 kHz WAV；跟读识别尚未进行实际录音验证。

修改 `.env` 后必须重启后端进程，再刷新前端页面；IDEA 中启动的调试进程也需要点击重新运行。`GET /api/auth/session` 返回的 `audio_enabled` 应为 `true`，点击朗读时会请求 `POST /api/audio/tts`。接口不可用时前端仍会回退到浏览器语音。

默认 Whisper 使用 `base.en` / CPU / int8，可通过 `WHISPER_MODEL`、`WHISPER_DEVICE`、`WHISPER_COMPUTE_TYPE` 设置。新环境首次下载模型需要网络和额外磁盘空间。

## 日志与耗时监控

后端启动后会自动创建 `logs/happy-english.log`。文件使用滚动写入，默认单个文件最大 10 MB，保留 5 个历史文件；同时仍输出到控制台。日志不会记录朗读文本、参考文本、转写内容或用户录音，只会记录长度、语言、模型配置、状态和耗时。

```sh
tail -f logs/happy-english.log
```

每个 API 请求都会记录 `request_id`、方法、路径、状态码和 `duration_ms`，并在响应头返回 `X-Request-ID`，方便关联前端报错和服务端日志。请求超过 `REQUEST_SLOW_MS`（默认 1000 ms）会以 warning 记录。

文本转语音会记录缓存命中、等待生成锁、Kokoro 管线初始化、语音合成开始和结束；跟读评分会记录上传读取、Whisper 模型初始化、转写开始和结束、评分与总耗时。若需查看中英混读时的音素转换耗时，将 `LOG_LEVEL=DEBUG` 后重启服务。

可在 `.env` 中配置：

```ini
LOG_DIR=logs
LOG_LEVEL=INFO
LOG_MAX_BYTES=10485760
LOG_BACKUP_COUNT=5
LOG_CONSOLE=true
REQUEST_SLOW_MS=1000
```

## 测试

```sh
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/pytest -q
.venv/bin/ruff check app tests
```

测试仅使用内存 SQLite，不写入你的 MySQL。前端的 Playwright 测试会启动 `tests.browser_app`，该入口同样只使用隔离的测试数据。

## 部署

后端可独立部署：

```sh
.venv/bin/uvicorn app.main:create_app --factory --host 0.0.0.0 --port 8000
```

生产环境设置随机 `SECRET_KEY`、`APP_ENV=production`、`COOKIE_SECURE=true`，由 HTTPS 反向代理转发 `/api` 与 `/static`；静态前端在另一个服务提供。上传文件通过 `data/static` 持久化，数据库独立管理。提供基础 `Dockerfile`，不包含大型音频依赖与模型。前端项目的 `deploy/nginx.conf` 提供同域代理例子。



Nginx 已配置为直接返回静态图片，不再经过 FastAPI。

配置变更：

新增 location /static/ 块，使用 alias 指向 /home/admin/happy_english_server/happy-english/data/static/
设置 30 天浏览器缓存（expires 30d + Cache-Control: public）
关闭该路径的 access_log 减少 IO
验证结果：

检查项	结果
图片 Content-Type	✅ image/png（Nginx 直接返回）
图片大小	✅ 1898426 bytes（与磁盘一致）
缓存头	✅ max-age=2592000 (30天)
API /api/health	✅ 正常
前端页面	✅ 正常
注意事项：

FastAPI 中的 app.mount("/static", ...) 可保留作为兜底，但生产流量已由 Nginx 处理
如后续新增其他静态资源子目录，无需修改 Nginx，/static/ 下所有文件均自动由 Nginx 服务

## 单词之旅游戏 API（已上线）

`https://api.happylingo.cn/api/game/v1/water-sort` 已部署，Android 项目为 `../happylingo-english-game`。复用账号会话、CSRF、会员及两课试听权限；词条直接读取已发布的 Wordly Wise 教材课时，补充中文来源保存在 `app/data/water_sort/translations.json`。

- `GET /progress`：当前账号已完成关卡及已学词。
- `GET /vocabulary?book=1&offset=0&limit=50`：1–12 册分页词表，按教材访问权限过滤。
- `POST /levels:next`：`level_number`、`campaign_version: 2`、UUID `request_id`；200 关固定绑定 1,023 个教材词条。
- `POST /attempts/{attempt_id}/actions`：服务器验证倒水、撤回、重开、确认学习、通关和空瓶问答。使用 `revision` 和 UUID `request_id` 保证重试不会重复执行。

每个游戏账号独立保存进度；题目和选项只用已学词，不下发答案。答对三题发放一支奖励瓶；重开保留奖励瓶，撤回不能复制奖励。增量表位于 `sql/20261105_add_water_sort_game.sql`，MySQL 外键使用与现有 `user.id` 一致的 `BIGINT UNSIGNED`。

现有教材词条总计 3,147 条。Book 4 Lesson 4 原始导入仅 13 条，Book 5 Lesson 7 仅 14 条，尚需校对补齐这三处；未用示例词冒充完整教材。中文优先采用课程已有释义，其余采用 [ECDICT](https://github.com/skywind3000/ECDICT)（MIT，许可证随数据发布）和少量自编释义。

验证：`.venv/bin/pytest -q tests/test_water_sort.py tests/test_architecture.py tests/test_opaque_ids.py`。准备数据使用 `scripts/prepare_water_sort_data.py`；发布使用 `scripts/deploy_water_sort.py`，只上传功能文件并检查服务器已有文件的 SHA256、备份代码、执行增量建表、检查词库和健康状态；失败自动回滚代码。已上传内容不包含 `.env`、用户数据或其他未提交改动。完整客户端契约见相邻游戏项目的 `docs/WATER_SORT_LIVE_API.md`。
