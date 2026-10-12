"""Seed interactive KET vocabulary mind-map courseware into the catalogue.

The "用思维导图速记KET词汇1000单词" PDF is a visual vocabulary reference.
This seed deliberately does not import page images or transcribe its layout.
Instead, it creates native vocabulary branches and word leaves in a reusable
mind-map.v1 shape:

    centre word -> semantic branches -> selectable word leaves

This is a repeatable catalogue-data seed, not a request-time dependency.

Run with:

    PYTHONPATH=. .venv/bin/python scripts/seed_ket_mind_map_courseware.py
"""

from __future__ import annotations

import json

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app import models as m
from app import schemas as s
from app.core.config import Settings
from app.core.database import make_engine
from app.services.learning_catalog import LearningCatalogService


ACTOR = {"id": 1}
MODULE_CODE = "elementary-english"
TEMPLATE_CODE = "mind-map"
TOPIC_CODE = "ket-mind-map-vocabulary"
MATERIAL_CODE = "ket-mind-map-family-demo"
LESSON_CODE = "ket-mind-map-family-01"
COURSE_CODE = "ket-mind-map-family-demo"
FOOD_MATERIAL_CODE = "ket-mind-map-food-demo"
FOOD_LESSON_CODE = "ket-mind-map-food-01"
FOOD_COURSE_CODE = "ket-mind-map-food-demo"


def row_id(db: Session, table, column, value):
    return db.execute(select(table.c.id).where(column == value)).scalar_one_or_none()


