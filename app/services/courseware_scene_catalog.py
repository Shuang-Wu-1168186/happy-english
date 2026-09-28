"""Hand-reviewed scenes for source cards that otherwise produce a fake dialogue.

Each tuple is ``(first English, first Chinese, reply English, reply Chinese)``.
These are deliberately concrete exchanges: two people are reacting to a
recognisable event, rather than asking for a definition of the expression.
"""


CURATED_REAL_LIFE_SCENES = {
    1535: (
        "The children are colouring at the next table. Can we discuss their surprise now?", "孩子们正在隔壁桌画画。我们现在能讨论给他们的惊喜吗？",
        "Let's wait until they're no longer within earshot.", "等他们听不见了再说吧。",
    ),
    1560: (
        "Do you want to sort through those receipts from 2018 before we move?", "搬家前你想整理那些 2018 年的收据吗？",
        "No, don't bother with them; the accountant already has copies.", "不用，别费心管它们了；会计已经有副本。",
    ),
    1573: (
        "Maya thinks her birthday dinner is just a casual meal.", "玛雅以为她的生日晚餐只是一次普通聚餐。",
        "Then don't let on that we've invited all her friends.", "那就别透露我们已经邀请了她所有朋友。",
    ),
    1595: (
        "This old family photo has no date. How can we tell who is in it?", "这张旧家庭照片没有日期。我们怎么知道里面是谁？",
        "Let's marry it up with the names in Grandma's album.", "把它和奶奶相册里的名字对应起来吧。",
    ),
    1602: (
        "We only have one cake for the whole club. How should we divide it?", "整个社团只有一个蛋糕。我们怎么分？",
        "Everyone should get a fair share of it.", "每个人都应该分到公平的一份。",
    ),
    1609: (
        "The library app signed me out while I was reserving a book.", "我预订图书时，图书馆应用把我登出了。",
        "The authentication session expires after 30 minutes.", "身份验证会话会在 30 分钟后过期。",
    ),
    1614: (
        "Why do the children's art classes, sports club, and music lessons use one logo?", "为什么儿童美术课、运动社团和音乐课都用同一个标志？",
        "They all run under the umbrella of the community centre.", "它们都归社区中心统一管理。",
    ),
    1626: (
        "We've planned the picnic, but someone still needs to collect the food.", "野餐已经安排好了，但还得有人去取食物。",
        "Let's delegate that job to Sam; he lives near the market.", "把这项工作交给萨姆吧，他住在市场附近。",
    ),
    1646: (
        "You brought me another souvenir, even though I said not to.", "我都说不用了，你还是又给我带了纪念品。",
        "I know—I like to gift you things when I travel.", "我知道，我旅行时就喜欢送你东西。",
    ),
    1650: (
        "Why are you opening every window? It's chilly outside.", "你为什么把每扇窗都打开？外面很冷。",
        "The room feels stuffy after all those people were in here.", "这么多人待过以后，房间里感觉很闷。",
    ),
    1413: (
        "Are you leaving for the appointment now?", "你现在要去赴约了吗？",
        "Just let me get the confirmation before you move off.", "等我在你离开前把确认信息拿到。",
    ),
    1416: (
        "I need another day to finish the poster because the paint is still wet.", "海报的颜料还没干，我还需要一天才能完成。",
        "Fair enough. We'll hang it up on Friday instead.", "有道理。那我们周五再挂起来。",
    ),
    1419: (
        "The café with the longest queue must be the best one, right?", "排队最长的咖啡馆一定是最好的，对吧？",
        "That's not necessarily true; it may just have the only outdoor table.", "那不一定对；它可能只是唯一有户外桌位的店。",
    ),
    1452: (
        "We have one name tag for every child at camp. How are we checking the list?", "夏令营里每个孩子都有一个名牌。我们怎么核对名单？",
        "Each name tag should correspond one-to-one with a child on the register.", "每个名牌都应该和名单上的一名孩子一一对应。",
    ),
    1474: (
        "This soup tastes flat, but I don't want it too salty.", "这汤味道有点淡，但我又不想放得太咸。",
        "Add just a pinch of salt, then taste it again.", "加一小撮盐，再尝尝看。",
    ),
    1494: (
        "The school planted trees last year. Was it only to make the playground prettier?", "学校去年种了树。只是为了让操场更好看吗？",
        "No, the benefits extend beyond appearance; they give the children shade too.", "不是，好处不止于外观；树也给孩子们提供了阴凉。",
    ),
    1500: (
        "The recipe continues on the next page of the magazine.", "食谱在杂志的下一页。",
        "Just flick over; the cooking times are there.", "翻过去看看，烹饪时间写在那儿。",
    ),
    1512: (
        "The bedroom feels much colder than the hallway.", "卧室比走廊冷得多。",
        "Open the vent so warm air can circulate into the room.", "打开通风口，让暖空气流进房间。",
    ),
    1430: (
        "I'm making a poster for the geography club. Do you know the average height of Earth's land?", "我在为地理社团做海报。你知道地球陆地的平均海拔吗？",
        "The mean elevation of the Earth's land surface is 840 metres.", "地球陆地表面的平均海拔是 840 米。",
    ),
    1444: (
        "We're driving to the sunrise lookout. Which direction should we follow?", "我们要开车去看日出的观景点。该往哪个方向走？",
        "Head east; the sun will rise in front of us.", "往东走；太阳会从我们前方升起。",
    ),
    1453: (
        "The village festival still uses hand-painted signs. Is that tradition dying out?", "村里的节日还在使用手绘招牌。这种传统正在消失吗？",
        "No, those customs still prevail in the older villages.", "没有，那些习俗在老村庄里仍然盛行。",
    ),
    1464: (
        "The neighbours want solar panels but worry about the cost.", "邻居想装太阳能板，但担心费用。",
        "They can apply for a government subsidy to help pay for them.", "他们可以申请政府补贴来分担费用。",
    ),
    1466: (
        "We saw a tiny island from the ferry. Does anyone live there?", "我们从渡轮上看到一座小岛。有人住在那里吗？",
        "The guide says it has about 5,000 inhabitants.", "导游说那里大约有五千名居民。",
    ),
    1470: (
        "Why is one stall always crowded at the weekend market?", "为什么周末市场里有一个摊位总是很拥挤？",
        "That bakery dominates sales because its bread sells out early.", "那家面包店的销量占了上风，因为它的面包很早就卖光。",
    ),
    1505: (
        "There are only six boys in our dance class. Is it mostly girls?", "我们舞蹈班只有六个男生。大多数都是女生吗？",
        "Yes, the girls outnumber the boys by nearly four to one.", "对，女生人数几乎是男生的四倍。",
    ),
    327: (
        "I just moved here and can only order food and ask for directions.", "我刚搬到这里，只会点餐和问路。",
        "That's enough to get by in this country while you keep learning.", "在你继续学习时，这已经足够让你在这个国家应付生活了。",
    ),
    358: (
        "I'll bring the snacks instead of cooking a full lunch.", "我带零食来，不做一顿正式午餐了。",
        "Is that okay with everyone?", "大家觉得这样可以吗？",
    ),
    360: (
        "We tried both light bulbs, but the room is still dim.", "我们试了两种灯泡，但房间还是很暗。",
        "It doesn't seem to make any difference which bulb we use.", "我们用哪种灯泡似乎都没有区别。",
    ),
    382: (
        "How do we keep the party secret from Nina?", "我们怎么瞒住妮娜这个派对？",
        "Tell her it's a small dinner, unless you can't get her to come otherwise.", "就说是小型晚餐，除非你没办法用别的方式让她来。",
    ),
    953: (
        "I finally found out why the train was delayed.", "我终于弄清火车为什么晚点了。",
        "Go on—I'm all ears.", "继续说，我正认真听着呢。",
    ),
    957: (
        "Why did the driver ask that passenger to use headphones?", "司机为什么让那位乘客戴耳机？",
        "Loud music can bother people on public transportation.", "大声放音乐会打扰公共交通上的其他人。",
    ),
    962: (
        "My nephew says school is boring, but I think paying bills is worse.", "我外甥说上学很无聊，但我觉得交账单更糟。",
        "Do you think childhood is boring, or is adulthood more boring?", "你觉得童年无聊，还是成年生活更无聊？",
    ),
    969: (
        "The lights just came on, and the sprinklers are running inside the hall.", "大厅里的灯刚亮，喷淋器却在喷水。",
        "What the heck is going on?", "到底在搞什么？",
    ),
    980: (
        "Why won't you watch that old puppet film with me?", "你为什么不和我一起看那部旧木偶电影？",
        "The way the dolls move really creeps me out.", "那些玩偶的移动方式真的让我发毛。",
    ),
    983: (
        "I missed the neighbourhood meeting because my bus was late.", "我因为公交晚点错过了社区会议。",
        "Sure thing—I'll fill you in on the decisions.", "没问题，我会把大家的决定告诉你。",
    ),
    1004: (
        "I've changed the frames on my glasses.", "我换了眼镜框。",
        "Do you like the way this looks?", "你觉得这样看起来怎么样？",
    ),
    811: (
        "You work long hours at the charity shop even when no one asks.", "即使没人要求，你也在慈善商店工作很久。",
        "For me, helping the community is a worthwhile pursuit.", "对我来说，帮助社区是一项值得追求的事。",
    ),
    829: (
        "Why are the streets near the convention centre closed?", "为什么会展中心附近的街道封闭了？",
        "The city leaders are meeting there for the regional summit.", "城市领导人正在那里参加区域峰会。",
    ),
    844: (
        "He wants everyone to swim in the sea during a thunderstorm.", "他想让大家在雷雨天去海里游泳。",
        "That sounds nuts to me.", "我觉得这太离谱了。",
    ),
    849: (
        "There's something on your coat.", "你外套上有东西。",
        "It's just a strand of hair from the dog.", "只是狗掉的一根毛。",
    ),
    852: (
        "Why did nobody trust the raffle after the tickets disappeared?", "抽奖券丢失后，为什么没人相信抽奖了？",
        "Those missing tickets undermined people's trust in it.", "那些丢失的抽奖券削弱了人们对它的信任。",
    ),
    855: (
        "The bike is $80 and the tyres look new.", "这辆自行车卖 80 美元，轮胎看起来很新。",
        "That sounds like a solid price.", "听起来是个不错的价格。",
    ),
    861: (
        "The witness saw a lot but is nervous about guessing.", "目击者看到了很多，但担心自己猜测。",
        "Tell her to confine her statement to what she actually saw.", "告诉她只陈述自己真正看到的内容。",
    ),
    879: (
        "The fence has a loose wire sticking out.", "篱笆上有一根松动的电线露出来。",
        "Be sure not to touch it until the electrician comes.", "电工来之前一定别碰它。",
    ),
    884: (
        "This holiday package includes flights and a hotel for only $99.", "这个旅行套餐只要 99 美元，含机票和酒店。",
        "It sounds great, but what's the catch?", "听起来很好，但有什么猫腻？",
    ),
    901: (
        "Can we still park here after Monday?", "周一以后我们还能在这里停车吗？",
        "No, the new parking rule goes into effect then.", "不能，新停车规定那时开始生效。",
    ),
    910: (
        "The plants look dry but the soil is still loose.", "植物看起来有点干，但土壤还是松的。",
        "Spray the leaves lightly before the sun gets hot.", "太阳变热前轻轻喷湿叶子。",
    ),
    913: (
        "The cookies are out of the oven but look plain.", "饼干出炉了，但看起来很普通。",
        "Sprinkle a little cinnamon on top.", "在上面撒一点肉桂粉。",
    ),
    914: (
        "He keeps joking about people's accents even after they ask him to stop.", "即使别人让他停下，他还一直拿别人的口音开玩笑。",
        "That behaviour borders on bullying.", "那种行为近乎霸凌。",
    ),
    927: (
        "The landlord accepted your application?", "房东接受你的申请了吗？",
        "Yes, that's wonderful news!", "是的，这真是个好消息！",
    ),
    938: (
        "Why are you covering the bowl with a towel?", "你为什么用毛巾盖住碗？",
        "I'm letting the dough rise before I bake the bread.", "我在烤面包前让面团发酵。",
    ),
    731: (
        "The children cannot see the sugar we added to the lemonade.", "孩子们看不到我们加进柠檬水里的糖。",
        "It will dissolve once we stir it.", "我们一搅拌，它就会溶解。",
    ),
    791: (
        "We're only a few dollars short of buying the team a pizza.", "我们离给球队买披萨只差几美元。",
        "If everyone chucks in two dollars, we'll have enough.", "如果每个人凑两美元，我们就够了。",
    ),
    797: (
        "You expected Manchester to be busy and noisy all the time?", "你以为曼彻斯特会一直很忙很吵？",
        "It is lively, but Manchester feels really chill to me.", "它很有活力，但对我来说曼彻斯特感觉很放松。",
    ),
    800: (
        "You've just started working at the animal shelter.", "你刚开始在动物收容所工作。",
        "What's a typical day like there?", "那里典型的一天是什么样的？",
    ),
    807: (
        "The weather report says it's freezing in Mumbai tonight.", "天气预报说孟买今晚会很冷。",
        "Isn't Mumbai in the tropics? How can it have below-zero temperatures?", "孟买不是在热带吗？怎么可能有零下温度？",
    ),
    385: (
        "Have we packed the tickets, snacks, and umbrellas for the picnic?", "野餐的票、零食和雨伞都带了吗？",
        "Yes, everything's in the car, so we're good to go.", "都在车里了，我们可以出发了。",
    ),
    392: (
        "How is your first week looking after the twins?", "你照顾双胞胎的第一周怎么样？",
        "Tiring, but so far so good.", "很累，但目前还不错。",
    ),
    394: (
        "The school talent show starts in five minutes. Are you nervous?", "学校才艺表演五分钟后开始。你紧张吗？",
        "A little, but I'll perform the song the way I practised.", "有一点，但我会按练习时的方式表演这首歌。",
    ),
    426: (
        "Why did Leo quit the puzzle after only two minutes?", "利奥为什么才玩两分钟拼图就放弃了？",
        "He's used to instant gratification from games on his phone.", "他习惯了从手机游戏里立刻获得满足感。",
    ),
    427: (
        "Why did the lake look higher this morning than yesterday?", "为什么湖面今天早上比昨天高？",
        "The water level can fluctuate after heavy rain.", "大雨后水位会波动。",
    ),
    434: (
        "You volunteered to sing without rehearsing?", "你没排练就自愿去唱歌？",
        "Have you always been this confident?", "你一直都这么自信吗？",
    ),
    440: (
        "I heard your dad has been in hospital all week.", "我听说你爸爸整周都在住院。",
        "Thanks for asking. How are you holding up?", "谢谢你关心。你自己还撑得住吗？",
    ),
    475: (
        "I haven't seen you at Saturday yoga in a while.", "我有段时间没在周六瑜伽课见到你了。",
        "Are you still into yoga these days?", "你最近还喜欢练瑜伽吗？",
    ),
    488: (
        "Do you think the damp patch came from the roof?", "你觉得那块潮湿的痕迹是屋顶漏水造成的吗？",
        "It could well be; it appeared after the storm.", "很可能是；它是在暴风雨后出现的。",
    ),
    659: (
        "We've talked about the budget and the venue.", "我们已经讨论过预算和场地了。",
        "That brings us to the guest list.", "接下来就该谈宾客名单了。",
    ),
    669: (
        "The school council election is today. Have you decided?", "今天是学生会选举日。你决定投谁了吗？",
        "I'm going to cast my vote for Amira.", "我要把票投给阿米拉。",
    ),
    681: (
        "I'm applying for the volunteer coordinator role tomorrow.", "我明天要申请志愿者协调员这个岗位。",
        "They may ask what motivates you to do your best at work.", "他们可能会问什么激励你在工作中做到最好。",
    ),
    683: (
        "The careers adviser is helping me prepare for an interview.", "职业顾问正在帮我准备面试。",
        "She told me to think about where I see myself in the next few years.", "她让我想想自己未来几年想走到哪里。",
    ),
    684: (
        "You've set a goal to run a half marathon.", "你设定了跑半程马拉松的目标。",
        "My coach asked what steps I'm taking to reach that goal.", "我的教练问我为实现那个目标正在采取什么步骤。",
    ),
    702: (
        "Why did Grandpa keep the old letters in a box?", "爷爷为什么把旧信件放在盒子里？",
        "He believes they carry a piece of the writer's soul.", "他相信那些信件承载着写信人的一部分灵魂。",
    ),
    716: (
        "You keep a journal after every hiking trip.", "每次徒步后你都会写日记。",
        "An adventure belongs only to you until you choose to share it.", "一段冒险经历只属于你自己，直到你选择把它分享出来。",
    ),
    770: (
        "I ran into Priya at the market after she moved away.", "普里娅搬走后，我在市场偶遇了她。",
        "Haven't seen you in a while! How have you been?", "好久没见到你了！你最近怎么样？",
    ),
    774: (
        "Your parents were telling us their wedding story.", "你父母正在给我们讲他们的婚礼故事。",
        "Did you meet your wife yourself, or was it a family setup?", "你是自己认识你妻子的，还是家里安排的？",
    ),
    776: (
        "How did you and Nina first meet?", "你和妮娜最初是怎么认识的？",
        "My friend set me up with her cousin, and we kept seeing each other.", "我朋友把我介绍给她的表姐，后来我们就一直见面。",
    ),
    778: (
        "Your brother is overseas. Can we call him now?", "你哥哥在国外。我们现在能给他打电话吗？",
        "Let me check what time it is there now.", "我先看看他那里现在几点。",
    ),
    493: (
        "The café is replacing its chairs, and some are by the bin.", "咖啡馆正在换椅子，有些椅子放在垃圾箱旁。",
        "Are these all being thrown away?", "这些都要扔掉吗？",
    ),
    495: (
        "The queue is getting longer and Mia is alone at checkout.", "排队的人越来越多，米娅一个人在收银台。",
        "Can I help out on the till as well?", "我也可以帮忙收银吗？",
    ),
    496: (
        "The stroller keeps rolling when I leave it by the door.", "我把婴儿车放在门边时，它总会滑动。",
        "If I put the stroller here, it happens every time.", "如果我把婴儿车放在这里，每次都会这样。",
    ),
    498: (
        "Your staff badge has a different colour from ours.", "你的员工证颜色和我们的不一样。",
        "Are you a permanent employee, or are you here for the season?", "你是正式员工，还是只做这个季节？",
    ),
    499: (
        "You know everyone's name at this café.", "你认识这家咖啡馆里的每个人。",
        "How long have you been working here?", "你在这里工作多久了？",
    ),
    500: (
        "We just got a delivery of winter hats.", "我们刚收到一批冬帽。",
        "Can I put those hats on the shelf by the door?", "我能把那些帽子放到门边的架子上吗？",
    ),
    503: (
        "The bus driver says the machine does not give change.", "公交司机说机器不找零。",
        "Do you have smaller change?", "你有更小面额的零钱吗？",
    ),
    505: (
        "The charity shop is closing in ten minutes.", "慈善商店十分钟后关门。",
        "Where should I put these two donation bags?", "这两个捐赠袋该放在哪里？",
    ),
    508: (
        "Thanks for helping me find the station.", "谢谢你帮我找到车站。",
        "You're welcome. Have a good rest of the day.", "不客气。祝你今天余下的时间愉快。",
    ),
    516: (
        "You said you needed advice before speaking to your sister.", "你说在和姐姐谈话前需要一些建议。",
        "Your suggestion to apologise first really hit the spot.", "你建议我先道歉，这正好说到点子上。",
    ),
    524: (
        "We won't actually do this, but imagine the bus breaks down in the mountains.", "我们不会真的这样做，但假设公交车在山里抛锚了。",
        "Let's discuss that hypothetical situation for a minute.", "我们先讨论一下这个假设情境。",
    ),
    529: (
        "The museum has hundreds of objects. Does every one go into the exhibition?", "博物馆有数百件藏品。每一件都会展出吗？",
        "No, only a select few items are displayed each season.", "不会，每个季度只展出精挑细选的少数几件。",
    ),
    535: (
        "How many rooms are in the new flat?", "新公寓有几个房间？",
        "It comprises a kitchen, two bedrooms, and a small study.", "它包括一间厨房、两间卧室和一间小书房。",
    ),
    542: (
        "I'm standing across the stream and forgot the map.", "我站在小溪对面，忘了带地图。",
        "Toss it to me; I can catch it.", "把它扔给我，我能接住。",
    ),
    551: (
        "You're going hiking at noon without a hat.", "你中午去徒步却没戴帽子。",
        "At least use sunscreen as a shield against the sun.", "至少用防晒霜来抵挡阳光。",
    ),
    552: (
        "You want to feel more comfortable speaking English before your trip?", "你想在旅行前更自在地说英语吗？",
        "Try to immerse yourself in English by watching one show every night.", "试着每晚看一集节目，让自己沉浸在英语里。",
    ),
    566: (
        "The shelf is empty, but I need size ten boots.", "货架空了，但我需要十号靴子。",
        "Do you have anything out the back?", "后面的仓库还有货吗？",
    ),
    24: (
        "The supermarket prices keep changing, and I can't work out why.", "超市价格一直在变，我弄不明白为什么。",
        "What's the economy about anyway?", "经济到底是怎么回事？",
    ),
    39: (
        "Your sister is in the same school year as you?", "你姐姐和你是同一个学年吗？",
        "No, we're two years apart.", "不是，我们相差两岁。",
    ),
    73: (
        "I found your scarf at my place.", "我在我家找到你的围巾。",
        "Can you pop in for a minute to pick it up?", "你能顺路过来一会儿把它拿走吗？",
    ),
    88: (
        "The cake has arrived and everyone is hiding in the kitchen.", "蛋糕到了，大家都藏在厨房里。",
        "Congrats on another successful trip around the sun!", "恭喜你又成功绕太阳转了一圈！",
    ),
    94: (
        "We're meeting at the beach for lunch.", "我们要在海边吃午饭。",
        "Do you need me to bring anything?", "你需要我带点什么吗？",
    ),
    125: (
        "Why did Jacob agree to try vaping when he said he didn't want to?", "雅各布明明说不想尝试电子烟，为什么还是同意了？",
        "He may have felt peer pressure from the older kids.", "他可能感受到了年长孩子的同伴压力。",
    ),
    130: (
        "You drove three hours just to return a lost wallet?", "你开了三小时车，只是为了归还一个丢失的钱包？",
        "What on earth compelled you to do that?", "到底是什么促使你这么做？",
    ),
    132: (
        "Your parents were strict when you were little, weren't they?", "你小时候父母很严格，对吧？",
        "What did you get grounded for as a child?", "你小时候因为什么被禁足过？",
    ),
    231: (
        "You keep asking whether I remember cassette tapes.", "你一直问我记不记得磁带。",
        "How young do you think I am?", "你觉得我有多年轻？",
    ),
    235: (
        "Tomas is serving a long queue by himself.", "托马斯一个人服务长长的队伍。",
        "Do you want to help Tomas at the till?", "你想去帮托马斯收银吗？",
    ),
    245: (
        "The form only has room for a short title before the name.", "表格里姓名前只能写一个简短头衔。",
        "Put 'Dr.' on the badge; that abbreviation will fit in the space.", "在名牌上写“Dr.”吧，这个缩写正好放得下。",
    ),
    289: (
        "The library lets you borrow seeds to grow at home.", "图书馆可以让你借种子回家种。",
        "That's pretty cool. I didn't know libraries did that.", "这挺酷的。我不知道图书馆还会做这个。",
    ),
    292: (
        "We watched the first film last Friday.", "我们上周五看了第一部电影。",
        "Have you seen the sequel yet?", "你看续集了吗？",
    ),
    294: (
        "Your haircut looks great—did you do it yourself?", "你的发型看起来真不错，是自己剪的吗？",
        "No. Where do you get your hair cut?", "不是。你通常在哪里剪头发？",
    ),
    298: (
        "He wants everyone to wear costumes to the parent meeting.", "他想让每个人都穿戏服参加家长会。",
        "That sounds a bit extreme.", "听起来有点太夸张了。",
    ),
    1039: (
        "Why do teenagers use different words from their parents?", "为什么青少年会用和父母不同的词？",
        "Language evolves as each generation invents new ways to speak.", "每一代人都会创造新的说法，所以语言会不断演变。",
    ),
    1044: (
        "Why did you choose a homestay instead of a beach resort?", "你为什么选择住寄宿家庭，而不是海滨度假村？",
        "I want travel to expand my horizons, not just give me a break.", "我想让旅行开阔眼界，不只是休息一下。",
    ),
    1066: (
        "We know the bus leaves at six. What about the ticket price?", "我们知道公交六点出发。票价呢？",
        "As for the price, I think it's under ten dollars.", "至于价格，我想不到十美元。",
    ),
    1071: (
        "You've had four coffees and your hands are shaking.", "你已经喝了四杯咖啡，手都在抖。",
        "You might want to lay off the coffee for today.", "你今天可能该少喝点咖啡。",
    ),
    1076: (
        "You look nervous waiting for the ferry alone.", "你一个人等渡轮，看起来有点紧张。",
        "I'll try to strike up a conversation with the woman reading that book.", "我试着和正在看书的那位女士搭个话。",
    ),
    1082: (
        "Why is your bakery hiring extra staff in December?", "为什么你的面包店十二月要多招员工？",
        "It gets hectic here before Christmas.", "圣诞节前这里会忙得不可开交。",
    ),
    1085: (
        "We've spent an hour debating fonts. What is the real problem?", "我们已经花了一小时讨论字体。真正的问题是什么？",
        "The essence of the issue is that we still don't know who the poster is for.", "问题的本质是我们还不知道海报面向谁。",
    ),
    1090: (
        "Why do two tomatoes from the same box taste so different?", "为什么同一箱里的两个番茄味道差这么多？",
        "There's some variability in flavour from one batch to another.", "不同批次之间的风味会有些差异。",
    ),
    1097: (
        "You never bring an umbrella, even though you complain about rain.", "你从不带伞，尽管总抱怨下雨。",
        "Every single time I visit that town, it rains.", "我每次去那个镇都会下雨。",
    ),
    1099: (
        "Why did you keep practising after you missed the first shot?", "你第一次投失后为什么还一直练？",
        "I try to keep a learning mentality instead of giving up.", "我尽量保持学习的心态，而不是放弃。",
    ),
    1114: (
        "What do you actually do at the community radio station?", "你在社区电台到底做什么？",
        "Most of my work revolves around planning the weekend shows.", "我的大部分工作围绕安排周末节目展开。",
    ),
    1117: (
        "The garage is such a mess that I don't know where to begin.", "车库乱得我不知道从哪里开始收拾。",
        "Let's divide and conquer: you sort the tools, and I'll clear the boxes.", "我们分工吧：你整理工具，我清理箱子。",
    ),
    1118: (
        "The wedding invitation template still shows a name in brackets.", "婚礼请柬模板里还显示着方括号中的名字。",
        "That's a placeholder; replace it with the couple's names.", "那是占位文字，把它换成新人的名字。",
    ),
    1532: (
        "Can the washing machine finish before we leave?", "我们出门前洗衣机能洗完吗？",
        "Potentially, yes, if we use the short cycle.", "有可能，如果我们用快速洗程序。",
    ),
    1534: (
        "The twins remember the camping trip in completely different ways.", "这对双胞胎对那次露营的记忆完全不同。",
        "It's hard to reconcile their two versions of the story.", "很难调和他们对这件事的两种说法。",
    ),
    1537: (
        "We changed the opening hours, added signs, and trained the volunteers.", "我们改了开放时间、加了标识，还培训了志愿者。",
        "All those small changes amount to a major improvement.", "所有这些小改变加起来就是很大的改善。",
    ),
    1539: (
        "You saw a lot on the hike. What did you enjoy most?", "这次徒步你看到了很多。最喜欢什么？",
        "Seeing the mountains was the highlight of the trip.", "看到群山是这趟旅行最精彩的部分。",
    ),
    1562: (
        "We gave the plants one extra cup of water. Will that solve the problem?", "我们给植物多浇了一杯水。这能解决问题吗？",
        "That small change won't move the needle; they need more sunlight too.", "这个小改变不会带来明显效果；它们还需要更多阳光。",
    ),
    1565: (
        "Why couldn't the fans get near the singer after the concert?", "演唱会后粉丝为什么没法靠近歌手？",
        "A small army of reporters was waiting outside.", "外面等着一大群记者。",
    ),
    1579: (
        "Grandpa seems much weaker than he did last week.", "爷爷看起来比上周虚弱得多。",
        "The doctors are concerned about the rapid deterioration in his condition.", "医生担心他的状况在迅速恶化。",
    ),
    1584: (
        "Why is your video call freezing every few seconds?", "你的视频通话为什么每几秒就卡一下？",
        "It's lagging because the signal is weak in this room.", "因为这个房间信号很弱，所以它卡顿。",
    ),
    1585: (
        "Was the community meeting busy last night?", "昨晚的社区会议人多吗？",
        "Quite a lot of people came to share their ideas.", "有不少人来分享他们的想法。",
    ),
    1589: (
        "Can we double this cake recipe and then cut it back to the original size?", "我们能把这个蛋糕食谱加倍后再恢复原来的量吗？",
        "You can halve it from the full recipe, but not the other way around without changing the eggs.", "你可以从完整食谱减半，但反过来不改鸡蛋用量就不行。",
    ),
    1590: (
        "I borrowed your charger. Will mine work with your phone too?", "我借了你的充电器。我的也能给你的手机用吗？",
        "Yes, and it works the other way around too.", "能，而且反过来也一样能用。",
    ),
    1596: (
        "I've written down my sleep times for a week. Is that useful?", "我记录了一周的睡眠时间。这有用吗？",
        "It's useful to track things over time rather than judge one day.", "长期跟踪会更有用，不要只看某一天。",
    ),
    1604: (
        "The bus is late again. Does this happen every morning?", "公交又晚点了。这每天早上都会发生吗？",
        "Traffic jams have become a regular feature of city life.", "交通拥堵已经成了城市生活中的常见现象。",
    ),
    1607: (
        "What do you look for in a good babysitter?", "你觉得一个好的保姆该有什么特点？",
        "Patience is an important characteristic of a good babysitter.", "耐心是好保姆的重要特质。",
    ),
    1615: (
        "The shop manager is leaving early. Who will open and close today?", "店长要早走。今天谁负责开店和关店？",
        "I can take on those two responsibilities this afternoon.", "今天下午我可以承担这两项职责。",
    ),
    1623: (
        "The family tree has a dash instead of a birth date for one person.", "家谱里有个人的出生日期位置写着横线。",
        "A missing value is represented by a dash.", "缺失的信息用横线表示。",
    ),
    1624: (
        "I keep adding names to the picnic list. Where will the new rows go?", "我一直往野餐名单里加名字。新行会出现在哪里？",
        "The table extends downwards when new names are added.", "加入新名字后，表格会向下延伸。",
    ),
    1632: (
        "We're hanging this picture above the sofa. Is it straight?", "我们要把这幅画挂在沙发上方。它摆正了吗？",
        "Keep the frame horizontal, not vertical or diagonal.", "让画框保持水平，不要竖直或倾斜。",
    ),
    1634: (
        "Which path should we take with the pram?", "我们推婴儿车该走哪条路？",
        "The coastal path is better in that it stays flat.", "沿海小路更好，因为它一直很平坦。",
    ),
    1410: (
        "Why did the maths lesson become confusing halfway through?", "数学课为什么上到一半变得难懂了？",
        "It got confusing when we got into negatives.", "讲到负数时就开始让人困惑了。",
    ),
    1411: (
        "We're both tired, but still have a two-hour drive home.", "我们都累了，但回家还要开两小时车。",
        "It would be sensible to stop for the night.", "停下来过夜会是明智的选择。",
    ),
    1418: (
        "I checked every step of your homework. Is the answer right?", "我检查了你作业的每一步。答案对吗？",
        "Mathematically, the answer is correct.", "从数学上说，答案是正确的。",
    ),
    1425: (
        "Why are there flags from so many countries at the games?", "为什么比赛现场有那么多国家的旗帜？",
        "New Zealand is a member of the Commonwealth.", "新西兰是英联邦成员。",
    ),
    1437: (
        "Are you still hurting from your fall yesterday?", "你昨天摔倒后还疼吗？",
        "The pain has started to fade away.", "疼痛已经开始慢慢消退。",
    ),
    1469: (
        "Did people always use this bike path through the park?", "人们以前一直走公园里的这条自行车道吗？",
        "No, it's a relatively recent development.", "不是，这是比较近期才有的变化。",
    ),
    1476: (
        "Why do birdwatchers visit the wetlands every spring?", "为什么观鸟者每年春天都来湿地？",
        "The wetlands are home to dozens of bird species.", "这片湿地是数十种鸟类的栖息地。",
    ),
    1477: (
        "How much is one metre in centimetres?", "一米等于多少厘米？",
        "One metre is equivalent to 100 centimetres.", "一米等于一百厘米。",
    ),
    1480: (
        "The neighbour wants to turn her garage into a shop.", "邻居想把车库改成商店。",
        "The land cannot be used for commercial purposes.", "这块地不能用于商业用途。",
    ),
    1484: (
        "Why do sailors check the forecast before leaving the coast?", "水手离岸前为什么要看天气预报？",
        "New Zealand has strong offshore winds in that area.", "新西兰那一带海上风很强。",
    ),
    1489: (
        "Why did he make that sarcastic speech at the party?", "他为什么在派对上说那番讽刺的话？",
        "His remarks were calculated to provoke anger.", "他的言论是故意激怒人的。",
    ),
    1511: (
        "How long should I set aside to paint the shed?", "我该留出多长时间给工具棚刷漆？",
        "It takes a fair bit of time if you prepare the walls properly.", "如果认真处理墙面，会花不少时间。",
    ),
    1408: (
        "You've been quiet since the camping trip. What are you thinking about?", "露营回来后你一直很安静。在想什么？",
        "The trip gave me an opportunity for reflection.", "这趟旅行给了我反思的机会。",
    ),
    1429: (
        "Will this photo fit in the frame we bought?", "这张照片能放进我们买的相框吗？",
        "Its dimensions are 20 by 30 centimetres.", "它的尺寸是二十乘三十厘米。",
    ),
    1432: (
        "Why does the science class have a display about volcanoes and earthquakes?", "为什么科学课有关于火山和地震的展板？",
        "Earthquakes and volcanic eruptions are natural phenomena.", "地震和火山喷发都是自然现象。",
    ),
    1435: (
        "Why do we need to carry water on a short walk?", "为什么短途步行也要带水？",
        "Water is vital to human life, especially on a hot day.", "水对生命至关重要，尤其是在炎热的日子。",
    ),
    1440: (
        "Why did Sam qualify for the training programme?", "萨姆为什么能参加这个培训项目？",
        "Her educational attainment met the entry requirement.", "她的学历达到了入学要求。",
    ),
    1441: (
        "Why is the library running free reading classes for adults?", "图书馆为什么为成年人开免费的阅读课？",
        "They want to improve the town's literacy rate.", "他们想提高这个镇的识字率。",
    ),
    1459: (
        "It hasn't rained for weeks. How are the crops surviving?", "已经几周没下雨了。庄稼是怎么存活的？",
        "Farmers rely on irrigation during dry periods.", "干旱时期农民依靠灌溉。",
    ),
    1460: (
        "Why can that farm pack so many apples so quickly?", "为什么那个农场能这么快包装那么多苹果？",
        "It uses modern machinery during harvest.", "收获季它使用现代机械。",
    ),
    1463: (
        "Why is the battery still charging after the house lights are on?", "房子里的灯都亮了，为什么电池还在充电？",
        "The solar panels produce surplus electricity during the day.", "太阳能板白天会产生多余的电。",
    ),
    313: (
        "Why did you move the picnic indoors?", "你为什么把野餐搬到室内？",
        "It's absolutely sweltering today.", "今天热得要命。",
    ),
    331: (
        "Why are there lumps in the pancake batter?", "煎饼面糊里为什么有结块？",
        "The flour has gone clumpy in the cupboard.", "面粉在橱柜里结块了。",
    ),
    333: (
        "Why did you choose that blanket for the baby?", "你为什么给宝宝选那条毯子？",
        "The texture of this fabric is soft and gentle.", "这种布料的质地柔软亲肤。",
    ),
    339: (
        "Did you feel at home when you joined the new team?", "加入新团队时你很快融入了吗？",
        "It took me a while to integrate into the team.", "我花了一段时间才融入团队。",
    ),
    352: (
        "Why is the minister always talking about the budget?", "为什么这位部长总在谈预算？",
        "She holds the finance portfolio.", "她负责财政事务。",
    ),
    354: (
        "Why must we wear helmets at the construction visit?", "为什么参观施工现场时必须戴头盔？",
        "Wearing a helmet is mandatory on this site.", "在这个场地戴头盔是强制要求。",
    ),
    356: (
        "Have many people come into the shop this afternoon?", "今天下午有很多人进店吗？",
        "No, it's been very quiet.", "没有，一直很冷清。",
    ),
    363: (
        "Why is your grandmother reluctant to throw out those figurines?", "你奶奶为什么舍不得扔掉那些小雕像？",
        "A lot of people have their collections displayed in cabinets.", "很多人把自己的收藏展示在柜子里。",
    ),
    375: (
        "Why is that little hotel so peaceful even in summer?", "为什么那家小酒店即使夏天也很安静？",
        "It's off the beaten path, far from the main road.", "它远离热门路线，离主路很远。",
    ),
    943: (
        "Why are you working an extra shift this weekend?", "你为什么这个周末还要加班？",
        "We're trying to make ends meet after the rent went up.", "房租涨了以后，我们得努力维持收支平衡。",
    ),
    946: (
        "Have you decided whether to move house yet?", "你决定要不要搬家了吗？",
        "As yet, nothing is decided, but the best is yet to come.", "目前还没有决定，但最好的还在后头。",
    ),
    947: (
        "The bus is late again?", "公交又晚点了？",
        "Yet another delay—this is getting ridiculous.", "又一次延误，这越来越离谱了。",
    ),
    948: (
        "Why are we planning such a big party for your great-aunt?", "为什么要为你曾祖姨妈办这么大的派对？",
        "She's a centenarian this year.", "她今年满一百岁。",
    ),
    956: (
        "How did you feel during that three-hour lecture?", "那场三个小时的讲座让你感觉怎么样？",
        "The lecture was boring, so I was bored halfway through.", "讲座很无聊，所以到一半我就觉得厌烦了。",
    ),
    973: (
        "Why did you miss the speech at the birthday party?", "你为什么错过了生日派对上的演讲？",
        "The noise was a distraction, but it was a special occasion, so nobody minded.", "噪音让人分心，但那是个特别场合，所以没人介意。",
    ),
    975: (
        "Why is the science exhibition showing shrinking ice?", "为什么科学展览在展示缩小的冰块？",
        "The polar ice caps are melting as the climate warms.", "随着气候变暖，极地冰盖正在融化。",
    ),
    988: (
        "I saw moving boxes outside your flat.", "我看到你公寓外有搬家纸箱。",
        "Excuse me if I'm being a bit nosy, but are you moving?", "如果我有点多管闲事请见谅，不过你要搬家了吗？",
    ),
    993: (
        "Should I visit Ava if she still has that cough?", "如果艾娃还咳嗽，我该去看她吗？",
        "You shouldn't; it may still be contagious.", "最好别去；可能还会传染。",
    ),
    1009: (
        "How did you and your flatmate end up on the same train that day?", "那天你和室友怎么会刚好坐上同一趟火车？",
        "It was a twist of fate that changed both our lives.", "那是一个改变了我们两人生活的命运转折。",
    ),
    809: (
        "Why do visitors travel so far to see that university?", "为什么游客跑那么远去看那所大学？",
        "It's renowned for its old library and gardens.", "它以古老的图书馆和花园闻名。",
    ),
    810: (
        "The weather was terrible. Did you cancel the walk?", "天气很糟。你取消散步了吗？",
        "It was raining; nonetheless, we finished the walk.", "当时在下雨；不过我们还是走完了。",
    ),
    817: (
        "Can I join the pottery course if I have never used a wheel?", "如果我从没用过拉坯机，还能上陶艺课吗？",
        "Yes, no prior experience is required.", "可以，不需要之前的经验。",
    ),
    823: (
        "Who is helping Mia serve lunch at the fundraiser?", "谁在筹款午餐会上帮米娅上菜？",
        "Her sister is serving alongside her today.", "她姐姐今天和她一起服务。",
    ),
    824: (
        "Why can't the florist open a shop in that garage?", "为什么花店不能在那间车库开店？",
        "The council says it cannot be used for commercial purposes.", "市政会说那里不能用于商业用途。",
    ),
    825: (
        "Did moving the party indoors change how many people came?", "把派对搬到室内改变了来的人数吗？",
        "It did not materially affect the turnout.", "这没有实质性影响到出席人数。",
    ),
    830: (
        "Why did the meeting about the garden fence take all afternoon?", "为什么讨论花园篱笆的会议花了一下午？",
        "The negotiation took hours because both neighbours wanted different things.", "谈判花了好几个小时，因为两家邻居想要的不同。",
    ),
    836: (
        "Did everyone get out of the cinema safely when the alarm rang?", "警报响起时，大家都安全离开电影院了吗？",
        "Yes, the evacuation was completed safely.", "是的，疏散安全完成了。",
    ),
    845: (
        "Your sister works with loans and savings, right?", "你姐姐是做贷款和储蓄相关工作的，对吧？",
        "Yes, she works in the finance sector.", "对，她在金融行业工作。",
    ),
    851: (
        "How did your child settle into the new class?", "你孩子适应新班级怎么样？",
        "The transition was smooth after the first week.", "第一周后，过渡就很顺利。",
    ),
    854: (
        "Why is my phone bill higher this month?", "为什么我这个月的手机账单更高？",
        "It's a one-off payment for the new handset.", "这是买新手机的一次性付款。",
    ),
    857: (
        "How do gardeners spread wildflower seeds over a big field?", "园丁怎么把野花种子撒到大片田里？",
        "They scatter the seeds by hand in spring.", "他们在春天用手撒种子。",
    ),
    862: (
        "Why hasn't Grandma left the house since her injury?", "奶奶受伤后为什么一直没出门？",
        "She's been confined to the house while she recovers.", "康复期间她只能待在家里。",
    ),
    865: (
        "This kettle looked fine in the shop. Should we keep it?", "这个水壶在店里看着没问题。我们该留着吗？",
        "On closer inspection, the product is defective.", "仔细检查后，这个产品有瑕疵。",
    ),
    869: (
        "Are you taking the job at the café after school?", "你放学后要去咖啡馆做那份工作吗？",
        "Yes, it has good prospects for learning customer service.", "要，它对学习客户服务很有前景。",
    ),
    871: (
        "Was it easy to bring the dog down from the cliff path?", "把那只狗从悬崖小路上救下来容易吗？",
        "No, the rescue took hours in the rain.", "不容易，雨中的救援花了好几个小时。",
    ),
    877: (
        "Why did he delete the betting app from his phone?", "他为什么把手机里的投注应用删了？",
        "He didn't want to fall into the trap of online gambling.", "他不想落入网络赌博的陷阱。",
    ),
    897: (
        "We both wore the same costume without planning it.", "我们没商量却穿了同样的戏服。",
        "That was a bizarre coincidence.", "那真是个奇怪的巧合。",
    ),
    898: (
        "Why were you and Leo at the same café in different cities?", "你和利奥怎么会分别在不同城市的同一家咖啡馆？",
        "It was an amazing coincidence.", "这真是个令人惊讶的巧合。",
    ),
    906: (
        "Why did the singer lose all his friends and money?", "那位歌手为什么失去了所有朋友和钱？",
        "His temper was his undoing.", "他的坏脾气毁了他。",
    ),
    908: (
        "Why are the workers wearing hard hats near the loose cables?", "为什么工人在松动电线旁戴着安全帽？",
        "Loose cables pose a risk to safety.", "松动的电线会带来安全风险。",
    ),
    912: (
        "Why are the children dripping wet after lunch?", "午饭后孩子们为什么浑身湿透？",
        "They were splashing in the pool.", "他们在游泳池里戏水。",
    ),
    915: (
        "How was the school concert last night?", "昨晚学校音乐会怎么样？",
        "It was a splendid performance.", "那是一场精彩的表演。",
    ),
    920: (
        "Why are you looking at that ring for so long?", "你为什么盯着那枚戒指看这么久？",
        "The workmanship is exquisite.", "工艺非常精美。",
    ),
    921: (
        "How was your holiday by the lake?", "你在湖边的假期怎么样？",
        "It was fantastic—we swam every morning.", "太棒了，我们每天早上都游泳。",
    ),
    922: (
        "Why are you buying that dress for the party?", "你为什么要买那条裙子去参加派对？",
        "It's gorgeous, and it fits perfectly.", "它很漂亮，而且非常合身。",
    ),
    923: (
        "How is your daughter doing with piano this term?", "你女儿这学期钢琴学得怎么样？",
        "Her progress is really impressive.", "她的进步真让人印象深刻。",
    ),
    932: (
        "Why are so many people leaving the factory today?", "为什么今天有这么多人离开工厂？",
        "Seventy workers were made redundant.", "七十名工人被裁员了。",
    ),
    934: (
        "Where should the new volunteer sit on her first day?", "新志愿者第一天该坐在哪里？",
        "Each employee has a workstation by the window.", "每位员工在窗边都有一个工作位。",
    ),
    935: (
        "Why are you returning that kettle to the shop?", "你为什么把那个水壶退回商店？",
        "The product is defective.", "这个产品有缺陷。",
    ),
    936: (
        "Why does the bike brake keep sticking?", "自行车刹车为什么总是卡住？",
        "The bike has a serious defect.", "这辆自行车有严重缺陷。",
    ),
    937: (
        "Why are you buying two pizzas for just the two of us?", "为什么我们两个人要买两份披萨？",
        "The shop is running a two-for-one special today.", "这家店今天有买一送一优惠。",
    ),
    939: (
        "Why did you replace the old door handle?", "你为什么换掉旧门把手？",
        "This part was installed in replacement of the old one.", "这个零件是用来替换旧零件安装的。",
    ),
    726: (
        "You've been looking after the twins all week. Are you coping?", "你照顾双胞胎一整周了。还应付得来吗？",
        "I cope by taking a short walk when they nap.", "他们午睡时我会短暂散步来调节。",
    ),
    732: (
        "How can a deaf student see the rhythm in a song?", "聋哑学生怎么能看见歌曲的节奏？",
        "This waveform gives us a direct visual representation of sound.", "这个波形给我们直接的声音视觉呈现。",
    ),
    736: (
        "Why couldn't the actor move when the door creaked open?", "门嘎吱响时，为什么演员动不了？",
        "His body was rigid with fear.", "他的身体因恐惧而僵硬。",
    ),
    742: (
        "Why is there a plaque outside the old teacher's classroom?", "为什么老教师的教室外有一块牌匾？",
        "Her work left a lasting legacy at the school.", "她的工作在学校留下了长久的影响。",
    ),
    744: (
        "Do you want to try bungee jumping on our trip?", "旅行时你想试试蹦极吗？",
        "Not really—it's not my cup of tea.", "不太想——那不是我喜欢的事。",
    ),
    753: (
        "Why do we only see the old houses that are still standing?", "为什么我们只看到还保存下来的老房子？",
        "That's survivorship bias; the weaker houses disappeared long ago.", "这就是幸存者偏差；不结实的房子早就消失了。",
    ),
    755: (
        "Can you carry this bag of oranges by yourself?", "你能自己搬这袋橙子吗？",
        "No, it's way too heavy.", "不行，它太重了。",
    ),
    793: (
        "Why are you taking so many programming classes?", "你为什么选这么多编程课？",
        "My major is Applied Computing.", "我的专业是应用计算。",
    ),
    1169: (
        "You finished the whole charity run even after your shoe broke.", "即使鞋子坏了，你还是跑完了整场慈善跑。",
        "I wanted to accomplish something I had trained for.", "我想完成一件自己为之训练过的事。",
    ),
    1181: (
        "Should we let the toddler drink from the public fountain?", "我们该让幼儿喝公共饮水台里的水吗？",
        "Only if the tap and cup look sanitary.", "只有水龙头和杯子看起来卫生才行。",
    ),
    1183: (
        "That man walked straight past everyone waiting for tickets.", "那个人径直从所有等票的人身边走过去。",
        "He shouldn't jump the line like that.", "他不该这样插队。",
    ),
    1187: (
        "Why does the librarian run puzzles for the children every Wednesday?", "为什么图书管理员每周三都给孩子们安排谜题？",
        "They build cognitive skills while the children play.", "孩子们玩耍时也能培养认知能力。",
    ),
    1191: (
        "The seller claimed the broken phone was brand new.", "卖家声称这部坏手机是全新的。",
        "The mendacity of that claim was obvious once we saw the scratches.", "一看到划痕，那种说法的虚假就很明显了。",
    ),
    1196: (
        "They want us to charge guests for tap water.", "他们想让我们向客人收自来水费。",
        "That's ridiculous; nobody will accept it.", "这太荒谬了；没人会接受。",
    ),
    1203: (
        "The chicken smells good but tastes bland.", "鸡肉闻起来很香，但吃起来没味道。",
        "Season it with a little lemon and pepper.", "加一点柠檬和胡椒调味。",
    ),
    1204: (
        "I spilled juice on the tablecloth, but it will wash out.", "我把果汁洒在桌布上了，但能洗掉。",
        "Don't make a big deal out of it.", "别把这件事看得太严重。",
    ),
    1208: (
        "Maya said she was 'busy' when we invited her.", "我们邀请玛雅时，她说自己“很忙”。",
        "Do you think she was trying to imply that she didn't want to come?", "你觉得她是在暗示自己不想来吗？",
    ),
    1209: (
        "Your nephew is shy around new people.", "你外甥在陌生人面前很害羞。",
        "Give him time to bond with you through games.", "给他一点时间，通过游戏和你建立感情。",
    ),
    1211: (
        "We booked the picnic table for noon. Where is Ben?", "我们订了中午的野餐桌。本在哪儿？",
        "He'll probably rock up late, as usual.", "他大概又会像往常一样迟到才出现。",
    ),
    1218: (
        "I brought the soup you liked after your cold.", "你感冒后，我带来了你喜欢的汤。",
        "That's lovely—thank you so much.", "太贴心了，非常感谢。",
    ),
    1222: (
        "The new flat is cheaper, but it's an hour from school.", "新公寓更便宜，但离学校要一个小时。",
        "No, that choice doesn't feel right for us.", "不，这个选择对我们来说不太合适。",
    ),
    1226: (
        "The vase has a blue pattern that curls upward.", "花瓶上有一道向上盘旋的蓝色图案。",
        "The line spirals around the glass.", "那条线绕着玻璃盘旋。",
    ),
    1227: (
        "We want vines to climb over the patio wall.", "我们想让藤蔓爬满露台的墙。",
        "Let's fix a wooden lattice there for them.", "在那里装一个木格架吧。",
    ),
    1229: (
        "The café with the longest queue must be the best one, right?", "排队最长的咖啡馆一定是最好的，对吧？",
        "It's not necessarily the best; it may just have the only outdoor table.", "它不一定是最好的；可能只是唯一有户外桌位的店。",
    ),
    1230: (
        "Your daughter can read the story aloud, but does she understand it?", "你女儿能把故事朗读出来，但她理解了吗？",
        "Her comprehension is improving; she answered every question.", "她的理解能力在提高；每个问题都答上来了。",
    ),
    1231: (
        "We keep missing the morning bus because we leave late.", "我们总因为出门晚而错过早班车。",
        "From now on, let's pack our bags the night before.", "从现在起，我们前一天晚上就把包收好。",
    ),
    1232: (
        "You've been indoors all weekend and look tired.", "你整个周末都待在室内，看起来很累。",
        "A short walk in the sun would do you good.", "去阳光下散会儿步会对你有好处。",
    ),
    1233: (
        "Can we see many stars outside the city?", "城外能看到很多星星吗？",
        "Yes, the sky is so starry at the campsite.", "可以，营地的天空星光璀璨。",
    ),
    1234: (
        "That cat has been sleeping behind the bakery for three days.", "那只猫已经在面包店后面睡了三天。",
        "It looks like a stray cat; let's call the shelter.", "它看起来像一只流浪猫；我们给收容所打电话吧。",
    ),
    1235: (
        "Did you really enjoy your first pottery class?", "你真的喜欢第一次陶艺课吗？",
        "I genuinely did—I lost track of time.", "我真的很喜欢，完全忘了时间。",
    ),
    1237: (
        "The bakery has just put warm cinnamon rolls in the window.", "面包店刚把热腾腾的肉桂卷放到橱窗里。",
        "Look at Theo licking his lips already.", "看，西奥已经在舔嘴唇了。",
    ),
    1239: (
        "The dog snapped when I reached for its bowl.", "我伸手去拿狗碗时，狗突然扑咬了一下。",
        "I drew back before it could bite me.", "它咬到我之前，我就往后退了。",
    ),
    1240: (
        "That actor collapsed in the final scene of the old detective film.", "那部老侦探电影的最后一幕里，演员倒下了。",
        "In the scene, he fell dead on the spot after the poison took effect.", "在那一幕中，毒药发作后他当场倒地身亡。",
    ),
    1241: (
        "I'm trying not to buy dessert tonight.", "我今晚尽量不买甜点。",
        "Don't walk past that bakery—the smell will tempt you.", "别从那家面包店门口走过，香味会诱惑你的。",
    ),
    1248: (
        "Why are you carrying your camera to the coast before sunrise?", "你为什么日出前就带着相机去海边？",
        "I'm learning photography, and the light is best early in the morning.", "我在学摄影，清晨的光线最好。",
    ),
    1250: (
        "Do you still hear from your old neighbour?", "你还会收到老邻居的消息吗？",
        "Yes, she sends a postcard from time to time.", "会，她偶尔会寄明信片来。",
    ),
    1251: (
        "We're planting trees at the park on Saturday. Want to join?", "我们周六去公园植树。想参加吗？",
        "Yes, I'm keen to help.", "想，我很愿意帮忙。",
    ),
    1252: (
        "Those boots have survived three winters. Are they still okay?", "那双靴子经历了三个冬天。还好吗？",
        "They've held up well, even on wet walks.", "它们一直很耐穿，就算雨天走路也没问题。",
    ),
    1254: (
        "The new playground looks great, but why did they remove the shade trees?", "新操场看起来很棒，但他们为什么砍掉了遮阴的树？",
        "They improved the view at the expense of comfort.", "他们以牺牲舒适度为代价改善了景观。",
    ),
    1255: (
        "The children don't understand what a food chain is.", "孩子们不明白什么是食物链。",
        "Draw a simple diagram to illustrate how energy moves.", "画一张简单图来说明能量如何传递。",
    ),
    1256: (
        "Why is the mother bird carrying worms to the nest all day?", "为什么鸟妈妈整天把虫子叼回巢里？",
        "She's raising her young.", "她在养育幼鸟。",
    ),
    1257: (
        "You knew about the concert before anyone else.", "你比其他人都早知道那场演唱会。",
        "Mia told me way before the tickets went on sale.", "米娅在门票开售很久前就告诉我了。",
    ),
    1259: (
        "The vegetables are too large for the soup pot.", "蔬菜块对汤锅来说太大了。",
        "I'll chop them up before we start cooking.", "开始做饭前我会把它们切碎。",
    ),
    1260: (
        "Can that ship really fit through the harbour?", "那艘船真的能穿过港口吗？",
        "It's gigantic, but the channel is wide enough.", "它非常巨大，但航道够宽。",
    ),
    1261: (
        "Why is the science museum letting us touch those plastic bones?", "为什么科学博物馆允许我们触摸那些塑料骨头？",
        "They make up a model of a human skeleton.", "它们组成了一个人体骨骼模型。",
    ),
    1263: (
        "Why are those plants growing in the aquarium?", "为什么那些植物长在水族箱里？",
        "They're aquatic plants, so their roots stay underwater.", "它们是水生植物，所以根部泡在水里。",
    ),
    1265: (
        "Where did you hurt your finger?", "你手指哪里受伤了？",
        "Right at the tip, where I caught it in the drawer.", "就在指尖，我被抽屉夹到了那里。",
    ),
    1266: (
        "The little boy is scared of the tall slide.", "那个小男孩害怕高滑梯。",
        "He's clinging onto his dad's hand.", "他紧紧抓着爸爸的手。",
    ),
    1267: (
        "Why is Jamie offering the teacher coffee and carrying all her books?", "杰米为什么给老师端咖啡，还替她拿所有书？",
        "He's trying to suck up to her before grades come out.", "他想在成绩出来前讨好她。",
    ),
    1270: (
        "The rain is so heavy that I can barely hear you.", "雨太大了，我几乎听不见你说话。",
        "That whistle can pierce through the noise.", "那只哨子能穿透噪音。",
    ),
    1271: (
        "Why did Anna start sneezing as soon as she visited the cat?", "安娜一见到猫为什么就打喷嚏？",
        "She has an allergy to animal hair.", "她对动物毛发过敏。",
    ),
    1272: (
        "Have you decided which university course to take?", "你决定读哪个大学专业了吗？",
        "I'm not quite sure yet; I'm visiting two campuses first.", "我还不太确定，得先参观两所学校。",
    ),
    1277: (
        "How does the canoe move when you pull the paddle?", "你划桨时，独木舟是怎么前进的？",
        "Each stroke propels it forward.", "每一次划桨都会推动它向前。",
    ),
    1280: (
        "How will we lead the pony from the field?", "我们怎么把小马从田里牵出来？",
        "Put its halter on first, then clip on the rope.", "先给它戴上笼头，再扣上牵绳。",
    ),
    1287: (
        "The puppy fell into the storm drain. Is anyone coming?", "小狗掉进雨水井里了。有人来帮忙吗？",
        "The fire crew is on the way to rescue it.", "消防队正在赶来救它。",
    ),
    1288: (
        "Why are the book shelves empty at the old library?", "旧图书馆的书架为什么空了？",
        "They're relocating the collection to the new building.", "他们正在把藏书搬到新楼。",
    ),
    1291: (
        "We only have one long table for ten guests.", "十位客人只有一张长桌。",
        "Let's arrange the chairs around it so everyone can talk.", "把椅子围着它摆放，这样每个人都能交谈。",
    ),
    1292: (
        "What is that small stone house at the edge of the field?", "田边那座小石屋是什么？",
        "It's an old dwelling that a shepherd used to live in.", "那是一座牧羊人曾经住过的老住所。",
    ),
    1295: (
        "How did you get into the costume party without being recognised?", "你怎么在化装派对上没被认出来？",
        "I used a wig and glasses as a disguise.", "我用假发和眼镜作伪装。",
    ),
    1297: (
        "Why are the children digging for fossils at the museum?", "孩子们为什么在博物馆里挖化石？",
        "They're learning about prehistoric animals.", "他们在学习史前动物。",
    ),
    1299: (
        "The wind is getting stronger. Are the sailing lessons still on?", "风越来越大。帆船课还继续吗？",
        "They've suspended the lessons until the weather improves.", "课程已暂停，等天气好转再继续。",
    ),
    1300: (
        "Where should we stand to watch the fireworks?", "我们站在哪里看烟花最好？",
        "The hill behind the school gives us the best vantage point.", "学校后面的山坡给我们最好的观景位置。",
    ),
    1305: (
        "Why is everyone lining up outside that restaurant with a warning sign?", "为什么大家在那家挂着警告牌的餐馆外排队？",
        "It's an extreme eatery where you can try very spicy food.", "那是一家极限餐厅，可以挑战非常辣的食物。",
    ),
    1307: (
        "The soup still has chunks of pumpkin in it.", "汤里还有南瓜块。",
        "Blend it for another minute until it's smooth.", "再搅打一会儿，直到它变得顺滑。",
    ),
    1311: (
        "Why do you need a map every time you visit Tokyo?", "为什么你每次去东京都需要地图？",
        "It's such a huge metropolis that I still get lost.", "它是一座巨大的都市，我还是会迷路。",
    ),
    1312: (
        "Did the coach write down the instructions?", "教练把指示写下来了吗？",
        "No, she gave us verbal directions before the match.", "没有，她在比赛前口头告诉了我们。",
    ),
    1313: (
        "Why are we taking a flight instead of a ferry to the island?", "为什么我们去那座岛坐飞机而不是渡轮？",
        "It's some 800 miles away from Jakarta.", "它离雅加达大约八百英里。",
    ),
    1314: (
        "The council has cleared an empty field and wants to start again.", "市政会清空了一块空地，想从头开始建设。",
        "Building a new city from scratch will only lead to more pollution.", "从零开始建一座新城只会带来更多污染。",
    ),
    1315: (
        "Why is there a mark on the dining table?", "餐桌上为什么有一道痕迹？",
        "The cat scratched it while jumping down.", "猫跳下来时把它划伤了。",
    ),
    1317: (
        "This jacket feels expensive, but compared with designer brands it isn't.", "这件夹克感觉很贵，但和设计师品牌相比并不算贵。",
        "Price is relative; it depends what you compare it with.", "价格是相对的，要看你拿它和什么比较。",
    ),
    1318: (
        "Why is the rooster chasing the new hen around?", "为什么公鸡追着新来的母鸡跑？",
        "It's trying to assert dominance over the flock.", "它在试图确立自己在鸡群中的主导地位。",
    ),
    1319: (
        "Who are you playing in the final?", "你决赛要和谁比赛？",
        "My opponent is the girl who won last year's tournament.", "我的对手是去年赢得锦标赛的那个女孩。",
    ),
    1321: (
        "Why are the actors wearing chain mail at the castle?", "为什么演员在城堡里穿锁子甲？",
        "The film is set in medieval Europe.", "这部电影以中世纪欧洲为背景。",
    ),
    1325: (
        "What did you see in the museum's underground room?", "你在博物馆地下展厅看到了什么？",
        "They keep the Roman antiquities there.", "那里收藏着罗马古物。",
    ),
    1328: (
        "Why is your neighbour wearing a winter coat in summer?", "为什么你邻居夏天穿着冬大衣？",
        "It is a bit peculiar, isn't it?", "这有点奇怪，不是吗？",
    ),
    1354: (
        "I sent the rental contract yesterday. Is there anything else?", "我昨天发了租房合同。还需要做什么吗？",
        "With regard to the contract, please add your phone number.", "关于这份合同，请补上你的电话号码。",
    ),
    1357: (
        "The carrots won't cook evenly in big chunks.", "胡萝卜块太大，无法均匀煮熟。",
        "Chop them into small pieces first.", "先把它们切成小块。",
    ),
    1362: (
        "Why does the teacher give the children a checklist before packing up?", "老师为什么在收拾东西前给孩子们一张清单？",
        "It supports their executive function and helps them organise tasks.", "这能帮助他们的执行功能，并让他们组织好任务。",
    ),
    1368: (
        "Someone left a sofa beside the creek overnight.", "有人夜里把一张沙发丢在小溪旁。",
        "They shouldn't dump rubbish there.", "他们不该在那里乱倒垃圾。",
    ),
    1373: (
        "I bought the mug online. What happens now?", "我在网上买了这个杯子。接下来会怎样？",
        "You receive a confirmation email after the order is processed.", "订单处理后，你会收到一封确认邮件。",
    ),
    1381: (
        "Everyone wants to go camping, but you look unsure.", "大家都想去露营，但你看起来不太确定。",
        "Sleeping in a tent doesn't really appeal to me.", "睡帐篷对我没有太大吸引力。",
    ),
    1404: (
        "The bakery refuses to use artificial colours even when it costs more.", "即使成本更高，那家面包店也拒绝使用人工色素。",
        "They hew to strict ingredient standards.", "他们坚持严格的配料标准。",
    ),
    1651: (
        "You keep screenshots of useful phrases on your phone.", "你一直在手机里保存有用短语的截图。",
        "I keep new words, useful phrases, and example sentences in one notebook.", "我把新单词、实用短语和例句记在同一本笔记本里。",
    ),
    1656: (
        "We can save money by buying the cheapest paint.", "买最便宜的油漆可以省钱。",
        "Not at the expense of safety; the nursery walls need washable paint.", "但不能以安全为代价；托儿所的墙需要可清洗的油漆。",
    ),
    1659: (
        "I've never used the self-service checkout.", "我从没用过自助结账机。",
        "No problem—I'll talk you through it step by step.", "没问题，我一步一步带你操作。",
    ),
    1664: (
        "We want to light a fire on the beach tonight.", "我们今晚想在海滩上生火。",
        "Check the rules first; you don't want to fall foul of local regulations.", "先查一下规定；你可不想违反当地规定。",
    ),
    1007: (
        "Why are they raising the minimum wage this year?", "为什么他们今年要提高最低工资？",
        "They hope it will narrow the income gap.", "他们希望这能缩小收入差距。",
    ),
    1017: (
        "Why did everyone jump during the birthday party?", "生日派对上为什么大家都吓了一跳？",
        "The balloon burst beside the cake.", "气球在蛋糕旁边爆了。",
    ),
    899: (
        "He wants to build a snowman indoors with bags of ice.", "他想用几袋冰在室内堆雪人。",
        "That silly idea sounds ridiculous.", "那个傻主意听起来很荒谬。",
    ),
    661: (
        "We can take the early bus or wait for the train. Which is easier?", "我们可以坐早班公交，或者等火车。哪个更方便？",
        "The former is cheaper, but the latter gets us there faster.", "前者更便宜，但后者能更快到达。",
    ),
    568: (
        "Why is there a white layer at the bottom of the kettle?", "水壶底为什么有一层白色的东西？",
        "It's residue left after the water boiled.", "那是水煮沸后留下的残留物。",
    ),
}


