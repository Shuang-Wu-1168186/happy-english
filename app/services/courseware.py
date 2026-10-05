"""Validation, publication rules, and serialisation for lesson courseware."""

import hashlib
import json
import re

from fastapi import HTTPException
from sqlalchemy import func, or_, select

from app import models as m
from app import schemas as s
from app.dao.courseware import CoursewareBlockDAO, CoursewareBlockSourceDAO
from app.services.courseware_scene_catalog import (
    CURATED_REAL_LIFE_EXPRESSION_SCENES,
    CURATED_REAL_LIFE_SCENES,
)


def _decode(value, fallback):
    if value is None:
        return fallback
    try:
        return json.loads(value)
    except (TypeError, ValueError) as error:
        raise HTTPException(500, "Stored courseware data is invalid.") from error


def serialise_courseware_block(row, sources=None):
    result = dict(row)
    result["payload"] = _decode(result.pop("payload_json"), {})
    if sources is not None:
        result["sources"] = [serialise_courseware_source(source) for source in sources]
    return result


def serialise_courseware_source(row):
    result = dict(row)
    result["source_locator"] = _decode(result.pop("source_locator_json"), None)
    return result


class CoursewareBlockService:
    """Owns courseware block validation and the publication boundary."""

    dao_type = CoursewareBlockDAO
    source_dao_type = CoursewareBlockSourceDAO

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)
        self.sources = self.source_dao_type(db)

    def require_any(self, block_id):
        row = self.dao.find_by_id(block_id)
        if not row:
            raise HTTPException(404, "Courseware block not found.")
        return row

    @staticmethod
    def _string(payload, key, label, required=True):
        value = payload.get(key)
        if value is None and not required:
            return ""
        if not isinstance(value, str) or not value.strip():
            raise HTTPException(422, f"{label} requires a non-empty {key}.")
        return value

    @classmethod
    def _sentence(cls, value, label):
        if not isinstance(value, dict):
            raise HTTPException(422, f"{label} must be an object.")
        cls._string(value, "english", label)
        cls._string(value, "chinese", label)

    @classmethod
    def validate_payload(cls, block_type, payload):
        if not isinstance(payload, dict):
            raise HTTPException(422, "payload must be an object.")
        if block_type == "hero":
            cls._string(payload, "phrase", "hero")
            cls._string(payload, "meaning", "hero")
            cls._string(payload, "memory", "hero")
            cls._sentence(payload.get("key_sentence"), "hero.key_sentence")
            return
        if block_type == "usage_group":
            uses = payload.get("uses")
            if not isinstance(uses, list) or not uses:
                raise HTTPException(422, "usage_group requires a non-empty uses list.")
            for index, use in enumerate(uses, start=1):
                if not isinstance(use, dict):
                    raise HTTPException(422, f"usage_group.uses[{index}] must be an object.")
                cls._string(use, "title", f"usage_group.uses[{index}]")
                cls._string(use, "description", f"usage_group.uses[{index}]")
                examples = use.get("examples")
                if not isinstance(examples, list) or not examples:
                    raise HTTPException(422, f"usage_group.uses[{index}] requires examples.")
                for example in examples:
                    cls._sentence(example, f"usage_group.uses[{index}].examples")
            return
        if block_type == "dialogue":
            cls._string(payload, "scene", "dialogue")
            lines = payload.get("lines")
            if not isinstance(lines, list) or not lines:
                raise HTTPException(422, "dialogue requires a non-empty lines list.")
            for line in lines:
                if not isinstance(line, dict):
                    raise HTTPException(422, "dialogue.lines must contain objects.")
                cls._string(line, "speaker", "dialogue.lines")
                cls._sentence(line, "dialogue.lines")
            if NoteCoursewareService.is_low_quality_scene_dialogue(lines):
                raise HTTPException(
                    422,
                    "Dialogue must be a coherent real-life exchange, not a vocabulary-definition prompt.",
                )
            return
        if block_type == "comparison":
            items = payload.get("items")
            if not isinstance(items, list) or len(items) < 2:
                raise HTTPException(422, "comparison requires at least two items.")
            for item in items:
                if not isinstance(item, dict):
                    raise HTTPException(422, "comparison.items must contain objects.")
                for key in ("expression", "label", "meaning", "english", "chinese"):
                    cls._string(item, key, "comparison.items")
            return
        if block_type == "output":
            cls._string(payload, "instruction", "output")
            patterns = payload.get("patterns")
            if not isinstance(patterns, list) or not patterns or not all(
                isinstance(pattern, str) and pattern.strip() for pattern in patterns
            ):
                raise HTTPException(422, "output requires non-empty text patterns.")
            if not all(NoteCoursewareService._is_meaningful_practice_sentence(pattern) for pattern in patterns):
                raise HTTPException(
                    422,
                    "Each output pattern must be a complete English sentence with the target expression blanked.",
                )
            return
        if block_type == "recap":
            cls._string(payload, "summary", "recap")
            cls._sentence(payload.get("key_sentence"), "recap.key_sentence")

    def list_for_lesson(self, lesson_id, published_only=False, include_sources=False):
        rows = self.dao.list_for_lesson(lesson_id, published_only)
        return [
            serialise_courseware_block(
                row,
                self.sources.list_for_block(row["id"]) if include_sources else None,
            )
            for row in rows
        ]

    def save(self, lesson_id, payload: s.CoursewareBlockInput, actor, block_id=None):
        lesson = self.db.execute(
            select(m.learning_material_lesson).where(m.learning_material_lesson.c.id == lesson_id)
        ).mappings().first()
        if not lesson:
            raise HTTPException(404, "Learning material lesson not found.")
        if lesson["lesson_format"] != "courseware":
            raise HTTPException(409, "Courseware blocks require a courseware lesson.")
        values = payload.model_dump()
        self.validate_payload(values["block_type"], values["payload"])
        values["title"] = values["title"] or None
        values["payload_json"] = json.dumps(
            values.pop("payload"), ensure_ascii=False, separators=(",", ":")
        )
        values["material_lesson_id"] = lesson_id
        if block_id is not None:
            existing = self.require_any(block_id)
            if existing["material_lesson_id"] != lesson_id:
                raise HTTPException(409, "The courseware block belongs to a different lesson.")
        if values["status"] == "published":
            target_id = block_id
            if target_id is None:
                raise HTTPException(422, "Save a draft block and sources before publishing it.")
            if not self.sources.list_for_block(target_id):
                raise HTTPException(422, "A published courseware block needs at least one source snapshot.")
        if block_id is None:
            values["created_by"] = actor["id"]
            block_id = self.dao.insert(values)
        else:
            values["updated_by"] = actor["id"]
            self.dao.update(block_id, values)
        self.db.commit()
        return serialise_courseware_block(self.require_any(block_id), self.sources.list_for_block(block_id))

    def replace_sources(self, block_id, payload: s.CoursewareBlockSourcesInput):
        self.require_any(block_id)
        values = []
        for source in payload.items:
            item = self._validate_source(source)
            values.append({**item, "courseware_block_id": block_id})
        self.sources.delete_where(self.sources.table.c.courseware_block_id == block_id)
        for value in values:
            self.sources.insert(value)
        self.db.commit()
        return [serialise_courseware_source(row) for row in self.sources.list_for_block(block_id)]

    def _validate_source(self, source: s.CoursewareBlockSourceInput):
        record = self.db.execute(
            select(m.english_note_item).where(m.english_note_item.c.id == source.source_reference_id)
        ).mappings().first()
        if not record:
            raise HTTPException(422, "The courseware source record is unavailable.")
        source_text = record[source.source_field] or ""
        snapshot = source.source_snapshot_text
        if snapshot not in source_text:
            raise HTTPException(422, "The source snapshot must be copied from its selected source field.")
        return {
            "source_resource": source.source_resource,
            "source_reference_id": source.source_reference_id,
            "source_field": source.source_field,
            "source_locator_json": json.dumps(
                source.source_locator, ensure_ascii=False, separators=(",", ":")
            ) if source.source_locator is not None else None,
            "source_snapshot_text": snapshot,
            "source_hash": hashlib.sha256(snapshot.encode("utf-8")).hexdigest(),
            "sort_order": source.sort_order,
        }

    def delete(self, block_id):
        self.require_any(block_id)
        self.dao.delete(block_id)
        self.db.commit()


class CoursewareBlockSourceService:
    dao_type = CoursewareBlockSourceDAO

    def __init__(self, db):
        self.db = db
        self.dao = self.dao_type(db)


COURSEWARE_TABLE_SERVICE_TYPES = {
    "courseware_block": CoursewareBlockService,
    "courseware_block_source": CoursewareBlockSourceService,
}


