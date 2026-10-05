"""Publish three short reference courses for the Commute Micro English topic.

Each reference course contains four four-minute lessons.  The lessons reuse the
commute lesson renderer, but their core terms are checked against the whole
existing commute catalogue before anything is written.

Run with:
    PYTHONPATH=. .venv/bin/python scripts/create_commute_reference_courses.py
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models as m
from app import schemas as s
from app.core.config import Settings
from app.core.database import make_engine
from app.services.learning_catalog import LearningCatalogService
from app.services.lesson_content import GenericLessonContentService
from scripts import complete_commute_micro_english as micro


ACTOR = micro.ACTOR
TOPIC_CODE = micro.TOPIC_CODE
REFERENCE_PREFIX = "commute-reference-"


@dataclass(frozen=True)
class ReferenceCourse:
    """A self-contained practical reference pack inside the commute topic."""

    number: int
    slug: str
    title: str
    title_en: str
    summary: str
    art: str
    lessons: tuple[micro.Lesson, ...]


def lesson_code(lesson: micro.Lesson) -> str:
    return f"commute-c{lesson.chapter:02d}-l{lesson.number:02d}-{lesson.slug}"


def material_code(reference: ReferenceCourse) -> str:
    return f"{REFERENCE_PREFIX}{reference.slug}"


def course_code(reference: ReferenceCourse) -> str:
    return material_code(reference)


# Every example is a usable reply to the question immediately before it.  The
# generic commute renderer turns these examples into the vocabulary cards,
# dialogues, quick replies and speaking prompts, so core terms always occur in
# learner-facing conversation rather than in a detached word list.
REFERENCE_COURSES: tuple[ReferenceCourse, ...] = (
    ReferenceCourse(
        11,
        "transit",
        "地铁出行速查",
        "Transit Essentials",
        "四节课看懂站内提示、处理车票、听懂线路公告，并在需要时获得帮助。",
        "route",
        (
            micro.L(
                11,
                1,
                "read-station-signs",
                "看懂站内标识",
                "Read Station Signs",
                "用四个高频站内表达确认列车方向、候车位置和乘车安全。",
                "在站台上确认列车方向和安全提示",
                "在站台上确认列车方向和安全提示。",
                "route",
                micro.P(
                    "bound for",
                    "开往……方向；目的地是……。",
                    "Used in railway information to state the destination or direction a train is travelling toward",
                    "This train is bound for Harbor Point.",
                    "这趟车开往 Harbor Point。",
                    "Does this train go toward Harbor Point?",
                    "这趟车是去 Harbor Point 方向的吗？",
                ),
                micro.P(
                    "platform edge",
                    "站台边缘。",
                    "The outer edge of a railway platform next to the tracks",
                    "Please stand behind the platform edge line.",
                    "请站在站台边缘线后面。",
                    "Where should I wait safely for the train?",
                    "我应该在哪里安全候车？",
                ),
                micro.P(
                    "mind the gap",
                    "小心站台与列车之间的缝隙。",
                    "A safety warning telling passengers to watch the space between a train and the platform",
                    "Mind the gap when you step onto the train.",
                    "上车时请小心缝隙。",
                    "Is there anything I should watch for while getting on?",
                    "上车时有什么需要注意的吗？",
                ),
                micro.P(
                    "stand clear",
                    "请避开；请不要靠近。",
                    "An instruction to keep away from doors, tracks, or another restricted area",
                    "Please stand clear of the closing doors.",
                    "请避开正在关闭的车门。",
                    "The doors are closing. What should passengers do?",
                    "车门要关了，乘客该怎么做？",
                ),
            ),
            micro.L(
                11,
                2,
                "tickets-and-fares",
                "车票与费用",
                "Tickets and Fares",
                "在闸机和售票机前，用简短表达完成刷卡、充值和费用确认。",
                "在进出站闸机前使用交通卡",
                "在进出站闸机前使用交通卡。",
                "phone",
                micro.P(
                    "tap on",
                    "进站时刷卡或碰一下感应器。",
                    "To touch a travel card or phone on a reader at the start of a trip so the journey is recorded",
                    "Remember to tap on before you enter the platform.",
                    "进站台前记得刷卡。",
                    "What do I do with my travel card at the gate?",
                    "我在闸机前要怎么用交通卡？",
                ),
                micro.P(
                    "tap off",
                    "出站时刷卡或碰一下感应器。",
                    "To touch a travel card or phone on a reader at the end of a trip to complete the fare calculation",
                    "You need to tap off when you leave the station.",
                    "离开车站时你需要刷卡出站。",
                    "Do I use my card again after the ride?",
                    "坐完车后还要再刷一次卡吗？",
                ),
                micro.P(
                    "fare cap",
                    "票价上限；在规定时段内最多扣取的车费。",
                    "The maximum amount a traveller is charged for eligible trips during a set period",
                    "I've reached the daily fare cap, so later rides are free today.",
                    "我已经达到每日票价上限，今天之后的乘车免费。",
                    "Why was I not charged for this last trip?",
                    "为什么我这最后一趟没有被扣费？",
                ),
                micro.P(
                    "top up your card",
                    "给交通卡充值。",
                    "To add money or travel credit to a transit card",
                    "You can top up your card at the machine by the gate.",
                    "你可以在闸机旁的机器上给交通卡充值。",
                    "My card balance is low. What can I do?",
                    "我的卡余额不多了，怎么办？",
                ),
            ),
            micro.L(
                11,
                3,
                "service-announcements",
                "线路公告",
                "Service Announcements",
                "遇到临时改线或施工时，听懂公告里真正影响行程的四类信息。",
                "列车临时调整时查看线路公告",
                "列车临时调整时查看线路公告。",
                "signal",
                micro.P(
                    "replacement bus",
                    "替代接驳巴士。",
                    "A bus arranged to carry passengers when a train service is disrupted",
                    "A replacement bus is running between Central and Parkside.",
                    "中央站和 Parkside 之间有替代接驳巴士运行。",
                    "The line is closed. How will passengers travel between those stations?",
                    "这条线路关闭了，乘客怎么在这两个站之间出行？",
                ),
                micro.P(
                    "service advisory",
                    "运营提示；服务变动公告。",
                    "An official notice explaining a change, disruption, or condition on a transport service",
                    "Check the service advisory before you leave for the station.",
                    "去车站前先查看运营提示。",
                    "Where can I find the latest information about this disruption?",
                    "我能在哪里找到这次故障的最新消息？",
                ),
                micro.P(
                    "single-track operation",
                    "单线运行；双向列车共用一条轨道的临时运行方式。",
                    "A temporary arrangement in which trains use one track for both directions",
                    "The line is under single-track operation through the tunnel today.",
                    "今天这条线路经过隧道时采用单线运行。",
                    "Why are trains moving more slowly through the tunnel?",
                    "为什么列车经过隧道时开得更慢？",
                ),
                micro.P(
                    "skip this stop",
                    "不停靠这一站。",
                    "To pass a station without stopping there",
                    "This train will skip this stop because of track work.",
                    "由于轨道施工，这趟车将不停靠这一站。",
                    "Why isn't the train stopping here?",
                    "为什么这趟车不在这里停？",
                ),
            ),
            micro.L(
                11,
                4,
                "station-assistance",
                "站内求助与安全",
                "Station Assistance and Safety",
                "需要找失物、无障碍入口或紧急帮助时，用清楚表达说明自己的需要。",
                "在车站寻找帮助和无障碍设施",
                "在车站寻找帮助和无障碍设施。",
                "help",
                micro.P(
                    "lost property",
                    "失物招领处；遗失物品。",
                    "The service that stores and helps return items left behind by passengers",
                    "The lost property office is beside the main exit.",
                    "失物招领处在主出口旁边。",
                    "I left my umbrella on the train. Where should I go?",
                    "我把伞落在列车上了，应该去哪里？",
                ),
                micro.P(
                    "accessible entrance",
                    "无障碍入口。",
                    "An entrance designed for people using wheelchairs, prams, or other mobility aids",
                    "Use the accessible entrance if you need the lift.",
                    "如果你需要电梯，请走无障碍入口。",
                    "Which entrance has step-free access?",
                    "哪个入口可以无台阶通行？",
                ),
                micro.P(
                    "priority seating",
                    "优先座位。",
                    "Seats reserved for passengers who may need them more, such as older people or pregnant passengers",
                    "Please leave the priority seating for passengers who need it.",
                    "请把优先座位留给有需要的乘客。",
                    "Who should these marked seats be left for?",
                    "这些标记座位应该留给谁？",
                ),
                micro.P(
                    "emergency intercom",
                    "紧急对讲装置。",
                    "A device used to contact station staff or the driver for urgent help",
                    "Press the emergency intercom only if you need urgent help.",
                    "只有需要紧急帮助时才按紧急对讲装置。",
                    "How can I contact staff quickly in an emergency?",
                    "紧急情况下，我怎么快速联系工作人员？",
                ),
            ),
        ),
    ),
    ReferenceCourse(
        12,
        "work",
        "通勤职场速查",
        "Workday Essentials",
        "四节课处理交接、会议、文档协作和远程办公状态，让通勤消息更清楚。",
        "work",
        (
            micro.L(
                12,
                1,
                "write-a-handover",
                "写好工作交接",
                "Write a Clear Handover",
                "用四个具体职场词，把交接内容、负责人和截止时间一次说明白。",
                "下班路上把项目交接给同事",
                "下班路上把项目交接给同事。",
                "work",
                micro.P(
                    "handover note",
                    "工作交接说明。",
                    "A short written update that passes task context and next steps to another person",
                    "I left a handover note with the tasks for tomorrow.",
                    "我留下了一份写有明日任务的交接说明。",
                    "Where can I see what needs to happen tomorrow?",
                    "我在哪里能看到明天要做什么？",
                ),
                micro.P(
                    "action item",
                    "待办事项；会议后需要完成的具体任务。",
                    "A specific task that someone agrees to complete after a discussion or meeting",
                    "The action item is to send the revised quote today.",
                    "待办事项是今天发出修改后的报价单。",
                    "What is the next concrete task after this meeting?",
                    "这场会议后的下一项具体任务是什么？",
                ),
                micro.P(
                    "task owner",
                    "任务负责人。",
                    "The person who is responsible for completing or coordinating a task",
                    "Mina is the task owner for the client follow-up.",
                    "Mina 是客户跟进任务的负责人。",
                    "Who is responsible for following up with the client?",
                    "谁负责跟进客户？",
                ),
                micro.P(
                    "due by",
                    "最晚在……之前完成。",
                    "Used to state the latest date or time by which something must be completed",
                    "This report is due by 3 p.m. on Friday.",
                    "这份报告最晚周五下午三点前完成。",
                    "What is the latest time I can send this report?",
                    "我最晚什么时候能发这份报告？",
                ),
            ),
            micro.L(
                12,
                2,
                "calendar-and-meetings",
                "日历与会议",
                "Calendar and Meetings",
                "在日历里安排跨时区会议前，先把议程、准备时间和链接讲清楚。",
                "在地铁上确认下周的线上会议",
                "在地铁上确认下周的线上会议。",
                "clock",
                micro.P(
                    "send an agenda",
                    "发送会议议程。",
                    "To share a list of meeting topics beforehand so people can prepare",
                    "Please send an agenda before the planning meeting.",
                    "请在计划会议前发送议程。",
                    "What should I share so everyone can prepare for the meeting?",
                    "我该分享什么，让大家能为会议做准备？",
                ),
                micro.P(
                    "block out time",
                    "预留一段不被占用的时间。",
                    "To reserve a period in a calendar for a particular task or activity",
                    "I need to block out time on Tuesday to prepare the presentation.",
                    "我需要在周二预留时间准备演示文稿。",
                    "How will you make sure you have time to prepare?",
                    "你怎么确保自己有时间准备？",
                ),
                micro.P(
                    "time zone",
                    "时区。",
                    "A region that uses the same standard time",
                    "The time zone difference puts the call at 7 a.m. for me.",
                    "时差让这场电话会议对我来说在早上七点。",
                    "Why is the meeting time so early for you?",
                    "为什么这场会议对你来说这么早？",
                ),
                micro.P(
                    "calendar invite",
                    "日历邀请；会议日程邀请。",
                    "A calendar entry sent to attendees with a meeting time and details",
                    "I sent a calendar invite with the video link.",
                    "我发了一封带视频链接的日历邀请。",
                    "Where can I find the meeting link and time?",
                    "我在哪里能找到会议链接和时间？",
                ),
            ),
            micro.L(
                12,
                3,
                "review-a-document",
                "协作文档审阅",
                "Review a Shared Document",
                "在共享文档里给出可操作的反馈，并确认最终版本能否通过。",
                "通勤中审阅同事发来的文档",
                "通勤中审阅同事发来的文档。",
                "phone",
                micro.P(
                    "leave a comment",
                    "留下评论或批注。",
                    "To add a written note or question to a specific part of a shared document",
                    "Please leave a comment where the wording is unclear.",
                    "措辞不清楚的地方请留下批注。",
                    "How should I point out a sentence that needs clarification?",
                    "我该怎么指出一句需要澄清的话？",
                ),
                micro.P(
                    "track changes",
                    "修订模式；跟踪修改。",
                    "A document feature that records edits so reviewers can see what changed",
                    "Turn on track changes before you edit the contract.",
                    "编辑合同前请打开修订模式。",
                    "How can the team see every edit I make?",
                    "团队怎样才能看到我的每一处修改？",
                ),
                micro.P(
                    "version history",
                    "版本历史。",
                    "A record showing earlier versions of a document and who made changes",
                    "The version history shows who changed that paragraph.",
                    "版本历史会显示是谁改了那一段。",
                    "Where can I check who edited this paragraph?",
                    "我在哪里能查看是谁编辑了这一段？",
                ),
                micro.P(
                    "approve the draft",
                    "批准草稿。",
                    "To confirm that a draft is ready to move to the next step or be sent out",
                    "Could you approve the draft before I send it to the client?",
                    "我发给客户之前，你能批准这份草稿吗？",
                    "What do you need from me before you send this to the client?",
                    "你发给客户前需要我做什么？",
                ),
            ),
            micro.L(
                12,
                4,
                "show-your-availability",
                "说明工作状态",
                "Show Your Availability",
                "在专注工作、远程办公或休假时，用具体说法告知同事自己的可联系时间。",
                "早高峰里设置当天的工作状态",
                "早高峰里设置当天的工作状态。",
                "signal",
                micro.P(
                    "heads-down time",
                    "专注工作时间；不受打扰的深度工作时段。",
                    "Scheduled time reserved for uninterrupted, focused work",
                    "I have heads-down time from nine to eleven.",
                    "我九点到十一点是专注工作时间。",
                    "When should I avoid interrupting you with non-urgent messages?",
                    "我什么时候应避免用不紧急的消息打扰你？",
                ),
                micro.P(
                    "out of office",
                    "不在办公室；休假或暂时无法工作。",
                    "Away from normal work and not available to respond as usual",
                    "I'll be out of office on Thursday afternoon.",
                    "我周四下午不在办公室。",
                    "Will you be available to reply on Thursday afternoon?",
                    "你周四下午能回复消息吗？",
                ),
                micro.P(
                    "working remotely",
                    "远程办公。",
                    "Doing your job from somewhere other than the usual workplace",
                    "I'm working remotely today, so please message me first.",
                    "我今天远程办公，所以请先给我发消息。",
                    "Why should I message you before calling today?",
                    "今天为什么我该先给你发消息再打电话？",
                ),
                micro.P(
                    "response time",
                    "回复所需时间。",
                    "The amount of time it usually takes someone to answer a message or request",
                    "My response time will be slower while I am travelling.",
                    "我在路上时回复会慢一些。",
                    "When should I expect to hear back from you today?",
                    "今天我大概什么时候能收到你的回复？",
                ),
            ),
        ),
    ),
    ReferenceCourse(
        13,
        "city-services",
        "城市服务速查",
        "City Services Essentials",
        "四节课覆盖药房、支付与银行、包裹领取和健身设施，适合城市通勤途中预习。",
        "help",
        (
            micro.L(
                13,
                1,
                "visit-a-pharmacy",
                "去药房买药",
                "Visit a Pharmacy",
                "说明药品是否需要处方、续药需求和用药疑问，得到更准确的帮助。",
                "下班路上到药房咨询常用药",
                "下班路上到药房咨询常用药。",
                "help",
                micro.P(
                    "over-the-counter",
                    "非处方的；无需处方即可购买。",
                    "Available to buy without a prescription from a doctor",
                    "Is this medicine available over-the-counter?",
                    "这种药可以不凭处方购买吗？",
                    "Do I need a doctor's prescription for this medicine?",
                    "我买这种药需要医生处方吗？",
                ),
                micro.P(
                    "prescription refill",
                    "处方续配；按原处方再次取药。",
                    "A new supply of medicine provided under an existing prescription",
                    "I need a prescription refill for my asthma medicine.",
                    "我的哮喘药需要按原处方续配。",
                    "What do you need from the pharmacy today?",
                    "你今天需要药房帮你办什么？",
                ),
                micro.P(
                    "side effects",
                    "副作用。",
                    "Unwanted physical or mental effects that a medicine can cause",
                    "What side effects should I look out for?",
                    "我应该留意哪些副作用？",
                    "What should I ask before I start taking this medicine?",
                    "开始服这种药前我该问什么？",
                ),
                micro.P(
                    "pharmacist",
                    "药剂师；药房中能提供用药建议的专业人员。",
                    "A qualified health professional who prepares medicines and advises people about using them",
                    "Could I speak to the pharmacist about this medicine?",
                    "我能和药剂师咨询一下这种药吗？",
                    "Who can give me professional advice about how to use this medicine?",
                    "谁能给我如何使用这种药的专业建议？",
                ),
            ),
            micro.L(
                13,
                2,
                "pay-and-bank",
                "支付与银行",
                "Pay and Bank",
                "在店铺或银行服务台前，确认支付方式、取现费用和开户材料。",
                "通勤中顺路办理支付与银行业务",
                "通勤中顺路办理支付与银行业务。",
                "phone",
                micro.P(
                    "contactless payment",
                    "非接触式支付。",
                    "A payment made by tapping a card, phone, or wearable device on a reader",
                    "Do you accept contactless payment here?",
                    "这里可以使用非接触式支付吗？",
                    "Can I pay by tapping my phone at this shop?",
                    "我能在这家店用手机碰一下付款吗？",
                ),
                micro.P(
                    "cash withdrawal",
                    "取现；从账户提取现金。",
                    "The act of taking cash out of a bank account, usually from an ATM or bank",
                    "Is there a fee for a cash withdrawal at this ATM?",
                    "在这台自动取款机取现要收费吗？",
                    "Will this ATM charge me for taking out cash?",
                    "这台 ATM 会对我取现收费吗？",
                ),
                micro.P(
                    "service counter",
                    "服务柜台。",
                    "A staffed desk where customers can ask for help with an account or service",
                    "The service counter can help you update your address.",
                    "服务柜台可以帮你更新地址。",
                    "Where should I go to change the address on my account?",
                    "我该去哪里更改账户上的地址？",
                ),
                micro.P(
                    "proof of address",
                    "住址证明。",
                    "A document that confirms where you live, such as a utility bill or tenancy agreement",
                    "Bring proof of address when you open the account.",
                    "开户时请带上住址证明。",
                    "Which document do I need to show where I live?",
                    "我需要带什么文件证明住址？",
                ),
            ),
            micro.L(
                13,
                3,
                "collect-a-parcel",
                "领取包裹",
                "Collect a Parcel",
                "到取件点前确认地点、身份核验、营业时间和排队流程，避免白跑一趟。",
                "下班后到车站附近领取包裹",
                "下班后到车站附近领取包裹。",
                "route",
                micro.P(
                    "collection point",
                    "包裹取件点。",
                    "A designated place where people collect parcels or orders",
                    "Your parcel is waiting at the collection point by the station.",
                    "你的包裹在车站旁的取件点等着。",
                    "Where can I pick up the parcel near the station?",
                    "我能在哪里领取车站附近的包裹？",
                ),
                micro.P(
                    "identity check",
                    "身份核验。",
                    "A process used to confirm that a person is who they say they are",
                    "They will do an identity check before they release the parcel.",
                    "他们会在交出包裹前进行身份核验。",
                    "Why do I need to show my ID before collecting the parcel?",
                    "为什么我取包裹前需要出示身份证件？",
                ),
                micro.P(
                    "opening hours",
                    "营业时间。",
                    "The times when a shop, office, or service is open to customers",
                    "The opening hours say the counter closes at six.",
                    "营业时间显示柜台六点关门。",
                    "What time does the collection counter close?",
                    "取件柜台几点关门？",
                ),
                micro.P(
                    "queue number",
                    "排队号码。",
                    "A numbered ticket that shows your place in a waiting line",
                    "Take a queue number and wait until it appears on the screen.",
                    "拿一张排队号码，等它出现在屏幕上。",
                    "How will I know when it is my turn at the counter?",
                    "我怎么知道什么时候轮到我到柜台办理？",
                ),
            ),
            micro.L(
                13,
                4,
                "use-a-gym",
                "使用健身设施",
                "Use a Gym",
                "试课或办理会员前，确认价格、体验安排、高峰时段和访客权限。",
                "下班路上到健身房咨询会员",
                "下班路上到健身房咨询会员。",
                "friends",
                micro.P(
                    "membership fee",
                    "会员费。",
                    "The regular amount paid to belong to a gym, club, or service",
                    "The membership fee includes access to all group classes.",
                    "会员费包括所有团体课程的使用权。",
                    "What is included in the monthly cost of joining?",
                    "每月入会费用包括什么？",
                ),
                micro.P(
                    "trial session",
                    "体验课；试用时段。",
                    "A short first session that lets someone try a service before committing to it",
                    "Can I book a trial session before I join?",
                    "我入会前可以预约一节体验课吗？",
                    "Can I try the gym once before paying for membership?",
                    "我可以先体验一次健身房再付会员费吗？",
                ),
                micro.P(
                    "peak hours",
                    "高峰时段。",
                    "The busiest times of day, when a place or service has the most users",
                    "The gym is busiest during peak hours after work.",
                    "健身房下班后的高峰时段最拥挤。",
                    "When is the gym usually most crowded?",
                    "健身房通常什么时候人最多？",
                ),
                micro.P(
                    "guest pass",
                    "访客体验券；带朋友使用设施的临时许可。",
                    "A temporary pass that allows a non-member to use a facility",
                    "Can I get a guest pass for my friend?",
                    "我能给朋友办一张访客体验券吗？",
                    "May my friend use the gym with me for one day?",
                    "我的朋友可以和我一起用一天健身房吗？",
                ),
            ),
        ),
    ),
)


def all_reference_lessons():
    for reference in REFERENCE_COURSES:
        yield from reference.lessons


def validate_reference_curriculum() -> None:
    """Fail before DB writes if source content loses its quality guarantees."""

    micro.validate_curriculum()
    if [reference.number for reference in REFERENCE_COURSES] != [11, 12, 13]:
        raise ValueError("Reference course numbers must follow the ten main stops.")

    seen = set(micro.INITIAL_CORE_TERMS)
    seen = {micro.normalise_term(term) for term in seen}
    for chapter in micro.CHAPTERS:
        seen.update(micro.normalise_term(phrase.term) for lesson in chapter.lessons for phrase in lesson.phrases)

    lesson_total = 0
    for reference in REFERENCE_COURSES:
        if len(reference.lessons) != 4:
            raise ValueError(f"{reference.slug} must contain exactly four lessons.")
        for expected_number, lesson in enumerate(reference.lessons, start=1):
            if lesson.chapter != reference.number or lesson.number != expected_number:
                raise ValueError(f"{lesson.slug} has an invalid reference course position.")
            if len(lesson.phrases) != 4:
                raise ValueError(f"{lesson.slug} must have four core phrases.")
            payload = s.LearningMaterialLessonInput(
                lesson_code=lesson_code(lesson),
                title=lesson.title,
                title_en=lesson.title_en,
                summary=lesson.summary,
                illustration_url=micro.illustration_url(lesson),
                lesson_format="structured",
                estimated_minutes=4,
                sort_order=lesson.number * 10,
                sections=micro.lesson_sections(lesson),
            )
            GenericLessonContentService.validate_sections(payload.sections, require_complete=True)
            dialogue_text = json.dumps(
                payload.sections[1].model_dump(), ensure_ascii=False
            )
            for phrase in lesson.phrases:
                key = micro.normalise_term(phrase.term)
                if key in seen:
                    raise ValueError(f"Repeated commute core phrase: {phrase.term}")
                if key not in micro.normalise_term(phrase.reply):
                    raise ValueError(f"{phrase.term} is missing from its dialogue reply.")
                if not phrase.explanation or not phrase.meaning or not phrase.reply_zh:
                    raise ValueError(f"{phrase.term} needs an English explanation and bilingual example.")
                if phrase.reply not in dialogue_text:
                    raise ValueError(f"{phrase.term} is not covered by a situational dialogue.")
                seen.add(key)
            image = micro.illustration_svg(lesson, reference.art).encode("utf-8")
            if len(image) >= micro.MAX_ILLUSTRATION_BYTES:
                raise ValueError(f"{lesson.slug} illustration exceeds 100KB.")
            lesson_total += 1

    if lesson_total != 12 or len(seen) != 368:
        raise ValueError("Reference curriculum must add twelve lessons and forty-eight core terms.")


def existing_commute_core_terms(db: Session) -> dict[str, set[str]]:
    """Return every currently stored commute core term and its lesson code."""

    rows = db.execute(
        select(
            m.learning_material_lesson.c.lesson_code,
            m.learning_lesson_item.c.payload_json,
        )
        .select_from(
            m.learning_material_lesson.join(
                m.learning_lesson_section,
                m.learning_lesson_section.c.lesson_id == m.learning_material_lesson.c.id,
            ).join(
                m.learning_lesson_item,
                m.learning_lesson_item.c.section_id == m.learning_lesson_section.c.id,
            )
        )
        .where(m.learning_material_lesson.c.lesson_code.like("commute-%"))
        .where(m.learning_lesson_section.c.section_code == "core_vocabulary")
    ).all()
    result: dict[str, set[str]] = {}
    for code, raw_payload in rows:
        try:
            term = json.loads(raw_payload).get("term")
        except (TypeError, ValueError, AttributeError) as error:
            raise ValueError(f"Invalid core vocabulary payload in {code}.") from error
        if term:
            result.setdefault(micro.normalise_term(term), set()).add(code)
    return result


def assert_no_database_term_collisions(db: Session) -> None:
    """Allow a rerun of the same lesson, reject reuse anywhere else."""

    planned = {
        micro.normalise_term(phrase.term): lesson_code(lesson)
        for lesson in all_reference_lessons()
        for phrase in lesson.phrases
    }
    collisions = []
    for term, lesson_codes in existing_commute_core_terms(db).items():
        expected_lesson = planned.get(term)
        if expected_lesson is None:
            continue
        foreign_lessons = sorted(code for code in lesson_codes if code != expected_lesson)
        if foreign_lessons:
            collisions.append((term, foreign_lessons, expected_lesson))
    if collisions:
        details = "; ".join(
            f"{term}: already in {', '.join(codes)} (planned for {planned_code})"
            for term, codes, planned_code in collisions
        )
        raise ValueError(f"Reference courses repeat existing commute core terms: {details}")


def reference_material_payload(
    template_id: int, reference: ReferenceCourse, cover_url: str
) -> s.LearningMaterialInput:
    return s.LearningMaterialInput(
        template_id=template_id,
        material_code=material_code(reference),
        title=f"通勤资料 · {reference.title}",
        title_en=f"Commute Reference · {reference.title_en}",
        summary=reference.summary,
        material_type="commute",
        publisher="Happy English",
        version_name="通勤速查 v1",
        cover_url=cover_url,
        difficulty_code="a2-b1",
        estimated_minutes=16,
        sort_order=reference.number * 10,
        is_published=1,
    )


def reference_course_payload(
    topic_id: int, material_id: int, reference: ReferenceCourse, cover_url: str
) -> s.LearningCourseInput:
    return s.LearningCourseInput(
        topic_id=topic_id,
        material_ids=[material_id],
        course_code=course_code(reference),
        title=f"地铁通勤英语 · {reference.title}",
        title_en=f"Commute Micro English · {reference.title_en}",
        summary=reference.summary,
        course_type="commute",
        cover_url=cover_url,
        estimated_minutes=16,
        difficulty_code="a2-b1",
        sort_order=reference.number * 10,
        is_published=1,
        access_policy="free",
    )


def seed_reference_course(
    catalog: LearningCatalogService,
    db: Session,
    settings: Settings,
    template_id: int,
    topic_id: int,
    reference: ReferenceCourse,
) -> dict:
    cover = micro.install_illustration(settings, reference.lessons[0], reference.art)
    current_material_id = micro.row_id(
        db, m.learning_material, m.learning_material.c.material_code, material_code(reference)
    )
    material_payload = reference_material_payload(template_id, reference, cover)
    material = (
        catalog.save_material(material_payload, ACTOR, current_material_id)
        if current_material_id is not None
        else catalog.save_material(material_payload, ACTOR)
    )

    lesson_ids = []
    for lesson in reference.lessons:
        image_url = micro.install_illustration(settings, lesson, reference.art)
        code = lesson_code(lesson)
        current_lesson_id = micro.lesson_id(db, material["id"], code)
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
                sections=micro.lesson_sections(lesson),
            ),
            ACTOR,
            current_lesson_id,
        )
        catalog.lesson_content.publish(saved["id"], ACTOR)
        lesson_ids.append(saved["id"])

    # Save again only after all lesson images and structured sections exist,
    # so the material is valid as a public course entry.
    material = catalog.save_material(material_payload, ACTOR, material["id"])
    current_course_id = micro.row_id(
        db, m.learning_course, m.learning_course.c.course_code, course_code(reference)
    )
    course = catalog.save_course(
        reference_course_payload(topic_id, material["id"], reference, cover),
        ACTOR,
        current_course_id,
    )
    return {
        "reference": reference.slug,
        "material_id": material["id"],
        "course_id": course["id"],
        "lesson_ids": lesson_ids,
    }


def audit_reference_courses(db: Session, topic_id: int) -> dict:
    """Verify the public records, exact term count, and installed image files."""

    course_rows = db.execute(
        select(
            m.learning_course.c.id,
            m.learning_course.c.course_code,
            m.learning_course.c.is_published,
            m.learning_material.c.id.label("material_id"),
            m.learning_material.c.material_code,
            m.learning_material.c.is_published.label("material_published"),
        )
        .select_from(
            m.learning_topic_course.join(
                m.learning_course,
                m.learning_course.c.id == m.learning_topic_course.c.course_id,
            ).join(
                m.learning_course_material,
                m.learning_course_material.c.course_id == m.learning_course.c.id,
            ).join(
                m.learning_material,
                m.learning_material.c.id == m.learning_course_material.c.material_id,
            )
        )
        .where(m.learning_topic_course.c.topic_id == topic_id)
        .where(m.learning_course.c.course_code.like("commute-%"))
        .order_by(m.learning_topic_course.c.sort_order)
    ).mappings().all()
    material_ids = [row["material_id"] for row in course_rows]
    lesson_rows = db.execute(
        select(
            m.learning_material_lesson.c.id,
            m.learning_material_lesson.c.lesson_code,
            m.learning_material_lesson.c.illustration_url,
            m.learning_material_lesson.c.is_published,
            m.learning_material_lesson.c.content_status,
        )
        .where(m.learning_material_lesson.c.material_id.in_(material_ids))
        .order_by(m.learning_material_lesson.c.lesson_code)
    ).mappings().all()

    term_map = existing_commute_core_terms(db)
    duplicates = {
        term: sorted(codes) for term, codes in term_map.items() if len(codes) > 1
    }
    static_dir = Settings().static_dir
    missing_images = []
    for lesson in lesson_rows:
        image_url = lesson["illustration_url"] or ""
        if not image_url.startswith("/static/"):
            missing_images.append(lesson["lesson_code"])
            continue
        path = static_dir / image_url.removeprefix("/static/")
        if not path.exists() or path.stat().st_size >= micro.MAX_ILLUSTRATION_BYTES:
            missing_images.append(lesson["lesson_code"])

    return {
        "topic_id": topic_id,
        "course_count": len(course_rows),
        "material_count": len({row["material_id"] for row in course_rows}),
        "lesson_count": len(lesson_rows),
        "core_phrase_count": len(term_map),
        "duplicate_core_phrases": duplicates,
        "unpublished_courses": [
            row["course_code"]
            for row in course_rows
            if row["is_published"] != 1 or row["material_published"] != 1
        ],
        "unpublished_lessons": [
            row["lesson_code"]
            for row in lesson_rows
            if row["is_published"] != 1 or row["content_status"] != "published"
        ],
        "image_problems": missing_images,
        "reference_course_codes": [
            row["course_code"]
            for row in course_rows
            if row["course_code"].startswith(REFERENCE_PREFIX)
        ],
    }


def main() -> None:
    validate_reference_curriculum()
    settings = Settings()
    engine = make_engine(settings.database_url)
    with Session(engine) as db:
        catalog = LearningCatalogService(db)
        topic = micro.ensure_topic(catalog, db)
        assert_no_database_term_collisions(db)
        template_id = micro.template_id_for(db)
        created = [
            seed_reference_course(catalog, db, settings, template_id, topic["id"], reference)
            for reference in REFERENCE_COURSES
        ]
        audit = audit_reference_courses(db, topic["id"])

    if (
        audit["course_count"] != 13
        or audit["material_count"] != 13
        or audit["lesson_count"] != 92
        or audit["core_phrase_count"] != 368
        or audit["duplicate_core_phrases"]
        or audit["unpublished_courses"]
        or audit["unpublished_lessons"]
        or audit["image_problems"]
        or len(audit["reference_course_codes"]) != 3
    ):
        raise RuntimeError(f"Commute reference course audit failed: {audit}")

    print(json.dumps({"created": created, "audit": audit}, ensure_ascii=False))


if __name__ == "__main__":
    main()
