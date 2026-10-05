from scripts import complete_commute_micro_english as curriculum

from app import schemas as s
from app.services.lesson_content import GenericLessonContentService


def test_commute_curriculum_has_complete_unique_micro_lessons():
    curriculum.validate_curriculum()

    assert len(curriculum.CHAPTERS) == 10
    assert [len(chapter.lessons) for chapter in curriculum.CHAPTERS] == [
        7,
        8,
        8,
        8,
        8,
        8,
        8,
        8,
        8,
        8,
    ]

    terms = {
        curriculum.normalise_term(term) for term in curriculum.INITIAL_CORE_TERMS
    }
    total = 1
    for chapter in curriculum.CHAPTERS:
        for lesson in chapter.lessons:
            payload = s.LearningMaterialLessonInput(
                lesson_code=(
                    f"commute-c{lesson.chapter:02d}-l{lesson.number:02d}-{lesson.slug}"
                ),
                title=lesson.title,
                title_en=lesson.title_en,
                summary=lesson.summary,
                illustration_url=curriculum.illustration_url(lesson),
                lesson_format="structured",
                estimated_minutes=4,
                sort_order=lesson.number * 10,
                sections=curriculum.lesson_sections(lesson),
            )
            GenericLessonContentService.validate_sections(
                payload.sections,
                require_complete=True,
            )
            for phrase in lesson.phrases:
                normalised = curriculum.normalise_term(phrase.term)
                assert normalised not in terms
                terms.add(normalised)
                assert phrase.explanation
                assert phrase.reply
                assert phrase.reply_zh
            image = curriculum.illustration_svg(lesson, chapter.art).encode("utf-8")
            assert len(image) < curriculum.MAX_ILLUSTRATION_BYTES
            total += 1

    assert total == 80
    assert len(terms) == 320
