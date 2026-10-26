#!/usr/bin/env python3
"""Publish the non-Word-List parts of Wordly Wise 3000 Book 2, Lesson 1.

The existing Book 2 importer owns the fifteen Word List lessons.  This
companion script deliberately owns only the additional Lesson 1 courseware,
so rerunning either importer cannot remove the other lesson shape.

Run locally or on the application server with:

    PYTHONPATH=. .venv/bin/python scripts/seed_wordly_wise_2_lesson1_courseware.py
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from sqlalchemy import delete, func, select, update
from sqlalchemy.engine import Connection, Engine

from app import models as m
from app.core.config import Settings
from app.core.database import make_engine


MATERIAL_CODE = "wordlywise-3000-book-2"
COURSE_CODE = "wordly-wise-2-preview"
LESSON_CODE = "wordly-wise-2-practice-lesson-01"

SOURCE_DOCUMENT = "Wordly Wise 3000 Book 2"
SOURCE_LESSON = 1
SOURCE_PDF_PAGES = (10, 11, 12, 13, 14, 15, 16, 17)
SOURCE_BOOK_PAGES = (4, 5, 6, 7, 8, 9, 10, 11)


@dataclass(frozen=True)
class CoursewareBlock:
    block_code: str
    block_type: str
    title: str
    payload: dict
    sort_order: int


def source(page: int, section: str) -> dict:
    """Keep page-level provenance alongside every independently editable block."""

    return {
        "document": SOURCE_DOCUMENT,
        "source_lesson": SOURCE_LESSON,
        "pdf_page": page,
        "book_page": page - 6,
        "section": section,
    }


def choice(identifier: str, text: str) -> dict:
    return {"id": identifier, "text": text}


BLOCKS: tuple[CoursewareBlock, ...] = (
    CoursewareBlock(
        block_code="wordly-wise-hero",
        block_type="hero",
        title="Lesson 1 · 阅读与练习",
        sort_order=10,
        payload={
            "family": "wordly_wise",
            "eyebrow": "WORDLY WISE 3000 · BOOK 2 · LESSON 1",
            "phrase": "Bailey Finds a New Home",
            "meaning": "阅读、理解与应用",
            "memory": "先在练习里用词，再在 Bailey 的故事里读懂词。",
            "key_sentence": {
                "english": "Bailey finds a new home at Sugar Wood Farm.",
                "chinese": "Bailey 在 Sugar Wood Farm 找到了一个新家。",
            },
            "sections": [
                "词义辨析",
                "关联归类",
                "语义应用",
                "课文阅读",
                "阅读理解",
                "词汇拓展",
                "复习",
            ],
            "source": source(13, "Lesson 1 courseware overview"),
        },
    ),
    CoursewareBlock(
        block_code="wordly-wise-meanings",
        block_type="wordly_wise_meaning_match",
        title="1A · Words and Their Meanings",
        sort_order=20,
        payload={
            "family": "wordly_wise",
            "intro": "看释义或单词，选出意思相同的一项。",
            "items": [
                {
                    "number": 1,
                    "prompt": "to move up and down",
                    "choices": [
                        choice("a", "claw"),
                        choice("b", "shelter"),
                        choice("c", "flap"),
                        choice("d", "groom"),
                    ],
                    "answer": "c",
                    "explanation": "flap 作动词时表示“上下拍动”。",
                },
                {
                    "number": 2,
                    "prompt": "to use with others",
                    "choices": [
                        choice("a", "groom"),
                        choice("b", "claw"),
                        choice("c", "shelter"),
                        choice("d", "share"),
                    ],
                    "answer": "d",
                    "explanation": "share 表示“与他人一起使用或享受”。",
                },
                {
                    "number": 3,
                    "prompt": "the word name for 0",
                    "choices": [
                        choice("a", "couple"),
                        choice("b", "zero"),
                        choice("c", "yard"),
                        choice("d", "calf"),
                    ],
                    "answer": "b",
                    "explanation": "zero 是数字 0 的英文名称。",
                },
                {
                    "number": 4,
                    "prompt": "the land around a building",
                    "choices": [
                        choice("a", "yard"),
                        choice("b", "groom"),
                        choice("c", "claw"),
                        choice("d", "cushion"),
                    ],
                    "answer": "a",
                    "explanation": "yard 指建筑物周围的院子或空地。",
                },
                {
                    "number": 5,
                    "prompt": "something that protects",
                    "choices": [
                        choice("a", "calf"),
                        choice("b", "shelter"),
                        choice("c", "zero"),
                        choice("d", "couple"),
                    ],
                    "answer": "b",
                    "explanation": "shelter 是能提供遮蔽或保护的地方、物体。",
                },
                {
                    "number": 6,
                    "prompt": "claw",
                    "choices": [
                        choice("a", "a person who takes care of horses"),
                        choice("b", "the curved nail of a bird"),
                        choice("c", "a length of three feet"),
                        choice("d", "the curved horn of a cow"),
                    ],
                    "answer": "b",
                    "explanation": "claw 是鸟或动物脚趾上的弯曲利爪。",
                },
                {
                    "number": 7,
                    "prompt": "calf",
                    "choices": [
                        choice("a", "a baby sheep"),
                        choice("b", "the arm between the hand and the elbow"),
                        choice("c", "a baby horse"),
                        choice("d", "the back of the leg between the knee and the ankle"),
                    ],
                    "answer": "d",
                    "explanation": "calf 可指小腿肚；本题考查这个意思。",
                },
                {
                    "number": 8,
                    "prompt": "couple",
                    "choices": [
                        choice("a", "a large number of things"),
                        choice("b", "a man getting married"),
                        choice("c", "two things of the same kind"),
                        choice("d", "a woman getting married"),
                    ],
                    "answer": "c",
                    "explanation": "a couple of 表示“一对、两个同类的东西”。",
                },
                {
                    "number": 9,
                    "prompt": "groom",
                    "choices": [
                        choice("a", "to make clean and neat"),
                        choice("b", "to use with others"),
                        choice("c", "to move up and down"),
                        choice("d", "to swing from side to side"),
                    ],
                    "answer": "a",
                    "explanation": "groom 作动词表示“梳理、清洁并整理”。",
                },
                {
                    "number": 10,
                    "prompt": "cushion",
                    "choices": [
                        choice("a", "food for horses"),
                        choice("b", "a pad with a soft filling"),
                        choice("c", "a feeling of happiness"),
                        choice("d", "a young cow"),
                    ],
                    "answer": "b",
                    "explanation": "cushion 是里面有柔软填充物的垫子或靠垫。",
                },
            ],
            "source": source(10, "1A Words and Their Meanings"),
        },
    ),
    CoursewareBlock(
        block_code="wordly-wise-connections",
        block_type="wordly_wise_connections",
        title="1B · Seeing Connections",
        sort_order=30,
        payload={
            "family": "wordly_wise",
            "intro": "每组中有三个词存在关联，找出不属于这一组的词。",
            "items": [
                {
                    "number": 1,
                    "words": ["stool", "wall", "chair", "cushion"],
                    "answer": "wall",
                    "reason": "stool、chair 和 cushion 都与坐有关；wall 是墙。",
                },
                {
                    "number": 2,
                    "words": ["seven", "two", "too", "zero"],
                    "answer": "too",
                    "reason": "seven、two、zero 都是数字名称；too 不是数字。",
                },
                {
                    "number": 3,
                    "words": ["pony", "calf", "elbow", "knee"],
                    "answer": "pony",
                    "reason": "calf、elbow、knee 都是身体部位；pony 是小马。",
                },
                {
                    "number": 4,
                    "words": ["bride", "groom", "apple", "ring"],
                    "answer": "apple",
                    "reason": "bride、groom、ring 都与婚礼有关；apple 是苹果。",
                },
                {
                    "number": 5,
                    "words": ["pair", "two", "couple", "crowd"],
                    "answer": "crowd",
                    "reason": "pair、two、couple 都表示两个；crowd 表示一群人。",
                },
            ],
            "source": source(11, "1B Seeing Connections"),
        },
    ),
    CoursewareBlock(
        block_code="wordly-wise-application",
        block_type="wordly_wise_application",
        title="1C · Applying Meanings",
        sort_order=40,
        payload={
            "family": "wordly_wise",
            "intro": "把单词放进真实场景里，选出最合适的答案。",
            "items": [
                {
                    "number": 1,
                    "prompt": "Which of the following is equal to a yard?",
                    "target_word": "yard",
                    "choices": [
                        choice("a", "twelve inches"),
                        choice("b", "a couple"),
                        choice("c", "three feet"),
                        choice("d", "zero"),
                    ],
                    "answer": "c",
                    "explanation": "一 yard 等于 three feet。",
                },
                {
                    "number": 2,
                    "prompt": "Which of the following could provide shelter?",
                    "target_word": "shelter",
                    "choices": [
                        choice("a", "a calf"),
                        choice("b", "a cushion"),
                        choice("c", "a claw"),
                        choice("d", "a cave"),
                    ],
                    "answer": "d",
                    "explanation": "a cave 可以提供遮蔽和保护。",
                },
                {
                    "number": 3,
                    "prompt": "Which of the following has claws?",
                    "target_word": "claws",
                    "choices": [
                        choice("a", "a groom"),
                        choice("b", "a crab"),
                        choice("c", "a calf"),
                        choice("d", "a shark"),
                    ],
                    "answer": "b",
                    "explanation": "crab 的钳子也称 claws。",
                },
                {
                    "number": 4,
                    "prompt": "Which of the following might have a flap?",
                    "target_word": "flap",
                    "choices": [
                        choice("a", "a tent"),
                        choice("b", "a couple"),
                        choice("c", "a bird"),
                        choice("d", "a swing"),
                    ],
                    "answer": "a",
                    "explanation": "帐篷入口常有可以掀开的 flap。",
                },
                {
                    "number": 5,
                    "prompt": "Which of the following cannot be shared?",
                    "target_word": "shared",
                    "choices": [
                        choice("a", "money"),
                        choice("b", "shelter"),
                        choice("c", "toys"),
                        choice("d", "zero"),
                    ],
                    "answer": "d",
                    "explanation": "zero 代表没有东西，不能分享。",
                },
            ],
            "source": source(12, "1C Applying Meanings"),
        },
    ),
    CoursewareBlock(
        block_code="wordly-wise-reading",
        block_type="wordly_wise_reading",
        title="1D · Vocabulary in Context",
        sort_order=50,
        payload={
            "family": "wordly_wise",
            "title": "Bailey Finds a New Home",
            "intro": "听读故事，在语境中找到本课单词。",
            "target_words": [
                "couple",
                "calf",
                "share",
                "zero",
                "shelter",
                "yard",
                "cushion",
                "flap",
                "groom",
                "claws",
            ],
            "paragraphs": [
                {
                    "number": 1,
                    "english": "Sandra Adams and Ken Hodkinson live at Sugar Wood Farm in New Hampshire. They have a cat named Bailey. He did not always live with them. If Bailey could talk, he might tell you how he came to live with Sandra and Ken. Let's imagine he can.",
                    "chinese": "Sandra Adams 和 Ken Hodkinson 住在新罕布什尔州的 Sugar Wood Farm。他们养了一只名叫 Bailey 的猫。Bailey 并不是一直和他们住在一起。如果 Bailey 会说话，他或许会告诉你自己怎样来到 Sandra 和 Ken 家。让我们想象他真的会说话。",
                    "focus_words": [],
                },
                {
                    "number": 2,
                    "english": "At first, Ken and Sandra didn't want me. Many times I waited outside their door for them to return home. I knew I had only a couple of seconds to make my move. So I would rub against Sandra's calf, purring loudly and looking up at her face. But Ken always said, \"Don't let him in. Don't let him in.\" And they shut the door in my face.",
                    "chinese": "一开始，Ken 和 Sandra 并不想要我。很多次，我在门外等他们回家。我知道自己只有几秒钟来行动，所以我会蹭 Sandra 的小腿肚，响亮地呼噜着，抬头望着她的脸。但 Ken 总是说：“别让他进来，别让他进来。”于是他们当着我的面关上了门。",
                    "focus_words": ["couple", "calf"],
                },
                {
                    "number": 3,
                    "english": "It's true that I already had a home. But I had to share it with two other cats who liked to bully me. That was no fun. I wanted something better. Sugar Wood Farm was just around the corner, and I checked it out carefully. I counted the cats that lived there. The number I came up with was zero. As we cats say, \"Purr-fect!\"",
                    "chinese": "确实，我原来已经有个家。但我得和两只喜欢欺负我的猫共用它，这一点也不好玩。我想要更好的生活。Sugar Wood Farm 就在附近，我仔细考察了那里，还数了数住在那里的猫。结果是零只。正如我们猫会说的：“呼噜——完美！”",
                    "focus_words": ["share", "zero"],
                },
                {
                    "number": 4,
                    "english": "Weeks went by, and it was the same every time. I hung around the door for hours, and Ken and Sandra always closed it in my face. But I never gave up. Then, one dark and stormy night, my chance came. I was waiting for them to come home, as usual, when it started to rain. Now, cats know enough to get out of the rain. I could have taken shelter in their woodshed. But I wanted to be right there on the doorstep when they came home.",
                    "chinese": "几个星期过去了，每次都是一样。我在门边徘徊好几个小时，Ken 和 Sandra 总是当着我的面关门。但我从不放弃。后来一个黑暗而暴风雨交加的夜晚，我的机会来了。像往常一样，我在等他们回家时开始下雨。猫当然知道要避雨；我本可以去他们的木棚躲雨，但我想在他们回家时正好待在门口。",
                    "focus_words": ["shelter"],
                },
                {
                    "number": 5,
                    "english": "Before long, the rain turned to snow. This was even better. I was sure that no one would turn a cat away on such a night. I heard their car pull into the yard. Then I watched them hurry toward the house. As soon as they saw me, I started to meow like a little lost kitten.",
                    "chinese": "不久，雨变成了雪，这就更好了。我确信在这样的夜晚，没有人会赶走一只猫。我听见他们的车开进院子，看着他们匆匆走向房子。他们一看见我，我就像一只迷路的小猫那样开始喵喵叫。",
                    "focus_words": ["yard"],
                },
                {
                    "number": 6,
                    "english": "In no time, I was inside the house. Sandra dried me with a warm, fluffy towel. Ken kept saying, \"Don't feed him. Don't feed him.\" But I wasn't looking for food just then. I was looking for a new home. At last, I thought I had found it. I was right. Before long, they were feeding me. Sandra talked to my old owners about me. They missed me, but they had two other cats. I didn't feel bad.",
                    "chinese": "很快，我就进了屋。Sandra 用温暖、蓬松的毛巾把我擦干。Ken 一直说：“别喂他，别喂他。”但那时我不是在找食物，我在找一个新家。终于，我觉得自己找到了；我猜对了。不久，他们开始喂我。Sandra 和我的旧主人谈了谈，他们想念我，但他们还有另外两只猫，所以我并不觉得难过。",
                    "focus_words": [],
                },
                {
                    "number": 7,
                    "english": "Cats spend a lot of time sleeping, so Sandra made a soft cushion for me to use. To be honest, I prefer their bed. They also made a cat door for me with a little flap. I just push it open with my nose, and it closes behind me. Sandra likes to groom me. I think I do it better myself, but it gives her a lot of pleasure. I try not to sharpen my claws on their furniture. I think they are happy to have me around.",
                    "chinese": "猫花很多时间睡觉，所以 Sandra 给我做了一个柔软的靠垫。老实说，我更喜欢他们的床。他们还给我做了一扇带小门帘的猫门。我只要用鼻子把它推开，它就会在我身后关上。Sandra 喜欢给我梳理毛发。我觉得自己做得更好，不过这让她很开心。我尽量不在他们的家具上磨爪子。我想他们很高兴有我在身边。",
                    "focus_words": ["cushion", "flap", "groom", "claws"],
                },
            ],
            "source": {
                "document": SOURCE_DOCUMENT,
                "source_lesson": SOURCE_LESSON,
                "pdf_pages": [13, 14],
                "book_pages": [7, 8],
                "section": "1D Vocabulary in Context",
            },
        },
    ),
    CoursewareBlock(
        block_code="wordly-wise-comprehension",
        block_type="wordly_wise_comprehension",
        title="阅读理解 · 用一句完整的话回答",
        sort_order=60,
        payload={
            "family": "wordly_wise",
            "intro": "先自己说一说，再查看答题线索和参考答案。",
            "items": [
                {
                    "number": 1,
                    "question": "How did Bailey know there were zero cats at Sugar Wood Farm?",
                    "cue": "Look at what Bailey did after he checked out the farm.",
                    "sample_answer": "He checked the farm carefully and counted the cats that lived there.",
                },
                {
                    "number": 2,
                    "question": "How do you know that Ken didn't want to share his home with Bailey?",
                    "cue": "Recall what Ken said at the door and inside the house.",
                    "sample_answer": "Ken kept saying, \"Don't let him in,\" and later, \"Don't feed him.\"",
                },
                {
                    "number": 3,
                    "question": "Why do you think Bailey rubbed against Sandra's calf and not Ken's?",
                    "cue": "Think about which person seemed more likely to let Bailey in.",
                    "sample_answer": "Sandra seemed more likely to welcome Bailey, while Ken did not want him inside.",
                },
                {
                    "number": 4,
                    "question": "Why didn't Bailey look for shelter when it started to rain and then snow?",
                    "cue": "What did Bailey want most that night?",
                    "sample_answer": "He wanted to stay on the doorstep so Sandra and Ken would see him and let him in.",
                },
                {
                    "number": 5,
                    "question": "What happened to Bailey a couple of days after he was let into the house?",
                    "cue": "Read the paragraph after Sandra dried Bailey.",
                    "sample_answer": "Sandra talked to Bailey's old owners, and Bailey began living with Sandra and Ken.",
                },
                {
                    "number": 6,
                    "question": "How do you know that Bailey can come in and go out to the yard easily?",
                    "cue": "Find the detail about the cat door.",
                    "sample_answer": "He has a cat door with a flap that he can push open with his nose.",
                },
                {
                    "number": 7,
                    "question": "Why didn't Bailey need to have Sandra groom him?",
                    "cue": "What does Bailey say about grooming himself?",
                    "sample_answer": "He thought he could groom himself better.",
                },
                {
                    "number": 8,
                    "question": "How often do you think Bailey sleeps on the cushion Sandra made for him? Explain your answer.",
                    "cue": "This is an inference question. Compare the cushion with Bailey's preferred place.",
                    "sample_answer": "Probably not often, because Bailey says he prefers their bed.",
                },
                {
                    "number": 9,
                    "question": "Do you think Bailey likes having the cat door with the flap? Explain your answer.",
                    "cue": "Think about how easily Bailey uses it.",
                    "sample_answer": "Yes. He can push the flap open with his nose and move in and out easily.",
                },
                {
                    "number": 10,
                    "question": "What are some ways Bailey might use his claws?",
                    "cue": "Use the passage and what you know about cats.",
                    "sample_answer": "He might scratch, climb, catch things, or sharpen his claws.",
                },
            ],
            "fun_fact": {
                "english": "The plural of calf is calves, not calfs.",
                "chinese": "calf 的复数是不规则形式 calves，不是 calfs。",
            },
            "source": {
                "document": SOURCE_DOCUMENT,
                "source_lesson": SOURCE_LESSON,
                "pdf_pages": [14, 15],
                "book_pages": [8, 9],
                "section": "1D Reading Questions and Fun Fact",
            },
        },
    ),
    CoursewareBlock(
        block_code="wordly-wise-extension",
        block_type="wordly_wise_extension",
        title="Vocabulary Extension · share",
        sort_order=70,
        payload={
            "family": "wordly_wise",
            "word": "share",
            "forms": [
                {
                    "part_of_speech": "verb",
                    "definition": "To use or enjoy with others.",
                    "chinese": "与他人一起使用或享受。",
                },
                {
                    "part_of_speech": "noun",
                    "definition": "A part that each person gets of a whole.",
                    "chinese": "整体中每个人得到的一份。",
                },
            ],
            "academic_context": {
                "english": "In school, sharing is telling others something. You can share stories or ideas or read something aloud that you wrote.",
                "chinese": "在学校里，sharing 指把某件事告诉他人。你可以分享故事、想法，或朗读自己写的内容。",
            },
            "prompt": "Tell about a time you or someone else shared a story in class.",
            "steps": [
                {
                    "minutes": 2,
                    "instruction": "Turn and talk to your partner or group.",
                    "chinese": "和同伴或小组交流。",
                },
                {
                    "minutes": 3,
                    "instruction": "Write 1–3 sentences. Be ready to share what you have written.",
                    "chinese": "写 1–3 句，并准备分享。",
                },
            ],
            "source": source(16, "Vocabulary Extension"),
        },
    ),
    CoursewareBlock(
        block_code="wordly-wise-review",
        block_type="wordly_wise_review",
        title="Review · Hidden Message",
        sort_order=80,
        payload={
            "family": "wordly_wise",
            "intro": "补全句子后再揭晓谜语答案；每题都能回到本课词义。",
            "riddle": "Joanne bet Joe that her dog could jump higher than a house. How did she win the bet?",
            "riddle_answer": "A house can't jump.",
            "items": [
                {
                    "number": 1,
                    "prompt": "The cloth was one ______ wide.",
                    "answer": "yard",
                    "chinese": "这块布宽一 yard。",
                },
                {
                    "number": 2,
                    "prompt": "Sue forgot her lunch, so I offered to ______ mine with her.",
                    "answer": "share",
                    "chinese": "Sue 忘了带午饭，所以我提出和她分享我的午饭。",
                },
                {
                    "number": 3,
                    "prompt": "______ is the opposite of bad.",
                    "answer": "good",
                    "chinese": "good 是 bad 的反义词。",
                },
                {
                    "number": 4,
                    "prompt": "Ramon needs a ______ of stamps for his letter.",
                    "answer": "couple",
                    "chinese": "Ramon 的信需要两张邮票。",
                },
                {
                    "number": 5,
                    "prompt": "Ellen put the ______ back on the sofa, after it fell.",
                    "answer": "cushion",
                    "chinese": "Ellen 把掉下来的靠垫放回沙发。",
                },
                {
                    "number": 6,
                    "prompt": "Three, two, one, ______.",
                    "answer": "zero",
                    "chinese": "三、二、一、零。",
                },
                {
                    "number": 7,
                    "prompt": "The kitten scratched my arm with its ______.",
                    "answer": "claws",
                    "chinese": "小猫用爪子抓伤了我的胳膊。",
                },
                {
                    "number": 8,
                    "prompt": "The baby ______ followed its mother to the barn.",
                    "answer": "calf",
                    "chinese": "小牛跟着妈妈去了谷仓。",
                },
                {
                    "number": 9,
                    "prompt": "The children ran for ______ as soon as the rain started.",
                    "answer": "shelter",
                    "chinese": "一下雨，孩子们就跑去避雨。",
                },
                {
                    "number": 10,
                    "prompt": "The opposite of in is ______.",
                    "answer": "out",
                    "chinese": "out 是 in 的反义词。",
                },
                {
                    "number": 11,
                    "prompt": "The ______ leads the horse to the stable.",
                    "answer": "groom",
                    "chinese": "马夫把马带到马厩。",
                },
                {
                    "number": 12,
                    "prompt": "Large birds must ______ their wings to get into the air.",
                    "answer": "flap",
                    "chinese": "大型鸟必须拍动翅膀才能飞起来。",
                },
            ],
            "source": source(17, "Review Hidden Message"),
        },
    ),
)


def encode(value: dict) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def validate_source_data() -> None:
    """Fail before touching the database when the hand-transcribed lesson drifts."""

    expected_codes = {
        "wordly-wise-hero",
        "wordly-wise-meanings",
        "wordly-wise-connections",
        "wordly-wise-application",
        "wordly-wise-reading",
        "wordly-wise-comprehension",
        "wordly-wise-extension",
        "wordly-wise-review",
    }
    actual_codes = {block.block_code for block in BLOCKS}
    if actual_codes != expected_codes or len(BLOCKS) != len(expected_codes):
        raise RuntimeError("Lesson 1 courseware block codes are incomplete or duplicated.")
    if [block.sort_order for block in BLOCKS] != sorted(block.sort_order for block in BLOCKS):
        raise RuntimeError("Lesson 1 courseware blocks must be ordered.")

    by_code = {block.block_code: block for block in BLOCKS}
    meanings = by_code["wordly-wise-meanings"].payload["items"]
    applications = by_code["wordly-wise-application"].payload["items"]
    connections = by_code["wordly-wise-connections"].payload["items"]
    reading = by_code["wordly-wise-reading"].payload["paragraphs"]
    comprehension = by_code["wordly-wise-comprehension"].payload["items"]
    review = by_code["wordly-wise-review"].payload["items"]
    if not (len(meanings) == 10 and len(applications) == 5 and len(connections) == 5):
        raise RuntimeError("Lesson 1 exercise counts do not match the source pages.")
    if len(reading) != 7 or len(comprehension) != 10 or len(review) != 12:
        raise RuntimeError("Lesson 1 reading, comprehension, or review data is incomplete.")
    if not all(paragraph["english"].strip() and paragraph["chinese"].strip() for paragraph in reading):
        raise RuntimeError("Every reading paragraph needs English and Chinese text.")


def _required_id(connection: Connection, statement, label: str) -> int:
    values = [int(value) for value in connection.execute(statement).scalars()]
    if len(values) != 1:
        raise RuntimeError(f"Expected exactly one {label}; found {len(values)}.")
    return values[0]


def _inserted_id(connection: Connection, result, table, where_clause) -> int:
    inserted_id = result.inserted_primary_key[0]
    if inserted_id is not None:
        return int(inserted_id)
    return int(connection.execute(select(table.c.id).where(where_clause)).scalar_one())


def _upsert_lesson(
    connection: Connection, material_id: int, actor_id: int, report: dict[str, int]
) -> int:
    source_metadata = {
        "courseware_family": "wordly_wise",
        "courseware_version": 1,
        "source": {
            "document": SOURCE_DOCUMENT,
            "source_lesson": SOURCE_LESSON,
            "pdf_pages": list(SOURCE_PDF_PAGES),
            "book_pages": list(SOURCE_BOOK_PAGES),
            "page_kind": "practice-reading-extension-review",
        },
        "block_codes": [block.block_code for block in BLOCKS],
    }
    values = {
        "lesson_code": LESSON_CODE,
        "title": "Lesson 1 · 阅读与练习",
        "title_en": "Bailey Finds a New Home",
        "summary": "词义辨析、关联归类、语义应用、课文阅读、理解题、词汇拓展和复习。",
        "illustration_url": None,
        "source_resource": None,
        "source_reference_id": None,
        "content_json": encode(source_metadata),
        "lesson_format": "courseware",
        "lesson_schema_version": 1,
        "content_status": "published",
        "published_at": func.now(),
        "estimated_minutes": 35,
        # Book 2 Lesson 1 Word List uses source page 7.  Page 10 keeps this
        # companion lesson directly after it and before Lesson 2's page 18.
        "sort_order": 10,
        "is_published": 1,
    }
    lesson_id = connection.execute(
        select(m.learning_material_lesson.c.id).where(
            m.learning_material_lesson.c.material_id == material_id,
            m.learning_material_lesson.c.lesson_code == LESSON_CODE,
        )
    ).scalar_one_or_none()
    if lesson_id is None:
        result = connection.execute(
            m.learning_material_lesson.insert().values(
                material_id=material_id, created_by=actor_id, **values
            )
        )
        lesson_id = _inserted_id(
            connection,
            result,
            m.learning_material_lesson,
            (
                (m.learning_material_lesson.c.material_id == material_id)
                & (m.learning_material_lesson.c.lesson_code == LESSON_CODE)
            ),
        )
        report["lessons_created"] += 1
    else:
        connection.execute(
            update(m.learning_material_lesson)
            .where(m.learning_material_lesson.c.id == lesson_id)
            .values(updated_by=actor_id, **values)
        )
        report["lessons_updated"] += 1
    return int(lesson_id)


def _replace_blocks(
    connection: Connection, lesson_id: int, actor_id: int, report: dict[str, int]
) -> None:
    expected_codes = {block.block_code for block in BLOCKS}
    existing = {
        str(row["block_code"]): int(row["id"])
        for row in connection.execute(
            select(m.courseware_block.c.id, m.courseware_block.c.block_code).where(
                m.courseware_block.c.material_lesson_id == lesson_id
            )
        ).mappings()
    }
    stale_ids = [block_id for code, block_id in existing.items() if code not in expected_codes]
    if stale_ids:
        connection.execute(
            delete(m.courseware_block_source).where(
                m.courseware_block_source.c.courseware_block_id.in_(stale_ids)
            )
        )
        connection.execute(delete(m.courseware_block).where(m.courseware_block.c.id.in_(stale_ids)))
        report["blocks_removed"] += len(stale_ids)

    for block in BLOCKS:
        values = {
            "block_type": block.block_type,
            "title": block.title,
            "payload_json": encode(block.payload),
            "sort_order": block.sort_order,
            "status": "published",
        }
        block_id = existing.get(block.block_code)
        if block_id is None:
            result = connection.execute(
                m.courseware_block.insert().values(
                    material_lesson_id=lesson_id,
                    block_code=block.block_code,
                    created_by=actor_id,
                    updated_by=actor_id,
                    **values,
                )
            )
            _inserted_id(
                connection,
                result,
                m.courseware_block,
                (
                    (m.courseware_block.c.material_lesson_id == lesson_id)
                    & (m.courseware_block.c.block_code == block.block_code)
                ),
            )
            report["blocks_created"] += 1
        else:
            connection.execute(
                update(m.courseware_block)
                .where(m.courseware_block.c.id == block_id)
                .values(updated_by=actor_id, **values)
            )
            report["blocks_updated"] += 1


def seed_wordly_wise_2_lesson1_courseware(engine: Engine) -> dict[str, int]:
    """Create or refresh only the Book 2 Lesson 1 practice/read courseware."""

    validate_source_data()
    report = {
        "lessons_created": 0,
        "lessons_updated": 0,
        "blocks_created": 0,
        "blocks_updated": 0,
        "blocks_removed": 0,
    }
    with engine.begin() as connection:
        actor_id = _required_id(
            connection,
            select(m.user.c.id)
            .where(m.user.c.role == "admin")
            .order_by(m.user.c.id)
            .limit(1),
            "administrator account",
        )
        material_id = _required_id(
            connection,
            select(m.learning_material.c.id).where(
                m.learning_material.c.material_code == MATERIAL_CODE
            ),
            f"Wordly Wise 2 material {MATERIAL_CODE!r}",
        )
        course_id = _required_id(
            connection,
            select(m.learning_course.c.id).where(
                m.learning_course.c.course_code == COURSE_CODE
            ),
            f"Wordly Wise 2 course {COURSE_CODE!r}",
        )
        linked_material = connection.execute(
            select(m.learning_course_material.c.id).where(
                m.learning_course_material.c.course_id == course_id,
                m.learning_course_material.c.material_id == material_id,
            )
        ).scalar_one_or_none()
        if linked_material is None:
            raise RuntimeError("The Wordly Wise 2 course is not linked to its material.")
        lesson_id = _upsert_lesson(connection, material_id, actor_id, report)
        _replace_blocks(connection, lesson_id, actor_id, report)

    return {
        **report,
        "material_id": material_id,
        "course_id": course_id,
        "lesson_id": lesson_id,
        "block_count": len(BLOCKS),
    }


def main() -> None:
    print(
        json.dumps(
            seed_wordly_wise_2_lesson1_courseware(make_engine(Settings().database_url)),
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
