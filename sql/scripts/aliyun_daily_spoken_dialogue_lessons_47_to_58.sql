-- Extracted from the next ten available PDFs in doc/, ordered by source file identifier.
-- Sources: Learn & Talk I, Chapter 6 Lessons 47-51 and Chapter 7 Lessons 54-58.
-- Source PDFs for Lessons 52 and 53 were unavailable during this import.
-- The target table is created by aliyun_daily_spoken_dialogue_buying_clothes.sql.
-- Re-running this file updates only the lesson_code/item_order pairs below.

SET NAMES utf8mb4;
START TRANSACTION;

-- Lesson 47 · In the Dorm (doc/114207_811_In the Dorm.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'roommate', 'roommate', '室友', '/ˈruːmmeɪt/', 'a person that you share a room with, especially at a college or university', 'It''s important to know the sleeping habits of your roommates.', 'roommate, dorm, university', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'berth', 'berth', '床位；铺位', '/bɜːrθ/', 'a place to sit or sleep, especially on a ship or vehicle', 'The lower berth has been occupied.', 'berth, dorm, bunk bed', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'dorm', 'dorm', '宿舍', '/dɔːrm/', 'short for dormitory; a room for several people to sleep in, especially in a school or other institution', 'Most dorms in China have four people in one room.', 'dorm, dormitory, university', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'by the way', 'by the way', '顺带一提', NULL, 'used to introduce a comment or question that is not directly related to what you have been talking about', 'Oh, by the way, if you see Jack, tell him I''ll call him this evening.', 'by the way, conversation, dorm', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'work out', 'work out', '（顺利）发展；进行', '/wɜːrk aʊt/', 'to develop in a successful way', 'Things have worked out quite well for us.', 'work out, dorm, roommates', 1),

    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'Hi. My name is Jack. Looks like we''re going to be roommates.', '你好。我叫 Jack。看来我们要成为室友了。', NULL, NULL, NULL, 'roommates, dorm', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Alfred', NULL, 'I''m Alfred. Nice to meet you.', '我是 Alfred。很高兴认识你。', NULL, NULL, NULL, 'nice to meet you, roommate', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'Hey, if you don''t mind, I want to take this berth of the dorm.', '嗨，如果你不介意，我想要宿舍里的这个床位。', NULL, NULL, NULL, 'if you do not mind, berth', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Alfred', NULL, 'No problem. They look the same to me.', '没问题。对我来说它们看起来都一样。', NULL, NULL, NULL, 'no problem, dorm', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'By the way, are you a morning person or a night person?', '顺便问一下，你是早起型还是夜猫子型的人？', NULL, NULL, NULL, 'morning person, night person', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Alfred', NULL, 'Night person. I like to sleep in the morning.', '夜猫子型。我喜欢早上睡觉。', NULL, NULL, NULL, 'night person, sleep', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'That''s great! So am I. That should work out well then.', '太好了！我也是。那我们应该能相处得很顺利。', NULL, NULL, NULL, 'work out, roommates', 1),

    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Hello! You must be my new roommate. Glad to meet you!', '你好！你一定是我的新室友。很高兴认识你！', NULL, '根据课件提示补全。', NULL, 'roommate, dorm', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Glad to meet you, too.', '我也很高兴认识你。', NULL, NULL, NULL, 'nice to meet you, roommate', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'How long have you been in the dorm?', '你来宿舍多久了？', NULL, NULL, NULL, 'dorm, university', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'I got here about an hour ago. Oh, if you don''t mind, I''ve taken the lower berth there.', '我大约一小时前到的。哦，如果你不介意，我选了那边的下铺。', NULL, NULL, NULL, 'lower berth, dorm', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'It''s fine! They are the same to me. I''ll take the upper one.', '没关系！对我来说它们都一样。我选上铺。', NULL, NULL, NULL, 'upper berth, dorm', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Cool. By the way, where are you from? I''m from Beijing.', '太好了。顺便问一下，你来自哪里？我来自北京。', NULL, NULL, NULL, 'by the way, hometown', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'I''m from Shanghai.', '我来自上海。', NULL, NULL, NULL, 'hometown, dorm', 1),

    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you ever lived in a dorm? Do you like it or not? Why?', '你曾住过宿舍吗？你喜欢吗？为什么？', NULL, '可以谈中学、高中或大学宿舍。喜欢：价格可负担、舒适；不喜欢：空间小、没有隐私、没有电梯等。', NULL, 'dorm, university, roommates', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you think it''s difficult to get along with roommates in a dorm? Why or why not?', '你认为在宿舍和室友相处困难吗？为什么？', NULL, '可以谈不同生活习惯和作息、彼此需要分享物品，以及要保持宿舍干净整洁。', NULL, 'roommates, dorm, get along', 1),

    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'If you don''t mind, I want to take this berth of the dorm.\nAre you a morning person or a night person?', '复习：roommate / berth / dorm / by the way / work out。', NULL, NULL, NULL, 'review, dorm', 1),

    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Dorm life: moving out', 'Best: You finally get to move out and have your own place, even if you have to share with a roommate.', '优点：你终于能搬出去拥有自己的空间，即使还得和室友合住。', NULL, '课后拓展：宿舍生活的优缺点。', NULL, 'dorm life, roommate', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Dorm life: fifth floor', 'Worst: Realizing you live on the fifth floor and having to carry heavy loads up the stairs.', '缺点：发现住在五楼，还得把重物搬上楼。', NULL, '课后拓展：宿舍生活的优缺点。', NULL, 'dorm life, stairs', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Dorm life: friends nearby', 'Best: There are lots of people to hang out with anytime.', '优点：随时都有很多人可以一起玩。', NULL, '课后拓展：宿舍生活的优缺点。', NULL, 'dorm life, friends', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Dorm life: loud music', 'Worst: When the guy living next door plays music loud and keeps you up late at night.', '缺点：隔壁的人大声放音乐，让你晚上很晚都睡不着。', NULL, '课后拓展：宿舍生活的优缺点。', NULL, 'dorm life, noise', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'Dorm life: room to yourself', 'Best: When your roommate is never around and you enjoy the whole room.', '优点：室友从不在，你能独享整个房间。', NULL, '课后拓展：宿舍生活的优缺点。', NULL, 'dorm life, roommate', 1),
    ('in-the-dorm', 'Chapter 6 · Education', 'Lesson 47 · In the Dorm', 47, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'Dorm life: television', 'Worst: When your roommate is in the dorm all the time and watches television without headphones on.', '缺点：室友总在宿舍里，而且看电视不戴耳机。', NULL, '课后拓展：宿舍生活的优缺点。', NULL, 'dorm life, roommate, noise', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 48 · Taking an Exam (doc/114213_811_Taking an Exam.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'tough', 'tough', '难熬的；困难的', '/tʌf/', 'having or causing problems or difficulties', 'She''s been having a tough time lately.', 'tough, exam, finals', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'paper', 'paper', '论文（美式英语）', '/ˈpeɪpər/', 'a long piece of written work that a student does on a subject', 'Your grade will be based on four papers and a final exam.', 'paper, exam, university', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'due', 'due', '到期的；应上交的', '/duː/', 'scheduled, arranged, or expected', 'The train is due in five minutes.', 'due, deadline, paper', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'percentage', 'percentage', '百分比', '/pərˈsentɪdʒ/', 'a number, amount, or rate expressed as part of a total of 100', 'What percentage of the population is overweight?', 'percentage, grade, exam', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'pull an all-nighter', 'pull an all-nighter', '熬夜一整晚；开夜车（学习）', NULL, 'to stay awake all night studying', 'The final essay is very time-consuming. I had to pull an all-nighter just to finish.', 'all-nighter, finals, study', 1),

    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'I finished my last final exam this morning! How about you?', '我今天早上完成了最后一门期末考试！你呢？', NULL, NULL, NULL, 'final exam, finals', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Tom', NULL, 'Ah, I still have three more to go. I''ve pulled an all-nighter.', '啊，我还有三门要考。我熬了一整夜。', NULL, NULL, NULL, 'all-nighter, finals', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'Yeah, you look tired. Looks like it''s a tough week for you.', '是啊，你看起来很累。看来这周对你很难熬。', NULL, NULL, NULL, 'tough week, finals', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Tom', NULL, 'And I have a paper that is due next Friday. I haven''t started it yet.', '而且我还有一篇下周五截止的论文，还没开始写。', NULL, NULL, NULL, 'paper, due date', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'How much percentage is it towards the final grade?', '它占期末总成绩的百分之多少？', NULL, NULL, NULL, 'percentage, final grade', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Tom', NULL, 'The professor said it was twenty percent of our final grade.', '教授说它占我们期末总成绩的 20%。', NULL, NULL, NULL, 'twenty percent, final grade', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'You know, if you need help with your paper, I can help you this weekend.', '如果你写论文需要帮助，我这个周末可以帮你。', NULL, NULL, NULL, 'help with paper, study', 1),

    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Aww, I hate finals week. I pulled an all-nighter just to finish all these essays and so on.', '唉，我讨厌期末考试周。我熬了一整夜才完成这些论文之类的作业。', NULL, '根据课件提示补全。', NULL, 'finals week, all-nighter', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I agree. It''s really a tough time. So are you completely done with them?', '我同意。这真是段难熬的时间。那你全都完成了吗？', NULL, NULL, NULL, 'tough, finals week', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Nope. I still have one to go, and it''s due tomorrow.', '没有。我还有一项没完成，明天截止。', NULL, NULL, NULL, 'due, finals', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'How many pages do you have to write?', '你需要写多少页？', NULL, NULL, NULL, 'paper, university', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'It''s a 10-page paper on habitual behavior for Psychology 211.', '这是 Psychology 211 课程一篇关于习惯行为的 10 页论文。', NULL, NULL, NULL, '10-page paper, Psychology', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'I guess you need to pull another all-nighter for that.', '我猜你得再熬一个通宵来完成它。', NULL, NULL, NULL, 'all-nighter, paper', 1),

    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'How do you prepare for a final exam? Is finals week tough for you?', '你如何准备期末考试？期末考试周对你来说难熬吗？', NULL, '可以复习所有材料、练习旧试卷、待在图书馆／宿舍／教室学习，也可以谈熬夜。', NULL, 'final exam, finals week, study', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Which do you prefer, taking an exam or writing a paper? Why?', '考试和写论文你更喜欢哪一个？为什么？', NULL, '可以谈写论文耗时，但压力较小，可向朋友、书籍和网络求助；考试则更多依靠自己独立完成。', NULL, 'exam, paper, university', 1),

    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Looks like it''s a tough week for you.\nHow much percentage is it towards the final grade?', '复习：tough / paper / due / percentage / pull an all-nighter。', NULL, NULL, NULL, 'review, exam', 1),

    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'mid-term', 'mid-term', '期中考试', NULL, '课后拓展：考试术语。', NULL, 'mid-term, exam', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'finals week', 'finals week', '期末考试周', NULL, '课后拓展：考试术语。', NULL, 'finals week, exam', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'quiz', 'quiz', '随堂小测', NULL, '课后拓展：考试术语。', NULL, 'quiz, exam', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'pop-quiz', 'pop-quiz', '突击随堂小测', NULL, '课后拓展：考试术语。', NULL, 'pop-quiz, exam', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'take-home exam', 'take-home exam', '可以把试卷带回家做的考试', NULL, '课后拓展：考试术语。', NULL, 'take-home exam, exam', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'research paper', 'research paper', '学术论文', NULL, '课后拓展：考试术语。', NULL, 'research paper, university', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'extra', '拓展学习', 6, 'extra', 507, NULL, 'final paper', 'final paper', '期末论文', NULL, '课后拓展：考试术语。', NULL, 'final paper, university', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'extra', '拓展学习', 6, 'extra', 508, NULL, 'report', 'report', '报告', NULL, '课后拓展：考试术语。', NULL, 'report, university', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'extra', '拓展学习', 6, 'extra', 509, NULL, 'essay', 'essay', '短篇论文', NULL, '课后拓展：考试术语。', NULL, 'essay, university', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'extra', '拓展学习', 6, 'extra', 510, NULL, 'presentation', 'presentation', '演讲；展示', NULL, '课后拓展：考试术语。', NULL, 'presentation, university', 1),
    ('taking-an-exam', 'Chapter 6 · Education', 'Lesson 48 · Taking an Exam', 48, 'extra', '拓展学习', 6, 'extra', 511, NULL, 'open-book exam', 'open-book exam', '开卷考试', NULL, '课后拓展：考试术语。', NULL, 'open-book exam, university', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 49 · University Classes (doc/114239_811_University Classes.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'available', 'available', '可选的；可用的', '/əˈveɪləbl/', 'that you can get, buy, or find', 'This was the only room available.', 'available, classes, registration', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'register for', 'register for', '注册；选（课）', '/ˈredʒɪstər/', 'to record your name on an official list', 'What classes are you registering for?', 'register, classes, university', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'instructor', 'instructor', '讲师；教员；授课教职员', '/ɪnˈstrʌktər/', 'a teacher below the rank of assistant professor at a college or university', 'The English instructor was very patient.', 'instructor, classes, university', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'fail', 'fail', '挂（科）；未通过考试', '/feɪl/', 'to not pass a test or an exam', 'He failed his English Literature exam.', 'fail, exam, university', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'easy grader', 'easy grader', '给分高的老师；“水课”老师', '/ˈiːzi ˈɡreɪdər/', 'a teacher or professor who gives high grades to students', 'Professor Aaron is an easy grader. He is known as the angel of giving “A”s.', 'easy grader, classes, university', 1),

    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'dialogue', '示范对话', 2, 'dialogue', 101, 'May', NULL, 'Hey John, what classes do you plan on taking?', '嗨，John，你计划选什么课？', NULL, NULL, NULL, 'classes, registration', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'dialogue', '示范对话', 2, 'dialogue', 102, 'John', NULL, 'I want to take Interpersonal Communication, but I don''t know if it will be available. Last semester it was full by the time I registered.', '我想选人际沟通课，但不知道是否还有名额。上学期我注册时它已经满了。', NULL, NULL, NULL, 'available, register, classes', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'dialogue', '示范对话', 2, 'dialogue', 103, 'May', NULL, 'Wow, is that class really that popular? Who is the instructor?', '哇，这门课真的这么热门吗？授课老师是谁？', NULL, NULL, NULL, 'popular class, instructor', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'dialogue', '示范对话', 2, 'dialogue', 104, 'John', NULL, 'Professor Michaels. He''s an easy grader and is quite fair.', '是 Michaels 教授。他给分高，而且很公平。', NULL, NULL, NULL, 'easy grader, professor', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'dialogue', '示范对话', 2, 'dialogue', 105, 'May', NULL, 'That sounds great. You know what? I failed my biology course last semester, and my GPA is terrible now. I guess I should also take an easy class.', '听起来不错。你知道吗？我上学期生物课挂了，现在 GPA 很糟。我想我也该选一门容易的课。', NULL, NULL, NULL, 'failed course, GPA, easy class', 1),

    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Have you registered for classes yet?', '你已经选课了吗？', NULL, '根据课件提示补全。', NULL, 'register, classes', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Nope; I will register next Monday. How about you? What classes are you going to take?', '还没有；我下周一选课。你呢？你准备选什么课？', NULL, NULL, NULL, 'register, university classes', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I plan on taking English and chemistry, but I''ll have to see if they are available or not.', '我计划选英语和化学，但得看看是否还有名额。', NULL, NULL, NULL, 'available, classes', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'I want to take chemistry, too. But I don''t know who the instructor is.', '我也想选化学，但我不知道授课老师是谁。', NULL, NULL, NULL, 'instructor, chemistry', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'It''s Professor Li. He''s not an easy grader, but he''s definitely fair.', '是 Li 教授。他给分不高，但肯定很公平。', NULL, NULL, NULL, 'easy grader, professor', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Well, I have to study hard then. I don''t want to fail any exam.', '那我得努力学习了。我不想挂任何一门考试。', NULL, NULL, NULL, 'fail, exam, study', 1),

    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'How do you, or did you, register for classes at school or university? If you registered for classes before, did you always get the classes you wanted?', '你在学校或大学如何选课？如果你之前选过课，总能选到想要的吗？', NULL, '可以谈网上选课或到选课办公室办理；课可能有名额、无名额或已满，也可讨论糟糕的选课系统。', NULL, 'register, classes, university', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'What courses do you have, or did you have, at university? Do you like them? Why or why not?', '你在大学上哪些课？你喜欢它们吗？为什么？', NULL, '可谈是否有许多小测和展示、从授课老师学到很多还是没有学到，以及老师给分容易或困难。', NULL, 'courses, university, instructor', 1),

    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'What classes do you plan on taking?\nHe''s an easy grader and is quite fair.', '复习：available / register / instructor / fail / easy grader。', NULL, NULL, NULL, 'review, university classes', 1),

    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'major in', 'major in ...', '主修……', NULL, '课后拓展：大学课程术语。', NULL, 'major, university', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'minor in', 'minor in ...', '辅修……', NULL, '课后拓展：大学课程术语。', NULL, 'minor, university', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'mandatory course', 'mandatory course', '必修课', NULL, '课后拓展：大学课程术语。', NULL, 'mandatory course, university', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'elective course', 'optional / elective course', '选修课', NULL, '课后拓展：大学课程术语。', NULL, 'elective course, university', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'credit', 'credit', '学分', NULL, '课后拓展：大学课程术语。', NULL, 'credit, university', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'GPA', 'GPA (Grade Point Average)', '绩点', NULL, '课后拓展：大学课程术语。', NULL, 'GPA, grade point average, university', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'extra', '拓展学习', 6, 'extra', 507, NULL, 'enroll in', 'enroll in ...', '选……课', NULL, '课后拓展：大学课程术语。', NULL, 'enroll, classes, university', 1),
    ('university-classes', 'Chapter 6 · Education', 'Lesson 49 · University Classes', 49, 'extra', '拓展学习', 6, 'extra', 508, NULL, 'drop the course', 'drop the course', '取消选课；退课', NULL, '课后拓展：大学课程术语。', NULL, 'drop course, university', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 50 · Studying Abroad (doc/114449_811_Studying Abroad.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'abroad', 'abroad', '在国外；到国外', '/əˈbrɔːd/', 'in or to a foreign country', 'He lived abroad for many years.', 'abroad, study, education', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'upcoming', 'upcoming', '即将到来的', '/ˈʌpkʌmɪŋ/', 'going to happen soon', 'We were all enthusiastic about the upcoming holidays.', 'upcoming, study abroad', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'sort of', 'sort of', '有一点；稍微', '/sɔːrt əv/', 'to some extent but in a way that you cannot easily describe', '“Do you understand?” “Sort of.”', 'sort of, study abroad', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'terribly', 'terribly', '非常；极度', '/ˈterəbli/', 'very much; very badly', 'The meeting was terribly boring.', 'terribly, study abroad', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'make up one''s mind', 'make up one''s mind', '下定决心', NULL, 'to decide something', 'They''re both beautiful — I can''t make up my mind.', 'make up one''s mind, study abroad', 1),

    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jill', NULL, 'Do you plan to study abroad, Larry?', 'Larry，你计划出国留学吗？', NULL, NULL, NULL, 'study abroad, education', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Larry', NULL, 'Yes. Actually, this upcoming summer I''ll be going to Australia.', '是的。事实上，即将到来的这个夏天我会去澳大利亚。', NULL, NULL, NULL, 'upcoming summer, Australia', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jill', NULL, 'Wow, that''s cool! So how do you feel about it? Are you nervous?', '哇，真酷！你对此感觉怎样？紧张吗？', NULL, NULL, NULL, 'nervous, study abroad', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Larry', NULL, 'I''m really excited because it''ll be my first time on a plane! And it''s going to be my first time going out of the country as well. I''m nervous and excited at the same time.', '我非常兴奋，因为这是我第一次坐飞机！这也是我第一次出国。我既紧张又兴奋。', NULL, NULL, NULL, 'first time, nervous, excited', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jill', NULL, 'How did you make up your mind? Was it difficult for you?', '你是如何下定决心的？对你来说困难吗？', NULL, NULL, NULL, 'make up your mind, study abroad', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Larry', NULL, 'Well, sort of. My mom was terribly worried about me!', '嗯，有一点。我妈妈非常担心我！', NULL, NULL, NULL, 'sort of, terribly worried', 1),

    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Finally you are back home! So, how was it? Did you enjoy studying abroad?', '你终于回家了！怎么样？你喜欢出国留学吗？', NULL, '根据课件提示补全。', NULL, 'studying abroad, education', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Definitely. I''ve made so many friends, and I love the climate there.', '当然。我交了很多朋友，也喜欢那里的气候。', NULL, NULL, NULL, 'friends, climate, abroad', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Oh, I hope I could go abroad, too. But I don''t think my parents would agree. They would miss me terribly if I left them for a long period of time.', '哦，我也希望能出国。但我觉得父母不会同意。如果我长时间离开他们，他们会非常想我。', NULL, NULL, NULL, 'go abroad, terribly, parents', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Studying abroad can be expensive if you don''t get a scholarship. Have you made up your mind where to go?', '如果得不到奖学金，出国留学会很贵。你决定去哪里了吗？', NULL, NULL, NULL, 'scholarship, make up your mind', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Well, sort of. I want to go to the UK so that I can improve my English, but I''m also considering Japan — I love Japanese culture very much.', '嗯，有一点决定了。我想去英国提高英语，但也在考虑日本——我非常喜欢日本文化。', NULL, NULL, NULL, 'sort of, UK, Japan, culture', 1),

    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you ever considered studying abroad? If yes, where do you consider going and why? If no, why not?', '你考虑过出国留学吗？如果考虑过，想去哪里，为什么？如果没有，为什么？', NULL, '可谈英国、美国、加拿大、澳大利亚、新西兰、日本、德国、法国或荷兰，以及当地食物、气候、语言、专业和学费。也可谈费用高、浪费时间或没有必要等原因。', NULL, 'study abroad, countries, education', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'What do you think are the pros and cons of studying abroad? Try to name as many as you can.', '你认为出国留学有什么优缺点？尽量多说一些。', NULL, '优点：新朋友、文化和语言，变得独立、旅行，以全新视角理解生活。缺点：孤独、想家、学费和生活成本高、语言问题、课程落后和可能的歧视。', NULL, 'study abroad, pros and cons', 1),

    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'This upcoming summer I''ll be going to Australia.\nIt''s going to be my first time going out of the country.', '复习：abroad / upcoming / sort of / terribly / make up one''s mind。', NULL, NULL, NULL, 'review, studying abroad', 1),

    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Experience a new culture', 'Experience a new culture.', '体验异国文化。', NULL, '课后拓展：留学的益处。', NULL, 'study abroad, culture', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Make friends worldwide', 'Make friends from around the world.', '广交世界友人。', NULL, '课后拓展：留学的益处。', NULL, 'study abroad, friends', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Become independent', 'Become truly independent.', '独立自主。', NULL, '课后拓展：留学的益处。', NULL, 'study abroad, independence', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Change your thinking', 'Change the way you think.', '改变思考方式。', NULL, '课后拓展：留学的益处。', NULL, 'study abroad, perspective', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'International workplace', 'Get ready for an international workplace.', '准备迎接国际化职场环境。', NULL, '课后拓展：留学的益处。', NULL, 'study abroad, workplace', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'Develop language skills', 'Develop your language skills.', '强化语言技能。', NULL, '课后拓展：留学的益处。', NULL, 'study abroad, language', 1),
    ('studying-abroad', 'Chapter 6 · Education', 'Lesson 50 · Studying Abroad', 50, 'extra', '拓展学习', 6, 'extra', 507, NULL, 'Travel more widely', 'Travel more widely.', '旅行各地。', NULL, '课后拓展：留学的益处。', NULL, 'study abroad, travel', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 51 · Studying Online (doc/114450_811_Studying Online.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'face-to-face', 'face-to-face', '面对面的；面对面地', '/ˌfeɪs tə ˈfeɪs/', 'involving people who are close together and looking at each other', 'Let''s talk about it face-to-face.', 'face-to-face, online learning', 1),
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'to be frank', 'to be frank', '坦白说……', '/fræŋk/', 'used to introduce your honest opinion, especially when the person you are talking to might not like it', 'To be frank with you, Harvey, I may have made a mistake.', 'to be frank, honestly, online learning', 1),
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'people person', 'people person', '喜欢和人打交道的人', '/ˈpiːpl pɜːrsn/', 'a person who enjoys, and is good at, being with and talking to other people', 'Gary is such a people person; he can get along with almost anybody.', 'people person, online learning', 1),
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'affordable', 'affordable', '便宜的；负担得起的', '/əˈfɔːrdəbl/', 'cheap enough that people can afford to buy or pay for it', 'The company makes wearable, beautiful clothes at affordable prices.', 'affordable, online learning', 1),
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'make sense', 'make sense', '说得通；有道理', '/meɪk sens/', 'if something makes sense, you can understand it or it seems sensible to you', 'They all said, “This is crazy, this makes no sense.”', 'make sense, online learning', 1),

    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Luna', NULL, 'Hey Mike, I heard that you are taking a French course online. How''s it going?', '嗨，Mike。我听说你在网上上法语课，怎么样？', NULL, NULL, NULL, 'French course, online learning', 1),
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mike', NULL, 'Quite well. I''ve had about five sessions, and it does help.', '相当不错。我已经上了大约五节课，确实有帮助。', NULL, NULL, NULL, 'sessions, online course', 1),
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Luna', NULL, 'But why do you choose to learn a language online? I mean, isn''t it better to talk with others face-to-face if you want to improve language skills?', '但你为什么选择在线学语言？我是说，如果想提高语言技能，和别人面对面交流不是更好吗？', NULL, NULL, NULL, 'face-to-face, language skills', 1),
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mike', NULL, 'To be frank, I''m not a people person, so I''d prefer staying at home and communicating online. What''s more, this online course is much more affordable for me. It can also save me a lot of time on transportation.', '坦白说，我不太擅长和人打交道，所以更愿意待在家里在线交流。而且这门在线课程对我来说更实惠，也能省很多交通时间。', NULL, NULL, NULL, 'to be frank, affordable, online', 1),
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Luna', NULL, 'Oh, I see. That makes sense. I guess it saves you the travel costs, too.', '哦，我明白了。这很有道理。我想它也为你节省了出行费用。', NULL, NULL, NULL, 'makes sense, travel costs', 1),

    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Have you ever tried learning something online?', '你尝试过在线学习吗？', NULL, '根据课件提示补全。', NULL, 'online learning, education', 1),
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes, I took an online writing course last year. Why do you ask?', '是的，我去年上过在线写作课。你为什么问？', NULL, NULL, NULL, 'online writing course, education', 1),
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I want to take a speaking course, but I''m not sure if it works. You know, face-to-face communication is important in speaking. Why did you choose to study online?', '我想上口语课，但不确定是否有效。你知道，面对面交流对口语很重要。你为什么选择在线学习？', NULL, NULL, NULL, 'face-to-face, speaking course', 1),
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Well, to be frank, I chose that online course simply because it is more affordable. I didn''t have much money since I was looking for a job.', '嗯，坦白说，我选那门在线课只是因为它更实惠。当时我在找工作，钱不多。', NULL, NULL, NULL, 'to be frank, affordable', 1),
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Oh yes, it makes sense. I guess I should also give it a try.', '哦，是的，这很有道理。我想我也应该试一试。', NULL, NULL, NULL, 'makes sense, online course', 1),

    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Why did you choose to study online? What do you think are the pros and cons of studying online?', '你为什么选择在线学习？你认为在线学习有什么优缺点？', NULL, '优点：实惠、灵活、节省时间和交通费。缺点：没有和同学交流、技术问题，以及必须独立安排时间。', NULL, 'online learning, pros and cons', 1),
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you think very young kids, aged 3 to 5, should study online? Why or why not?', '你认为 3 到 5 岁的幼儿应该在线学习吗？为什么？', NULL, '支持：能快速学新东西，早期学会用电脑。反对：伤眼睛、缺少与其他孩子交流，需要更多户外和身体活动。', NULL, 'young kids, online learning, education', 1),

    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'To be frank, I''m not a people person.\nThis online course is much more affordable for me.', '复习：face-to-face / to be frank / people person / affordable / make sense。', NULL, NULL, NULL, 'review, studying online', 1),

    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Flexibility', 'Whether you have a full-time job or a family to take care of, boosting your career by studying will still be possible for you.', '无论你有全职工作还是要照顾家庭，仍然可以通过学习提升职业发展。', NULL, '课后拓展：为什么要在线学习。', NULL, 'flexibility, online learning, career', 1),
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Saving money', 'Online courses are a more affordable option than traditional classroom learning.', '在线课程比传统课堂学习更实惠。', NULL, '课后拓展：为什么要在线学习。', NULL, 'saving money, online learning', 1),
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Variety of courses', 'No matter what you wish to study, you can find online the courses or programs you need.', '无论你想学什么，都可以在线找到所需课程或项目。', NULL, '课后拓展：为什么要在线学习。', NULL, 'courses, online learning', 1),
    ('studying-online', 'Chapter 6 · Education', 'Lesson 51 · Studying Online', 51, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Support', 'Most online courses are designed so that you can engage with tutors and have access to support staff and other learners.', '大多数在线课程都让你能够与导师互动，并获得支持人员和其他学习者的帮助。', NULL, '课后拓展：为什么要在线学习。', NULL, 'support, tutors, online learning', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 54 · Job Hunting (doc/114480_812_Job Hunting.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'hunt for', 'hunt for', '搜索；寻找', '/hʌnt/', 'to look for something that is difficult to find', 'She is still hunting for a new job.', 'hunt for, search for, job', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'resume', 'resume', '简历', '/ˈrez.ə.meɪ/', 'also résumé; a written record of your education and jobs that you send when applying for a job', 'Do you have a resume with you?', 'resume, job hunting, CV', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'follow up', 'follow up', '跟进', '/ˈfɑːloʊ ʌp/', 'to add to something you have just done by doing something else', 'You should follow up your phone call with an email or a letter.', 'follow up, job interview, email', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'initiative', 'initiative', '主动性；进取心', '/ɪˈnɪʃətɪv/', 'the ability to decide and act on your own without waiting for somebody to tell you what to do', 'You won''t get much help. You''ll have to use your initiative.', 'initiative, job hunting, work', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'on a roll', 'on a roll', '好运连连；进展顺利', '/roʊl/', 'informal: experiencing a period of success at what you are doing', 'I''m on a roll this semester — I''ve gotten A''s in all my classes!', 'on a roll, job hunting, success', 1),

    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Vera', NULL, 'So, how''s the job hunting going?', '那么，找工作进展如何？', NULL, NULL, NULL, 'job hunting, work', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Ben', NULL, 'I''ve sent out about 30 resumes and gone to 4 interviews so far this month.', '这个月到目前为止，我已经投了大约 30 份简历，参加了 4 场面试。', NULL, NULL, NULL, 'resumes, interviews, job hunting', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Vera', NULL, 'Wow, you''re on a roll! Any news about that sales job for the finance company? It seemed like the perfect position for you.', '哇，你进展很顺利！那家金融公司的销售工作有消息了吗？它看起来很适合你。', NULL, NULL, NULL, 'on a roll, sales job, position', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Ben', NULL, 'Not yet. They said they''d get back to me by last week, but I haven''t heard from them.', '还没有。他们说上周会回复我，但我没有收到消息。', NULL, NULL, NULL, 'get back to, job hunting', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Vera', NULL, 'Ah, okay. Well, make sure you follow up with all the places where you''ve interviewed — it shows initiative.', '啊，好吧。一定要跟进你面试过的所有公司——这能体现主动性。', NULL, NULL, NULL, 'follow up, initiative, interview', 1),

    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Are you still hunting for a job?', '你还在找工作吗？', NULL, '根据课件提示补全。', NULL, 'hunt for, job', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yeah, I sent out 10 resumes and went to three interviews last week.', '是的，我上周投了 10 份简历，参加了三场面试。', NULL, NULL, NULL, 'resumes, interviews, job', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Seems like you''re quite busy. Have you got any offer yet? What about the sales job you mentioned several days ago? I thought it was perfect for you.', '看来你很忙。你收到工作邀约了吗？几天前提到的销售工作怎么样？我以为它很适合你。', NULL, NULL, NULL, 'job offer, sales job', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Hmm, they said they''d get back to me by the end of this week. I''m going to send them an email to follow up.', '嗯，他们说本周末前会回复我。我准备发邮件跟进。', NULL, NULL, NULL, 'follow up, email, job', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Good idea. That shows your initiative.', '好主意。这体现了你的主动性。', NULL, NULL, NULL, 'initiative, job hunting', 1),

    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'In China, what do people do when they hunt for a job? What are the typical steps they take?', '在中国，人们找工作时会做什么？典型步骤有哪些？', NULL, '可以写简历、取得推荐信、在网络或报纸寻找职位、投递简历和参加面试。', NULL, 'job hunting, resume, interview', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you think it''s difficult nowadays for young people to hunt for a job in China? Why or why not?', '你认为如今中国年轻人找工作困难吗？为什么？', NULL, '困难：竞争更大、大学毕业生更多、岗位更少、生活成本上涨。不困难：大城市机会更多、小型和初创公司更多，且可通过互联网求职。', NULL, 'job hunting, young people, work', 1),

    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'It seemed like the perfect position for you.\nThey said they''d get back to me by last week.', '复习：hunt / resume / on a roll / follow up with / initiative。', NULL, NULL, NULL, 'review, job hunting', 1),

    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'annual hiring cycle', 'annual hiring cycle', '每年的招聘季', NULL, '课后拓展：求职词汇。', NULL, 'hiring cycle, job hunting', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'graduation season', 'graduation season', '毕业季', NULL, '课后拓展：求职词汇。', NULL, 'graduation, job hunting', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'career fair', 'career fair', '招聘会', NULL, '课后拓展：求职词汇。', NULL, 'career fair, job hunting', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'curriculum vitae', 'curriculum vitae / CV', '履历', NULL, '课后拓展：求职词汇。', NULL, 'CV, curriculum vitae, job hunting', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'cover letter', 'cover letter', '求职信', NULL, '课后拓展：求职词汇。', NULL, 'cover letter, job hunting', 1),
    ('job-hunting', 'Chapter 7 · Work', 'Lesson 54 · Job Hunting', 54, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'CV versus resume', 'The word CV comes from Latin. A CV is usually more detailed and longer than a resume.', 'CV 一词来自拉丁语；CV 通常比 resume 更详细、更长。', NULL, '课后拓展：求职词汇。', NULL, 'CV, resume, job hunting', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 55 · Job Interview (doc/114557_812_Job Interview.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'employer', 'employer', '雇主；公司', '/ɪmˈplɔɪər/', 'a person or company that pays people to work for them', 'They''re one of the largest employers in the area.', 'employer, job interview, work', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'tend to', 'tend to do something', '倾向于；往往会（做某事）', '/tend tuː/', 'to be likely to do something because this is what usually happens; have a tendency to', 'When I''m tired, I tend to make mistakes.', 'tend to, job interview, habits', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'strength', 'strength', '强项；长处', '/streŋθ/', 'a quality or ability that a person or thing has that gives them an advantage', 'The ability to keep calm is one of her many strengths.', 'strength, job interview, work', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'weakness', 'weakness', '弱点', '/ˈwiːknəs/', 'a weak point in a system or somebody''s character', 'It''s important to know your own strengths and weaknesses.', 'weakness, job interview, work', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'have trouble', 'have trouble doing something', '（做某事）有困难；有麻烦', '/hæv ˈtrʌbl/', 'another way to say “it''s hard to do something” or “have difficulty doing something”', 'I have trouble sleeping at night.', 'have trouble, job interview', 1),

    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Lara', NULL, 'Good morning. I am here for my interview.', '早上好。我是来面试的。', NULL, NULL, NULL, 'job interview, work', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'dialogue', '示范对话', 2, 'dialogue', 102, 'John', NULL, 'Have a seat. Did you have any trouble finding the place?', '请坐。你找这里有困难吗？', NULL, NULL, NULL, 'have trouble, interview', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Lara', NULL, 'No problem.', '没有问题。', NULL, NULL, NULL, 'no problem, interview', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'dialogue', '示范对话', 2, 'dialogue', 104, 'John', NULL, 'So, why do you want to leave your current employer?', '那么，你为什么想离开现在的雇主？', NULL, NULL, NULL, 'current employer, interview', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Lara', NULL, 'Our company is moving to Shanghai and I wish to stay in this city.', '我们公司要搬到上海，而我希望留在这个城市。', NULL, NULL, NULL, 'employer, move company', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'dialogue', '示范对话', 2, 'dialogue', 106, 'John', NULL, 'That''s clear. What would you consider your biggest strength and weakness?', '明白了。你认为自己最大的优点和缺点是什么？', NULL, NULL, NULL, 'strength, weakness, interview', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Lara', NULL, 'Well, I''m good at researching materials, but I tend to get bored easily and I''d love to keep myself challenged.', '嗯，我擅长研究资料，但我容易感到无聊，希望不断挑战自己。', NULL, NULL, NULL, 'tend to, strength, challenge', 1),

    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Good afternoon. Thanks for giving me the opportunity to interview for this position.', '下午好。感谢您给我这个岗位面试的机会。', NULL, '根据课件提示补全。', NULL, 'opportunity, job interview', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Nice to meet you. Did you have trouble finding your way here?', '很高兴认识你。你找到这里有困难吗？', NULL, NULL, NULL, 'have trouble, interview', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I''m very familiar with the area so there was no problem.', '我很熟悉这个地区，所以没有问题。', NULL, NULL, NULL, 'familiar, interview', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Glad to hear that. You said on your resume that you''re experienced in selling. So, what would you consider your biggest strength?', '很高兴听到这个。你在简历上说自己有销售经验。那么，你认为自己最大的强项是什么？', NULL, NULL, NULL, 'resume, selling, strength', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'I''m probably best at convincing customers to buy our products.', '我最擅长说服顾客购买我们的产品。', NULL, NULL, NULL, 'convince customers, strength', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'What about your biggest weakness? What are you not good at?', '那你最大的弱点呢？你不擅长什么？', NULL, NULL, NULL, 'weakness, interview', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'Well, I don''t like sitting idly all day, and I tend to keep myself busy.', '嗯，我不喜欢整天无所事事，我倾向于让自己忙起来。', NULL, NULL, NULL, 'tend to, keep busy', 1),

    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you ever been to a job interview? What questions were you asked? Or what questions do you think you''ll be asked?', '你参加过工作面试吗？被问了什么问题？或者你认为会被问到什么？', NULL, '可谈自我介绍、优点和缺点、性格、时间管理、压力下工作和犯错等问题。', NULL, 'job interview, questions, work', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'If you are going to take a job interview, what will you do to prepare for it?', '如果你要参加工作面试，会如何准备？', NULL, '可以研究公司、查询公共交通路线、准备问题、打印多份简历、决定穿着，并确保准时到达。', NULL, 'job interview, preparation, resume', 1),

    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Why do you want to leave your current employer?\nWhat would you consider your biggest strength and weakness?', '复习：employer / tend to / strength / weakness / have trouble。', NULL, NULL, NULL, 'review, job interview', 1),

    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Research the company', 'Research the company''s profile and the position you are applying for.', '研究公司的简介和你申请的职位。', NULL, '课后拓展：面试前必须做的四件事。', NULL, 'company profile, job interview', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Anticipate questions', 'Anticipate regular questions from the interviewer, such as “Why do you want this job?” and “What is your biggest weakness?”', '预想面试官的常见问题，例如“你为什么想要这份工作？”和“你最大的弱点是什么？”', NULL, '课后拓展：面试前必须做的四件事。', NULL, 'interviewer, questions, weakness', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Dress well', 'Dress well. The image you present is really important.', '穿着得体。你展示出的形象非常重要。', NULL, '课后拓展：面试前必须做的四件事。', NULL, 'dress well, job interview', 1),
    ('job-interview', 'Chapter 7 · Work', 'Lesson 55 · Job Interview', 55, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Arrive early', 'It''s important to arrive a few minutes early.', '提前几分钟到达很重要。', NULL, '课后拓展：面试前必须做的四件事。', NULL, 'arrive early, job interview', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 56 · Arriving Late (doc/114558_812_Arriving Late.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'continual', 'continual', '连续的；频繁的', '/kənˈtɪnjuəl/', 'repeated many times in a way that is annoying; usually not used for positive things', 'The baby''s continual crying drove me crazy.', 'continual, arriving late, work', 1),
    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'hold up', 'hold up', '阻碍；使停滞', '/hoʊld ʌp/', 'to delay or block the movement or progress of somebody or something', 'An accident is holding up traffic.', 'hold up, traffic, arriving late', 1),
    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'anticipate', 'anticipate', '预测；预料', '/ænˈtɪsɪpeɪt/', 'to see what might happen in the future and take action to prepare for it; predict', 'Try and anticipate what the interviewers will ask.', 'anticipate, work, planning', 1),
    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'promise', 'promise', '承诺', '/ˈprɑːmɪs/', 'to tell somebody that you will definitely do or not do something, or that something will definitely happen', 'I''ll see what I can do but I can''t promise anything.', 'promise, work, arriving late', 1),
    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'plan on', 'plan on doing something', '计划；打算（做某事）', '/plæn ɑːn/', 'to intend to do something, or to expect something to happen', 'We are planning on going to Australia this year.', 'plan on, work, arriving late', 1),

    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Philip', NULL, 'You have been late three times in the last two weeks. Is this going to be a continual problem?', '过去两周你已经迟到三次了。这会成为持续的问题吗？', NULL, NULL, NULL, 'continual problem, late for work', 1),
    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Jack', NULL, 'I''m so sorry. I really got unlucky this morning. I planned on coming to the office early today, but there was an accident that held up traffic.', '非常抱歉。我今天早上真的很倒霉。我计划早到办公室，但发生了一起事故，耽误了交通。', NULL, NULL, NULL, 'planned on, held up traffic', 1),
    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Philip', NULL, 'You''d better start anticipating all problems because I''m not going to tolerate your being late any longer. Is that clear?', '你最好开始预料所有问题，因为我不会再容忍你迟到了。明白吗？', NULL, NULL, NULL, 'anticipate, tolerate, late', 1),
    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Jack', NULL, 'Perfectly clear. I promise I will not be late again.', '完全明白。我保证再也不会迟到。', NULL, NULL, NULL, 'promise, not be late', 1),
    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Philip', NULL, 'That''s all.', '就这样。', NULL, NULL, NULL, 'work, arriving late', 1),

    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'You''ve been late three times in the last week. Is this going to be your habit?', '上周你迟到三次了。这会成为你的习惯吗？', NULL, '根据课件提示补全。', NULL, 'late, work', 1),
    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I''m so sorry. Last week I had a lot of personal problems. This morning I planned on going to work early, but an accident held up traffic on the road.', '非常抱歉。上周我有很多个人问题。今天早上我计划早去上班，但路上的事故耽误了交通。', NULL, NULL, NULL, 'planned on, held up traffic', 1),
    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'You''d better anticipate all your personal problems. If you are late frequently, it shows that you are irresponsible.', '你最好预料到所有个人问题。如果你经常迟到，就表明你不负责任。', NULL, NULL, NULL, 'anticipate, irresponsible, late', 1),
    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Yes, sir. I promise I''ll never be late again.', '是的，先生。我保证再也不会迟到。', NULL, NULL, NULL, 'promise, late', 1),
    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Fine. Now get back to your work.', '好。现在回去工作吧。', NULL, NULL, NULL, 'get back to work, workplace', 1),

    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'How often are you late for work? What are some common reasons or excuses for being late?', '你多久上班迟到一次？迟到有哪些常见原因或借口？', NULL, '可谈堵车、闹钟没响、身体不舒服、照顾家人或宠物，以及恶劣天气。', NULL, 'arriving late, work, excuses', 1),
    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you think being late is a serious problem? If you were a team leader and some team members were always late for work, what would you do?', '你认为迟到是严重问题吗？如果你是团队负责人，有成员总是上班迟到，你会怎么做？', NULL, '严重：缺乏责任感、浪费他人时间、表现出成员对工作的态度。不严重：可能只是倒霉，人人都会遇到，工作质量更重要。可先找原因并帮助他们解决问题。', NULL, 'team leader, arriving late, work', 1),

    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'There was an accident that held up traffic.\nI promise I will not be late again.', '复习：continual / hold up / anticipate / promise / plan on。', NULL, NULL, NULL, 'review, arriving late', 1),

    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'punctual', 'punctual', '准时的；准点的', NULL, '课后拓展：守时词汇。', NULL, 'punctual, work', 1),
    ('arriving-late', 'Chapter 7 · Work', 'Lesson 56 · Arriving Late', 56, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'unpunctual', 'unpunctual', '不守时的；爱迟到的', NULL, '课后拓展：守时词汇。', NULL, 'unpunctual, work', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 57 · Asking for a Leave (doc/115059_812_Asking for a Leave.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'flu', 'flu', '流感', '/fluː/', 'also influenza; an infectious disease like a very bad cold that causes fever, pains, and weakness', 'The whole family has the flu.', 'flu, sick leave, work', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'log', 'log', '登记；记录', '/lɔːɡ/', 'to put information in an official record or write a record of events', 'The police log all phone calls.', 'log, sick day, work', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'cover', 'cover', '照料；处理', '/ˈkʌvər/', 'to include something; to deal with something', 'This should cover everyone in the group.', 'cover, co-worker, work', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'urgent', 'urgent', '紧急的', '/ˈɜːrdʒənt/', 'that needs to be dealt with or happen immediately', 'They''ve called an urgent meeting for this evening.', 'urgent, sick leave, work', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'sick day', 'sick day', '病假日', '/sɪk deɪ/', 'also sick leave; a day for which an employee receives pay while absent from work because of illness', 'Each employee gets 7 paid sick days each year.', 'sick day, sick leave, work', 1),

    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'Hi Martha. This is Jack. I think I caught a flu or something. I feel worse than yesterday.', '嗨，Martha。我是 Jack。我想我得了流感之类的病，感觉比昨天更糟。', NULL, NULL, NULL, 'flu, feel worse, sick leave', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Martha', NULL, 'You''d better stay home today then.', '那你今天最好待在家里。', NULL, NULL, NULL, 'stay home, sick leave', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'I think that will be best. I''ll log my sick day tomorrow when I get to the office.', '我想这样最好。我明天到办公室后会登记病假。', NULL, NULL, NULL, 'log sick day, office', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Martha', NULL, 'No problem. Just get some rest. We have everything covered here so don''t worry.', '没问题。好好休息。这里的事情我们都能处理好，所以别担心。', NULL, NULL, NULL, 'covered, rest, work', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'Okay. If something urgent happens, you can call me at home. I''ll be here all day.', '好的。如果有紧急情况，你可以打电话到我家。我会整天待在这里。', NULL, NULL, NULL, 'urgent, call at home', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Martha', NULL, 'Okay. Thanks for calling. See you when you get better.', '好的。谢谢你打电话来。你好些了再见。', NULL, NULL, NULL, 'get better, sick leave', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'All right. Thanks. Bye.', '好的。谢谢。再见。', NULL, NULL, NULL, 'thanks, sick leave', 1),

    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Hey boss, is there anything urgent that needs to be done today?', '老板，今天有什么紧急的事情需要做吗？', NULL, '根据课件提示补全。', NULL, 'urgent, work', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'No, I don''t believe so. What''s the matter?', '没有，我想没有。怎么了？', NULL, NULL, NULL, 'work, sick leave', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I have a terrible headache and I''m wondering if I could take a sick day today.', '我头痛得厉害，我想知道今天能否请病假。', NULL, NULL, NULL, 'sick day, headache', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'I don''t see why not. Don''t worry, we''ll get everything covered here.', '我觉得可以。别担心，我们会把这里的事情处理好。', NULL, NULL, NULL, 'cover, sick leave, work', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Thanks. I''ll log my sick day when I get to the office tomorrow.', '谢谢。我明天到办公室后会登记病假。', NULL, NULL, NULL, 'log, sick day', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'No problem. Get some rest and see you tomorrow.', '没问题。好好休息，明天见。', NULL, NULL, NULL, 'rest, sick leave', 1),

    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'How often do you ask for a sick day or personal day at work? What are some common reasons for you to ask for leave?', '你多久会在工作中请一次病假或事假？请假的常见原因有哪些？', NULL, '可以谈生病，例如发烧、流感或感冒；也可谈家里发生紧急情况。', NULL, 'sick day, personal day, work', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you need to cover your co-worker''s tasks when they take a day off? If your co-worker takes sick days frequently and you always have to do their work, what would you do?', '当同事请假时，你需要处理他们的任务吗？如果同事经常请病假，而你总得做他们的工作，你会怎么做？', NULL, '可以先和那位同事沟通，或向老板寻求帮助。', NULL, 'cover, co-worker, sick leave', 1),

    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I''m wondering if I could take a sick or personal day today.\nIf something urgent happens, you can call me at home.', '复习：flu / log / sick day / cover / urgent。', NULL, NULL, NULL, 'review, leave', 1),

    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'marriage leave', 'marriage leave', '婚假', NULL, '课后拓展：假期类型。', NULL, 'marriage leave, work', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'mourning leave', 'mourning leave', '丧假', NULL, '课后拓展：假期类型。', NULL, 'mourning leave, work', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'maternity leave', 'maternity leave', '产假', NULL, '课后拓展：假期类型。', NULL, 'maternity leave, work', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'paternity leave', 'paternity leave', '陪产假', NULL, '课后拓展：假期类型。', NULL, 'paternity leave, work', 1),
    ('asking-for-a-leave', 'Chapter 7 · Work', 'Lesson 57 · Asking for a Leave', 57, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'lactation leave', 'lactation leave', '哺乳假', NULL, '课后拓展：假期类型。', NULL, 'lactation leave, work', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 58 · Working Overtime (doc/115126_812_Working Overtime.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'punch out', 'punch out', '打卡（下班）', '/pʌntʃ aʊt/', 'to record the time at which you leave work', 'She punches out at 7:15.', 'punch out, work, overtime', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'no way', 'no way', '没门儿；想得美', '/noʊ weɪ/', 'informal: used to say there is no possibility that you will do something or that something will happen', '“Do you want to help?” “No way!”', 'no way, work, overtime', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'first thing', 'first thing', '首先；一大早', '/fɜːrst θɪŋ/', 'before anything else; early in the morning', 'I need the report on my desk first thing Monday morning.', 'first thing, deadline, work', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'deadline', 'deadline', '截止日期；交付期限', '/ˈdedlaɪn/', 'a point in time by which something must be done', 'The deadline for applications is April 30.', 'deadline, work, overtime', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'have enough of', 'have enough of', '受够了', NULL, 'used when something or somebody is annoying you and you no longer want to do or see it; followed by a noun or gerund', 'I''ve had enough of working overtime.', 'have enough of, overtime, work', 1),

    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Daniel', NULL, 'It''s quitting time. I''m going to punch out now. See you, guys.', '到下班时间了。我现在要打卡下班。各位再见。', NULL, NULL, NULL, 'quitting time, punch out', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Tony', NULL, 'Wait, Daniel. Have you finished all the documents we need for tomorrow''s meeting?', '等等，Daniel。明天会议需要的所有文件你完成了吗？', NULL, NULL, NULL, 'documents, meeting, overtime', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Daniel', NULL, 'Not yet. But I can finish those tomorrow.', '还没有，但我明天可以完成。', NULL, NULL, NULL, 'finish documents, work', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Tony', NULL, 'No way! We need those materials first thing in the morning. You must finish them tonight.', '没门儿！我们明天一早就需要这些材料。你今晚必须完成。', NULL, NULL, NULL, 'no way, first thing, deadline', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Daniel', NULL, 'Ugh, I''ve had enough of working overtime!', '唉，我受够加班了！', NULL, NULL, NULL, 'had enough of, overtime', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Tony', NULL, 'This is business. We have a deadline to meet. And you won''t be the only one under pressure. We''ve all got to work on this project tonight.', '这是工作。我们有截止日期要赶。而且不止你一个人有压力，我们今晚都得做这个项目。', NULL, NULL, NULL, 'deadline, under pressure, project', 1),

    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Ugh, I''ve had enough of working overtime.', '唉，我受够加班了。', NULL, '根据课件提示补全。', NULL, 'had enough of, overtime', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'So have I, but that is business. This project is urgent.', '我也是，但这就是工作。这个项目很紧急。', NULL, NULL, NULL, 'urgent project, overtime', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Yeah, we have a deadline to meet, and that is tomorrow. I really wish I could punch out and go home now. Maybe we can work on the report tomorrow.', '是啊，我们要赶截止日期，就是明天。我真希望现在能打卡下班回家。也许我们明天再做报告。', NULL, NULL, NULL, 'deadline, punch out, report', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'No way. We need this report first thing in the morning.', '没门儿。明天一早我们就需要这份报告。', NULL, NULL, NULL, 'no way, first thing, report', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'I know. And I''m not the only one under pressure. You guys are all with me.', '我知道。而且不止我一个人有压力。你们大家都和我一起。', NULL, NULL, NULL, 'under pressure, teamwork', 1),

    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'How often do you need to work overtime? What are some common reasons for you and your co-workers to work overtime?', '你多久需要加班？你和同事加班有哪些常见原因？', NULL, '可以谈紧急项目或会议、无法按时完成任务、帮助或等待同事，以及补回病假时间。', NULL, 'overtime, co-workers, work', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'What are your feelings about working overtime? Think of some jobs that work overtime the most in China. Do you want to choose one of those jobs?', '你对加班有什么感受？想想在中国最常加班的一些工作。你想选择其中之一吗？', NULL, '可谈累、个人时间变少，但有时是必须的，也在帮助社会。可举警察、护士和医生、司机、IT 从业者等职业。', NULL, 'overtime, jobs, work', 1),

    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I''ve had enough of working overtime.\nThis is business. We have a deadline to meet.', '复习：punch out / no way / first thing / deadline / have had enough of。', NULL, NULL, NULL, 'review, working overtime', 1),

    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Commitment and overtime', 'Arriving at 8 a.m. and leaving at 7 p.m. every day might look good and show your commitment to the company, but be careful not to do it every day.', '每天早上 8 点到、晚上 7 点离开可能看起来很好，也能表明你对公司的投入，但要注意不要每天都这样做。', NULL, '课后拓展：加班的影响。', NULL, 'overtime, commitment, work', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Overtime can cause harm', 'Sometimes, working overtime may bring you more harm than favors.', '有时加班带来的伤害可能大于好处。', NULL, '课后拓展：加班的影响。', NULL, 'overtime, health, work', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Effects on work', 'Your time-management skills may be questioned; you may be piled up with more work or miss new opportunities; and overtime can become something your boss takes for granted.', '你的时间管理能力可能受到质疑；你可能堆积更多工作或错失新机会；加班也可能成为老板认为理所当然的事。', NULL, '课后拓展：加班的影响。', NULL, 'overtime, time management, work', 1),
    ('working-overtime', 'Chapter 7 · Work', 'Lesson 58 · Working Overtime', 58, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Effects on performance', 'Your performance may drop dramatically if you feel overworked.', '如果你感到工作过度，表现可能会显著下降。', NULL, '课后拓展：加班的影响。', NULL, 'overtime, performance, work', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

COMMIT;