def mind_map_content() -> dict:
    """Return original learner-facing copy for the Family vocabulary example."""

    return {
        "mind_map": {
            "title": "Family",
            "title_zh": "家庭",
            "center": {
                "label": "Family",
                "label_zh": "家庭",
                "emoji": "🏠",
            },
            "branches": [
                {
                    "id": "parents",
                    "label": "Parents",
                    "label_zh": "父母",
                    "emoji": "👨‍👩‍👧",
                    "tone": "violet",
                    "leaves": [
                        {
                            "word": "parent",
                            "chinese": "父母；家长",
                            "example": "A parent is waiting at the school gate.",
                            "example_zh": "一位家长正在学校门口等候。",
                        },
                        {
                            "word": "mother",
                            "chinese": "母亲",
                            "example": "Her mother makes dinner on Fridays.",
                            "example_zh": "她的妈妈每周五做晚饭。",
                        },
                        {
                            "word": "father",
                            "chinese": "父亲",
                            "example": "My father drives me to the station.",
                            "example_zh": "我爸爸开车送我去车站。",
                        },
                        {
                            "word": "mum / dad",
                            "chinese": "妈妈 / 爸爸（口语）",
                            "example": "Dad, can you help me with this bag?",
                            "example_zh": "爸爸，你能帮我拿一下这个包吗？",
                        },
                    ],
                },
                {
                    "id": "children",
                    "label": "Children",
                    "label_zh": "孩子",
                    "emoji": "🧒",
                    "tone": "rose",
                    "leaves": [
                        {
                            "word": "child",
                            "chinese": "孩子",
                            "example": "Every child gets a name tag.",
                            "example_zh": "每个孩子都会拿到一个姓名牌。",
                        },
                        {
                            "word": "daughter",
                            "chinese": "女儿",
                            "example": "Their daughter loves drawing pictures.",
                            "example_zh": "他们的女儿喜欢画画。",
                        },
                        {
                            "word": "son",
                            "chinese": "儿子",
                            "example": "His son is in my English class.",
                            "example_zh": "他的儿子和我在同一个英语班。",
                        },
                        {
                            "word": "twin",
                            "chinese": "双胞胎中的一个",
                            "example": "She has a twin brother.",
                            "example_zh": "她有一个双胞胎兄弟。",
                        },
                    ],
                },
                {
                    "id": "grandparents",
                    "label": "Grandparents",
                    "label_zh": "祖辈",
                    "emoji": "👵",
                    "tone": "sun",
                    "leaves": [
                        {
                            "word": "grandparent",
                            "chinese": "祖父母；外祖父母",
                            "example": "My grandparents live near the park.",
                            "example_zh": "我的祖父母住在公园附近。",
                        },
                        {
                            "word": "grandmother",
                            "chinese": "祖母；外祖母",
                            "example": "Her grandmother tells funny stories.",
                            "example_zh": "她的奶奶会讲有趣的故事。",
                        },
                        {
                            "word": "grandfather",
                            "chinese": "祖父；外祖父",
                            "example": "My grandfather grows tomatoes.",
                            "example_zh": "我的爷爷种番茄。",
                        },
                        {
                            "word": "grandma / grandpa",
                            "chinese": "奶奶 / 爷爷（口语）",
                            "example": "Grandpa is making tea in the kitchen.",
                            "example_zh": "爷爷正在厨房泡茶。",
                        },
                    ],
                },
                {
                    "id": "relatives",
                    "label": "Relatives",
                    "label_zh": "亲属",
                    "emoji": "🤝",
                    "tone": "sky",
                    "leaves": [
                        {
                            "word": "relative",
                            "chinese": "亲属",
                            "example": "We visit relatives during the holiday.",
                            "example_zh": "假期里我们会探望亲属。",
                        },
                        {
                            "word": "uncle",
                            "chinese": "叔叔；舅舅；伯伯",
                            "example": "My uncle works in a bookshop.",
                            "example_zh": "我叔叔在一家书店工作。",
                        },
                        {
                            "word": "aunt",
                            "chinese": "阿姨；姑姑；姨妈",
                            "example": "Aunt May is coming for lunch.",
                            "example_zh": "梅姨要来吃午饭。",
                        },
                        {
                            "word": "cousin",
                            "chinese": "堂（表）兄弟姐妹",
                            "example": "I play badminton with my cousin.",
                            "example_zh": "我和表哥一起打羽毛球。",
                        },
                    ],
                },
                {
                    "id": "relationships",
                    "label": "Relationships",
                    "label_zh": "家庭关系",
                    "emoji": "💞",
                    "tone": "mint",
                    "leaves": [
                        {
                            "word": "family",
                            "chinese": "家庭；家人",
                            "example": "There are four people in my family.",
                            "example_zh": "我家有四口人。",
                        },
                        {
                            "word": "husband",
                            "chinese": "丈夫",
                            "example": "Her husband is cooking tonight.",
                            "example_zh": "她的丈夫今晚在做饭。",
                        },
                        {
                            "word": "wife",
                            "chinese": "妻子",
                            "example": "His wife is good at singing.",
                            "example_zh": "他的妻子很擅长唱歌。",
                        },
                        {
                            "word": "married",
                            "chinese": "已婚的",
                            "example": "Are your parents married?",
                            "example_zh": "你的父母结婚了吗？",
                        },
                    ],
                },
            ],
        }
    }


FOOD_WORD_PRONUNCIATIONS = {
    "food": "/fuːd/",
    "crop": "/krɒp/",
    "rice": "/raɪs/",
    "flour": "/ˈflaʊə(r)/",
    "pasta": "/ˈpæstə/",
    "noodle": "/ˈnuːdl/",
    "omelette": "/ˈɒmlət/",
    "pizza": "/ˈpiːtsə/",
    "sandwich": "/ˈsænwɪtʃ/",
    "cheese": "/tʃiːz/",
    "burger": "/ˈbɜːɡə(r)/",
    "cheeseburger": "/ˈtʃiːzbɜːɡə(r)/",
    "chip": "/tʃɪp/",
    "steak": "/steɪk/",
    "tin": "/tɪn/",
    "ham": "/hæm/",
    "sausage": "/ˈsɒsɪdʒ/",
    "salad": "/ˈsæləd/",
    "soup": "/suːp/",
    "popcorn": "/ˈpɒpkɔːn/",
    "nut": "/nʌt/",
    "peanut": "/ˈpiːnʌt/",
}

