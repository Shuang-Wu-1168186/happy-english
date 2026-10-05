"""Complete the published 10-chapter Commute Micro English curriculum.

Run with:
    PYTHONPATH=. .venv/bin/python scripts/complete_commute_micro_english.py

The initial Stop 1 lesson is intentionally kept as authored content.  This
script adds its remaining seven lessons, then creates Stops 2–10.  It is
idempotent: running it again updates the same curriculum records.
"""

from __future__ import annotations

import html
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models as m
from app import schemas as s
from app.core.config import Settings
from app.core.database import make_engine
from app.services.learning_catalog import LearningCatalogService


ACTOR = {"id": 1}
TOPIC_CODE = "commute-micro-english"
ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "illustrations" / "commute"
STATIC_DIRECTORY = "commute-covers"
MAX_ILLUSTRATION_BYTES = 100 * 1024
INITIAL_CORE_TERMS = {
    "sounds good",
    "give me a second",
    "i'm on my way",
    "pick it up later",
}


@dataclass(frozen=True)
class Phrase:
    """One teachable phrase with a concrete bilingual use case."""

    term: str
    meaning: str
    gloss: str
    reply: str
    reply_zh: str
    cue: str
    cue_zh: str

    @property
    def explanation(self) -> str:
        return self.gloss.rstrip(".") + "."


@dataclass(frozen=True)
class Lesson:
    chapter: int
    number: int
    slug: str
    title: str
    title_en: str
    summary: str
    scene: str
    scene_zh: str
    art: str
    phrases: tuple[Phrase, Phrase, Phrase, Phrase]


@dataclass(frozen=True)
class Chapter:
    number: int
    title: str
    title_en: str
    summary: str
    art: str
    lessons: tuple[Lesson, ...]


def P(
    term: str,
    meaning: str,
    gloss: str,
    reply: str,
    reply_zh: str,
    cue: str,
    cue_zh: str,
) -> Phrase:
    return Phrase(term, meaning, gloss, reply, reply_zh, cue, cue_zh)


def L(
    chapter: int,
    number: int,
    slug: str,
    title: str,
    title_en: str,
    summary: str,
    scene: str,
    scene_zh: str,
    art: str,
    *phrases: Phrase,
) -> Lesson:
    if len(phrases) != 4:
        raise ValueError(f"{slug} needs exactly four core phrases.")
    return Lesson(
        chapter,
        number,
        slug,
        title,
        title_en,
        summary,
        scene,
        scene_zh,
        art,
        tuple(phrases),  # type: ignore[arg-type]
    )