# These entries repair older note cards whose original examples were fragments,
# definitions, or a generic question followed by an isolated sentence.  Every
# pair begins with a particular event and has a reply that moves that event on.
CURATED_REAL_LIFE_SCENES.update({
    9: (
        "I took a bite of this red fruit at the market and my face puckered.", "我在市场咬了一口这个红色水果，脸都皱起来了。",
        "Be careful—hawthorn is very sour.", "小心，山楂很酸。",
    ),
    10: (
        "Grandma is making a fruit filling for the pie tonight.", "奶奶今晚要做水果派馅。",
        "She can use plums or prunes, depending on what is in the cupboard.", "她可以用李子或西梅，看橱柜里有什么。",
    ),
    30: (
        "Your sister is moving house and the school concert is tonight.", "你姐姐在搬家，学校音乐会又在今晚。",
        "With everything happening right now, let's postpone dinner until Sunday.", "眼下这么多事情挤在一起，我们把晚饭推到周日吧。",
    ),
    37: (
        "Can we still get tickets for the lantern festival this Saturday?", "我们这周六还能买到灯会的票吗？",
        "No, it was booked out weeks ago.", "不行，几周前就订满了。",
    ),
    43: (
        "Why are the words in this superhero comic so large?", "为什么这本超级英雄漫画里的字这么大？",
        "A lot of comic books are written in capital letters so the action stands out.", "很多漫画会用大写字母，让动作场面更醒目。",
    ),
    63: (
        "My neighbour has applied for ten jobs since finishing college.", "我邻居大学毕业后已经申请了十份工作。",
        "So the job market is quite tough at the moment.", "所以目前就业市场确实很难。",
    ),
    83: (
        "Leo keeps leaving his violin at home on lesson days.", "利奥总是在上课那天把小提琴忘在家里。",
        "I'll remind him to pack it before breakfast tomorrow.", "我明天早餐前提醒他带上。",
    ),
    100: (
        "You've eaten three slices of cake already. Would you like another?", "你已经吃了三块蛋糕了，还要一块吗？",
        "No thanks—a treat is best enjoyed in moderation.", "不了，谢谢；甜点适量享用最好。",
    ),
    102: (
        "Grandpa can finally shower downstairs without using the steep stairs.", "爷爷终于可以不用爬陡楼梯，在楼下洗澡了。",
        "Installing that shower was a game changer for him.", "装上那个淋浴间对他来说改变太大了。",
    ),
    111: (
        "This photo shows you waiting beside a pay phone with your school bag.", "这张照片里你背着书包，站在公用电话旁等着。",
        "Back in the day, we had to queue to call home after school.", "以前放学后我们得排队打电话回家。",
    ),
    113: (
        "Mina finished the charity run much faster than anyone expected.", "米娜完成慈善跑的速度比大家预想的快得多。",
        "For context, she only began training six weeks ago.", "补充一下背景，她六周前才开始训练。",
    ),
    114: (
        "Your cousin is deciding whether to take a job in another country.", "你表姐正在考虑要不要去另一个国家工作。",
        "As far as freedom is concerned, she wants a place where she can travel easily on weekends.", "就自由度而言，她想去一个周末出行方便的地方。",
    ),
    121: (
        "I realised my passport was missing just before the airport bus arrived.", "机场巴士快到时，我发现护照不见了。",
        "At that point, I called the taxi driver who had dropped me off.", "那时候，我给送我来的出租车司机打了电话。",
    ),
    129: (
        "Can we cancel the picnic if the rain gets heavier?", "如果雨更大，我们能取消野餐吗？",
        "It depends on the circumstances; the children may still enjoy an indoor picnic.", "要看具体情况；孩子们也许还是会喜欢室内野餐。",
    ),
    133: (
        "My brother lost his tablet for a week after ignoring his chores.", "我弟弟没做家务后，一个星期都不能用平板。",
        "Taking away screen time was a common discipline tactic in our house.", "在我们家，没收屏幕时间是常见的管教方式。",
    ),
    240: (
        "Which building are we meeting outside after the concert?", "音乐会结束后，我们在哪栋楼外面见面？",
        "This is the house with the blue door and the lemon tree.", "就是这栋有蓝色门和柠檬树的房子。",
    ),
    249: (
        "Why do you always drink mint tea after a heavy meal?", "为什么你每次吃完大餐都喝薄荷茶？",
        "It settles my digestion after spicy food.", "吃辣以后，它能让我的消化舒服些。",
    ),
    255: (
        "Nora's text sounds polite, but she used a full stop after every word.", "诺拉的短信看起来客气，但每个词后面都用了句号。",
        "There is a slight nuance in her tone that makes her sound annoyed.", "她的语气里有一点细微差别，让她听起来像在生气。",
    ),
    264: (
        "Where shall we eat our sandwiches before the museum opens?", "博物馆开门前，我们去哪里吃三明治？",
        "The bench beside the fountain is my favourite lunch spot.", "喷泉旁的长椅是我最喜欢的午餐地点。",
    ),
    290: (
        "Why are you carrying such a large camera bag on the hike?", "你徒步时为什么背这么大的相机包？",
        "That lens is so big that it needs its own padded case.", "那个镜头太大了，得单独放在带衬垫的包里。",
    ),
    295: (
        "The coach watched our first practice and pointed at the slow warm-up.", "教练看了我们的第一次训练，指着慢吞吞的热身。",
        "But you guys are gonna step those up before the tournament.", "不过你们要在比赛前把那些训练加强起来。",
    ),
    296: (
        "Why can't Jin join us for the beach trip this month?", "金为什么这个月不能和我们去海边？",
        "My friend is doing military service in Singapore until December.", "我朋友在新加坡服兵役，要到十二月。",
    ),
    305: (
        "Maya's parents let her stay out late after the school play.", "玛雅的父母允许她看完学校演出后很晚才回家。",
        "They are fairly permissive about weekend curfews.", "他们对周末宵禁比较宽松。",
    ),
    309: (
        "The school used to ban phones completely, but now everyone checks one in class.", "学校以前完全禁止手机，但现在每个人都在课堂上看手机。",
        "The pendulum has swung too far in the other direction.", "这种做法已经从一个极端摆到另一个极端了。",
    ),
    391: (
        "The tutor drew a sample question on the whiteboard after our practice test.", "模拟考后，辅导老师在白板上写了一道示例题。",
        "And this is what the exam tests you on.", "而这正是考试要考你的内容。",
    ),
    396: (
        "Can I join the advanced baking class without taking the beginners' course?", "我没上过初级课，可以参加高级烘焙课吗？",
        "Basic knife skills are a prerequisite for that class.", "基本刀工是那门课的先修条件。",
    ),
    405: (
        "You look tired after your first week at the childcare centre.", "你在托儿中心上完第一周班，看起来很累。",
        "Looking after three toddlers all day is demanding, but I love it.", "一整天照顾三个幼儿很辛苦，不过我喜欢这份工作。",
    ),
    428: (
        "Can we add another bedroom to this tiny old cottage?", "我们能在这栋很小的老房子里再加一间卧室吗？",
        "The building has inherent limits because the walls are protected.", "因为墙体受保护，这栋房子有其固有的限制。",
    ),
    432: (
        "Why did you bring pastries for everyone this morning?", "你今天早上为什么给大家带了糕点？",
        "My manager gave me a small bonus for covering the weekend shift.", "经理因为我代班周末，给了我一笔小奖金。",
    ),
    438: (
        "Why did all the shopping lists stick to the fridge door?", "为什么所有购物清单都吸在冰箱门上？",
        "The door is magnetic, so the clips hold the paper there.", "门有磁性，所以夹子能把纸固定住。",
    ),
    450: (
        "The bakery sold out of rolls before lunchtime again.", "面包店午饭前又把小圆面包卖光了。",
        "The new oven has doubled the bakery's throughput.", "新烤箱让面包店的产量翻了一倍。",
    ),
    451: (
        "Did you find parking near the stadium before the match?", "比赛前，你在体育场附近找到停车位了吗？",
        "No, spaces there are hard to come by on game days.", "没有，比赛日那里很难找到车位。",
    ),
    452: (
        "You have spent every Sunday restoring that old garden gate.", "你每个星期天都在修复那扇旧花园门。",
        "It is a labor of love because it belonged to my grandmother.", "这是出于爱做的事，因为它属于我奶奶。",
    ),
    455: (
        "My back hurts after an hour at the kitchen table.", "我在餐桌前坐一小时，背就疼。",
        "Try this chair; it has proper lumbar support.", "试试这把椅子；它有合适的腰部支撑。",
    ),
    467: (
        "The community centre has no ramp at its front entrance.", "社区中心正门没有坡道。",
        "A ramp is really needed for parents with prams and wheelchair users.", "带婴儿车的家长和轮椅使用者确实需要一个坡道。",
    ),
    477: (
        "Owen copied his friend's answers during the science quiz.", "欧文在科学小测时抄了朋友的答案。",
        "He could fail the course if he keeps trying to cheat on tests.", "如果他继续在考试中作弊，可能会挂科。",
    ),
    482: (
        "Ben threw the board game pieces because he lost one round.", "本因为输了一轮，就把桌游棋子扔了。",
        "That was a childish reaction, even for a ten-year-old.", "那种反应太幼稚了，即使对十岁孩子来说也是。",
    ),
    483: (
        "Why don't you replace that old toaster? It barely pops up anymore.", "你为什么不换掉那台旧烤面包机？它都快弹不起来了。",
        "This toaster has sentimental value because it was my mum's first gift to me.", "这台烤面包机有纪念意义，因为它是妈妈送我的第一件礼物。",
    ),
    509: (
        "I can barely see the butterfly against the wall in this photo.", "这张照片里，我几乎看不见墙边的蝴蝶。",
        "It is similar to the background, so the camera missed it too.", "它和背景很相似，所以相机也没拍清楚。",
    ),
    520: (
        "Should we each drive separately to the hiking trail?", "我们要不要各自开车去徒步路线？",
        "That would defeat the purpose of carpooling.", "那样就失去拼车的意义了。",
    ),
    522: (
        "Does every paperback on this table cost five dollars?", "这张桌上的每本平装书都卖五美元吗？",
        "Yes, with one qualifier: the new releases are not included.", "是的，不过有一个限定：新书不包括在内。",
    ),
    523: (
        "The rain washed out our picnic just as everyone arrived.", "大家刚到，大雨就把野餐搅黄了。",
        "That's a bummer, but we can move the food into the hall.", "真扫兴，不过我们可以把食物搬进大厅。",
    ),
    528: (
        "Why did you pack a tiny torch for a daytime camping trip?", "白天露营，你为什么带了一支小手电？",
        "It is very handy when we look for things in the tent after dark.", "天黑后在帐篷里找东西时，它很有用。",
    ),
    540: (
        "Can you hear the clock ticking from the other end of the room?", "你在房间另一头能听到钟表滴答声吗？",
        "Only just—the sound is almost imperceptible from here.", "勉强能听到——从这里听，声音几乎察觉不到。",
    ),
    553: (
        "The label on your jumper is showing at the front.", "你毛衣的标签露在前面了。",
        "Oh no, I put it on inside out this morning.", "糟了，我今天早上穿反了。",
    ),
    565: (
        "The burnt cheese is stuck to the bottom of the baking dish.", "焦掉的奶酪粘在烤盘底部了。",
        "Fill it with warm water and let it soak while we eat.", "装上温水，吃饭时让它泡一会儿。",
    ),
    596: (
        "I waved at a stranger in the supermarket because I thought she was my aunt.", "我在超市向一个陌生人挥手，因为我以为她是我姨妈。",
        "That must have been awkward.", "那一定很尴尬。",
    ),
    606: (
        "I sent the birthday invitation to the person whose party it was.", "我把生日邀请发给了过生日的那个人本人。",
        "That was awkward, but at least the surprise was small.", "那很尴尬，不过至少这个惊喜不算大。",
    ),
    613: (
        "Naomi failed her driving test but booked another lesson on the way home.", "娜奥米驾照考试没通过，但回家路上就预约了下一节课。",
        "That is exactly the spark of a growth mindset.", "这正是成长型思维的火花。",
    ),
    614: (
        "You found Mia's lost wallet after promising to help her look for it.", "你答应帮米娅找钱包后，真的找到了。",
        "For me, handing it back is about honouring that promise as the only way forward.", "对我来说，把它还回去是为了履行那个承诺，也是唯一该做的事。",
    ),
})


