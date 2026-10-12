"""Create the original ``日常生活英语`` guided curriculum.

The lesson sequence follows the everyday-life scene progression in the
``English for Everyday Activities`` reference PDF in ``lecture/``.  The PDF
is a scanned reference, so this script deliberately creates new learning
copy, short dialogues, and speaking prompts instead of importing its pages
or transcribing its text.

Run with:

    PYTHONPATH=. .venv/bin/python scripts/create_everyday_activities_english.py

The script is idempotent.  It creates six one-material courses because the
mini-program roadmap presents a topic as a vertical textbook-by-textbook
path.  Every material lesson is structured into individual learning screens,
but it uses a concise, natural scene rather than padding it with repeated
"say this again" prompts.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw
from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from app import models as m
from app import schemas as s
from app.core.config import Settings
from app.core.database import make_engine
from app.services.learning_catalog import LearningCatalogService


ACTOR = {"id": 1}
TOPIC_CODE = "everyday-activities-english"
MODULE_CODE = "elementary-english"
TEMPLATE_CODE = "dialogue"
STATIC_SUBDIRECTORY = Path("images/learning_material/icon")
BENEFIT_CODE = "all-courses-access"


@dataclass(frozen=True)
class Lesson:
    """One short, self-contained scene lesson with original learning copy."""

    number: int
    title: str
    title_en: str
    scene: str
    term: str
    meaning: str
    support_term: str
    support_meaning: str
    sentence: str
    sentence_zh: str
    cue: str
    cue_zh: str
    icon: str


@dataclass(frozen=True)
class Material:
    """One roadmap textbook / one learner-facing course."""

    number: int
    title: str
    title_en: str
    summary: str
    icon: str
    lessons: tuple[Lesson, ...]


def L(
    number: int,
    title: str,
    title_en: str,
    scene: str,
    term: str,
    meaning: str,
    support_term: str,
    support_meaning: str,
    sentence: str,
    sentence_zh: str,
    cue: str,
    cue_zh: str,
    icon: str,
) -> Lesson:
    return Lesson(
        number,
        title,
        title_en,
        scene,
        term,
        meaning,
        support_term,
        support_meaning,
        sentence,
        sentence_zh,
        cue,
        cue_zh,
        icon,
    )


# These are concise, newly authored micro-lessons.  Their scene ordering is
# inspired by the reference book; none of the scanned pages or page copy is
# stored in the product.
MATERIALS: tuple[Material, ...] = (
    Material(
        1,
        "教材一 · 晨间开始",
        "Starting the Day",
        "从醒来到出门，用 11 个晨间场景把每天都会说的英语变成自然反应。",
        "morning",
        (
            L(1, "醒来", "Waking Up", "早晨醒来后聊起床时间", "wake up", "醒来", "get out of bed", "起床", "I wake up at seven on weekdays.", "工作日我七点醒来。", "What time do you usually wake up?", "你通常几点醒来？", "morning"),
            L(2, "刷牙和使用牙线", "Brushing Your Teeth", "洗漱时描述自己的习惯", "brush my teeth", "刷牙", "floss my teeth", "用牙线清洁牙齿", "I brush my teeth after breakfast.", "我早餐后刷牙。", "Do you brush your teeth before breakfast?", "你在早餐前刷牙吗？", "tooth"),
            L(3, "洗澡", "Taking a Shower", "早晨准备出门前的洗澡时间", "take a shower", "洗澡", "wash my hair", "洗头", "I take a quick shower in the morning.", "我早晨快速冲个澡。", "Do you have time for a shower?", "你有时间洗个澡吗？", "shower"),
            L(4, "男士穿衣", "Getting Dressed · A Man", "出门前选择衬衫和鞋子", "put on a shirt", "穿上一件衬衫", "put on my shoes", "穿上鞋", "I put on a clean shirt for work.", "我上班会穿一件干净的衬衫。", "What are you going to wear today?", "你今天打算穿什么？", "clothes"),
            L(5, "女士穿衣", "Getting Dressed · A Woman", "根据天气挑选当天的衣服", "choose an outfit", "挑选一套衣服", "try on clothes", "试穿衣服", "I choose a light outfit for the warm weather.", "天气暖和，我选一套轻便的衣服。", "Is it warm enough for a dress today?", "今天暖和到可以穿裙子吗？", "clothes"),
            L(6, "整理床铺", "Making a Bed", "早晨离开卧室前整理床", "make the bed", "整理床铺", "straighten the sheets", "整理床单", "I make the bed before I leave the room.", "我离开房间前会整理床铺。", "Do you make your bed every morning?", "你每天早晨整理床铺吗？", "bed"),
            L(7, "冲咖啡和泡茶", "Making Coffee or Tea", "早晨为自己或家人准备热饮", "make a cup of coffee", "冲一杯咖啡", "make tea", "泡茶", "I make a cup of tea before work.", "我上班前会泡一杯茶。", "Would you like coffee or tea?", "你想喝咖啡还是茶？", "coffee"),
            L(8, "准备麦片和吐司", "Cereal and Toast", "快速准备简单早餐", "pour cereal", "倒麦片", "make toast", "烤吐司", "I pour cereal into a bowl and add milk.", "我把麦片倒进碗里，再加牛奶。", "Would you like some toast with breakfast?", "早餐要来点吐司吗？", "breakfast"),
            L(9, "煎鸡蛋", "Frying an Egg", "在厨房里说早餐的做法", "fry an egg", "煎鸡蛋", "crack an egg", "打一个鸡蛋", "I fry an egg for breakfast on Sundays.", "周日我会煎个鸡蛋当早餐。", "How do you like your eggs?", "你的鸡蛋喜欢怎么做？", "egg"),
            L(10, "吃早餐", "Eating Breakfast", "和家人一起吃早餐", "have breakfast", "吃早餐", "drink orange juice", "喝橙汁", "We have breakfast together when we can.", "有机会时我们会一起吃早餐。", "Are you ready for breakfast?", "你准备好吃早餐了吗？", "meal"),
            L(11, "离开家", "Leaving the House", "出门前确认随身物品和门锁", "lock the door", "锁门", "grab my keys", "拿上钥匙", "I lock the door and check my keys.", "我锁好门，再确认钥匙带了。", "Do you have everything you need?", "你需要的东西都带齐了吗？", "door"),
        ),
    ),
    Material(
        2,
        "教材二 · 城市出行",
        "Getting Around",
        "坐公交、开车、乘火车或骑车，掌握 8 个在路上马上能用的场景。",
        "transport",
        (
            L(1, "乘公交车", "Taking a Bus", "在公交站等车并确认线路", "catch the bus", "赶上公交车", "wait at the bus stop", "在公交站等候", "I catch the bus near my home every morning.", "我每天早晨在家附近坐公交。", "Which bus goes to the station?", "哪路公交去车站？", "bus"),
            L(2, "开车出发", "Starting Out by Car", "上车后准备开始驾驶", "start the car", "启动汽车", "check the mirrors", "查看后视镜", "I start the car after I check the mirrors.", "我查看后视镜后再启动汽车。", "Are you ready to leave?", "你准备好出发了吗？", "car"),
            L(3, "操作汽车", "Operating a Car", "驾驶前确认安全步骤", "fasten my seat belt", "系好安全带", "use the brakes", "踩刹车", "I fasten my seat belt before we move.", "我们出发前，我会系好安全带。", "Have you fastened your seat belt?", "你系好安全带了吗？", "car"),
            L(4, "沿路驾驶", "Driving Along", "根据路标在城市里开车", "turn left", "左转", "follow the signs", "按照路标行驶", "Turn left at the next set of lights.", "在下一个红绿灯左转。", "Do we turn here or at the lights?", "我们在这里转，还是在红绿灯转？", "directions"),
            L(5, "乘火车", "Taking a Train", "在站台确认要乘坐的列车", "take the train", "坐火车", "check the platform", "确认站台", "I take the train into the city on Fridays.", "周五我坐火车进城。", "Which platform is the train leaving from?", "火车从哪个站台发车？", "train"),
            L(6, "乘出租车", "Taking a Taxi", "上车后告诉司机目的地", "get a taxi", "打车", "tell the driver my destination", "告诉司机目的地", "I get a taxi when I have heavy bags.", "行李很重时我会打车。", "Where would you like to go?", "您想去哪里？", "taxi"),
            L(7, "步行前往", "Walking Somewhere", "在城市里步行去附近地点", "walk to the station", "步行去车站", "cross the street", "过马路", "I walk to the station when the weather is nice.", "天气好时我步行去车站。", "Is the station within walking distance?", "车站步行能到吗？", "walk"),
            L(8, "骑自行车", "Riding a Bicycle", "出发前检查安全装备", "ride a bike", "骑自行车", "wear a helmet", "戴头盔", "I ride my bike to the park at weekends.", "周末我骑自行车去公园。", "Do you always wear a helmet?", "你总是戴头盔吗？", "bike"),
        ),
    ),
    Material(
        3,
        "教材三 · 晚间居家",
        "At Home in the Evening",
        "回家、做饭、放松到睡觉，用 14 个晚间生活场景练习家庭英语。",
        "home",
        (
            L(1, "回到家", "Returning Home", "结束一天后回家放松", "get home", "到家", "take off my shoes", "脱鞋", "I get home around six in the evening.", "我傍晚六点左右到家。", "What time do you usually get home?", "你通常几点到家？", "home"),
            L(2, "做沙拉", "Making a Salad", "晚餐前准备一份简单沙拉", "make a salad", "做沙拉", "wash the lettuce", "洗生菜", "I make a salad with tomatoes and cheese.", "我用番茄和奶酪做沙拉。", "Would you like a salad with dinner?", "晚餐要来份沙拉吗？", "salad"),
            L(3, "处理蔬菜", "Preparing Vegetables", "做饭前清洗和切配蔬菜", "chop the vegetables", "切蔬菜", "peel a carrot", "削胡萝卜皮", "I chop the vegetables before I start cooking.", "开始做饭前，我先把蔬菜切好。", "Can you help me prepare the vegetables?", "你能帮我处理一下蔬菜吗？", "vegetables"),
            L(4, "煮意大利面", "Making Spaghetti", "准备一道简单的意大利面", "boil the pasta", "煮意大利面", "add the sauce", "加酱汁", "I boil the pasta while the sauce is heating.", "酱汁加热时，我煮意大利面。", "Is the pasta ready yet?", "意大利面做好了吗？", "pasta"),
            L(5, "煮米饭", "Cooking Rice", "为晚餐准备米饭", "cook rice", "煮米饭", "use a rice cooker", "使用电饭煲", "I cook rice in the rice cooker.", "我用电饭煲煮米饭。", "How much rice should we make?", "我们应该煮多少米饭？", "rice"),
            L(6, "吃晚餐", "Eating Dinner", "和家人坐下来吃晚餐", "sit down for dinner", "坐下来吃晚餐", "pass the food", "递食物", "We sit down for dinner at half past six.", "我们六点半坐下来吃晚餐。", "Can you pass the vegetables, please?", "请把蔬菜递给我，好吗？", "meal"),
            L(7, "收拾餐桌", "Clearing the Table", "饭后把盘子和剩菜收起来", "clear the table", "收拾餐桌", "put away leftovers", "收好剩菜", "I clear the table after everyone finishes eating.", "大家吃完后，我收拾餐桌。", "Can I help clear the table?", "我可以帮忙收拾餐桌吗？", "table"),
            L(8, "洗碗", "Doing the Dishes", "饭后分工洗碗和擦干", "wash the dishes", "洗碗", "dry the dishes", "擦干餐具", "I wash the dishes, and my brother dries them.", "我洗碗，哥哥擦干。", "Would you like me to wash or dry?", "你想让我洗还是擦干？", "dishes"),
            L(9, "使用互联网", "Using the Internet", "在家上网查资料或安排事情", "go online", "上网", "search for information", "搜索信息", "I go online to check the weather for tomorrow.", "我上网查看明天的天气。", "Can you search for the address online?", "你能上网查一下地址吗？", "laptop"),
            L(10, "听音乐", "Listening to Music", "在家用手机放松听歌", "listen to music", "听音乐", "charge my phone", "给手机充电", "I listen to music while I make dinner.", "我做晚餐时听音乐。", "What kind of music do you like to listen to?", "你喜欢听什么类型的音乐？", "music"),
            L(11, "读书", "Reading", "睡前留一点时间阅读", "read a book", "读书", "turn the page", "翻页", "I read a book for twenty minutes before bed.", "我睡前读二十分钟书。", "What are you reading at the moment?", "你现在在读什么？", "book"),
            L(12, "看电视", "Watching Television", "晚上选一个节目放松", "watch TV", "看电视", "change the channel", "换台", "We watch TV after dinner sometimes.", "我们有时晚餐后看电视。", "Can you change the channel?", "你能换个台吗？", "tv"),
            L(13, "看电影", "Watching a Movie", "在家选择一部电影一起看", "watch a movie", "看电影", "choose a film", "选一部电影", "Let's watch a movie after the kids are asleep.", "孩子们睡着后，我们看部电影吧。", "Which film would you like to watch?", "你想看哪部电影？", "movie"),
            L(14, "去睡觉", "Going to Bed", "结束一天并准备第二天", "go to bed", "去睡觉", "set an alarm", "设闹钟", "I go to bed early when I have work the next day.", "第二天要上班时我会早点睡。", "What time do you need to get up tomorrow?", "你明天几点要起床？", "sleep"),
        ),
    ),
    Material(
        4,
        "教材四 · 打理家庭",
        "Managing a Household",
        "洗衣、照顾宠物、购物和银行事务，覆盖 10 个高频家庭任务。",
        "household",
        (
            L(1, "洗衣服", "Doing Laundry", "把衣服分类、清洗和晾好", "do the laundry", "洗衣服", "hang up clothes", "晾衣服", "I do the laundry on Saturday morning.", "我周六早晨洗衣服。", "Have you done the laundry this week?", "你这周洗衣服了吗？", "laundry"),
            L(2, "打扫房间", "Cleaning the House", "安排家里的日常清洁", "clean the house", "打扫房子", "vacuum the floor", "用吸尘器清扫地板", "I clean the house before guests arrive.", "客人来之前我会打扫房子。", "Which room should we clean first?", "我们应该先打扫哪个房间？", "cleaning"),
            L(3, "照顾猫咪", "Taking Care of a Cat", "给猫喂食并处理日常用品", "feed the cat", "喂猫", "clean the litter box", "清理猫砂盆", "I feed the cat before I leave for work.", "我上班前会喂猫。", "Has the cat eaten today?", "猫今天吃过了吗？", "cat"),
            L(4, "照顾狗狗", "Taking Care of a Dog", "带狗出门散步", "walk the dog", "遛狗", "put a leash on the dog", "给狗系上牵引绳", "I walk the dog after dinner every day.", "我每天晚餐后遛狗。", "Would you like to walk the dog with me?", "你想和我一起遛狗吗？", "dog"),
            L(5, "清洗汽车", "Cleaning a Car", "清洗车身和车窗", "wash the car", "洗车", "clean the windows", "擦车窗", "I wash the car when the weather is sunny.", "天气晴朗时我会洗车。", "Does the car need a wash?", "车需要洗吗？", "car"),
            L(6, "送车去维修", "Taking a Car to a Garage", "联系车行预约检查", "take the car in", "把车送去维修", "book an appointment", "预约时间", "I need to take the car in for a service.", "我得把车送去保养。", "Can I book an appointment for Friday?", "我能预约周五吗？", "garage"),
            L(7, "购买日用品", "Shopping for Groceries", "列清单并在超市购买食材", "buy groceries", "购买日用品", "make a shopping list", "列购物清单", "I buy groceries on my way home.", "我回家路上买日用品。", "What do we need from the supermarket?", "我们需要从超市买什么？", "groceries"),
            L(8, "付款", "Paying for Things", "结账时选择合适的支付方式", "pay by card", "刷卡付款", "keep the receipt", "保留收据", "I'd like to pay by card, please.", "我想刷卡付款，谢谢。", "Would you like to pay by cash or card?", "您想付现金还是刷卡？", "payment"),
            L(9, "去银行", "Going to a Bank", "办理简单的存款业务", "go to the bank", "去银行", "deposit money", "存钱", "I need to go to the bank after lunch.", "午饭后我得去银行。", "What do you need to do at the bank?", "你去银行要办什么？", "bank"),
            L(10, "使用取款机", "Using an ATM", "在取款机上查看余额或取现", "withdraw cash", "取现金", "check my balance", "查看余额", "I need to withdraw some cash from the ATM.", "我需要从取款机取些现金。", "Do you know where the nearest ATM is?", "你知道最近的取款机在哪里吗？", "atm"),
        ),
    ),
    Material(
        5,
        "教材五 · 保持联系",
        "Keeping in Touch",
        "从邮件到电话和信件，用 9 个沟通场景把联系他人的英语说得清楚自然。",
        "contact",
        (
            L(1, "收发邮件", "Getting and Sending Emails", "查看邮件并回复重要信息", "check my email", "查看邮件", "reply to a message", "回复消息", "I check my email before my first meeting.", "我第一次会议前会查看邮件。", "Have you replied to that email yet?", "你回复那封邮件了吗？", "email"),
            L(2, "使用手机和发短信", "Texting", "不方便通话时发送简短信息", "send a text", "发短信", "call back later", "稍后回电", "I'll send you a text when I arrive.", "我到了会给你发短信。", "Can you send me the details by text?", "你能把细节短信发给我吗？", "text"),
            L(3, "打电话", "Making a Phone Call", "给朋友或同事拨打电话", "make a phone call", "打电话", "leave a voicemail", "留下语音留言", "I need to make a quick phone call.", "我需要打一个简短的电话。", "Is now a good time to call?", "现在方便打电话吗？", "phone"),
            L(4, "接电话", "Answering a Telephone", "礼貌地接起来电", "answer the phone", "接电话", "say hello", "打招呼", "I answer the phone with a friendly hello.", "我会友好地说 hello 来接电话。", "Can you answer the phone for me?", "你能帮我接一下电话吗？", "phone"),
            L(5, "留言", "Leaving a Message", "对方不在时留下清楚留言", "leave a message", "留言", "call back later", "稍后回电", "Please leave a message after the beep.", "请在提示音后留言。", "Would you like to leave a message?", "您想留言吗？", "message"),
            L(6, "记录留言", "Taking a Message", "替别人接听并记下重点", "take a message", "记录留言", "write it down", "写下来", "I'll take a message and let her know.", "我会记下留言并告诉她。", "Can you take a message for him?", "你能帮他记个留言吗？", "note"),
            L(7, "听语音留言", "Checking Voicemail", "查看错过的来电和语音", "listen to voicemail", "听语音留言", "check missed calls", "查看未接来电", "I listen to my voicemail after work.", "下班后我会听语音留言。", "Did anyone leave a voicemail?", "有人留语音留言吗？", "message"),
            L(8, "写私人信件", "Writing a Personal Letter", "把近况写给远方的朋友", "write a letter", "写一封信", "write by hand", "手写", "I write a letter to my grandmother every month.", "我每个月给奶奶写一封信。", "When did you last write a letter?", "你上次写信是什么时候？", "letter"),
            L(9, "寄信", "Mailing a Letter", "准备邮票并把信寄出去", "mail a letter", "寄信", "buy a stamp", "买邮票", "I need to mail this letter today.", "我今天得把这封信寄出去。", "Where is the nearest post box?", "最近的邮筒在哪里？", "stamp"),
        ),
    ),
    Material(
        6,
        "教材六 · 和朋友享受生活",
        "Having Fun with Friends",
        "生日、聚餐、电影、快餐和咖啡馆，用 5 个社交场景练习轻松自然的邀请和回应。",
        "friends",
        (
            L(1, "参加生日派对", "Going to a Birthday Party", "给朋友准备生日祝福和礼物", "bring a present", "带一份礼物", "say happy birthday", "说生日快乐", "I'm bringing a small present for her birthday.", "我会给她的生日带一份小礼物。", "What should we get for her birthday?", "我们该给她买什么生日礼物？", "gift"),
            L(2, "参加晚餐聚会", "Going to a Dinner Party", "邀请朋友到家里共进晚餐", "invite friends over", "邀请朋友来家里", "set the table", "摆餐桌", "We're inviting friends over for dinner on Saturday.", "我们周六邀请朋友来家里吃饭。", "What time should we come over?", "我们几点过去合适？", "party"),
            L(3, "去看电影", "Going to a Movie", "约朋友选电影和买票", "go to the movies", "去看电影", "buy a ticket", "买票", "Let's go to the movies this weekend.", "这个周末我们去看电影吧。", "Which movie would you like to see?", "你想看哪部电影？", "movie"),
            L(4, "吃快餐", "At a Fast Food Restaurant", "在快餐店选择餐点并下单", "place an order", "点单", "choose a meal", "选择套餐", "I'd like to place an order for two meals.", "我想点两份套餐。", "Are you ready to order?", "您准备好点单了吗？", "burger"),
            L(5, "在咖啡馆见面", "At a Coffee Shop", "约朋友喝咖啡并选择饮品", "meet for coffee", "约喝咖啡", "order a latte", "点一杯拿铁", "Let's meet for coffee after work.", "我们下班后一起喝咖啡吧。", "What would you like to drink?", "你想喝点什么？", "coffee"),
        ),
    ),
)


# A scene needs one more genuinely useful line than a generic "say it again"
# prompt.  These lines are authored per scene so the dialogue keeps a natural
# relationship to the activity instead of manufacturing an answer template.
NATURAL_SCENE_DETAILS: dict[str, tuple[str, str]] = {
    "Waking Up": (
        "I usually get out of bed as soon as the alarm rings.",
        "闹钟一响，我通常就起床。",
    ),
    "Brushing Your Teeth": (
        "I floss before I brush, especially at night.",
        "我通常在刷牙前用牙线，尤其是在晚上。",
    ),
    "Taking a Shower": (
        "I wash my hair every other day.",
        "我隔一天洗一次头。",
    ),
    "Getting Dressed · A Man": (
        "I choose my shoes after I pick a shirt.",
        "我选好衬衫后再挑鞋。",
    ),
    "Getting Dressed · A Woman": (
        "I check the weather before I decide what to wear.",
        "我决定穿什么之前会看天气。",
    ),
    "Making a Bed": (
        "I pull up the sheets and smooth the pillow.",
        "我会拉平床单，再整理枕头。",
    ),
    "Making Coffee or Tea": (
        "I make tea when I want something lighter.",
        "我想喝清淡一点时会泡茶。",
    ),
    "Cereal and Toast": (
        "I make toast if I need something warm.",
        "我想吃点热的时会烤吐司。",
    ),
    "Frying an Egg": (
        "I crack the egg into a small bowl first.",
        "我先把鸡蛋打进一个小碗。",
    ),
    "Eating Breakfast": (
        "I usually drink orange juice with it.",
        "我通常配着早餐喝橙汁。",
    ),
    "Leaving the House": (
        "I grab my keys just before I step outside.",
        "我迈出门前会拿上钥匙。",
    ),
    "Taking a Bus": (
        "I wait at the stop a few minutes early.",
        "我会提前几分钟到站等车。",
    ),
    "Starting Out by Car": (
        "I check the mirrors before I start the car.",
        "开车前我会先看后视镜。",
    ),
    "Operating a Car": (
        "I use the brakes gently near the lights.",
        "到红绿灯附近时我会轻踩刹车。",
    ),
    "Driving Along": (
        "I follow the signs until I see the right street.",
        "我沿着路标走，直到看到正确的街道。",
    ),
    "Taking a Train": (
        "I check the platform number on the board.",
        "我在显示牌上确认站台号。",
    ),
    "Taking a Taxi": (
        "I tell the driver exactly where I need to go.",
        "我会准确告诉司机要去哪里。",
    ),
    "Walking Somewhere": (
        "I cross at the lights when the road is busy.",
        "路上繁忙时我会从红绿灯处过马路。",
    ),
    "Riding a Bicycle": (
        "I always wear a helmet when I ride.",
        "骑车时我总会戴头盔。",
    ),
    "Returning Home": (
        "I take off my shoes and put my bag down.",
        "我脱下鞋，再放下包。",
    ),
    "Making a Salad": (
        "I wash the lettuce before I add the other ingredients.",
        "我加其他食材前会先洗生菜。",
    ),
    "Preparing Vegetables": (
        "I peel the carrot before I chop it.",
        "我先削胡萝卜，再把它切好。",
    ),
    "Making Spaghetti": (
        "I add the sauce when the pasta is almost ready.",
        "意面快熟时我会加酱汁。",
    ),
    "Cooking Rice": (
        "I use the rice cooker so the rice stays warm.",
        "我用电饭煲让米饭保持温热。",
    ),
    "Eating Dinner": (
        "I pass the food around so everyone can help themselves.",
        "我把食物传过去，让大家自己取。",
    ),
    "Clearing the Table": (
        "I put the leftovers in the fridge for tomorrow.",
        "我把剩菜放进冰箱留到明天。",
    ),
    "Doing the Dishes": (
        "I dry the dishes and put them away.",
        "我把餐具擦干，再收好。",
    ),
    "Using the Internet": (
        "I search for the address before I leave home.",
        "我出门前会查好地址。",
    ),
    "Listening to Music": (
        "I charge my phone while I make dinner.",
        "我做晚餐时会给手机充电。",
    ),
    "Reading": (
        "I turn the page when I finish a chapter.",
        "读完一章后我会翻页。",
    ),
    "Watching Television": (
        "I change the channel if there is nothing interesting on.",
        "没有有趣节目时我会换台。",
    ),
    "Watching a Movie": (
        "I choose a film before we sit down.",
        "我们坐下前会先选一部电影。",
    ),
    "Going to Bed": (
        "I set an alarm before I go to bed.",
        "我睡觉前会设好闹钟。",
    ),
    "Doing Laundry": (
        "I hang up the clothes while they are still warm.",
        "衣服还温着的时候我会晾起来。",
    ),
    "Cleaning the House": (
        "I vacuum the floor after I tidy the room.",
        "我整理完房间后会吸地。",
    ),
    "Taking Care of a Cat": (
        "I clean the litter box every morning.",
        "我每天早晨清理猫砂盆。",
    ),
    "Taking Care of a Dog": (
        "I put a leash on the dog before we go outside.",
        "出门前我会给狗系好牵引绳。",
    ),
    "Cleaning a Car": (
        "I clean the windows with a soft cloth.",
        "我用软布擦车窗。",
    ),
    "Taking a Car to a Garage": (
        "I book an appointment before I take the car in.",
        "我送车去维修前会先预约。",
    ),
    "Shopping for Groceries": (
        "I make a shopping list before I go to the supermarket.",
        "我去超市前会列购物清单。",
    ),
    "Paying for Things": (
        "I keep the receipt in case I need to return something.",
        "我会保留收据，以防需要退货。",
    ),
    "Going to a Bank": (
        "I deposit money when I visit the bank.",
        "我去银行时会存钱。",
    ),
    "Using an ATM": (
        "I check my balance before I take out cash.",
        "取钱前我会先查余额。",
    ),
    "Getting and Sending Emails": (
        "I reply to important messages before lunch.",
        "我午饭前会回复重要消息。",
    ),
    "Texting": (
        "I call back later if I cannot talk right away.",
        "不能马上说话时，我会稍后回电。",
    ),
    "Making a Phone Call": (
        "I leave a voicemail if no one answers.",
        "没人接时我会留语音留言。",
    ),
    "Answering a Telephone": (
        "I say hello and ask who is calling.",
        "我先打招呼，再问是谁来电。",
    ),
    "Leaving a Message": (
        "I call back when I have a quiet moment.",
        "我有安静时间时会回电。",
    ),
    "Taking a Message": (
        "I write the name and number down carefully.",
        "我会仔细记下姓名和电话。",
    ),
    "Checking Voicemail": (
        "I check missed calls when I get home.",
        "到家后我会查看未接来电。",
    ),
    "Writing a Personal Letter": (
        "I write by hand when I want the letter to feel personal.",
        "我想让信更有温度时会手写。",
    ),
    "Mailing a Letter": (
        "I buy a stamp before I post the letter.",
        "寄信前我会先买邮票。",
    ),
    "Going to a Birthday Party": (
        "I say happy birthday when I give her the present.",
        "我送礼物时会说生日快乐。",
    ),
    "Going to a Dinner Party": (
        "I set the table before the guests arrive.",
        "客人来前我会摆好餐桌。",
    ),
    "Going to a Movie": (
        "I buy a ticket before the film starts.",
        "电影开始前我会买票。",
    ),
    "At a Fast Food Restaurant": (
        "I choose a meal before I place the order.",
        "点单前我会选好套餐。",
    ),
    "At a Coffee Shop": (
        "I order a latte if I want something milky.",
        "我想喝奶味咖啡时会点拿铁。",
    ),
}


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


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


NATURAL_FOLLOW_UP_PROMPTS = (
    ("What is that like for you?", "对你来说那是怎样的？"),
    ("How do you usually do it?", "你通常怎么做？"),
    ("What does your routine look like?", "你的习惯是什么样的？"),
    ("What else do you do around then?", "那时你还会做些什么？"),
    ("Can you tell me a little more?", "你能再多说一点吗？"),
    ("How does it usually go?", "通常是怎样的？"),
)


def natural_follow_up(lesson: Lesson) -> tuple[str, str, str, str]:
    """Return one authored detail and a light conversational follow-up."""

    prompt, prompt_zh = NATURAL_FOLLOW_UP_PROMPTS[
        sum(ord(character) for character in lesson.title_en) % len(NATURAL_FOLLOW_UP_PROMPTS)
    ]
    try:
        detail, detail_zh = NATURAL_SCENE_DETAILS[lesson.title_en]
    except KeyError as error:
        raise ValueError(f"Missing natural scene detail for {lesson.title_en}.") from error
    return prompt, prompt_zh, detail, detail_zh


def lesson_sections(lesson: Lesson) -> list[dict]:
    """Build a concise, scene-first learning flow for one life situation."""

    follow_up_prompt, follow_up_prompt_zh, follow_up, follow_up_zh = natural_follow_up(lesson)
    return [
        section(
            "core_vocabulary",
            "核心词汇",
            "Core Words",
            10,
            [
                item(
                    "core-expression",
                    10,
                    {
                        "term": lesson.term,
                        "meaning": lesson.meaning,
                        "explanation": f"“{lesson.scene}”时可以自然用到的核心表达。",
                        "examples": [
                            {"english": lesson.sentence, "chinese": lesson.sentence_zh}
                        ],
                    },
                    lesson.term,
                ),
                item(
                    "support-expression",
                    20,
                    {
                        "term": lesson.support_term,
                        "meaning": lesson.support_meaning,
                        "explanation": "与本节生活动作自然衔接的常用搭配。",
                    },
                    lesson.support_term,
                ),
            ],
        ),
        section(
            "situational_dialogues",
            "情景对话",
            "A Real-Life Exchange",
            20,
            [
                item(
                    "life-exchange",
                    10,
                    {
                        "title": lesson.scene,
                        "scenario": "一个真实生活片段。理解意思后，按自己的情况替换内容。",
                        "turns": [
                            {"speaker": "Mia", "english": lesson.cue, "chinese": lesson.cue_zh},
                            {"speaker": "You", "english": lesson.sentence, "chinese": lesson.sentence_zh},
                            {"speaker": "Mia", "english": follow_up_prompt, "chinese": follow_up_prompt_zh},
                            {"speaker": "You", "english": follow_up, "chinese": follow_up_zh},
                        ],
                    },
                    lesson.scene,
                )
            ],
        ),
        section(
            "key_sentence_patterns",
            "自然说法",
            "One Natural Way to Say It",
            30,
            [
                item(
                    "key-sentence",
                    10,
                    {
                        "pattern": lesson.sentence,
                        "meaning": lesson.sentence_zh,
                        "explanation": "这是自然的示例说法，不是固定回答。把时间、人物或动作换成你自己的内容即可。",
                    },
                    lesson.sentence,
                )
            ],
        ),
        section(
            "speaking_practice",
            "开口练习",
            "Make It Your Own",
            40,
            [
                item(
                    "make-it-yours",
                    10,
                    {
                        "instruction": "用自己的情况说说这个场景",
                        "question": "Talk about this part of your day in your own words.",
                        "question_zh": f"用自己的话说说“{lesson.scene}”。",
                        "guidance": "可以换时间、人物、物品和地点，不必照抄示例句。",
                    },
                    "说出自己的版本",
                )
            ],
        ),
        section(
            "mini_exercises",
            "小练习",
            "Quick Check",
            50,
            [
                item(
                    "personal-check",
                    10,
                    {
                        "instruction": "想一想真实生活",
                        "question": "What would be true for you in this situation?",
                        "question_zh": "这个场景里，哪件事最符合你的真实生活？",
                        "guidance": "任选本节一个词或短语，组成一句自己的话。",
                    },
                    "真实生活小练习",
                )
            ],
        ),
        section(
            "useful_tips",
            "实用提示",
            "Useful Tip",
            60,
            [
                item(
                    "scene-tip",
                    10,
                    {
                        "title": "把搭配连起来",
                        "meaning": f"{lesson.support_term} · {lesson.support_meaning}",
                        "explanation": "核心表达和这个搭配放在一起，就能说出一段更完整、更像真实生活的话。",
                    },
                    "场景搭配",
                )
            ],
        ),
        section(
            "extended_reading",
            "延伸听读",
            "Listen and Read",
            70,
            [
                item(
                    "mini-reading",
                    10,
                    {
                        "text": f"{lesson.sentence} {follow_up}",
                        "summary": f"{lesson.sentence_zh}{follow_up_zh}",
                        "explanation": "听读这段短片段时，注意两句话之间的自然停顿。",
                    },
                    "一句生活片段",
                )
            ],
        ),
    ]


def icon_filename(material: Material, lesson: Lesson) -> str:
    return (
        f"everyday-activities-m{material.number:02d}-l{lesson.number:02d}-"
        f"{slugify(lesson.title_en)}.png"
    )


def icon_url(material: Material, lesson: Lesson) -> str:
    return f"/static/{STATIC_SUBDIRECTORY.as_posix()}/{icon_filename(material, lesson)}"


def section_icon_url(material: Material) -> str:
    first_lesson = material.lessons[0]
    return icon_url(material, first_lesson)


def color_for(material_number: int) -> tuple[str, str, str]:
    palettes = (
        ("#fff4dc", "#d78529", "#8f4d12"),
        ("#e6f5fb", "#389bc0", "#17617e"),
        ("#e9f7ec", "#429264", "#1d653c"),
        ("#f4edff", "#8161ba", "#4c347f"),
        ("#fff0f4", "#c86080", "#843049"),
        ("#fff5df", "#d5793b", "#91471c"),
    )
    return palettes[material_number - 1]


def draw_simple_icon(draw: ImageDraw.ImageDraw, icon: str, fill: str, accent: str) -> None:
    """Draw compact, readable PNG art without a font or external asset set."""

    # Common geometric helpers are intentionally simple because the image is
    # displayed at thumbnail size beside a lesson title in the mini program.
    def line(points, width=7):
        draw.line(points, fill=fill, width=width, joint="curve")

    def outline_box(box, width=7):
        draw.rounded_rectangle(box, radius=12, outline=fill, width=width)

    if icon in {"morning", "sleep"}:
        if icon == "morning":
            draw.ellipse((48, 42, 112, 106), fill=fill)
            for start, end in [((80, 21), (80, 34)), ((80, 114), (80, 128)), ((25, 74), (38, 74)), ((122, 74), (135, 74)), ((42, 37), (51, 46)), ((109, 102), (118, 111)), ((42, 111), (51, 102)), ((109, 46), (118, 37))]:
                line([start, end], 6)
        else:
            draw.ellipse((47, 42, 111, 106), fill=fill)
            draw.ellipse((69, 29, 124, 84), fill=accent)
    elif icon == "tooth":
        line([(34, 102), (118, 45)], 11)
        draw.rounded_rectangle((27, 96, 49, 117), radius=8, fill=fill)
        for offset in range(4):
            line([(98 + offset * 7, 37 + offset * 3), (105 + offset * 7, 48 + offset * 3)], 3)
    elif icon == "shower":
        line([(36, 48), (69, 48), (80, 62)], 9)
        line([(36, 48), (36, 74)], 9)
        for x in (76, 94, 112):
            draw.ellipse((x, 75, x + 12, 94), fill=accent)
    elif icon == "clothes":
        line([(80, 38), (80, 25), (91, 21)], 6)
        draw.polygon([(53, 52), (73, 39), (87, 39), (107, 52), (118, 84), (102, 91), (102, 120), (58, 120), (58, 91), (42, 84)], fill=fill)
    elif icon == "bed":
        line([(37, 48), (37, 119)], 9)
        line([(123, 73), (123, 119)], 9)
        draw.rounded_rectangle((36, 68, 124, 104), radius=8, fill=fill)
        draw.rounded_rectangle((46, 75, 72, 91), radius=5, fill=accent)
    elif icon in {"coffee", "meal", "breakfast", "egg", "salad", "pasta", "rice", "burger"}:
        if icon == "coffee":
            draw.rounded_rectangle((46, 50, 104, 108), radius=12, fill=fill)
            draw.arc((91, 62, 123, 98), 270, 90, fill=fill, width=8)
            for x in (61, 79, 97):
                line([(x, 39), (x + 4, 28)], 4)
        elif icon == "egg":
            draw.ellipse((38, 48, 122, 112), fill=fill)
            draw.ellipse((67, 67, 94, 94), fill=accent)
        elif icon == "salad":
            draw.arc((40, 51, 120, 121), 0, 180, fill=fill, width=10)
            for x, y in ((62, 66), (82, 59), (100, 71)):
                draw.ellipse((x, y, x + 20, y + 20), fill=accent)
        elif icon == "pasta":
            draw.arc((36, 46, 124, 124), 0, 180, fill=fill, width=10)
            for y in (68, 82, 96):
                draw.arc((54, y - 12, 105, y + 12), 180, 360, fill=accent, width=5)
        elif icon == "rice":
            draw.arc((37, 57, 123, 122), 0, 180, fill=fill, width=10)
            for x, y in ((61, 70), (78, 62), (94, 72)):
                draw.ellipse((x, y, x + 15, y + 11), fill=accent)
        elif icon == "burger":
            draw.rounded_rectangle((42, 53, 118, 75), radius=18, fill=fill)
            draw.rectangle((42, 78, 118, 91), fill=accent)
            draw.rounded_rectangle((42, 94, 118, 113), radius=8, fill=fill)
        else:
            draw.ellipse((40, 47, 120, 121), outline=fill, width=10)
            draw.ellipse((62, 69, 98, 105), fill=accent)
            if icon == "breakfast":
                line([(30, 52), (30, 112)], 5)
                line([(23, 52), (37, 52)], 4)
    elif icon == "door":
        outline_box((45, 29, 112, 124))
        draw.ellipse((93, 78, 102, 87), fill=accent)
    elif icon == "bus":
        draw.rounded_rectangle((34, 45, 126, 105), radius=12, fill=fill)
        draw.rectangle((48, 58, 111, 80), fill=accent)
        for x in (52, 105):
            draw.ellipse((x, 94, x + 21, 115), fill=accent)
    elif icon in {"car", "taxi", "garage"}:
        draw.rounded_rectangle((36, 69, 124, 105), radius=12, fill=fill)
        draw.polygon([(52, 69), (67, 48), (99, 48), (113, 69)], fill=fill)
        for x in (52, 105):
            draw.ellipse((x, 94, x + 20, 114), fill=accent)
        if icon == "taxi":
            draw.rectangle((72, 38, 91, 49), fill=accent)
    elif icon == "directions":
        line([(39, 106), (75, 70), (112, 70)], 9)
        line([(112, 70), (96, 54)], 9)
        line([(112, 70), (96, 86)], 9)
    elif icon == "train":
        draw.rounded_rectangle((48, 33, 112, 111), radius=15, fill=fill)
        draw.rectangle((60, 48, 100, 69), fill=accent)
        for x in (62, 91):
            draw.ellipse((x, 82, x + 12, 94), fill=accent)
        line([(61, 117), (48, 130)], 6)
        line([(99, 117), (112, 130)], 6)
    elif icon == "walk":
        draw.ellipse((72, 31, 90, 49), fill=fill)
        line([(81, 52), (74, 81), (58, 102)], 8)
        line([(74, 81), (99, 104)], 8)
        line([(75, 62), (55, 70)], 7)
        line([(78, 64), (101, 72)], 7)
    elif icon == "bike":
        for x in (47, 99):
            draw.ellipse((x, 80, x + 33, 113), outline=fill, width=7)
        line([(64, 80), (81, 58), (95, 80), (64, 80)], 6)
        line([(81, 58), (104, 58)], 6)
        line([(76, 53), (69, 46)], 6)
    elif icon in {"home", "table", "dishes"}:
        if icon == "home":
            draw.polygon([(40, 70), (80, 35), (120, 70)], fill=fill)
            draw.rounded_rectangle((49, 67, 111, 119), radius=6, fill=fill)
            draw.rectangle((72, 87, 88, 119), fill=accent)
        elif icon == "table":
            line([(40, 69), (120, 69)], 11)
            line([(52, 69), (52, 119)], 8)
            line([(108, 69), (108, 119)], 8)
            draw.ellipse((64, 40, 96, 63), fill=accent)
        else:
            draw.ellipse((42, 45, 118, 112), outline=fill, width=9)
            draw.ellipse((61, 63, 99, 101), outline=accent, width=7)
    elif icon in {"vegetables", "groceries"}:
        if icon == "vegetables":
            draw.polygon([(50, 103), (95, 42), (117, 66), (71, 116)], fill=fill)
            draw.polygon([(91, 47), (106, 33), (119, 48)], fill=accent)
        else:
            draw.polygon([(42, 57), (118, 57), (108, 112), (52, 112)], outline=fill, fill=None, width=8)
            line([(58, 57), (65, 40), (95, 40), (102, 57)], 7)
            draw.ellipse((65, 72, 85, 92), fill=accent)
    elif icon == "laptop":
        outline_box((44, 43, 116, 94))
        draw.rounded_rectangle((34, 99, 126, 111), radius=5, fill=fill)
        draw.rectangle((56, 54, 104, 83), fill=accent)
    elif icon == "music":
        line([(68, 38), (68, 105)], 8)
        line([(68, 40), (109, 29)], 8)
        line([(109, 29), (109, 88)], 8)
        draw.ellipse((47, 94, 71, 113), fill=fill)
        draw.ellipse((88, 78, 112, 97), fill=fill)
    elif icon == "book":
        draw.polygon([(42, 43), (78, 53), (78, 118), (42, 108)], fill=fill)
        draw.polygon([(82, 53), (118, 43), (118, 108), (82, 118)], fill=accent)
        line([(80, 51), (80, 119)], 5)
    elif icon in {"tv", "movie"}:
        outline_box((39, 45, 121, 106))
        if icon == "tv":
            line([(63, 37), (51, 24)], 6)
            line([(97, 37), (109, 24)], 6)
        else:
            draw.polygon([(69, 61), (69, 91), (98, 76)], fill=accent)
    elif icon == "laundry":
        outline_box((45, 36, 115, 120))
        draw.ellipse((61, 64, 99, 102), outline=fill, width=8)
        draw.ellipse((66, 45, 75, 54), fill=accent)
    elif icon == "cleaning":
        line([(94, 35), (58, 100)], 9)
        draw.polygon([(45, 96), (78, 107), (64, 123), (34, 111)], fill=fill)
    elif icon in {"cat", "dog"}:
        draw.ellipse((48, 54, 112, 116), fill=fill)
        if icon == "cat":
            draw.polygon([(52, 60), (57, 35), (73, 54)], fill=fill)
            draw.polygon([(88, 54), (105, 35), (108, 60)], fill=fill)
        else:
            draw.ellipse((43, 49, 83, 83), fill=fill)
            draw.ellipse((43, 38, 57, 65), fill=accent)
            draw.ellipse((68, 39, 82, 65), fill=accent)
        draw.ellipse((65, 77, 73, 85), fill=accent)
        draw.ellipse((89, 77, 97, 85), fill=accent)
    elif icon == "payment":
        draw.rounded_rectangle((37, 53, 123, 107), radius=10, fill=fill)
        draw.rectangle((39, 68, 121, 80), fill=accent)
        draw.rounded_rectangle((50, 87, 80, 94), radius=3, fill=accent)
    elif icon in {"bank", "atm"}:
        if icon == "bank":
            draw.polygon([(41, 56), (80, 31), (119, 56)], fill=fill)
            line([(47, 58), (113, 58)], 7)
            for x in (55, 76, 97):
                draw.rectangle((x, 62, x + 10, 105), fill=fill)
            line([(43, 109), (117, 109)], 7)
        else:
            outline_box((48, 30, 112, 121))
            draw.rectangle((60, 46, 100, 72), fill=accent)
            draw.rounded_rectangle((60, 88, 100, 102), radius=3, fill=accent)
    elif icon in {"email", "letter"}:
        outline_box((37, 53, 123, 109))
        line([(39, 55), (80, 85), (121, 55)], 7)
        if icon == "letter":
            draw.rectangle((58, 34, 102, 51), fill=accent)
    elif icon == "text":
        draw.rounded_rectangle((39, 44, 119, 100), radius=18, fill=fill)
        draw.polygon([(57, 98), (59, 114), (76, 100)], fill=fill)
        for x in (58, 78, 98):
            draw.ellipse((x, 68, x + 8, 76), fill=accent)
    elif icon in {"phone", "message", "note"}:
        if icon == "phone":
            draw.arc((43, 42, 117, 116), 135, 315, fill=fill, width=12)
            draw.rounded_rectangle((43, 78, 59, 101), radius=5, fill=fill)
            draw.rounded_rectangle((101, 55, 117, 78), radius=5, fill=fill)
        elif icon == "message":
            draw.rounded_rectangle((39, 45, 121, 101), radius=18, fill=fill)
            draw.polygon([(92, 99), (102, 115), (108, 99)], fill=fill)
            line([(57, 65), (103, 65)], 5)
            line([(57, 82), (91, 82)], 5)
        else:
            draw.polygon([(49, 35), (106, 35), (118, 49), (118, 121), (49, 121)], fill=fill)
            draw.polygon([(106, 35), (106, 51), (118, 51)], fill=accent)
            for y in (68, 84, 100):
                line([(62, y), (104, y)], 5)
    elif icon == "stamp":
        draw.rectangle((48, 42, 112, 116), fill=fill)
        draw.rectangle((59, 54, 101, 104), outline=accent, width=5)
        draw.ellipse((71, 67, 89, 85), fill=accent)
    elif icon == "gift":
        draw.rounded_rectangle((43, 66, 117, 117), radius=7, fill=fill)
        draw.rounded_rectangle((38, 55, 122, 73), radius=5, fill=fill)
        draw.rectangle((75, 55, 85, 117), fill=accent)
        draw.arc((56, 36, 80, 61), 160, 355, fill=fill, width=7)
        draw.arc((80, 36, 104, 61), 185, 20, fill=fill, width=7)
    elif icon == "party":
        draw.polygon([(48, 113), (82, 38), (113, 113)], fill=fill)
        for x, y in ((66, 83), (83, 71), (96, 94)):
            draw.ellipse((x, y, x + 10, y + 10), fill=accent)
        line([(39, 51), (50, 38)], 5)
        line([(111, 51), (121, 38)], 5)
    else:
        # A deliberately clear fallback keeps every generated asset usable if
        # a newly added lesson refers to a fresh art key.
        draw.ellipse((45, 45, 115, 115), fill=fill)
        draw.ellipse((69, 69, 91, 91), fill=accent)


def ensure_lesson_icon(settings: Settings, material: Material, lesson: Lesson) -> str:
    """Write a small local PNG the mini program can load through ``/static``."""

    image_path = settings.static_dir / STATIC_SUBDIRECTORY / icon_filename(material, lesson)
    image_path.parent.mkdir(parents=True, exist_ok=True)
    background, fill, accent = color_for(material.number)
    image = Image.new("RGB", (160, 160), background)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((3, 3, 157, 157), radius=34, fill=background)
    draw_simple_icon(draw, lesson.icon, fill, accent)
    image.save(image_path, format="PNG", optimize=True)
    if image_path.stat().st_size >= 100 * 1024:
        raise ValueError(f"{image_path.name} must stay below 100KB.")
    return icon_url(material, lesson)


def ensure_topic(catalog: LearningCatalogService, db: Session) -> dict:
    module_id = db.execute(
        select(m.learning_module.c.id).where(m.learning_module.c.module_code == MODULE_CODE)
    ).scalar_one_or_none()
    if module_id is None:
        raise RuntimeError(f"Missing learning module: {MODULE_CODE}")
    current_id = row_id(db, m.learning_topic, m.learning_topic.c.topic_code, TOPIC_CODE)
    return catalog.save_topic(
        s.LearningTopicInput(
            module_id=module_id,
            topic_code=TOPIC_CODE,
            title="日常生活英语",
            title_en="English for Everyday Activities",
            description="从起床、出行到家务和社交，用 57 个日常场景练习最常用的英文表达。",
            sort_order=55,
            is_published=1,
        ),
        ACTOR,
        current_id,
    )


def template_id_for(db: Session) -> int:
    template_id = db.execute(
        select(m.learning_template.c.id).where(
            m.learning_template.c.template_code == TEMPLATE_CODE,
            m.learning_template.c.template_version == 1,
            m.learning_template.c.status == "active",
        )
    ).scalar_one_or_none()
    if template_id is None:
        raise RuntimeError(f"Missing active material template: {TEMPLATE_CODE}")
    return template_id


def material_payload(template_id: int, material: Material, cover_url: str) -> s.LearningMaterialInput:
    return s.LearningMaterialInput(
        template_id=template_id,
        material_code=f"everyday-activities-english-book-{material.number}",
        title=material.title,
        title_en=material.title_en,
        summary=material.summary,
        material_type="dialogue",
        publisher="Happy English",
        version_name="日常生活英语 v1",
        cover_url=cover_url,
        difficulty_code="a1-a2",
        estimated_minutes=len(material.lessons) * 3,
        sort_order=material.number * 10,
        is_published=1,
    )


def course_payload(topic_id: int, material_id: int, material: Material, cover_url: str) -> s.LearningCourseInput:
    return s.LearningCourseInput(
        topic_id=topic_id,
        material_ids=[material_id],
        course_code=f"everyday-activities-english-book-{material.number}",
        title=f"日常生活英语 · 教材{material.number}",
        title_en=f"Everyday Activities · Book {material.number}",
        summary=material.summary,
        course_type="dialogue",
        cover_url=cover_url,
        estimated_minutes=len(material.lessons) * 3,
        difficulty_code="a1-a2",
        sort_order=material.number * 10,
        is_published=1,
        access_policy="benefit",
    )


def seed_material(
    catalog: LearningCatalogService,
    db: Session,
    settings: Settings,
    template_id: int,
    topic_id: int,
    material: Material,
) -> dict:
    icon_urls = {lesson.number: ensure_lesson_icon(settings, material, lesson) for lesson in material.lessons}
    material_code = f"everyday-activities-english-book-{material.number}"
    current_material_id = row_id(db, m.learning_material, m.learning_material.c.material_code, material_code)
    payload = material_payload(template_id, material, section_icon_url(material))
    saved_material = (
        catalog.save_material(payload, ACTOR, current_material_id)
        if current_material_id is not None
        else catalog.save_material(payload, ACTOR)
    )

    lesson_ids = []
    for lesson in material.lessons:
        lesson_code = (
            f"everyday-activities-m{material.number:02d}-l{lesson.number:02d}-"
            f"{slugify(lesson.title_en)}"
        )
        current_lesson_id = lesson_id(db, saved_material["id"], lesson_code)
        saved_lesson = catalog.save_material_lesson(
            saved_material["id"],
            s.LearningMaterialLessonInput(
                lesson_code=lesson_code,
                title=lesson.title,
                title_en=lesson.title_en,
                summary=f"{lesson.scene}：掌握 {lesson.term}，并用一句完整表达说出自己的情况。",
                illustration_url=icon_urls[lesson.number],
                lesson_format="structured",
                estimated_minutes=3,
                sort_order=lesson.number * 10,
                sections=lesson_sections(lesson),
            ),
            ACTOR,
            current_lesson_id,
        )
        catalog.lesson_content.publish(saved_lesson["id"], ACTOR)
        lesson_ids.append(saved_lesson["id"])

    # Revalidate the template against all newly published structured lessons.
    saved_material = catalog.save_material(payload, ACTOR, saved_material["id"])
    course_code = f"everyday-activities-english-book-{material.number}"
    current_course_id = row_id(db, m.learning_course, m.learning_course.c.course_code, course_code)
    course = catalog.save_course(
        course_payload(topic_id, saved_material["id"], material, section_icon_url(material)),
        ACTOR,
        current_course_id,
    )
    db.execute(
        update(m.learning_topic_course)
        .where(
            m.learning_topic_course.c.topic_id == topic_id,
            m.learning_topic_course.c.course_id == course["id"],
        )
        .values(sort_order=material.number * 10, updated_by=ACTOR["id"])
    )
    db.commit()
    return {
        "material": material.number,
        "material_id": saved_material["id"],
        "course_id": course["id"],
        "lesson_ids": lesson_ids,
    }


def bind_member_access(db: Session, courses: list[dict]) -> None:
    """Attach every textbook to the existing all-courses membership benefit."""

    benefit_id = db.execute(
        select(m.membership_benefit.c.id).where(
            m.membership_benefit.c.benefit_code == BENEFIT_CODE
        )
    ).scalar_one_or_none()
    if benefit_id is None:
        raise RuntimeError(f"Missing membership benefit: {BENEFIT_CODE}")

    for entry in courses:
        course_id = entry["course_id"]
        existing_id = db.execute(
            select(m.membership_benefit_course.c.id).where(
                m.membership_benefit_course.c.benefit_id == benefit_id,
                m.membership_benefit_course.c.course_id == course_id,
                m.membership_benefit_course.c.access_action == "study",
            )
        ).scalar_one_or_none()
        values = {
            "is_enabled": 1,
            "sort_order": entry["material"] * 10,
            "updated_by": ACTOR["id"],
        }
        if existing_id is None:
            db.execute(
                insert(m.membership_benefit_course).values(
                    benefit_id=benefit_id,
                    course_id=course_id,
                    access_action="study",
                    created_by=ACTOR["id"],
                    **values,
                )
            )
        else:
            db.execute(
                update(m.membership_benefit_course)
                .where(m.membership_benefit_course.c.id == existing_id)
                .values(**values)
            )
    db.commit()


def validate_curriculum() -> None:
    if len(MATERIALS) != 6:
        raise ValueError(f"Expected six materials, found {len(MATERIALS)}.")
    total = sum(len(material.lessons) for material in MATERIALS)
    if total != 57:
        raise ValueError(f"Expected 57 lessons, found {total}.")
    lesson_title_en = {
        lesson.title_en for material in MATERIALS for lesson in material.lessons
    }
    if lesson_title_en != set(NATURAL_SCENE_DETAILS):
        missing = sorted(lesson_title_en - set(NATURAL_SCENE_DETAILS))
        extra = sorted(set(NATURAL_SCENE_DETAILS) - lesson_title_en)
        raise ValueError(f"Natural scene details differ from lessons: missing={missing}, extra={extra}")
    seen_titles = set()
    for material in MATERIALS:
        expected_numbers = list(range(1, len(material.lessons) + 1))
        actual_numbers = [lesson.number for lesson in material.lessons]
        if actual_numbers != expected_numbers:
            raise ValueError(f"Lesson order is invalid in material {material.number}.")
        for lesson in material.lessons:
            if not all(
                (
                    lesson.title,
                    lesson.title_en,
                    lesson.term,
                    lesson.sentence,
                    lesson.cue,
                )
            ):
                raise ValueError(f"Incomplete lesson: {lesson}")
            title_key = (material.number, lesson.title)
            if title_key in seen_titles:
                raise ValueError(f"Duplicate lesson title: {lesson.title}")
            seen_titles.add(title_key)


def main() -> None:
    validate_curriculum()
    settings = Settings()
    engine = make_engine(settings.database_url)
    with Session(engine) as db:
        catalog = LearningCatalogService(db)
        topic = ensure_topic(catalog, db)
        template_id = template_id_for(db)
        created = [
            seed_material(catalog, db, settings, template_id, topic["id"], material)
            for material in MATERIALS
        ]
        bind_member_access(db, created)
    print(
        json.dumps(
            {
                "topic_id": topic["id"],
                "topic_code": TOPIC_CODE,
                "materials": created,
                "material_count": len(MATERIALS),
                "lesson_count": sum(len(material.lessons) for material in MATERIALS),
                "access_policy": "benefit",
                "free_preview": "the first two lessons across the whole topic",
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
