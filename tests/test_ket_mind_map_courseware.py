from scripts import seed_ket_mind_map_courseware as demo

from app import schemas as s
from app.services.learning_catalog import (
    DEFAULT_TEMPLATE_BY_MATERIAL_TYPE,
    MATERIAL_TEMPLATE_DEFINITIONS,
)


def test_ket_family_mind_map_is_a_complete_self_contained_lesson():
    content = demo.mind_map_content()
    demo.validate_mind_map_content(content)

    payload = s.LearningMaterialLessonInput(
        lesson_code=demo.LESSON_CODE,
        title="家庭词汇地图",
        lesson_format="source",
        content=content,
        is_published=1,
    )
    assert payload.content == content
    assert payload.source_resource == ""

    root = content["mind_map"]
    assert root["center"]["label"] == "Family"
    assert "subtitle" not in root
    assert "recall" not in root
    assert all("prompt" not in branch for branch in root["branches"])
    assert [branch["id"] for branch in root["branches"]] == [
        "parents",
        "children",
        "grandparents",
        "relatives",
        "relationships",
    ]
    assert sum(len(branch["leaves"]) for branch in root["branches"]) == 20


def test_ket_food_mind_map_follows_the_food_courseware_branches():
    content = demo.food_mind_map_content()
    demo.validate_mind_map_content(
        content,
        expected_branch_count=4,
        expected_leaf_counts=(6, 6, 6, 3),
    )

    payload = s.LearningMaterialLessonInput(
        lesson_code=demo.FOOD_LESSON_CODE,
        title="食物词汇地图",
        lesson_format="source",
        content=content,
        is_published=1,
    )
    assert payload.content == content
    assert payload.source_resource == ""

    root = content["mind_map"]
    assert root["center"]["label"] == "Food"
    assert "subtitle" not in root
    assert "recall" not in root
    assert all("prompt" not in branch for branch in root["branches"])
    assert [branch["id"] for branch in root["branches"]] == [
        "cereal",
        "fast-food",
        "dinner",
        "snack",
    ]
    assert [len(branch["leaves"]) for branch in root["branches"]] == [6, 6, 6, 3]
    assert sum(len(branch["leaves"]) for branch in root["branches"]) == 21
    assert root["center"]["pronunciation"] == "/fuːd/"
    assert root["center"]["memory_label"] == "音律记忆"

    leaves_by_word = {
        leaf["word"]
        : leaf
        for branch in root["branches"]
        for leaf in branch["leaves"]
    }
    assert leaves_by_word["pizza"]["pronunciation"] == "/ˈpiːtsə/"
    assert leaves_by_word["pizza"]["memory_label"] == "发音记忆"
    assert leaves_by_word["pizza"]["memory_tip"] == "先读长音 /piː/，再清楚带出中间的 /ts/。"
    assert leaves_by_word["cheeseburger"]["memory_label"] == "构词记忆"
    assert leaves_by_word["crop"]["study_notes"] == [
        {
            "type": "collocation",
            "label": "搭配",
            "english": "crop of the year",
            "chinese": "年产量",
        }
    ]
    assert leaves_by_word["sandwich"]["study_notes"][0]["english"] == "sandwiches"
    assert len(leaves_by_word["chip"]["study_notes"]) == 2
    assert root["branches"][1]["study_notes"][0]["english"] == "fast-food restaurants"


def test_mind_map_renderer_contract_is_registered_for_materials():
    definition = MATERIAL_TEMPLATE_DEFINITIONS["mind-map"]

    assert definition["version"] == 1
    assert definition["content_kind"] == "source"
    assert definition["source_resources"] is None
    assert DEFAULT_TEMPLATE_BY_MATERIAL_TYPE["mind_map"] == "mind-map"
