# 私人专区与家庭组

私人专区是学习内容和个人工具的入口。目录中的教材、课程和内容记录仍然只有一份，收藏通过 `private_zone_item` 保存引用，并在返回值中标记来源范围：

- `personal`：只对当前用户可见。
- `family`：对指定家庭组的 active 成员可见。

家庭组的成员关系由 `family_group` 和 `family_group_member` 管理。家庭组权限只解决“谁能看到这个私人专区条目”，不等于会员权益，也不会把付费课程授权给家庭成员。课程或教材被家庭成员打开时，系统仍按当前用户自己的会员状态返回 `available`、`preview` 或 `locked`。

## 学习者看到的入口和工具

- **收藏课程**：只显示收藏的课程。打开列表后，点击课程即进入原有课程学习页；条目仍会标明来自个人还是家庭组。
- **公共学习入口**：配置和数据会保留在 `private_zone_feature`，但当前功能尚未开放；学习端和小程序暂不展示，也不会收到可打开的公共入口。
- **家庭常用入口**：只显示当前用户所在家庭组的快捷入口。数据保存在 `private_zone_shortcut`，以 `scope_type=family` 和 `family_group_id` 标记；入口由家庭 owner 或家庭管理员在后台配置，家庭成员都会看到。
- **个人笔记**：面向所有用户的自由笔记，数据保存在 `personal_note`。它只属于创建者，支持正文、标签、颜色和置顶，和 `english_note` 完全分表，不会进入 English Note 的学习内容或复习流程。

家庭组用于共享收藏内容和家庭常用入口，不能查看或编辑其他成员的个人笔记。

## 预留的公共入口配置

`private_zone_feature` 为后续公共入口保留标题、说明、图标和 `target_url`，管理员编辑时会保留内部 `config_json`。当前 `PRIVATE_ZONE_PUBLIC_ENTRIES_ENABLED = False`，学习端、小程序和后台入口管理页均不展示这部分功能；配置接口和已有数据会保留，待产品方案明确后再启用。它仍可使用以下匹配条件，把收藏的内容归入合适的功能分类：

```json
{
  "resource_types": ["material"],
  "material_types": ["textbook", "vocabulary", "card_set"]
}
```

默认功能包括：

- `my-english-notes`：个人笔记、家庭共学笔记和笔记条目。
- `my-textbooks`：课本和教材。
- `textbook-vocabulary`：课本单词、词卡和复习词表。
- `my-interview-questions`：面试题和回答练习。
- `saved-learning`：课程和其他收藏内容；学习端以“收藏课程”模块提供入口，默认不额外展示该公共卡片。

管理员通过 `GET /api/admin/private-zone/features` 查看公共入口，通过 `POST /api/admin/private-zone/features` 新增、`PUT /api/admin/private-zone/features/{feature_code}` 修改。家庭常用入口通过 `GET/POST /api/admin/private-zone/shortcuts` 查看或新增，通过 `PUT/DELETE /api/admin/private-zone/shortcuts/{id}` 编辑或移除；保存时必须提供 `family_group_id`，且操作者必须是该家庭的 owner 或家庭管理员。没有执行迁移种子时，服务首次读取也会补齐默认功能。

## 学习者接口

- `GET /api/learning/private-zone`：当前 `public_entries` 固定返回空数组；同时返回当前用户所在家庭组的 `shortcuts`、家庭组和聚合条目。
- `GET /api/learning/private-zone/favorite-courses`：返回当前用户可见的已收藏课程，含个人或家庭来源。
- `GET /api/learning/private-zone/shortcuts`：读取当前用户所在家庭组的常用入口。学习端没有新增、修改或删除常用入口的接口。
- `GET/POST /api/learning/private-zone/personal-notes`：读取或创建自己的个人笔记；`GET/PUT/DELETE /personal-notes/{id}` 查看、修改或删除。
- `POST /api/learning/private-zone/items`：收藏已发布的 `material`、`course`、平台共享的 `note` 或可访问的 `note_item`。
- `DELETE /api/learning/private-zone/items/{item_id}`：移除个人条目；家庭条目由家庭 owner/admin 移除。
- `POST /api/learning/private-zone/notes`：创建个人或家庭笔记，并自动加入对应作用域。
- `POST /api/learning/private-zone/notes/{note_id}/items`：向个人或家庭笔记添加笔记条目。
- `GET /api/learning/private-zone/notes`：只返回当前用户能访问的私有笔记。
- `GET/POST /api/learning/family-groups`：查看或创建家庭组。
- `POST /api/learning/family-groups/{group_id}/members`：由 owner/admin 添加已有用户。
- `DELETE /api/learning/family-groups/{group_id}/members/{user_id}`：owner/admin 移除成员，成员也可以移除自己。

旧的 `/api/content/notes` 和 `/api/content/note-items` 只读取 `scope_type=platform` 的内容，因此个人或家庭笔记不会因为调用旧内容接口而泄露。

## 数据库变更

依次执行 [`20261009_add_private_zone_family_sharing.sql`](../sql/20261009_add_private_zone_family_sharing.sql)、[`20261010_add_private_zone_personal_tools.sql`](../sql/20261010_add_private_zone_personal_tools.sql)、[`20261010_move_private_zone_shortcuts_to_admin.sql`](../sql/20261010_move_private_zone_shortcuts_to_admin.sql)、[`20261010_restore_personal_shortcuts_and_publish_features.sql`](../sql/20261010_restore_personal_shortcuts_and_publish_features.sql) 和 [`20261010_make_private_zone_shortcuts_family_shared.sql`](../sql/20261010_make_private_zone_shortcuts_family_shared.sql)；`sql/create_database.sql` 已按顺序加入它们。最后一个脚本为旧快捷入口补齐家庭关系：优先放入入口创建者已加入的家庭；若还没有家庭，则创建一个可邀请成员的初始家庭。
