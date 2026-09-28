"""Language-register and usage-scene labels for English study-note cards.

The labels are deliberately conservative.  A card that compares several
alternatives is marked ``mixed`` and an isolated term without a reliable
register is marked ``neutral`` or ``reference`` instead of being presented as
spoken English by default.
"""

from collections.abc import Mapping
from dataclasses import dataclass
import re
from typing import Any


AUTO_CLASSIFICATION_SOURCE = "auto_rule_v1"

LANGUAGE_REGISTERS = (
    "common_spoken",
    "formal_spoken",
    "written",
    "mixed",
    "neutral",
    "reference",
    "unclassified",
)

USAGE_SCENARIOS = (
    "daily_life",
    "friends_social",
    "workplace",
    "meeting_presentation",
    "customer_service",
    "interview",
    "travel_service",
    "email_writing",
    "report_writing",
    "academic",
    "technical",
    "health_medical",
    "online_chat",
    "general",
)


@dataclass(frozen=True)
class NoteLanguageClassification:
    language_register: str
    usage_scenarios: list[str]
    register_reason: str
    classification_confidence: int
    classification_source: str = AUTO_CLASSIFICATION_SOURCE


def _normalise(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "").lower().replace("’", "'")).strip()


def _item_text(item: Mapping[str, Any]) -> str:
    fields = (
        "item_title",
        "raw_text",
        "english_text",
        "chinese_text",
        "explanation",
        "examples",
        "keywords",
    )
    return _normalise(" ".join(str(item.get(field) or "") for field in fields))


def _has_any(text: str, signals: tuple[str, ...]) -> bool:
    return any(signal in text for signal in signals)


# These are explicit style cues from the notes themselves, plus a compact set
# of forms with a reliably conversational register.  Do not include ordinary
# contractions here: "I'm" and "we'll" are common in neutral writing too.
SPOKEN_SIGNALS = (
    "口语",
    "日常口语",
    "非正式",
    "随意",
    "聊天",
    "俚语",
    "口语感",
    "自然表达",
    "很自然",
    "更自然",
    "更日常",
    "日常表达",
    "日常说法",
    "缩写形式",
    "新西兰口语",
    "澳洲口语",
    "英式口语",
    "美式口语",
    "gonna",
    "wanna",
    "gotta",
    "kinda",
    "sorta",
    "lemme",
    "gimme",
    "dunno",
    "ain't",
    "yep",
    "nope",
    "nah",
    "just chilling",
    "hang out",
    "pop in",
    "pop over",
    "good to go",
    "i reckon",
    "show up",
)

# Cues which specifically describe the language choice, rather than a noun
# such as "正式员工".  This distinction prevents false formal labels.
FORMAL_SPOKEN_SIGNALS = (
    "正式口语",
    "正式表达",
    "更正式",
    "较正式",
    "比较正式",
    "礼貌表达",
    "礼貌地",
    "正式场合",
    "正式谈话",
    "商务沟通",
    "面试回答",
    "professional communication",
    "would you mind",
    "would you be able to",
    "could you please",
    "may i ",
    "i would like to",
    "i'd like to",
    "i would appreciate",
    "please let me know",
    "my apologies",
    "would it be possible",
    "at your earliest convenience",
)

WRITTEN_SIGNALS = (
    "书面语",
    "正式写作",
    "书面表达",
    "偏书面",
    "更书面",
    "比较书面",
    "书面场景",
    "学术写作",
    "法律文书",
    "公文",
    "合同措辞",
    "政策文件",
    "新闻报道",
    "文学表达",
    "written language",
    "formal writing",
    "academic writing",
    "therefore",
    "moreover",
    "furthermore",
    "nevertheless",
    "consequently",
    "hence",
    "whereas",
    "hereby",
    "therein",
    "thereof",
    "herein",
    "pursuant to",
    "notwithstanding",
    "aforementioned",
    "in accordance with",
    "coupled with",
    "conversely",
)

REFERENCE_SIGNALS = (
    "术语",
    "技术语境",
    "医学",
    "法律",
    "科学",
    "统计学",
    "数据库",
    "系统架构",
    "编程",
    "专业词汇",
    "technical jargon",
    "medical jargon",
    "legal jargon",
    "api",
    "database",
    "software",
    "methodology",
)

