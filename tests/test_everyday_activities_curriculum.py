from scripts import create_everyday_activities_english as curriculum

from app import schemas as s
from app.services.lesson_content import GenericLessonContentService


def test_everyday_activities_curriculum_uses_concise_scene_first_lessons():
    curriculum.validate_curriculum()

    assert len(curriculum.MATERIALS) == 6
    assert [len(material.lessons) for material in curriculum.MATERIALS] == [
        11,
        8,
        14,
        10,
        9,
        5,
    ]

    for material in curriculum.MATERIALS:
        for lesson in material.lessons:
            payload = s.LearningMaterialLessonInput(
                lesson_code=f"everyday-activities-{material.number}-{lesson.number}",
                title=lesson.title,
                title_en=lesson.title_en,
                lesson_format="structured",
                sections=curriculum.lesson_sections(lesson),
            )
            GenericLessonContentService.validate_sections(
                payload.sections,
                require_complete=True,
            )
            sections = {section.section_code: section for section in payload.sections}
            assert [len(section.items) for section in payload.sections] == [2, 1, 1, 1, 1, 1, 1]

            dialogue = sections["situational_dialogues"].items[0].payload["turns"]
            assert [turn["english"] for turn in dialogue] == [
                lesson.cue,
                lesson.sentence,
                curriculum.natural_follow_up(lesson)[0],
                curriculum.natural_follow_up(lesson)[2],
            ]
            rendered = " ".join(turn["english"] for turn in dialogue)
            assert "repeat the key expression" not in rendered.lower()
            assert "one more time" not in rendered.lower()
