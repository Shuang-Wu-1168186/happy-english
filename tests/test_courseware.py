import pytest

from fastapi import HTTPException

from app.services.courseware import NoteCoursewareService
from app.services.courseware_scene_catalog import (
    CURATED_REAL_LIFE_EXPRESSION_SCENES,
    CURATED_REAL_LIFE_SCENES,
)
from tests.conftest import sign_in


def _block_payload(preview, block_type):
    return next(block["payload"] for block in preview["blocks"] if block["block_type"] == block_type)


def test_note_courseware_uses_a_real_scene_and_a_blanked_sentence_for_output():
    service = NoteCoursewareService(None)
    items = [
        {
            "id": 338,
            "item_title": "rear-view mirror",
            "raw_text": "rear-view mirror",
            "english_text": "rear-view mirror",
            "chinese_text": "车内后视镜。",
            "explanation": "",
            "examples": "rear-view mirror = 后视镜",
        },
        {
            "id": 343,
            "item_title": "twist",
            "raw_text": "twist",
            "english_text": "twist",
            "chinese_text": "扭；拧；转折。",
            "explanation": "",
            "examples": "Twist the cap off.",
        },
        {
            "id": 330,
            "item_title": "1800 / eighteen hundred",
            "raw_text": "1800 / eighteen hundred",
            "english_text": "1800 / eighteen hundred",
            "chinese_text": "作为年份时常读作 eighteen hundred。",
            "explanation": "",
            "examples": "This building was built in eighteen hundred.",
        },
    ]

    previews = [service._preview_item(item) for item in items]

    assert _block_payload(previews[0], "dialogue")["lines"] == [
        {"speaker": "人物 A", "english": "Which mirror should I check before reversing?", "chinese": "倒车前我该看哪面镜子？"},
        {"speaker": "人物 B", "english": "Check the rear-view mirror.", "chinese": "看后视镜。"},
    ]
    assert _block_payload(previews[1], "dialogue")["lines"] == [
        {"speaker": "人物 A", "english": "This bottle won't open. What should I do?", "chinese": "这个瓶子打不开，我该怎么做？"},
        {"speaker": "人物 B", "english": "Twist the cap off.", "chinese": "把瓶盖拧下来。"},
    ]
    assert _block_payload(previews[2], "dialogue")["lines"] == [
        {"speaker": "人物 A", "english": "Do you know when this building was built?", "chinese": "你知道这座楼是什么时候建的吗？"},
        {"speaker": "人物 B", "english": "It was built in eighteen hundred.", "chinese": "它建于 1800 年。"},
    ]
    assert [_block_payload(preview, "output")["patterns"] for preview in previews] == [
        ["Check the ________."],
        ["________ the cap off."],
        ["It was built in ________."],
    ]
    assert all(
        payload["instruction"] == "先读完整句，再把横线处填成今天要练的关键词。"
        and all(NoteCoursewareService._is_meaningful_practice_sentence(pattern) for pattern in payload["patterns"])
        for payload in (_block_payload(preview, "output") for preview in previews)
    )


def test_note_courseware_quality_gate_rejects_old_generic_scene_openers():
    assert NoteCoursewareService.is_low_quality_scene_dialogue([
        {"speaker": "人物 A", "english": "Something unexpected happened this morning.", "chinese": "今天早上发生了一件意外的事。"},
        {"speaker": "人物 B", "english": "Twist the cap off.", "chinese": "把瓶盖拧下来。"},
    ])
    assert not NoteCoursewareService.is_low_quality_scene_dialogue([
        {"speaker": "人物 A", "english": "This bottle won't open. What should I do?", "chinese": "这个瓶子打不开，我该怎么做？"},
        {"speaker": "人物 B", "english": "Twist the cap off.", "chinese": "把瓶盖拧下来。"},
    ])