FOOD_BRANCH_PRONUNCIATIONS = {
    "cereal": "/ˈsɪəriəl/",
    "fast-food": "/ˌfɑːst ˈfuːd/",
    "dinner": "/ˈdɪnə(r)/",
    "snack": "/snæk/",
}

FOOD_MEMORY_HINTS = {
    "food": {
        "memory_label": "音律记忆",
        "memory_tip": "拉长 /uːd/，用 good、wood 的尾音帮助记住 food。",
    },
    "pizza": {
        "memory_label": "发音记忆",
        "memory_tip": "先读长音 /piː/，再清楚带出中间的 /ts/。",
    },
    "tin": {
        "memory_label": "发音记忆",
        "memory_tip": "把 tin 联想成“一听罐头”的“听”，记住 /tɪn/。",
    },
    "nut": {
        "memory_label": "音律记忆",
        "memory_tip": "用 cut /kʌt/ 的尾音带出 nut /nʌt/，两词共享 /ʌ/。",
    },
    "sandwich": {
        "memory_label": "发音记忆",
        "memory_tip": "“三明治”的常用读音可帮助联想 sandwich；注意结尾 /wɪtʃ/。",
    },
    "cheeseburger": {
        "memory_label": "构词记忆",
        "memory_tip": "先拆成 cheese 和 burger，再组合成“芝士汉堡”。",
    },
}

FOOD_BRANCH_STUDY_NOTES = {
    "fast-food": [
        {
            "type": "collocation",
            "label": "搭配",
            "english": "fast-food restaurants",
            "chinese": "快餐店",
        }
    ],
    "dinner": [
        {
            "type": "collocation",
            "label": "搭配",
            "english": "have dinner",
            "chinese": "吃正餐；吃晚餐",
        }
    ],
}

FOOD_WORD_STUDY_NOTES = {
    "crop": [
        {
            "type": "collocation",
            "label": "搭配",
            "english": "crop of the year",
            "chinese": "年产量",
        }
    ],
    "tin": [
        {
            "type": "collocation",
            "label": "搭配",
            "english": "a tin of beans",
            "chinese": "一罐豆子",
        }
    ],
    "sausage": [
        {
            "type": "collocation",
            "label": "搭配",
            "english": "pork sausage",
            "chinese": "猪肉香肠",
        }
    ],
    "salad": [
        {
            "type": "collocation",
            "label": "搭配",
            "english": "fruit salad",
            "chinese": "水果沙拉",
        }
    ],
    "popcorn": [
        {
            "type": "collocation",
            "label": "搭配",
            "english": "a bag of popcorn",
            "chinese": "一袋爆米花",
        }
    ],
    "peanut": [
        {
            "type": "collocation",
            "label": "搭配",
            "english": "peanut butter",
            "chinese": "花生酱",
        }
    ],
    "sandwich": [
        {
            "type": "word_form",
            "label": "复数",
            "english": "sandwiches",
            "chinese": "",
        }
    ],
    "chip": [
        {
            "type": "usage",
            "label": "用法",
            "english": "chips",
            "chinese": "表示炸薯条时常用复数",
        },
        {
            "type": "related_word",
            "label": "近义",
            "english": "fry",
            "chinese": "炸薯条",
        },
    ],
}


