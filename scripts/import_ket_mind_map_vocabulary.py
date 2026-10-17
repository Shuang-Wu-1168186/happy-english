"""Import the complete KET mind-map vocabulary PDF into the learning catalogue.

The source PDF has a consistent vocabulary-card layout: an English term,
IPA, part of speech, Chinese meaning, and optional study notes such as
collocations, inflections, word formation, and memory cues.  This importer
keeps that source structure in two existing places:

* ``vocabulary_library`` remains the reusable, searchable vocabulary source.
* ``learning_material_lesson.content_json`` stores the client-neutral
  ``mind-map.v1`` lesson payload used by both the web app and mini program.

It is safe to run repeatedly.  Imported vocabulary rows carry a stable source
marker in ``extra_note`` and course records use stable catalogue codes.

Run with:

    PYTHONPATH=. .venv/bin/python scripts/import_ket_mind_map_vocabulary.py
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field, replace
from pathlib import Path

from sqlalchemy import func, select, update
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
PDF_PATH = Path(__file__).resolve().parents[1] / "lecture" / "用思维导图速记KET词汇1000单词.pdf"
VOCABULARY_CATEGORY_PREFIX = "KET 思维导图"
SOURCE_MARKER_PREFIX = "[ket-mind-map-pdf:"

ENTRY_RE = re.compile(
    r"^(?P<term>[A-Za-z][A-Za-z .()'’/-]*?)\s*\[(?P<ipa>[^\]\n]+)\]\s*(?P<definition>.*)$"
)
IPA_CONTINUATION_RE = re.compile(r"^\[(?P<ipa>[^\]\n]+)\]\s*(?P<definition>.*)$")
TERM_ONLY_RE = re.compile(r"^[A-Za-z][A-Za-z .()'’/-]*$")
NO_IPA_ENTRY_RE = re.compile(
    r"^(?P<term>[A-Za-z][A-Za-z .()'’/-]*?)\s+(?P<definition>[\u4e00-\u9fff].*)$"
)
NOTE_RE = re.compile(
    r"^(?P<prefix>搭|复|过|派|反|近|同|比|现|三单|合成词|发音记忆|音律记忆|联想记忆)\s*(?P<body>.*)$"
)
POS_RE = re.compile(
    r"^(?P<part>序数|系动词|名|动|形|副|介|连|代|数|情|冠|助|缩)"
    r"(?:\s*/\s*(?:序数|系动词|名|动|形|副|介|连|代|数|情|冠|助|缩))*\s*(?P<meaning>.*)$"
)

MEMORY_PREFIXES = {"合成词", "发音记忆", "音律记忆", "联想记忆"}
RELATION_PREFIXES = {"复", "过", "派", "反", "近", "同", "比", "现", "三单"}
NOTE_LABELS = {
    "搭": ("collocation", "搭配"),
    "复": ("plural", "复数"),
    "过": ("past_tense", "过去式"),
    "派": ("derived", "派生"),
    "反": ("opposite", "反义"),
    "近": ("similar", "近义"),
    "同": ("synonym", "同义"),
    "比": ("comparison", "比较级"),
    "现": ("present_participle", "现在分词"),
    "三单": ("third_person_singular", "三单"),
}
MEMORY_LABELS = {
    "合成词": "构词记忆",
    "发音记忆": "发音记忆",
    "音律记忆": "音律记忆",
    "联想记忆": "联想记忆",
}
IRREGULAR_FORMS = {
    "bad": {"worse", "worst"},
    "be": {"was", "were", "been", "being"},
    "break": {"broke", "broken"},
    "catch": {"caught"},
    "choose": {"chose", "chosen", "choosing"},
    "do": {"did", "done", "doing"},
    "fall": {"fell", "fallen", "falling"},
    "feel": {"felt"},
    "get": {"got", "gotten", "getting"},
    "go": {"went", "gone", "going"},
    "hang": {"hung", "hanging"},
    "have": {"had", "having"},
    "lie": {"lay", "lied", "lying"},
    "make": {"made", "making"},
    "prefer": {"preferred", "preferring"},
    "shine": {"shone", "shined", "shining"},
    "sit": {"sat", "sitting"},
    "spit": {"spat", "spitting"},
    "swim": {"swam", "swum", "swimming"},
    "long": {"length"},
    "nice": {"nicer", "nicest"},
    "noisy": {"noisily"},
    "coast": {"coastal"},
}
BRANCH_DEFINITIONS = (
    ("noun", "Nouns", "名词", "📦", "violet"),
    ("verb", "Verbs", "动词", "🏃", "rose"),
    ("adjective", "Adjectives", "形容词", "🎨", "sun"),
    ("adverb", "Adverbs", "副词", "🧭", "sky"),
    ("function", "Function Words", "其他词性", "🔗", "mint"),
)
CHAPTER_EMOJIS = (
    "🍽️",
    "🍎",
    "🍳",
    "🏠",
    "👪",
    "🤝",
    "🔌",
    "🧴",
    "👕",
    "🎨",
    "🫀",
    "🩺",
    "⚽",
    "🙂",
    "💭",
    "💬",
    "🎸",
    "🎭",
    "💼",
    "💻",
    "🎓",
    "📝",
    "🌍",
    "🏔️",
    "🌦️",
    "🍂",
    "🐾",
    "🌿",
    "🏙️",
    "🌾",
    "🛍️",
    "🧳",
    "🚌",
    "🎬",
    "🔢",
    "🕒",
    "🏃",
    "📍",
    "⚡",
    "❗",
)

# These notes are printed at a different point in the visual mind map than
# their word cards.  The page + label pair is unique in this source PDF, so a
# small explicit map is safer than a nearest-neighbour guess (which can attach
# a note to an unrelated word in the other column).
MANUAL_NOTE_TARGETS = {
    (9, 50, "合成词"): "handkerchief",
    (11, 57, "反"): "bad",
    (12, 59, "派"): "harm",
    (12, 61, "合成词"): "drugstore",
    (12, 62, "派"): "use",
    (14, 71, "反"): "polite",
    (18, 91, "反"): "war",
    (19, 98, "复"): "businessman",
    (20, 106, "合成词"): "online",
    (21, 108, "合成词"): "playground",
    (21, 110, "过"): "clip",
    (22, 113, "合成词"): "schoolchild",
    (22, 115, "合成词"): "homework",
    (29, 142, "合成词"): "guest-house",
    (29, 144, "反"): "bottom",
    (29, 144, "联想记忆"): "along",
    (31, 151, "近"): "advertisement/ad",
    (32, 159, "合成词"): "postcard",
    (33, 164, "近"): "underground",
    (37, 189, "过"): "drop",
}

TERM_PRONUNCIATION_OVERRIDES = {
    # The source prints both short forms inside one IPA pair:
    # [ədˈvɜːtɪsmənt/æd].  Split them for the learner-facing renderer.
    "advertisement/ad": "/ədˈvɜːtɪsmənt/ · /æd/",
}

# Most map labels are available as PDF text immediately above their artwork.
# These two labels live inside the raster illustration, so preserve their
# verified source wording instead of falling back to the broader chapter name.
SOURCE_MAP_TITLE_OVERRIDES = {
    (34, 169): ("Press", "报刊"),
    (38, 197): ("Conjunctions", "连词"),
}


@dataclass(frozen=True)
class Chapter:
    """One numbered source chapter from the PDF table of contents."""

    number: int
    title_en: str
    title_zh: str
    start_page: int
    end_page: int


@dataclass(frozen=True)
class PdfBlock:
    """Text and geometry for one PDF text block."""

    index: int
    x0: float
    y0: float
    x1: float
    y1: float
    text: str


@dataclass
class SourceNote:
    """An optional source-study note attached to a vocabulary entry."""

    prefix: str
    body: str
    block: PdfBlock
    block_indexes: list[int] = field(default_factory=list)


@dataclass
class VocabularyEntry:
    """One parsed source card and its optional annotations."""

    chapter: Chapter
    page: int
    order: int
    term: str
    ipa: str
    part_of_speech: str
    meaning: str
    block: PdfBlock
    notes: list[SourceNote] = field(default_factory=list)
    block_indexes: list[int] = field(default_factory=list)
    supplements: list[str] = field(default_factory=list)

    @property
    def source_key(self) -> str:
        return (
            f"ket-mind-map-pdf:{self.chapter.number:02d}:{self.page:03d}:"
            f"{slugify(self.term)}:{self.order:02d}"
        )


@dataclass(frozen=True)
class ParsedPage:
    """All source entries collected from one physical PDF page."""

    chapter: Chapter
    page: int
    entries: tuple[VocabularyEntry, ...]
    note_count: int
    unassigned_note_count: int
    unassigned_notes: tuple[SourceNote, ...] = ()
    orphan_definition_blocks: tuple[PdfBlock, ...] = ()
    # The source book alternates between illustrated mind maps and ordinary
    # two-column word pages.  Keep that distinction with the parsed page so
    # the client never has to pretend that a word list is a diagram.
    source_has_mind_map: bool = False
    source_map_title_en: str = ""
    source_map_title_zh: str = ""


@dataclass(frozen=True)
class MapBranchSpec:
    """One coloured arm in a hand-drawn learner-facing map."""

    id: str
    label: str
    label_zh: str
    emoji: str
    tone: str
    position: str
    terms: tuple[str, ...]


@dataclass(frozen=True)
class MapLessonSpec:
    """A map reconstructed from the source vocabulary, never from page art."""

    id: str
    page: int
    source_pages: tuple[int, ...]
    title_en: str
    title_zh: str
    center_label: str
    center_zh: str
    center_emoji: str
    terms: tuple[str, ...]
    branches: tuple[MapBranchSpec, ...]


@dataclass(frozen=True)
class ImportedMapLesson:
    """The vocabulary and presentation metadata for one generated map lesson."""

    page: int
    source_pages: tuple[int, ...]
    title_en: str
    title_zh: str
    center_label: str
    center_zh: str
    center_emoji: str
    entries: tuple[VocabularyEntry, ...]
    presentation: str = "mind-map"
    branches: tuple[MapBranchSpec, ...] = ()


# Unit 04 contains three diagrams whose definitions continue across following
# pages.  Keep the words in the same semantic arms as the printed maps, but
# draw the result with client-native shapes and text instead of embedding a
# rasterized PDF page.
UNIT4_MAP_SPECS = (
    MapLessonSpec(
        id="home",
        page=25,
        source_pages=(25, 26),
        title_en="Home",
        title_zh="家",
        center_label="home",
        center_zh="家",
        center_emoji="🏠",
        terms=(
            "home",
            "house",
            "apartment",
            "address",
            "flat",
            "space",
            "live",
            "garden",
            "entrance",
            "gate",
            "door",
            "lawn",
            "garage",
            "lock",
            "basement",
        ),
        branches=(
            MapBranchSpec(
                "entrance", "entrance", "入口", "🚪", "rose", "northwest",
                ("entrance", "gate", "door", "lock", "garage", "basement"),
            ),
            MapBranchSpec(
                "garden", "garden", "花园", "🌳", "sun", "southwest",
                ("garden", "lawn"),
            ),
            MapBranchSpec(
                "house", "house", "房屋", "🏘️", "violet", "northeast",
                ("house", "address", "space"),
            ),
            MapBranchSpec(
                "live", "live", "居住", "🏢", "mint", "southeast",
                ("live", "apartment", "flat"),
            ),
        ),
    ),
    MapLessonSpec(
        id="room",
        page=26,
        source_pages=(26, 27, 28),
        title_en="Room",
        title_zh="房间",
        center_label="room",
        center_zh="房间",
        center_emoji="🛋️",
        terms=(
            "room",
            "window",
            "living room",
            "curtain",
            "sitting room",
            "wall",
            "hall",
            "furniture",
            "bed",
            "sheet",
            "sofa",
            "armchair",
            "pillow",
            "blanket",
            "carpet",
            "wardrobe",
            "desk",
            "kitchen",
            "bookcase",
            "chimney",
            "closet",
            "cupboard",
            "bookshelf",
            "shelf",
            "dining-room",
            "cabinet",
            "table",
            "bedroom",
            "drawer",
            "chair",
            "bathroom",
            "toilet",
            "basin",
            "bath",
            "stair",
            "floor",
            "shower",
            "balcony",
            "washroom",
            "roof",
            "ceiling",
        ),
        branches=(
            MapBranchSpec(
                "living", "living room", "起居空间", "🪟", "sun", "northwest",
                ("living room", "sitting room", "hall", "wall", "window", "curtain"),
            ),
            MapBranchSpec(
                "furniture", "furniture", "家具", "🪑", "rose", "northeast",
                ("furniture", "sofa", "armchair", "desk", "bookcase", "bookshelf", "shelf", "cabinet", "table", "chair", "drawer"),
            ),
            MapBranchSpec(
                "kitchen", "kitchen", "厨房", "🍽️", "violet", "east",
                ("kitchen", "chimney", "closet", "cupboard", "dining-room"),
            ),
            MapBranchSpec(
                "bedroom", "bedroom", "卧室", "🛏️", "rose", "southwest",
                ("bedroom", "bed", "sheet", "pillow", "blanket", "carpet", "wardrobe"),
            ),
            MapBranchSpec(
                "utility", "bathroom", "卫浴与楼层", "🚿", "sky", "southeast",
                ("bathroom", "bath", "shower", "toilet", "basin", "washroom", "stair", "floor", "balcony", "roof", "ceiling"),
            ),
        ),
    ),
    MapLessonSpec(
        id="descriptions",
        page=28,
        source_pages=(28, 29),
        title_en="Common Descriptions",
        title_zh="常用描述词",
        center_label="描述词",
        center_zh="房间位置与状态",
        center_emoji="🏡",
        terms=(
            "upstairs",
            "inside",
            "outside",
            "downstairs",
            "tidy",
            "untidy",
            "indoor",
            "mess",
            "outdoor",
            "neat",
            "outdoors",
        ),
        branches=(
            MapBranchSpec(
                "levels", "upstairs", "楼层方向", "🪜", "rose", "northwest",
                ("upstairs", "downstairs"),
            ),
            MapBranchSpec(
                "place", "inside", "室内外位置", "🧭", "sky", "northeast",
                ("inside", "outside", "indoor", "outdoor", "outdoors"),
            ),
            MapBranchSpec(
                "order", "tidy", "整洁状态", "🧺", "mint", "south",
                ("tidy", "untidy", "neat", "mess"),
            ),
        ),
    ),
)


@dataclass(frozen=True)
class DetachedTextTarget:
    """One known source fragment whose visual position is detached from its card."""

    term: str
    kind: str
    value: str
    part_of_speech: str | None = None
    note_prefix: str | None = None


# The PDF's mind-map artwork occasionally places a continuation at the top of
# another branch or page.  These entries are source-verified full values, not
# generated translations.  Keeping the mapping explicit prevents a spatial
# parser from attaching a fragment to a nearby but unrelated card.
MANUAL_DETACHED_TEXT_TARGETS = {
    (9, 47, 4): DetachedTextTarget("clothing", "meaning", "(尤指某种)服装"),
    (
        12,
        59,
        0,
    ): DetachedTextTarget("spit", "meaning", "吐(唾沫、食物等);怒斥 名 唾沫;吐痰", "动 / 名"),
    (12, 61, 0): DetachedTextTarget("drugstore", "meaning", "(美式英语)药店"),
    (13, 65, 0): DetachedTextTarget("surf", "meaning", "冲浪;(互联网上的)冲浪"),
    (13, 64, 50): DetachedTextTarget(
        "baseball",
        "note",
        "base(垒)+ball(球)→涉及“一垒、二垒”的球类运动就是baseball(棒球)",
        note_prefix="合成词",
    ),
    (15, 78, 6): DetachedTextTarget("excellent", "meaning", "极好的;优秀的"),
    (16, 83, 0): DetachedTextTarget("fast", "meaning", "快速的;敏捷的 副 快速;快", "形 / 副"),
    (18, 91, 0): DetachedTextTarget(
        "role",
        "note",
        "leading role 主角 play a role in 起作用;在......中扮演角色",
        note_prefix="搭",
    ),
    (20, 103, 0): DetachedTextTarget("cell phone", "meaning", "(美式英语)手机;移动电话"),
    (21, 108, 1): DetachedTextTarget("playground", "meaning", "操场;游乐场"),
    (21, 110, 0): DetachedTextTarget("clip", "meaning", "回形针;片段;修剪 动 夹住;修剪", "名 / 动"),
    (
        23,
        121,
        3,
    ): DetachedTextTarget("Japanese", "meaning", "日本人;日语 形 日本人的;日本的", "名 / 形"),
    (28, 139, 0): DetachedTextTarget(
        "wood",
        "note",
        "woody(形 树木茂密的) wooden(形 木制的)",
        note_prefix="派",
    ),
    (34, 171, 7): DetachedTextTarget(
        "ID", "supplement", "identification(名 身份证明)的缩写形式"
    ),
    (37, 193, 0): DetachedTextTarget("trick", "meaning", "花招;诡计;恶作剧 动 欺骗;戏弄", "名 / 动"),
}


def normalise_text(value: str) -> str:
    """Remove PDF extraction artefacts while retaining learner-facing text."""

    normalised = unicodedata.normalize("NFKC", value).replace("\x08", "").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", normalised).strip()


def slugify(value: str) -> str:
    """Produce a stable ASCII fragment for a catalogue/source key."""

    compact = normalise_text(value).lower().replace("’", "'")
    compact = re.sub(r"[^a-z0-9]+", "-", compact).strip("-")
    return compact or "word"


def pronunciation_of(ipa: str) -> str:
    compact = normalise_text(ipa)
    return compact if compact.startswith("/") else f"/{compact}/"


def pronunciation_for(term: str, ipa: str) -> str:
    """Return a displayable IPA string, preserving verified source variants."""

    override = TERM_PRONUNCIATION_OVERRIDES.get(normalise_text(term).lower())
    return override or pronunciation_of(ipa)


def row_id(db: Session, table, column, value: str) -> int | None:
    return db.execute(select(table.c.id).where(column == value)).scalar_one_or_none()


def chapter_category(chapter: Chapter) -> str:
    return f"{VOCABULARY_CATEGORY_PREFIX} · {chapter.number:02d} {chapter.title_en}"


def extract_chapters(toc: list[tuple]) -> tuple[Chapter, ...]:
    """Read the forty numbered source chapters from the PDF TOC."""

    raw_chapters: list[tuple[int, str, str, int]] = []
    for entry in toc:
        level, title, page = entry[:3]
        if level != 1:
            continue
        match = re.match(r"^(?P<number>\d{2})\s+(?P<title>.+)$", normalise_text(title))
        if not match:
            continue
        number = int(match.group("number"))
        if number < 1 or number > 40:
            continue
        title_text = match.group("title")
        chinese_start = re.search(r"[\u4e00-\u9fff]", title_text)
        if not chinese_start:
            raise ValueError(f"Missing Chinese title in chapter TOC entry: {title}")
        title_en = title_text[: chinese_start.start()].strip()
        title_zh = title_text[chinese_start.start() :].strip()
        raw_chapters.append((number, title_en, title_zh, int(page)))

    if len(raw_chapters) != 40:
        raise ValueError(f"Expected 40 KET chapters in the PDF TOC, got {len(raw_chapters)}.")

    chapters = []
    for index, (number, title_en, title_zh, start_page) in enumerate(raw_chapters):
        end_page = raw_chapters[index + 1][3] - 1 if index + 1 < len(raw_chapters) else 205
        chapters.append(Chapter(number, title_en, title_zh, start_page, end_page))
    return tuple(chapters)


def pdf_blocks(page) -> tuple[PdfBlock, ...]:
    """Return non-empty source text blocks without flattening their layout."""

    result = []
    for index, raw in enumerate(page.get_text("blocks", sort=False)):
        text = normalise_text(str(raw[4]))
        if text:
            result.append(PdfBlock(index, float(raw[0]), float(raw[1]), float(raw[2]), float(raw[3]), text))
    return tuple(result)


def source_mind_map_bounds(page) -> tuple[float, float, float, float] | None:
    """Locate the full-width illustration used for a printed mind map.

    The book stores each illustrated map as one wide raster image.  Ordinary
    vocabulary pages also contain small decorative pictures, so require both
    a large source image and a wide placement on the page.  This uses only
    source layout metadata; no PDF image is exposed to the learner.
    """

    for image in page.get_image_info(xrefs=True):
        bbox = image.get("bbox")
        if not isinstance(bbox, (tuple, list)) or len(bbox) != 4:
            continue
        x0, y0, x1, y1 = (float(value) for value in bbox)
        image_width = float(image.get("width") or 0)
        if image_width >= 600 and x1 - x0 >= 300:
            return (x0, y0, x1, y1)
    return None


def source_map_title(blocks: tuple[PdfBlock, ...], bounds: tuple[float, float, float, float]) -> str:
    """Read the short printed title immediately above a map illustration."""

    left, top, right, _ = bounds
    map_center = (left + right) / 2
    candidates = []
    for block in blocks:
        if not top - 90 <= block.y1 <= top + 6:
            continue
        # Vocabulary cards are laid out in two columns. A map heading is
        # centered, so this keeps a wrapped card definition from becoming the
        # map's title when the actual heading is baked into the illustration.
        if abs(((block.x0 + block.x1) / 2) - map_center) > 58:
            continue
        if entry_match(block) or no_ipa_entry_match(block) or NOTE_RE.fullmatch(block.text):
            continue
        if is_ignorable_block(block.text):
            continue
        candidates.append(block)
    if not candidates:
        return ""
    # The map label is the last text block before the illustration.  This
    # also skips the larger chapter heading printed near the top of the page.
    return normalise_text(max(candidates, key=lambda block: (block.y1, block.x1 - block.x0)).text)


def split_source_map_title(title: str, chapter: Chapter) -> tuple[str, str]:
    """Split source labels such as ``甜品饮料Dessert & Drink`` for the UI."""

    value = normalise_text(title).strip()
    if not value:
        return chapter.title_en, chapter.title_zh

    first_latin = re.search(r"[A-Za-z]", value)
    if first_latin and first_latin.start() > 0:
        chinese = value[: first_latin.start()].strip(" ·—-:：")
        english = value[first_latin.start() :].strip(" ·—-:：")
        # ``动词(A-E)`` is a single Chinese map label with a letter range,
        # rather than a translated Chinese/English pair.
        if chinese.endswith("(") and re.fullmatch(r"[A-Z]-[A-Z]\)?", english):
            return value, ""
        if chinese and re.search(r"[\u4e00-\u9fff]", chinese):
            return english or chinese, chinese

    first_chinese = re.search(r"[\u4e00-\u9fff]", value)
    if first_chinese and first_chinese.start() > 0:
        english = value[: first_chinese.start()].strip(" ·—-:：")
        chinese = value[first_chinese.start() :].strip(" ·—-:：")
        if english:
            return english, chinese

    # Several printed labels are Chinese-only.  Put the source wording in
    # the prominent position once rather than repeating it as a translation.
    return value, ""


def entry_match(block: PdfBlock):
    return ENTRY_RE.fullmatch(block.text)


def no_ipa_entry_match(block: PdfBlock):
    """Recognise source cards printed without an IPA line."""

    return NO_IPA_ENTRY_RE.fullmatch(block.text)


def is_ignorable_block(text: str) -> bool:
    """Skip titles, page numbers, promotion text, and workbook prompts."""

    if not text:
        return True
    if re.fullmatch(r"\d{1,3}", text):
        return True
    if "海量学习资源" in text or "deanna121" in text:
        return True
    return text.startswith(("练 习", "练习", "拿起手中的笔", "把单词填", "将单词", "读句子"))


def is_continuation_text(text: str) -> bool:
    """Recognise a wrapped Chinese definition while excluding a new source card."""

    if (
        is_ignorable_block(text)
        or NOTE_RE.fullmatch(text)
        or ENTRY_RE.fullmatch(text)
        or NO_IPA_ENTRY_RE.fullmatch(text)
    ):
        return False
    return bool(re.match(r"^(?:[名动形副介连代数序情冠助缩]|[（(]|[\u4e00-\u9fff])", text))


def same_column(left: PdfBlock, right: PdfBlock) -> bool:
    return abs(left.x0 - right.x0) <= 24


def is_word_column(block: PdfBlock) -> bool:
    """Return whether a block starts in one of the PDF's two word columns."""

    return any(abs(block.x0 - column) <= 8 for column in (64.3, 257.1))


