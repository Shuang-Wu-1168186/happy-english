-- Extracted from the next ten available PDFs in doc/, ordered by source file identifier.
-- Sources: Learn & Talk I, Chapter 9 Lessons 83-84 and Chapter 10 Lessons 87-94.
-- Source PDFs for Lessons 85 and 86 were unavailable during this import.
-- The target table is created by aliyun_daily_spoken_dialogue_buying_clothes.sql.
-- Re-running this file updates only the lesson_code/item_order pairs below.

SET NAMES utf8mb4;
START TRANSACTION;

-- Lesson 83 · Giving Suggestions (doc/116494_814_Giving Suggestions.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'give someone a hand', 'give someone a hand', '帮助某人', NULL, 'to help someone with something that needs a lot of effort', 'He gives her a hand.', 'give a hand, help, suggestions', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'essential', 'essential', '必要的；极其重要的', '/ɪˈsenʃl/', 'completely necessary; extremely important in a particular situation or for a particular activity', 'The museum is closed while essential repairs are being carried out.', 'essential, report, suggestions', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'definitely', 'definitely', '肯定；当然', '/ˈdefɪnətli/', 'used to emphasize that something is true and there is no doubt about it', 'I definitely remember sending the letter.', 'definitely, certainty, suggestions', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'eye-catching', 'eye-catching', '引人注目的', '/ˈaɪ kætʃɪŋ/', 'immediately noticeable because it is particularly interesting, bright, or attractive', 'This is an eye-catching scene.', 'eye-catching, presentation, suggestions', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'work on', 'work on', '改善；努力做', '/wɜːrk ɑːn/', 'to try hard to improve or achieve something', 'He needs to work on his diet to get rid of the junk food.', 'work on, improvement, suggestions', 1),

    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'Could you give me a hand with this report?', '你能帮我处理这份报告吗？', NULL, NULL, NULL, 'give a hand, report, help', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'Sure. I''d be happy to give you some hints and advice.', '当然。我很乐意给你一些提示和建议。', NULL, NULL, NULL, 'hints, advice, suggestions', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'Thanks. Would you mind taking a look at the content?', '谢谢。你介意看一下内容吗？', NULL, NULL, NULL, 'take a look, content, report', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'I think you''ve included all the essential things. You might want to make the conclusion a little longer. Restate your reasons clearly.', '我认为你已经包含了所有必要内容。你可以把结论写得长一点，清楚地重述你的理由。', NULL, NULL, NULL, 'essential, conclusion, report', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'Is it okay to include the picture?', '可以加图片吗？', NULL, NULL, NULL, 'picture, report, suggestions', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'Definitely! I would include one or two on each page if possible. Remember that you should make the report as eye-catching as possible.', '当然！如果可以，我会每页放一两张。记住，你应该让报告尽可能吸引人。', NULL, NULL, NULL, 'definitely, eye-catching, report', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'Thanks for those ideas. I''ll get to work on them right away.', '谢谢这些想法。我马上着手改进。', NULL, NULL, NULL, 'work on, suggestions, report', 1),

    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Could you give me a hand with the speech?', '你能帮我准备演讲吗？', NULL, '根据课件提示补全。', NULL, 'give a hand, speech, suggestions', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Definitely. We are good friends.', '当然。我们是好朋友。', NULL, NULL, NULL, 'definitely, friendship, help', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Would you mind taking a look at the content?', '你介意看一下内容吗？', NULL, NULL, NULL, 'content, speech, suggestions', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'I think you''ve included all the essential things. However, I think it''s not eye-catching enough, and the audience may get bored.', '我认为你已经包含了所有必要内容。不过，我觉得它还不够吸引人，观众可能会觉得无聊。', NULL, NULL, NULL, 'essential, eye-catching, audience', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Thanks for your advice. I will work on that.', '谢谢你的建议。我会努力改进。', NULL, NULL, NULL, 'advice, work on, suggestions', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'You''re welcome.', '不客气。', NULL, NULL, NULL, 'suggestions, help', 1),

    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'When you have problems, do you prefer to solve them by yourself or ask for help from others? Why?', '遇到问题时，你更喜欢自己解决还是向别人求助？为什么？', NULL, '可谈独立解决问题、不打扰别人；或求助可以节省时间、获得他人的建议。', NULL, 'problems, help, suggestions', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Suppose your friend has a bad habit and you have suggestions. If sharing them may ruin your friendship, what will you do? Why?', '假如朋友有坏习惯而你有建议，但说出来可能破坏友谊，你会怎么做？为什么？', NULL, '可谈告诉朋友，因为朋友会理解并相信友谊；或不说，以尊重习惯并避免破坏友谊。', NULL, 'suggestions, friendship, bad habit', 1),

    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Could you give me a hand with this report?\nI''d be happy to give you some hints and advice.\nWould you mind taking a look at the content?\nI''ll get to work on them right away.', '复习：give somebody a hand / essential / definitely / eye-catching / work on。', NULL, NULL, NULL, 'review, giving suggestions', 1),

    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Take a second', 'Take a second.', '等一下，冷静一下。', NULL, '课后拓展：给建议时可用的表达。', NULL, 'suggestions, phrase', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Put my two cents in', 'Can I put my two cents in?', '我能说两句吗？我能提供一下自己的观点吗？', NULL, '课后拓展：给建议时可用的表达。', NULL, 'suggestions, opinion, phrase', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Do not count your chickens before they hatch', 'Don''t count your chickens before they''ve hatched.', '别高兴得太早。', NULL, '课后拓展：给建议时可用的表达。', NULL, 'suggestions, proverb, phrase', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Do not bite off more than you can chew', 'Don''t bite off more than you can chew.', '贪多嚼不烂。', NULL, '课后拓展：给建议时可用的表达。', NULL, 'suggestions, proverb, phrase', 1),
    ('giving-suggestions', 'Chapter 9 · Socializing', 'Lesson 83 · Giving Suggestions', 83, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'Rome was not built in a day', 'Rome wasn''t built in a day.', '罗马不是一天建成的。', NULL, '课后拓展：给建议时可用的表达。', NULL, 'suggestions, proverb, phrase', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 84 · Body Language (doc/116501_814_Body Language.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'impressive', 'impressive', '给人留下深刻印象的', '/ɪmˈpresɪv/', 'making you feel admiration because someone or something is very large, good, skillful, or similar', 'He was very impressive in the interview.', 'impressive, interview, body language', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'make eye contact with', 'make eye contact with', '与……眼神接触', NULL, 'the situation in which two people look at each other''s eyes at the same time', 'They are making eye contact with each other.', 'eye contact, body language, communication', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'slouch', 'slouch', '低头垂肩地站、坐或走；驼背', '/slaʊtʃ/', 'to stand, sit, or move in a lazy way, often with your shoulders and head bent forward', 'Sit up straight. Don''t slouch.', 'slouch, posture, body language', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'posture', 'posture', '姿态；体态', '/ˈpɑːstʃər/', 'the position in which you hold your body when standing or sitting', 'Good posture is essential when reading books.', 'posture, body language, confidence', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'body language', 'body language', '肢体语言', '/ˈbɑːdi læŋɡwɪdʒ/', 'communicating what you feel or think by the way you place and move your body rather than by words', 'You can tell from a person''s body language.', 'body language, communication, posture', 1),

    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'Well, what did you think of the last candidate? Do you think we should hire her?', '那么，你觉得上一位候选人怎么样？我们该雇用她吗？', NULL, NULL, NULL, 'candidate, interview, body language', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'She has a very impressive resume, but she seemed to lack confidence.', '她的简历很令人印象深刻，但她似乎缺乏自信。', NULL, NULL, NULL, 'impressive, resume, confidence', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'What made you think that she wasn''t very confident?', '什么让你觉得她不太自信？', NULL, NULL, NULL, 'confidence, interview', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'Did you notice the way that she avoided making eye contact with us while she talked?', '你有没有注意到她说话时避免和我们有眼神接触？', NULL, NULL, NULL, 'eye contact, body language', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'I guess she was a bit nervous. What else?', '我想她有点紧张。还有什么？', NULL, NULL, NULL, 'nervous, interview', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'Did you also notice the way she slouched in her chair during most of the interview? She had horrible posture!', '你还注意到她在面试的大部分时间里都驼背坐在椅子上吗？她的姿势糟透了！', NULL, NULL, NULL, 'slouch, posture, interview', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'I agree. I guess I was paying more attention to her answers than her body language.', '我同意。我想我更关注她的回答，而不是她的肢体语言。', NULL, NULL, NULL, 'body language, interview, answers', 1),

    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Have you ever noticed your body language?', '你注意过自己的肢体语言吗？', NULL, '根据课件提示补全。', NULL, 'body language, communication', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'What do you mean by that?', '你是什么意思？', NULL, NULL, NULL, 'body language, communication', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'When you are talking with someone, you don''t like to make eye contact, and it looks like you are not listening.', '当你和人交谈时，你不喜欢眼神接触，看起来像没有在听。', NULL, NULL, NULL, 'make eye contact, listening', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'That''s not true. I''m just afraid to look directly at someone''s eyes. I''ll work on that.', '不是这样。我只是害怕直视别人的眼睛。我会努力改进。', NULL, NULL, NULL, 'eye contact, work on, confidence', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Besides, you need to mind your posture. You slouch when you are walking and sitting, and it really doesn''t look good.', '另外，你需要注意姿势。你走路和坐着时都驼背，看起来真的不好。', NULL, NULL, NULL, 'posture, slouch, body language', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Thanks for your advice.', '谢谢你的建议。', NULL, NULL, NULL, 'advice, body language', 1),

    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you make eye contact with other people when talking? Why do or do not you make eye contact?', '交谈时你会和别人有眼神接触吗？为什么会或不会？', NULL, '可谈用眼神接触表示在倾听、显得自信；也可谈害羞、害怕或尴尬。', NULL, 'eye contact, body language, communication', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Some people think body language is more authentic than words. Do you believe this idea? Give your reasons.', '有些人认为肢体语言比语言更真实。你相信这个观点吗？请说明理由。', NULL, '可谈交谈时很少有人注意肢体语言、肢体语言总会说真话；也可谈不一定能清楚观察和理解肢体语言，人仍可能用肢体语言撒谎。', NULL, 'body language, authenticity, communication', 1),

    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Did you notice the way that she avoided making eye contact with us while she talked?\nDid you also notice the way she slouched in her chair during most of the interview? She had horrible posture!', '复习：impressive / make eye contact with / slouch / posture / body language。', NULL, NULL, NULL, 'review, body language', 1),

    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Eye contact', 'If you want your body language to show you are listening to another person, make eye contact and then slightly glance away.', '眼神接触：若想用肢体语言表明自己在倾听，可先眼神接触，再稍微移开目光。', NULL, '课后拓展：常见肢体语言含义。', NULL, 'eye contact, body language', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Crossed arms', 'Others may read crossed arms as meaning that you are distant, insecure, anxious, defensive, or stubborn.', '双臂交叉：别人可能解读为疏离、缺乏安全感、焦虑、防御或固执。', NULL, '课后拓展：常见肢体语言含义。', NULL, 'crossed arms, body language', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Sitting with legs spread', 'Sitting with legs spread can be read as marking your territory; people with power are seen to take up more space.', '双腿岔开坐：可能被解读为在标记领地；有权力的人往往占用更多空间。', NULL, '课后拓展：常见肢体语言含义。', NULL, 'legs spread, body language', 1),
    ('body-language', 'Chapter 9 · Socializing', 'Lesson 84 · Body Language', 84, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Crossed legs', 'Crossed legs can signal confidence and dominance. Crossing the legs at the ankles, known as an ankle lock, can mean holding back, uncertainty, or fear.', '双腿交叉：可能表示自信和支配感；脚踝交叉（ankle lock）可能表示克制、不确定或害怕。', NULL, '课后拓展：常见肢体语言含义。', NULL, 'crossed legs, body language, ankle lock', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 87 · April Fool's Day (doc/116586_4651_April Fool's Day.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'prank', 'prank', '恶作剧', '/præŋk/', 'a trick that is played on somebody as a joke', 'I''ve had enough of your childish pranks.', 'prank, April Fool''s Day, holiday', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'gullible', 'gullible', '容易上当的', '/ˈɡʌləbl/', 'too willing to believe or accept what other people tell you and therefore easily tricked', 'The advertisement is aimed at gullible young women worried about their weight.', 'gullible, prank, April Fool''s Day', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'hoax', 'hoax', '恶作剧；骗局；谣言', '/hoʊks/', 'a trick or plan to deceive someone by making them believe something that is not true; compared with prank, hoax emphasizes deception more', 'The emergency call turned out to be a hoax.', 'hoax, prank, April Fool''s Day', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'make a fool of', 'make a fool of', '愚弄', '/meɪk ə fuːl əv/', 'to trick someone or make someone appear stupid in some way', 'He sent me a gift to make a fool of me.', 'make a fool of, prank, April Fool''s Day', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'lighten up', 'lighten up', '使放松；使缓和', '/ˈlaɪtn ʌp/', 'to make something more relaxed and less serious', 'His jokes really lightened up the whole day.', 'lighten up, joke, April Fool''s Day', 1),

    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'Hi, Mary, what''s up?', '嗨，Mary，怎么了？', NULL, NULL, NULL, 'April Fool''s Day, greeting', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'I''m a little scared today. Today is April Fool''s Day. I''m afraid somebody will pull a prank on me.', '我今天有点害怕。今天是愚人节。我担心有人会对我恶作剧。', NULL, NULL, NULL, 'April Fool''s Day, prank', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'Did that happen a lot when you were a kid?', '你小时候这种事经常发生吗？', NULL, NULL, NULL, 'prank, childhood', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'Yes, I was always so gullible and believed everything I heard.', '是的，我以前总是很容易上当，什么都相信。', NULL, NULL, NULL, 'gullible, prank', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'Me too. When I was a kid, some other kids told me something was true, and it turned out to be a hoax. Therefore, they made a fool of me.', '我也是。小时候，一些孩子告诉我某件事是真的，结果那是个骗局，因此他们愚弄了我。', NULL, NULL, NULL, 'hoax, make a fool of, childhood', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'It''s funny. I never know what is real and what is fake on April Fool''s Day.', '这很有趣。在愚人节，我永远不知道什么是真的，什么是假的。', NULL, NULL, NULL, 'April Fool''s Day, real, fake', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'But sometimes the jokes could really lighten up the whole day.', '但有时玩笑真的能让一整天轻松起来。', NULL, NULL, NULL, 'lighten up, jokes, April Fool''s Day', 1),

    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'I''m so angry. John pulled a prank on me.', '我太生气了。John 对我恶作剧。', NULL, '根据课件提示补全。', NULL, 'prank, April Fool''s Day', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'What did he do?', '他做了什么？', NULL, NULL, NULL, 'prank, question', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'He told me we would have a test today, but it turned out to be a hoax. I can''t believe I''m so gullible.', '他告诉我今天要考试，但结果是骗局。我不敢相信自己这么容易上当。', NULL, NULL, NULL, 'hoax, gullible, prank', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'That''s not your fault. He really likes to make a fool of other people.', '这不是你的错。他真的喜欢愚弄别人。', NULL, NULL, NULL, 'make a fool of, prank', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Thank you. You have lightened up my life.', '谢谢。你让我的生活轻松了些。', NULL, NULL, NULL, 'lighten up, friendship', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'You''re welcome.', '不客气。', NULL, NULL, NULL, 'friendship, April Fool''s Day', 1),

    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'When is April Fool''s Day? What do people do on April Fool''s Day? Do you have any prank to pull?', '愚人节是什么时候？人们会做什么？你有想玩的恶作剧吗？', NULL, '可谈拉恶作剧、开玩笑或愚弄别人。', NULL, 'April Fool''s Day, prank, holiday', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Have you ever been fooled on April Fool''s Day? How would you feel if your dearest friends fooled you?', '你在愚人节被愚弄过吗？如果最亲近的朋友愚弄你，你会有什么感受？', NULL, '可谈觉得好笑、和朋友聊自己有多傻；也可谈觉得受辱、生气或结束友谊。', NULL, 'April Fool''s Day, friendship, feelings', 1),

    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I''m afraid somebody will pull a prank on me.\nI''m always so gullible and believe everything.\nThe jokes really lighten up the whole day.', '复习：prank / gullible / hoax / make a fool of / lighten up。', NULL, NULL, NULL, 'review, April Fool''s Day', 1),

    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Swap sugar and salt', 'Swap sugar and salt.', '把糖和盐调换。', NULL, '课后拓展：愚人节玩笑示例。', NULL, 'prank, April Fool''s Day', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Power down the remote', 'Power down the remote control.', '关掉遥控器电源。', NULL, '课后拓展：愚人节玩笑示例。', NULL, 'prank, April Fool''s Day', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Turn everything upside down', 'Turn everything upside down.', '把所有东西倒过来。', NULL, '课后拓展：愚人节玩笑示例。', NULL, 'prank, April Fool''s Day', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Change a phone language setting', 'Borrow a friend''s cellphone and change the language setting to a foreign language that the friend does not know.', '借朋友的手机，把语言设置改成对方不懂的外语。', NULL, '课后拓展：愚人节玩笑示例。', NULL, 'prank, phone, April Fool''s Day', 1),
    ('april-fools-day', 'Chapter 10 · Holidays', 'Lesson 87 · April Fool''s Day', 87, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'Replace Oreo filling', 'Replace Oreo cream filling with toothpaste and offer one to a friend.', '把奥利奥夹心替换成牙膏，再给朋友一块。', NULL, '课后拓展：愚人节玩笑示例。', NULL, 'prank, April Fool''s Day, Oreo', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 88 · Thanksgiving Day (doc/116604_4651_Thanksgiving Day.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'gratitude', 'gratitude', '感谢', '/ˈɡrætɪtuːd/', 'the feeling of being grateful and wanting to express your thanks', 'He sent a card to express his gratitude.', 'gratitude, Thanksgiving, holiday', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'harvest', 'harvest', '收获；收成', '/ˈhɑːrvɪst/', 'the time of year when crops are gathered in, or the act of cutting and gathering crops', 'Farmers are extremely busy during harvest season.', 'harvest, Thanksgiving, holiday', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'turkey', 'turkey', '火鸡；火鸡肉', '/ˈtɜːrki/', 'a large bird kept for its meat, eaten especially at Christmas in the UK and at Thanksgiving in the US', 'We raise turkeys mainly for the meat.', 'turkey, Thanksgiving, food', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'tasty', 'tasty', '美味的', '/ˈteɪsti/', 'having a strong and pleasant flavor', 'The pumpkin pie is very tasty.', 'tasty, Thanksgiving, food', 1),

    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'What is the typical Thanksgiving like in your opinion?', '在你看来，典型的感恩节是什么样的？', NULL, NULL, NULL, 'Thanksgiving, holiday', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'Thanksgiving is all about family. Family traditions include staying at home and cooking a big meal together.', '感恩节就是关于家庭。家庭传统包括待在家里，一起做一顿大餐。', NULL, NULL, NULL, 'Thanksgiving, family, meal', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'Thanksgiving is also a time to express gratitude for the harvest and things in general. What do people usually have on Thanksgiving?', '感恩节也是为收获和生活中的一切表达感激的时候。人们感恩节通常吃什么？', NULL, NULL, NULL, 'gratitude, harvest, Thanksgiving', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'A roast turkey is essential. It is usually stuffed with bread and vegetables to absorb the tasty juices. There are many other delicious dishes to celebrate this festival, such as sweet potato and pumpkin pie.', '烤火鸡是必不可少的。它通常会塞入面包和蔬菜以吸收美味的汁水。还有许多其他美食庆祝节日，例如红薯和南瓜派。', NULL, NULL, NULL, 'turkey, tasty, Thanksgiving food', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'That sounds delicious.', '听起来很美味。', NULL, NULL, NULL, 'Thanksgiving, food', 1),

    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Do you know anything about Thanksgiving Day?', '你了解感恩节吗？', NULL, '根据课件提示补全。', NULL, 'Thanksgiving, holiday', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes, I have an American friend, and he once invited me to his family on Thanksgiving.', '是的，我有一位美国朋友，他曾在感恩节邀请我去他家。', NULL, NULL, NULL, 'Thanksgiving, family, American', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Tell me about it. What did you do?', '给我讲讲。你们做了什么？', NULL, NULL, NULL, 'Thanksgiving, conversation', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'We had a great meal. The main dish was a turkey, and we had a big and tasty turkey.', '我们吃了一顿很棒的饭。主菜是一只火鸡，我们吃了一只又大又美味的火鸡。', NULL, NULL, NULL, 'turkey, tasty, Thanksgiving', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Why do they celebrate Thanksgiving Day?', '他们为什么庆祝感恩节？', NULL, NULL, NULL, 'Thanksgiving, holiday', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'They want to express gratitude for the harvest and other things in general.', '他们想为收获和生活中的其他事情表达感激。', NULL, NULL, NULL, 'gratitude, harvest, Thanksgiving', 1),

    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you ever celebrated Thanksgiving Day? Do you know what people do on Thanksgiving Day?', '你庆祝过感恩节吗？你知道人们在感恩节做什么吗？', NULL, '可谈吃包括火鸡、红薯和南瓜派的大餐，看美式橄榄球或游行。', NULL, 'Thanksgiving, holiday, food', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Suppose you are celebrating Thanksgiving. What will you say to your family?', '假如你在庆祝感恩节，你会对家人说什么？', NULL, '可谈感谢家人的帮助、为自己所做的一切、在难过时让自己开心、给有用建议等。', NULL, 'gratitude, family, Thanksgiving', 1),

    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'It is a time to give thanks for the harvest and express gratitude in general.\nIt is usually stuffed with bread and vegetables to absorb the tasty juices.', '复习：harvest / gratitude / tasty / turkey。', NULL, NULL, NULL, 'review, Thanksgiving', 1),

    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'leaf', 'leaf', '叶子', NULL, '课后拓展：感恩节相关词汇。', NULL, 'Thanksgiving, leaf', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'pumpkin pie', 'pumpkin pie', '南瓜派', NULL, '课后拓展：感恩节相关词汇。', NULL, 'Thanksgiving, pumpkin pie', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'tendril', 'tendril', '植物的卷须', NULL, '课后拓展：感恩节相关词汇。', NULL, 'Thanksgiving, tendril', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'sweet potato fries', 'sweet potato fries', '红薯条；番薯条', NULL, '课后拓展：感恩节相关词汇。', NULL, 'Thanksgiving, sweet potato', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'corn', 'corn', '玉米', NULL, '课后拓展：感恩节相关词汇。', NULL, 'Thanksgiving, corn', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'twig', 'twig', '细枝条', NULL, '课后拓展：感恩节相关词汇。', NULL, 'Thanksgiving, twig', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'extra', '拓展学习', 6, 'extra', 507, NULL, 'cherry pie', 'cherry pie', '樱桃派', NULL, '课后拓展：感恩节相关词汇。', NULL, 'Thanksgiving, cherry pie', 1),
    ('thanksgiving-day', 'Chapter 10 · Holidays', 'Lesson 88 · Thanksgiving Day', 88, 'extra', '拓展学习', 6, 'extra', 508, NULL, 'cranberry sauce', 'cranberry sauce', '蔓越莓果酱', NULL, '课后拓展：感恩节相关词汇。', NULL, 'Thanksgiving, cranberry sauce', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 89 · Halloween (doc/116612_4651_Halloween.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'dress up', 'dress up', '装扮', '/dres ʌp/', 'to put on special clothes, especially to pretend to be somebody or something different', 'The boy dressed up as a pirate.', 'dress up, Halloween, costume', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'costume', 'costume', '化妆服', '/ˈkɑːstuːm/', 'a set of clothes worn to look like someone or something else, especially for a party or entertainment', 'They were dressed in Halloween costumes.', 'costume, Halloween, dress up', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'decorate', 'decorate', '装饰', '/ˈdekəreɪt/', 'to make something look more attractive by putting things on it; use decorate with', 'They decorated the house with balloons.', 'decorate, Halloween, house', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'spooky', 'spooky', '怪异的；诡异的', '/ˈspuːki/', 'strange and frightening', 'This is a spooky forest.', 'spooky, Halloween, costume', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'get under one''s skin', 'get under one''s skin', '激怒某人', NULL, 'to annoy somebody', 'Don''t get under my skin!', 'get under one''s skin, Halloween, annoyance', 1),

    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'What do you think about Halloween?', '你怎么看万圣节？', NULL, NULL, NULL, 'Halloween, holiday', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'I actually like it. It''s a fun holiday for kids especially, because you get to dress up in costumes and get lots of candy when going trick-or-treating.', '我其实喜欢它。它尤其是孩子们的有趣节日，因为可以穿着化妆服装扮，玩“不给糖就捣蛋”时还能得到很多糖果。', NULL, NULL, NULL, 'Halloween, dress up, costumes', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'What were you on Halloween?', '你万圣节装扮成什么？', NULL, NULL, NULL, 'Halloween, costume', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'Last year, I dressed up as a ghost to a party. How about you?', '去年我装扮成幽灵去参加聚会。你呢？', NULL, NULL, NULL, 'dress up, ghost, Halloween', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'When I was a kid, my parents always decorated our house with spooky things. I dressed up as Batman because I wanted to look like a hero.', '我小时候，父母总用怪异的东西装饰房子。我装扮成蝙蝠侠，因为我想像英雄。', NULL, NULL, NULL, 'decorate, spooky, Batman', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'That''s great. When I was a kid, some of my classmates liked to pull a prank on me on Halloween, and it really got under my skin.', '那很棒。我小时候，一些同学喜欢在万圣节对我恶作剧，这真的让我很生气。', NULL, NULL, NULL, 'prank, get under one''s skin, Halloween', 1),

    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Do you have plans for Halloween?', '你有万圣节计划吗？', NULL, '根据课件提示补全。', NULL, 'Halloween, plans', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes, I will dress up as a ghost. What about you?', '有，我会装扮成幽灵。你呢？', NULL, NULL, NULL, 'dress up, ghost, Halloween', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'First, I will help my parents to decorate the house, and they want to make it spooky.', '首先，我会帮父母装饰房子，他们想让它很诡异。', NULL, NULL, NULL, 'decorate, spooky, Halloween', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'That''s interesting. What about your costume?', '这很有趣。你的化妆服呢？', NULL, NULL, NULL, 'costume, Halloween', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'I haven''t decided yet … Batman or Superman.', '我还没决定……蝙蝠侠还是超人。', NULL, NULL, NULL, 'costume, Batman, Superman', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'You''d better make a quick decision. There are only two days left.', '你最好快点决定。只剩两天了。', NULL, NULL, NULL, 'Halloween, decision', 1),

    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'What do you know about Halloween? What do people do on Halloween?', '你了解万圣节什么？人们在万圣节做什么？', NULL, '可谈穿化妆服、雕刻南瓜、玩“不给糖就捣蛋”、装饰房子。', NULL, 'Halloween, holiday, costumes', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Have you ever celebrated Halloween? Do you think it is worth spending much time and money on Halloween costumes? Why?', '你庆祝过万圣节吗？你认为值得花很多时间和金钱在万圣节化妆服上吗？为什么？', NULL, '可谈和家人与朋友共度欢乐时光、设计自己的服装、了解美国文化；也可谈服装通常只用一次、浪费时间和钱。', NULL, 'Halloween, costumes, holiday', 1),

    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'It''s a fun holiday for kids especially, because you get to dress up in costumes and get lots of candy when going trick-or-treating.\nMy parents always decorated our house with spooky things.', '复习：dress up / costume / decorate / spooky / get under one''s skin。', NULL, NULL, NULL, 'review, Halloween', 1),

    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'ghost', 'ghost', '幽灵', NULL, '课后拓展：万圣节相关词汇。', NULL, 'Halloween, ghost', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'witch', 'witch', '女巫', NULL, '课后拓展：万圣节相关词汇。', NULL, 'Halloween, witch', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'skeleton', 'skeleton', '骷髅', NULL, '课后拓展：万圣节相关词汇。', NULL, 'Halloween, skeleton', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Jack-o''-lantern', 'Jack-o''-lantern', '南瓜灯', NULL, '课后拓展：万圣节相关词汇。', NULL, 'Halloween, jack-o''-lantern', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'werewolf', 'werewolf', '狼人', NULL, '课后拓展：万圣节相关词汇。', NULL, 'Halloween, werewolf', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'owl', 'owl', '猫头鹰', NULL, '课后拓展：万圣节相关词汇。', NULL, 'Halloween, owl', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'extra', '拓展学习', 6, 'extra', 507, NULL, 'bat', 'bat', '蝙蝠', NULL, '课后拓展：万圣节相关词汇。', NULL, 'Halloween, bat', 1),
    ('halloween', 'Chapter 10 · Holidays', 'Lesson 89 · Halloween', 89, 'extra', '拓展学习', 6, 'extra', 508, NULL, 'cross', 'cross', '十字架', NULL, '课后拓展：万圣节相关词汇。', NULL, 'Halloween, cross', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 90 · Christmas (doc/116664_4651_Christmas.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'date back to', 'date back to', '追溯到', '/deɪt bæk tu/', 'to have existed since a particular time in the past or for the length of time mentioned', 'The college dates back to medieval times.', 'date back to, Christmas, tradition', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'ornament', 'ornament', '装饰品', '/ˈɔːrnəmənt/', 'an object used as decoration in a room, garden, or similar place rather than for a particular purpose', 'There were a few china ornaments on the shelf above the fireplace.', 'ornament, Christmas, tree', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'chimney', 'chimney', '烟囱', '/ˈtʃɪmni/', 'a structure through which smoke or steam is carried away from a fire and through a building roof', 'He threw a bit of paper onto the fire and it flew up the chimney.', 'chimney, Christmas, house', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'Santa Claus', 'Santa Claus', '圣诞老人', '/ˈsæntə klɔːz/', 'an imaginary old man in red clothes with a long white beard who, parents tell children, brings presents at Christmas', 'Go to sleep quickly or Santa Claus won''t come!', 'Santa Claus, Christmas, presents', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'prominent', 'prominent', '显眼的', '/ˈprɑːmɪnənt/', 'easily seen', 'The presents are prominent next to the tree.', 'prominent, Christmas, presents', 1),

    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'Your Christmas tree looks beautiful. Do you decorate it this way every year?', '你的圣诞树看起来很漂亮。你每年都这样装饰吗？', NULL, NULL, NULL, 'Christmas tree, decorate', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'Yes, it''s a family tradition dating back to my childhood. We use the same lights and ornaments, but of course we have a new tree each year. We also place these stockings next to the chimney. The children wish that Santa Claus would come.', '是的，这是可追溯到我童年的家庭传统。我们用同样的灯和装饰品，当然每年都有一棵新树。我们还把袜子放在烟囱旁。孩子们希望圣诞老人会来。', NULL, NULL, NULL, 'date back to, ornaments, chimney, Santa Claus', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'Well, everything seems to be just about ready. Do you exchange presents in the morning?', '一切看起来都快准备好了。你们早上交换礼物吗？', NULL, NULL, NULL, 'presents, Christmas morning', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'Oh, yes. We all put presents in the prominent place next to the tree. After we clean up the mess, we have a big breakfast. Then the kids have the whole day to play with their new toys.', '哦，是的。我们都把礼物放在树旁显眼的地方。收拾完之后，我们吃丰盛的早餐。然后孩子们可以整天玩新玩具。', NULL, NULL, NULL, 'presents, prominent, Christmas', 1),

    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Are you decorating your Christmas tree?', '你在装饰圣诞树吗？', NULL, '根据课件提示补全。', NULL, 'Christmas tree, decorate', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes, I''m putting ornaments on the tree.', '是的，我在树上挂装饰品。', NULL, NULL, NULL, 'ornaments, Christmas tree', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'These lights look pretty old.', '这些灯看起来相当旧。', NULL, NULL, NULL, 'lights, Christmas', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Yeah, they date back to my childhood.', '是啊，它们可以追溯到我的童年。', NULL, NULL, NULL, 'date back to, childhood, Christmas', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Where will you keep presents?', '你会把礼物放在哪里？', NULL, NULL, NULL, 'presents, Christmas', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Somewhere prominent, perhaps I will put them near the chimney.', '放在显眼的地方吧，也许我会放在烟囱旁。', NULL, NULL, NULL, 'prominent, chimney, presents', 1),

    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you ever celebrated Christmas? What do people do at Christmas?', '你庆祝过圣诞节吗？人们圣诞节会做什么？', NULL, '可谈准备圣诞树、家庭聚会、给别人送礼、散步和购物。', NULL, 'Christmas, holiday, family', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'More and more young Chinese celebrate Christmas. Do you think it is a good thing? Give your reasons.', '越来越多的中国年轻人庆祝圣诞节。你认为这是好事吗？请说明理由。', NULL, '可谈促进文化交流、让生活更有趣；也可谈容易忽视本土文化、在装饰品上浪费钱。', NULL, 'Christmas, culture, holiday', 1),

    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'It''s a family tradition dating back to my childhood.\nWe use the same lights and ornaments.\nWe also place these stockings next to the chimney.\nWe all put presents in the prominent place next to the tree.', '复习：date back to / ornament / chimney / Santa Claus / prominent。', NULL, NULL, NULL, 'review, Christmas', 1),

    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'ribbon', 'ribbon', '彩带', NULL, '课后拓展：圣诞装饰词汇。', NULL, 'Christmas, ribbon', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'tree topper', 'tree topper', '树顶装饰物', NULL, '课后拓展：圣诞装饰词汇。', NULL, 'Christmas, tree topper', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'tree light', 'tree light', '圣诞树彩灯', NULL, '课后拓展：圣诞装饰词汇。', NULL, 'Christmas, tree light', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'bauble', 'bauble', '小装饰品', NULL, '课后拓展：圣诞装饰词汇。', NULL, 'Christmas, bauble', 1),
    ('christmas', 'Chapter 10 · Holidays', 'Lesson 90 · Christmas', 90, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'candy cane', 'candy cane', '拐杖糖', NULL, '课后拓展：圣诞装饰词汇。', NULL, 'Christmas, candy cane', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 91 · Mother's Day (doc/116665_4651_Mother's Day.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'carnation', 'carnation', '康乃馨', '/kɑːrˈneɪʃn/', 'a white, pink, red, or yellow flower often worn as a decoration on formal occasions', 'He was wearing a carnation in his buttonhole.', 'carnation, Mother''s Day, flower', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'put up with', 'put up with', '忍受；忍耐', '/pʊt ʌp wɪθ/', 'to accept somebody or something annoying or unpleasant without complaining', 'He can''t put up with the noise.', 'put up with, Mother''s Day, family', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'give birth to', 'give birth to', '分娩；生下', '/ɡɪv bɜːrθ tu/', 'to give birth to a baby', 'Mary gave birth to a healthy baby girl.', 'give birth to, Mother''s Day, family', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'pregnancy', 'pregnancy', '怀孕', '/ˈpreɡnənsi/', 'the state of being pregnant', 'Most women feel sick in the mornings during their first months of pregnancy.', 'pregnancy, Mother''s Day, family', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'devote to', 'devote … to …', '奉献给……', '/dɪˈvəʊt/', 'to give all of something, especially time, effort, love, or yourself, to something you believe in or to a person', 'Mother devotes everything to her child.', 'devote, Mother''s Day, family', 1),

    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'What are you getting for your mom on Mother''s Day?', '母亲节你要给妈妈买什么？', NULL, NULL, NULL, 'Mother''s Day, gift', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'I will buy a carnation for her, because carnation is regarded as the flower for mothers. What about you?', '我会给她买一束康乃馨，因为康乃馨被认为是母亲的花。你呢？', NULL, NULL, NULL, 'carnation, Mother''s Day, gift', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'I will buy a necklace for her using the money that I''ve saved. She puts up with all my faults.', '我会用攒下的钱给她买一条项链。她忍受了我所有的缺点。', NULL, NULL, NULL, 'necklace, put up with, Mother''s Day', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'dialogue', '示范对话', 2, 'dialogue', 104, 'David', NULL, 'Mothers give birth to us after over nine months'' of pregnancy, and they devote themselves to their children.', '母亲经历九个多月的怀孕生下我们，并把自己奉献给孩子。', NULL, NULL, NULL, 'give birth to, pregnancy, devote', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'Yes, they certainly deserve all the respect. They do the most important job: being a mom.', '是的，她们当然值得所有尊重。她们做着最重要的工作：成为母亲。', NULL, NULL, NULL, 'respect, mothers, Mother''s Day', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'I am incredibly lucky to have my mom who raises, loves, and looks after me.', '我非常幸运，有一位养育、爱护和照顾我的妈妈。', NULL, NULL, NULL, 'mother, family, gratitude', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'So do I.', '我也是。', NULL, NULL, NULL, 'mother, family, agreement', 1),

    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'What will you do on Mother''s Day?', '母亲节你会做什么？', NULL, '根据课件提示补全。', NULL, 'Mother''s Day, plans', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I will prepare a carnation for her, the flower of mothers. How about you?', '我会给她准备一束康乃馨，母亲的花。你呢？', NULL, NULL, NULL, 'carnation, Mother''s Day', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I will just clean up the whole house. Thank her for putting up with my messy room.', '我会把整个房子打扫干净。感谢她忍受我凌乱的房间。', NULL, NULL, NULL, 'put up with, housework, Mother''s Day', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'They certainly deserve a good rest. They give birth to us after over nine months'' of pregnancy, and they devote their time and energy to our well-being.', '她们当然值得好好休息。她们经历九个多月怀孕生下我们，把时间和精力奉献给我们的幸福。', NULL, NULL, NULL, 'give birth to, pregnancy, devote', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'You''re right.', '你说得对。', NULL, NULL, NULL, 'Mother''s Day, agreement', 1),

    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you ever celebrated Mother''s Day? What do you do for your mom on that day? If you have not, what do you plan to do next Mother''s Day?', '你庆祝过母亲节吗？那天你为妈妈做什么？如果没有，下一个母亲节计划做什么？', NULL, '可谈买礼物、做家务、做让妈妈开心的事、让她休息或给她洗脚。', NULL, 'Mother''s Day, mother, gratitude', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Have you ever expressed gratitude to your mother? If so, what did you say? If not, what would you say?', '你向母亲表达过感激吗？如果表达过，你说了什么？如果没有，你会说什么？', NULL, '可谈“我爱你”“谢谢你把我带到这个世界”“谢谢你为我做的一切”或“谢谢你忍受我做的烦人事情”。', NULL, 'gratitude, mother, Mother''s Day', 1),

    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I will buy a carnation for her, because carnation is regarded as the flower for mothers.\nMothers give birth to us after over nine months'' of pregnancy, and they devote themselves to their children.', '复习：carnation / put up with / give birth to / pregnancy / devote … to …。', NULL, NULL, NULL, 'review, Mother''s Day', 1),

    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'A mother is strong', 'While women are vulnerable, the mother is strong. — Victor Hugo', '女性也许脆弱，但母亲是坚强的。——维克多·雨果', NULL, '课后拓展：关于母亲的名言。', NULL, 'mother, Mother''s Day, quote', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'A mother''s prayers', 'I remember my mother''s prayers and they have always followed me; they have clung to me all my life. — Abraham Lincoln', '我记得母亲的祈祷，它们一直伴随着我，紧紧跟随我的一生。——亚伯拉罕·林肯', NULL, '课后拓展：关于母亲的名言。', NULL, 'mother, Mother''s Day, quote', 1),
    ('mothers-day', 'Chapter 10 · Holidays', 'Lesson 91 · Mother''s Day', 91, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'A refined mother', 'I have met many people around the world, but never a more thoroughly refined woman than my mother. If I have amounted to anything, it will be due to her. — Charles Chaplin', '我在世界各地遇到许多人，却从未见过比我母亲更优雅的女性。若我有所成就，都归功于她。——查理·卓别林', NULL, '课后拓展：关于母亲的名言。', NULL, 'mother, Mother''s Day, quote', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 92 · New Year (doc/116794_4651_New Year.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'be about to', 'be about to', '即将；刚要；正打算', '/bi əˈbaʊt tu/', 'to be close to doing something; to be going to do something very soon', 'I was just about to ask you the same thing.', 'be about to, New Year, plans', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'clean slate', 'clean slate', '空白；既往不咎', '/kliːn sleɪt/', 'a record without mistakes or bad things, or a decision to forget past behavior and start again', 'When we are born, we are a clean slate. / We''ll start again with a clean slate this semester.', 'clean slate, New Year, fresh start', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'resolution', 'resolution', '决心', '/ˌrezəˈluːʃn/', 'a firm decision to do or not to do something', 'He made a resolution to climb over the mountain.', 'resolution, New Year, goals', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'spectacular', 'spectacular', '壮观的；壮丽的；令人惊叹的', '/spekˈtækjələr/', 'very impressive', 'There is a spectacular display of fireworks.', 'spectacular, New Year, fireworks', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'countdown', 'countdown', '倒计时', '/ˈkaʊntdaʊn/', 'the short period of time before something important happens', 'The countdown to the New Year has already begun.', 'countdown, New Year, holiday', 1),

    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'We are about to start a brand new year!', '我们即将开始崭新的一年！', NULL, NULL, NULL, 'be about to, New Year', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'I know. It''s so exciting! A new year is always like a clean slate – a fresh start to accomplish any dreams, objectives and goals.', '我知道。太令人兴奋了！新年总像一张白纸，是实现任何梦想、目标和目的的全新开始。', NULL, NULL, NULL, 'clean slate, fresh start, New Year', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'Do you have a New Year''s resolution?', '你有新年决心吗？', NULL, NULL, NULL, 'New Year''s resolution, goals', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'I was thinking about it, but I''m never able to keep my New Year''s resolution. Last year, for example, I joined a gym and only went twice.', '我想过这件事，但我从来无法坚持新年决心。比如去年我加入健身房，却只去了两次。', NULL, NULL, NULL, 'New Year''s resolution, gym, goals', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'Perhaps you can have a simpler resolution, like seeing the large and spectacular fireworks displays.', '也许你可以有一个更简单的决心，例如去看盛大而壮观的烟花表演。', NULL, NULL, NULL, 'resolution, spectacular, fireworks', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'That''s a good idea, and we can''t miss the countdown to midnight.', '这是个好主意，而且我们不能错过午夜倒计时。', NULL, NULL, NULL, 'countdown, midnight, New Year', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'Let''s go.', '我们走吧。', NULL, NULL, NULL, 'New Year, plans', 1),

    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Do you have a New Year''s resolution?', '你有新年决心吗？', NULL, '根据课件提示补全。', NULL, 'New Year''s resolution, goals', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'This year, I plan to start from a clean slate and study harder. What about you?', '今年我计划从头开始，更努力学习。你呢？', NULL, NULL, NULL, 'clean slate, study, New Year', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'I am about to go to a spectacular concert. I''ve listened to the songs of pop star Jay Chou for a long time, and finally I can go to his concert this month.', '我正打算去一场精彩的音乐会。我听流行歌手周杰伦的歌很久了，终于能在这个月去他的演唱会。', NULL, NULL, NULL, 'be about to, spectacular, concert', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'You are so lucky. I wish you had a good time.', '你真幸运。祝你玩得开心。', NULL, NULL, NULL, 'New Year, wishes', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Thank you.', '谢谢。', NULL, NULL, NULL, 'New Year, wishes', 1),

    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'How do you spend New Year on January 1st? Do you have any traditions?', '你如何度过 1 月 1 日的新年？有什么传统吗？', NULL, '可谈和朋友闲逛、看烟花表演或家庭聚会。', NULL, 'New Year, traditions, holiday', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you like to make New Year''s resolutions? What would you make today? Have you successfully kept resolutions? Why or why not?', '你喜欢制定新年决心吗？今天会制定什么？你成功坚持过决心吗？为什么？', NULL, '可谈更努力学习或工作、去健身房、旅行；也可谈自己懒惰、决心太简单或缺少能力和时间。', NULL, 'New Year''s resolution, goals, holiday', 1),

    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'We are about to start a brand-new year!\nA new year is always like a clean slate, fresh start to accomplish any dreams, objectives and goals.\nDo you have a New Year''s resolution?', '复习：be about to / clean slate / resolution / spectacular / countdown。', NULL, NULL, NULL, 'review, New Year', 1),

    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Coal in Scottish New Year', 'On New Year''s Eve, a lump of coal can signify warmth and wish hosts enough heat in the coming year.', '苏格兰新年前夜的煤块象征温暖，祝愿主人来年有足够热量。', NULL, '课后拓展：苏格兰新年习俗。', NULL, 'Scottish New Year, coal, warmth', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Shortbread in Scottish New Year', 'Shortbread represents food and wishes that people will have enough to eat.', '奶油甜酥饼代表食物，祝愿人们有足够食物。', NULL, '课后拓展：苏格兰新年习俗。', NULL, 'Scottish New Year, shortbread, food', 1),
    ('new-year', 'Chapter 10 · Holidays', 'Lesson 92 · New Year', 92, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Whisky in Scottish New Year', 'Whisky was called the water of life by Scots and wishes the hosts enough to drink.', '威士忌被苏格兰人称为“生命之水”，祝愿主人有足够饮品。', NULL, '课后拓展：苏格兰新年习俗。', NULL, 'Scottish New Year, whisky, tradition', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 93 · Chinese New Year (doc/116795_4651_Chinese New Year.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'couplet', 'couplet', '对句；春联', '/ˈkʌplət/', 'two lines of poetry of equal length, one after the other', 'Have you put up the Spring Festival couplets?', 'couplet, Chinese New Year, Spring Festival', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'sweep away', 'sweep away', '一扫而空', '/swiːp əˈweɪ/', 'to get rid of something completely', 'They want to sweep away the bad luck.', 'sweep away, bad luck, Chinese New Year', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'set off', 'set off', '使爆炸；燃放', '/set ɔːf/', 'to make a bomb or similar thing explode', 'Don''t set off the bomb.', 'set off, firecrackers, Chinese New Year', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'gala', 'gala', '庆典；盛会', '/ˈɡeɪlə/', 'a special public celebration or entertainment', 'Let''s watch the Spring Festival Gala.', 'gala, Chinese New Year, Spring Festival', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'firecracker', 'firecracker', '爆竹；鞭炮', '/ˈfaɪərkrækər/', 'a small firework that explodes with a loud noise', 'The kids are setting off firecrackers.', 'firecracker, Chinese New Year, Spring Festival', 1),

    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'Time flies! Chinese New Year is around the corner!', '时间过得真快！春节快到了！', NULL, NULL, NULL, 'Chinese New Year, Spring Festival', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Mary', NULL, 'Have you put up Chinese New Year couplets?', '你贴春联了吗？', NULL, NULL, NULL, 'couplets, Chinese New Year', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'I am busy doing cleaning, and meanwhile sweeping away bad luck.', '我正忙着打扫，同时扫走坏运气。', NULL, NULL, NULL, 'sweep away, bad luck, cleaning', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Mary', NULL, 'Really? How mysterious!', '真的吗？多神秘啊！', NULL, NULL, NULL, 'Chinese New Year, traditions', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'Yes, there''re many beautiful legends about Chinese New Year.', '是的，关于春节有很多美丽的传说。', NULL, NULL, NULL, 'legends, Chinese New Year', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Mary', NULL, 'Will you stay up late?', '你会熬夜吗？', NULL, NULL, NULL, 'stay up late, Chinese New Year', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'I will go to bed after the Chinese New Year Gala on TV and after setting off firecrackers. I have to stay energetic when visiting relatives and friends tomorrow.', '我会在电视上看完春节联欢晚会、燃放鞭炮后睡觉。明天拜访亲戚朋友时我得保持精力。', NULL, NULL, NULL, 'gala, set off firecrackers, relatives', 1),

    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Have you put up Chinese New Year couplets?', '你贴春联了吗？', NULL, '根据课件提示补全。', NULL, 'couplets, Chinese New Year', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'No, my family will do it tomorrow. I just helped my parents clean up the whole house to sweep away the bad luck.', '还没有，我家明天会贴。我刚帮父母打扫整个房子来扫走坏运气。', NULL, NULL, NULL, 'sweep away, bad luck, cleaning', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'How do you spend Chinese New Year?', '你如何度过春节？', NULL, NULL, NULL, 'Chinese New Year, traditions', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'My family watch the Chinese New Year Gala, and we set off firecrackers together.', '我家看春节联欢晚会，我们一起燃放鞭炮。', NULL, NULL, NULL, 'gala, set off firecrackers, Chinese New Year', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'So do my family.', '我家也是。', NULL, NULL, NULL, 'Chinese New Year, family', 1),

    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'How do you celebrate Chinese New Year? Introduce the festival and some of its traditions.', '你如何庆祝春节？介绍这个节日及其一些传统。', NULL, '可谈贴春联、看春晚、燃放鞭炮和看舞龙。', NULL, 'Chinese New Year, traditions, Spring Festival', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'In some Chinese cities, people are not allowed to set off firecrackers during Spring Festival. What do you think of this rule?', '在一些中国城市，人们春节期间不允许燃放鞭炮。你怎么看这项规定？', NULL, '可谈减少污染和噪音、提升安全、节省金钱；也可谈会破坏传统和节日氛围。', NULL, 'firecrackers, Spring Festival, regulation', 1),

    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Have you put up Chinese New Year couplets?\nI am busy doing cleaning, and meanwhile sweeping away bad luck.\nI will go to bed after the Chinese New Year Gala on TV and after setting off firecrackers.', '复习：couplet / sweep away / gala / set off / firecracker。', NULL, NULL, NULL, 'review, Chinese New Year', 1),

    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'extra', '拓展学习', 6, 'extra', 501, NULL, '金玉满堂', 'May your wealth (gold and jade) come to fill a hall.', '愿你的财富（金玉）充满厅堂。', NULL, '课后拓展：春节祝福语。', NULL, 'Chinese New Year, blessing', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'extra', '拓展学习', 6, 'extra', 502, NULL, '大展宏图', 'May you realize your ambitions.', '愿你实现抱负。', NULL, '课后拓展：春节祝福语。', NULL, 'Chinese New Year, blessing, ambition', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'extra', '拓展学习', 6, 'extra', 503, NULL, '迎春接福', 'Greet the New Year and encounter happiness.', '迎接新年，收获幸福。', NULL, '课后拓展：春节祝福语。', NULL, 'Chinese New Year, blessing, happiness', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'extra', '拓展学习', 6, 'extra', 504, NULL, '万事如意', 'May all your wishes be fulfilled.', '愿你万事如意。', NULL, '课后拓展：春节祝福语。', NULL, 'Chinese New Year, blessing, wishes', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'extra', '拓展学习', 6, 'extra', 505, NULL, '吉庆有余', 'May your happiness be without limits.', '愿你幸福无尽。', NULL, '课后拓展：春节祝福语。', NULL, 'Chinese New Year, blessing, happiness', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'extra', '拓展学习', 6, 'extra', 506, NULL, '福寿双全', 'May your happiness and longevity be complete.', '愿你福寿双全。', NULL, '课后拓展：春节祝福语。', NULL, 'Chinese New Year, blessing, longevity', 1),
    ('chinese-new-year', 'Chapter 10 · Holidays', 'Lesson 93 · Chinese New Year', 93, 'extra', '拓展学习', 6, 'extra', 507, NULL, '招财进宝', 'When wealth is acquired, precious objects follow.', '招来财富，获得珍宝。', NULL, '课后拓展：春节祝福语。', NULL, 'Chinese New Year, blessing, wealth', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 94 · Mid-Autumn Festival (doc/116797_4651_Mid-Autumn Festival.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'lunar calendar', 'lunar calendar', '阴历', '/ˈluːnər ˈkælɪndər/', 'a calendar based on lunar cycles', 'Mid-Autumn Festival is held on the 15th day of the eighth month in China''s lunar calendar.', 'lunar calendar, Mid-Autumn Festival, holiday', 1),
    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'reunion', 'reunion', '团聚', '/ˌriːˈjuːniən/', 'a social occasion or party attended by a group of people who have not seen each other for a long time', 'We''re having a family reunion next week.', 'reunion, Mid-Autumn Festival, family', 1),
    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'riddle', 'riddle', '谜语', '/ˈrɪdl/', 'a question that is difficult to understand and has a surprising answer, which you ask somebody as a game', 'There are riddles on the lanterns.', 'riddle, Mid-Autumn Festival, lantern', 1),
    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'lantern', 'lantern', '灯笼', '/ˈlæntərn/', 'a lamp in a transparent case, often metal with glass sides, which has a handle so you can carry it outside', 'It''s time to light up the lanterns.', 'lantern, Mid-Autumn Festival, riddle', 1),
    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'mooncake', 'mooncake', '月饼', '/ˈmuːnkeɪk/', 'a round Chinese cake, usually pastry with thick sweet stuffing, traditionally eaten during the Mid-Autumn Festival', 'Let''s have some mooncakes.', 'mooncake, Mid-Autumn Festival, food', 1),

    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Jack', NULL, 'The Mid-Autumn Festival is held on the 15th day of the eighth month in China''s lunar calendar. Am I right?', '中秋节在中国农历八月十五举行。我说得对吗？', NULL, NULL, NULL, 'lunar calendar, Mid-Autumn Festival', 1),
    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Lin', NULL, 'You''re right.', '你说得对。', NULL, NULL, NULL, 'Mid-Autumn Festival, agreement', 1),
    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Jack', NULL, 'How do you usually celebrate?', '你通常怎么庆祝？', NULL, NULL, NULL, 'Mid-Autumn Festival, traditions', 1),
    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Lin', NULL, 'I have a family reunion. The Mid-Autumn Festival is an important family holiday for Chinese people. Many families will write riddles on lanterns and have other people try to guess the answers, and they will also watch the moon in the sky.', '我会家庭团聚。中秋节是中国人重要的家庭节日。许多家庭会在灯笼上写谜语，让别人猜答案，还会赏月。', NULL, NULL, NULL, 'reunion, riddles, lanterns, moon', 1),
    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Jack', NULL, 'I have heard that you eat a special food called mooncake on Mid-Autumn Festival as well.', '我听说中秋节还会吃一种叫月饼的特殊食物。', NULL, NULL, NULL, 'mooncake, Mid-Autumn Festival', 1),
    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Lin', NULL, 'That''s correct. Actually, I have brought one for you. Here you are.', '没错。其实我给你带了一个。给你。', NULL, NULL, NULL, 'mooncake, gift, Mid-Autumn Festival', 1),
    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Jack', NULL, 'Thank you so much.', '非常感谢。', NULL, NULL, NULL, 'mooncake, gratitude', 1),

    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'How do you spend the Mid-Autumn Festival?', '你如何度过中秋节？', NULL, '根据课件提示补全。', NULL, 'Mid-Autumn Festival, traditions', 1),
    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Last year, I had a family reunion. After we had our dinner, we went out to watch the red lanterns and the moon. Luckily, I figured out the answers to some riddles and won a gift.', '去年我家庭团聚。晚饭后，我们出去看红灯笼和月亮。幸运的是，我猜出了一些谜语的答案，还赢得了一份礼物。', NULL, NULL, NULL, 'reunion, lanterns, riddles', 1),
    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'How lucky you were! Did you forget to eat mooncakes?', '你真幸运！你忘记吃月饼了吗？', NULL, NULL, NULL, 'mooncakes, Mid-Autumn Festival', 1),
    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Of course not. After my family came home, we ate a few and watched TV.', '当然没有。家人回家后，我们吃了几个月饼并看电视。', NULL, NULL, NULL, 'mooncakes, family, Mid-Autumn Festival', 1),

    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'How do you spend your Mid-Autumn Festival? Introduce the festival and its traditions.', '你如何度过中秋节？介绍这个节日及其传统。', NULL, '可谈家庭团聚、吃月饼、赏月、点灯笼和猜灯谜。', NULL, 'Mid-Autumn Festival, traditions, family', 1),
    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Try to tell the story of Chang''e and Hou Yi. Use the prompts bow, arrow, god, and elixir of life.', '试着讲述嫦娥和后羿的故事，可使用“弓、箭、神、长生不老药”等提示。', NULL, '故事梗概：天上曾有十个太阳，天气异常炎热。弓箭手后羿射落九个太阳，拯救人间。神仙赐给后羿长生不老药作为奖励；他的妻子嫦娥喝下药后飞到天上，从此住在月亮上。', NULL, 'Chang''e, Hou Yi, Mid-Autumn Festival, legend', 1),

    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'Mid-Autumn Festival is held on the 15th day of the eighth month in China''s lunar calendar.\nSome families will write riddles on lanterns and have other people try to guess the answers, and they will also watch the moon in the sky.', '复习：lunar calendar / reunion / riddle / lantern / mooncake。', NULL, NULL, NULL, 'review, Mid-Autumn Festival', 1),

    ('mid-autumn-festival', 'Chapter 10 · Holidays', 'Lesson 94 · Mid-Autumn Festival', 94, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Mooncake rebellion legend', 'During the Yuan Dynasty, rebels are said to have hidden messages outlining an attack inside special cakes before the Moon Festival. The successful uprising is commemorated by eating mooncakes during the Mid-Autumn Festival.', '元朝时期的传说称，反抗者在中秋节前将起义信息藏在特制糕点里。成功起义后，人们在中秋节吃月饼以纪念这场反抗。', NULL, '课后拓展：月饼传说。', NULL, 'mooncake, Mid-Autumn Festival, Yuan Dynasty', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

COMMIT;