def test_courseware_quality_gate_rejects_definition_quizzes_and_catalogue_scenes_are_real():
    assert NoteCoursewareService.is_low_quality_scene_dialogue([
        {"speaker": "人物 A", "english": "What happened in that situation?", "chinese": "当时发生了什么？"},
        {"speaker": "人物 B", "english": "Stray means an animal without a home.", "chinese": "stray 指无主的动物。"},
    ])
    assert NoteCoursewareService.is_low_quality_scene_dialogue([
        {"speaker": "人物 A", "english": "What does photography do?", "chinese": "photography 做什么？"},
        {"speaker": "人物 B", "english": "Photography means the art of taking photos.", "chinese": "摄影指拍照的艺术。"},
    ])
    for opener in (
        "Can you tell me what happened?",
        "What did he do?",
        "How is she doing?",
        "What are you doing there?",
        "What will the wind do?",
    ):
        assert NoteCoursewareService.is_low_quality_scene_dialogue([
            {"speaker": "人物 A", "english": opener, "chinese": "空泛的提问。"},
            {"speaker": "人物 B", "english": "The wind will pick up after lunch.", "chinese": "午饭后风会变大。"},
        ])

    for scene in list(CURATED_REAL_LIFE_SCENES.values()) + list(CURATED_REAL_LIFE_EXPRESSION_SCENES.values()):
        lines = [
            {"speaker": "人物 A", "english": scene[0], "chinese": scene[1]},
            {"speaker": "人物 B", "english": scene[2], "chinese": scene[3]},
        ]
        assert not NoteCoursewareService.is_low_quality_scene_dialogue(lines)

    for (_, phrase), scene in CURATED_REAL_LIFE_EXPRESSION_SCENES.items():
        assert (
            NoteCoursewareService._blank_keyword(scene[0], phrase)
            or NoteCoursewareService._blank_keyword(scene[2], phrase)
            or NoteCoursewareService._blank_keyword_anchor(scene[0], phrase)
            or NoteCoursewareService._blank_keyword_anchor(scene[2], phrase)
        )


def test_courseware_quality_gate_rejects_frames_and_note_review_prompts():
    assert not NoteCoursewareService._is_meaningful_practice_sentence(
        "have an ________ to do sth"
    )
    assert not NoteCoursewareService._is_meaningful_practice_sentence(
        "I noticed a ________ on my way home."
    )
    assert NoteCoursewareService._is_meaningful_practice_sentence(
        "The wind will ________ the dry leaves across the path."
    )
    assert NoteCoursewareService.is_low_quality_scene_dialogue([
        {
            "speaker": "人物 A",
            "english": "I was looking at the autumn wind earlier. What did you find out?",
            "chinese": "我刚才在看秋风。",
        },
        {
            "speaker": "人物 B",
            "english": "The wind disperses the dry leaves across the path.",
            "chinese": "风把干树叶吹散到小路上。",
        },
    ])


def test_note_courseware_turns_a_bilingual_example_into_a_concrete_scene():
    item = {
        "id": 999,
        "item_title": "showcase",
        "raw_text": "showcase",
        "english_text": "showcase",
        "chinese_text": "展示柜；展示",
        "explanation": (
            "• The necklace is in the showcase. 那条项链在展示柜里。\n"
            "• The exhibition showcases modern art. 这个展览展示现代艺术。"
        ),
        "examples": "",
        "usage_scenarios_json": '["technical", "workplace"]',
    }

    assert NoteCoursewareService._dialogue_lines(item, "showcase", "展示柜；展示", {}) == [
        {
            "speaker": "人物 A",
            "english": "I can't find the necklace. Where is it?",
            "chinese": "我找不到它了，它在哪里？",
        },
        {
            "speaker": "人物 B",
            "english": "The necklace is in the showcase.",
            "chinese": "那条项链在展示柜里。",
        },
    ]