def continuation_for(
    entry: VocabularyEntry,
    blocks: tuple[PdfBlock, ...],
    occupied_indexes: set[int],
    entry_indexes: set[int],
) -> list[PdfBlock]:
    """Collect directly-below wrapped definition blocks from the same column."""

    parts: list[PdfBlock] = []
    last_y = entry.block.y1
    for block in sorted(blocks, key=lambda item: (item.y0, item.x0, item.index)):
        if not same_column(entry.block, block):
            continue
        if block.index in entry_indexes:
            if block.index != entry.block.index and block.y0 >= last_y - 0.5:
                # Do not let a definition line below the next source card be
                # captured by the previous card in the same visual column.
                break
            continue
        if block.index in occupied_indexes:
            continue
        vertical_gap = block.y0 - last_y
        if vertical_gap < -0.5:
            continue
        if vertical_gap > 34:
            break
        if not is_continuation_text(block.text):
            break
        parts.append(block)
        occupied_indexes.add(block.index)
        last_y = block.y1
    return parts


def split_definition(value: str) -> tuple[str, str]:
    """Separate the compact Chinese part-of-speech prefix from its meaning."""

    compact = normalise_text(value)
    match = POS_RE.match(compact)
    if not match:
        return "", compact
    return normalise_text(match.group("part")), normalise_text(match.group("meaning"))


