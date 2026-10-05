"""Create the first published, metro-friendly Commute Micro English lesson.

Run with:
    PYTHONPATH=. .venv/bin/python scripts/create_commute_micro_english.py
"""

import json
import shutil
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models as m
from app import schemas as s
from app.core.config import Settings
from app.core.database import make_engine
from app.services.learning_catalog import LearningCatalogService


ACTOR = {"id": 1}
TOPIC_CODE = "commute-micro-english"
MATERIAL_CODE = "commute-micro-english-stop-1"
COURSE_CODE = "commute-micro-english-stop-1"
LESSON_CODE = "commute-quick-replies-01"
ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATION_SOURCE = ROOT / "assets" / "illustrations" / "commute" / "quick-replies.svg"
ILLUSTRATION_PATH = "commute-covers/quick-replies.svg"
MAX_ILLUSTRATION_BYTES = 100 * 1024


def row_id(db, table, column, code):
    row = db.execute(select(table.c.id).where(column == code)).first()
    return row[0] if row else None


def install_illustration(settings):
    """Copy the tracked source image to the locally served static directory."""
    target = settings.static_dir / ILLUSTRATION_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ILLUSTRATION_SOURCE, target)
    if target.stat().st_size >= MAX_ILLUSTRATION_BYTES:
        raise ValueError("Commute lesson illustration must remain smaller than 100KB.")
    return f"/static/{ILLUSTRATION_PATH}"


def item(code, order, payload, title=""):
    return {
        "item_code": code,
        "item_order": order,
        "title": title,
        "payload": payload,
    }


def section(code, title, title_en, order, items):
    return {
        "section_code": code,
        "title": title,
        "title_en": title_en,
        "sort_order": order,
        "items": items,
    }