CURATED_REAL_LIFE_SCENES.update({
    617: (
        "The first two loaves of sourdough collapsed in the oven.", "前两条酸面包在烤箱里塌掉了。",
        "Learning sourdough has been trial and error, but this loaf finally rose.", "学做酸面包一直是不断尝试和犯错，不过这条终于发起来了。",
    ),
    624: (
        "We left for the cinema ten minutes after the film had started.", "电影开始十分钟后我们才出发去电影院。",
        "Missing the opening scene was the inevitable result of leaving so late.", "这么晚才出发，错过开场是不可避免的结果。",
    ),
    639: (
        "We are halfway up the hill and the wind is getting stronger.", "我们已经爬到半山腰，风越来越大。",
        "The trail is steep, but we can push through it after a short break.", "路很陡，但短暂休息后我们能坚持走完。",
    ),
    642: (
        "Mia almost skipped piano practice so she could watch another episode.", "米娅差点为了再看一集电视剧而不练钢琴。",
        "Practising tonight is one way to cast a vote for the person you want to become.", "今晚练琴，就是在为你想成为的那个人投一票。",
    ),
    646: (
        "The rail crew has been working beside the station since sunrise.", "铁路工人从日出起就在车站旁施工。",
        "The tracks are laid down one metre at a time so each section stays level.", "铁轨是一米一米铺设的，这样每一段才能保持平整。",
    ),
    647: (
        "I want to save enough for a weekend away by spring.", "我想在春天前存够钱去度个周末。",
        "Putting twenty dollars aside every Friday will make the result inevitable.", "每周五存二十美元，会让这个结果水到渠成。",
    ),
    648: (
        "I thought asking for help meant I had failed.", "我原来以为求助就代表我失败了。",
        "That is a big shift in how I see things after talking with my sister.", "和姐姐谈过后，我看事情的方式有了很大改变。",
    ),
    655: (
        "We have stood in the paint aisle for twenty minutes choosing between two blues.", "我们在油漆区两种蓝色之间纠结了二十分钟。",
        "Setting a five-minute timer is a simple way to bypass overthinking.", "设个五分钟计时器，是绕开过度思考的简单方法。",
    ),
    662: (
        "Sam is rewriting a birthday card because the first version sounds too formal.", "萨姆正在重写生日卡片，因为第一版听起来太正式。",
        "‘I'm thinking of you’ is another way of saying ‘I miss you’ without sounding heavy.", "“我在想你”是表达“我想你”的另一种说法，听起来没那么沉重。",
    ),
    666: (
        "We both want to keep walking after dinner instead of doing it for one week.", "我们都想饭后一直散步，而不是只坚持一个星期。",
        "By making it part of dinner, we can make these changes stick for life.", "把它变成晚饭的一部分，我们就能让这些改变长期坚持下去。",
    ),
    671: (
        "After the habit workshop, Leila still skips her evening walk whenever it rains.", "习惯工作坊后，蕾拉一到下雨天还是会不去晚间散步。",
        "Which of the six strategies do you think is her missing piece?", "你觉得六种策略中，哪一种是她缺失的关键？",
    ),
    673: (
        "The sink overflowed while the children were making paper boats.", "孩子们折纸船时，水槽溢出来了。",
        "Calling this kitchen a mess is an understatement.", "说这个厨房乱简直太轻描淡写了。",
    ),
    675: (
        "Ned posted one photo of himself cleaning the beach, then left before the work began.", "内德发了一张自己清理海滩的照片，真正开始干活前就走了。",
        "It felt performative rather than helpful.", "这感觉更像是在表演，而不是真的帮忙。",
    ),
    676: (
        "I only meant to bake one batch of cookies for the fundraiser.", "我本来只想为筹款活动烤一批饼干。",
        "Then I got into the whole thing—matching napkins, signs, and a playlist.", "后来我整套都搞起来了——配套餐巾、标牌和播放列表。",
    ),
    682: (
        "My sister is choosing between two job offers after graduation.", "我姐姐毕业后要在两份工作之间做选择。",
        "She wants a company that values teamwork and gives people opportunities to grow.", "她想去一家重视团队合作、也给员工成长机会的公司。",
    ),
    685: (
        "The laundry basket is overflowing and I do not know where to start.", "洗衣篮已经满出来了，我不知道从哪里开始。",
        "Don't let the pile overwhelm you; start with the towels.", "别让这一堆衣服压垮你；先从毛巾开始。",
    ),
    688: (
        "We arrived at the night market just as the lights came on.", "夜市刚亮灯时，我们就到了。",
        "The crowd at opening time was overwhelming, so we found a quieter street.", "刚开市时人群多得让人招架不住，所以我们找了条安静的街。",
    ),
    689: (
        "Can we print the poster for the school hallway this afternoon?", "我们今天下午能把学校走廊的海报打印出来吗？",
        "Yes, after I make the growth mindset wording corrections.", "可以，等我把成长型思维那部分的措辞改好。",
    ),
    691: (
        "He promised to feed the cat, then forgot for the third time this week.", "他答应喂猫，但这周已经第三次忘了。",
        "After all those broken promises, nothing he says counts with his sister.", "这么多承诺落空后，他姐姐已经不信他说的话了。",
    ),
    693: (
        "I study English for four hours on Sunday but rarely speak during the week.", "我周日学四小时英语，但平时很少开口。",
        "Your tutor is right: the key to learning English is practising consistently.", "你的老师说得对：学英语的关键是持续练习。",
    ),
    703: (
        "Mum booked one quiet hour at the pool after caring for everyone all week.", "妈妈照顾大家一周后，给自己订了一小时的游泳时间。",
        "Taking that hour for herself is not an act of selfishness.", "为自己留出这一小时并不是自私。",
    ),
    705: (
        "I did not want to pay for travel insurance for our short trip.", "我本来不想为短途旅行买保险。",
        "When you put it that way, one lost suitcase would cost much more.", "你这么一说，丢一个行李箱的损失会大得多。",
    ),
    718: (
        "The vase looks perfect until you turn it toward the window.", "这个花瓶看起来很完美，直到你把它转向窗边。",
        "There is a tiny flaw in the glaze near the base.", "底部附近的釉面有一个小瑕疵。",
    ),
    752: (
        "My birthday parcel went to an office across town instead of our flat.", "我的生日包裹没有送到公寓，却送到了城另一头的办公室。",
        "It was misdirected because the courier read the street number wrong.", "快递员看错了门牌号，所以把它送错地方了。",
    ),
    760: (
        "Lily still misses her dog months after he died.", "莉莉的狗去世几个月了，她还是很想它。",
        "Losing a pet hurts; it takes time to heal.", "失去宠物会很痛苦，需要时间慢慢疗愈。",
    ),
    763: (
        "How are we going to fit that suitcase into the small car?", "这么大的行李箱怎么放进这辆小车？",
        "It is massive; we may need to put it on the back seat.", "它太大了；我们可能得放到后座。",
    ),
    767: (
        "Should we put our picnic blanket beside the lake or under those trees?", "我们把野餐垫铺在湖边，还是铺在那几棵树下？",
        "Let's sit under the trees; it is too sunny here.", "我们坐树下吧；这里太阳太晒了。",
    ),
    782: (
        "Did the photo from the lookout turn out well?", "观景台拍的照片效果好吗？",
        "Not really—the photo is blurry because my hands were cold.", "不太好——我的手冻僵了，照片拍糊了。",
    ),
    1003: (
        "Did Uncle Ray say whether he could collect us from the station?", "雷叔叔说过能不能来车站接我们吗？",
        "Now that I think of it, he did mention he would be there at six.", "现在想起来，他确实说过六点会到。",
    ),
    1018: (
        "Why are you taking on extra shifts at the café this term?", "这个学期你为什么在咖啡馆多上班？",
        "The tuition is expensive, so I am saving for next semester.", "学费很贵，所以我在为下学期存钱。",
    ),
    1024: (
        "We toured a house with a bathroom bigger than our whole flat.", "我们看了一套房，它的浴室比我们整套公寓还大。",
        "That multi-million-dollar mansion has a dual vanity, but its price is ridiculous.", "那栋价值数百万美元的豪宅有双洗手台，不过价格太离谱了。",
    ),
    1031: (
        "My nephew stayed up scrolling videos and could barely wake for school.", "我侄子刷视频到很晚，早上几乎起不来上学。",
        "We should talk about the negative impact of technology on his sleep.", "我们该谈谈科技产品对他睡眠的负面影响。",
    ),
    1048: (
        "The fruit stall at the market has the same peaches as the supermarket.", "市场里的水果摊卖的桃子和超市一样。",
        "This stall is two bucks less for a whole bag.", "这个摊子一整袋便宜两美元。",
    ),
    1069: (
        "How are the dumplings from the new stall?", "新摊位的饺子怎么样？",
        "They are scrumptious—let's get another plate to share.", "非常好吃——我们再点一盘一起吃吧。",
    ),
    1075: (
        "Your client is worried because the haircut looks shorter while it is still wet.", "你的顾客担心头发湿着时看起来剪得太短。",
        "Stay calm and stick with your client until she sees it dry.", "保持冷静，陪着你的顾客等她看到头发干后的效果。",
    ),
    1084: (
        "Have you ever seen the northern lights outside the city?", "你在城外见过北极光吗？",
        "Seeing them dance across the sky would blow my mind.", "看着它们在天空中舞动会让我震撼不已。",
    ),
    1091: (
        "Your message said 'fine' but it sounded cold when you read it aloud.", "你的信息写着“好”，但你读出来时听起来很冷淡。",
        "It was my tone of voice; I was tired, not angry.", "是我的语气问题；我只是累了，不是生气。",
    ),
    1105: (
        "Why is the cloud-service bill so high after the weekend?", "周末过后，为什么云服务账单这么高？",
        "The test accidentally started a fleet of Amazon EC2 instances overnight.", "测试意外地一夜之间启动了一大批 Amazon EC2 实例。",
    ),
    1106: (
        "My twins think borrowing a library book and renting a movie are the same thing.", "我的双胞胎觉得借图书馆的书和租电影是一回事。",
        "They are fundamentally different concepts, so I explained the return rules.", "它们是根本不同的概念，所以我解释了归还规则。",
    ),
    1107: (
        "Are we definitely having the concert in the park tomorrow?", "我们明天一定会在公园办音乐会吗？",
        "The outdoor concert is subject to cancellation if the storm arrives.", "如果暴风雨来了，户外音乐会可能会取消。",
    ),
    1119: (
        "You like the green paint, and I like the blue paint for the bedroom.", "你喜欢用绿色油漆，我喜欢卧室用蓝色。",
        "Which one looks nicer is not objective reality; it is personal taste.", "哪种更好看不是客观现实，而是个人喜好。",
    ),
    1125: (
        "The school moved pickup time half an hour earlier without asking families.", "学校没有征求家长意见，就把接孩子的时间提前了半小时。",
        "From a parent's perspective, that makes an already busy afternoon harder.", "从家长的角度看，这让本来就忙的下午更难安排。",
    ),
    1135: (
        "Should the club order more vegetarian meals for next month's picnic?", "社团下个月野餐要不要多订些素食？",
        "The survey statistics show that half the members prefer them.", "调查统计显示，一半会员更喜欢素食。",
    ),
    1145: (
        "The globe in the museum looks slightly squashed at the poles.", "博物馆里的地球仪两极看起来有点扁。",
        "Our guide said the Earth is closer to an ellipsoid than a perfect sphere.", "导游说，地球更接近椭球体，而不是完美的球体。",
    ),
    1146: (
        "The theatre website shows rows A to D still available.", "剧院网站显示 A 到 D 排还有座位。",
        "Do not assume the seats are together until you open the seating plan.", "在打开座位图前，别以为这些座位是连在一起的。",
    ),
    1147: (
        "Is the walk to the waterfall suitable for Grandma?", "去瀑布的路适合奶奶走吗？",
        "The terrain is rocky near the top, so she may prefer the lower track.", "靠近山顶的地形很崎岖，她可能更适合走下面那条路。",
    ),
    1148: (
        "The community garden collected donations but no one knew who could approve a purchase.", "社区花园收到了捐款，但没人知道谁能批准采购。",
        "We need simple governance so everyone knows who makes each decision.", "我们需要简单的治理规则，让每个人都清楚由谁做决定。",
    ),
    1153: (
        "The ranger asked us to keep away from the nesting birds near the beach.", "护林员让我们远离海滩边筑巢的鸟。",
        "We can walk along the coast, but not down onto the shore today.", "我们今天可以沿着海岸走，但不能下到海滩上。",
    ),
    1155: (
        "Did you like the lemon cake I made for the picnic?", "你喜欢我为野餐做的柠檬蛋糕吗？",
        "It is good, just overly sweet for me.", "很好，只是对我来说有点太甜。",
    ),
    1163: (
        "My shoulder still hurts after I fell off the bike.", "我从自行车上摔下来后，肩膀还是疼。",
        "The practitioner at the clinic can show you some safe stretches.", "诊所的专业人员可以教你一些安全的拉伸动作。",
    ),
    1168: (
        "We opened the hall doors just before the school concert started.", "学校音乐会开始前，我们刚打开礼堂大门。",
        "Within minutes, the room was filled with parents and grandparents.", "几分钟后，房间里就坐满了家长和祖父母。",
    ),
    1178: (
        "The raffle host is about to announce the winner of the bicycle.", "抽奖主持人马上要公布自行车的中奖者。",
        "Give us a drumroll before you say the name!", "说名字前先来一段击鼓声吧！",
    ),
})