def term_variants(term: str) -> tuple[str, ...]:
    """Return searchable spelling variants for source-note association."""

    lower = normalise_text(term).lower().replace("’", "'")
    without_parentheses = re.sub(r"\([^)]*\)", "", lower)
    without_slashes = re.sub(r"\s*/\s*", " ", without_parentheses)
    variants = {lower, without_parentheses, without_slashes}
    return tuple(value.strip() for value in variants if len(value.strip()) >= 3)


def source_forms(term: str) -> tuple[tuple[str, int], ...]:
    """Return source-note spellings, including common inflections/derivations."""

    variants = [(variant, 3) for variant in term_variants(term)]
    if " " in term or "/" in term:
        return tuple(variants)
    base = normalise_text(term).lower().replace("’", "'")
    if len(base) < 3 or not re.fullmatch(r"[a-z-]+", base):
        return tuple(variants)

    derived = {f"{base}s", f"{base}es", f"{base}er", f"{base}ly", f"{base}ness"}
    if base.endswith("e"):
        derived.add(f"{base[:-1]}ing")
        derived.add(f"{base}d")
        derived.update({f"{base[:-1]}er", f"{base[:-1]}est"})
    else:
        derived.update({f"{base}ing", f"{base}ed", f"{base}er", f"{base}est"})
    if base.endswith("y") and len(base) > 3:
        derived.update(
            {
                f"{base[:-1]}ies",
                f"{base[:-1]}ied",
                f"{base[:-1]}ier",
                f"{base[:-1]}iest",
                f"{base[:-1]}ily",
            }
        )
    if base.endswith("fe"):
        derived.add(f"{base[:-2]}ves")
    elif base.endswith("f"):
        derived.add(f"{base[:-1]}ves")
    derived.update(IRREGULAR_FORMS.get(base, set()))
    variants.extend((form, 2) for form in derived if len(form) >= 3)
    return tuple(variants)