def lesson_sections():
    return [
        section(
            "core_vocabulary",
            "核心短语",
            "Core Phrases",
            10,
            [
                item(
                    "sounds-good",
                    1,
                    {
                        "term": "sounds good",
                        "meaning": "听起来不错；好啊。",
                        "explanation": "A natural way to say that you agree with a plan or suggestion.",
                        "pronunciation": "/saʊndz ɡʊd/",
                        "examples": [
                            {
                                "english": "Can we meet outside the station at six? — Sounds good.",
                                "chinese": "我们六点在车站外见面，可以吗？——好啊。",
                            }
                        ],
                    },
                    "sounds good",
                ),
                item(
                    "give-me-a-second",
                    2,
                    {
                        "term": "give me a second",
                        "meaning": "等我一下。",
                        "explanation": "A polite way to ask for a short moment while you do something.",
                        "pronunciation": "/ɡɪv mi ə ˈsekənd/",
                        "examples": [
                            {
                                "english": "Give me a second. I’m opening the message now.",
                                "chinese": "等我一下，我正在打开消息。",
                            }
                        ],
                    },
                    "give me a second",
                ),
                item(
                    "im-on-my-way",
                    3,
                    {
                        "term": "I’m on my way",
                        "meaning": "我在路上。",
                        "explanation": "A way to say that you have started travelling to the place.",
                        "pronunciation": "/aɪm ɒn maɪ weɪ/",
                        "examples": [
                            {
                                "english": "I’m on my way. The train is one stop away.",
                                "chinese": "我在路上，地铁还有一站就到了。",
                            }
                        ],
                    },
                    "I’m on my way",
                ),
                item(
                    "pick-it-up-later",
                    4,
                    {
                        "term": "pick it up later",
                        "meaning": "晚点再继续做。",
                        "explanation": "To stop doing something now and continue it at another time.",
                        "pronunciation": "/pɪk ɪt ʌp ˈleɪtə(r)/",
                        "examples": [
                            {
                                "english": "Let’s pick it up later when the signal is better.",
                                "chinese": "等信号好一点，我们晚点再继续。",
                            }
                        ],
                    },
                    "pick it up later",
                ),
            ],
        ),
        section(
            "situational_dialogues",
            "情景对话",
            "Situational Dialogues",
            20,
            [
                item(
                    "meet-at-the-station",
                    1,
                    {
                        "scene": "下班后约在车站见面",
                        "turns": [
                            {
                                "speaker": "Mia",
                                "english": "Can we meet outside Central Station at six?",
                                "chinese": "我们六点在中央车站外见面，可以吗？",
                            },
                            {
                                "speaker": "Leo",
                                "english": "Sounds good. I’ll come straight from work.",
                                "chinese": "好啊。我下班后直接过去。",
                            },
                        ],
                    },
                    "约在车站见面",
                ),
                item(
                    "find-the-address",
                    2,
                    {
                        "scene": "在车厢里找地址",
                        "turns": [
                            {
                                "speaker": "Mia",
                                "english": "Could you send the café address again?",
                                "chinese": "你能再发一次咖啡馆地址吗？",
                            },
                            {
                                "speaker": "Leo",
                                "english": "Give me a second. I’m opening the message.",
                                "chinese": "等我一下，我正在打开消息。",
                            },
                        ],
                    },
                    "在车厢里找地址",
                ),
                item(
                    "one-stop-away",
                    3,
                    {
                        "scene": "告诉同事快到了",
                        "turns": [
                            {
                                "speaker": "Mia",
                                "english": "Are you close to the office?",
                                "chinese": "你快到办公室了吗？",
                            },
                            {
                                "speaker": "Leo",
                                "english": "I’m on my way. I’ll get off at the next stop.",
                                "chinese": "我在路上，下一站下车。",
                            },
                        ],
                    },
                    "告诉同事快到了",
                ),
                item(
                    "weak-signal",
                    4,
                    {
                        "scene": "信号不稳时暂停阅读",
                        "turns": [
                            {
                                "speaker": "Mia",
                                "english": "Do you want to finish the article now?",
                                "chinese": "你想现在把文章看完吗？",
                            },
                            {
                                "speaker": "Leo",
                                "english": "Let’s pick it up later. The signal is weak.",
                                "chinese": "我们晚点再继续吧，信号不太好。",
                            },
                        ],
                    },
                    "信号不稳时暂停阅读",
                ),
                item(
                    "calendar-change",
                    5,
                    {
                        "scene": "临时调整日程",
                        "turns": [
                            {
                                "speaker": "Mia",
                                "english": "The client moved the call to four thirty.",
                                "chinese": "客户把电话改到四点半了。",
                            },
                            {
                                "speaker": "Leo",
                                "english": "Sounds good. Give me a second and I’ll update my calendar.",
                                "chinese": "好啊。等我一下，我更新一下日历。",
                            },
                        ],
                    },
                    "临时调整日程",
                ),
                item(
                    "tunnel-message",
                    6,
                    {
                        "scene": "地铁进隧道前回复",
                        "turns": [
                            {
                                "speaker": "Mia",
                                "english": "Can you check the document on the train?",
                                "chinese": "你能在地铁上看看那份文件吗？",
                            },
                            {
                                "speaker": "Leo",
                                "english": "I can read it now, but I’ll pick it up later if the signal drops.",
                                "chinese": "我现在能看，不过要是信号断了，我晚点再继续。",
                            },
                        ],
                    },
                    "地铁进隧道前回复",
                ),
            ],
        ),
        section(
            "key_sentence_patterns",
            "核心句型",
            "Key Sentence Patterns",
            30,
            [
                item(
                    "agree-and-act",
                    1,
                    {
                        "pattern": "Sounds good. I’ll + verb …",
                        "meaning": "同意后，补一句你接下来会做什么。",
                        "explanation": "Use it to agree and make your next action clear.",
                        "examples": [
                            {
                                "english": "Sounds good. I’ll bring the notes.",
                                "chinese": "好啊。我会把笔记带上。",
                            }
                        ],
                    },
                    "同意并说明下一步",
                ),
                item(
                    "ask-for-a-moment",
                    2,
                    {
                        "pattern": "Give me a second. I’m + verb-ing …",
                        "meaning": "请对方稍等，并说明你正在做什么。",
                        "explanation": "This makes a short wait sound polite and specific.",
                        "examples": [
                            {
                                "english": "Give me a second. I’m checking the platform number.",
                                "chinese": "等我一下，我在看站台号。",
                            }
                        ],
                    },
                    "请稍等并说明原因",
                ),
                item(
                    "arrival-update",
                    3,
                    {
                        "pattern": "I’m on my way. I’ll + verb when …",
                        "meaning": "说明你已经出发，并给出下一步时间点。",
                        "explanation": "Use it when someone needs a quick arrival update.",
                        "examples": [
                            {
                                "english": "I’m on my way. I’ll call when I get off the train.",
                                "chinese": "我在路上，下地铁后给你打电话。",
                            }
                        ],
                    },
                    "报备行程",
                ),
                item(
                    "pause-and-return",
                    4,
                    {
                        "pattern": "Let’s pick it up later.",
                        "meaning": "现在先暂停，约好以后继续。",
                        "explanation": "Use it to pause a task without abandoning it.",
                        "examples": [
                            {
                                "english": "Let’s pick it up later after dinner.",
                                "chinese": "晚饭后我们再继续吧。",
                            }
                        ],
                    },
                    "暂停后再继续",
                ),
            ],
        ),
        section(
            "speaking_practice",
            "开口接话",
            "Quick Reply Practice",
            40,
            [
                item(
                    "meet-at-six",
                    1,
                    {
                        "question": "Choose the reply that fits the situation.",
                        "question_zh": "同事问：六点在地铁站口见，可以吗？你已经同意。选出最自然的回应。",
                        "sentence": "Your colleague suggests meeting at six. ______ — I’ll be there.",
                        "answer": "Sounds good",
                        "choices": [
                            "Sounds good",
                            "Give me a second",
                            "Pick it up later",
                        ],
                        "explanation": "Use this short reply when you agree with a suggestion.",
                        "turns": [
                            {
                                "speaker": "Colleague",
                                "english": "Can we meet at the station at six?",
                                "chinese": "我们六点在车站见，可以吗？",
                            },
                            {
                                "speaker": "You",
                                "english": "Sounds good. I’ll be there.",
                                "chinese": "好啊。我会到。",
                            },
                        ],
                    },
                    "约见面的快速回应",
                ),
                item(
                    "arrival-voice-reply",
                    2,
                    {
                        "instruction": "看完提示后，用 I’m on my way 说出完整回应。",
                        "question": "Your friend asks whether you have left home.",
                        "question_zh": "朋友问你出门了吗。你已经坐上地铁，再补一句你会在下车后联系对方。",
                        "guidance": "Say: I’m on my way. I’ll text you when I get off.",
                        "turns": [
                            {
                                "speaker": "Friend",
                                "english": "Have you left home yet?",
                                "chinese": "你出门了吗？",
                            },
                            {
                                "speaker": "You",
                                "english": "I’m on my way. I’ll text you when I get off.",
                                "chinese": "我在路上，下车后给你发消息。",
                            },
                        ],
                    },
                    "报备已经出发",
                ),
            ],
        ),
        section(
            "mini_exercises",
            "开口讨论",
            "Speak It Out",
            50,
            [
                item(
                    "signal-drops",
                    1,
                    {
                        "question": "Your train is entering a tunnel and the signal may disappear. Tell your teammate that you will continue reviewing the file later.",
                        "question_zh": "地铁要进隧道，信号可能会断。告诉同事你会晚点继续看文件。",
                        "guidance": "Start with: Let’s pick it up later …",
                        "sample_answer": "Let’s pick it up later. I’ll review the file when I have a better signal.",
                    },
                    "隧道里暂停工作",
                ),
                item(
                    "find-the-platform",
                    2,
                    {
                        "question": "A friend asks for the platform number while you are looking at the station board. Ask for a brief moment and say what you are doing.",
                        "question_zh": "朋友问你站台号，你正在看站牌。请对方稍等，并说明你在做什么。",
                        "guidance": "Start with: Give me a second …",
                        "sample_answer": "Give me a second. I’m checking the platform number now.",
                    },
                    "查看站台号",
                ),
            ],
        ),
        section(
            "useful_tips",
            "通勤提示",
            "Commuting Tips",
            60,
            [
                item(
                    "short-first",
                    1,
                    {
                        "title": "先说短句，再补信息",
                        "summary": "地铁上回复消息时，先用 Sounds good 或 I’m on my way 完成核心回应；需要时再补一句时间或动作。",
                        "explanation": "A short first sentence still works when the train is noisy or the signal is weak.",
                    },
                    "先完成核心回应",
                ),
                item(
                    "silent-rehearsal",
                    2,
                    {
                        "title": "可以默读，不必出声",
                        "summary": "先在心里读一遍，等到出站或方便说话时，再把一句完整回应说出来。",
                        "explanation": "Silent rehearsal keeps the lesson useful even in a crowded carriage.",
                    },
                    "拥挤车厢也能练",
                ),
            ],
        ),
        section(
            "extended_reading",
            "延伸阅读",
            "Extended Reading",
            70,
            [
                item(
                    "train-message",
                    1,
                    {
                        "text": "On a crowded train, Leo gets a message: “Can we meet at six?” He replies, “Sounds good. I’m on my way after I get off.”",
                        "chinese": "拥挤的地铁上，Leo 收到消息：“我们六点见，可以吗？”他回复：“好啊。我下地铁后就过去。”",
                        "explanation": "Two short phrases give both agreement and an arrival update.",
                    },
                    "车厢里的简短回复",
                ),
                item(
                    "pause-with-a-plan",
                    2,
                    {
                        "text": "Mia loses her signal in a tunnel. She says, “Give me a second. If it drops again, let’s pick it up later.”",
                        "chinese": "Mia 在隧道里信号变弱。她说：“等我一下。如果又断了，我们晚点再继续。”",
                        "explanation": "The reply explains the delay and keeps the task moving forward.",
                    },
                    "信号不好时的安排",
                ),
            ],
        ),
    ]