CURATED_REAL_LIFE_SCENES.update({
    1188: (
        "The school play and the basketball final both start at seven tonight.", "学校演出和篮球决赛今晚七点同时开始。",
        "They are simultaneous, so we will have to choose one.", "它们是同时进行的，所以我们得选一个。",
    ),
    1189: (
        "Why are you packing three shirts and your name badge?", "你为什么收拾了三件衬衫和名牌？",
        "I'm taking the train to a conference in Wellington tomorrow.", "我明天要坐火车去惠灵顿参加一个会议。",
    ),
    1198: (
        "The restaurant brought tiny fried mushrooms before our mains arrived.", "主菜上来前，餐厅端来了一小盘炸蘑菇。",
        "Those are the appetizer; save room for the pasta.", "那是开胃菜；给意面留点肚子。",
    ),
    1201: (
        "Is the egg on your toast cooked the way you like it?", "吐司上的鸡蛋煮得合你口味吗？",
        "Yes, I like the yolk runny so it soaks into the bread.", "是的，我喜欢蛋黄流心，能浸到面包里。",
    ),
    1202: (
        "I added soy sauce twice because I forgot the first spoonful.", "我忘了第一次已经加过酱油，又加了一次。",
        "That explains why the noodles are overseasoned.", "这就解释了为什么面条调味太重。",
    ),
    1243: (
        "Can your cousin sleep over tonight after the birthday party?", "生日派对后你表姐能在这里过夜吗？",
        "Not until the spare room stops being covered with piles of clothes.", "等客房不再堆满衣服再说。",
    ),
    1244: (
        "What are you making with all those coloured threads?", "你用这些彩线在做什么？",
        "I'm doing cross-stitch for a bookmark for Grandma.", "我在十字绣一个书签送给奶奶。",
    ),
    1245: (
        "Why does Oliver carry a novel everywhere, even to the dentist?", "为什么奥利弗到哪里都带着小说，连去看牙医也带？",
        "He is a mystery-book addict and never wants to stop at one chapter.", "他是个推理小说迷，一章都舍不得停。",
    ),
    1258: (
        "That tune from the bakery advert has been in my head all morning.", "面包店广告里的那段旋律整个上午都在我脑子里转。",
        "It is so catchy that everyone at work is humming it.", "它太朗朗上口了，办公室每个人都在哼。",
    ),
    1264: (
        "We have twelve children for the treasure hunt but only three maps.", "寻宝游戏有十二个孩子，却只有三张地图。",
        "Let's split them up into three teams before we start.", "开始前我们把他们分成三队吧。",
    ),
    1268: (
        "Why did the old tree make that strange sound when you tapped it?", "你敲那棵老树时，为什么发出奇怪的声音？",
        "The trunk is hollow inside after years of rot.", "树干多年腐烂后，里面空了。",
    ),
    1275: (
        "The children saw a large reptile at the wildlife park and could not name it.", "孩子们在野生动物园看到一只大型爬行动物，却叫不出名字。",
        "The keeper said it was an alligator, not a crocodile.", "饲养员说那是短吻鳄，不是鳄鱼。",
    ),
    1278: (
        "Something green just jumped from the long grass onto my shoe.", "有个绿色的东西刚从长草里跳到我鞋上。",
        "Don't worry, it is only a grasshopper.", "别担心，只是一只蚱蜢。",
    ),
    1279: (
        "How can the town feed so many people at the winter festival?", "小镇冬季节怎么能给这么多人提供食物？",
        "They are cooking soup on a huge scale in the sports hall.", "他们在体育馆里大规模煮汤。",
    ),
    1296: (
        "Why are we stopping at this railing before the next part of the walk?", "走下一段路前，我们为什么要在这个栏杆前停下？",
        "The canyon is deep here, so the guide wants everyone together.", "这里峡谷很深，导游想让大家集中在一起。",
    ),
    1298: (
        "What did you find in the rock pool near the beach?", "你在海边岩石潮池附近发现了什么？",
        "This shell-shaped fossil is millions of years old.", "这个贝壳形状的化石有几百万年历史了。",
    ),
    1303: (
        "Are you really going to cross the valley on that cable?", "你真的要沿着那根缆绳穿过山谷吗？",
        "Yes, the zip line is part of the adventure course.", "是的，高空滑索是探险课程的一部分。",
    ),
    1306: (
        "Where was your favourite stop on the trip through the Caucasus?", "高加索之旅中，你最喜欢哪一站？",
        "Georgia was my favourite because of the food and mountain villages.", "我最喜欢格鲁吉亚，因为那里的食物和山村都很棒。",
    ),
    1309: (
        "Why is there a no-smoking sign beside the school gate?", "为什么学校门口有禁烟标志？",
        "It is part of the new anti-smoking campaign for families.", "它是面向家庭的新反吸烟宣传活动的一部分。",
    ),
    1332: (
        "Why does the lettuce leaf stay firm after we water the garden?", "我们浇完花园后，为什么生菜叶还是很挺？",
        "Its cell wall helps the plant keep its shape.", "它的细胞壁帮助植物保持形状。",
    ),
    1333: (
        "Is the sponge cake supposed to feel this light when you press it?", "海绵蛋糕按下去这么轻软是正常的吗？",
        "Yes, the texture is soft because we folded the eggs in gently.", "是的，口感松软，因为我们轻轻拌入了鸡蛋。",
    ),
    1339: (
        "How are the tomatoes doing after the cold week?", "冷了一周后，番茄长得怎么样？",
        "They are progressing well now that they get more sun.", "现在阳光更多了，它们长得很好。",
    ),
    1345: (
        "What do they make in the factory beside the railway line?", "铁路旁那家工厂生产什么？",
        "They manufacture reusable water bottles for local shops.", "他们为本地商店生产可重复使用的水瓶。",
    ),
    1346: (
        "Can our class raise enough money to repaint the playground by June?", "我们班能在六月前筹够钱重新粉刷操场吗？",
        "It is feasible if every family joins the Saturday bake sale.", "如果每个家庭都参加周六义卖，这是可行的。",
    ),
    1347: (
        "Which pastries should the bakery make more of next month?", "面包店下个月应该多做哪种糕点？",
        "The sales analytics show that the almond croissants sell out first.", "销售分析显示，杏仁可颂最先卖完。",
    ),
    1349: (
        "The café ran out of oat milk just as the morning queue formed.", "早晨排队刚开始，咖啡馆就没了燕麦奶。",
        "The manager chose a substitute on the spot instead of closing the machine.", "经理当场决定换一种替代品，而没有关掉机器。",
    ),
    1355: (
        "Would you wear those glittery shoes to a friend's backyard barbecue?", "你会穿那双亮片鞋去朋友家的后院烧烤吗？",
        "They are lovely, but not right for such a casual setting.", "它们很好看，但不适合这么休闲的场合。",
    ),
    1356: (
        "The council wants to remove the old trees to widen the road.", "市议会想砍掉老树来拓宽道路。",
        "It is a controversial plan, so the meeting will be crowded tonight.", "这是个有争议的计划，所以今晚会议人会很多。",
    ),
    1359: (
        "The children are clapping along to the new playground chant.", "孩子们正跟着新操场口号拍手。",
        "It has a strong rhythm, but the last words do not rhyme.", "它节奏很强，但最后几个词并不押韵。",
    ),
    1364: (
        "Has the soup cooled down enough for the children?", "汤凉到孩子们能喝了吗？",
        "It is somewhat cooler, but let it sit for another minute.", "是稍微凉了一些，但再放一分钟吧。",
    ),
    1365: (
        "Why did the price of coffee jump so much at the market?", "为什么市场上的咖啡价格涨了这么多？",
        "Coffee is a commodity, so harvest problems can affect its price quickly.", "咖啡是一种大宗商品，所以收成出问题会很快影响价格。",
    ),
    1380: (
        "Which poster should we put in the library window for the book sale?", "图书义卖的海报，我们该把哪一张贴在图书馆窗户上？",
        "Choose the blue one; it is more visually appealing from the street.", "选蓝色那张；从街上看它更吸引人。",
    ),
    1384: (
        "How do you know the basil plant needs water before its leaves droop?", "罗勒叶还没耷拉下来前，你怎么知道它缺水？",
        "Dry soil is usually a good indicator that it needs a drink.", "土壤干了通常是它需要浇水的一个好迹象。",
    ),
    1386: (
        "The projector froze just before the parents arrived for the slideshow.", "家长来观看幻灯片前，投影仪卡住了。",
        "Technology is not behaving this morning, so I'll print the photos instead.", "今天早上设备不太配合，我改为把照片打印出来。",
    ),
    1387: (
        "My alarm did not ring, and the bus timetable will not load either.", "我的闹钟没响，公交时刻表也加载不出来。",
        "Technology is not behaving this morning, but we can still walk to the stop.", "今天早上设备不太配合，不过我们还是可以走去车站。",
    ),
    1390: (
        "The children just tipped a whole bag of flour onto the kitchen floor.", "孩子们刚把一整袋面粉倒在厨房地板上。",
        "This is going to be a long afternoon if we start cleaning now.", "要是现在开始收拾，今天下午可有得忙了。",
    ),
    1391: (
        "Do I need a special tool to hang this picture frame?", "我需要特殊工具才能挂这幅画框吗？",
        "No, the instructions are straightforward: measure, drill, and hang it.", "不用，说明很直接：量尺寸、打孔、挂上去。",
    ),
    1392: (
        "Why is there a plastic cake on the table at the bakery display?", "面包店展示台上为什么有一个塑料蛋糕？",
        "It is a dummy cake for showing the design to customers.", "那是用来向顾客展示样式的仿真蛋糕。",
    ),
    1396: (
        "Why are you washing the red shirt separately from the white towels?", "你为什么把红衬衫和白毛巾分开洗？",
        "This setting is meant to protect the colours from running.", "这个设置是为了防止颜色串染。",
    ),
    1661: (
        "Why does this lunch box have a small rubber seal around the lid?", "这个午餐盒盖子周围为什么有一圈小橡胶密封条？",
        "It is designed to keep soup from leaking in your bag.", "它的设计是为了防止汤在包里漏出来。",
    ),
    1663: (
        "The forecast changed just before we packed for the beach picnic.", "我们正要收拾去海边野餐的东西，天气预报变了。",
        "If it rains, the hall booking will come into play.", "如果下雨，礼堂预订就会派上用场。",
    ),
    1666: (
        "The art class and the swimming lesson are both on Tuesday afternoon.", "美术课和游泳课都在周二下午。",
        "They overlap by half an hour, so I cannot take both children.", "它们有半小时重叠，所以我没法同时送两个孩子去。",
    ),
    1676: (
        "Why is the jewellery shop closed with police tape across the door?", "为什么珠宝店关门了，门上还拉着警戒线？",
        "There was a smash-and-grab last night, but nobody was hurt.", "昨晚发生了一起砸窗抢劫，不过没有人受伤。",
    ),
})