def test_note_courseware_uses_a_short_label_and_one_sentence_recap():
    source_item = {
        "id": 1267,
        "item_title": "suck up",
        "raw_text": "suck up",
        "english_text": "suck up",
        "chinese_text": (
            "phrasal verb\n\n🇨🇳 中文意思\n\n吸收；吸走；拍马屁 / 讨好\n\n"
            "suck up 有两个常见意思：\n\n表示液体、灰尘、空气等被吸进去。"
        ),
        "explanation": "",
        "examples": "💡 Memory Tip\n\n想象一个吸尘器把灰尘“吸进去”：",
    }
    combined_item = {
        **source_item,
        "item_title": "open up",
        "english_text": "open up\nIt opened up a whole new world.",
    }
    long_sentence_item = {
        **source_item,
        "item_title": "I started learning English when I was quite young...",
        "english_text": (
            "I started learning English when I was quite young, but I did not get much "
            "chance to practise speaking."
        ),
    }
    phrase_collection = {
        **source_item,
        "item_title": "Useful chunks to remember",
        "english_text": "run around\nlike a chicken with my head cut off\nget everything organized",
    }

    meaning = NoteCoursewareService._brief_meaning(source_item, source_item["chinese_text"])

    assert NoteCoursewareService._card_phrase(combined_item) == "open up"
    assert not NoteCoursewareService.is_long_sentence_item(combined_item)
    assert NoteCoursewareService.is_long_sentence_item(long_sentence_item)
    assert not NoteCoursewareService.is_long_sentence_item(phrase_collection)
    assert meaning == "吸收；吸走；拍马屁 / 讨好"
    assert NoteCoursewareService._recap_summary("suck up", meaning) == (
        "“suck up”表示吸收；吸走；拍马屁 / 讨好。"
    )


def test_note_courseware_splits_numbered_and_contextual_meanings_into_separate_cards():
    suck_up = {
        "chinese_text": "1. 吸收 / 吸走\n2. 拍马屁 / 讨好",
        "explanation": (
            "1. suck up + something\n"
            "This towel can suck up a lot of water.\n"
            "这条毛巾能吸很多水。\n\n"
            "2. suck up to + someone\n"
            "He’s sucking up to the manager.\n"
            "他在讨好经理。"
        ),
        "examples": "",
    }
    take_down = {
        "chinese_text": "take down 常见有几个意思。",
        "explanation": (
            "不同含义与常见用法\n\n"
            "取下；拆掉\n"
            "They took down the old sign.\n"
            "他们把旧招牌拆下来了。\n\n"
            "写下；记下\n"
            "Can you take down his phone number?\n"
            "你能把他的电话号码记下来吗？\n\n"
            "击倒；制服\n"
            "The police took down the suspect.\n"
            "警方制服了嫌疑人。\n\n"
            "删除 / 下架网络内容\n"
            "The platform took down the post.\n"
            "平台下架了这条帖子。\n\n"
            "打败某人 / 某组织\n"
            "The smaller team took down the champions.\n"
            "那支较弱的队伍击败了冠军队。"
        ),
        "examples": "",
    }

    suck_up_uses = NoteCoursewareService._usage_groups(
        suck_up["explanation"],
        NoteCoursewareService._pairs(suck_up["explanation"]),
        suck_up,
    )
    take_down_uses = NoteCoursewareService._usage_groups(
        take_down["explanation"],
        NoteCoursewareService._pairs(take_down["explanation"]),
        take_down,
    )

    assert [(use["title"], use["description"]) for use in suck_up_uses] == [
        ("suck up + something", "吸收 / 吸走"),
        ("suck up to + someone", "拍马屁 / 讨好"),
    ]
    assert [use["examples"][0]["english"] for use in suck_up_uses] == [
        "This towel can suck up a lot of water.",
        "He’s sucking up to the manager.",
    ]
    assert [use["title"] for use in take_down_uses] == [
        "取下；拆掉",
        "写下；记下",
        "击倒；制服",
        "删除 / 下架网络内容",
        "打败某人 / 某组织",
    ]