# The curriculum data is deliberately authored rather than assembled from a
# generic phrase list.  Each phrase has its own meaning, explanation and
# conversational cue, so that the dialogue and quick-reply activity stay tied
# to a real situation.
CHAPTERS: tuple[Chapter, ...] = (
    Chapter(
        1,
        "快速自然回应",
        "Fast, Natural Replies",
        "把通勤中最常见的确认、暂停、更新和替代说法说得短而自然。",
        "chat",
        (
            L(
                1,
                2,
                "confirm-a-plan",
                "确认安排",
                "Confirming a Plan",
                "用四句短回应确认自己愿意参加、接受时间或同意一个安排。",
                "下班路上确认晚上的见面安排",
                "下班路上确认晚上的见面安排。",
                "clock",
                P("works for me", "对我来说可以；我方便。", "A reply that says a suggested time or arrangement is acceptable to you", "Six thirty works for me.", "六点半对我来说可以。", "Would six thirty be okay for you?", "六点半对你方便吗？"),
                P("count me in", "算我一个；我参加。", "An enthusiastic way to say that you want to join a plan", "Count me in for dinner after work.", "下班后的晚饭算我一个。", "A few of us are having dinner after work. Want to join?", "我们几个人下班后要吃饭，你来吗？"),
                P("that works", "这样可以；这个办法行。", "A short response that accepts a proposed solution or schedule", "That works. I'll meet you at the station entrance.", "这样可以，我在车站入口见你。", "Could we meet at the station entrance instead?", "我们改在车站入口见面可以吗？"),
                P("I'm good with that", "我同意这个；这样我没问题。", "A relaxed way to say that you accept someone else's suggestion", "I'm good with that. Let's keep the plan simple.", "我同意这个，我们就简单安排吧。", "Let's keep it simple and meet after your train arrives.", "我们简单一点，等你的车到了再见面吧。"),
            ),
            L(
                1,
                3,
                "pause-and-check",
                "暂停并确认",
                "Pause and Check",
                "在看消息、查站台或打开日历时，礼貌地请对方稍等。",
                "车厢里核对地点和时间",
                "在车厢里核对地点和时间。",
                "chat",
                P("hold on", "等一下；先别挂。", "A direct but friendly way to ask someone to wait briefly", "Hold on, I'm checking which exit we need.", "等一下，我在看我们要走哪个出口。", "Which exit should we use?", "我们该走哪个出口？"),
                P("let me check", "让我查一下。", "A phrase used before you look up information or verify a detail", "Let me check the calendar before I confirm.", "让我先查一下日历再确认。", "Are you free on Thursday evening?", "你周四晚上有空吗？"),
                P("bear with me", "请稍等一下；请耐心等我。", "A polite request for patience while you finish something", "Bear with me; the station map is still loading.", "请稍等，车站地图还在加载。", "Can you tell me which platform it is?", "你能告诉我是哪个站台吗？"),
                P("just a moment", "就等一下。", "A courteous way to ask for a very short pause", "Just a moment, I'm opening the address now.", "就等一下，我现在打开地址。", "Can you send me the café address again?", "你能再发一次咖啡馆地址吗？"),
            ),
            L(
                1,
                4,
                "busy-but-reachable",
                "忙碌时也能回应",
                "Busy but Reachable",
                "不方便说话时，说明自己正在忙，并给出更合适的回复方式。",
                "拥挤车厢里处理工作消息",
                "在拥挤车厢里处理工作消息。",
                "signal",
                P("I'm tied up", "我正忙着；暂时走不开。", "A way to say that you are busy and cannot deal with something right now", "I'm tied up until I get off the train.", "我下地铁前都在忙。", "Can you review this document right now?", "你现在能看一下这份文件吗？"),
                P("can't talk right now", "我现在不方便说话。", "A clear, polite way to say that a call is not possible at the moment", "I can't talk right now, but I can text.", "我现在不方便说话，但可以发消息。", "Can I call you for two minutes?", "我能给你打两分钟电话吗？"),
                P("message me instead", "改发消息给我吧。", "A request to use text messages rather than a call", "Message me instead; the train is too loud.", "改发消息给我吧，车厢太吵了。", "Should I call you or send the details?", "我该打电话还是把细节发给你？"),
                P("I'll reply shortly", "我很快回复你。", "A promise that you will send a response soon", "I'll reply shortly when I reach the platform.", "我到站台后很快回复你。", "When will you be able to answer?", "你什么时候能回复？"),
            ),
            L(
                1,
                5,
                "acknowledge-and-update",
                "确认收到并跟进",
                "Acknowledge and Update",
                "先让对方知道你已收到，再说明下一步会做什么。",
                "收到同事的临时更新",
                "收到同事的临时更新。",
                "work",
                P("got it", "知道了；收到。", "A brief acknowledgement that you understand the information", "Got it. I'll use the new meeting link.", "收到，我会用新的会议链接。", "The meeting link has changed.", "会议链接改了。"),
                P("FYI", "供你参考；顺便告知。", "An abbreviation used to share information without requiring an immediate action", "FYI, the client moved the call to Friday.", "供你参考，客户把电话改到周五了。", "Do I need to change anything in the calendar?", "我需要改日历里的内容吗？"),
                P("I'll take a look", "我会看一下。", "A calm way to say that you will review something before responding", "I'll take a look when I have a better signal.", "我信号好一点时会看一下。", "Can you check the spreadsheet on your way in?", "你上班路上能看一下表格吗？"),
                P("keep me in the loop", "有进展请告诉我。", "A request to be included in future updates about a situation", "Keep me in the loop if the meeting time changes again.", "如果会议时间又变了，请告诉我。", "We're still waiting for the final time.", "我们还在等最后确认的时间。"),
            ),
            L(
                1,
                6,
                "offer-an-alternative",
                "提出替代方案",
                "Offer an Alternative",
                "不直接否定对方，而是表达顾虑并给出一个可行选择。",
                "临时调整下班后的安排",
                "临时调整下班后的安排。",
                "change",
                P("I'm not convinced", "我还不太认同；我觉得不太稳妥。", "A polite way to show that an idea has not persuaded you", "I'm not convinced that we can finish before six.", "我不太相信我们能在六点前完成。", "Do you think we can finish before six?", "你觉得我们能在六点前完成吗？"),
                P("how about", "……怎么样？", "A phrase used to introduce an alternative suggestion", "How about meeting one stop closer to you?", "我们在离你近一站的地方见面怎么样？", "The café near my office is too far for you.", "我办公室附近的咖啡馆对你太远了。"),
                P("I'd prefer", "我更倾向于；我更想要。", "A polite way to state the option you like better", "I'd prefer to meet after the rush hour.", "我更想在高峰期之后见面。", "Should we meet at five or after six?", "我们五点见还是六点后见？"),
                P("that could be difficult", "那样可能有点难办。", "A gentle way to explain that a proposed plan may not be practical", "That could be difficult because my train is delayed.", "那样可能有点难，因为我的车晚点了。", "Can you be at the restaurant in ten minutes?", "你十分钟后能到餐厅吗？"),
            ),
            L(
                1,
                7,
                "keep-a-simple-plan",
                "保持简单的安排",
                "Keep a Simple Plan",
                "复盘确认和安排用语，在消息很多时仍把计划说清楚。",
                "通勤中把聚会计划压缩成几条消息",
                "在通勤中把聚会计划压缩成几条消息。",
                "route",
                P("as planned", "按原计划。", "A phrase that confirms that nothing in the arrangement has changed", "We're meeting as planned at the usual entrance.", "我们还是按原计划在常用入口见面。", "Has anything changed for tonight?", "今晚有什么变动吗？"),
                P("no problem", "没问题。", "A friendly reply that says a request or small change is acceptable", "No problem. I can wait for ten minutes.", "没问题，我可以等十分钟。", "Could you wait a little longer?", "你能再等一会儿吗？"),
                P("all set", "都准备好了；没问题了。", "A way to say that the necessary preparation is complete", "All set. I have the tickets on my phone.", "都准备好了，票在我手机里。", "Do you have the tickets and the address?", "你有票和地址了吗？"),
                P("that's fine", "那也可以；没关系。", "A calm response that accepts a minor inconvenience or change", "That's fine. We can meet after your call.", "那也可以，我们在你电话结束后见。", "I may be five minutes late.", "我可能会晚五分钟。"),
            ),
            L(
                1,
                8,
                "continuous-quick-replies",
                "连续快速接话",
                "Continuous Quick Replies",
                "在一段连续消息里报备进度、让对方先开始，并说明自己会赶上。",
                "朋友已经到达，你还在地铁上",
                "朋友已经到了，你还在地铁上。",
                "route",
                P("I'm nearly there", "我快到了。", "A quick update that says you will arrive very soon", "I'm nearly there; I can see the station exit.", "我快到了，已经看到车站出口了。", "Are you still on the train?", "你还在地铁上吗？"),
                P("go ahead without me", "你们先开始，不用等我。", "A considerate way to tell others not to delay their plan for you", "Go ahead without me; I'll join you in a few minutes.", "你们先开始，不用等我，我几分钟后加入。", "We're ready to order. Should we wait?", "我们可以点单了，要等你吗？"),
                P("save me a seat", "给我留个座位。", "A request for someone to keep a place for you", "Save me a seat near the window if you can.", "如果可以，靠窗给我留个座位。", "We're at the café already. Where should we sit?", "我们已经到咖啡馆了，坐哪里好？"),
                P("I'll catch up", "我会赶上；我随后补上。", "A promise that you will join or learn the missed part soon", "I'll catch up when I get there.", "我到了以后会赶上进度。", "We're starting the discussion now.", "我们现在开始讨论了。"),
            ),
        ),
    ),
    Chapter(
        2,
        "约时间和地点",
        "Time and Place",
        "在地铁上用短句约时间、改时间、找地点和确认见面细节。",
        "pin",
        (
            L(
                2,
                1,
                "suggest-a-time",
                "提出时间",
                "Suggest a Time",
                "用自然问法提出可见面的时间，并留出调整空间。",
                "和朋友确认下班后的见面时间",
                "和朋友确认下班后的见面时间。",
                "clock",
                P("are you available", "你有空吗？", "A direct question about whether someone has time", "Are you available after work on Thursday?", "你周四下班后有空吗？", "I'd like to meet this week.", "我想这周见一面。"),
                P("does that suit you?", "这个时间你方便吗？", "A polite question that checks whether a proposed arrangement is convenient", "Does seven o'clock suit you?", "七点钟你方便吗？", "I can meet at seven.", "我七点可以见面。"),
                P("sometime after", "在……之后的某个时间。", "A phrase that gives a flexible starting point for a time", "I'm free sometime after six.", "我六点之后都可以。", "When are you free this evening?", "你今晚什么时候有空？"),
                P("before then", "在那之前。", "A phrase that sets a deadline before a known time", "I can call you before then if the train is quiet.", "如果车厢安静，我可以在那之前打给你。", "Let's decide by eight.", "我们八点前决定吧。"),
            ),
            L(
                2,
                2,
                "change-the-time",
                "调整时间",
                "Change the Time",
                "时间有变时，清楚说出是延后、提前、改约还是自己会迟到。",
                "临时调整一个原定的会面",
                "临时调整一个原定的会面。",
                "change",
                P("push it back", "把时间往后推。", "To move an event to a later time", "Can we push it back by half an hour?", "我们能把时间往后推半小时吗？", "My train is running slowly.", "我的车开得很慢。"),
                P("move it forward", "把时间提前。", "To change an event to an earlier time", "Could we move it forward to five thirty?", "我们能把时间提前到五点半吗？", "I finish work earlier today.", "我今天下班早。"),
                P("reschedule", "重新安排时间。", "To arrange a new time for something that cannot happen as planned", "Let's reschedule the call for tomorrow morning.", "我们把电话重新安排到明天早上吧。", "I won't have a quiet place to talk tonight.", "我今晚没有安静的地方说话。"),
                P("run behind", "落后于计划；要晚了。", "To be later than expected because progress or travel is slow", "I'm running behind because the service stopped.", "因为线路停了，我要晚了。", "Are you still able to make six?", "你还能六点到吗？"),
            ),
            L(
                2,
                3,
                "describe-the-place",
                "描述见面地点",
                "Describe the Place",
                "用入口、出口、对面和街角等定位词快速找到对方。",
                "在陌生车站外描述集合点",
                "在陌生车站外描述集合点。",
                "pin",
                P("by the entrance", "在入口旁边。", "A location phrase for a place immediately next to an entrance", "I'll wait by the entrance with the red sign.", "我会在红色标志旁的入口等你。", "Where should I look for you?", "我该去哪里找你？"),
                P("near the exit", "在出口附近。", "A location phrase for a place close to an exit", "The bakery is near the exit on the left.", "面包店在左边出口附近。", "Is the café inside the station?", "咖啡馆在车站里面吗？"),
                P("across from", "在……对面。", "A phrase used to locate something directly opposite another place", "I'm across from the bookshop.", "我在书店对面。", "I can see the bookshop. Are you close?", "我看到书店了，你在附近吗？"),
                P("on the corner", "在街角。", "A phrase for a place where two streets meet", "The bus stop is on the corner of King Street.", "公交站在 King Street 的街角。", "Which side of King Street should I walk to?", "我应该走到 King Street 的哪一边？"),
            ),
            L(
                2,
                4,
                "find-each-other",
                "找到彼此",
                "Find Each Other",
                "对方已经到了却看不见彼此时，用具体地标和位置继续沟通。",
                "高峰期车站外寻找朋友",
                "在高峰期的车站外寻找朋友。",
                "friends",
                P("where are you exactly?", "你具体在哪里？", "A request for a more precise location when a general answer is not enough", "Where are you exactly? I can see two exits.", "你具体在哪里？我看到两个出口。", "I'm outside the station.", "我在车站外面。"),
                P("I'm by", "我在……旁边。", "A quick way to name the landmark next to you", "I'm by the large station map.", "我在那张大车站地图旁边。", "Can you see the information desk?", "你看得到服务台吗？"),
                P("I can't spot you", "我没看到你。", "A natural way to say that you cannot find a person in a crowd", "I can't spot you in this crowd.", "人太多了，我没看到你。", "I'm wearing a blue jacket.", "我穿着蓝色夹克。"),
                P("look for the blue sign", "找那个蓝色标志。", "A clear instruction that uses a visible landmark to guide someone", "Look for the blue sign beside the taxi rank.", "找出租车候客区旁的蓝色标志。", "Which direction should I walk?", "我应该往哪个方向走？"),
            ),
            L(
                2,
                5,
                "arrive-and-wait",
                "到达和等待",
                "Arrive and Wait",
                "报备自己已经到达，让对方不必着急，并给出等待地点或时间。",
                "你已到餐厅，对方还在路上",
                "你已经到餐厅，对方还在路上。",
                "clock",
                P("I've arrived", "我到了。", "A simple update that tells someone you have reached the meeting place", "I've arrived and found us a table.", "我到了，也找到一张桌子。", "Did you get to the restaurant already?", "你已经到餐厅了吗？"),
                P("take your time", "慢慢来；不用着急。", "A reassuring phrase that says the other person does not need to hurry", "Take your time; I'm happy to wait inside.", "慢慢来，我愿意在里面等。", "I'm still two stops away.", "我还有两站才到。"),
                P("wait inside", "在里面等。", "A phrase that tells someone you will wait indoors rather than outside", "I'll wait inside near the window.", "我会在里面靠窗的位置等。", "It's starting to rain outside.", "外面开始下雨了。"),
                P("be there in five", "五分钟后到。", "A short arrival estimate for a very near destination", "I'll be there in five; I'm leaving the platform now.", "我五分钟后到，我现在正离开站台。", "How much longer will you need?", "你还需要多久？"),
            ),
            L(
                2,
                6,
                "leave-and-meet",
                "出发去见面",
                "Leave and Meet",
                "告诉对方你正往哪里走、会顺路经过，或只短暂停留一下。",
                "从地铁站出发去见朋友",
                "从地铁站出发去见朋友。",
                "route",
                P("head over", "过去；往那边去。", "To start moving toward a nearby destination", "I'm heading over to the café now.", "我现在正往咖啡馆过去。", "Are you still at the station?", "你还在车站吗？"),
                P("meet up", "碰面；会合。", "To come together with someone at an agreed place", "Let's meet up outside the cinema.", "我们在电影院外面碰面吧。", "Where do you want to see each other?", "你想在哪里见面？"),
                P("swing by", "顺路过去一下。", "To visit a place briefly while going somewhere else", "I can swing by the shop before I come over.", "我过去前可以顺路去一下商店。", "Could you get some water on the way?", "你路上能买点水吗？"),
                P("drop in", "顺便来一下；短暂拜访。", "To visit someone or somewhere without staying long", "I'll drop in after I get off the train.", "我下地铁后会顺便过去一下。", "Do you have time to see the manager today?", "你今天有时间见经理吗？"),
            ),
            L(
                2,
                7,
                "time-place-review",
                "时间地点复习",
                "Time and Place Review",
                "把时间地点串成一条清楚的消息，避免来回确认。",
                "把约见信息一次说清楚",
                "把约见信息一次说清楚。",
                "chat",
                P("touch base", "联系一下；简单确认。", "To contact someone briefly to exchange an update or confirm a plan", "Let's touch base when you get off the train.", "你下地铁后我们联系一下。", "I may not know my exact arrival time yet.", "我可能还不知道准确到达时间。"),
                P("set a time", "定个时间。", "To choose and agree on a specific time for something", "Let's set a time before the day gets busy.", "趁今天还没忙起来，我们定个时间吧。", "We keep missing each other this week.", "这周我们总是错过彼此。"),
                P("make it", "赶得上；能参加。", "To be able to arrive or attend at the planned time", "I can make it by seven if the train keeps moving.", "如果地铁不停，我七点能赶到。", "Will you be able to join dinner?", "你能来吃晚饭吗？"),
                P("work around your schedule", "配合你的时间安排。", "To arrange something in a way that fits another person's commitments", "We can work around your schedule this week.", "这周我们可以配合你的时间安排。", "My shifts change every day.", "我每天的班次都不一样。"),
            ),
            L(
                2,
                8,
                "time-place-challenge",
                "时间地点实战",
                "Time and Place Challenge",
                "在一条连续消息里敲定中间地点、常用集合点、准点到达和地图定位。",
                "两个人从不同方向赶往同一个活动",
                "两个人从不同方向赶往同一个活动。",
                "pin",
                P("meet halfway", "在中间碰面。", "To choose a meeting point that is equally convenient for two people", "Let's meet halfway near the river station.", "我们在河边车站附近的中间地点见吧。", "Your office is east of the city and mine is west.", "你的办公室在城东，我的在城西。"),
                P("the usual place", "平常那个地方。", "A familiar location that people normally use for meeting", "Let's meet at the usual place after work.", "我们下班后在平常那个地方见。", "Do we need to choose a new café this time?", "这次我们需要换一家咖啡馆吗？"),
                P("right on time", "准时。", "A phrase that says someone or something arrives exactly at the planned time", "I'll be right on time if this train doesn't stop again.", "如果这趟车不再停，我会准时到。", "Will you make the six o'clock booking?", "你能赶上六点的预订吗？"),
                P("send a pin", "发一个地图定位。", "To share a map location so another person can find you", "Send a pin when you reach the entrance.", "你到入口时发个地图定位。", "There are too many exits at this station.", "这个车站出口太多了。"),
            ),
        ),
    ),
    Chapter(
        3,
        "通勤中的消息回复",
        "Messages on the Move",
        "在信号不稳、即将下车或不方便通话时，仍能清楚处理消息。",
        "signal",
        (
            L(
                3,
                1,
                "poor-signal",
                "信号不好时",
                "When the Signal Is Poor",
                "说明连接不稳定，避免对方以为你故意不回。",
                "地铁进入信号较弱的路段",
                "地铁进入信号较弱的路段。",
                "signal",
                P("the signal is patchy", "信号断断续续。", "A way to say that your mobile connection works only intermittently", "The signal is patchy, so my messages may arrive late.", "信号断断续续，所以我的消息可能会晚到。", "Why are your replies arriving so slowly?", "为什么你的回复来得这么慢？"),
                P("I may lose reception", "我可能会没信号。", "A warning that your phone connection may disappear soon", "I may lose reception in the tunnel.", "进隧道后我可能会没信号。", "Can we stay on the call for another minute?", "我们能再通话一分钟吗？"),
                P("the message didn't go through", "消息没有发出去。", "A phrase that explains that a text or file failed to send", "The message didn't go through, so I'm sending it again.", "消息没有发出去，所以我再发一次。", "Did you receive the address I sent?", "你收到我发的地址了吗？"),
                P("try again later", "晚点再试一次。", "A suggestion to repeat an action after the connection improves", "Let's try again later when I'm above ground.", "等我到地面上后我们再试一次。", "The file still won't upload.", "文件还是上传不了。"),
            ),
            L(
                3,
                2,
                "send-the-details",
                "发送细节",
                "Send the Details",
                "让对方把链接、文件或转发内容以容易查看的方式发过来。",
                "在地铁上索取工作资料",
                "在地铁上索取工作资料。",
                "chat",
                P("send it over", "发给我吧。", "A casual request for someone to send a document, link or detail", "Send it over and I'll read it on the train.", "发给我吧，我会在地铁上看。", "Do you need the draft before the meeting?", "你开会前需要草稿吗？"),
                P("forward it", "转发给我。", "To send on a message that you received from someone else", "Could you forward it to me with the attachment?", "你能把带附件的那封邮件转发给我吗？", "The client replied to my email.", "客户回复了我的邮件。"),
                P("share the link", "分享链接。", "To give someone access to an online page or file by sending its link", "Please share the link instead of a screenshot.", "请直接分享链接，不要发截图。", "How can I open the latest document?", "我怎么打开最新文档？"),
                P("add an attachment", "添加附件。", "To include a file with an email or message before sending it", "Don't forget to add an attachment before you send the email.", "发邮件前别忘了添加附件。", "Is the report ready to send?", "报告可以发了吗？"),
            ),
            L(
                3,
                3,
                "read-it-later",
                "晚点阅读处理",
                "Read It Later",
                "没法仔细看信息时，说清楚你会如何继续处理。",
                "通勤中收到需要阅读的材料",
                "通勤中收到需要阅读的材料。",
                "work",
                P("catch up on", "补看；补上之前错过的内容。", "To do or read things that you missed earlier", "I'll catch up on the notes after I get a seat.", "我坐下后会补看笔记。", "Did you read the updates from this morning?", "你看今天早上的更新了吗？"),
                P("read through", "从头到尾读一遍。", "To read something carefully from beginning to end", "I'll read through the proposal before I reply.", "我回复前会把提案从头到尾读一遍。", "Can you give me feedback on the proposal?", "你能给这份提案一点反馈吗？"),
                P("look into", "调查；仔细了解。", "To examine a problem or question in order to learn more", "I'll look into the error when I reach the office.", "我到办公室后会查一下这个错误。", "Do you know why the report failed?", "你知道报告为什么失败吗？"),
                P("go over", "复核；一起过一遍。", "To review details carefully, often with another person", "Can we go over the agenda before the call?", "我们通话前能把议程过一遍吗？", "What should we cover in the meeting?", "我们会议里要讲什么？"),
            ),
            L(
                3,
                4,
                "voice-notes",
                "语音消息",
                "Voice Notes",
                "在嘈杂或不便打字的时刻，处理语音消息并要求清楚表达。",
                "车厢里收听和回复语音消息",
                "在车厢里收听和回复语音消息。",
                "phone",
                P("leave a voice note", "留一条语音消息。", "To record and send a short spoken message instead of typing", "Leave a voice note if typing is inconvenient.", "如果打字不方便，就留一条语音消息。", "I need to explain the change quickly.", "我需要快速解释这个变化。"),
                P("play it back", "回放一遍。", "To listen to a recorded message again", "I'll play it back when the train is quieter.", "等车厢安静一点，我会再回放一遍。", "Did you understand my voice message?", "你听懂我的语音了吗？"),
                P("speak clearly", "说清楚一点。", "A request for someone to pronounce words more distinctly", "Could you speak clearly? I'm on a noisy train.", "你能说清楚一点吗？我在很吵的地铁上。", "Can you hear the number I just said?", "你听清我刚才说的号码了吗？"),
                P("type it out", "把它打出来。", "A request to write information as text instead of saying it aloud", "Please type it out so I don't miss the address.", "请把它打出来，免得我错过地址。", "Should I send the code in a voice note?", "我需要把验证码用语音发吗？"),
            ),
            L(
                3,
                5,
                "train-status",
                "地铁状态更新",
                "Train Status Updates",
                "用简短消息说明自己刚上车、即将下车或正卡在两站之间。",
                "向等你的人实时更新通勤进度",
                "向等你的人实时更新通勤进度。",
                "route",
                P("I just boarded", "我刚上车。", "An update that says you have only just entered a train, bus or plane", "I just boarded, so I'll be a little later than planned.", "我刚上车，所以会比计划晚一点。", "Have you started your trip yet?", "你已经出发了吗？"),
                P("getting off now", "我现在下车。", "A quick update that says you are leaving the vehicle at this moment", "I'm getting off now and walking to the exit.", "我现在下车，正往出口走。", "Are you close to the station?", "你离车站近了吗？"),
                P("between stations", "在两站之间。", "A description of being on a train that has not reached the next station", "I'm between stations, so I can't check the map yet.", "我在两站之间，所以还没法看地图。", "Can you tell me which exit to use?", "你能告诉我该走哪个出口吗？"),
                P("my stop is next", "下一站就是我下车的站。", "A status update that says your destination station is the next one", "My stop is next, so I'll call you in a minute.", "下一站就是我下车的站，我一分钟后打给你。", "When will you have a quiet place to talk?", "你什么时候能在安静的地方说话？"),
            ),
            L(
                3,
                6,
                "acknowledge-a-message",
                "确认收到消息",
                "Acknowledge a Message",
                "让对方知道你已经看见信息、理解提醒，并会在合适时回复。",
                "上班路上收到团队更新",
                "上班路上收到团队更新。",
                "chat",
                P("I saw your message", "我看到你的消息了。", "An acknowledgement that tells someone their message has reached you", "I saw your message and will reply after my transfer.", "我看到你的消息了，换乘后回复你。", "Did you get my update about the client?", "你收到我关于客户的更新了吗？"),
                P("thanks for the heads-up", "谢谢你提前告知。", "A way to thank someone for warning or informing you early", "Thanks for the heads-up about the platform change.", "谢谢你提前告诉我站台改了。", "Your train will leave from platform four today.", "你今天的车会从四号站台出发。"),
                P("noted", "已知悉；记下了。", "A concise formal acknowledgement that information has been recorded", "Noted. I'll bring the printed copy.", "已知悉，我会带打印版。", "Please bring the signed form tomorrow.", "请明天带上签好的表格。"),
                P("I'll get back to you", "我会再回复你。", "A promise to respond after you have more time or information", "I'll get back to you once I've checked the numbers.", "我查完数字后再回复你。", "Can you confirm the final cost today?", "你今天能确认最终费用吗？"),
            ),
            L(
                3,
                7,
                "message-review",
                "消息回复复习",
                "Message Review",
                "在连接中断后恢复联系，给对方一个简短进度说明。",
                "出了隧道后重新接上对话",
                "出了隧道后重新接上对话。",
                "signal",
                P("lost connection", "连接断了。", "A short explanation that a call, chat or internet link stopped working", "Sorry, I lost connection in the tunnel.", "抱歉，我在隧道里断线了。", "Why did the call end suddenly?", "电话为什么突然断了？"),
                P("send a quick update", "发个简短更新。", "To send only the essential current information", "Send a quick update when you know your arrival time.", "知道到达时间后发个简短更新。", "I don't need every detail; I just need to know when you'll arrive.", "我不需要每个细节，只需要知道你何时到。"),
                P("check in", "报个平安；联系一下。", "To make brief contact to show that you are okay or still engaged", "I'll check in when I reach the office.", "我到办公室后会联系一下。", "Can you let me know you're safe after the delay?", "晚点后你能告诉我你平安吗？"),
                P("keep the conversation going", "让对话继续下去。", "To continue communicating instead of letting an exchange stop", "A short question can keep the conversation going.", "一个简短问题就能让对话继续下去。", "What can I say after I give an update?", "我更新完情况后还能说什么？"),
            ),
            L(
                3,
                8,
                "battery-and-goodbye",
                "低电量和暂别",
                "Low Battery and Goodbye",
                "低电量时说明情况、节省电量，并自然结束一段消息或通话。",
                "回家路上手机快没电",
                "回家路上手机快没电。",
                "phone",
                P("my battery is low", "我手机快没电了。", "A warning that your phone may turn off soon", "My battery is low, so I may go offline.", "我手机快没电了，所以可能会离线。", "Why might you stop replying?", "你为什么可能不回复了？"),
                P("plug it in", "把它插上充电。", "To connect a device to power so that it can charge", "I'll plug it in as soon as I get home.", "我一到家就把它插上充电。", "Can you call me when you arrive?", "你到家后能打给我吗？"),
                P("save some power", "省点电。", "To reduce phone use so that the battery lasts longer", "I'll save some power and read the file later.", "我先省点电，晚点再看文件。", "Do you want to watch the video on the train?", "你想在地铁上看这个视频吗？"),
                P("talk soon", "晚点聊。", "A friendly way to end a conversation while expecting to speak again soon", "Talk soon; I'm about to change trains.", "晚点聊，我马上要换乘了。", "I need to get off at the next station.", "我下一站要下车。"),
            ),
        ),
    ),
    Chapter(
        4,
        "工作即时沟通",
        "Work Messages on the Move",
        "用短而明确的英语说明工作进度、确认理解、分配任务和请求帮助。",
        "work",
        (
            L(
                4,
                1,
                "report-progress",
                "汇报进度",
                "Report Progress",
                "在地铁上用一句话告诉同事任务是否顺利、接近完成或出现延误。",
                "上班路上回复同事的进度询问",
                "上班路上回复同事的进度询问。",
                "work",
                P("I'm working on it", "我正在处理。", "A direct update that says you have started and are actively doing a task", "I'm working on it and will send a draft this morning.", "我正在处理，今天上午会发草稿。", "Have you started the client summary?", "你开始写客户摘要了吗？"),
                P("on track", "进展正常；按计划进行。", "A phrase that says work is progressing as planned", "We're on track to finish before lunch.", "我们进展正常，午饭前能完成。", "Will the report be ready today?", "报告今天能好吗？"),
                P("behind schedule", "落后于进度。", "A phrase that says a task is taking longer than the planned timeline", "We're behind schedule because we need more data.", "因为还需要更多数据，我们落后于进度。", "Why hasn't the analysis been sent yet?", "分析为什么还没发？"),
                P("almost done", "快完成了。", "A reassuring update that says only a small amount of work remains", "I'm almost done; I just need to check the final numbers.", "我快完成了，只需要核对最后的数字。", "How much is left to do?", "还剩多少要做？"),
            ),
            L(
                4,
                2,
                "clarify-a-request",
                "确认工作要求",
                "Clarify a Request",
                "没听清或不确定任务要求时，用礼貌提问避免做错方向。",
                "通勤中收到一项不够清楚的任务",
                "通勤中收到一项不够清楚的任务。",
                "chat",
                P("just to confirm", "确认一下。", "A phrase used before repeating a detail to make sure it is correct", "Just to confirm, you need the slides by noon?", "确认一下，你中午前需要幻灯片吗？", "Could you send the presentation today?", "你今天能发演示稿吗？"),
                P("could you clarify?", "你能说明得更清楚吗？", "A polite request for more precise information", "Could you clarify which figures you want me to compare?", "你能说明要我比较哪些数据吗？", "Please update the analysis section.", "请更新分析部分。"),
                P("what do you mean by...?", "你说的……是什么意思？", "A question used to ask about the meaning of a specific word or instruction", "What do you mean by a short summary?", "你说的“简短摘要”具体是什么意思？", "Please keep the introduction short.", "请把开头写短一点。"),
                P("let me make sure I understand", "让我确认我理解对了。", "A phrase that introduces your own restatement of an instruction", "Let me make sure I understand: you want the email first, then the report.", "让我确认我理解对了：你想先要邮件，再要报告。", "Please send the email before you finish the report.", "请先发邮件，再完成报告。"),
            ),
            L(
                4,
                3,
                "take-ownership",
                "承担和分配任务",
                "Take Ownership",
                "明确谁来处理某件事，也可以请同事接手更合适的部分。",
                "团队在群里分配紧急任务",
                "团队在群里分配紧急任务。",
                "work",
                P("I'll handle it", "我来处理。", "A confident way to say that you will take responsibility for a task", "I'll handle it and update everyone after the call.", "我来处理，通话后会更新大家。", "Who can speak to the supplier?", "谁能和供应商沟通？"),
                P("can you take this?", "你能接手这个吗？", "A direct but polite request for someone to take responsibility for a task", "Can you take this while I'm on the train?", "我在地铁上时你能先接手这个吗？", "The customer needs an answer before ten.", "客户十点前需要答复。"),
                P("it's on me", "这件事我负责。", "An informal way to accept responsibility for an action or mistake", "It's on me; I'll fix the booking today.", "这件事我负责，今天会把预订改好。", "Who entered the wrong date in the calendar?", "谁把日历里的日期填错了？"),
                P("take the lead", "牵头；带头推进。", "To guide a task or discussion and make sure it moves forward", "Could you take the lead in the client meeting?", "客户会议你能牵头吗？", "We need someone to open the discussion.", "我们需要有人先开启讨论。"),
            ),
            L(
                4,
                4,
                "ask-for-help-at-work",
                "工作中请求帮助",
                "Ask for Help at Work",
                "卡住时说明自己需要什么帮助，而不是只说“我不会”。",
                "地铁上向同事发出求助消息",
                "地铁上向同事发出求助消息。",
                "help",
                P("give me a hand", "帮我一把。", "An informal request for practical help with a task", "Could you give me a hand with the last section?", "你能帮我看一下最后一部分吗？", "I'm nearly finished, but the conclusion needs work.", "我快完成了，但结论还需要修改。"),
                P("I could use some help", "我需要一些帮助。", "A modest way to say that assistance would be useful", "I could use some help checking the numbers.", "我需要一些帮助来核对数字。", "Is everything clear in the spreadsheet?", "表格里的内容都清楚吗？"),
                P("walk me through it", "一步步带我过一遍。", "A request for someone to explain a process step by step", "Can you walk me through it when I get to the office?", "我到办公室后你能一步步带我过一遍吗？", "Have you used the new system before?", "你以前用过这个新系统吗？"),
                P("point me in the right direction", "给我指个方向。", "A request for a useful starting point rather than a full solution", "Could you point me in the right direction for the policy?", "你能告诉我这份政策该从哪里看起吗？", "I'm not sure where the latest policy is stored.", "我不确定最新版政策放在哪里。"),
            ),
            L(
                4,
                5,
                "share-a-work-update",
                "发送工作更新",
                "Share a Work Update",
                "说明自己已经开始、已经发送、等待审核或将继续同步进展。",
                "向团队同步一个正在推进的任务",
                "向团队同步一个正在推进的任务。",
                "work",
                P("I made a start", "我已经开始做了。", "A phrase that says you have begun a task even if it is not finished", "I made a start on the draft during my commute.", "我通勤时已经开始写草稿了。", "Have you had time to begin the draft?", "你有时间开始写草稿了吗？"),
                P("I've sent it over", "我已经发过去了。", "An update that says a requested file or message has been sent", "I've sent it over; please check your inbox.", "我已经发过去了，请查收邮箱。", "Can you send the revised file to me?", "你能把修改后的文件发给我吗？"),
                P("ready for review", "可以审核了。", "A status phrase that says work is complete enough for another person to check", "The draft is ready for review when you have time.", "草稿可以审核了，你有空时看看。", "Is the first version complete?", "第一版完成了吗？"),
                P("share an update", "分享一个更新。", "To give others the latest relevant information about progress", "I'll share an update once the meeting ends.", "会议结束后我会分享一个更新。", "When will we know the final decision?", "我们什么时候能知道最终决定？"),
            ),
            L(
                4,
                6,
                "join-a-meeting",
                "进入会议",
                "Join a Meeting",
                "说明自己能否参加电话会议、如何加入，或为何需要暂时离开。",
                "通勤中协调一场线上会议",
                "通勤中协调一场线上会议。",
                "phone",
                P("join the call", "加入电话会议。", "To enter a phone or video conversation with other people", "I can join the call once I leave the station.", "我出站后就能加入电话会议。", "Will you be able to attend the team call?", "你能参加团队电话会议吗？"),
                P("hop on", "快速加入。", "An informal phrase for joining a call or online meeting quickly", "I'll hop on for the first ten minutes.", "我会快速加入前十分钟。", "Can you join briefly to answer one question?", "你能短暂加入回答一个问题吗？"),
                P("dial in", "拨号加入会议。", "To join a meeting by telephone using a number or access code", "I'll dial in if the video link doesn't load.", "如果视频链接打不开，我会拨号加入。", "What should I do if the meeting app fails?", "如果会议应用打不开，我该怎么办？"),
                P("step away", "暂时离开一下。", "To leave a meeting or task briefly and return later", "I need to step away when my train reaches the terminal.", "我的车到终点时需要暂时离开一下。", "Will you stay on the call for the whole hour?", "你会在电话会上待满一个小时吗？"),
            ),
            L(
                4,
                7,
                "follow-up-and-issues",
                "跟进和问题",
                "Follow Up and Issues",
                "把需要注意的问题说清楚，安排后续跟进，而不让任务停在消息里。",
                "出站前提醒团队一个待处理的问题",
                "出站前提醒团队一个待处理的问题。",
                "help",
                P("flag an issue", "标记一个问题；提醒注意。", "To draw attention to a problem that needs action", "I want to flag an issue with the latest figures.", "我想提醒一下最新数字有个问题。", "Is there anything the team should know before the call?", "通话前团队有什么需要知道的吗？"),
                P("follow up on", "继续跟进。", "To take another action about something that was discussed earlier", "I'll follow up on the supplier's reply tomorrow.", "我明天会继续跟进供应商的回复。", "What happens after we send this message?", "我们发出这条消息后要做什么？"),
                P("raise a question", "提出一个问题。", "To bring a question or concern into a discussion", "I'd like to raise a question about the deadline.", "我想就截止日期提一个问题。", "Is everyone comfortable with Friday?", "大家都能接受周五吗？"),
                P("circle back", "之后再回头讨论。", "To return to a topic after more information or time is available", "Let's circle back after I check the contract.", "等我查看合同后我们再回头讨论。", "Can we decide on this point now?", "我们现在能决定这个点吗？"),
            ),
            L(
                4,
                8,
                "work-message-challenge",
                "工作消息实战",
                "Work Message Challenge",
                "在一段短消息里给出最新情况、补充问题并确保大家对齐。",
                "到办公室前发送最后一条团队消息",
                "到办公室前发送最后一条团队消息。",
                "work",
                P("here's the latest", "最新情况是这样的。", "A phrase that introduces the most recent information", "Here's the latest: the client approved the outline.", "最新情况是：客户批准了大纲。", "Has the client replied yet?", "客户回复了吗？"),
                P("one quick thing", "还有一件小事。", "A phrase used to add one brief but important point", "One quick thing: the deadline is now Thursday.", "还有一件小事：截止日期改到周四了。", "Is there anything else we should know?", "还有什么我们需要知道的吗？"),
                P("I've got a question", "我有个问题。", "A natural introduction before asking for information or clarification", "I've got a question about the final slide.", "我有个关于最后一页幻灯片的问题。", "Do you need anything from me before the meeting?", "会议前你需要我做什么吗？"),
                P("let's get aligned", "我们先对齐一下。", "A collaborative phrase used to make sure people share the same understanding", "Let's get aligned before we send the proposal.", "我们发提案前先对齐一下。", "Should we send the draft now?", "我们现在要发草稿吗？"),
            ),
        ),
    ),
    Chapter(
        5,
        "日常生活安排",
        "Everyday Arrangements",
        "把下班后的吃饭、购物、预约、家庭和配送安排说得清楚简洁。",
        "food",
        (
            L(
                5,
                1,
                "make-a-food-plan",
                "约饭",
                "Make a Food Plan",
                "在车上快速约饭、选择外食或外带，并表达自己是否还吃得下。",
                "下班路上和朋友讨论晚饭",
                "下班路上和朋友讨论晚饭。",
                "food",
                P("grab a bite", "吃点东西；简单吃一口。", "An informal way to suggest having a quick meal", "Do you want to grab a bite after work?", "你下班后想简单吃点东西吗？", "I'm hungry, but I don't have much time.", "我饿了，但时间不多。"),
                P("eat out", "出去吃。", "To have a meal at a restaurant rather than at home", "Let's eat out instead of cooking tonight.", "我们今晚出去吃吧，不做饭了。", "Do you want to cook or go somewhere?", "你想做饭还是出去吃？"),
                P("get it to go", "打包带走。", "To order food to take away rather than eat at the restaurant", "I'll get it to go and eat when I get home.", "我会打包带走，回家再吃。", "Do you want to sit here or take the food home?", "你想坐在这里吃还是带回家？"),
                P("save room", "留点肚子。", "To avoid eating too much because more food is coming later", "Save room; we're sharing dessert later.", "留点肚子，我们等会儿要一起吃甜点。", "Should I order another snack now?", "我现在要不要再点一份小吃？"),
            ),
            L(
                5,
                2,
                "shop-with-confidence",
                "购物沟通",
                "Shop with Confidence",
                "购买前问库存、试穿、结账或处理不合适的商品。",
                "下班路上确认商店里要买的东西",
                "下班路上确认商店里要买的东西。",
                "chat",
                P("out of stock", "缺货。", "A phrase that says a product is not currently available to buy", "The size I need is out of stock online.", "我需要的尺码网上缺货。", "Can you order the jacket for me?", "你能帮我订那件夹克吗？"),
                P("try it on", "试穿。", "To put on clothing to see whether it fits or looks right", "I'll try it on before I decide.", "我试穿后再决定。", "Do you want to buy the coat now?", "你现在想买这件外套吗？"),
                P("check out", "结账。", "To pay for items and finish a purchase", "I'll check out once I find the right size.", "我找到合适尺码后就结账。", "Are you still shopping?", "你还在逛吗？"),
                P("get a refund", "退款。", "To receive your money back for something you return", "I need to get a refund because the item arrived damaged.", "东西到货时已经损坏了，我需要退款。", "What should I do with the broken item?", "这个坏掉的商品我该怎么办？"),
            ),
            L(
                5,
                3,
                "manage-an-appointment",
                "预约安排",
                "Manage an Appointment",
                "预订、确认、争取空位，或在临时有事时取消预约。",
                "通勤中安排看医生或理发时间",
                "通勤中安排看医生或理发时间。",
                "clock",
                P("book an appointment", "预约。", "To arrange a specific time to see a professional or use a service", "I'd like to book an appointment for Friday afternoon.", "我想预约周五下午。", "When would you like to see the dentist?", "你想什么时候看牙医？"),
                P("confirm the time", "确认时间。", "To check that an agreed appointment time is still correct", "Could you confirm the time by text?", "你能短信确认一下时间吗？", "I wrote down Tuesday at three.", "我记的是周二三点。"),
                P("fit me in", "给我挤出一个时间。", "To find an available time for someone in a busy schedule", "Could you fit me in after five?", "五点后你能给我挤出一个时间吗？", "The clinic is fully booked today.", "诊所今天预约满了。"),
                P("cancel at short notice", "临时取消。", "To cancel something with very little warning time", "I'm sorry to cancel at short notice; my train has stopped.", "很抱歉临时取消，我的地铁停了。", "Are you still able to make your appointment?", "你还能赶上预约吗？"),
            ),
            L(
                5,
                4,
                "home-and-family-tasks",
                "家庭事务",
                "Home and Family Tasks",
                "告诉家人自己在办事、会晚到，或正在照顾某件事情。",
                "回家路上协调家务和家庭安排",
                "回家路上协调家务和家庭安排。",
                "friends",
                P("run an errand", "跑一趟办点事。", "To make a short trip to complete a practical task", "I need to run an errand before I come home.", "我回家前得去办点事。", "Will you be home right after work?", "你下班后会直接回家吗？"),
                P("take care of", "处理；照顾好。", "To deal with a task or responsibility so it is no longer a problem", "I'll take care of the grocery order on my way home.", "我回家路上会处理好杂货订单。", "Who is ordering dinner tonight?", "今晚谁来订晚饭？"),
                P("make it home", "平安到家；赶回家。", "To arrive home, especially after a long or difficult trip", "I won't make it home before eight tonight.", "我今晚八点前到不了家。", "What time do you think you'll be back?", "你觉得几点能回来？"),
                P("look after", "照看；照顾。", "To care for a person, animal or thing that needs attention", "Can you look after the dog until I get home?", "我到家前你能照看一下狗吗？", "Who will feed the dog this evening?", "今晚谁喂狗？"),
            ),
            L(
                5,
                5,
                "make-evening-plans",
                "安排晚上",
                "Make Evening Plans",
                "预订、暂缓、想办法协调，或给晚上留出时间。",
                "朋友在消息里敲定周末安排",
                "朋友在消息里敲定周末安排。",
                "clock",
                P("make a reservation", "预订座位。", "To arrange a table, ticket or place before you arrive", "I'll make a reservation for seven thirty.", "我会预订七点半的座位。", "Should we book the restaurant before it fills up?", "我们要不要趁餐厅订满前先预订？"),
                P("put it on hold", "先搁置；暂缓处理。", "To delay a decision or action until you have more information", "Let's put it on hold until everyone replies.", "等大家都回复后，我们先把这件事搁置。", "Should we buy the tickets now?", "我们现在要买票吗？"),
                P("work something out", "想出一个办法。", "To find a practical solution through discussion", "I'm sure we can work something out for Saturday.", "我相信我们能为周六想出一个办法。", "My shift ends later than expected.", "我的班比预想结束得晚。"),
                P("keep the evening free", "晚上空出来。", "To avoid making plans so you remain available later", "I'll keep the evening free in case we need to reschedule.", "我会把晚上空出来，以防我们需要改时间。", "Are you available if the meeting moves to tonight?", "如果会议改到今晚，你有空吗？"),
            ),
            L(
                5,
                6,
                "track-a-delivery",
                "处理配送",
                "Track a Delivery",
                "说明包裹在哪、是否到门口、谁需要签收以及预计到达时间。",
                "地铁上跟家人确认一个快递",
                "在地铁上跟家人确认一个快递。",
                "route",
                P("on the doorstep", "在门口台阶上。", "A phrase that says a delivery has been left immediately outside a door", "The parcel is on the doorstep, according to the photo.", "根据照片，包裹在门口台阶上。", "Did the delivery arrive already?", "快递已经到了吗？"),
                P("track a package", "追踪包裹。", "To check a delivery's current location and expected arrival", "You can track the package with the order number.", "你可以用订单号追踪包裹。", "How do I know where the parcel is?", "我怎么知道包裹到哪里了？"),
                P("sign for it", "签收。", "To write your name to confirm that you received a delivery", "Can someone sign for it if it arrives before I do?", "如果它比我先到，有人能帮忙签收吗？", "The courier needs a signature.", "快递员需要签名。"),
                P("arrive by", "在……之前到达。", "To be delivered no later than a stated time", "The package should arrive by six.", "包裹应该六点前到。", "When should the order reach the house?", "订单大概什么时候到家？"),
            ),
            L(
                5,
                7,
                "daily-plan-review",
                "日常安排复习",
                "Daily Plan Review",
                "当时间不够时，挤出时间、腾出时间、围绕限制安排并做出选择。",
                "一边通勤一边重排当晚的事项",
                "一边通勤一边重排当晚的事项。",
                "clock",
                P("squeeze in", "挤出时间做。", "To find a small amount of time for something in a busy day", "I can squeeze in a quick grocery stop after work.", "下班后我能挤出时间快速买个菜。", "Do you have time to collect the package today?", "你今天有时间取包裹吗？"),
                P("free up", "腾出时间；空出来。", "To make time available by finishing or moving something else", "I can free up an hour after dinner.", "晚饭后我能腾出一个小时。", "When will you have time to talk?", "你什么时候有时间说话？"),
                P("plan around", "围绕……来安排。", "To organize activities while taking a limit or fixed event into account", "Let's plan around your appointment tomorrow.", "我们围绕你明天的预约来安排吧。", "I have a dentist appointment at four.", "我四点有牙医预约。"),
                P("settle on", "最终确定为。", "To choose one option after considering several possibilities", "Let's settle on the café near your station.", "我们最终定在你车站附近的咖啡馆吧。", "There are three places we could meet.", "我们可以见面的地方有三个。"),
            ),
            L(
                5,
                8,
                "daily-life-challenge",
                "日常安排实战",
                "Everyday Plan Challenge",
                "自然地婉拒、放松对方、邀请加入，或结束一天的安排。",
                "周五傍晚临时改变聚会计划",
                "周五傍晚临时改变聚会计划。",
                "friends",
                P("take a rain check", "改天再约。", "A friendly way to decline an invitation now while suggesting another time", "Can I take a rain check? I'm exhausted today.", "我能改天再约吗？我今天太累了。", "Do you want to meet after work tonight?", "你今晚下班后想见面吗？"),
                P("no rush", "不着急。", "A reassuring phrase that says someone can take their time", "No rush; we can decide after you get home.", "不着急，你到家后我们再决定。", "I need a few minutes to check my schedule.", "我需要几分钟看一下日程。"),
                P("come along", "一起来。", "An invitation to join people who are going somewhere", "Come along if you're free after your appointment.", "你预约结束后有空就一起来吧。", "We're going to the market after dinner.", "我们晚饭后要去市场。"),
                P("call it a day", "今天就到这里。", "To decide to stop working or doing an activity for the day", "Let's call it a day and finish the rest tomorrow.", "我们今天就到这里，剩下的明天完成。", "Do you want to keep planning tonight?", "你想今晚继续安排吗？"),
            ),
        ),
    ),
    Chapter(
        6,
        "请求帮助与解决问题",
        "Ask for Help and Solve Problems",
        "遇到找路、交通、账号或设备问题时，准确说出困难并推进解决。",
        "help",
        (
            L(
                6,
                1,
                "ask-for-directions",
                "问路",
                "Ask for Directions",
                "主动说明你要去哪里，问清方向、距离和线路是否正确。",
                "在换乘站向工作人员问路",
                "在换乘站向工作人员问路。",
                "pin",
                P("point me to", "告诉我去……的方向。", "A polite request for directions to a place", "Could you point me to platform five?", "你能告诉我五号站台怎么走吗？", "I need to change to the airport line.", "我需要换乘机场线。"),
                P("which way is", "……往哪边走？", "A direct question asking for the direction of a place", "Which way is the museum from here?", "从这里去博物馆往哪边走？", "I just left the station and can't see the signs.", "我刚出站，看不到指示牌。"),
                P("how far is", "……有多远？", "A question used to ask about distance or walking time", "How far is the hotel from this exit?", "酒店离这个出口有多远？", "Should I walk or take a bus?", "我该走路还是坐公交？"),
                P("is this the right line?", "这是正确的线路吗？", "A question that checks whether you are on the correct train or route", "Is this the right line for Riverside?", "这是去 Riverside 的正确线路吗？", "The display changed while I was boarding.", "我上车时显示屏变了。"),
            ),
            L(
                6,
                2,
                "handle-a-transport-delay",
                "处理交通延误",
                "Handle a Transport Delay",
                "错过列车或线路延误时，解释情况并给出下一步。",
                "早高峰遇到地铁延误",
                "早高峰遇到地铁延误。",
                "route",
                P("missed the train", "错过列车。", "A phrase that says you did not board before a train left", "I missed the train, so I'll take the next one.", "我错过了这趟车，所以会坐下一班。", "Why will you arrive later than usual?", "你为什么会比平时晚到？"),
                P("service is delayed", "线路服务延误。", "A status message that says public transport is running late", "The service is delayed because of a signal problem.", "因为信号问题，线路服务延误。", "Why has the train stopped between stations?", "列车为什么停在两站之间？"),
                P("take a detour", "绕路走。", "To use a longer or different route because the normal one is unavailable", "I'll take a detour through the next station.", "我会绕路经过下一站。", "The usual exit is closed today.", "今天常用出口关闭了。"),
                P("catch the next one", "赶下一班。", "To take the following train, bus or opportunity instead of the one you missed", "Don't wait for me; I'll catch the next one.", "别等我，我坐下一班。", "The doors just closed before I reached the platform.", "我到站台前门刚关上。"),
            ),
            L(
                6,
                3,
                "fix-an-access-problem",
                "解决登录问题",
                "Fix an Access Problem",
                "账户或门禁出问题时，说清楚无法进入、需要重置或需要权限。",
                "上班路上发现无法登录工作系统",
                "上班路上发现无法登录工作系统。",
                "work",
                P("I can't get in", "我进不去。", "A simple way to say that you cannot enter a place, account or system", "I can't get in to the shared folder.", "我进不去共享文件夹。", "Can you open the project files?", "你能打开项目文件吗？"),
                P("reset my password", "重置我的密码。", "To create a new password after the old one no longer works", "I need to reset my password before the meeting.", "开会前我需要重置密码。", "Why can't you sign in to the dashboard?", "你为什么登录不了仪表盘？"),
                P("sign in", "登录。", "To enter an account or system with your credentials", "I can sign in on my phone but not on my laptop.", "我手机能登录，但笔记本不行。", "Does the new password work everywhere?", "新密码在所有设备上都能用吗？"),
                P("get access", "获得访问权限。", "To receive permission to use a file, system or place", "Could you help me get access to the folder?", "你能帮我获得这个文件夹的访问权限吗？", "The team added you to the project yesterday.", "团队昨天把你加进项目了。"),
            ),
            L(
                6,
                4,
                "describe-a-problem",
                "描述问题",
                "Describe a Problem",
                "让对方快速理解哪里出错、页面有什么表现，以及你需要什么协助。",
                "地铁上向技术同事说明一个页面故障",
                "在地铁上向技术同事说明一个页面故障。",
                "help",
                P("something went wrong", "出问题了。", "A broad but useful way to say that a process did not work as expected", "Something went wrong when I submitted the form.", "我提交表单时出问题了。", "Did the confirmation screen appear?", "确认页面出现了吗？"),
                P("it won't load", "它加载不出来。", "A phrase that says a page, file or app refuses to open", "The dashboard won't load on my phone.", "仪表盘在我手机上加载不出来。", "Can you see the latest report?", "你能看到最新报告吗？"),
                P("I'm having trouble", "我遇到困难。", "A polite lead-in before explaining what is difficult", "I'm having trouble uploading the document.", "我上传文档时遇到困难。", "Is the upload button working for you?", "上传按钮对你来说能用吗？"),
                P("could you check it?", "你能检查一下吗？", "A direct request for someone to inspect a problem", "Could you check it when you have a moment?", "你有空时能检查一下吗？", "The payment page looks different today.", "今天付款页面看起来不一样。"),
            ),
            L(
                6,
                5,
                "move-toward-a-fix",
                "推进解决",
                "Move Toward a Fix",
                "提出要处理、调查、弄明白或修好问题，让对方知道下一步。",
                "团队在群里处理一个紧急故障",
                "团队在群里处理一个紧急故障。",
                "help",
                P("sort it out", "把它解决好。", "To resolve a confusing or difficult situation", "I'll sort it out when I reach a computer.", "我到电脑前就把它解决好。", "Can someone fix the booking before noon?", "有人能在中午前修好预订吗？"),
                P("investigate", "调查；查明。", "To examine a problem carefully to discover its cause", "We'll investigate why the payment failed.", "我们会调查付款为什么失败。", "Do we know what caused the error?", "我们知道错误是怎么造成的吗？"),
                P("figure it out", "弄明白；想出办法。", "To understand a problem or find a solution after thinking about it", "Give me ten minutes and I'll figure it out.", "给我十分钟，我会弄明白。", "Do you know which setting changed?", "你知道哪个设置变了吗？"),
                P("get it fixed", "把它修好。", "To arrange for a problem to be repaired or corrected", "We need to get it fixed before customers see it.", "我们需要在客户看到之前把它修好。", "Can the broken link stay up until tomorrow?", "那个坏链接能一直放到明天吗？"),
            ),
            L(
                6,
                6,
                "thank-someone",
                "表达感谢",
                "Thank Someone",
                "别人给出帮助后，用不同程度的感谢和轻松回应让对话自然收尾。",
                "同事帮你处理了一个临时问题",
                "同事帮你处理了一个临时问题。",
                "friends",
                P("I appreciate it", "我很感激。", "A sincere way to thank someone for their time or help", "I really appreciate it; that saved me a lot of time.", "我真的很感激，这帮我省了很多时间。", "I updated the document for you.", "我帮你更新了文档。"),
                P("that helps a lot", "这帮了大忙。", "A response that says someone's action has made a real difference", "That helps a lot. I can finish the rest on the train.", "这帮了大忙，剩下的我可以在地铁上完成。", "I found the correct link for you.", "我帮你找到了正确链接。"),
                P("you're a lifesaver", "你真是救星。", "A warm informal thank-you for help at an important moment", "You're a lifesaver; I was about to miss the deadline.", "你真是救星，我差点赶不上截止日期。", "I sent you the file just before the meeting.", "我在开会前刚好把文件发给你。"),
                P("no worries", "没事；不用客气。", "A relaxed response that says the help was not a problem", "No worries. I'm glad it worked out.", "没事，很高兴事情解决了。", "Thanks for staying late to help me.", "谢谢你留下来帮我。"),
            ),
            L(
                6,
                7,
                "help-and-problem-review",
                "求助复习",
                "Help and Problem Review",
                "把请求、尝试和下一步说清楚，让对方更容易帮到你。",
                "在路上向朋友请求一个小帮助",
                "在路上向朋友请求一个小帮助。",
                "help",
                P("do me a favor", "帮我个忙。", "An informal way to ask someone for a helpful action", "Could you do me a favor and hold the door?", "你能帮我个忙，帮我扶一下门吗？", "I'm carrying a bag and can't use both hands.", "我拿着包，没法同时腾出两只手。"),
                P("give it a try", "试试看。", "An encouraging suggestion to attempt something before giving up", "Give it a try with the new password first.", "先用新密码试试看。", "I'm not sure the link will open on my phone.", "我不确定这个链接在手机上能不能打开。"),
                P("let me know if", "如果……请告诉我。", "A phrase that invites someone to report a problem or change", "Let me know if the train is cancelled again.", "如果地铁又取消了请告诉我。", "I'll check the service board at the next stop.", "我下一站会看服务公告板。"),
                P("check it over", "检查一遍。", "To review something carefully for mistakes or missing details", "Could you check it over before I send it?", "我发送前你能检查一遍吗？", "I finished the form on my phone.", "我在手机上填完表格了。"),
            ),
            L(
                6,
                8,
                "problem-solving-challenge",
                "问题解决实战",
                "Problem-Solving Challenge",
                "在被打断时求助、补发信息、承认遗漏，并礼貌结束对话。",
                "通勤途中发现自己漏掉了一条重要消息",
                "通勤途中发现自己漏掉了一条重要消息。",
                "chat",
                P("I'm stuck", "我卡住了；我不知道怎么继续。", "A direct way to say that you cannot make progress without help", "I'm stuck on the last step of the form.", "我卡在表格的最后一步了。", "Have you been able to submit the request?", "你能提交这个请求了吗？"),
                P("could you resend it?", "你能再发一次吗？", "A polite request for someone to send a message or file again", "Could you resend it? The attachment disappeared.", "你能再发一次吗？附件不见了。", "Did the document arrive in your inbox?", "文档到你的邮箱了吗？"),
                P("it slipped my mind", "我忘了。", "A natural way to admit that you forgot something without making a big excuse", "It slipped my mind; I'll add it to the calendar now.", "我忘了，我现在就把它加到日历里。", "Did you remember to confirm the appointment?", "你记得确认预约了吗？"),
                P("thanks anyway", "不管怎样还是谢谢。", "A polite thank-you when someone tried to help but could not solve the problem", "Thanks anyway; I'll ask the help desk when I arrive.", "不管怎样还是谢谢，我到后会问服务台。", "I can't see the setting you need on my phone.", "我手机上看不到你需要的设置。"),
            ),
        ),
    ),
    Chapter(
        7,
        "朋友和社交",
        "Friends and Social Life",
        "在通勤的碎片时间里自然邀约、接受或婉拒，也能关心朋友、保持联系。",
        "friends",
        (
            L(
                7,
                1,
                "make-an-invitation",
                "发出邀请",
                "Make an Invitation",
                "用不强迫的方式邀请朋友一起吃饭、参加活动或到家里坐坐。",
                "下班路上邀请朋友周末见面",
                "下班路上邀请朋友周末见面。",
                "friends",
                P("are you up for", "你想不想；你有兴趣吗。", "A casual question asking whether someone wants to do something", "Are you up for coffee after work?", "你下班后想喝杯咖啡吗？", "I have an hour free before I go home.", "我回家前有一个小时空闲。"),
                P("want to join us?", "想和我们一起吗？", "A friendly invitation to become part of a group plan", "We're going to the market. Want to join us?", "我们要去市场，你想和我们一起吗？", "A few of us are meeting near the station.", "我们几个人要在车站附近见面。"),
                P("feel like", "想不想；有没有心情。", "A casual phrase used to ask what someone wants to do", "Do you feel like watching a film tonight?", "你今晚想看电影吗？", "I don't have any fixed plans after dinner.", "我晚饭后没有固定安排。"),
                P("come over", "过来我这儿。", "To visit someone at their home or current place", "Come over when you finish work if you're free.", "如果你有空，下班后过来吧。", "I'd like to show you the new apartment.", "我想让你看看新公寓。"),
            ),
            L(
                7,
                2,
                "accept-an-invitation",
                "接受邀请",
                "Accept an Invitation",
                "高兴地答应邀请，并让对方知道自己愿意加入。",
                "在车上回复朋友的周末邀请",
                "在车上回复朋友的周末邀请。",
                "friends",
                P("I'd love to", "我很愿意。", "A warm and enthusiastic way to accept an invitation", "I'd love to come to dinner on Saturday.", "我很愿意周六来吃晚饭。", "Would you like to come over this weekend?", "你这个周末想过来吗？"),
                P("I'm in", "我参加；算我一个。", "A short informal way to say you want to join a plan", "I'm in. Send me the time and place.", "我参加，把时间和地点发给我吧。", "We're booking tickets for the concert.", "我们要订音乐会门票。"),
                P("sounds like fun", "听起来很好玩。", "A response that shows a plan sounds enjoyable", "That sounds like fun. I've never been there.", "听起来很好玩，我还没去过那里。", "We're trying a new food market after work.", "我们下班后要去一家新的美食市场。"),
                P("I'd be happy to", "我很乐意。", "A polite and positive way to agree to help or take part", "I'd be happy to help you move on Sunday.", "我很乐意周日帮你搬家。", "Could you help me carry a few boxes?", "你能帮我搬几个箱子吗？"),
            ),
            L(
                7,
                3,
                "decline-kindly",
                "礼貌婉拒",
                "Decline Kindly",
                "不能参加时，表达遗憾、说明已有安排，并把关系留在下一次。",
                "通勤中婉拒一个临时邀请",
                "在通勤中婉拒一个临时邀请。",
                "chat",
                P("I wish I could", "真希望我能去。", "A warm expression of regret when you cannot accept an invitation", "I wish I could, but I already have plans tonight.", "真希望我能去，但我今晚已经有安排了。", "We're meeting for dinner in an hour.", "我们一小时后要去吃晚饭。"),
                P("I have other plans", "我有别的安排。", "A straightforward but polite reason for declining", "I have other plans this weekend, unfortunately.", "很遗憾，我这个周末有别的安排。", "Can you come to the picnic on Sunday?", "你周日能来野餐吗？"),
                P("maybe another time", "下次吧。", "A gentle way to suggest a future opportunity after saying no now", "Maybe another time? I'd still like to catch up.", "下次吧？我还是很想和你聊聊。", "No problem if tonight is too busy.", "如果今晚太忙也没关系。"),
                P("I'll have to pass", "这次我得不参加了。", "An informal but clear way to decline a plan", "I'll have to pass tonight; I need an early night.", "今晚我得不参加了，我需要早点休息。", "Are you joining the late movie?", "你会来参加晚场电影吗？"),
            ),
            L(
                7,
                4,
                "check-in-with-a-friend",
                "关心朋友",
                "Check In with a Friend",
                "很久没联系时，用自然问题重新打开一段关心对话。",
                "地铁上给久未联系的朋友发消息",
                "在地铁上给久未联系的朋友发消息。",
                "chat",
                P("how have you been?", "你最近怎么样？", "A friendly question about someone's life since you last spoke", "How have you been? It's been far too long.", "你最近怎么样？我们太久没聊了。", "I saw your photo from the weekend.", "我看到你周末的照片了。"),
                P("how's everything?", "一切都好吗？", "A broad, caring question about someone's current situation", "How's everything at your new job?", "你新工作一切都好吗？", "You started somewhere new last month.", "你上个月开始了新工作。"),
                P("just checking in", "就是来问候一下。", "A phrase that says you are contacting someone to see how they are", "Just checking in to see how your interview went.", "就是来问候一下，看看你的面试怎么样了。", "I know you had an important interview today.", "我知道你今天有个重要面试。"),
                P("it's been a while", "好久不见；好久没联系。", "A natural opener when you have not seen or spoken to someone for some time", "It's been a while. We should meet for coffee soon.", "好久没联系了，我们应该很快见面喝杯咖啡。", "I haven't seen you since the old office closed.", "自从老办公室关闭后我就没见过你。"),
            ),
            L(
                7,
                5,
                "support-a-friend",
                "支持朋友",
                "Support a Friend",
                "朋友压力大或遇到困难时，给出不空泛而有温度的回应。",
                "朋友在消息里说今天过得很难",
                "朋友在消息里说今天过得很难。",
                "friends",
                P("I'm here for you", "我在这里支持你。", "A caring phrase that tells someone they can rely on you", "I'm here for you if you want to talk later.", "如果你晚点想聊，我会在这里支持你。", "Today has been really overwhelming.", "今天真的压力很大。"),
                P("take it easy", "别太累；慢一点来。", "A kind suggestion to rest or avoid putting too much pressure on yourself", "Take it easy tonight and get some rest.", "今晚别太累，好好休息。", "I have been working since early this morning.", "我从今天一早就一直在工作。"),
                P("that sounds hard", "听起来不容易。", "An empathetic response that recognises someone is facing difficulty", "That sounds hard. Do you want to tell me more?", "听起来不容易，你想多说一点吗？", "My manager changed the plan at the last minute.", "我的经理最后一刻改了计划。"),
                P("you've got this", "你能做到。", "An encouraging phrase that expresses confidence in someone", "You've got this. One step at a time.", "你能做到，一步一步来。", "I'm nervous about presenting tomorrow.", "我对明天的演讲很紧张。"),
            ),
            L(
                7,
                6,
                "build-a-connection",
                "建立联系",
                "Build a Connection",
                "说出和某人相处得来、共同点多，或想在之后继续联系。",
                "下班路上聊起一位新认识的同事",
                "下班路上聊起一位新认识的同事。",
                "friends",
                P("get along", "相处得来。", "To have a friendly and comfortable relationship with someone", "We get along really well at work.", "我们在工作中相处得很好。", "How is your new teammate?", "你的新队友怎么样？"),
                P("have a lot in common", "有很多共同点。", "To share many interests, experiences or opinions with someone", "We have a lot in common, especially about travel.", "我们有很多共同点，尤其是旅行方面。", "Did you enjoy talking to your new neighbour?", "你和新邻居聊得开心吗？"),
                P("catch up with", "和……聊聊近况。", "To spend time talking with someone about recent events in their life", "I'd like to catch up with you after work sometime.", "我想找个时间下班后和你聊聊近况。", "We haven't spoken since last summer.", "我们从去年夏天后就没聊过。"),
                P("stay in touch", "保持联系。", "To continue communicating with someone over time", "Let's stay in touch after you move.", "你搬走后我们也保持联系吧。", "I'm leaving the team next month.", "我下个月要离开团队。"),
            ),
            L(
                7,
                7,
                "social-review",
                "社交复习",
                "Social Review",
                "把邀请、招待和陪伴自然地放进一段轻松的对话。",
                "朋友到你附近来办事，想顺路见面",
                "朋友到你附近来办事，想顺路见面。",
                "friends",
                P("keep me company", "陪陪我。", "A request for someone to spend time with you so you are not alone", "Keep me company while I wait for the next train.", "我等下一班车时陪我聊聊吧。", "I have a long wait at the station.", "我在车站要等很久。"),
                P("make yourself at home", "别拘束，当自己家。", "A welcoming phrase that makes a guest feel comfortable", "Make yourself at home while I finish dinner.", "我做完晚饭前你别拘束，当自己家。", "Should I wait in the kitchen or the living room?", "我该在厨房还是客厅等？"),
                P("bring someone along", "带个人一起来。", "To invite someone to bring another person with them", "Feel free to bring someone along to the picnic.", "野餐时你随时可以带个人一起来。", "My sister would like to join us too.", "我妹妹也想加入我们。"),
                P("be up for it", "愿意参加；有心情做。", "To be willing and interested enough to do something", "I'd be up for it after a quiet evening.", "安静休息一晚后，我愿意参加。", "Would you like to go hiking on Sunday?", "你周日想去徒步吗？"),
            ),
            L(
                7,
                8,
                "social-message-challenge",
                "社交消息实战",
                "Social Message Challenge",
                "无法马上赶到时，说清楚自己会什么时候加入，并保持双方联系。",
                "朋友已经到聚会地点，你还在地铁上",
                "朋友已经到了聚会地点，你还在地铁上。",
                "route",
                P("I'll join you later", "我晚点加入你们。", "A promise to meet people after they have already started", "I'll join you later when I get off the train.", "我下地铁后晚点加入你们。", "We're starting dinner now.", "我们现在开始吃晚饭了。"),
                P("let's make a plan", "我们定个计划吧。", "A friendly suggestion to choose a time or activity together", "Let's make a plan for next week instead.", "我们改成下周定个计划吧。", "This weekend is too busy for both of us.", "这个周末我们俩都太忙了。"),
                P("don't wait up", "别等我。", "A request that tells someone not to stay awake or delay because of you", "Don't wait up; this delay could take a while.", "别等我了，这次延误可能会持续一会儿。", "Will you be home for dinner?", "你会回家吃晚饭吗？"),
                P("text me when you arrive", "你到了给我发消息。", "A request for a message after someone reaches their destination", "Text me when you arrive so I know you're safe.", "你到了给我发消息，这样我就知道你平安了。", "I'm leaving the station now.", "我现在要离开车站了。"),
            ),
        ),
    ),
    Chapter(
        8,
        "电话与语音沟通",
        "Calls and Voice Messages",
        "在车厢、站台和出站路上清楚处理电话、听不清和留言场景。",
        "phone",
        (
            L(
                8,
                1,
                "start-a-call",
                "开始通话",
                "Start a Call",
                "打电话前先确认时机，说明来意，必要时提出稍后回拨。",
                "下班路上接到一通工作电话",
                "下班路上接到一通工作电话。",
                "phone",
                P("is now a good time?", "现在方便吗？", "A considerate question asked before starting a conversation", "Is now a good time to talk for two minutes?", "现在方便聊两分钟吗？", "I need to ask you about tomorrow's meeting.", "我需要问你明天会议的事。"),
                P("I'm calling about", "我打电话是想说……", "A phrase that clearly states the reason for a phone call", "I'm calling about the change to tomorrow's schedule.", "我打电话是想说一下明天日程的变化。", "Why did you call while I was on the train?", "你为什么在我坐地铁时打电话？"),
                P("could I call you back?", "我能晚点回拨给你吗？", "A polite question used when you cannot talk properly now", "Could I call you back when I leave the station?", "我出站后能回拨给你吗？", "Can we discuss the details right now?", "我们现在能讨论细节吗？"),
                P("hold the line", "请别挂断。", "A request for someone to stay connected while you deal with something briefly", "Hold the line; I'm moving to a quieter carriage.", "请别挂断，我正往安静一点的车厢走。", "Can you hear me over the train noise?", "隔着地铁噪音你能听见我吗？"),
            ),
            L(
                8,
                2,
                "fix-audio-problems",
                "听不清时",
                "Fix Audio Problems",
                "当电话声音断续或听不清时，明确说出发生了什么并请对方调整。",
                "地铁上通话的声音不稳定",
                "地铁上通话的声音不稳定。",
                "signal",
                P("you're breaking up", "你的声音断断续续。", "A phrase that says the other person's audio is cutting in and out", "You're breaking up; I only caught the first part.", "你的声音断断续续，我只听到了前半部分。", "Did you hear the new time I mentioned?", "你听到我说的新时间了吗？"),
                P("I can't make that out", "我听不清那个。", "A polite way to say that words or sounds are not understandable", "I can't make that out with the train noise.", "有地铁噪音，我听不清那个。", "The platform number is twelve.", "站台号是十二。"),
                P("speak a bit louder", "说大声一点。", "A request for someone to increase their speaking volume slightly", "Could you speak a bit louder for the last number?", "最后那个数字你能说大声一点吗？", "I'll tell you the booking code now.", "我现在告诉你预订代码。"),
                P("the audio keeps cutting out", "声音一直断。", "A description of repeated interruptions in sound during a call", "The audio keeps cutting out in this tunnel.", "这个隧道里声音一直断。", "Should we keep trying to talk?", "我们要继续努力通话吗？"),
            ),
            L(
                8,
                3,
                "take-and-pass-messages",
                "留言和转达",
                "Take and Pass Messages",
                "无法直接接通时，帮人记录、转达和设法联系到正确的人。",
                "在车上替同事处理一通转来的电话",
                "在车上替同事处理一通转来的电话。",
                "phone",
                P("take a message", "记个口信。", "To write down information for someone who is unavailable", "I can take a message and pass it on.", "我可以记个口信再转达。", "Jordan is away from the desk right now.", "Jordan 现在不在桌前。"),
                P("pass it along", "转达给他。", "To give information or a message to the intended person", "I'll pass it along as soon as I see her.", "我一见到她就转达。", "Could you tell Mia that the time changed?", "你能告诉 Mia 时间改了吗？"),
                P("get through to", "联系上；接通。", "To successfully reach a person by phone or another connection", "I couldn't get through to the clinic this morning.", "我今天早上没能打通诊所电话。", "Did anyone answer when you called the office?", "你打办公室电话时有人接吗？"),
                P("call someone back", "回拨给某人。", "To return a phone call after you missed or ended one", "I'll call her back when I get above ground.", "我到地面后会回拨给她。", "Mia left you a missed call.", "Mia 给你打过电话但你没接到。"),
            ),
            L(
                8,
                4,
                "clarify-on-the-phone",
                "电话里确认细节",
                "Clarify on the Phone",
                "遇到号码、地址或指令时，请对方重复、拼写、放慢或留出记录时间。",
                "在通话中记录预订和地址信息",
                "在通话中记录预订和地址信息。",
                "phone",
                P("could you repeat that?", "你能再说一遍吗？", "A polite request to hear the same information again", "Could you repeat that? I missed the street name.", "你能再说一遍吗？我没听到街道名。", "The address is 18 Franklin Road.", "地址是 Franklin Road 18 号。"),
                P("did you say...?", "你刚才说的是……吗？", "A checking question used to confirm a word, number or detail you heard", "Did you say fifteen or fifty?", "你刚才说的是十五还是五十？", "The code starts with one-five.", "代码开头是一五。"),
                P("let me write that down", "让我记下来。", "A phrase used to pause while recording important information", "Let me write that down before you continue.", "你继续前让我先记下来。", "There are two reference numbers you need.", "你需要记两个参考号码。"),
                P("slow down a little", "稍微说慢一点。", "A polite request for someone to reduce their speaking speed", "Could you slow down a little when you read the number?", "你读号码时能稍微慢一点吗？", "I'll spell the surname for you now.", "我现在拼写姓氏给你听。"),
            ),
            L(
                8,
                5,
                "manage-voicemail",
                "处理未接来电",
                "Manage Voicemail",
                "错过电话后说明原因、请对方留下号码或录音，并及时查看语音信箱。",
                "地铁里错过一个重要来电",
                "在地铁里错过一个重要来电。",
                "phone",
                P("I missed your call", "我没接到你的电话。", "An acknowledgement that someone phoned while you were unavailable", "I missed your call because I was changing trains.", "我换乘时没接到你的电话。", "Why didn't you answer a few minutes ago?", "你几分钟前为什么没接？"),
                P("leave your number", "留下你的号码。", "A request for a caller to provide a phone number for a return call", "Please leave your number and I'll call you back.", "请留下你的号码，我会回拨。", "What should I do if the line disconnects?", "如果电话断了我该怎么办？"),
                P("record a memo", "录一段备忘。", "To make a short recording so you remember information later", "I'll record a memo before I forget the details.", "我会先录一段备忘，免得忘记细节。", "Can you remember the changes until you get home?", "你到家前能记住这些变化吗？"),
                P("check my voicemail", "查看语音信箱。", "To listen to recorded messages left after you missed calls", "I'll check my voicemail when I leave the train.", "我下地铁后会查看语音信箱。", "Did the doctor leave a message for you?", "医生给你留语音了吗？"),
            ),
            L(
                8,
                6,
                "keep-a-call-short",
                "简短通话",
                "Keep a Call Short",
                "提前说明自己只有一点时间，让电话重点明确又不显得不礼貌。",
                "换乘前接一通简短电话",
                "换乘前接一通简短电话。",
                "clock",
                P("I only have a minute", "我只有一分钟。", "A clear time limit that helps keep a call focused", "I only have a minute before I change trains.", "我换乘前只有一分钟。", "Can we discuss the whole proposal now?", "我们现在能讨论整份提案吗？"),
                P("keep it brief", "尽量简短。", "A request to communicate only the essential information", "Please keep it brief; I'm about to lose signal.", "请尽量简短，我马上要没信号了。", "I have three updates for you.", "我有三条更新要告诉你。"),
                P("call from the train", "在地铁上打电话。", "To make a phone call while travelling by train", "I can call from the train if it's not too crowded.", "如果不太挤，我可以在地铁上打电话。", "When can we talk before the meeting?", "开会前我们什么时候能说话？"),
                P("put you on speaker", "开免提让你听。", "To use a phone's loudspeaker so others can hear the call", "I'll put you on speaker when I reach the platform.", "我到站台后开免提让你听。", "Can the whole group hear this update?", "整个小组都能听到这条更新吗？"),
            ),
            L(
                8,
                7,
                "route-a-call",
                "转接电话",
                "Route a Call",
                "拨错号码或找错部门时，礼貌请求转接，并在线上等待。",
                "给机构打电话时需要找到正确的人",
                "给机构打电话时需要找到正确的人。",
                "phone",
                P("wrong number", "打错号码。", "A phrase that says a call reached the wrong person or department", "Sorry, I think I have the wrong number.", "抱歉，我想我打错号码了。", "This is the transport office, not the clinic.", "这里是交通办公室，不是诊所。"),
                P("put me through", "帮我转接。", "A request to connect your call to another person or department", "Could you put me through to customer support?", "你能帮我转接到客服吗？", "The billing team can answer that question.", "账单团队能回答那个问题。"),
                P("transfer the call", "转接电话。", "To connect a caller to another person or department", "Please transfer the call to the booking desk.", "请把电话转到预订部门。", "You need to speak with someone who handles appointments.", "你需要和负责预约的人说话。"),
                P("stay on the line", "请在线等候。", "A request to remain connected while someone transfers or checks something", "Please stay on the line while I check that for you.", "我为你查询时请在线等候。", "Can you find my booking reference?", "你能找到我的预订编号吗？"),
            ),
            L(
                8,
                8,
                "end-a-call-naturally",
                "自然结束通话",
                "End a Call Naturally",
                "需要下车或进隧道时，清楚礼貌地结束通话，并约好之后再联系。",
                "到站前结束一通电话",
                "到站前结束一通电话。",
                "phone",
                P("I've got to go", "我得走了；我得挂了。", "A natural way to say that you must end a conversation now", "I've got to go; my stop is coming up.", "我得挂了，我的站快到了。", "Can we keep talking for another ten minutes?", "我们能再聊十分钟吗？"),
                P("thanks for calling", "谢谢你打来。", "A polite phrase that acknowledges the caller before ending", "Thanks for calling. That clears things up.", "谢谢你打来，这下事情清楚了。", "I wanted to make sure you knew about the change.", "我想确认你知道这个变化。"),
                P("I'll ring you later", "我晚点打给你。", "An informal promise to phone someone again later", "I'll ring you later when I'm somewhere quieter.", "我到安静一点的地方后晚点打给你。", "Can you explain the rest when you have time?", "你有时间时能解释剩下的吗？"),
                P("bye for now", "先这样；回头见。", "A friendly closing that suggests you expect to talk again", "Bye for now. Have a safe trip home.", "先这样，回家路上注意安全。", "I need to step off the train now.", "我现在要下地铁了。"),
            ),
        ),
    ),
    Chapter(
        9,
        "临时变化和突发情况",
        "Last-Minute Changes",
        "当计划被取消、延误或意外打断时，及时说明、道歉并给出可行的下一步。",
        "change",
        (
            L(
                9,
                1,
                "cancel-a-plan",
                "取消计划",
                "Cancel a Plan",
                "临时取消时，清楚说出发生了什么，不让对方一直等消息。",
                "地铁延误导致无法按原计划见面",
                "地铁延误导致无法按原计划见面。",
                "change",
                P("call it off", "取消；叫停。", "To decide that an event or plan will not happen", "We may need to call it off if the trains stop again.", "如果列车又停了，我们可能得取消。", "Can we still meet tonight with this delay?", "这次延误下我们今晚还能见吗？"),
                P("cancel at the last minute", "最后一刻取消。", "To cancel very close to the planned time", "I'm sorry to cancel at the last minute.", "很抱歉最后一刻取消。", "Are you still coming to the booking we made?", "你还会来我们预订的地方吗？"),
                P("fall through", "落空；没能实现。", "To fail to happen because a plan or arrangement does not work out", "The dinner plan fell through when the restaurant closed early.", "餐厅提前关门，晚饭计划落空了。", "Why aren't we meeting at the usual place?", "我们为什么不在常去的地方见面？"),
                P("be off", "取消；不再进行。", "To be cancelled or no longer happening", "The event is off because of the weather warning.", "因为天气警报，活动取消了。", "Should I still travel to the park?", "我还需要去公园吗？"),
            ),
            L(
                9,
                2,
                "offer-a-backup",
                "提出备选方案",
                "Offer a Backup",
                "原计划不可行时，不只说不行，也给出替代方式。",
                "通勤路上为取消的计划找替代方案",
                "在通勤路上为取消的计划找替代方案。",
                "change",
                P("come up with a backup", "想出一个备选方案。", "To create another plan in case the original one cannot happen", "Let's come up with a backup before the weather gets worse.", "天气变得更糟前我们想个备选方案吧。", "The outdoor event might be cancelled.", "户外活动可能会取消。"),
                P("switch to", "改用；改成。", "To stop using one option and use another instead", "We can switch to a video call tonight.", "我们今晚可以改成视频通话。", "The café is full and we can't meet there.", "咖啡馆满了，我们没法在那里见。"),
                P("change course", "改变方向；改变做法。", "To choose a different direction or strategy after conditions change", "We should change course and meet closer to your station.", "我们应该改变做法，在离你车站更近的地方见。", "The usual route is closed for repairs.", "常用路线因维修关闭了。"),
                P("a fallback option", "备用选择。", "An alternative choice that you can use if the first option fails", "A phone call is a good fallback option if the app stops working.", "如果应用不能用，打电话是个不错的备用选择。", "What can we do if the shared link fails?", "如果共享链接失效，我们能怎么办？"),
            ),
            L(
                9,
                3,
                "apologise-well",
                "真诚道歉",
                "Apologise Well",
                "错过信息或给对方添麻烦时，承认问题、表达歉意并说明补救。",
                "因为地铁中断错过一个重要约定",
                "因为地铁中断错过一个重要约定。",
                "chat",
                P("I'm sorry I missed", "很抱歉我错过了。", "An apology for failing to attend, answer or notice something", "I'm sorry I missed your call earlier.", "很抱歉我刚才错过了你的电话。", "Why didn't you answer when I called?", "我打电话时你为什么没接？"),
                P("I didn't mean to", "我不是故意的。", "A phrase that explains an unwanted action was not intentional", "I didn't mean to leave you waiting outside.", "我不是故意让你在外面等的。", "I've been standing at the station for twenty minutes.", "我已经在车站站了二十分钟。"),
                P("that's my fault", "那是我的错。", "A direct way to accept responsibility for a mistake", "That's my fault; I wrote down the wrong station.", "那是我的错，我记错车站了。", "Why did we end up at different exits?", "我们为什么到了不同出口？"),
                P("make it up to you", "补偿你；弥补。", "To do something kind after causing inconvenience or disappointment", "Let me make it up to you with coffee tomorrow.", "让我明天请你喝咖啡补偿你。", "I missed the dinner you planned for us.", "我错过了你为我们安排的晚饭。"),
            ),
            L(
                9,
                4,
                "explain-a-delay",
                "解释延误",
                "Explain a Delay",
                "迟到时说出原因、预计影响和自己正在做什么。",
                "下班高峰期遇到交通堵塞",
                "下班高峰期遇到交通堵塞。",
                "route",
                P("held up", "被耽搁；被拖住。", "To be delayed by something outside your control", "I'm held up at the station because of a signal fault.", "因为信号故障，我被耽搁在车站。", "Why haven't you left the station yet?", "你为什么还没离开车站？"),
                P("caught in traffic", "堵在路上。", "To be delayed because road traffic is moving slowly", "The bus is caught in traffic near the bridge.", "公交车在桥附近堵住了。", "Why is the bus taking so long?", "公交车为什么这么久？"),
                P("take longer than expected", "比预计花更长时间。", "To require more time than you originally thought", "This transfer is taking longer than expected.", "这次换乘比预计花更长时间。", "Are you still on track to arrive by six?", "你还能按计划六点到吗？"),
                P("be delayed", "被延误。", "To be forced to arrive or happen later than planned", "I'll be delayed, but I'm still on my way.", "我会晚到，但还在路上。", "Will you need to cancel completely?", "你需要完全取消吗？"),
            ),
            L(
                9,
                5,
                "handle-the-unexpected",
                "应对突发情况",
                "Handle the Unexpected",
                "突发任务或计划改变时，先说明现实，再决定如何处理。",
                "出站前收到一条改变晚上安排的消息",
                "出站前收到一条改变晚上安排的消息。",
                "change",
                P("something came up", "临时出了点事。", "A natural way to say an unexpected matter needs your attention", "Something came up, so I need to leave the meeting early.", "临时出了点事，所以我得早点离开会议。", "Why can't you stay for dinner anymore?", "你为什么不能继续吃晚饭了？"),
                P("plans have changed", "计划变了。", "A clear update that the original arrangement is no longer current", "Plans have changed; I'm meeting you at the other exit.", "计划变了，我改在另一个出口和你见。", "Are we still using the same meeting point?", "我们还用同一个集合点吗？"),
                P("I didn't expect that", "我没料到会这样。", "A response that shows genuine surprise at new information", "I didn't expect that the last train would be cancelled.", "我没料到末班车会取消。", "The service board says there are no more trains tonight.", "服务公告牌显示今晚没有更多列车了。"),
                P("deal with it", "处理它；应对它。", "To take practical action about a difficult situation", "I'll deal with it once I get some signal.", "等我有信号了就会处理它。", "The client sent an urgent question.", "客户发来了一个紧急问题。"),
            ),
            L(
                9,
                6,
                "work-around-a-change",
                "绕开变化继续推进",
                "Work Around a Change",
                "即使原计划不能继续，也能提出新路径、让其他人先走或先凑合完成。",
                "一项安排受阻后重新分配下一步",
                "一项安排受阻后重新分配下一步。",
                "route",
                P("work around it", "绕开它解决。", "To find a practical way to continue despite a problem", "We can work around it by meeting online first.", "我们可以先线上见面来绕开这个问题。", "The meeting room is unavailable this afternoon.", "今天下午会议室不能用。"),
                P("find another way", "找另一种办法。", "To look for a different method when the first one fails", "We'll find another way to send the file.", "我们会找另一种办法发文件。", "The upload keeps failing on the train Wi-Fi.", "地铁 Wi-Fi 上传一直失败。"),
                P("carry on without me", "不用我也继续吧。", "A considerate request for others to continue while you are delayed", "Please carry on without me; I'll read the notes later.", "请不用等我继续，我晚点看笔记。", "The workshop starts in five minutes.", "研讨会五分钟后开始。"),
                P("make do", "先凑合用；将就一下。", "To manage with what is available when the ideal option is not possible", "We'll have to make do with a phone call today.", "今天我们只好先凑合用电话沟通。", "The video room is closed for maintenance.", "视频会议室因维护关闭了。"),
            ),
            L(
                9,
                7,
                "change-review",
                "变化复习",
                "Change Review",
                "把变化通知得及时、具体，并为下一步留下灵活空间。",
                "在地铁上给所有相关人同步变动",
                "在地铁上给所有相关人同步变动。",
                "chat",
                P("let you know right away", "马上告诉你。", "A promise to share important news as soon as you receive it", "I'll let you know right away if the service resumes.", "如果线路恢复，我马上告诉你。", "Please tell me when trains start moving again.", "列车恢复运行时请告诉我。"),
                P("keep an eye on", "留意；持续关注。", "To watch a situation carefully for changes", "Keep an eye on the weather before you leave.", "你出门前留意一下天气。", "The forecast says heavy rain may start tonight.", "预报说今晚可能下大雨。"),
                P("stay flexible", "保持灵活。", "To remain willing to change plans when conditions change", "Let's stay flexible until the trains are back to normal.", "等列车恢复正常前，我们先保持灵活。", "We don't know when the delay will end.", "我们不知道延误何时结束。"),
                P("leave room for", "给……留出余地。", "To allow time or space for something that may happen", "Leave room for a delay when you plan the trip.", "你规划行程时给延误留出余地。", "The transfer is usually quick, but not always.", "换乘通常很快，但也不总是。"),
            ),
            L(
                9,
                8,
                "change-scenario-challenge",
                "变化场景实战",
                "Change Scenario Challenge",
                "在紧急消息里提出延后、坚持完成、快速决定，并保持冷静。",
                "临时变化接连发生时的简短回应",
                "临时变化接连发生时的简短回应。",
                "change",
                P("postpone until", "推迟到……。", "To move an event to a later specified time", "Let's postpone until tomorrow morning.", "我们推迟到明天早上吧。", "The train delay means neither of us will arrive on time.", "地铁延误意味着我们谁都不能准时到。"),
                P("push through", "坚持做完；克服困难继续。", "To continue despite difficulty until something is completed", "I'll push through the last section tonight.", "我今晚会坚持完成最后一部分。", "The report is nearly complete, but you're tired.", "报告快完成了，但你已经累了。"),
                P("make a quick decision", "快速做决定。", "To choose an action without spending a long time discussing it", "We need to make a quick decision before the doors close.", "关门前我们需要快速做决定。", "The platform has changed at the last second.", "站台在最后一刻变了。"),
                P("stay calm", "保持冷静。", "A reminder to avoid panic so you can respond effectively", "Stay calm; we'll find the next train together.", "保持冷静，我们会一起找到下一班车。", "The display is confusing and everyone is rushing.", "显示屏很混乱，大家都在赶。"),
            ),
        ),
    ),
    Chapter(
        10,
        "综合通勤实战",
        "Commute in Real Life",
        "把时间地点、工作、社交、电话和突发变化串成完整而自然的通勤英语。",
        "route",
        (
            L(
                10,
                1,
                "navigate-the-route",
                "完成通勤路线",
                "Navigate the Route",
                "用四个动作短语说明换乘、找座、赶上衔接和下车。",
                "早高峰完成一段需要换乘的通勤",
                "早高峰完成一段需要换乘的通勤。",
                "route",
                P("change trains", "换乘。", "To leave one train and board another to continue a journey", "I need to change trains at Central.", "我需要在 Central 换乘。", "Does this train go all the way to the office?", "这趟车能直接到办公室吗？"),
                P("get a seat", "找到座位。", "To find an empty place to sit on public transport", "I finally got a seat, so I can read the notes now.", "我终于有座位了，现在可以看笔记。", "Is the train crowded this morning?", "今天早上地铁挤吗？"),
                P("make a connection", "赶上换乘。", "To arrive in time to transfer to the next train, bus or flight", "I can make the connection if this train arrives on time.", "如果这趟车准时到，我能赶上换乘。", "Will you catch the airport train at the next station?", "你下一站能赶上机场线吗？"),
                P("step off", "下车。", "To leave a train, bus or other vehicle", "Step off at the next stop and follow the signs.", "下一站下车，然后跟着指示牌走。", "Where should I leave the train?", "我该在哪一站下车？"),
            ),
            L(
                10,
                2,
                "arrive-and-start-work",
                "到岗开工",
                "Arrive and Start Work",
                "到办公室后从通勤状态切换到工作状态，开始、补上信息并进入专注。",
                "下地铁后准备开始一天的工作",
                "下地铁后准备开始一天的工作。",
                "work",
                P("settle in", "安顿下来进入状态。", "To become comfortable and ready after arriving somewhere", "Give me five minutes to settle in, then I'll join the call.", "给我五分钟安顿下来，然后我加入电话会议。", "Can you start the meeting as soon as you arrive?", "你一到就能开始会议吗？"),
                P("get started", "开始做。", "To begin a task or activity", "I'll get started on the email as soon as I sit down.", "我一坐下就开始写邮件。", "What will you work on first today?", "你今天先做什么？"),
                P("get down to work", "认真开始工作。", "To begin working with focus after preparation or distraction", "Once I have coffee, I'll get down to work.", "我喝完咖啡就认真开始工作。", "Are you ready to focus on the report?", "你准备好专注做报告了吗？"),
                P("get up to speed", "快速了解最新情况。", "To learn enough recent information to work effectively", "I'll get up to speed by reading the team updates.", "我会通过看团队更新快速了解情况。", "You missed yesterday's meeting.", "你错过了昨天的会议。"),
            ),
            L(
                10,
                3,
                "meet-for-coffee",
                "咖啡见面",
                "Meet for Coffee",
                "把通勤后的短暂见面安排得清楚：喝咖啡、午休、在大厅见和分账。",
                "上班前和朋友约一杯咖啡",
                "上班前和朋友约一杯咖啡。",
                "food",
                P("grab a coffee", "喝杯咖啡。", "An informal suggestion to meet briefly for coffee", "Do you want to grab a coffee before work?", "你上班前想喝杯咖啡吗？", "I arrive near your office ten minutes early.", "我会比上班时间早十分钟到你办公室附近。"),
                P("take a lunch break", "休午餐时间。", "To stop work temporarily for a meal in the middle of the day", "Let's take a lunch break after the client call.", "客户电话后我们休午餐吧。", "We've been working since early morning.", "我们从早上开始一直在工作。"),
                P("meet in the lobby", "在大厅见。", "To choose the lobby as the meeting place", "Let's meet in the lobby at twelve fifteen.", "我们十二点十五在大厅见。", "The café upstairs is hard to find.", "楼上的咖啡馆不太好找。"),
                P("split the bill", "平分账单。", "To divide a shared cost so each person pays a part", "We can split the bill after lunch.", "午饭后我们可以平分账单。", "Should one person pay for the whole meal?", "要不要一个人付整顿饭的钱？"),
            ),
            L(
                10,
                4,
                "lock-in-the-details",
                "敲定细节",
                "Lock In the Details",
                "把时间放进日历、设提醒并确认细节，减少临近时的来回沟通。",
                "通勤中完成一个活动的最后确认",
                "在通勤中完成一个活动的最后确认。",
                "clock",
                P("lock it in", "敲定；最终确定。", "To make a plan final so it will not keep changing", "Great, let's lock it in for Friday evening.", "很好，我们就把它敲定在周五晚上。", "Are we still deciding between Friday and Saturday?", "我们还在周五和周六之间选吗？"),
                P("put it in the calendar", "把它放进日历。", "To record an event in a calendar so you remember it", "I'll put it in the calendar as soon as I get a signal.", "我一有信号就把它放进日历。", "How will you remember the appointment next week?", "你怎么记住下周的预约？"),
                P("send a reminder", "发送提醒。", "To message someone before an event so they do not forget", "I'll send a reminder the day before.", "我会在前一天发送提醒。", "What if the group forgets the meeting time?", "如果大家忘了会议时间怎么办？"),
                P("confirm the details", "确认细节。", "To check the important information one final time", "Let's confirm the details before we book it.", "我们预订前确认一下细节。", "Do we have the correct date, time and address?", "我们有正确的日期、时间和地址吗？"),
            ),
            L(
                10,
                5,
                "wrap-up-a-work-message",
                "收尾工作消息",
                "Wrap Up a Work Message",
                "在通勤中用一句清楚的消息安排通话、承担后续、补齐信息和结束任务。",
                "回家地铁上给同事发工作收尾消息",
                "回家地铁上给同事发工作收尾消息。",
                "work",
                P("give someone a call", "给某人打电话。", "To phone a person in order to discuss something directly", "I'll give the supplier a call when I get home.", "我到家后会给供应商打电话。", "How will you clarify the delivery problem?", "你会怎么澄清配送问题？"),
                P("leave it with me", "交给我吧。", "A reassuring phrase that says you will take responsibility for the next step", "Leave it with me; I'll send the final version tonight.", "交给我吧，我今晚会发最终版。", "Who can finish the final edits?", "谁能完成最后的修改？"),
                P("bring someone up to speed", "让某人了解最新进展。", "To give a person the information they need to understand the current situation", "I'll bring Alex up to speed tomorrow morning.", "我明天早上会让 Alex 了解最新进展。", "Alex was away for the client call.", "Alex 没参加客户电话。"),
                P("wrap up", "收尾；结束。", "To finish the last part of a task or conversation", "Let's wrap up the notes before the train reaches my stop.", "地铁到我那站前我们把笔记收尾吧。", "Do we need to discuss anything else today?", "今天还有别的需要讨论吗？"),
            ),
            L(
                10,
                6,
                "adapt-on-the-route",
                "路线变化实战",
                "Adapt on the Route",
                "遇到路线或时间变化时，说明如何调整，同时让事情继续向前。",
                "回家途中发现常用路线被关闭",
                "回家途中发现常用路线被关闭。",
                "route",
                P("handle a disruption", "应对中断。", "To manage an unexpected interruption to travel or a plan", "We can handle the disruption by taking the bus from here.", "我们可以从这里坐公交来应对中断。", "The train service has stopped unexpectedly.", "列车服务意外停止了。"),
                P("take a different route", "走另一条路线。", "To travel by another way when the normal route is unavailable", "I'll take a different route home tonight.", "我今晚会走另一条路线回家。", "The main exit is closed for repairs.", "主出口因维修关闭了。"),
                P("keep things moving", "让事情继续推进。", "To prevent a task or plan from stopping completely", "Let's keep things moving while we wait for the update.", "我们等更新时也让事情继续推进。", "The final approval may take another hour.", "最终批准可能还要一个小时。"),
                P("adjust on the fly", "随机应变；临场调整。", "To change your approach quickly as new conditions appear", "We can adjust on the fly if the platform changes again.", "如果站台又变了，我们可以临场调整。", "The service board keeps changing the departure time.", "服务公告牌一直在改发车时间。"),
            ),
            L(
                10,
                7,
                "learn-on-the-go-review",
                "通勤学习复习",
                "Learn on the Go Review",
                "把通勤中学到的表达真的说出来：短句、完整句和随手练习。",
                "用回家路上的三分钟复习今天的表达",
                "用回家路上的三分钟复习今天的表达。",
                "chat",
                P("say it out loud", "大声说出来。", "To practise a phrase by speaking rather than only reading it", "Say it out loud once when you leave the platform.", "离开站台后大声说一遍。", "How can I remember the phrase better?", "我怎样能更好记住这个短语？"),
                P("keep it simple", "保持简单。", "A reminder to use clear, uncomplicated language", "Keep it simple: one clear sentence is enough.", "保持简单：一句清楚的话就够了。", "Do I need to explain every detail in my reply?", "我需要在回复中解释每一个细节吗？"),
                P("use a full sentence", "用一个完整句子。", "To include enough words for a response to be clear and natural", "Try to use a full sentence after the short reply.", "简短回应后试着再用一个完整句子。", "I can say the phrase, but then I don't know what to add.", "我会说这个短语，但之后不知道加什么。"),
                P("practice on the go", "在路上练习。", "To use spare moments while travelling for short practice", "You can practice on the go without speaking loudly.", "你可以在路上练习，不必大声说话。", "I only have three minutes before my stop.", "我到站前只有三分钟。"),
            ),
            L(
                10,
                8,
                "final-commute-challenge",
                "综合通勤实战",
                "Final Commute Challenge",
                "用自然的结尾和鼓励性表达完成一段从地铁到目的地的连续对话。",
                "结束一整段通勤中的安排和沟通",
                "结束一整段通勤中的安排和沟通。",
                "route",
                P("ready when you are", "你准备好我就可以。", "A relaxed way to say that you are prepared to begin whenever the other person is", "I'm ready when you are; just send the final link.", "你准备好我就可以，发最终链接就行。", "I've finished checking the details.", "我已经检查完细节了。"),
                P("take it from here", "接下来交给我。", "A phrase that says you will handle the next part of a task", "You can take it from here while I change trains.", "我换乘时接下来就交给你了。", "I've sent you the draft and the client is waiting.", "我把草稿发给你了，客户在等。"),
                P("one step at a time", "一步一步来。", "An encouraging reminder to handle a difficult situation in small parts", "One step at a time; first let's find the right platform.", "一步一步来，我们先找到正确站台。", "Everything changed at once and I feel overwhelmed.", "所有事一下都变了，我觉得不知所措。"),
                P("see you around", "回头见；之后见。", "A friendly casual goodbye when you expect to see someone again", "See you around. Text me when you get home.", "回头见，到家后给我发消息。", "I'm getting off here, but we work in the same building.", "我要在这里下车，不过我们在同一栋楼工作。"),
            ),
        ),
    ),
)