def food_mind_map_content() -> dict:
    """Return original learner-facing copy for the Food vocabulary example.

    Its branch order and variable leaf counts follow the Food page in the
    reference courseware: cereal, fast food, dinner, and snacks.  The examples
    are newly written for this interactive lesson.
    """

    content = {
        "mind_map": {
            "title": "Food",
            "title_zh": "食物",
            "center": {
                "label": "Food",
                "label_zh": "食物",
                "emoji": "🍽️",
            },
            "branches": [
                {
                    "id": "cereal",
                    "label": "Cereal",
                    "label_zh": "谷物主食",
                    "emoji": "🌾",
                    "tone": "violet",
                    "leaves": [
                        {
                            "word": "crop",
                            "chinese": "农作物",
                            "example": "Rice is an important crop in this town.",
                            "example_zh": "水稻是这个小镇的重要农作物。",
                        },
                        {
                            "word": "rice",
                            "chinese": "米饭；大米",
                            "example": "Would you like rice or bread with your soup?",
                            "example_zh": "你的汤想配米饭还是面包？",
                        },
                        {
                            "word": "flour",
                            "chinese": "面粉",
                            "example": "We need flour to make the birthday cake.",
                            "example_zh": "做生日蛋糕需要面粉。",
                        },
                        {
                            "word": "pasta",
                            "chinese": "意大利面",
                            "example": "Pasta is ready in ten minutes.",
                            "example_zh": "意大利面十分钟就做好了。",
                        },
                        {
                            "word": "noodle",
                            "chinese": "面条",
                            "example": "My brother likes noodles for lunch.",
                            "example_zh": "我弟弟午饭喜欢吃面条。",
                        },
                        {
                            "word": "omelette",
                            "chinese": "煎蛋卷",
                            "example": "Can you make an omelette with mushrooms?",
                            "example_zh": "你能做一个蘑菇煎蛋卷吗？",
                        },
                    ],
                },
                {
                    "id": "fast-food",
                    "label": "Fast Food",
                    "label_zh": "快餐",
                    "emoji": "🍔",
                    "tone": "rose",
                    "leaves": [
                        {
                            "word": "pizza",
                            "chinese": "比萨饼",
                            "example": "The children chose a vegetable pizza.",
                            "example_zh": "孩子们选了一份蔬菜比萨。",
                        },
                        {
                            "word": "sandwich",
                            "chinese": "三明治",
                            "example": "My sandwich has egg and tomato in it.",
                            "example_zh": "我的三明治里有鸡蛋和番茄。",
                        },
                        {
                            "word": "cheese",
                            "chinese": "奶酪",
                            "example": "Please put a little cheese on the pasta.",
                            "example_zh": "请在意面上放一点奶酪。",
                        },
                        {
                            "word": "burger",
                            "chinese": "汉堡",
                            "example": "He ordered a burger after the football game.",
                            "example_zh": "足球赛后他点了一个汉堡。",
                        },
                        {
                            "word": "cheeseburger",
                            "chinese": "芝士汉堡",
                            "example": "A cheeseburger comes with chips on the side.",
                            "example_zh": "芝士汉堡配有薯条。",
                        },
                        {
                            "word": "chip",
                            "chinese": "炸薯条；薯片",
                            "example": "The chips are still warm.",
                            "example_zh": "这些薯条还是热的。",
                        },
                    ],
                },
                {
                    "id": "dinner",
                    "label": "Dinner",
                    "label_zh": "晚餐",
                    "emoji": "🍲",
                    "tone": "sun",
                    "leaves": [
                        {
                            "word": "steak",
                            "chinese": "牛排",
                            "example": "Dad cooks steak for Sunday dinner.",
                            "example_zh": "爸爸周日晚餐会做牛排。",
                        },
                        {
                            "word": "tin",
                            "chinese": "罐头；金属罐",
                            "example": "The beans are in a tin in the cupboard.",
                            "example_zh": "豆子装在橱柜里的一个罐头里。",
                        },
                        {
                            "word": "ham",
                            "chinese": "火腿",
                            "example": "There is ham in the salad today.",
                            "example_zh": "今天的沙拉里有火腿。",
                        },
                        {
                            "word": "sausage",
                            "chinese": "香肠",
                            "example": "The sausage is hot, so wait a minute.",
                            "example_zh": "香肠很烫，等一会儿。",
                        },
                        {
                            "word": "salad",
                            "chinese": "沙拉",
                            "example": "The salad is fresh and colourful.",
                            "example_zh": "这份沙拉新鲜又色彩丰富。",
                        },
                        {
                            "word": "soup",
                            "chinese": "汤",
                            "example": "This chicken soup smells wonderful.",
                            "example_zh": "这碗鸡汤闻起来很香。",
                        },
                    ],
                },
                {
                    "id": "snack",
                    "label": "Snack",
                    "label_zh": "零食",
                    "emoji": "🍿",
                    "tone": "sky",
                    "leaves": [
                        {
                            "word": "popcorn",
                            "chinese": "爆米花",
                            "example": "We shared popcorn during the movie.",
                            "example_zh": "看电影时我们一起分享爆米花。",
                        },
                        {
                            "word": "nut",
                            "chinese": "坚果",
                            "example": "A handful of nuts is easy to carry.",
                            "example_zh": "一小把坚果很方便携带。",
                        },
                        {
                            "word": "peanut",
                            "chinese": "花生",
                            "example": "She cannot eat peanuts at school.",
                            "example_zh": "她在学校不能吃花生。",
                        },
                    ],
                },
            ],
        }
    }
    root = content["mind_map"]
    root["center"]["part_of_speech"] = "noun"
    root["center"]["pronunciation"] = FOOD_WORD_PRONUNCIATIONS["food"]
    root["center"].update(FOOD_MEMORY_HINTS["food"])
    for branch in root["branches"]:
        branch["part_of_speech"] = "noun"
        branch["pronunciation"] = FOOD_BRANCH_PRONUNCIATIONS[branch["id"]]
        if branch["id"] in FOOD_BRANCH_STUDY_NOTES:
            branch["study_notes"] = FOOD_BRANCH_STUDY_NOTES[branch["id"]]
        for leaf in branch["leaves"]:
            word = leaf["word"]
            leaf["part_of_speech"] = "noun"
            leaf["pronunciation"] = FOOD_WORD_PRONUNCIATIONS[word]
            if word in FOOD_MEMORY_HINTS:
                leaf.update(FOOD_MEMORY_HINTS[word])
            if word in FOOD_WORD_STUDY_NOTES:
                leaf["study_notes"] = FOOD_WORD_STUDY_NOTES[word]
    return content