def test_note_courseware_splits_explicit_multi_headwords_into_separate_lessons():
    item = {
        "id": 334,
        "item_order": 23,
        "item_type": "vocab",
        "item_title": "scraggly / scraggle / straggly",
        "raw_text": "scraggle",
        "english_text": "scraggly / scraggle / straggly",
        "chinese_text": (
            "scraggly = 乱糟糟的；参差不齐的。"
            "scraggle = 变得乱糟糟。"
            "straggly = 更常见的“稀疏杂乱”。"
        ),
        "explanation": "常用于头发、胡子、植物、灌木。",
        "examples": "He has a scraggly beard.\nScraggly bushes grew along the fence.",
        "usage_scenarios_json": '["general"]',
    }

    previews = NoteCoursewareService(None)._preview_entries(item)

    assert [(entry["phrase"], entry["meaning"]) for entry in previews] == [
        ("scraggly", "乱糟糟的；参差不齐的"),
        ("scraggle", "变得稀疏杂乱"),
        ("straggly", "稀疏杂乱的"),
    ]
    assert [entry["source_locator"]["index"] for entry in previews] == [0, 1, 2]
    assert [
        next(block for block in entry["blocks"] if block["block_type"] == "dialogue")["payload"]["lines"]
        for entry in previews
    ] == [
        [
            {
                "speaker": "人物 A",
                "english": "Has he had time to trim his beard lately?",
                "chinese": "他最近有时间修胡子吗？",
            },
            {
                "speaker": "人物 B",
                "english": "He has a scraggly beard.",
                "chinese": "他的胡子乱糟糟的。",
            },
        ],
        [
            {
                "speaker": "人物 A",
                "english": "Why are the vines spreading over the fence like that?",
                "chinese": "藤蔓怎么那样蔓到篱笆上去了？",
            },
            {
                "speaker": "人物 B",
                "english": "The vines began to scraggle over the fence.",
                "chinese": "藤蔓开始杂乱地沿着篱笆蔓生。",
            },
        ],
        [
            {
                "speaker": "人物 A",
                "english": "How did the garden look after the dry summer?",
                "chinese": "干燥的夏天过后，花园看起来怎么样？",
            },
            {
                "speaker": "人物 B",
                "english": "After the dry summer, the garden looked straggly.",
                "chinese": "干燥的夏天过后，花园看起来稀疏又杂乱。",
            },
        ],
    ]

    ambiguous = {**item, "chinese_text": "这是一组形容凌乱状态的词。"}
    assert NoteCoursewareService._split_expression_entries(ambiguous) == []
    variants = {
        **item,
        "english_text": "megacity / megacities",
        "chinese_text": "megacity = 超大城市。megacities = 多个超大城市。",
    }
    assert NoteCoursewareService._split_expression_entries(variants) == []


def test_note_courseware_splits_labelled_headword_groups_and_rejects_unresolved_collections():
    service = NoteCoursewareService(None)
    happy_group = {
        "id": 312,
        "item_order": 1,
        "item_title": "happy / glad / delighted / thrilled / elated / overjoyed / ecstatic",
        "raw_text": "happy / glad / delighted / thrilled / elated / overjoyed / ecstatic",
        "english_text": "happy / glad / delighted / thrilled / elated / overjoyed / ecstatic",
        "chinese_text": "开心程度和使用场景的一组词。",
        "explanation": (
            "日常小开心 / 通用：\n"
            "happy\n"
            "glad\n\n"
            "礼貌、正式、邮件：\n"
            "delighted\n\n"
            "兴奋型开心（机会、旅行）：\n"
            "thrilled\n\n"
            "更偏成就感、振奋：\n"
            "elated\n\n"
            "情感型强烈喜悦（家人、平安、重大喜讯）：\n"
            "overjoyed\n\n"
            "狂喜、顶级开心（重大成功）：\n"
            "ecstatic"
        ),
        "examples": (
            "I’m happy today.\n我今天很开心。\n"
            "I’m glad to hear that.\n听到这个我很高兴。\n"
            "I’m delighted to meet you.\n很高兴见到你。\n"
            "I’m thrilled about the offer.\n我对这个机会非常兴奋。\n"
            "I felt elated after passing the exam.\n考试通过后我很振奋。\n"
            "We were overjoyed to see them safe.\n看到他们平安，我们喜出望外。\n"
            "She was ecstatic when she got the result.\n她得知结果时欣喜若狂。"
        ),
    }

    entries = service._preview_entries(happy_group)

    assert [entry["phrase"] for entry in entries] == [
        "happy", "glad", "delighted", "thrilled", "elated", "overjoyed", "ecstatic"
    ]
    assert [entry["meaning"] for entry in entries] == [
        "日常小开心 / 通用", "日常小开心 / 通用", "礼貌、正式、邮件",
        "兴奋型开心（机会、旅行）", "更偏成就感、振奋",
        "情感型强烈喜悦（家人、平安、重大喜讯）", "狂喜、顶级开心（重大成功）",
    ]

    unresolved = {
        **happy_group,
        "english_text": "red / blue",
        "chinese_text": "两种颜色。",
        "explanation": "",
        "examples": "",
    }
    with pytest.raises(HTTPException, match="multiple independent expressions"):
        service._preview_entries(unresolved)

    pronunciation = {
        **happy_group,
        "english_text": "renovate /ˈrenəveɪt/",
        "item_title": "renovate /ˈrenəveɪt/",
    }
    assert service._card_phrase(pronunciation) == "renovate"


