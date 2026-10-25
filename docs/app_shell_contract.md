# App Shell 后端契约实施说明

本次实现以增量方式增加了后端驱动的 App 壳层能力。已有 Android 版本继续调用原有目录、课程、私人专区和进度接口；没有删除、改名或改变任何旧接口的响应字段。

## 部署顺序

1. 先执行 [`sql/20261026_add_app_shell_contract.sql`](../sql/20261026_add_app_shell_contract.sql)。该迁移只创建新表，并补充已验证 Android 渲染器的模板声明。
2. 再部署应用代码。
3. 保持 Android 继续使用旧接口；发布包含 `AppManifest`、`UiActionResolver` 和 `AnalyticsTracker` 的版本后，再逐步开启新端点。

如果只部署应用代码而没有执行迁移，当前 App 不受影响，因为它不会调用新端点；新 Bootstrap、展示配置和埋点端点会返回数据库架构未就绪的错误。

## 新增接口

| 接口 | 用途 |
| --- | --- |
| `GET /api/learning/app/bootstrap` | 返回导航、页面槽位、集合、动作、渲染器与埋点策略。 |
| `GET /api/learning/app/collections/{collection_code}` | 返回通用资源集合和 `open_content` 动作。 |
| `GET/POST/PUT/DELETE /api/admin/app-presentation-configs` | 管理模块、专题、集合和页面槽位的展示配置。 |
| `GET /api/analytics/policy` | 获取内置和后台注册的埋点事件字典。 |
| `POST /api/analytics/events:batch` | 接收认证用户的幂等批量埋点。 |
| `GET/POST/PUT /api/admin/analytics/event-definitions` | 管理未来业务事件及允许属性。 |
| `GET/POST/PUT/DELETE /api/learning/family-groups/{group_id}/shortcuts` | 家庭拥有者和家庭管理员自助维护快捷入口。 |

内部入口通过 `UiAction` 表示，例如 `open_collection`、`open_course`、`open_material` 和 `open_content`。旧的 `target_url` 仍保留给已运行的 Android 版本；新家庭快捷入口接口同时返回由该 URL 推导出的 `action`。

## 发布边界

展示配置只接受后端已注册的布局：`section_list_v1`、`topic_grid_v1`、`course_roadmap_v1`、`shortcut_grid_v1`、`content_list_v1` 和 `content_grid_v1`。回退动作也必须是已注册的类型。这样后台不能发布当前 App 没有实现的任意页面。

模板 `supported_clients` 现在可声明 `android` 和 `ios`。迁移会为当前已验证的内置模板补上 `android`，而新模板由发布人员明确声明支持的平台。

## 埋点隐私与可靠性

事件使用 UUID 去重，支持离线重试和批量上传。服务端只接受事件字典中注册的事件名和标量属性，并拒绝笔记正文、原文内容、音频、邀请码、凭证和个人资料字段。埋点请求体和 `analytics_event` SQL 参数不会写入应用日志。

支付、会员权益、课程完成等最终业务口径仍应由服务端业务事务产生；客户端埋点用于页面、入口、动作和学习漏斗分析。