def validate_mind_map_content(
    content: dict,
    *,
    expected_branch_count: int | None = None,
    expected_leaf_counts: tuple[int, ...] | None = None,
) -> None:
    """Validate the flexible mind-map.v1 shape without flattening its branches."""

    root = content.get("mind_map")
    if not isinstance(root, dict):
        raise ValueError("The demo must include a mind_map object.")
    branches = root.get("branches")
    if not isinstance(branches, list) or not branches:
        raise ValueError("A mind map must include at least one semantic branch.")
    if expected_branch_count is not None and len(branches) != expected_branch_count:
        raise ValueError(
            f"Expected {expected_branch_count} semantic branches, got {len(branches)}."
        )
    if expected_leaf_counts is not None and len(branches) != len(expected_leaf_counts):
        raise ValueError("Expected leaf counts must describe every semantic branch.")
    if any(not isinstance(branch, dict) for branch in branches):
        raise ValueError("Each semantic branch must be an object.")
    ids = [branch.get("id") for branch in branches]
    if len(ids) != len(set(ids)) or any(not branch_id for branch_id in ids):
        raise ValueError("Mind-map branch IDs must be unique and non-empty.")
    words = []
    for index, branch in enumerate(branches):
        leaves = branch.get("leaves")
        if not isinstance(leaves, list) or not leaves:
            raise ValueError("Each semantic branch must have at least one word leaf.")
        if (
            expected_leaf_counts is not None
            and len(leaves) != expected_leaf_counts[index]
        ):
            raise ValueError(
                f"Branch {branch['id']} should have {expected_leaf_counts[index]} word leaves."
            )
        for leaf in leaves:
            if not isinstance(leaf, dict) or not all(
                leaf.get(field)
                for field in ("word", "chinese", "example", "example_zh")
            ):
                raise ValueError("Each word leaf needs word, meaning, and example copy.")
            words.append(leaf["word"])
    if len(words) != len(set(words)):
        raise ValueError("A word leaf should only appear once in this demo map.")


