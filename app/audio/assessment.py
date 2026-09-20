"""Pure transcript-comparison helpers shared by both HTTP applications."""

import re
from difflib import SequenceMatcher


def normalise_assessment_text(text: str) -> str:
    """
    Normalise English text before comparing
    the reference and transcript.
    """

    text = (text or "").lower()

    text = text.replace("’", "").replace("'", "")

    return re.sub(
        r"[^a-z0-9\s]",
        " ",
        text,
    ).strip()


def word_edit_distance(
    left_words,
    right_words,
) -> int:
    previous = list(range(len(right_words) + 1))

    for left_index, left_word in enumerate(
        left_words,
        start=1,
    ):
        current = [left_index]

        for right_index, right_word in enumerate(
            right_words,
            start=1,
        ):
            substitution_cost = 0 if left_word == right_word else 1

            current.append(
                min(
                    current[right_index - 1] + 1,
                    previous[right_index] + 1,
                    previous[right_index - 1] + substitution_cost,
                )
            )

        previous = current

    return previous[-1]


def calculate_assessment_score(
    reference_text: str,
    transcript: str,
) -> int:
    """
    Return a forgiving 0-100 transcript similarity score.
    """

    reference = normalise_assessment_text(reference_text)

    spoken = normalise_assessment_text(transcript)

    if not reference or not spoken:
        return 0

    reference_words = reference.split()
    spoken_words = spoken.split()

    word_scale = max(
        len(reference_words),
        len(spoken_words),
    )

    word_score = (
        1
        - word_edit_distance(
            reference_words,
            spoken_words,
        )
        / word_scale
    )

    character_score = SequenceMatcher(
        None,
        reference,
        spoken,
    ).ratio()

    score = (word_score * 0.7 + character_score * 0.3) * 100

    return max(
        0,
        min(
            100,
            round(score),
        ),
    )