def test_split_projection_fallbacks_use_real_scenes_and_meaningful_output_sentences():
    service = NoteCoursewareService(None)

    for (_, phrase), sentence in service._CURATED_SPLIT_PRACTICE_SENTENCES.items():
        pattern = service._blank_keyword(sentence, phrase)
        assert pattern is not None
        assert service._is_meaningful_practice_sentence(pattern)

    for (item_id, phrase), scene in service._CURATED_SPLIT_SCENES.items():
        lines = service._dialogue_lines(
            {"id": item_id, "chinese_text": "", "explanation": "", "examples": ""},
            phrase,
            "日常表达",
            {},
        )
        assert not service.is_low_quality_scene_dialogue(lines)
        assert (
            service._blank_keyword(lines[1]["english"], phrase)
            or service._blank_keyword_anchor(lines[1]["english"], phrase)
        )

    with pytest.raises(HTTPException, match="complete, meaningful sentence"):
        service._practice_patterns(
            {"id": -1, "chinese_text": "", "explanation": "", "examples": ""},
            "unmapped entry",
            "日常表达",
            [],
            [],
            [],
        )
    with pytest.raises(HTTPException, match="coherent real-life scene"):
        service._dialogue_lines(
            {
                "id": -1, "english_text": "", "raw_text": "", "chinese_text": "",
                "explanation": "", "examples": "",
            },
            "unmapped entry",
            "日常表达",
            {},
        )


def test_courseware_lesson_publishes_validated_blocks_to_course_learners(client):
    admin_headers = sign_in(client)
    material = client.post(
        "/api/admin/learning-materials",
        headers=admin_headers,
        json={
            "topic_id": 2,
            "material_code": "courseware-phrases",
            "title": "短语课件",
            "material_type": "courseware",
        },
    )
    assert material.status_code == 201
    material_id = material.json()["id"]

    lesson = client.post(
        f"/api/admin/learning-materials/{material_id}/lessons",
        headers=admin_headers,
        json={
            "lesson_code": "phrase-good-morning",
            "title": "Good morning",
            "lesson_format": "courseware",
        },
    )
    assert lesson.status_code == 201
    lesson_id = lesson.json()["id"]
    assert lesson.json()["is_published"] == 0

    hero_payload = {
        "block_code": "hero",
        "block_type": "hero",
        "payload": {
            "phrase": "Good morning",
            "meaning": "早上好",
            "memory": "morning = 早晨",
            "key_sentence": {"english": "Good morning.", "chinese": "早上好。"},
        },
    }
    hero = client.post(
        f"/api/admin/learning-material-lessons/{lesson_id}/courseware-blocks",
        headers=admin_headers,
        json=hero_payload,
    )
    assert hero.status_code == 201
    block_id = hero.json()["id"]
    assert hero.json()["status"] == "draft"

    publish_without_source = client.put(
        f"/api/admin/courseware-blocks/{block_id}",
        headers=admin_headers,
        json={**hero_payload, "status": "published"},
    )
    assert publish_without_source.status_code == 422

    invalid_source = client.put(
        f"/api/admin/courseware-blocks/{block_id}/sources",
        headers=admin_headers,
        json={
            "items": [
                {
                    "source_resource": "english_note_item",
                    "source_reference_id": 1,
                    "source_field": "english_text",
                    "source_snapshot_text": "Not in the source",
                }
            ]
        },
    )
    assert invalid_source.status_code == 422

    sources = client.put(
        f"/api/admin/courseware-blocks/{block_id}/sources",
        headers=admin_headers,
        json={
            "items": [
                {
                    "source_resource": "english_note_item",
                    "source_reference_id": 1,
                    "source_field": "english_text",
                    "source_snapshot_text": "Good morning",
                }
            ]
        },
    )
    assert sources.status_code == 200
    assert len(sources.json()["items"][0]["source_hash"]) == 64

    published_hero = client.put(
        f"/api/admin/courseware-blocks/{block_id}",
        headers=admin_headers,
        json={**hero_payload, "status": "published"},
    )
    assert published_hero.status_code == 200
    assert published_hero.json()["sources"][0]["source_snapshot_text"] == "Good morning"

    published_lesson = client.put(
        f"/api/admin/learning-material-lessons/{lesson_id}",
        headers=admin_headers,
        json={
            "lesson_code": "phrase-good-morning",
            "title": "Good morning",
            "lesson_format": "courseware",
            "is_published": 1,
        },
    )
    assert published_lesson.status_code == 200

    course = client.post(
        "/api/admin/learning/courses",
        headers=admin_headers,
        json={
            "topic_id": 2,
            "material_id": material_id,
            "course_code": "courseware-phrases-course",
            "title": "短语课件",
        },
    )
    assert course.status_code == 201

    learner_headers = sign_in(client, "learner_test")
    opened = client.post(
        f"/api/learning/courses/{course.json()['id']}/open",
        headers=learner_headers,
    )
    assert opened.status_code == 200
    learner_lesson = opened.json()["lessons"][0]
    assert learner_lesson["lesson_format"] == "courseware"
    assert learner_lesson["courseware_blocks"] == [
        {
            "id": block_id,
            "material_lesson_id": lesson_id,
            "block_code": "hero",
            "block_type": "hero",
            "title": None,
            "payload": hero_payload["payload"],
            "sort_order": 0,
            "status": "published",
            "created_by": 1,
            "updated_by": 1,
            "created_at": learner_lesson["courseware_blocks"][0]["created_at"],
            "updated_at": learner_lesson["courseware_blocks"][0]["updated_at"],
        }
    ]
    assert "sources" not in learner_lesson["courseware_blocks"][0]

    material_lesson = client.get(
        f"/api/learning/materials/{material_id}/lessons/{lesson_id}",
        headers=learner_headers,
    )
    assert material_lesson.status_code == 200
    assert material_lesson.json()["courseware_blocks"] == learner_lesson["courseware_blocks"]