# A small number of source notes were split into several independent lessons.
# Their source ID alone is not enough to choose a scene: each entry below is
# keyed by ``(source item ID, normalised lesson expression)`` so a learner sees
# an event that actually uses the expression on that particular card.
CURATED_REAL_LIFE_EXPRESSION_SCENES = {
    (596, "clumsy"): (
        "I knocked over a stack of paper cups while trying to carry three drinks.", "我想一次拿三杯饮料时，把一摞纸杯撞倒了。",
        "That was clumsy, but at least nobody got wet.", "那确实有点笨拙，不过至少没人被弄湿。",
    ),
    (596, "monument"): (
        "What is that tall stone structure beside the river?", "河边那座高高的石头建筑是什么？",
        "It is a monument to the people who built the old bridge.", "那是一座纪念修建老桥的人们的纪念碑。",
    ),
    (568, "leftovers"): (
        "Should we throw away the pasta from last night's dinner?", "我们要把昨晚剩下的意面扔掉吗？",
        "No, put the leftovers in a container for tomorrow's lunch.", "不用，把剩菜装进盒子，明天午饭吃。",
    ),
    (973, "chubby"): (
        "Has your cat always been this round?", "你的猫一直这么圆吗？",
        "She has become a little chubby since Grandma started giving her treats.", "奶奶开始喂零食后，她变得有点胖乎乎的。",
    ),
    (1017, "headquarters"): (
        "Where should we meet before the neighbourhood clean-up begins?", "社区清洁活动开始前，我们在哪里集合？",
        "The old library is our volunteer group's headquarters today.", "旧图书馆今天是我们志愿者小组的大本营。",
    ),
    (1017, "suspect"): (
        "Who keeps taking the biscuits from the jar before dinner?", "晚饭前总是谁把罐子里的饼干拿走？",
        "Your little brother is the main suspect because of the crumbs on his shirt.", "你弟弟是头号嫌疑人，因为他衬衫上有饼干屑。",
    ),
    (1018, "finals"): (
        "Can you help us decorate for the party next weekend?", "下周末你能帮我们布置派对吗？",
        "I wish I could, but my finals start on Monday.", "我真想去，不过我的期末考试周一就开始了。",
    ),
    (1018, "major in"): (
        "What subject did you choose after visiting the marine centre?", "参观海洋中心后，你选了什么专业？",
        "I decided to major in marine biology.", "我决定主修海洋生物学。",
    ),
    (1018, "gory details"): (
        "How did your cousin hurt his knee at the skate park?", "你表弟在滑板公园怎么伤到膝盖的？",
        "He fell badly, but you do not need the gory details before lunch.", "他摔得很厉害，不过午饭前你不用听那些血腥细节。",
    ),
    (752, "misinformed"): (
        "Why did you come to the restaurant at six when the booking is for seven?", "预订是七点，你为什么六点就到餐厅了？",
        "I was misinformed about the time by the group chat.", "群聊里给我的时间信息不对。",
    ),
    (617, "messed up"): (
        "The cake came out flat after I forgot the baking powder.", "我忘了放泡打粉，蛋糕烤出来扁扁的。",
        "I messed up the recipe, so let's turn it into a trifle.", "我把食谱搞砸了，我们把它做成水果奶油甜点吧。",
    ),
    (617, "stuffed it up"): (
        "Did you manage to book the campsite for the long weekend?", "你订到长周末的露营地了吗？",
        "No, I stuffed it up and chose the wrong month on the form.", "没有，我搞砸了，表格上选错了月份。",
    ),
    (617, "born under a lucky star"): (
        "Mia found the last free seat on the packed train just before the doors closed.", "车门快关时，米娅在挤满人的火车上找到了最后一个空位。",
        "She must have been born under a lucky star.", "她一定是天生好运。",
    ),
    (245, "abbreviate"): (
        "The form has room for only a short title before the name.", "表格里姓名前只有很短的位置。",
        "We can abbreviate Doctor to Dr. to make it fit.", "我们可以把 Doctor 缩写成 Dr.，这样就放得下。",
    ),
    (245, "abbreviated"): (
        "Why does the name badge say 'Dr.' instead of the full title?", "为什么名牌上写的是“Dr.”，不是完整头衔？",
        "The title is abbreviated so it fits above the photo.", "头衔被缩写了，这样才能放在照片上方。",
    ),
    (1024, "pantry"): (
        "Where did the agent say the extra shelves were during the house tour?", "看房时，中介说额外的架子在哪里？",
        "The pantry is behind that narrow door beside the kitchen.", "储藏室就在厨房旁那扇窄门后面。",
    ),
    (1024, "gorgeous"): (
        "Did you like the house with the big windows by the garden?", "你喜欢花园边那套有大窗户的房子吗？",
        "The morning light in the living room was gorgeous.", "客厅的晨光美极了。",
    ),
    (1518, "an avalanche of sth"): (
        "The school sent one message about the concert date changing.", "学校发了一条消息，说音乐会日期变了。",
        "Within an hour, we received an avalanche of emails from worried parents.", "不到一小时，我们就收到了家长们雪片般的邮件。",
    ),
    (1521, "alongside"): (
        "Where should we put the two stalls at the community market?", "社区市集的两个摊位该放在哪里？",
        "Put the flower stall alongside the honey stall near the entrance.", "把鲜花摊放在入口附近蜂蜜摊的旁边。",
    ),
    (1529, "surge back"): (
        "The café was empty while the road outside was closed for repairs.", "外面的路维修封闭时，咖啡馆一直空着。",
        "Customers surged back as soon as the street reopened.", "街道一开放，顾客就一下子回来了。",
    ),
    (1536, "within sight"): (
        "We have been walking uphill for two hours and everyone is tired.", "我们已经上坡走了两个小时，大家都很累。",
        "Keep going—the lookout is finally within sight.", "继续走——观景台终于近在眼前了。",
    ),
    (1564, "point a finger at"): (
        "The picnic food went missing before anyone had arrived.", "大家还没到，野餐食物就不见了。",
        "Don't point a finger at Noah until we check the storage room.", "在查看储藏室前，别急着指责诺亚。",
    ),
    (1616, "conduct vs perform"): (
        "The school fair needs both a survey and a music show.", "学校义卖会既要做调查，也要办音乐演出。",
        "The students will conduct the survey while the band performs on stage.", "学生们负责开展调查，乐队则在台上表演。",
    ),
    (1620, "initially"): (
        "Why did you bring two umbrellas when the morning looked clear?", "早上看起来很晴，你为什么带了两把伞？",
        "Initially, I thought we would walk home, but the forecast changed.", "起初我以为我们会走路回家，但天气预报变了。",
    ),
    (1628, "to have myself"): (
        "You have been helping everyone move furniture all weekend.", "你整个周末都在帮大家搬家具。",
        "After such a long week, I'm going to have myself a proper rest.", "忙了这么久后，我要好好休息一下。",
    ),
    (1635, "allegedly"): (
        "Why is the street outside the bakery blocked this morning?", "为什么今天早上面包店外的街道封了？",
        "Police say a driver allegedly damaged several parked cars overnight.", "警方说有名司机涉嫌在夜里撞坏了几辆停着的车。",
    ),
    (1636, "on one occasion"): (
        "Has your neighbour ever helped you when the shop was closed?", "商店关门时，你邻居帮过你吗？",
        "On one occasion, she drove across town to bring me medicine.", "有一次，她开车穿过整个城市给我送药。",
    ),
    (1417, "subsequently"): (
        "Rosa started as a shop assistant five years ago.", "罗莎五年前从店员做起。",
        "She trained new staff and subsequently became the store manager.", "她培训新员工，后来成了店长。",
    ),
    (1449, "break apart"): (
        "The clouds have covered the beach since breakfast.", "从早餐后开始，云就一直盖住海滩。",
        "They should break apart later, so we can still go for a walk.", "晚些时候云层应该会散开，我们还是可以去散步。",
    ),
    (1468, "aid"): (
        "The storm flooded several homes at the edge of town.", "暴风雨淹了城边的几户人家。",
        "The community centre is collecting aid for the families tonight.", "社区中心今晚正在为这些家庭募集援助物资。",
    ),
    (1479, "electrified"): (
        "The home team scored in the final minute of the match.", "主队在比赛最后一分钟进球了。",
        "The stadium was electrified, and strangers were hugging each other.", "整个体育场沸腾了，陌生人都在互相拥抱。",
    ),
    (819, "decease"): (
        "The family is meeting the solicitor to settle Grandma's papers.", "家人正和律师见面，处理奶奶留下的文件。",
        "The house was transferred to her children after her decease.", "她去世后，这栋房子转给了她的孩子们。",
    ),
    (820, "be appointed liquidator"): (
        "The old department store closed suddenly and left many bills unpaid.", "那家老百货店突然关门，还留下许多未付账单。",
        "A lawyer was appointed liquidator to handle the remaining assets.", "一名律师被任命为清算人，处理剩余资产。",
    ),
    (843, "sharemarket"): (
        "My uncle checked his retirement account after hearing the morning news.", "我叔叔听完早间新闻后查看了退休账户。",
        "The sharemarket fell sharply after the announcement.", "公告发布后，股市大幅下跌。",
    ),
    (461, "every now and then"): (
        "Do you still hike even though you moved closer to the city?", "你搬到离市区更近的地方后，还去徒步吗？",
        "Yes, I go to the hills every now and then when I need fresh air.", "去啊，我偶尔会去山里呼吸新鲜空气。",
    ),
    (478, "conquer"): (
        "The children have been trying to reach the top of the climbing wall all term.", "孩子们整个学期都在尝试爬到攀岩墙顶端。",
        "Luca finally conquered the hardest route today.", "卢卡今天终于征服了最难的路线。",
    ),
    (696, "back then"): (
        "This old photo shows the street before the new library was built.", "这张老照片拍的是新图书馆建成前的街道。",
        "Back then, there was only a small grocery shop on this corner.", "那时候，这个街角只有一家小杂货店。",
    ),
    (105, "tragic"): (
        "The town put flowers outside the theatre after the bus crash.", "公交事故后，小镇的人在剧院外放了鲜花。",
        "It was a tragic accident that affected the whole community.", "那是一场影响整个社区的悲剧性事故。",
    ),
    (1167, "gigantic"): (
        "Why is everyone stopping outside the school hall?", "为什么大家都停在学校礼堂外？",
        "The children built a gigantic paper dinosaur for the science fair.", "孩子们为科学展做了一只巨大的纸恐龙。",
    ),
    (1228, "build up"): (
        "We should leave for the airport before the afternoon rush.", "我们该在下午高峰前出发去机场。",
        "Traffic will build up near the bridge after five o'clock.", "五点后桥边的车流会逐渐拥堵起来。",
    ),
    (1240, "fell dead on the spot"): (
        "We were watching an old detective film with a very dramatic final scene.", "我们在看一部结局非常戏剧化的老侦探电影。",
        "After the poison took effect, the actor fell dead on the spot.", "毒药发作后，演员当场倒地身亡。",
    ),
    (1246, "reluctant"): (
        "I did not want to speak first at the new book club.", "在新的读书会里，我一开始不想第一个发言。",
        "I felt reluctant at first, but the group was friendly.", "起初我有点不情愿，不过大家都很友好。",
    ),
    (1286, "tournament"): (
        "Why are the children wearing matching jerseys this Saturday?", "这个周六，孩子们为什么穿着一样的球衣？",
        "Their football tournament starts at nine in the park.", "他们的足球锦标赛九点在公园开始。",
    ),
    (1308, "put on bandages"): (
        "My nephew scraped his knee when he fell off his scooter.", "我侄子从滑板车上摔下来，擦破了膝盖。",
        "The nurse cleaned the cut and put on bandages.", "护士清理了伤口，然后包上绷带。",
    ),
    (1322, "intact"): (
        "We checked the old shed after the storm passed through the garden.", "暴风雨穿过花园后，我们检查了旧棚屋。",
        "The roof is still intact, so we only need to clear the leaves.", "屋顶仍然完好，所以我们只需要清理树叶。",
    ),
    (1327, "is set to be"): (
        "When will the town open the new swimming pool?", "小镇的新游泳池什么时候开放？",
        "It is set to be opened at the start of the summer holidays.", "它计划在暑假开始时开放。",
    ),
    (1377, "formalize that process"): (
        "New volunteers keep asking who can borrow the garden tools.", "新志愿者总在问谁可以借花园工具。",
        "Let's formalize that process with a simple sign-out sheet.", "我们用一张简单的借用登记表把流程正式化吧。",
    ),
    (1397, "evolve into"): (
        "We started with one table of donated books outside the library.", "我们一开始只是在图书馆外摆了一张捐书桌。",
        "It evolved into a monthly book swap for the whole neighbourhood.", "它后来发展成整个社区每月一次的换书活动。",
    ),
    (1402, "novelty"): (
        "The children begged to play with the new robot every day at first.", "孩子们一开始每天都吵着要玩新机器人。",
        "After a few weeks, the novelty wore off and it stayed on the shelf.", "几周后，新鲜感过去了，它就一直放在架子上。",
    ),
    (1161, "appear"): (
        "The rain stopped just as we reached the hill lookout.", "我们刚到山顶观景台，雨就停了。",
        "A rainbow began to appear over the hills.", "山丘上方开始出现一道彩虹。",
    ),
    (1580, "be done"): (
        "Can we leave the school project until the weekend?", "我们能把学校项目留到周末再做吗？",
        "No, the work needs to be done by Friday afternoon.", "不行，这项工作周五下午前必须完成。",
    ),
    (1482, "photovoltaic"): (
        "Why did the school install dark panels on the gym roof?", "为什么学校在体育馆屋顶装了深色面板？",
        "The photovoltaic panels generate electricity for the building.", "这些光伏板为大楼发电。",
    ),
    (813, "engage"): (
        "The children became restless during the long museum talk.", "博物馆讲解太长，孩子们开始坐不住了。",
        "The guide used a scavenger hunt to engage them in learning.", "导游用寻宝游戏吸引他们投入学习。",
    ),
    (868, "aspect"): (
        "The poster looks nearly ready for the school fair.", "学校义卖会的海报看起来快完成了。",
        "The lighting is one aspect we still need to improve.", "灯光是我们还需要改进的一个方面。",
    ),
    (623, "get out of the way"): (
        "The removal van has arrived and the movers are carrying the sofa upstairs.", "搬家车到了，搬运工正把沙发抬上楼。",
        "Let's get out of the way so they can use the narrow hallway.", "我们让开一点，好让他们通过狭窄的走廊。",
    ),
    (55, "basically"): (
        "The picnic plan has too many stops and nobody knows when to bring food.", "野餐计划安排了太多环节，没人知道什么时候带食物。",
        "Basically, the plan needs to be simplified before Saturday.", "简单说，周六前得把计划简化。",
    ),
    (222, "causal"): (
        "Our science project compares how much water two identical plants receive.", "我们的科学项目比较两盆相同植物得到的水量。",
        "That setup helps us examine the causal relationship between water and growth.", "这样的设计能帮助我们研究水量与生长之间的因果关系。",
    ),
    (287, "go around to primary schools"): (
        "What do you do when you are not presenting the weekend radio show?", "除了主持周末电台节目外，你平时做什么？",
        "I go around to primary schools to run short music workshops.", "我会去不同的小学开展短时音乐工作坊。",
    ),
    (1293, "dwell"): (
        "The guide pointed to a dark opening in the hillside during our walk.", "徒步时，导游指着山坡上的一个黑洞。",
        "People used to dwell in caves like that during the winter.", "以前人们冬天会住在那样的洞穴里。",
    ),
}


CURATED_REAL_LIFE_EXPRESSION_SCENES.update({
    (1642, "morning rush hour"): (
        "Why are you leaving for work before seven tomorrow?", "你明天为什么七点前就要去上班？",
        "I try to leave home before the morning rush hour begins.", "我尽量在早高峰开始前出门。",
    ),
    (1426, "organic"): (
        "Why are you choosing those carrots at the weekend market?", "你为什么在周末市场挑那些胡萝卜？",
        "They are organic, and the grower picked them this morning.", "它们是有机的，种植者今天早上刚采摘。",
    ),
    (371, "i wish that i could ... but ..."): (
        "We are leaving for the beach after lunch. Can you come with us?", "我们午饭后去海边，你能一起来吗？",
        "I wish that I could, but I promised to help my aunt move house.", "我真希望能去，但我答应了帮姨妈搬家。",
    ),
    (976, "beg to differ"): (
        "Tom says every pizza tastes the same once it has enough cheese.", "汤姆说披萨只要奶酪够多，味道都一样。",
        "I understand his point, but I beg to differ after trying that new place.", "我明白他的意思，不过吃过那家新店后，我不敢苟同。",
    ),
    (1001, "turn something over in your head"): (
        "You have been staring at the invitation since breakfast.", "从早餐起，你就一直盯着那张邀请函。",
        "I keep turning the decision over in my head before I reply.", "回复前，我一直在脑子里反复琢磨这个决定。",
    ),
    (890, "in ages"): (
        "Mia is coming to the reunion after living overseas for years.", "米娅在海外生活多年后，要来参加聚会。",
        "I haven't seen her in ages, so I can hardly wait.", "我好久没见她了，简直等不及。",
    ),
    (909, "spill"): (
        "Why is milk running across the kitchen bench?", "为什么牛奶正从厨房台面流下来？",
        "I spilled the carton while reaching for the cups.", "我伸手拿杯子时把整盒牛奶打翻了。",
    ),
    (727, "tear the place apart"): (
        "Have you found your passport for tomorrow's flight yet?", "你找到明天坐飞机要用的护照了吗？",
        "Not yet—I tore the place apart looking for it last night.", "还没有——我昨晚为了找它把家里翻了个遍。",
    ),
    (733, "particularly"): (
        "Which fruit should I put in the children's lunch boxes?", "我该把什么水果放进孩子们的午餐盒？",
        "They like fruit, particularly apples and grapes.", "他们喜欢水果，尤其是苹果和葡萄。",
    ),
    (734, "blow off steam"): (
        "That meeting ran for three hours and everyone looks tense.", "那场会议开了三小时，大家看起来都很紧绷。",
        "I'm going for a run to blow off steam before dinner.", "晚饭前我要去跑步发泄一下。",
    ),
    (785, "i've got two assignments because i'm studying two papers."): (
        "Why are your books spread across the whole dining table?", "为什么你的书铺满了整个餐桌？",
        "I've got two assignments because I'm studying two papers this term.", "我这个学期修两门课，所以有两份作业。",
    ),
    (402, "wander into"): (
        "How did you find that quiet garden behind the museum?", "你怎么找到博物馆后面那座安静花园的？",
        "I wandered into it while looking for a shortcut to the bus stop.", "我找去公交站的近路时，误打误撞走进去了。",
    ),
    (433, "thrill"): (
        "Did you enjoy the first drop on the roller coaster?", "你喜欢过山车第一次俯冲吗？",
        "I felt a real thrill when the carriage rushed over the top.", "车厢冲过顶端时，我感到一阵刺激。",
    ),
    (441, "miserable"): (
        "You went quiet after the argument with your brother.", "和弟弟吵架后，你一直很安静。",
        "I felt miserable all evening and wished I had spoken more kindly.", "我一晚上都很难受，希望当时说话能更温和些。",
    ),
    (454, "thrifty"): (
        "Why did you mend that jacket instead of buying another one?", "你为什么补那件夹克，而不买一件新的？",
        "I'm trying to be thrifty while I save for the trip.", "我想在为旅行存钱时节俭一点。",
    ),
    (473, "i told you i am a catch."): (
        "Your date said she was lucky to meet you after dinner.", "晚饭后，你的约会对象说认识你很幸运。",
        "I told you I am a catch, didn't I?", "我早就说过我很不错，对吧？",
    ),
    (474, "i get the feeling he was lying."): (
        "Did Ben really miss the train, or did he just not want to come?", "本是真的错过火车，还是只是不想来？",
        "I get the feeling he was lying about the train.", "我感觉他关于火车的说法是在撒谎。",
    ),
    (489, "i switch from line 7 to line 8."): (
        "Which train should we take after the art gallery closes?", "美术馆关门后，我们该坐哪趟火车？",
        "I switch from Line 7 to Line 8 at Central Station.", "我在中央车站从 7 号线换到 8 号线。",
    ),
    (580, "fancy"): (
        "The rain has stopped and the park is nearly empty.", "雨停了，公园里几乎没人。",
        "I fancy going for a walk before we cook dinner.", "我想在做晚饭前去散个步。",
    ),
    (643, "choose an apple over a cookie"): (
        "The café has fresh cookies beside the fruit bowl.", "咖啡馆的水果碗旁边摆着新鲜饼干。",
        "I'll choose an apple over a cookie today.", "今天我选苹果，不选饼干。",
    ),
    (680, "i kept the customer updated until they got their order."): (
        "The customer's coffee machine was delayed for two weeks.", "顾客的咖啡机延误了两周。",
        "I kept the customer updated until they got their order.", "直到顾客收到订单前，我一直向他更新进度。",
    ),
    (690, "a little spark of peace"): (
        "The house finally became quiet after the birthday guests left.", "生日客人离开后，家里终于安静下来。",
        "Sitting by the window gave me a little spark of peace.", "坐在窗边让我感到一点宁静。",
    ),
    (697, "look forward to"): (
        "Your sister arrives from Christchurch next Friday.", "你姐姐下周五从基督城来。",
        "I'm really looking forward to seeing her again.", "我非常期待再见到她。",
    ),
    (761, "run around"): (
        "You have been to the post office, supermarket, and school already today.", "你今天已经跑了邮局、超市和学校。",
        "I've been running around all day, so let's order dinner.", "我一整天都在奔波，我们点外卖吧。",
    ),
    (564, "in a row"): (
        "Why are you taking Friday off work?", "你为什么周五要请假？",
        "I've worked late three nights in a row and need an early evening.", "我已经连续三晚加班到很晚，需要早点回家。",
    ),
    (38, "i forget where he’s originally from. i forget what his background is."): (
        "The new neighbour mentioned growing up overseas, but I cannot remember where.", "新邻居提过自己在海外长大，但我想不起是哪里。",
        "I forget where he's originally from and what his background is.", "我忘了他原本来自哪里，也忘了他的背景。",
    ),
    (40, "give someone a tour of..."): (
        "Your cousin is visiting the university for the first time tomorrow.", "你表弟明天第一次来参观大学。",
        "I'll give him a tour of the campus before his interview.", "面试前我会带他参观校园。",
    ),
    (68, "i really put you to work."): (
        "You helped me carry boxes, hang lights, and wash dishes for the party.", "你帮我搬箱子、挂灯、洗派对的碗碟。",
        "I really put you to work today—thank you for staying so late.", "我今天真把你忙坏了——谢谢你待到这么晚。",
    ),
    (79, "i didn’t hear too much of our native language speaking through."): (
        "How did the new teacher sound during the English conversation club?", "英语会话俱乐部的新老师说话听起来怎么样？",
        "I didn't hear too much of our native language speaking through.", "我没太听出母语口音。",
    ),
    (223, "i just wanted to ask for permission before opening it."): (
        "Why did you leave the parcel by the door instead of opening it?", "你为什么把包裹放在门口，而没有打开？",
        "I just wanted to ask for permission before opening it.", "我只是想在打开前先征求许可。",
    ),
    (280, "i understand how challenging it can be to ..."): (
        "Maya is caring for her father while working full time.", "玛雅一边全职工作，一边照顾父亲。",
        "I understand how challenging it can be to carry both responsibilities.", "我理解同时承担这两份责任有多难。",
    ),
    (283, "what to focus on"): (
        "The assignment brief has five pages and the deadline is Friday.", "作业要求有五页，截止日期是周五。",
        "I don't know what to focus on first.", "我不知道该先关注什么。",
    ),
    (301, "i enjoy films that make you think."): (
        "Would you rather watch a comedy or the new mystery film tonight?", "今晚你想看喜剧，还是新出的悬疑片？",
        "Let's choose the mystery one; I enjoy films that make you think.", "选悬疑片吧；我喜欢让人思考的电影。",
    ),
    (303, "i believe in gentle parenting."): (
        "Your son knocked over the plant again. Are you going to shout?", "你儿子又撞倒花盆了，你会吼他吗？",
        "No, I believe in gentle parenting, even when I am frustrated.", "不会，即使我很烦，我也相信温和育儿。",
    ),
    (310, "all of that"): (
        "Do you remember the old flat, the noisy street, and our tiny balcony?", "你还记得那套旧公寓、吵闹的街道和小阳台吗？",
        "Yes, I remember all of that.", "记得，那些我都记得。",
    ),
    (1042, "sci-fi"): (
        "The cinema is showing a space adventure and a family comedy tonight.", "电影院今晚上映一部太空冒险片和一部家庭喜剧。",
        "Let's see the space one; I love sci-fi.", "我们看太空那部吧；我喜欢科幻。",
    ),
    (1051, "literal vs literally"): (
        "Your brother said he was 'literally starving' after football practice.", "你弟弟踢完球说自己“真的要饿死了”。",
        "He was not using literally in the literal sense.", "他并不是按字面意义使用 literally。",
    ),
    (1072, "side gig"): (
        "How are you saving for your camera without taking extra shifts at the café?", "你不在咖啡馆加班，怎么为相机存钱？",
        "I do graphic design as a side gig on weekends.", "我周末接平面设计的副业。",
    ),
    (1078, "i get the gist of it"): (
        "The museum guide spoke quickly, but you were nodding along.", "博物馆导游讲得很快，但你一直点头。",
        "I get the gist of it, even if I miss a few details.", "即使漏掉一些细节，我也能明白大意。",
    ),
    (1086, "out of the goodness of my heart"): (
        "Why did you spend your Saturday helping the elderly neighbour paint her fence?", "你为什么花周六帮年长邻居刷栅栏？",
        "I helped her out of the goodness of my heart.", "我是真心想帮她。",
    ),
    (1110, "intentionally"): (
        "The glass slipped from your hand while you were drying the dishes.", "你擦碗时，玻璃杯从手里滑掉了。",
        "I didn't break it intentionally—I was trying to catch it.", "我不是故意打碎它的——我当时正想接住。",
    ),
    (1116, "on a regular basis"): (
        "How often do you call your grandparents now that they live farther away?", "祖父母搬远后，你现在多久给他们打一次电话？",
        "I call them on a regular basis every Sunday evening.", "我每周日晚上都会定期给他们打电话。",
    ),
    (1128, "take all … into account"): (
        "The forecast, the children's ages, and the tide are all different this weekend.", "这个周末天气预报、孩子年龄和潮汐情况都不一样。",
        "We need to take all of that into account before choosing the beach.", "选海滩前，我们得把这些因素都考虑进去。",
    ),
    (1138, "probe information"): (
        "The journalist has three conflicting accounts of the neighbourhood meeting.", "记者拿到了三种相互矛盾的社区会议说法。",
        "She will probe the information before she publishes the story.", "她会在发表报道前仔细核实信息。",
    ),
    (1149, "take .... seriously"): (
        "The trail sign warns that loose rocks fall after heavy rain.", "步道标志警告说，大雨后会有落石。",
        "Let's take that warning seriously and use the lower path.", "我们认真对待这个警告，走下面那条路吧。",
    ),
    (1154, "come down the road"): (
        "Your contract ends in spring. Are you worried about finding work?", "你的合同春天结束，你担心找工作吗？",
        "No, I can see some good opportunities coming down the road.", "不，我能看到一些不错的机会正在出现。",
    ),
    (1179, "specialize"): (
        "What kind of repairs does your uncle do at his workshop?", "你叔叔的维修店主要修什么？",
        "He specializes in restoring old bicycles.", "他专门修复老式自行车。",
    ),
    (1185, "run into issues"): (
        "Did the projector work when you set up for the school talk?", "你为学校讲座做准备时，投影仪正常吗？",
        "We ran into issues with the cable, but the caretaker found a spare.", "我们遇到了线缆问题，不过管理员找到了备用的。",
    ),
    (1285, "withdrawal"): (
        "Why are you visiting the bank before your term deposit ends?", "为什么定期存款到期前你要去银行？",
        "I'd like to make an early withdrawal and ask about the interest.", "我想提前取款，并问问利息怎么算。",
    ),
    (1324, "specialize in"): (
        "Which class should I take if I want to learn bread making?", "如果我想学做面包，该上哪门课？",
        "Choose Mia's class; she specializes in sourdough.", "选米娅的课吧；她专门教酸面包。",
    ),
    (1331, "wonder"): (
        "The last bus has left, but Daniel still has not arrived at the café.", "末班车都走了，但丹尼尔还没到咖啡馆。",
        "I wonder where he went after work.", "我想知道他下班后去了哪里。",
    ),
    (1342, "at all"): (
        "Did you ever work for the company that sponsored the event?", "赞助这次活动的公司，你以前在那里工作过吗？",
        "No, I didn't work for them at all.", "没有，我根本没在他们那里工作过。",
    ),
    (1388, "comment on"): (
        "The reporter asked you about the neighbour's private family matter.", "记者问你邻居家的私事。",
        "I can't really comment on that at the moment.", "目前我不太方便评论那件事。",
    ),
    (312, "elated"): (
        "Your driving-test result just appeared on your phone.", "你的驾照考试结果刚出现在手机上。",
        "I felt elated when I saw that I had passed.", "看到自己通过了，我感到非常兴奋。",
    ),
    (530, "on occasion"): (
        "Do you ever order takeaway when you are too tired to cook?", "累得不想做饭时，你会点外卖吗？",
        "Yes, I eat fast food on occasion, but not every week.", "会，我偶尔吃快餐，但不是每周都吃。",
    ),
})