def normalise_term(term: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", term.lower()).strip()


def validate_curriculum() -> None:
    if len(CHAPTERS) != 10:
        raise ValueError("The commute curriculum must contain exactly 10 chapters.")

    seen = {normalise_term(term) for term in INITIAL_CORE_TERMS}
    total = 1  # The already-published first lesson.
    for expected_chapter, chapter in enumerate(CHAPTERS, start=1):
        if chapter.number != expected_chapter:
            raise ValueError("Chapter numbers must be consecutive.")
        expected_lessons = 7 if chapter.number == 1 else 8
        if len(chapter.lessons) != expected_lessons:
            raise ValueError(
                f"Chapter {chapter.number} must contribute {expected_lessons} new lessons."
            )
        for lesson in chapter.lessons:
            if lesson.chapter != chapter.number:
                raise ValueError(f"{lesson.slug} belongs to the wrong chapter.")
            minimum_lesson = 2 if chapter.number == 1 else 1
            if lesson.number < minimum_lesson or lesson.number > 8:
                raise ValueError(f"{lesson.slug} has an invalid lesson number.")
            for phrase in lesson.phrases:
                key = normalise_term(phrase.term)
                if key in seen:
                    raise ValueError(f"Repeated core phrase: {phrase.term}")
                if not phrase.reply or not phrase.reply_zh:
                    raise ValueError(f"{phrase.term} needs a bilingual example.")
                seen.add(key)
            total += 1
    if total != 80:
        raise ValueError(f"Expected 80 lessons, found {total}.")


def item(code: str, order: int, payload: dict, title: str = "") -> dict:
    return {
        "item_code": code,
        "item_order": order,
        "title": title,
        "payload": payload,
    }


def section(code: str, title: str, title_en: str, order: int, items: list[dict]) -> dict:
    return {
        "section_code": code,
        "title": title,
        "title_en": title_en,
        "sort_order": order,
        "items": items,
    }


def illustration_name(lesson: Lesson) -> str:
    return f"commute-c{lesson.chapter:02d}-l{lesson.number:02d}-{lesson.slug}.svg"


def illustration_url(lesson: Lesson) -> str:
    return f"/static/{STATIC_DIRECTORY}/{illustration_name(lesson)}"


def illustration_svg(lesson: Lesson, chapter_art: str) -> str:
    """Return a tiny, distinct and scene-oriented SVG for each lesson."""

    palette = [
        ("#DDF5F0", "#15706C", "#F6B85E"),
        ("#E8EEFF", "#3D5FB6", "#EF8A75"),
        ("#FFF0D9", "#B86630", "#5D927E"),
        ("#F4E9FF", "#77519E", "#EF9BAA"),
        ("#E6F3DF", "#4D8050", "#D99A43"),
    ]
    background, primary, accent = palette[(lesson.chapter + lesson.number) % len(palette)]
    label = html.escape(f"{lesson.chapter}.{lesson.number}")
    icon = lesson.art or chapter_art
    shapes = {
        "clock": '<circle cx="48" cy="48" r="25" fill="none" stroke="{p}" stroke-width="7"/><path d="M48 30v19l13 8" fill="none" stroke="{p}" stroke-linecap="round" stroke-linejoin="round" stroke-width="7"/>',
        "pin": '<path d="M48 20c-14 0-25 10-25 24 0 18 25 39 25 39s25-21 25-39c0-14-11-24-25-24z" fill="{p}"/><circle cx="48" cy="44" r="8" fill="{b}"/>',
        "signal": '<path d="M24 68h9V56h-9zm15 0h9V45h-9zm15 0h9V34h-9zm15 0h9V23h-9z" fill="{p}"/><circle cx="73" cy="25" r="10" fill="{a}"/>',
        "chat": '<path d="M20 27c0-8 7-14 16-14h28c9 0 16 6 16 14v16c0 8-7 14-16 14H46L32 70V57h-1c-6 0-11-6-11-14z" fill="{p}"/><circle cx="42" cy="35" r="4" fill="{b}"/><circle cx="51" cy="35" r="4" fill="{b}"/><circle cx="60" cy="35" r="4" fill="{b}"/>',
        "work": '<rect x="19" y="29" width="58" height="43" rx="7" fill="{p}"/><path d="M36 29v-7h24v7" fill="none" stroke="{p}" stroke-width="7"/><path d="M19 46h58" stroke="{b}" stroke-width="6"/><rect x="43" y="43" width="10" height="7" rx="2" fill="{a}"/>',
        "food": '<path d="M27 20v24m-7-24v15c0 7 5 11 12 11s12-4 12-11V20m-17 0v17m12-17v17M59 20v61m0-61c10 0 16 9 16 21S69 61 59 61" fill="none" stroke="{p}" stroke-linecap="round" stroke-width="6"/>',
        "help": '<circle cx="48" cy="48" r="29" fill="{p}"/><path d="M39 39c1-7 17-9 18 2 1 8-9 8-9 15" fill="none" stroke="{b}" stroke-linecap="round" stroke-width="6"/><circle cx="48" cy="67" r="4" fill="{b}"/>',
        "friends": '<circle cx="37" cy="36" r="12" fill="{p}"/><circle cx="62" cy="38" r="10" fill="{a}"/><path d="M18 76c2-17 14-25 28-25s26 8 28 25" fill="{p}"/><path d="M50 76c1-13 10-20 21-20 6 0 11 2 15 6" fill="{a}"/>',
        "phone": '<rect x="29" y="14" width="38" height="68" rx="8" fill="{p}"/><rect x="36" y="24" width="24" height="39" rx="3" fill="{b}"/><circle cx="48" cy="72" r="4" fill="{a}"/>',
        "change": '<path d="M22 34h45l-9-9m9 9-9 9M74 62H29l9-9m-9 9 9 9" fill="none" stroke="{p}" stroke-linecap="round" stroke-linejoin="round" stroke-width="7"/><circle cx="76" cy="21" r="8" fill="{a}"/>',
        "route": '<path d="M20 70c15-29 27 1 41-27 7-14 11-21 19-21" fill="none" stroke="{p}" stroke-linecap="round" stroke-width="7"/><circle cx="20" cy="70" r="8" fill="{a}"/><circle cx="80" cy="22" r="8" fill="{p}"/>',
    }.get(icon, '<circle cx="48" cy="48" r="27" fill="{p}"/>')
    shapes = shapes.format(p=primary, a=accent, b=background)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" role="img" aria-label="Commute lesson {label}">
  <rect width="96" height="96" rx="20" fill="{background}"/>
  {shapes}
  <text x="76" y="84" font-family="Arial, sans-serif" font-size="11" font-weight="700" fill="{primary}" text-anchor="end">{label}</text>
</svg>\n'''


def install_illustration(settings: Settings, lesson: Lesson, chapter_art: str) -> str:
    source = ASSET_DIR / illustration_name(lesson)
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(illustration_svg(lesson, chapter_art), encoding="utf-8")
    if source.stat().st_size >= MAX_ILLUSTRATION_BYTES:
        raise ValueError(f"{source.name} exceeds the 100KB commute image limit.")
    target = settings.static_dir / STATIC_DIRECTORY / source.name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if target.stat().st_size >= MAX_ILLUSTRATION_BYTES:
        raise ValueError(f"{target.name} exceeds the 100KB commute image limit.")
    return illustration_url(lesson)


def slug_code(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def phrase_payload(phrase: Phrase) -> dict:
    return {
        "term": phrase.term,
        "meaning": phrase.meaning,
        "explanation": phrase.explanation,
        "examples": [{"english": phrase.reply, "chinese": phrase.reply_zh}],
    }


def blanked_reply(phrase: Phrase) -> str:
    return re.sub(re.escape(phrase.term), "______", phrase.reply, count=1, flags=re.I)


def dialogue_item(index: int, lesson: Lesson, phrase: Phrase) -> dict:
    return item(
        f"scene-{index:02d}",
        index,
        {
            "scene": lesson.scene,
            "turns": [
                {"speaker": "Mia", "english": phrase.cue, "chinese": phrase.cue_zh},
                {
                    "speaker": "You",
                    "english": phrase.reply,
                    "chinese": phrase.reply_zh,
                },
            ],
        },
        lesson.scene,
    )


def combined_dialogue(index: int, lesson: Lesson, first: Phrase, second: Phrase) -> dict:
    return item(
        f"scene-{index:02d}",
        index,
        {
            "scene": f"{lesson.scene} · 连续回应",
            "turns": [
                {"speaker": "Mia", "english": first.cue, "chinese": first.cue_zh},
                {"speaker": "You", "english": first.reply, "chinese": first.reply_zh},
                {"speaker": "Mia", "english": second.cue, "chinese": second.cue_zh},
                {"speaker": "You", "english": second.reply, "chinese": second.reply_zh},
            ],
        },
        f"{lesson.scene} · 连续回应",
    )


def lesson_sections(lesson: Lesson) -> list[dict]:
    phrases = lesson.phrases
    dialogues = [dialogue_item(index, lesson, phrase) for index, phrase in enumerate(phrases, start=1)]
    dialogues.extend(
        [
            combined_dialogue(5, lesson, phrases[0], phrases[1]),
            combined_dialogue(6, lesson, phrases[2], phrases[3]),
        ]
    )
    return [
        section(
            "core_vocabulary",
            "核心短语",
            "Core Phrases",
            10,
            [
                item(
                    f"term-{index:02d}-{slug_code(phrase.term)}",
                    index,
                    phrase_payload(phrase),
                    phrase.term,
                )
                for index, phrase in enumerate(phrases, start=1)
            ],
        ),
        section("situational_dialogues", "情景对话", "Situational Dialogues", 20, dialogues),
        section(
            "key_sentence_patterns",
            "核心句型",
            "Key Sentence Patterns",
            30,
            [
                item(
                    f"pattern-{index:02d}",
                    index,
                    {
                        "pattern": phrase.term,
                        "meaning": phrase.meaning,
                        "explanation": phrase.explanation,
                        "examples": [
                            {"english": phrase.reply, "chinese": phrase.reply_zh}
                        ],
                    },
                    phrase.term,
                )
                for index, phrase in enumerate(phrases, start=1)
            ],
        ),
        section(
            "speaking_practice",
            "开口接话",
            "Quick Reply Practice",
            40,
            [
                item(
                    "quick-reply-choice",
                    1,
                    {
                        "question": "Choose the reply that fits the situation.",
                        "question_zh": f"{phrases[0].cue_zh} 选出最自然的回应。",
                        "sentence": f'Your friend says: “{phrases[0].cue}” Reply: “{blanked_reply(phrases[0])}”',
                        "answer": phrases[0].term,
                        "choices": [phrase.term for phrase in phrases],
                        "explanation": phrases[0].explanation,
                        "turns": [
                            {"speaker": "Friend", "english": phrases[0].cue, "chinese": phrases[0].cue_zh},
                            {"speaker": "You", "english": phrases[0].reply, "chinese": phrases[0].reply_zh},
                        ],
                    },
                    "选出自然回应",
                ),
                item(
                    "say-it-in-full",
                    2,
                    {
                        "instruction": f"用 {phrases[1].term} 说出完整回应。",
                        "question": phrases[1].cue,
                        "question_zh": phrases[1].cue_zh,
                        "guidance": f"Say: {phrases[1].reply}",
                        "turns": [
                            {"speaker": "Friend", "english": phrases[1].cue, "chinese": phrases[1].cue_zh},
                            {"speaker": "You", "english": phrases[1].reply, "chinese": phrases[1].reply_zh},
                        ],
                    },
                    "说出完整回应",
                ),
            ],
        ),
        section(
            "mini_exercises",
            "开口讨论",
            "Speak It Out",
            50,
            [
                item(
                    "speak-for-yourself",
                    1,
                    {
                        "question": phrases[2].cue,
                        "question_zh": phrases[2].cue_zh,
                        "guidance": f"Try starting with: {phrases[2].term}",
                        "sample_answer": phrases[2].reply,
                        "sample_answer_zh": phrases[2].reply_zh,
                    },
                    "用自己的话回应",
                ),
                item(
                    "one-more-reply",
                    2,
                    {
                        "question": phrases[3].cue,
                        "question_zh": phrases[3].cue_zh,
                        "guidance": f"Try starting with: {phrases[3].term}",
                        "sample_answer": phrases[3].reply,
                        "sample_answer_zh": phrases[3].reply_zh,
                    },
                    "补一句完整回应",
                ),
            ],
        ),
        section(
            "useful_tips",
            "通勤提示",
            "Commuting Tips",
            60,
            [
                item(
                    "short-first",
                    1,
                    {
                        "title": "先把关键回应说出来",
                        "summary": f"在车厢里先说 “{phrases[0].term}”，再视情况补充信息；短句也能让对方知道你的意思。",
                        "explanation": f"{phrases[0].explanation} This keeps a reply clear even when the train is noisy.",
                    },
                    "先回应，再补充",
                ),
                item(
                    "repeat-at-the-exit",
                    2,
                    {
                        "title": "出站后再说一遍完整句",
                        "summary": f"默读 “{phrases[1].reply}”，出站后再出声练习；你不需要在拥挤车厢里大声说英语。",
                        "explanation": "Silent rehearsal protects your focus and still prepares a natural spoken reply.",
                    },
                    "默读也有效",
                ),
            ],
        ),
        section(
            "extended_reading",
            "延伸阅读",
            "Extended Reading",
            70,
            [
                item(
                    "two-message-story",
                    1,
                    {
                        "text": (
                            f"On the train, Mia gets a message: “{phrases[0].cue}” "
                            f"She replies, “{phrases[0].reply}” A minute later, her friend asks, "
                            f'“{phrases[1].cue}” Mia answers, “{phrases[1].reply}”'
                        ),
                        "chinese": (
                            f"地铁上，Mia 收到消息：“{phrases[0].cue_zh}” "
                            f"她回复：“{phrases[0].reply_zh}” 过了一会儿，朋友又问：“{phrases[1].cue_zh}” "
                            f"Mia 回答：“{phrases[1].reply_zh}”"
                        ),
                        "explanation": "Two short, specific replies are easier to understand than one long message.",
                    },
                    "两条消息的连续回应",
                ),
                item(
                    "after-the-tunnel",
                    2,
                    {
                        "text": (
                            f"When the train enters a tunnel, Mia keeps her next reply ready: "
                            f'“{phrases[2].reply}” If the conversation continues after she gets out, she can add: '
                            f'“{phrases[3].reply}”'
                        ),
                        "chinese": (
                            f"地铁进隧道时，Mia 先准备好下一句：“{phrases[2].reply_zh}” "
                            f"出隧道后如果还需要继续，她再补一句：“{phrases[3].reply_zh}”"
                        ),
                        "explanation": "Preparing one useful sentence makes interruptions less disruptive.",
                    },
                    "信号中断后的继续回应",
                ),
            ],
        ),
    ]


def row_id(db: Session, table, column, code: str) -> int | None:
    row = db.execute(select(table.c.id).where(column == code)).first()
    return row[0] if row else None


def lesson_id(db: Session, material_id: int, lesson_code: str) -> int | None:
    return db.execute(
        select(m.learning_material_lesson.c.id).where(
            m.learning_material_lesson.c.material_id == material_id,
            m.learning_material_lesson.c.lesson_code == lesson_code,
        )
    ).scalar_one_or_none()


def ensure_topic(catalog: LearningCatalogService, db: Session) -> dict:
    current_id = row_id(db, m.learning_topic, m.learning_topic.c.topic_code, TOPIC_CODE)
    return catalog.save_topic(
        s.LearningTopicInput(
            module_id=2,
            topic_code=TOPIC_CODE,
            title="地铁通勤英语",
            title_en="Commute Micro English",
            description="每节约 3–5 分钟，在地铁上用单手完成听读、记忆和一句开口回应。",
            sort_order=50,
            is_published=1,
        ),
        ACTOR,
        current_id,
    )


def template_id_for(db: Session) -> int:
    template_id = row_id(db, m.learning_template, m.learning_template.c.template_code, "commute")
    if template_id is None:
        raise RuntimeError("The commute template is missing. Run create_commute_micro_english.py first.")
    return template_id


def chapter_material_payload(template_id: int, chapter: Chapter, cover_url: str) -> s.LearningMaterialInput:
    return s.LearningMaterialInput(
        template_id=template_id,
        material_code=f"commute-micro-english-stop-{chapter.number}",
        title=f"第{chapter.number}站 · {chapter.title}",
        title_en=f"Stop {chapter.number} · {chapter.title_en}",
        summary=chapter.summary,
        material_type="commute",
        publisher="Happy English",
        version_name="通勤微课 v1",
        cover_url=cover_url,
        difficulty_code="a1-a2",
        estimated_minutes=4,
        sort_order=chapter.number * 10,
        is_published=1,
    )


def chapter_course_payload(topic_id: int, material_id: int, chapter: Chapter, cover_url: str) -> s.LearningCourseInput:
    return s.LearningCourseInput(
        topic_id=topic_id,
        material_ids=[material_id],
        course_code=f"commute-micro-english-stop-{chapter.number}",
        title=f"地铁通勤英语 · 第{chapter.number}站",
        title_en=f"Commute Micro English · Stop {chapter.number}",
        summary=chapter.summary,
        course_type="commute",
        cover_url=cover_url,
        estimated_minutes=4,
        difficulty_code="a1-a2",
        sort_order=chapter.number * 10,
        is_published=1,
        access_policy="free",
    )


def seed_chapter(
    catalog: LearningCatalogService,
    db: Session,
    settings: Settings,
    template_id: int,
    topic_id: int,
    chapter: Chapter,
) -> dict:
    cover = install_illustration(settings, chapter.lessons[0], chapter.art)
    material_code = f"commute-micro-english-stop-{chapter.number}"
    current_material_id = row_id(db, m.learning_material, m.learning_material.c.material_code, material_code)
    material_payload = chapter_material_payload(template_id, chapter, cover)
    material = (
        catalog.save_material(material_payload, ACTOR, current_material_id)
        if current_material_id is not None
        else catalog.save_material(material_payload, ACTOR)
    )

    lesson_ids = []
    for lesson in chapter.lessons:
        image_url = install_illustration(settings, lesson, chapter.art)
        code = f"commute-c{lesson.chapter:02d}-l{lesson.number:02d}-{lesson.slug}"
        current_lesson_id = lesson_id(db, material["id"], code)
        saved = catalog.save_material_lesson(
            material["id"],
            s.LearningMaterialLessonInput(
                lesson_code=code,
                title=lesson.title,
                title_en=lesson.title_en,
                summary=lesson.summary,
                illustration_url=image_url,
                lesson_format="structured",
                estimated_minutes=4,
                sort_order=lesson.number * 10,
                sections=lesson_sections(lesson),
            ),
            ACTOR,
            current_lesson_id,
        )
        catalog.lesson_content.publish(saved["id"], ACTOR)
        lesson_ids.append(saved["id"])

    # Revalidate every lesson now that all illustrations have been installed.
    material = catalog.save_material(material_payload, ACTOR, material["id"])
    course_code = f"commute-micro-english-stop-{chapter.number}"
    current_course_id = row_id(db, m.learning_course, m.learning_course.c.course_code, course_code)
    course = catalog.save_course(
        chapter_course_payload(topic_id, material["id"], chapter, cover),
        ACTOR,
        current_course_id,
    )
    return {
        "chapter": chapter.number,
        "material_id": material["id"],
        "course_id": course["id"],
        "lesson_ids": lesson_ids,
    }


def main() -> None:
    validate_curriculum()
    settings = Settings()
    engine = make_engine(settings.database_url)
    with Session(engine) as db:
        catalog = LearningCatalogService(db)
        topic = ensure_topic(catalog, db)
        template_id = template_id_for(db)
        created = [
            seed_chapter(catalog, db, settings, template_id, topic["id"], chapter)
            for chapter in CHAPTERS
        ]
    print(
        json.dumps(
            {
                "topic_id": topic["id"],
                "chapters": created,
                "new_lesson_count": sum(len(chapter.lessons) for chapter in CHAPTERS),
                "total_lesson_count": 80,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
