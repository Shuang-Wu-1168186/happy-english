"""Server-authored application shell data built on top of existing services.

This is intentionally additive.  Legacy catalogue and private-zone endpoints
keep their current shapes so deployed Android releases continue to work while
new clients migrate to the bootstrap contract.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from fastapi import HTTPException

from app import schemas as s
from app.dao.app_shell import AppPresentationConfigDAO
from app.services.analytics import AnalyticsService
from app.services.app_actions import action_for_content, action_for_target_url, is_supported_action
from app.services.content import ContentService, RESOURCE_SERVICE_TYPES
from app.services.learning_catalog import LearningCatalogService
from app.services.membership import MembershipService
from app.services.private_zone import PrivateZoneFeatureService, PrivateZoneService


APP_SHELL_SCHEMA_VERSION = 1
DEFAULT_CACHE_TTL_SECONDS = 900
SUPPORTED_LAYOUT_CODES = frozenset(
    {
        "section_list_v1",
        "topic_grid_v1",
        "course_roadmap_v1",
        "shortcut_grid_v1",
        "content_list_v1",
        "content_grid_v1",
    }
)

DEFAULT_COLLECTIONS = {
    "notes": {
        "source_resource": "notes",
        "title": "学习笔记",
        "subtitle": "整理高频表达和学习记录。",
        "icon": "notebook",
        "theme": "violet",
    },
    "professional-vocabulary": {
        "source_resource": "vocabulary",
        "title": "专业词汇",
        "subtitle": "职场和专业场景常用表达。",
        "icon": "briefcase",
        "theme": "violet",
    },
    "vocabulary": {
        "source_resource": "vocabulary",
        "title": "专业词汇",
        "subtitle": "职场和专业场景常用表达。",
        "icon": "briefcase",
        "theme": "violet",
    },
    "interviews": {
        "source_resource": "interviews",
        "title": "面试英语",
        "subtitle": "在常见求职场景中练习回答。",
        "icon": "chat",
        "theme": "blue",
    },
    "kids-cards": {
        "source_resource": "kids-cards",
        "title": "儿童英语卡片",
        "subtitle": "从图片、发音和例句认识单词。",
        "icon": "book-open",
        "theme": "green",
    },
    "math-cards": {
        "source_resource": "math-cards",
        "title": "数学卡片",
        "subtitle": "把关键概念拆成易复习的小卡片。",
        "icon": "calculator",
        "theme": "orange",
    },
    "textbook": {
        "source_resource": "textbook",
        "title": "英文课本",
        "subtitle": "按单元和课文顺序学习。",
        "icon": "book-open",
        "theme": "green",
    },
    "phonics": {
        "source_resource": "phonics",
        "title": "自然拼读",
        "subtitle": "按音素和规律练习见词能读。",
        "icon": "languages",
        "theme": "orange",
    },
}


def _decode_json(value, default):
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (TypeError, ValueError):
            value = default
    return value if isinstance(value, type(default)) else default


def _string(value: object) -> str:
    return str(value or "").strip()


class AppPresentationService:
    """Versioned presentation metadata independent from legacy content rows."""

    def __init__(self, db):
        self.db = db
        self.dao = AppPresentationConfigDAO(db)

    @staticmethod
    def serialise(row):
        result = dict(row)
        result["presentation"] = _decode_json(result.pop("presentation_json", None), {})
        result["fallback_action"] = _decode_json(result.pop("fallback_action_json", None), {}) or None
        return result

    @staticmethod
    def _values(payload: s.AppPresentationConfigInput, actor):
        return {
            "target_type": payload.target_type,
            "target_key": payload.target_key,
            "platform": payload.platform,
            "layout_code": payload.layout_code,
            "presentation_json": json.dumps(payload.presentation, ensure_ascii=False, separators=(",", ":")),
            "min_app_version": payload.min_app_version or None,
            "fallback_action_json": (
                json.dumps(payload.fallback_action, ensure_ascii=False, separators=(",", ":"))
                if payload.fallback_action
                else None
            ),
            "status": payload.status,
            "sort_order": payload.sort_order,
            "updated_by": actor["id"],
        }

    def list(self):
        return {"items": [self.serialise(row) for row in self.dao.list_all()]}

    def save(self, payload: s.AppPresentationConfigInput, actor, config_id=None):
        if payload.layout_code not in SUPPORTED_LAYOUT_CODES:
            raise HTTPException(422, "The layout_code is not registered by the app shell.")
        if payload.fallback_action and not is_supported_action(payload.fallback_action):
            raise HTTPException(422, "fallback_action is not a registered typed action.")
        existing = self.dao.find_by_id(config_id) if config_id is not None else None
        if config_id is not None and not existing:
            raise HTTPException(404, "App presentation configuration not found.")
        duplicate = self.dao.by_target(payload.target_type, payload.target_key, payload.platform)
        if duplicate and duplicate["id"] != config_id:
            raise HTTPException(409, "App presentation configuration already exists for this target.")
        values = self._values(payload, actor)
        if existing:
            self.dao.update(config_id, values)
            saved_id = config_id
        else:
            saved_id = self.dao.insert({**values, "created_by": actor["id"]})
        self.db.commit()
        return self.serialise(self.dao.find_by_id(saved_id))

    def delete(self, config_id):
        if not self.dao.find_by_id(config_id):
            raise HTTPException(404, "App presentation configuration not found.")
        self.dao.delete(config_id)
        self.db.commit()

    def resolve(self, target_type, target_key, platform, *, layout_code, presentation=None):
        """Return a supported layout plus a shallow override of display data."""

        result = {
            "layout_code": layout_code,
            "presentation": dict(presentation or {}),
            "min_app_version": "",
            "fallback_action": None,
        }
        configured = self.dao.effective_for(target_type, target_key, platform)
        if not configured:
            return result
        config = self.serialise(configured)
        configured_presentation = config["presentation"]
        result["presentation"] = {**result["presentation"], **configured_presentation}
        result["layout_code"] = config["layout_code"] or result["layout_code"]
        result["min_app_version"] = config.get("min_app_version") or ""
        result["fallback_action"] = config.get("fallback_action")
        return result


class AppBootstrapService:
    """Compose a stable app manifest from existing catalogue and private-zone data."""

    def __init__(self, db):
        self.db = db
        self.presentations = AppPresentationService(db)

    @staticmethod
    def _availability(action):
        if action:
            return {"state": "available"}
        return {
            "state": "unavailable",
            "reason_code": "unsupported_target",
            "message": "此入口需要更新 App 后打开。",
        }

    @staticmethod
    def _revision(payload):
        encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(encoded.encode()).hexdigest()[:20]

    def _module_card(self, module, platform):
        presentation = self.presentations.resolve(
            "module",
            module["module_code"],
            platform,
            layout_code="section_list_v1",
            presentation={
                "title": _string(module.get("name")),
                "subtitle": _string(module.get("description")),
                "icon": _string(module.get("icon")) or "book-open",
                "theme": _string(module.get("color")) or "blue",
            },
        )
        action = {"type": "open_module", "module_id": module["id"]}
        return {
            "id": f"module:{module['module_code']}",
            "kind": "module",
            "title": presentation["presentation"].get("title") or module["name"],
            "subtitle": presentation["presentation"].get("subtitle") or "",
            "presentation": presentation["presentation"],
            "layout_code": presentation["layout_code"],
            "min_app_version": presentation["min_app_version"],
            "fallback_action": presentation["fallback_action"],
            "action": action,
            "availability": self._availability(action),
            "analytics_key": f"module.{module['module_code']}",
        }

    def _shortcut_card(self, shortcut, platform):
        action = action_for_target_url(shortcut.get("target_url"))
        presentation = self.presentations.resolve(
            "placement",
            "private_zone.shortcuts",
            platform,
            layout_code="shortcut_grid_v1",
            presentation={
                "title": _string(shortcut.get("title")),
                "subtitle": _string(shortcut.get("description")),
                "icon": _string(shortcut.get("icon")) or "bookmark",
                "theme": "violet",
            },
        )
        return {
            "id": shortcut["id"],
            "kind": "shortcut",
            "title": presentation["presentation"].get("title") or shortcut["title"],
            "subtitle": presentation["presentation"].get("subtitle") or "",
            "presentation": presentation["presentation"],
            "action": action,
            "legacy_target_url": shortcut.get("target_url"),
            "availability": self._availability(action),
            "analytics_key": f"private_zone.shortcut.{shortcut['id']}",
        }

    def _feature_card(self, feature, platform):
        action = action_for_target_url(feature.get("target_url"))
        presentation = self.presentations.resolve(
            "placement",
            "private_zone.features",
            platform,
            layout_code="shortcut_grid_v1",
            presentation={
                "title": _string(feature.get("title")),
                "subtitle": _string(feature.get("description")),
                "icon": _string(feature.get("icon")) or "bookmark",
                "theme": "violet",
            },
        )
        return {
            "id": f"feature:{feature['feature_code']}",
            "kind": "feature",
            "title": presentation["presentation"].get("title") or feature["title"],
            "subtitle": presentation["presentation"].get("subtitle") or "",
            "presentation": presentation["presentation"],
            "action": action,
            "legacy_target_url": feature.get("target_url"),
            "availability": self._availability(action),
            "analytics_key": f"private_zone.feature.{feature['feature_code']}",
        }

    def _collection_card(self, collection_code, definition, platform):
        presentation = self.presentations.resolve(
            "collection",
            collection_code,
            platform,
            layout_code="content_list_v1",
            presentation={key: definition[key] for key in ("title", "subtitle", "icon", "theme")},
        )
        action = {"type": "open_collection", "collection_code": collection_code}
        return {
            "id": f"collection:{collection_code}",
            "kind": "collection",
            "title": presentation["presentation"].get("title") or definition["title"],
            "subtitle": presentation["presentation"].get("subtitle") or "",
            "presentation": presentation["presentation"],
            "layout_code": presentation["layout_code"],
            "action": action,
            "availability": self._availability(action),
            "analytics_key": f"collection.{collection_code}",
        }

    def _renderer_summaries(self, platform):
        templates = LearningCatalogService(self.db).list_templates(active_only=True)["items"]
        result = []
        for template in templates:
            clients = template.get("supported_clients") or []
            result.append(
                {
                    "code": template.get("template_code") or template.get("code"),
                    "version": template.get("template_version") or template.get("version", 1),
                    "content_kind": template.get("content_kind"),
                    "supported_clients": clients,
                    "declares_platform_support": platform in clients,
                }
            )
        return result

    def bootstrap(self, user, platform, app_version, locale):
        modules = LearningCatalogService(self.db).list_modules()["items"]
        features = PrivateZoneFeatureService(self.db).list(enabled_only=True)
        shortcuts = PrivateZoneService(self.db).list_shortcuts(user)["items"]
        payload = {
            "schema_version": APP_SHELL_SCHEMA_VERSION,
            "cache_ttl_seconds": DEFAULT_CACHE_TTL_SECONDS,
            "client": {"platform": platform, "app_version": app_version, "locale": locale},
            "navigation": [
                {"id": "home", "title": "首页", "action": {"type": "open_home"}},
                {"id": "explore", "title": "学习资源", "action": {"type": "open_explore"}},
                {"id": "private-zone", "title": "私人专区", "action": {"type": "open_private_zone"}},
            ],
            "placements": [
                {
                    "slot": "home.modules",
                    "layout_code": "section_list_v1",
                    "items": [self._module_card(module, platform) for module in modules],
                },
                {
                    "slot": "learn.collections",
                    "layout_code": "section_list_v1",
                    "items": [
                        self._collection_card(code, definition, platform)
                        for code, definition in DEFAULT_COLLECTIONS.items()
                    ],
                },
                {
                    "slot": "private_zone.features",
                    "layout_code": "shortcut_grid_v1",
                    "items": [self._feature_card(feature, platform) for feature in features],
                },
                {
                    "slot": "private_zone.shortcuts",
                    "layout_code": "shortcut_grid_v1",
                    "items": [self._shortcut_card(shortcut, platform) for shortcut in shortcuts],
                },
            ],
            "renderers": self._renderer_summaries(platform),
            "analytics_policy": AnalyticsService(self.db).policy(),
        }
        return {"revision": self._revision(payload), **payload}

    def _collection_definition(self, collection_code, platform):
        definition = dict(DEFAULT_COLLECTIONS.get(collection_code) or {})
        configured = self.presentations.resolve(
            "collection",
            collection_code,
            platform,
            layout_code="content_list_v1",
            presentation=definition,
        )
        merged = configured["presentation"]
        source_resource = _string(merged.pop("source_resource", ""))
        if not source_resource or source_resource not in RESOURCE_SERVICE_TYPES:
            raise HTTPException(404, "Learning collection not found.")
        return {
            "collection_code": collection_code,
            "source_resource": source_resource,
            "layout_code": configured["layout_code"],
            "presentation": merged,
            "min_app_version": configured["min_app_version"],
            "fallback_action": configured["fallback_action"],
        }

    @staticmethod
    def _content_title(item):
        return _string(
            item.get("title")
            or item.get("item_title")
            or item.get("term")
            or item.get("word")
            or item.get("question")
            or item.get("lesson_name")
            or item.get("tag")
            or "学习内容"
        )

    @staticmethod
    def _content_subtitle(item):
        return _string(
            item.get("summary")
            or item.get("chinese_meaning")
            or item.get("translation")
            or item.get("question_cn")
            or item.get("subtitle")
        )

    def collection(
        self,
        collection_code,
        user,
        platform,
        q="",
        category="",
        page=1,
        page_size=20,
    ):
        definition = self._collection_definition(collection_code, platform)
        MembershipService(self.db).require_legacy_content_access(user, definition["source_resource"])
        content = ContentService(self.db).list_content(
            definition["source_resource"],
            q=q,
            category=category,
            page=page,
            page_size=page_size,
            user=user,
        )
        items = []
        for item in content["items"]:
            action = action_for_content(definition["source_resource"], item["id"])
            items.append(
                {
                    "id": item["id"],
                    "title": self._content_title(item),
                    "subtitle": self._content_subtitle(item),
                    "action": action,
                    "availability": self._availability(action),
                    "analytics_key": f"collection.{collection_code}.item.{item['id']}",
                    "payload": item,
                }
            )
        return {
            **definition,
            "items": items,
            "total": content["total"],
            "page": content["page"],
            "page_size": content["page_size"],
            "total_pages": content["total_pages"],
        }


APP_SHELL_TABLE_SERVICE_TYPES = {
    "app_presentation_config": AppPresentationService,
}