def text_contains_term(text: str, term: str) -> bool:
    return bool(re.search(rf"(?<![a-z]){re.escape(term)}(?![a-z])", text))


def note_target(note: SourceNote, entries: list[VocabularyEntry]) -> VocabularyEntry | None:
    """Associate an annotation with its source word despite two-column layouts."""

    same_column_previous = [
        entry
        for entry in entries
        if same_column(entry.block, note.block) and entry.block.y1 <= note.block.y0
    ]
    previous = max(same_column_previous, key=lambda entry: entry.block.y1, default=None)
    previous_gap = note.block.y0 - previous.block.y1 if previous is not None else float("inf")

    # Inflections and lexical relationships nearly always describe the card
    # immediately above them.  Prefer that spatial relationship to a related
    # word mentioned in the annotation (for example, "反 inside").
    if note.prefix in RELATION_PREFIXES and previous is not None and previous_gap <= 86:
        return previous

    haystack = note.body.lower().replace("’", "'")
    matches: list[tuple[int, float, VocabularyEntry]] = []
    for entry in entries:
        for variant, strength in source_forms(entry.term):
            if text_contains_term(haystack, variant):
                distance = abs(entry.block.y0 - note.block.y0) + abs(entry.block.x0 - note.block.x0)
                matches.append((strength * 100 + len(variant), distance, entry))
                break
    if matches:
        # The longest word wins for compounds such as cheeseburger; geometry
        # breaks ties for repeated short words.
        return max(matches, key=lambda value: (value[0], -value[1]))[2]
    if previous is not None and previous_gap <= 120:
        return previous
    return None


def chapter_note_target(
    note: SourceNote,
    source_page: int,
    entries: list[VocabularyEntry],
) -> VocabularyEntry | None:
    """Resolve a note whose word card flows across a page/column boundary."""

    haystack = note.body.lower().replace("’", "'")
    matches: list[tuple[int, int, float, VocabularyEntry]] = []
    for entry in entries:
        for variant, strength in source_forms(entry.term):
            if not text_contains_term(haystack, variant):
                continue
            page_distance = abs(entry.page - source_page)
            geometry = abs(entry.block.y0 - note.block.y0) + abs(entry.block.x0 - note.block.x0)
            matches.append((strength * 100 + len(variant), page_distance, geometry, entry))
            break
    if matches:
        return max(matches, key=lambda value: (value[0], -value[1], -value[2]))[3]

    return None


def manual_note_target(
    note: SourceNote,
    chapter_number: int,
    page_number: int,
    entries: list[VocabularyEntry],
) -> VocabularyEntry | None:
    """Resolve the few source notes intentionally separated from their card."""

    target_term = MANUAL_NOTE_TARGETS.get((chapter_number, page_number, note.prefix))
    if target_term is None:
        return None
    matches = [
        entry
        for entry in entries
        if normalise_text(entry.term).lower() == normalise_text(target_term).lower()
    ]
    if len(matches) != 1:
        raise ValueError(
            "Manual KET note target is missing or ambiguous: "
            f"chapter {chapter_number}, page {page_number}, {note.prefix} -> {target_term}"
        )
    return matches[0]


def attach_chapter_notes(pages: tuple[ParsedPage, ...]) -> tuple[ParsedPage, ...]:
    """Attach annotations split from their cards by the PDF's two-column flow."""

    entries = [entry for page in pages for entry in page.entries]
    assigned_targets: dict[int, VocabularyEntry] = {}
    remaining_by_page: dict[int, list[SourceNote]] = {}
    for page in pages:
        remaining = []
        for note in page.unassigned_notes:
            target = manual_note_target(note, page.chapter.number, page.page, entries)
            if target is None:
                target = chapter_note_target(note, page.page, entries)
            if target is None:
                remaining.append(note)
            else:
                target.notes.append(note)
                assigned_targets[id(note)] = target
        remaining_by_page[page.page] = remaining

    # A memory label sometimes appears immediately before the collocation
    # that names its word.  Once the latter resolves, keep the nearby label
    # with that same card instead of discarding the source memory cue.
    for page in pages:
        still_unassigned = []
        all_page_notes = list(page.unassigned_notes)
        for note in remaining_by_page[page.page]:
            companions = [
                candidate
                for candidate in all_page_notes
                if id(candidate) in assigned_targets
                and same_column(candidate.block, note.block)
                and abs(candidate.block.y0 - note.block.y0) <= 70
            ]
            if companions:
                companion = min(companions, key=lambda candidate: abs(candidate.block.y0 - note.block.y0))
                target = assigned_targets[id(companion)]
                target.notes.append(note)
                assigned_targets[id(note)] = target
            else:
                still_unassigned.append(note)
        remaining_by_page[page.page] = still_unassigned

    return tuple(
        ParsedPage(
            page.chapter,
            page.page,
            page.entries,
            page.note_count,
            len(remaining_by_page[page.page]),
            tuple(remaining_by_page[page.page]),
            page.orphan_definition_blocks,
            page.source_has_mind_map,
            page.source_map_title_en,
            page.source_map_title_zh,
        )
        for page in pages
    )


def detached_text_target_entry(
    entries: list[VocabularyEntry],
    target: DetachedTextTarget,
    source_key: tuple[int, int, int],
) -> VocabularyEntry:
    """Locate the one card named by a verified detached-text mapping."""

    matches = [
        entry
        for entry in entries
        if normalise_text(entry.term).lower() == normalise_text(target.term).lower()
    ]
    if len(matches) != 1:
        raise ValueError(f"Detached KET source text target is missing or ambiguous: {source_key}")
    return matches[0]


def apply_detached_source_text(pages: tuple[ParsedPage, ...]) -> tuple[ParsedPage, ...]:
    """Merge source fragments printed away from their word card in the PDF."""

    entries = [entry for page in pages for entry in page.entries]
    resolved_keys: set[tuple[int, int, int]] = set()
    retained_pages = []
    for page in pages:
        retained_orphans = []
        for block in page.orphan_definition_blocks:
            source_key = (page.chapter.number, page.page, block.index)
            target = MANUAL_DETACHED_TEXT_TARGETS.get(source_key)
            if target is None:
                retained_orphans.append(block)
                continue
            entry = detached_text_target_entry(entries, target, source_key)
            if target.kind == "meaning":
                entry.meaning = target.value
                if target.part_of_speech:
                    entry.part_of_speech = target.part_of_speech
            elif target.kind == "note":
                notes = [note for note in entry.notes if note.prefix == target.note_prefix]
                if len(notes) != 1:
                    raise ValueError(f"Detached KET source note target is missing or ambiguous: {source_key}")
                notes[0].body = target.value
            elif target.kind == "supplement":
                entry.supplements.append(target.value)
            else:
                raise ValueError(f"Unknown detached KET source text type: {target.kind}")
            resolved_keys.add(source_key)
        retained_pages.append(
            ParsedPage(
                page.chapter,
                page.page,
                page.entries,
                page.note_count,
                page.unassigned_note_count,
                page.unassigned_notes,
                tuple(retained_orphans),
                page.source_has_mind_map,
                page.source_map_title_en,
                page.source_map_title_zh,
            )
        )

    missing = set(MANUAL_DETACHED_TEXT_TARGETS) - resolved_keys
    if missing:
        raise ValueError(f"Expected detached KET source text is absent: {sorted(missing)}")
    return tuple(retained_pages)


def parse_note_body(value: str) -> tuple[str, str]:
    """Split common source-note forms into displayable English and Chinese text."""

    compact = normalise_text(value)
    chinese = re.search(r"[\u4e00-\u9fff]", compact)
    if not chinese:
        return compact, ""
    english = compact[: chinese.start()].strip(" -—:：；;（(")
    translation = compact[chinese.start() :].strip()
    return english, translation


