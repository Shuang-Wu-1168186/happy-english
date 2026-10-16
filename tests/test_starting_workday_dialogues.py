from app.curriculum.starting_workday_dialogues import (
    EXPECTED_EXPRESSIONS,
    LESSON_DIALOGUES,
    validate_dialogues,
)


def test_starting_workday_dialogues_are_complete_and_coherent():
    assert validate_dialogues() == []
    assert len(LESSON_DIALOGUES) == 10
    assert sum(len(dialogues) for dialogues in LESSON_DIALOGUES.values()) == 70

    for lesson_code, dialogues in LESSON_DIALOGUES.items():
        assert len(dialogues) == len(EXPECTED_EXPRESSIONS[lesson_code]) == 7
        for scene in dialogues:
            turns = scene["turns"]
            assert len(turns) >= 3
            assert all(turn["english"] and turn["chinese"] for turn in turns)
            assert all(
                earlier["speaker"] != later["speaker"]
                for earlier, later in zip(turns, turns[1:])
            )
