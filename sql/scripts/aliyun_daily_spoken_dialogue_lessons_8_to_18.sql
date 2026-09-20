-- Extracted from the first ten PDFs in doc/, ordered by source file identifier.
-- Sources: Learn & Talk I, Chapter 1 Lessons 8-10 and Chapter 2 Lessons 12-18.
-- The target table is created by aliyun_daily_spoken_dialogue_buying_clothes.sql.
-- Re-running this file updates only the lesson_code/item_order pairs below.

SET NAMES utf8mb4;
START TRANSACTION;

-- Lesson 8 · Return & Refund (doc/110410_806_Return & Refund.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'return', 'return', '归还；退货', '/rɪˈtɜːrn/', 'to send, take, give, put, etc. something back to where it came from', 'The new TV broke, so they returned it to the shop.', 'return, refund, shopping', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'refund', 'refund', '退款', '/ˈriːfʌnd/', 'an amount of money that is given back to you, especially because you are not happy with a product or service you bought', 'I took the radio back to the shop and asked for a refund.', 'refund, return, shopping', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'turn off', 'turn off', '关闭；关掉', '/tɜːrn ɔːf/', 'to stop heat, sound, or water from being produced by adjusting the controls', 'Have you turned off the TV?', 'turn off, on its own, device', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'take care of', 'take care of', '处理；照顾；注意', '/teɪk ker əv/', 'to be responsible for or deal with a situation or task', 'Take good care of that girl of yours — she is very special.', 'take care of, handle, refund', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'on one''s own', 'on one''s own', '靠自己；独自；自行', NULL, 'alone; without help from anyone else', 'They want to do things on their own.', 'on one''s own, alone, device', 1),

    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Salesman', NULL, 'How can I help you, sir?', '先生，我能帮您什么吗？', NULL, NULL, NULL, 'return, customer service', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Peter', NULL, 'I''m returning a cellphone that I bought yesterday.', '我想退掉昨天买的一部手机。', NULL, NULL, NULL, 'return, cellphone', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Salesman', NULL, 'Is there something wrong with it?', '它有什么问题吗？', NULL, NULL, NULL, 'something wrong, return', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Peter', NULL, 'It keeps turning off on its own. It doesn''t work at all.', '它总是自己关机，完全不能用。', NULL, NULL, NULL, 'turn off on its own, defective', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Salesman', NULL, 'I''m sorry to hear about your bad experience. Do you have the receipt with you?', '很抱歉您有这样的糟糕经历。您带收据了吗？', NULL, NULL, NULL, 'receipt, bad experience', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Peter', NULL, 'I have it right here.', '我就在这儿带着。', NULL, NULL, NULL, 'receipt, right here', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Salesman', NULL, 'Thank you, sir. I am going to take care of this and give you the refund.', '谢谢您，先生。我会处理这件事并给您退款。', NULL, NULL, NULL, 'take care of, refund', 1),

    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Hi, there. Can I help you?', '您好，我能帮您什么吗？', NULL, '根据课件提示补全。', NULL, 'return, practice', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I''d like to return something that I bought last week.', '我想退掉上周买的一件东西。', NULL, NULL, NULL, 'return, purchase', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'What would you like to return?', '您想退什么？', NULL, NULL, NULL, 'return, question', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'I''m returning a computer.', '我想退一台电脑。', NULL, NULL, NULL, 'return, computer', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Is there something wrong with it?', '它有什么问题吗？', NULL, NULL, NULL, 'something wrong, defective', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Yes. It is defective. It always turns off on its own.', '是的，它有瑕疵，总是自己关机。', NULL, NULL, NULL, 'defective, turn off on its own', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'I''m sorry to hear about your bad experience. Do you have the receipt?', '很抱歉您有这样的糟糕经历。您有收据吗？', NULL, NULL, NULL, 'receipt, return', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'practice', '情景补全对话', 3, 'practice', 208, 'B', NULL, 'Yes, I have it right here.', '有，我就在这儿带着。', NULL, NULL, NULL, 'receipt, right here', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'practice', '情景补全对话', 3, 'practice', 209, 'A', NULL, 'Thank you. I''ll take care of this and give you the refund.', '谢谢。我会处理这件事并给您退款。', NULL, NULL, NULL, 'take care of, refund', 1),

    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you ever returned something to a shop? Why did you return that thing? Try to describe it with details.', '你曾经退过货吗？为什么要退？请详细描述。', NULL, '可以说明退了什么、为什么退，以及是否得到了应得的退款。', NULL, 'return, refund, experience', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'For online shopping on Taobao.com, customers can return things to sellers without giving any reasons within seven days. Do you support this policy? Why or why not?', '在淘宝购物时，消费者可以七天无理由退货。你支持这项政策吗？为什么？', NULL, '支持：保护买家权益、推动卖家提供更好的产品、买家需要看到实物后才能决定。反对：损害卖家利益、可能被少数人滥用、运输也可能造成损坏。', NULL, 'seven-day return, online shopping, policy', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Do you think physical stores should also implement a seven-day return-and-refund policy without giving a reason, like Taobao.com does? Why or why not?', '你认为实体店也应该像淘宝一样实行七天无理由退换货吗？为什么？', NULL, '可从商家方面的权益、知名度、成本和利润，以及消费者方面的便利性、权益和选择来谈。', NULL, 'physical store, return policy, consumer rights', 1),

    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I''m returning a cellphone that I bought yesterday.\nIs there something wrong with it?\nI am going to take care of this and give you the refund.', '复习：return / refund / turn off / take care of / on one''s own。', NULL, NULL, NULL, 'review, return, refund', 1),

    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'return of goods without reasons within 7 days', 'return of goods without reasons within 7 days', '7天无理由退换货', NULL, NULL, NULL, 'return, seven days', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'tax refund', 'tax refund', '退税', NULL, NULL, NULL, 'tax, refund', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'substandard goods', 'substandard goods', '不合格产品', NULL, NULL, NULL, 'substandard, goods', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'knockoff', 'knockoff', '假货；仿制品', NULL, NULL, NULL, 'knockoff, fake', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'defective', 'defective', '有瑕疵的', NULL, NULL, NULL, 'defective, return', 1),
    ('return-and-refund', 'Chapter 1 · Shopping', 'Lesson 8 · Return & Refund', 8, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'damaged', 'damaged', '有破损的', NULL, NULL, NULL, 'damaged, return', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 9 · Online Shopping (doc/110413_806_Online Shopping.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'order', 'order', '订购', '/ˈɔːrdər/', 'to ask for something to be made, supplied, or delivered, especially in a restaurant or shop', 'There are no shirts left in this size, but we could order one for you.', 'order, online shopping', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'deal', 'deal', '交易；划算的买卖', '/diːl/', 'an agreement or arrangement, especially in business', 'She got a good deal on her new house.', 'deal, discount, shopping', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'discount', 'discount', '折扣', '/ˈdɪskaʊnt/', 'a reduction in the usual price', 'They offer a 10% discount on travel for students.', 'discount, price, online shopping', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'original', 'original', '原始的；最初的；原价的', '/əˈrɪdʒənl/', 'existing since the beginning, or being the earliest form of something', 'The gardens have recently been restored to their original glory.', 'original price, shopping', 1),

    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Anna', NULL, 'Hey, where did you buy this dress?', '嘿，你在哪里买的这条裙子？', NULL, NULL, NULL, 'buy, dress', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Fiona', NULL, 'I ordered it on eBay.', '我在 eBay 上订的。', NULL, NULL, NULL, 'order, eBay', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Anna', NULL, 'Didn''t you find it expensive there?', '你不觉得那里很贵吗？', NULL, NULL, NULL, 'expensive, online shopping', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Fiona', NULL, 'No, not at all. It has some great deals! I got crazy discounts!', '完全不贵。那里有很多超值优惠！我拿到了超大折扣！', NULL, NULL, NULL, 'great deal, discount', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Anna', NULL, 'How much did this cost you?', '这个花了你多少钱？', NULL, NULL, NULL, 'cost, price', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Fiona', NULL, 'Well, I got a 45% discount on the original price.', '我在原价基础上拿到了 45% 的折扣。', NULL, NULL, NULL, '45% discount, original price', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Anna', NULL, 'Wow! That''s a super deal. I will check it out today.', '哇！真划算。我今天就去看看。', NULL, NULL, NULL, 'super deal, check out', 1),

    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'You got another package today.', '你今天又收到一个包裹。', NULL, '根据课件提示补全。', NULL, 'package, online shopping', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Great!', '太好了！', NULL, NULL, NULL, 'package', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'What did you order this time?', '这次你订了什么？', NULL, NULL, NULL, 'order, online shopping', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Books, clothes, and shoes.', '书、衣服和鞋子。', NULL, NULL, NULL, 'books, clothes, shoes', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Wow! That''s a lot of stuff. How much did they cost you?', '哇！东西真多。它们花了你多少钱？', NULL, NULL, NULL, 'cost, shopping', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, '$48 including shipping fees.', '包含运费一共 48 美元。', NULL, NULL, NULL, 'shipping fees, price', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'It''s quite cheap.', '相当便宜。', NULL, NULL, NULL, 'cheap, price', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'practice', '情景补全对话', 3, 'practice', 208, 'B', NULL, 'Yes, it has some great deals! I got crazy discounts! It''s much cheaper than the original price. That''s why I love to shop online.', '是啊，那里有很多超值优惠！我拿到了很大的折扣！这比原价便宜多了，所以我喜欢网购。', NULL, NULL, NULL, 'deal, discount, original price', 1),

    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'What online shopping websites do you often use? What do you often buy online? Can you describe an experience of online shopping you recently had?', '你常用哪些网购网站？常在网上买什么？请描述一次最近的网购经历。', NULL, '可说明所用的网站、购买的东西、花费，以及是否满意和原因。', NULL, 'online shopping, experience, website', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Have you ever bought any fake or poor-quality goods? How did you deal with it?', '你买过假货或质量差的商品吗？你是怎么处理的？', NULL, '可说明买了什么、花了多少钱，以及是否投诉要求退款，或因低价瑕疵品很常见而接受了它。', NULL, 'fake goods, poor quality, refund', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Nowadays, online shopping has become more popular than in-store shopping. Is it a positive or a negative trend?', '如今网购比实体店购物更受欢迎。这是积极还是消极的趋势？', NULL, '积极面：更方便、价格更低且常有折扣、商品选择广、节省时间和金钱。消极面：假货和劣质产品、可能欺骗消费者、有时浪费时间和钱。', NULL, 'online shopping, in-store shopping, trend', 1),

    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'It has some great deals! I got crazy discounts!\nHow much did this cost you?\nI got a 45% discount on the original price.', '复习：order / deal / original / discount。', NULL, NULL, NULL, 'review, online shopping', 1),

    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Products may differ from their advertisements.', 'Sometimes, the things I bought from online shops were quite different from their advertisements.', '网购商品有时与广告不符。', NULL, '课后拓展：网购的缺点。', NULL, 'advertisement, online shopping', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Risk of fraud', 'Without close examination, we are taking a risk of buying frauds.', '无法仔细检查商品时，可能有买到假货的风险。', NULL, '课后拓展：网购的缺点。', NULL, 'fraud, online shopping', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Online transactions are not always safe.', 'Making transactions on the Internet is not always safe, though some measures have been taken to solve this problem.', '虽然已有一些应对措施，但网上交易并不总是安全。', NULL, '课后拓展：网购的缺点。', NULL, 'transaction, online safety', 1),
    ('online-shopping', 'Chapter 1 · Shopping', 'Lesson 9 · Online Shopping', 9, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Online shops may disappear.', 'Online shops may suddenly disappear, and sellers may be nowhere to be found.', '网店可能突然消失，卖家也无处可寻。', NULL, '课后拓展：网购的缺点。', NULL, 'seller, online shop', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 10 · Revision One (doc/110840_806_Revision One.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 1, NULL, 'on sale', 'on sale', '减价的；降价出售的', '/ɑːn seɪl/', 'reduced in price', 'These clothes are on sale now!', 'on sale, shopping', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 2, NULL, 'try on', 'try on', '试穿；试戴', '/traɪ ɑːn/', 'to put on clothing to see whether it fits or looks nice', 'May I try on these shoes?', 'try on, clothes', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 3, NULL, 'out of stock', 'out of stock', '缺货的；售罄的', '/aʊt əv stɑːk/', 'if a store has sold all of a particular product; sold out', 'I''m sorry, it''s out of stock now.', 'out of stock, shopping', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 4, NULL, 'take in', 'take in', '将衣物改小；收紧', '/teɪk ɪn/', 'to make a dress, jacket, or other item of clothing smaller and tighter', 'The dress is loose. I''ll take it in.', 'take in, clothes', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 5, NULL, 'look for', 'look for', '寻找', '/lʊk fər/', 'to try to find something or someone', 'They''re looking for insects in the field.', 'look for, shopping', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 6, NULL, 'have something in mind', 'have something in mind', '心里有想法；想到', NULL, 'to think of something', 'What do you have in mind?', 'have in mind, idea', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 7, NULL, 'how about (doing) something', 'how about (doing) something', '……怎么样？', NULL, 'used to introduce a new subject that is relevant to the conversation', 'How about a cup of coffee? How about going to the cinema?', 'how about, suggestion', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 8, NULL, 'gift-wrap', 'gift-wrap', '礼品包装', '/ɡɪft ræp/', 'to wrap as a gift with decorative paper, ribbon, etc.', 'She''s gift-wrapping the chocolate.', 'gift-wrap, gift', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 9, NULL, 'offer', 'offer', '提供；供应', '/ˈɔːfər/', 'to provide or supply something', 'He offered me a glass of water.', 'offer, shopping', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 10, NULL, 'delivery', 'delivery', '运送；递送', '/dɪˈlɪvəri/', 'the act of taking goods, letters, or parcels to a home or workplace', 'They offer free delivery, so it''s a good deal.', 'delivery, shopping', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 11, NULL, 'top-of-the-line', 'top-of-the-line', '顶级的；最高档的', '/tɑːp əv ðə laɪn/', 'of the best quality or among the most expensive of its kind', 'A top-of-the-line smartphone can replace a computer.', 'top-of-the-line, smartphone', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 12, NULL, 'have access to', 'have access to', '可以使用；可以访问', NULL, 'to have the right or opportunity to use or look at something', 'You''ll have access to the building with the card.', 'access, card', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 13, NULL, 'set somebody back', 'set somebody back', '使某人花费（金钱）', NULL, 'if something sets you back a certain amount of money, it costs you that much money', 'My daughter''s wedding set me back $20,000.', 'set back, cost', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 14, NULL, 'make an exception', 'make an exception', '破例；作为例外', NULL, 'not to treat someone or something according to the usual rules', 'Would you kindly make an exception for us this time?', 'exception, shopping', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 15, NULL, 'credit card', 'credit card', '信用卡', '/ˈkredɪt kɑːrd/', 'a small plastic card used to buy things and services and pay for them later', 'Can I pay by credit card?', 'credit card, payment', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 16, NULL, 'password', 'password', '口令；密码', '/ˈpæswɜːrd/', 'a secret word or combination of letters or numbers used for identification', 'You won''t have access to the computer without the password.', 'password, payment', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 17, NULL, 'change', 'change', '找零；零钱', '/tʃeɪndʒ/', 'money returned to someone who has paid more than the cost', 'You''ve given me the wrong change.', 'change, cash', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 18, NULL, 'receipt', 'receipt', '发票；收据', '/rɪˈsiːt/', 'a piece of paper that proves money, goods, or information have been received', 'Make sure you are given a receipt for everything you buy.', 'receipt, shopping', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 19, NULL, 'return', 'return', '归还；退货', '/rɪˈtɜːrn/', 'to send, take, give, put, etc. something back to where it came from', 'The new TV broke, so they returned it to the shop.', 'return, refund', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'vocabulary', '购物词汇复习', 1, 'vocabulary', 20, NULL, 'refund', 'refund', '退款', '/ˈriːfʌnd/', 'an amount of money that is given back because you are not happy with a product or service', 'I took the radio back to the shop and asked for a refund.', 'refund, return', 1),

    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'discussion', '开口讨论', 2, 'discussion', 301, NULL, NULL, 'Where do you usually buy clothes, in a store or online? Why?', '你通常在哪里买衣服，实体店还是网上？为什么？', NULL, '实体店：可以试穿。网上：随时随地购物，衣服可能更常打折。', NULL, 'clothes, online shopping, store', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'discussion', '开口讨论', 2, 'discussion', 302, NULL, NULL, 'What do you think of bargaining? Will you bargain when buying something? Talk about your reasons.', '你怎么看待讨价还价？买东西时会还价吗？说说原因。', NULL, '积极面：保护自己的权益，尤其价格明显不合理时。消极面：有人会贪小便宜。', NULL, 'bargaining, shopping', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'discussion', '开口讨论', 2, 'discussion', 303, NULL, NULL, 'Do you have a credit card? When do you usually use it? Why do you think some people never apply for a credit card?', '你有信用卡吗？通常什么时候用？为什么有些人从不申请信用卡？', NULL, '可用于买贵重物品、资金不足时，或享受信用卡公司的优惠。有人不用以控制开支、避免银行费用或过度消费，移动支付也足够。', NULL, 'credit card, payment', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'discussion', '开口讨论', 2, 'discussion', 304, NULL, NULL, 'What methods of payment do you usually use? Why do you usually pay in this way?', '你通常使用哪些付款方式？为什么这样付款？', NULL, '现金：习惯或容易忘记银行卡密码。信用卡／借记卡：买电脑、手机等贵重物品。移动支付：很方便，也不用带银行卡或大量现金。', NULL, 'payment, cash, card', 1),
    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'discussion', '开口讨论', 2, 'discussion', 305, NULL, NULL, 'Have you ever bought any fake or low-quality products? How did you deal with it?', '你买过假货或低质量产品吗？你是怎么处理的？', NULL, '可说明产品、价格，以及是否投诉并要求退款，或因低价瑕疵产品很常见而接受了情况。', NULL, 'fake products, refund', 1),

    ('revision-one', 'Chapter 1 · Shopping', 'Lesson 10 · Revision One', 10, 'review', '章节复习', 3, 'review', 401, NULL, 'Shopping review', 'Review the shopping vocabulary, phrases, and discussion topics from Lessons 1–9.', '复习第 1–9 课的购物词汇、常用表达和讨论话题。', NULL, '本课为 Chapter 1 Shopping 的复习课。', NULL, 'review, shopping', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 12 · In a Restaurant (doc/111349_807_In a Restaurant.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'free of charge', 'free of charge', '免费', NULL, 'without having to pay', 'These leaflets are offered free of charge.', 'free of charge, restaurant', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'main course', 'main course', '主菜；大菜', NULL, 'the largest or most important part of a meal in which different parts are served separately', 'I had salmon for my main course.', 'main course, restaurant', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'special', 'special', '特色菜', '/ˈspeʃl/', 'a dish available in a restaurant on a particular day that is not usually available', 'Today''s specials are written on the board.', 'special, restaurant, menu', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'offer', 'offer', '提供；供应', '/ˈɔːfər/', 'to provide or supply something', 'The hotel offers great facilities for families.', 'offer, restaurant', 1),

    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Waiter', NULL, 'Good evening. May I take your order?', '晚上好。我可以为您点单吗？', NULL, NULL, NULL, 'take your order, restaurant', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Emma', NULL, 'Yes, I would like to have the salad, please, and I think the bread and butter is free of charge?', '好的，我想要一份沙拉。面包和黄油是免费的吗？', NULL, NULL, NULL, 'salad, free of charge', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Waiter', NULL, 'Yes, bread and butter is free. Are you interested in a main course?', '是的，面包和黄油免费。您想点主菜吗？', NULL, NULL, NULL, 'main course, free', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Emma', NULL, 'Yes. Do you have any specials tonight?', '想。今晚有特色菜吗？', NULL, NULL, NULL, 'specials, restaurant', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Waiter', NULL, 'Of course. Tonight we''re offering lobster for only twenty dollars.', '当然有。今晚我们提供龙虾，只要 20 美元。', NULL, NULL, NULL, 'offer, lobster, special', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Emma', NULL, 'Okay. I''ll take it!', '好，我就要这个！', NULL, NULL, NULL, 'I''ll take it, order', 1),

    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Hi, I''m George. I''ll be your waiter this evening. Are you ready to order, or do you need a few more minutes?', '您好，我是 George，今晚由我为您服务。您准备好点餐了吗，还是还需要几分钟？', NULL, '根据课件提示补全。', NULL, 'ready to order, waiter', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I''m ready. I would like to have the mixed salad.', '我准备好了。我想要一份综合沙拉。', NULL, NULL, NULL, 'mixed salad, order', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Okay. What would you like to have for the main course?', '好的。您的主菜想要什么？', NULL, NULL, NULL, 'main course, order', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Well, do you have any specials?', '嗯，你们有特色菜吗？', NULL, NULL, NULL, 'specials, restaurant', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Yes. We are offering the roast chicken with vegetables tonight.', '有。今晚我们提供配蔬菜的烤鸡。', NULL, NULL, NULL, 'offer, roast chicken', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'I''ll have it! And I think the soup is free of charge?', '我就要这个！另外汤是免费的吗？', NULL, NULL, NULL, 'free of charge, soup', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'Yes, it''s free.', '是的，免费。', NULL, NULL, NULL, 'free, restaurant', 1),

    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'How often do you eat at restaurants? Why? Who do you usually go with when you eat at restaurants?', '你多久去一次餐馆？为什么？通常和谁一起去？', NULL, '可用 once/twice/three times a week/month/year；很少去可说喜欢在家吃，更便宜、更健康；同伴可以是父母、朋友或同事。', NULL, 'restaurant, dining habits', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you like to try new restaurants, or do you prefer to go to those you have already been to? Why?', '你喜欢尝试新餐馆，还是更喜欢去已经去过的餐馆？为什么？', NULL, '尝试新店：品尝不同菜肴、获得新体验、了解新菜系和文化。常去同一家：熟悉环境和菜品，节省点单时间，避免不喜欢的食物。', NULL, 'new restaurants, dining', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Some experts say that most people have unhealthy eating habits. Do you agree or disagree? Do you know how to develop healthy eating habits?', '一些专家说大多数人的饮食习惯不健康。你同意吗？怎样培养健康饮食习惯？', NULL, '可谈多吃蔬菜、水果和坚果等天然食物，避免加工食品，记录饮食，并每天规律用餐。', NULL, 'healthy eating habits, food', 1),

    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'May I take your order?\nDo you have any specials?', '复习：free of charge / main course / special / offer。', NULL, NULL, NULL, 'review, restaurant', 1),

    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'appetizer', 'appetizer', '前菜；开胃菜', NULL, NULL, NULL, 'appetizer, restaurant', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'entrée / main course', 'entrée / main course', '主菜', NULL, NULL, NULL, 'entrée, main course', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'dessert', 'dessert', '甜品；甜点', NULL, NULL, NULL, 'dessert, restaurant', 1),
    ('in-a-restaurant', 'Chapter 2 · Dining', 'Lesson 12 · In a Restaurant', 12, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'well-done / medium well / medium / medium rare / rare', 'well-done / medium well / medium / medium rare / rare', '牛排熟度：全熟／七分熟／五分熟／三分熟／一分熟', NULL, 'Steak doneness levels.', NULL, 'steak, doneness', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 13 · In the Food Court (doc/111350_807_In the Food Court.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'be in the mood (for something / to do something)', 'be in the mood (for something / to do something)', '想要做……；有心情做……', NULL, 'to feel like doing or having something', 'I''m not really in the mood for shopping.', 'in the mood, food court', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'department store', 'department store', '百货公司；商场', '/dɪˈpɑːrtmənt stɔːr/', 'a large shop divided into several parts, each selling different things', 'She took a job as a sales assistant in the sports section of a department store.', 'department store, shopping', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'enormous', 'enormous', '巨大的；庞大的', '/ɪˈnɔːrməs/', 'extremely large', 'There is an enormous house there.', 'enormous, food court', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'food court', 'food court', '美食广场；饮食区', '/fuːd kɔːrt/', 'a large area, often in a shopping center, with small restaurants and shared tables', 'There is a food court in the center of the mall.', 'food court, mall', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'review', 'review', '评论；评价', '/rɪˈvjuː/', 'to consider something in order to make changes, study it, or give an opinion about it', 'The movie was reviewed in the newspaper.', 'review, restaurant', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'vocabulary', '核心词汇', 1, 'vocabulary', 6, NULL, 'appetite', 'appetite', '食欲；胃口', '/ˈæpɪtaɪt/', 'the feeling that you want to eat food', 'I don''t have much of an appetite.', 'appetite, food', 1),

    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Larry', NULL, 'Are we still on for dinner tonight? I''m already getting hungry.', '我们今晚还去吃饭吗？我已经饿了。', NULL, NULL, NULL, 'dinner, hungry', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Tina', NULL, 'Sure! What do you have in mind?', '当然！你有什么想法？', NULL, NULL, NULL, 'have in mind, dinner', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Larry', NULL, 'I''d like a big meal in the evening. What about you? What are you in the mood for?', '晚上我想吃顿大餐。你呢？你想吃什么？', NULL, NULL, NULL, 'big meal, in the mood', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Tina', NULL, 'We should head over to the new department store. They''ve got an enormous food court with loads of different restaurants. There are supposed to be Japanese, Korean, Thai restaurants and so on.', '我们应该去那家新百货商场。那里有一个很大的美食广场，有很多不同的餐馆，据说有日餐、韩餐、泰餐等等。', NULL, NULL, NULL, 'department store, enormous food court', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Larry', NULL, 'My friend gave great reviews of the Mexican and Italian places. Are you in the mood for a taco or a burrito? Or maybe some pasta?', '我朋友对墨西哥餐和意大利餐评价很好。你想吃墨西哥卷饼、玉米煎饼，还是意面？', NULL, NULL, NULL, 'reviews, taco, burrito, pasta', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Tina', NULL, 'I think I have more of an appetite for Italian food right now.', '我觉得我现在更想吃意大利菜。', NULL, NULL, NULL, 'appetite, Italian food', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Larry', NULL, 'Let''s definitely go there.', '那我们一定去那里。', NULL, NULL, NULL, 'definitely, restaurant', 1),

    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'practice', '情景补全对话', 3, 'practice', 201, 'Larry', NULL, 'Are we still on for dinner tonight? I''m already getting hungry.', '我们今晚还去吃饭吗？我已经饿了。', NULL, '根据课件答案补全。', NULL, 'dinner, hungry', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'practice', '情景补全对话', 3, 'practice', 202, 'Tina', NULL, 'Sure! What do you have in mind?', '当然！你有什么想法？', NULL, NULL, NULL, 'have in mind, dinner', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'practice', '情景补全对话', 3, 'practice', 203, 'Larry', NULL, 'I''d like a big meal in the evening. What about you? What are you in the mood for?', '晚上我想吃顿大餐。你呢？你想吃什么？', NULL, NULL, NULL, 'big meal, in the mood', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'practice', '情景补全对话', 3, 'practice', 204, 'Tina', NULL, 'We should head over to the new department store. They''ve got an enormous food court with loads of different restaurants. There are supposed to be Japanese, Korean, Thai restaurants and so on.', '我们应该去那家新百货商场。那里有一个很大的美食广场，里面有很多不同的餐馆，据说有日餐、韩餐、泰餐等等。', NULL, NULL, NULL, 'department store, food court', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'practice', '情景补全对话', 3, 'practice', 205, 'Larry', NULL, 'My friend gave great reviews of the Mexican and Italian places. Are you in the mood for a taco or a burrito? Or maybe some pasta?', '我朋友对墨西哥餐和意大利餐评价很好。你想吃墨西哥卷饼、玉米煎饼，还是意面？', NULL, NULL, NULL, 'reviews, Mexican food', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'practice', '情景补全对话', 3, 'practice', 206, 'Tina', NULL, 'I think I have more of an appetite for Mexican food right now.', '我觉得我现在更想吃墨西哥菜。', NULL, NULL, NULL, 'appetite, Mexican food', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'practice', '情景补全对话', 3, 'practice', 207, 'Larry', NULL, 'Then let''s go to the Mexican restaurant!', '那我们去墨西哥餐厅吧！', NULL, NULL, NULL, 'Mexican restaurant, dinner', 1),

    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you had a meal in the food court recently? Can you describe the meal in detail?', '你最近在美食广场吃过饭吗？请详细描述这顿饭。', NULL, '可谈和谁去、点了什么、价格如何，以及是否满意。', NULL, 'food court, meal, experience', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you like eating in the food court? Why or why not? Explain with details.', '你喜欢在美食广场吃饭吗？为什么？请详细说明。', NULL, '喜欢：菜系选择多、通常比正规餐厅便宜。不喜欢：拥挤、希望安静环境、很难决定点什么。', NULL, 'food court, dining', 1),

    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'What do you have in mind?\nWhat are you in the mood for?\nI have more of an appetite for ... right now.', '复习：be in the mood / department store / appetite / enormous / food court / review。', NULL, NULL, NULL, 'review, food court', 1),

    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Typical North American and European food courts', 'Typical North American and European food courts consist of fast food chains such as McDonald''s and KFC, as well as a few small private vendors. Cuisines and choices are varied, with larger food courts offering more global choices.', '典型的北美和欧洲美食广场包含麦当劳、肯德基等快餐连锁店和一些小型私营摊贩；规模更大的美食广场提供更多全球化选择。', NULL, NULL, NULL, 'food court, cuisine', 1),
    ('in-the-food-court', 'Chapter 2 · Dining', 'Lesson 13 · In the Food Court', 13, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Typical Asian and African food courts', 'Asian and African food courts are mostly private vendors that offer local cuisines. In Singapore, food courts and hawker centers are the people''s main eating choice when dining out.', '亚洲和非洲的美食广场大多由提供本地菜系的私营摊贩组成；在新加坡，美食广场和小贩中心是人们外出就餐的主要选择。', NULL, NULL, NULL, 'food court, hawker center', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 14 · At the Café (doc/111351_807_At the Café.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'mocha', 'mocha', '摩卡咖啡；摩卡', '/ˈmoʊkə/', 'a type of strong coffee; or a mixture or flavouring of coffee and chocolate', 'In Europe, “mocha coffee” can refer either to a chocolate-flavoured drink or simply to coffee.', 'mocha, coffee, cafe', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'cappuccino', 'cappuccino', '卡布奇诺咖啡', '/ˌkæpuˈtʃiːnoʊ/', 'a coffee made with heated milk and steamed milk foam', 'I''d like a cup of cappuccino.', 'cappuccino, coffee, cafe', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'espresso', 'espresso', '浓缩咖啡', '/eˈspresoʊ/', 'strong coffee made by forcing hot water through crushed coffee beans and served without milk', 'Would you like an extra shot of espresso in your cappuccino?', 'espresso, coffee, cafe', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'brownie', 'brownie', '巧克力果仁小蛋糕；布朗尼', '/ˈbraʊni/', 'a small square chocolate cake, often with nuts in it', 'Brownies and chocolate bars will be served after the main meal.', 'brownie, dessert, cafe', 1),

    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Salesman', NULL, 'Hi, what can I get you?', '您好，您想要点什么？', NULL, NULL, NULL, 'what can I get you, cafe', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Daniel', NULL, 'I''ll have a large mocha with cream, and a small cappuccino.', '我要一大杯加奶油的摩卡和一小杯卡布奇诺。', NULL, NULL, NULL, 'mocha, cappuccino', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Salesman', NULL, 'Would you like anything else?', '您还需要别的吗？', NULL, NULL, NULL, 'anything else, order', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Daniel', NULL, 'Yes, I''d also like an espresso and a brownie, please.', '是的，我还想要一杯浓缩咖啡和一块布朗尼。', NULL, NULL, NULL, 'espresso, brownie', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Salesman', NULL, 'Are they for here or to go?', '在这里吃还是带走？', NULL, NULL, NULL, 'for here or to go, cafe', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Daniel', NULL, 'To go.', '带走。', NULL, NULL, NULL, 'to go, takeaway', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Salesman', NULL, 'Your total comes to $12.', '一共是 12 美元。', NULL, NULL, NULL, 'total, price', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Daniel', NULL, 'Here you go.', '给您。', NULL, NULL, NULL, 'here you go, payment', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'dialogue', '示范对话', 2, 'dialogue', 109, 'Salesman', NULL, 'Here''s your change. Thank you.', '这是您的找零。谢谢。', NULL, NULL, NULL, 'change, payment', 1),

    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Excuse me, Miss.', '打扰一下，小姐。', NULL, '根据课件提示补全。', NULL, 'cafe, order', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes, what can I get you?', '您好，您想要点什么？', NULL, NULL, NULL, 'what can I get you, cafe', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'A large mocha, please.', '请给我一大杯摩卡。', NULL, NULL, NULL, 'mocha, cafe', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Anything else?', '还需要别的吗？', NULL, NULL, NULL, 'anything else, order', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'A brownie, please.', '请再来一块布朗尼。', NULL, NULL, NULL, 'brownie, cafe', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Are they for here or to go?', '在这里吃还是带走？', NULL, NULL, NULL, 'for here or to go', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'To go.', '带走。', NULL, NULL, NULL, 'to go, takeaway', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'practice', '情景补全对话', 3, 'practice', 208, 'B', NULL, 'That will be $8.', '一共 8 美元。', NULL, NULL, NULL, 'price, payment', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'practice', '情景补全对话', 3, 'practice', 209, 'A', NULL, 'Here you go. Thank you very much.', '给您。非常感谢。', NULL, NULL, NULL, 'here you go, payment', 1),

    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you like coffee? What type of coffee do you often drink? How often do you drink coffee?', '你喜欢咖啡吗？常喝哪种咖啡？多久喝一次？', NULL, '咖啡类型：espresso / cappuccino / mocha / latte。频率：每天、每周三四次、每周一次、很少或从不；不喝咖啡也可谈茶、果汁、牛奶或豆浆。', NULL, 'coffee, cafe, habit', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'What is your favorite drink? Can you describe it with details?', '你最喜欢的饮料是什么？请详细描述。', NULL, '可说明饮料是什么、是买的还是在家做的、哪类人最常喝，以及喜欢它的原因。', NULL, 'favorite drink, cafe', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Can you describe a café you have recently visited?', '你能描述一家最近去过的咖啡馆吗？', NULL, '可谈咖啡馆的样子、位置、吃了什么喝了什么，以及喜欢或不喜欢它的原因。', NULL, 'cafe, description', 1),

    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'What can I get you?\nWould you like anything else?\nAre they for here or to go?\nYour total comes to ... / That will be ...\nHere you go. / Here you are.', '复习：mocha / cappuccino / espresso / brownie。', NULL, NULL, NULL, 'review, cafe', 1),

    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'solo / one shot of espresso', 'solo / one shot of espresso', '一份浓缩咖啡', NULL, NULL, NULL, 'espresso, shot', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'double / triple shots', 'double / triple shots', '双份／三份浓缩咖啡', NULL, NULL, NULL, 'espresso, shot', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'whole / low-fat / non-fat milk', 'whole / low-fat / non-fat milk', '全脂／低脂／脱脂牛奶', NULL, NULL, NULL, 'milk, coffee', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'less / half / extra syrup', 'less / half / extra syrup', '少糖浆／半糖浆／加糖浆', NULL, NULL, NULL, 'syrup, coffee', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'milk foam', 'milk foam', '奶泡', NULL, NULL, NULL, 'milk foam, coffee', 1),
    ('at-the-cafe', 'Chapter 2 · Dining', 'Lesson 14 · At the Café', 14, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'cream', 'cream', '奶油', NULL, NULL, NULL, 'cream, coffee', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 15 · Eating Junk Food (doc/111352_807_Eating Junk Food.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'on a diet', 'on a diet', '节食减肥', '/ˈdaɪət/', 'trying to lose weight by eating less food or specific foods', 'I don''t eat any cake because I''m on a diet.', 'on a diet, weight loss', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'junk food', 'junk food', '垃圾食品；不利健康的食品', '/ˈdʒʌŋk fuːd/', 'food that is unhealthy because it is high in fat, sugar, or artificial substances', 'Children in America are exposed to many television advertisements for junk food.', 'junk food, health', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'lollipop', 'lollipop', '棒棒糖', '/ˈlɑːlipɑːp/', 'a hard sweet on a stick', 'George Smith put hard candy on a stick and called it a “lollipop.”', 'lollipop, junk food', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'addictive', 'addictive', '让人上瘾的', '/əˈdɪktɪv/', 'an addictive activity or food is one that you cannot stop doing or eating once you have started', 'These hamburgers are addictive — I can''t stop eating them.', 'addictive, junk food', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'in moderation', 'in moderation', '适度；有节制地', '/ˌmɑːdəˈreɪʃn/', 'not too much; within reasonable limits', 'My doctor advised me to eat anything I want as long as it''s in moderation.', 'in moderation, healthy eating', 1),

    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Laura', NULL, 'What''d you have for lunch today?', '你今天午饭吃了什么？', NULL, NULL, NULL, 'lunch, food', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Ben', NULL, 'I had sushi with a salad.', '我吃了寿司和沙拉。', NULL, NULL, NULL, 'sushi, salad', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Laura', NULL, 'Oh, sounds healthy.', '哦，听起来很健康。', NULL, NULL, NULL, 'healthy, food', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Ben', NULL, 'I''m watching my weight.', '我在控制体重。', NULL, NULL, NULL, 'watch your weight, diet', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Laura', NULL, 'You don''t need to go on a diet. You look fine.', '你不用节食。你看起来很好。', NULL, NULL, NULL, 'go on a diet, weight', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Ben', NULL, 'I know, but I''ve been eating too much junk food lately, like too many lollipops, packets of chips, and lots of chocolate bars.', '我知道，但我最近吃了太多垃圾食品，比如太多棒棒糖、薯片和巧克力棒。', NULL, NULL, NULL, 'junk food, lately', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Laura', NULL, 'I know, those potato chips are really addictive. You just can''t stop.', '我知道，那些薯片真的很容易让人上瘾。你就是停不下来。', NULL, NULL, NULL, 'addictive, potato chips', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Ben', NULL, 'So I''m trying to be healthy for a few weeks.', '所以我想健康饮食几周。', NULL, NULL, NULL, 'healthy, diet', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'dialogue', '示范对话', 2, 'dialogue', 109, 'Laura', NULL, 'Well, everything in moderation.', '嗯，凡事都要适度。', NULL, NULL, NULL, 'everything in moderation, health', 1),

    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Lucy, do you like fish and chips?', 'Lucy，你喜欢炸鱼薯条吗？', NULL, '根据课件提示补全。', NULL, 'fish and chips, junk food', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Yes, fish and chips are my favorite. However, I''m watching my weight.', '是的，炸鱼薯条是我的最爱。不过我在控制体重。', NULL, NULL, NULL, 'watch my weight, diet', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'You don''t need to go on a diet. You look fine.', '你不用节食。你看起来很好。', NULL, NULL, NULL, 'go on a diet, weight', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'But I''ve been eating too much junk food lately.', '但我最近吃了太多垃圾食品。', NULL, NULL, NULL, 'junk food, lately', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Like what?', '比如什么？', NULL, NULL, NULL, 'food, question', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'Like too many hamburgers, sandwiches, potato chips, and lots of Coca-Cola.', '比如太多汉堡、三明治、薯片和可乐。', NULL, NULL, NULL, 'hamburgers, chips, Coca-Cola', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'I know. Those potato chips are really addictive. You just can''t stop.', '我知道。那些薯片真的很容易让人上瘾。你就是停不下来。', NULL, NULL, NULL, 'addictive, potato chips', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'practice', '情景补全对话', 3, 'practice', 208, 'B', NULL, 'So I''m trying to be healthy for a few weeks.', '所以我想健康饮食几周。', NULL, NULL, NULL, 'healthy, diet', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'practice', '情景补全对话', 3, 'practice', 209, 'A', NULL, 'Sure. Everything in moderation.', '当然。凡事都要适度。', NULL, NULL, NULL, 'everything in moderation, health', 1),

    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Do you like to eat junk food? When was the last time you ate it?', '你喜欢吃垃圾食品吗？上一次是什么时候吃的？', NULL, '可说喜欢什么、多久吃一次、上次吃了什么、何时何地吃的、和谁一起，以及是否喜欢那顿饭。', NULL, 'junk food, eating habit', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Junk food has become a part of modern popular culture. Why do so many people enjoy eating junk food?', '垃圾食品已成为现代流行文化的一部分。为什么这么多人喜欢吃垃圾食品？', NULL, '可谈味道好而令人上瘾、容易买到且节省时间、比其他菜便宜。', NULL, 'junk food, popular culture', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Fast food is bad. Do you agree or disagree with this argument?', '快餐有害。你同意还是不同意这个观点？', NULL, '可谈肥胖、糖尿病等健康问题；塑料包装对环境的影响；不良饮食习惯；也可用 everything in moderation 表达适度的观点。', NULL, 'fast food, health, environment', 1),

    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'What''d you have for lunch?\nI''m watching my weight.\nI''ve been eating too much junk food lately.\nEverything in moderation.', '复习：on a diet / junk food / lollipop / addictive / in moderation。', NULL, NULL, NULL, 'review, junk food', 1),

    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Junk food composition', 'Junk food consists largely of excess fat, simple carbohydrates, and processed sugar.', '垃圾食品主要由过量脂肪、简单碳水化合物和加工糖组成。', NULL, '课后拓展：垃圾食品对健康的影响。', NULL, 'junk food, nutrition', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Health risks of junk food', 'It contributes to an increased risk of obesity, cardiovascular disease, and many other chronic health conditions.', '它会增加肥胖、心血管疾病和许多慢性健康问题的风险。', NULL, '课后拓展：垃圾食品对健康的影响。', NULL, 'obesity, cardiovascular disease', 1),
    ('eating-junk-food', 'Chapter 2 · Dining', 'Lesson 15 · Eating Junk Food', 15, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'pig out on', 'Consumers also tend to pig out on junk food in one sitting, which is bad for their stomach.', '消费者也常一口气狼吞虎咽地吃很多垃圾食品，这对胃不好。', NULL, 'pig out on = 狼吞虎咽地吃很多。', NULL, 'pig out on, junk food', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 16 · Chinese Food (doc/111353_807_Chinese Food.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'divide', 'divide', '把……分成（若干部分）', '/dɪˈvaɪd/', 'to cause something to separate into parts or groups', 'After the Second World War, Germany was divided into two separate countries.', 'divide, cuisine', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'cuisine', 'cuisine', '烹饪法；菜肴；菜系', '/kwɪˈziːn/', 'a style of cooking', 'Most countries differ from one another in language, culture, cuisine, clothing, and music.', 'cuisine, Chinese food', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'mapo tofu', 'mapo tofu', '麻婆豆腐', NULL, 'a dish of tofu in a spicy sauce based on bean paste and fermented black beans, often with minced pork', 'Mapo tofu is also called Mapo bean curd.', 'mapo tofu, Sichuan cuisine', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'yuxiang shredded pork', 'yuxiang shredded pork', '鱼香肉丝', NULL, 'a mildly sour dish with shredded pork, vegetables, pickled pepper, sugar, ginger, and garlic; it does not contain fish', 'Yuxiang shredded pork is also called fish-flavoured pork slices.', 'yuxiang shredded pork, Sichuan cuisine', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'vocabulary', '核心词汇', 1, 'vocabulary', 5, NULL, 'recommendation', 'recommendation', '建议；推荐', '/ˌrekəmenˈdeɪʃn/', 'a suggestion that something is good or suitable for a particular purpose or job', 'I don''t know what to choose. What''s your recommendation?', 'recommendation, food', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'vocabulary', '核心词汇', 1, 'vocabulary', 6, NULL, 'light', 'light', '清淡的', '/laɪt/', 'not containing much fat or having a strong flavour, so easy for the stomach to digest', 'The soup itself was light, fragrant, and slightly sweet.', 'light, food, flavour', 1),

    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Kelly', NULL, 'Excuse me, I''d like to try some Chinese food.', '打扰一下，我想尝尝中国菜。', NULL, NULL, NULL, 'Chinese food, restaurant', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Waiter', NULL, 'We serve authentic Chinese food. Which style do you prefer?', '我们提供正宗中国菜。您喜欢哪种菜系？', NULL, NULL, NULL, 'authentic, style, cuisine', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Kelly', NULL, 'I know nothing about Chinese food. Could you give me some suggestions?', '我不了解中国菜。您能给我一些建议吗？', NULL, NULL, NULL, 'suggestion, Chinese food', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Waiter', NULL, 'It''s divided into eight regional cuisines, such as Cantonese food, Shandong food, and Sichuan food.', '中国菜分为八大菜系，例如粤菜、鲁菜和川菜。', NULL, NULL, NULL, 'divide, regional cuisines', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Kelly', NULL, 'Is there any difference?', '它们有什么不同吗？', NULL, NULL, NULL, 'difference, cuisine', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Waiter', NULL, 'Yes, Cantonese food is lighter while Sichuan dishes are spicy and hot. They taste different.', '有。粤菜更清淡，川菜则香辣。它们的味道不同。', NULL, NULL, NULL, 'light, spicy, cuisine', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Kelly', NULL, 'Oh, really? I like hot food. So what is your recommendation for me?', '哦，真的吗？我喜欢辣的食物。那么您推荐我吃什么？', NULL, NULL, NULL, 'recommendation, spicy food', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Waiter', NULL, 'I think mapo tofu and yuxiang shredded pork are quite special and delicious. I recommend the Sichuan food dining room on the third floor.', '我觉得麻婆豆腐和鱼香肉丝非常有特色，也很美味。我推荐三楼的川菜餐厅。', NULL, NULL, NULL, 'mapo tofu, yuxiang shredded pork', 1),

    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'I would like to try some Chinese food.', '我想尝尝中国菜。', NULL, '根据课件答案补全。', NULL, 'Chinese food, restaurant', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'Which style do you prefer?', '您喜欢哪种菜系？', NULL, NULL, NULL, 'style, cuisine', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Um, I have no idea. Could you give me some suggestions?', '嗯，我不太清楚。您能给我一些建议吗？', NULL, NULL, NULL, 'suggestions, Chinese food', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'Chinese food is divided into eight cuisines. For example, Sichuan dishes are spicy and taste heavier, while Cantonese food is lighter. They taste different.', '中国菜分为八大菜系。例如川菜香辣、口味较重，而粤菜更清淡。它们味道不同。', NULL, NULL, NULL, 'divide, cuisine, light, spicy', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Wow, that sounds great! I love spicy food. What''s your recommendation for me?', '哇，听起来不错！我喜欢辣的食物。您推荐我吃什么？', NULL, NULL, NULL, 'spicy food, recommendation', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'I think mapo tofu and yuxiang shredded pork are quite good for you.', '我觉得麻婆豆腐和鱼香肉丝很适合您。', NULL, NULL, NULL, 'mapo tofu, yuxiang shredded pork', 1),

    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'What''s your favorite cuisine apart from Chinese food? Why do you like it most? Explain the reason in detail.', '除了中国菜以外，你最喜欢什么菜系？为什么？请详细说明。', NULL, '可以谈韩餐、日餐、法餐、意餐、印度菜或快餐；理由可从口味、节省时间和金钱、方便等方面说。', NULL, 'cuisine, favourite food', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'What is your favorite Chinese food? What is the taste? Do you know how it is cooked? Try to describe it in detail.', '你最喜欢的中国菜是什么？味道如何？你知道怎么做吗？请详细描述。', NULL, '味道可用 light/heavy/sweet/spicy/sour；烹饪方法可用 boiled/fried/steamed/smoked/stewed/deep-fried/roasted/chopped/diced/sliced。', NULL, 'Chinese food, cooking, flavour', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'Do you like to dine out or eat at home? Try to explain the reason in detail.', '你喜欢外出就餐还是在家吃？请详细解释原因。', NULL, '外出就餐：环境和服务好、节省时间、不用清理厨房、适合约会和家庭聚会。在家吃：更健康、更便宜，也能自行设计食谱。', NULL, 'dine out, eat at home', 1),

    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'We serve authentic Chinese food. Which style do you prefer?\nCould you give me some suggestions?\nWhat is your recommendation for me?\nCantonese food is lighter while Sichuan dishes are spicy and hot. They taste different.', '复习：divide / cuisine / recommendation / light / mapo tofu / yuxiang shredded pork。', NULL, NULL, NULL, 'review, Chinese food', 1),

    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'chili', 'chili', '小尖椒；红辣椒', NULL, 'Common ingredient of Sichuan cuisine.', NULL, 'chili, Sichuan cuisine', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'pepper', 'pepper', '辣椒；胡椒；胡椒粉', NULL, 'Common ingredient of Sichuan cuisine.', NULL, 'pepper, Sichuan cuisine', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'prickly ash', 'prickly ash', '花椒', NULL, 'Common ingredient of Sichuan cuisine.', NULL, 'prickly ash, Sichuan cuisine', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'fermented soya beans', 'fermented soya beans', '豆豉', NULL, 'Common ingredient of Sichuan cuisine.', NULL, 'fermented soya beans, Sichuan cuisine', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'extra', '拓展学习', 6, 'extra', 505, NULL, 'scallions', 'scallions', '大葱；青葱', NULL, 'Common ingredient of Sichuan cuisine.', NULL, 'scallions, Sichuan cuisine', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'extra', '拓展学习', 6, 'extra', 506, NULL, 'coriander', 'coriander', '香菜', NULL, 'Common ingredient of Sichuan cuisine.', NULL, 'coriander, Sichuan cuisine', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'extra', '拓展学习', 6, 'extra', 507, NULL, 'aniseed', 'aniseed', '八角；茴香', NULL, 'Common ingredient of Sichuan cuisine.', NULL, 'aniseed, Sichuan cuisine', 1),
    ('chinese-food', 'Chapter 2 · Dining', 'Lesson 16 · Chinese Food', 16, 'extra', '拓展学习', 6, 'extra', 508, NULL, 'cumin', 'cumin', '孜然', NULL, 'Common ingredient of Sichuan cuisine.', NULL, 'cumin, Sichuan cuisine', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 17 · Ordering Food by Phone (doc/111354_807_Ordering Food by Phone.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'grocery', 'grocery', '食品杂货', '/ˈɡroʊsəri/', 'food that you buy in a grocer''s shop or supermarket', 'Many people buy their groceries online.', 'grocery, order', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'vanilla', 'vanilla', '香草；香草味', '/vəˈnɪlə/', 'a substance from the seeds of a tropical plant, used to flavour sweet foods', 'We have three flavours of ice cream: vanilla, chocolate, and strawberry.', 'vanilla, grocery', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'vocabulary', '核心词汇', 1, 'vocabulary', 3, NULL, 'syrup', 'syrup', '糖浆', '/ˈsɪrəp/', 'a very sweet, thick liquid', 'Corn syrup and cough syrup are common examples.', 'syrup, grocery', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'vocabulary', '核心词汇', 1, 'vocabulary', 4, NULL, 'delivery staff', 'delivery staff', '送货员；外卖送餐员（集合）', '/dɪˈlɪvəri stæf/', 'a group of people who deliver merchandise from a store to customers'' homes or offices; staff is a collective noun', 'He works as a delivery staff member for a cafe.', 'delivery staff, delivery', 1),

    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Wesley', NULL, 'Good morning. I''d like to order some groceries, please.', '早上好。我想订一些食品杂货。', NULL, NULL, NULL, 'order, groceries', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Salesman', NULL, 'Sure, what''d you like to order?', '当然，您想订什么？', NULL, NULL, NULL, 'order, groceries', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Wesley', NULL, 'Well, I need a medium bottle of vanilla essence, a small bottle of chocolate syrup, and some dark chocolate cubes. When can I expect the delivery?', '我需要一中瓶香草精、一小瓶巧克力糖浆和一些黑巧克力块。预计什么时候送到？', NULL, NULL, NULL, 'vanilla, syrup, delivery', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Salesman', NULL, 'It''ll be delivered in about an hour. May I please have your name and address?', '大约一小时送到。请告诉我您的姓名和地址好吗？', NULL, NULL, NULL, 'delivery, name, address', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Wesley', NULL, 'Sure. My name is Wesley Thomas. The address is 34-B, George Street.', '当然。我叫 Wesley Thomas，地址是 George Street 34-B。', NULL, NULL, NULL, 'name, address, delivery', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Salesman', NULL, 'Alright. A delivery staff member will reach your place in about an hour.', '好的。一位送货员大约一小时后会到您那里。', NULL, NULL, NULL, 'delivery staff, delivery', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Wesley', NULL, 'What''s the total amount of the things that I just purchased?', '我刚买的这些东西总共多少钱？', NULL, NULL, NULL, 'total amount, purchase', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Salesman', NULL, 'That would be $25.', '一共 25 美元。', NULL, NULL, NULL, 'price, total', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'dialogue', '示范对话', 2, 'dialogue', 109, 'Wesley', NULL, 'Thank you.', '谢谢。', NULL, NULL, NULL, 'thanks, delivery', 1),

    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Hello, this is Garden Cuisine. What would you like to order?', '您好，这里是 Garden Cuisine。您想订什么？', NULL, '根据课件提示补全。', NULL, 'order, delivery', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I''d like to order some noodles and chicken dim sum for two, please.', '我想订两份面条和鸡肉点心。', NULL, NULL, NULL, 'order, noodles, dim sum', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'Is that all? Would you like to order some starters or soup?', '就这些吗？您想再订一些开胃菜或汤吗？', NULL, NULL, NULL, 'starters, soup, order', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'No thanks, that''s it.', '不用了，谢谢，就这些。', NULL, NULL, NULL, 'that''s it, order', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'May I have your address?', '可以告诉我您的地址吗？', NULL, NULL, NULL, 'address, delivery', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'My address is 42 Beverly Street. When can I expect the delivery?', '我的地址是 Beverly Street 42 号。预计什么时候送到？', NULL, NULL, NULL, 'address, expect delivery', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'Your order will be delivered within 30 minutes.', '您的订单会在 30 分钟内送达。', NULL, NULL, NULL, 'delivery, 30 minutes', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'practice', '情景补全对话', 3, 'practice', 208, 'B', NULL, 'What''s the total amount of the things that I just purchased?', '我刚买的这些东西总共多少钱？', NULL, NULL, NULL, 'total amount, price', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'practice', '情景补全对话', 3, 'practice', 209, 'A', NULL, 'That would be $14.', '一共 14 美元。', NULL, NULL, NULL, 'price, total', 1),

    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you ordered food on the phone? Try to talk about it in detail.', '你通过电话订过餐吗？请详细谈谈。', NULL, '可说明订了什么、花了多少钱，以及是否满意和原因。', NULL, 'order food, phone, experience', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'What are the advantages and disadvantages of ordering food on the phone?', '电话订餐有哪些优点和缺点？', NULL, '优点：直接和工作人员沟通，可避免外卖应用点单的常见错误。缺点：看不到完整菜单，工作人员可能听错电话内容。', NULL, 'phone order, advantages, disadvantages', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'What apps do you often use to order food? Is ordering food online popular in your country? Why or why not?', '你常用哪些应用点餐？网上订餐在你的国家流行吗？为什么？', NULL, '可谈年轻人常用 Meituan、Eleme 等应用；他们可能日程忙，或只是想享受配送的便利。', NULL, 'food delivery app, online order', 1),

    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'I''d like to order some ...\nWhen/What time can I expect the delivery?\nMay I please have your name and address?\nWhat''s the total amount of the things that I just purchased?', '复习：grocery / vanilla / syrup / delivery staff。', NULL, NULL, NULL, 'review, phone order', 1),

    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Food appearance affects appetite.', 'The appearance of food affects our appetite subconsciously. We prefer food served on a clean white plate; the same food in a cheap plastic box can make us lose our appetite.', '食物的外观会潜意识地影响食欲；同样的食物装在廉价塑料盒里可能使我们失去食欲。', NULL, '课后拓展：电话订餐的缺点。', NULL, 'appetite, takeout', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Long waits for takeout', 'When takeout takes longer than expected, we start guessing and may feel agitated until it arrives.', '外卖比预期更久时，我们会不断猜测，并在送到前感到焦虑不安。', NULL, '课后拓展：电话订餐的缺点。', NULL, 'takeout, wait, agitated', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Some foods are not suitable for takeout.', 'French fries are best served crispy and hot, but travel time can turn them cold and soft.', '有些食物不适合外卖；例如薯条最好酥脆且热，但运输会让它变冷变软。', NULL, '课后拓展：电话订餐的缺点。', NULL, 'takeout, French fries', 1),
    ('ordering-food-by-phone', 'Chapter 2 · Dining', 'Lesson 17 · Ordering Food by Phone', 17, 'extra', '拓展学习', 6, 'extra', 504, NULL, 'Food safety risk', 'Many restaurants do business without a license, and food may be produced in a filthy environment.', '一些餐馆无证经营，食物可能在肮脏环境中制作。', NULL, '课后拓展：电话订餐的缺点。', NULL, 'food safety, takeout', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

-- Lesson 18 · Reserving a Table at a Restaurant (doc/112062_807_Reserving a Table at a Restaurant.pdf)
INSERT INTO `daily_spoken_dialogue_item` (
    `lesson_code`, `chapter_title`, `lesson_title`, `lesson_order`,
    `section_code`, `section_title`, `section_order`, `item_type`, `item_order`,
    `speaker`, `item_title`, `english_text`, `chinese_text`, `pronunciation`,
    `explanation`, `examples`, `keywords`, `is_published`
) VALUES
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'vocabulary', '核心词汇', 1, 'vocabulary', 1, NULL, 'assist', 'assist', '帮助；协助', '/əˈsɪst/', 'to help', 'The company said it would assist workers in finding new jobs.', 'assist, restaurant', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'vocabulary', '核心词汇', 1, 'vocabulary', 2, NULL, 'reservation', 'reservation', '预约；预订', '/ˌrezərˈveɪʃn/', 'an arrangement in which a seat, table, or other place is kept for you', 'I''d like to make a table reservation for two people for 9 o''clock.', 'reservation, restaurant', 1),

    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'dialogue', '示范对话', 2, 'dialogue', 101, 'Waiter', NULL, 'Hello, this is Love Restaurant. How may I assist you?', '您好，这里是 Love Restaurant。我能帮您什么吗？', NULL, NULL, NULL, 'assist, restaurant', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'dialogue', '示范对话', 2, 'dialogue', 102, 'Cindy', NULL, 'I''d like to make a reservation for two.', '我想预订两人的座位。', NULL, NULL, NULL, 'make a reservation, table', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'dialogue', '示范对话', 2, 'dialogue', 103, 'Waiter', NULL, 'May I have your name, please?', '请问您叫什么名字？', NULL, NULL, NULL, 'name, reservation', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'dialogue', '示范对话', 2, 'dialogue', 104, 'Cindy', NULL, 'I''m Cindy Lautner.', '我是 Cindy Lautner。', NULL, NULL, NULL, 'name, reservation', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'dialogue', '示范对话', 2, 'dialogue', 105, 'Waiter', NULL, 'Okay, when is your reservation for?', '好的，您预订什么时间？', NULL, NULL, NULL, 'reservation time, restaurant', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'dialogue', '示范对话', 2, 'dialogue', 106, 'Cindy', NULL, 'It''s for tomorrow evening at 6 p.m.', '明天晚上 6 点。', NULL, NULL, NULL, 'reservation time, evening', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'dialogue', '示范对话', 2, 'dialogue', 107, 'Waiter', NULL, 'Okay, ma''am. Would you like the corner table or the middle?', '好的，女士。您想要角落的桌子还是中间的？', NULL, NULL, NULL, 'corner table, reservation', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'dialogue', '示范对话', 2, 'dialogue', 108, 'Cindy', NULL, 'In the corner with a window view.', '角落里靠窗的位置。', NULL, NULL, NULL, 'corner, window view', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'dialogue', '示范对话', 2, 'dialogue', 109, 'Waiter', NULL, 'Okay, done. We reserved your table for two for tomorrow evening.', '好的，办好了。我们已经为您预订明晚两人的座位。', NULL, NULL, NULL, 'reserved table, restaurant', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'dialogue', '示范对话', 2, 'dialogue', 110, 'Cindy', NULL, 'Yes, thanks a lot.', '好的，非常感谢。', NULL, NULL, NULL, 'thanks, reservation', 1),

    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'practice', '情景补全对话', 3, 'practice', 201, 'A', NULL, 'Hello, this is Love Restaurant. What may I assist you with?', '您好，这里是 Love Restaurant。我能帮您什么吗？', NULL, '根据课件提示补全。', NULL, 'assist, reservation', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'practice', '情景补全对话', 3, 'practice', 202, 'B', NULL, 'I''d like to make a reservation for two.', '我想预订两人的座位。', NULL, NULL, NULL, 'reservation, table', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'practice', '情景补全对话', 3, 'practice', 203, 'A', NULL, 'May I have your name, please?', '请问您叫什么名字？', NULL, NULL, NULL, 'name, reservation', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'practice', '情景补全对话', 3, 'practice', 204, 'B', NULL, 'I''m Laura Wong.', '我是 Laura Wong。', NULL, NULL, NULL, 'name, reservation', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'practice', '情景补全对话', 3, 'practice', 205, 'A', NULL, 'Okay, when is your reservation for?', '好的，您预订什么时间？', NULL, NULL, NULL, 'reservation time, restaurant', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'practice', '情景补全对话', 3, 'practice', 206, 'B', NULL, 'It''s for tomorrow evening at 6 p.m.', '明天晚上 6 点。', NULL, NULL, NULL, 'reservation time, evening', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'practice', '情景补全对话', 3, 'practice', 207, 'A', NULL, 'Okay, ma''am. Would you like the corner table or the middle?', '好的，女士。您想要角落的桌子还是中间的？', NULL, NULL, NULL, 'corner table, reservation', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'practice', '情景补全对话', 3, 'practice', 208, 'B', NULL, 'I''d like a table in the corner with a window view.', '我想要一张角落里靠窗的桌子。', NULL, NULL, NULL, 'corner, window view', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'practice', '情景补全对话', 3, 'practice', 209, 'A', NULL, 'Okay, done. We just reserved your table for two for tomorrow evening.', '好的，办好了。我们刚刚为您预订了明晚两人的座位。', NULL, NULL, NULL, 'reserved table, restaurant', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'practice', '情景补全对话', 3, 'practice', 210, 'B', NULL, 'Yes, thanks a lot.', '好的，非常感谢。', NULL, NULL, NULL, 'thanks, reservation', 1),

    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'discussion', '开口讨论', 4, 'discussion', 301, NULL, NULL, 'Have you ever made a dinner reservation? Describe that experience in detail. If you haven''t done so, imagine what you would do.', '你曾经预订过晚餐吗？请详细描述这次经历。如果没有，请设想一下你会怎么做。', NULL, '可谈餐馆是什么、为了什么预订、预订了哪种座位，以及预订人数。', NULL, 'dinner reservation, experience', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'discussion', '开口讨论', 4, 'discussion', 302, NULL, NULL, 'Do you think making a reservation for a meal is necessary? Why do you think so? Explain the reasons in detail.', '你认为预订用餐有必要吗？为什么？请详细说明。', NULL, '如果认为有必要，可谈节省等待时间，以及可以选择舒适、景观好的座位。', NULL, 'reservation, restaurant', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'discussion', '开口讨论', 4, 'discussion', 303, NULL, NULL, 'What kind of restaurants do you usually go to for business and for pleasure?', '你通常因为商务和休闲分别去什么类型的餐厅？', NULL, '可以谈墨西哥或韩国烧烤、自助餐、中国火锅等。', NULL, 'restaurant, business, pleasure', 1),

    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'review', '复习表达', 5, 'review', 401, NULL, 'Key expressions', 'What may I assist you with? / How may I assist you?\nI''d like to make a reservation for two.\nWhen is your reservation for?\nWould you like the corner table or the middle?', '复习：assist / reservation。', NULL, NULL, NULL, 'review, reservation', 1),

    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'extra', '拓展学习', 6, 'extra', 501, NULL, 'Do not reserve more places than you need.', 'Make reservations for no more people than you really are. Otherwise, the restaurant loses other potential reservations because of you.', '不要预订超过实际人数的座位，否则餐馆会失去其他潜在的预订。', NULL, '课后拓展：预订餐厅的注意事项。', NULL, 'reservation etiquette, restaurant', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'extra', '拓展学习', 6, 'extra', 502, NULL, 'Do not be wishy-washy about the time.', 'Do not be wishy-washy about the time.', '不要对时间犹豫不决。', NULL, 'wishy-washy = 犹豫不决的。', NULL, 'wishy-washy, reservation', 1),
    ('reserving-a-table', 'Chapter 2 · Dining', 'Lesson 18 · Reserving a Table at a Restaurant', 18, 'extra', '拓展学习', 6, 'extra', 503, NULL, 'Do not hang up too early.', 'Wait until the restaurant finishes asking all necessary questions before hanging up. Make sure to give all of your information.', '在餐馆问完所有必要问题前不要挂断电话，确保提供所有信息。', NULL, '课后拓展：预订餐厅的注意事项。', NULL, 'hang up, reservation', 1)
ON DUPLICATE KEY UPDATE
    `chapter_title` = VALUES(`chapter_title`), `lesson_title` = VALUES(`lesson_title`), `lesson_order` = VALUES(`lesson_order`),
    `section_code` = VALUES(`section_code`), `section_title` = VALUES(`section_title`), `section_order` = VALUES(`section_order`),
    `item_type` = VALUES(`item_type`), `speaker` = VALUES(`speaker`), `item_title` = VALUES(`item_title`),
    `english_text` = VALUES(`english_text`), `chinese_text` = VALUES(`chinese_text`), `pronunciation` = VALUES(`pronunciation`),
    `explanation` = VALUES(`explanation`), `examples` = VALUES(`examples`), `keywords` = VALUES(`keywords`),
    `is_published` = VALUES(`is_published`);

COMMIT;
