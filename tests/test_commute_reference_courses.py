from scripts import complete_commute_micro_english as main_curriculum
from scripts import create_commute_reference_courses as references


def test_commute_reference_courses_are_complete_unique_and_dialogue_backed():
    references.validate_reference_curriculum()

    assert [course.slug for course in references.REFERENCE_COURSES] == [
        "transit",
        "work",
        "city-services",
    ]
    assert [len(course.lessons) for course in references.REFERENCE_COURSES] == [4, 4, 4]

    main_terms = {
        main_curriculum.normalise_term(term)
        for term in main_curriculum.INITIAL_CORE_TERMS
    }
    main_terms.update(
        main_curriculum.normalise_term(phrase.term)
        for chapter in main_curriculum.CHAPTERS
        for lesson in chapter.lessons
        for phrase in lesson.phrases
    )
    reference_terms = [
        main_curriculum.normalise_term(phrase.term)
        for lesson in references.all_reference_lessons()
        for phrase in lesson.phrases
    ]

    assert len(reference_terms) == 48
    assert len(set(reference_terms)) == 48
    assert not (set(reference_terms) & main_terms)
    assert all(
        main_curriculum.normalise_term(phrase.term)
        in main_curriculum.normalise_term(phrase.reply)
        for lesson in references.all_reference_lessons()
        for phrase in lesson.phrases
    )
