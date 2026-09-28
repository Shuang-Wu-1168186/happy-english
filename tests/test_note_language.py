from app.services.note_language import classify_note_item


def classify(**values):
    return classify_note_item(
        {
            "item_type": "phrase",
            "item_title": "Example",
            "raw_text": "Example",
            "english_text": "Example",
            "chinese_text": "示例",
            "explanation": "",
            "examples": "",
            "keywords": "",
            **values,
        }
    )


def test_classifies_explicit_everyday_spoken_language():
    result = classify(
        item_title="gonna",
        english_text="I'm gonna head out.",
        explanation="gonna 是 going to 的口语缩写，很适合日常聊天。",
    )
    assert result.language_register == "common_spoken"
    assert result.usage_scenarios == ["friends_social"]
    assert result.classification_confidence >= 90


def test_classifies_polite_business_language_as_formal_spoken():
    result = classify(
        english_text="Would you mind joining the meeting?",
        explanation="适合礼貌地邀请同事参加会议。",
    )
    assert result.language_register == "formal_spoken"
    assert result.usage_scenarios == ["meeting_presentation", "workplace"]


def test_classifies_formal_writing_language():
    result = classify(
        item_type="vocab",
        item_title="therefore",
        english_text="Therefore, the report needs revision.",
        explanation="therefore 常用于正式写作和报告。",
    )
    assert result.language_register == "written"
    assert result.usage_scenarios == ["report_writing"]


def test_marks_comparisons_between_registers_as_mixed():
    result = classify(
        item_title="enough / sufficient",
        english_text="We have enough time.",
        explanation="enough 更自然、更口语；sufficient 更正式、更书面。",
    )
    assert result.language_register == "mixed"


def test_keeps_isolated_technical_vocabulary_as_reference():
    result = classify(
        item_type="vocab",
        item_title="methodology",
        explanation="研究与技术语境中的专业术语。",
    )
    assert result.language_register == "reference"
    assert result.usage_scenarios == ["academic", "technical"]