class NoteCoursewareService:
    """Turns one English-note item into a reviewable, traceable courseware draft."""

    # Keep the source note untouched for traceability, but do not carry an
    # obvious typo into a learner-facing title, recap, dialogue, or exercise.
    _COURSEWARE_PHRASE_CORRECTIONS = {
        "fantarstic": "fantastic",
    }

    # A few older notes combine genuinely different headwords in one source
    # record.  Their source still remains one record, but each headword needs
    # its own learner-facing lesson.  These additions fill the gaps where the
    # original note only supplied an example for one of the headwords.
    _CURATED_SPLIT_ENTRY_CONTENT = {
        ("scraggly", "scraggle", "straggly"): {
            "scraggly": {
                "meaning": "乱糟糟的；参差不齐的",
                "explanation": "常用于头发、胡子、植物或灌木。",
                "examples": (
                    "He has a scraggly beard.\n"
                    "他的胡子乱糟糟的。\n\n"
                    "Scraggly bushes grew along the fence.\n"
                    "篱笆边长着参差不齐的灌木。"
                ),
            },
            "scraggle": {
                "meaning": "变得稀疏杂乱",
                "explanation": "多用于植物、枝条等变得零乱、稀疏。",
                "examples": (
                    "The vines began to scraggle over the fence.\n"
                    "藤蔓开始杂乱地沿着篱笆蔓生。"
                ),
            },
            "straggly": {
                "meaning": "稀疏杂乱的",
                "explanation": "常用于头发、植物或灌木，比 scraggly 更常见。",
                "examples": (
                    "After the dry summer, the garden looked straggly.\n"
                    "干燥的夏天过后，花园看起来稀疏又杂乱。"
                ),
            },
        },
    }

    # A thematic note can contain several expressions.  These cards practise
    # one phrase that genuinely occurs in the source rather than blanking an
    # artificial title such as "travel and airport set".
    _CURATED_PRACTICE_EXPRESSIONS = {
        35: "shocked by",
        57: "see how you guys get on",
        304: "drop the ball",
        380: "throw a party",
        582: "worthy of",
        599: "growth mindset",
        600: "excited but quiet inside",
        621: "key insight",
        622: "chip away",
        585: "make his evening easier",
        587: "make her day easier",
        692: "key insight",
        719: "hot mess",
        840: "an eye on",
        994: "in the meantime",
        1006: "brief overview",
        979: "trust",
        1015: "connecting flight",
        1012: "get through",
        1016: "hit the road",
        1027: "part-time job application",
        1206: "prop it against",
        1052: "have my eye on",
        1310: "hydro power",
        1473: "to put it in perspective",
        1486: "take it the wrong way",
        1493: "get our skates on",
        1640: "draw you into",
    }

    # These scenes replace pre-existing generated lines even if those lines
    # happen to pass a structural check.  Each had either an unrelated reply,
    # a vague prompt, or a theme label that concealed the actual expression.
    _SCENE_REPAIR_ITEM_IDS = {
        5, 12, 14, 16, 19, 25, 35, 57, 73, 96, 101, 128, 229, 239, 250,
        251, 256, 281, 286, 300, 304, 308, 314, 315, 316, 317, 325, 340,
        348, 366, 380, 406, 409, 439, 468, 504, 511, 515, 517, 519, 536,
        544, 569, 571, 572, 575, 577, 581, 582, 584, 585, 587, 597, 599,
        600, 612, 621, 622, 630, 632, 637, 644, 645, 649, 652, 658, 692, 699,
        712, 714, 715, 719, 720, 738, 762, 765, 777, 781, 798, 814, 815, 820,
        839, 840, 848, 874, 875, 876, 885, 895, 900, 904, 949, 950, 952,
        955, 966, 971, 972, 978, 979, 984, 987, 990, 994, 1006, 1012, 1015, 1016,
        1019, 1027, 1041, 1047, 1052, 1077, 1094, 1095, 1104, 1143, 1206,
        1212, 1223, 1289, 1310, 1320, 1366, 1374, 1397, 1445, 1456, 1472, 1473,
        1483, 1486, 1493, 1553, 1570, 1575, 1576, 1605, 1617, 1630, 1637,
        1640, 1680,
    }

    # Some old notes only supplied a headword or a broken frame.  These
    # sentences are hand-written, complete situations used solely to make a
    # meaningful blanked-output card; they are not vocabulary instructions.
    _CURATED_PRACTICE_SENTENCES = {
        73: "Can you pop in for a minute?",
        128: "Some older boys beat him up after school.",
        229: "I'm just chilling at home tonight.",
        250: "Daylight saving started on Sunday.",
        286: "Let me get the tape measure and check the width.",
        314: "The wind will disperse the dry leaves across the path.",
        316: "Use the sack barrow to move those boxes.",
        406: "Is that good for you?",
        409: "The silence after his joke was awkward.",
        468: "The road was blocked, hence creating a long delay.",
        572: "I commiserated with her after the bad news.",
        597: "I stumbled on the stairs.",
        599: "A growth mindset treats mistakes as part of learning.",
        600: "I feel excited but a little quiet inside.",
        658: "I'm pre-programming my brain by making the plan tonight.",
        814: "A mystery can engage the children's interest.",
        815: "They engaged her as a consultant.",
        874: "The city will auction off the old licences.",
        876: "The bakery will advertise the new menu online.",
        895: "He lost it during the argument.",
        904: "She fulfilled her promise.",
        994: "In the meantime, you can start the slides.",
        1015: "Our connecting flight leaves in an hour.",
        1016: "Let's hit the road before it gets dark.",
        1027: "I sent in my part-time job application yesterday.",
        1041: "They fell in love at first sight when they met.",
        1053: "We're renovating the house.",
        1094: "Narrate your life in English while you cook dinner.",
        1310: "The dam generates hydro power from water.",
        1397: "Our small idea evolved into a practical solution.",
        1456: "The same problem may recur unless we prevent a recurrence.",
        1473: "To put this in perspective, the mountain is three times higher than the nearby hills.",
        1570: "Mia has the responsibility to prepare it, and her manager has accountability for the result.",
        1576: "It all boils down to poor communication.",
        1617: "This class composes two other classes to share the work.",
        1630: "You did a fantastic job.",
    }

    # These split projections have a source-derived meaning and examples, but
    # their selected source lines are labels or fragments rather than a full
    # sentence that can be blanked.  Supply one concrete everyday situation
    # for the output card instead of falling back to a generic question.
    _CURATED_SPLIT_PRACTICE_SENTENCES = {
        (312, "happy"): "I felt happy when my friends surprised me with dinner.",
        (339, "integrate with"): "This calendar needs to integrate with our booking system.",
        (1010, "fabricate"): "He tried to fabricate an excuse for missing the meeting.",
        (1011, "deter someone from"): "The heavy rain did not deter us from going for a walk.",
        (880, "condom"): "We bought a condom at the pharmacy before the trip.",
        (898, "coincident"): "The two events were coincident, but they were not connected.",
        (752, "misguide"): "The unclear sign could misguide visitors at the station.",
        (752, "mislead"): "The advert may mislead customers about the price.",
        (436, "introvert"): "As an introvert, Mia prefers a quiet evening with a book.",
        (449, "spike"): "There was a sudden spike in electricity use during the heatwave.",
        (449, "buzz"): "The café has a cheerful buzz on Saturday mornings.",
        (596, "statue"): "A bronze statue stands in the middle of the town square.",
        (596, "sculpture"): "The gallery displayed a stone sculpture by the entrance.",
        (596, "idol"): "The singer became a teenage idol after the show.",
        (607, "sculpture"): "The museum bought a modern sculpture for its entrance.",
        (607, "idol"): "The footballer was an idol to local children.",
        (781, "the thing is"): "The thing is, the last bus leaves in ten minutes.",
        (541, "telescope"): "We used a telescope to look at the moon last night.",
        (541, "binoculars"): "Bring your binoculars if you want to watch the birds.",
        (541, "monocular"): "He carried a small monocular on the hiking trip.",
        (240, "housing"): "Affordable housing is hard to find near the city centre.",
        (240, "household"): "Every household received a recycling bin this week.",
        (299, "autobiography"): "She wrote an autobiography about her years at sea.",
        (299, "bibliography"): "Please add a bibliography at the end of your report.",
        (1161, "emerge"): "A new problem began to emerge after the storm.",
        (1161, "appear"): "A rainbow started to appear after the rain.",
    }

    # A split source often keeps examples for only one of its original
    # headwords.  These scenes cover the remaining projections with a real
    # two-turn situation, rather than forcing a verb or adjective into the
    # old catch-all “I noticed a …” reply.
    _CURATED_SPLIT_SCENES = {
        (369, "be heading to"): (
            "Are you leaving already?", "你这么快就要走了吗？",
            "Yes, I'm heading to the library before it closes.", "对，我要在图书馆关门前去那里。",
        ),
        (992, "lay down arms"): (
            "Has the fighting stopped at last?", "冲突终于停止了吗？",
            "The rebels agreed to lay down arms at noon.", "反叛者同意在中午放下武器。",
        ),
        (1003, "look forward to"): (
            "Are you excited about visiting your sister next weekend?", "你期待下周末去看姐姐吗？",
            "Yes, I'm really looking forward to seeing her.", "是的，我非常期待见到她。",
        ),
        (1005, "be educated at"): (
            "Where did your grandfather go to school?", "你爷爷在哪里上学？",
            "He was educated at a small boarding school in Wellington.", "他在惠灵顿的一所小型寄宿学校接受教育。",
        ),
        (1007, "narrow your eyes"): (
            "I can't read the sign in this sunlight.", "阳光太强了，我看不清这个牌子。",
            "Narrow your eyes a little and try again.", "稍微眯起眼睛再试试。",
        ),
        (1011, "deter someone from"): (
            "Did the rain make you cancel the walk?", "下雨让你取消散步了吗？",
            "No, it didn't deter us from going out.", "没有，它没让我们打消出门的念头。",
        ),
        (752, "misguide"): (
            "Which platform should we use for the train?", "我们该去哪个站台坐火车？",
            "Don't follow that old sign; it could misguide passengers.", "别跟着那块旧牌子走，它可能会误导乘客。",
        ),
        (449, "spike"): (
            "Why was the power bill so high this month?", "这个月的电费为什么这么高？",
            "There was a spike in electricity use during the heatwave.", "热浪期间用电量突然猛增。",
        ),
        (661, "rule out"): (
            "Could the noise be coming from the washing machine?", "这个声音会不会是洗衣机发出的？",
            "No, we can rule out the washing machine; it isn't running.", "不会，我们可以排除洗衣机，因为它没在运转。",
        ),
        (241, "ankle biters"): (
            "Why is the waiting room so noisy?", "候诊室为什么这么吵？",
            "Those ankle biters have been running around since breakfast.", "那些小不点从早餐后就一直跑来跑去。",
        ),
        (1161, "emerge"): (
            "Why are we checking the roof again?", "我们为什么又要检查屋顶？",
            "A new leak began to emerge after the storm.", "暴风雨过后开始出现新的漏水问题。",
        ),
        (339, "integrate with"): (
            "Will the new calendar work with our booking system?", "新日历能和我们的预约系统配合使用吗？",
            "Yes, it should integrate with it once we finish setup.", "可以，完成设置后它应该能与之集成。",
        ),
        (369, "be headed to"): (
            "Where are those cyclists going?", "那些骑自行车的人要去哪里？",
            "They're headed to the lake before sunset.", "他们正赶在日落前去湖边。",
        ),
        (992, "lay down the law"): (
            "Why are the kids suddenly so quiet?", "孩子们怎么突然这么安静？",
            "Dad is going to lay down the law about screen time tonight.", "爸爸今晚要严厉规定屏幕使用时间。",
        ),
        (993, "come down with a cold"): (
            "Why isn't Sam coming to work today?", "萨姆今天为什么没来上班？",
            "He's come down with a cold.", "他得感冒了。",
        ),
        (1010, "fabricate"): (
            "Why didn't he tell the truth about being late?", "他为什么不坦白迟到的原因？",
            "He tried to fabricate an excuse.", "他试图编造一个借口。",
        ),
        (1011, "put someone off"): (
            "Did the rude service change your mind about the restaurant?", "糟糕的服务改变了你去那家餐厅的想法吗？",
            "Yes, it really put me off.", "是的，它真的让我很反感。",
        ),
        (1017, "flush something down the toilet"): (
            "The sink won't drain. What happened?", "水槽下不了水，发生什么事了？",
            "Someone tried to flush a toy down the toilet.", "有人试图把一个玩具冲进马桶。",
        ),
        (1017, "be foreign to somebody"): (
            "Do you know how this old sewing machine works?", "你知道这台旧缝纫机怎么用吗？",
            "No, the controls are completely foreign to me.", "不知道，这些控制按钮我完全不熟悉。",
        ),
        (1017, "shut off"): (
            "Why is the room so dark?", "房间为什么这么暗？",
            "The power was shut off while they fixed the wiring.", "他们修电线时把电源关掉了。",
        ),
        (1018, "be scheduled for"): (
            "When is the parents' meeting?", "家长会是什么时候？",
            "It's scheduled for Thursday evening.", "安排在周四晚上。",
        ),
        (1018, "be scheduled to"): (
            "What time is the delivery due?", "快递预计几点到？",
            "It's scheduled to arrive before noon.", "安排在中午前送到。",
        ),
        (1018, "sign up for"): (
            "Are you joining the pottery class?", "你要参加陶艺课吗？",
            "Yes, I signed up for it yesterday.", "是的，我昨天报名了。",
        ),
        (1018, "figure out"): (
            "Can you solve the bus timetable?", "你能弄懂这张公交时刻表吗？",
            "Give me a minute—I'll figure out the timetable.", "给我一分钟，我会弄明白这张时刻表。",
        ),
        (880, "condom"): (
            "We forgot something at the pharmacy, didn't we?", "我们是不是忘了在药店买东西？",
            "Yes, we need to buy a condom before the trip.", "是的，出发前我们得买一个避孕套。",
        ),
        (880, "hydrogen peroxide"): (
            "How did the hairdresser lighten the dye?", "发型师是怎么把染发剂颜色变浅的？",
            "She used hydrogen peroxide to lighten it.", "她用双氧水把它漂浅。",
        ),
        (898, "coincident"): (
            "Did the two events happen at the same time?", "这两件事是同时发生的吗？",
            "Yes, they were coincident, but not connected.", "是的，它们碰巧同时发生，但并没有关联。",
        ),
        (752, "mislead"): (
            "Can I trust this advert's price?", "我能相信这个广告标的价格吗？",
            "Be careful—it may mislead customers about the final cost.", "要小心，它可能会误导顾客对最终价格的判断。",
        ),
        (410, "compassionate"): (
            "Why did Mia stay late to help the new neighbour?", "米娅为什么留下来帮助新邻居？",
            "She's very compassionate when someone needs support.", "有人需要帮助时，她很有同情心。",
        ),
        (425, "self-esteem"): (
            "Why did the coach praise the children after practice?", "教练为什么在训练后表扬孩子们？",
            "She wanted to build their self-esteem.", "她想建立他们的自信心。",
        ),
        (436, "introvert"): (
            "Why did Ben leave the party early?", "本为什么早早离开派对？",
            "He's an introvert and needs some quiet time.", "他是个内向的人，需要一点安静时间。",
        ),
        (449, "buzz"): (
            "Why is the café so lively today?", "咖啡馆今天为什么这么热闹？",
            "There's a real buzz because the market is on.", "市场开着，所以这里很有热闹的气氛。",
        ),
        (596, "statue"): (
            "What's in the middle of the town square?", "城镇广场中央有什么？",
            "A bronze statue of the town founder.", "一尊城镇创始人的铜像。",
        ),
        (596, "sculpture"): (
            "What did the gallery put by the entrance?", "画廊在入口旁放了什么？",
            "A stone sculpture from a local artist.", "一件当地艺术家的石雕。",
        ),
        (596, "idol"): (
            "Why are the teenagers waiting outside the theatre?", "青少年为什么在剧院外等着？",
            "Their pop idol is performing tonight.", "他们的流行偶像今晚演出。",
        ),
        (607, "sculpture"): (
            "What did you buy at the art fair?", "你在艺术展销会上买了什么？",
            "A small sculpture for the garden.", "一件放在花园里的小雕塑。",
        ),
        (607, "monument"): (
            "What is that tall structure by the river?", "河边那座高高的建筑是什么？",
            "It's a monument to the people who built the bridge.", "那是一座纪念建桥者的纪念碑。",
        ),
        (607, "idol"): (
            "Who does your little brother want to meet?", "你弟弟想见谁？",
            "His football idol is visiting the school.", "他的足球偶像要来学校。",
        ),
        (781, "the thing is"): (
            "Can we stay for another hour?", "我们能再待一个小时吗？",
            "The thing is, the last bus leaves in ten minutes.", "问题是，末班车十分钟后就开了。",
        ),
        (541, "telescope"): (
            "Can we see the moon's craters tonight?", "今晚我们能看到月球上的陨石坑吗？",
            "Yes, if we bring the telescope outside.", "可以，只要我们把望远镜带到外面。",
        ),
        (541, "binoculars"): (
            "How can I see the birds across the lake?", "我怎样才能看清湖对岸的鸟？",
            "Use these binoculars; they make the birds much clearer.", "用这副双筒望远镜，鸟会看得清楚很多。",
        ),
        (541, "monocular"): (
            "Why did you pack that small tube for the hike?", "你为什么带那个小圆筒去徒步？",
            "It's a monocular for watching distant birds.", "那是用来观察远处鸟类的单筒望远镜。",
        ),
        (240, "housing"): (
            "Why are young families moving farther from town?", "为什么年轻家庭搬到离市区更远的地方？",
            "Affordable housing is hard to find near the centre.", "市中心附近很难找到负担得起的住房。",
        ),
        (240, "household"): (
            "Who gets the new recycling bin?", "谁能拿到新的回收箱？",
            "Every household on this street gets one.", "这条街上的每户人家都有一个。",
        ),
        (274, "mineral"): (
            "What gives this water its unusual taste?", "这水为什么有特别的味道？",
            "It contains a lot of minerals from the spring.", "它含有很多来自泉水的矿物质。",
        ),
        (299, "autobiography"): (
            "What kind of book did the actor write?", "这位演员写的是什么书？",
            "An autobiography about her early years.", "一本关于她早年生活的自传。",
        ),
        (299, "bibliography"): (
            "What do I need to add after the last page of my report?", "我的报告最后一页后还要加什么？",
            "A bibliography that lists the books you used.", "列出你用过书籍的参考书目。",
        ),
        (1161, "appear"): (
            "What happened after the rain stopped?", "雨停后发生了什么？",
            "A rainbow began to appear over the hills.", "山丘上方开始出现一道彩虹。",
        ),
        (530, "for a special occasion"): (
            "Why are you wearing that dress today?", "你今天为什么穿那条裙子？",
            "I saved it for a special occasion.", "我把它留到特别的场合再穿。",
        ),
        (530, "rise to the occasion"): (
            "The host is sick. Can Maya handle the speech?", "主持人生病了，玛雅能应付这场演讲吗？",
            "Yes, she knows how to rise to the occasion.", "可以，她知道如何在关键时刻挺身而出。",
        ),
        (1024, "ceramic tile"): (
            "What are you using for the kitchen floor?", "厨房地面你们准备用什么材料？",
            "Each ceramic tile is easy to wipe clean.", "每块瓷砖都很容易擦干净。",
        ),
    }

    def __init__(self, db):
        self.db = db

    def list_notes(self):
        rows = self.db.execute(
            select(m.english_note).order_by(m.english_note.c.created_at.desc(), m.english_note.c.id.desc())
        ).mappings().all()
        return {"items": [dict(row) for row in rows]}

    def list_note_items(self, note_id):
        rows = self.db.execute(
            select(m.english_note_item)
            .where(m.english_note_item.c.note_id == note_id)
            .order_by(m.english_note_item.c.item_order, m.english_note_item.c.id)
        ).mappings().all()
        return {"items": [dict(row) for row in rows]}

    def _item(self, item_id):
        row = self.db.execute(
            select(m.english_note_item).where(m.english_note_item.c.id == item_id)
        ).mappings().first()
        if not row:
            raise HTTPException(404, "Note item not found.")
        return row

    @staticmethod
    def _lines(text):
        return [
            re.sub(r"^[🎯🧩💬📖🆚⚠️🧠]\s*", "", line).strip()
            for line in (text or "").splitlines()
            if line.strip()
        ]

    @staticmethod
    def _is_english(text):
        return bool(re.search(r"[A-Za-z]", text)) and not text.startswith(("=", "→"))

    @staticmethod
    def _is_chinese(text):
        return bool(re.search(r"[\u4e00-\u9fff]", text)) and not re.fullmatch(r"[A-Za-z0-9 /+,'’().-]+", text)

    @classmethod
    def _pairs(cls, text):
        lines = cls._lines(text)
        pairs = []
        for index in range(len(lines) - 1):
            english, chinese = lines[index], lines[index + 1]
            if cls._is_english(english) and cls._is_chinese(chinese):
                pairs.append({"english": english, "chinese": chinese})
        return pairs

    @staticmethod
    def _is_sentence(text):
        return bool(re.search(r"[.!?。！？]$", text)) or bool(
            re.match(r"^(?:I|We|You|He|She|They|It|There|This|That|Let|Please|Don['’]t)\b", text, re.I)
        )

    @staticmethod
    def _single_line(text):
        return re.sub(r"\s+", " ", (text or "")).strip()

    @classmethod
    def _source_phrase(cls, item):
        return (item.get("english_text") or item.get("raw_text") or item.get("item_title") or "").strip()

    @staticmethod
    def _word_count(text):
        return len(re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)?", text or ""))

    @classmethod
    def _is_long_card_text(cls, text):
        """Keep catalogue cards to a readable expression rather than a transcript."""
        value = cls._single_line(text)
        return cls._word_count(value) >= 13 or len(value) >= 72

    @classmethod
    def _is_sentence_like_label(cls, text):
        value = cls._single_line(text)
        lower = value.lower()
        if not value:
            return False
        if value.endswith(("...", "…")):
            words = re.findall(r"[a-z]+", lower)
            # A trailing ellipsis is useful for a phrase template such as
            # "give someone a tour of…", but it is usually a clipped sentence
            # when it ends in an ordinary content word.
            if not words or words[-1] not in {
                "about", "after", "around", "at", "by", "for", "from", "in", "into", "of",
                "on", "out", "over", "through", "to", "with", "without",
            }:
                return True
        if not value.endswith(("...", "…")) and re.search(r"[.!?](?:[\"”’)]*)$", value):
            return True
        if re.match(
            r"^(?:i|we|you|he|she|they|it|there|this|that|what|when|where|why|how|who|which|"
            r"can|could|would|will|do|does|did|have|has|had|am|are|is|was|were|let['’]s|"
            r"please|don['’]t|don't|my|your|his|her|our|their)\b",
            lower,
        ):
            return True
        return bool(re.search(
            r"(?:^|[,;:]\s*)(?:i|we|you|he|she|they|it|there|this|that)\s+"
            r"(?:am|are|is|was|were|have|has|had|do|does|did|can|could|will|would|should)\b",
            lower,
        ))

    @classmethod
    def _is_compact_card_label(cls, text):
        value = cls._single_line(text)
        if (
            not value
            or not cls._is_english(value)
            or bool(re.search(r"[\u4e00-\u9fff]", value))
            or cls._is_long_card_text(value)
            or cls._is_sentence_like_label(value)
        ):
            return False
        lower = value.lower()
        generic_label = (
            r"^(?:a |the )?(?:useful|common|key|important|natural)\s+"
            r"(?:chunk|chunks|piece|pieces|phrase|phrases|expression|expressions|sentence|sentences|"
            r"word|words|example|examples)\b"
        )
        return not re.search(generic_label, lower) and not re.search(
            r"\b(?:explanation|notes?|examples?)$", lower
        )

    @classmethod
    def _compact_item_title(cls, item):
        title = cls._single_line(item.get("item_title"))
        return title if cls._is_compact_card_label(title) else ""

    @classmethod
    def _is_sentence_source(cls, source):
        """Distinguish one long utterance from a set of short expressions."""
        if "/" in source or "|" in source:
            return False
        lines = [cls._single_line(line) for line in source.splitlines() if line.strip()]
        if len(lines) > 1:
            if len(lines) >= 4 and not cls._is_sentence_like_label(lines[0]):
                return False
            sentence_lines = [line for line in lines if cls._is_sentence_like_label(line)]
            return bool(sentence_lines) and len(sentence_lines) * 2 > len(lines)
        value = cls._single_line(source)
        lower = value.lower()
        if re.search(r"[.!?]", value) or cls._is_sentence_like_label(value):
            return True
        if re.match(
            r"^(?:after|although|as|because|before|but|if|last|once|since|so|sometimes|then|when|while|with)\b",
            lower,
        ):
            return True
        return bool(re.search(
            r"\b(?:i|we|you|he|she|they|it|there|this|that)\s+"
            r"(?:am|are|is|was|were|have|has|had|do|does|did|can|could|will|would|should)\b",
            lower,
        ))

    @classmethod
    def _collection_card_label(cls, source):
        """Give a multi-expression note a readable heading without inventing a new term."""
        parts = []
        for line in (source or "").splitlines() or [source]:
            parts.extend(re.split(r"\s*(?:/|\|)\s*", line))
        for part in parts:
            candidate = cls._single_line(cls._clean_source_line(part))
            if (
                cls._is_english(candidate)
                and not bool(re.search(r"[\u4e00-\u9fff]", candidate))
                and cls._word_count(candidate) <= 8
                and len(candidate) <= 42
            ):
                return candidate
        return "Phrase collection"

    @classmethod
    def normalise_courseware_phrase(cls, phrase):
        value = re.sub(r"\s+", " ", (phrase or "").strip())
        return cls._COURSEWARE_PHRASE_CORRECTIONS.get(value.casefold(), value)

    @classmethod
    def _card_phrase(cls, item):
        """Use a note's compact title when its English field also contains examples."""
        source = cls._strip_pronunciation_notation(cls._source_phrase(item))
        compact_title = cls._compact_item_title(item)
        single_source = cls._single_line(source)
        if compact_title and (
            "\n" in source
            or cls._is_long_card_text(source)
            or (
                single_source != compact_title
                and (
                    cls._is_sentence_like_label(single_source)
                    or len(single_source) > len(compact_title) + 12
                )
            )
        ):
            return cls.normalise_courseware_phrase(compact_title)
        if cls._is_long_card_text(source) and not cls._is_sentence_source(source):
            return cls.normalise_courseware_phrase(cls._collection_card_label(source))
        return cls.normalise_courseware_phrase(single_source)

    @classmethod
    def _expression_key(cls, text):
        return re.sub(r"\s+", " ", (text or "").strip()).casefold()

    @classmethod
    def _same_inflectional_headword(cls, terms):
        """Keep a singular/plural or regional-spelling pair on one card."""
        irregular_singular = {
            "men": "man", "women": "woman", "children": "child", "people": "person",
            "teeth": "tooth", "feet": "foot", "mice": "mouse", "geese": "goose",
            "stimuli": "stimulus", "analyses": "analysis", "crises": "crisis",
        }

        def word_forms(word):
            value = irregular_singular.get(word.casefold(), word.casefold())
            # Common UK/US spelling changes are variants of one headword, not
            # separate vocabulary lessons.
            forms = {value, value.replace("our", "or").replace("ise", "ize")}
            if value.endswith("ies") and len(value) > 4:
                forms.add(value[:-3] + "y")
            if value.endswith("es") and len(value) > 4:
                # Keep both possible stems: ``premises`` -> ``premise`` and
                # ``boxes`` -> ``box``.  The caller compares word forms rather
                # than trying to guess the one correct lemma in isolation.
                forms.update((value[:-1], value[:-2]))
            if value.endswith("s") and len(value) > 3 and not value.endswith(("ss", "us", "is")):
                forms.add(value[:-1])
            return {
                form.replace("our", "or").replace("ise", "ize")
                for form in forms
            }

        words_by_term = [
            re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)?", term)
            for term in terms
        ]
        if not words_by_term or not all(words_by_term):
            return False
        word_count = len(words_by_term[0])
        if any(len(words) != word_count for words in words_by_term):
            return False
        return all(
            set.intersection(*(word_forms(words[position]) for words in words_by_term))
            for position in range(word_count)
        )

    @classmethod
    def _strip_pronunciation_notation(cls, value):
        """Remove a trailing IPA transcription from a learner-facing headword."""
        value = cls._single_line(value)
        match = re.match(r"^(?P<label>.+?)\s*/\s*(?P<ipa>[^/]+)\s*/\s*$", value)
        if not match:
            return value
        ipa = match.group("ipa")
        # IPA often contains Latin-looking letters too (for example ``ren``
        # in /ˈrenəveɪt/), but its distinctive symbols and lack of spaces make
        # it unambiguously a pronunciation rather than a second expression.
        if re.search(r"[ˈˌːəɪʊɛæɑɔɜŋθðʃʒɹɾʔ]", ipa) and not re.search(r"\s", ipa):
            return match.group("label").strip()
        return value

    @classmethod
    def _collection_expression_terms(cls, item):
        """Return every slash- or pipe-separated expression in a source label.

        Unlike ``_split_expression_terms``, this is an audit helper.  It also
        sees incomplete frames and sentence fragments so generation can refuse
        to turn a whole collection into one learner-facing card.
        """
        source = cls._strip_pronunciation_notation(cls._source_phrase(item))
        if not re.search(r"[|/]", source):
            return []
        parts = [cls._single_line(part) for part in re.split(r"\s*(?:/|\|)\s*", source)]
        if not 2 <= len(parts) <= 8 or any(not part for part in parts):
            return []
        for part in parts:
            if bool(re.search(r"[\u4e00-\u9fff]", part)) or len(part) > 100:
                return []
            if not re.search(r"(?:[A-Za-z]|\d)", part):
                return []
        return parts

    @classmethod
    def has_unresolved_expression_collection(cls, item):
        """Whether a note would otherwise create one card for several entries."""
        return bool(
            cls._collection_expression_terms(item)
            and not cls._split_expression_entries(item)
        )

    @classmethod
    def _split_expression_terms(cls, item):
        """Return a compact slash-separated series of standalone expressions.

        A slash alone is not enough to split a card: notes also use it for a
        single expression's alternatives and translations.  The caller only
        proceeds when each term can be matched to an explicit source meaning.
        """
        source = cls._source_phrase(item)
        if not source or "\n" in source or not re.search(r"[|/]", source):
            return []
        terms = [cls._single_line(part) for part in re.split(r"\s*(?:/|\|)\s*", source)]
        if not 2 <= len(terms) <= 8 or any(not term for term in terms):
            return []
        for term in terms:
            words = re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)?", term)
            if (
                not words
                or len(words) > 8
                or len(term) > 64
                or bool(re.search(r"[\u4e00-\u9fff]", term))
                or cls._is_sentence_like_label(term)
            ):
                return []
        keys = [cls._expression_key(term) for term in terms]
        if len(set(keys)) != len(keys) or cls._same_inflectional_headword(terms):
            return []
        return terms

    @classmethod
    def _explicit_term_definitions(cls, text, terms):
        """Read ``term = Chinese definition`` pairs without guessing meanings."""
        if not text or not terms:
            return {}
        alternatives = "|".join(re.escape(term) for term in sorted(terms, key=len, reverse=True))
        pattern = re.compile(
            rf"(?<![A-Za-z])(?P<term>{alternatives})(?![A-Za-z])\s*(?:=|:|：)\s*",
            re.I,
        )
        matches = list(pattern.finditer(text))
        definitions = {}
        for index, match in enumerate(matches):
            term = next(
                (
                    candidate
                    for candidate in terms
                    if cls._expression_key(candidate) == cls._expression_key(match.group("term"))
                ),
                None,
            )
            if term is None:
                continue
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            definition = text[match.end():end].strip().strip("。；; \t\r\n")
            if definition and cls._is_chinese(definition):
                definitions[cls._expression_key(term)] = definition
        return definitions if len(definitions) == len(terms) else {}

    @classmethod
    def _short_term_definition(cls, value):
        """Keep a source-provided Chinese label usable as a card meaning."""
        value = cls._single_line(value).strip("：:；;，、。 ")
        if not value or not cls._is_chinese(value):
            return ""
        # Section labels such as “常见搭配” and “例句” describe the note,
        # not the expression.  They must never become a learner-facing meaning.
        if re.search(
            r"(?:例句|常见(?:用法|搭配|结构)|一句话|记忆|场景|使用说明|小提醒|拼写|读音)",
            value,
        ):
            return ""
        value = re.split(r"[。！？]", value, maxsplit=1)[0].strip("：:；;，、。 ")
        if len(value) > 44:
            cut_points = [index for index, char in enumerate(value[:45]) if char in "，；："]
            value = value[:cut_points[-1] if cut_points else 44].rstrip("：:；;，、。 ")
        return value

    @classmethod
    def _structured_term_definitions(cls, text, terms):
        """Read labelled note sections such as ``delighted`` under ``正式、礼貌``.

        Older notes often record a compact group of headwords with Chinese
        section headings instead of writing every row as ``word = meaning``.
        The headings and the terms are still explicit source content, so they
        are safe to project into separate cards.  This deliberately does not
        infer a definition from a bare example sentence.
        """
        explicit = cls._explicit_term_definitions(text, terms)
        if explicit:
            return explicit
        if not text or not terms:
            return {}

        term_by_key = {cls._expression_key(term): term for term in terms}

        def leading_term(line):
            cleaned = re.sub(r"^(?:\d+\s*[.、）)]\s*|[-•*]\s*)+", "", line).strip()
            for key, term in sorted(term_by_key.items(), key=lambda pair: len(pair[1]), reverse=True):
                if re.match(rf"^{re.escape(term)}(?:\s*(?:[:：=]|强调|表示|指|是|更像|偏|用于|作)\s*|$)", cleaned, re.I):
                    return key, cleaned[len(term):].strip()
            return None, ""

        definitions = {}
        current_label = ""
        pending_key = None
        lines = cls._lines(text)
        for line in lines:
            key, remainder = leading_term(line)
            if key is not None:
                inline = re.sub(r"^(?:[:：=]|强调|表示|指|是|更像|偏|用于|作)\s*", "", remainder)
                definition = cls._short_term_definition(inline)
                if definition:
                    definitions[key] = definition
                    pending_key = None
                else:
                    if current_label:
                        definitions.setdefault(key, current_label)
                    pending_key = key
                continue

            # A Chinese-only heading remains in effect for all following
            # headwords until another heading appears.  This handles groups
            # such as “日常小开心／通用： happy, glad”.
            if cls._is_chinese(line) and not any(
                cls._term_occurs_in(line, term) for term in terms
            ):
                definition = cls._short_term_definition(line)
                if pending_key is not None and definition:
                    definitions.setdefault(pending_key, definition)
                    pending_key = None
                if definition:
                    current_label = definition

        return definitions if len(definitions) == len(terms) else {}

    @classmethod
    def _term_occurs_in(cls, text, term):
        escaped = re.escape(cls._single_line(term))
        return bool(re.search(rf"(?<![A-Za-z]){escaped}(?![A-Za-z])", text or "", re.I))

    @classmethod
    def _matching_example_lines(cls, text, phrase):
        """Keep only source examples that actually use this split expression."""
        lines = (text or "").splitlines()
        selected = []
        for index, line in enumerate(lines):
            if not cls._term_occurs_in(line, phrase):
                continue
            selected.append(line)
            if index + 1 < len(lines) and cls._is_chinese(lines[index + 1].strip()):
                selected.append(lines[index + 1])
        return "\n".join(selected).strip()

    @classmethod
    def _split_entry_override(cls, terms, phrase):
        signature = tuple(cls._expression_key(term) for term in terms)
        return cls._CURATED_SPLIT_ENTRY_CONTENT.get(signature, {}).get(
            cls._expression_key(phrase), {}
        )

    @classmethod
    def _split_expression_entries(cls, item):
        """Create independently teachable projections of a multi-headword note.

        Splitting is deliberately conservative: every expression must have an
        explicit Chinese definition in the source.  This keeps spelling
        variants and loosely related collections intact until they have enough
        source detail for separate teaching cards.
        """
        terms = cls._split_expression_terms(item)
        if not terms:
            return []
        definitions = next(
            (
                parsed
                for field in ("chinese_text", "explanation", "examples")
                if (parsed := cls._structured_term_definitions(item.get(field) or "", terms))
            ),
            {},
        )
        if not definitions:
            return []
        source_phrase = cls._single_line(cls._source_phrase(item))
        entries = []
        for index, phrase in enumerate(terms):
            key = cls._expression_key(phrase)
            override = cls._split_entry_override(terms, phrase)
            explanation = (item.get("explanation") or "").strip()
            other_terms = [term for term in terms if cls._expression_key(term) != key]
            if any(cls._term_occurs_in(explanation, term) for term in other_terms):
                explanation = "\n".join(
                    line for line in explanation.splitlines() if cls._term_occurs_in(line, phrase)
                ).strip()
            projected = {
                **dict(item),
                "item_title": phrase,
                "raw_text": phrase,
                "english_text": phrase,
                "chinese_text": override.get("meaning") or definitions[key],
                "explanation": override.get("explanation") or explanation,
                "examples": override.get("examples") or cls._matching_example_lines(
                    item.get("examples") or "", phrase
                ),
            }
            entries.append({
                "index": index,
                "phrase": phrase,
                "source_item": dict(item),
                "item": projected,
                "source_locator": {
                    "kind": "split_expression",
                    "index": index,
                    "count": len(terms),
                    "phrase": phrase,
                    "source_phrase": source_phrase,
                },
            })
        return entries

    @classmethod
    def item_for_existing_phrase(cls, source_item, phrase):
        """Use the projected split entry when repairing an already split lesson."""
        expression_key = cls._expression_key(phrase)
        for entry in cls._split_expression_entries(source_item):
            if cls._expression_key(entry["phrase"]) == expression_key:
                return dict(entry["item"])
        return dict(source_item)

    @classmethod
    def is_long_sentence_item(cls, item):
        """Exclude a long complete utterance, while retaining a collection of phrases."""
        phrase = cls._card_phrase(item)
        return cls._is_long_card_text(phrase) and cls._is_sentence_source(cls._source_phrase(item))

    @classmethod
    def _usage_source_lines(cls, text):
        """Keep the source order while removing note-only decoration from a line."""
        lines = []
        for raw in (text or "").splitlines():
            raw = raw.strip()
            if not raw:
                continue
            value = cls._single_line(cls._clean_source_line(raw))
            # Most notes introduce a section with an emoji.  Strip decoration
            # but leave numbered headings such as ``1. take down a post`` intact.
            value = re.sub(r"^[^\w\u4e00-\u9fff①②③④⑤⑥⑦⑧⑨⑩]+", "", value).strip()
            if value and value != "⸻":
                lines.append((raw, value))
        return lines

    @classmethod
    def _numbered_usage_heading(cls, line):
        """Return a numbered usage heading as ``(number, title)`` when present."""
        circled_numbers = {char: index for index, char in enumerate("①②③④⑤⑥⑦⑧⑨⑩", start=1)}
        match = re.match(
            r"^(?:(?P<circled>[①②③④⑤⑥⑦⑧⑨⑩])|(?P<arabic>\d{1,2})\s*[.、)）:：\-–—])\s*(?P<title>.+)$",
            line or "",
        )
        if not match:
            match = re.match(r"^(?:用法|含义|意思|结构)\s*(?P<arabic>\d{1,2})\s*[：:]\s*(?P<title>.+)$", line or "")
        if not match:
            return None
        number = circled_numbers.get(match.groupdict().get("circled"))
        if number is None:
            number = int(match.group("arabic"))
        return number, match.group("title").strip()

    @classmethod
    def _usage_title(cls, value):
        value = cls._single_line(cls._clean_source_line(value))
        value = re.sub(r"^[^\w\u4e00-\u9fff]+", "", value).strip()
        numbered = cls._numbered_usage_heading(value)
        if numbered:
            value = numbered[1]
            value = re.sub(r"^[^\w\u4e00-\u9fff]+", "", value).strip()
        value = re.sub(r"^(?:用法|含义|意思|结构)\s*\d*\s*[：:]\s*", "", value).strip()
        return value.strip("：:；;。.!！?？ ")

    @classmethod
    def _is_usage_section_break(cls, raw, line):
        """Do not turn comparisons, cautions, and memory notes into use cards."""
        lower = (line or "").lower()
        if any(marker in (raw or "") for marker in ("🆚", "⚠", "🧠", "📖", "🔍")):
            return True
        if re.search(
            r"^(?:原句解析|近义词|易混|对比(?:学习)?|常见错误|易错点|记忆(?:方法|画面)?|发音|来源|"
            r"自然口语|口语表达|一句话记)",
            line or "",
        ):
            return True
        return bool(re.search(
            r"^(?:natural spoken|common mistakes|memory tip|pronunciation|sentence analysis|"
            r"comparison|sources?)\b",
            lower,
        ))

    @classmethod
    def _is_secondary_usage_section(cls, line):
        """A new broad section should not be attached to the last meaning."""
        return cls._usage_title(line).lower() in {
            "common usage", "common patterns", "common structures", "常见搭配", "常见结构",
        }

    @classmethod
    def _is_generic_usage_heading(cls, value):
        title = cls._usage_title(value)
        lower = title.lower()
        if not title:
            return True
        if re.fullmatch(
            r"(?:不同含义与)?常见(?:用法|结构|搭配)?|核心(?:意思|含义|感觉)?|"
            r"中文意思|例句(?: examples)?|中英双语例句|不同含义与常见用法|"
            r"common (?:usage|patterns|structures)|different meanings(?: and common usage)?|"
            r"examples?|key (?:meaning|idea)|meaning|structure",
            lower,
        ):
            return True
        if title in {
            "意思", "含义", "用法", "结构", "常见搭配", "重点", "例句", "口语感觉",
            "解释", "提示", "补充说明", "例", "例如", "常见例句", "你的原句", "句型",
            "你刚才那句", "或者", "拆开理解", "合起来",
        }:
            return True
        return lower in {"simple understanding", "interview sentence", "for example", "example", "examples"}

    @classmethod
    def _has_following_sentence_pair(cls, lines, index):
        """A short heading is useful only when its own bilingual example follows."""
        for cursor in range(index + 1, min(len(lines) - 1, index + 6)):
            raw, english = lines[cursor]
            if cls._is_usage_section_break(raw, english):
                return False
            _, chinese = lines[cursor + 1]
            if (
                cls._is_english(english)
                and not cls._is_chinese(english)
                and cls._is_chinese(chinese)
                and (
                    cls._is_sentence(english)
                    or (
                        cls._word_count(english) <= 8
                        and not cls._is_sentence_like_label(english)
                        and not cls._is_generic_usage_heading(english)
                    )
                )
            ):
                return True
        return False

    @classmethod
    def _has_following_full_sentence_pair(cls, lines, index):
        """Find an actual example sentence, not merely the next collocation label."""
        for cursor in range(index + 1, min(len(lines) - 1, index + 7)):
            raw, english = lines[cursor]
            if cls._is_usage_section_break(raw, english):
                return False
            if cls._usage_title(english).lower() in {"例", "例如", "例句", "for example", "example"}:
                return False
            _, chinese = lines[cursor + 1]
            if (
                cls._is_english(english)
                and not cls._is_chinese(english)
                and cls._is_chinese(chinese)
                and cls._is_sentence(english)
            ):
                return True
        return False

    @classmethod
    def _is_chinese_usage_heading(cls, lines, index):
        _, line = lines[index]
        title = cls._usage_title(line)
        previous = lines[index - 1][1] if index else ""
        numbered = cls._numbered_usage_heading(line)
        if (
            not cls._is_chinese(title)
            or bool(re.search(r"[A-Za-z]", title))
            or (not numbered and cls._is_english(previous))
            or len(title) > 48
            or (
                line.endswith(("。", "！", "？", ".", "!", "?"))
                and "：" not in line
                and ":" not in line
            )
            or cls._is_generic_usage_heading(title)
        ):
            return False
        if re.match(
            r"^(?:这|也|因为|所以|比如|例如|注意|不要|如果|通常|主要|不过|但是|而且|另外|"
            r"可以|最|很|更|还有|然后|因此)",
            title,
        ):
            return False
        return cls._has_following_sentence_pair(lines, index)

    @classmethod
    def _english_usage_heading(cls, lines, index, numbered=None):
        """Return an English use heading and its adjacent Chinese definition."""
        _, line = lines[index]
        number, raw_title = numbered or (None, line)
        title = raw_title
        title = cls._usage_title(title)
        if (
            not title
            or cls._is_chinese(title)
            or not cls._is_english(title)
            or len(title) > 80
            or cls._word_count(title) > 12
            or cls._is_generic_usage_heading(title)
        ):
            return None
        # A numbered line is often a sentence-shaped pattern (for example,
        # "What have you been up to?").  A long normal sentence, however, is
        # more likely a numbered example than a heading.
        source_looks_like_sentence = (
            cls._is_sentence(raw_title)
            or cls._is_sentence_like_label(raw_title)
            or bool(re.search(r"[.!?。！？]$", raw_title))
        )
        if number is None and source_looks_like_sentence:
            return None
        if number is not None and source_looks_like_sentence and cls._word_count(title) > 7:
            return None

        next_line = lines[index + 1][1] if index + 1 < len(lines) else ""
        if cls._numbered_usage_heading(next_line):
            return None
        if cls._is_chinese(next_line):
            next_title = cls._usage_title(next_line)
            if next_title in {"意思", "含义", "中文意思", "核心意思", "解释", "用法"}:
                for cursor in range(index + 2, min(len(lines), index + 5)):
                    candidate = lines[cursor][1]
                    if cls._is_chinese(candidate) and not cls._is_generic_usage_heading(candidate):
                        return {
                            "number": number,
                            "title": title,
                            "description": candidate,
                            "skip": cursor - index + 1,
                        }
                    if cls._is_english(candidate):
                        break
                return {"number": number, "title": title, "description": "", "skip": 2}
            if next_title in {"例句", "中英双语例句", "examples"}:
                return {"number": number, "title": title, "description": "", "skip": 2}
            return {"number": number, "title": title, "description": next_line, "skip": 2}
        if (
            index + 2 < len(lines)
            and cls._is_english(next_line)
            and cls._is_sentence(next_line)
            and cls._is_chinese(lines[index + 2][1])
        ):
            return {"number": number, "title": title, "description": "", "skip": 1}
        if number is not None and cls._has_following_sentence_pair(lines, index):
            return {"number": number, "title": title, "description": "", "skip": 1}
        return None

    @classmethod
    def _numbered_meaning_hints(cls, item):
        """Use the note's numbered Chinese definitions for pattern-card descriptions."""
        hints = {}
        for _, line in cls._usage_source_lines((item or {}).get("chinese_text") or ""):
            numbered = cls._numbered_usage_heading(line)
            if not numbered:
                continue
            number, title = numbered
            title = cls._usage_title(title)
            if (
                number not in hints
                and cls._is_chinese(title)
                and len(title) <= 60
                and not title.endswith(("。", "！", "？"))
                and not cls._is_generic_usage_heading(title)
            ):
                hints[number] = title
        return hints

    @classmethod
    def _expression_meaning_hints(cls, item):
        """Read concise ``expression = Chinese meaning`` lines from a source note."""
        hints = {}
        for source in ((item or {}).get("explanation") or "", (item or {}).get("chinese_text") or ""):
            for _, line in cls._usage_source_lines(source):
                match = re.match(r"^(?P<expression>[A-Za-z][A-Za-z0-9 /+'’().-]{0,70}?)\s*=\s*(?P<meaning>.+)$", line)
                if not match:
                    continue
                expression = cls._usage_title(match.group("expression"))
                meaning = cls._usage_title(match.group("meaning"))
                if (
                    expression
                    and cls._is_chinese(meaning)
                    and len(meaning) <= 64
                    and expression.casefold() not in hints
                ):
                    hints[expression.casefold()] = meaning
        return hints

    @classmethod
    def _usage_description(cls, title, explicit, number, hints, expression_hints):
        description = cls._usage_title(explicit)
        if cls._is_chinese(description):
            return description[:64].rstrip("，、；：")
        if number in hints:
            return hints[number]
        if title.casefold() in expression_hints:
            return expression_hints[title.casefold()]
        if cls._is_chinese(title):
            return title[:64].rstrip("，、；：")
        return f"按“{title}”这个结构使用。"

    @classmethod
    def _structured_usage_groups(cls, text, item=None):
        """Split numbered and contextual meanings into separate, teachable use cards."""
        lines = cls._usage_source_lines(text)
        hints = cls._numbered_meaning_hints(item)
        expression_hints = cls._expression_meaning_hints(item)
        groups, current = [], None

        def finish_current():
            nonlocal current
            if current and current["examples"]:
                seen = set()
                current["examples"] = [
                    pair for pair in current["examples"]
                    if not ((key := (pair["english"], pair["chinese"])) in seen or seen.add(key))
                ]
                groups.append(current)
            current = None

        index = 0
        while index < len(lines):
            raw, line = lines[index]
            if cls._is_usage_section_break(raw, line):
                break
            if current and cls._is_secondary_usage_section(line):
                break

            numbered = cls._numbered_usage_heading(line)
            heading = cls._english_usage_heading(lines, index, numbered)
            if heading and current and heading["description"]:
                following = lines[index + 2][1] if index + 2 < len(lines) else ""
                if (
                    cls._usage_title(following).lower() in {"例", "例如", "例句", "for example", "example"}
                    or not cls._has_following_full_sentence_pair(lines, index)
                ):
                    heading = None
            if heading:
                finish_current()
                current = {
                    "title": heading["title"],
                    "description": cls._usage_description(
                        heading["title"], heading["description"], heading["number"], hints, expression_hints
                    ),
                    "examples": [],
                }
                index += heading["skip"]
                continue

            if cls._is_chinese_usage_heading(lines, index):
                finish_current()
                title = cls._usage_title(line)
                current = {
                    "title": title,
                    "description": cls._usage_description(title, title, None, hints, expression_hints),
                    "examples": [],
                }
                index += 1
                continue

            next_line = lines[index + 1][1] if index + 1 < len(lines) else ""
            if cls._is_english(line) and not cls._is_chinese(line) and cls._is_chinese(next_line):
                if current:
                    current["examples"].append({"english": line, "chinese": next_line})
                index += 2
                continue
            index += 1
        finish_current()

        merged = []
        for group in groups:
            existing = next(
                (candidate for candidate in merged if candidate["title"].casefold() == group["title"].casefold()),
                None,
            )
            if existing is None:
                merged.append(group)
                continue
            known = {(pair["english"], pair["chinese"]) for pair in existing["examples"]}
            existing["examples"].extend(
                pair for pair in group["examples"]
                if (pair["english"], pair["chinese"]) not in known
            )
        return merged if len(merged) >= 2 else []

    @classmethod
    def _usage_groups(cls, text, fallback_pairs, item=None, additional_text=""):
        """Read the note's usage headings as teaching cards, rather than one raw example list."""
        raw_lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
        groups, current = [], None
        index = 0
        while index < len(raw_lines):
            heading = re.match(r"^[🧩💰🛠️🕵️🧭💞]\s*用法\s*\d*\s*[：:]\s*(.+)$", raw_lines[index])
            if heading:
                if current:
                    groups.append(current)
                current = {"title": heading.group(1), "description": "", "examples": []}
                index += 1
                continue
            line = raw_lines[index]
            next_line = raw_lines[index + 1] if index + 1 < len(raw_lines) else ""
            if current and cls._is_english(line) and not cls._is_sentence(line) and not current["description"]:
                current["description"] = line
            if current and cls._is_english(line) and cls._is_chinese(next_line):
                current["examples"].append({"english": line, "chinese": next_line})
                index += 2
                continue
            index += 1
        if current:
            groups.append(current)
        groups = [
            {**group, "description": group["description"] or group["title"]}
            for group in groups
            if group["examples"]
        ]
        if groups:
            return groups

        # Older notes frequently use plain numbered headings or a Chinese
        # scenario label rather than the newer "🧩 用法 N" notation.  Parse
        # those first so distinct senses do not collapse into one generic card.
        structured_groups = []
        for source in (text, additional_text, (item or {}).get("chinese_text") or ""):
            structured = cls._structured_usage_groups(source, item)
            if structured:
                structured_groups = structured
                break

        lines = cls._lines(text)
        groups, current = [], None
        index = 0
        while index < len(lines):
            line = lines[index]
            next_line = lines[index + 1] if index + 1 < len(lines) else ""
            if cls._is_english(line) and cls._is_chinese(next_line) and not cls._is_sentence(line):
                if current and current["examples"]:
                    groups.append(current)
                current = {"title": line, "description": next_line, "examples": []}
                index += 2
                continue
            if cls._is_english(line) and cls._is_chinese(next_line):
                if current is None:
                    current = {"title": "在句子中使用", "description": "放进真实表达里理解。", "examples": []}
                current["examples"].append({"english": line, "chinese": next_line})
                index += 2
                continue
            index += 1
        if current and current["examples"]:
            groups.append(current)
        if groups:
            # Keep a richer pre-existing section split when a note has both
            # styles.  The structured parser is preferred whenever it finds at
            # least as many distinct cards, which avoids collapsing content
            # while still repairing one-card multi-meaning entries.
            if structured_groups and len(structured_groups) >= len(groups):
                return structured_groups
            return groups
        if structured_groups:
            return structured_groups
        return [{
            "title": "核心用法",
            "description": "结合原笔记中的句子理解这个表达。",
            "examples": fallback_pairs[:2],
        }] if fallback_pairs else []

    @classmethod
    def _comparison_items(cls, text):
        lines = [line.strip() for line in (text or "").splitlines() if line.strip()]
        headers, pairs = [], []
        for index, line in enumerate(lines[:-1]):
            line = re.sub(r"^[🎯🧩💬📖🆚⚠️🧠]\s*", "", line)
            if "记忆" in line:
                break
            next_line = lines[index + 1]
            if " vs " in line.lower():
                continue
            if cls._is_english(line) and cls._is_chinese(next_line):
                if cls._is_sentence(line):
                    pairs.append({"english": line, "chinese": next_line})
                elif len(headers) < 2:
                    headers.append({"expression": line, "meaning": re.sub(r"^👉\s*", "", next_line)})
        return [
            {
                **header,
                "label": "易混表达",
                "english": pair["english"],
                "chinese": pair["chinese"],
            }
            for header, pair in zip(headers, pairs[:2])
        ]

    @classmethod
    def _memory(cls, item, meaning):
        lines = cls._lines(item["examples"] or "")
        memory_start = next(
            (i for i, line in enumerate(lines) if "记忆" in line or "memory" in line.lower()),
            None,
        )
        candidates = lines[memory_start + 1:] if memory_start is not None else []
        return next((line for line in candidates if line and len(line) <= 72), meaning)

    @classmethod
    def _brief_meaning(cls, item, fallback):
        """Extract a definition that can be read at a glance on a lesson card."""
        headings = {
            "核心意思", "中文意思", "词性", "类型", "结构", "发音", "记忆", "常见用法", "例句",
            "相近词", "核心语气", "常见句型", "自然口语", "一句话记忆",
        }
        skipped_prefixes = (
            "注意", "想象", "常见", "例句", "这个意思", "这种用法", "不是", "核心语气",
        )

        def clean(line):
            value = cls._single_line(cls._clean_source_line(line))
            value = re.sub(r"^[^A-Za-z\u4e00-\u9fff]+", "", value)
            value = re.sub(
                r"^(?:中文意思|核心意思|核心含义|释义|含义|意思|更自然(?:的)?(?:表达|说法))\s*[：:]?\s*",
                "",
                value,
                flags=re.I,
            )
            value = re.sub(r"^\d+\s*[.、）)]\s*", "", value)
            if "=" in value:
                leading, definition = value.split("=", 1)
                if not cls._is_chinese(leading) and cls._is_chinese(definition):
                    value = definition.strip()
            if not value or value in headings or not cls._is_chinese(value):
                return ""
            lower = value.lower()
            if value.startswith(skipped_prefixes) or re.search(
                r"(?:有|是).{0,12}(?:常见)?(?:意思|含义)", value
            ) and bool(re.search(r"[a-z]", lower)):
                return ""
            value = re.split(r"[。！？]", value, maxsplit=1)[0].strip(" ，、；：")
            if len(value) > 44:
                cut_points = [
                    index for index, char in enumerate(value[:45]) if char in "，；："
                ]
                value = value[:cut_points[-1] if cut_points else 44].rstrip(" ，、；：")
            return value

        for line in cls._lines(item.get("chinese_text") or ""):
            value = clean(line)
            if value:
                return value
        for line in cls._lines(fallback):
            value = clean(line)
            if value:
                return value
        fallback = cls._single_line(fallback)
        if not cls._is_chinese(fallback):
            return "日常沟通中的常用表达"
        fallback = re.split(r"[。！？]", fallback, maxsplit=1)[0].strip(" ，、；：")
        return fallback[:44].rstrip(" ，、；：") or "这个表达的常用意思"

    @classmethod
    def _recap_summary(cls, phrase, meaning):
        expression = cls._single_line(phrase)
        definition = cls._single_line(meaning).rstrip("。！？；：，、 ")
        if expression == "Phrase collection":
            return "本课整理了一组常用表达，可结合例句理解。"
        variants = [
            item.strip() for item in re.split(r"\s*(?:/|\||;|；)\s*", expression) if item.strip()
        ]
        if len(variants) > 1:
            label = variants[0]
            if len(label) <= 42:
                return f"本课聚焦“{label}”等常用表达，可结合例句理解。"
            return "本课聚焦几个常用表达，可结合例句理解。"
        if definition == "日常沟通中的常用表达":
            return "这个表达常用于日常沟通。"
        if len(expression) <= 32:
            return f"“{expression}”表示{definition}。"
        return f"这个表达表示{definition}。"

    @classmethod
    def _dialogue_meaning(cls, item, fallback):
        """Pick one concise Chinese meaning for a generated everyday fallback."""
        def shorten(text):
            if len(text) <= 80:
                return text
            excerpt = text[:80]
            sentence_end = max(excerpt.rfind(mark) for mark in "。！？；")
            return (excerpt[: sentence_end + 1] if sentence_end >= 20 else excerpt).rstrip("，、；：")

        headings = {"核心意思", "词性", "类型", "结构", "发音", "记忆", "常见用法", "例句", "相近词"}
        for line in cls._lines(item["chinese_text"] or ""):
            candidate = re.sub(r"^[^A-Za-z\u4e00-\u9fff]+", "", line)
            candidate = re.sub(r"^(?:核心意思|中文意思|核心含义)\s*[：:]?\s*", "", candidate)
            if candidate in headings or not cls._is_chinese(candidate):
                continue
            return shorten(candidate)
        fallback_line = next((line for line in cls._lines(fallback) if cls._is_chinese(line)), fallback)
        return shorten(fallback_line)

    @staticmethod
    def _dialogue_choice(phrase, options, salt):
        index = int(hashlib.sha256(f"{phrase}:{salt}".encode("utf-8")).hexdigest(), 16) % len(options)
        return options[index]

    @staticmethod
    def _clean_source_line(line):
        """Remove note markup without changing the English or Chinese sentence."""
        return re.sub(r"^(?:[•*\-✅❌👉✏️💬🧩🧠📌⚠️⭐🔄]+\s*)+", "", (line or "").strip())

    @classmethod
    def _clean_scene_chinese(cls, text, fallback):
        value = cls._clean_source_line(text)
        value = re.sub(r"^[^A-Za-z\u4e00-\u9fff]+", "", value)
        if not cls._is_chinese(value) or len(value) > 220:
            return fallback
        return value

    @staticmethod
    def _is_definition_style_scene_sentence(sentence):
        """Reject dictionary glosses before they become a learner dialogue turn.

        A phrase such as ``photography means the art of taking photos`` is
        useful source material for a definition card, but it is not something
        one person naturally says in response to another person in a scene.
        Pronoun-led clauses are deliberately excluded so ordinary lines such
        as ``It means a lot to me`` remain valid speech.
        """
        lower = re.sub(r"\s+", " ", (sentence or "").strip()).lower()
        if not lower:
            return False
        if re.match(
            r"^(?!(?:i|we|you|he|she|they|it|this|that|there|the|a|an)\b)"
            r"[a-z][a-z0-9'’\- ]{0,72}\s+(?:usually\s+)?"
            r"(?:means?|refers to|is short for)\b",
            lower,
        ):
            return True
        return bool(re.match(
            r"^the\s+(?:word|term|phrase|expression)\b.*\b(?:means?|refers to)\b",
            lower,
        ))

    @classmethod
    def _english_sentences(cls, text):
        """Return standalone English utterances from one note line."""
        value = cls._clean_source_line(text)
        if not value or re.search(r"[\u4e00-\u9fff]", value):
            return []
        value = re.sub(r"\s+", " ", value)
        sentences = [
            match.group(0).strip(" '\"“”")
            for match in re.finditer(r"[A-Za-z][^.!?]{1,300}[.!?]", value)
        ]
        if sentences:
            return sentences
        if cls._is_usable_scene_sentence(value):
            return [value]
        return []

    @staticmethod
    def _is_usable_scene_sentence(sentence):
        value = (sentence or "").strip()
        words = re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)?", value)
        if len(words) < 2 or len(words) > 36:
            return False
        lower = value.lower()
        if NoteCoursewareService._is_definition_style_scene_sentence(value):
            return False
        if any(marker in value for marker in ("=", "→", "…", "/", "\\")):
            return False
        if value.count("“") != value.count("”") or value.count('"') % 2:
            return False
        if re.match(r"^(?:to |the act of |the process of )", lower) and not re.match(
            r"^(?:to put (?:this|that|it) in perspective,|to some extent[,.!]?)",
            lower,
        ):
            return False
        # A dictionary label or an unfinished collocation is not dialogue.
        # Let the scene compiler create a complete situation instead of
        # pairing one of these fragments with a made-up question.
        if re.fullmatch(r"[A-Za-z][A-Za-z'’-]*\s+(?:n|v|adj|adv)\.?", value, re.I):
            return False
        if re.search(r"\b(?:sth|sb)\b", lower):
            return False
        if re.fullmatch(r"[a-z][a-z'’-]*\s+(?:with|to|of|for|as)\.?", lower):
            return False
        if re.match(
            r"^(?:would it be possible to|give (?:someone|somebody) a tour of|"
            r"as far as .+ is concerned,?|hence creating)\s*\.?$",
            lower,
        ):
            return False
        # Notes sometimes preserve a transcript label such as ``A:``.  It is
        # not a standalone learner-facing answer and cannot be paired with a
        # newly written first line without making a fake dialogue.
        if re.match(r"^(?:[A-Z]|speaker\s+[A-Z])\s*:", value):
            return False
        if re.search(
            r"\b(?:how do you say|how would you say|can you use|the expression|"
            r"(?:this|that|the word|the phrase)\s+means?|refers to|is short for)\b",
            lower,
        ):
            return False
        if re.search(r"\b(?:use this frame|make your own sentence)\b", lower):
            return False
        if lower in {"i reckon", "i wonder", "we shall see"} or lower.startswith(("so, as we said", "as we said")):
            return False
        if value.endswith((".", "!", "?")):
            return True
        starters = (
            "i ", "i'm ", "i’m ", "we ", "we're ", "we’re ", "you ", "he ", "she ",
            "they ", "it ", "there ", "this ", "that ", "let's ", "let’s ", "don't ", "do not ",
            "please ", "can ", "could ", "would ", "will ", "good morning", "good afternoon",
            "good evening", "no worries", "just chilling",
        )
        return lower.startswith(starters) or bool(re.search(r"\b(?:is|are|was|were|has|have|had)\b", lower))

    @staticmethod
    def _phrase_variants(phrase):
        variants = []
        for part in re.split(r"[\n/|;]+", phrase or ""):
            candidate = re.sub(r"[()\[\]{}\"“”]", "", part).strip().lower()
            candidate = re.sub(r"\s+", " ", candidate)
            words = re.findall(r"[a-z0-9]+(?:['’][a-z]+)?", candidate)
            if words and len(words) <= 32:
                variants.append(" ".join(words))
                if "-" in candidate:
                    variants.append(candidate)
                    variants.append(candidate.replace("-", " "))
                contractions = (
                    ("do not", "don't"),
                    ("does not", "doesn't"),
                    ("did not", "didn't"),
                    ("is not", "isn't"),
                    ("are not", "aren't"),
                    ("will not", "won't"),
                    ("cannot", "can't"),
                )
                for long_form, short_form in contractions:
                    if long_form in candidate:
                        variants.append(candidate.replace(long_form, short_form))
        return list(dict.fromkeys(variants))

    @classmethod
    def _blank_keyword(cls, sentence, phrase):
        """Return one natural sentence with the target expression blanked.

        A practice card must be a sentence learners can actually say.  The
        old implementation fell back to labels such as ``Use this frame`` or
        ``word = meaning`` when a source example was absent.  This helper is
        deliberately conservative: it only blanks the target expression (or
        a simple inflection of a one-word target) inside a complete English
        sentence.
        """
        value = cls._normalise_practice_sentence(sentence)
        if not cls._is_usable_scene_sentence(value):
            return None
        if re.search(r"\bfrom\s+\.\.\.\s+to\s+\.\.\.\s+to\s+\.\.\.", phrase or "", re.I):
            route = re.compile(r"\bfrom\s+[^,.!?]+?\s+to\s+[^,.!?]+?\s+to\s+[^,.!?]+", re.I)
            if route.search(value):
                return route.sub("________", value, count=1)
        variants = sorted(cls._phrase_variants(phrase), key=len, reverse=True)
        for variant in variants:
            if not variant:
                continue
            pattern = cls._keyword_pattern(variant)
            if pattern.search(value):
                return pattern.sub("________", value, count=1)
            if " " not in variant:
                inflected = re.compile(
                    rf"(?<![A-Za-z]){re.escape(variant)}(?:s|es|ed|ing)?(?![A-Za-z])",
                    re.I,
                )
                if inflected.search(value):
                    return inflected.sub("________", value, count=1)
        return None

    @staticmethod
    def _keyword_pattern(variant):
        """Match a phrase in source prose, including ``sth``/``sb`` frames."""
        tokens = re.findall(r"[a-z]+(?:['’][a-z]+)?", (variant or "").lower())
        placeholders = {"sth", "sb", "someone", "somebody", "something", "one"}
        tokens = tokens[: next((index for index, token in enumerate(tokens) if token in placeholders), len(tokens))]
        if not tokens:
            return re.compile(r"(?!x)x")

        irregular = {
            "be": r"(?:be|is|are|was|were|been|being)",
            "beat": r"(?:beat|beats|beaten|beating)",
            "do": r"(?:do|does|did|doing|done)",
            "fall": r"(?:fall|falls|fell|falling|fallen)",
            "fantastic": r"(?:fantastic)",
            "fantarstic": r"(?:fantastic)",
            "fulfil": r"(?:fulfil|fulfils|fulfilled|fulfilling|fulfill|fulfills|fulfillment|fulfilment)",
            "get": r"(?:get|gets|got|getting|gotten)",
            "give": r"(?:give|gives|gave|giving|given)",
            "go": r"(?:go|goes|went|going|gone)",
            "lose": r"(?:lose|loses|lost|losing)",
            "recur": r"(?:recur|recurs|recurred|recurring|recurrence)",
            "run": r"(?:run|runs|ran|running)",
            "stick": r"(?:stick|sticks|stuck|sticking)",
            "take": r"(?:take|takes|took|taking|taken)",
            "virus": r"(?:virus|viral)",
        }
        first = tokens[0]
        if first in irregular:
            first_pattern = irregular[first]
        elif len(first) <= 2:
            first_pattern = re.escape(first)
        elif first.endswith("e"):
            stem = re.escape(first[:-1])
            first_pattern = rf"(?:{re.escape(first)}|{re.escape(first)}s|{stem}ed|{stem}ing)"
        elif first.endswith("y") and len(first) > 3:
            stem = re.escape(first[:-1])
            first_pattern = rf"(?:{re.escape(first)}|{stem}ies|{stem}ied|{stem}ying)"
        else:
            first_pattern = rf"{re.escape(first)}(?:s|es|ed|ing)?"
        rest = [re.escape(token) for token in tokens[1:]]
        joined = first_pattern + "".join(r"[\s-]+" + token for token in rest)
        return re.compile(rf"(?<![A-Za-z0-9]){joined}(?![A-Za-z0-9])", re.I)

    @classmethod
    def _blank_keyword_anchor(cls, sentence, phrase):
        """Blank the meaningful core when a note stores a pattern, not a full headword."""
        value = cls._normalise_practice_sentence(sentence)
        if not cls._is_usable_scene_sentence(value):
            return None
        ignored = {
            "a", "an", "and", "as", "at", "be", "by", "for", "from", "in", "into", "of", "on",
            "or", "s", "sb", "so", "some", "someone", "somebody", "something", "sth", "that", "the",
            "to", "vs", "with",
        }
        candidates = []
        for variant in cls._phrase_variants(phrase):
            words = re.findall(r"[a-z0-9]+(?:['’][a-z]+)?", variant.lower())
            # Prefer a meaningful chunk such as ``registered nurse`` over a
            # lone word from a sentence-shaped note title.
            for size in range(min(4, len(words)), 1, -1):
                candidates.extend(" ".join(words[index:index + size]) for index in range(len(words) - size + 1))
            candidates.extend(words)
        for word in sorted(dict.fromkeys(candidates), key=len, reverse=True):
            if word in ignored or len(word) < 3:
                continue
            pattern = cls._keyword_pattern(word)
            if pattern.search(value):
                blanked = pattern.sub("________", value, count=1)
                if cls._is_meaningful_practice_sentence(blanked):
                    return blanked
        return None

    @staticmethod
    def _normalise_practice_sentence(sentence):
        """Repair harmless transcript punctuation before a learner sees it."""
        value = re.sub(r"\s+", " ", (sentence or "").strip())
        value = re.sub(
            r"\b(it|there|what|when|where|why|who|you|we|i)\s+s\b",
            r"\1's",
            value,
            flags=re.I,
        )
        if value and not value.endswith((".", "!", "?")) and re.match(
            r"^(?:how|what|when|where|why|who|is|are|can|could|would|do|does|did)\b",
            value,
            re.I,
        ):
            value += "?"
        return value

    @staticmethod
    def _is_meaningful_practice_sentence(pattern):
        """Keep generated output cards free of definitions and instructions."""
        value = (pattern or "").strip()
        if "________" not in value:
            return False
        terminal = value.rstrip("”\"'）)] ")
        if not terminal.endswith((".", "!", "?")):
            return False
        if re.search(r"(?:use this frame|make your own sentence|=|在句子中使用)", value, re.I):
            return False
        if re.search(r"(?:\.{2,}|\b(?:sth|sb)\b|[*•]|\s/\s)", value, re.I):
            return False
        lower = value.lower()
        if lower.startswith((
            "i heard someone mention ________",
            "i noticed a ________",
            "we need to ________ before we leave",
            "could we talk about ________",
        )):
            return False
        # ``Let's ________.`` technically has a verb once filled, but gives
        # the learner no situation.  Keep enough surrounding language for a
        # real sentence rather than a bare collocation prompt.
        remaining_words = re.findall(r"[A-Za-z]{2,}", value.replace("________", ""))
        return len(remaining_words) >= 2

    @classmethod
    def is_low_quality_scene_dialogue(cls, lines):
        """Identify dialogue that does not establish a real situation and reply."""
        if not isinstance(lines, list) or len(lines) < 2:
            return True
        first = str(lines[0].get("english", "")).strip()
        second = str(lines[1].get("english", "")).strip()
        if not cls._is_usable_scene_sentence(first) or not cls._is_usable_scene_sentence(second):
            return True
        lower = first.lower()
        second_lower = second.lower()
        if cls._is_definition_style_scene_sentence(first) or cls._is_definition_style_scene_sentence(second):
            return True
        # A question about a definition is a flashcard quiz.  It never
        # establishes the people, event, or consequence needed for a scene.
        if re.match(r"^what happened\b", lower) or re.match(
            r"^what does\b", lower
        ) or re.match(
            r"^what (?:does|do|is|are)\b.*\bmean(?:s)?\b.*\??$",
            lower,
        ) or lower.rstrip("?!.") == "can you tell me what happened" or re.match(
            r"^what did (?:he|she|they|it|someone|somebody|the [a-z][a-z -]{0,35}|this|that) do\?$",
            lower,
        ) or re.match(
            r"^how is (?:he|she|it|this|that|these|the [a-z][a-z -]{0,35})(?: doing)?\?$",
            lower,
        ) or lower == "what are you doing there?" or lower == "what are you hoping to do?" or re.match(
            r"^what (?:can|will|may|would) .+ do\?$",
            lower,
        ) or lower == "could you explain that to me?" or re.match(
            r"^what did you (?:do|buy|get|watch)\??$", lower
        ) or re.match(r"^where should i put (?:the photo|it)\?$", lower) or lower in {
            "how is these numbers?",
            "how is it probably isn't gonna?",
            "how is would?",
            "how is income inequality?",
            "how is cost?",
            "how is it tends to?",
            "how is that’s what it?",
            "how is that's what it?",
            "how is that deal?",
            "how is so visually it?",
            "how is pretty lucky to?",
            "what do we need?",
            "what do platforms use behavioural profiling for?",
            "what do my parents use it for?",
        }:
            return True
        if second_lower.rstrip(".!") in {
            "yes, of course",
            "let me check for you",
            "let me show you",
            "let's work it out together",
            "let’s work it out together",
            "fair enough",
        }:
            return True
        # These are remnants of the old "read a note, then report back"
        # generator.  They sound like a vocabulary quiz rather than two
        # people responding to an event, even if the second line is good.
        if re.match(
            r"^i was looking (?:at|into) .+ earlier\. what did you find out\?$",
            lower,
        ) or re.match(
            r"^i was wondering what you were up to\. what happened\?$",
            lower,
        ) or lower == "i was trying to understand it. what happened?":
            return True
        generic_starts = (
            "how are things going with the plan",
            "what happened with ",
            "what happened to them",
            "what should we do",
            "something unexpected happened",
            "something has everyone thinking",
            "we're deciding what to do",
            "we’re deciding what to do",
            "we were talking about it",
            "i'm not sure i can manage it on my own",
            "i’m not sure i can manage it on my own",
            "which one should i look at first",
            "i'm stuck and don't know what to do next",
            "i’m stuck and don't know what to do next",
        )
        if lower.startswith(generic_starts):
            return True
        # A bare question about an unnamed action never supplies enough
        # context for the reply.  Specific questions such as "What did you
        # buy at the market?" remain valid.
        if lower in {
            "what should i do?",
            "what was he doing?",
            "what was she doing?",
            "what were they doing?",
            "what kind of story is it?",
        }:
            return True
        if re.match(r"^i noticed a .+ on my way home\.$", second.lower()):
            return True
        # These were the tag-only fallbacks used before the reply-aware scene
        # compiler.  They can be fine sentences by themselves, but none tells
        # the learner why the following line is being said.
        tag_only_contexts = {
            "the queue at the counter is getting longer.",
            "a customer has just asked for some help.",
            "i haven't seen you in ages.",
            "we bumped into each other at the market this morning.",
            "we've just arrived and are looking for the hotel.",
            "the train leaves in a few minutes.",
            "i've been feeling unwell since yesterday.",
            "the doctor asked how i had been feeling.",
            "we're getting ready for tomorrow's class.",
            "our teacher gave us a new task this morning.",
            "the meeting starts in five minutes.",
            "we only have a few minutes before the next appointment.",
            "we need to explain what happened before lunch.",
            "the team is putting the final details together.",
            "i saw your message while i was making dinner.",
            "i finally had time to reply this evening.",
            "the shop is busy this afternoon.",
            "we need to finish this before the day ends.",
        }
        return lower in tag_only_contexts

    @classmethod
    def _sentence_matches_phrase(cls, sentence, phrase):
        lower = sentence.lower()
        lemma_like = re.sub(
            r"\b(?:went|gone)\b", "go", lower
        )
        lemma_like = re.sub(r"\b(?:took|taken)\b", "take", lemma_like)
        lemma_like = re.sub(r"\b(?:ran)\b", "run", lemma_like)
        lemma_like = re.sub(r"\b(?:got|gotten)\b", "get", lemma_like)
        score = 0
        for variant in cls._phrase_variants(phrase):
            if len(variant) < 3:
                continue
            if re.search(rf"(?<![a-z]){re.escape(variant)}(?![a-z])", lemma_like):
                score = max(score, 45 + min(len(variant), 24))
            elif " " not in variant and re.search(rf"\b{re.escape(variant)}(?:s|d|ing)?\b", lemma_like):
                score = max(score, 35 + min(len(variant), 16))
        return score

    @staticmethod
    def _is_non_technical_scene_sentence(sentence):
        lower = sentence.lower()
        technical = re.compile(
            r"\b(?:software|systems?|technical|technology|data|code|coding|computers?|servers?|databases?|api|"
            r"ocr|algorithm|programming|login|log in|review logic|debug(?:ging)?|interface|source code|"
            r"machine learning|codebuild|readme|erp|click[- ]through|test data|\bai\b|\bbug\b|"
            r"gis|gps|fields?\s+(?:were|are|should)|low-accuracy)\b"
        )
        teaching = re.compile(
            r"\b(?:how (?:do|would) (?:you|i) say|can you use|the (?:word|phrase|expression)|"
            r"this (?:word|phrase|expression) means)\b"
        )
        return (
            not technical.search(lower)
            and not teaching.search(lower)
            and not NoteCoursewareService._is_definition_style_scene_sentence(sentence)
        )

    @classmethod
    def _source_scene_examples(cls, item, fallback_chinese, phrase):
        """Extract and rank natural, non-technical source sentences for a scene."""
        inline_pattern = re.compile(
            r"(?P<english>[A-Za-z][^\u4e00-\u9fff]*?[.!?])\s*(?P<chinese>[\u4e00-\u9fff].*)$"
        )
        candidates = {}
        order = 0

        def add(english, chinese, bilingual):
            nonlocal order
            order += 1
            english = re.sub(r"\s+", " ", (english or "").strip())
            if (
                cls._is_definition_style_scene_sentence(english)
                or not cls._is_usable_scene_sentence(english)
                or not cls._is_non_technical_scene_sentence(english)
            ):
                return
            chinese = cls._clean_scene_chinese(chinese, fallback_chinese)
            key = english.lower()
            words = len(re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)?", english))
            score = (100 if bilingual else 0) + cls._sentence_matches_phrase(english, phrase)
            if 4 <= words <= 26:
                score += 8
            if re.search(r"\b(?:because|so|after|before|when|while|subsequently|later|eventually)\b", english, re.I):
                score += 8
            if re.match(r"^(?:don't worry|don’t worry|no worries|it's all good|it’s all good|let's|let’s|please)\b", english, re.I):
                score += 12
            candidate = {
                "english": english,
                "chinese": chinese,
                "_bilingual": bilingual,
                "_score": score,
                "_order": order,
            }
            existing = candidates.get(key)
            if existing is None or (candidate["_score"], candidate["_bilingual"]) > (
                existing["_score"], existing["_bilingual"]
            ):
                candidates[key] = candidate

        primary_chinese = cls._clean_scene_chinese(item["chinese_text"] or "", fallback_chinese)
        for field in ("english_text", "raw_text"):
            for sentence in cls._english_sentences(item[field] or ""):
                add(sentence, primary_chinese, True)

        for text in (item["chinese_text"] or "", item["explanation"] or "", item["examples"] or ""):
            lines = [cls._clean_source_line(line) for line in text.splitlines() if line.strip()]
            for index, line in enumerate(lines):
                inline = inline_pattern.search(line)
                if inline:
                    add(inline.group("english"), inline.group("chinese"), True)
                if not re.search(r"[\u4e00-\u9fff]", line):
                    for sentence in cls._english_sentences(line):
                        add(sentence, fallback_chinese, False)
                if index + 1 < len(lines) and not re.search(r"[\u4e00-\u9fff]", line):
                    following = lines[index + 1]
                    if cls._is_chinese(following):
                        for sentence in cls._english_sentences(line):
                            add(sentence, following, True)

        values = list(candidates.values())
        bilingual = [candidate for candidate in values if candidate["_bilingual"]]
        ranked = sorted(
            bilingual or values,
            key=lambda candidate: (-candidate["_score"], candidate["_order"], candidate["english"].lower()),
        )
        return [{"english": item["english"], "chinese": item["chinese"]} for item in ranked]

    @classmethod
    def _scene_tags(cls, item):
        try:
            tags = json.loads(item.get("usage_scenarios_json") or "[]")
        except (TypeError, ValueError):
            tags = []
        return [tag for tag in tags if isinstance(tag, str) and tag != "technical"]

    @classmethod
    def _scenario_context(cls, item, phrase):
        """A spoken first line when an item has no usable source reply."""
        contexts = {
            "customer_service": [
                ("The queue at the counter is getting longer.", "收银台前的队伍越来越长了。"),
                ("A customer has just asked for some help.", "刚有位顾客来寻求帮助。"),
            ],
            "friends_social": [
                ("I haven't seen you in ages.", "我好久没见到你了。"),
                ("We bumped into each other at the market this morning.", "我们今天早上在市场偶遇了。"),
            ],
            "travel_service": [
                ("We've just arrived and are looking for the hotel.", "我们刚到，正在找酒店。"),
                ("The train leaves in a few minutes.", "火车几分钟后就要开了。"),
            ],
            "health_medical": [
                ("I've been feeling unwell since yesterday.", "我从昨天起就感觉不舒服。"),
                ("The doctor asked how I had been feeling.", "医生问我最近感觉怎么样。"),
            ],
            "academic": [
                ("We're getting ready for tomorrow's class.", "我们正在为明天的课做准备。"),
                ("Our teacher gave us a new task this morning.", "老师今天早上给了我们一项新任务。"),
            ],
            "meeting_presentation": [
                ("The meeting starts in five minutes.", "会议五分钟后开始。"),
                ("We only have a few minutes before the next appointment.", "下一个约定前我们只剩几分钟了。"),
            ],
            "report_writing": [
                ("We need to explain what happened before lunch.", "午饭前我们得说明发生了什么。"),
                ("The team is putting the final details together.", "大家正在整理最后的细节。"),
            ],
            "online_chat": [
                ("I saw your message while I was making dinner.", "我做晚饭时看到了你的消息。"),
                ("I finally had time to reply this evening.", "今晚我终于有时间回复了。"),
            ],
            "workplace": [
                ("The shop is busy this afternoon.", "今天下午店里很忙。"),
                ("We need to finish this before the day ends.", "我们得在今天结束前把这件事做完。"),
            ],
            "daily_life": [
                ("Something unexpected happened on my way home.", "我回家路上发生了一件意外的事。"),
                ("We're deciding what to do this afternoon.", "我们在商量今天下午做什么。"),
            ],
            "general": [
                ("Something unexpected happened this morning.", "今天早上发生了一件意外的事。"),
                ("We were talking about it over coffee.", "我们喝咖啡时正聊到这件事。"),
            ],
        }
        tags = cls._scene_tags(item)
        tag = next((value for value in tags if value in contexts), "daily_life")
        return cls._dialogue_choice(phrase, contexts[tag], f"scenario-{tag}")

    @classmethod
    def _curated_scene(cls, item_id):
        """Hand-reviewed scenes for older note cards that contain only a bare term."""
        scenes = {
            3: ("Would you like to join us for lunch?", "要不要和我们一起吃午饭？", "I'm just very focused on finishing this today.", "我现在只想专心把这件事今天做完。"),
            4: ("These two labels are on the wrong boxes.", "这两个标签贴错盒子了。", "Let's interchange them.", "我们把它们互换一下吧。"),
            6: ("The red cups are on the blue table.", "红杯子放在蓝桌子上了。", "Let's swap them.", "我们把它们换一下吧。"),
            7: ("What was the best part of the workshop?", "这次工作坊最棒的部分是什么？", "The interchange of ideas was really useful.", "大家交流想法特别有收获。"),
            8: ("What is that sour fruit in the bowl?", "碗里那个酸酸的水果是什么？", "It's hawthorn.", "那是山楂。"),
            13: ("You look exhausted. Have you been busy?", "你看起来很累，今天很忙吗？", "I've been running around all day.", "我今天一整天都在忙来忙去。"),
            15: ("Why are you still at the hall?", "你怎么还在大厅里？", "I'm trying to get everything organized before the guests arrive.", "我想在客人来之前把一切都安排好。"),
            17: ("Why is everyone covering two tables?", "为什么每个人都在照看两张桌子？", "We're short-staffed tonight.", "我们今晚人手不够。"),
            23: ("What is the event called?", "这个活动叫什么名字？", "The event is called “Spring Market.”", "这个活动叫“春日集市”。"),
            26: ("Where is the talk being held?", "讲座在哪里举行？", "It's in the big room just across.", "就在对面那间大房间里。"),
            28: ("Are you expecting everyone at the party?", "你们预计派对上的人都会来吗？", "We'll see if they all show up.", "到时候看看他们会不会都到场。"),
            29: ("Do you think the rain will stop soon?", "你觉得雨很快会停吗？", "I reckon it will clear up soon.", "我觉得很快会放晴。"),
            31: ("Can we invite more people?", "我们还能多邀请一些人吗？", "That's the maximum number of people we can have in that room.", "那已经是这个房间最多能容纳的人数了。"),
            32: ("Could you send me the final invitation?", "你能把最终版邀请函发给我吗？", "Sure, here's a slightly polished version.", "当然，这是稍微润色过的版本。"),
            34: ("Can we get a table at the restaurant tonight?", "我们今晚能订到餐厅的位子吗？", "Sorry, it's fully booked.", "抱歉，已经订满了。"),
            35: ("The concert still has plenty of seats.", "音乐会居然还有很多座位。", "That's something I'm shocked by.", "这件事真让我吃惊。"),
            42: ("What are you reading on the bus?", "你在公交车上看什么？", "It's a graphic novel.", "这是一本图像小说。"),
            46: ("Why are the children so excited today?", "孩子们今天为什么这么兴奋？", "It's the last day of the school term.", "今天是学期的最后一天。"),
            47: ("When is the garden festival?", "花园节是什么时候？", "It's in the very last week of April.", "在四月的最后一个星期。"),
            49: ("How should I cut this paper?", "这张纸应该怎么剪？", "Cut it into strips.", "把它剪成长条。"),
            50: ("Where can we get coffee nearby?", "附近哪里能买到咖啡？", "There's a shopping strip just around the corner.", "拐角处就有一排商店。"),
            54: ("How do we start the game?", "这个游戏怎么开始？", "Grab a question strip at random.", "随手随机拿一张问题纸条吧。"),
            56: ("Should we decide now?", "我们现在就决定吗？", "Let's have a wee discussion first.", "我们先稍微讨论一下吧。"),
            57: ("What happens after we split into groups?", "我们分组后要做什么？", "I'll come back later and see how you guys get on.", "我晚点回来看看你们进行得怎么样。"),
            60: ("Who can tell me how to take this medicine?", "谁能告诉我这个药怎么吃？", "Ask the pharmacist.", "问问药剂师吧。"),
            62: ("Why is your brother worried about his career?", "你哥哥为什么担心自己的职业发展？", "The job market is changing quickly, and that worries a lot of people.", "就业市场变化很快，这让很多人担心。"),
            66: ("Everyone is looking at the materials.", "大家都看着手上的材料。", "What we're gonna do now is choose a partner.", "我们现在要做的是选一位搭档。"),
            67: ("We've both answered our cards.", "我们的卡片都答完了。", "Let's exchange the questions.", "我们交换一下问题卡吧。"),
            70: ("The queue is getting longer.", "队伍越来越长了。", "I'll help serve the customers.", "我来帮忙服务顾客。"),
            74: ("You tend to speak very quickly.", "你通常说话很快。", "I know. I try to be mindful of that.", "我知道，所以我会有意识地注意这一点。"),
            76: ("How do you follow a conversation when the room is noisy?", "房间里很吵时，你怎么听懂大家的谈话？", "Sometimes I can understand people from the context, but without clues it's hard.", "有时候我能从上下文听懂大家，但没有线索时就很难。"),
            80: ("I finished the poster before lunch.", "我午饭前就把海报做完了。", "Good work on that!", "这点做得真不错！"),
            82: ("Make a wish first.", "先许个愿。", "Okay, now blow out the candle.", "好，现在把蜡烛吹灭吧。"),
            85: ("Why don't people wear those hats anymore?", "为什么现在没人戴那种帽子了？", "They're falling out of fashion.", "它们正在慢慢过时。"),
            87: ("It's Maya's birthday today.", "今天是玛雅的生日。", "Congrats on another trip around the sun!", "恭喜你又绕太阳转了一圈！"),
            89: ("We waited for you at the café.", "我们在咖啡馆等了你一会儿。", "Sorry, I got tied up with a customer.", "抱歉，我被一位顾客耽搁住了。"),
            90: ("Why are you late?", "你为什么迟到了？", "I got held up talking to my friend.", "我和朋友聊天耽搁了。"),
            95: ("My shoulder is still sore.", "我的肩膀还是很酸。", "A warm shower might ease the pain.", "洗个热水澡可能会缓解疼痛。"),
            99: ("Where can I find the address and start time?", "地址和开始时间在哪里看？", "All the other details will be in the invitation.", "其他细节都会写在邀请函里。"),
            103: ("Will this new bus route change the neighborhood?", "这条新公交线路会改变这个社区吗？", "It could have a big impact on local shops.", "它可能会对当地商店产生很大影响。"),
            105: ("What happened to the family?", "这个家庭发生什么事了？", "It was a tragic accident.", "那是一场悲剧性的事故。"),
            107: ("How do you remember all your appointments?", "你怎么记住所有约会安排的？", "I use a calendar to stay on top of things.", "我用日历把所有事情安排得井井有条。"),
            109: ("Why did you leave home so early?", "你为什么这么早出门？", "I didn't want to be late.", "我不想迟到。"),
            221: ("What kind of job are you looking for this summer?", "你今年夏天想找什么工作？", "I'm looking for casual work.", "我在找临时工作。"),
            222: ("What does the report examine?", "这份报告研究什么？", "It looks at the causal relationship between the two events.", "它研究这两件事之间的因果关系。"),
            234: ("Where should we sit while we wait?", "等的时候我们坐哪里？", "Let's sit on that bench.", "我们坐那张长凳吧。"),
            236: ("This old box is taking up too much space.", "这个旧箱子太占地方了。", "Let's get rid of it.", "我们把它处理掉吧。"),
            237: ("Where does your uncle live?", "你叔叔住在哪里？", "He lives out in the back of Oxford.", "他住在牛津后面那一片。"),
            238: ("I need a trim. Do you know anywhere nearby?", "我想修一下头发，你知道附近哪里好吗？", "There's a good haircut place by the supermarket.", "超市旁边有家不错的理发店。"),
            242: ("What is the painting like?", "这幅画是什么风格？", "It has a peaceful, pastoral feel.", "它有一种宁静的田园气息。"),
            243: ("Are you free later today?", "你今天晚些时候有空吗？", "Yes, I'm free this arvo.", "有，我今天下午有空。"),
            247: ("We don't need these old boxes anymore.", "这些旧箱子已经用不着了。", "Let's ditch them.", "我们把它们丢掉吧。"),
            252: ("Why does the doctor say rest is important?", "医生为什么说休息很重要？", "It helps your immune system.", "它有助于你的免疫系统。"),
            253: ("Why are you reading the label?", "你为什么在看标签？", "I'm checking for additives.", "我在看有没有添加剂。"),
            254: ("How did you make the fabric blue?", "你怎么把布料染成蓝色的？", "I used blue dye.", "我用了蓝色染料。"),
            268: ("Who is welcoming everyone tonight?", "今晚谁来接待大家？", "Mia is our host.", "玛雅是我们的主人。"),
            271: ("Should I bring lunch to the workshop?", "我需要给工作坊带午饭吗？", "Yes, it's an all-day event.", "要，这是一个全天活动。"),
            273: ("This apple looks delicious.", "这个苹果看起来很好吃。", "Go on, take a bite out of it.", "来吧，咬一口。"),
            274: ("What did you put in the cereal?", "你在麦片里放了什么？", "Some raisins and almonds.", "一些葡萄干和杏仁。"),
            275: ("Why did the nurse ask about the medicine?", "护士为什么问起这个药？", "She wanted to make sure I hadn't taken an overdose.", "她想确认我没有服用过量。"),
            277: ("How would you like your eggs?", "你的鸡蛋想怎么做？", "I'll have an omelette, please.", "我要一份煎蛋卷，谢谢。"),
            278: ("How many flowers should we buy?", "我们该买多少花？", "Let's get a bunch of them.", "我们买一束吧。"),
            279: ("How did you get your first internship?", "你是怎么拿到第一份实习的？", "I was fortunate to secure it through the program.", "我很幸运通过这个项目拿到了它。"),
            282: ("How did your career develop?", "你的职业是怎么发展的？", "It took me from retail to training to management.", "我从零售做到了培训，再到管理。"),
            284: ("What are you doing this weekend?", "你这个周末在做什么？", "I'm preparing for interviews.", "我在准备面试。"),
            285: ("Why are people retraining so often?", "为什么大家常常要重新学习技能？", "They work in a fast-moving industry.", "因为他们所在的行业变化很快。"),
            287: ("What does your job involve?", "你的工作具体做什么？", "I go around to primary schools.", "我会去不同的小学。"),
            288: ("Why did you bring that old camera?", "你为什么带着那台旧相机？", "I found a roll of film for it.", "我找到了一卷能用的胶卷。"),
            291: ("Why don't you want to watch it alone?", "你为什么不想一个人看它？", "It's a creepy movie.", "这是一部让人毛骨悚然的电影。"),
            297: ("Why won't this old camera take a photo?", "这台旧相机为什么拍不了照？", "The shutter blade is stuck.", "快门叶片卡住了。"),
            299: ("What sort of book is this?", "这是哪一类书？", "It's a biography of a famous musician.", "这是一本著名音乐家的传记。"),
            330: ("Do you know when this building was built?", "你知道这座楼是什么时候建的吗？", "It was built in eighteen hundred.", "它建于 1800 年。"),
            338: ("Which mirror should I check before reversing?", "倒车前我该看哪面镜子？", "Check the rear-view mirror.", "看后视镜。"),
            343: ("This bottle won't open. What should I do?", "这个瓶子打不开，我该怎么做？", "Twist the cap off.", "把瓶盖拧下来。"),
            347: ("What could you see from the plane?", "从飞机上你看到了什么？", "We could see a big stretch of mountains.", "我们能看到一大片连绵的山脉。"),
            376: ("What should we visit while we're in town?", "我们在镇上该去哪里逛？", "The old lighthouse is a popular tourist attraction.", "老灯塔是很受欢迎的景点。"),
            377: ("What would you like with your coffee?", "你的咖啡想配点什么？", "I'd like a pastry with my coffee.", "我想点一份糕点配咖啡。"),
            378: ("The main street is blocked. Is there another way?", "大路被堵住了，还有别的路吗？", "Let's take the alley behind the café.", "我们从咖啡馆后面那条路走吧。"),
            388: ("We have several experienced volunteers at the event.", "活动上有几位经验丰富的志愿者。", "We can leverage their experience.", "我们可以善用他们的经验。"),
            387: ("How will the staff know you're with the event?", "工作人员怎么知道你是活动参与者？", "I'll wear my name badge.", "我会戴上我的姓名牌。"),
            393: ("How will you organize the research?", "你打算怎么组织这项研究？", "We'll use the same methodology throughout.", "我们会始终使用同一套研究方法。"),
            394: ("What should I do before the show?", "演出前我该做什么？", "I'll perform my song the way I practised.", "我会按练习时的方式表演这首歌。"),
            407: ("Why does this job feel so tiring?", "这份工作为什么让人这么累？", "The demands are high.", "要求很高。"),
            410: ("Why do you spend so much time painting?", "你为什么花这么多时间画画？", "It's my passion.", "这是我的热爱。"),
            421: ("The rain changed our picnic plans.", "下雨改变了我们的野餐计划。", "We changed the plan on the fly.", "我们临时改变了计划。"),
            423: ("Do we need to build a new sign-up sheet?", "我们需要重新做一份报名表吗？", "No, let's not reinvent the wheel.", "不用了，别做重复劳动。"),
            443: ("Why did that small win make you smile?", "为什么那点小成功让你笑了？", "It gave me a little hit of dopamine.", "它给了我一点多巴胺带来的快乐。"),
            445: ("Why are you adjusting the old fan?", "你为什么在调那台旧风扇？", "I just need to get it doing what it should.", "我只需要让它正常运转起来。"),
            446: ("Can you stay for the whole ceremony?", "你能参加完整个仪式吗？", "I have an obligation to be there.", "我有义务到场。"),
            456: ("Why do people choose that apartment?", "人们为什么选择那套公寓？", "The balcony is its biggest selling point.", "阳台是它最大的卖点。"),
            459: ("The path is blocked by a fallen tree.", "小路被倒下的树挡住了。", "We need to figure out another way around.", "我们得想办法从别处绕过去。"),
            462: ("How often do you visit your grandparents?", "你多久去看一次祖父母？", "I visit them every other week.", "我每隔一周去看他们一次。"),
            470: ("What should I bring to the picnic?", "野餐我该带什么？", "Bring a jacket along with some water.", "带件外套，再带些水。"),
            476: ("Why are your parents worried?", "你父母为什么担心？", "I stayed out past midnight.", "我在外面待到午夜以后。"),
            526: ("What is the baby drinking now?", "宝宝现在喝什么？", "She's having formula milk.", "她在喝配方奶。"),
            537: ("Your shoes look brand-new.", "你的鞋看起来像新的一样。", "I polished them until they were shiny.", "我把它们擦得很有光泽。"),
            567: ("Why is the cat scratching the sofa?", "猫为什么抓沙发？", "She needs a cat scratching post.", "她需要一个猫抓柱。"),
            590: ("How did the film show so many years passing?", "电影怎么表现那么多年过去的？", "It used a movie montage.", "它用了一个蒙太奇片段。"),
            607: ("What is that figure in the town square?", "镇广场上的那个雕像是什么？", "It's a statue of the town founder.", "那是小镇创建者的雕像。"),
            611: ("How is your new brace feeling?", "你戴着新支架感觉怎么样？", "It causes a little discomfort.", "它会带来一点不适。"),
            674: ("Did anything serious happen at work?", "工作中发生什么严重的事了吗？", "No, it was just a mild, slightly funny occurrence.", "没有，只是一件不太严重、还有点好笑的小事。"),
            735: ("Do you understand the new bus timetable yet?", "你已经看懂新的公交时刻表了吗？", "I'm starting to get a clear idea of it.", "我开始对它有一个清楚的概念了。"),
            747: ("How did she tell you the news?", "她是怎么告诉你这个消息的？", "She said it matter-of-factly.", "她用很平静、就事论事的语气说了。"),
            787: ("What are you working on after class?", "下课后你在做什么？", "My other assignment is about local history.", "我的另一份作业是关于当地历史的。"),
            788: ("What is your other assignment about?", "你的另一份作业是关于什么的？", "It's about local history.", "是关于当地历史的。"),
            789: ("Are you nearly finished with your assignment?", "你的作业快完成了吗？", "I'm nearly done; I just need to add the final details.", "我快完成了，只差补上最后的细节。"),
            790: ("Will you finish the assignment tonight?", "你今晚能完成作业吗？", "I've almost finished it, but I still need to add a few details.", "我几乎完成了，但还要补几个细节。"),
            803: ("What kind of work interested you most?", "你当时最感兴趣的是什么工作？", "I was more drawn to finance and office work.", "我当时更被金融和办公室工作吸引。"),
            882: ("Will this charger work with your phone?", "这个充电器能用在你的手机上吗？", "It's compatible with mine.", "它和我的手机兼容。"),
            911: ("The mosquitoes are terrible tonight.", "今晚蚊子特别多。", "Put on some bug spray.", "喷一点驱蚊喷雾吧。"),
            1034: ("How did you find the trail?", "你是怎么找到这条步道的？", "We used GPS.", "我们用了 GPS。"),
            1045: ("Can you see the birds on the cliff?", "你能看到悬崖上的鸟吗？", "Yes, through these binoculars.", "能，用这副双筒望远镜就能看到。"),
            1053: ("Why is your kitchen full of dust?", "你家厨房为什么全是灰？", "We're renovating the house.", "我们在翻新房子。"),
            1054: ("Why is the door still open?", "门为什么还开着？", "It's because Sam is still outside.", "因为萨姆还在外面。"),
            1055: ("Do you like where you live now?", "你喜欢现在住的地方吗？", "Yes, it's a quiet neighborhood.", "喜欢，这是一个安静的社区。"),
            1056: ("Who brought over those cookies?", "谁送来了这些饼干？", "Our neighbor did.", "我们的邻居送来的。"),
            1057: ("Should we change the plan again?", "我们要不要又改计划？", "No, let's stick to it.", "不用，就按这个计划坚持下去。"),
            1058: ("Can you fix the drawer today?", "你今天能修好这个抽屉吗？", "It's a tricky thing to fix.", "这东西修起来有点棘手。"),
            1059: ("Why do you play guitar every night?", "你为什么每天晚上都弹吉他？", "Music is my passion.", "音乐是我的热爱。"),
            1061: ("Why are you taking the shoes back?", "你为什么要退这双鞋？", "There's a defect in the stitching.", "缝线有瑕疵。"),
            1102: ("What time should we meet for lunch?", "我们午饭几点见？", "At 12 pm, not 12 am.", "中午十二点，不是半夜十二点。"),
            1136: ("Did many people open the event email?", "很多人打开活动邮件了吗？", "The click-through rate was high.", "点击率很高。"),
            1310: ("The sign says this dam provides hydroelectric power. What does hydro- refer to there?", "牌子上说这座水坝提供水电，这里的 hydro- 指什么？", "It refers to water.", "它指的是水。"),
            1348: ("Can people join the workshop from home?", "大家能从家里参加这个工作坊吗？", "No, this session is on-premise.", "不能，这次活动需要线下参加。"),
            1372: ("Where does the order go after the counter?", "订单在收银台之后会去哪里？", "It goes straight to the stock room.", "它会直接送到库存间。"),
            73: ("Can you pop in for a minute?", "你能进来一会儿吗？", "Yes, of course.", "当然可以。"),
            128: ("Why did he come home with a black eye?", "他回家时眼睛为什么青了？", "Some older boys beat him up after school.", "放学后有几个高年级男生把他打了一顿。"),
            229: ("You look relaxed today. Are you doing anything?", "你今天看起来很放松，在忙什么吗？", "No, I'm just chilling at home.", "没有，我就在家放松一下。"),
            250: ("Why is the meeting an hour earlier than last week?", "为什么这次会议比上周早一小时？", "Daylight saving started on Sunday.", "周日开始实行夏令时了。"),
            286: ("Will the sofa fit in this room?", "这张沙发能放进这个房间吗？", "Let me get the tape measure and check the width.", "我拿卷尺量一下宽度。"),
            314: ("What happens to the leaves when the wind picks up?", "风大起来时落叶会怎么样？", "The wind disperses the dry leaves across the path.", "风会把干树叶吹散到小路上。"),
            316: ("These boxes are too heavy to carry. How can we move them?", "这些箱子太重搬不动，怎么挪？", "Use the sack barrow.", "用两轮手推车。"),
            406: ("I can meet at four instead of three. Is that good for you?", "我可以从三点改到四点见面，你觉得可以吗？", "Yes, four works for me.", "可以，四点对我合适。"),
            409: ("The room went silent after his joke. How did it feel?", "他讲完笑话后房间突然安静了，感觉怎么样？", "It was awkward for everyone.", "大家都觉得很尴尬。"),
            468: ("The road was blocked, so everyone used the narrow detour. What happened?", "路被堵了，大家都走狭窄的绕路，后来怎么样？", "The detour was crowded, hence creating a long delay.", "绕路很拥挤，因此造成了长时间延误。"),
            519: ("Why are you sleeping on the sofa tonight?", "你今晚为什么睡沙发？", "I'm in the doghouse after forgetting our anniversary.", "我忘了纪念日，惹对方生气了。"),
            544: ("Are you ready for the presentation?", "你准备好做展示了吗？", "To some extent. I'm not fully ready, but I'm getting there.", "在某种程度上准备好了，但还没完全准备好。"),
            572: ("How did you respond when she received the bad news?", "她收到坏消息时你怎么回应的？", "I commiserated with her and stayed for a cup of tea.", "我陪她难过，还留下来陪她喝了杯茶。"),
            597: ("Why are you holding your knee?", "你为什么捂着膝盖？", "I stumbled on the stairs.", "我在楼梯上绊了一下。"),
            599: ("I ruined my first cake and feel like giving up. What do you think?", "我第一次做蛋糕搞砸了，想放弃。你觉得呢？", "A growth mindset treats mistakes as part of learning.", "成长型思维会把错误看作学习的一部分。"),
            600: ("How did you feel after talking about the big change?", "聊完那个大变化后你感觉怎么样？", "I felt excited but also a little quiet inside.", "我既兴奋，内心又有一点安静。"),
            658: ("How do you stop debating whether to exercise every morning?", "你怎么避免每天早上纠结要不要锻炼？", "I'm pre-programming my brain by making the plan the night before.", "我前一晚就定好计划，等于提前给大脑设定程序。"),
            715: ("Where should I put “already” in this sentence?", "这句话里的 already 应该放在哪里？", "Put the adverb after “have”: “I have already finished.”", "把副词放在 have 后面：I have already finished。"),
            814: ("How can we keep the children listening during the story?", "讲故事时怎样让孩子一直听下去？", "A mystery at the start can engage their interest.", "开头设置一个悬念能吸引他们的兴趣。"),
            815: ("We need help with the legal contract. What should we do?", "我们需要人帮忙处理法律合同，该怎么办？", "Let's engage her as a consultant.", "我们聘请她担任顾问吧。"),
            874: ("The city no longer needs those licences. What will it do with them?", "这座城市不再需要这些许可证了，会怎么处理？", "It will auction them off to the highest bidders.", "它会把许可证拍卖给出价最高的人。"),
            876: ("How will people hear about the new bakery?", "大家怎么知道这家新面包店？", "We'll advertise it on the local noticeboard and online.", "我们会在本地公告栏和网上宣传它。"),
            895: ("He stayed calm for a long time. What happened during the argument?", "他一直很冷静，争吵时后来怎么了？", "He finally lost it and shouted.", "他终于情绪失控，大喊起来。"),
            904: ("Did she do what she promised the customer?", "她兑现对顾客的承诺了吗？", "Yes, she fulfilled her promise.", "是的，她履行了承诺。"),
            994: ("Can you start the slides while I finish the report?", "我完成报告时你能开始做幻灯片吗？", "Sure. In the meantime, I'll choose the images, and we can work at the same time.", "当然。这期间我来选图片，我们可以同时进行。"),
            1015: ("Our connecting flight lands late at the airport. Where should we meet?", "我们的转机航班很晚才到机场，在哪里碰面？", "Let's meet at baggage claim after the flight.", "航班到达后在行李提取处见。"),
            1016: ("It's getting late and we still have a long drive.", "天晚了，我们还有很长的车程。", "Let's hit the road.", "我们出发吧。"),
            1027: ("I handed in my part-time job application last week. What should I do now?", "我上周交了兼职申请，现在该做什么？", "Wait and stay patient while they work through the applications.", "等他们逐份处理申请，耐心一点。"),
            1041: ("How did your grandparents first meet?", "你的祖父母最初是怎么认识的？", "They fell in love at first sight.", "他们一见钟情。"),
            1094: ("How can I practise speaking while I cook dinner?", "做晚饭时怎么练口语？", "Narrate your life in English as you do each small task.", "做每个小事时都用英语描述自己的生活。"),
            1143: ("Which number tells us how far east the campsite is on the map?", "地图上哪个数字表示营地向东多远？", "The easting gives the eastward position.", "东向坐标表示向东的位置。"),
            1223: ("These two pieces don't have price tags. Do they belong together?", "这两个零件都没有价签，它们是一套的吗？", "What's that on? It might be part of a set.", "这个是哪个东西上的？它可能是一套中的一部分。"),
            1310: ("The dam uses hydroelectric power. How is it powered?", "这座水坝用水力发电，它靠什么供能？", "It is powered by water.", "它靠水力供能。"),
            1320: ("The advert says the product is best because nothing is better. Is that convincing?", "广告说它最好，因为没有比它更好的，这有说服力吗？", "No, it begs the question instead of proving the claim.", "没有，它预设了结论，并没有证明这个说法。"),
            1397: ("What happened to the small idea after several months of testing?", "这个小想法经过几个月测试后怎么样了？", "It evolved into a more practical solution.", "它逐渐发展成了更实用的方案。"),
            1456: ("Did the same problem come back after the last repair?", "上次修好后同一个问题又出现了吗？", "Yes, it recurred, so we need to prevent another recurrence.", "是的，它又出现了，所以要防止再次发生。"),
            1473: ("Three thousand metres sounds huge. How high is that really?", "三千米听起来很高，究竟有多高？", "To put this in perspective, it's three times higher than the nearby hills.", "为了便于理解，它比附近山丘高三倍。"),
            1570: ("Who prepares the report, and who gives the final sign-off?", "谁负责准备报告，谁对最终结果签字负责？", "Mia has the responsibility to prepare it, and her manager has accountability for the final result.", "米娅负责准备，经理则对最终结果负责。"),
            1576: ("We've discussed many causes. What's the main issue?", "我们讨论了很多原因，核心问题是什么？", "It all boils down to poor communication.", "归根结底是沟通不畅。"),
            1617: ("This class has two separate jobs. How can we keep it simple?", "这个类承担两项不同工作，怎样保持简单？", "It composes two other classes to share the work.", "它组合另外两个类来分担工作。"),
            1630: ("I got the job!", "我拿到这份工作了！", "Fantastic! You worked hard for it.", "太棒了！你为此付出了很多努力。"),
            5: ("These name labels are mixed up. What should we do?", "这些姓名标签弄混了，该怎么办？", "Interchange the two labels.", "把这两个标签互换一下。"),
            25: ("The dentist is fully booked this week. How can I get an appointment?", "牙医这周全满了，怎么预约？", "Call now and book in for next week.", "现在打电话，预约下周。"),
            35: ("The concert still has lots of empty seats. Can you believe it?", "音乐会居然还有很多空座，你能相信吗？", "I'm shocked by how many seats are still empty.", "我很震惊还有这么多空座。"),
            57: ("You've finished your group task. What will the teacher do next?", "你们完成小组任务后，老师接下来会做什么？", "She'll come back later to see how you guys get on.", "她晚点会回来看看你们进展如何。"),
            239: ("Why are there so many cranes in this neighbourhood?", "这个社区为什么有这么多起重机？", "There's lots of housing going on around here.", "这附近正在建很多住宅。"),
            251: ("Do people still use paper maps when they travel?", "人们旅行时还会用纸质地图吗？", "For most travellers, they're a thing of the past.", "对大多数旅行者来说，它们已经是过去的东西了。"),
            256: ("The children kept begging for ice cream. What did their dad do?", "孩子们一直求买冰淇淋，爸爸怎么做了？", "He finally gave in.", "他最后还是让步了。"),
            281: ("I'm new to investing and all the choices feel confusing.", "我刚开始投资，各种选择让我很困惑。", "It takes time to navigate the world of investing.", "熟悉投资领域需要时间。"),
            300: ("Why do you keep practising guitar every day?", "你为什么每天坚持练吉他？", "My older sister inspires me.", "姐姐激励着我。"),
            308: ("The volunteers are waiting for instructions. Who should lead?", "志愿者在等安排，谁该带头？", "You're supposed to be in charge in this situation.", "这种情况下本来应该由你负责。"),
            315: ("You noticed every reference in the novel. How do you know so much?", "你注意到了小说中的每个典故，怎么懂这么多？", "You really are a literature PhD, just as I thought.", "果然和我想的一样，你真是文学博士。"),
            317: ("I've been studying for hours. Is it wrong to do something else for a little while?", "我已经学习好几个小时了，做点别的休息一下不可以吗？", "No, a short break can help you focus.", "不会，短暂休息能帮助你集中注意力。"),
            325: ("We're collecting ideas for the party. Do you have any?", "我们在收集派对点子，你有想法吗？", "Feel free to chip in with a suggestion.", "随时可以提个建议。"),
            340: ("Are you nervous about driving again?", "你重新开车会紧张吗？", "A little. I haven't done it for a while.", "有一点，我有一阵子没开了。"),
            366: ("I'm heading to the concert now.", "我现在要去音乐会了。", "Have a good time!", "玩得开心！"),
            439: ("Why does the novel switch between the past and the present?", "这本小说为什么在过去和现在之间切换？", "That structure strengthens the narrative.", "这种结构强化了叙事。"),
            504: ("Where should I leave these clothes for charity?", "这些捐给慈善机构的衣服该放在哪里？", "You can ask them to put it in the trolley for donations.", "你可以请他们放进捐赠手推车。"),
            515: ("You look tired this morning. What do you need?", "你今天早上看起来很累，需要什么？", "I need something to pick me up, maybe a strong coffee.", "我需要点提神的东西，也许是一杯浓咖啡。"),
            517: ("Why does he still refuse to use online banking?", "他为什么还拒绝使用网上银行？", "He's stuck in the Stone Age.", "他还停留在石器时代。"),
            536: ("I'm doing every task myself and falling behind. Any advice?", "我一个人做所有任务，已经跟不上了，有什么建议？", "Delegate some responsibilities instead of doing everything yourself.", "把一些职责委派出去，不要全自己做。"),
            569: ("The soup tastes a little plain. What should I do with these herbs?", "汤有点淡，这些香草该怎么处理？", "Just throw it in with the vegetables.", "直接把它加到蔬菜里。"),
            575: ("I'm still slow at this game.", "我玩这个游戏还是很慢。", "Keep practising—you'll be a pro in no time.", "继续练，很快你就会变成高手。"),
            585: ("He's stressed after work. How can I help?", "他下班后压力很大，我怎么帮忙？", "You can make his evening easier by making him tea.", "给他泡杯茶能让他的晚上轻松些。"),
            587: ("My sister is overwhelmed with errands. What can I do?", "我姐姐被各种杂事压得喘不过气，我能做什么？", "A small favour can make her day easier.", "一个小帮忙就能让她的一天轻松些。"),
            612: ("The last kilometre feels hard. Should I stop?", "最后一公里很难坚持，我该停下吗？", "You just have to push through the discomfort.", "你只要咬牙熬过这阵不适。"),
            630: ("How do you improve faster at piano?", "怎样更快提高钢琴水平？", "Seek out the difficult stuff instead of only easy songs.", "主动找难的内容练，而不是只弹简单的曲子。"),
            632: ("I've had a tough week and want to give up.", "这一周太难了，我想放弃。", "You want to quit because it feels like too much, but take one small step.", "你想放弃是因为压力太大了，但先迈出一小步。"),
            637: ("I keep comparing my progress with others online. What should I do?", "我总在网上和别人比较进步，该怎么办？", "When you feel the urge to look at someone else's progress, return to your own plan.", "当你想看别人进展时，回到自己的计划上来。"),
            644: ("You made one mistake and feel terrible. What should you tell yourself?", "你犯了一个错就很难受，该怎么对自己说？", "Don't be hard on yourself.", "别对自己太苛刻。"),
            645: ("You spilled coffee on the table. Is the mark permanent?", "你把咖啡洒在桌上了，印子会一直在吗？", "No, you can wipe it away with a single finger.", "不会，用一根手指就能擦掉。"),
            649: ("We can't attend the ceremony in person. Will the team still feel our support?", "我们不能亲自参加仪式，团队还能感受到支持吗？", "You'd all already be there in spirit.", "你们的心意其实已经到场了。"),
            699: ("You do everything your family wants, but never what you want.", "你总做家人希望你做的事，却从不做自己想做的。", "You're living for everyone else.", "你在为所有其他人而活。"),
            712: ("What do you like doing at the café window?", "你喜欢坐在咖啡馆窗边做什么？", "I like to watch people walking by.", "我喜欢看行人走过。"),
            714: ("Will all this practice really change me?", "这么多练习真的会改变我吗？", "One day, you won't even recognise the person you used to be.", "总有一天，你甚至认不出过去的自己。"),
            765: ("Where should I stop the car to unload the bags?", "我该把车停在哪里卸行李？", "You can pull up by the front door.", "你可以停在前门旁。"),
            777: ("Can I borrow your phone for a minute?", "我能借你的手机用一分钟吗？", "Yes, as long as you're careful.", "可以，只要你小心使用。"),
            781: ("I've been invited to apply today. Should I wait?", "今天有人邀请我申请，我应该等一等吗？", "It's perfect timing—take it seriously and apply now.", "时机正好，认真对待并现在就申请。"),
            839: ("The bus is cancelled and it's pouring. How should we get home?", "公交取消了，雨又很大，我们怎么回家？", "You'd be better off taking a taxi in this weather.", "这种天气坐出租车更合适。"),
            848: ("Can I use my phone while driving?", "开车时我可以用手机吗？", "No, you're not supposed to use it while driving.", "不行，开车时不应该用手机。"),
            875: ("Why did the cat come so close to the carrier?", "猫为什么靠近航空箱了？", "I used a treat to lure it inside.", "我用零食把它引进去。"),
            949: ("Would somebody explain what's going on?", "谁能解释一下发生什么了吗？", "The train has stopped because of a signal problem.", "火车因信号问题停下来了。"),
            952: ("Why are you carrying all these boxes into your flat?", "你为什么往公寓里搬这么多箱子？", "It's a long story.", "说来话长。"),
            972: ("Did you mean to suggest he was lying?", "你是想暗示他在撒谎吗？", "No, I accidentally insinuated it.", "不是，我是不小心暗示了这个意思。"),
            984: ("Why won't she tell us how much she earns?", "她为什么不愿意告诉我们她赚多少？", "That's personal, so she'd rather not discuss it.", "那是私人问题，所以她不愿讨论。"),
            966: ("Why are you rubbing your shoulder?", "你为什么揉肩膀？", "I banged into someone in the crowded station.", "我在拥挤的车站撞到人了。"),
            978: ("He kept shouting and breaking things. What did the coach do?", "他一直大喊还砸东西，教练怎么做了？", "The coach kicked him out for his misbehavior.", "教练因为他的不当行为把他赶出去了。"),
            979: ("Who should I trust with the spare key?", "备用钥匙该交给谁保管？", "Give it to someone you trust, then text them the address.", "交给你信任的人，再把地址发给他们。"),
            1012: ("This is a difficult week. How are you coping?", "这周很艰难，你怎么应对？", "We'll get through it together.", "我们会一起熬过去。"),
            1077: ("Can I only do the tasks I like?", "我可以只做我喜欢的任务吗？", "No, you can't just pick and choose.", "不行，你不能只挑自己喜欢的。"),
            1095: ("I made mistakes in practice. Should I hide them?", "我练习时犯错了，应该藏起来吗？", "No, embrace your mistakes if you want to improve.", "不，如果想进步，就接纳自己的错误。"),
            1104: ("Why can't I apply for this course yet?", "我为什么还不能申请这门课程？", "You need more experience to meet these requirements.", "你需要更多经验来达到这些要求。"),
            1206: ("My phone keeps falling while I watch the recipe.", "我看食谱时手机一直倒，怎么办？", "Prop it against a cup.", "把它靠在杯子上。"),
            1212: ("Why didn't you come to the event?", "你为什么没来活动？", "I was meant to be there, but my flight was cancelled.", "我本来应该到场，但航班取消了。"),
            1289: ("I finished the presentation ahead of time.", "我提前完成了展示。", "You did a stellar job.", "你做得非常出色。"),
            1366: ("Can I go out after I finish my homework?", "做完作业后我可以出去吗？", "Yes, as long as you finish it first.", "可以，只要你先完成作业。"),
            1374: ("The office is closed tomorrow. Would it be possible to submit it online?", "办公室明天关门，可以在线提交吗？", "Yes, you can send it through the website.", "可以，你可以通过网站提交。"),
            720: ("This song sounds like the one we heard on holiday.", "这首歌听起来像我们度假时听到的那首。", "That just reminded me of an old story.", "这刚好让我想起一个老故事。"),
            1019: ("You fixed the bike in ten minutes!", "你十分钟就修好了自行车！", "You've got mad skills.", "你太有两下子了。"),
            1472: ("Should I put a question mark at the end of this sentence?", "这句话末尾要加问号吗？", "No, you don't need a question mark because it isn't a question.", "不用，因为它不是疑问句。"),
            1483: ("Can I make changes to your bike?", "我能改动你的自行车吗？", "You need the owner's consent first.", "你得先得到车主同意。"),
            1486: ("I worry she meant to criticize me. How should I take it?", "我担心她是在批评我，我该怎么理解？", "Don't take it the wrong way; she wants to help.", "别往坏处想，她是想帮忙。"),
            1493: ("The train leaves in ten minutes. Are we ready?", "火车十分钟后开，我们准备好了吗？", "We need to get our skates on.", "我们得赶紧行动了。"),
            885: ("The shop just found your size in the last pair.", "商店刚好找到了最后一双你的尺码。", "You're in luck today.", "你今天运气真好。"),
            738: ("When is the report due?", "报告什么时候截止？", "You're supposed to finish it today.", "你本来应该今天完成它。"),
            762: ("Do you think the café is still open?", "你觉得咖啡馆还开着吗？", "I doubt it; it closes at six.", "我觉得不会，它六点关门。"),
            798: ("I see you sell photos online. Is it something you're getting some revenue off?", "我看到你在网上卖照片，这能给你带来收入吗？", "Yes, it brings in a little extra money.", "是的，能带来一点额外收入。"),
            1553: ("Can I start using the booking system on my own?", "我能自己开始用这个预约系统吗？", "You'll need some familiarity with it first.", "你得先熟悉一下它。"),
            1575: ("I keep forgetting to review my notes. Any advice?", "我总忘记复习笔记，有什么建议？", "Cultivate the habit of reviewing them each evening.", "培养每天晚上复习的习惯。"),
            1605: ("We don't have evidence for that claim. What should we do?", "我们没有证据支持那个说法，该怎么办？", "We can't fabricate evidence just to support it.", "我们不能为了支持它而编造证据。"),
            1637: ("What are you reading on the train?", "你在火车上读什么？", "It's a family saga spanning three generations.", "这是一个跨越三代人的家族故事。"),
            1640: ("They're arguing again. Should we get involved?", "他们又吵起来了，我们要卷进去吗？", "No, don't let them draw you into their argument.", "不要，别让他们把你拉进争吵里。"),
            12: ("What did the community centre offer during the holidays?", "社区中心假期里提供了什么？", "It ran food programs for local families.", "它为当地家庭开设了餐食项目。"),
            14: ("Why are you so rushed today?", "你今天为什么这么匆忙？", "I've been running around like a chicken with my head cut off.", "我忙得像没头苍蝇一样。"),
            16: ("Should I take a jacket tonight?", "我今晚该带外套吗？", "Yes, it's gonna rain later.", "要，晚些时候要下雨。"),
            19: ("Why are you exhausted?", "你为什么累坏了？", "I've been running around all day.", "我一整天都在忙来忙去。"),
            96: ("Can this form be simpler for parents?", "这份表格能不能让家长填得简单一点？", "Yes, a shorter form can ease the burden on parents.", "可以，短一点的表格能减轻家长负担。"),
            101: ("Why do you use a calendar for everything?", "你为什么什么事都用日历？", "It works for so many things in life.", "它在生活中很多事情上都很好用。"),
            304: ("Why did we miss the deadline?", "我们为什么错过截止日期？", "We dropped the ball on the final check.", "我们在最后检查上出了岔子。"),
            348: ("Will this blue cushion match the sofa?", "这个蓝色靠垫和沙发搭吗？", "Yes, it fits with that colour scheme.", "搭，它适合那个配色。"),
            380: ("Why are you buying balloons and snacks?", "你为什么买气球和零食？", "We're throwing a party for Mia on Saturday.", "我们周六要为米娅办派对。"),
            511: ("How do you organise your filing?", "你怎么整理文件？", "We go by date, newest first.", "我们按日期排，最新的在前。"),
            571: ("Does your son try new food?", "你儿子愿意尝试新食物吗？", "No, he's a picky eater.", "不太愿意，他很挑食。"),
            577: ("Why are you carrying a ladder and paint?", "你为什么带着梯子和油漆？", "I'm on a mission to fix the shed.", "我有个任务，要去修工具棚。"),
            581: ("Why are you still working so late?", "你为什么还工作到这么晚？", "I don't want to let the team down.", "我不想让团队失望。"),
            582: ("You passed after studying hard. How do you feel?", "你努力学习后通过了，感觉怎么样？", "I finally feel worthy of the result.", "我终于觉得自己配得上这个结果。"),
            584: ("This has been a special day. What should we do?", "今天很特别，我们该怎么做？", "Let's hold on to this memory.", "让我们珍惜这段回忆。"),
            621: ("What did you learn after weeks of practice?", "练了几周后你学到了什么？", "The key insight is that steady practice matters.", "关键领悟是持续练习很重要。"),
            622: ("How did you remove the old paint?", "你怎么去掉旧油漆？", "We chipped away at it with a scraper.", "我们用刮刀一点点刮掉。"),
            652: ("How do you stay consistent with exercise?", "你怎么坚持锻炼？", "I show up for my goals every morning.", "我每天早上都为目标行动。"),
            692: ("What did the teacher say was most important?", "老师说什么最重要？", "One key insight is to practise consistently.", "一个关键领悟是要持续练习。"),
            719: ("Why is every drawer open?", "为什么每个抽屉都开着？", "I'm a hot mess today.", "我今天乱成一团。"),
            820: ("What happened after the company went bankrupt?", "公司破产后发生了什么？", "A lawyer was appointed liquidator.", "一位律师被任命为清算人。"),
            840: ("Can I have a piece of cake now?", "我现在能吃一块蛋糕吗？", "Not yet—keep an eye on it while it cools.", "还不行，放凉时盯着它。"),
            900: ("Can you join us for dinner tonight?", "你今晚能和我们一起吃饭吗？", "I can't; I have other commitments tonight.", "不行，我今晚还有别的安排。"),
            950: ("Why does everyone look upset after the results?", "结果出来后大家为什么看起来很难过？", "I've never seen so many long faces.", "我从没见过这么多愁眉苦脸的人。"),
            955: ("Which route should we take?", "我们该走哪条路？", "In my opinion, the coastal road is safer.", "我认为沿海那条路更安全。"),
            971: ("Can I hand in this half-finished draft?", "我能交这份半成品草稿吗？", "No, that's not gonna cut it.", "不行，这可不够好。"),
            987: ("Why did you bring flowers to work?", "你为什么带花来上班？", "I don't know if you've heard, but Maya had a baby.", "不知道你听说没有，玛雅生宝宝了。"),
            990: ("Did you see the driver who left?", "你看清离开的那个司机了吗？", "No, I couldn't get a good look at him.", "没有，我没看清他的样子。"),
            1006: ("Do you need a full report now?", "你现在需要完整报告吗？", "No, a brief overview is enough; feel free to keep it short.", "不用，简短概览就够了，尽管写短一些。"),
            1047: ("Why were there so many stalls and shoppers?", "为什么有这么多摊位和顾客？", "It was a big market on Saturday.", "周六是个很大的集市。"),
            1052: ("Which jacket do you want?", "你想要哪件外套？", "I have my eye on the green one.", "我看中那件绿色的。"),
            1445: ("The printer is working again.", "打印机又正常了。", "There we go—it's finally printing.", "好了，终于开始打印了。"),
            1680: ("Why did you choose a later flight?", "你为什么选了晚一点的航班？", "We had to take into account the weather.", "我们必须把天气考虑进去。"),
        }
        return CURATED_REAL_LIFE_SCENES.get(item_id) or scenes.get(item_id)

    @staticmethod
    def _scene_subject(sentence):
        """Extract a short, speakable topic from a declarative reply."""
        match = re.match(
            r"^(?P<subject>(?:the|this|that|my|our|his|her|their|a|an)\s+"
            r"(?:[A-Za-z][A-Za-z'’-]*\s+){0,4}[A-Za-z][A-Za-z'’-]*|"
            r"I|we|you|he|she|they|it|there)\b",
            (sentence or "").strip(),
            re.I,
        )
        return match.group("subject") if match else ""

    @staticmethod
    def _lowercase_subject(subject):
        if not subject or subject == "I":
            return subject
        return subject[:1].lower() + subject[1:]

    @staticmethod
    def _declarative_parts(sentence):
        """Find a simple subject and finite verb without pulling a verb into it.

        The source notes are intentionally free-form, so this is a small
        spoken-English parser rather than a grammar engine.  It is enough to
        turn ``The report glossed over ...`` into the topic ``the report``
        instead of the old malformed ``the report glossed over``.
        """
        value = (sentence or "").strip()
        if re.match(r"^(?:after|when|while|because)\b", value, re.I) and "," in value:
            value = value.split(",", 1)[1].strip()
        words = re.findall(r"[A-Za-z]+(?:['’][A-Za-z]+)?", value)
        if len(words) < 2:
            return "", "", ""
        forms = {
            "am", "are", "be", "been", "being", "can", "could", "did", "do", "does", "had", "has", "have",
            "is", "may", "might", "must", "shall", "should", "was", "were", "will", "would",
            "became", "become", "began", "begin", "believe", "broke", "break", "called", "call", "caused", "cause",
            "changed", "change", "come", "consider", "continued", "continue", "covered", "cover", "decided", "decide",
            "depend", "disagree", "drew", "draw", "engaged", "engage", "exposed", "expose", "extended", "extend",
            "filled", "fill", "found", "find", "gave", "give", "go", "goes", "got", "get", "held", "hold",
            "included", "include", "increased", "increase", "kept", "keep", "landed", "land", "looked", "look",
            "made", "make", "meant", "moved", "move", "needed", "need", "noticed", "notice", "owned", "own",
            "performed", "perform", "pointed", "point", "posed", "pose", "provided", "provide", "received", "receive", "referred", "refer",
            "remained", "remain", "represented", "represent", "required", "require", "ran", "run", "said", "say", "saw",
            "see", "seemed", "seem", "showed", "show", "spanned", "span", "started", "start", "stuck", "stick",
            "surged", "surge", "took", "take", "travelled", "traveled", "travel", "turned", "turn", "used", "use",
            "waited", "wait", "walked", "walk", "wore", "wear", "worked", "work",
        }
        for index, word in enumerate(words[1:], start=1):
            lower = word.lower()
            root = lower[:-1] if lower.endswith("s") else lower
            auxiliaries_or_irregular = {
                "am", "are", "be", "been", "being", "can", "could", "did", "do", "does", "had", "has", "have",
                "is", "may", "might", "must", "shall", "should", "was", "were", "will", "would",
                "became", "began", "broke", "came", "drew", "found", "gave", "got", "held", "kept", "made", "ran",
                "said", "saw", "shot", "spoke", "stuck", "took", "went", "wore",
            }
            prior = words[index - 1].lower()
            is_verb = (
                lower in auxiliaries_or_irregular
                or lower.endswith(("ed", "ing"))
                or (lower.endswith("s") and root in forms)
                or (lower in forms and prior.endswith("s") and not prior.endswith(("'s", "’s")))
            )
            if (
                index == 1
                and words[0].lower() in {"a", "an", "the", "this", "that"}
                and lower.endswith("ing")
            ):
                is_verb = False
            if index == 1 and words[0].lower() in {"a", "an", "the", "this", "that"}:
                next_word = words[index + 1].lower() if index + 1 < len(words) else ""
                next_root = next_word[:-1] if next_word.endswith("s") else next_word
                next_is_verb = (
                    next_word in forms or next_root in forms or next_word.endswith(("ed", "ing"))
                )
                if next_is_verb and lower not in {"is", "are", "was", "were", "has", "have", "had"}:
                    is_verb = False
            if not is_verb:
                continue
            subject = " ".join(words[:index]).strip(" ,")
            if subject.lower() in {"and", "but", "so"}:
                continue
            return subject, word, " ".join(words[index + 1:]).strip()
        return "", "", ""

    @staticmethod
    def _verb_root(verb):
        irregular = {
            "gave": "give", "got": "get", "went": "go", "ran": "run", "saw": "see", "took": "take",
            "made": "make", "found": "find", "thought": "think", "wore": "wear", "bought": "buy",
        }
        lower = (verb or "").lower()
        if lower in irregular:
            return irregular[lower]
        if lower.endswith("ies"):
            return lower[:-3] + "y"
        if lower.endswith("es"):
            return lower[:-2]
        if lower.endswith("s") and len(lower) > 3:
            return lower[:-1]
        if lower.endswith("ed") and len(lower) > 4:
            return lower[:-2]
        return lower

    @classmethod
    def _imperative_scene_question(cls, sentence):
        """Give an instruction a real trigger instead of an unrelated opener."""
        lower = sentence.lower().strip()
        lower = re.sub(r"^(?:come on[,!]?\s*|just\s+)", "", lower)
        if re.match(r"^(?:twist|unscrew)\s+.*\b(?:cap|lid)\b", lower):
            return "The cap is stuck. How do I get it off?", "盖子卡住了，怎么打开？"
        if lower.startswith("check the rear-view mirror"):
            return "Which mirror should I check before reversing?", "倒车前我该看哪面镜子？"
        if lower.startswith("check "):
            return "Before we leave, what should I check first?", "出发前我该先检查什么？"
        if lower.startswith(("put on ", "put some ")):
            return "The mosquitoes are out. What should I put on?", "有蚊子了，我该涂什么？"
        if lower.startswith("put "):
            return "Where should I put it for now?", "我现在该把它放在哪里？"
        if lower.startswith(("bring ", "take ")):
            return "What should I bring with me?", "我该带什么？"
        if lower.startswith(("grab ", "pick up ")):
            return "What should I pick up first?", "我该先拿什么？"
        if lower.startswith("cut "):
            return "How should I cut this paper?", "这张纸应该怎么剪？"
        if lower.startswith(("turn on ", "turn off ")):
            return "What should I do with it before we go?", "我们走之前该怎么处理它？"
        if lower.startswith(("don't ", "do not ")):
            return "I'm about to do that. Is there anything I should avoid?", "我正准备这么做，有什么需要避免的吗？"
        if lower.startswith("please "):
            return "What would you like me to do first?", "你希望我先做什么？"
        if re.match(
            r"^(?:ask|blow|call|carry|chew|chip|clean|close|come|cut|do|dump|feel|fix|get|go|learn|look|"
            r"make|move|pick|pull|refer|run|say|set|show|shrug|start|stop|take|throw|try|use|walk|wipe|work)\b",
            lower,
        ):
            return "I'm not sure what to do here. What should I do?", "我不确定这里该怎么做，你建议我怎么做？"
        return None

    @classmethod
    def _personal_scene_question(cls, sentence):
        """Prompt a first-person answer with a question about that action."""
        lower = sentence.lower().strip()
        if re.search(r"\bkeep pace\b", lower):
            return "Was he walking faster than you?", "他走得比你快吗？"
        if re.search(r"\bdefer to\b", lower):
            return "Who should make the final call?", "最后该由谁来决定？"
        if re.search(r"\bdisagree\b", lower):
            return "What do you think of that description?", "你怎么看那个说法？"
        if re.search(r"\bhad a sudden impulse\b", lower):
            return "What made you want to call him all of a sudden?", "是什么让你突然想打给他？"
        if re.search(r"\bfrom time to time\b", lower):
            return "Do you still go there often?", "你现在还常去那里吗？"
        if re.search(r"\bowe you\b", lower):
            return "Why do you owe me a favour?", "你为什么欠我一个人情？"
        if re.search(r"\b(?:deem|think).*(?:restaurant|café|cafe)\b", lower):
            return "What did you think of the restaurant?", "你觉得这家餐厅怎么样？"
        if re.search(r"\bwork with\b", lower):
            return "Who do you work with?", "你和谁一起工作？"
        if re.search(r"\bfeel\b", lower):
            return "How do you feel about it?", "你对此感觉怎么样？"
        if re.search(r"\b(?:want|hope|plan)\b", lower):
            return "What are you hoping to do?", "你希望做什么？"
        if re.search(r"\bneed\b", lower):
            return "What do you need?", "你需要什么？"
        if "last week" in lower:
            return "What did you do last week?", "你上周做了什么？"
        if "yesterday" in lower:
            return "What did you do yesterday?", "你昨天做了什么？"
        if "when i was a kid" in lower or "when i was young" in lower:
            return "What did you enjoy doing when you were young?", "你小时候喜欢做什么？"
        if lower.startswith("i bought "):
            return "What did you buy?", "你买了什么？"
        if lower.startswith("i got "):
            return "What did you get?", "你得到了什么？"
        if lower.startswith("i watched "):
            return "What did you watch?", "你看了什么？"
        if lower.startswith("i went "):
            return "Where did you go?", "你去了哪里？"
        if lower.startswith("i ended up "):
            return "What did you end up doing?", "你最后做了什么？"
        if lower.startswith("i tried "):
            return "What were you trying to do?", "你当时想做什么？"
        if lower.startswith("i long for "):
            return "What do you miss about the past?", "你怀念过去的什么？"
        if re.match(r"^i(?:'m|’m| am| was| were| have|’ve| had| will|’ll)\b", lower):
            return "What have you been doing?", "你最近在做什么？"
        return "Can you tell me what happened?", "你能说说发生什么了吗？"

    @classmethod
    def _group_scene_question(cls, sentence):
        lower = sentence.lower().strip()
        after = re.search(r"\bafter (?P<event>[^,.!?]+)", sentence, re.I)
        if after and re.search(r"\b(?:received|got|heard|saw)\b", lower):
            return f"What happened after {after.group('event')}?", "后来发生了什么？"
        if re.search(r"\bneed\b", lower):
            return "What do we need?", "我们需要什么？"
        if re.search(r"\b(?:decided|chose|agreed)\b", lower):
            return "What did you decide to do?", "你们最后决定怎么做？"
        if re.match(r"^we(?:'re|’re| are| were| will|’ll)\b", lower):
            return "What are you doing there?", "你们在那里做什么？"
        if lower.startswith("we booked "):
            return "How are you travelling there?", "你们准备怎么去那里？"
        return "What did you decide to do together?", "你们最后一起决定怎么做？"

    @classmethod
    def _third_person_scene_question(cls, sentence):
        lower = sentence.lower().strip()
        subject = lower.split(None, 1)[0] if lower else "they"
        person, be, past_be = {
            "he": ("he", "is", "was"),
            "she": ("she", "is", "was"),
            "they": ("they", "are", "were"),
        }.get(subject, ("they", "are", "were"))
        if re.search(r"\btwisted (?:his|her) ankle\b", lower):
            return "Why is he limping?", "他为什么一瘸一拐的？"
        if re.search(r"\bstuck up for\b", lower):
            return "Why was that colleague being criticised?", "那位同事为什么被批评？"
        if re.search(r"\bpored over\b", lower):
            return "How did he prepare for the trip?", "他是怎么为旅行做准备的？"
        if re.search(r"\bgot beaten up\b", lower):
            return "Why does he have a black eye?", "他为什么有黑眼圈？"
        if re.search(r"\blost it\b", lower):
            return "Why did he shout during the argument?", "他为什么在争吵时大喊？"
        if re.search(r"\b(?:made|make) a compelling argument\b", lower):
            return "Why did she argue for that change?", "她为什么主张做那个改变？"
        if re.search(r"\b(?:has|have) a fascination with\b", lower):
            return "What is he especially interested in?", "他对什么特别感兴趣？"
        if re.search(r"\b(?:is|are|was|were)\b", lower):
            return f"How {be} {person} doing?", "他／她／他们怎么样？"
        return f"What did {person} do?", "他／她／他们做了什么？"

    @classmethod
    def _action_scene_question(cls, sentence, subject, verb, rest):
        """Turn an ordinary factual sentence into a direct, connected question.

        This is intentionally modest: the source note supplies the answer,
        while the prompt asks about the same action, time, or result.  It is
        much more natural than the former "I was looking at …" vocabulary
        prompt and remains useful for the many notes that have no dialogue.
        """
        lower = sentence.lower().strip()
        natural_subject = cls._lowercase_subject(subject)
        temporal = re.search(r"\bafter (?P<event>[^,.!?]+)", sentence, re.I)
        modal = re.search(r"\b(can|could|will|would|may|might|should|must)\b", lower)
        if modal and temporal:
            action = re.match(r"(?P<verb>[A-Za-z]+)", (rest or "").strip())
            if action:
                return (
                    f"When {modal.group(1)} {natural_subject} {action.group('verb')}?",
                    "它什么时候会这样？",
                )
        if temporal:
            return (
                f"What happened after {temporal.group('event')}?",
                "那之后发生了什么？",
            )
        if re.search(r"\badvertis(?:e|ed|es|ing)\b", lower):
            object_match = re.search(
                r"\badvertis(?:e|ed|es|ing)\s+(?P<object>.+?)(?:\s+(?:heavily|widely|online))?[.!?]?$",
                sentence,
                re.I,
            )
            object_text = object_match.group("object") if object_match else "the product"
            return (
                f"How did {natural_subject} promote {object_text}?",
                "它是怎么推广的？",
            )
        if re.search(r"\bbroke into (?:spontaneous )?applause\b", lower):
            return f"How did {natural_subject} react?", "大家有什么反应？"
        if re.search(r"\b(?:feel|feels|felt)\b", lower):
            return f"How does {natural_subject} feel?", "它感觉怎么样？"
        if re.search(r"\b(?:use|uses|used)\b", lower) and re.search(r"\bto\b", lower):
            object_match = re.search(r"\buse[sd]?\s+(?P<object>.+?)\s+to\b", sentence, re.I)
            object_text = object_match.group("object") if object_match else "it"
            plural = bool(re.search(r"(?:^|\s)(?:these|those|they|we)\b", natural_subject, re.I)) or (
                natural_subject.lower().endswith("s") and not natural_subject.lower().endswith("ss")
            )
            auxiliary = "do" if plural else "does"
            return f"What {auxiliary} {natural_subject} use {object_text} for?", "它用这个来做什么？"
        if modal:
            return f"What {modal.group(1)} {natural_subject} do?", "它能／会做什么？"
        if cls._verb_root(verb) in {"be", "seem", "look", "remain"}:
            return f"How is {natural_subject}?", "它的情况怎么样？"
        if re.search(r"\b(?:because|due to|owing to)\b", lower):
            return f"Why did {natural_subject} do that?", "它为什么会这样做？"
        if verb.lower().endswith(("ed", "t")):
            return f"What did {natural_subject} do?", "它做了什么？"
        return f"What does {natural_subject} do?", "它做什么？"

    @classmethod
    def _declarative_scene_question(cls, sentence):
        """Create a topic-linked lead-in for a factual source sentence."""
        lower = sentence.lower().strip()
        if re.search(r"\b(?:was|were) built in\b", lower):
            subject = cls._scene_subject(sentence) or "this building"
            return f"Do you know when {cls._lowercase_subject(subject)} was built?", "你知道它是什么时候建的吗？"
        if "dates back to" in lower:
            return "How old is this building?", "这座建筑有多久历史了？"
        if re.match(r"^it cost\b", lower):
            return "How much did it cost?", "它花了多少钱？"
        substitute = re.search(r"there is no substitute for (?P<thing>.+?)[.!?]?$", sentence, re.I)
        if substitute:
            thing = substitute.group("thing").rstrip(".")
            return f"Can anything replace {thing}?", "有什么能取代它吗？"
        if "gave the proposal" in lower and "backing" in lower:
            return "Did the board support the proposal?", "董事会支持这个提案吗？"
        if "needs a complete revamp" in lower:
            return "Does the website need a small update or a full redesign?", "这个网站只需小改，还是得彻底改版？"
        if "went viral" in lower:
            return "Did people start sharing the video after it was posted?", "视频发布后，大家开始转发了吗？"
        if lower.startswith("the report "):
            return "What did the report say about it?", "报告对此怎么说？"
        if lower.startswith("the police "):
            return "What did the police find?", "警方发现了什么？"
        if lower.startswith("the board "):
            return "What did the board decide?", "董事会作了什么决定？"
        if lower.startswith("the website "):
            return "What does the website need?", "这个网站需要什么？"
        if lower.startswith("the video "):
            return "What happened after the video was posted?", "视频发布后发生了什么？"
        if lower.startswith("there is ") or lower.startswith("there are "):
            noun = re.sub(r"^there (?:is|are)\s+", "", sentence, flags=re.I).split(".", 1)[0]
            return f"What did you notice about {noun}?", "你注意到什么情况了吗？"
        if lower.startswith("there "):
            return "What has changed recently?", "最近有什么变化？"
        subject, verb, rest = cls._declarative_parts(sentence)
        if subject.lower() in {"i", "we", "you", "he", "she", "they"}:
            # Contractions are normalised by the caller, but preserve this
            # guard for source notes that omit an apostrophe.
            if subject.lower() == "i":
                return cls._personal_scene_question(sentence)
            if subject.lower() == "we":
                return cls._group_scene_question(sentence)
            if subject.lower() == "you":
                return "What should I do?", "我该怎么做？"
            return cls._third_person_scene_question(sentence)
        if subject and re.search(r"\bfilled (?:me|him|her|them) with\b", lower):
            return f"How did {cls._lowercase_subject(subject)} make you feel?", "它让你有什么感觉？"
        if subject and cls._verb_root(verb) == "need":
            return f"What does {cls._lowercase_subject(subject)} need?", "它需要什么？"
        if subject and cls._verb_root(verb) in {"be", "seem", "look", "remain"}:
            return f"How is {cls._lowercase_subject(subject)}?", "它的情况怎么样？"
        if subject and subject.lower() in {"this", "that", "it"}:
            return cls._action_scene_question(sentence, subject, verb, rest)
        if subject:
            return cls._action_scene_question(sentence, subject, verb, rest)
        return "What happened in that situation?", "当时发生了什么？"

    @classmethod
    def _scene_for_question(cls, question, chinese):
        """Keep a question-shaped source sentence inside a coherent exchange."""
        value = cls._normalise_practice_sentence(question)
        lower = value.lower()
        if lower.startswith(("why ", "how come")):
            reply = "I'm not sure. Let's look into it together."
            reply_chinese = "我也不确定，我们一起查一下吧。"
        elif lower.startswith(("can ", "could ", "would ", "do you want")):
            reply = "Yes, of course."
            reply_chinese = "当然可以。"
        elif lower.startswith(("where ", "what ", "which ")):
            reply = "Let me check for you."
            reply_chinese = "我帮你查一下。"
        elif lower.startswith("how "):
            reply = "Let me show you."
            reply_chinese = "我给你演示一下。"
        else:
            reply = "Let's work it out together."
            reply_chinese = "我们一起弄清楚吧。"
        return [
            {"speaker": "人物 A", "english": value, "chinese": chinese},
            {"speaker": "人物 B", "english": reply, "chinese": reply_chinese},
        ]

    @classmethod
    def _scene_question(cls, item, sentence, phrase):
        """Create a concrete, spoken lead-in for the selected source reply."""
        lower = sentence.lower()
        if "scraggly beard" in lower:
            return "Has he had time to trim his beard lately?", "他最近有时间修胡子吗？"
        if "vines began to scraggle" in lower:
            return "Why are the vines spreading over the fence like that?", "藤蔓怎么那样蔓到篱笆上去了？"
        if "garden looked straggly" in lower:
            return "How did the garden look after the dry summer?", "干燥的夏天过后，花园看起来怎么样？"
        if lower.startswith("it refers to water"):
            return (
                "The sign says the town uses hydroelectric power. What does hydro- refer to there?",
                "牌子上说这个小镇使用水电，这里的 hydro- 指什么？",
            )
        if lower in {"good morning", "good morning!", "good afternoon", "good afternoon!", "good evening", "good evening!"}:
            return "Hi, Mrs. Chen. You're up early today.", "早上好，陈太太。您今天起得真早。"
        if lower.startswith(("don't worry", "don’t worry")):
            return "I'm worried that I'm the only one having a hard time.", "我担心只有我一个人觉得很难。"
        if lower.startswith(("no worries", "it's all good", "it’s all good")):
            return "I'm sorry I kept you waiting.", "抱歉让你久等了。"
        if lower.startswith(("so we'll see", "so we’ll see", "we'll see", "we’ll see")):
            return "Do you think the weather will clear up?", "你觉得天气会放晴吗？"
        if lower.startswith(("i don't mind", "i don’t mind", "i'm not bothered", "i’m not bothered")):
            return "Do you have a preference?", "你有特别想选的吗？"
        imperative = cls._imperative_scene_question(sentence)
        if imperative:
            return imperative
        if lower.startswith("let me "):
            return "Could you explain that to me?", "你能给我解释一下吗？"
        if re.search(r"\b(?:was|were) built in\b", lower):
            return cls._declarative_scene_question(sentence)
        if sentence.strip().endswith("?"):
            if lower.startswith(("how do ", "how can ")):
                return "I'm stuck and don't know what to do next.", "我卡住了，不知道下一步该怎么做。"
            if lower.startswith("would somebody"):
                return "The lights just went out.", "灯刚刚灭了。"
            if lower.startswith("can you fill me in"):
                return "I arrived after everyone had started talking.", "大家开始聊天后我才到。"
            if lower.startswith("is there a way"):
                return "We had to stop halfway through the task.", "我们做到一半就不得不停下来了。"
            if re.search(r"what have you been up to", lower):
                return "I haven't seen you since last month.", "我从上个月起就没见过你。"
            if re.search(r"what are you on about", lower):
                return "I said we should change the plan at the last minute.", "我说我们应该临时改一下计划。"
            if re.match(r"^(?:can|could) i\b", lower):
                return cls._scenario_context(item, phrase)
            return "Something has everyone thinking for a moment.", "这件事让大家一时都在琢磨。"
        if lower.startswith(("let's ", "let’s ")):
            return "We've finished the first part. What should we do now?", "第一部分已经做完了。接下来该做什么？"
        if lower.startswith(("please ",)):
            return "What would you like me to do first?", "你希望我先做什么？"
        if lower.startswith("put "):
            return "Where should I put the photo?", "这张照片该放在哪里？"
        if lower.startswith("check "):
            return "Which one should I look at first?", "我应该先看哪一个？"
        if lower.startswith("you know the drill"):
            return "Do we need to go through the rules again?", "我们还需要再讲一遍规则吗？"
        if lower.startswith("have a bash"):
            return "Do you want to try making one yourself?", "你想自己试着做一个吗？"
        if lower.startswith("please stick"):
            return "The path is steep. Should I slow down?", "这条路很陡，我要不要慢一点？"
        if lower.startswith("don't procrastinate") or lower.startswith("don’t procrastinate"):
            return "I keep putting the application off.", "我一直拖着不写申请。"
        if lower.startswith(("cut it out", "stop ")):
            return "The children keep making noise in the next room.", "隔壁房间的孩子一直在吵闹。"
        if re.search(r"\b(?:subsequently|afterward|afterwards|later|then|eventually)\b", lower):
            before = re.split(r"\s+(?:and\s+)?(?:subsequently|afterward|afterwards|later|then|eventually)\b", sentence, maxsplit=1, flags=re.I)[0].rstrip(" ,")
            if before:
                before = before[:1].lower() + before[1:]
                return f"What happened after {before}?", "后来发生了什么？"
        if re.search(r"\b(?:running short|run short|run out of)\s+(?:on |of )?time\b", lower):
            return "The café closes in ten minutes. Can we keep talking?", "咖啡馆十分钟后就关门了。我们还能继续聊吗？"
        if "in the same boat" in lower:
            return "I'm finding this new routine difficult too.", "我也觉得这个新安排很难适应。"
        if "out of the equation" in lower:
            return "I keep changing my mind about it.", "我总是对这件事犹豫不决。"
        if "condone" in lower:
            return "A student asked whether fighting was allowed.", "有个学生问打架是不是可以被允许。"
        if "joke went" in lower or "went too far" in lower:
            return "He made a joke about her family.", "他拿她的家人开了个玩笑。"
        if "strip it back" in lower:
            return "This poster is full of extra details.", "这张海报塞满了多余的细节。"
        if "ripped me off" in lower or "ripped us off" in lower:
            return "That souvenir cost far more than I expected.", "那个纪念品比我预期贵得多。"
        if lower.startswith("my friend is outside"):
            return "Is your friend here already?", "你的朋友已经到了吗？"
        location = re.match(
            r"^(?P<subject>(?:the|a|an|my|our|his|her|this|that)\s+.+?)\s+(?P<verb>is|are|was|were)\s+(?:in|on|at|under|near|behind)\b",
            sentence,
            re.I,
        )
        if location and not re.search(r"\bat odds\b", lower):
            subject = location.group("subject")
            subject = subject[:1].lower() + subject[1:]
            pronoun = "they" if location.group("verb").lower() == "are" else "it"
            where_be = "are" if pronoun == "they" else "is"
            return f"I can't find {subject}. Where {where_be} {pronoun}?", "我找不到它了，它在哪里？"
        showcase = re.match(r"^(?P<subject>(?:the|this|that)\s+.+?)\s+showcases?\b", sentence, re.I)
        if showcase:
            return f"What does {showcase.group('subject').lower()} feature?", "它主要展示什么？"
        if re.match(r"^the problem was .+\b(?:fixed|solved)\b", lower):
            return "Did anyone manage to solve the problem?", "后来有人把这个问题解决了吗？"
        if re.match(r"^i(?:\s|['’])", lower):
            if lower.startswith("i think"):
                if "best age" in lower:
                    return "What age is best for a child to start learning?", "孩子几岁开始学习最好？"
                return "What did you think about what happened?", "你觉得刚才发生的事怎么样？"
            if lower.startswith("i work as"):
                return "What do you do for work?", "你是做什么工作的？"
            if lower.startswith("i sat in"):
                return "What did you do this morning?", "你今天早上做了什么？"
            if lower.startswith("i started"):
                return "When did you start?", "你是什么时候开始的？"
            if lower.startswith("i look back"):
                return "What do you remember most about those days?", "你最记得那段日子的什么？"
            if lower.startswith("i need"):
                return "You've been thinking about this all morning. What do you need?", "你整个早上都在想这件事。你需要什么？"
            return cls._personal_scene_question(sentence)
        if re.match(r"^we(?:\s|['’])", lower):
            if lower.startswith("we need"):
                return cls._group_scene_question(sentence)
            if lower.startswith("we cannot") or lower.startswith("we can't") or lower.startswith("we can’t"):
                return "What should we do about it?", "这件事我们该怎么处理？"
            return cls._group_scene_question(sentence)
        if re.match(r"^you(?:\s|['’])", lower):
            if re.search(r"\b(?:enough|sufficient)\b", lower):
                return "I'm worried I won't finish my homework.", "我担心自己做不完作业。"
            if "found some stuff out" in lower:
                return "Did you learn anything useful?", "你发现什么有用的内容了吗？"
            if "can tell straight away" in lower:
                return "How do you know when someone is lying?", "你怎么知道有人在说谎？"
            return "What should I do?", "我该怎么做？"
        if re.match(r"^(?:he|she|they)(?:\s|['’])", lower):
            return cls._third_person_scene_question(sentence)
        if lower.startswith(("don't ", "do not ", "let's ", "please ")):
            return "What should we do next?", "接下来我们该怎么做？"
        if re.search(r"\b(?:novel|book|story)\b", lower):
            return "What kind of story is it?", "这是一个什么样的故事？"
        if re.search(r"\b(?:cloud|rain|storm|weather)\b", lower):
            return "Should we head home before the weather changes?", "天气变坏前我们要不要先回家？"
        if re.search(r"\b(?:view|mountain|beach|gorge)\b", lower):
            return "How was the view from up there?", "从上面看到的景色怎么样？"
        if lower.startswith("that's a brilliant") or lower.startswith("that’s a brilliant"):
            return "What do you think of my plan?", "你觉得我的计划怎么样？"
        if lower.startswith("that old photo"):
            return "How did the old photo make you feel?", "那张旧照片让你有什么感觉？"
        if lower.startswith("this is your send-off"):
            return "What is this event for?", "这个活动是为了什么？"
        if lower.startswith("that was his ultimate goal"):
            return "What did he want most?", "他最想要的是什么？"
        if lower.startswith("it rained"):
            return "Why are the garden paths so wet?", "花园的小路为什么这么湿？"
        if "sharemarket" in lower:
            return "What happened in the market today?", "今天市场发生什么事了？"
        if "staycation" in lower:
            return "Are you going away this year?", "你今年会出门旅行吗？"
        if "kick them out" in lower:
            return "What happens if someone keeps shouting?", "如果有人一直大声吵闹怎么办？"
        if "great deal of change" in lower:
            return "Has much changed at work?", "工作上变化很大吗？"
        if "panel was optimistic" in lower:
            return "What did the panel think would happen next?", "专家小组觉得接下来会怎样？"
        if "workshop" in lower:
            return "What did the workshop leader say?", "工作坊的带领人怎么说？"
        return cls._declarative_scene_question(sentence)

    @classmethod
    def _fallback_expression(cls, phrase):
        first = re.split(r"[\n/|;]+", phrase or "", maxsplit=1)[0]
        return re.sub(r"\s+", " ", first).strip(" .。") or "that"

    @classmethod
    def _fallback_reply(cls, item, phrase, meaning):
        """Use the target expression in an ordinary, non-teaching exchange."""
        expression = cls._fallback_expression(phrase)
        lower = expression.lower()
        combined = f"{item.get('chinese_text') or ''}\n{item.get('explanation') or ''}"
        direct_starters = (
            "i ", "i'm ", "i’m ", "we ", "we're ", "we’re ", "you ", "he ", "she ",
            "they ", "it ", "there ", "this ", "that ", "let's ", "let’s ", "don't ", "do not ",
            "please ", "can ", "could ", "would ", "will ", "what ", "where ", "why ", "how ",
        )
        if lower.startswith(direct_starters) or expression.endswith(("?", "!", ".")):
            return expression, meaning
        if lower in {"good morning", "good afternoon", "good evening", "hello", "hi", "no worries"}:
            return f"{expression}!", meaning
        if lower == "called" or lower.startswith("called "):
            return "The event is called “Spring Market.”", "这个活动叫“春日集市”。"
        if lower.startswith("from ") and " to " in lower:
            return "The route goes from the station to the beach.", "这条路线从车站一直通到海边。"
        if re.search(r"(?:副词|adverb)", combined, re.I):
            return f"She explained it {expression}.", "她把这件事解释得很清楚。"
        if re.search(r"(?:形容词|adjective)", combined, re.I):
            if re.search(r"(?:可行|现实|可能)", combined):
                return f"The plan looks {expression}.", "这个计划看起来可行。"
            return f"The view was {expression}.", "景色非常好。"
        if re.search(r"(?:小巷|街道|道路|车站|机场|海边|地方|位置|方向)", combined):
            return f"Let's take the {expression} behind the café.", "我们从咖啡馆后面那条路走吧。"
        if re.search(r"(?:糕点|面包|食物|甜点|咖啡)", combined):
            return f"I'd like a {expression} with my coffee.", "我想点一份糕点配咖啡。"
        if re.search(r"(?:动词|verb)", combined, re.I) or lower.startswith("to "):
            verb = re.sub(r"^to\s+", "", expression, flags=re.I)
            verb = re.sub(r"\bsomething\b", "this", verb, flags=re.I)
            verb = re.sub(r"\bsomeone\b", "them", verb, flags=re.I)
            return f"We need to {verb} before we leave.", "我们离开前得先把这件事处理好。"
        if re.search(r"(?:ance|ence|ity|ness|ment|ship|ism|ology)$", lower):
            return f"Our {expression} on it is growing.", "我们对它的依赖越来越强。"
        return f"I noticed a {expression} on my way home.", "我回家路上注意到了这个东西。"

    @classmethod
    def _fallback_lead_in(cls, reply_english, item, phrase):
        lower = reply_english.lower()
        if lower.startswith("let's take "):
            return "The main street is blocked. Is there another way?", "大路被堵住了，还有别的路吗？"
        if lower.startswith("i'd like ") or lower.startswith("i’d like "):
            return "What would you like with your coffee?", "你的咖啡想配点什么？"
        if lower.startswith("the plan looks "):
            return "Do you think we can finish this before Friday?", "你觉得我们周五前能完成吗？"
        if lower.startswith("we need to "):
            return "What should we do before we leave?", "我们离开前该做什么？"
        if lower.startswith("our ") and " on it is growing" in lower:
            return "Do you think we're depending on it too much?", "你觉得我们是不是太依赖它了？"
        if lower.startswith("she explained "):
            return "How did she explain it to you?", "她是怎么向你解释的？"
        if lower.startswith("the event is called "):
            return "What is the event called?", "这个活动叫什么名字？"
        if lower.startswith("the route goes "):
            return "How do we get from the station to the beach?", "我们怎么从车站去海边？"
        if lower.startswith("i noticed "):
            return "What did you notice on your way home?", "你回家路上注意到了什么？"
        return cls._declarative_scene_question(reply_english)

    @classmethod
    def _curated_split_scene(cls, item, phrase):
        key = (item.get("id"), cls._expression_key(phrase))
        return (
            CURATED_REAL_LIFE_EXPRESSION_SCENES.get(key)
            or cls._CURATED_SPLIT_SCENES.get(key)
        )

    @classmethod
    def _fallback_scene(cls, item, phrase, prompt_meaning):
        curated = cls._curated_split_scene(item, phrase) or cls._curated_scene(item["id"])
        if curated:
            first_english, first_chinese, reply_english, reply_chinese = curated
            return [
                {"speaker": "人物 A", "english": first_english, "chinese": first_chinese},
                {"speaker": "人物 B", "english": reply_english, "chinese": reply_chinese},
            ]
        reply_english, reply_chinese = cls._fallback_reply(item, phrase, prompt_meaning)
        first_english, first_chinese = cls._fallback_lead_in(reply_english, item, phrase)
        scene = [
            {"speaker": "人物 A", "english": first_english, "chinese": first_chinese},
            {"speaker": "人物 B", "english": reply_english, "chinese": reply_chinese},
        ]
        if cls.is_low_quality_scene_dialogue(scene):
            raise HTTPException(
                422,
                "This note has no coherent real-life scene for the dialogue card.",
            )
        return scene

    @classmethod
    def _dialogue_lines(cls, item, phrase, meaning, key_sentence):
        prompt_meaning = cls._dialogue_meaning(item, meaning)
        # These cards were reviewed one by one because their source only has
        # a bare word or a fragmented note.  Prefer them to an automatically
        # guessed lead-in even when the source also contains a short example.
        curated = cls._curated_split_scene(item, phrase) or cls._curated_scene(item["id"])
        if curated:
            first_english, first_chinese, reply_english, reply_chinese = curated
            return [
                {"speaker": "人物 A", "english": first_english, "chinese": first_chinese},
                {"speaker": "人物 B", "english": reply_english, "chinese": reply_chinese},
            ]
        source_examples = cls._source_scene_examples(item, prompt_meaning, phrase)
        question_example = None
        for source_example in source_examples:
            reply = cls._normalise_practice_sentence(source_example["english"])
            # A question quoted from the notes belongs in the first turn.  It
            # should not be forced into the answer slot of a made-up prompt.
            if reply.endswith("?"):
                question_example = question_example or {
                    "english": reply,
                    "chinese": source_example["chinese"],
                }
                continue
            if not cls._is_usable_scene_sentence(reply):
                continue
            english, chinese = cls._scene_question(item, reply, phrase)
            scene = [
                {"speaker": "人物 A", "english": english, "chinese": chinese},
                {"speaker": "人物 B", "english": reply, "chinese": source_example["chinese"]},
            ]
            if not cls.is_low_quality_scene_dialogue(scene):
                return scene
        if question_example:
            scene = cls._scene_for_question(question_example["english"], question_example["chinese"])
            if not cls.is_low_quality_scene_dialogue(scene):
                return scene
        return cls._fallback_scene(item, phrase, prompt_meaning)

    @classmethod
    def _practice_expression(cls, item, phrase):
        """Pick the real expression practised by a thematic source card."""
        return cls._CURATED_PRACTICE_EXPRESSIONS.get(
            item.get("id"), cls.normalise_courseware_phrase(phrase)
        )

    @classmethod
    def _practice_patterns(cls, item, phrase, meaning, dialogue_lines, groups, pairs):
        """Build short, speakable fill-in sentences from real card content."""
        practice_expression = cls._practice_expression(item, phrase)
        curated_split_sentence = cls._CURATED_SPLIT_PRACTICE_SENTENCES.get(
            (item.get("id"), cls._expression_key(practice_expression)), ""
        )
        candidates = [
            curated_split_sentence,
            cls._CURATED_PRACTICE_SENTENCES.get(item.get("id"), ""),
        ]
        # In a natural conversation the expression may appear in either turn:
        # a request such as "Can you pop in?" belongs in the first turn,
        # whereas an instruction such as "Twist the cap off" is the reply.
        if len(dialogue_lines) > 1:
            candidates.append(dialogue_lines[1].get("english", ""))
            candidates.append(dialogue_lines[0].get("english", ""))
        candidates.append(practice_expression)
        candidates.extend(pair.get("english", "") for pair in pairs)
        candidates.extend(
            example.get("english", "")
            for group in groups
            for example in group.get("examples", [])
            if isinstance(example, dict)
        )
        patterns = []
        for candidate in candidates:
            pattern = cls._blank_keyword(candidate, practice_expression)
            if pattern and cls._is_meaningful_practice_sentence(pattern) and pattern not in patterns:
                patterns.append(pattern)
            # One strong sentence is preferable to several mechanically
            # generated frames.  A second source sentence adds useful variety
            # only when it is already present in the note.
            if len(patterns) == 2:
                return patterns

        if patterns:
            return patterns

        # Source notes often name a reusable frame such as ``stick up for sb``
        # while the sentence has an inflected verb and a real person in place
        # of ``sb``.  Keep the sentence and blank its target core rather than
        # replacing it with an instructional template.
        for candidate in candidates:
            pattern = cls._blank_keyword_anchor(candidate, practice_expression)
            if pattern and pattern not in patterns:
                patterns.append(pattern)
            if len(patterns) == 2:
                return patterns

        if patterns:
            return patterns

        reply, _ = cls._fallback_reply(item, practice_expression, meaning)
        pattern = cls._blank_keyword(reply, practice_expression)
        if pattern and cls._is_meaningful_practice_sentence(pattern):
            return [pattern]

        expression = cls._fallback_expression(practice_expression)
        if expression.lower() in {"good morning", "good afternoon", "good evening", "hello", "hi"}:
            return ["________, it's good to see you."]
        raise HTTPException(
            422,
            "This note has no complete, meaningful sentence for the output practice card.",
        )

    def _preview_item(self, item):
        phrase = self._card_phrase(item)
        if self.is_long_sentence_item(item):
            raise HTTPException(
                422,
                "Long sentence note items are not suitable for a standalone courseware card.",
            )
        source_meaning = (item["chinese_text"] or "来自学习笔记的核心表达。").strip()
        meaning = self._brief_meaning(item, source_meaning)
        usage_text = item["explanation"] or ""
        examples_text = item["examples"] or ""
        pairs = self._pairs(f"{usage_text}\n{examples_text}")
        key_sentence = pairs[0] if pairs else {"english": phrase, "chinese": meaning}
        uses = self._usage_groups(usage_text, pairs, item, examples_text)
        if not uses:
            # Some older cards contain only a definition.  They still need a
            # complete teaching card, so use the card's own expression and
            # meaning as the minimal, traceable usage example.
            uses = [{
                "title": "核心用法",
                "description": meaning,
                "examples": [key_sentence],
            }]
        dialogue_lines = self._dialogue_lines(item, phrase, meaning, key_sentence)
        comparison = self._comparison_items(examples_text)
        blocks = [
            {
                "block_code": "hero",
                "block_type": "hero",
                "title": "",
                "sort_order": 10,
                "payload": {
                    "phrase": phrase,
                    "meaning": meaning,
                    "memory": self._memory(item, meaning),
                    "key_sentence": key_sentence,
                },
            },
            {
                "block_code": "usage",
                "block_type": "usage_group",
                "title": "一个画面，延伸出不同用法",
                "sort_order": 20,
                "payload": {
                    "intro": "每张卡对应笔记中一个明确的用法，不把整段笔记直接堆到页面上。",
                    "uses": uses,
                },
            },
        ]
        blocks.append({
            "block_code": "scene-practice", "block_type": "dialogue", "title": "真实场景对话",
            "sort_order": 30,
            "payload": {"scene": "真实发生的日常场景", "intro": "把原笔记里的表达放进日常实际会发生的对话中。", "collocations": [use["title"] for use in uses], "lines": dialogue_lines},
        })
        if len(comparison) >= 2:
            blocks.append({
                "block_code": "comparison", "block_type": "comparison", "title": "别把这些表达混在一起",
                "sort_order": 40,
                "payload": {"intro": "以下内容来自笔记中的近义词／易混对比部分。", "items": comparison},
            })
        blocks.extend([
            {
                "block_code": "say-it", "block_type": "output", "title": "轮到你开口", "sort_order": 50,
                "payload": {
                    "instruction": "先读完整句，再把横线处填成今天要练的关键词。",
                    "patterns": self._practice_patterns(item, phrase, meaning, dialogue_lines, uses, pairs),
                },
            },
            {
                "block_code": "recap", "block_type": "recap", "title": "", "sort_order": 60,
                "payload": {
                    "summary": self._recap_summary(phrase, meaning),
                    "key_sentence": key_sentence,
                },
            },
        ])
        return {"phrase": phrase, "meaning": meaning, "blocks": blocks}

    def _preview_entries(self, source_item):
        split_entries = self._split_expression_entries(source_item)
        if not split_entries and self.has_unresolved_expression_collection(source_item):
            raise HTTPException(
                422,
                "This note contains multiple independent expressions. Split the note into separate entries or add an explicit Chinese definition for each expression before generating courseware.",
            )
        if not split_entries and self._card_phrase(source_item) == "Phrase collection":
            raise HTTPException(
                422,
                "This note is a collection of expressions. Split it into separate entries before generating courseware.",
            )
        if not split_entries:
            preview = self._preview_item(source_item)
            return [{
                "index": 0,
                "is_split": False,
                "source_item": dict(source_item),
                "item": dict(source_item),
                "source_locator": None,
                **preview,
            }]
        previews = []
        for entry in split_entries:
            preview = self._preview_item(entry["item"])
            previews.append({"is_split": True, **entry, **preview})
        return previews

    def preview(self, item_id):
        source_item = self._item(item_id)
        previews = self._preview_entries(source_item)
        primary = previews[0]
        return {
            "source_item": dict(source_item),
            # Preserve the original response shape for existing callers while
            # exposing all independently generated lesson cards.
            "blocks": primary["blocks"],
            "split": len(previews) > 1,
            "entries": [
                {
                    "index": entry["index"],
                    "phrase": entry["phrase"],
                    "meaning": entry["meaning"],
                    "blocks": entry["blocks"],
                    "source_locator": entry["source_locator"],
                }
                for entry in previews
            ],
        }

    def _resolve_generation_material(self, topic_id, actor, material_id):
        topic = self.db.execute(
            select(m.learning_topic).where(m.learning_topic.c.id == topic_id)
        ).mappings().first()
        if not topic:
            raise HTTPException(404, "Learning topic not found.")
        if material_id is None:
            material_code = "idiomatic-everyday-english"
            material_id = self.db.execute(
                select(m.learning_material.c.id).where(
                    m.learning_material.c.material_code == material_code,
                )
            ).scalar_one_or_none()
            if material_id is None:
                template_id = self.db.execute(
                    select(m.learning_template.c.id).where(
                        m.learning_template.c.template_code == "put-aside",
                        m.learning_template.c.template_version == 1,
                        m.learning_template.c.status == "active",
                    )
                ).scalar_one_or_none()
                material_id = self.db.execute(m.learning_material.insert().values(
                    template_id=template_id,
                    material_code=material_code, title="地道短语",
                    title_en="Idiomatic Phrases", summary="把高频短语放进画面、场景和自己的表达里。",
                    material_type="textbook", estimated_minutes=8, sort_order=10,
                    is_published=1, created_by=actor["id"],
                )).inserted_primary_key[0]
        material = self.db.execute(
            select(m.learning_material).where(m.learning_material.c.id == material_id)
        ).mappings().first()
        if not material:
            raise HTTPException(404, "Learning material not found.")
        if material.get("template_id"):
            template = self.db.execute(
                select(m.learning_template).where(
                    m.learning_template.c.id == material["template_id"]
                )
            ).mappings().first()
            if not template or (
                template["template_code"] != "put-aside"
                or template["template_version"] != 1
            ):
                raise HTTPException(
                    422,
                    "笔记转课件只能写入使用 Put aside 模板的教材。",
                )
        return material_id, material

    def _existing_lesson_for_entry(self, material_id, source_item, entry, lesson_code):
        direct = self.db.execute(
            select(m.learning_material_lesson.c.id).where(
                m.learning_material_lesson.c.material_id == material_id,
                m.learning_material_lesson.c.lesson_code == lesson_code,
            )
        ).scalar_one_or_none()
        if direct is not None:
            return direct
        if not entry["is_split"]:
            # One note can legitimately contain the same expression more than
            # once.  For a normal card, source linkage is the stable rebuild key.
            return self.db.execute(
                select(m.learning_material_lesson.c.id)
                .join(
                    m.courseware_block,
                    m.courseware_block.c.material_lesson_id == m.learning_material_lesson.c.id,
                )
                .join(
                    m.courseware_block_source,
                    m.courseware_block_source.c.courseware_block_id == m.courseware_block.c.id,
                )
                .where(
                    m.learning_material_lesson.c.material_id == material_id,
                    m.courseware_block_source.c.source_resource == "english_note_item",
                    m.courseware_block_source.c.source_reference_id == source_item["id"],
                )
                .order_by(m.learning_material_lesson.c.id)
            ).scalars().first()
        if entry["index"] != 0:
            return None
        # The first split card adopts the old combined lesson ID, so existing
        # learner links keep working when a previously generated note is fixed.
        old_phrase = self._card_phrase(source_item)
        old_slug = re.sub(r"[^a-z0-9]+", "-", old_phrase.lower()).strip("-") or "entry"
        legacy_codes = {
            f"phrase-{source_item['id']}-{old_slug}"[:120],
            f"phrase-{old_slug}"[:120],
        }
        return self.db.execute(
            select(m.learning_material_lesson.c.id).where(
                m.learning_material_lesson.c.material_id == material_id,
                m.learning_material_lesson.c.lesson_code.in_(legacy_codes),
            )
        ).scalars().first()

    def _save_generated_entry(self, material_id, source_item, entry, actor):
        phrase = entry["phrase"]
        preview = entry
        slug = re.sub(r"[^a-z0-9]+", "-", phrase.lower()).strip("-") or "entry"
        lesson_code = f"phrase-{source_item['id']}-{slug}"[:120]
        lesson_id = self._existing_lesson_for_entry(
            material_id, source_item, entry, lesson_code
        )
        if lesson_id is None:
            legacy_lesson_code = f"phrase-{slug}"[:120]
            lesson_id = self.db.execute(select(m.learning_material_lesson.c.id).where(
                m.learning_material_lesson.c.material_id == material_id,
                m.learning_material_lesson.c.lesson_code == legacy_lesson_code,
            )).scalar_one_or_none()
        rebuilt = lesson_id is not None
        lesson_title = phrase[:255].rstrip()
        lesson_values = {
            "title": lesson_title, "title_en": lesson_title,
            "summary": preview["blocks"][0]["payload"]["meaning"],
            "lesson_format": "courseware", "estimated_minutes": 8,
            "sort_order": source_item["item_order"] * 10 + entry["index"],
            "is_published": 1, "updated_by": actor["id"],
        }
        if lesson_id is None:
            lesson_id = self.db.execute(m.learning_material_lesson.insert().values(
                material_id=material_id, lesson_code=lesson_code,
                created_by=actor["id"], **lesson_values,
            )).inserted_primary_key[0]
        else:
            block_ids = select(m.courseware_block.c.id).where(
                m.courseware_block.c.material_lesson_id == lesson_id
            )
            self.db.execute(m.courseware_block_source.delete().where(
                m.courseware_block_source.c.courseware_block_id.in_(block_ids)
            ))
            self.db.execute(m.courseware_block.delete().where(
                m.courseware_block.c.material_lesson_id == lesson_id
            ))
            self.db.execute(m.learning_material_lesson.update().where(
                m.learning_material_lesson.c.id == lesson_id
            ).values(lesson_code=lesson_code, **lesson_values))
        source_fields = [
            (field, (source_item[field] or "").strip())
            for field in ("raw_text", "english_text", "chinese_text", "explanation", "examples")
            if (source_item[field] or "").strip()
        ]
        source_locator = entry["source_locator"]
        for block in preview["blocks"]:
            block_id = self.db.execute(m.courseware_block.insert().values(
                material_lesson_id=lesson_id, block_code=block["block_code"],
                block_type=block["block_type"], title=block["title"] or None,
                payload_json=json.dumps(block["payload"], ensure_ascii=False, separators=(",", ":")),
                sort_order=block["sort_order"], status="published", created_by=actor["id"],
            )).inserted_primary_key[0]
            self.db.execute(m.courseware_block_source.insert(), [
                {
                    "courseware_block_id": block_id,
                    "source_resource": "english_note_item",
                    "source_reference_id": source_item["id"],
                    "source_field": field,
                    "source_locator_json": json.dumps(
                        source_locator, ensure_ascii=False, separators=(",", ":")
                    ) if source_locator is not None else None,
                    "source_snapshot_text": snapshot,
                    "source_hash": hashlib.sha256(snapshot.encode("utf-8")).hexdigest(),
                    "sort_order": source_order,
                }
                for source_order, (field, snapshot) in enumerate(source_fields)
            ])
        return {"lesson_id": lesson_id, "phrase": phrase, "rebuilt": rebuilt}

    def _ensure_generated_course(self, material_id, material, topic_id, actor):
        course_material = m.learning_course_material
        mapped_course_ids = select(course_material.c.course_id).where(
            course_material.c.material_id == material_id
        )
        course = self.db.execute(
            select(m.learning_course.c.id)
            .where(
                or_(
                    m.learning_course.c.id.in_(mapped_course_ids),
                    m.learning_course.c.material_id == material_id,
                )
            )
            .order_by(m.learning_course.c.id)
        ).first()
        if course:
            course_id = course[0]
            self.db.execute(m.learning_course.update().where(m.learning_course.c.id == course_id).values(
                estimated_minutes=8, course_type="phrase", difficulty_code="elementary",
                is_published=1, updated_by=actor["id"],
            ))
        else:
            course_id = self.db.execute(m.learning_course.insert().values(
                material_id=material_id,
                course_code=f"{material['material_code']}-course"[:120],
                title=material["title"], title_en=material["title_en"] or "Idiomatic Phrases",
                summary="通过记忆画面、真实场景和开口练习掌握高频短语。",
                course_type="phrase", estimated_minutes=8, difficulty_code="elementary",
                sort_order=10, is_published=1, access_policy="free", created_by=actor["id"],
            )).inserted_primary_key[0]
        topic_course = m.learning_topic_course
        existing_topic_mapping = self.db.execute(
            select(topic_course.c.id).where(
                topic_course.c.topic_id == topic_id,
                topic_course.c.course_id == course_id,
            )
        ).first()
        if not existing_topic_mapping:
            next_sort_order = self.db.scalar(
                select(func.max(topic_course.c.sort_order)).where(
                    topic_course.c.topic_id == topic_id
                )
            ) or 0
            self.db.execute(topic_course.insert().values(
                topic_id=topic_id,
                course_id=course_id,
                sort_order=next_sort_order + 10,
                created_by=actor["id"],
                updated_by=actor["id"],
            ))
        existing_mapping = self.db.execute(
            select(course_material.c.id).where(
                course_material.c.course_id == course_id,
                course_material.c.material_id == material_id,
            )
        ).first()
        if not existing_mapping:
            self.db.execute(course_material.insert().values(
                course_id=course_id,
                material_id=material_id,
                sort_order=10,
                created_by=actor["id"],
                updated_by=actor["id"],
            ))
        return course_id

    def generate(self, item_id, topic_id, actor, material_id=None):
        source_item = self._item(item_id)
        previews = self._preview_entries(source_item)
        material_id, material = self._resolve_generation_material(topic_id, actor, material_id)
        lessons = [
            self._save_generated_entry(material_id, source_item, entry, actor)
            for entry in previews
        ]
        course_id = self._ensure_generated_course(material_id, material, topic_id, actor)
        self.db.commit()
        first = lessons[0]
        return {
            "material_id": material_id,
            "lesson_id": first["lesson_id"],
            "course_id": course_id,
            "rebuilt": first["rebuilt"],
            "split": len(lessons) > 1,
            "lessons": lessons,
        }
