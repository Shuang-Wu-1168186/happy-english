-- Extracted from the next ten available PDFs in doc/, ordered by source file identifier.
-- Sources: Learn & Talk I, Chapter 3 Lessons 21-27 and Chapter 4 Lessons 30-32.
-- 112072_808_Revision Three.pdf was unavailable during this import, so processing continued with 112316_809_Opening a Bank Account.pdf.
-- The target table is created by aliyun_daily_spoken_dialogue_buying_clothes.sql.
-- Re-running this file updates only the lesson_code/item_order pairs below.

SET NAMES utf8mb4;
START TRANSACTION;

-- Lesson 21 · A Pleasant Journey (doc/112065_808_A Pleasant Journey.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'peaceful', 'peaceful', '安静的；平静的', '/ˈpiːsfl/', 'quiet and calm; not worried or disturbed in any way', 'I had my first peaceful sleep in three weeks.', 'peaceful, travel, vacation', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'relaxing', 'relaxing', '令人放松的；轻松的', '/rɪˈlæksɪŋ/', 'helping you rest and become less anxious; describes something that makes people feel relaxed', 'We come here once a year expecting a quiet, relaxing holiday.', 'relaxing, vacation, travel', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'tight', 'tight', '紧的；拮据的；不宽裕的', '/taɪt/', 'difficult to manage because there is not enough time or money', 'The president has a tight schedule today.', 'tight schedule, travel', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'upload', 'upload', '上传', '/ˌʌpˈloʊd/', 'to copy or move programs or information to a larger computer system or to the internet', 'You can upload your photos to Instagram.', 'upload, photos, travel', 1),

    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Brandy', NULL, 'Hey, Jerry! Glad to see you''re back. How was your vacation?', '嗨，Jerry！很高兴你回来了。假期怎么样？', NULL, NULL, NULL, 'vacation, travel', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Jerry', NULL, 'Oh! This was the best vacation I''ve ever had in my life!', '哦！这是我一生中度过的最棒的假期！', NULL, NULL, NULL, 'best vacation, travel', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Brandy', NULL, 'Wow! Where did you go?', '哇！你去了哪里？', NULL, NULL, NULL, 'where did you go, vacation', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Jerry', NULL, 'We went to the Bahamas.', '我们去了巴哈马群岛。', NULL, NULL, NULL, 'Bahamas, travel', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Brandy', NULL, 'The Bahamas is a really peaceful place. It must have been quite relaxing.', '巴哈马是个非常宁静的地方。一定很放松吧。', NULL, NULL, NULL, 'peaceful, relaxing, vacation', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Jerry', NULL, 'Yes! After all the tight schedules, it''s nice to have a peaceful vacation. All I got was blue sea and a clear sky.', '是啊！忙完紧凑的日程后，享受一个宁静的假期真好。我看到的只有蔚蓝的大海和晴朗的天空。', NULL, NULL, NULL, 'tight schedule, peaceful vacation', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Brandy', NULL, 'Great! Did you take any pictures?', '太好了！你拍照了吗？', NULL, NULL, NULL, 'take pictures, vacation', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Jerry', NULL, 'Yes. I''ll be uploading them to Facebook today. You can check them out.', '拍了。我今天会把它们上传到 Facebook，你可以去看看。', NULL, NULL, NULL, 'upload, photos, Facebook', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'dialogue', '示范对话', 2, 'dialogue', 109, 'Brandy', NULL, 'That''s great!', '太好了！', NULL, NULL, NULL, 'great, vacation', 1),

    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Hi. You''re looking good. Did you go for a vacation somewhere?', '嗨。你气色不错。你去哪里度假了吗？', NULL, '根据课件提示补全。', NULL, 'vacation, travel', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes, I''ve just come back from Hawaii.', '是的，我刚从夏威夷回来。', NULL, NULL, NULL, 'Hawaii, vacation', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Wow, did you enjoy your vacation?', '哇，你喜欢这次假期吗？', NULL, NULL, NULL, 'enjoy your vacation, travel', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Yes. The islands are so green and the water is so blue, and it is a really peaceful place. It''s nice to have a vacation after my tight schedules.', '是的。岛屿很绿，海水很蓝，那里是个非常宁静的地方。紧凑日程之后去度假真好。', NULL, NULL, NULL, 'peaceful, tight schedules, Hawaii', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'That sounds great! It must have been quite relaxing.', '听起来真棒！一定很放松。', NULL, NULL, NULL, 'relaxing, vacation', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'I took a lot of pictures, but I don''t know how to upload them to the Internet. Could you help me?', '我拍了很多照片，但不知道怎么上传到网上。你能帮我吗？', NULL, NULL, NULL, 'upload, pictures, Internet', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'Of course!', '当然！', NULL, NULL, NULL, 'help, upload', 1),

    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you like to travel with your friends or family members? Why or why not?', '你喜欢和朋友还是家人一起旅行？为什么？', NULL, '和朋友旅行：共同爱好更多，活动可能更刺激。和家人旅行：感觉更安全，也能在不同环境中增进感情。', NULL, 'travel, friends, family', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'What is the best way to travel: by car, plane, boat, train, or something else?', '最佳旅行方式是什么：汽车、飞机、轮船、火车，还是其他方式？', NULL, '短途可开车：便宜、方便、可按自己的时间出发，也能带更多行李。长途可坐飞机：更快、更舒适，通常也被认为最安全。', NULL, 'transport, car, plane, travel', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Describe a long journey that you enjoyed.', '描述一次你喜欢的长途旅行。', NULL, '可以说明去了哪里、何时去的、怎么到达、和谁同行，以及喜欢这次旅行的原因。', NULL, 'long journey, travel, experience', 1),

    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'How was your vacation?\nThis was the best vacation I''ve ever had in my life!\nDid you enjoy your vacation?', '复习：peaceful / relaxing / tight / upload。', NULL, NULL, NULL, 'review, pleasant journey', 1),

    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Mogao Grottoes', 'Mogao Grottoes are world-famous treasure houses of art, also known as the Thousand Buddha Grottoes.', '莫高窟是世界著名的艺术宝库，也被称为千佛洞。', NULL, '课后拓展：莫高窟。', NULL, 'Mogao Grottoes, travel, art', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Early Buddhist cave art', 'Some paintings in Mogao Grottoes date back to the fourth century and represent early Buddhist cave art.', '莫高窟的一些壁画可追溯到四世纪，是早期佛教洞窟艺术的代表。', NULL, '课后拓展：莫高窟。', NULL, 'Buddhist cave art, Mogao Grottoes', 1),
    ('a-pleasant-journey', 'Chapter 3 · Traveling', 'Lesson 21 · A Pleasant Journey', 21, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Founded in 336 AD', 'Mogao Grottoes were founded in 336 AD, from the Former Qin to the Yuan Dynasty.', '莫高窟始建于公元 336 年，历经前秦至元朝。', NULL, '课后拓展：莫高窟。', NULL, 'Mogao Grottoes, history', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 22 · Getting a License (doc/112066_808_Getting a License.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'driver''s license', 'driver''s license', '驾照', '/ˈdraɪvərz laɪsns/', 'official permission to drive a car, received after passing a driving test, or the document showing this', 'I got my driver''s license when I was 18.', 'driver''s license, driving', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'gas', 'gas', '汽油', '/ɡæs/', 'a liquid obtained from petroleum and used especially as fuel for cars, aircraft, and other vehicles', 'I''ll stop and get some gas.', 'gas, car, driving', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'maintenance', 'maintenance', '维修；保养', '/ˈmeɪntənəns/', 'the work needed to keep a road, building, machine, or other object in good condition', 'This course gives drivers grounding in car maintenance.', 'maintenance, car, driving', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'insurance', 'insurance', '保险', '/ɪnˈʃʊrəns/', 'an agreement in which you pay a company and it pays costs after an accident, injury, or loss', 'It is a legal requirement that you have insurance for your car.', 'insurance, car, driving', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'public transport', 'public transport', '公共交通', '/ˌpʌblɪk ˈtrænspɔːrt/', 'a system of buses and trains that runs at regular times on fixed routes for public use', 'There is no public transport from the village.', 'public transport, bus, train', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'vocabulary', '核心词汇', 1, 'vocabulary', 6, NULL, 'road trip', 'road trip', '开车长途旅行', '/ˈroʊd trɪp/', 'a long trip or holiday taken by car', 'This summer we''re going on a road trip around Canada.', 'road trip, travel, car', 1),

    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Sarah', NULL, 'So Jeff, you got your driver''s license recently, right?', 'Jeff，你最近拿到驾照了，对吧？', NULL, NULL, NULL, 'driver''s license, driving', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Jeff', NULL, 'Yeah, I was pretty excited about that.', '是啊，我对此很兴奋。', NULL, NULL, NULL, 'excited, driver''s license', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Sarah', NULL, 'Are you planning to buy a new car?', '你打算买辆新车吗？', NULL, NULL, NULL, 'buy a car, driving', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Jeff', NULL, 'Not yet. Maybe after this semester I''ll start saving some cash.', '还没有。也许这学期结束后我会开始存点钱。', NULL, NULL, NULL, 'save cash, car', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Sarah', NULL, 'It does cost a lot. Plus, you have to pay for gas, maintenance, and insurance when you own a car. So I like taking public transport.', '确实花很多钱。而且有车后还得付汽油、保养和保险费。所以我喜欢坐公共交通。', NULL, NULL, NULL, 'gas, maintenance, insurance, public transport', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Jeff', NULL, 'So do I. Buses and trains are pretty convenient. But I would like to take a road trip someday.', '我也是。公交车和火车很方便。不过我有一天想来一次公路旅行。', NULL, NULL, NULL, 'public transport, road trip', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Sarah', NULL, 'Well, good luck driving. Hope to see you around this semester.', '那祝你开车顺利。希望这学期还能见到你。', NULL, NULL, NULL, 'good luck, driving', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Jeff', NULL, 'Yeah, same here. Catch you later, Sarah.', '好的，你也是。回头见，Sarah。', NULL, NULL, NULL, 'catch you later, driving', 1),

    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'I got my driver''s license last week.', '我上周拿到驾照了。', NULL, '根据课件提示补全。', NULL, 'driver''s license, driving', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Wow, that''s awesome! Are you planning to buy a car?', '哇，太棒了！你打算买车吗？', NULL, NULL, NULL, 'buy a car, driving', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Not yet. It will cost me a lot. And I have to pay for gas, maintenance, and insurance if I own a car. Personally, I like taking public transport.', '还没有。买车会花我很多钱，而且有车得付汽油、保养和保险费。就我个人而言，我喜欢坐公共交通。', NULL, NULL, NULL, 'gas, maintenance, insurance, public transport', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Yes, that''s true. Trains and buses are quite convenient and help me save a lot of money.', '是的，确实如此。火车和公交很方便，也帮我省很多钱。', NULL, NULL, NULL, 'trains, buses, public transport', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'But I am going on a road trip with my friends next month. For now I just use my mother''s car on the weekends.', '但我下个月要和朋友去公路旅行。现在我只在周末开我妈妈的车。', NULL, NULL, NULL, 'road trip, car', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'That''s not so bad.', '那也不错。', NULL, NULL, NULL, 'road trip, driving', 1),

    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'What modes of transport do you usually use? Do you often use public transport? Why do you think so many modern people drive cars?', '你通常使用哪些交通方式？你常坐公共交通吗？为什么现代人这么多人开车？', NULL, '交通方式可谈火车、公交、地铁、出租车等；原因可包括方便、省时、舒适、私人空间、公共交通拥挤或发展慢等。', NULL, 'transport, public transport, driving', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you have a driver''s license? Was it easy to get your driver''s license? Do you think it is necessary to learn to drive?', '你有驾照吗？拿驾照容易吗？你认为学开车有必要吗？', NULL, '有必要：现代人应有的基本技能、扩大就业机会、不必在雨中等公交或为了赶车早出门。没必要：汽油、保险、保养和车贷贵；污染环境；堵车、浪费时间且难找停车位。', NULL, 'driver''s license, driving skills', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'How important do you think it is for drivers to have good driving skills? What advice would you give people about safe driving?', '你认为司机具备良好驾驶技能有多重要？你会给安全驾驶什么建议？', NULL, '可谈安全、责任、紧急情况和辨认方向；建议理解并遵守路标与交规，不要在困倦、饮酒或看手机导航时驾驶，并按建议限速或更低速度行驶。', NULL, 'safe driving, road safety', 1),

    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Are you planning to buy a new car?\nI like taking public transport.\nBuses and trains are pretty convenient.', '复习：driver''s license / gas / maintenance / insurance / public transport / road trip。', NULL, NULL, NULL, 'review, driving', 1),

    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Determine the license class and type you need.', 'Determine what license class and type you need.', '确定你需要哪种驾照类别和类型。', NULL, '课后拓展：美国纽约州申请驾照步骤。', NULL, 'driver''s license, New York', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Get a learner permit.', 'Get a learner permit or learner''s permit.', '取得学习驾驶许可证。', NULL, '课后拓展：美国纽约州申请驾照步骤。', NULL, 'learner permit, driver''s license', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Practice driving and take a pre-licensing course.', 'Practice driving and take a pre-licensing course.', '练习驾驶并参加考前课程。', NULL, '课后拓展：美国纽约州申请驾照步骤。', NULL, 'practice driving, licensing course', 1),
    ('getting-a-license', 'Chapter 3 · Traveling', 'Lesson 22 · Getting a License', 22, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Pass a road test.', 'Pass a road test.', '通过路考。', NULL, '课后拓展：美国纽约州申请驾照步骤。', NULL, 'road test, driver''s license', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 23 · Asking for Directions (doc/112067_808_Asking for Directions.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'distant', 'distant', '遥远的', '/ˈdɪstənt/', 'far away in space or time; for regular long distances in daily life, far is more common', 'The telescope reveals many distant stars to our sight.', 'distant, far, directions', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'straight', 'straight', '直走；笔直的', '/streɪt/', 'continuing in one direction without bending or curving', 'Go straight along this road and turn left at the traffic lights.', 'straight, directions', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'intersection', 'intersection', '十字路口；交叉口', '/ˈɪntərsekʃn/', 'a place where two or more roads, lines, or paths meet or cross each other', 'Traffic lights have been placed at all major intersections.', 'intersection, directions', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'block', 'block', '街区', '/blɑːk/', 'a square of buildings or houses with roads on each side', 'My friend and I live on the same block.', 'block, directions', 1),

    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jill', NULL, 'Excuse me, could you tell me how to get to the science museum? I want to see the distant stars through telescopes.', '打扰一下，您能告诉我怎么去科学博物馆吗？我想通过望远镜看遥远的星星。', NULL, NULL, NULL, 'science museum, directions', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Stranger', NULL, 'Sure! It''s not too far from here. Just go straight along this road for two blocks and turn left at the traffic lights.', '当然！离这儿不太远。沿着这条路直走两个街区，在红绿灯处左转。', NULL, NULL, NULL, 'far, straight, blocks', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jill', NULL, 'So that''s where the museum is?', '所以博物馆就在那儿吗？', NULL, NULL, NULL, 'museum, directions', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Stranger', NULL, 'No. Walk east on Green Street and go through two intersections. The Science Museum will be on your right.', '不是。沿 Green Street 向东走，穿过两个十字路口。科学博物馆就在你的右边。', NULL, NULL, NULL, 'walk east, intersection, directions', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jill', NULL, 'Thanks so much for your help.', '非常感谢您的帮助。', NULL, NULL, NULL, 'thanks, directions', 1),

    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Excuse me, Miss, could you tell me how to get to the bank?', '打扰一下，女士，您能告诉我怎么去银行吗？', NULL, '根据课件提示补全。', NULL, 'bank, directions', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes, you can go straight down this road and go through two intersections. Then you turn left at the traffic lights.', '可以。沿这条路直走，穿过两个十字路口，然后在红绿灯处左转。', NULL, NULL, NULL, 'straight, intersections, directions', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'How long will it take me to get there?', '我到那里要多久？', NULL, NULL, NULL, 'how long, directions', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'It will be about 5 minutes, and it''s not too far from here.', '大约五分钟，离这儿不太远。', NULL, NULL, NULL, 'five minutes, far', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Okay.', '好的。', NULL, NULL, NULL, 'directions', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'The bank is on the corner of that block. You will see it when you turn left.', '银行就在那个街区的拐角处。左转时你会看见它。', NULL, NULL, NULL, 'corner, block, bank', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'Thanks for your help.', '谢谢您的帮助。', NULL, NULL, NULL, 'thanks, directions', 1),

    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'What do you do when you get lost while traveling?', '旅行时迷路了你会怎么办？', NULL, '可以向乘客或路人求助，也可以使用 Google Maps、Apple Maps、百度地图或高德地图等 GPS 软件。', NULL, 'get lost, directions, GPS', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Suppose Mark is in the train station and wants to go to the jewelry store, but he has lost his way. Can you help him?', '假设 Mark 在火车站，想去珠宝店但迷路了。你能帮他指路吗？', NULL, '可用两条路线练习：沿 Pine Street 或 Second Avenue 直走，穿过路口后在指定地点左／右转；珠宝店可在街区拐角或意大利餐厅旁边。', NULL, 'train station, jewelry store, directions', 1),

    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Could you tell me how to get to the science museum?\nHow long will it take me to get there?\nJust go straight down/along this road and turn left/right at ...', '复习：distant / straight / intersection / block。', NULL, NULL, NULL, 'review, directions', 1),

    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'go in the opposite direction', 'I''m afraid you''re going in the opposite direction.', '恐怕你正朝相反的方向走。', NULL, '课后拓展：问路表达。', NULL, 'opposite direction, directions', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'go back the way you came', 'Go back the way you came, and take the second turning on your left.', '沿原路返回，在第二个路口左转。', NULL, '课后拓展：问路表达。', NULL, 'go back, turning, directions', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'go straight ahead', 'Go straight ahead and the People''s Park is next to a bookstore. You won''t miss it.', '一直往前走，人民公园就在一家书店旁边。你不会错过的。', NULL, '课后拓展：问路表达。', NULL, 'straight ahead, directions', 1),
    ('asking-for-directions', 'Chapter 3 · Traveling', 'Lesson 23 · Asking for Directions', 23, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'fifteen minutes'' walk', 'It''s about fifteen minutes'' walk.', '步行大约十五分钟。', NULL, '课后拓展：问路表达。', NULL, 'minutes'' walk, directions', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 24 · Applying for a Passport (doc/112068_808_Applying for a Passport.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'figure out', 'figure out', '弄清楚；解决', '/ˈfɪɡjər aʊt/', 'to understand or solve something', 'It takes most people some time to figure out how new software works.', 'figure out, passport', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'document', 'document', '文件', '/ˈdɑːkjumənt/', 'a paper or set of papers with written or printed information, especially of an official type', 'Please try to find time to read the document before the meeting.', 'document, passport, application', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'submit', 'submit', '提交；呈送', '/səbˈmɪt/', 'to give or offer something for a decision to be made by others', 'You must submit your application before January 1st.', 'submit, passport, application', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'fill out', 'fill out', '填写', '/fɪl aʊt/', 'to write or type information in spaces provided for it; similar to fill in', 'Fill out the application carefully, and keep copies of it.', 'fill out, passport, form', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'apply', 'apply', '申请', '/əˈplaɪ/', 'to request something officially, especially in writing or by sending in a form', 'We could apply for a loan to buy a car.', 'apply, passport, application', 1),

    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Sam', NULL, 'Good morning, Jim. Can you help me figure out how to get a passport?', '早上好，Jim。你能帮我弄清楚怎样办护照吗？', NULL, NULL, NULL, 'figure out, passport', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Jim', NULL, 'Sure! You just need the correct documents to apply for it.', '当然！你只需要准备正确的申请文件。', NULL, NULL, NULL, 'documents, apply for passport', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Sam', NULL, 'But I don''t know which documents are needed.', '但我不知道需要哪些文件。', NULL, NULL, NULL, 'documents, passport', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Jim', NULL, 'You have to submit your birth certificate, your ID card, a photo, and fill out an application form. It''s easy.', '你得提交出生证明、身份证、一张照片，并填写申请表。很简单。', NULL, NULL, NULL, 'submit, fill out, application form', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Sam', NULL, 'I have all of that. Can I fill out this form online?', '这些我都有。我可以在线填写这张表吗？', NULL, NULL, NULL, 'fill out, online form', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Jim', NULL, 'I don''t think so. If you''re applying for the first time, you''ll need to go there and submit the form.', '我想不行。如果你是第一次申请，需要亲自去那里提交表格。', NULL, NULL, NULL, 'first time, submit form', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Sam', NULL, 'Okay. Thanks a lot.', '好的。非常感谢。', NULL, NULL, NULL, 'thanks, passport', 1),

    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Hi. I want to apply for a passport. Can you help me figure out how to get it?', '你好。我想申请护照。你能帮我弄清楚怎么办吗？', NULL, '根据课件提示补全。', NULL, 'apply for, passport', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Sure. Are you applying for the first time?', '当然。你是第一次申请吗？', NULL, NULL, NULL, 'first time, passport', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Yes. I''ve never been abroad before.', '是的。我以前从没出过国。', NULL, NULL, NULL, 'been abroad, passport', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'No problem. You need to fill out a form and submit other documents, for example, your ID card and a photo.', '没问题。你需要填写一张表并提交其他文件，例如身份证和照片。', NULL, NULL, NULL, 'fill out, submit, documents', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'I got it right here.', '我都带来了。', NULL, NULL, NULL, 'documents, passport', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Great! Just submit it to the counter over there.', '很好！把它提交到那边的柜台就行。', NULL, NULL, NULL, 'submit, counter, passport', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'Thanks for your help.', '谢谢你的帮助。', NULL, NULL, NULL, 'thanks, passport', 1),

    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Is it easy to get a passport in your country? Are there many stamps and visas in your passport?', '在你的国家办护照容易吗？你的护照上有很多出入境章和签证吗？', NULL, '容易：填写申请表、准备照片和身份证、缴费、网上预约或登记。困难：排队久、等待时间长、服务态度不好。可谈是否去过很多国家或从未出国。', NULL, 'passport, visa, travel', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Would you worry if you lost your passport while traveling? What should you do?', '旅行时丢了护照你会担心吗？应该怎么办？', NULL, '可以先冷静下来，仔细寻找护照，并向警察、使馆工作人员或领事官员求助。', NULL, 'lost passport, embassy, travel', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Is the passport from your country more or less powerful than passports from other countries?', '你国家的护照比其他国家的护照更有用还是较不方便？', NULL, '根据课件的 2020 年前示例，可比较不同护照可免签前往的国家和地区数量；旅行政策可能会变化。', NULL, 'passport, visa-free travel', 1),

    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Can you help me figure out how to get/apply for a passport?', '复习：figure out / document / submit / fill out / apply。', NULL, NULL, NULL, 'review, passport', 1),

    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'visa-free', 'visa-free', '免签', NULL, NULL, NULL, 'visa-free, passport', 1),
    ('applying-for-a-passport', 'Chapter 3 · Traveling', 'Lesson 24 · Applying for a Passport', 24, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'visa upon arrival', 'visa upon arrival', '落地签', NULL, NULL, NULL, 'visa on arrival, passport', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 25 · Checking In (doc/112069_808_Checking In.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'check in', 'check in', '办理入住；办理值机；登记', '/tʃek ɪn/', 'to go to a desk in a hotel, airport, or similar place and tell an official that you have arrived', 'We''ve checked in at the hotel.', 'check in, hotel, travel', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'reservation', 'reservation', '预约；预订', '/ˌrezərˈveɪʃn/', 'an arrangement in which a seat, table, or other place is kept for you', 'I''d like to make a table reservation for two people for nine o''clock.', 'reservation, hotel, travel', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'request', 'request', '请求；要求', '/rɪˈkwest/', 'the act of politely or officially asking for something', 'They made a request for better education.', 'request, hotel, travel', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'departure', 'departure', '离开；启程；出发', '/dɪˈpɑːrtʃər/', 'the fact of a person or vehicle leaving somewhere', 'Our departure was delayed because of bad weather.', 'departure, hotel, travel', 1),

    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Clerk', NULL, 'Welcome to the Royal Hotel. How may I help you today?', '欢迎来到 Royal Hotel。今天我能为您做什么？', NULL, NULL, NULL, 'hotel, check in', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Peter', NULL, 'I''d like to check in, please.', '我想办理入住。', NULL, NULL, NULL, 'check in, hotel', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Clerk', NULL, 'Certainly, sir. Do you have your reservation letter?', '当然，先生。您有预订确认信吗？', NULL, NULL, NULL, 'reservation letter, hotel', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Peter', NULL, 'I do. Here it is. I''ve booked a room for three nights. The last name is Barnes.', '有。这是确认信。我订了三晚的房间，姓 Barnes。', NULL, NULL, NULL, 'booked room, three nights', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Clerk', NULL, 'Let me confirm: Mr. Peter Barnes for three nights?', '我确认一下：Peter Barnes 先生，住三晚？', NULL, NULL, NULL, 'confirm, reservation', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Peter', NULL, 'Correct. I also requested a non-smoking room.', '对。我还要求了一间无烟房。', NULL, NULL, NULL, 'requested, non-smoking room', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Clerk', NULL, 'Yes, we have that right here. You''ll be in a single, non-smoking room. Here is the key card to your room.', '是的，已经为您安排好了。您住单人无烟房。这是房间的门卡。', NULL, NULL, NULL, 'single room, key card', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Peter', NULL, 'Great. What time do I need to check out of my room?', '太好了。我需要在几点前退房？', NULL, NULL, NULL, 'check out, hotel', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'dialogue', '示范对话', 2, 'dialogue', 109, 'Clerk', NULL, 'Please check out by 11 a.m. on the day of your departure.', '请在离店当天上午 11 点前退房。', NULL, NULL, NULL, 'check out, departure', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'dialogue', '示范对话', 2, 'dialogue', 110, 'Peter', NULL, 'Great! Thank you.', '太好了！谢谢。', NULL, NULL, NULL, 'thanks, hotel', 1),

    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Good afternoon. Welcome to the Pacific Hotel. How may I help you?', '下午好。欢迎来到 Pacific Hotel。我能帮您什么吗？', NULL, '根据课件提示补全。', NULL, 'hotel, check in', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I have a reservation for today. It''s under the name of Sally Wang.', '我今天有预订，名字是 Sally Wang。', NULL, NULL, NULL, 'reservation, hotel', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Yes, Miss Wang, we''ve reserved a double room for you.', '是的，Wang 女士，我们为您预订了一间双人房。', NULL, NULL, NULL, 'double room, reservation', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Thanks, and I also requested a non-smoking room.', '谢谢，我还要求了一间无烟房。', NULL, NULL, NULL, 'requested, non-smoking room', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Yes. Your room is 487. Here is your key. To get to your room, take the elevator on the right up to the fourth floor.', '是的。您的房间是 487。这是钥匙。去房间请乘右边的电梯到四楼。', NULL, NULL, NULL, 'room number, elevator, hotel', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Okay, what time do I need to check out of my room?', '好的，我需要在几点前退房？', NULL, NULL, NULL, 'check out, hotel', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'At midday on the day of your departure, Miss.', '在您离店当天的中午前，女士。', NULL, NULL, NULL, 'departure, check out', 1),

    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Are there many hotels in the country, city, or town you live in? Which areas have the most hotels?', '你所在的国家、城市或城镇有很多酒店吗？哪些区域的酒店最多？', NULL, '可谈商务酒店、机场酒店、快捷酒店和豪华酒店；酒店多的地方如市中心、火车站附近或大学附近。', NULL, 'hotels, city, travel', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'What do you look for when choosing a hotel? Give your reasons.', '选择酒店时你会看重什么？请说明原因。', NULL, '可从价格、距离市中心／餐馆／夜生活的远近、距离机场／火车站的远近、舒适度和 Wi-Fi 等方面谈。', NULL, 'choose a hotel, travel', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Many hotels now have key cards instead of traditional room keys. What are the advantages and disadvantages?', '许多酒店现在用门卡代替传统钥匙。优点和缺点是什么？', NULL, '门卡更容易管理和维护，可降低维护或替换成本；但锁故障或信息未更新时，可能被锁在门外，还得回前台求助。', NULL, 'key card, hotel, advantages', 1),

    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I''d like to check in, please.\nHow may I help you today?\nWhat time do I need to check out of my room?', '复习：check in / reservation / request / departure。', NULL, NULL, NULL, 'review, check in', 1),

    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'access code of wireless internet', 'access code of wireless internet', '无线网络登录密码', NULL, '办理入住时可获取的信息。', NULL, 'wireless internet, hotel', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'details of the hotel amenities', 'details of the hotel amenities', '酒店设施详情', NULL, '办理入住时可获取的信息。', NULL, 'hotel amenities, check in', 1),
    ('checking-in', 'Chapter 3 · Traveling', 'Lesson 25 · Checking In', 25, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'local sightseeing tips', 'local sightseeing tips', '当地观光指南', NULL, '办理入住时可获取的信息。', NULL, 'sightseeing, hotel, travel', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 26 · Room Service (doc/112070_808_Room Service.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'department', 'department', '部；局；处；系', '/dɪˈpɑːrtmənt/', 'any division or part of a school, business, or government', 'The finance department is on the fifth floor.', 'department, room service, hotel', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'order', 'order', '点（饭菜）；订购', '/ˈɔːrdər/', 'to ask for something to be made, supplied, or delivered, especially in a restaurant or shop', 'I ordered some pasta and some tomatoes.', 'order, room service, hotel', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'a set of', 'a set of', '一套；一副', NULL, 'a group of similar things that belong together in some way', 'We bought Charles and Mandy a set of cutlery as a wedding present.', 'a set of, room service', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'serve', 'serve', '提供（食物或饮料）', '/sɜːrv/', 'to provide food or drinks', 'Breakfast is served in the restaurant between 7 a.m. and 11 a.m.', 'serve, room service, hotel', 1),

    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Sam', NULL, 'Good morning. Room service department. How may I help you?', '早上好。这里是客房服务部。我能帮您什么吗？', NULL, NULL, NULL, 'room service department, hotel', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Olivia', NULL, 'Hello. I would like to order breakfast.', '你好。我想订早餐。', NULL, NULL, NULL, 'order breakfast, room service', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Sam', NULL, 'Would you tell me your room number and your name, please?', '请告诉我您的房间号和姓名好吗？', NULL, NULL, NULL, 'room number, hotel', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Olivia', NULL, 'My name is Olivia Blossom and I''m in room 623.', '我叫 Olivia Blossom，住 623 房间。', NULL, NULL, NULL, 'room number, hotel', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Sam', NULL, 'What would you like to order, Miss Blossom?', 'Blossom 女士，您想点什么？', NULL, NULL, NULL, 'order, room service', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Olivia', NULL, 'I would like to have a set of British breakfast.', '我想要一份英式早餐。', NULL, NULL, NULL, 'British breakfast, room service', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Sam', NULL, 'Okay. Would you like to have coffee or tea?', '好的。您想要咖啡还是茶？', NULL, NULL, NULL, 'coffee or tea, breakfast', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Olivia', NULL, 'Coffee, please. And I would like to be served around 7 a.m.', '请给我咖啡。我想在早上 7 点左右送到。', NULL, NULL, NULL, 'served, 7 a.m., room service', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'dialogue', '示范对话', 2, 'dialogue', 109, 'Sam', NULL, 'Okay. Thank you for using the room service. I hope you enjoy your meal and have a nice day.', '好的。感谢您使用客房服务。祝您用餐愉快，祝您一天愉快。', NULL, NULL, NULL, 'enjoy your meal, room service', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'dialogue', '示范对话', 2, 'dialogue', 110, 'Olivia', NULL, 'Great! Thank you.', '太好了！谢谢。', NULL, NULL, NULL, 'thanks, room service', 1),

    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Hello, is this room service department?', '你好，这里是客房服务部吗？', NULL, '根据课件提示补全。', NULL, 'room service department, hotel', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes. How may I help you?', '是的。我能帮您什么吗？', NULL, NULL, NULL, 'how may I help you, room service', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I''m calling from room 324, and I''d like to order breakfast for my room.', '我从 324 房间打来，想为房间订早餐。', NULL, NULL, NULL, 'room 324, order breakfast', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Sure. What would you like to order?', '当然。您想点什么？', NULL, NULL, NULL, 'order, room service', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'A set of British breakfast. By the way, do you serve wine in the room?', '一份英式早餐。顺便问一下，你们提供房间送酒服务吗？', NULL, NULL, NULL, 'British breakfast, serve wine', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'I''m afraid not. Alcoholic drinks are served only at the hotel bar.', '恐怕不行。酒精饮料只在酒店酒吧提供。', NULL, NULL, NULL, 'alcoholic drinks, hotel bar', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'That''s fine. Thanks for your help.', '没关系。谢谢你的帮助。', NULL, NULL, NULL, 'thanks, room service', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'practice', '情景补全对话', 3, 'practice', 208, 'B', NULL, 'You''re welcome. I hope you enjoy your meal and have a nice day.', '不客气。祝您用餐愉快，祝您一天愉快。', NULL, NULL, NULL, 'enjoy your meal, room service', 1),

    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you ever used room service for champagne, breakfast, or a sandwich in the middle of the night?', '你用过客房服务点香槟、早餐或半夜的三明治吗？', NULL, '用过：很方便。没用过：价格贵，客房服务菜单的同样菜品通常比酒店餐厅贵很多；可以用自动售货机或去便利店。', NULL, 'room service, hotel, food', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you usually dine out when you''re on holiday, or do you try to get back to the hotel in time for meals?', '假期里你通常在外面吃饭，还是尽量及时回酒店吃饭？', NULL, '外出就餐：享受不同种类的本地食物，选择更多。酒店吃：舒适方便，也可从超市买食物或零食带回去。还可以在 Airbnb 做饭，享受新鲜便宜的食物，并与房东互动了解当地文化。', NULL, 'dine out, hotel, holiday', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'What''s your opinion on breakfast and lunch buffets? In your experience, are they of good quality? Are they worth the money?', '你怎么看早餐和午餐自助餐？以你的经验，它们质量好吗？值得花钱吗？', NULL, '自助餐适合一次服务大量客人；用餐者可以自己看食物、选择真正喜欢的并决定吃多少。质量会因酒店和餐厅而异。', NULL, 'buffet, hotel, food', 1),

    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'How may I help you?\nWhat would you like to order?\nI hope you enjoy your meal and have a nice day.', '复习：department / order / a set of / serve。', NULL, NULL, NULL, 'review, room service', 1),

    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'filet mignon', 'filet mignon', '菲力牛排', NULL, '课后拓展：客房服务点餐。', NULL, 'filet mignon, room service', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'porterhouse steak', 'porterhouse steak', '红屋牛排；丁骨牛排', NULL, 'A porterhouse steak is similar to a T-bone steak.', NULL, 'porterhouse steak, room service', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'charge something to your room', 'This will be charged to your room.', '这笔费用将记到您的房间账单上。', NULL, '课后拓展：客房服务点餐。', NULL, 'charge to room, hotel', 1),
    ('room-service', 'Chapter 3 · Traveling', 'Lesson 26 · Room Service', 26, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'momentarily', 'The food will be brought to you momentarily.', '食物很快会送到您房间。', NULL, 'momentarily = 很快；片刻后。', NULL, 'momentarily, room service', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 27 · At the Airport (doc/112071_808_At the Airport.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'passport', 'passport', '护照', '/ˈpæspɔːrt/', 'an official document that identifies you as a citizen of a particular country and that you may have to show when you enter or leave a country', 'My passport is valid for another two years.', 'passport, airport, travel', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'visa', 'visa', '签证', '/ˈviːzə/', 'an official mark, usually made in a passport, that allows you to enter or leave a particular country', 'I need to extend my visa.', 'visa, passport, airport', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'stopover', 'stopover', '中途停留', '/ˈstɑːpoʊvər/', 'a short stay in a place in between two parts of a journey', 'The Sunday flights will make a stopover in Nairobi.', 'stopover, flight, airport', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'board', 'board', '登船；登机；上火车', '/bɔːrd/', 'to get onto or allow people to get onto a boat, train, or aircraft', 'Flight 474 to Beijing is now boarding at gate 9.', 'board, boarding, flight', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'delightful', 'delightful', '令人愉快的；宜人的', '/dɪˈlaɪtfl/', 'very pleasant, attractive, or enjoyable', 'It was the most delightful garden I had ever seen.', 'delightful, trip, travel', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'vocabulary', '核心词汇', 1, 'vocabulary', 6, NULL, 'assistance', 'assistance', '帮助；援助；支持', '/əˈsɪstəns/', 'help or support', 'The company needs more financial assistance from the government.', 'assistance, airport, travel', 1),

    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Clerk', NULL, 'Welcome to TransGlobal Airlines. How may I help you?', '欢迎来到 TransGlobal 航空公司。我能为您做什么？', NULL, NULL, NULL, 'airline, airport', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Peter', NULL, 'I''m flying with TransGlobal to Moscow today.', '我今天乘坐 TransGlobal 航空公司的航班去莫斯科。', NULL, NULL, NULL, 'flying to Moscow, airport', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Clerk', NULL, 'Thank you for flying with us. May I see your passport?', '感谢您乘坐我们的航班。请出示您的护照好吗？', NULL, NULL, NULL, 'May I see your passport, airport', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Peter', NULL, 'Here you go. My visitor visa for Russia is inside as well.', '给您。我的俄罗斯访问签证也在里面。', NULL, NULL, NULL, 'visitor visa, passport', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Clerk', NULL, 'Thank you, Mr. Peter Evans. You are travelling in business class to Moscow, with a stopover in Hong Kong.', '谢谢您，Peter Evans 先生。您将乘坐商务舱前往莫斯科，并在香港中途停留。', NULL, NULL, NULL, 'business class, stopover', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Peter', NULL, 'That''s correct.', '是的。', NULL, NULL, NULL, 'correct, flight', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Clerk', NULL, 'Okay. Here''s your passport and boarding pass, Mr. Evans. Your flight leaves at Gate 20, and your boarding time is 7:40 p.m. Your luggage will be directly transferred to Moscow, so you don''t need to recheck luggage in Hong Kong. Have a delightful trip!', '好的。这是您的护照和登机牌，Evans 先生。您的航班从 20 号登机口起飞，登机时间是晚上 7:40。您的行李会直接转运到莫斯科，因此无需在香港重新托运。祝您旅途愉快！', NULL, NULL, NULL, 'boarding pass, gate, recheck luggage', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Peter', NULL, 'Thank you very much for your assistance.', '非常感谢您的帮助。', NULL, NULL, NULL, 'thank you for your assistance, airport', 1),

    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Good evening. Welcome to A1 Airlines. May I see your passport?', '晚上好。欢迎来到 A1 航空公司。请出示您的护照好吗？', NULL, '根据课件提示补全。', NULL, 'passport, airport', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Here they are. My visitor visa for Japan is also inside.', '给您。我的日本访问签证也在里面。', NULL, NULL, NULL, 'visa, passport', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Thank you.', '谢谢。', NULL, NULL, NULL, 'airport, assistance', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'practice', '情景补全对话', 3, 'practice', 204, 'A', NULL, 'You are travelling in first class to Tokyo, with a stopover in Hong Kong.', '您将乘坐头等舱前往东京，并在香港中途停留。', NULL, NULL, NULL, 'first class, stopover', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Here''s your passport and boarding pass. Your flight leaves at Gate 8, and your boarding time is 7:40. Have a delightful trip!', '这是您的护照和登机牌。您的航班从 8 号登机口起飞，登机时间是 7:40。祝您旅途愉快！', NULL, NULL, NULL, 'boarding pass, boarding time', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Thank you for your assistance.', '谢谢您的帮助。', NULL, NULL, NULL, 'assistance, airport', 1),

    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you like traveling by plane? Why or why not?', '你喜欢乘飞机旅行吗？为什么？', NULL, '喜欢：可在相对短的时间内走很远的距离，也能从空中看美景。不喜欢：票价贵、座位不舒服，或容易晕机。', NULL, 'plane, airport, travel', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Where do you prefer to sit on a plane: the window seat, aisle seat, or middle seat?', '在飞机上你更喜欢坐靠窗、靠过道还是中间的位置？', NULL, '靠过道座位方便随时去洗手间，不必跨过或叫醒邻座乘客；靠窗座位适合工作或睡觉，也能欣赏窗外景色。', NULL, 'window seat, aisle seat, plane', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'What sorts of things do you do to pass the time while flying?', '飞行途中你会做些什么打发时间？', NULL, '可以带书或 Kindle、看电影或电视剧、听音乐、喝饮料、计划下一次旅行、修图或处理办公室工作。', NULL, 'flying, pass the time, airport', 1),

    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'May I see your passport?', '复习：passport / visa / stopover / board / delightful / assistance。', NULL, NULL, NULL, 'review, airport', 1),

    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Checking in for a flight', 'Excuse me, is this the right counter to check in for Flight CA323 to Los Angeles?', '请问，这是办理 CA323 次洛杉矶航班值机的正确柜台吗？', NULL, '课后拓展：机场值机。', NULL, 'check in, flight, counter', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Show your documents', 'Yes, please show me your ticket and passport.', '是的，请出示您的机票和护照。', NULL, '课后拓展：机场值机。', NULL, 'ticket, passport, airport', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'aisle seat', 'And I''d like an aisle seat, please.', '我想要一个靠过道的座位。', NULL, '课后拓展：机场值机。', NULL, 'aisle seat, flight', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'pieces of baggage', 'How many pieces of baggage?', '您有几件行李？', NULL, '课后拓展：机场值机。', NULL, 'baggage, airport', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'put them on this scale', 'Please put them on this scale.', '请把它们放到这个秤上。', NULL, '课后拓展：机场值机。', NULL, 'scale, baggage, airport', 1),
    ('at-the-airport', 'Chapter 3 · Traveling', 'Lesson 27 · At the Airport', 27, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'boarding pass', 'Here is your passport, ticket and boarding pass. Have a nice trip.', '这是您的护照、机票和登机牌。祝您旅途愉快。', NULL, '课后拓展：机场值机。', NULL, 'boarding pass, airport', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 30 · Finding a Book at the Bookstore (doc/112314_809_Finding a Book at the Bookstore.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'fiction', 'fiction', '小说', '/ˈfɪkʃn/', 'the type of book or story that is written about imaginary characters and events and not based on real people and facts', 'The book is a work of fiction and not intended as a historical account.', 'fiction, bookstore, books', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'release', 'release', '发布（新书等）', '/rɪˈliːs/', 'to make a product such as a book available for the public to buy; launch', 'The new edition of the dictionary will be released by the education minister later this month.', 'release, bookstore, books', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'title', 'title', '题目；标题；名称', '/ˈtaɪtl/', 'the name of a film, book, painting, piece of music, or other work', 'The author''s name was printed below the title.', 'title, book, bookstore', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'bestseller', 'bestseller', '畅销书', '/ˌbestˈselər/', 'a product that is extremely popular and has sold in very large numbers', 'The "Harry Potter" novels were all bestsellers.', 'bestseller, book, bookstore', 1),

    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Clerk', NULL, 'Hello, can I help you find something?', '你好，我可以帮您找些什么吗？', NULL, NULL, NULL, 'bookstore, find a book', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Jones', NULL, 'Yes. Can you tell me where the fiction section is, please?', '好的。请问小说区在哪里？', NULL, NULL, NULL, 'fiction section, bookstore', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Clerk', NULL, 'Well, the fiction new releases are at the front of the store. The dedicated fiction section is on your right. Is there a specific book I can help you find?', '小说新书在书店前面。专门的小说区在您的右边。有具体的书需要我帮您找吗？', NULL, NULL, NULL, 'new releases, fiction section', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Jones', NULL, 'I''m looking for an old book and I''m not sure of the title.', '我在找一本旧书，但不确定书名。', NULL, NULL, NULL, 'old book, title', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Clerk', NULL, 'Well, if it''s an old book, it may be out of print. If it was a bestseller at one time, there''s a chance that it''s still in print.', '如果是旧书，它可能已经绝版了。如果它曾经是畅销书，仍有可能还在印刷。', NULL, NULL, NULL, 'out of print, bestseller', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Jones', NULL, 'Okay, thank you.', '好的，谢谢。', NULL, NULL, NULL, 'thanks, bookstore', 1),

    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Could you tell me where the fiction section is, please?', '请问小说区在哪里？', NULL, '根据课件提示补全。', NULL, 'fiction section, bookstore', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Sure. It''s in the back of the store, past the biographies. Can I help you find anything?', '当然。在书店后面，传记区的后面。需要我帮您找什么吗？', NULL, NULL, NULL, 'biographies, bookstore', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Well, I''m looking for a book that was released recently.', '我在找一本最近发布的书。', NULL, NULL, NULL, 'released, book', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Okay, what''s the title of the book?', '好的，这本书叫什么名字？', NULL, NULL, NULL, 'title, book', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'It''s called "The Black Book".', '它叫《The Black Book》。', NULL, NULL, NULL, 'The Black Book, title', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'This book is the bestseller of 2019. You can find it behind the fiction shelves on your right.', '这本书是 2019 年的畅销书。您可以在右手边小说书架的后面找到它。', NULL, NULL, NULL, 'bestseller, fiction shelves', 1),

    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Which do you prefer, reading physical books or electronic books (e-books)? Explain why.', '纸质书和电子书你更喜欢哪一种？请说明原因。', NULL, '电子书更环保，许多书包括经典名著都免费；纸质书的翻页和握书体验更好，对眼睛也通常比电子书友好。', NULL, 'physical books, e-books, reading', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'What kind(s) of books do you like? And why?', '你喜欢什么类型的书？为什么？', NULL, '可谈历史、传记、科幻、侦探故事和古典文学等，并说明喜欢的原因。', NULL, 'books, reading, genre', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Describe a book you would like to read again.', '描述一本你想再读一次的书。', NULL, '可以说明书的内容、当初阅读它的原因、从中学到的东西，以及想重读的原因。', NULL, 'book, reading, discussion', 1),

    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Can you tell me where the fiction section is, please?', '复习：fiction / release / title / bestseller。', NULL, NULL, NULL, 'review, bookstore', 1),

    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Make a list', 'Make a list answering these questions: What genre of books do you like? What authors do you like?', '列一个清单并回答：你喜欢什么类型的书？你喜欢哪些作者？', NULL, '课后拓展：如何选择一本好书。', NULL, 'genre, authors, book', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Ask for a recommendation', 'Ask someone to recommend a good book.', '请别人推荐一本好书。', NULL, '课后拓展：如何选择一本好书。', NULL, 'recommendation, book', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Use the bookstore search engine', 'Use the search engine in the bookstore to find a certain book.', '使用书店里的搜索引擎查找某本书。', NULL, '课后拓展：如何选择一本好书。', NULL, 'search engine, bookstore', 1),
    ('finding-a-book-at-the-bookstore', 'Chapter 4 · Daily Life', 'Lesson 30 · Finding a Book at the Bookstore', 30, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Skim the book', 'Find the book and skim over the back of the book or the inside flap. If that holds your attention, it''s probably a good book for you.', '找到这本书，快速浏览封底或内页折口；如果它能吸引你的注意力，它可能就是适合你的好书。', NULL, '课后拓展：如何选择一本好书。', NULL, 'skim, book, bookstore', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 31 · Renting an Apartment (doc/112315_809_Renting an Apartment.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'apartment', 'apartment', '公寓套房', '/əˈpɑːrtmənt/', 'a set of rooms for living in, especially on one floor of a building', 'I will give you the keys to my apartment.', 'apartment, rent, home', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'location', 'location', '地点；位置', '/loʊˈkeɪʃn/', 'a place or position', 'The hotel is in a beautiful location, overlooking the lake.', 'location, apartment, rent', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'magnificent', 'magnificent', '极好的；壮丽的；令人羡慕的', '/mæɡˈnɪfɪsnt/', 'very good, beautiful, or deserving to be admired', 'The palace was absolutely magnificent.', 'magnificent, apartment, view', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'lease', 'lease', '租约', '/liːs/', 'a legal agreement in which you pay money in order to use a building, piece of land, vehicle, or other property for a period', 'He has the house on a long lease.', 'lease, apartment, rent', 1),

    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Mrs. Rand', NULL, 'Hello, Carrie. Please come in. I hope you didn''t have trouble finding the apartment.', '你好，Carrie。请进。希望你找这套公寓时没遇到麻烦。', NULL, NULL, NULL, 'finding the apartment, rent', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Carrie', NULL, 'None at all. The location is very convenient.', '完全没有。这儿的位置很方便。', NULL, NULL, NULL, 'location, convenient', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Mrs. Rand', NULL, 'It is. The subway station and a major bus stop are right nearby, so there are plenty of public transportation options.', '是的。地铁站和一个主要公交站就在附近，所以公共交通选择很多。', NULL, NULL, NULL, 'subway station, public transportation', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Carrie', NULL, 'May I have a look around?', '我可以四处看看吗？', NULL, NULL, NULL, 'have a look around, apartment', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Mrs. Rand', NULL, 'Of course. I''ll give you a quick tour. Here''s the living room. This is the bedroom, which offers a magnificent view of the park, and there, you have the bathroom and kitchen.', '当然。我带你简单参观一下。这是客厅；这是卧室，可以看到壮丽的公园景色；那边是浴室和厨房。', NULL, NULL, NULL, 'quick tour, magnificent view', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Carrie', NULL, 'I''m very interested. If all goes well, I look forward to signing the lease.', '我很感兴趣。如果一切顺利，我期待签租约。', NULL, NULL, NULL, 'signing the lease, apartment', 1),

    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'I''m thinking about renting a new place to live.', '我正考虑租个新地方住。', NULL, '根据课件提示补全。', NULL, 'renting, new place', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I have a friend who wants to rent out his apartment.', '我有个朋友想把他的公寓出租。', NULL, NULL, NULL, 'rent out, apartment', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'What''s the location? I don''t want to live far from my work.', '位置在哪里？我不想住得离工作地点太远。', NULL, NULL, NULL, 'location, work', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'It''s near West Road. It will only take half an hour to cycle to your work. And the bedroom offers a magnificent view of the park.', '它在 West Road 附近。骑车到你的工作地点只要半小时。而且卧室能看到壮丽的公园景色。', NULL, NULL, NULL, 'West Road, magnificent view', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Okay. Can you take me to see your friend and the house tomorrow?', '好的。你明天能带我去见你的朋友和看看房子吗？', NULL, NULL, NULL, 'see the house, apartment', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Of course. If everything goes well, you can sign the lease quickly.', '当然。如果一切顺利，你很快就能签租约。', NULL, NULL, NULL, 'sign the lease, apartment', 1),

    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you like the place where you are living? Why or why not? In which room does your family spend most of the time?', '你喜欢目前居住的地方吗？为什么？你的家人在哪个房间待得最多？', NULL, '可谈客厅或起居室，因为那里适合放松、社交和招待客人。', NULL, 'home, living room, apartment', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'What do you need to consider before renting an apartment?', '租公寓之前需要考虑什么？', NULL, '考虑位置，例如是否靠近地铁和公交站；也要考虑预算，确认能否负担理想公寓的租金，必要时可找室友。', NULL, 'renting, location, budget', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Do you live with your parents or roommates, or live alone? Is it expensive to rent an apartment in your country?', '你和父母或室友住，还是独居？在你的国家租公寓贵吗？', NULL, '租金取决于所在城市和街区、公寓大小、距公共交通、学校、医院和公园的远近，以及公寓的新旧程度。', NULL, 'rent, roommates, apartment', 1),

    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'May I have a look around?\nIf all goes well, I look forward to signing the lease.\nI''m thinking about renting a new place to live.', '复习：apartment / location / magnificent / lease。', NULL, NULL, NULL, 'review, apartment', 1),

    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Seek web to pick features', 'Seek web to pick features. You will need to find one that is within your budget and suits your needs in terms of number of rooms, amenities, and proximity to school and work.', '通过网络筛选房屋特征。房子要符合预算，并满足房间数量、设施、距离学校和工作地点等需求。', NULL, '课后拓展：如何租公寓。', NULL, 'budget, amenities, apartment', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Make an appointment', 'Make an appointment with the landlord or the letting agent before visiting.', '看房前与房东或租赁代理人预约。', NULL, '课后拓展：如何租公寓。', NULL, 'landlord, letting agent, appointment', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Bring a pen and paper', 'Bring a pen and paper to make notes about the pros and cons of each apartment, the deposit, the monthly rent, and anything else that seems important to remember.', '带上纸笔，记录每套公寓的优缺点、押金、月租以及其他重要信息。', NULL, '课后拓展：如何租公寓。', NULL, 'pros and cons, deposit, monthly rent', 1),
    ('renting-an-apartment', 'Chapter 4 · Daily Life', 'Lesson 31 · Renting an Apartment', 31, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Signing the lease', 'Signing the lease.', '签订租约。', NULL, '课后拓展：如何租公寓。', NULL, 'signing the lease, apartment', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 32 · Opening a Bank Account (doc/112316_809_Opening a Bank Account.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'valid', 'valid', '有效的；正式认可的', '/ˈvælɪd/', 'a ticket or other document is valid if it is based on or used according to a set of official conditions that often include a time limit', 'My passport is valid for another two years.', 'valid, bank account, ID', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'initial', 'initial', '开始的；最初的', '/ɪˈnɪʃl/', 'of or at the beginning', 'The experiments have given initial results.', 'initial, bank account, deposit', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'deposit', 'deposit', '将（钱）存入银行；存款', '/dɪˈpɑːzɪt/', 'to put money into a bank account', 'I deposited 500 dollars in my account this morning.', 'deposit, bank account, money', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'account', 'account', '账户；户头', '/əˈkaʊnt/', 'an arrangement with a bank to keep your money there and allow you to take it out when you need to', 'I need to draw some money out of my account.', 'account, bank, money', 1),

    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jerry', NULL, 'Welcome to Standard Bank. How may I help you?', '欢迎来到 Standard Bank。我能为您做什么？', NULL, NULL, NULL, 'bank, opening an account', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Tom', NULL, 'I have some questions about opening a bank account here.', '我想问一些在这里开银行账户的问题。', NULL, NULL, NULL, 'opening a bank account, bank', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jerry', NULL, 'I''d be happy to help.', '我很乐意帮忙。', NULL, NULL, NULL, 'help, bank', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Tom', NULL, 'Great! First, what do I need to open an account?', '太好了！首先，我开户需要什么？', NULL, NULL, NULL, 'open an account, bank', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jerry', NULL, 'You''ll need to bring a valid form of photo ID and we''ll also need your home address and telephone number.', '您需要带一份有效的带照片身份证明文件，还需要提供家庭住址和电话号码。', NULL, NULL, NULL, 'valid photo ID, bank account', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Tom', NULL, 'How much cash do I need to deposit at the time of opening an account?', '开户时我需要存入多少现金？', NULL, NULL, NULL, 'deposit, bank account', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jerry', NULL, 'Well, the initial deposit is 25 dollars.', '初始存款是 25 美元。', NULL, NULL, NULL, 'initial deposit, bank', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Tom', NULL, 'Thanks! You''ve been very helpful. I''d like to open a savings account.', '谢谢！您帮了大忙。我想开一个储蓄账户。', NULL, NULL, NULL, 'savings account, bank', 1),

    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Good morning, how can I help you?', '早上好，我能帮您什么？', NULL, '根据课件提示补全。', NULL, 'bank, help', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I want to open a savings account.', '我想开一个储蓄账户。', NULL, NULL, NULL, 'savings account, bank', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Okay. Would you please fill out this application form first? And give me a valid form of photo ID, please.', '好的。请先填写这份申请表，然后请给我一份有效的带照片身份证明文件。', NULL, NULL, NULL, 'application form, valid photo ID', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Sure. How much cash do I need to deposit at the time of opening an account?', '好的。开户时我需要存入多少现金？', NULL, NULL, NULL, 'deposit, bank account', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Well, the initial deposit is 25 dollars. And you will also get an ATM card.', '初始存款是 25 美元，您还会得到一张 ATM 卡。', NULL, NULL, NULL, 'initial deposit, ATM card', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Okay, I will put 30 dollars in my account.', '好的，我会把 30 美元存入我的账户。', NULL, NULL, NULL, 'account, deposit', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'Thank you, could you please sign on this line?', '谢谢，请您在这条线上签字好吗？', NULL, NULL, NULL, 'sign, bank account', 1),

    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you have your own bank account(s)? How do you choose a bank to open an account?', '你有自己的银行账户吗？你怎样选择开户银行？', NULL, '可考虑大型银行、提供促销和优惠的银行、位置是否便利以及网点数量。', NULL, 'bank account, choose a bank', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you have the habit of saving money? Can you provide some money-saving tips?', '你有存钱的习惯吗？能给出一些省钱建议吗？', NULL, '可在超市临近关门时买食物并在家做饭；也可开设定期存款账户并关联储蓄账户，每月固定转一笔钱进去。', NULL, 'saving money, time deposit, savings', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Do you have a credit card? When do you usually use it? Why do you think some people never apply for a credit card?', '你有信用卡吗？通常什么时候用？为什么有些人从不申请信用卡？', NULL, '可在购买贵重物品、现金不足或想享受信用卡优惠时使用。有人不办卡是为了控制支出、避免银行费用和过度消费，或觉得移动支付已经足够。', NULL, 'credit card, saving money, bank', 1),

    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'What do I need to open an account?\nHow much cash do I need to deposit at the time of opening an account?', '复习：initial / deposit / valid / account。', NULL, NULL, NULL, 'review, bank account', 1),

    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Check eligibility', 'Make sure you''re eligible to open an account.', '确认你有资格开立账户。', NULL, '课后拓展：开户步骤。', NULL, 'eligible, bank account', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Choose a bank', 'Choose the bank that''s best for you: a large chain bank or a smaller local bank.', '选择最适合你的银行：大型连锁银行或较小的本地银行。', NULL, '课后拓展：开户步骤。', NULL, 'chain bank, local bank', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Ask important questions', 'Visit your bank and ask important questions before you finalize your account, such as whether there is a monthly maintenance fee and what minimum balance you must keep.', '在最终开户前到银行询问重要问题，例如是否有月度账户管理费，以及必须保持的最低余额。', NULL, '课后拓展：开户步骤。', NULL, 'monthly fee, minimum balance, bank', 1),
    ('opening-a-bank-account', 'Chapter 4 · Daily Life', 'Lesson 32 · Opening a Bank Account', 32, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Supply the necessary information', 'Supply the necessary information to create your account.', '提供开立账户所需的信息。', NULL, '课后拓展：开户步骤。', NULL, 'information, bank account', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

COMMIT;
