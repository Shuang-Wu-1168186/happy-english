-- Extracted from the next ten available PDFs in doc/, ordered by source file identifier.
-- Sources: Learn & Talk I, Chapter 8 Lessons 71-73 and Chapter 9 Lessons 76-82.
-- Source PDFs for Lessons 74 and 75 were unavailable during this import.
-- The target table is created by aliyun_daily_spoken_dialogue_buying_clothes.sql.
-- Re-running this file updates only the lesson_code/item_order pairs below.

SET NAMES utf8mb4;
START TRANSACTION;

-- Lesson 71 · Chinese Medicine (doc/116223_813_Chinese Medicine.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'acupuncture', 'acupuncture', '针灸', '/ˈækjupʌŋktʃər/', 'a Chinese method of treating pain and illness using special thin needles pushed into particular parts of the body', 'Using acupuncture to treat diseases is a way of medical therapy.', 'acupuncture, Chinese medicine, health', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'traditional', 'traditional', '传统的', '/trəˈdɪʃənl/', 'being part of the beliefs, customs, or way of life of a group of people that has not changed for a long time', 'My grandpa loves traditional Chinese medicine.', 'traditional, Chinese medicine, culture', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'occurrence', 'occurrence', '发生', '/əˈkɜːrəns/', 'the fact of something happening or existing', 'The occurrence of the plane crash is really a tragedy.', 'occurrence, development, disease', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'herb', 'herb', '药草', '/ɝːb/', 'a plant whose leaves, flowers, or seeds are used in medicines', 'She has an herb garden.', 'herb, Chinese medicine, treatment', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'mineral', 'mineral', '矿物；矿物质', '/ˈmɪnərəl/', 'a substance naturally present in the earth; some minerals are also in food, drink, and the human body and are necessary for good health', 'His body needs more minerals.', 'mineral, health, nutrition', 1),

    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Doctor', NULL, 'Hello, Mr. Smith. How are you feeling today?', '您好，Smith 先生。您今天感觉如何？', NULL, NULL, NULL, 'doctor, health', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Patient', NULL, 'Much better, thank you! I can sit straight today. The acupuncture is really great.', '好多了，谢谢！我今天能坐直了。针灸真的很棒。', NULL, NULL, NULL, 'acupuncture, treatment', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Doctor', NULL, 'Yes, Chinese medicine has a history of more than 5,000 years. It has a complete theory about the occurrence, development and treatment of diseases.', '是的，中医已有五千多年历史。它对疾病的发生、发展和治疗有完整的理论。', NULL, NULL, NULL, 'Chinese medicine, occurrence, treatment', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Patient', NULL, 'How do Chinese doctors treat their patients?', '中医怎样治疗病人？', NULL, NULL, NULL, 'Chinese doctors, treatment', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Doctor', NULL, 'Traditional medicines are often used, such as herbs, minerals, and so on.', '常会使用中药，例如药草、矿物质等。', NULL, NULL, NULL, 'traditional medicine, herbs, minerals', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Patient', NULL, 'Thank you very much, Doctor. I''ve got a better understanding of traditional Chinese medicine now.', '非常感谢您，医生。我现在对传统中医有了更好的了解。', NULL, NULL, NULL, 'traditional Chinese medicine, understanding', 1),

    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Have you ever tried any treatment of traditional Chinese medicine? For example, acupuncture, which makes good use of needles?', '你试过传统中医的治疗吗？例如充分利用针的针灸？', NULL, '根据课件提示补全。', NULL, 'Chinese medicine, acupuncture', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'No, it sounds too scary; I''m afraid of needles.', '没有，听起来太可怕了；我怕针。', NULL, NULL, NULL, 'needles, acupuncture', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'How about some herbs? Traditional Chinese doctors often use plants to treat the patients.', '那药草怎么样？中医经常用植物治疗病人。', NULL, NULL, NULL, 'herbs, Chinese doctors', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'That sounds okay for me. What else do Chinese doctors use?', '这个我可以接受。中医还会用什么？', NULL, NULL, NULL, 'Chinese doctors, treatment', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Sometimes they give patients minerals. You know, these are good for your health as well as vitamins.', '有时他们会给病人矿物质。你知道，它们和维生素一样对健康有益。', NULL, NULL, NULL, 'minerals, vitamins, health', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Thank you for your introduction. Someday I may give it a try.', '谢谢你的介绍。总有一天我可能会试一试。', NULL, NULL, NULL, 'Chinese medicine, treatment', 1),

    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you or someone you know ever tried treatments of Chinese medicine? Why or why not? What do you think of the treatment?', '你或你认识的人尝试过中医治疗吗？为什么？你怎么看这种治疗？', NULL, '可谈中药、药草、针灸或拔火罐；也可谈觉得有趣、有效，或觉得可怕、古怪、害怕。', NULL, 'Chinese medicine, acupuncture, treatment', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Comparing traditional Chinese medicine with western medicine, which one do you prefer or use more often? Why?', '比较传统中医和西医，你更喜欢或更常使用哪一种？为什么？', NULL, '可比较持久效果、恢复速度、使用范围和副作用。', NULL, 'Chinese medicine, western medicine, health', 1),

    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'It has a complete theory about the occurrence, development and treatment of diseases.\nI''ve got a better understanding of Chinese medicine now.', '复习：acupuncture / traditional / occurrence / herb / mineral。', NULL, NULL, NULL, 'review, Chinese medicine', 1),

    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'diagnosis through observation', 'diagnosis through observation', '望诊', NULL, '课后拓展：中医四诊。', NULL, 'Chinese medicine, diagnosis', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'diagnosis through auscultation and olfaction', 'diagnosis through auscultation and olfaction', '闻诊', NULL, '课后拓展：中医四诊。', NULL, 'Chinese medicine, diagnosis', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'diagnosis through inquiry', 'diagnosis through inquiry', '问诊', NULL, '课后拓展：中医四诊。', NULL, 'Chinese medicine, diagnosis', 1),
    ('chinese-medicine', 'Chapter 8 · Health', 'Lesson 71 · Chinese Medicine', 71, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'diagnosis through pulse feeling', 'diagnosis through pulse feeling', '切诊', NULL, '课后拓展：中医四诊。', NULL, 'Chinese medicine, diagnosis', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 72 · Plastic Surgery (doc/116290_813_Plastic Surgery.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'plastic surgery', 'plastic surgery', '整容手术', '/ˌplæstɪk ˈsɜːrdʒəri/', 'medical operations to repair injury to a person''s skin or to improve a person''s appearance', 'She needs extensive plastic surgery to her face.', 'plastic surgery, appearance, health', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'wrinkle', 'wrinkle', '皱纹', '/ˈrɪŋkl/', 'a line or small fold in your skin, especially on your face, that forms as you get older', 'There were fine wrinkles around her eyes.', 'wrinkle, appearance, face', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'ridiculous', 'ridiculous', '荒唐的；胡闹的', '/rɪˈdɪkjələs/', 'very silly or unreasonable', 'Don''t be ridiculous! You can''t pay $480 for a T-shirt!', 'ridiculous, opinion, appearance', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'weird', 'weird', '古怪的', '/wɪrd/', 'strange in a mysterious and frightening way', 'The fish began to make weird, horrible sounds.', 'weird, appearance, opinion', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'black and blue', 'black and blue', '青一块紫一块；遍体鳞伤', NULL, 'if a part of your body is black and blue, it is badly bruised', 'She was black and blue all over after falling down the stairs.', 'black and blue, bruise, surgery', 1),

    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Carol', NULL, 'Look at me! I look as if I were 40. I think it''s time for some plastic surgery.', '看看我！我看起来好像四十岁了。我觉得该做点整容手术了。', NULL, NULL, NULL, 'plastic surgery, appearance', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Amy', NULL, 'Come on, you''re only 20. I don''t see any wrinkles on your face. Stop being ridiculous.', '拜托，你才二十岁。我看不到你脸上有任何皱纹。别胡闹了。', NULL, NULL, NULL, 'wrinkles, ridiculous', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Carol', NULL, 'Whatever. I think I''m gonna get a nose job.', '随便。我想我会去做个隆鼻手术。', NULL, NULL, NULL, 'nose job, plastic surgery', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Amy', NULL, 'I honestly don''t think you need it. Besides, people who had plastic surgery look weird and unnatural.', '我真的认为你不需要做。况且，做过整容手术的人看起来很古怪、不自然。', NULL, NULL, NULL, 'plastic surgery, weird, unnatural', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Carol', NULL, 'Hey, I thought you were my friend and would support me on this!', '嘿，我以为你是我的朋友，会支持我这件事！', NULL, NULL, NULL, 'support, friends, plastic surgery', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Amy', NULL, 'I like you the way you are! And plastic surgery hurts!', '我喜欢你本来的样子！而且整容手术会痛！', NULL, NULL, NULL, 'plastic surgery, appearance', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Carol', NULL, 'What? Really?', '什么？真的吗？', NULL, NULL, NULL, 'plastic surgery, reaction', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Amy', NULL, 'Yeah! When I got my nose job, I was black and blue for a week!', '是啊！我做隆鼻手术后，整整一周都青一块紫一块的！', NULL, NULL, NULL, 'nose job, black and blue', 1),

    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'I''ve got two wrinkles around my left eye. I need plastic surgery to remove them.', '我的左眼周围有两道皱纹。我需要整容手术去掉它们。', NULL, '根据课件提示补全。', NULL, 'wrinkles, plastic surgery', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'What? Don''t be ridiculous. No one will need a surgery for that reason. Besides, you still look beautiful.', '什么？别荒唐了。没人会为这个理由做手术。况且，你看起来仍然很漂亮。', NULL, NULL, NULL, 'ridiculous, surgery, appearance', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Hey, aren''t you my friend? I thought you would support me on this.', '嘿，你不是我朋友吗？我以为你会支持我。', NULL, NULL, NULL, 'support, friends', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'I am, but I really don''t like this idea.', '我是，但我真的不喜欢这个想法。', NULL, NULL, NULL, 'opinion, friends', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'So, what do you think of plastic surgery? You don''t like it, do you?', '那么，你怎么看整容手术？你不喜欢它，对吗？', NULL, NULL, NULL, 'plastic surgery, opinion', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Nope. I think people who had this surgery look weird and unnatural.', '不喜欢。我觉得做过这种手术的人看起来古怪、不自然。', NULL, NULL, NULL, 'weird, unnatural, plastic surgery', 1),

    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you or someone you know had plastic surgery? Is plastic surgery popular in China? Why?', '你或你认识的人做过整容手术吗？整容手术在中国流行吗？为什么？', NULL, '可谈手术更负担得起、更多人想改善外貌、受韩国潮流影响；也可谈价格高、风险和副作用。', NULL, 'plastic surgery, appearance, China', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Some people say that plastic surgery is a shortcut to beauty. Do you agree or disagree? Why?', '有人说整容手术是变美的捷径。你同意还是不同意？为什么？', NULL, '可谈去除皱纹、迅速变美，或未来可能需要更多手术；也可谈运动加饮食。', NULL, 'plastic surgery, beauty, opinion', 1),

    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I don''t see any wrinkles on your face.\nWhen I got my nose job, I was black and blue for a week.', '复习：plastic surgery / wrinkle / ridiculous / weird / black and blue。', NULL, NULL, NULL, 'review, plastic surgery', 1),

    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'double eyelid operation', 'double eyelid operation', '双眼皮手术', NULL, '课后拓展：整容手术词汇。', NULL, 'plastic surgery, eyelid', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'facelift', 'facelift', '拉皮手术', NULL, '课后拓展：整容手术词汇。', NULL, 'plastic surgery, facelift', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'lip implants', 'lip implants', '丰唇手术', NULL, '课后拓展：整容手术词汇。', NULL, 'plastic surgery, lips', 1),
    ('plastic-surgery', 'Chapter 8 · Health', 'Lesson 72 · Plastic Surgery', 72, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'chin implants', 'chin implants', '垫下巴手术', NULL, '课后拓展：整容手术词汇。', NULL, 'plastic surgery, chin', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 73 · Staying Up Late (doc/116291_813_Staying Up Late.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'stay up', 'stay up', '熬夜', '/steɪ ʌp/', 'to go to bed later than usual', 'I stayed up half the night playing computer games.', 'stay up, sleep, health', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'average', 'average', '平均；平均数', '/ˈævərɪdʒ/', 'typical or normal; as a verb, to be or come to an average', 'Adults should average 8 hours of sleep per night.', 'average, sleep, health', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'nervous', 'nervous', '紧张的', '/ˈnɜːrvəs/', 'anxious about something or afraid of something', 'I''m too nervous to have a speech.', 'nervous, sleep, exams', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'fall asleep', 'fall asleep', '睡着；进入梦乡', '/fɔːl əˈsliːp/', 'to start to sleep', 'The cat fell asleep right away.', 'fall asleep, sleep, health', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'condition', 'condition', '条件；实际环境', '/kənˈdɪʃn/', 'the state that something is in, or the physical situation that someone or something is in and affected by', 'The house is in a generally poor condition. / He needs a better living condition.', 'condition, sleep, health', 1),

    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'How many hours do you need for sleep?', '你需要睡几个小时？', NULL, NULL, NULL, 'sleep, health', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'I heard that adults should average 8 hours of sleep per night.', '我听说成年人每晚平均应该睡八小时。', NULL, NULL, NULL, 'average, sleep, adults', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'Yes, I heard 6-8 hours is what most people need. Did you ever stay up late?', '是的，我听说大部分人需要六到八小时。你熬过夜吗？', NULL, NULL, NULL, 'stay up, sleep', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'Yes, I''m too nervous to fall asleep every time before the exams and the papers are due.', '是的，每次考试和论文截止前，我都紧张得睡不着。', NULL, NULL, NULL, 'nervous, fall asleep, exams', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'Me too, so what do you need to do to get ideal sleep?', '我也是。那么要获得理想睡眠，你需要做什么？', NULL, NULL, NULL, 'ideal sleep, health', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'I think the first thing to do is to have a clear mind. The second thing is not to have sugar, alcohol and caffeine before sleep. Probably, the third thing is to have an ideal sleep condition.', '我认为第一件事是保持清醒的头脑。第二件事是睡前不要摄入糖、酒和咖啡因。第三件事可能是有理想的睡眠环境。', NULL, NULL, NULL, 'clear mind, caffeine, sleep condition', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'Thank you for sharing. It''s really helpful.', '谢谢你的分享。这真的很有帮助。', NULL, NULL, NULL, 'sleep, advice', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Mary', NULL, 'You''re welcome.', '不客气。', NULL, NULL, NULL, 'sleep, advice', 1),

    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Why do you stay up until now? It''s already 1 a.m.', '你为什么熬到现在？已经凌晨一点了。', NULL, '根据课件提示补全。', NULL, 'stay up, sleep', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'The exam is coming next week, and I haven''t prepared for it at all. I''m so nervous.', '下周就要考试了，我一点也没准备。我太紧张了。', NULL, NULL, NULL, 'exam, nervous, sleep', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'You can prepare for it by day. Perhaps an average of 8-hour sleep will help you learn more efficiently.', '你可以白天准备。平均八小时的睡眠也许能帮助你更高效学习。', NULL, NULL, NULL, 'average, sleep, study', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'But I just can''t fall asleep.', '但我就是睡不着。', NULL, NULL, NULL, 'fall asleep, nervous', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'How about clearing your mind and drinking a cup of milk?', '清空思绪，再喝杯牛奶怎么样？', NULL, NULL, NULL, 'clear mind, sleep', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'I''ll try. Thanks anyway.', '我会试试。还是谢谢你。', NULL, NULL, NULL, 'sleep, advice', 1),

    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you often stay up? Why or why not? Talk about an experience when you stayed up late. What happened then?', '你经常熬夜吗？为什么？谈谈一次熬夜的经历，当时发生了什么？', NULL, '可谈已经养成熬夜习惯，或熬夜不健康、第二天会头痛。', NULL, 'stay up, sleep, health', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'How long do you sleep every night? If you do not sleep enough or well, how do you feel and how do you adjust yourself?', '你每晚睡多久？如果睡眠不足或睡不好，会有什么感觉，如何调整？', NULL, '可谈筋疲力尽、头痛、喝咖啡或小睡。', NULL, 'sleep, health, adjustment', 1),

    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I''m too nervous to fall asleep every time before the exam and the paper due.\nWhat do you need to do to get ideal sleep?', '复习：average / stay up / nervous / fall asleep / condition。', NULL, NULL, NULL, 'review, staying up late', 1),

    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'dark circle', 'dark circle', '黑眼圈', NULL, '课后拓展：熬夜相关词汇。', NULL, 'dark circle, staying up late', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'dullness', 'dullness', '暗沉', NULL, '课后拓展：熬夜相关词汇。', NULL, 'dullness, staying up late', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'stain', 'stain', '色斑', NULL, '课后拓展：熬夜相关词汇。', NULL, 'stain, staying up late', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'decreased vision', 'decreased vision', '视力降低', NULL, '课后拓展：熬夜相关词汇。', NULL, 'vision, staying up late', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'puffy', 'puffy', '水肿的', NULL, '课后拓展：熬夜相关词汇。', NULL, 'puffy, staying up late', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'wrinkle', 'wrinkle', '皱纹', NULL, '课后拓展：熬夜相关词汇。', NULL, 'wrinkle, staying up late', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'extra', '拓展学习', 6, 'extra', 507, NULL, 'hallucination', 'hallucination', '幻觉', NULL, '课后拓展：熬夜相关词汇。', NULL, 'hallucination, staying up late', 1),
    ('staying-up-late', 'Chapter 8 · Health', 'Lesson 73 · Staying Up Late', 73, 'extra', '拓展学习', 6, 'extra', 508, NULL, 'irritable', 'irritable', '易怒的；暴躁的', NULL, '课后拓展：熬夜相关词汇。', NULL, 'irritable, staying up late', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 76 · The Only Child (doc/116368_814_The Only Child.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'dedicate', 'dedicate', '致力；奉献', '/ˈdedɪkeɪt/', 'to give a lot of your time and effort to a particular activity or purpose because you think it is important', 'They dedicate their time to work.', 'dedicate, family, attention', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'attention', 'attention', '关注', '/əˈtenʃn/', 'interest that people show in somebody or something', 'As the youngest child, he was always the center of attention.', 'attention, family, only child', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'deserve', 'deserve', '应得', '/dɪˈzɜːrv/', 'to have a right to something because of the way you have behaved or because of what you are', 'She deserves a rest after all that hard work.', 'deserve, family, attention', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'sibling', 'sibling', '兄弟姐妹', '/ˈsɪblɪŋ/', 'a brother or sister', 'The younger children were well treated by older siblings.', 'sibling, family, only child', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'share', 'share', '分享；共用', '/ʃer/', 'to have or use something at the same time as somebody else', 'They are sharing some food together.', 'share, sibling, family', 1),

    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'What do you think about being the only child? Is it a blessing or a curse?', '你怎么看独生子女？它是祝福还是诅咒？', NULL, NULL, NULL, 'only child, family', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'In my opinion, with one kid, parents can dedicate all the time and energy to make sure that the kid has the attention that he or she deserves.', '我认为，只有一个孩子时，父母可以投入全部时间和精力，确保孩子得到应得的关注。', NULL, NULL, NULL, 'dedicate, attention, deserve', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'Yes, with siblings, some attention is taken away from you, but I love having a sibling growing up with me. I will have 2 or 3 kids in the future, because I want them to have someone to protect.', '是的，有兄弟姐妹时，一些关注会从你身上分走，但我喜欢有兄弟姐妹陪我长大。以后我会要两三个孩子，因为我希望他们有可以保护的人。', NULL, NULL, NULL, 'siblings, attention, family', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'It doesn''t always work out that way. I like having some sister time with my cousin, but I don''t like sharing. Being the only child, I can have whatever I want.', '事情不总是那样发展。我喜欢和表姐妹相处的时光，但我不喜欢分享。作为独生子女，我可以拥有想要的一切。', NULL, NULL, NULL, 'only child, cousin, sharing', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'I guess being the only child and having siblings both have advantages and disadvantages.', '我想当独生子女和有兄弟姐妹都有优点和缺点。', NULL, NULL, NULL, 'only child, siblings, advantages', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'I agree with you on that.', '我同意你的看法。', NULL, NULL, NULL, 'agreement, family', 1),

    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'You are the only child in your family, so how do you feel about it?', '你是家里的独生子女，那么你对此感觉如何？', NULL, '根据课件提示补全。', NULL, 'only child, family', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Truly I can get all the attention from my parents, but sometimes I wish I could have someone to protect.', '确实，我能得到父母所有的关注，但有时我希望有个人可以保护。', NULL, NULL, NULL, 'attention, parents, only child', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I do enjoy having a sibling. We can share some happiness and sadness, and I think I have already got enough attention that I deserve.', '我确实喜欢有兄弟姐妹。我们可以分享快乐和悲伤，而且我觉得我已经得到了应得的足够关注。', NULL, NULL, NULL, 'sibling, share, deserve', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'I guess that''s also true. Luckily, I have a very close cousin.', '我想这也是真的。幸运的是，我有一位很亲近的表亲。', NULL, NULL, NULL, 'cousin, family', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'I''m really happy for you.', '我真为你高兴。', NULL, NULL, NULL, 'family, friendship', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Thank you.', '谢谢。', NULL, NULL, NULL, 'family, friendship', 1),

    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Are you the only child in your family? How do you feel about being or not being the only child?', '你是家里的独生子女吗？你如何看待自己是或不是独生子女？', NULL, '可谈拥有全部关注、不需要分享、感到孤独；或有可以建立纽带的兄弟姐妹、存在手足竞争。', NULL, 'only child, sibling, family', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Which is better, being an only child or having a sibling? Why? How many children would you like to have in the future?', '独生子女和有兄弟姐妹，哪一种更好？为什么？以后你想要几个孩子？', NULL, '可谈独生子女有更多父母的爱和私人空间；有兄弟姐妹不会孤单，可以分享，也像朋友。', NULL, 'only child, sibling, future family', 1),

    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Parents can dedicate all the time and energy to make sure that the kid has the attention that he or she deserves.\nI will have 2 or 3 kids in the future, because I want them to have someone to protect.', '复习：dedicate / attention / deserve / sibling / share。', NULL, NULL, NULL, 'review, only child', 1),

    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Have another one', 'Some parents may want more children, but fertility issues, financial problems, or lifestyle circumstances can make it impossible.', '“再要一个。”有些父母想要更多孩子，但生育、经济或生活状况可能使这无法实现。', NULL, '课后拓展：不要对独生子女父母作主观判断。', NULL, 'only child, parents, family', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Kids need siblings', 'The lesson notes that a healthy and sensible parent is the best gift a child can receive.', '“孩子需要兄弟姐妹。”课件指出，健康、理智的父母才是能给孩子最好的礼物。', NULL, '课后拓展：不要对独生子女父母作主观判断。', NULL, 'only child, siblings, parents', 1),
    ('the-only-child', 'Chapter 9 · Socializing', 'Lesson 76 · The Only Child', 76, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Only children are lonely', 'Do not assume that every only child feels the same way; avoid imposing your own thoughts on others.', '“独生子女都很孤独。”不要假设每一位独生子女都有同样的感受，也不要把自己的想法强加给别人。', NULL, '课后拓展：不要对独生子女父母作主观判断。', NULL, 'only child, family, empathy', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 77 · Arguing with Your Friend (doc/116405_814_Arguing with Your Friend.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'argument', 'argument', '争吵', '/ˈɑːrɡjumənt/', 'a conversation or discussion in which two or more people disagree, often angrily; the verb is argue', 'She got into an argument with her husband.', 'argument, friendship, disagreement', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'disagreement', 'disagreement', '不一致；争论；意见不同', '/ˌdɪsəˈɡriːmənt/', 'a situation where people have different opinions about something and often argue', 'There''s no room for disagreement on this point.', 'disagreement, argument, friendship', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'patch up', 'patch (something) up', '和好；修补关系', '/pætʃ ʌp/', 'to try to stop arguing with somebody and be friends again', 'They patched their friendship up. / They patched things up.', 'patch up, friendship, argument', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'ruin', 'ruin', '毁灭；破坏', '/ˈruːɪn/', 'to damage something so badly that it loses all its value or pleasure; to spoil something', 'The wild fire ruined the whole forest.', 'ruin, friendship, argument', 1),

    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'I had a big argument with David yesterday. I hope he''s not still mad at me.', '我昨天和 David 大吵了一架。我希望他没有还在生我的气。', NULL, NULL, NULL, 'argument, friendship', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'What did you argue about?', '你们为什么争吵？', NULL, NULL, NULL, 'argument, friendship', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'He borrowed my iPad and I needed it back, but he said he needed it one more night.', '他借了我的 iPad，我需要拿回来，但他说还需要再用一晚。', NULL, NULL, NULL, 'borrow, argument, friendship', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'Well, he should return it. It''s only fair.', '嗯，他应该还回来。这才公平。', NULL, NULL, NULL, 'return, fairness, friendship', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'Yes, but I got angry with him too quickly. He probably thought that I mistrusted him. I shouldn''t have got angry.', '是的，但我太快就对他生气了。他可能觉得我不信任他。我不该生气。', NULL, NULL, NULL, 'mistrust, argument, apology', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'Well, talk to him about it next time you see him. He probably feels as bad about it as you do. Close friends sometimes have disagreements. It''s nothing unusual.', '下次见到他时和他谈谈。他可能和你一样难受。亲密朋友有时会有分歧，这没什么不寻常的。', NULL, NULL, NULL, 'disagreements, close friends', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'I guess you''re right. We should patch things up.', '我想你是对的。我们应该和好。', NULL, NULL, NULL, 'patch up, friendship', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Mary', NULL, 'Of course, you should. You wouldn''t want a silly argument to ruin a long-term friendship, would you?', '当然应该。你不会想让一场无谓的争吵毁掉长期友谊，对吧？', NULL, NULL, NULL, 'ruin, long-term friendship', 1),

    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'I''m sorry. I shouldn''t have an argument with you yesterday.', '对不起。我昨天不应该和你争吵。', NULL, '根据课件提示补全。', NULL, 'argument, apology', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'No, it''s my fault. I shouldn''t be late for the movie.', '不，是我的错。我不该看电影迟到。', NULL, NULL, NULL, 'fault, apology, friendship', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I''m so glad that you are not still mad at me, and we can patch things up.', '我很高兴你没有还在生我的气，我们可以和好。', NULL, NULL, NULL, 'patch up, friendship', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Don''t be ridiculous. Close friends sometimes have disagreements, and I won''t let a silly argument ruin our friendship.', '别傻了。亲密朋友有时会有分歧，我不会让一场无谓的争吵毁掉我们的友谊。', NULL, NULL, NULL, 'disagreements, ruin, friendship', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'I''m still so glad to have you back.', '我还是很高兴我们重归于好。', NULL, NULL, NULL, 'friendship, patch up', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'So am I.', '我也是。', NULL, NULL, NULL, 'friendship, agreement', 1),

    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Talk about an experience when you argued with your friend. What were you arguing about? Did you patch up later, and why?', '谈谈一次你和朋友争吵的经历。你们为什么争吵？后来和好了吗，为什么？', NULL, '可谈被不信任、秘密被说给别人；也可谈争吵无谓、友谊牢固，或不能原谅、拒绝道歉。', NULL, 'argument, patch up, friendship', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'If you have an argument with your friend and it is your fault, what will you do? How about when it is his or her fault?', '如果你和朋友争吵且是你的错，你会怎么做？如果是对方的错呢？', NULL, '可谈主动道歉、因羞愧难以开口；或先表达善意、等待对方道歉。', NULL, 'argument, apology, friendship', 1),

    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Close friends sometimes have disagreements. It''s nothing unusual.\nYou wouldn''t want a silly argument to ruin a long friendship, would you?', '复习：argument / disagreement / patch up / ruin。', NULL, NULL, NULL, 'review, arguing with friend', 1),

    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Calm down first', 'Wait until you have had time to calm down.', '先等到自己有时间冷静下来。', NULL, '课后拓展：与朋友和好的步骤。', NULL, 'patch up, calm down, friendship', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Plan key points', 'Plan your key talking points.', '规划好要谈的重点。', NULL, '课后拓展：与朋友和好的步骤。', NULL, 'patch up, communication, friendship', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Meet privately', 'Ask your friend to meet up with you and choose a private place where you both feel comfortable.', '约朋友见面，并选择让双方都舒服的私密地点。', NULL, '课后拓展：与朋友和好的步骤。', NULL, 'patch up, meeting, friendship', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Speak calmly', 'Speak calmly, make eye contact, and avoid pinning the blame on your friend.', '平静表达、保持眼神交流，避免把责任推给朋友。', NULL, '课后拓展：与朋友和好的步骤。', NULL, 'patch up, communication, blame', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'Listen to the other side', 'Listen to your friend''s side of the story.', '倾听朋友那一边的说法。', NULL, '课后拓展：与朋友和好的步骤。', NULL, 'patch up, listen, friendship', 1),
    ('arguing-with-your-friend', 'Chapter 9 · Socializing', 'Lesson 77 · Arguing with Your Friend', 77, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'Find a compromise', 'Talk about your ideal solution and listen to your friend''s. Negotiate until you reach a compromise that suits both of you.', '谈谈理想的解决方案，也听取朋友的想法，协商到达双方都适合的妥协。', NULL, '课后拓展：与朋友和好的步骤。', NULL, 'patch up, compromise, friendship', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 78 · Going to a Party (doc/116406_814_Going to a Party.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'turn up', 'turn up', '出现；到场', '/tɜːrn ʌp/', 'of a person, to arrive or show up', 'Nobody turns up in the conference room.', 'turn up, party, socializing', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'squeeze', 'squeeze', '拥挤', '/skwiːz/', 'a situation where it is almost impossible for people or things to fit into a small or restricted space', 'The truck is a squeeze.', 'squeeze, party, crowded', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'look forward to', 'look forward to', '期待', '/lʊk ˈfɔːrwərd tu/', 'to think with pleasure about something that is going to happen because you expect to enjoy it; use look forward to + doing', 'He is looking forward to the sunrise. / I look forward to taking part in a party.', 'look forward to, party, socializing', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'blast', 'blast', '热闹、痛快的时光', '/blæst/', 'a very enjoyable experience that is a lot of fun', 'The party is a blast.', 'blast, party, fun', 1),

    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'Are you going to Helen''s party on Friday evening?', '你周五晚上要去 Helen 的聚会吗？', NULL, NULL, NULL, 'party, invitation', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'I wouldn''t miss it for the world! It''s sure to be fun. She''s invited a lot of people. Do you think everyone will be able to get into her house?', '我绝不会错过！肯定很有趣。她邀请了很多人。你觉得大家都能进她家吗？', NULL, NULL, NULL, 'party, invitation, fun', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'If everyone turned up, it would be a squeeze, but a few people said that they couldn''t go, so I think it should be okay.', '如果所有人都来了，就会很拥挤，不过有几个人说不能去，所以我觉得应该没问题。', NULL, NULL, NULL, 'turn up, squeeze, party', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'Are you taking anything?', '你会带些什么吗？', NULL, NULL, NULL, 'party, gift', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'I''ll take a bottle of wine.', '我会带一瓶酒。', NULL, NULL, NULL, 'party, wine', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'That''s a good idea. She told me she had bought plenty of food and snacks. I''m really looking forward to it. This party is going to be a blast!', '这是个好主意。她告诉我她买了很多食物和零食。我真的很期待。这场聚会一定很热闹！', NULL, NULL, NULL, 'look forward to, blast, party', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'Well, I''ll see you on Friday at Helen''s.', '那周五在 Helen 家见。', NULL, NULL, NULL, 'party, meeting', 1),

    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Today''s party is really a blast!', '今天的聚会真是太热闹了！', NULL, '根据课件提示补全。', NULL, 'blast, party', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes, I have a great time, even though it''s a squeeze.', '是的，我玩得很开心，尽管这里很拥挤。', NULL, NULL, NULL, 'squeeze, party, fun', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'You can''t blame her. Her middle school classmates turned up from nowhere.', '你不能怪她。她的中学同学不知从哪里都来了。', NULL, NULL, NULL, 'turn up, classmates, party', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Anyhow, I enjoyed all the drinks and snacks, and I''m really looking forward to your birthday party next week.', '不管怎样，我喜欢所有饮料和零食，我真的很期待你下周的生日聚会。', NULL, NULL, NULL, 'look forward to, birthday party', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'I''ll make a full preparation for it.', '我会为此做好充分准备。', NULL, NULL, NULL, 'party, preparation', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'And I will prepare you a surprising gift.', '我会给你准备一份惊喜礼物。', NULL, NULL, NULL, 'party, gift', 1),

    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Talk about a party that you have been to. What kind of party was it? What did you do at the party?', '谈谈你参加过的一场聚会。那是什么类型的聚会？你在聚会上做了什么？', NULL, '可谈生日、婚礼或毕业聚会；喝饮料、吃零食、看表演或表演节目。', NULL, 'party, socializing, celebration', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you like attending parties or hosting parties? Why? If you like neither, why?', '你喜欢参加聚会还是举办聚会？为什么？如果两者都不喜欢，为什么？', NULL, '可谈参加聚会更有趣且不必收拾；举办聚会享受做主人和看到朋友开心；也可谈喜欢独处、觉得吵闹或不擅长社交。', NULL, 'attending parties, hosting parties, socializing', 1),

    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'If everyone turned up, it would be a squeeze, but a few people said that they couldn''t go, so I think it should be okay.\nI''m really looking forward to it. This party is going to be a blast!', '复习：turn up / squeeze / look forward to / blast。', NULL, NULL, NULL, 'review, going to a party', 1),

    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'After-party', 'An after-party is held after a musical or theatrical performance, or after another event such as a wedding or school dance.', '后续聚会：在音乐、戏剧表演或婚礼、学校舞会等活动之后举办的聚会。', NULL, '课后拓展：不同类型的聚会。', NULL, 'after-party, party, celebration', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Pre-party', 'A pre-party is held immediately before an event such as a school dance, a wedding, or a birthday party.', '预热聚会：在学校舞会、婚礼或生日聚会等活动之前马上举办的聚会。', NULL, '课后拓展：不同类型的聚会。', NULL, 'pre-party, party, celebration', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Cast party', 'A cast party is a celebration following the final performance of a theatrical event such as a play, musical, or opera.', '剧组庆功宴：在戏剧、音乐剧或歌剧等最后一场表演后举办的庆祝活动。', NULL, '课后拓展：不同类型的聚会。', NULL, 'cast party, theatre, celebration', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Shower', 'A shower is a party whose primary purpose is to give gifts to the guest of honor, commonly a bride-to-be or mother-to-be.', '送礼聚会：主要目的是向主角赠礼，通常为准新娘或准妈妈举办。', NULL, '课后拓展：不同类型的聚会。', NULL, 'shower, gifts, party', 1),
    ('going-to-a-party', 'Chapter 9 · Socializing', 'Lesson 78 · Going to a Party', 78, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'Block party', 'A block party is a public party attended by residents of a specific city block or neighborhood.', '街区聚会：由特定街区或社区居民参加的公开聚会。', NULL, '课后拓展：不同类型的聚会。', NULL, 'block party, neighborhood, socializing', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 79 · Talking about Weather (doc/116434_814_Talking about Weather.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'be raining cats and dogs', 'be raining cats and dogs', '下倾盆大雨', NULL, 'to be raining heavily', 'It''s raining cats and dogs outside.', 'raining cats and dogs, weather, rain', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'miserable', 'miserable', '令人痛苦的', '/ˈmɪzrəbl/', 'making you feel very unhappy or uncomfortable', 'She suffers from a miserable headache.', 'miserable, weather, feeling', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'drought', 'drought', '干旱', '/draʊt/', 'a long period of time when there is little or no rain', 'The country''s entire grain harvest has been hit by drought.', 'drought, weather, climate', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'forecaster', 'forecaster', '预报员', '/ˈfɔːrkæstər/', 'a person who says what is expected to happen, especially someone whose job is to forecast the weather; also weatherman or weathercaster', 'He is a successful forecaster.', 'forecaster, weather, forecast', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'predict', 'predict', '预测', '/prɪˈdɪkt/', 'to say that something will happen in the future; to forecast', 'The weather forecast predicts tomorrow is a sunny day. Related adjective: predictable.', 'predict, forecast, weather', 1),

    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Mary', NULL, 'I thought the sunny day was going to continue.', '我以为晴天会持续下去。', NULL, NULL, NULL, 'sunny day, weather', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Jack', NULL, 'So did I. That''s why I went shopping without my umbrella. I got caught in the rain in the afternoon. It was raining cats and dogs.', '我也是。所以我没带伞就去购物了。下午我被雨淋到了，雨下得倾盆大。', NULL, NULL, NULL, 'umbrella, raining cats and dogs', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Mary', NULL, 'I know. I could not believe it when I got hit by that storm. It was pouring with rain all afternoon.', '我知道。我被那场暴风雨袭击时都不敢相信。整个下午都在下大雨。', NULL, NULL, NULL, 'storm, pouring rain, weather', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Jack', NULL, 'We really have some miserable weather sometimes. I wish I could live somewhere that is sunny all year round.', '我们有时的天气真的很糟。我希望住在全年晴朗的地方。', NULL, NULL, NULL, 'miserable weather, sunny', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Mary', NULL, 'If it was sunny all year round, there would be drought. You probably would not like it either.', '如果全年都晴朗，就会有干旱。你可能也不会喜欢。', NULL, NULL, NULL, 'drought, sunny weather', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Jack', NULL, 'I guess you are right. Maybe I just wish the weather could be a little more predictable.', '我想你是对的。也许我只是希望天气能更容易预测一点。', NULL, NULL, NULL, 'predictable, weather', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Mary', NULL, 'The weather forecasters are not good at predicting the weather. Our weather is so changeable.', '天气预报员不太擅长预测天气。我们的天气太多变了。', NULL, NULL, NULL, 'forecasters, predict, changeable', 1),

    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'What did the forecaster say about tomorrow''s weather?', '预报员怎么说明天的天气？', NULL, '根据课件提示补全。', NULL, 'forecaster, weather', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'He said it will be raining cats and dogs tomorrow.', '他说明天会下倾盆大雨。', NULL, NULL, NULL, 'raining cats and dogs, weather', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Oh! I hate rainy days! It''s such a sunny day today. I have already made a plan to go to the beach tomorrow.', '哦！我讨厌雨天！今天是个大晴天，我已经计划明天去海滩了。', NULL, NULL, NULL, 'rainy days, sunny, beach', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Bad luck! Nobody can predict what will happen tomorrow.', '真倒霉！没人能预测明天会发生什么。', NULL, NULL, NULL, 'predict, weather', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'I guess I''ll have to cancel my plan and spend a miserable weekend.', '我想我得取消计划，过一个痛苦的周末。', NULL, NULL, NULL, 'miserable, cancel, weather', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Maybe tomorrow is a clear day, who knows?', '也许明天是晴天，谁知道呢？', NULL, NULL, NULL, 'clear day, weather', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'Yeah, maybe you are right.', '是啊，也许你是对的。', NULL, NULL, NULL, 'weather, agreement', 1),

    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'How is the weather in your hometown? Talk about your hometown''s weather in four seasons.', '你家乡的天气怎么样？谈谈四季天气。', NULL, '可谈雨、雪、风、暴风雨、沙尘暴、冰雹、台风，以及多雨、多雪、多风、炎热、寒冷、凉爽、雾霾、干燥或潮湿。', NULL, 'weather, hometown, seasons', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'What kind of weather do you like? Is it hot or cold? Is it dry or humid? Give your reasons.', '你喜欢什么天气？热还是冷？干燥还是潮湿？请说明原因。', NULL, '可谈热天少穿衣服、吃冰淇淋；冷天不易出汗、有雪；干燥感觉清新凉爽；潮湿对皮肤更好。', NULL, 'weather, hot, cold, humid', 1),

    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I wish I could live somewhere that is sunny all year round.\nThe weather forecasters are not good at predicting the weather.', '复习：be raining cats and dogs / miserable / drought / forecaster / predict。', NULL, NULL, NULL, 'review, weather', 1),

    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'storm out', 'storm out', '猛冲而出', NULL, 'leave a room quickly and angrily. Example: They had a fight, and then stormed out.', NULL, 'storm out, weather idiom, anger', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'under the weather', 'under the weather', '身体不适', NULL, 'to feel slightly ill or sick and not as well as usual. Example: I''m under the weather today.', NULL, 'under the weather, health, idiom', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'weather a storm', 'weather a storm', '克服困难', NULL, 'to get through a difficult situation. Example: He suffered from a terrible breakup, and now he weathered a storm.', NULL, 'weather a storm, difficulty, idiom', 1),
    ('talking-about-weather', 'Chapter 9 · Socializing', 'Lesson 79 · Talking about Weather', 79, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'get wind of something', 'get wind of something', '听到风声', NULL, 'to learn a piece of information, especially when it has been a secret. Example: We have a crisis on our hands and do not want the press to get wind of it.', NULL, 'get wind of, information, idiom', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 80 · Talking about Hobbies (doc/116480_814_Talking about Hobbies.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'in one''s spare time', 'in one''s spare time', '在某人的空闲时间', NULL, 'time when you are not working or do not have anything you must do', 'She likes to go cycling in her spare time.', 'spare time, hobbies, leisure', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'get into', 'get into', '开始对……感兴趣', '/ɡet ˈɪntu/', 'to become interested in something', 'He gets into reading books.', 'get into, hobbies, interests', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'leisure', 'leisure', '空闲', '/ˈliːʒər/', 'time that is spent doing what you enjoy when you are not working or studying', 'He spends his leisure time cooking.', 'leisure, hobbies, free time', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'be occupied with', 'be occupied with something / doing something', '忙于', NULL, 'to be busy with something or doing something', 'They are occupied with doing their work.', 'occupied, work, hobbies', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'take up', 'take up (something)', '开始从事', '/teɪk ʌp/', 'to learn or start to do something, especially for pleasure', 'He takes up fishing.', 'take up, hobbies, interests', 1),

    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'What do you like to do in your spare time?', '你空闲时喜欢做什么？', NULL, NULL, NULL, 'spare time, hobbies', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'I''ve been getting into photography.', '我开始对摄影感兴趣了。', NULL, NULL, NULL, 'get into, photography, hobbies', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'Photography? Do you often go out to take pictures?', '摄影？你经常出去拍照吗？', NULL, NULL, NULL, 'photography, hobbies', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'I''d love to take more pictures, but I am often occupied with lots of homework. Enough about me, how do you spend your leisure time?', '我很想多拍些照片，但我常忙于很多作业。别说我了，你如何度过闲暇时间？', NULL, NULL, NULL, 'occupied with, homework, leisure', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'I''m occupied with watching football games.', '我忙于看足球比赛。', NULL, NULL, NULL, 'occupied with, football, hobbies', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'Football, when did you take it up?', '足球？你什么时候开始从事它的？', NULL, NULL, NULL, 'take up, football, hobbies', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'I grew up playing and watching football all the time. Football can strengthen my body.', '我从小一直踢球、看球。足球可以强健我的身体。', NULL, NULL, NULL, 'football, hobbies, health', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Mary', NULL, 'You''re right. It''s important to have a healthy body.', '你说得对。拥有健康的身体很重要。', NULL, NULL, NULL, 'healthy body, hobbies', 1),

    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'How do you spend your leisure time?', '你如何度过闲暇时间？', NULL, '根据课件提示补全。', NULL, 'leisure, hobbies', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I am occupied with my work every day. In my spare time, I will just sleep.', '我每天都忙于工作。在空闲时间，我只会睡觉。', NULL, NULL, NULL, 'occupied with, spare time, work', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I think you should take up some sports, like running, cycling, etc.', '我觉得你应该开始做些运动，例如跑步、骑行等。', NULL, NULL, NULL, 'take up, sports, hobbies', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'I am so tired, and just want to get a good rest, doing nothing.', '我很累，只想好好休息，什么也不做。', NULL, NULL, NULL, 'rest, work, hobbies', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'I can understand that feeling, but you really need more exercise.', '我理解那种感觉，但你真的需要更多运动。', NULL, NULL, NULL, 'exercise, health, hobbies', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Thanks for your advice. I''ll try.', '谢谢你的建议。我会试试。', NULL, NULL, NULL, 'advice, exercise, hobbies', 1),

    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'What do you like to do in your spare time? Why? Talk about your hobbies with your teacher.', '你空闲时喜欢做什么？为什么？和老师谈谈你的爱好。', NULL, '可谈运动、电脑游戏、艺术或阅读，以及变得健康、获得乐趣和精神放松。', NULL, 'spare time, hobbies, leisure', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Nowadays, more and more people like to spend leisure time on their computer and smartphone. What do you think about it? Give your reasons.', '如今越来越多人喜欢把闲暇时间花在电脑和智能手机上。你怎么看？请说明理由。', NULL, '可谈过度使用会不健康、减少阅读和运动；也可谈正常使用能带来乐趣和精神放松。', NULL, 'leisure, computer, smartphone, hobbies', 1),

    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'What do you like to do in your spare time?\nI''ve been getting into photography.\nHow do you spend your leisure time?\nI''m occupied with watching football games.', '复习：in one''s spare time / get into / leisure / be occupied with doing / take up。', NULL, NULL, NULL, 'review, hobbies', 1),

    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'competitive mooing', 'Mooing: imitating the call of a cow. Some people take part in competitive mooing.', '模仿牛叫：有些人会参加模仿牛叫比赛。', NULL, '课后拓展：世界上的奇特爱好。', NULL, 'mooing, strange hobbies', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'soap carving', 'People carve commercial soap bars into beautiful sculptures and carefully seal them so they do not disappear.', '肥皂雕刻：把普通肥皂雕成精美雕塑，并仔细密封保存。', NULL, '课后拓展：世界上的奇特爱好。', NULL, 'soap carving, strange hobbies', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'tape art', 'Pull out magnetic tape from inside its casing and use it to create a portrait of the artist.', '磁带艺术：从磁带盒中抽出磁带，用它创作艺术家的肖像。', NULL, '课后拓展：世界上的奇特爱好。', NULL, 'tape art, strange hobbies', 1),
    ('talking-about-hobbies', 'Chapter 9 · Socializing', 'Lesson 80 · Talking about Hobbies', 80, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'trainspotting', 'People watch for trains and record the train numbers when they see them.', '观察火车：看到火车时记录机车号码。', NULL, '课后拓展：世界上的奇特爱好。', NULL, 'trainspotting, strange hobbies', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 81 · Talking about Future Plans (doc/116481_814_Talking about Future Plans.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'graduate', 'graduate', '毕业', '/ˈɡrædʒuət/', 'to get a degree, especially your first degree, from a university or college; use graduate from', 'She graduated from Harvard this year.', 'graduate, future plans, university', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'overcome', 'overcome', '克服', '/ˌoʊvərˈkʌm/', 'to succeed in dealing with or controlling a problem that has prevented you from achieving something', 'He finally managed to overcome his fear of heights.', 'overcome, obstacles, future plans', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'ambition', 'ambition', '抱负；志向', '/æmˈbɪʃn/', 'something that you want to do or achieve very much', 'His ambition is to climb over the mountain.', 'ambition, future plans, goals', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'realistic', 'realistic', '实事求是的；现实的', '/ˌriːəˈlɪstɪk/', 'sensible and appropriate; possible to achieve', 'We must set realistic goals. It is unrealistic to accomplish all missions in one day.', 'realistic, goals, future plans', 1),

    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'What do you hope to do when you finish university?', '大学毕业后你希望做什么？', NULL, NULL, NULL, 'university, future plans', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'I''d like to go into management. How about you?', '我想进入管理行业。你呢？', NULL, NULL, NULL, 'management, future plans', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'After I graduate, I have to do some more studies to pass exams to become a lawyer.', '毕业后，我必须继续学习、通过考试，才能成为律师。', NULL, NULL, NULL, 'graduate, lawyer, study', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'We both have to overcome several obstacles if we are to achieve our ambitions.', '如果要实现抱负，我们都必须克服几个障碍。', NULL, NULL, NULL, 'overcome, obstacles, ambitions', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'If life were easy, then we''d achieve our ambition quickly and then get bored.', '如果生活很容易，我们就会很快实现抱负，然后感到无聊。', NULL, NULL, NULL, 'ambition, life, future plans', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'Unfortunately, it''s inevitable that some people are going to work hard yet not succeed.', '不幸的是，有些人会努力工作却无法成功，这是不可避免的。', NULL, NULL, NULL, 'work hard, success, future plans', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'That''s why ambition needs to be realistic. You can''t achieve something that''s totally unrealistic.', '这就是为什么抱负需要现实。你无法实现完全不现实的事情。', NULL, NULL, NULL, 'ambition, realistic, goals', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Mary', NULL, 'As long as you plan carefully, most things are possible.', '只要认真规划，大多数事情都有可能。', NULL, NULL, NULL, 'plan carefully, future plans', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'dialogue', '示范对话', 2, 'dialogue', 109, 'Jack', NULL, 'You are right about that.', '这一点你是对的。', NULL, NULL, NULL, 'agreement, future plans', 1),

    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'What do you want to do after graduating from college?', '大学毕业后你想做什么？', NULL, '根据课件提示补全。', NULL, 'graduating, college, future plans', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I have an ambition to be a famous singer, but my parents disagree with me.', '我有成为著名歌手的抱负，但父母不同意。', NULL, NULL, NULL, 'ambition, parents, future plans', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Perhaps they think it''s not realistic.', '也许他们觉得这不现实。', NULL, NULL, NULL, 'realistic, future plans', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'I''m also aware of that, but I have liked singing since I was a child.', '我也意识到这一点，但我从小就喜欢唱歌。', NULL, NULL, NULL, 'singing, ambition, future plans', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Okay, if you insist, you need to overcome many difficulties.', '好吧，如果你坚持，你需要克服很多困难。', NULL, NULL, NULL, 'overcome, difficulties, future plans', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'I think I can do that.', '我觉得我能做到。', NULL, NULL, NULL, 'confidence, future plans', 1),

    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Talk about your future plans. Explain why you want to achieve those plans and what you will do to achieve them.', '谈谈你的未来规划。解释为什么想实现它们，以及将如何实现。', NULL, '未来规划可以包括工作、生活或爱好；原因可以谈喜欢和选择；行动可谈学习和存钱。', NULL, 'future plans, goals, ambition', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Are your future plans realistic or unrealistic in your parents'' opinion? If they think they are unrealistic, will you stop? Why?', '在父母看来，你的未来规划是现实还是不现实？如果他们觉得不现实，你会停止吗？为什么？', NULL, '可谈停止是因为不可能实现或没有意义；也可谈不停止，因为相信能成功、享受过程并不过度关注结果。', NULL, 'future plans, parents, realistic', 1),

    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'We both have to overcome several obstacles if we are to achieve our ambitions.\nUnfortunately, it''s inevitable that some people are going to work hard yet not succeed.', '复习：graduate / overcome / ambition / realistic。', NULL, NULL, NULL, 'review, future plans', 1),

    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Choose categories', 'For a five-year plan, choose categories such as healthy goals, financial goals, fun goals, and family goals.', '制定五年计划时，可选择健康、财务、乐趣和家庭等目标类别。', NULL, '课后拓展：如何写五年计划。', NULL, 'five-year plan, goals, future plans', 1),
    ('talking-about-future-plans', 'Chapter 9 · Socializing', 'Lesson 81 · Talking about Future Plans', 81, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Draw up the list', 'Be as specific as possible, identify the most important items on each list, and divide subsidiary goals into individual years.', '尽量具体，找出每张清单上最重要的事项，并把子目标分配到每一年。', NULL, '课后拓展：如何写五年计划。', NULL, 'five-year plan, goals, planning', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 82 · Chatting with Neighbors (doc/116491_814_Chatting with Neighbors.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'community', 'community', '社区', '/kəˈmjuːnəti/', 'all the people who live in a particular area or country when talked about as a group', 'He lives in the community over ten years.', 'community, neighbors, socializing', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'stop by', 'stop by', '顺便拜访', '/stɑːp baɪ/', 'to make a short visit somewhere', 'She stops by to meet her parents.', 'stop by, neighbors, visit', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'convenient', 'convenient', '方便的', '/kənˈviːniənt/', 'useful, easy, or quick to do; not causing problems', 'A bicycle is often more convenient than a car in towns.', 'convenient, community, neighborhood', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'make one''s acquaintance', 'make one''s acquaintance', '初次相识', '/meɪk wʌnz əˈkweɪntəns/', 'to meet someone for the first time', 'They make their acquaintance in the meeting.', 'make acquaintance, neighbors, socializing', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'show somebody around', 'show somebody around', '带某人参观', NULL, 'to be a guide for somebody when they visit a place for the first time and show them what is interesting', 'The tour guide shows the tourists around.', 'show around, community, neighbors', 1),

    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Lucas', NULL, 'Hi, I''m Lucas. I just moved in the community. I just want to stop by to make your acquaintance.', '你好，我是 Lucas。我刚搬到这个社区。我只是想顺便来和你认识一下。', NULL, NULL, NULL, 'community, stop by, make acquaintance', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Barbara', NULL, 'Oh, hi Lucas, come on in. I''m Barbara. Nice to meet you.', '哦，嗨 Lucas，请进。我是 Barbara。很高兴认识你。', NULL, NULL, NULL, 'neighbors, meet', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Lucas', NULL, 'Nice to meet you, too.', '我也很高兴认识你。', NULL, NULL, NULL, 'neighbors, meet', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Barbara', NULL, 'Would you like something to drink? I''ve got tea and some grape juice.', '你想喝点什么吗？我有茶和一些葡萄汁。', NULL, NULL, NULL, 'neighbors, hospitality', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Lucas', NULL, 'Thanks. Some tea would be nice. Chinese tea is great. I really like your tea. Where did you get it?', '谢谢。来点茶就很好。中国茶很棒。我真的喜欢你的茶。你在哪里买的？', NULL, NULL, NULL, 'Chinese tea, neighbors', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Barbara', NULL, 'Oh, there is a supermarket not far from here. It''s quiet and very convenient. You can get to the bus and the subway stations within ten minutes'' walk. There''s a grocery store, a book store, a gym, and many restaurants along the street. If you like, I can show you around.', '哦，这里不远有个超市。那里安静又方便。步行十分钟可以到公交站和地铁站。沿街还有杂货店、书店、健身房和很多餐馆。如果你愿意，我可以带你四处看看。', NULL, NULL, NULL, 'convenient, community, show around', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Lucas', NULL, 'Thank you for offering help. That would be wonderful.', '谢谢你愿意帮忙。那太好了。', NULL, NULL, NULL, 'neighbors, help, community', 1),

    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Hello, neighbor. I just want to stop by and personally welcome you to the neighborhood.', '你好，邻居。我只是想顺便来，亲自欢迎你来到这个社区。', NULL, '根据课件提示补全。', NULL, 'stop by, neighborhood, neighbors', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Thank you! It''s a pleasure to make your acquaintance.', '谢谢！很高兴认识你。', NULL, NULL, NULL, 'make acquaintance, neighbors', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Same here. It''s been a few days. How do you like it so far?', '我也是。已经几天了。到目前为止你觉得怎么样？', NULL, NULL, NULL, 'neighbors, community', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'I like it. It''s convenient for both my job and my family.', '我喜欢这里。它对我的工作和家人都很方便。', NULL, NULL, NULL, 'convenient, community, family', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'I''m glad to hear that. If you have time, I am willing to show you around.', '听到这个我很高兴。如果你有时间，我愿意带你四处看看。', NULL, NULL, NULL, 'show around, neighbors, community', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'That sounds good. I''m not quite familiar with the community.', '听起来不错。我对这个社区还不太熟悉。', NULL, NULL, NULL, 'community, neighbors', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'Let''s go!', '我们走吧！', NULL, NULL, NULL, 'community, neighbors', 1),

    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you ever chatted with your neighbors? Do you think it is important to know and chat with your neighbors? Talk about your reasons.', '你和邻居聊过天吗？你认为认识并和邻居聊天重要吗？谈谈原因。', NULL, '可谈成为朋友、需要时互相帮助；也可谈聊天没有意义或可能被迫帮助别人。', NULL, 'neighbors, community, socializing', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'What kind of community are you in: one with more older people or more young people? If you could choose, which would you choose to live in? Why?', '你所在的社区是老年人更多还是年轻人更多？如果可以选择，你会选择住在哪种社区？为什么？', NULL, '可谈年轻人作息相近、容易交朋友；或老年人大多友善、噪音更少。', NULL, 'community, older people, young people', 1),

    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I just moved in the community. I just want to stop by to make your acquaintance.\nIf you like, I can show you around.\nYou are so generous to offer help. That would be wonderful. Thanks!', '复习：community / stop by / convenient / make one''s acquaintance / show somebody around。', NULL, NULL, NULL, 'review, chatting with neighbors', 1),

    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'mowing the lawn', 'mowing the lawn', '修剪草坪', NULL, '课后拓展：让邻居更亲近的活动。', NULL, 'neighbors, lawn, community', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'shoveling snow', 'shoveling snow', '铲雪', NULL, '课后拓展：让邻居更亲近的活动。', NULL, 'neighbors, snow, community', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'getting a paper route', 'getting a paper route', '送报纸的工作', NULL, '课后拓展：让邻居更亲近的活动。', NULL, 'neighbors, paper route, community', 1),
    ('chatting-with-neighbors', 'Chapter 9 · Socializing', 'Lesson 82 · Chatting with Neighbors', 82, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'babysitting', 'babysitting', '照看孩子', NULL, '课后拓展：让邻居更亲近的活动。', NULL, 'neighbors, babysitting, community', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

COMMIT;