CURATED_REAL_LIFE_EXPRESSION_SCENES.update({
    (1546, "shoot back"): (
        "The children started a water fight in the garden after lunch.", "午饭后，孩子们在花园里打起了水仗。",
        "Mia shot back with the hose and soaked everyone.", "米娅拿水管反击，把大家都淋湿了。",
    ),
    (1587, "as in"): (
        "Dad asked whether the new suitcase was light enough to carry upstairs.", "爸爸问新行李箱够不够轻，能不能搬上楼。",
        "He meant light, as in not heavy.", "他说的是 light，指的是“不重”。",
    ),
    (1599, "get blamed for sth"): (
        "The dog knocked over the recycling bin while everyone was out.", "大家出门时，狗撞翻了回收箱。",
        "Ben always gets blamed for the mess because he is the youngest.", "因为本最小，他总是会为这类乱子背锅。",
    ),
    (1601, "upset victory"): (
        "The school team had never beaten the regional champions before.", "校队以前从没赢过地区冠军。",
        "They scored an upset victory in the final minute.", "他们在最后一分钟爆冷获胜。",
    ),
    (1603, "accuse sb of sth"): (
        "Someone ate the birthday cake before the guests arrived.", "客人到之前，有人把生日蛋糕吃掉了一块。",
        "Don't accuse Leo of taking it until we ask everyone.", "在问过所有人前，别指责利奥拿了它。",
    ),
    (1608, "overqualified"): (
        "Nora has managed a whole shop for ten years but applied for a junior role.", "诺拉管理过一家店十年，却申请了一个初级职位。",
        "She may be overqualified for that position, but she wants shorter hours.", "她对那个职位可能资历过高，但她想要更短的工时。",
    ),
    (1611, "barren desert"): (
        "Our guide stopped the bus at a viewpoint during the road trip.", "公路旅行时，导游让巴士停在一个观景点。",
        "Beyond the road was a vast barren desert with no trees at all.", "公路外是一望无际的荒漠，连一棵树都没有。",
    ),
    (1612, "keep a low profile"): (
        "After the noisy argument at the meeting, Kai did not want more attention.", "会议上激烈争吵后，凯不想再引人注意。",
        "He decided to keep a low profile for a few days.", "他决定低调几天。",
    ),
    (1621, "cause the number of to explode"): (
        "The library posted one photo of its new reading corner online.", "图书馆在网上发了一张新阅读角的照片。",
        "That post caused the number of weekend bookings to explode.", "那条消息让周末预约数量猛增。",
    ),
    (1633, "incessantly"): (
        "The child beside us talked through the whole coach ride.", "我们旁边的孩子整趟长途车都在说话。",
        "He chatted incessantly until his mum gave him a book.", "他不停地说话，直到妈妈给了他一本书。",
    ),
    (1638, "throw someone under the bus"): (
        "The group project was late, and the teacher asked who missed the deadline.", "小组作业迟交了，老师问是谁错过了截止日期。",
        "Sam threw his partner under the bus instead of sharing the responsibility.", "萨姆没有共同承担责任，反而把伙伴推出来背锅。",
    ),
    (1639, "expose someone s dirty secrets"): (
        "A gossip account began sharing private messages from people at school.", "一个八卦账号开始公开学校里同学的私信。",
        "It is cruel to expose someone's dirty secrets for likes.", "为了点赞而揭露别人的隐私很残忍。",
    ),
    (1641, "massive amounts of"): (
        "The town is rebuilding the playground after the old equipment broke.", "旧设备坏掉后，小镇正在重建操场。",
        "The project needs massive amounts of timber and paint.", "这个项目需要大量木材和油漆。",
    ),
    (1647, "offensive stuff"): (
        "The class group chat became quiet after one student shared a cruel meme.", "有学生发了一张刻薄的表情包后，班级群突然安静了。",
        "The teacher asked everyone to stop posting offensive stuff.", "老师要求大家不要再发冒犯人的内容。",
    ),
    (1446, "get clipped by"): (
        "Why are you sitting down with a scraped elbow after crossing the road?", "过马路后你为什么擦破了手肘，还坐下了？",
        "I got clipped by a bicycle, but the rider stopped to help.", "我被一辆自行车蹭到了，不过骑车的人停下来帮忙了。",
    ),
    (1509, "in lockstep"): (
        "The dance group practised the same turn again and again before the show.", "舞蹈队演出前反复练习同一个转身动作。",
        "By Friday, they were moving in lockstep across the stage.", "到周五时，他们已经能在舞台上步调一致地移动。",
    ),
    (1431, "fascination"): (
        "Leo asks to borrow books about planets every week.", "利奥每周都想借关于行星的书。",
        "He has had a fascination with space since he was six.", "他从六岁起就对太空着迷。",
    ),
    (1481, "orchard"): (
        "Where did those bags of apples from your uncle come from?", "你叔叔送来的那几袋苹果是从哪里来的？",
        "He grows them in a small orchard behind his house.", "他在房子后面的小果园里种这些苹果。",
    ),
    (337, "dangly"): (
        "Your earrings keep catching on the scarf when you put it on.", "你戴围巾时，耳环总勾到上面。",
        "They are dangly earrings, so I'll wear studs instead today.", "它们是垂坠耳环，所以我今天改戴耳钉。",
    ),
    (357, "glow"): (
        "You look different after a week of sleeping well and walking outside.", "你好好睡了一周、每天在外面散步后，看起来不一样了。",
        "I finally have a healthy glow again.", "我终于又有健康的气色了。",
    ),
    (945, "yet"): (
        "The train is due any minute, but I cannot see Maya on the platform.", "火车随时会到，但我在站台上看不到玛雅。",
        "She has not arrived yet, so let's wait by the entrance.", "她还没到，我们在入口等一下吧。",
    ),
    (968, "break free"): (
        "Maya feels she does the same job, commute, and chores every week.", "玛雅觉得自己每周都在重复同样的工作、通勤和家务。",
        "She wants to break free from that routine by taking an art class.", "她想通过上美术课摆脱那种日常循环。",
    ),
    (970, "cheat on someone"): (
        "Why did Ava move out of the flat so suddenly?", "艾娃为什么突然搬出公寓？",
        "She found out that her partner had cheated on her.", "她发现伴侣背叛了她。",
    ),
    (985, "come in from china"): (
        "Why did the shop owner wait so long for those tea cups?", "店主为什么等那些茶杯等了这么久？",
        "They came in from China on the last cargo ship.", "它们是随上一艘货船从中国运来的。",
    ),
    (991, "lay down"): (
        "The band booked a small studio after writing three new songs.", "乐队写了三首新歌后，订了一间小录音室。",
        "They went in to lay down the tracks before the festival.", "他们去录音，在音乐节前把曲目录下来。",
    ),
    (1014, "call off and communication phrases"): (
        "The wind became too strong for the outdoor movie night.", "风太大了，没法办露天电影夜。",
        "The organisers called off the event and texted everyone before sunset.", "组织者取消了活动，并在日落前给大家发了短信。",
    ),
    (808, "renown"): (
        "Why do visitors travel so far to see the old painter's work?", "为什么游客特地跑很远来看那位老画家的作品？",
        "She gained renown for the portraits she painted of local families.", "她因画当地家庭的肖像而闻名。",
    ),
    (812, "in pursuit of"): (
        "Ben left a steady office job to join a small theatre company.", "本辞掉稳定的办公室工作，加入了一家小剧团。",
        "He did it in pursuit of his dream of performing.", "他这么做是为了追求表演梦想。",
    ),
    (822, "reciprocal"): (
        "The two neighbours agreed to water each other's gardens during holidays.", "两位邻居约好假期里互相浇花。",
        "It is a reciprocal arrangement that helps both families.", "这是一个互惠的安排，对两家都有帮助。",
    ),
    (826, "liquidation"): (
        "The old furniture shop put a closing sign in its window.", "那家老家具店在橱窗里贴出关门告示。",
        "It entered liquidation after rent and supply costs rose.", "租金和进货成本上涨后，它进入了清算程序。",
    ),
    (831, "tariff"): (
        "Why did the price of imported olive oil rise at the supermarket?", "为什么超市进口橄榄油涨价了？",
        "A new tariff on imports made the bottles more expensive.", "新的进口关税让每瓶都更贵了。",
    ),
    (832, "expertise"): (
        "Who should help us plan the neighbourhood budget meeting?", "谁应该帮我们筹划社区预算会议？",
        "Ask Priya—she has expertise in finance.", "问普里娅吧；她在财务方面很专业。",
    ),
    (837, "bring back"): (
        "The children miss the old wooden chess board from the library.", "孩子们想念图书馆那块旧木制棋盘。",
        "They want to bring back the board for the next club meeting.", "他们想在下次社团活动时把那块棋盘带回来。",
    ),
    (846, "outsource"): (
        "The small bakery cannot pack all the festival orders by itself.", "那家小面包店没法独自包装所有节日订单。",
        "They decided to outsource the delivery work to a local courier.", "他们决定把配送工作外包给本地快递。",
    ),
    (850, "superintendent"): (
        "The school wants to repaint the faded lines on the sports court.", "学校想重新粉刷运动场褪色的线条。",
        "The superintendent approved the work for the holidays.", "主管批准假期里施工。",
    ),
    (853, "ticket"): (
        "Why is there a yellow notice under your windscreen wiper?", "为什么你的雨刷下面夹着一张黄色通知单？",
        "I got a parking ticket because I stayed too long at the market.", "我在市场停车太久，收到了一张罚单。",
    ),
    (858, "umbra"): (
        "The moon began to darken during the eclipse last night.", "昨晚月食时，月亮开始变暗。",
        "It moved into the Earth's umbra for nearly an hour.", "它进入地球本影将近一小时。",
    ),
    (864, "distract herself from"): (
        "After the hospital appointment, Grace did not want to sit alone at home.", "看完医院后，格蕾丝不想一个人坐在家里。",
        "She watched a funny series to distract herself from the pain.", "她看一部搞笑剧，让自己暂时忘掉疼痛。",
    ),
    (866, "inspection"): (
        "The café owner spent all morning fixing the loose handrail and exit sign.", "咖啡馆老板整个上午都在修松动的扶手和出口标志。",
        "The building passed inspection that afternoon.", "那天下午，这栋楼通过了检查。",
    ),
    (867, "inspect"): (
        "Why are two people in helmets walking around the construction site?", "为什么有两个人戴着安全帽在工地里走来走去？",
        "They came to inspect the site before work starts again.", "他们来检查工地，之后才能重新开工。",
    ),
    (870, "prospective"): (
        "The owners cleaned every room before opening the house on Saturday.", "房主在周六开放看房前打扫了每个房间。",
        "They met several prospective buyers that afternoon.", "那天下午，他们见了几位潜在买家。",
    ),
    (872, "nurse"): (
        "Why does your sister leave home before sunrise three days a week?", "你姐姐为什么每周三天日出前就出门？",
        "She works as a nurse on the early ward shift.", "她在病房上早班，当护士。",
    ),
    (873, "fitted"): (
        "Why did the builders measure every corner of the new kitchen?", "为什么工人量了新厨房的每个角落？",
        "They installed a fitted kitchen that uses all the space.", "他们安装了一套嵌入式厨房，充分利用了空间。",
    ),
    (883, "throw in"): (
        "The camera shop wants you to buy the display model before closing.", "相机店想让你在打烊前买下展示机。",
        "They said they would throw in a free case with it.", "他们说会额外送一个免费相机包。",
    ),
    (894, "freak out"): (
        "A spider crawled across the bathroom mirror while Ella was brushing her teeth.", "艾拉刷牙时，一只蜘蛛爬过浴室镜子。",
        "She totally freaked out and called me from the hallway.", "她吓坏了，从走廊里喊我。",
    ),
    (896, "shriek"): (
        "The surprise box popped open at the children's party.", "儿童派对上，惊喜盒子突然弹开。",
        "Mia let out a shriek and then started laughing.", "米娅尖叫了一声，然后笑起来。",
    ),
    (903, "take shelter from"): (
        "The rain started just as we reached the open part of the trail.", "我们刚走到没有遮挡的步道，雨就下起来了。",
        "We took shelter from the storm under the picnic roof.", "我们躲到野餐棚下避雨。",
    ),
    (916, "excellent"): (
        "Your daughter performed the piano piece without stopping once.", "你女儿完整地弹完了那首钢琴曲，一次也没停。",
        "She did an excellent job at the recital.", "她在演奏会上表现得非常出色。",
    ),
    (919, "exceptional"): (
        "The choir director asked Zara to sing the difficult solo.", "合唱团指挥请扎拉演唱那段高难度独唱。",
        "She has exceptional talent for music.", "她在音乐方面极有天赋。",
    ),
    (926, "outstanding"): (
        "The audience stood up after the final dance at the school show.", "学校演出的最后一支舞结束后，观众都站了起来。",
        "The dancers gave an outstanding performance.", "舞者们带来了精彩的表演。",
    ),
    (933, "lay-off"): (
        "The factory noticeboard was covered with worried messages this morning.", "今天早上，工厂公告板上贴满了让人担忧的通知。",
        "The company announced a lay-off after losing its largest order.", "失去最大订单后，公司宣布裁员。",
    ),
    (754, "visceral"): (
        "The documentary showed a family being reunited after the flood.", "纪录片播放了一家人在洪水后重聚的画面。",
        "I had a visceral reaction and had to pause the film.", "我产生了强烈的本能反应，不得不暂停影片。",
    ),
    (399, "rip through"): (
        "The teacher handed out a long report just before the meeting.", "会议前，老师发了一份很长的报告。",
        "Ben ripped through it in an hour and highlighted the key points.", "本一小时就迅速看完，并标出了要点。",
    ),
    (435, "misconception"): (
        "Several parents thought the school trip was cancelled because of one old email.", "几位家长因为一封旧邮件，以为学校旅行取消了。",
        "The teacher cleared up that misconception before lunchtime.", "老师在午饭前澄清了那个误解。",
    ),
})


CURATED_REAL_LIFE_EXPRESSION_SCENES.update({
    (437, "glow up"): (
        "Mia arrived at the reunion looking confident and full of energy.", "米娅来到聚会时看起来自信又有活力。",
        "After her new job and regular exercise, she has had a real glow up.", "开始新工作并坚持运动后，她真的变得更好了。",
    ),
    (471, "he should not have lost his temper."): (
        "Ben shouted and swept the board-game pieces off the table when he lost.", "本输掉桌游后大喊，还把棋子扫到桌下。",
        "He should not have lost his temper over one game.", "他不该因为一局游戏发脾气。",
    ),
    (479, "he turned the page dramatically."): (
        "Grandpa was reading the mystery novel aloud after dinner.", "晚饭后，爷爷在朗读那本悬疑小说。",
        "At the cliffhanger, he turned the page dramatically.", "读到悬念处，他夸张地翻了页。",
    ),
    (619, "varsity"): (
        "Your cousin stayed late for basketball tryouts all month.", "你表弟整个月都留到很晚参加篮球选拔。",
        "He made the varsity team in his first year.", "他第一年就进了校队。",
    ),
    (620, "he missed 9000 shots in his career."): (
        "The coach showed the team a video about learning from mistakes.", "教练给队员看了一段关于从错误中学习的视频。",
        "It said he missed 9000 shots in his career before becoming a champion.", "视频说他职业生涯投丢过九千次，后来才成为冠军。",
    ),
    (629, "this led me to a question"): (
        "The old map showed a footpath that no longer appears on any sign.", "旧地图上有一条小路，现在的路牌上却没有。",
        "This led me to a question about who updates the local maps.", "这让我想到一个问题：谁负责更新本地地图？",
    ),
    (631, "weightlifter"): (
        "Why does your brother bring such heavy bags to the gym?", "你弟弟为什么带那么重的包去健身房？",
        "He trains like a weightlifter before the rowing season.", "赛艇季开始前，他像举重运动员一样训练。",
    ),
    (656, "bypass"): (
        "The children tried to enter the pool without waiting for the safety talk.", "孩子们想不听安全说明就进游泳池。",
        "The lifeguard stopped them from trying to bypass the rules.", "救生员阻止他们绕过规定。",
    ),
    (677, "miffed"): (
        "Sam said he was fine after we forgot his birthday cake.", "我们忘了给萨姆准备生日蛋糕后，他说自己没事。",
        "He sounded fine, but he was probably a bit miffed.", "他嘴上说没事，不过可能还是有点不高兴。",
    ),
    (687, "overwhelm someone"): (
        "Lina opened the letter and learned she had won the art scholarship.", "莉娜打开信，得知自己拿到了艺术奖学金。",
        "The good news overwhelmed her and she started crying.", "这个好消息让她情绪涌上来，哭了起来。",
    ),
    (783, "sabotage"): (
        "Someone cut the ribbon on the school garden gate the night before judging.", "评比前一晚，有人剪断了学校花园大门上的彩带。",
        "The caretaker thinks someone tried to sabotage the project.", "管理员认为有人试图破坏这个项目。",
    ),
    (518, "curse"): (
        "The children are telling ghost stories around the camp lantern.", "孩子们围着露营灯讲鬼故事。",
        "In the story, a wizard put a curse on the old house.", "故事里，一个巫师给老房子下了诅咒。",
    ),
    (534, "retrieve"): (
        "Your suitcase appeared on the wrong baggage belt after the flight.", "下飞机后，你的行李箱出现在错误的行李转盘上。",
        "I went to retrieve it from the lost-and-found desk.", "我去失物招领处把它取回来。",
    ),
    (559, "nostalgia"): (
        "Dad found an old photo of his first flat in a moving box.", "爸爸在搬家箱子里发现一张第一套公寓的老照片。",
        "It gave him a wave of nostalgia for his student days.", "这让他涌起对学生时代的怀念。",
    ),
    (22, "do a presentation"): (
        "Why are you carrying a poster tube and your laptop to school?", "你为什么带着海报筒和笔记本去学校？",
        "I'm doing a presentation on climate change this morning.", "我今天上午要做关于气候变化的展示。",
    ),
    (51, "they all have different prompts on them"): (
        "How will each team know what to act out in the party game?", "派对游戏里，每队怎么知道要表演什么？",
        "Pick a card— they all have different prompts on them.", "抽一张卡吧——每张上面都有不同的提示。",
    ),
    (59, "pharmacy technician"): (
        "Why does your aunt know so much about prescriptions and medicine labels?", "你姨妈为什么这么懂处方和药品标签？",
        "She works as a pharmacy technician at the clinic.", "她在诊所当药房技术员。",
    ),
    (97, "with ease"): (
        "Mia looked relaxed during the driving test while everyone else was nervous.", "大家都紧张时，米娅在驾考中看起来很放松。",
        "She passed the test with ease.", "她轻松通过了考试。",
    ),
    (98, "feel at ease"): (
        "I was nervous about meeting your grandparents for the first time.", "第一次见你祖父母时，我很紧张。",
        "They made me feel at ease as soon as I arrived.", "我一到，他们就让我放松下来。",
    ),
    (136, "explicit"): (
        "The new shelf came with many screws and pieces in one box.", "新书架的盒子里有很多螺丝和零件。",
        "The instructions were explicit, so we finished it without guessing.", "说明很明确，所以我们不用猜就装好了。",
    ),
    (230, "show off"): (
        "Why does Leo keep doing tricks with his skateboard when people walk past?", "为什么有人路过时，利奥总用滑板做花式动作？",
        "He likes to show off when his friends are watching.", "朋友看着时，他喜欢炫耀。",
    ),
    (260, "catch up with"): (
        "Your brother walks so fast that we are already far behind.", "你弟弟走得太快，我们已经落后很远了。",
        "Let's jog for a minute so we can catch up with him.", "我们小跑一会儿，好追上他。",
    ),
    (1037, "extraordinary"): (
        "The music teacher asked Zara to sing the final solo at the concert.", "音乐老师请扎拉在音乐会上唱最后的独唱。",
        "She has an extraordinary talent for music.", "她有非凡的音乐天赋。",
    ),
    (1038, "wrestle"): (
        "Why does Grandpa still keep that old medal above his desk?", "爷爷为什么还把那枚旧奖牌放在书桌上？",
        "He used to wrestle in high school and won it at a local match.", "他高中时练摔跤，在一场本地比赛中赢得了它。",
    ),
    (1043, "filthy rich"): (
        "The family bought three houses after selling their beach business.", "那家人卖掉海边生意后买了三套房。",
        "People say they got filthy rich from the sale.", "人们说他们靠那笔交易变得非常有钱。",
    ),
    (1080, "with no hesitation"): (
        "The teacher asked who could help the new student find her classroom.", "老师问谁能帮新同学找到教室。",
        "Mia said yes with no hesitation.", "米娅毫不犹豫地答应了。",
    ),
    (1087, "take accountability for"): (
        "The fundraiser posters had the wrong date, so hardly anyone came.", "筹款海报写错日期，几乎没人来。",
        "The organiser took accountability for the mistake and printed new posters.", "组织者为这个错误负责，并重新印了海报。",
    ),
    (1134, "campaign"): (
        "The bakery wants more families to know about its reusable cup discount.", "面包店想让更多家庭知道可重复使用杯子的折扣。",
        "It launched a small campaign with posters at the market.", "它在市场张贴海报，发起了一场小型宣传活动。",
    ),
    (1139, "dual"): (
        "Why does Priya carry both the keys and the club register?", "为什么普里娅既拿着钥匙又拿着社团登记册？",
        "She has a dual role as caretaker and club secretary.", "她兼任管理员和社团秘书两个角色。",
    ),
    (1151, "key lesson"): (
        "The hiking group got lost because everyone followed a different map.", "徒步小组迷路了，因为每个人都跟着不同的地图。",
        "The key lesson was to check one route together before leaving.", "关键教训是出发前要一起确认一条路线。",
    ),
    (1182, "to recuperate"): (
        "Ben still looked tired after recovering from the flu.", "本流感好转后看起来还是很累。",
        "The doctor told him to stay home for two days to recuperate.", "医生让他在家休养两天。",
    ),
    (1194, "mansion"): (
        "Which house is the tour bus stopping outside by the sea?", "观光巴士要在海边哪栋房子外停？",
        "That white mansion belongs to a family that restores old boats.", "那栋白色豪宅属于一个修复老船的家庭。",
    ),
    (1210, "to head…"): (
        "The office is quiet now that the lunch break is over.", "午休结束后，办公室安静下来了。",
        "She headed back to the office after lunch.", "午饭后，她回到了办公室。",
    ),
    (1216, "peeled off tags"): (
        "The shop found several dresses with their price labels missing.", "商店发现好几条裙子的价格标签不见了。",
        "Someone probably peeled off the tags to confuse the cashier.", "有人可能撕掉标签，想让收银员搞不清价格。",
    ),
    (1224, "make it up"): (
        "Ava forgot the team meeting and missed the decision about the trip.", "艾娃忘了团队会议，错过了关于旅行的决定。",
        "She brought morning tea to make it up to everyone.", "她带来早茶，想向大家补偿一下。",
    ),
    (1276, "fringe"): (
        "Why did you book a haircut before the school photos?", "为什么学校拍照前你预约了理发？",
        "My fringe kept falling into my eyes, so I had it trimmed.", "我的刘海总掉进眼睛里，所以去修了一下。",
    ),
    (1284, "mutual"): (
        "The two flatmates share chores without keeping score.", "两位室友分担家务，从不计较谁做得更多。",
        "They have mutual respect, which makes the flat peaceful.", "他们彼此尊重，所以合租生活很融洽。",
    ),
    (1335, "mission"): (
        "The volunteers finished planting every tree before the rain arrived.", "下雨前，志愿者把所有树都种完了。",
        "The team completed its mission and celebrated with hot chocolate.", "团队完成了任务，用热巧克力庆祝。",
    ),
    (1370, "end-to-end"): (
        "The theatre is selling tickets online for the first time this year.", "剧院今年第一次在线售票。",
        "Staff tested the booking journey end-to-end before opening sales.", "开售前，工作人员完整测试了从预订到付款的流程。",
    ),
    (1376, "mentioned it briefly"): (
        "Did Sam say anything about moving to a new flat?", "萨姆提过要搬新公寓吗？",
        "He mentioned it briefly while we were walking home.", "我们走回家时，他简单提了一下。",
    ),
    (1394, "take all the credit"): (
        "The poster design was a group project, but Ben presented it alone.", "海报设计是小组作业，但本一个人去展示了。",
        "He tried to take all the credit for the work.", "他试图把所有功劳都揽到自己身上。",
    ),
    (1399, "analytic"): (
        "Why does your sister enjoy the puzzle corner more than the art table?", "你姐姐为什么比起美术桌更喜欢解谜角？",
        "She has an analytic mind and loves finding patterns.", "她有分析型思维，喜欢寻找规律。",
    ),
    (1403, "cruise through"): (
        "Mia finished the maths test while everyone else was still on page two.", "大家还在做第二页时，米娅已经做完数学测验了。",
        "She cruised through the exam because she practised every night.", "因为每天晚上练习，她轻松完成了考试。",
    ),
    (1652, "directive"): (
        "The council asked every department to cut back on printing and travel.", "市议会要求每个部门减少打印和出差。",
        "It issued a directive to reduce unnecessary spending.", "它发布了一项减少不必要开支的指令。",
    ),
    (1653, "file for something"): (
        "After receiving repeated threats, Maya spoke with a support worker.", "多次收到威胁后，玛雅找了支持工作人员谈话。",
        "She decided to file for a temporary protection order.", "她决定申请临时保护令。",
    ),
    (1654, "exaggerate"): (
        "Noah said the fish he caught was as long as the boat.", "诺亚说自己钓到的鱼和船一样长。",
        "He tends to exaggerate when he tells fishing stories.", "他讲钓鱼故事时总爱夸大。",
    ),
    (1655, "online persona"): (
        "Everyone at school thought Theo travelled every weekend because of his photos.", "学校里大家都以为西奥每个周末都在旅行，因为他总发照片。",
        "He built an online persona that looked much richer than his real life.", "他塑造了一个看起来比真实生活富裕得多的网络形象。",
    ),
    (1658, "derogatory"): (
        "The coach stopped the practice when one player mocked another's accent.", "一名队员嘲笑另一人的口音时，教练叫停了训练。",
        "She said derogatory comments are not acceptable on the team.", "她说带有贬义的评论在队里不能接受。",
    ),
    (1670, "in two separate carloads"): (
        "There were seven of us going to the lake, but only two small cars.", "我们七个人去湖边，但只有两辆小车。",
        "We arrived in two separate carloads before lunch.", "午饭前，我们分两车到了。",
    ),
    (1674, "punch"): (
        "The boxing coach reminded everyone to keep their gloves up in sparring.", "拳击教练提醒大家对练时要把手套举好。",
        "Leo threw a punch but missed the pad.", "利奥出了一拳，但没打中靶垫。",
    ),
    (1005, "settle down"): (
        "After years of moving for seasonal work, the couple wants a home base.", "多年为了季节性工作搬来搬去后，这对夫妻想有个固定的家。",
        "They hope to settle down near the coast.", "他们希望在海边附近安定下来。",
    ),
    (880, "tablet"): (
        "The pharmacist gave Dad something for his headache after checking his prescription.", "药剂师核对处方后，给爸爸拿了头痛药。",
        "He took one tablet with a glass of water.", "他用一杯水服了一片药。",
    ),
    (449, "resentful"): (
        "Mia did all the washing up while her brother played games.", "米娅洗完了所有碗碟，而弟弟在玩游戏。",
        "She felt resentful because nobody offered to help.", "没人主动帮忙，这让她感到不满。",
    ),
    (241, "affection"): (
        "The toddler ran to her grandfather as soon as he came through the door.", "祖父一进门，小孩就跑向他。",
        "She showed great affection by wrapping both arms around him.", "她张开双臂抱住他，表现出深深的亲昵。",
    ),
})