def test_note_courseware_can_be_generated_into_a_selected_material(client):
    admin_headers = sign_in(client)
    material = client.post(
        "/api/admin/learning-materials",
        headers=admin_headers,
        json={
            "topic_id": 2,
            "material_code": "idiomatic-phrases-august",
            "title": "地道英语日积月累【8月】",
            "material_type": "courseware",
        },
    )
    assert material.status_code == 201

    generated = client.post(
        "/api/admin/courseware/from-note-item",
        headers=admin_headers,
        json={"note_item_id": 1, "topic_id": 2, "material_id": material.json()["id"]},
    )

    assert generated.status_code == 201
    assert generated.json()["material_id"] == material.json()["id"]
    course_id = generated.json()["course_id"]
    blocks = client.get(
        f"/api/admin/learning-material-lessons/{generated.json()['lesson_id']}/courseware-blocks",
        headers=admin_headers,
    )
    assert blocks.status_code == 200
    usage = next(item for item in blocks.json()["items"] if item["block_type"] == "usage_group")
    assert usage["payload"]["uses"] == [
        {
            "title": "核心用法",
            "description": "早上好",
            "examples": [{"english": "Good morning", "chinese": "早上好"}],
        }
    ]
    dialogue = next(item for item in blocks.json()["items"] if item["block_type"] == "dialogue")
    assert dialogue["payload"]["scene"] == "真实发生的日常场景"
    assert dialogue["title"] == "真实场景对话"
    assert dialogue["payload"]["lines"][0] == {
        "speaker": "人物 A",
        "english": "Hi, Mrs. Chen. You're up early today.",
        "chinese": "早上好，陈太太。您今天起得真早。",
    }
    assert dialogue["payload"]["lines"][1] == {
        "speaker": "人物 B",
        "english": "Good morning",
        "chinese": "早上好",
    }
    lessons = client.get(
        f"/api/admin/learning-materials/{material.json()['id']}/lessons",
        headers=admin_headers,
    )
    assert lessons.status_code == 200
    assert [item["title"] for item in lessons.json()["items"]] == ["Good morning"]

    changed_access = client.put(
        f"/api/admin/learning/courses/{course_id}",
        headers=admin_headers,
        json={
            "topic_id": 2,
            "material_id": material.json()["id"],
            "course_code": "idiomatic-phrases-august-course",
            "title": "地道英语日积月累【8月】",
            "course_type": "phrase",
            "estimated_minutes": 8,
            "difficulty_code": "elementary",
            "sort_order": 10,
            "access_policy": "benefit",
        },
    )
    assert changed_access.status_code == 200
    assert changed_access.json()["access_policy"] == "benefit"

    rebuilt = client.post(
        "/api/admin/courseware/from-note-item",
        headers=admin_headers,
        json={"note_item_id": 1, "topic_id": 2, "material_id": material.json()["id"]},
    )
    assert rebuilt.status_code == 201
    assert rebuilt.json()["course_id"] == course_id
    assert client.get(
        f"/api/admin/learning-courses?material_id={material.json()['id']}",
        headers=admin_headers,
    ).json()["items"][0]["access_policy"] == "benefit"