def parse_page_blocks(chapter: Chapter, page: int, blocks: tuple[PdfBlock, ...]) -> ParsedPage:
    """Parse one PDF page using geometry to retain wrapped definitions."""

    supplemental_forms: dict[int, list[tuple[str, str, PdfBlock]]] = defaultdict(list)
    combined_entries: dict[int, tuple[str, str, str, PdfBlock]] = {}
    combined_plain_entries: dict[int, tuple[str, str, PdfBlock]] = {}
    supplemental_indexes: set[int] = set()
    for block in blocks:
        continuation_match = IPA_CONTINUATION_RE.fullmatch(block.text)
        if not continuation_match:
            continue
        predecessors = [
            candidate
            for candidate in blocks
            if same_column(candidate, block) and candidate.y1 <= block.y0 and block.y0 - candidate.y1 <= 34
        ]
        if not predecessors:
            continue
        predecessor = max(predecessors, key=lambda candidate: candidate.y1)
        predecessor_match = entry_match(predecessor)
        if predecessor_match:
            supplemental_forms[predecessor.index].append(
                (
                    normalise_text(continuation_match.group("ipa")),
                    normalise_text(continuation_match.group("definition")),
                    block,
                )
            )
            supplemental_indexes.add(block.index)
        elif TERM_ONLY_RE.fullmatch(predecessor.text):
            combined_entries[predecessor.index] = (
                normalise_text(predecessor.text),
                normalise_text(continuation_match.group("ipa")),
                normalise_text(continuation_match.group("definition")),
                block,
            )
            supplemental_indexes.add(block.index)

    for block in blocks:
        if not is_word_column(block) or not TERM_ONLY_RE.fullmatch(block.text):
            continue
        successors = [
            candidate
            for candidate in blocks
            if same_column(candidate, block)
            and candidate.y0 >= block.y1
            and candidate.y0 - block.y1 <= 34
            and is_continuation_text(candidate.text)
        ]
        if not successors:
            continue
        successor = min(successors, key=lambda candidate: candidate.y0)
        combined_plain_entries[block.index] = (
            normalise_text(block.text),
            normalise_text(successor.text),
            successor,
        )
        supplemental_indexes.add(successor.index)

    unresolved: list[
        tuple[str, str, str, PdfBlock, list[tuple[str, str, PdfBlock]], list[int]]
    ] = []
    notes: list[SourceNote] = []
    occupied_indexes: set[int] = set()
    active_note: SourceNote | None = None

    for block in blocks:
        combined = combined_entries.get(block.index)
        if combined:
            term, ipa, definition, ipa_block = combined
            unresolved.append((term, ipa, definition, block, [], [block.index, ipa_block.index]))
            occupied_indexes.update({block.index, ipa_block.index})
            active_note = None
            continue

        plain_combined = combined_plain_entries.get(block.index)
        if plain_combined:
            term, definition, definition_block = plain_combined
            unresolved.append((term, "", definition, block, [], [block.index, definition_block.index]))
            occupied_indexes.update({block.index, definition_block.index})
            active_note = None
            continue
        match = entry_match(block)
        if match:
            unresolved.append(
                (
                    normalise_text(match.group("term")),
                    normalise_text(match.group("ipa")),
                    normalise_text(match.group("definition")),
                    block,
                    supplemental_forms.get(block.index, []),
                    [
                        block.index,
                        *(supplemental_block.index for _, _, supplemental_block in supplemental_forms.get(block.index, [])),
                    ],
                )
            )
            occupied_indexes.add(block.index)
            active_note = None
            continue

        if block.index in supplemental_indexes:
            active_note = None
            occupied_indexes.add(block.index)
            continue

        note_match = NOTE_RE.fullmatch(block.text)
        if note_match:
            active_note = SourceNote(
                prefix=note_match.group("prefix"),
                body=normalise_text(note_match.group("body")),
                block=block,
                block_indexes=[block.index],
            )
            notes.append(active_note)
            occupied_indexes.add(block.index)
            continue

        plain_entry_match = no_ipa_entry_match(block) if is_word_column(block) else None
        if plain_entry_match:
            unresolved.append(
                (
                    normalise_text(plain_entry_match.group("term")),
                    "",
                    normalise_text(plain_entry_match.group("definition")),
                    block,
                    [],
                    [block.index],
                )
            )
            occupied_indexes.add(block.index)
            active_note = None
            continue

        if active_note is None:
            continue
        is_adjacent = same_column(active_note.block, block) and 0 <= block.y0 - active_note.block.y1 <= 36
        if is_adjacent and not is_ignorable_block(block.text):
            active_note.body = normalise_text(f"{active_note.body} {block.text}")
            active_note.block_indexes.append(block.index)
            occupied_indexes.add(block.index)
            # A wrapped note can span several physical blocks.
            active_note = SourceNote(
                prefix=active_note.prefix,
                body=active_note.body,
                block=PdfBlock(
                    active_note.block.index,
                    active_note.block.x0,
                    active_note.block.y0,
                    active_note.block.x1,
                    block.y1,
                    active_note.block.text,
                ),
                block_indexes=active_note.block_indexes,
            )
            notes[-1] = active_note
        else:
            active_note = None

    entries: list[VocabularyEntry] = []
    entry_indexes = {block.index for _, _, _, block, _, _ in unresolved}
    for term, ipa, definition, block, alternate_forms, source_indexes in unresolved:
        provisional = VocabularyEntry(chapter, page, 0, term, ipa, "", "", block)
        continuation = continuation_for(provisional, blocks, occupied_indexes, entry_indexes)
        part_of_speech, meaning = split_definition(" ".join([definition, *(item.text for item in continuation)]))
        pronunciations = [pronunciation_for(term, ipa)] if ipa else []
        parts_of_speech = [part_of_speech] if part_of_speech else []
        meanings = [meaning] if meaning else []
        for alternate_ipa, alternate_definition, _ in alternate_forms:
            alternate_part, alternate_meaning = split_definition(alternate_definition)
            pronunciations.append(pronunciation_for(term, alternate_ipa))
            if alternate_part:
                parts_of_speech.append(alternate_part)
            if alternate_meaning:
                meanings.append(alternate_meaning)
        entries.append(
            VocabularyEntry(
                chapter=chapter,
                page=page,
                order=0,
                term=term,
                ipa=" · ".join(dict.fromkeys(pronunciations)),
                part_of_speech=" / ".join(dict.fromkeys(parts_of_speech)),
                meaning="；".join(dict.fromkeys(meanings)),
                block=block,
                block_indexes=[*source_indexes, *(item.index for item in continuation)],
            )
        )

    entries.sort(key=lambda entry: (entry.block.y0, entry.block.x0, entry.term.lower()))
    for order, entry in enumerate(entries, start=1):
        entry.order = order

    unassigned_notes = []
    for note in notes:
        target = note_target(note, entries)
        if target is None:
            unassigned_notes.append(note)
        elif note.body:
            target.notes.append(note)

    orphan_definition_blocks = tuple(
        block
        for block in blocks
        if block.index not in occupied_indexes and is_continuation_text(block.text)
    )

    return ParsedPage(
        chapter,
        page,
        tuple(entries),
        len(notes),
        len(unassigned_notes),
        tuple(unassigned_notes),
        orphan_definition_blocks,
    )


def parse_pdf(path: Path = PDF_PATH) -> tuple[Chapter, tuple[ParsedPage, ...]]:
    """Load the source PDF and parse every vocabulary page in its 40 chapters."""

    if not path.is_file():
        raise FileNotFoundError(f"KET source PDF does not exist: {path}")

    import pymupdf

    document = pymupdf.open(path)
    try:
        chapters = extract_chapters(document.get_toc(simple=False))
        pages = []
        for chapter in chapters:
            chapter_pages = []
            for page_number in range(chapter.start_page, chapter.end_page + 1):
                source_page = document[page_number - 1]
                blocks = pdf_blocks(source_page)
                parsed = parse_page_blocks(chapter, page_number, blocks)
                bounds = source_mind_map_bounds(source_page)
                if bounds:
                    title_en, title_zh = SOURCE_MAP_TITLE_OVERRIDES.get(
                        (chapter.number, page_number),
                        split_source_map_title(source_map_title(blocks, bounds), chapter),
                    )
                    parsed = replace(
                        parsed,
                        source_has_mind_map=True,
                        source_map_title_en=title_en,
                        source_map_title_zh=title_zh,
                    )
                if parsed.entries or parsed.source_has_mind_map:
                    chapter_pages.append(parsed)
            pages.extend(attach_chapter_notes(tuple(chapter_pages)))
        return chapters, apply_detached_source_text(tuple(pages))
    finally:
        document.close()


def source_note_payload(note: SourceNote) -> dict[str, str]:
    note_type, label = NOTE_LABELS[note.prefix]
    english, chinese = parse_note_body(note.body)
    return {"type": note_type, "label": label, "english": english, "chinese": chinese}