CURATED_REAL_LIFE_EXPRESSION_SCENES.update({
    (1557, "determined"): (
        "Mia missed the finish line by a minute at last year's fun run.", "米娅去年趣味跑比终点晚了一分钟。",
        "She is determined to train and enter again this year.", "她决心训练后今年再参加一次。",
    ),
    (1582, "harass"): (
        "A boy kept sending unwanted messages to a girl from the debate team.", "一个男孩不断给辩论队的女孩发不受欢迎的信息。",
        "The coach warned him not to harass her again.", "教练警告他不要再骚扰她。",
    ),
    (944, "yet"): (
        "Mia was exhausted after stacking chairs for the school concert.", "学校音乐会后，米娅累坏了，还在叠椅子。",
        "She was tired, yet she stayed to help clean the hall.", "她很累，却还是留下来帮忙清理礼堂。",
    ),
    (827, "proponent"): (
        "Why does Priya bring her reusable cup to every meeting?", "为什么普里娅每次开会都带可重复使用的杯子？",
        "She is a strong proponent of reducing single-use waste.", "她是减少一次性垃圾的坚定支持者。",
    ),
    (828, "intent on"): (
        "Ben ignored the snack table because the chess final was about to start.", "棋赛决赛快开始了，本连点心桌都没看。",
        "He was intent on winning the last match.", "他一心想赢下最后一场。",
    ),
    (841, "eligible for"): (
        "Maya finished all her volunteer hours before the scholarship deadline.", "奖学金截止前，玛雅完成了所有志愿服务时间。",
        "She is now eligible for the community scholarship.", "她现在有资格申请社区奖学金。",
    ),
    (842, "eligible to do"): (
        "Has Leo completed the safety course for the climbing wall?", "利奥完成攀岩墙安全课程了吗？",
        "Yes, he is eligible to climb without an adult now.", "完成了，他现在有资格不在成人陪同下攀爬。",
    ),
    (863, "desperate"): (
        "The last bus had left and Sam's phone battery was flat.", "末班车已经走了，萨姆的手机也没电了。",
        "He was desperate for help, so he knocked on the station office door.", "他急需帮助，于是敲了车站办公室的门。",
    ),
    (886, "remain"): (
        "The club changed its meeting room but not its membership rules.", "社团换了会议室，但没有改会员规定。",
        "The rules remain unchanged this term.", "这学期规定仍然不变。",
    ),
    (918, "distinguished"): (
        "The university invited an elderly scientist to open the new library wing.", "大学邀请一位年长科学家为新图书馆翼楼揭幕。",
        "He is a distinguished professor who once studied there.", "他是一位杰出教授，曾在这里读书。",
    ),
    (401, "thoughtful"): (
        "Mia noticed I was cold at the outdoor concert and brought me a blanket.", "露天音乐会时，米娅发现我冷，给我带来一条毯子。",
        "That was very thoughtful of her.", "她真是很体贴。",
    ),
    (436, "extrovert"): (
        "Ben introduced himself to every new family at the picnic.", "本在野餐会上向每个新家庭自我介绍。",
        "He is an extrovert who enjoys meeting strangers.", "他是个外向的人，喜欢认识陌生人。",
    ),
    (698, "go through a hard time"): (
        "Lina has been quiet since her dad lost his job.", "爸爸失业后，莉娜一直很安静。",
        "She is going through a hard time, so let's invite her for dinner.", "她正在经历一段艰难时期，我们请她来吃晚饭吧。",
    ),
    (506, "superior"): (
        "Tom corrected everyone's pronunciation at the table and laughed at mistakes.", "汤姆在餐桌上纠正每个人的发音，还嘲笑错误。",
        "He was acting superior, which made the room uncomfortable.", "他表现得高高在上，让大家很不舒服。",
    ),
    (532, "pay off"): (
        "Why is Maya taking weekend shifts at the bakery?", "玛雅为什么在面包店周末加班？",
        "She is working hard to pay off her credit-card debt.", "她努力工作是为了还清信用卡欠款。",
    ),
    (557, "in charge of"): (
        "Who has the keys to the hall and the list of volunteers?", "谁拿着礼堂钥匙和志愿者名单？",
        "Priya is in charge of the event tonight.", "今晚活动由普里娅负责。",
    ),
    (563, "let it slide"): (
        "Ben arrived ten minutes late again but apologised before the lesson began.", "本又迟到了十分钟，不过上课前就道歉了。",
        "I decided to let it slide this time because the bus broke down.", "因为公交车坏了，我决定这次算了。",
    ),
    (276, "vegetarian"): (
        "Should we make a separate dish for Ava at the barbecue?", "烧烤时，我们要不要给艾娃单独做一道菜？",
        "Yes, she is vegetarian, so she will have the grilled mushrooms.", "要，她吃素，所以她吃烤蘑菇。",
    ),
    (1033, "referred to"): (
        "Why do the younger students ask Dr. Wong for help with every science project?", "为什么低年级学生每次科学项目都来请王博士帮忙？",
        "He is often referred to as the school's science genius.", "大家常称他为学校的科学天才。",
    ),
    (1098, "capable of"): (
        "Maya has practised the safety steps on the boat all summer.", "整个夏天，玛雅都在练习船上的安全步骤。",
        "She is capable of steering it with an adult nearby.", "有成年人在旁时，她能胜任掌舵。",
    ),
    (1200, "appetite"): (
        "Nora pushed her soup away after one spoonful this morning.", "今天早上，诺拉只喝了一口汤就推开了。",
        "She has lost her appetite because she is feeling unwell.", "她身体不舒服，所以没胃口。",
    ),
    (1215, "about five or so"): (
        "How old was your cousin when she first learned to ride a bike?", "你表妹第一次学骑自行车时多大？",
        "She was about five or so when Dad took off the training wheels.", "爸爸拆掉辅助轮时，她大约五岁。",
    ),
    (1220, "prognosis"): (
        "The doctor has reviewed Grandpa's latest test results with the family.", "医生和家人一起看了爷爷最新的检查结果。",
        "The prognosis looks good, and he can go home tomorrow.", "预后看起来不错，他明天可以回家。",
    ),
    (1671, "storm around"): (
        "After the argument about chores, Ben slammed the bedroom door.", "因为家务争吵后，本猛地关上了卧室门。",
        "He was storming around the house for half an hour.", "他在屋里怒气冲冲地走了半小时。",
    ),
    (1679, "reluctant"): (
        "The teacher asked Noah to admit that he had broken the model plane.", "老师让诺亚承认是他弄坏了模型飞机。",
        "He was reluctant to admit it until his friend spoke up.", "直到朋友站出来，他才不情愿地承认。",
    ),
    (1502, "skeptic"): (
        "Everyone thinks the new cafe will be busy, but Ben is not convinced.", "大家都认为新咖啡馆会很火，但本不相信。",
        "He is a skeptic and wants to see the first month's sales.", "他是个怀疑论者，想先看看第一个月的销量。",
    ),
    (312, "ecstatic"): (
        "Mia checked the email outside the exam room and started jumping up and down.", "米娅在考场外查看邮件后，高兴得跳起来。",
        "She was ecstatic when she saw that she had passed.", "看到自己通过了，她欣喜若狂。",
    ),
})


CURATED_REAL_LIFE_EXPRESSION_SCENES.update({
    (319, "work out"): (
        "We have three broken chairs and guests arriving for dinner tonight.", "有三把椅子坏了，今晚客人就要来吃饭。",
        "Don't worry—we'll work out a solution before they arrive.", "别担心——客人到之前我们会想出办法。",
    ),
    (322, "we’re parked over there with the trailer."): (
        "The camping gear is too heavy to carry from the far car park.", "露营装备太重，没法从远处停车场搬过来。",
        "We're parked over there with the trailer, so we can collect it easily.", "我们的车和拖车停在那边，可以很方便地拿装备。",
    ),
    (833, "flat-out"): (
        "Why did nobody answer the shop phone yesterday afternoon?", "昨天下午为什么没人接商店电话？",
        "We were working flat-out because the market had just opened.", "市场刚开门，我们忙得不可开交。",
    ),
    (805, "prospective vs perspective"): (
        "Why are you dressing up before the open-home viewing tomorrow?", "明天开放看房前，你为什么要打扮得很正式？",
        "We are meeting prospective clients who may buy the house.", "我们要见几位可能买房的潜在客户。",
    ),
    (400, "backlog"): (
        "The post office was closed for two days after the power cut.", "停电后，邮局关了两天。",
        "We're dealing with a backlog of parcels this morning.", "我们今天早上正在处理积压的包裹。",
    ),
    (711, "we are doing nothing and letting the mud settle."): (
        "The pond water turned brown after the children stirred up the bottom.", "孩子们搅动池底后，池水变成了棕色。",
        "We are doing nothing and letting the mud settle before adding fish.", "我们先什么也不做，等泥沙沉下去再放鱼。",
    ),
    (769, "we are good to go."): (
        "Have we packed the snacks, checked the tyres, and locked the house?", "零食装好了吗？轮胎检查了吗？房子锁好了吗？",
        "Yes, we are good to go.", "都好了，我们可以出发了。",
    ),
    (494, "get rid of"): (
        "The garage is full of toys the children no longer use.", "车库里堆满了孩子们不再玩的玩具。",
        "We're getting rid of them at the neighbourhood sale.", "我们打算在社区义卖时处理掉它们。",
    ),
    (501, "we will come back and pick it up."): (
        "The bookshelf is too heavy to fit in the car with the children today.", "今天车里有孩子，这个书架太重，放不下。",
        "We will come back and pick it up with the trailer tomorrow.", "我们明天开拖车回来取它。",
    ),
    (93, "holiday gathering"): (
        "Why are you cooking enough food for twenty people this weekend?", "为什么这个周末你要做二十个人的饭？",
        "We're having a holiday gathering with the whole family.", "我们要和全家人办节日聚会。",
    ),
    (244, "bach"): (
        "Where are you going when the city gets too busy over the long weekend?", "长周末城市太拥挤时，你们要去哪里？",
        "We're going to the bach by the beach for two quiet nights.", "我们要去海边的小度假屋住两个安静的晚上。",
    ),
    (269, "a small get-together"): (
        "Why are there only six plates on the table for your birthday?", "为什么你的生日餐桌上只有六个盘子？",
        "I'm just having a small get-together with close friends.", "我只是和亲近的朋友小聚一下。",
    ),
    (306, "be resistant to discipline"): (
        "Why did the children argue every time the teacher asked them to line up?", "为什么老师每次让排队，孩子们都要争辩？",
        "They were resistant to discipline because the rules felt unfair to them.", "他们抗拒管教，因为觉得规则不公平。",
    ),
    (1064, "we were right about that"): (
        "The dark clouds arrived exactly when the weather app predicted.", "乌云正好在天气应用预测的时间出现。",
        "We were right about that, so I'm glad we packed umbrellas.", "这件事我们判断对了，所以还好带了伞。",
    ),
    (1173, "short on"): (
        "The bus leaves in eight minutes and we still need to buy lunch.", "公交车八分钟后就开，我们还得买午饭。",
        "We're short on time, so let's get sandwiches to take away.", "我们时间不够了，买三明治带走吧。",
    ),
    (312, "overjoyed"): (
        "The rescue team brought the missing dog back to the family after two days.", "两天后，救援队把走失的狗带回了家人身边。",
        "We were overjoyed to see him safe.", "看到它安然无恙，我们高兴极了。",
    ),
})


CURATED_REAL_LIFE_EXPRESSION_SCENES.update({
    (345, "i want to become a registered nurse in new zealand."): (
        "Why are you spending your evenings studying biology and English?", "你为什么晚上都在学生物和英语？",
        "I want to become a registered nurse in New Zealand.", "我想在新西兰成为一名注册护士。",
    ),
    (930, "drama"): (
        "The family dinner has already had two arguments before the food arrived.", "饭菜还没上桌，家庭晚餐已经吵了两次。",
        "I do not want any more drama tonight.", "我今晚不想再有任何闹剧了。",
    ),
    (419, "break free from this cycle"): (
        "Maya works late, sleeps badly, and then feels too tired to exercise.", "玛雅加班、睡不好，然后又累得没法运动。",
        "She wants to break free from this cycle of stress and exhaustion.", "她想摆脱这种压力和疲惫的循环。",
    ),
    (491, "bring it up"): (
        "You noticed the rent has increased, but your flatmate looks stressed.", "你发现房租涨了，但室友看起来压力很大。",
        "I did not want to bring it up during dinner.", "我不想在晚饭时提起这件事。",
    ),
    (112, "i want you to think back to when ..."): (
        "The coach wants the team to remember how far they have come this season.", "教练希望队员记住这个赛季走了多远。",
        "I want you to think back to when practice felt impossible.", "我想让你回想一下练习曾经觉得多么不可能。",
    ),
    (1081, "to be all over the place"): (
        "Your essay jumps from holidays to science and then to family stories.", "你的作文从假期跳到科学，又跳到家庭故事。",
        "I do not want the final version to be all over the place.", "我不想让最终版本杂乱无章。",
    ),
    (1083, "a can of worms"): (
        "Why did you stop asking about the missing money at the club?", "你为什么不再追问社团少的钱了？",
        "It might open a can of worms that nobody is ready to handle.", "这可能会引出一堆没人准备好处理的问题。",
    ),
    (1111, "listening comprehension"): (
        "The podcast host speaks quickly, and I miss the main point sometimes.", "播客主持人说得很快，我有时抓不住重点。",
        "I want to improve my listening comprehension before the course starts.", "课程开始前，我想提高听力理解。",
    ),
    (1242, "i take it"): (
        "You have read the travel plan twice and nodded at every change.", "你把旅行计划看了两遍，还对每项修改点头。",
        "I take it that you agree with the plan.", "我想你是同意这个计划的。",
    ),
    (1294, "alumni"): (
        "Will you still see people from university after graduation?", "毕业后你还会见大学同学吗？",
        "I hope to stay connected with the alumni network.", "我希望继续和校友网络保持联系。",
    ),
    (1326, "come across"): (
        "I worried that my joke about the delayed bus sounded rude.", "我担心自己拿公交延误开玩笑，听起来很不礼貌。",
        "I hope I did not come across as rude.", "我希望自己没有显得无礼。",
    ),
})


CURATED_REAL_LIFE_EXPRESSION_SCENES.update({
    (1563, "be broadly referred to as"): (
        "The parent workshop discussed hurtful messages, fake profiles, and repeated targeting online.", "家长工作坊讨论了恶意信息、假账号和反复针对他人的行为。",
        "These behaviours can broadly be referred to as online abuse.", "这些行为可以统称为网络欺凌。",
    ),
    (1592, "but this setup would take care of that"): (
        "The rain keeps dripping through the open window onto the plant shelf.", "雨水一直从开着的窗户滴到植物架上。",
        "A small cover over the shelf would take care of that.", "在架子上方加个小遮棚就能解决这个问题。",
    ),
    (1424, "skew"): (
        "Our class survey has one answer from a teacher and forty from students.", "我们班的调查有一份来自老师，四十份来自学生。",
        "That one outlier could skew the results.", "那个离群值可能会让结果失真。",
    ),
    (1428, "give rise to"): (
        "The new bus timetable lists two different stops for the same route.", "新的公交时刻表给同一路线列了两个不同站点。",
        "That mistake may give rise to confusion for visitors.", "这个错误可能会让游客感到困惑。",
    ),
    (1433, "introduce a problem"): (
        "We moved the picnic to the smaller room because it might rain.", "因为可能下雨，我们把野餐移到较小的房间。",
        "That change may introduce a problem because there are not enough chairs.", "这个改变可能会带来问题，因为椅子不够。",
    ),
    (1438, "pick up"): (
        "The flags at the beach have started to flutter more strongly.", "海滩上的旗子开始飘得更厉害了。",
        "The wind will pick up this afternoon, so let's leave before then.", "下午风会变大，所以我们那之前离开吧。",
    ),
    (1448, "roll in"): (
        "The picnic blankets are already spread on the grass.", "野餐垫已经铺在草地上。",
        "Some showers will roll in this afternoon, so bring the umbrellas.", "下午会有阵雨来，带上伞吧。",
    ),
    (1471, "drift across"): (
        "The coastal walk is clear now, but the forecast keeps changing.", "海岸步道现在很晴朗，但预报一直在变。",
        "A few showers may drift across the coast later.", "晚些时候可能有几阵雨飘过海岸。",
    ),
    (1478, "national grid"): (
        "The school installed solar panels above the gym during the holidays.", "假期里，学校在体育馆上方安装了太阳能板。",
        "On sunny days, they feed extra power back into the national grid.", "晴天时，它们会把多余电力回送到国家电网。",
    ),
    (1492, "pay for itself"): (
        "The café owner is deciding whether to buy a dishwasher that saves water.", "咖啡馆老板正在考虑买一台节水洗碗机。",
        "The installer says it will pay for itself in three years.", "安装人员说它三年后就能回本。",
    ),
    (1496, "massive difference"): (
        "Several farms in the valley are adding small solar panels to their sheds.", "山谷里的几家农场正在给棚屋安装小型太阳能板。",
        "Together, those panels can make a massive difference to local power use.", "这些面板加起来能大大改变本地的用电情况。",
    ),
    (1497, "as a whole"): (
        "The town is discussing solar panels for homes, farms, and the school.", "小镇正在讨论为家庭、农场和学校安装太阳能板。",
        "As a whole, the community could save a lot of energy.", "总体来看，社区能节省很多能源。",
    ),
    (1508, "a cascading range of things"): (
        "One wrong date on the school newsletter meant buses and lunches were booked for the wrong day.", "学校简报上一个日期写错，导致巴士和午餐都订错了日子。",
        "That small error triggered a cascading range of problems.", "那个小错误引发了一连串问题。",
    ),
    (1510, "chop and change"): (
        "The garden team keeps changing the layout after every meeting.", "花园小组每次会议后都在改布局。",
        "If we chop and change too often, we will never finish the beds.", "如果我们老是变来变去，花坛永远完不了。",
    ),
    (1454, "obstacle"): (
        "Mia has found a job she likes, but it requires a licence she does not have.", "米娅找到一份喜欢的工作，但需要她没有的执照。",
        "Lack of experience can be an obstacle to getting that job.", "缺乏经验可能成为得到那份工作的障碍。",
    ),
    (1458, "can halve their electricity bills"): (
        "The family checks their power bill every winter because heating costs so much.", "每到冬天，这家人都会看电费单，因为取暖很贵。",
        "The adviser said solar panels can halve their electricity bills.", "顾问说太阳能板能让他们的电费减半。",
    ),
    (834, "provision"): (
        "Parents were worried that the free lunches might stop after the holidays.", "家长担心假期后免费午餐会停止。",
        "The school confirmed that the provision of lunches will continue.", "学校确认午餐供应会继续。",
    ),
    (887, "roll over"): (
        "You still have money left on your bus card at the end of the month.", "月底时，你的公交卡里还有余额。",
        "The remaining balance will roll over to next month.", "剩余余额会结转到下个月。",
    ),
    (397, "ramp up to 100%"): (
        "The bakery bought a second oven before the holiday rush.", "面包店在节日高峰前买了第二台烤箱。",
        "Production will ramp up to 100% next month.", "下个月产量会提升到百分之百。",
    ),
    (411, "a domain can span across multiple accounts."): (
        "The community centre runs its booking, email, and volunteer pages under one web address.", "社区中心把预约、邮件和志愿者页面都放在一个网站地址下。",
        "A domain can span across multiple accounts when the centre manages it that way.", "这样管理时，一个域名可以覆盖多个账户。",
    ),
    (466, "solidify"): (
        "The children made jelly for tomorrow's party and put it in the fridge.", "孩子们为明天的派对做了果冻，放进冰箱了。",
        "It will solidify overnight and be ready by morning.", "它会在夜里凝固，早上就能吃。",
    ),
    (668, "self-image"): (
        "Mia stopped comparing her photos with everyone else's and began learning guitar for fun.", "米娅不再拿自己的照片和别人比较，开始为了开心学吉他。",
        "Those habits have changed her self-image for the better.", "这些习惯让她对自己的看法变得更好。",
    ),
    (497, "maybe you can wrap that with some paper."): (
        "The vase is a birthday gift, but we have no gift bag at home.", "花瓶是生日礼物，但家里没有礼物袋。",
        "Maybe you can wrap that with some paper and a ribbon.", "也许你可以用纸和丝带把它包装起来。",
    ),
    (541, "wavy"): (
        "How do you want your hair to look for the school dance?", "学校舞会时，你想要什么样的发型？",
        "If I braid it overnight, it will be wavy in the morning.", "如果我晚上编起来，早上头发会卷卷的。",
    ),
    (554, "comfy"): (
        "We have a long bus ride to the zoo tomorrow.", "我们明天要坐很久的巴士去动物园。",
        "Wear something comfy so you can sleep on the way.", "穿舒服一点，路上可以睡一会儿。",
    ),
    (27, "the maximum number of people we can have in that room"): (
        "The fire marshal checked the small hall before our family party.", "家庭聚会前，消防检查员查看了小礼堂。",
        "Thirty is the maximum number of people we can have in that room.", "那间房最多只能容纳三十人。",
    ),
    (116, "as long as"): (
        "You are worried because you still make mistakes when speaking English.", "你担心自己说英语时还会犯错。",
        "As long as you keep practising, your English will improve.", "只要持续练习，你的英语就会进步。",
    ),
    (311, "that would not have been me."): (
        "Ben volunteered to sing alone in front of the whole school.", "本自愿在全校面前独唱。",
        "That would not have been me—I would have been too nervous.", "换成我可做不到——我会太紧张。",
    ),
    (1062, "that would fit down there as well"): (
        "The new bookshelf is too wide for the living-room wall.", "新书架对客厅那面墙来说太宽了。",
        "The smaller one would fit down there as well.", "小一点的那套也能放到下面那里。",
    ),
    (1093, "rejuvenate"): (
        "You have worked six weekends in a row and look exhausted.", "你已经连续六个周末工作，看起来很疲惫。",
        "A short holiday by the lake would rejuvenate you.", "去湖边度个短假会让你恢复精神。",
    ),
    (1096, "propel you forward"): (
        "Your first cake collapsed, but you wrote down what went wrong.", "你第一次烤的蛋糕塌了，但你记下了问题。",
        "Mistakes like that can propel you forward if you learn from them.", "如果从中学习，这样的错误能推动你进步。",
    ),
    (1109, "upon"): (
        "When will the new library app appear on the school tablets?", "新图书馆应用什么时候会出现在学校平板上？",
        "It will be installed upon launch next Monday.", "它会在下周一上线时安装。",
    ),
    (1124, "migration"): (
        "The club is moving its membership list to a new system before summer.", "社团要在夏天前把会员名单迁到新系统。",
        "A clear migration plan will reduce the chance of losing records.", "清晰的迁移计划能减少记录丢失的风险。",
    ),
    (1137, "assumption"): (
        "The council planned extra buses because it expected more visitors this year.", "市议会因为预计今年游客更多，计划增加巴士。",
        "The plan was based on the assumption that traffic would increase.", "这个计划基于交通量会增加的假设。",
    ),
    (1141, "premature"): (
        "We have only viewed one flat, but Ben wants to sign a lease tonight.", "我们只看了一套公寓，本却想今晚签租约。",
        "It would be premature to decide before seeing the other places.", "在看完其他房子前做决定还太早。",
    ),
    (1150, "rotate to"): (
        "The children are watching a wide nature video on the tablet.", "孩子们正在平板上看宽屏自然纪录片。",
        "The screen will rotate to landscape mode automatically.", "屏幕会自动旋转到横屏模式。",
    ),
    (1160, "emergency vs emerge"): (
        "The school drill starts when smoke appears in the science room.", "科学教室出现烟雾时，学校演练就开始。",
        "When a serious problem emerges, it can quickly become an emergency.", "严重问题一出现，就可能很快变成紧急情况。",
    ),
    (1162, "come down to"): (
        "Both bands can play at the festival, but there is only one evening slot left.", "两个乐队都能参加音乐节，但只剩一个晚间时段。",
        "The final choice may come down to timing.", "最终选择可能取决于时间安排。",
    ),
    (1164, "skewed"): (
        "Only three people answered the survey before the deadline.", "截止日期前只有三个人完成了调查。",
        "The results may be skewed because the sample is too small.", "样本太小，结果可能会有偏差。",
    ),
    (1177, "rough"): (
        "The puppy chewed one end of the wooden table while we were out.", "我们出门时，小狗咬了木桌的一端。",
        "The surface feels rough now, so we need to sand it.", "现在表面摸起来很粗糙，我们得打磨一下。",
    ),
    (1274, "symptom"): (
        "Maya has a fever and keeps coughing after school.", "玛雅放学后发烧，还一直咳嗽。",
        "A cough can be a symptom of a cold or another illness.", "咳嗽可能是感冒或其他疾病的症状。",
    ),
    (1290, "translucent"): (
        "The bathroom faces the neighbour's driveway, so we need privacy and daylight.", "浴室正对邻居车道，所以我们既要隐私也要采光。",
        "A translucent window lets light in without showing people clearly.", "半透明窗能透光，又看不清人。",
    ),
    (1316, "take some pressure off"): (
        "We finished the invitations before the rest of the wedding tasks arrived.", "其他婚礼任务到来前，我们先完成了请柬。",
        "Finishing that early will take some pressure off us this week.", "早点完成那件事会减轻我们这周的压力。",
    ),
    (1338, "compatibility"): (
        "Will this new charger work safely with your old camera?", "这个新充电器能安全地配你的旧相机吗？",
        "We need to check their compatibility before plugging it in.", "插电前，我们得检查它们是否兼容。",
    ),
    (1668, "conversely"): (
        "The grocer lowered the price of strawberries before the weekend market.", "周末市集前，杂货店降低了草莓价格。",
        "Lower prices may increase demand; conversely, higher prices may reduce it.", "价格降低可能提高需求；反过来，价格升高可能减少需求。",
    ),
    (880, "overdose"): (
        "The pharmacist pointed to a warning label while explaining the medicine.", "药剂师解释药物时，指着警示标签。",
        "The label warns that an overdose can be fatal.", "标签警告说，过量服用可能致命。",
    ),
})


