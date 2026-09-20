-- English textbook export: schema and all bilingual lesson-card data.
-- Includes CREATE TABLE and idempotent INSERT/UPDATE statements for Unit 1, Lessons 1–6.
-- Run with: mysql -u USER -p DATABASE < scripts/create_english_textbook.sql

SET NAMES utf8mb4;

CREATE TABLE IF NOT EXISTS english_textbook_lesson (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    unit_name VARCHAR(100) NOT NULL,
    lesson_name VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    title_cn VARCHAR(255) DEFAULT NULL,
    summary TEXT DEFAULT NULL,
    unit_order INT NOT NULL DEFAULT 0,
    lesson_order INT NOT NULL DEFAULT 0,
    is_published TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_textbook_unit_lesson (unit_name, lesson_name),
    KEY idx_textbook_lesson_order (is_published, unit_order, lesson_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='英语教材课文';

CREATE TABLE IF NOT EXISTS english_textbook_sentence (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    lesson_id BIGINT UNSIGNED NOT NULL,
    sentence_order INT NOT NULL DEFAULT 0,
    english_text TEXT NOT NULL,
    chinese_text TEXT NOT NULL,
    is_published TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_textbook_sentence_order (lesson_id, sentence_order),
    KEY idx_textbook_sentence_order (lesson_id, is_published, sentence_order),
    CONSTRAINT fk_textbook_sentence_lesson
        FOREIGN KEY (lesson_id) REFERENCES english_textbook_lesson(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='英语教材中英对照句子';

-- Unit 1, Lesson 1. English text below was provided by the user.
INSERT INTO english_textbook_lesson
    (unit_name, lesson_name, title, title_cn, summary, unit_order, lesson_order)
VALUES
    ('Unit 1', 'Lesson 1', 'What did you do this summer?', '这个暑假你做了什么？',
     '暑假活动对话：用一般过去时谈论旅行、家庭活动和运动。', 1, 1)
ON DUPLICATE KEY UPDATE
    title = VALUES(title), title_cn = VALUES(title_cn), summary = VALUES(summary),
    unit_order = VALUES(unit_order), lesson_order = VALUES(lesson_order), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 1, 'Mike: Hello, Baobao and Yangyang!', '迈克：你好，宝宝和阳阳！'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 2, 'Baobao: Hi, Mike!', '宝宝：嗨，迈克！'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 3, 'Baobao: How was your summer holiday?', '宝宝：你的暑假过得怎么样？'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 4, 'Baobao: Where did you go?', '宝宝：你去了哪里？'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 5, 'Mike: It was good!', '迈克：很好！'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 6, 'Mike: I went to see my grandparents in Canada.', '迈克：我去加拿大看望了我的祖父母。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 7, 'Mike: I stayed with them for three weeks.', '迈克：我和他们一起住了三个星期。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 8, 'Mike: What about you, Baobao?', '迈克：你呢，宝宝？'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 9, 'Baobao: I visited some places in Northeast China with my family.', '宝宝：我和家人去了中国东北的一些地方。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 10, 'Baobao: We had a good time there.', '宝宝：我们在那里玩得很开心。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 11, 'Mike: Sounds fun.', '迈克：听起来很有趣。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 12, 'Mike: What did you do there?', '迈克：你在那里做了什么？'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 13, 'Baobao: We went to the beach in Dalian, enjoyed the view of Tianchi Lake on Changbai Mountain, and visited Beijicun in Mohe.', '宝宝：我们去了大连的海滩，欣赏了长白山天池的景色，还参观了漠河的北极村。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 14, 'Yangyang: Wow, that’s wonderful!', '阳阳：哇，太棒了！'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 15, 'Baobao: How was your holiday, Yangyang?', '宝宝：阳阳，你的假期怎么样？'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 16, 'Baobao: Where did you go?', '宝宝：你去了哪里？'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 17, 'Baobao: What did you do there?', '宝宝：你在那里做了什么？'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 18, 'Yangyang: I stayed in Beijing and had a great time, too.', '阳阳：我留在北京，也玩得很开心。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 19, 'Yangyang: My friends and I joined a sports club.', '阳阳：我和朋友们参加了一个体育俱乐部。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 20, 'Yangyang: We played ping-pong and went swimming together.', '阳阳：我们一起打乒乓球、游泳。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 21, 'Baobao: Cool!', '宝宝：酷！'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;
INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 22, 'Baobao: We all enjoyed our summer holiday.', '宝宝：我们都享受了暑假。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 1'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

DELETE sentence
FROM english_textbook_sentence AS sentence
JOIN english_textbook_lesson AS lesson ON lesson.id = sentence.lesson_id
WHERE lesson.unit_name = 'Unit 1'
  AND lesson.lesson_name = 'Lesson 1'
  AND sentence.sentence_order > 22;

-- Unit 1, Lesson 2. English text below was provided by the user.
INSERT INTO english_textbook_lesson
    (unit_name, lesson_name, title, title_cn, summary, unit_order, lesson_order)
VALUES
    ('Unit 1', 'Lesson 2', 'All of Us Had a Meaningful Summer Holiday', '我们都度过了一个有意义的暑假',
     '暑假活动对话：旅行、图书馆、博物馆、交通方式和有意义的假期。', 1, 2)
ON DUPLICATE KEY UPDATE
    title = VALUES(title), title_cn = VALUES(title_cn), summary = VALUES(summary),
    unit_order = VALUES(unit_order), lesson_order = VALUES(lesson_order), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 1, 'Guoguo: Hi, Lingling.', '果果：嗨，玲玲。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 2, 'Guoguo: Did you travel this summer holiday?', '果果：这个暑假你去旅行了吗？'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 3, 'Lingling: No, I didn’t.', '玲玲：不，我没有。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 4, 'Lingling: I stayed in Beijing.', '玲玲：我留在北京。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 5, 'Lingling: I went to the National Library of China on foot and read books there.', '玲玲：我步行去了中国国家图书馆，并在那里读书。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 6, 'Guoguo: That’s good.', '果果：那很好。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 7, 'Guoguo: Did you also stay in Beijing, Maomao?', '果果：毛毛，你也留在北京了吗？'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 8, 'Maomao: Yes, I did.', '毛毛：是的。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 9, 'Maomao: I worked as a helper at the China Science and Technology Museum.', '毛毛：我在中国科学技术馆当了一名帮手。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 10, 'Guoguo: Wonderful!', '果果：太棒了！'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 11, 'Guoguo: When did you work there?', '果果：你什么时候在那里工作的？'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 12, 'Maomao: From the 1st to the 10th of August.', '毛毛：从八月一日到十日。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 13, 'Lingling: Is the museum far from your home?', '玲玲：博物馆离你家远吗？'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 14, 'Lingling: How did you get there?', '玲玲：你怎么去那里的？'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 15, 'Maomao: Not too far.', '毛毛：不算太远。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 16, 'Maomao: I went there by bus.', '毛毛：我坐公交车去那里。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 17, 'Maomao: Where did you go, Guoguo?', '毛毛：果果，你去了哪里？'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 18, 'Guoguo: I went to Hubei to see my grandparents.', '果果：我去了湖北看望祖父母。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 19, 'Guoguo: I learned to take care of plants and animals.', '果果：我学会了照料植物和动物。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 20, 'Lingling: Hubei is far from here.', '玲玲：湖北离这里很远。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 21, 'Lingling: How did you get there?', '玲玲：你怎么去那里的？'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 22, 'Guoguo: I took a train.', '果果：我坐火车去的。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 23, 'Maomao: Wow!', '毛毛：哇！'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 24, 'Maomao: All of us had a meaningful summer holiday.', '毛毛：我们大家都度过了一个有意义的暑假。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 2'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

DELETE sentence
FROM english_textbook_sentence AS sentence
JOIN english_textbook_lesson AS lesson ON lesson.id = sentence.lesson_id
WHERE lesson.unit_name = 'Unit 1'
  AND lesson.lesson_name = 'Lesson 2'
  AND sentence.sentence_order > 24;

-- Unit 1, Lesson 3. English text below was provided by the user.
INSERT INTO english_textbook_lesson
    (unit_name, lesson_name, title, title_cn, summary, unit_order, lesson_order)
VALUES
    ('Unit 1', 'Lesson 3', 'My Summer Holiday', '我的暑假',
     '暑假生活叙述：探亲、照料动物、钓鱼和家庭故事。', 1, 3)
ON DUPLICATE KEY UPDATE
    title = VALUES(title), title_cn = VALUES(title_cn), summary = VALUES(summary),
    unit_order = VALUES(unit_order), lesson_order = VALUES(lesson_order), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 1, 'I had a wonderful summer holiday.', '我度过了一个美好的暑假。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 2, 'My little sister and I went to Hubei to see our grandparents.', '我和妹妹去了湖北看望祖父母。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 3, 'We took the train to get there.', '我们乘火车去那里。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 4, 'My two cousins visited them, too.', '我的两个表（堂）兄弟姐妹也去看望了他们。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 5, 'We stayed there for two weeks and had a lot of fun together.', '我们在那里住了两个星期，一起玩得很开心。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 6, 'In the early morning, we fed the chickens, cats and dogs.', '清晨，我们喂鸡、猫和狗。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 7, 'My sister and I enjoyed taking care of the baby chicks.', '妹妹和我喜欢照顾小鸡。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 8, 'After breakfast, we walked the two dogs.', '早餐后，我们带两只狗散步。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 9, 'We ran after them and played games together.', '我们追着它们跑，一起玩游戏。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 10, 'This was our favourite job.', '这是我们最喜欢的任务。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 11, 'In the afternoon, we usually stayed at home.', '下午，我们通常待在家里。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 12, 'Sometimes we went fishing with Grandpa.', '有时我们和爷爷一起钓鱼。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 13, 'We also watered the flowers and vegetables in the garden.', '我们还给花园里的花和蔬菜浇水。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 14, 'In the evening, we told stories together.', '晚上，我们一起讲故事。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 15, 'Grandpa and Grandma told us many interesting old stories.', '爷爷和奶奶给我们讲了许多有趣的老故事。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 16, 'We really enjoyed them.', '我们真的很喜欢这些故事。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 17, 'That was my wonderful summer holiday.', '那就是我美好的暑假。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 3'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

DELETE sentence
FROM english_textbook_sentence AS sentence
JOIN english_textbook_lesson AS lesson ON lesson.id = sentence.lesson_id
WHERE lesson.unit_name = 'Unit 1'
  AND lesson.lesson_name = 'Lesson 3'
  AND sentence.sentence_order > 17;

-- Unit 1, Lesson 4. English text transcribed from the user-provided textbook page.
INSERT INTO english_textbook_lesson
    (unit_name, lesson_name, title, title_cn, summary, unit_order, lesson_order)
VALUES
    ('Unit 1', 'Lesson 4', 'The Children''s Summer Stories', '孩子们的暑假故事',
     '暑假故事：北京夏令营活动，以及迈克在加拿大探亲和帮助中国学生的经历。', 1, 4)
ON DUPLICATE KEY UPDATE
    title = VALUES(title), title_cn = VALUES(title_cn), summary = VALUES(summary),
    unit_order = VALUES(unit_order), lesson_order = VALUES(lesson_order), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 1, 'Sara and her friends went to a summer camp in Beijing this August.', '今年八月，萨拉和她的朋友们去北京参加夏令营。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 4'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 2, 'The camp was not far away from home, so they went there by bus.', '夏令营离家不远，所以她们乘公共汽车去那里。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 4'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 3, 'They had a good time at the summer camp.', '她们在夏令营玩得很开心。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 4'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 4, 'In the daytime, they climbed mountains and did sports.', '白天，她们爬山并参加体育活动。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 4'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 5, 'In the evening, they sang, danced and told stories.', '晚上，她们唱歌、跳舞、讲故事。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 4'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 6, 'They enjoyed the time together, and found it hard to say goodbye.', '她们很享受在一起的时光，临别时很舍不得。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 4'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 7, 'Mike flew back to Canada to see his grandparents this summer.', '今年夏天，迈克飞回加拿大看望祖父母。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 4'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 8, 'He helped them with a lot of chores.', '他帮他们做了许多家务。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 4'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 9, 'He also helped some Chinese students travel and learn in Canada.', '他还帮助一些中国学生在加拿大旅行和学习。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 4'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 10, 'They walked around the University of Toronto and the University of Ottawa together.', '他们一起游览了多伦多大学和渥太华大学。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 4'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 11, 'They also visited the Canadian Museum of History and the Canada Science and Technology Museum.', '他们还参观了加拿大历史博物馆和加拿大科学技术博物馆。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 4'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT id, 12, 'Before the students left Canada, Mike and these new friends watched an ice hockey game together.', '在学生们离开加拿大前，迈克和这些新朋友一起看了一场冰球比赛。'
FROM english_textbook_lesson WHERE unit_name = 'Unit 1' AND lesson_name = 'Lesson 4'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

DELETE sentence
FROM english_textbook_sentence AS sentence
JOIN english_textbook_lesson AS lesson ON lesson.id = sentence.lesson_id
WHERE lesson.unit_name = 'Unit 1'
  AND lesson.lesson_name = 'Lesson 4'
  AND sentence.sentence_order > 12;

-- Unit 2, Lesson 5. English text transcribed from the user-provided textbook page.
INSERT INTO english_textbook_lesson
    (unit_name, lesson_name, title, title_cn, summary, unit_order, lesson_order)
VALUES
    ('Unit 2', 'Lesson 5', 'We Should Ride Bikes Safely', '我们应该安全骑自行车',
     '骑车安全对话：杨阳受伤的原因，以及骑自行车时应遵守的三条安全规则。', 2, 5)
ON DUPLICATE KEY UPDATE
    title = VALUES(title), title_cn = VALUES(title_cn), summary = VALUES(summary),
    unit_order = VALUES(unit_order), lesson_order = VALUES(lesson_order), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT lesson.id, source.sentence_order, source.english_text, source.chinese_text
FROM english_textbook_lesson AS lesson
JOIN (
    SELECT 1 AS sentence_order, 'Mike: Why didn''t Yangyang come to school today?' AS english_text, '迈克：杨阳今天为什么没来上学？' AS chinese_text
    UNION ALL SELECT 2, 'Baobao: He broke his right leg last weekend.', '宝宝：他上周末摔伤了右腿。'
    UNION ALL SELECT 3, 'Baobao: He is in hospital now.', '宝宝：他现在在医院。'
    UNION ALL SELECT 4, 'Mike: Oh, I''m sorry to hear that.', '迈克：哦，听到这个消息我很难过。'
    UNION ALL SELECT 5, 'Mike: How did that happen to him?', '迈克：他怎么会这样？'
    UNION ALL SELECT 6, 'Baobao: He rode a bike in the park.', '宝宝：他在公园骑自行车。'
    UNION ALL SELECT 7, 'Baobao: But he was too fast and fell off the bike.', '宝宝：但是他骑得太快，从自行车上摔了下来。'
    UNION ALL SELECT 8, 'Mike: That was too bad.', '迈克：那太糟糕了。'
    UNION ALL SELECT 9, 'Baobao: He can''t move his right leg now.', '宝宝：他现在不能动右腿。'
    UNION ALL SELECT 10, 'Baobao: But luckily, his head was not hurt because he wore a helmet.', '宝宝：不过幸运的是，因为他戴了头盔，头部没有受伤。'
    UNION ALL SELECT 11, 'Mike: Oh, we should ride bikes safely.', '迈克：哦，我们应该安全骑自行车。'
    UNION ALL SELECT 12, 'Baobao: You''re right.', '宝宝：你说得对。'
    UNION ALL SELECT 13, 'Baobao: We need to follow three safety rules when we ride bikes.', '宝宝：骑自行车时，我们需要遵守三条安全规则。'
    UNION ALL SELECT 14, 'Baobao: Number one, always wear a helmet.', '宝宝：第一，始终戴头盔。'
    UNION ALL SELECT 15, 'Baobao: Number two, stay on the right side of the road.', '宝宝：第二，靠道路右侧行驶。'
    UNION ALL SELECT 16, 'Baobao: Number three, ride slowly and carefully.', '宝宝：第三，骑得慢一些、仔细一些。'
    UNION ALL SELECT 17, 'Mike: Wow!', '迈克：哇！'
    UNION ALL SELECT 18, 'Mike: How do you know all the bike safety rules?', '迈克：你怎么知道所有这些骑车安全规则？'
    UNION ALL SELECT 19, 'Baobao: I read a book about how to stay safe and healthy.', '宝宝：我读了一本关于如何保持安全和健康的书。'
    UNION ALL SELECT 20, 'Mike: Oh, cool!', '迈克：哦，真酷！'
    UNION ALL SELECT 21, 'Mike: We should tell more friends about that.', '迈克：我们应该把这件事告诉更多朋友。'
) AS source ON 1 = 1
WHERE lesson.unit_name = 'Unit 2' AND lesson.lesson_name = 'Lesson 5'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

DELETE sentence
FROM english_textbook_sentence AS sentence
JOIN english_textbook_lesson AS lesson ON lesson.id = sentence.lesson_id
WHERE lesson.unit_name = 'Unit 2'
  AND lesson.lesson_name = 'Lesson 5'
  AND sentence.sentence_order > 21;

-- Unit 2, Lesson 6. English text transcribed from the user-provided textbook page.
INSERT INTO english_textbook_lesson
    (unit_name, lesson_name, title, title_cn, summary, unit_order, lesson_order)
VALUES
    ('Unit 2', 'Lesson 6', 'It''s Better to Eat Right and Play Smart', '合理饮食，聪明运动更健康',
     '看病对话：胃痛的饮食与运动原因，以及合理饮食、科学运动的健康建议。', 2, 6)
ON DUPLICATE KEY UPDATE
    title = VALUES(title), title_cn = VALUES(title_cn), summary = VALUES(summary),
    unit_order = VALUES(unit_order), lesson_order = VALUES(lesson_order), is_published = 1;

INSERT INTO english_textbook_sentence (lesson_id, sentence_order, english_text, chinese_text)
SELECT lesson.id, source.sentence_order, source.english_text, source.chinese_text
FROM english_textbook_lesson AS lesson
JOIN (
    SELECT 1 AS sentence_order, 'Doctor: Hello, Mike.' AS english_text, '医生：你好，迈克。' AS chinese_text
    UNION ALL SELECT 2, 'Doctor: How can I help you?', '医生：我能怎样帮助你？'
    UNION ALL SELECT 3, 'Mike: I have a stomachache.', '迈克：我肚子疼。'
    UNION ALL SELECT 4, 'Doctor: Could you show me where it hurts?', '医生：你能指给我看哪里疼吗？'
    UNION ALL SELECT 5, 'Mike: Right here.', '迈克：就是这里。'
    UNION ALL SELECT 6, 'Doctor: Does it hurt when I touch here?', '医生：我碰这里时疼吗？'
    UNION ALL SELECT 7, 'Mike: Yes, Doctor.', '迈克：是的，医生。'
    UNION ALL SELECT 8, 'Doctor: What did you have for lunch today?', '医生：你今天午饭吃了什么？'
    UNION ALL SELECT 9, 'Mike: I had a lot of rice, meat and fish.', '迈克：我吃了很多米饭、肉和鱼。'
    UNION ALL SELECT 10, 'Mike: Then I had a bowl of soup.', '迈克：然后我喝了一碗汤。'
    UNION ALL SELECT 11, 'Mike: After that, I ate a piece of cake, a banana and some grapes.', '迈克：之后，我吃了一块蛋糕、一个香蕉和一些葡萄。'
    UNION ALL SELECT 12, 'Doctor: I''m afraid you ate too much.', '医生：恐怕你吃得太多了。'
    UNION ALL SELECT 13, 'Mike: I felt fine after lunch.', '迈克：午饭后我感觉很好。'
    UNION ALL SELECT 14, 'Mike: And I played football with my friends before I had a stomachache.', '迈克：肚子疼之前，我还和朋友们踢了足球。'
    UNION ALL SELECT 15, 'Doctor: Hmm, it''s better to eat right and play smart.', '医生：嗯，合理饮食、聪明运动会更好。'
    UNION ALL SELECT 16, 'Doctor: I''ll give you some medicine to take.', '医生：我会给你一些药吃。'
    UNION ALL SELECT 17, 'Doctor: And I''ll give you some advice, too.', '医生：我也会给你一些建议。'
    UNION ALL SELECT 18, 'Doctor: You shouldn''t eat too much.', '医生：你不应该吃得太多。'
    UNION ALL SELECT 19, 'Doctor: Also, you shouldn''t do sports right after eating.', '医生：另外，你不应该刚吃完饭就运动。'
    UNION ALL SELECT 20, 'Doctor: Those are bad for your health.', '医生：那些对你的健康有害。'
) AS source ON 1 = 1
WHERE lesson.unit_name = 'Unit 2' AND lesson.lesson_name = 'Lesson 6'
ON DUPLICATE KEY UPDATE english_text = VALUES(english_text), chinese_text = VALUES(chinese_text), is_published = 1;

DELETE sentence
FROM english_textbook_sentence AS sentence
JOIN english_textbook_lesson AS lesson ON lesson.id = sentence.lesson_id
WHERE lesson.unit_name = 'Unit 2'
  AND lesson.lesson_name = 'Lesson 6'
  AND sentence.sentence_order > 20;

-- English textbook import verification
SELECT lesson.unit_name, lesson.lesson_name, lesson.title,
       COUNT(sentence.id) AS sentence_count
FROM english_textbook_lesson AS lesson
LEFT JOIN english_textbook_sentence AS sentence ON sentence.lesson_id = lesson.id
WHERE lesson.unit_name IN ('Unit 1', 'Unit 2')
GROUP BY lesson.id, lesson.unit_name, lesson.lesson_name, lesson.title
ORDER BY lesson.unit_order, lesson.lesson_order;
