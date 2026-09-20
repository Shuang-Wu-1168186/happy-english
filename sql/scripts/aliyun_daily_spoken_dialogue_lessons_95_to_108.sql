-- Extracted from the next ten available PDFs in doc/, ordered by source file identifier.
-- Sources: Learn & Talk I, Chapter 10 Lesson 95, Chapter 11 Lessons 98-103, and Chapter 12 Lessons 106-108.
-- Source PDFs for Lessons 96, 97, 104, and 105 were unavailable during this import.
-- The target table is created by aliyun_daily_spoken_dialogue_buying_clothes.sql.
-- Re-running this file updates only the lesson_code/item_order pairs below.

SET NAMES utf8mb4;
START TRANSACTION;

-- Lesson 95 · Dragon Boat Festival (doc/116956_4651_Dragon Boat Festival.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'commemorate', 'commemorate', '纪念；缅怀', '/kəˈmeməreɪt/', 'to remind people of an important person or event from the past with a special action or object; to exist to remind people of such a person or event', 'The statue is to commemorate the poet Qu Yuan.', 'commemorate, Dragon Boat Festival, Qu Yuan', 1),
    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'glutinous rice', 'glutinous rice', '糯米', '/ˈɡluːtənəs raɪs/', 'a type of rice that is especially sticky when cooked', 'Zongzi is made of glutinous rice.', 'glutinous rice, zongzi, Dragon Boat Festival', 1),
    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'participate in', 'participate in', '参与', '/pɑːrˈtɪsɪpeɪt ɪn/', 'to take part in or become involved in an activity', 'Many people participate in the dragon boat race.', 'participate in, dragon boat race, festival', 1),
    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'take the lead', 'take the lead', '领先', NULL, 'a winning position during a race or other situation where people are competing', 'He is taking the lead in the race.', 'take the lead, dragon boat race, competition', 1),
    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'fervent', 'fervent', '热情的；强烈的', '/ˈfɜːrvənt/', 'having or showing very strong and sincere feelings about something', 'There are many fervent supporters of the team.', 'fervent, cheers, dragon boat race', 1),

    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'It''s said we are going to have a day off next week because of the Dragon Boat Festival. What is it?', '据说下周因为端午节我们要放一天假。端午节是什么？', NULL, NULL, NULL, 'Dragon Boat Festival, holiday', 1),
    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Lin', NULL, 'Oh, that''s a very old tradition. Dragon Boat Festival has a history of over 2,000 years. It''s to commemorate the great poet Qu Yuan.', '哦，那是一个非常古老的传统。端午节已有两千多年历史，是为了纪念伟大诗人屈原。', NULL, NULL, NULL, 'commemorate, Qu Yuan, Dragon Boat Festival', 1),
    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'What do you do at the Dragon Boat Festival?', '端午节你们做什么？', NULL, NULL, NULL, 'Dragon Boat Festival, traditions', 1),
    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Lin', NULL, 'We usually eat Zongzi, a kind of food made of glutinous rice wrapped in bamboo leaves.', '我们通常吃粽子，一种用糯米包在竹叶里的食物。', NULL, NULL, NULL, 'zongzi, glutinous rice, Dragon Boat Festival', 1),
    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'What else?', '还有什么？', NULL, NULL, NULL, 'Dragon Boat Festival, traditions', 1),
    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Lin', NULL, 'There are many people participating in the dragon boat races. Rows of dragons strive to take the lead. The river rings with fervent cheers of “Go! Row! Go! Row!” to the rhythm of the athletes'' oars.', '有很多人参加赛龙舟。一排排龙舟努力领先。河上回响着伴随选手桨声节奏的热情欢呼：“加油！划！加油！划！”', NULL, NULL, NULL, 'participate in, take the lead, fervent cheers', 1),

    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'How will you spend the Dragon Boat Festival?', '你会如何度过端午节？', NULL, '根据课件提示补全。', NULL, 'Dragon Boat Festival, plans', 1),
    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I will just stay at home and have Zongzi made of glutinous rice. What about you?', '我会待在家里吃用糯米做的粽子。你呢？', NULL, NULL, NULL, 'zongzi, glutinous rice, festival', 1),
    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'This year, my family will go to see the dragon boat race. I heard there are many people participating in the race.', '今年我家会去看赛龙舟。我听说有很多人参加比赛。', NULL, NULL, NULL, 'dragon boat race, participate in', 1),
    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Rows of dragons strive to take the lead. That should be interesting. I''m sure you will hear fervent cheers. Remember to send some photos to me.', '一排排龙舟努力领先。那一定很有趣。我相信你会听到热情的欢呼。记得给我发些照片。', NULL, NULL, NULL, 'take the lead, fervent, dragon boat race', 1),
    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Okay.', '好的。', NULL, NULL, NULL, 'Dragon Boat Festival, conversation', 1),

    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'How do you spend the Dragon Boat Festival? Introduce the festival and some traditions.', '你如何度过端午节？介绍这个节日及其一些传统。', NULL, '可谈吃糯米粽子和观看赛龙舟。', NULL, 'Dragon Boat Festival, zongzi, dragon boat race', 1),
    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you know the origin of the Dragon Boat Festival? Try to tell the origin using the prompts politician, banish, demise of the state, and drown oneself.', '你知道端午节的起源吗？可使用“政治家、流放、国家灭亡、投河自尽”等提示讲述。', NULL, '故事梗概：端午节纪念屈原。传说中，他是被流放的政治家，在听到国家灭亡后结束了自己的生命。人们划龙舟沿河寻找他，并投入糯米以保护遗体，演变成赛龙舟和吃粽子的习俗。课件提示：遇到困难时，请向朋友、家人、老师或当地专业支持求助。', NULL, 'Dragon Boat Festival, Qu Yuan, origin', 1),

    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'It''s to commemorate the great poet Qu Yuan.\nWe usually eat Zongzi, a kind of food made of glutinous rice wrapped in bamboo leaves.\nThere are many people participating in the dragon boat races.\nRows of dragons strive to take the lead.', '复习：commemorate / glutinous rice / participate in / take the lead / fervent。', NULL, NULL, NULL, 'review, Dragon Boat Festival', 1),

    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'extra', '拓展学习', 6, 'extra', 501, NULL, '5-colored silk-threaded braid', 'In some regions of China, parents braid silk threads of five colors and put them on children''s wrists at the Dragon Boat Festival. People believe this keeps evil spirits and disease away.', '五色绳：在中国一些地区，父母会在端午节编五色丝线戴在孩子手腕上，人们相信这能驱邪避病。', NULL, '课后拓展：端午节其他传统。', NULL, 'Dragon Boat Festival, five-colored braid, tradition', 1),
    ('dragon-boat-festival', 'Chapter 10 · Holidays', 'Lesson 95 · Dragon Boat Festival', 95, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'realgar wine', 'Realgar wine, also called xionghuang wine, is a Chinese alcoholic drink made from Chinese yellow wine with powdered realgar.', '雄黄酒：又称 xionghuang wine，是一种用中国黄酒加入雄黄粉制成的酒。', NULL, '课后拓展：端午节其他传统。', NULL, 'Dragon Boat Festival, realgar wine, tradition', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 98 · Delight (doc/117168_4652_Delight.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'on cloud nine', 'on cloud nine', '非常高兴', NULL, 'extremely happy', 'This girl is on cloud nine.', 'on cloud nine, delight, emotions', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'can''t help doing', 'can''t help doing', '不禁做某事', NULL, 'to feel that it is impossible to prevent or avoid doing something', 'He can''t help jumping up.', 'can''t help, delight, emotions', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'over the moon', 'over the moon', '欣喜若狂', NULL, 'extremely happy and excited', 'The kids are over the moon.', 'over the moon, delight, emotions', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'terrific', 'terrific', '极好的', '/təˈrɪfɪk/', 'excellent; wonderful', 'Today''s weather is terrific.', 'terrific, delight, emotions', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'rejoice', 'rejoice', '高兴；欢庆', '/rɪˈdʒɔɪs/', 'to express great happiness about something', 'The kid rejoices in the game.', 'rejoice, delight, emotions', 1),

    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Amy', NULL, 'Tomorrow, I will go to the Fragrant Hills in Beijing. I''m on cloud nine!', '明天我要去北京香山。我太高兴了！', NULL, NULL, NULL, 'on cloud nine, Fragrant Hills, delight', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'Especially in autumn, the red leaves of the maple trees make the whole mountain red.', '尤其在秋天，枫树红叶让整座山变红。', NULL, NULL, NULL, 'autumn, maple leaves, Fragrant Hills', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Amy', NULL, 'I can''t help thinking of visiting that place. It must be very beautiful.', '我不禁想到去那个地方。那里一定很美。', NULL, NULL, NULL, 'can''t help, visit, delight', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'Yes, the first time that I went there, I was over the moon.', '是的，我第一次去那里时欣喜若狂。', NULL, NULL, NULL, 'over the moon, delight, travel', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Amy', NULL, 'Really? Have you ever been there?', '真的吗？你去过吗？', NULL, NULL, NULL, 'travel, Fragrant Hills', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'A couple of times.', '去过几次。', NULL, NULL, NULL, 'travel, Fragrant Hills', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Amy', NULL, 'Can you go there with me? I''d like someone who is familiar with that area to go with me.', '你能和我一起去吗？我想要熟悉那个地方的人陪我去。', NULL, NULL, NULL, 'travel, familiar, Fragrant Hills', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Mary', NULL, 'Sure. I''d be very glad to be your tour guide.', '当然。我很乐意当你的导游。', NULL, NULL, NULL, 'tour guide, delight, travel', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'dialogue', '示范对话', 2, 'dialogue', 109, 'Amy', NULL, 'Terrific! We will both rejoice in the tour.', '太棒了！我们都会享受这次旅行。', NULL, NULL, NULL, 'terrific, rejoice, tour', 1),

    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Why are you so delighted? You are over the moon!', '你为什么这么高兴？你欣喜若狂！', NULL, '根据课件提示补全。', NULL, 'over the moon, delight', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I have got a ticket to my favorite singer''s concert. I can''t help thinking of going to the concert.', '我拿到了最喜欢歌手演唱会的门票。我不禁想着去演唱会。', NULL, NULL, NULL, 'can''t help, concert, delight', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Terrific! Do you mean the Bruno Mars concert? If so, we can go together.', '太棒了！你是说 Bruno Mars 的演唱会吗？如果是，我们可以一起去。', NULL, NULL, NULL, 'terrific, concert, delight', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Really? We will both rejoice in the concert.', '真的吗？我们都会在演唱会上感到高兴。', NULL, NULL, NULL, 'rejoice, concert, delight', 1),

    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you often feel delighted? What are the three most important things for you to be delighted?', '你经常感到高兴吗？让你高兴的三件最重要的事情是什么？', NULL, '可谈爱、友谊、健康、金钱、自由、知识或游戏。', NULL, 'delight, emotions, happiness', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you think delight lies within you, or does it depend on other people and external things?', '你认为高兴来自内心，还是取决于他人和外部事物？', NULL, '可谈高兴源自内心和心态；也可谈外部事物会影响情绪，高兴是外部事物的情感反应。', NULL, 'delight, emotions, happiness', 1),

    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I''m on cloud nine!\nYes, the first time that I went there, I was over the moon.\nTerrific! We will both rejoice in the tour.', '复习：on cloud nine / can''t help doing / over the moon / terrific / rejoice。', NULL, NULL, NULL, 'review, delight', 1),

    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'on top of the world', 'on top of the world', '欣喜若狂；无比快乐', NULL, '课后拓展：表达非常高兴的短语。', NULL, 'delight, phrase, happiness', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'be full of the joys of spring', 'be full of the joys of spring', '心花怒放；充满喜悦', NULL, '课后拓展：表达非常高兴的短语。', NULL, 'delight, phrase, happiness', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'a dog with two tails', 'a dog with two tails', '乐不可支', NULL, '课后拓展：表达非常高兴的短语。', NULL, 'delight, phrase, happiness', 1),
    ('delight', 'Chapter 11 · Emotions and Attitudes', 'Lesson 98 · Delight', 98, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'like the cat got the cream', 'like the cat got the cream', '心满意足；得意洋洋', NULL, '课后拓展：表达非常高兴的短语。', NULL, 'delight, phrase, happiness', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 99 · Sadness (doc/117169_4652_Sadness.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'out of sorts', 'out of sorts', '心情不佳；身体不适', NULL, 'sick or upset', 'He is out of sorts.', 'out of sorts, sadness, emotions', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'discouraged', 'discouraged', '心灰意冷的', '/dɪsˈkɜːrɪdʒd/', 'feeling less confident or enthusiastic about doing something', 'He feels discouraged.', 'discouraged, sadness, emotions', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'bummer', 'bummer', '令人不快的事', '/ˈbʌmər/', 'a disappointing or unpleasant situation', 'He lost his wallet. What a bummer!', 'bummer, sadness, disappointment', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'gloomy', 'gloomy', '忧郁的', '/ˈɡluːmi/', 'sad and without hope', 'He is gloomy because he broke up with his girlfriend.', 'gloomy, sadness, emotions', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'grief', 'grief', '悲伤', '/ɡriːf/', 'something that causes great sadness', 'It was a grief to her that she lost a family member in an accident.', 'grief, sadness, emotions', 1),

    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'I''m feeling out of sorts today.', '我今天心情不佳。', NULL, NULL, NULL, 'out of sorts, sadness', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'What happened? You look so discouraged.', '发生什么事了？你看起来很沮丧。', NULL, NULL, NULL, 'discouraged, sadness', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'Well, I''m really unhappy about the changes at work.', '嗯，我对工作上的变化真的很不开心。', NULL, NULL, NULL, 'work, unhappy, sadness', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'What a bummer. It''s been difficult for everyone.', '真令人不快。每个人都很不容易。', NULL, NULL, NULL, 'bummer, work, sadness', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'It makes no sense! I just don''t feel well.', '这毫无道理！我就是感觉不好。', NULL, NULL, NULL, 'sadness, feelings', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'Maybe you need some time off work. You can''t always be that gloomy in the company.', '也许你需要请假休息一下。你不能总是在公司里这么忧郁。', NULL, NULL, NULL, 'time off, gloomy, work', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'Yes, maybe that''s it.', '是的，也许是这样。', NULL, NULL, NULL, 'sadness, agreement', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Mary', NULL, 'Feel free to talk to me anytime if you are feeling a lot of grief.', '如果你感到很悲伤，随时都可以和我谈谈。', NULL, NULL, NULL, 'grief, support, sadness', 1),

    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'What happened? You look so discouraged.', '发生什么事了？你看起来很沮丧。', NULL, '根据课件提示补全。', NULL, 'discouraged, sadness', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I am out of sorts. I didn''t get the promotion that I want.', '我心情不佳。我没有得到想要的晋升。', NULL, NULL, NULL, 'out of sorts, promotion, sadness', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'What a bummer. I think you need to ask for an early leave to cheer up.', '真倒霉。我想你需要申请早点离开，振作起来。', NULL, NULL, NULL, 'bummer, cheer up, sadness', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Perhaps you are right. Thanks for talking with me.', '也许你是对的。谢谢你和我谈话。', NULL, NULL, NULL, 'support, sadness, friendship', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Talk to me whenever you need help, especially when you are feeling a lot of grief.', '任何需要帮助的时候都和我说，尤其是感到很悲伤时。', NULL, NULL, NULL, 'grief, help, support', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Thank you.', '谢谢。', NULL, NULL, NULL, 'support, friendship', 1),

    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you often feel sad? What are the three main reasons for you to be sad?', '你经常感到难过吗？让你难过的三个主要原因是什么？', NULL, '可谈学校或工作压力、失去朋友或亲人、与人争吵。', NULL, 'sadness, emotions, stress', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Are you good at getting rid of sadness? What do you do to cheer yourself up when feeling sad?', '你擅长摆脱悲伤吗？难过时你会做什么让自己振作？', NULL, '可谈和朋友聊天、做运动、睡觉、喝茶、玩游戏、听音乐或看喜剧。', NULL, 'sadness, cheer up, emotions', 1),

    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I''m feeling out of sorts today.\nWhat a bummer!', '复习：out of sorts / discouraged / bummer / gloomy / grief。', NULL, NULL, NULL, 'review, sadness', 1),

    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Open the conversation', 'Let the person know that you see they are upset and that you are available to listen.', '开启谈话：让对方知道你注意到他们难过，并愿意倾听。', NULL, '课后拓展：如何安慰难过的人。', NULL, 'sadness, comfort, listening', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Ask how they feel', 'Ask the person how they are feeling to help get the conversation going.', '询问对方感觉如何，帮助开启谈话。', NULL, '课后拓展：如何安慰难过的人。', NULL, 'sadness, comfort, conversation', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Do not force positivity', 'Do not try to turn the conversation instantly positive.', '不要试图立刻把谈话转向积极。', NULL, '课后拓展：如何安慰难过的人。', NULL, 'sadness, comfort, support', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Let the person be heard', 'People who are crying or upset often just need someone to listen; do not talk over them or immediately offer solutions.', '让对方被倾听：哭泣或难过的人常常只需要有人听，不要打断或立刻提供解决方案。', NULL, '课后拓展：如何安慰难过的人。', NULL, 'sadness, listening, support', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'Be sincere', 'If you offer support or help, make sure you are willing to follow through.', '真诚：若提供支持或帮助，要确保愿意真正做到。', NULL, '课后拓展：如何安慰难过的人。', NULL, 'sadness, support, sincerity', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'Offer a hug', 'If you feel comfortable doing so, offer the person a hug.', '拥抱：若双方都觉得合适，可以给对方一个拥抱。', NULL, '课后拓展：如何安慰难过的人。', NULL, 'sadness, comfort, hug', 1),
    ('sadness', 'Chapter 11 · Emotions and Attitudes', 'Lesson 99 · Sadness', 99, 'extra', '拓展学习', 6, 'extra', 507, NULL, 'Check in again', 'Do not forget to check in with the person from time to time.', '再次关心：不要忘记不时问候对方。', NULL, '课后拓展：如何安慰难过的人。', NULL, 'sadness, comfort, support', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 100 · Anger (doc/117170_4652_Anger.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'flare up', 'flare up', '突然发怒', '/fler ʌp/', 'to suddenly become angry', 'He flares up at his employees.', 'flare up, anger, emotions', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'enrage', 'enrage', '激怒', '/ɪnˈreɪdʒ/', 'to make somebody very angry', 'The newspaper article enraged him.', 'enrage, anger, emotions', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'short-tempered', 'short-tempered', '易怒的', '/ˌʃɔːrt ˈtempərd/', 'tending to become angry very quickly and easily', 'Being tired makes me very short-tempered.', 'short-tempered, anger, emotions', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'get somebody''s back up', 'get somebody''s back up', '使某人恼火', NULL, 'to make somebody annoyed or bored', 'Her attitude really gets my back up.', 'get back up, anger, emotions', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'blow a fuse', 'blow a fuse', '勃然大怒', '/bloʊ ə fjuːz/', 'to get very angry', 'He blows a fuse because his wallet was stolen.', 'blow a fuse, anger, emotions', 1),

    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'Do you realize what time it is?', '你知道现在几点了吗？', NULL, NULL, NULL, 'anger, time', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'I''m sorry. I lost track of time, but please do not flare up at me.', '对不起。我忘了时间，但请不要对我突然发火。', NULL, NULL, NULL, 'lost track of time, flare up', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'Do you honestly believe that is a good excuse? I think you are trying to enrage me. Actually, I''m already upset.', '你真的认为这是个好借口吗？我觉得你在试图激怒我。事实上，我已经很生气了。', NULL, NULL, NULL, 'enrage, upset, anger', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'I didn''t mean to upset you. That is what really happened. Don''t be so short-tempered.', '我不是故意让你不高兴的。那就是实际发生的事。别那么易怒。', NULL, NULL, NULL, 'short-tempered, anger, apology', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'Hey! Your attitude really got my back up!', '嘿！你的态度真的让我恼火！', NULL, NULL, NULL, 'get my back up, anger', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'Sorry, I apologize for my actions. I will never be late again. Please do not blow a fuse.', '对不起，我为自己的行为道歉。我再也不会迟到了。请不要勃然大怒。', NULL, NULL, NULL, 'apologize, blow a fuse, anger', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'You''d better keep your promise.', '你最好遵守承诺。', NULL, NULL, NULL, 'promise, anger', 1),

    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'What happened? You look so angry, and I know you are not a short-tempered person.', '发生什么事了？你看起来很生气，我知道你不是一个易怒的人。', NULL, '根据课件提示补全。', NULL, 'short-tempered, anger', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Somebody stole my wallet. What gets my back up is that he even took my ID card.', '有人偷了我的钱包。让我恼火的是他甚至拿走了我的身份证。', NULL, NULL, NULL, 'get my back up, wallet, anger', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'There is no use in blowing a fuse. Did you call the police?', '勃然大怒没有用。你报警了吗？', NULL, NULL, NULL, 'blow a fuse, police, anger', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Of course, the police said they would investigate.', '当然，警察说他们会调查。', NULL, NULL, NULL, 'police, investigate, anger', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Just wait. Don''t let this thing enrage you.', '等等。别让这件事激怒你。', NULL, NULL, NULL, 'enrage, anger, calm down', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Thank you for talking with me. I am better now.', '谢谢你和我谈话。我现在好多了。', NULL, NULL, NULL, 'anger, support, friendship', 1),

    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you often get angry? What do you usually do when you get angry?', '你经常生气吗？生气时通常做什么？', NULL, '可谈做运动、和人交谈、独处冷静、听音乐或去打拳。', NULL, 'anger, emotions, calm down', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'What are the physical effects of getting angry? Is anger a good thing or a bad thing? Give your reasons.', '生气有什么身体反应？愤怒是好事还是坏事？请说明理由。', NULL, '可谈血压升高、脸变红、非常兴奋；也可谈愤怒帮助减压或表达不满，但可能伤害身体和他人的感受。', NULL, 'anger, emotions, health', 1),

    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I lost track of time, but please do not flare up at me.\nDon''t be so short-tempered.\nYour attitude really gets my back up!\nPlease do not blow a fuse.', '复习：flare up / enrage / short-tempered / get somebody''s back up / blow a fuse。', NULL, NULL, NULL, 'review, anger', 1),

    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'be on the warpath', 'be on the warpath', '怒气冲冲；准备发火', NULL, '课后拓展：表达强烈愤怒的短语。', NULL, 'anger, phrase, emotions', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'like a red rag to a bull', 'like a red rag to a bull', '极易激怒某人', NULL, '课后拓展：表达强烈愤怒的短语。', NULL, 'anger, phrase, emotions', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'rub someone the wrong way', 'rub someone the wrong way', '惹恼某人', NULL, '课后拓展：表达强烈愤怒的短语。', NULL, 'anger, phrase, emotions', 1),
    ('anger', 'Chapter 11 · Emotions and Attitudes', 'Lesson 100 · Anger', 100, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'spitting mad', 'spitting mad', '暴怒的', NULL, '课后拓展：表达强烈愤怒的短语。', NULL, 'anger, phrase, emotions', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 101 · Complaint (doc/117408_4652_Complaint.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'complaint', 'complaint', '投诉；抱怨', '/kəmˈpleɪnt/', 'a reason for not being satisfied, or a statement saying that somebody is not satisfied', 'He made a complaint about his problems at work.', 'complaint, emotions, socializing', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'make a fuss', 'make a fuss', '大惊小怪', '/fʌs/', 'to give too much attention to small unimportant matters, usually in a worried or tense way', 'He is making a fuss over the news.', 'make a fuss, complaint, emotions', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'pass the buck', 'pass the buck', '推卸责任', '/bʌk/', 'to blame someone or make them responsible for a problem that you should deal with', 'She''s always trying to pass the buck and I''m sick of it!', 'pass the buck, complaint, responsibility', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'negligence', 'negligence', '疏忽', '/ˈneɡlɪdʒəns/', 'the failure to give somebody or something enough care or attention', 'The accident was caused by negligence on the part of the driver.', 'negligence, complaint, responsibility', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'lose heart', 'lose heart', '失望；失去信心', '/luːz hɑːrt/', 'to stop hoping for something or trying to do something because you no longer feel confident', 'Don''t lose heart.', 'lose heart, complaint, emotions', 1),

    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'Ah! What happened?', '啊！发生什么了？', NULL, NULL, NULL, 'complaint, blackout', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'It''s a blackout.', '停电了。', NULL, NULL, NULL, 'blackout, complaint', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'What! I''ve just lost one hour''s worth of work. I''m gonna make a complaint to the electric company!', '什么！我刚丢失了一小时的工作成果。我要向电力公司投诉！', NULL, NULL, NULL, 'complaint, electric company, work', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'Don''t make a fuss, and don''t pass the buck. It is because of your own negligence.', '别大惊小怪，也别推卸责任。这是因为你自己的疏忽。', NULL, NULL, NULL, 'make a fuss, pass the buck, negligence', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'I know, but I just don''t know what to do.', '我知道，但我就是不知道该怎么办。', NULL, NULL, NULL, 'complaint, feelings', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'Don''t lose heart. You already have an outline, and you can rewrite it quickly.', '别失去信心。你已经有提纲了，可以很快重写。', NULL, NULL, NULL, 'lose heart, outline, support', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'I guess I have to.', '我想我只能这样了。', NULL, NULL, NULL, 'rewrite, support, complaint', 1),

    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Oh! My house was robbed. The thief took everything.', '哦！我家被抢了。小偷拿走了一切。', NULL, '根据课件提示补全。', NULL, 'robbed, complaint, security', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'You can make a complaint to the community security guard about your incident. They can''t pass the buck.', '你可以就这件事向社区保安投诉。他们不能推卸责任。', NULL, NULL, NULL, 'complaint, pass the buck, security', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I did. They said that the accident happened because of my negligence. I left my door open.', '我投诉了。他们说这件事是因为我的疏忽，我把门开着。', NULL, NULL, NULL, 'negligence, complaint, security', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Don''t lose heart. The police will find all your belongings.', '别失去信心。警察会找到你所有的物品。', NULL, NULL, NULL, 'lose heart, police, support', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'I hope so.', '我希望如此。', NULL, NULL, NULL, 'hope, complaint, support', 1),

    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'What do you have in mind when you hear the word “complain”? Who do you usually complain to? What do you complain about?', '听到“抱怨”这个词时你会想到什么？你通常向谁抱怨？抱怨什么？', NULL, '可谈抱怨是正常、烦人或愤怒的；对象可以是亲戚、朋友、同学、同事或网上陌生人；内容可包括学校或工作的人、服务差或社会不公。', NULL, 'complaint, emotions, socializing', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you like to complain? Is complaining a good thing or a bad thing? Why?', '你喜欢抱怨吗？抱怨是好事还是坏事？为什么？', NULL, '可谈抱怨能减压、帮助人或事变得更好；也可谈会让人觉得烦、浪费时间精力、带来负面能量。', NULL, 'complaint, emotions, opinions', 1),

    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I''m gonna make a complaint to the electric company!\nDon''t make a fuss, and don''t pass the buck. It is because of your own negligence.\nDon''t lose heart.', '复习：complaint / make a fuss / pass the buck / negligence / lose heart。', NULL, NULL, NULL, 'review, complaint', 1),

    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Do something about it', 'If you have time to whine and complain about something, then you have time to do something about it. — Anthony J. D''Angelo', '如果你有时间抱怨某件事，就有时间对此做点什么。——Anthony J. D''Angelo', NULL, '课后拓展：关于抱怨的说法。', NULL, 'complaint, action, quote', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Do not listen to complainers', 'Do not listen to those who weep and complain, for their disease is contagious. — Og Mandino', '不要倾听哭泣和抱怨的人，因为他们的“疾病”具有传染性。——Og Mandino', NULL, '课后拓展：关于抱怨的说法。', NULL, 'complaint, quote, emotions', 1),
    ('complaint', 'Chapter 11 · Emotions and Attitudes', 'Lesson 101 · Complaint', 101, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Be grateful', 'Be grateful for what you have and stop complaining; it bores everybody else, does you no good, and does not solve problems. — Zig Ziglar', '对拥有的一切心怀感恩并停止抱怨；抱怨让别人厌烦、对自己没有好处，也不解决问题。——Zig Ziglar', NULL, '课后拓展：关于抱怨的说法。', NULL, 'complaint, gratitude, quote', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 102 · Compliment (doc/117409_4652_Compliment.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'gifted', 'gifted', '有天赋的', '/ˈɡɪftɪd/', 'having a lot of natural ability or intelligence', 'As a musician, he is gifted.', 'gifted, compliment, emotions', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'compliment', 'compliment', '赞美', '/ˈkɑːmpləmənt/', 'a remark that expresses praise or admiration of somebody', 'It''s nice of you to give compliments to other people.', 'compliment, praise, emotions', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'flatter', 'flatter', '奉承；讨好', '/ˈflætər/', 'to say nice things about somebody, often insincerely, because you want them to do something for you or want to please them', 'I am flattered to win this award.', 'flatter, compliment, praise', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'diligent', 'diligent', '认真刻苦的', '/ˈdɪlɪdʒənt/', 'showing care and effort in your work or duties', 'He stays up to study. He is diligent.', 'diligent, compliment, study', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'pay off', 'pay off', '取得成功；带来好结果', '/peɪ ɔːf/', 'to be successful and bring good results', 'All his hard work paid off in the end, and he finally climbed over the mountain.', 'pay off, compliment, success', 1),

    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'You must like negotiating a lot. People are saying that you are gifted.', '你一定很喜欢谈判。人们都说你很有天赋。', NULL, NULL, NULL, 'negotiating, gifted, compliment', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'Thanks for your compliment. I am flattered. Actually, you don''t need to like negotiating to be good at it. You just need to understand how it works.', '谢谢你的赞美。我很受宠若惊。实际上，你不必喜欢谈判才能擅长它，只需理解它如何运作。', NULL, NULL, NULL, 'compliment, flattered, negotiating', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'I am not good at it by any means. Please give me some advice. You must be a diligent and experienced negotiator.', '我完全不擅长。请给我一些建议。你一定是一位勤奋而有经验的谈判者。', NULL, NULL, NULL, 'diligent, experienced, compliment', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'Well, generally speaking, if you want to change someone''s mind or understand his or her position, you have to put yourself in his shoes.', '一般来说，如果你想改变某人的想法或理解其立场，就要设身处地为对方着想。', NULL, NULL, NULL, 'put yourself in someone''s shoes, negotiating', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'Sounds easy. But you must have practiced a lot before things finally paid off.', '听起来很简单。但在最终取得成果之前，你一定练习了很多。', NULL, NULL, NULL, 'pay off, practice, compliment', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'Be confident in yourself. You will succeed.', '相信自己。你会成功的。', NULL, NULL, NULL, 'confidence, success, compliment', 1),

    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Hey, your Chinese is coming along. It''s a lot better now.', '嘿，你的中文进步了。现在好多了。', NULL, '根据课件提示补全。', NULL, 'Chinese, compliment, progress', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Thanks for your compliment. I am flattered.', '谢谢你的赞美。我很受宠若惊。', NULL, NULL, NULL, 'compliment, flattered, praise', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'You are such a diligent learner, and I think you are gifted.', '你是一个如此勤奋的学习者，我觉得你很有天赋。', NULL, NULL, NULL, 'diligent, gifted, compliment', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Oh, thank you, but I still get stuck on the different tones. It drives me crazy.', '哦，谢谢，但我仍会被不同声调难住。这让我很抓狂。', NULL, NULL, NULL, 'tones, Chinese, learning', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Hang in there. Your efforts will pay off soon.', '坚持住。你的努力很快会有回报。', NULL, NULL, NULL, 'pay off, encouragement, compliment', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Thank you.', '谢谢。', NULL, NULL, NULL, 'compliment, encouragement', 1),

    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'When was the last time you received a compliment? How about giving a compliment? What was it about?', '你上一次收到赞美是什么时候？你给过赞美吗？内容是什么？', NULL, '可谈关于衣服、成功或性格的赞美。', NULL, 'compliment, praise, socializing', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'How do you feel when you receive a compliment? How does it feel to give compliments? Are compliments important in interpersonal relationships? Why?', '收到赞美时你有什么感受？给别人赞美时呢？赞美在人际关系中重要吗？为什么？', NULL, '可谈感到受宠若惊、开心、自豪或尴尬；给赞美时可以真诚或不真诚；赞美可让他人感觉良好，但不能只靠赞美交朋友。', NULL, 'compliment, interpersonal relationships, emotions', 1),

    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Thanks for your compliment. I am flattered.\nWell, generally speaking, if you want to change someone''s mind or understand his or her position, you have to put yourself in his shoes.\nYou must have practiced a lot before things finally paid off.', '复习：gifted / compliment / flatter / diligent / pay off。', NULL, NULL, NULL, 'review, compliment', 1),

    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Be specific', 'When giving someone a compliment, be specific so the person knows exactly what he or she did well. Example: Great job on the presentation!', '具体：赞美别人时要具体，让对方清楚自己哪里做得好，例如“你的演示做得真棒！”', NULL, '课后拓展：给赞美的要点。', NULL, 'compliment, specific, praise', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Do not overdo it', 'Limit the number of compliments you give; too many can make you sound insincere and become excessive flattery.', '不要过度：限制赞美次数，太多会显得不真诚，成为过度奉承。', NULL, '课后拓展：给赞美的要点。', NULL, 'compliment, sincerity, flatter', 1),
    ('compliment', 'Chapter 11 · Emotions and Attitudes', 'Lesson 102 · Compliment', 102, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Use an appropriate tone', 'Express enthusiasm with an appropriate tone; a smile can naturally lift your tone.', '使用恰当语气：用合适的语调表达热情；微笑能自然提升语调。', NULL, '课后拓展：给赞美的要点。', NULL, 'compliment, tone, smile', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 103 · Apology (doc/117410_4652_Apology.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'yell at', 'yell at', '对……吼叫', '/jel æt/', 'to shout loudly, for example because you are angry, excited, frightened, or in pain', 'The boss yelled at his employees.', 'yell at, apology, emotions', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'apologize', 'apologize', '道歉', '/əˈpɑːlədʒaɪz/', 'to say that you are sorry for doing something wrong or causing a problem', 'He apologized to his friend.', 'apologize, apology, friendship', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'slip somebody''s mind', 'slip somebody''s mind', '忘记', NULL, 'to forget something or forget to do something', 'I''m sorry I didn''t tell you. It completely slipped my mind.', 'slip mind, apology, forget', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'after all', 'after all', '毕竟', '/ˈæftər ɔːl/', 'used when explaining something or giving a reason', 'He should have paid. He suggested it, after all.', 'after all, apology, reason', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'make up for', 'make up for', '补偿', NULL, 'to do or give something because you caused somebody trouble, suffering, or disappointment and wish to show you are sorry', 'She bought me dinner to make up for being so late the day before.', 'make up for, apology, friendship', 1),

    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'I''m so sorry about yesterday. I shouldn''t have yelled at you in front of everyone. I want to apologize to you.', '昨天的事我很抱歉。我不应该当着大家的面吼你。我想向你道歉。', NULL, NULL, NULL, 'apologize, yell at, friendship', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'Don''t worry about it. After all, I am the one who forgot to bring your notebook. It totally slipped my mind.', '别担心。毕竟，是我忘了带你的笔记本，这件事完全被我忘了。', NULL, NULL, NULL, 'after all, slip mind, apology', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'I shouldn''t have made a big deal of it.', '我不该把这件事闹大。', NULL, NULL, NULL, 'apology, friendship', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'I know the exam is so important for you. Please let me make up for your trouble.', '我知道考试对你很重要。请让我补偿给你带来的麻烦。', NULL, NULL, NULL, 'make up for, exam, apology', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'How about having a dinner together?', '一起吃顿饭怎么样？', NULL, NULL, NULL, 'dinner, friendship, apology', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'That sounds great.', '听起来不错。', NULL, NULL, NULL, 'friendship, apology', 1),

    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'I want to apologize for what I did yesterday. I shouldn''t have yelled at you in front of everyone.', '我想为昨天做的事道歉。我不应该当着大家的面吼你。', NULL, '根据课件提示补全。', NULL, 'apologize, yell at, friendship', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Don''t mention it. I am the one who forgot to return your money. It totally slipped my mind.', '别提了。是我忘了还你的钱。这件事完全被我忘了。', NULL, NULL, NULL, 'slip mind, money, apology', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I shouldn''t have made a big deal of it.', '我不该把这件事闹大。', NULL, NULL, NULL, 'apology, friendship', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Not at all. Please let me make up for your trouble.', '一点也不。请让我补偿给你带来的麻烦。', NULL, NULL, NULL, 'make up for, apology, friendship', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'It won''t be necessary. I just hope that it didn''t affect our friendship.', '没必要。我只希望这没有影响我们的友谊。', NULL, NULL, NULL, 'friendship, apology', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Sure.', '当然。', NULL, NULL, NULL, 'friendship, apology', 1),

    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you ever felt the need to apologize to a colleague or friend? What happened?', '你曾觉得需要向同事或朋友道歉吗？发生了什么？', NULL, '可谈给别人造成麻烦、犯错或伤害某人的感受。', NULL, 'apology, colleague, friendship', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you think it is difficult to make an apology? Why or why not?', '你认为道歉很难吗？为什么或为什么不？', NULL, '可谈会尴尬、难以承认错误、担心道歉不被接受；也可谈真心认识到错误时容易道歉，道歉没有羞耻。', NULL, 'apology, emotions, friendship', 1),

    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I shouldn''t have yelled at you in front of everyone. I want to apologize to you.\nAfter all, I am the one who forgot to bring your notebook. It totally slipped my mind.\nPlease let me make up for your trouble.', '复习：yell at / apologize / after all / slip somebody''s mind / make up for。', NULL, NULL, NULL, 'review, apology', 1),

    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'It doesn''t matter', 'It doesn''t matter.', '没关系。', NULL, '课后拓展：接受道歉的表达。', NULL, 'apology, acceptance, phrase', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'No problem', 'No problem.', '没问题。', NULL, '课后拓展：接受道歉的表达。', NULL, 'apology, acceptance, phrase', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Please don''t mention it', 'Please don''t mention it.', '请别提了。', NULL, '课后拓展：接受道歉的表达。', NULL, 'apology, acceptance, phrase', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Please don''t let it happen again', 'Please don''t let it happen again.', '请别让它再发生。', NULL, '课后拓展：接受道歉的表达。', NULL, 'apology, acceptance, phrase', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'I forgive you', 'You should be, but I forgive you.', '你是该道歉，但我原谅你。', NULL, '课后拓展：接受道歉的表达。', NULL, 'apology, acceptance, forgiveness', 1),
    ('apology', 'Chapter 11 · Emotions and Attitudes', 'Lesson 103 · Apology', 103, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'Apology accepted', 'Apology accepted.', '接受道歉。', NULL, '课后拓展：接受道歉的表达。', NULL, 'apology, acceptance, phrase', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 106 · Air Pollution (doc/117585_4653_Air Pollution.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'smog', 'smog', '雾霾', '/smɑːɡ/', 'a form of air pollution that is or looks like a mixture of smoke and fog, especially in cities', 'The smog in the city is very serious.', 'smog, air pollution, environment', 1),
    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'emission', 'emission', '排放', '/ɪˈmɪʃn/', 'the production or sending out of light, heat, gas, or similar matter', 'The emission of the gas is controlled.', 'emission, air pollution, environment', 1),
    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'exhaust fume', 'exhaust fume', '尾气', '/ɪɡˈzɔːst fjuːm/', 'waste gases that come out of a vehicle, engine, or machine', 'Exhaust fumes are the main reason for the city''s pollution.', 'exhaust fume, vehicles, air pollution', 1),
    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'bacteria', 'bacteria', '细菌', '/bækˈtɪriə/', 'the simplest and smallest forms of life, existing in large numbers in air, water, soil, and living and dead creatures; often a cause of disease', 'Neither chilling nor freezing kills all bacteria.', 'bacteria, air pollution, health', 1),
    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'suburb', 'suburb', '郊区', '/ˈsʌbɜːrb/', 'an area where people live outside the center of a city; use in the suburbs', 'They live in the suburbs.', 'suburb, city, air pollution', 1),

    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'Look at the smog. The air quality in this city is so terrible. The pollution levels are so high that we aren''t even supposed to go outside without a mask!', '看看雾霾。这座城市的空气质量太糟糕了。污染水平如此高，我们甚至不该不戴口罩出门！', NULL, NULL, NULL, 'smog, air quality, mask', 1),
    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'The emission of exhaust fumes from vehicles and the bacteria in the air have caused a great deal of damage to the environment and human body.', '车辆尾气的排放和空气中的细菌对环境和人体造成了大量损害。', NULL, NULL, NULL, 'emission, exhaust fumes, bacteria', 1),
    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'On top of that, there are a few large chemical factories in the suburbs, which are contributing to the high pollution levels in the water and the air in this city.', '此外，郊区还有一些大型化工厂，导致这座城市水和空气污染水平很高。', NULL, NULL, NULL, 'suburbs, chemical factories, pollution', 1),
    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'As much as I love this city, I think I''m going to have to find a greener city to live in. Living in a polluted city like this just can''t be good for my health.', '尽管我很爱这座城市，我想我不得不找一座更绿色的城市居住。在这样受污染的城市生活对健康一定不好。', NULL, NULL, NULL, 'green city, pollution, health', 1),

    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Why didn''t you go to work yesterday?', '你昨天为什么没去上班？', NULL, '根据课件提示补全。', NULL, 'work, air pollution', 1),
    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I was sick because of the smog.', '我因雾霾生病了。', NULL, NULL, NULL, 'smog, health, air pollution', 1),
    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I''m sorry to hear that. I am also a little uncomfortable because of the exhaust fumes from vehicles.', '听到这个我很难过。我也因车辆尾气有些不舒服。', NULL, NULL, NULL, 'exhaust fumes, vehicles, air pollution', 1),
    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'I guess I have to stay in the suburbs for some time to have some fresh air. The doctor said the bacteria in the air is the cause of the illness.', '我想我得在郊区待一阵子呼吸新鲜空气。医生说空气中的细菌是生病的原因。', NULL, NULL, NULL, 'suburbs, bacteria, fresh air', 1),
    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Wearing a mask is necessary.', '戴口罩是必要的。', NULL, NULL, NULL, 'mask, air pollution, health', 1),

    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you often wear a mask? Talk about the air quality in your city.', '你经常戴口罩吗？谈谈你所在城市的空气质量。', NULL, '可谈空气新鲜、看得到蓝天、不必戴口罩；污染但不严重；或外出经常要戴口罩、很少看见蓝天。', NULL, 'air quality, mask, air pollution', 1),
    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'What can you do to protect yourself from air pollution? What can you do to help reduce it?', '你能做什么保护自己免受空气污染？又能做什么帮助减少污染？', NULL, '可谈住在污染少的地方或郊区、戴口罩、购买空气净化器；以及多用公共交通、不放烟花、不焚烧物品。', NULL, 'air pollution, mask, public transportation', 1),

    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'The emission of exhaust fumes from vehicles and the bacteria in the air cause a great deal of damage to the environment and human body.\nOn top of that, there are a few large chemical factories in the suburbs, which are contributing to the high pollution levels in the water and the air in this city.', '复习：smog / emission / exhaust fume / bacteria / suburb。', NULL, NULL, NULL, 'review, air pollution', 1),

    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Effects on human health', 'The course notes state that air pollution is one of the world''s biggest killers and is associated with around four million premature deaths each year.', '对人体健康的影响：课件指出空气污染是全球最大的致死因素之一，并与每年约四百万例过早死亡有关。', NULL, '课后拓展：空气污染的影响。', NULL, 'air pollution, health, environment', 1),
    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Effects on plants', 'Air pollution can seriously affect plant growth. Chemical residues can be found in plants that grow alongside highways.', '对植物的影响：空气污染会严重影响植物生长。例如，公路旁生长的植物中容易发现化学残留物。', NULL, '课后拓展：空气污染的影响。', NULL, 'air pollution, plants, environment', 1),
    ('air-pollution', 'Chapter 12 · Environment', 'Lesson 106 · Air Pollution', 106, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Other effects', 'Air pollution can blacken buildings with soot and also contributes to acid rain.', '其他影响：空气污染会让烟尘熏黑建筑物，也会导致酸雨。', NULL, '课后拓展：空气污染的影响。', NULL, 'air pollution, soot, acid rain', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 107 · Climate Change (doc/117587_4653_Climate Change.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'carbon dioxide', 'carbon dioxide', '二氧化碳', '/ˌkɑːrbən daɪˈɑːksaɪd/', 'a gas breathed out by people and animals or produced by burning carbon; CO2', 'The factory produces much carbon dioxide.', 'carbon dioxide, climate change, environment', 1),
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'global warming', 'global warming', '全球变暖', '/ˌɡloʊbl ˈwɔːrmɪŋ/', 'the increase in the temperature of the earth''s atmosphere caused by an increase in particular gases, especially carbon dioxide; an important aspect of climate change', 'The icebergs are melting because of global warming.', 'global warming, climate change, environment', 1),
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'greenhouse effect', 'greenhouse effect', '温室效应', '/ˈɡriːnhaʊs ɪfekt/', 'the gradual rise in temperature of the earth''s atmosphere caused by an increase in gases such as carbon dioxide that trap the sun''s heat', 'There will be less ice because of the greenhouse effect.', 'greenhouse effect, climate change, environment', 1),
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'glacier', 'glacier', '冰川', '/ˈɡleɪʃər/', 'a large mass of ice formed by snow on mountains that moves very slowly down a valley', 'The glacier is getting smaller and smaller.', 'glacier, climate change, environment', 1),
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'in jeopardy', 'in jeopardy', '处于危险之中', '/ɪn ˈdʒepərdi/', 'in a dangerous position or situation and likely to be lost or harmed; in danger', 'Animals'' living environment is in jeopardy.', 'in jeopardy, climate change, environment', 1),

    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'Your hometown is famous for winter camping. Do you get a lot of snow there?', '你的家乡以冬季露营闻名。那里下很多雪吗？', NULL, NULL, NULL, 'winter camping, snow, climate', 1),
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'We get quite a bit of snow, but it''s mostly just up in the mountains.', '我们下不少雪，但主要在山上。', NULL, NULL, NULL, 'snow, mountains, climate', 1),
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'Lately there have been a lot of discussions about global warming. Have you experienced the greenhouse effect, such as less snow in winter?', '最近有很多关于全球变暖的讨论。你有没有经历温室效应，比如冬天雪变少？', NULL, NULL, NULL, 'global warming, greenhouse effect, snow', 1),
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'I think I do. I think there''s been less snow. It is quite noticeable that the glaciers on the mountains have gotten smaller and smaller. Our living environment is in jeopardy.', '我想有。我觉得雪变少了。山上的冰川越来越小很明显。我们的生存环境处于危险之中。', NULL, NULL, NULL, 'glaciers, in jeopardy, climate change', 1),
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'Really! Do you think global warming may be getting worse?', '真的吗！你认为全球变暖可能在变得更糟吗？', NULL, NULL, NULL, 'global warming, climate change', 1),
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'I would say so, because people are producing more and more carbon dioxide.', '我会这么说，因为人们正在产生越来越多的二氧化碳。', NULL, NULL, NULL, 'carbon dioxide, global warming, climate change', 1),

    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'What is your opinion about global warming?', '你怎么看全球变暖？', NULL, '根据课件提示补全。', NULL, 'global warming, climate change', 1),
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'It''s pretty serious, man. There have been tons of scientific studies, and the scientific community says that the earth is heating up mainly because of the production of carbon dioxide.', '这很严重，朋友。已有大量科学研究，科学界认为地球变暖主要是由二氧化碳排放造成的。', NULL, NULL, NULL, 'carbon dioxide, global warming, science', 1),
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Yes, I heard the glaciers are melting all over the world.', '是的，我听说世界各地的冰川正在融化。', NULL, NULL, NULL, 'glaciers, melting, climate change', 1),
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Besides, our living environment is in jeopardy.', '此外，我们的生存环境处于危险之中。', NULL, NULL, NULL, 'in jeopardy, environment, climate change', 1),

    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Explain global warming in your own words. Do you think it is around us? What climate changes have you noticed?', '用自己的话解释全球变暖。你认为它在我们身边吗？你注意到哪些气候变化？', NULL, '可谈气温上升和二氧化碳；冬天平均更不冷、雪更少、夏天更热、更多极端天气、更多暴雨或完全不下雨。', NULL, 'global warming, climate change, environment', 1),
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you think people need to do something about global warming? What will you do to fight it?', '你认为人们需要对全球变暖采取行动吗？你会做什么应对它？', NULL, '可谈形势严峻、极端天气增加、海平面上升使人失去家园；也可讨论“只是理论”的观点。行动可包括多用公共交通和保护植物。', NULL, 'global warming, public transportation, environment', 1),

    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Lately there have been a lot of discussions about global warming. Have you experienced the greenhouse effect, like less snow?\nIt is quite noticeable that the glaciers on the mountains have gotten smaller and smaller. Our living environment is in jeopardy.', '复习：carbon dioxide / global warming / greenhouse effect / glacier / in jeopardy。', NULL, NULL, NULL, 'review, climate change', 1),

    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'rising sea level', 'rising sea level', '海平面上升', NULL, '课后拓展：全球变暖与气候变化的后果。', NULL, 'climate change, sea level', 1),
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'melting glaciers and permafrost', 'melting glaciers and permafrost', '冰川和冻土消融', NULL, '课后拓展：全球变暖与气候变化的后果。', NULL, 'climate change, glaciers, permafrost', 1),
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'destroying ecosystem balance', 'destroying ecosystem balance / balance of nature', '破坏自然生态系统平衡', NULL, '课后拓展：全球变暖与气候变化的后果。', NULL, 'climate change, ecosystem, environment', 1),
    ('climate-change', 'Chapter 12 · Environment', 'Lesson 107 · Climate Change', 107, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'reducing biodiversity', 'reducing biodiversity', '生物多样性减少', NULL, '课后拓展：全球变暖与气候变化的后果。', NULL, 'climate change, biodiversity, environment', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 108 · Desertification (doc/117591_4653_Desertification.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'desertification', 'desertification', '沙漠化', '/dɪˌzɜːrtɪfɪˈkeɪʃn/', 'the process of becoming or making something a desert', 'People need to grow more plants to prevent desertification.', 'desertification, desert, environment', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'expansion', 'expansion', '扩大；增加；扩展', '/ɪkˈspænʃn/', 'an act of increasing or making something increase in size, amount, or importance; related verb: expand', 'People have taken measures to prevent the expansion of the desert.', 'expansion, desertification, desert', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'fertile', 'fertile', '肥沃的', '/ˈfɜːrtl/', 'of land or soil, able to grow plants well', 'Fertile land can produce a large number of good-quality crops.', 'fertile, soil, desertification', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'soil', 'soil', '土壤', '/sɔɪl/', 'the top layer of the earth in which plants and trees grow', 'The soil in this area is very fertile.', 'soil, fertile, desertification', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'delicate', 'delicate', '脆弱的', '/ˈdelɪkət/', 'easily damaged or broken', 'Delicate plants need to be taken care of carefully.', 'delicate, environment, desertification', 1),

    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'Recently I attended a lecture about desertification.', '最近我参加了一场关于沙漠化的讲座。', NULL, NULL, NULL, 'desertification, lecture, environment', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'Desertification? What is it?', '沙漠化？那是什么？', NULL, NULL, NULL, 'desertification, environment', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'To put it simply, desertification is the expansion of the desert.', '简单地说，沙漠化就是沙漠的扩张。', NULL, NULL, NULL, 'desertification, expansion, desert', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'It sounds like a bad thing. Why does the desert expand?', '听起来像一件坏事。沙漠为什么会扩张？', NULL, NULL, NULL, 'desert, expansion, environment', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'There are many reasons. Primarily, it is because of lack of plants. The plants can keep the fertile soil from turning into the desert.', '有很多原因。主要是因为缺少植物。植物能防止肥沃的土壤变成沙漠。', NULL, NULL, NULL, 'plants, fertile soil, desertification', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'That''s why we need to plant more trees. I have never known the Earth is so delicate until today.', '这就是为什么我们需要种更多树。直到今天我才知道地球如此脆弱。', NULL, NULL, NULL, 'plant trees, delicate, environment', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'You are right, so we need to protect the plants and the environment.', '你说得对，所以我们需要保护植物和环境。', NULL, NULL, NULL, 'protect plants, environment, desertification', 1),

    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Do you have any knowledge about desertification?', '你了解沙漠化吗？', NULL, '根据课件提示补全。', NULL, 'desertification, environment', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'In my opinion, desertification is the expansion of the desert.', '在我看来，沙漠化是沙漠的扩张。', NULL, NULL, NULL, 'desertification, expansion, desert', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Basically, you are right. Because of lack of plants, much fertile soil has turned into desert.', '基本上你是对的。因为缺少植物，很多肥沃土壤已经变成沙漠。', NULL, NULL, NULL, 'lack of plants, fertile soil, desert', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'That''s terrible. What can humans do to stop it?', '太糟糕了。人类能做什么来阻止它？', NULL, NULL, NULL, 'desertification, environment, action', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'First of all, we need to protect plants which can keep the soil. Our earth is delicate, so everyone needs to protect it.', '首先，我们需要保护能保持土壤的植物。我们的地球很脆弱，所以每个人都需要保护它。', NULL, NULL, NULL, 'protect plants, soil, delicate', 1),

    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Explain desertification in your own words. Is there a desert near or in your hometown? Have you ever been to a desert? How did you feel?', '用自己的话解释沙漠化。你的家乡附近或境内有沙漠吗？你去过沙漠吗？感觉如何？', NULL, '可谈沙漠扩张和肥沃土壤流失；也可谈清晰、荒凉、孤独等感觉。', NULL, 'desertification, desert, environment', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'List some damages caused by desertification. What can you do to stop it?', '列举一些沙漠化造成的破坏。你能做什么来阻止它？', NULL, '可谈沙尘暴、人类可居住空间减少、可耕肥沃土壤减少；可谈多种树、保护植物、向他人普及沙漠化知识。', NULL, 'desertification, sandstorm, environment', 1),

    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Recently I attended a lecture about desertification.\nTo put it simply, desertification is the expansion of the desert.\nThe plants can keep the fertile soil from turning into the desert.\nI have never known our earth is so delicate until today.', '复习：desertification / expansion / fertile / soil / delicate。', NULL, NULL, NULL, 'review, desertification', 1),

    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'sandstorm', 'sandstorm', '沙尘暴', NULL, '课后拓展：沙漠化的危害。', NULL, 'desertification, sandstorm, environment', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'debris flow', 'debris flow', '泥石流', NULL, '课后拓展：沙漠化的危害。', NULL, 'desertification, debris flow, environment', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'flood', 'flood', '洪水', NULL, '课后拓展：沙漠化的危害。', NULL, 'desertification, flood, environment', 1),
    ('desertification', 'Chapter 12 · Environment', 'Lesson 108 · Desertification', 108, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'landslide', 'landslide', '滑坡', NULL, '课后拓展：沙漠化的危害。', NULL, 'desertification, landslide, environment', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

COMMIT;
