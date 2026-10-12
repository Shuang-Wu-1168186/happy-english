import pytest

from scripts import import_ket_mind_map_vocabulary as importer


def chapter() -> importer.Chapter:
    return importer.Chapter(1, "Food and Drink", "食物和饮料", 11, 15)


def home_chapter() -> importer.Chapter:
    return importer.Chapter(4, "Describing one's Home", "描述某人的家", 25, 31)


def test_parser_keeps_split_pronunciations_and_plain_phrase_cards():
    parsed = importer.parse_page_blocks(
        chapter(),
        11,
        (
            importer.PdfBlock(
                0,
                64.3,
                100,
                220,
                118,
                "record [ˈrekɔːd] 名 唱片;记录",
            ),
            importer.PdfBlock(1, 64.3, 120, 220, 138, "[rɪˈkɔːd] 动 记录;录音"),
            importer.PdfBlock(2, 64.3, 160, 220, 178, "waiting room 候车室"),
            importer.PdfBlock(3, 257.1, 100, 420, 118, "advertisement/ad"),
            importer.PdfBlock(4, 257.1, 120, 420, 138, "[ədˈvɜːtɪsmənt/æd] 名 广告"),
        ),
    )

    by_term = {entry.term: entry for entry in parsed.entries}
    record = by_term["record"]
    assert record.ipa == "/ˈrekɔːd/ · /rɪˈkɔːd/"
    assert record.part_of_speech == "名 / 动"
    assert record.meaning == "唱片;记录；记录;录音"

    waiting_room = by_term["waiting room"]
    assert waiting_room.ipa == ""
    assert waiting_room.meaning == "候车室"
    assert importer.leaf_payload(waiting_room)["pronunciation"] == ""

    assert by_term["advertisement/ad"].ipa == "/ədˈvɜːtɪsmənt/ · /æd/"


def test_pdf_page_lesson_builds_an_interactive_map_without_a_unit_center():
    source = home_chapter()
    entry = importer.VocabularyEntry(
        chapter=source,
        page=25,
        order=1,
        term="home",
        ipa="həʊm",
        part_of_speech="名",
        meaning="家",
        block=importer.PdfBlock(0, 0, 0, 0, 0, "home"),
    )

    content = importer.mind_map_content(source, 25, [entry], 1)
    mind_map = content["mind_map"]
    source_page = mind_map["source"]

    assert source_page["page"] == 25
    assert mind_map["center"]["label"] == "home"
    assert mind_map["diagram"]["style"] == "storybook-branches"
    assert mind_map["diagram"]["presentation"] == "mind-map"
    assert "subtitle" not in mind_map
    assert "recall" not in mind_map
    assert all("prompt" not in branch for branch in mind_map["branches"])


@pytest.mark.skipif(not importer.PDF_PATH.is_file(), reason="KET source PDF is not present")
def test_unit4_rebuilds_home_room_and_description_maps_from_vocabulary_data():
    _, pages = importer.parse_pdf()
    chapter_pages = [page for page in pages if page.chapter.number == 4]
    lessons = importer.course_lesson_entries(chapter_pages)

    assert [
        (lesson.page, lesson.presentation, lesson.title_en, lesson.center_label, len(lesson.entries))
        for lesson in lessons
    ] == [
        (25, "mind-map", "Home", "home", 15),
        (26, "mind-map", "Room", "room", 41),
        (27, "word-list", "Word List · 27", "Describing one's Home", 23),
        (28, "mind-map", "Common Descriptions", "描述词", 11),
        (29, "word-list", "Word List · 29", "Describing one's Home", 11),
    ]

    source_pages = {page.page: page for page in chapter_pages}
    assert source_pages[25].source_has_mind_map
    assert source_pages[25].source_map_title_en == "Home"
    assert not source_pages[27].source_has_mind_map

    room = lessons[1]
    content = importer.mind_map_content(
        chapter_pages[0].chapter,
        room.page,
        list(room.entries),
        2,
        room,
    )
    root = content["mind_map"]
    assert root["center"]["label"] == "room"
    assert [branch["label"] for branch in root["branches"]] == [
        "living room",
        "furniture",
        "kitchen",
        "bedroom",
        "bathroom",
    ]
    assert sum(len(branch["leaves"]) for branch in root["branches"]) == 40

    plain_page = lessons[2]
    plain_content = importer.mind_map_content(
        chapter_pages[0].chapter,
        plain_page.page,
        list(plain_page.entries),
        3,
        plain_page,
    )
    plain_root = plain_content["mind_map"]
    assert plain_root["diagram"]["presentation"] == "word-list"
    assert "subtitle" not in plain_root
    assert "recall" not in plain_root
    assert all("prompt" not in branch for branch in plain_root["branches"])
    assert [word["word"] for word in plain_root["word_list"]] == [
        entry.term for entry in plain_page.entries
    ]


@pytest.mark.skipif(not importer.PDF_PATH.is_file(), reason="KET source PDF is not present")
def test_complete_ket_pdf_source_is_parseable_without_lost_word_column_text():
    chapters, pages = importer.parse_pdf()
    importer.validate_source_data(chapters, pages)

    entries = [entry for page in pages for entry in page.entries]
    by_term = {entry.term: entry for entry in entries}
    assert len(chapters) == 40
    assert len(entries) >= 1_950
    assert sum(page.unassigned_note_count for page in pages) == 0
    assert not [
        block
        for page in pages
        for block in page.orphan_definition_blocks
        if importer.is_word_column(block)
    ]
    assert by_term["playground"].meaning == "操场;游乐场"
    assert by_term["cell phone"].meaning == "(美式英语)手机;移动电话"
    assert by_term["waiting room"].meaning == "候车室"
    assert by_term["ID"].supplements == ["identification(名 身份证明)的缩写形式"]

    pages_by_key = {(page.chapter.number, page.page): page for page in pages}
    # A few pages contain only the printed map artwork. They still need a
    # native map lesson, with the source cards from the following page.
    family_map_page = pages_by_key[(5, 32)]
    assert family_map_page.source_has_mind_map
    assert not family_map_page.entries
    family_lessons = importer.course_lesson_entries(
        [page for page in pages if page.chapter.number == 5]
    )
    family_map = next(lesson for lesson in family_lessons if lesson.page == 32)
    assert family_map.presentation == "mind-map"
    assert family_map.source_pages == (32, 33)
    assert len(family_map.entries) == 34

    assert pages_by_key[(34, 169)].source_map_title_en == "Press"
    assert pages_by_key[(38, 197)].source_map_title_en == "Conjunctions"

    covered_food = importer.curated_word_keys()[1]
    assert importer.is_covered_by_curated_map(by_term["crop"], covered_food)
    assert not importer.is_covered_by_curated_map(by_term["food"], covered_food)
    assert not importer.is_covered_by_curated_map(by_term["cereal"], covered_food)