CURATED_REAL_LIFE_EXPRESSION_SCENES.update({
    (1555, "pull up"): (
        "The teacher cannot see the attendance list on the small screen.", "老师在小屏幕上看不到出勤名单。",
        "I'll pull up the report on the projector for everyone.", "我会把报告调到投影仪上给大家看。",
    ),
    (1648, "give sb five cents"): (
        "We cannot decide whether to repaint the kitchen yellow or green.", "我们决定不了厨房要刷黄色还是绿色。",
        "Let me give you my two cents before you choose.", "决定前让我说说自己的看法。",
    ),
    (457, "throw on"): (
        "The doorbell rang just as I was still wearing my pyjamas.", "我还穿着睡衣时，门铃响了。",
        "Give me a second to throw on a jacket.", "给我一分钟，我套件外套。",
    ),
    (784, "under the hood"): (
        "The mechanic lifted the car bonnet after hearing the strange noise.", "听到奇怪声音后，修车工掀起了车盖。",
        "He showed us what was happening under the hood.", "他给我们看车盖下面出了什么问题。",
    ),
    (1343, "hear back"): (
        "You sent the landlord an application for the flat yesterday.", "你昨天向房东提交了公寓申请。",
        "Let me know when you hear back from them.", "有回复时告诉我一声。",
    ),
    (1644, "live stream"): (
        "We could not travel to the concert, so we set up the laptop in the lounge.", "我们没法去现场音乐会，于是在客厅架好笔记本。",
        "We watched the live stream from home.", "我们在家看了直播。",
    ),
    (429, "a set of shelves"): (
        "Why is there a long flat box in the hallway?", "为什么走廊里有一个长长的扁盒子？",
        "I bought a set of shelves for the living room.", "我给客厅买了一套架子。",
    ),
    (472, "i got very emotional when we were talking about our problems."): (
        "The family finally spoke honestly after dinner instead of changing the subject.", "晚饭后，家人终于坦诚谈话，没有再回避话题。",
        "I got very emotional when we were talking about our problems.", "谈到我们的问题时，我情绪非常激动。",
    ),
    (724, "i watched 21 minutes in one go."): (
        "Did you finish the whole language video before breakfast?", "你早餐前把整段语言视频看完了吗？",
        "No, I watched 21 minutes in one go and will finish it later.", "没有，我一口气看了二十一分钟，晚点再看完。",
    ),
    (521, "get nothing from it"): (
        "Did the expensive workshop help you plan your new business?", "那场昂贵的工作坊有没有帮你规划新生意？",
        "Honestly, I got nothing from it except a folder of adverts.", "老实说，除了一个广告文件夹，我什么也没得到。",
    ),
    (543, "i got this when i was a lot younger."): (
        "Why do you still keep that faded concert T-shirt?", "为什么你还留着那件褪色的演唱会 T 恤？",
        "I got this when I was a lot younger, so I cannot throw it away.", "我年轻很多时得到它，所以舍不得扔。",
    ),
    (1360, "cantaloupe"): (
        "What should we bring to the picnic besides sandwiches?", "除了三明治，野餐还该带什么？",
        "I bought a cantaloupe at the supermarket for everyone to share.", "我在超市买了一个哈密瓜给大家分享。",
    ),
    (999, "put your thinking cap on"): (
        "The treasure-hunt clue says the next key is hidden where books sleep.", "寻宝线索说，下一把钥匙藏在书本睡觉的地方。",
        "Put your thinking cap on and work out the answer.", "动动脑筋，把答案想出来。",
    ),
    (390, "finishing touches"): (
        "The cake is iced, but the birthday table still looks plain.", "蛋糕已经裱好花，但生日桌看起来还是有点空。",
        "Let's put the finishing touches on it with candles and flowers.", "我们用蜡烛和花做最后的点缀吧。",
    ),
    (1065, "put it in place"): (
        "The loose tile beside the front door keeps catching people's shoes.", "前门旁松动的地砖总勾到人的鞋。",
        "Hold it steady while I put it in place.", "你扶稳它，我把它放回原位。",
    ),
    (1067, "up here"): (
        "The hook beside the stove is too low for the frying pan.", "炉子旁的挂钩对煎锅来说太低了。",
        "Put it up here on the higher shelf instead.", "把它放到这里更高的架子上吧。",
    ),
    (1538, "seem off"): (
        "The shop sold twice as many loaves yesterday, but the tally only shows ten.", "商店昨天卖了两倍的面包，但统计表只显示十条。",
        "These numbers seem off, so let's count the receipts again.", "这些数字不太对，我们再数一次收据吧。",
    ),
    (1412, "probably isn’t gonna be"): (
        "The forecast says only a few drops of rain during the football match.", "天气预报说足球赛期间只会下几滴雨。",
        "It probably isn't gonna be too wet for us to play.", "应该不会湿到没法踢。",
    ),
    (1407, "outlier"): (
        "Every child in the class ran the race in about ten minutes except one.", "班上每个孩子跑步都用了大约十分钟，只有一个不同。",
        "That twelve-minute result would be considered an outlier.", "那个十二分钟的结果会被视为离群值。",
    ),
    (1442, "inequality"): (
        "The town report shows some families can afford heating while others cannot.", "小镇报告显示，有些家庭能负担取暖，有些却不能。",
        "Income inequality remains a serious issue in the area.", "收入不平等仍是这个地区的严重问题。",
    ),
    (1462, "hurdle"): (
        "Mia found a course she loves, but the fees are far higher than she expected.", "米娅找到一门喜欢的课程，但费用比预期高得多。",
        "The cost is the biggest hurdle for her right now.", "目前费用是她最大的障碍。",
    ),
    (323, "it tends to be ..."): (
        "The lake looks calm in the morning but gets choppy after lunch.", "湖面早上很平静，午饭后会变得有浪。",
        "It tends to be windier later in the day.", "一天晚些时候通常风会更大。",
    ),
    (362, "that’s what it looks like when it glows."): (
        "The fireflies started lighting up above the grass at dusk.", "黄昏时，萤火虫开始在草地上方发光。",
        "That's what it looks like when it glows.", "它发光时看起来就是那样。",
    ),
    (889, "too good to be true"): (
        "This holiday website is offering a beachfront room for ten dollars a night.", "这个旅游网站说海景房每晚只要十美元。",
        "That deal seems too good to be true, so check the reviews first.", "这笔交易好得不太真实，先看看评价吧。",
    ),
    (923, "impressive"): (
        "Your daughter has practised piano for only one term, but she can already play both hands together.", "你女儿只练了一学期钢琴，却已经能双手同时弹。",
        "Her progress this term is really impressive.", "她这个学期的进步真让人印象深刻。",
    ),
    (386, "so visually"): (
        "The builder unfolded a drawing of the new garden path for the neighbours.", "建造者给邻居展开了一张新花园小路的图纸。",
        "So visually, it will look like this once the stones are in place.", "从视觉上看，石头铺好后会是这样。",
    ),
    (392, "so far so good"): (
        "You have been looking after your sister's twins for three mornings now.", "你已经连续三个早上照看姐姐的双胞胎了。",
        "It is tiring, but so far so good.", "很累，不过到目前为止还不错。",
    ),
    (611, "discomfort"): (
        "The new knee brace feels tight when I climb stairs.", "我上楼时，新护膝感觉很紧。",
        "It causes a little discomfort, but the physio says that is normal at first.", "它会带来一点不适，不过理疗师说刚开始这样很正常。",
    ),
    (233, "pretty lucky to be here."): (
        "The rain cleared just before our flight landed between the mountains.", "我们的航班在山间降落前，雨刚好停了。",
        "We are pretty lucky to be here on such a clear day.", "这么晴朗的一天能来到这里，我们真幸运。",
    ),
})


CURATED_REAL_LIFE_EXPRESSION_SCENES.update({
    (1517, "capacity vs capability vs compatibility"): (
        "The library has only ten study seats, but thirty students arrive after school.", "图书馆只有十个学习座位，放学后却来了三十名学生。",
        "We need more capacity to fit everyone comfortably.", "我们需要更大的容纳能力，才能让大家坐得下。",
    ),
    (1519, "obligation"): (
        "Our elderly neighbour cannot carry her groceries up the stairs today.", "年长邻居今天没法把杂货搬上楼。",
        "We have a moral obligation to help when we can.", "在力所能及时，我们有道义上的责任去帮忙。",
    ),
    (1520, "behavioural profiling"): (
        "After I searched for hiking boots once, similar adverts followed me everywhere.", "我只搜过一次徒步靴，类似广告就到处跟着我。",
        "The store may use behavioural profiling to guess what interests me.", "商店可能通过行为画像来猜测我的兴趣。",
    ),
    (134, "take certain things away"): (
        "When I ignored my chores as a teenager, my parents set a consequence.", "我青少年时不做家务，父母会给我设定后果。",
        "They used to take certain things away, like my phone for the evening.", "他们过去会拿走我的一些东西，比如晚上不让我用手机。",
    ),
})


CURATED_REAL_LIFE_EXPRESSION_SCENES.update({
    (1526, "discrepancy"): (
        "The bakery counted fifty rolls sold, but the till report says forty-eight.", "面包店数到卖出五十个面包卷，但收银报告写的是四十八个。",
        "There is a discrepancy between the two figures.", "这两个数字之间有出入。",
    ),
    (1528, "smuggle"): (
        "Airport staff found several undeclared boxes hidden in a traveller's luggage.", "机场工作人员在一名旅客的行李里发现了几个未申报的隐藏盒子。",
        "Police discovered a plan to smuggle restricted goods into the country.", "警方发现了一个把违禁物品走私入境的计划。",
    ),
    (1561, "wrap my head around sth"): (
        "The new board game has rules for cards, coins, trains, and four different maps.", "新桌游有卡牌、硬币、火车和四张不同地图的规则。",
        "There are so many moving parts that I cannot wrap my head around it yet.", "部分太多了，我还没法完全弄明白。",
    ),
    (1567, "gloss over sth"): (
        "The school report praised the new playground but did not mention the broken gate.", "学校报告表扬了新操场，却没有提坏掉的大门。",
        "It glossed over several serious safety issues.", "它对几个严重的安全问题一笔带过。",
    ),
    (1568, "in depth"): (
        "I need more than a short brochure before choosing a hiking route.", "选徒步路线前，我需要的不只是一本简短宣传册。",
        "This guide gives an in-depth look at each track and its conditions.", "这本指南深入介绍了每条路线及其状况。",
    ),
    (1569, "outsource"): (
        "The bakery has more wedding-cake orders than its small team can deliver.", "面包店的婚礼蛋糕订单比小团队能配送的还多。",
        "They decided to outsource deliveries to a local courier.", "他们决定把配送外包给本地快递。",
    ),
    (1578, "deem"): (
        "We tried the little restaurant after the theatre last night.", "昨晚看完剧，我们去了那家小餐厅。",
        "I deem it good value because the portions were generous.", "我认为它很划算，因为分量很足。",
    ),
    (1581, "turn up"): (
        "We had almost started the birthday song without Ben.", "我们差点没等本就开始唱生日歌了。",
        "Nobody expected him to turn up after his delayed flight.", "他的航班延误后，没人想到他还能出现。",
    ),
    (1421, "per"): (
        "You asked me to move the picnic to Sunday because Saturday will rain.", "你让我把野餐改到周日，因为周六会下雨。",
        "Per your request, I've updated the invitation.", "按你的要求，我已经更新了邀请函。",
    ),
    (1502, "skepticism"): (
        "The town discussed solar panels at the community hall last night.", "昨晚，小镇在社区礼堂讨论太阳能板。",
        "The panel was optimistic, despite some skepticism from residents.", "尽管有居民持怀疑态度，专家组仍很乐观。",
    ),
    (1503, "feed into"): (
        "Late buses, roadworks, and heavy rain made the school run difficult.", "公交晚点、道路施工和大雨让接送孩子变得困难。",
        "Several factors feed into the morning delays.", "有几个因素造成了早晨的延误。",
    ),
    (1513, "coupled with"): (
        "The market ran out of strawberries by ten in the morning.", "早上十点，市场的草莓就卖光了。",
        "High demand, coupled with limited supply, pushed prices up.", "需求高再加上供应有限，推高了价格。",
    ),
    (1436, "variation"): (
        "We needed both sunscreen and warm jackets on the same camping day.", "同一天露营，我们既需要防晒霜又需要暖外套。",
        "There was a lot of variation in temperature from morning to evening.", "从早到晚温度变化很大。",
    ),
    (1450, "instability"): (
        "The afternoon sky keeps changing from bright blue to dark grey.", "下午的天空一直从亮蓝变成深灰。",
        "There is some instability in the atmosphere, so the forecast may change.", "大气有些不稳定，所以预报可能会变化。",
    ),
    (1457, "vaccine"): (
        "The clinic sent me a reminder before winter began.", "冬天开始前，诊所给我发了提醒。",
        "I got the flu vaccine last week.", "我上周打了流感疫苗。",
    ),
    (1461, "upfront"): (
        "The family likes the electric car, but the price tag made them pause.", "这家人喜欢那辆电动车，但价格让他们犹豫。",
        "There is a high upfront cost, even though it saves money later.", "虽然以后能省钱，但前期费用很高。",
    ),
    (1501, "optimistic"): (
        "The community garden had fewer volunteers than hoped in its first month.", "社区花园第一个月的志愿者比预期少。",
        "The organisers are still optimistic that more people will join in spring.", "组织者仍乐观地认为春天会有更多人加入。",
    ),
    (1504, "disruptive"): (
        "One child kept shouting while the class was trying to listen to a story.", "全班听故事时，一个孩子不停大喊。",
        "His disruptive behaviour affected everyone in the room.", "他的干扰行为影响了屋里的每个人。",
    ),
    (318, "looks like you’ve got the hang of it pretty well already."): (
        "You fixed the bicycle chain without asking anyone for help.", "你没请人帮忙就修好了自行车链条。",
        "Looks like you've got the hang of it pretty well already.", "看来你已经掌握得很不错了。",
    ),
    (954, "bound to be"): (
        "The new families are moving into the building on the same weekend.", "新住户会在同一个周末搬进大楼。",
        "There is bound to be some confusion at first, so we made a welcome list.", "一开始肯定会有些混乱，所以我们做了一份欢迎清单。",
    ),
    (982, "scare the heck out of me"): (
        "A sudden bang came from the shed while I was locking up at night.", "我晚上锁门时，棚屋里突然传来一声巨响。",
        "That noise scared the heck out of me.", "那声音把我吓坏了。",
    ),
    (816, "a chain of"): (
        "The school play started late because the bus was delayed, then the lights failed.", "校剧因为巴士晚点而迟开始，接着灯光又坏了。",
        "A chain of small events led to the delay.", "一连串小事导致了延误。",
    ),
    (860, "hospital stay"): (
        "Grandpa is packing a book and warm socks for his treatment tomorrow.", "爷爷正为明天的治疗收拾书和暖袜子。",
        "His hospital stay should last about a week.", "他的住院时间大约会持续一周。",
    ),
    (888, "fee"): (
        "Before joining the sports club, I read every line of the membership form.", "加入运动社团前，我读了会员表上的每一行。",
        "There is an annual fee for using the courts.", "使用球场每年要交一笔费用。",
    ),
    (892, "run into"): (
        "I stopped at the market yesterday to buy apples after work.", "昨天我下班后去市场买苹果。",
        "I ran into an old friend near the flower stall.", "我在花摊旁偶遇了一位老朋友。",
    ),
    (905, "ultimate"): (
        "Ben practised the same guitar song for months before the talent show.", "才艺表演前，本练了好几个月同一首吉他曲。",
        "Playing it on stage was his ultimate goal.", "在台上演奏它是他的终极目标。",
    ),
    (931, "dramatically"): (
        "Mia practised the speech every night for a month.", "米娅一个月里每天晚上练演讲。",
        "Her confidence improved dramatically by the competition.", "到比赛时，她的自信显著提高了。",
    ),
    (413, "i sat in on a meeting with the department head."): (
        "Why did you wear a name badge to the office this morning?", "你今天早上为什么戴名牌去办公室？",
        "I sat in on a meeting with the department head.", "我旁听了部门主管的会议。",
    ),
    (425, "self-worth"): (
        "Mia's old manager criticised everything she did, but her new team gives helpful feedback.", "米娅以前的经理批评她做的每件事，但新团队会给有帮助的反馈。",
        "This new job has helped her rebuild her self-worth.", "这份新工作帮助她重建自我价值感。",
    ),
    (692, "one key insight"): (
        "The tutor asked what we should remember after failing a difficult practice test.", "辅导老师问我们做完一套难模拟题后该记住什么。",
        "One key insight is to practise consistently, not only before exams.", "一个关键领悟是持续练习，而不是只在考试前练。",
    ),
    (758, "my fingers rambled over the keyboard."): (
        "The room was quiet while I tried to find a melody for the song.", "我想为歌曲找旋律时，房间很安静。",
        "My fingers rambled over the keyboard until a tune appeared.", "我的手指在键盘上随意游走，直到出现一段旋律。",
    ),
})


CURATED_REAL_LIFE_EXPRESSION_SCENES.update({
    (779, "there is a two-hour time difference with new zealand."): (
        "Why does your cousin call from Sydney before we have finished breakfast?", "你表哥为什么我们还没吃完早饭就从悉尼打电话？",
        "There is a two-hour time difference with New Zealand.", "和新西兰有两个小时的时差。",
    ),
    (548, "drip down"): (
        "The roof leaked after last night's heavy rain.", "昨晚下大雨后，屋顶漏水了。",
        "Water dripped down the wall beside the window.", "水沿着窗边的墙滴下来。",
    ),
    (12, "food programs"): (
        "Several families needed extra support during the school holidays.", "学校假期里，有几户家庭需要额外帮助。",
        "The community centre ran food programs for local families.", "社区中心为当地家庭开展了食物援助项目。",
    ),
    (41, "comic book"): (
        "What did you choose from the bookshop after school?", "放学后，你在书店选了什么？",
        "I bought a comic book about a time-travelling cat.", "我买了一本关于时间旅行猫的漫画书。",
    ),
    (110, "open up"): (
        "Learning to swim meant I could join my friends at the lake each summer.", "学会游泳后，每年夏天我都能和朋友去湖边。",
        "It opened up a whole new world for me.", "这为我打开了一个全新的世界。",
    ),
    (115, "around my neighborhood"): (
        "You always walk the dog on a different street after dinner.", "晚饭后你总带狗走不同的街道。",
        "There are a lot of small parks around my neighbourhood.", "我家附近有很多小公园。",
    ),
    (119, "sleepover"): (
        "What did you enjoy most at your friends' houses when you were little?", "小时候去朋友家时，你最喜欢什么？",
        "I loved going to sleepovers and staying up to tell stories.", "我喜欢参加过夜聚会，熬夜讲故事。",
    ),
    (274, "raisin"): (
        "The children want something sweet in their breakfast cereal.", "孩子们想在早餐麦片里加点甜的。",
        "Add a few raisins and almonds to each bowl.", "每碗加一些葡萄干和杏仁。",
    ),
    (1050, "virus & bacteria"): (
        "I have a sore throat, a fever, and no energy for the school trip.", "我喉咙痛、发烧，也没精力参加学校旅行。",
        "I think I might have a viral infection.", "我想我可能得了病毒感染。",
    ),
    (1088, "all of a sudden"): (
        "We were eating outside under a clear sky at lunchtime.", "午饭时我们在晴朗天空下的外面吃饭。",
        "All of a sudden, it started raining and everyone ran inside.", "突然下起雨来，大家都跑进去了。",
    ),
    (1112, "elevate"): (
        "The evening class gives us a chance to speak English with visitors every week.", "晚间课程每周都让我们有机会和访客说英语。",
        "It has helped me elevate my English skills.", "它帮助我提升了英语能力。",
    ),
    (1121, "trade-off"): (
        "We can finish the posters quickly, or we can spend another day making them perfect.", "我们可以很快完成海报，也可以再花一天把它们做得更完美。",
        "There is always a trade-off between speed and quality.", "速度和质量之间总有取舍。",
    ),
    (1131, "colleague"): (
        "How did you hear about the opening at the local library?", "你怎么知道本地图书馆有职位空缺？",
        "A former colleague recommended the role to me.", "一位以前的同事向我推荐了这个职位。",
    ),
    (1175, "go ahead"): (
        "The rain has stopped and the hall is available for the fundraiser.", "雨停了，礼堂也可以用于筹款活动。",
        "Let's go ahead with the event as planned.", "我们按原计划继续办活动吧。",
    ),
    (1197, "electrical vs electronic"): (
        "The lights flicker whenever the kettle and heater run together.", "水壶和暖气一起开时，灯就会闪。",
        "There may be an electrical fault in the house wiring.", "房屋线路可能有电气故障。",
    ),
    (1207, "nuance"): (
        "The two invitations sound polite, but one feels much warmer than the other.", "两张邀请函听起来都礼貌，但其中一张温暖得多。",
        "There is a subtle nuance between the two word choices.", "两种用词之间有细微差别。",
    ),
    (1249, "adopt"): (
        "The club needs a simpler way to let members book the tennis court.", "社团需要一种更简单的方式让会员预约网球场。",
        "I think we should adopt this approach because it is easier for everyone.", "我认为我们应该采用这个方法，因为对大家都更容易。",
    ),
    (1298, "fossil"): (
        "The guide asked us to look carefully at the stone near the rock pool.", "导游让我们仔细看潮池旁的一块石头。",
        "That shell shape is a fossil from millions of years ago.", "那个贝壳形状是几百万年前的化石。",
    ),
    (1325, "antiquities"): (
        "Why is the museum's underground room kept so cool and dim?", "为什么博物馆的地下室保持凉爽又昏暗？",
        "They keep the Roman antiquities there to protect them.", "他们把罗马古物放在那里保护起来。",
    ),
    (1341, "end up doing"): (
        "The rain cancelled our hike just as we were packing lunch.", "我们正收拾午饭时，雨取消了徒步计划。",
        "We ended up staying home and playing cards.", "我们最后待在家里玩牌。",
    ),
    (1367, "in turn"): (
        "The teacher passed one microphone around the circle for story time.", "老师在故事时间把一个麦克风传给围坐的孩子们。",
        "Each student answered the question in turn.", "每个学生轮流回答问题。",
    ),
    (1371, "what processing steps are involved?"): (
        "The class is planning how oranges become juice for the market stall.", "班级正在规划橙子如何变成果汁，在市场摊位上卖。",
        "We listed the processing steps involved, from washing to bottling.", "我们列出了从清洗到装瓶所涉及的加工步骤。",
    ),
    (1393, "there is no point"): (
        "The café closes in two minutes and the queue is still outside.", "咖啡馆两分钟后就关门，队伍还在外面。",
        "There is no point joining now; let's make coffee at home.", "现在排队没有意义了，我们回家煮咖啡吧。",
    ),
    (1662, "broad brush"): (
        "The town report describes every teenager as if they have the same needs.", "小镇报告把所有青少年都说得好像有同样需求。",
        "It takes a broad-brush approach and misses important differences.", "它采取了粗略概括的做法，忽略了重要差异。",
    ),
    (1669, "along with"): (
        "Did you send the permission slip before the school-trip deadline?", "学校旅行截止前，你发出同意书了吗？",
        "Yes, I submitted it along with the emergency contact form.", "发了，我还一起交了紧急联系人表。",
    ),
    (601, "patch of soil"): (
        "Where can we plant the sunflower seeds behind the shed?", "我们可以把向日葵种子种在棚屋后哪里？",
        "There is a sunny patch of soil beside the fence.", "篱笆旁有一小块晒得到太阳的土。",
    ),
    (596, "sculpture"): (
        "The gallery changed its entrance display for the spring exhibition.", "画廊为春季展览更换了入口展示。",
        "A stone sculpture by a local artist now stands by the door.", "一件当地艺术家的石雕现在放在门旁。",
    ),
    (607, "sculpture"): (
        "What did you bring home from the weekend art fair?", "周末艺术展销会后，你带了什么回家？",
        "I bought a small sculpture for the garden.", "我买了一件小雕塑放花园。",
    ),
    (274, "almond"): (
        "The children want their cereal to have something crunchy in it.", "孩子们想让麦片里有点脆脆的东西。",
        "Add an almond or two with the raisins.", "和葡萄干一起加一两颗杏仁。",
    ),
    (530, "mark the occasion"): (
        "Your parents are celebrating forty years of marriage this month.", "你父母这个月庆祝结婚四十周年。",
        "We are having a small dinner to mark the occasion.", "我们办一顿小晚餐来纪念这个时刻。",
    ),
    (1531, "characterisation"): (
        "The newspaper called our quiet neighbour 'the troublemaker of the street'.", "报纸把我们安静的邻居称作“这条街的麻烦制造者”。",
        "I disagree with that characterisation of him.", "我不同意那样描述他。",
    ),
    (1607, "characteristic"): (
        "We are choosing someone to look after the children during the party.", "我们正在选一个人在派对期间照看孩子。",
        "Patience is an important characteristic in a good babysitter.", "耐心是好保姆的重要特质。",
    ),
    (960, "i work as a freelancer."): (
        "Why can you take your laptop to the library on a Tuesday morning?", "为什么周二早上你能带着笔记本去图书馆？",
        "I work as a freelancer, so my hours are flexible.", "我是自由职业者，所以时间比较灵活。",
    ),
    (917, "brilliant"): (
        "Mia suggested turning the school fair into a picnic if the hall is busy.", "米娅建议如果礼堂太忙，就把学校义卖会改成野餐。",
        "That's a brilliant idea—we can use the park instead.", "这主意太好了——我们可以用公园。",
    ),
    (712, "watch people walking by"): (
        "Why do you always choose the table by the café window?", "为什么你总选咖啡馆窗边的桌子？",
        "I like to watch people walking by while I drink my coffee.", "我喜欢喝咖啡时看人来人往。",
    ),
    (1114, "revolve around"): (
        "You are at the community radio station all Saturday. What keeps you busy?", "你整个周六都在社区电台，主要忙什么？",
        "Most of my work revolves around planning the weekend shows.", "我的大部分工作都围绕策划周末节目。",
    ),
    (1281, "long for"): (
        "The city feels noisy after the quiet village where you grew up.", "和你长大的安静村庄相比，城市感觉很吵。",
        "I long for the days when life felt simpler.", "我怀念生活更简单的那些日子。",
    ),
    (1345, "manufacture"): (
        "The children saw crates of shiny bottles outside the factory by the railway.", "孩子们看到铁路旁工厂外堆着一箱箱闪亮的瓶子。",
        "They manufacture reusable water bottles for local shops.", "他们为本地商店生产可重复使用的水瓶。",
    ),
    (299, "bibliography"): (
        "Your report is finished, but the teacher asked where your facts came from.", "你的报告写完了，但老师问资料来自哪里。",
        "Add a bibliography that lists the books and websites you used.", "加一份参考书目，列出你使用的书和网站。",
    ),
})