SCENARIO_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "interview",
        ("面试", "interview", "resume", "résumé", "cv", "candidate", "recruit"),
    ),
    (
        "customer_service",
        (
            "客户",
            "customer",
            "client",
            "收银",
            "checkout",
            "till",
            "cashier",
            "退货",
            "complaint",
            "订单",
            "order",
        ),
    ),
    (
        "meeting_presentation",
        (
            "会议",
            "汇报",
            "演示",
            "讲座",
            "meeting",
            "presentation",
            "conference",
            "agenda",
            "briefing",
            "workshop",
            "session",
        ),
    ),
    (
        "email_writing",
        ("邮件", "email", "email thread", "reply", "inbox", "写信"),
    ),
    (
        "report_writing",
        (
            "报告",
            "文档",
            "合同",
            "政策",
            "公告",
            "法规",
            "report",
            "document",
            "documentation",
            "contract",
            "policy",
        ),
    ),
    (
        "academic",
        (
            "学术",
            "论文",
            "研究",
            "课堂",
            "大学",
            "academic",
            "thesis",
            "research",
            "lecture",
            "professor",
            "university",
        ),
    ),
    (
        "technical",
        ("技术", "系统", "数据库", "编程", "开发", "software", "database", "api", "code"),
    ),
    (
        "health_medical",
        ("健康", "医院", "医生", "医疗", "medical", "health", "doctor", "hospital", "immune"),
    ),
    (
        "travel_service",
        (
            "旅行",
            "机场",
            "航班",
            "酒店",
            "签证",
            "旅游",
            "travel",
            "airport",
            "flight",
            "hotel",
            "visa",
            "tourist",
        ),
    ),
    (
        "online_chat",
        ("网络", "社交媒体", "线上", "帖子", "online", "social media", "post", "internet"),
    ),
    (
        "workplace",
        (
            "工作",
            "职场",
            "公司",
            "同事",
            "项目",
            "任务",
            "团队",
            "老板",
            "workplace",
            "company",
            "colleague",
            "manager",
            "project",
            "employee",
            "office",
            "shift",
        ),
    ),
    (
        "friends_social",
        (
            "朋友",
            "聊天",
            "恋爱",
            "约会",
            "聚会",
            "关系",
            "friend",
            "relationship",
            "dating",
            "party",
            "hang out",
            "social",
        ),
    ),
    (
        "daily_life",
        (
            "日常",
            "生活",
            "家庭",
            "购物",
            "食物",
            "家里",
            "周末",
            "天气",
            "生活场景",
            "daily life",
            "shopping",
            "family",
            "weekend",
            "weather",
            "errand",
            "meal",
            "neighborhood",
        ),
    ),
)


def _usage_scenarios(text: str, language_register: str) -> list[str]:
    scenarios = [code for code, signals in SCENARIO_RULES if _has_any(text, signals)]
    # A general daily-life match is less useful once a specific setting exists.
    if len(scenarios) > 1 and "daily_life" in scenarios:
        scenarios.remove("daily_life")
    if len(scenarios) > 3:
        scenarios = scenarios[:3]
    if scenarios:
        return scenarios
    if language_register == "common_spoken":
        return ["daily_life"]
    if language_register == "formal_spoken":
        return ["workplace"]
    if language_register == "written":
        return ["report_writing"]
    return ["general"]


def classify_note_item(item: Mapping[str, Any]) -> NoteLanguageClassification:
    """Classify one note item without changing the supplied mapping."""
    text = _item_text(item)
    item_type = _normalise(item.get("item_type"))
    spoken = _has_any(text, SPOKEN_SIGNALS)
    formal_spoken = _has_any(text, FORMAL_SPOKEN_SIGNALS)
    written = _has_any(text, WRITTEN_SIGNALS)
    reference = _has_any(text, REFERENCE_SIGNALS)

    if spoken and (formal_spoken or written):
        language_register = "mixed"
        reason = "这张卡片比较了日常说法与正式或书面替代表达。"
        confidence = 92
    elif written:
        language_register = "written"
        reason = "表达或说明指向书面、学术、法律或正式写作语境。"
        confidence = 90
    elif formal_spoken:
        language_register = "formal_spoken"
        reason = "表达更适合礼貌、商务、会议或面试等正式沟通。"
        confidence = 86
    elif spoken:
        language_register = "common_spoken"
        reason = "含有明确的日常口语、缩略或非正式表达线索。"
        confidence = 90
    elif item_type in {"phrase", "sentence", "chunk", "correction", "example", "idiom"}:
        language_register = "common_spoken"
        reason = "这是一条以日常对话为主要使用方式的短语或句型。"
        confidence = 70
    elif item_type in {"grammar", "knowledge"} or reference:
        language_register = "reference"
        reason = "这是语法、知识点或专业术语卡，需结合上下文选择语体。"
        confidence = 78
    else:
        language_register = "neutral"
        reason = "该词本身可用于口语和书面语，属于中性表达。"
        confidence = 62

    return NoteLanguageClassification(
        language_register=language_register,
        usage_scenarios=_usage_scenarios(text, language_register),
        register_reason=reason,
        classification_confidence=confidence,
    )