def leaf_payload(entry: VocabularyEntry) -> dict:
    """Create the reusable client content for one vocabulary leaf."""

    payload = {
        "id": f"{entry.page}-{slugify(entry.term)}-{entry.order}",
        "word": entry.term,
        "chinese": entry.meaning,
        "pronunciation": pronunciation_of(entry.ipa) if entry.ipa else "",
        "part_of_speech": entry.part_of_speech,
    }
    study_notes = []
    for note in entry.notes:
        if note.prefix in MEMORY_PREFIXES and "memory_tip" not in payload:
            payload["memory_label"] = MEMORY_LABELS[note.prefix]
            payload["memory_tip"] = note.body
            continue
        if note.prefix in NOTE_LABELS:
            source_note = source_note_payload(note)
            study_notes.append(source_note)
            if note.prefix == "搭" and source_note["english"] and "example" not in payload:
                payload["example"] = source_note["english"]
                payload["example_zh"] = source_note["chinese"]
    for supplement in entry.supplements:
        study_notes.append(
            {
                "type": "source_note",
                "label": "原书说明",
                "english": supplement,
                "chinese": "",
            }
        )
    if study_notes:
        payload["study_notes"] = study_notes
    return payload


def word_group(entry: VocabularyEntry) -> str:
    part = entry.part_of_speech
    if "名" in part:
        return "noun"
    if "动" in part:
        return "verb"
    if "形" in part:
        return "adjective"
    if "副" in part:
        return "adverb"
    return "function"


def canonical_term(value: str) -> str:
    """Match source words while keeping the learner-facing spelling intact."""

    return re.sub(r"\s+", " ", value.strip()).casefold()


def default_map_lesson(
    chapter: Chapter, page: int, entries: list[VocabularyEntry]
) -> ImportedMapLesson:
    """Use the first source word as the visual root for ordinary pages."""

    center = entries[0] if entries else None
    return ImportedMapLesson(
        page=page,
        source_pages=(page,),
        title_en=f"{chapter.title_en} · Word Map",
        title_zh=chapter.title_zh,
        center_label=center.term if center else chapter.title_en,
        center_zh=center.meaning if center else chapter.title_zh,
        center_emoji=CHAPTER_EMOJIS[chapter.number - 1],
        entries=tuple(entries),
    )


def source_page_lesson(
    parsed_page: ParsedPage,
    entries: tuple[VocabularyEntry, ...] | list[VocabularyEntry] | None = None,
    source_pages: tuple[int, ...] | None = None,
) -> ImportedMapLesson:
    """Create a native map or a source-order word list for one PDF page."""

    chapter = parsed_page.chapter
    lesson_entries = tuple(parsed_page.entries if entries is None else entries)
    lesson_source_pages = source_pages or (parsed_page.page,)
    if parsed_page.source_has_mind_map:
        title_en = parsed_page.source_map_title_en or chapter.title_en
        title_zh = parsed_page.source_map_title_zh or chapter.title_zh
        return ImportedMapLesson(
            page=parsed_page.page,
            source_pages=lesson_source_pages,
            title_en=title_en,
            title_zh=title_zh,
            center_label=title_en,
            center_zh=title_zh,
            center_emoji=CHAPTER_EMOJIS[chapter.number - 1],
            entries=lesson_entries,
        )

    return ImportedMapLesson(
        page=parsed_page.page,
        source_pages=lesson_source_pages,
        title_en="Extra Vocabulary",
        title_zh="扩展单词",
        center_label=chapter.title_en,
        center_zh=chapter.title_zh,
        center_emoji=CHAPTER_EMOJIS[chapter.number - 1],
        entries=lesson_entries,
        presentation="word-list",
    )


def entry_by_term(entries: list[VocabularyEntry]) -> dict[str, VocabularyEntry]:
    return {canonical_term(entry.term): entry for entry in entries}


def entries_for_terms(
    entries: list[VocabularyEntry], terms: tuple[str, ...]
) -> tuple[VocabularyEntry, ...]:
    by_term = entry_by_term(entries)
    missing = [term for term in terms if canonical_term(term) not in by_term]
    if missing:
        raise ValueError(f"Mind-map terms were not parsed: {', '.join(missing)}")
    return tuple(by_term[canonical_term(term)] for term in terms)


def validate_mind_map_content(content: dict) -> None:
    """Catch malformed imports before catalogue writes start."""

    root = content.get("mind_map")
    if not isinstance(root, dict):
        raise ValueError("Imported lesson must contain mind_map.")
    branches = root.get("branches")
    if not isinstance(branches, list) or not 1 <= len(branches) <= 5:
        raise ValueError("Imported mind map must contain between one and five branches.")
    leaves = [leaf for branch in branches for leaf in branch.get("leaves", [])]
    if not leaves:
        raise ValueError("Imported mind map must contain at least one word leaf.")
    if any(not leaf.get("word") or not leaf.get("chinese") for leaf in leaves):
        raise ValueError("Every imported leaf needs a word and Chinese meaning.")
    if len({leaf["id"] for leaf in leaves}) != len(leaves):
        raise ValueError("Leaf IDs must be unique within an imported mind map.")
    diagram = root.get("diagram")
    if not isinstance(diagram, dict):
        raise ValueError("Imported lesson must contain diagram metadata.")
    if diagram.get("presentation") == "word-list":
        word_list = root.get("word_list")
        if not isinstance(word_list, list) or len(word_list) != len(leaves):
            raise ValueError("Imported word-list lesson must preserve every source word.")