def main():
    settings = Settings()
    illustration_url = install_illustration(settings)
    engine = make_engine(settings.database_url)
    with Session(engine) as db:
        catalog = LearningCatalogService(db)

        template_id = row_id(
            db, m.learning_template, m.learning_template.c.template_code, "commute"
        )
        template = catalog.save_template(
            s.LearningTemplateInput(
                template_code="commute",
                template_version=1,
                name="通勤微课",
                description="为地铁和短时通勤设计的分步听读与情境接话学习页。",
                content_kind="structured",
                supported_clients=["web", "mini"],
                config={"recommended_minutes": 3, "interaction": "swipe-cards"},
                status="active",
                sort_order=35,
            ),
            ACTOR,
            template_id,
        )

        topic_id = row_id(db, m.learning_topic, m.learning_topic.c.topic_code, TOPIC_CODE)
        topic = catalog.save_topic(
            s.LearningTopicInput(
                module_id=2,
                topic_code=TOPIC_CODE,
                title="地铁通勤英语",
                title_en="Commute Micro English",
                description="每节约 3 分钟，在地铁上用单手完成听读、记忆和一句开口回应。",
                sort_order=50,
                is_published=1,
            ),
            ACTOR,
            topic_id,
        )

        material_id = row_id(
            db, m.learning_material, m.learning_material.c.material_code, MATERIAL_CODE
        )
        material_payload = s.LearningMaterialInput(
            template_id=template["id"],
            material_code=MATERIAL_CODE,
            title="第一站 · 3 分钟自然接话",
            title_en="Stop 1 · Quick Replies",
            summary="在地铁上学会同意、请稍等、报备在路上和约好晚点继续。",
            material_type="commute",
            publisher="Happy English",
            version_name="通勤微课 v1",
            cover_url=illustration_url,
            difficulty_code="a1-a2",
            estimated_minutes=3,
            sort_order=10,
            is_published=1,
        )
        if material_id is None:
            material = catalog.save_material(material_payload, ACTOR)
        else:
            material = catalog.get_admin_material(material_id)

        lesson_id = db.execute(
            select(m.learning_material_lesson.c.id).where(
                m.learning_material_lesson.c.material_id == material["id"],
                m.learning_material_lesson.c.lesson_code == LESSON_CODE,
            )
        ).scalar_one_or_none()
        lesson = catalog.save_material_lesson(
            material["id"],
            s.LearningMaterialLessonInput(
                lesson_code=LESSON_CODE,
                title="地铁上也能学 · 3 分钟自然接话",
                title_en="Three-Minute Natural Replies",
                summary="用四个短语，自然地同意、请人稍等、说明自己在路上，并约好晚点继续。",
                illustration_url=illustration_url,
                lesson_format="structured",
                estimated_minutes=3,
                sort_order=10,
                sections=lesson_sections(),
            ),
            ACTOR,
            lesson_id,
        )
        catalog.lesson_content.publish(lesson["id"], ACTOR)
        if material_id is not None:
            material = catalog.save_material(material_payload, ACTOR, material_id)

        course_id = row_id(db, m.learning_course, m.learning_course.c.course_code, COURSE_CODE)
        course = catalog.save_course(
            s.LearningCourseInput(
                topic_id=topic["id"],
                material_ids=[material["id"]],
                course_code=COURSE_CODE,
                title="地铁通勤英语 · 第一站",
                title_en="Commute Micro English · Stop 1",
                summary="一节 3 分钟的短卡片课，适合拥挤、嘈杂和随时会被打断的通勤路上。",
                course_type="commute",
                cover_url=illustration_url,
                estimated_minutes=3,
                difficulty_code="a1-a2",
                sort_order=10,
                is_published=1,
                access_policy="free",
            ),
            ACTOR,
            course_id,
        )

        print(
            json.dumps(
                {
                    "template_id": template["id"],
                    "topic_id": topic["id"],
                    "material_id": material["id"],
                    "lesson_id": lesson["id"],
                    "illustration_url": illustration_url,
                    "illustration_bytes": (settings.static_dir / ILLUSTRATION_PATH).stat().st_size,
                    "course_id": course["id"],
                    "course_path": f"/courses/{course['id']}",
                },
                ensure_ascii=False,
            )
        )


if __name__ == "__main__":
    main()
