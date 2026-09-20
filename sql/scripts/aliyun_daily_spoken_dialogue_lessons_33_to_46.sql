-- Extracted from the next ten available PDFs in doc/, ordered by source file identifier.
-- Sources: Learn & Talk I, Chapter 4 Lessons 33-35, Chapter 5 Lessons 38-43, and Chapter 6 Lesson 46.
-- Source PDFs for the intervening lesson numbers were unavailable during this import.
-- The target table is created by aliyun_daily_spoken_dialogue_buying_clothes.sql.
-- Re-running this file updates only the lesson_code/item_order pairs below.

SET NAMES utf8mb4;
START TRANSACTION;

-- Lesson 33 · Making Phone Calls (doc/112317_809_Making Phone Calls.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'appointment', 'appointment', '约会；预约；约定', '/əˈpɔɪntmənt/', 'a formal arrangement to meet or visit someone at a particular time and place', 'I''d like to make an appointment with Dr. Evans, please.', 'appointment, phone call, schedule', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'be able to', 'be able to', '能够做某事', NULL, 'to have the necessary physical strength, mental power, skill, time, money, or opportunity to do something', 'Will she be able to cope with the work?', 'be able to, phone call', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'available', 'available', '可获得的；可用的；有空的', '/əˈveɪləbl/', 'able to be bought or used; free to meet or talk', 'Is this dress available in a larger size?', 'available, appointment, phone call', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'pass on', 'pass on', '将……传给；将……交给', '/pæs ɑːn/', 'to give something to someone so that they have it instead of you', 'Could you pass on the message to him?', 'pass on, message, phone call', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'apology', 'apology', '道歉；认错；谢罪', '/əˈpɑːlədʒi/', 'an act of saying that you are sorry for something wrong you have done', 'I have an apology to make to you — I''m afraid I opened your letter by mistake.', 'apology, phone call, message', 1),

    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Secretary', NULL, 'Good morning, ABC Company. How may I help you?', '早上好，这里是 ABC 公司。我能帮您什么？', NULL, NULL, NULL, 'company, phone call', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Tom', NULL, 'Hello, I would like to speak to Mr. Jones, please.', '你好，我想和 Jones 先生通话。', NULL, NULL, NULL, 'speak to, phone call', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Secretary', NULL, 'Who''s calling, please?', '请问您是哪位？', NULL, NULL, NULL, 'who is calling, phone call', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Tom', NULL, 'It''s Tom White from EFG Company.', '我是 EFG 公司的 Tom White。', NULL, NULL, NULL, 'calling, company', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Secretary', NULL, 'May I ask what it''s about?', '请问是什么事？', NULL, NULL, NULL, 'what it is about, phone call', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Tom', NULL, 'Yes, of course. I have an appointment with Mr. Jones today, but something came up and I won''t be able to make it.', '当然。我今天和 Jones 先生有预约，但临时出了点事，我无法赴约。', NULL, NULL, NULL, 'appointment, something came up', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Secretary', NULL, 'Okay. But he''s in a meeting at the moment.', '好的。不过他现在正在开会。', NULL, NULL, NULL, 'in a meeting, phone call', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Tom', NULL, 'Do you know when he''ll be available, please?', '请问您知道他什么时候有空吗？', NULL, NULL, NULL, 'available, phone call', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'dialogue', '示范对话', 2, 'dialogue', 109, 'Secretary', NULL, 'He''ll be back at 11 a.m.', '他上午 11 点回来。', NULL, NULL, NULL, 'be back, appointment', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'dialogue', '示范对话', 2, 'dialogue', 110, 'Tom', NULL, 'Okay. Please pass on my apologies to Jones.', '好的。请代我向 Jones 先生致歉。', NULL, NULL, NULL, 'pass on apologies, phone call', 1),

    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Hello, this is Jack and I have an appointment with Mr. Jones today.', '你好，我是 Jack，今天和 Jones 先生有预约。', NULL, '根据课件提示补全。', NULL, 'appointment, phone call', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes, Jack. You are scheduled for 3 p.m.', '好的，Jack。您预约在下午 3 点。', NULL, NULL, NULL, 'scheduled, appointment', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Actually, something came up and I won''t be able to make it. Could you please reschedule my appointment?', '实际上临时出了点事，我无法赴约。您能帮我重新安排预约吗？', NULL, NULL, NULL, 'be able to, reschedule', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Sure. No problem. Mr. Jones will be available at 4 p.m. the day after tomorrow.', '当然，没问题。Jones 先生后天下午 4 点有空。', NULL, NULL, NULL, 'available, reschedule', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'That would be fine. Please pass on my apologies to Mr. Jones.', '那很好。请代我向 Jones 先生致歉。', NULL, NULL, NULL, 'pass on, apologies', 1),

    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you ever dialed the wrong number? What happened? How did you feel?', '你曾拨错号码吗？发生了什么？你感觉如何？', NULL, '可以谈感到尴尬或觉得有趣。', NULL, 'wrong number, phone call', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'How often do you use your mobile phone? What''s your favorite smartphone brand? And why?', '你多久使用一次手机？你最喜欢哪个智能手机品牌？为什么？', NULL, '可谈几乎每天都用，难以想象没有手机的生活；iPhone 设计优美、体验流畅、iOS 强大；华为、小米、OPPO、vivo 价格选择多，并有适合中国市场的功能。', NULL, 'mobile phone, smartphone, brand', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Do you agree with the idea that students can take mobile phones to school?', '你同意学生带手机去学校吗？', NULL, '同意：便于和父母保持联系，路上发生事情时可求助。不同意：可能在课堂或深夜打游戏、看视频、发过多消息，影响学习和健康。', NULL, 'students, mobile phone, school', 1),

    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I would like to speak to Mr. Jones, please.\nWho''s calling, please?', '复习：appointment / be able to / available / pass on / apology。', NULL, NULL, NULL, 'review, phone calls', 1),

    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Introduce yourself', 'Hello, this is Lily speaking.', '你好，我是 Lily。', NULL, '课后拓展：电话常用表达。', NULL, 'phone call, introduce yourself', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Ask who is calling', 'May I ask who is calling? Could I have your name, please?', '请问是哪位打来的？可以告诉我您的姓名吗？', NULL, '课后拓展：电话常用表达。', NULL, 'who is calling, phone call', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Ask to speak with someone', 'Can I speak to Jane?', '我可以和 Jane 通话吗？', NULL, '课后拓展：电话常用表达。', NULL, 'speak to, phone call', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Put someone on the phone', 'Just a moment, please. I will put her on.', '请稍等，我让她接电话。', NULL, '课后拓展：电话常用表达。', NULL, 'just a moment, phone call', 1),
    ('making-phone-calls', 'Chapter 4 · Daily Life', 'Lesson 33 · Making Phone Calls', 33, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'Leave a message', 'Would you like to leave a message? Should I ask her to call you back?', '您要留言吗？需要我请她回电吗？', NULL, '课后拓展：电话常用表达。', NULL, 'leave a message, call back', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 34 · A Visit to the Hospital (doc/112318_809_A Visit to the Hospital.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'temperature', 'temperature', '温度；体温', '/ˈtemprətʃər/', 'the measured amount of heat in a place or in the body', 'The doctor examined him and took his temperature.', 'temperature, hospital, health', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'flu', 'flu', '流行性感冒；流感', '/fluː/', 'a common infectious illness that causes fever and headache', 'There are lots of people off school this week with flu.', 'flu, hospital, health', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'medicine', 'medicine', '药；药物；药剂', '/ˈmedɪsn/', 'a substance, especially in the form of a liquid or a pill, that is a treatment for illness or injury', 'Did you take your medicine?', 'medicine, hospital, health', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'pharmacy', 'pharmacy', '药店；药房；药品部', '/ˈfɑːrməsi/', 'a shop or part of a shop in which medicines are prepared and sold', 'If your pharmacy doesn''t have the product you want in stock, ask them to order it for you.', 'pharmacy, medicine, hospital', 1),

    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Doctor', NULL, 'Good morning, Mr. Jones. What''s wrong?', '早上好，Jones 先生。您哪里不舒服？', NULL, NULL, NULL, 'doctor, hospital', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Jones', NULL, 'Morning. I feel very ill. I''m coughing and I feel hot and cold all the time.', '早上好。我感觉很不舒服，一直咳嗽，而且总觉得一会儿冷一会儿热。', NULL, NULL, NULL, 'ill, coughing, symptoms', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Doctor', NULL, 'Let me take your temperature. How long have you had the symptoms?', '让我量一下体温。你有这些症状多久了？', NULL, NULL, NULL, 'take temperature, symptoms', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Jones', NULL, 'They started about a day ago.', '大约一天前开始的。', NULL, NULL, NULL, 'symptoms, hospital', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Doctor', NULL, 'Yes, your temperature is very high. You have the flu. You''ll have to go home and stay in bed until it gets better. Drink lots of water.', '是的，你的体温很高。你得了流感。你需要回家卧床休息，直到好转，多喝水。', NULL, NULL, NULL, 'flu, stay in bed, water', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Jones', NULL, 'Can you give me some medicine?', '您能给我开些药吗？', NULL, NULL, NULL, 'medicine, doctor', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Doctor', NULL, 'Of course. I''ll write you a prescription and you can collect the medicine from the pharmacy.', '当然。我会给你开处方，你可以去药房取药。', NULL, NULL, NULL, 'prescription, pharmacy', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Jones', NULL, 'Okay, thank you.', '好的，谢谢。', NULL, NULL, NULL, 'thanks, hospital', 1),

    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Doctor, what''s wrong with my mom?', '医生，我妈妈怎么了？', NULL, '根据课件提示补全。', NULL, 'doctor, hospital', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'She''s got the flu. I want you to monitor her temperature.', '她得了流感。我希望你监测她的体温。', NULL, NULL, NULL, 'flu, temperature', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'How often should I check it?', '我应该多久量一次？', NULL, NULL, NULL, 'temperature, hospital', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Once every four hours. And she''ll have to go home and stay in bed until it gets better.', '每四小时一次。而且她需要回家卧床休息，直到好转。', NULL, NULL, NULL, 'stay in bed, flu', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Thank you. By the way, can you give us some medicine?', '谢谢。顺便问一下，您能给我们开些药吗？', NULL, NULL, NULL, 'medicine, doctor', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Okay, I''ll write you a prescription and you can collect the medicine from the pharmacy.', '好的，我会给你开处方，你可以去药房取药。', NULL, NULL, NULL, 'prescription, pharmacy', 1),

    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'When you have a cold, what do you usually do? Please explain.', '感冒时你通常做什么？请解释。', NULL, '可以待在家里充分休息和睡眠，并喝足够的水。', NULL, 'cold, health, hospital', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'If your friend were sick and in the hospital, what would you do to cheer him or her up? What gifts would you buy?', '如果朋友生病住院，你会怎样让他／她开心？会买什么礼物？', NULL, '可以做一个好的倾听者，不急着给建议或说“振作”；寄亲笔便条或贺卡，送对方喜欢的礼物。', NULL, 'friend, hospital, gift', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'What kind of exercise, if any, do you do, and how often do you do it? What effects does it have on you?', '你做什么运动？多久做一次？它对你有什么影响？', NULL, '可谈慢跑、瑜伽、游泳、足球、篮球或羽毛球。慢跑可以预防疾病、帮助减重、提高自信并缓解压力。', NULL, 'exercise, health, jogging', 1),

    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'How long have you had the symptoms?\nYou''ll have to go home and stay in bed until it gets better.\nI''ll write you a prescription and you can collect the medicine from the pharmacy.', '复习：temperature / flu / medicine / pharmacy。', NULL, NULL, NULL, 'review, hospital', 1),

    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Obstetrics and Gynecology Hospital', 'Obstetrics and Gynecology Hospital', '妇产科医院', NULL, '课后拓展：医院类型。', NULL, 'obstetrics, gynecology, hospital', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Children''s Hospital', 'Children''s Hospital', '儿童医院', NULL, '课后拓展：医院类型。', NULL, 'children, hospital', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Stomatology Hospital', 'Stomatology Hospital', '口腔科医院', NULL, '课后拓展：医院类型。', NULL, 'stomatology, hospital', 1),
    ('a-visit-to-the-hospital', 'Chapter 4 · Daily Life', 'Lesson 34 · A Visit to the Hospital', 34, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'General Hospital', 'General Hospital', '综合医院', NULL, '课后拓展：医院类型。', NULL, 'general hospital, health', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 35 · At the Amusement Park (doc/112811_809_At the Amusement Park.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'roller coaster', 'roller coaster', '过山车', '/ˈroʊlər koʊstər/', 'an exciting entertainment in an amusement park, like a fast train that goes up and down steep slopes and around sudden bends', 'Let''s have another ride on the roller coaster.', 'roller coaster, amusement park', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'thrill', 'thrill', '兴奋；激动；紧张感', '/θrɪl/', 'a feeling of extreme excitement, usually caused by something pleasant', 'The video shows the thrills of motor racing.', 'thrill, amusement park', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'adventure', 'adventure', '冒险；历险；奇遇', '/ədˈventʃər/', 'an unusual, exciting, and possibly dangerous activity, trip, or experience', 'She had some exciting adventures in Egypt.', 'adventure, amusement park', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'confess', 'confess', '坦白；供认；承认', '/kənˈfes/', 'to admit that you have done something wrong or something that you feel guilty or bad about', 'He has confessed to the murder.', 'confess, amusement park', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'scared', 'scared', '惊恐的；恐惧的；害怕的', '/skerd/', 'frightened or worried', 'He''s scared of spiders.', 'scared, amusement park', 1),

    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Betty', NULL, 'Which way is the roller coaster, Don?', 'Don，过山车往哪边走？', NULL, NULL, NULL, 'roller coaster, amusement park', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Don', NULL, 'Let me check the map. Oh, it should be right around the corner from the bumper cars.', '让我看看地图。哦，它应该就在碰碰车拐角附近。', NULL, NULL, NULL, 'map, bumper cars', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Betty', NULL, 'Let''s go on the roller coaster next! I love thrill rides!', '接下来我们坐过山车吧！我喜欢刺激的游乐项目！', NULL, NULL, NULL, 'thrill rides, roller coaster', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Don', NULL, 'Do you think maybe we could go on something slower first? We just had lunch.', '你觉得我们能不能先玩个慢一点的项目？我们刚吃完午饭。', NULL, NULL, NULL, 'slower ride, amusement park', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Betty', NULL, 'Where''s your sense of adventure, Don?', 'Don，你的冒险精神呢？', NULL, NULL, NULL, 'sense of adventure, amusement park', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Don', NULL, 'Betty, there''s something I need to confess: I''m scared to go on the roller coaster.', 'Betty，有件事我得坦白：我害怕坐过山车。', NULL, NULL, NULL, 'confess, scared, roller coaster', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Betty', NULL, 'Don''t worry, I''ll hold your hand during the ride.', '别担心，游玩时我会握着你的手。', NULL, NULL, NULL, 'do not worry, ride', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Don', NULL, 'All right, then. Let''s go for it! Roller coaster, here we come!', '那好吧。我们去玩吧！过山车，我们来了！', NULL, NULL, NULL, 'go for it, roller coaster', 1),

    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Let''s go on the roller coaster next. It must be very exciting.', '我们接下来去坐过山车吧，一定很刺激。', NULL, '根据课件提示补全。', NULL, 'roller coaster, amusement park', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I''m sorry, I need to confess: I''m scared to go on the roller coaster.', '抱歉，我得坦白：我害怕坐过山车。', NULL, NULL, NULL, 'confess, scared', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Oh, come on! Where''s your sense of adventure? Don''t you love thrill rides? I''ll hold your hand during the ride. Don''t worry.', '哦，别这样！你的冒险精神呢？你不喜欢刺激的游乐项目吗？游玩时我会握着你的手，别担心。', NULL, NULL, NULL, 'adventure, thrill rides', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Okay, then. Let''s go for it!', '好吧，那我们去玩吧！', NULL, NULL, NULL, 'go for it, amusement park', 1),

    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you ever visited an amusement park?', '你去过游乐园吗？', NULL, '可以谈游乐园名称、地点、和谁一起去，以及玩过哪些项目。', NULL, 'amusement park, rides', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Who do you think enjoy theme parks the most — adults or children?', '你认为谁最喜欢主题公园，成年人还是儿童？', NULL, '成年人可从繁忙、压力大的工作中放松，并通过游乐设施寻找刺激；儿童觉得那里像仙境或梦想之地，可以自在地与童话、卡通或漫画人物互动。', NULL, 'theme park, adults, children', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Do you have any plans to go to an amusement park in the near future?', '你近期有去游乐园的计划吗？', NULL, '可谈去迪士尼、环球影城或欢乐谷，并说明和父母、朋友、同学、室友或同事一起；也可从健康与安全方面说明没有计划。', NULL, 'amusement park, plans, travel', 1),

    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I love thrill rides!\nDo you think maybe we could go on something slower first?\nWhere''s your sense of adventure, Don?\nI''m scared to go on the roller coaster.', '复习：roller coaster / thrill / adventure / confess / scared。', NULL, NULL, NULL, 'review, amusement park', 1),

    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'bumper car', 'bumper car', '碰碰车', NULL, '课后拓展：游乐园项目。', NULL, 'bumper car, amusement park', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'pirate ship', 'pirate ship', '海盗船', NULL, '课后拓展：游乐园项目。', NULL, 'pirate ship, amusement park', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Ferris wheel', 'Ferris wheel', '摩天轮', NULL, '课后拓展：游乐园项目。', NULL, 'Ferris wheel, amusement park', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'carousel', 'carousel', '旋转木马', NULL, '课后拓展：游乐园项目。', NULL, 'carousel, amusement park', 1),
    ('at-the-amusement-park', 'Chapter 4 · Daily Life', 'Lesson 35 · At the Amusement Park', 35, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'firework display', 'firework display', '烟火表演', NULL, '课后拓展：游乐园项目。', NULL, 'firework display, amusement park', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 38 · Going to the Movies (doc/113577_810_Going to the Movies.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'scary', 'scary', '吓人的；恐怖的', '/ˈskeri/', 'frightening', 'She''d had a dream in which scary monsters were chasing her.', 'scary, horror movie, movies', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'comedy', 'comedy', '喜剧；喜剧片', '/ˈkɑːmədi/', 'a type of film, play, or book that is intentionally funny in its characters or action', 'His latest movie is described as a romantic comedy.', 'comedy, movies, entertainment', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'action movie', 'action movie', '动作片', '/ˈækʃn muːvi/', 'a genre of movie with a fast-moving plot, usually containing scenes of violence', 'I like watching action movies.', 'action movie, movies, entertainment', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'pick somebody up', 'pick somebody up', '（通常指开车）接载某人', '/pɪk ʌp/', 'to go to the place where a person or thing waiting to be collected is and take them away, often in a car', 'I will drive to the airport tomorrow to pick you up.', 'pick up, movies, car', 1),

    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Betty', NULL, 'Hi, Sarah. What are you doing this weekend?', '嗨，Sarah。这个周末你做什么？', NULL, NULL, NULL, 'weekend, movies', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Sarah', NULL, 'Not much. What are you doing?', '没什么。你做什么？', NULL, NULL, NULL, 'weekend, movies', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Betty', NULL, 'I wanted to know if you would like to go to the movies with me.', '我想问你是否愿意和我一起去看电影。', NULL, NULL, NULL, 'go to the movies, invitation', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Sarah', NULL, 'That sounds nice. What kind of movie?', '听起来不错。看什么类型的电影？', NULL, NULL, NULL, 'kind of movie, movies', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Betty', NULL, 'Do you like scary movies, horror movies, or comedies?', '你喜欢恐怖片还是喜剧片？', NULL, NULL, NULL, 'scary movies, comedies', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Sarah', NULL, 'Neither. I like action movies. Can we see "Skyfall"?', '都不喜欢。我喜欢动作片。我们能看《Skyfall》吗？', NULL, NULL, NULL, 'action movies, Skyfall', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Betty', NULL, 'Sure, I love action movies. I will pick you up at 7 p.m.', '当然，我喜欢动作片。我晚上 7 点去接你。', NULL, NULL, NULL, 'pick you up, action movies', 1),

    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Do you want to see a movie today after school?', '今天放学后你想看电影吗？', NULL, '根据课件提示补全。', NULL, 'see a movie, after school', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Sure. What movie do you want to see?', '当然。你想看什么电影？', NULL, NULL, NULL, 'movie, entertainment', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Do you like scary movies?', '你喜欢恐怖片吗？', NULL, NULL, NULL, 'scary movies, horror', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'No, they are horrible. I like comedies, because they make me laugh.', '不喜欢，它们太可怕了。我喜欢喜剧，因为它们能让我发笑。', NULL, NULL, NULL, 'comedies, scary movies', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Okay. I will pick you up after school.', '好的。放学后我去接你。', NULL, NULL, NULL, 'pick you up, movies', 1),

    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you prefer watching movies at home or at a movie theater? Why?', '你更喜欢在家还是在电影院看电影？为什么？', NULL, '在家：去电影院可能贵，也可能有人说话或踢座椅；在电影院：视听效果更好，更能专注于电影，较少被其他事情分心。', NULL, 'movies, home, movie theater', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'What is your favorite movie? Who is your favorite movie star? Why?', '你最喜欢哪部电影？最喜欢哪位电影明星？为什么？', NULL, '可说明电影名称、主角、观看的时间和地点、电影内容，以及喜欢它的原因。', NULL, 'favorite movie, movie star', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Have you ever seen the same movie more than once? Do you usually eat something while you are watching a movie at the cinema?', '你看过同一部电影不止一次吗？在电影院看电影时通常会吃东西吗？', NULL, '可以谈独自看后又与父母、朋友或同学重看；可吃爆米花，也可因不想分心而不吃东西。', NULL, 'movies, popcorn, cinema', 1),

    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I wanted to know if you would like to go to the movies with me.\nDo you like scary movies, horror movies, or comedies?', '复习：scary / comedy / action movie / pick somebody up。', NULL, NULL, NULL, 'review, movies', 1),

    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'feature film', 'feature film', '剧情片', NULL, '课后拓展：电影类型。', NULL, 'feature film, movie', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'suspense film', 'suspense film', '悬疑片', NULL, '课后拓展：电影类型。', NULL, 'suspense film, movie', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'romance film', 'romance film', '爱情片', NULL, '课后拓展：电影类型。', NULL, 'romance film, movie', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'musical film', 'musical film', '歌舞片', NULL, '课后拓展：电影类型。', NULL, 'musical film, movie', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'action film', 'action film', '动作片', NULL, '课后拓展：电影类型。', NULL, 'action film, movie', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'documentary film', 'documentary film', '纪录片', NULL, '课后拓展：电影类型。', NULL, 'documentary film, movie', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'extra', '拓展学习', 6, 'extra', 507, NULL, 'literary film', 'literary film', '文艺片', NULL, '课后拓展：电影类型。', NULL, 'literary film, movie', 1),
    ('going-to-the-movies', 'Chapter 5 · Entertainment', 'Lesson 38 · Going to the Movies', 38, 'extra', '拓展学习', 6, 'extra', 508, NULL, 'cartoon film', 'cartoon film', '动画电影', NULL, '课后拓展：电影类型。', NULL, 'cartoon film, movie', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 39 · A Visit to the Zoo (doc/113741_810_A Visit to the Zoo.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'captivity', 'captivity', '关押；囚禁', '/kæpˈtɪvəti/', 'the situation in which a person or animal is kept somewhere and is not allowed to leave', 'He was held in captivity for three years.', 'captivity, zoo, animals', 1),
    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'upside', 'upside', '优点；好处；有利的一面', '/ˈʌpsaɪd/', 'the advantage of a situation', 'It''s annoying that we can''t travel until Thursday, but the upside is that tickets are cheaper then.', 'upside, zoo, animals', 1),
    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'check out', 'check out', '看一看；瞧瞧', '/tʃek aʊt/', 'to look at something, especially something new', 'Hey! Check out my new computer.', 'check out, zoo, animals', 1),
    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'alpaca', 'alpaca', '（南美的）羊驼', '/ælˈpækə/', 'a South American animal with a long neck and long hair that looks like a llama', 'Can you tell the difference between an alpaca and a llama?', 'alpaca, zoo, animals', 1),

    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Karen', NULL, 'I love coming to the zoo! There are so many cool animals to see.', '我喜欢来动物园！有这么多很酷的动物可以看。', NULL, NULL, NULL, 'zoo, animals', 1),
    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Steve', NULL, 'I''ll admit that I like looking at the animals, but sometimes I feel bad for them because they have to live their lives in captivity.', '我承认我喜欢看动物，但有时我为它们难过，因为它们不得不一生被圈养。', NULL, NULL, NULL, 'captivity, animals, zoo', 1),
    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Karen', NULL, 'That''s true, but there are some upsides to it. For example, the animals don''t have to worry about getting enough to eat. There are also some animals who have lost the ability to live in the wild, and living in zoos is the best option for them.', '确实，但也有一些好处。例如，动物不用担心食物不够。有些动物已经失去了在野外生存的能力，对它们来说住在动物园是最好的选择。', NULL, NULL, NULL, 'upsides, wild, zoo', 1),
    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Steve', NULL, 'You''re right. Anyway, which animal do you want to see first?', '你说得对。话说回来，你想先看哪种动物？', NULL, NULL, NULL, 'which animal, zoo', 1),
    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Karen', NULL, 'I definitely want to see the pandas.', '我一定想看熊猫。', NULL, NULL, NULL, 'pandas, zoo', 1),
    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Steve', NULL, 'Yeah, it''s one of the most popular animals here. Let''s check out the alpacas first because they''re right over there. They''re so cute!', '是的，熊猫是这里最受欢迎的动物之一。我们先去看看羊驼吧，它们就在那边，太可爱了！', NULL, NULL, NULL, 'check out, alpacas, zoo', 1),

    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Do you love coming to the zoo?', '你喜欢来动物园吗？', NULL, '根据课件提示补全。', NULL, 'zoo, animals', 1),
    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes, of course. Animals are so cute, but sometimes I feel bad for them because they''re never free. Some animals that are kept in captivity have been known to go insane.', '当然。动物很可爱，但有时我为它们难过，因为它们从不自由。有些被圈养的动物甚至会发疯。', NULL, NULL, NULL, 'captivity, animals, zoo', 1),
    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'That''s true, but there are some upsides to it. For example, zoos can keep injured and endangered animals safe.', '确实，不过也有一些好处。例如，动物园能保护受伤和濒危动物。', NULL, NULL, NULL, 'upsides, endangered animals', 1),
    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Well, that''s true. Let''s go check out the alpacas, and can you take my picture with the alpacas in the background? They''re so lovely.', '嗯，确实如此。我们去看看羊驼吧，你能给我拍张以羊驼为背景的照片吗？它们太可爱了。', NULL, NULL, NULL, 'check out, alpacas, picture', 1),

    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you like animals? Do you think animals can be people''s best friends?', '你喜欢动物吗？你认为动物能成为人类最好的朋友吗？', NULL, '有些动物喜欢陪伴人类，能在难过时安慰人，也有时能救人；如果尊重动物，大多数动物会对人友好。', NULL, 'animals, pets, friendship', 1),
    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Describe a pet you would like to own.', '描述一种你想养的宠物。', NULL, '可以说明它是什么、如何照顾它并让它快乐，以及养它的好处。', NULL, 'pet, animals, zoo', 1),
    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'What are the pros and cons of keeping a pet?', '养宠物有什么优点和缺点？', NULL, '优点：帮助人们对抗抑郁和孤独、增加安全感、培养责任感。缺点：花钱多、可能对宠物过敏，搬家或旅行时携带宠物困难。', NULL, 'pets, pros and cons, animals', 1),

    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Which animal do you want to see first?\nThere are so many cool animals to see.', '复习：captivity / upside / check out / alpaca。', NULL, NULL, NULL, 'review, zoo', 1),

    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Giant panda appearance', 'The giant panda is easily recognized by the large, distinctive black patches around its eyes, over the ears, and across its round body.', '大熊猫很容易辨认：眼睛周围、耳朵上方和圆润身体上都有明显的大黑斑。', NULL, '课后拓展：大熊猫。', NULL, 'giant panda, zoo, animals', 1),
    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Giant panda habitat', 'The giant panda is a terrestrial animal and primarily spends its life in the bamboo forests of the Qinling Mountains and in the hilly province of Sichuan.', '大熊猫是陆生动物，主要生活在秦岭的竹林和多山的四川省。', NULL, '课后拓展：大熊猫。', NULL, 'giant panda, habitat, bamboo', 1),
    ('a-visit-to-the-zoo', 'Chapter 5 · Entertainment', 'Lesson 39 · A Visit to the Zoo', 39, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Habitat fragmentation', 'Roads and railroads are increasingly fragmenting the forest, which isolates panda populations and prevents mating, and forest destruction also reduces pandas'' access to bamboo.', '道路和铁路日益切割森林，使熊猫种群隔离并阻碍交配；森林破坏也减少了熊猫获得竹子的机会。', NULL, '课后拓展：大熊猫。', NULL, 'giant panda, forest, conservation', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 40 · Working out at the Gym (doc/113743_810_Working out at the Gym.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'gym', 'gym', '健身俱乐部；健身房', '/dʒɪm/', 'a club where you can go to exercise and keep fit', 'He works in a sports center instructing people in the use of the gym equipment.', 'gym, exercise, fitness', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'instructor', 'instructor', '教练', '/ɪnˈstrʌktər/', 'a person whose job is to teach people a practical skill', 'He worked as a dance instructor in London before setting himself up in New York.', 'instructor, gym, fitness', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'wonder', 'wonder', '疑惑；想知道', '/ˈwʌndər/', 'to ask yourself questions or express a wish to know about something', 'He''s starting to wonder whether he did the right thing in accepting this job.', 'wonder, gym, exercise', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'cardio', 'cardio', '有氧运动', '/ˈkɑːrdioʊ/', 'physical exercise that increases the rate at which your heart works', 'My workout usually includes 15 to 20 minutes of cardio.', 'cardio, gym, exercise', 1),

    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Patrick', NULL, 'Hey! My name is Patrick. I''m new to the gym.', '嗨！我叫 Patrick，我刚来这家健身房。', NULL, NULL, NULL, 'new to the gym, fitness', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Steve', NULL, 'Hey Patrick. I''m Steve. I''m the instructor here. Tell me, how can I help you?', '嗨，Patrick。我是 Steve，这里的教练。告诉我，我能帮你什么？', NULL, NULL, NULL, 'instructor, gym', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Patrick', NULL, 'I was wondering if you could suggest some exercises to reduce my love handles.', '我想知道你能否建议一些运动来减掉我的腰间赘肉。', NULL, '对话中 I was wondering 相当于 I was thinking / I want to know。', NULL, 'wondering, love handles, exercise', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Steve', NULL, 'Sure. This is a quite common problem among girls too.', '当然。这也是女孩中很常见的问题。', NULL, NULL, NULL, 'common problem, fitness', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Patrick', NULL, 'Yeah! I sit all day, and never really get a chance to exercise.', '是啊！我整天坐着，几乎从没有机会运动。', NULL, NULL, NULL, 'exercise, sedentary', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Steve', NULL, 'All right! You''ll need to do a lot of cardio to fix that.', '好的！你需要做很多有氧运动来解决这个问题。', NULL, NULL, NULL, 'cardio, gym, exercise', 1),

    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Hi, do you come to the gym at the same time every day?', '嗨，你每天都在同一时间来健身房吗？', NULL, '根据课件提示补全。', NULL, 'gym, exercise', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes, I work here as an instructor, so it''s pretty much the same time every day. What about you?', '是的，我在这里当教练，所以每天基本都是同一时间。你呢？', NULL, NULL, NULL, 'instructor, gym', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Well, today is my first day at the gym, and I was wondering if I should get a treadmill at home.', '今天是我第一次来健身房，我想知道我是否应该在家买一台跑步机。', NULL, NULL, NULL, 'wondering, treadmill, gym', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Well, that''s not a good idea if you''re going to be a regular at the gym.', '如果你打算经常来健身房，那不是个好主意。', NULL, NULL, NULL, 'regular, gym, fitness', 1),

    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'What are some of the benefits of playing sports? Are people in your country crazy about sports?', '运动有什么好处？你所在国家的人很热衷运动吗？', NULL, '运动能培养成就感，从而形成积极的自我形象；参与体育活动能减少体脂、控制体重并改善健康。', NULL, 'sports, benefits, health', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Describe a game or sport that you enjoy playing.', '描述一项你喜欢玩的游戏或运动。', NULL, '可以说明这项运动是什么、和谁一起玩、在哪里玩，并解释为什么它有益健康。', NULL, 'game, sport, health', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'How do you feel about extreme sports? Would you like to try any of those?', '你怎么看极限运动？你想尝试其中的一种吗？', NULL, '可以从刺激、危险、害怕或酷等感受谈起。', NULL, 'extreme sports, gym, adventure', 1),

    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I was wondering if you could suggest some exercises to reduce my love handles.\nYou''ll need to do a lot of cardio to fix that.', '复习：gym / instructor / wonder / cardio。', NULL, NULL, NULL, 'review, gym', 1),

    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'hula hoop', 'hula hoop', '呼啦圈', NULL, '课后拓展：健身器材。', NULL, 'hula hoop, gym', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Swiss ball', 'Swiss ball', '健身球', NULL, '课后拓展：健身器材。', NULL, 'Swiss ball, gym', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'yoga mat', 'yoga mat', '瑜伽垫', NULL, '课后拓展：健身器材。', NULL, 'yoga mat, gym', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'dumbbell', 'dumbbell', '哑铃', NULL, '课后拓展：健身器材。', NULL, 'dumbbell, gym', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'barbell', 'barbell', '杠铃', NULL, '课后拓展：健身器材。', NULL, 'barbell, gym', 1),
    ('working-out-at-the-gym', 'Chapter 5 · Entertainment', 'Lesson 40 · Working out at the Gym', 40, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'treadmill', 'treadmill', '跑步机', NULL, '课后拓展：健身器材。', NULL, 'treadmill, gym', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 41 · Visiting a Museum (doc/113770_810_Visiting a Museum.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'audio', 'audio', '声音的；录音的；播音的；音频的', '/ˈɔːdioʊ/', 'connected with sound and the recording and broadcasting of sound', 'She uses her vocal training to record audio tapes of books for blind people.', 'audio, museum, guide', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'permanent', 'permanent', '长久的；永久的；永恒的', '/ˈpɜːrmənənt/', 'lasting for a long time or forever', 'The museum will have a permanent exhibition of 60 vintage cars.', 'permanent, museum, exhibition', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'except for', 'except for', '除……之外', '/ɪkˈsept fɔːr/', 'not including; but not', 'I''ve read all of the books he has written except for the latest one.', 'except for, museum, exhibition', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'photography', 'photography', '照相术；摄影', '/fəˈtɑːɡrəfi/', 'the activity or job of taking photographs or filming', 'Her hobbies include hiking and photography.', 'photography, museum, photos', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'exhibition', 'exhibition', '展览（会）；表现；显示', '/ˌeksɪˈbɪʃn/', 'an event at which objects such as paintings are shown to the public, or the act of showing them', 'There''s a new exhibition of sculpture at the city gallery.', 'exhibition, museum, art', 1),

    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Patrick', NULL, 'Excuse me. Could you tell me if the museum offers guided tours?', '打扰一下。请问博物馆提供导览吗？', NULL, NULL, NULL, 'guided tours, museum', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Steve', NULL, 'The only guides we offer are audio guides. They cover information about the museum''s permanent collection and special exhibitions. You can rent players over there.', '我们只提供语音导览。它们介绍博物馆的永久藏品和特别展览。你可以在那边租播放器。', NULL, NULL, NULL, 'audio guides, permanent collection', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Patrick', NULL, 'Oh, that sounds great! Are all of the exhibitions open to the public today?', '哦，听起来不错！今天所有展览都对公众开放吗？', NULL, NULL, NULL, 'exhibitions, public', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Steve', NULL, 'All except for the East Wing on the second floor.', '除了二楼东翼展厅，其他都开放。', NULL, NULL, NULL, 'except for, East Wing', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Patrick', NULL, 'Okay. By the way, may I take photos in the museum?', '好的。顺便问一下，我可以在博物馆里拍照吗？', NULL, NULL, NULL, 'take photos, museum', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Steve', NULL, 'You may, but flash photography is not allowed.', '可以，但不允许使用闪光灯摄影。', NULL, NULL, NULL, 'flash photography, museum', 1),

    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Excuse me. Could you tell me if the museum offers audio guides?', '打扰一下。请问博物馆提供语音导览吗？', NULL, '根据课件提示补全。', NULL, 'audio guides, museum', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes, of course. They cover information about the permanent collection and special exhibitions. You can rent players over there at the audio-guide desk.', '当然。它们介绍永久藏品和特别展览。你可以在那边的语音导览柜台租播放器。', NULL, NULL, NULL, 'permanent collection, exhibitions', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'That''s really helpful. I''m really looking forward to seeing the exhibition of paintings.', '这非常有帮助。我很期待看绘画展。', NULL, NULL, NULL, 'exhibition, paintings', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'That is one of our most popular attractions.', '那是我们最受欢迎的展览之一。', NULL, NULL, NULL, 'popular attraction, museum', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'By the way, may I take photos in the museum?', '顺便问一下，我可以在博物馆里拍照吗？', NULL, NULL, NULL, 'take photos, museum', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Yes, you can. But flash photography is not allowed.', '可以，但不允许使用闪光灯摄影。', NULL, NULL, NULL, 'flash photography, museum', 1),

    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Are there many, or any, museums or art galleries in your hometown?', '你的家乡有很多博物馆或美术馆吗？', NULL, '可以谈中国各类博物馆，例如现代艺术博物馆、科学博物馆和自然博物馆。', NULL, 'museums, art galleries, hometown', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Describe a museum that you visited.', '描述一家你参观过的博物馆。', NULL, '可以说明它在哪里、外观如何、有哪些设施，以及它对你的影响或你的感受。', NULL, 'museum, visit, art', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Do you think it''s appropriate for museums to sell things to visitors?', '你认为博物馆向参观者出售商品合适吗？', NULL, '合适：游客可留作纪念品或作为礼物送朋友。不合适：有些博物馆以很高价格向游客卖商品。', NULL, 'museum, souvenirs, visitors', 1),

    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Could you tell me if the museum offers guided tours?\nAre all of the exhibitions open to the public today?', '复习：audio / permanent / except for / photography / exhibition。', NULL, NULL, NULL, 'review, museum', 1),

    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'The British Museum', 'The British Museum, located in the Bloomsbury area of London, United Kingdom, is a public institution dedicated to human history, art and culture.', '大英博物馆位于英国伦敦布卢姆茨伯里地区，是一所致力于人类历史、艺术和文化的公共机构。', NULL, '课后拓展：大英博物馆。', NULL, 'British Museum, London, history, art', 1),
    ('visiting-a-museum', 'Chapter 5 · Entertainment', 'Lesson 41 · Visiting a Museum', 41, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Permanent collection', 'Its permanent collection numbers some 8 million works and is among the largest and most comprehensive in existence, documenting the story of human culture from its beginnings to the present. It is the first national public museum in the world.', '其永久藏品约有 800 万件，是现存规模最大、最全面的收藏之一，记录了从起源到现在的人类文化故事；它是世界上第一家国家级公共博物馆。', NULL, '课后拓展：大英博物馆。', NULL, 'permanent collection, museum, culture', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 42 · The Concert (doc/113794_810_The Concert.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'successful', 'successful', '成功的；达到目的的', '/səkˈsesfl/', 'achieving the results wanted or hoped for', 'My second attempt at making bread was a little more successful.', 'successful, concert, tickets', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'concert', 'concert', '现场演出；演唱会', '/ˈkɑːnsərt/', 'a live performance by a musician or group of musicians', 'I went to Bruno Mars'' concert last night. It was a blast!', 'concert, music, entertainment', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'row', 'row', '一排；一行；一列', '/roʊ/', 'a line of things, people, or animals arranged next to each other', 'We had seats in the front row of the theatre.', 'row, front row, concert', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'sell out', 'sell out', '卖光；售罄', '/sel aʊt/', 'to sell all of the supply that you have of something', 'We can sell out of the T-shirts in the first couple of hours.', 'sell out, sold out, concert tickets', 1),

    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Fiona', NULL, 'So, were you successful in buying tickets online for Jay Chou''s concert?', '那么，你成功在网上买到周杰伦演唱会的票了吗？', NULL, NULL, NULL, 'successful, tickets, concert', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Charlie', NULL, 'Not yet. Online ticket sales begin in ten minutes. But I''ve got my credit card ready. I just hope we''ll be able to get front-row seats this time.', '还没有。网上售票十分钟后开始，但我已经准备好信用卡了。我只希望这次能买到前排座位。', NULL, NULL, NULL, 'online ticket sales, front-row seats', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Patrick', NULL, 'I''ll be glad if we get tickets at all. Jay Chou''s concerts usually sell out within minutes.', '如果我们能买到票我就很高兴了。周杰伦的演唱会通常几分钟内就售罄。', NULL, NULL, NULL, 'sell out, concert tickets', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Steve', NULL, 'That''s true. By the way, I heard he always has really wonderful special guests in his shows.', '确实。顺便说一下，我听说他的演出总会有很棒的特别嘉宾。', NULL, NULL, NULL, 'special guests, concert', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Patrick', NULL, 'Yes. I wonder who''ll be his special guest this time.', '是的。我想知道这次谁会是他的特别嘉宾。', NULL, NULL, NULL, 'special guest, concert', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Steve', NULL, 'I don''t know, but I''m sure it''ll be someone really good.', '我不知道，但我相信会是很棒的人。', NULL, NULL, NULL, 'concert, special guest', 1),

    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Have you ever been to Jay Chou''s concert?', '你去过周杰伦的演唱会吗？', NULL, '根据课件提示补全。', NULL, 'Jay Chou, concert', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes, of course. His concert tickets usually sell out within minutes, but I was successful in buying the ticket for the "New Era World Tour" in 2010.', '当然。他的演唱会门票通常几分钟内售罄，但我成功买到了 2010 年“New Era World Tour”的票。', NULL, NULL, NULL, 'sell out, successful, concert', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'That''s true. I was lucky to snag the ticket too. And my seat was in the front row, which was pretty close to the stage. Jay really put on a great performance that night.', '确实。我也很幸运抢到了票。我的座位在前排，离舞台很近。那晚周杰伦的表演真的很精彩。', NULL, NULL, NULL, 'front row, stage, performance', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Yes, the whole crowd was singing and dancing along to his songs.', '是的，全场观众都跟着他的歌唱歌跳舞。', NULL, NULL, NULL, 'crowd, concert, music', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'The costumes were quite amazing as well.', '服装也非常惊艳。', NULL, NULL, NULL, 'costumes, concert', 1),

    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'What kind of music do you like? Do you listen to music while doing your work or homework?', '你喜欢什么类型的音乐？工作或做作业时会听音乐吗？', NULL, '可谈流行、摇滚、古典、舞曲、独立或 R&B 音乐。听音乐可减压、屏蔽噪音和干扰；不听则因为需要保持专注，不想被音乐分散注意力。', NULL, 'music, work, homework', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Can you play a musical instrument? If not, which musical instrument would you like to play?', '你会演奏乐器吗？如果不会，你想演奏什么乐器？', NULL, '可以说明想演奏或正在演奏的乐器、学习多久或需要多久，以及自己的水平或希望达到的熟练程度。', NULL, 'musical instrument, music, concert', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'How does music make you feel? Do you think music can heal sick people? Do you think that animals can enjoy music?', '音乐让你感觉如何？你认为音乐能疗愈病人吗？动物能享受音乐吗？', NULL, '音乐可能让人快乐、兴奋、悲伤或害怕；它可以改善情绪、减轻焦虑、提升动力。课件还举例说奶牛听舒缓音乐时会产更多奶。', NULL, 'music, feelings, animals', 1),

    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Were you successful in buying tickets online for Jay Chou''s concert?\nOnline ticket sales begin in ten minutes.\nI just hope we''ll be able to get front-row seats this time.', '复习：successful / concert / row / sell out。', NULL, NULL, NULL, 'review, concert', 1),

    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'guitar', 'guitar', '吉他', NULL, '课后拓展：乐队成员与乐器。', NULL, 'guitar, concert, music', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'bass guitar', 'bass guitar', '贝斯吉他；低音电吉他', NULL, '课后拓展：乐队成员与乐器。', NULL, 'bass guitar, concert, music', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'drums', 'drums', '鼓', NULL, '课后拓展：乐队成员与乐器。', NULL, 'drums, concert, music', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'keyboardist', 'keyboardist', '键盘手', NULL, '课后拓展：乐队成员与乐器。', NULL, 'keyboardist, concert, music', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'lead vocalist', 'lead vocalist', '主唱', NULL, '课后拓展：乐队成员与乐器。', NULL, 'lead vocalist, concert, music', 1),
    ('the-concert', 'Chapter 5 · Entertainment', 'Lesson 42 · The Concert', 42, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'keyboard', 'keyboard', '键盘', NULL, '课后拓展：乐队成员与乐器。', NULL, 'keyboard, concert, music', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 43 · Going to a Book Fair (doc/113801_810_Going to a Book Fair.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'fair', 'fair', '商品展销会；商品交易会', '/fer/', 'a large show at which people who work in a particular industry meet and sell and advertise their products', 'When he got bored he wandered around the book fair.', 'fair, book fair, books', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'illustrator', 'illustrator', '（尤指书籍的）插图画家', '/ˈɪləstreɪtər/', 'a person who draws pictures, especially for books', 'She models for an illustrator.', 'illustrator, book fair, books', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'line up', 'line up', '排队', '/laɪn ʌp/', 'to move so that people are standing in a line; queue up', 'Thousands of people lined up to buy tickets on opening night.', 'line up, queue up, book fair', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'be crowded with', 'be crowded with', '充满；拥挤；挤满', '/ˈkraʊdɪd/', 'to fill a place so there is little room to move', 'The roads are crowded with vehicles of all kinds.', 'crowded, book fair, people', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'signature', 'signature', '签名', '/ˈsɪɡnətʃər/', 'your name written by yourself, always in the same way, usually to show that something has been written or agreed by you', 'Please print your name clearly below your signature.', 'signature, autograph, book fair', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'vocabulary', '核心词汇', 1, 'vocabulary', 6, NULL, 'dawn', 'dawn', '拂晓；破晓；黎明', '/dɔːn/', 'the period in the day when light from the sun begins to appear in the sky', 'We left at the break of dawn.', 'dawn, book fair, early', 1),

    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Ryan', NULL, 'I''m so excited about tomorrow! The comic book fair is going to be much bigger than last year''s, and there will be a lot of authors and illustrators that we can meet.', '我对明天太兴奋了！漫画书展会比去年大得多，还有许多作者和插画家可以见。', NULL, NULL, NULL, 'comic book fair, authors, illustrators', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Albert', NULL, 'I think it will be great, too. I''m hoping to meet the creator of my favorite anime, Naruto. I want to get his autograph, so I have brought many copies of his comic books.', '我也觉得会很棒。我希望见到我最喜欢的动漫《火影忍者》的创作者。我想得到他的签名，所以带了很多本他的漫画书。', NULL, NULL, NULL, 'anime, autograph, comic books', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Ryan', NULL, 'If you''re going to do that, you''ll have to line up early. Once the fair is crowded with people, you might not even get a number to get your books signed.', '如果你要这样做，得早早排队。书展一旦挤满人，你可能连拿到签书号码都做不到。', NULL, NULL, NULL, 'line up, crowded, books signed', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Albert', NULL, 'Trust me. I plan to be at the fair''s entrance at the break of dawn.', '相信我。我计划黎明时分就到书展入口。', NULL, NULL, NULL, 'break of dawn, book fair', 1),

    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Did you go to the Hong Kong book fair last month?', '你上个月去香港书展了吗？', NULL, '根据课件提示补全。', NULL, 'Hong Kong book fair, books', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes, of course. It was a great day! I met a lot of authors and illustrators. How about you?', '当然。那天很棒！我见到了许多作者和插画家。你呢？', NULL, NULL, NULL, 'authors, illustrators, book fair', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I couldn''t manage to go. I had to work that day.', '我没能去，那天我必须工作。', NULL, NULL, NULL, 'book fair, work', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Well, the fair was crowded with people from all over the world. Some people didn''t even have a chance to get their favorite author''s autograph.', '书展挤满了来自世界各地的人。有些人甚至没机会得到最喜欢作者的签名。', NULL, NULL, NULL, 'crowded with, autograph, book fair', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Did you buy any book while you were there?', '你在那里买书了吗？', NULL, NULL, NULL, 'buy books, book fair', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Yes, I bought some of my favorite author''s early works at the fair.', '买了，我在书展买了几本我最喜欢作者的早期作品。', NULL, NULL, NULL, 'early works, book fair', 1),

    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'How often do you read? Why do you read?', '你多久阅读一次？为什么阅读？', NULL, '可以谈通常、经常、有时、每周一次或很少阅读；阅读能获得知识、了解他人的生活和经历，并探索不同的世界。', NULL, 'reading, books, book fair', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Describe a book you liked to read in your childhood.', '描述一本你童年喜欢读的书。', NULL, '可以说明作者、书的内容、何时读过，以及喜欢它的原因。', NULL, 'childhood book, reading', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Describe a book you would like to read again.', '描述一本你想再读一次的书。', NULL, '可以说明书的内容、阅读原因、学到的东西，以及希望重读的原因。', NULL, 'book, reading, discussion', 1),

    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I''m bringing copies of the comic books that I want him to sign.\nOnce the fair is crowded with people, you might not even get a number to get your books signed.', '复习：fair / illustrator / line up / be crowded with / signature / dawn。', NULL, NULL, NULL, 'review, book fair', 1),

    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'autograph', 'autograph', '名人签名', NULL, '课件注释：autograph 指名人的签名。', NULL, 'autograph, signature, book fair', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'dusk', 'dusk', '黄昏', NULL, '课件注释：dusk 是 dawn 的对应词。', NULL, 'dusk, dawn, book fair', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Hong Kong Book Fair', 'The first Hong Kong Book Fair was held in 1990, and it has become an annual major event in Hong Kong with the number of visitors reaching a new high every year.', '首届香港书展于 1990 年举办，现已成为香港一年一度的大型活动，访客数量每年创新高。', NULL, '课后拓展：香港书展。', NULL, 'Hong Kong Book Fair, annual event', 1),
    ('going-to-a-book-fair', 'Chapter 5 · Entertainment', 'Lesson 43 · Going to a Book Fair', 43, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Book fair activities', 'Apart from inviting people to visit and buy books, it also spares no effort in organizing diversified activities during the Book Fair period to improve the quality of the Fair.', '除了广泛邀请人们参观和买书，书展期间还不遗余力地举办多样活动，以提高书展质量。', NULL, '课后拓展：香港书展。', NULL, 'book fair, activities, books', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 46 · At the Library (doc/114184_811_At the Library.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'procedure', 'procedure', '流程；步骤；手续', '/prəˈsiːdʒər/', 'a way of doing something, especially the usual or correct way', 'What''s the procedure for opening a bank account?', 'procedure, library, borrowing', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'librarian', 'librarian', '图书管理员；图书馆馆长', '/laɪˈbreriən/', 'a person who is in charge of or works in a library', 'The librarian saved some rare books from the fire.', 'librarian, library, books', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'check out', 'check out', '借出（书等）', '/tʃek aʊt/', 'to borrow something from an official place, for example a book from a library', 'The book has been checked out in your name.', 'check out, library, books', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'wing', 'wing', '（建筑的）侧厅；厢房；翼', '/wɪŋ/', 'one of the parts of a large building that sticks out from the main part', 'I live in the west wing of the house.', 'wing, library, building', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'hand in', 'hand in', '递交；提交', '/hænd ɪn/', 'to give something to a person in authority, especially a piece of work or something that is lost', 'You must all hand in your homework by the end of next week.', 'hand in, library, homework', 1),

    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Tom', NULL, 'I want to borrow a book. Could you please tell me the procedure, please?', '我想借一本书。请问可以告诉我流程吗？', NULL, NULL, NULL, 'borrow a book, procedure', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Albert', NULL, 'Take the book to the librarian. She''ll check it out for you.', '把书拿给图书管理员。她会帮你办理借书。', NULL, NULL, NULL, 'librarian, check out', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Tom', NULL, 'Where can I find the librarian?', '我在哪里能找到图书管理员？', NULL, NULL, NULL, 'librarian, library', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Albert', NULL, 'There''s a desk on the extreme left of this wing. You''ll find her there.', '这个侧厅最左边有一张服务台，你能在那里找到她。', NULL, NULL, NULL, 'wing, librarian, library', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Tom', NULL, 'Do I need to hand in anything to get the book checked out?', '要借出这本书，我需要提交什么吗？', NULL, NULL, NULL, 'hand in, check out', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Albert', NULL, 'Yes. You''ll have to show your library card.', '需要。你得出示你的借书证。', NULL, NULL, NULL, 'library card, borrow books', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Tom', NULL, 'All right. Thank you.', '好的。谢谢。', NULL, NULL, NULL, 'thanks, library', 1),

    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Hi, I just got my library card. Do you know the procedure for borrowing books?', '嗨，我刚拿到借书证。你知道借书的流程吗？', NULL, '根据课件提示补全。', NULL, 'library card, procedure', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Sure. It''s very simple. Take the book you want to the librarian, and he''ll check it out for you.', '当然，很简单。把你想借的书拿给图书管理员，他会帮你办理借书。', NULL, NULL, NULL, 'librarian, check out', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'But where is the librarian?', '但图书管理员在哪里？', NULL, NULL, NULL, 'librarian, library', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Well, usually you can find him in the east wing of the library.', '通常你能在图书馆东翼找到他。', NULL, NULL, NULL, 'east wing, librarian', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Got it. Thanks!', '明白了，谢谢！', NULL, NULL, NULL, 'thanks, library', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Oh, and don''t forget to show him your library card!', '哦，别忘了向他出示你的借书证！', NULL, NULL, NULL, 'library card, borrow books', 1),

    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'How often do you go to a library? Why?', '你多久去一次图书馆？为什么？', NULL, '可谈通常、经常、有时、每周一次或很少去；原因可能是离家远、去那里花很长时间，或总是很拥挤。', NULL, 'library, reading, study', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'What''s the procedure for borrowing a book from the library in your city, town, or university?', '在你的城市、城镇或大学图书馆借书的流程是什么？', NULL, '可以先申请借书证，用机器扫描借书证和书，然后说明可借多久，例如一个月。', NULL, 'procedure, library card, borrow books', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Do you prefer reading or studying in the library, or at home? Why?', '你更喜欢在图书馆还是家里阅读／学习？为什么？', NULL, '图书馆可和别人一起读书或学习，更有动力；安静且少干扰，更专注；还能免费享受空调。', NULL, 'library, study, reading', 1),

    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Could you please tell me the procedure for something?\nDo I need to hand in anything to get the book checked out?', '复习：procedure / librarian / check out / wing / hand in。', NULL, NULL, NULL, 'review, library', 1),

    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Tianjin Binhai Library', 'Tianjin Binhai Library is nicknamed The Eye of Binhai because a luminous sphere that serves as an auditorium is in the center of the library. It appears like an iris and can be seen from the park outside through an eye-shaped opening.', '天津滨海图书馆被称为“滨海之眼”，因为图书馆中央有一个作为礼堂的发光球体；它看起来像虹膜，能从公园外透过眼形开口看到。', NULL, '课后拓展：天津滨海图书馆。', NULL, 'Tianjin Binhai Library, education, architecture', 1),
    ('at-the-library', 'Chapter 6 · Education', 'Lesson 46 · At the Library', 46, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Terraced bookshelves', 'It features floor-to-ceiling, terraced bookshelves able to hold 1.2 million books. However, rooms providing access to the upper tiers were not built, and book spines were printed onto the backs of the shelf space.', '馆内有从地板延伸到天花板的阶梯式书架，可容纳 120 万册图书；不过通往高层书架的房间未建成，书脊被印在书架空间背面。', NULL, '课后拓展：天津滨海图书馆。', NULL, 'bookshelves, library, architecture', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

COMMIT;