def source_map_branches(entries: list[VocabularyEntry]) -> list[dict]:
    """Lay unlabelled source map words across readable native branches.

    The PDF's branch lettering is baked into artwork, while the vocabulary
    cards remain selectable text.  Do not invent subject categories from part
    of speech: split the source-order cards into short, evenly sized arms so
    every word can stay large and clear on a phone-sized canvas.
    """

    if not entries:
        return []
    branch_count = 1 if len(entries) == 1 else min(4, max(2, (len(entries) + 3) // 4))
    chunk_size = (len(entries) + branch_count - 1) // branch_count
    positions_by_count = {
        1: ("east",),
        2: ("northwest", "southeast"),
        3: ("northwest", "northeast", "south"),
        4: ("northwest", "northeast", "southeast", "southwest"),
    }
    positions = positions_by_count[branch_count]
    branches = []
    for index, start in enumerate(range(0, len(entries), chunk_size)):
        branch_entries = entries[start : start + chunk_size]
        first_entry = branch_entries[0]
        _, _, _, emoji, tone = BRANCH_DEFINITIONS[index % len(BRANCH_DEFINITIONS)]
        branches.append(
            {
                "id": f"source-arm-{index + 1}",
                # The first source word visibly anchors its arm.  It is also
                # present in the selectable word detail below the diagram.
                "label": first_entry.term,
                "label_zh": first_entry.meaning,
                "emoji": emoji,
                "tone": tone,
                "position": positions[index],
                "leaves": [leaf_payload(entry) for entry in branch_entries],
            }
        )
    return branches


def mind_map_content(
    chapter: Chapter,
    page: int,
    entries: list[VocabularyEntry],
    segment: int,
    lesson: ImportedMapLesson | None = None,
) -> dict:
    """Build a client-native, hand-drawn-style vocabulary map."""

    map_lesson = lesson or default_map_lesson(chapter, page, entries)
    all_entries = list(map_lesson.entries)
    lookup = entry_by_term(all_entries)
    center_entry = lookup.get(canonical_term(map_lesson.center_label))
    display_entries = [entry for entry in all_entries if entry is not center_entry]
    if not display_entries:
        display_entries = all_entries

    if map_lesson.presentation == "word-list":
        # Keep the original reading order instead of grouping the list by
        # part of speech.  The branch remains in the neutral payload schema,
        # while Mini Program clients render ``word_list`` as clean cards.
        branches = [
            {
                "id": "source-words",
                "label": "Words",
                "label_zh": "本页单词",
                "emoji": "📖",
                "tone": "violet",
                "position": "south",
                "leaves": [leaf_payload(entry) for entry in all_entries],
            }
        ]
    elif map_lesson.branches:
        branches = []
        for spec in map_lesson.branches:
            branch_entries = entries_for_terms(all_entries, spec.terms)
            branches.append(
                {
                    "id": spec.id,
                    "label": spec.label,
                    "label_zh": spec.label_zh,
                    "emoji": spec.emoji,
                    "tone": spec.tone,
                    "position": spec.position,
                    "leaves": [leaf_payload(entry) for entry in branch_entries],
                }
            )
    else:
        branches = source_map_branches(display_entries)

    center_leaf = leaf_payload(center_entry) if center_entry else {}
    source_pages = map_lesson.source_pages
    is_word_list = map_lesson.presentation == "word-list"
    content = {
        "mind_map": {
            "title": map_lesson.title_en or f"{chapter.title_en} · Word Map {segment:02d}",
            "title_zh": map_lesson.title_zh or chapter.title_zh,
            "diagram": {
                "style": "word-list" if is_word_list else "storybook-branches",
                "presentation": "word-list" if is_word_list else "mind-map",
                "source_pages": list(source_pages),
            },
            "center": {
                "label": map_lesson.center_label,
                "label_zh": map_lesson.center_zh,
                "emoji": map_lesson.center_emoji,
                "pronunciation": center_leaf.get("pronunciation", ""),
                "memory_label": center_leaf.get("memory_label", ""),
                "memory_tip": center_leaf.get("memory_tip", ""),
            },
            "branches": branches,
            "word_list": [leaf_payload(entry) for entry in all_entries] if is_word_list else [],
            "source": {
                "document": PDF_PATH.name,
                "chapter": chapter.number,
                "page": page,
                "pages": list(source_pages),
                "import_key": f"ket-mind-map-pdf:{chapter.number:02d}:{page:03d}:{segment:02d}",
            },
        }
    }
    validate_mind_map_content(content)
    return content


def source_notes_text(entry: VocabularyEntry) -> str:
    lines = [f"{note.prefix} {note.body}".strip() for note in entry.notes if note.body]
    lines.extend(f"说明 {supplement}" for supplement in entry.supplements)
    return "\n".join(lines)


def vocabulary_values(entry: VocabularyEntry, sort_order: int) -> dict:
    """Map one parsed source entry into the existing vocabulary_library table."""

    source_lines = [
        f"[{entry.source_key}]",
        f"来源：{PDF_PATH.name} · 第 {entry.page} 页 · {entry.chapter.title_en}",
    ]
    if source_notes_text(entry):
        source_lines.append(source_notes_text(entry))
    collocations = [source_note_payload(note) for note in entry.notes if note.prefix == "搭"]
    first_collocation = collocations[0] if collocations else {"english": "", "chinese": ""}
    english_note_parts = []
    if entry.ipa:
        english_note_parts.append(f"音标 {pronunciation_of(entry.ipa)}")
    if entry.part_of_speech:
        english_note_parts.append(f"词性 {entry.part_of_speech}")
    return {
        "category": chapter_category(entry.chapter),
        "term": entry.term,
        "chinese_meaning": entry.meaning,
        "english_note": "；".join(english_note_parts),
        "example_sentence": first_collocation["english"],
        "extra_note": "\n".join(source_lines),
        "sort_order": sort_order,
    }


def existing_import_rows(db: Session) -> dict[str, int]:
    """Index existing source rows by the marker written into extra_note."""

    rows = db.execute(
        select(m.vocabulary_library.c.id, m.vocabulary_library.c.extra_note).where(
            m.vocabulary_library.c.extra_note.like(f"{SOURCE_MARKER_PREFIX}%")
        )
    ).all()
    indexed = {}
    for item_id, extra_note in rows:
        match = re.match(r"^\[(ket-mind-map-pdf:[^\]]+)\]", extra_note or "")
        if match:
            indexed[match.group(1)] = item_id
    return indexed


def import_vocabulary_rows(db: Session, pages: tuple[ParsedPage, ...]) -> tuple[int, int]:
    """Upsert all source vocabulary rows without creating a duplicate table."""

    existing = existing_import_rows(db)
    inserted = 0
    updated = 0
    sequence = 0
    for parsed_page in pages:
        for entry in parsed_page.entries:
            sequence += 1
            values = vocabulary_values(entry, sequence)
            current_id = existing.get(entry.source_key)
            if current_id is None:
                db.execute(m.vocabulary_library.insert().values(**values))
                inserted += 1
            else:
                db.execute(
                    update(m.vocabulary_library)
                    .where(m.vocabulary_library.c.id == current_id)
                    .values(**values, updated_at=func.now())
                )
                updated += 1
    return inserted, updated


def curated_word_keys() -> dict[int, set[str]]:
    """Avoid repeating only the real leaves in the published overview maps."""

    from scripts import seed_ket_mind_map_courseware as seeded

    result: dict[int, set[str]] = {}
    for chapter_number, content in ((1, seeded.food_mind_map_content()), (5, seeded.mind_map_content())):
        root = content["mind_map"]
        words = [leaf.get("word", "") for branch in root.get("branches", []) for leaf in branch.get("leaves", [])]
        keys = set()
        for word in words:
            for variant in term_variants(word):
                keys.add(variant)
        result[chapter_number] = keys
    return result


def is_covered_by_curated_map(entry: VocabularyEntry, covered_keys: set[str]) -> bool:
    return any(variant in covered_keys for variant in term_variants(entry.term))


def course_code(chapter: Chapter) -> str:
    return f"ket-mind-map-c{chapter.number:02d}-{slugify(chapter.title_en)}"


def material_code(chapter: Chapter) -> str:
    return f"ket-mind-map-c{chapter.number:02d}"


def curated_codes(chapter: Chapter, db: Session) -> tuple[str, str, int] | None:
    """Reuse the published Food and Family examples as chapter introductions."""

    known = {
        1: ("ket-mind-map-food-demo", "ket-mind-map-food-demo"),
        5: ("ket-mind-map-family-demo", "ket-mind-map-family-demo"),
    }
    codes = known.get(chapter.number)
    if codes is None:
        return None
    material_id = row_id(db, m.learning_material, m.learning_material.c.material_code, codes[0])
    if material_id is None:
        return None
    return codes[0], codes[1], material_id


def map_lesson_from_spec(
    spec: MapLessonSpec, entries: list[VocabularyEntry]
) -> ImportedMapLesson:
    return ImportedMapLesson(
        page=spec.page,
        source_pages=spec.source_pages,
        title_en=spec.title_en,
        title_zh=spec.title_zh,
        center_label=spec.center_label,
        center_zh=spec.center_zh,
        center_emoji=spec.center_emoji,
        entries=entries_for_terms(entries, spec.terms),
        branches=spec.branches,
    )


def next_entries_for_empty_map(
    parsed_pages: list[ParsedPage], start_index: int
) -> tuple[tuple[VocabularyEntry, ...], tuple[int, ...]]:
    """Borrow the immediately following source cards for an artwork-only map."""

    diagram_page = parsed_pages[start_index]
    for candidate in parsed_pages[start_index + 1 :]:
        if candidate.source_has_mind_map:
            break
        if candidate.entries:
            return tuple(candidate.entries), (diagram_page.page, candidate.page)
    return (), (diagram_page.page,)


def course_lesson_entries(parsed_pages: list[ParsedPage]) -> list[ImportedMapLesson]:
    """Create a native map for each diagram and a list for each plain page."""

    if not parsed_pages:
        return []
    chapter = parsed_pages[0].chapter
    all_entries = [entry for parsed_page in parsed_pages for entry in parsed_page.entries]
    if chapter.number == 4:
        diagrams = [map_lesson_from_spec(spec, all_entries) for spec in UNIT4_MAP_SPECS]
        word_lists = [
            source_page_lesson(parsed_page)
            for parsed_page in parsed_pages
            if not parsed_page.source_has_mind_map
        ]
        return sorted([*diagrams, *word_lists], key=lambda lesson: lesson.page)
    lessons = []
    for index, parsed_page in enumerate(parsed_pages):
        if parsed_page.source_has_mind_map:
            if parsed_page.entries:
                lessons.append(source_page_lesson(parsed_page))
                continue
            entries, source_pages = next_entries_for_empty_map(parsed_pages, index)
            if entries:
                lessons.append(source_page_lesson(parsed_page, entries, source_pages))
            continue
        if parsed_page.entries:
            lessons.append(source_page_lesson(parsed_page))
    return lessons


def ensure_template(catalog: LearningCatalogService, db: Session) -> dict:
    current_id = row_id(db, m.learning_template, m.learning_template.c.template_code, TEMPLATE_CODE)
    return catalog.save_template(
        s.LearningTemplateInput(
            template_code=TEMPLATE_CODE,
            template_version=1,
            name="思维导图课件",
            description="按 PDF 原页的思维导图或单词清单学习 KET 高频词汇。",
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
        current_id,
    )


def ensure_topic(catalog: LearningCatalogService, db: Session, module_id: int) -> dict:
    return catalog.save_topic(
        s.LearningTopicInput(
            module_id=module_id,
            topic_code=TOPIC_CODE,
            title="KET 词汇思维导图",
            title_en="KET Vocabulary Mind Maps",
            description="按原书 PDF 页面学习 40 个 KET 高频主题词汇。",
            sort_order=95,
            is_published=1,
        ),
        ACTOR,
        row_id(db, m.learning_topic, m.learning_topic.c.topic_code, TOPIC_CODE),
    )


def remove_stale_generated_lessons(
    db: Session,
    material_id: int,
    chapter: Chapter,
    expected_lesson_codes: set[str],
) -> int:
    """Remove only superseded importer pages while preserving curated intros."""

    code_prefix = f"ket-mind-map-c{chapter.number:02d}-"
    stale_ids = db.execute(
        select(m.learning_material_lesson.c.id).where(
            m.learning_material_lesson.c.material_id == material_id,
            m.learning_material_lesson.c.lesson_code.like(f"{code_prefix}%"),
            m.learning_material_lesson.c.lesson_code.not_in(expected_lesson_codes),
        )
    ).scalars().all()
    if stale_ids:
        db.execute(
            m.learning_material_lesson.delete().where(m.learning_material_lesson.c.id.in_(stale_ids))
        )
    return len(stale_ids)


def upsert_chapter_catalogue(
    catalog: LearningCatalogService,
    db: Session,
    template_id: int,
    topic_id: int,
    chapter: Chapter,
    parsed_pages: list[ParsedPage],
) -> dict[str, int]:
    """Create one material/course per source chapter and its word-map lessons."""

    curated = curated_codes(chapter, db)
    if curated:
        material_code_value, course_code_value, known_material_id = curated
    else:
        material_code_value = material_code(chapter)
        course_code_value = course_code(chapter)
        known_material_id = row_id(
            db, m.learning_material, m.learning_material.c.material_code, material_code_value
        )

    all_entries = [entry for parsed_page in parsed_pages for entry in parsed_page.entries]
    imported_lessons = course_lesson_entries(parsed_pages)
    existing_intro_count = 1 if curated else 0
    estimated_minutes = max(5, min(45, (len(all_entries) + 5) // 6))

    material = catalog.save_material(
        s.LearningMaterialInput(
            template_id=template_id,
            material_code=material_code_value,
            title=f"{chapter.number:02d} · {chapter.title_zh}",
            title_en=chapter.title_en,
            summary=f"{chapter.title_zh}主题词汇，共 {len(all_entries)} 条 PDF 词条。",
            material_type="mind_map",
            publisher="Happy English",
            version_name="KET 思维导图课件 v1",
            difficulty_code="ket",
            estimated_minutes=estimated_minutes,
            sort_order=chapter.number * 10,
            is_published=1,
        ),
        ACTOR,
        known_material_id,
    )

    expected_lesson_codes = set()
    for index, map_lesson in enumerate(imported_lessons, start=1 + existing_intro_count):
        page = map_lesson.page
        entries = list(map_lesson.entries)
        lesson_code = f"ket-mind-map-c{chapter.number:02d}-p{page:03d}-{index:02d}"
        expected_lesson_codes.add(lesson_code)
        lesson_id = db.execute(
            select(m.learning_material_lesson.c.id).where(
                m.learning_material_lesson.c.material_id == material["id"],
                m.learning_material_lesson.c.lesson_code == lesson_code,
            )
        ).scalar_one_or_none()
        content = mind_map_content(chapter, page, entries, index, map_lesson)
        is_word_list = map_lesson.presentation == "word-list"
        catalog.save_material_lesson(
            material["id"],
            s.LearningMaterialLessonInput(
                lesson_code=lesson_code,
                title="扩展单词" if is_word_list else f"{map_lesson.title_zh} · 词汇图",
                title_en=map_lesson.title_en,
                summary="",
                lesson_format="source",
                content=content,
                estimated_minutes=max(3, min(10, (len(entries) + 3) // 4)),
                sort_order=index * 10,
                is_published=1,
            ),
            ACTOR,
            lesson_id,
        )

    stale_lesson_count = remove_stale_generated_lessons(
        db, material["id"], chapter, expected_lesson_codes
    )

    # Saving a material after its lessons validates the full generated set
    # against the registered client renderer before the course is exposed.
    material = catalog.save_material(
        s.LearningMaterialInput(
            template_id=template_id,
            material_code=material_code_value,
            title=f"{chapter.number:02d} · {chapter.title_zh}",
            title_en=chapter.title_en,
            summary=f"{chapter.title_zh}主题词汇，共 {len(all_entries)} 条 PDF 词条。",
            material_type="mind_map",
            publisher="Happy English",
            version_name="KET 思维导图课件 v1",
            difficulty_code="ket",
            estimated_minutes=estimated_minutes,
            sort_order=chapter.number * 10,
            is_published=1,
        ),
        ACTOR,
        material["id"],
    )

    current_course_id = row_id(db, m.learning_course, m.learning_course.c.course_code, course_code_value)
    course = catalog.save_course(
        s.LearningCourseInput(
            topic_id=topic_id,
            material_ids=[material["id"]],
            course_code=course_code_value,
            title=f"KET 思维导图 · {chapter.number:02d} {chapter.title_zh}",
            title_en=f"KET Mind Map · {chapter.title_en}",
            summary=f"{chapter.title_zh}主题的 KET 词汇，按原书关系图绘制 {len(all_entries)} 个词条。",
            course_type="lesson",
            estimated_minutes=estimated_minutes,
            difficulty_code="ket",
            sort_order=chapter.number * 10,
            is_published=1,
            access_policy="free",
        ),
        ACTOR,
        current_course_id,
    )
    db.execute(
        update(m.learning_topic_course)
        .where(
            m.learning_topic_course.c.topic_id == topic_id,
            m.learning_topic_course.c.course_id == course["id"],
        )
        .values(sort_order=chapter.number * 10, updated_by=ACTOR["id"])
    )
    return {
        "course_id": course["id"],
        "material_id": material["id"],
        "imported_lesson_count": len(imported_lessons),
        "stale_lesson_count": stale_lesson_count,
    }


def validate_source_data(chapters: tuple[Chapter, ...], pages: tuple[ParsedPage, ...]) -> None:
    """Fail before writes if the PDF parser has obviously lost source data."""

    entries = [entry for page in pages for entry in page.entries]
    missing_meanings = [entry for entry in entries if not entry.meaning]
    unassigned_notes = [note for page in pages for note in page.unassigned_notes]
    unassigned_word_column_text = [
        (page, block)
        for page in pages
        for block in page.orphan_definition_blocks
        if is_word_column(block)
    ]
    if len(chapters) != 40:
        raise ValueError("The KET import requires all 40 source chapters.")
    if len(entries) < 1000:
        raise ValueError(f"Expected at least 1,000 source entries, got {len(entries)}.")
    if missing_meanings:
        examples = ", ".join(f"{entry.term} (p.{entry.page})" for entry in missing_meanings[:8])
        raise ValueError(f"Source entries without a parsed Chinese meaning: {examples}")
    if unassigned_notes:
        examples = ", ".join(
            f"{page.chapter.number:02d}/p.{page.page}: {note.prefix} {note.body}"
            for page in pages
            for note in page.unassigned_notes[:3]
        )
        raise ValueError(f"Source notes without a target word: {examples}")
    if unassigned_word_column_text:
        examples = ", ".join(
            f"{page.chapter.number:02d}/p.{page.page}: {block.text}"
            for page, block in unassigned_word_column_text[:3]
        )
        raise ValueError(f"Source word-column text without a target word: {examples}")


def import_pdf(path: Path = PDF_PATH) -> dict:
    """Parse, validate, and persist the complete source PDF."""

    chapters, pages = parse_pdf(path)
    validate_source_data(chapters, pages)
    pages_by_chapter: dict[int, list[ParsedPage]] = defaultdict(list)
    for parsed_page in pages:
        pages_by_chapter[parsed_page.chapter.number].append(parsed_page)

    settings = Settings()
    engine = make_engine(settings.database_url)
    with Session(engine) as db:
        catalog = LearningCatalogService(db)
        template = ensure_template(catalog, db)
        module_id = db.execute(
            select(m.learning_module.c.id).where(m.learning_module.c.module_code == MODULE_CODE)
        ).scalar_one_or_none()
        if module_id is None:
            raise RuntimeError(f"Missing learning module: {MODULE_CODE}")
        topic = ensure_topic(catalog, db, module_id)

        chapter_results = []
        for chapter in chapters:
            chapter_results.append(
                upsert_chapter_catalogue(
                    catalog,
                    db,
                    template["id"],
                    topic["id"],
                    chapter,
                    pages_by_chapter[chapter.number],
                )
            )

        inserted, updated = import_vocabulary_rows(db, pages)
        db.commit()

    entries = [entry for parsed_page in pages for entry in parsed_page.entries]
    return {
        "topic_id": topic["id"],
        "topic_code": TOPIC_CODE,
        "chapter_count": len(chapters),
        "source_page_count": len(pages),
        "source_entry_count": len(entries),
        "vocabulary_inserted": inserted,
        "vocabulary_updated": updated,
        "course_count": len(chapter_results),
        "material_count": len({result["material_id"] for result in chapter_results}),
        "imported_lesson_count": sum(result["imported_lesson_count"] for result in chapter_results),
        "stale_lesson_removed": sum(result["stale_lesson_count"] for result in chapter_results),
        "unassigned_note_count": sum(page.unassigned_note_count for page in pages),
        "template": f"{TEMPLATE_CODE}.v1",
    }


def main() -> None:
    print(json.dumps(import_pdf(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