def main() -> None:
    content = mind_map_content()
    validate_mind_map_content(
        content,
        expected_branch_count=5,
        expected_leaf_counts=(4, 4, 4, 4, 4),
    )
    food_content = food_mind_map_content()
    validate_mind_map_content(
        food_content,
        expected_branch_count=4,
        expected_leaf_counts=(6, 6, 6, 3),
    )
    settings = Settings()
    engine = make_engine(settings.database_url)
    with Session(engine) as db:
        catalog = LearningCatalogService(db)
        template = catalog.save_template(
            s.LearningTemplateInput(
                template_code=TEMPLATE_CODE,
                template_version=1,
                name="思维导图课件",
                description="逐页展示原 PDF 思维导图版面，兼容互动词汇图。",
                content_kind="source",
                supported_clients=["web", "mini"],
                config={
                    "content_schema": "mind-map.v1",
                    "presentation": "interactive-map",
                    "interaction": "branch-explorer",
                    "recommended_minutes": 5,
                },
                status="active",
                sort_order=45,
            ),
            ACTOR,
            row_id(db, m.learning_template, m.learning_template.c.template_code, TEMPLATE_CODE),
        )

        module_id = db.execute(
            select(m.learning_module.c.id).where(
                m.learning_module.c.module_code == MODULE_CODE
            )
        ).scalar_one_or_none()
        if module_id is None:
            raise RuntimeError(f"Missing learning module: {MODULE_CODE}")
        topic = catalog.save_topic(
            s.LearningTopicInput(
                module_id=module_id,
                topic_code=TOPIC_CODE,
                title="KET 词汇思维导图 · 范例",
                title_en="KET Vocabulary Mind Maps · Demo",
                description="用中心词、语义分支和词叶来记 KET 高频词汇；当前提供 Family 和 Food 两个交互范例。",
                sort_order=95,
                is_published=1,
            ),
            ACTOR,
            row_id(db, m.learning_topic, m.learning_topic.c.topic_code, TOPIC_CODE),
        )

        material_payload = s.LearningMaterialInput(
            template_id=template["id"],
            material_code=MATERIAL_CODE,
            title="Family · 家庭关系",
            title_en="Family Vocabulary Map",
            summary="一张可点击的家庭词汇地图：先看关系，再点开分支，最后用一句自己的话回忆。",
            material_type="mind_map",
            publisher="Happy English",
            version_name="思维导图课件 v1",
            difficulty_code="ket",
            estimated_minutes=5,
            sort_order=10,
            is_published=1,
        )
        material_id = row_id(
            db, m.learning_material, m.learning_material.c.material_code, MATERIAL_CODE
        )
        material = catalog.save_material(
            material_payload,
            ACTOR,
            material_id,
        )

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
                title="家庭词汇地图",
                title_en="Family Vocabulary Map",
                summary="",
                lesson_format="source",
                content=content,
                estimated_minutes=5,
                sort_order=10,
                is_published=1,
            ),
            ACTOR,
            lesson_id,
        )

        # Revalidate the material with its saved lesson before exposing the
        # generated one-material course.
        material = catalog.save_material(material_payload, ACTOR, material["id"])
        course = catalog.save_course(
            s.LearningCourseInput(
                topic_id=topic["id"],
                material_ids=[material["id"]],
                course_code=COURSE_CODE,
                title="KET 思维导图 · Family 范例",
                title_en="KET Mind Map · Family Demo",
                summary="用可点开的关系图记家庭词汇，作为思维导图课件的第一个交互范例。",
                course_type="lesson",
                estimated_minutes=5,
                difficulty_code="ket",
                sort_order=10,
                is_published=1,
                access_policy="free",
            ),
            ACTOR,
            row_id(db, m.learning_course, m.learning_course.c.course_code, COURSE_CODE),
        )
        db.execute(
            update(m.learning_topic_course)
            .where(
                m.learning_topic_course.c.topic_id == topic["id"],
                m.learning_topic_course.c.course_id == course["id"],
            )
            .values(sort_order=10, updated_by=ACTOR["id"])
        )

        food_material_payload = s.LearningMaterialInput(
            template_id=template["id"],
            material_code=FOOD_MATERIAL_CODE,
            title="Food · 食物",
            title_en="Food Vocabulary Map",
            summary="一张可点击的食物词汇地图：从谷物、快餐、晚餐到零食，把常见食物放进餐桌场景里记。",
            material_type="mind_map",
            publisher="Happy English",
            version_name="思维导图课件 v1",
            difficulty_code="ket",
            estimated_minutes=5,
            sort_order=20,
            is_published=1,
        )
        food_material_id = row_id(
            db,
            m.learning_material,
            m.learning_material.c.material_code,
            FOOD_MATERIAL_CODE,
        )
        food_material = catalog.save_material(
            food_material_payload,
            ACTOR,
            food_material_id,
        )

        food_lesson_id = db.execute(
            select(m.learning_material_lesson.c.id).where(
                m.learning_material_lesson.c.material_id == food_material["id"],
                m.learning_material_lesson.c.lesson_code == FOOD_LESSON_CODE,
            )
        ).scalar_one_or_none()
        food_lesson = catalog.save_material_lesson(
            food_material["id"],
            s.LearningMaterialLessonInput(
                lesson_code=FOOD_LESSON_CODE,
                title="食物词汇地图",
                title_en="Food Vocabulary Map",
                summary="",
                lesson_format="source",
                content=food_content,
                estimated_minutes=5,
                sort_order=10,
                is_published=1,
            ),
            ACTOR,
            food_lesson_id,
        )

        # Revalidate the Food material with its saved lesson before exposing
        # the generated one-material course.
        food_material = catalog.save_material(
            food_material_payload,
            ACTOR,
            food_material["id"],
        )
        food_course = catalog.save_course(
            s.LearningCourseInput(
                topic_id=topic["id"],
                material_ids=[food_material["id"]],
                course_code=FOOD_COURSE_CODE,
                title="KET 思维导图 · Food 范例",
                title_en="KET Mind Map · Food Demo",
                summary="用可点开的食物图记住餐桌词汇，展示思维导图课件如何承接一页词汇课件。",
                course_type="lesson",
                estimated_minutes=5,
                difficulty_code="ket",
                sort_order=20,
                is_published=1,
                access_policy="free",
            ),
            ACTOR,
            row_id(
                db,
                m.learning_course,
                m.learning_course.c.course_code,
                FOOD_COURSE_CODE,
            ),
        )
        db.execute(
            update(m.learning_topic_course)
            .where(
                m.learning_topic_course.c.topic_id == topic["id"],
                m.learning_topic_course.c.course_id == food_course["id"],
            )
            .values(sort_order=20, updated_by=ACTOR["id"])
        )
        db.commit()

    print(
        json.dumps(
            {
                "topic_id": topic["id"],
                "topic_code": TOPIC_CODE,
                "family": {
                    "material_id": material["id"],
                    "lesson_id": lesson["id"],
                    "course_id": course["id"],
                },
                "food": {
                    "material_id": food_material["id"],
                    "lesson_id": food_lesson["id"],
                    "course_id": food_course["id"],
                },
                "template": f"{TEMPLATE_CODE}.v1",
                "access_policy": "free",
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