def test_note_courseware_generates_one_lesson_for_each_explicit_headword(client):
    admin_headers = sign_in(client)
    note_item = client.post(
        "/api/content/note-items",
        headers=admin_headers,
        json={
            "note_id": 1,
            "item_type": "vocab",
            "item_title": "scraggly / scraggle / straggly",
            "raw_text": "scraggle",
            "english_text": "scraggly / scraggle / straggly",
            "chinese_text": (
                "scraggly = 乱糟糟的；参差不齐的。"
                "scraggle = 变得乱糟糟。"
                "straggly = 更常见的“稀疏杂乱”。"
            ),
            "explanation": "常用于头发、胡子、植物、灌木。",
            "examples": "He has a scraggly beard.\nScraggly bushes grew along the fence.",
            "example_image_url": "/static/uploads/scraggly.webp",
        },
    )
    assert note_item.status_code == 201
    item_id = note_item.json()["id"]
    material = client.post(
        "/api/admin/learning-materials",
        headers=admin_headers,
        json={
            "topic_id": 2,
            "material_code": "split-headwords",
            "title": "拆分词条教材",
            "material_type": "courseware",
        },
    )
    assert material.status_code == 201

    preview = client.post(
        "/api/admin/courseware/note-preview",
        headers=admin_headers,
        json={"note_item_id": item_id},
    )
    assert preview.status_code == 200
    assert preview.json()["split"] is True
    assert [entry["phrase"] for entry in preview.json()["entries"]] == [
        "scraggly", "scraggle", "straggly"
    ]

    generated = client.post(
        "/api/admin/courseware/from-note-item",
        headers=admin_headers,
        json={"note_item_id": item_id, "topic_id": 2, "material_id": material.json()["id"]},
    )
    assert generated.status_code == 201
    result = generated.json()
    assert result["split"] is True
    assert [lesson["phrase"] for lesson in result["lessons"]] == [
        "scraggly", "scraggle", "straggly"
    ]
    assert len({lesson["lesson_id"] for lesson in result["lessons"]}) == 3

    lessons = client.get(
        f"/api/admin/learning-materials/{material.json()['id']}/lessons",
        headers=admin_headers,
    )
    assert lessons.status_code == 200
    assert [lesson["title"] for lesson in lessons.json()["items"]] == [
        "scraggly", "scraggle", "straggly"
    ]
    first_order = note_item.json()["item_order"] * 10
    assert [lesson["sort_order"] for lesson in lessons.json()["items"]] == [
        first_order,
        first_order + 1,
        first_order + 2,
    ]

    for generated_lesson in result["lessons"]:
        blocks = client.get(
            f"/api/admin/learning-material-lessons/{generated_lesson['lesson_id']}/courseware-blocks",
            headers=admin_headers,
        )
        assert blocks.status_code == 200
        assert all(
            source["source_locator"]["kind"] == "split_expression"
            for block in blocks.json()["items"]
            for source in block["sources"]
        )

    rebuilt = client.post(
        "/api/admin/courseware/from-note-item",
        headers=admin_headers,
        json={"note_item_id": item_id, "topic_id": 2, "material_id": material.json()["id"]},
    )
    assert rebuilt.status_code == 201
    assert [lesson["rebuilt"] for lesson in rebuilt.json()["lessons"]] == [True, True, True]
