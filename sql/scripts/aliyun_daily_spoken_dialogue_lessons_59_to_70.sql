-- Extracted from the next ten available PDFs in doc/, ordered by source file identifier.
-- Sources: Learn & Talk I, Chapter 7 Lessons 59-62 and Chapter 8 Lessons 65-70.
-- Source PDFs for Lessons 63 and 64 were unavailable during this import.
-- The target table is created by aliyun_daily_spoken_dialogue_buying_clothes.sql.
-- Re-running this file updates only the lesson_code/item_order pairs below.

SET NAMES utf8mb4;
START TRANSACTION;

-- Lesson 59 · Meetings (doc/115247_812_Meetings.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'regular meeting', 'regular meeting', '例会', '/ˈreɡjələr ˈmiːtɪŋ/', 'a meeting that is held regularly, such as a weekly meeting from 9:00 to 9:30', 'Thank you all for coming to this month''s regular meeting.', 'regular meeting, work, agenda', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'brief', 'brief', '简短的；简洁的', '/briːf/', 'lasting only a short time', 'We should keep this meeting brief.', 'brief, meeting, work', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'client', 'client', '客户', '/ˈklaɪənt/', 'a person who uses the services or advice of a professional person or organization; a customer', 'We must always consider the needs of our clients.', 'client, meeting, project', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'behind schedule', 'behind schedule', '（进度）落后', '/bɪˈhaɪnd ˈskedʒuːl/', 'having failed to do something by the appointed time, especially the time given on a written plan', 'The project is behind schedule by two weeks. I don''t want to fall behind schedule.', 'behind schedule, project, deadline', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'halfway through', 'halfway through', '到一半；到中途', '/ˌhæfˈweɪ θruː/', 'half finished; at the middle point of something', 'We''re about halfway through the project.', 'halfway through, project, meeting', 1),

    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Joe', NULL, 'Okay, I know everyone is busy so we''ll keep this week''s regular meeting brief. Neil, how''s your team''s project going?', '好的，我知道大家都很忙，所以本周例会会简短些。Neil，你们团队的项目进展如何？', NULL, NULL, NULL, 'regular meeting, project', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Neil', NULL, 'Quite well. We have three weeks left before our deadline and we''re halfway through.', '相当不错。离截止日期还有三周，我们已经完成一半了。', NULL, NULL, NULL, 'deadline, halfway through', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Joe', NULL, 'Good. Kate, how''s your team doing with that website?', '很好。Kate，你们团队做那个网站进展如何？', NULL, NULL, NULL, 'team, website, meeting', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Kate', NULL, 'It''s a bit of a headache. The client keeps changing their mind about what they want.', '有点棘手。客户不停改变他们想要的东西。', NULL, NULL, NULL, 'client, change mind, project', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Joe', NULL, 'It sounds like you''re falling behind schedule?', '听起来你们进度落后了？', NULL, NULL, NULL, 'behind schedule, project', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Kate', NULL, 'I''m afraid so. It''s going to be hard for us to finish the website on time.', '恐怕是的。我们很难按时完成网站。', NULL, NULL, NULL, 'finish on time, website', 1),

    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Let''s keep the regular meeting brief since you''re all busy. So, how''s the project?', '既然大家都忙，我们把例会开得简短些。项目怎么样？', NULL, '根据课件提示补全。', NULL, 'regular meeting, brief', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'It''s not going so well. We''re already halfway through, but the client changed their mind yesterday. They said they wanted a new design for the website.', '进展不太顺利。我们已经做到一半，但客户昨天改变了主意，说网站要用新设计。', NULL, NULL, NULL, 'halfway through, client, design', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Hmm. I guess you won''t be able to finish it on time then.', '嗯。那我猜你们没法按时完成了。', NULL, NULL, NULL, 'finish on time, project', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'I''m afraid we are falling behind the schedule. Maybe we should change our plan.', '恐怕我们落后于计划了。也许应该改变计划。', NULL, NULL, NULL, 'behind schedule, plan', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'That makes sense. I''ll discuss it with other managers.', '这有道理。我会和其他经理讨论。', NULL, NULL, NULL, 'discuss, managers, meeting', 1),

    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you have regular meetings in your company? What do you talk about at the regular meeting?', '你的公司有例会吗？例会上谈些什么？', NULL, '可以谈项目、进度、跟进、总结和活动等。', NULL, 'regular meeting, work, project', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you like meetings? Do you think meetings are a waste of time? How can meetings be effective?', '你喜欢开会吗？你认为会议浪费时间吗？如何让会议有效？', NULL, '开会前要有准备、保持简短并聚焦议程。', NULL, 'meetings, agenda, work', 1),

    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I know everyone is busy so we''ll keep this week''s regular meeting brief.\nHow''s your team doing with ...?', '复习：regular meeting / brief / client / behind schedule / halfway through。', NULL, NULL, NULL, 'review, meetings', 1),

    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'gathering / party', 'gathering / party', '聚会', NULL, '课后拓展：会议与聚会类型。', NULL, 'gathering, party, meeting', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'seminar', 'seminar', '研讨会', NULL, '课后拓展：会议与聚会类型。', NULL, 'seminar, meeting', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'assembly', 'assembly', '集会', NULL, '课后拓展：会议与聚会类型。', NULL, 'assembly, meeting', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'conference', 'conference', '大型会议', NULL, '课后拓展：会议与聚会类型。', NULL, 'conference, meeting', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'congress', 'congress', '国内大会', NULL, '课后拓展：会议与聚会类型。', NULL, 'congress, meeting', 1),
    ('meetings', 'Chapter 7 · Work', 'Lesson 59 · Meetings', 59, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'summit', 'summit', '峰会', NULL, '课后拓展：会议与聚会类型。', NULL, 'summit, meeting', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 60 · Asking for a Raise (doc/115352_812_Asking for a Raise.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'salary', 'salary', '薪水；工资', '/ˈsæləri/', 'money that employees receive for doing their job, usually paid every month', 'She''s on a salary of £24,000.', 'salary, raise, work', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'raise', 'raise', '加薪', '/reɪz/', 'an increase in the money you are paid for the work you do', 'If I asked my boss for a raise, he would fire me.', 'raise, salary, work', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'lay off', 'lay off', '解雇；开除；裁员', '/leɪ ɔːf/', 'to stop employing somebody because there is not enough work or money; to fire somebody', '200 workers at the factory have been laid off.', 'lay off, job, work', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'exception', 'exception', '例外', '/ɪkˈsepʃn/', 'a thing that does not follow a rule', 'There are always a lot of exceptions to grammar rules.', 'exception, raise, work', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'take on', 'take on', '承担', '/teɪk ɑːn/', 'to decide to do something or agree to be responsible for something', 'I can''t take on any extra work.', 'take on, responsibility, work', 1),

    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Oliver', NULL, 'Take a seat. You wanted to meet with me?', '请坐。你想和我谈谈？', NULL, NULL, NULL, 'meet with, salary', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Amy', NULL, 'Yes, I was wondering if we could talk about my salary.', '是的，我想知道我们能否谈谈我的薪水。', NULL, NULL, NULL, 'salary, ask for a raise', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Oliver', NULL, 'Well, you''ve only been here for half a year. I think it''s too early for a raise.', '嗯，你在这里才工作半年。我觉得现在谈加薪还太早。', NULL, NULL, NULL, 'raise, work experience', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Amy', NULL, 'I know, but my husband was laid off from his job recently, and we have a lot of unpaid bills.', '我知道，但我丈夫最近被裁员了，我们有很多未付账单。', NULL, NULL, NULL, 'laid off, unpaid bills', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Oliver', NULL, 'Umm. Well, I''m willing to make an exception and give you a 5% raise. But from now on, you''ll have to take on some extra responsibilities.', '嗯。我愿意破例给你加薪 5%。但从现在起，你得承担一些额外责任。', NULL, NULL, NULL, 'exception, raise, responsibility', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Amy', NULL, 'That''s fine. Thank you so much.', '没问题。非常感谢。', NULL, NULL, NULL, 'thanks, raise', 1),

    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Hi boss, I''m wondering if we could talk about my salary.', '老板您好，我想知道我们能否谈谈我的薪水。', NULL, '根据课件提示补全。', NULL, 'salary, raise', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Oh, you''re a good employee, but you''ve only been here for half a year. It''s too early to talk about that, isn''t it?', '哦，你是个好员工，但你在这里才半年。现在谈这件事还太早，不是吗？', NULL, NULL, NULL, 'employee, salary, raise', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I know, but my parents ran into an accident recently, and I really need a raise. I promise that I will take on more responsibilities at work.', '我知道，但我父母最近出了事故，我确实需要加薪。我保证会在工作中承担更多责任。', NULL, NULL, NULL, 'raise, take on, responsibility', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'I''m sorry to hear that. Well, given this circumstance, I''m willing to make an exception and give you a 5% raise.', '听到这个我很难过。考虑到这种情况，我愿意破例给你加薪 5%。', NULL, NULL, NULL, 'exception, 5% raise', 1),

    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you ever asked for a raise? Are you happy with your salary? Why do you think some people never ask for a raise?', '你曾要求加薪吗？你对薪水满意吗？为什么有些人从不要求加薪？', NULL, '有人在需要开口前就得到加薪；有人不想失去工作；有人觉得和老板谈薪水不舒服。', NULL, 'raise, salary, work', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'How should employees ask for a raise? What do you think are good reasons for employees to get a raise?', '员工应该如何要求加薪？哪些理由适合加薪？', NULL, '沟通要简短且自信，展示数据和事实，例如为公司做出的贡献，并承诺承担更多工作。', NULL, 'ask for a raise, salary, work', 1),

    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I was wondering if we could talk about my salary.\nYou''ll have to take on some extra responsibilities.', '复习：salary / raise / lay off / exception / take on。', NULL, NULL, NULL, 'review, raise', 1),

    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Gather evidence', 'Gather evidence of your outstanding achievements at work.', '收集你在工作中突出成就的证据。', NULL, '课后拓展：如何要求加薪。', NULL, 'raise, achievements, work', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Choose the right moment', 'Choose the right moment. If you''ve just created a whole bunch of value for your company, it''s a great time to ask.', '选择合适的时机。如果你刚为公司创造了很多价值，就是提出要求的好时机。', NULL, '课后拓展：如何要求加薪。', NULL, 'raise, timing, value', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Be confident', 'Be calm and conversational, and establish an air of collaboration.', '保持冷静、自然交流，并营造合作的氛围。', NULL, '课后拓展：如何要求加薪。', NULL, 'raise, confidence, collaboration', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Avoid grievances or threats', 'Never start the conversation with a grievance or threat.', '不要以委屈或威胁开始谈话。', NULL, '课后拓展：如何要求加薪。', NULL, 'raise, communication', 1),
    ('asking-for-a-raise', 'Chapter 7 · Work', 'Lesson 60 · Asking for a Raise', 60, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'Have a Plan B', 'If your request is declined, have a Plan B at hand.', '如果请求被拒绝，要准备好备选方案。', NULL, '课后拓展：如何要求加薪。', NULL, 'raise, plan B, work', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 61 · Promotion (doc/115391_812_Promotion.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'replacement', 'replacement', '替代；替补', '/rɪˈpleɪsmənt/', 'a person who replaces another person in an organization, especially in their job', 'We need to find a replacement for Sue.', 'replacement, promotion, work', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'post', 'post', '张贴；公布', '/poʊst/', 'to put a notice in a public place so that people can see it', 'A copy of the letter was posted on the noticeboard.', 'post, job notice, promotion', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'internal', 'internal', '内部的', '/ɪnˈtɜːrnl/', 'involving only people who are part of a particular organization rather than people from outside it', 'This is an internal meeting.', 'internal, promotion, applicants', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'let someone down', 'let someone down', '使某人失望', NULL, 'to fail to help or support somebody as they had hoped or expected', 'I believe she won''t let you down.', 'let down, promotion, work', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'apply for', 'apply for', '申请（职位等）', '/əˈplaɪ/', 'to make a formal request, usually in writing, for something such as a job or a place at college', 'You should apply for this position by letter.', 'apply for, promotion, position', 1),

    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Kenny', NULL, 'I heard that Dan will be retiring soon. I''m wondering if you have found a replacement.', '我听说 Dan 很快要退休了。我想知道你是否已经找到替代人选。', NULL, NULL, NULL, 'retiring, replacement, promotion', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Wendy', NULL, 'Not yet. We''ll post a job notice for internal applicants this week.', '还没有。我们这周会为内部申请人张贴职位公告。', NULL, NULL, NULL, 'post job notice, internal applicants', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Kenny', NULL, 'I hope you''ll consider me for the position. I know it''s a challenging role, but I think I''m ready to take on more responsibility.', '我希望你能考虑让我担任这个职位。我知道这是有挑战的角色，但我认为自己已准备承担更多责任。', NULL, NULL, NULL, 'position, responsibility, promotion', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Wendy', NULL, 'Yes, it''s a big change to go from sales representative to sales manager. But I think you would make a good manager. I encourage you to apply for the position.', '是的，从销售代表到销售经理是很大变化。但我认为你会成为一名好经理。我鼓励你申请这个职位。', NULL, NULL, NULL, 'sales manager, apply for', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Kenny', NULL, 'Thank you. If you give me a chance, I know I won''t let you down.', '谢谢。如果你给我机会，我知道我不会让你失望。', NULL, NULL, NULL, 'let you down, promotion', 1),

    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Hi boss, I heard Mary will be quitting next month. Have you found a replacement for her?', '老板您好，我听说 Mary 下个月要辞职。您找到替代她的人了吗？', NULL, '根据课件提示补全。', NULL, 'replacement, promotion', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Not yet, we''re going to post a job notice tomorrow. Are you interested in that position?', '还没有，我们明天要张贴职位公告。你对这个职位感兴趣吗？', NULL, NULL, NULL, 'post, job notice, position', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Yes, if you''re considering internal applicants, please consider me for the position. I know it''s a challenging one, but I''m ready to take on the responsibility.', '是的，如果您考虑内部申请人，请考虑我担任这个职位。我知道它有挑战，但我准备承担这项责任。', NULL, NULL, NULL, 'internal applicants, responsibility', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Glad to hear that. After we post the notice, you can apply for the position by email.', '很高兴听到这个。公告张贴后，你可以通过电子邮件申请该职位。', NULL, NULL, NULL, 'apply for, email, position', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Thank you. If you give me a chance, I won''t let you down.', '谢谢。如果您给我机会，我不会让您失望。', NULL, NULL, NULL, 'let you down, promotion', 1),

    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you want a promotion? Would you ask for a promotion? What do you think are the pros and cons of a promotion?', '你想升职吗？会要求升职吗？升职有什么优缺点？', NULL, '优点：薪水更高、获得更多尊重和更有价值的经验。缺点：压力和责任更大、工作时间更长。', NULL, 'promotion, pros and cons, work', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'If a manager is quitting his or her job, what should the company do to get a replacement: promote internal employees, or hire new external employees? Which way do you think is better?', '如果经理辞职，公司应如何补位：提拔内部员工，还是招聘外部员工？你认为哪种方式更好？', NULL, '内部方式：彼此熟悉、无需培训、能激励员工。外部方式：带来新人和新想法，可从更多申请者中选择。', NULL, 'replacement, internal, external, promotion', 1),

    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I''m wondering if you had found a replacement.\nI know it''s a challenging role, but I think I''m ready to take on more responsibility.', '复习：replacement / post / internal / apply for / let someone down。', NULL, NULL, NULL, 'review, promotion', 1),

    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Set a career goal', 'Set a goal for your career and work towards that goal.', '为职业设定目标，并朝着它努力。', NULL, '课后拓展：获得升职的一些建议。', NULL, 'career goal, promotion', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Positive attitude', 'Keep a positive attitude at work.', '在工作中保持积极态度。', NULL, '课后拓展：获得升职的一些建议。', NULL, 'positive attitude, promotion', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Avoid gossip and politics', 'Avoid office gossip and office politics.', '避免办公室八卦和办公室政治。', NULL, '课后拓展：获得升职的一些建议。', NULL, 'office gossip, office politics', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Help your boss', 'Help your boss with their work if you can.', '如果可以，帮助老板处理工作。', NULL, '课后拓展：获得升职的一些建议。', NULL, 'boss, promotion, work', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'Volunteer for projects', 'Volunteer for new projects.', '主动参与新项目。', NULL, '课后拓展：获得升职的一些建议。', NULL, 'volunteer, projects, promotion', 1),
    ('promotion', 'Chapter 7 · Work', 'Lesson 61 · Promotion', 61, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'Ask at the right time', 'Wait until the time is right to ask for it.', '等到合适的时机再提出请求。', NULL, '课后拓展：获得升职的一些建议。', NULL, 'promotion, timing, work', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 62 · Starting a Business (doc/115392_812_Starting a Business.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'abandon', 'abandon', '放弃；抛弃', '/əˈbændən/', 'to stop doing something, especially before it is finished', 'They abandoned the match because of rain.', 'abandon, business, start-up', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'regulation', 'regulation', '规章；制度', '/ˌreɡjuˈleɪʃn/', 'an official rule made by a government or some other authority', 'Under the new regulations, selling wine online will be strictly controlled.', 'regulation, business, government', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'themed', 'themed', '（以……为）主题的', '/θiːmd/', 'designed to reflect a particular subject or period of history', 'At a themed café, you''re not only paying for the food, you''re paying for the experience.', 'themed, café, business', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'start-up', 'start-up', '初创的；启动的；初创公司', '/ˈstɑːrt ʌp/', 'connected with starting a new business or project; informally, a company in the first stage of its operations', 'Have you got enough money for start-up costs?', 'start-up, business, costs', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'one of a kind', 'one of a kind', '独一无二的', NULL, 'the only one like this; unique', 'My father was one of a kind — I''ll never be like him.', 'one of a kind, unique, business', 1),

    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Linda', NULL, 'Hey Jim, how''s your plan for that online wine shop going?', '嗨，Jim。你的在线葡萄酒商店计划进展如何？', NULL, NULL, NULL, 'online shop, business plan', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Jim', NULL, 'Oh, I''ve abandoned that idea. The government''s new regulations have made it too difficult to sell wine online. I''m thinking about opening a café downtown.', '哦，我已经放弃那个想法了。政府的新规使得网上卖酒太困难。我正考虑在市中心开一家咖啡馆。', NULL, NULL, NULL, 'abandon, regulations, café', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Linda', NULL, 'But there are already so many cafés downtown.', '但市中心已经有很多咖啡馆了。', NULL, NULL, NULL, 'cafés, business', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Jim', NULL, 'Yeah, but mine will be different. It''s going to be a cat-themed café. People will be able to pet all kinds of lovely cats while enjoying their food. It will be one of a kind.', '是的，但我的会不同。它将是一家猫主题咖啡馆。人们能一边享用食物，一边抚摸各种可爱的猫。它会独一无二。', NULL, NULL, NULL, 'cat-themed café, one of a kind', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Linda', NULL, 'That sounds interesting. Do you have enough money for rent and start-up costs?', '听起来很有趣。你有足够的钱支付租金和创业成本吗？', NULL, NULL, NULL, 'rent, start-up costs, business', 1),

    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'How''s your plan for that online wine shop going?', '你的在线葡萄酒商店计划进展如何？', NULL, '根据课件提示补全。', NULL, 'online wine shop, business', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'The government''s new regulations have made it too difficult to sell wine online, so I''ve abandoned that idea. I''m thinking about opening a themed café now.', '政府新规使网上卖酒太困难，所以我放弃了那个想法。我现在正考虑开一家主题咖啡馆。', NULL, NULL, NULL, 'regulations, abandon, themed café', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Sounds interesting. What theme will it be?', '听起来有趣。会是什么主题？', NULL, NULL, NULL, 'theme, café, business', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'I''m considering a Hello Kitty themed one. But first, I need to get enough money to cover the rent and other start-up costs.', '我在考虑以 Hello Kitty 为主题。但首先，我得筹到足够的钱来支付租金和其他创业成本。', NULL, NULL, NULL, 'themed, rent, start-up costs', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Yeah, maybe you can apply for a business loan.', '是啊，也许你可以申请商业贷款。', NULL, NULL, NULL, 'business loan, start-up', 1),

    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you have any friends who start their own business? Do you want to start your own business? Why or why not?', '你有朋友自己创业吗？你想自己创业吗？为什么？', NULL, '想创业：做自己的老板、赚钱、制定所有规则、自己做决定。不想：创业成本高、需要花更多时间、得照顾一切。', NULL, 'start a business, entrepreneurship, work', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you think it is difficult for young people to start a business in China? If young people are to start a business, what do you think they''ll need?', '你认为年轻人在中国创业困难吗？如果年轻人创业，你认为他们需要什么？', NULL, '可谈法规、政府或家庭支持、决心，以及创意、资金、法律帮助、地点和员工。', NULL, 'young people, start-up, business', 1),

    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'It will be one of a kind.\nDo you have enough money for rent and start-up costs?', '复习：abandon / regulation / themed / start-up / one of a kind。', NULL, NULL, NULL, 'review, starting a business', 1),

    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Evaluate yourself', 'Evaluate yourself. What skills do you have?', '评估自己：你有什么技能？', NULL, '课后拓展：创业指南。', NULL, 'business, skills, start-up', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Think of a business idea', 'Think of a business idea.', '思考一个商业创意。', NULL, '课后拓展：创业指南。', NULL, 'business idea, start-up', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Do market research', 'Do market research. Know your future rivals and partners.', '进行市场调研，了解未来的竞争对手和合作伙伴。', NULL, '课后拓展：创业指南。', NULL, 'market research, business', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Make it official', 'Make it official. You''d better go to a lawyer for help.', '让业务正式成立。最好向律师寻求帮助。', NULL, '课后拓展：创业指南。', NULL, 'lawyer, business, start-up', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'Write a business plan', 'Write your business plan.', '写下你的商业计划。', NULL, '课后拓展：创业指南。', NULL, 'business plan, start-up', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'Finance your business', 'Finance your business. Get the resources you need!', '为企业融资，获取所需资源！', NULL, '课后拓展：创业指南。', NULL, 'finance, resources, business', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'extra', '拓展学习', 6, 'extra', 507, NULL, 'Develop your product or service', 'Develop your product or service.', '开发你的产品或服务。', NULL, '课后拓展：创业指南。', NULL, 'product, service, business', 1),
    ('starting-a-business', 'Chapter 7 · Work', 'Lesson 62 · Starting a Business', 62, 'extra', '拓展学习', 6, 'extra', 508, NULL, 'Build your team', 'Start building your team.', '开始组建你的团队。', NULL, '课后拓展：创业指南。', NULL, 'team, start-up, business', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 65 · Sports (doc/115645_813_Sports.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'cycling', 'cycling', '骑行', '/ˈsaɪklɪŋ/', 'biking; the sport or activity of riding a bicycle', 'Cycling is Europe''s second most popular sport.', 'cycling, sports, health', 1),
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'cyclist', 'cyclist', '骑自行车的人；自行车骑手', '/ˈsaɪklɪst/', 'a person who rides a bicycle', 'They are both very keen cyclists.', 'cyclist, cycling, sports', 1),
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'court', 'court', '球场', '/kɔːrt/', 'a place where games such as tennis are played', 'There is a badminton court at the sports center.', 'court, tennis, badminton', 1),
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'sidewalk', 'sidewalk', '人行道', '/ˈsaɪdwɔːk/', 'a flat part at the side of a road for people to walk on', 'Don''t ride your bike on the sidewalk!', 'sidewalk, cycling, sports', 1),
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'running track', 'running track', '跑道', '/ˈrʌnɪŋ træ k/', 'a piece of ground, usually oval-shaped, used for races involving athletes', 'This is a 400m outdoor running track.', 'running track, running, sports', 1),

    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Bob', NULL, 'What sports do you do?', '你做什么运动？', NULL, NULL, NULL, 'sports, exercise', 1),
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Jane', NULL, 'Sometimes I play tennis, but I have to book the time to use the tennis court.', '我有时打网球，但必须预约使用网球场的时间。', NULL, NULL, NULL, 'tennis, court, booking', 1),
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Bob', NULL, 'Well, I prefer running. I can do that wherever I want to — go to the running track, or just use the sidewalk next to the road.', '嗯，我更喜欢跑步。我想在哪儿跑就在哪儿跑——去跑道，或者用道路旁的人行道。', NULL, NULL, NULL, 'running, running track, sidewalk', 1),
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Jane', NULL, 'Yeah, sounds great. How about cycling? Do you like it?', '是啊，听起来不错。骑行呢？你喜欢吗？', NULL, NULL, NULL, 'cycling, sports', 1),
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Bob', NULL, 'Yes, it''s faster than running.', '喜欢，它比跑步更快。', NULL, NULL, NULL, 'cycling, running, sports', 1),
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Jane', NULL, 'I have a friend who runs a cycling club. You can join his club to meet other cyclists and do the sport with them.', '我有个朋友经营一个骑行俱乐部。你可以加入，认识其他骑行者并和他们一起运动。', NULL, NULL, NULL, 'cycling club, cyclists', 1),

    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'What sports do you like?', '你喜欢什么运动？', NULL, '根据课件提示补全。', NULL, 'sports, exercise', 1),
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I like running very much. There is a playground near my home and I always use the running track there. What about you?', '我很喜欢跑步。我家附近有一个操场，我总用那里的跑道。你呢？', NULL, NULL, NULL, 'running track, sports', 1),
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I''m a big fan of cycling. It''s great fun to ride bicycles with a lot of other cyclists.', '我是骑行的忠实爱好者。和许多其他骑行者一起骑车很有趣。', NULL, NULL, NULL, 'cycling, cyclists, sports', 1),
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'That sounds good. Do you play ball games, like tennis or badminton?', '听起来不错。你打球类运动吗，例如网球或羽毛球？', NULL, NULL, NULL, 'tennis, badminton, sports', 1),
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Sometimes, but I find it difficult to book a court to play them.', '有时打，但我觉得很难预约球场。', NULL, NULL, NULL, 'book a court, ball games', 1),

    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you play any sports these days? If yes, which sports do you play and how often? If not, how do you get exercise?', '这些天你做运动吗？如果做，做什么以及多久一次？如果不做，如何锻炼？', NULL, '可以谈网球、足球、篮球、游泳、跑步或高尔夫；不做运动时可以散步、爬楼梯或去健身房。', NULL, 'sports, exercise, health', 1),
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'In your opinion, what''s the most popular sport in China? Do you like it? Why or why not?', '你认为中国最受欢迎的运动是什么？你喜欢吗？为什么？', NULL, '可以谈乒乓球、排球或羽毛球；理由包括有趣、有益健康、帮助放松，也可谈很累或麻烦，例如天气不好或需要预约球场。', NULL, 'popular sport, China, health', 1),

    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'What sports do you do to get exercise?\nI have to book the time to use the tennis court.', '复习：cycling / cyclist / court / sidewalk / running track。', NULL, NULL, NULL, 'review, sports', 1),

    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'spectator', 'spectator', '（体育赛事的）观众', NULL, '课后拓展：体育观赛词汇。', NULL, 'spectator, sports', 1),
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'seating areas', 'seating areas', '座位区域', NULL, '课后拓展：体育观赛词汇。', NULL, 'seating areas, sports', 1),
    ('sports', 'Chapter 8 · Health', 'Lesson 65 · Sports', 65, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'standing-only sections', 'standing-only sections', '站立式看台区域', NULL, '课后拓展：体育观赛词汇。', NULL, 'standing-only sections, sports', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 66 · Weight Control (doc/115725_813_Weight Control.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'diet', 'diet', '规定饮食；节食', '/ˈdaɪət/', 'a limited variety or amount of food that you eat for medical reasons or because you want to lose weight', 'I decided to go on a diet before my holiday.', 'diet, nutrition, health', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'fat', 'fat', '脂肪', '/fæt/', 'a white or yellow substance in the bodies of animals and humans, stored under the skin', 'This ham has too much fat on it.', 'fat, diet, nutrition', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'metabolism', 'metabolism', '新陈代谢', '/məˈtæbəlɪzəm/', 'the chemical processes in living things that change food into energy for growth', 'The body''s metabolism is slowed down by extreme cold.', 'metabolism, diet, health', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'speed up', 'speed up', '加速；使……加速', '/spiːd ʌp/', 'to make something move or happen faster', 'They have sped up production of the new car.', 'speed up, metabolism, health', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'incorporate', 'incorporate', '融入；结合', '/ɪnˈkɔːrpəreɪt/', 'to include something so that it forms a part of something', 'Many of your suggestions have been incorporated in the plan.', 'incorporate, exercise, diet', 1),

    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Ben', NULL, 'Hi Julie. You look great! Have you lost weight?', '嗨，Julie。你看起来很棒！你减重了吗？', NULL, NULL, NULL, 'weight control, diet', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Julie', NULL, 'Hi Ben. Yeah, I''ve been on a diet for a couple of months.', '嗨，Ben。是的，我已经节食几个月了。', NULL, NULL, NULL, 'on a diet, weight control', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Ben', NULL, 'Wow, what type of diet are you on?', '哇，你采用什么类型的饮食计划？', NULL, NULL, NULL, 'diet, nutrition', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Julie', NULL, 'Instead of eating 3 times a day, I eat 5 smaller meals. It naturally speeds up the metabolism and helps to burn fat at a faster rate.', '我不再一天吃三顿，而是吃五顿少量餐。这样能自然加快新陈代谢，并帮助更快燃烧脂肪。', NULL, NULL, NULL, 'smaller meals, metabolism, fat', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Ben', NULL, 'That makes sense. I''m going to try that.', '这有道理。我打算试试。', NULL, NULL, NULL, 'makes sense, diet', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Julie', NULL, 'Remember to incorporate a little exercise into your diet.', '记得在饮食计划中加入一些运动。', NULL, NULL, NULL, 'incorporate exercise, diet', 1),

    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'You look better! Did you lose weight?', '你看起来状态更好了！你减重了吗？', NULL, '根据课件提示补全。', NULL, 'weight control, diet', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes, I''ve been on a diet for two months and I''ve lost 5 kilograms.', '是的，我已节食两个月，减了 5 公斤。', NULL, NULL, NULL, 'diet, weight control', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'That''s very much. What kind of diet are you on?', '减了很多。你采用什么饮食计划？', NULL, NULL, NULL, 'diet, nutrition', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'I eat more fruits and vegetables, and avoid food with too much fat in it, such as ham. I also eat more times of smaller meals to speed up my body''s metabolism.', '我多吃水果和蔬菜，避免含太多脂肪的食物，例如火腿。我也少量多餐，以加快身体新陈代谢。', NULL, NULL, NULL, 'fruits, vegetables, fat, metabolism', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'That makes sense. What else have you done to lose weight?', '这有道理。你还做了什么来控制体重？', NULL, NULL, NULL, 'weight control, health', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'I''ve incorporated some exercise into my diet, too.', '我也把一些运动融入饮食计划中。', NULL, NULL, NULL, 'incorporate, exercise, diet', 1),

    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'What do you think a healthy diet is? Are you eating healthy?', '你认为健康饮食是什么？你吃得健康吗？', NULL, '可谈均衡饮食，少脂肪、糖和盐，并摄入鸡蛋、牛奶、水果、蔬菜、肉、鱼和水。', NULL, 'healthy diet, nutrition, health', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Are you satisfied with your weight? What do you think are good ways to control one''s weight, whether gaining or losing?', '你对自己的体重满意吗？你认为控制体重（增重或减重）的好方法是什么？', NULL, '可谈体重偏高或偏低、健康饮食、规律运动、喝足够的水、充足睡眠和保持放松。描述他人身体状况时，课件提示应避免不礼貌用语，优先使用中性表述。', NULL, 'weight control, healthy habits, health', 1),

    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I''ve been on a diet for a couple of months.\nIt speeds up the metabolism and helps to burn fat at a faster rate.', '复习：diet / fat / metabolism / speed up / incorporate。', NULL, NULL, NULL, 'review, weight control', 1),

    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Eat fruits and vegetables', 'Eat lots of fruits and vegetables.', '多吃蔬果。', NULL, '课后拓展：健康饮食建议。', NULL, 'fruits, vegetables, diet', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Eat more fish', 'Eat more fish.', '多吃鱼类。', NULL, '课后拓展：健康饮食建议。', NULL, 'fish, diet, health', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Cut down on fat and sugar', 'Cut down on fat and sugar.', '减少脂肪和糖的摄入。', NULL, '课后拓展：健康饮食建议。', NULL, 'fat, sugar, diet', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Eat less salt', 'Eat less salt.', '少吃盐。', NULL, '课后拓展：健康饮食建议。', NULL, 'salt, diet, health', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'Get more active', 'Get more active.', '多动起来。', NULL, '课后拓展：健康饮食建议。', NULL, 'activity, exercise, health', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'Stay hydrated', 'Don''t get thirsty.', '多喝水。', NULL, '课后拓展：健康饮食建议。', NULL, 'water, diet, health', 1),
    ('weight-control', 'Chapter 8 · Health', 'Lesson 66 · Weight Control', 66, 'extra', '拓展学习', 6, 'extra', 507, NULL, 'Do not skip breakfast', 'Don''t skip breakfast.', '按时吃早餐。', NULL, '课后拓展：健康饮食建议。', NULL, 'breakfast, diet, health', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 67 · Aches and Pains (doc/115726_813_Aches and Pains.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'limp', 'limp', '跛行；一瘸一拐地走', '/lɪmp/', 'to walk slowly or with difficulty because one leg is injured', 'She had twisted her ankle and was limping.', 'limp, injury, aches and pains', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'ache', 'ache', '疼；痛', '/eɪk/', 'as a verb, to feel a continuous dull pain; as a noun, a continuous feeling of pain in a part of the body', 'I''m aching all over. / I get aches and pains all over.', 'ache, pain, health', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'sore', 'sore', '酸痛的', '/sɔːr/', 'if a part of your body is sore, it is painful and often red, especially because of infection or because a muscle has been used too much', 'His feet were sore after the walk.', 'sore, muscles, pain', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'butt', 'butt', '臀部；屁股（非正式）', '/bʌt/', 'informal: the part of the body that you sit on', 'Get off your butt and do some work!', 'butt, informal, body', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'cramp', 'cramp', '痉挛；抽筋；绞痛', '/kræmp/', 'a sudden pain that you get when muscles in part of your body contract, usually caused by cold or too much exercise', 'I got (a) cramp while swimming and almost drowned. BrE: get cramp in your leg; AmE: get a cramp in your leg.', 'cramp, muscles, exercise', 1),

    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Matt', NULL, 'Hey Sarah. Why are you limping?', '嘿，Sarah。你为什么一瘸一拐的？', NULL, NULL, NULL, 'limp, aches and pains', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Sarah', NULL, 'Oh. Hi Matt. I went snowboarding yesterday and now my whole body aches.', '哦，嗨 Matt。我昨天去滑雪板了，现在全身都疼。', NULL, NULL, NULL, 'snowboarding, whole body aches', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Matt', NULL, 'I remember the first time I went. My back was sore, I couldn''t sit down because it hurt my butt, and I got a cramp in my legs if I walked too fast.', '我记得第一次去时，背很酸，屁股疼得坐不下，走快一点腿还会抽筋。', NULL, NULL, NULL, 'sore, butt, cramp, snowboarding', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Sarah', NULL, 'Ha, that''s exactly how I feel now. And I never want to go again.', '哈，这正是我现在的感觉。我再也不想去了。', NULL, NULL, NULL, 'aches and pains, snowboarding', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Matt', NULL, 'It''s only like that the first couple of times. It''ll be fun after a while.', '只有头几次会这样。过一阵就会觉得好玩了。', NULL, NULL, NULL, 'first couple of times, snowboarding', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Sarah', NULL, 'I''ll think about it after I start feeling better. Right now, I don''t even want to hear the word snowboarding.', '等我感觉好一点再考虑吧。现在我连“滑雪板”这个词都不想听。', NULL, NULL, NULL, 'feeling better, snowboarding', 1),

    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'I''m dying. My whole body is aching.', '我累坏了，全身都在疼。', NULL, '根据课件提示补全。', NULL, 'aching, whole body', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Are you okay? You''re limping. What''s wrong with your legs?', '你还好吗？你一瘸一拐的。腿怎么了？', NULL, NULL, NULL, 'limp, legs, pain', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I went snowboarding yesterday. Now I get a cramp in my legs when I walk, and my back feels sore. Even my butt hurts when I try to sit down.', '我昨天去滑雪板了。现在一走路腿就抽筋，背也酸痛，连想坐下时屁股都会疼。', NULL, NULL, NULL, 'cramp, sore, butt, snowboarding', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'It sounds like you''ve used your muscles too much.', '听起来像是你的肌肉使用过度了。', NULL, NULL, NULL, 'muscles, overuse, exercise', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'I guess so. And you know what? I''ll never go snowboarding again.', '我想是吧。你知道吗？我再也不去玩滑雪板了。', NULL, NULL, NULL, 'snowboarding, aches and pains', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Come on, everyone gets aches from time to time. All you need is enough rest.', '别这样，人人都会偶尔疼痛。你只需要充分休息。', NULL, NULL, NULL, 'aches, rest, health', 1),

    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'When was the last time you had aches and pains? What caused them?', '你最近一次感到疼痛是什么时候？是什么原因造成的？', NULL, '可谈生病时的发烧、感冒或流感；意外跌倒或碰撞；以及爬山、游泳、跑步等运动过量。', NULL, 'aches and pains, health, exercise', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Would you see a doctor when you have aches and pains? What would you do to feel better?', '疼痛时你会去看医生吗？你会怎样让自己好起来？', NULL, '可谈休息、按摩、止痛药、药膏或贴剂；也可以说明何时会去看医生。', NULL, 'doctor, rest, pain relief', 1),

    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'My whole body aches.\nI got (a) cramp in my legs if I walked too fast.', '复习：limp / ache / sore / butt / cramp。', NULL, NULL, NULL, 'review, aches and pains', 1),

    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'backache', 'backache', '背疼', NULL, '课后拓展：常见疼痛词汇。', NULL, 'backache, pain', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'headache', 'headache', '头疼', NULL, '课后拓展：常见疼痛词汇。', NULL, 'headache, pain', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'stomachache', 'stomachache', '胃疼', NULL, '课后拓展：常见疼痛词汇。', NULL, 'stomachache, pain', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'toothache', 'toothache', '牙疼', NULL, '课后拓展：常见疼痛词汇。', NULL, 'toothache, pain', 1),
    ('aches-and-pains', 'Chapter 8 · Health', 'Lesson 67 · Aches and Pains', 67, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'earache', 'earache', '耳朵疼', NULL, '课后拓展：常见疼痛词汇。', NULL, 'earache, pain', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 68 · Medical Check-up (doc/116121_813_Medical Check-up.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'check-up', 'check-up', '体检；健康检查', '/ˈtʃek ʌp/', 'a medical examination to test your general state of health', 'He goes to his doctor for a check-up.', 'check-up, health, doctor', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'at least', 'at least', '至少', '/æt liːst/', 'as much as, or more than, a number or amount', 'You''ll have to wait at least an hour.', 'at least, quantity, time', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'cause', 'cause', '原因；起因', '/kɔːz/', 'the reason why something, especially something bad, happens', 'Smoking is the biggest preventable cause of death and disease.', 'cause, health, disease', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'medicine', 'medicine', '药；药物；药剂', '/ˈmedɪsn/', 'a substance, especially in the form of a liquid or a pill, that is a treatment for illness or injury', 'Take a spoonful of medicine at mealtimes.', 'medicine, treatment, health', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'quit', 'quit', '停止；放弃', '/kwɪt/', 'to stop doing something; when followed by a verb, use its -ing form', 'I''m going to quit smoking. / Quit wasting my time!', 'quit, -ing, health', 1),

    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Mike', NULL, 'Hi, Mr. Smith. I''m Doctor Mike. Why are you here today?', '您好，Smith 先生。我是 Mike 医生。您今天为什么来？', NULL, NULL, NULL, 'doctor, medical check-up', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mr. Smith', NULL, 'I found it would be a good idea to get a medical check-up.', '我觉得做一次体检会是个好主意。', NULL, NULL, NULL, 'medical check-up, health', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Mike', NULL, 'Let me check. Your eyes and ears look fine. Take a breath, please. Do you smoke, Mr. Smith?', '让我检查一下。您的眼睛和耳朵看起来很好。请吸一口气。Smith 先生，您抽烟吗？', NULL, NULL, NULL, 'check-up, smoke, doctor', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mr. Smith', NULL, 'Yes, I just can''t quit smoking.', '是的，我就是戒不了烟。', NULL, NULL, NULL, 'quit smoking, health', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Mike', NULL, 'Smoking is the leading cause of lung cancer and heart disease. We have some medicine that might help. I will give you more information before you leave.', '吸烟是肺癌和心脏病的首要原因。我们有些药物可能有帮助。您离开前我会给您更多信息。', NULL, NULL, NULL, 'smoking, medicine, health', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mr. Smith', NULL, 'Thanks, doctor. I will try to get a check-up at least once a year.', '谢谢您，医生。我会尽量每年至少做一次体检。', NULL, NULL, NULL, 'check-up, at least, yearly', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Mike', NULL, 'You''re welcome.', '不客气。', NULL, NULL, NULL, 'doctor, health', 1),

    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Come in please. Can I help you?', '请进。我能帮您吗？', NULL, '根据课件提示补全。', NULL, 'doctor, check-up', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Thank you, doctor. I''m here for a check-up.', '谢谢您，医生。我来做体检。', NULL, NULL, NULL, 'check-up, doctor', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Okay, let me check. Um, there is something wrong with your eyes. Did you overuse your eyes?', '好的，让我看看。嗯，您的眼睛有点问题。您是不是用眼过度了？', NULL, NULL, NULL, 'eyes, overuse, check-up', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Yes, I just can''t quit using my phone. Usually, I use it at least 10 hours a day.', '是的，我就是戒不掉用手机。通常我每天至少用十小时。', NULL, NULL, NULL, 'quit, phone, at least', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'You really should stop using it too much right now! It''s a common cause for eye diseases. I can give you some medicine to help you.', '您现在确实应该停止过度使用！这是眼部疾病的常见原因。我可以给您一些药帮助您。', NULL, NULL, NULL, 'cause, medicine, eye diseases', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Thank you so much, doctor!', '非常感谢您，医生！', NULL, NULL, NULL, 'doctor, medicine', 1),

    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'How often do you take a medical check-up? Do you think it is necessary?', '你多久做一次体检？你认为有必要吗？', NULL, '可回答至少每年一次、每月一次或从不；可谈体检有用、重要，或觉得无聊、痛苦、浪费时间。', NULL, 'medical check-up, health', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you think a company should provide a free medical check-up for its staff annually? Would it be good or bad for a company?', '你认为公司应该每年为员工提供免费体检吗？这对公司是好事还是坏事？', NULL, '可谈吸引员工、确保员工健康状况和提高忠诚度；也可谈成本高、耗时或不是公司的职责。', NULL, 'company, medical check-up, staff', 1),

    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'It would be a good idea to get a check-up.\nI will try to come at least once a year.', '复习：check-up / cause / quit / medicine / at least。', NULL, NULL, NULL, 'review, medical check-up', 1),

    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'body weight scale', 'body weight scale', '体重秤', NULL, '课后拓展：体检相关用品。', NULL, 'body weight scale, check-up', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'tourniquet', 'tourniquet', '止血带', NULL, '课后拓展：体检相关用品。', NULL, 'tourniquet, check-up', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'iodine', 'iodine', '碘酒', NULL, '课后拓展：体检相关用品。', NULL, 'iodine, check-up', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'cotton swab', 'cotton swab', '棉签', NULL, '课后拓展：体检相关用品。', NULL, 'cotton swab, check-up', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'eye chart', 'eye chart', '视力表', NULL, '课后拓展：体检相关用品。', NULL, 'eye chart, check-up', 1),
    ('medical-check-up', 'Chapter 8 · Health', 'Lesson 68 · Medical Check-up', 68, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'tuning fork', 'tuning fork', '音叉', NULL, '课后拓展：体检相关用品。', NULL, 'tuning fork, check-up', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 69 · Seeing A Doctor (doc/116213_813_Seeing A Doctor.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'nauseous', 'nauseous', '感到恶心的；想呕吐的', '/ˈnɔːʃəs/', 'feeling as if you might vomit', 'Sitting in a car for too long makes me feel nauseous.', 'nauseous, symptoms, health', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'discomfort', 'discomfort', '不适；不安；不舒服', '/dɪsˈkʌmfərt/', 'a feeling of being uncomfortable physically or mentally', 'Steve had some discomfort.', 'discomfort, symptoms, health', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'on and off', 'on and off', '时断时续地；间歇地', '/ɑːn ænd ɔːf/', 'if something happens on and off during a period of time, it happens sometimes', 'I''ve had toothache on and off for a couple of months.', 'on and off, symptoms, time', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'recover', 'recover', '完全恢复健康', '/rɪˈkʌvər/', 'to become completely well again after an illness or injury; commonly used as recover from something', 'It took her a long time to recover from her heart operation.', 'recover, illness, injury', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'allergic', 'allergic', '过敏的', '/əˈlɜːrdʒɪk/', 'if you are allergic to something, you become sick or get a rash when you eat, smell, or touch it; use be allergic to', 'I''m allergic to cats. Nouns: allergy / allergies.', 'allergic, allergy, health', 1),

    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Doctor', NULL, 'Hello. What seems to be the problem?', '你好。看起来有什么问题？', NULL, NULL, NULL, 'doctor, symptoms', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Patient', NULL, 'I feel nauseous and haven''t been able to eat anything all day.', '我感到恶心，一整天都吃不下任何东西。', NULL, NULL, NULL, 'nauseous, symptoms', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Doctor', NULL, 'How long have you felt this way?', '你有这种感觉多久了？', NULL, NULL, NULL, 'symptoms, duration', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Patient', NULL, 'The discomfort has been on and off for a week.', '这种不适断断续续已有一周。', NULL, NULL, NULL, 'discomfort, on and off', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Doctor', NULL, 'Okay, I can give you some medicines to help you. Are you allergic to any medicines?', '好的，我可以给你一些药帮助你。你对任何药物过敏吗？', NULL, NULL, NULL, 'medicine, allergic, doctor', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Patient', NULL, 'No, I don''t have allergies.', '没有，我没有过敏症。', NULL, NULL, NULL, 'allergies, medicine', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Doctor', NULL, 'All right. You can pick up your medicine at the first floor now. You should recover soon.', '好的。现在可以到一楼取药了。你应该很快会恢复。', NULL, NULL, NULL, 'pick up medicine, recover', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Patient', NULL, 'Thank you doctor!', '谢谢您，医生！', NULL, NULL, NULL, 'doctor, medicine', 1),

    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'How are you? You don''t look very well.', '你怎么样？你看起来不太好。', NULL, '根据课件提示补全。', NULL, 'health, doctor', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I just saw a doctor, because I feel a little bit nauseous.', '我刚看过医生，因为我觉得有点恶心。', NULL, NULL, NULL, 'doctor, nauseous', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'How long have you felt this way?', '你这种感觉多久了？', NULL, NULL, NULL, 'symptoms, duration', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'The discomfort has been on and off for two days.', '这种不适断断续续已有两天。', NULL, NULL, NULL, 'discomfort, on and off', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'What did the doctor say about your illness?', '医生怎么说你的病情？', NULL, NULL, NULL, 'doctor, illness', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'She said it is because I''m allergic to some flowers and gave me some medicines.', '她说这是因为我对一些花过敏，并给了我一些药。', NULL, NULL, NULL, 'allergic, flowers, medicine', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'Hope you can recover soon. Give me a call when you''re feeling better. Have a good rest.', '希望你早日恢复。感觉好些时给我打电话。好好休息。', NULL, NULL, NULL, 'recover, rest, health', 1),

    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'When was the last time you saw a doctor? For what reasons? How long did it take for you to recover?', '你上一次看医生是什么时候？因为什么？花了多久恢复？', NULL, '可谈上月、上周或昨天；发烧、骨折、头痛等原因；以及吃药后很快恢复、在家休息一周或住院一个月。', NULL, 'seeing a doctor, recover, health', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you think it is necessary to see a doctor for mild diseases such as a cough or a runny nose? Why?', '你认为轻微疾病，如咳嗽或流鼻涕，有必要看医生吗？为什么？', NULL, '可谈及时关注疾病、减少痛苦、加快恢复或发现其他疾病；也可谈症状不严重、可自然恢复、费用高或害怕医生和针。', NULL, 'mild diseases, doctor, health', 1),

    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'The discomfort has been on and off for a week.\nI feel nauseous and haven''t been able to eat anything all day.', '复习：recover / nauseous / discomfort / allergic / on and off。', NULL, NULL, NULL, 'review, seeing a doctor', 1),

    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Describe how symptoms feel', 'Tell your doctor how your symptoms feel.', '告诉医生你的症状感觉如何。', NULL, '课后拓展：向医生描述症状的方法。', NULL, 'symptoms, doctor', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'State the exact location', 'Explain to or show your doctor the exact location in or on which you are experiencing your symptoms.', '向医生说明或展示出现症状的准确部位。', NULL, '课后拓展：向医生描述症状的方法。', NULL, 'symptoms, location, doctor', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Describe duration and frequency', 'Mention how long you''ve had your symptoms or how frequently you notice symptoms.', '说明症状持续了多久或出现得多频繁。', NULL, '课后拓展：向医生描述症状的方法。', NULL, 'symptoms, duration, frequency', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Mention relief or aggravation', 'Explain what relieves or exacerbates symptoms.', '说明什么能缓解或加剧症状。', NULL, '课后拓展：向医生描述症状的方法。', NULL, 'symptoms, relief, aggravation', 1),
    ('seeing-a-doctor', 'Chapter 8 · Health', 'Lesson 69 · Seeing A Doctor', 69, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'Mention shared symptoms', 'Let your doctor know if anyone else is experiencing the same symptoms.', '告诉医生是否还有其他人出现相同症状。', NULL, '课后拓展：向医生描述症状的方法。', NULL, 'symptoms, doctor, health', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 70 · At the Drugstore (doc/116218_813_At the Drugstore.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'pill', 'pill', '药片', '/pɪl/', 'a small flat round piece of medicine that you swallow without chewing it', 'Take three pills daily after meals. Related forms: tablet; capsule.', 'pill, medicine, drugstore', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'treatment', 'treatment', '治疗手段；疗法', '/ˈtriːtmənt/', 'something that is done to cure an illness or injury', 'There are many treatments available for this illness.', 'treatment, illness, health', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'symptom', 'symptom', '症状', '/ˈsɪmptəm/', 'a change in your body or mind that shows that you are not healthy', 'Symptoms include a headache and sore throat.', 'symptom, illness, health', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'prescription', 'prescription', '处方', '/prɪˈskrɪpʃn/', 'an official paper on which a doctor writes the medicine you should have, enabling you to get it from a drugstore', 'They are not available without a prescription.', 'prescription, medicine, drugstore', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'suffer from', 'suffer (from ...)', '饱受……之苦', '/ˈsʌfər/', 'to be badly affected by a disease, pain, sadness, a lack of something, or similar trouble', 'Many people are suffering from the flu. Companies are suffering from a lack of employees.', 'suffer from, illness, health', 1),

    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Ginny', NULL, 'What can I do for you?', '我能为您做什么？', NULL, NULL, NULL, 'drugstore, medicine', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'dialogue', '示范对话', 2, 'dialogue', 102, 'James', NULL, 'I need some medicine for my brother. He suffers from a bad cold.', '我需要给我弟弟买些药。他得了重感冒。', NULL, NULL, NULL, 'medicine, suffer from, cold', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Ginny', NULL, 'What symptoms does he have?', '他有什么症状？', NULL, NULL, NULL, 'symptoms, drugstore', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'dialogue', '示范对话', 2, 'dialogue', 104, 'James', NULL, 'Fever, a bad cough, and a backache.', '发烧、严重咳嗽和背疼。', NULL, NULL, NULL, 'fever, cough, backache', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Ginny', NULL, 'Okay. Let me see if we have anything for him ...', '好的。让我看看有没有适合他的药……', NULL, NULL, NULL, 'medicine, drugstore', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'dialogue', '示范对话', 2, 'dialogue', 106, 'James', NULL, 'Do you have Penicillin (盘尼西林/青霉素)? I think that will do for him.', '你们有盘尼西林（青霉素）吗？我觉得那个适合他。', NULL, NULL, NULL, 'penicillin, medicine', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Ginny', NULL, 'I''m sorry, but you can''t get Penicillin without a prescription. You may have these pills instead. They are effective treatments for a common cold.', '很抱歉，没有处方不能买青霉素。你可以改用这些药片。它们是治疗普通感冒的有效方法。', NULL, NULL, NULL, 'prescription, pills, treatment', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'dialogue', '示范对话', 2, 'dialogue', 108, 'James', NULL, 'Oh, I see. Thank you very much.', '哦，我明白了。非常感谢。', NULL, NULL, NULL, 'drugstore, medicine', 1),

    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Excuse me, I want some medicines for the common cold.', '打扰一下，我想买些治普通感冒的药。', NULL, '根据课件提示补全。', NULL, 'medicine, cold, drugstore', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'For yourself, yeah? What symptoms do you have?', '是给自己买的吗？你有什么症状？', NULL, NULL, NULL, 'symptoms, drugstore', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I suffer from a headache and sore throat.', '我头疼、嗓子疼。', NULL, NULL, NULL, 'suffer from, headache, sore throat', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'These pills will do then. Take six every day - two after each meal.', '那这些药片就可以。每天吃六片，每餐后两片。', NULL, NULL, NULL, 'pills, medicine, dosage', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Thank you. By the way, can I have some Penicillin?', '谢谢。顺便问一下，我可以买些青霉素吗？', NULL, NULL, NULL, 'penicillin, prescription', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Sorry but you can''t get Penicillin without a prescription. You''d better have some OTC (Over-the-counter) medicine instead.', '抱歉，没有处方不能买青霉素。你最好改用一些非处方药。', NULL, NULL, NULL, 'prescription, OTC, medicine', 1),

    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'When was the last time you went to a drugstore? How far was it from you? What medicine were you looking for? Describe in detail.', '你上一次去药房是什么时候？离你多远？你想买什么药？请详细描述。', NULL, '可谈药房在家旁边、几个街区外或很远；以及寻找的非处方药或处方药。', NULL, 'drugstore, medicine, OTC, prescription', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you have a medication box at home? Why or why not? What medicines or treatments should it contain?', '你家里有药箱吗？为什么有或没有？你认为里面应该有什么药物或治疗用品？', NULL, '可谈应急需要、可以随时去药房，以及感冒、咳嗽、发烧、疼痛药物、创可贴和棉球等。', NULL, 'medication box, medicine, emergency', 1),

    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'What symptoms does he have?\nYou can''t get Penicillin without a prescription.', '复习：suffer from / prescription / symptom / pill / treatment。', NULL, NULL, NULL, 'review, drugstore', 1),

    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'OTC medicines', 'Over-the-counter medicine is also known as OTC or nonprescription medicine. It can be bought without a prescription and is safe and effective when used as directed.', '非处方药又称 OTC，可以无需处方购买；按标签和医护人员指示使用时安全有效。', NULL, '课后拓展：OTC 与 Rx 药物。', NULL, 'OTC, nonprescription medicine, drugstore', 1),
    ('at-the-drugstore', 'Chapter 8 · Health', 'Lesson 70 · At the Drugstore', 70, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Rx medicines', 'A prescription medicine legally requires a medical prescription to be sold. Rx is a short form for prescription medicine, from the Latin word recipe, meaning take.', '处方药依法需要医疗处方才能出售；Rx 是 prescription medicine 的简称，源自拉丁语 recipe，意为“取用”。', NULL, '课后拓展：OTC 与 Rx 药物。', NULL, 'Rx, prescription medicine, drugstore', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

COMMIT;
