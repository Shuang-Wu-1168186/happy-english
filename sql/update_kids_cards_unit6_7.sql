# Migration: Unit 6 and Unit 7 word list continuation.
# Priorities 97-146 follow the photographed word list after the existing cards.

START TRANSACTION;

DELETE FROM `kids_english_card`
WHERE `priority_order` BETWEEN 97 AND 146;

INSERT INTO `kids_english_card`
(`word`, `translation`, `phonics`, `part_of_speech`, `level`, `syllables`, `stress`, `phonics_focus`, `syllable_tip`, `category`, `emoji`, `image_url`, `tip`, `priority_order`)
VALUES
('inventor', '发明家', '/ɪnˈventər/', 'noun', 'Core', 'in · ven · tor', 'in-VEN-tor', 'in → /ɪn/; ven → /ven/', '拆分练习：in · ven · tor。注意：in → /ɪn/; ven → /ven/。', 'Unit 6 · 18', '🧑‍🔬', NULL, NULL, 97),
('movable-type printing', '活字印刷术', '/ˌmuːvəbl taɪp ˈprɪntɪŋ/', 'noun', 'Core', 'mov · a · ble-type print · ing', 'MOV-a-ble-type PRINT-ing', '-able → /əbəl/; -ing → /ɪŋ/', '拆分练习：mov · a · ble-type print · ing。注意：-able → /əbəl/; -ing → /ɪŋ/。', 'Unit 6 · 18', '🖨️', NULL, NULL, 98),
('invention', '发明；创造；发明物', '/ɪnˈvenʃən/', 'noun', 'Core', 'in · ven · tion', 'in-VEN-tion', 'tion → /ʃən/', '拆分练习：in · ven · tion。注意：tion → /ʃən/。', 'Unit 6 · 18', '💡', NULL, NULL, 99),
('knowledge', '知识；学问', '/ˈnɒlɪdʒ/', 'noun', 'Core', 'knowl · edge', 'KNOWL-edge', 'kn → /n/; dge → /dʒ/', '拆分练习：knowl · edge。注意：kn → /n/; dge → /dʒ/。', 'Unit 6 · 18', '📚', NULL, NULL, 100),
('light bulb', '电灯泡', '/ˈlaɪt bʌlb/', 'noun', 'Core', 'light bulb', 'LIGHT BULB', 'igh → /aɪ/; u → /ʌ/', '拆分练习：light bulb。注意：igh → /aɪ/; u → /ʌ/。', 'Unit 6 · 18', '💡', NULL, NULL, 101),
('experiment', '实验', '/ɪkˈsperɪmənt/', 'noun', 'Core', 'ex · per · i · ment', 'ex-PER-i-ment', 'ex → /ɪk/; -ment → /mənt/', '拆分练习：ex · per · i · ment。注意：ex → /ɪk/; -ment → /mənt/。', 'Unit 6 · 18', '🧪', NULL, NULL, 102),
('poet', '诗人', '/ˈpoʊɪt/', 'noun', 'Core', 'po · et', 'PO-et', 'oe → /oʊ/', '拆分练习：po · et。注意：oe → /oʊ/。', 'Unit 6 · 18', '✍️', NULL, NULL, 103),
('friendship', '友谊', '/ˈfrendʃɪp/', 'noun', 'Core', 'friend · ship', 'FRIEND-ship', 'sh → /ʃ/', '拆分练习：friend · ship。注意：sh → /ʃ/。', 'Unit 6 · 18', '🤝', NULL, NULL, 104),
('recite', '背诵；熟记', '/rɪˈsaɪt/', 'verb', 'Core', 're · cite', 're-CITE', 'i_e → /aɪ/', '拆分练习：re · cite。注意：i_e → /aɪ/。', 'Unit 6 · 18', '🎤', NULL, NULL, 105),
('Germany', '德国（欧洲）', '/ˈdʒɜːrməni/', 'proper noun', 'Core', 'Ger · ma · ny', 'GER-ma-ny', 'g → /dʒ/; er → /ɜːr/', '拆分练习：Ger · ma · ny。注意：g → /dʒ/; er → /ɜːr/。', 'Unit 6 · 18', '🇩🇪', NULL, NULL, 106),
('lose', '丢失；丧失', '/luːz/', 'verb', 'Core', 'lose', 'LOSE', 'oo → /uː/; s → /z/', '拆分练习：lose。注意：oo → /uː/; s → /z/。', 'Unit 6 · 18', '🧤', NULL, NULL, 107),
('glow', '发光', '/ɡloʊ/', 'verb', 'Core', 'glow', 'GLOW', 'ow → /oʊ/', '拆分练习：glow。注意：ow → /oʊ/。', 'Unit 6 · 18', '✨', NULL, NULL, 108),
('spacesuit', '宇航服', '/ˈspeɪssuːt/', 'noun', 'Core', 'space · suit', 'SPACE-suit', 'a_e → /eɪ/; ui → /uː/', '拆分练习：space · suit。注意：a_e → /eɪ/; ui → /uː/。', 'Unit 6 · 18', '🧑‍🚀', NULL, NULL, 109),
('uniform', '制服', '/ˈjuːnɪfɔːrm/', 'noun', 'Core', 'u · ni · form', 'U-ni-form', 'u → /juː/; or → /ɔːr/', '拆分练习：u · ni · form。注意：u → /juː/; or → /ɔːr/。', 'Unit 6 · 18', '🧥', NULL, NULL, 110),
('mask', '口罩；防毒面具', '/mɑːsk/', 'noun', 'Core', 'mask', 'MASK', 'a → /ɑː/', '拆分练习：mask。注意：a → /ɑː/。', 'Unit 6 · 18', '😷', NULL, NULL, 111),
('speech', '演讲；发言', '/spiːtʃ/', 'noun', 'Core', 'speech', 'SPEECH', 'ee → /iː/; ch → /tʃ/', '拆分练习：speech。注意：ee → /iː/; ch → /tʃ/。', 'Unit 6 · 19', '🗣️', NULL, NULL, 112),
('dress', '穿衣；连衣裙', '/dres/', 'verb/noun', 'Core', 'dress', 'DRESS', 'short e → /e/', '拆分练习：dress。注意：short e → /e/。', 'Unit 6 · 19', '👗', NULL, NULL, 113),
('a pair of', '一双；一对', '/ə peər əv/', 'phrase', 'Core', 'a pair of', 'a PAIR of', 'ai → /eər/', '拆分练习：a pair of。注意：ai → /eər/。', 'Unit 6 · 19', '👟', NULL, NULL, 114),
('reuse', '再次利用；重复使用', '/ˌriːˈjuːz/', 'verb', 'Core', 're · use', 're-USE', 're- → /riː/; u_e → /uː/', '拆分练习：re · use。注意：re- → /riː/; u_e → /uː/。', 'Unit 6 · 20', '♻️', NULL, NULL, 115),
('cut down on', '减少；削减', '/kʌt daʊn ɒn/', 'phrase', 'Core', 'cut down on', 'CUT DOWN on', 'u → /ʌ/; ow → /aʊ/', '拆分练习：cut down on。注意：u → /ʌ/; ow → /aʊ/。', 'Unit 6 · 20', '📉', NULL, NULL, 116),
('in need', '处于需要……的状态', '/ɪn niːd/', 'phrase', 'Core', 'in need', 'in NEED', 'ee → /iː/', '拆分练习：in need。注意：ee → /iː/。', 'Unit 6 · 20', '🆘', NULL, NULL, 117),
('useless', '无用的；无价值的', '/ˈjuːsləs/', 'adjective', 'Core', 'use · less', 'USE-less', 'u_e → /uː/; -less → /ləs/', '拆分练习：use · less。注意：u_e → /uː/; -less → /ləs/。', 'Unit 6 · 20', '🗑️', NULL, NULL, 118),
('make use of', '利用', '/meɪk juːz əv/', 'phrase', 'Core', 'make use of', 'MAKE USE of', 'a_e → /eɪ/; use → /juːz/', '拆分练习：make use of。注意：a_e → /eɪ/; use → /juːz/。', 'Unit 6 · 20', '🛠️', NULL, NULL, 119),
('health', '健康', '/helθ/', 'noun', 'Core', 'health', 'HEALTH', 'ea → /e/; th → /θ/', '拆分练习：health。注意：ea → /e/; th → /θ/。', 'Unit 6 · 21', '❤️', NULL, NULL, 120),
('wrong', '问题；错误', '/rɒŋ/', 'adjective/noun', 'Core', 'wrong', 'WRONG', 'wr → /r/; ng → /ŋ/', '拆分练习：wrong。注意：wr → /r/; ng → /ŋ/。', 'Unit 6 · 21', '❌', NULL, NULL, 121),
('environment', '环境', '/ɪnˈvaɪrənmənt/', 'noun', 'Core', 'en · vi · ron · ment', 'en-VI-ron-ment', 'en → /ɪn/; vi → /vaɪ/', '拆分练习：en · vi · ron · ment。注意：en → /ɪn/; vi → /vaɪ/。', 'Unit 6 · 21', '🌳', NULL, NULL, 122),
('police', '警察', '/pəˈliːs/', 'noun', 'Core', 'po · lice', 'po-LICE', 'c → /s/; i_e → /iː/', '拆分练习：po · lice。注意：c → /s/; i_e → /iː/。', 'Unit 6 · 21', '👮', NULL, NULL, 123),
('outdoors', '（在）户外；（在）野外', '/ˌaʊtˈdɔːrz/', 'adverb', 'Core', 'out · doors', 'out-DOORS', 'ou → /aʊ/; oo → /ɔːr/', '拆分练习：out · doors。注意：ou → /aʊ/; oo → /ɔːr/。', 'Unit 6 · 21', '🏕️', NULL, NULL, 124),
('keep ... away', '（使）远离；（使）不靠近', '/kiːp əˈweɪ/', 'phrase', 'Core', 'keep ... a · way', 'KEEP ... a-WAY', 'ee → /iː/; a_y → /eɪ/', '拆分练习：keep ... a · way。注意：ee → /iː/; a_y → /eɪ/。', 'Unit 6 · 22', '🚫', NULL, NULL, 125),
('heat', '热；高温', '/hiːt/', 'noun', 'Core', 'heat', 'HEAT', 'ea → /iː/', '拆分练习：heat。注意：ea → /iː/。', 'Unit 6 · 22', '🔥', NULL, NULL, 126),
('mean', '意味着', '/miːn/', 'verb', 'Core', 'mean', 'MEAN', 'ea → /iː/', '拆分练习：mean。注意：ea → /iː/。', 'Unit 7 · 23', '➡️', NULL, NULL, 127),
('zodiac', '生肖', '/ˈzoʊdiæk/', 'noun', 'Core', 'zo · di · ac', 'ZO-di-ac', 'o → /oʊ/; c → /k/', '拆分练习：zo · di · ac。注意：o → /oʊ/; c → /k/。', 'Unit 7 · 23', '♈', NULL, NULL, 128),
('be named after', '以……命名', '/biː neɪmd ˈɑːftər/', 'phrase', 'Core', 'be named af · ter', 'be NAMED af-ter', 'a_e → /eɪ/; er → /ər/', '拆分练习：be named af · ter。注意：a_e → /eɪ/; er → /ər/。', 'Unit 7 · 23', '🏷️', NULL, NULL, 129),
('rat', '鼠', '/ræt/', 'noun', 'Core', 'rat', 'RAT', 'a → /æ/', '拆分练习：rat。注意：a → /æ/。', 'Unit 7 · 23', '🐀', NULL, NULL, 130),
('ox', '牛', '/ɒks/', 'noun', 'Core', 'ox', 'OX', 'x → /ks/', '拆分练习：ox。注意：x → /ks/。', 'Unit 7 · 23', '🐂', NULL, NULL, 131),
('dragon', '龙', '/ˈdræɡən/', 'noun', 'Core', 'drag · on', 'DRAG-on', 'a → /æ/; o → /ən/', '拆分练习：drag · on。注意：a → /æ/; o → /ən/。', 'Unit 7 · 23', '🐉', NULL, NULL, 132),
('snake', '蛇', '/sneɪk/', 'noun', 'Core', 'snake', 'SNAKE', 'a_e → /eɪ/', '拆分练习：snake。注意：a_e → /eɪ/。', 'Unit 7 · 23', '🐍', NULL, NULL, 133),
('goat', '羊', '/ɡoʊt/', 'noun', 'Core', 'goat', 'GOAT', 'oa → /oʊ/', '拆分练习：goat。注意：oa → /oʊ/。', 'Unit 7 · 23', '🐐', NULL, NULL, 134),
('paper-cutting', '剪纸', '/ˈpeɪpər ˌkʌtɪŋ/', 'noun', 'Core', 'pa · per-cut · ting', 'PAP-er-CUT-ting', 'a_e → /eɪ/; -ing → /ɪŋ/', '拆分练习：pa · per-cut · ting。注意：a_e → /eɪ/; -ing → /ɪŋ/。', 'Unit 7 · 24', '✂️', NULL, NULL, 135),
('during', '在……期间', '/ˈdjʊərɪŋ/', 'preposition', 'Core', 'dur · ing', 'DUR-ing', 'ur → /jʊər/; -ing → /ɪŋ/', '拆分练习：dur · ing。注意：ur → /jʊər/; -ing → /ɪŋ/。', 'Unit 7 · 24', '⏳', NULL, NULL, 136),
('find out', '查明；发现', '/faɪnd aʊt/', 'phrase', 'Core', 'find out', 'FIND OUT', 'i_e → /aɪ/; ou → /aʊ/', '拆分练习：find out。注意：i_e → /aɪ/; ou → /aʊ/。', 'Unit 7 · 24', '🔎', NULL, NULL, 137),
('stamp', '邮票', '/stæmp/', 'noun', 'Core', 'stamp', 'STAMP', 'a → /æ/', '拆分练习：stamp。注意：a → /æ/。', 'Unit 7 · 25', '📮', NULL, NULL, 138),
('set', '一组；一套', '/set/', 'noun', 'Core', 'set', 'SET', 'short e → /e/', '拆分练习：set。注意：short e → /e/。', 'Unit 7 · 25', '🎁', NULL, NULL, 139),
('meaning', '意义；价值', '/ˈmiːnɪŋ/', 'noun', 'Core', 'mean · ing', 'MEAN-ing', 'ea → /iː/; -ing → /ɪŋ/', '拆分练习：mean · ing。注意：ea → /iː/; -ing → /ɪŋ/。', 'Unit 7 · 25', '💭', NULL, NULL, 140),
('race', '赛跑；竞争', '/reɪs/', 'noun/verb', 'Core', 'race', 'RACE', 'a_e → /eɪ/; c → /s/', '拆分练习：race。注意：a_e → /eɪ/; c → /s/。', 'Unit 7 · 26', '🏃', NULL, NULL, 141),
('finish', '终点；完成', '/ˈfɪnɪʃ/', 'noun/verb', 'Core', 'fin · ish', 'FIN-ish', 'i → /ɪ/; sh → /ʃ/', '拆分练习：fin · ish。注意：i → /ɪ/; sh → /ʃ/。', 'Unit 7 · 26', '🏁', NULL, NULL, 142),
('winner', '获胜者', '/ˈwɪnər/', 'noun', 'Core', 'win · ner', 'WIN-ner', 'i → /ɪ/; -er → /ər/', '拆分练习：win · ner。注意：i → /ɪ/; -er → /ər/。', 'Unit 7 · 26', '🏆', NULL, NULL, 143),
('stone', '石头；石块', '/stoʊn/', 'noun', 'Core', 'stone', 'STONE', 'o_e → /oʊ/', '拆分练习：stone。注意：o_e → /oʊ/。', 'Unit 7 · 26', '🪨', NULL, NULL, 144),
('finally', '最后；终于', '/ˈfaɪnəli/', 'adverb', 'Core', 'fi · nal · ly', 'FI-nal-ly', 'i_e → /aɪ/; y → /i/', '拆分练习：fi · nal · ly。注意：i_e → /aɪ/; y → /i/。', 'Unit 7 · 26', '✅', NULL, NULL, 145),
('fall back', '后退', '/fɔːl bæk/', 'phrase', 'Core', 'fall back', 'FALL BACK', 'all → /ɔːl/; a → /æ/', '拆分练习：fall back。注意：all → /ɔːl/; a → /æ/。', 'Unit 7 · 26', '↩️', NULL, NULL, 146);

INSERT INTO `kids_english_card_sound_part` (`card_id`, `part_order`, `chunk`, `pronunciation`)
SELECT `id`, 1, `word`, `phonics`
FROM `kids_english_card`
WHERE `priority_order` BETWEEN 97 AND 146;

INSERT INTO `kids_english_card_example` (`card_id`, `example_text`, `translation`, `priority_order`) VALUES
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=97), 'Thomas Edison was a famous inventor.', '托马斯·爱迪生是一位著名的发明家。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=97), 'The young inventor built a simple robot.', '这位年轻的发明家造了一台简单的机器人。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=98), 'Movable-type printing made it easier to print many books.', '活字印刷术让人们更容易印制许多书。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=98), 'We learned about movable-type printing in history class.', '我们在历史课上学习了活字印刷术。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=99), 'The telephone was an important invention.', '电话是一项重要的发明。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=99), 'This invention saves people time.', '这项发明为人们节省了时间。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=100), 'Reading gives us knowledge about the world.', '阅读让我们了解关于世界的知识。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=100), 'She shared her knowledge of plants with the class.', '她和全班同学分享了她的植物知识。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=101), 'The light bulb lit up the room.', '电灯泡照亮了房间。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=101), 'My dad changed the broken light bulb.', '爸爸换掉了坏掉的电灯泡。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=102), 'We did a science experiment with water.', '我们做了一个关于水的科学实验。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=102), 'The experiment showed that plants need light.', '实验表明植物需要光。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=103), 'The poet wrote a poem about spring.', '这位诗人写了一首关于春天的诗。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=103), 'Our class invited a poet to read her poem.', '我们班邀请了一位诗人来朗读她的诗。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=104), 'Good friendship grows through trust and kindness.', '良好的友谊在信任和善意中不断加深。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=104), 'Our friendship grew stronger after we helped each other.', '我们互相帮助后，友谊变得更加深厚了。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=105), 'She can recite the poem from memory.', '她能背诵这首诗。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=105), 'We recited a poem at the school show.', '我们在学校演出上背诵了一首诗。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=106), 'Germany is a country in Europe.', '德国是欧洲的一个国家。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=106), 'My uncle visited Germany last summer.', '我叔叔去年夏天去过德国。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=107), 'Be careful not to lose your school ID.', '小心别把你的学生证弄丢了。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=107), 'I do not want to lose this game.', '我不想输掉这场比赛。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=108), 'The stars glow in the dark sky.', '星星在黑暗的天空中发光。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=108), 'The fireflies glow at night.', '萤火虫在夜晚发光。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=109), 'An astronaut wears a spacesuit in space.', '宇航员在太空中穿着宇航服。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=109), 'The spacesuit protects the astronaut from the cold.', '宇航服保护宇航员免受寒冷。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=110), 'Students wear a school uniform on Monday.', '学生们星期一穿校服。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=110), 'The nurse put on her clean uniform.', '护士穿上了干净的制服。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=111), 'Wear a mask when the air is dirty.', '空气脏的时候要戴口罩。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=111), 'The actor wore a dragon mask.', '演员戴着一个龙面具。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=112), 'Lily gave a short speech about kindness.', '莉莉做了一次关于善良的简短演讲。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=112), 'He practiced his speech before the school assembly.', '他在学校集会前练习了演讲。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=113), 'Please dress warmly on a cold day.', '天气冷时请穿暖和一些。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=113), 'She wore a blue dress to the party.', '她穿着一条蓝色连衣裙参加聚会。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=114), 'I need a pair of socks for the trip.', '我旅行时需要一双袜子。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=114), 'He bought a pair of new shoes.', '他买了一双新鞋。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=115), 'We can reuse this glass jar.', '我们可以再次利用这个玻璃罐。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=115), 'Reuse paper when you can to reduce waste.', '能重复使用纸张时就重复使用，以减少浪费。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=116), 'I am trying to cut down on candy.', '我正在努力少吃糖果。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=116), 'We should cut down on plastic bags.', '我们应该减少使用塑料袋。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=117), 'We should help people in need.', '我们应该帮助有需要的人。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=117), 'The shelter gives food to families in need.', '这个收容所为有需要的家庭提供食物。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=118), 'This broken pen is useless.', '这支坏掉的笔没有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=118), 'A map is useless if we cannot read it.', '如果我们看不懂地图，地图就没有用。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=119), 'We can make use of old boxes for art projects.', '我们可以利用旧盒子做美术作品。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=119), 'Make use of the library to find good books.', '利用图书馆去找一些好书。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=120), 'Regular exercise is good for your health.', '经常锻炼对你的健康有益。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=120), 'Eating vegetables helps protect your health.', '吃蔬菜有助于保护你的健康。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=121), 'It is wrong to laugh at someone who is hurt.', '嘲笑受伤的人是不对的。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=121), 'I wrote the wrong answer.', '我写错了答案。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=122), 'Planting trees helps protect the environment.', '植树有助于保护环境。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=122), 'We should keep our environment clean.', '我们应该保持环境清洁。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=123), 'The police helped the lost child find her family.', '警察帮助走失的孩子找到了家人。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=123), 'Call the police if there is an emergency.', '如果发生紧急情况，请报警。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=124), 'We played outdoors after lunch.', '午饭后我们在户外玩耍。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=124), 'Fresh air is good when you spend time outdoors.', '在户外活动时呼吸新鲜空气很好。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=125), 'Keep your hands away from the hot stove.', '让你的手远离热炉子。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=125), 'This fence keeps animals away from the road.', '这道栅栏使动物远离马路。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=126), 'The heat made us look for shade.', '炎热的天气让我们寻找阴凉处。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=126), 'Drink water in the summer heat.', '在夏日炎热的天气里要喝水。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=127), 'What does this sign mean?', '这个标志是什么意思？', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=127), 'Being honest means telling the truth.', '诚实意味着说实话。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=128), 'The Chinese zodiac has twelve animals.', '中国生肖有十二种动物。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=128), 'My grandmother knows a lot about the zodiac.', '我的奶奶很了解生肖。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=129), 'The park was named after a famous scientist.', '这个公园以一位著名科学家的名字命名。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=129), 'She was named after her grandmother.', '她的名字是以祖母的名字命名的。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=130), 'The cat chased a rat out of the kitchen.', '猫把一只老鼠赶出了厨房。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=130), 'A rat can squeeze through a small hole.', '老鼠可以钻过一个小洞。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=131), 'The ox pulled the cart along the road.', '牛拉着车沿着马路走。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=131), 'The ox is one of the animals in the Chinese zodiac.', '牛是中国生肖中的一种动物。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=132), 'The dragon is a symbol in many stories.', '龙是许多故事中的一种象征。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=132), 'We made a paper dragon for the festival.', '我们为节日做了一条纸龙。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=133), 'We saw a snake near the rocks.', '我们在岩石附近看到了一条蛇。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=133), 'The snake moved quietly through the grass.', '蛇安静地穿过草地。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=134), 'The goat climbed onto the rock.', '山羊爬上了岩石。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=134), 'We saw a white goat on the farm.', '我们在农场看到了一只白山羊。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=135), 'Paper-cutting is a traditional Chinese art.', '剪纸是中国传统艺术。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=135), 'Grandma taught me paper-cutting during the holiday.', '奶奶在假期教我剪纸。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=136), 'Please stay quiet during the test.', '考试期间请保持安静。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=136), 'We took many photos during the trip.', '旅行期间我们拍了许多照片。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=137), 'I want to find out more about space.', '我想进一步了解太空。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=137), 'Let us find out when the library opens.', '我们来查查图书馆什么时候开门。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=138), 'I put a stamp on the letter.', '我在信上贴了一张邮票。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=138), 'My grandpa has a collection of old stamps.', '我爷爷收藏了一些旧邮票。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=139), 'I got a set of colored pencils for my birthday.', '我生日时得到了一套彩色铅笔。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=139), 'This set has six cups.', '这套餐具里有六个杯子。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=140), 'What is the meaning of this word?', '这个单词的意思是什么？', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=140), 'The story has a special meaning for me.', '这个故事对我有特别的意义。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=141), 'I ran in a race at school.', '我参加了学校的赛跑。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=141), 'The two runners raced to the finish line.', '两名赛跑者向终点线跑去。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=142), 'Please finish your homework before dinner.', '请在晚饭前完成作业。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=142), 'Our team crossed the finish line together.', '我们队一起越过了终点线。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=143), 'The winner received a gold medal.', '获胜者得到了一枚金牌。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=143), 'Everyone cheered for the race winner.', '大家为赛跑的获胜者欢呼。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=144), 'He skipped a flat stone across the lake.', '他让一块扁平的石头在湖面上打水漂。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=144), 'The path was covered with small stones.', '小路上铺满了小石头。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=145), 'After many tries, I finally solved the puzzle.', '尝试多次后，我终于解开了这个谜题。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=145), 'We finally arrived at the museum.', '我们终于到了博物馆。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=146), 'When the path became unsafe, the hikers had to fall back.', '小路变得不安全时，徒步者不得不后退。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=146), 'When the ball came toward us, we had to fall back.', '球朝我们飞来时，我们不得不后退。', 2);

INSERT INTO `kids_english_card_word_family` (`card_id`, `related_word`, `part_of_speech`, `meaning`, `priority_order`) VALUES
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=97), 'invent', 'verb', '发明', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=99), 'inventive', 'adjective', '有创造力的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=104), 'friendly', 'adjective', '友好的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=118), 'use', 'verb', '使用', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=122), 'environmental', 'adjective', '环境的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=127), 'meaningful', 'adjective', '有意义的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=140), 'meaningful', 'adjective', '有意义的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=143), 'win', 'verb', '获胜', 1);

UPDATE `kids_english_card`
SET `tip` = CONCAT('Chunk it: ', `syllables`, '. Focus on ', `phonics_focus`, '.')
WHERE `is_active`=1 AND `priority_order` BETWEEN 97 AND 146;

UPDATE `kids_english_card`
SET `image_url` = CASE `priority_order`
    WHEN 97 THEN '/static/uploads/kids_cards/inventor-wide.png'
    WHEN 98 THEN '/static/uploads/kids_cards/movable-type-printing-wide.png'
    WHEN 99 THEN '/static/uploads/kids_cards/invention-wide.png'
    WHEN 100 THEN '/static/uploads/kids_cards/knowledge-wide.png'
    WHEN 101 THEN '/static/uploads/kids_cards/light-bulb-wide.png'
    WHEN 102 THEN '/static/uploads/kids_cards/experiment-wide.png'
    WHEN 103 THEN '/static/uploads/kids_cards/poet-wide.png'
    WHEN 104 THEN '/static/uploads/kids_cards/friendship-wide.png'
    WHEN 105 THEN '/static/uploads/kids_cards/recite-wide.png'
    WHEN 106 THEN '/static/uploads/kids_cards/germany-wide.png'
    WHEN 107 THEN '/static/uploads/kids_cards/lose-wide.png'
    WHEN 108 THEN '/static/uploads/kids_cards/glow-wide.png'
    WHEN 109 THEN '/static/uploads/kids_cards/spacesuit-wide.png'
    WHEN 110 THEN '/static/uploads/kids_cards/uniform-wide.png'
    WHEN 111 THEN '/static/uploads/kids_cards/mask-wide.png'
    WHEN 112 THEN '/static/uploads/kids_cards/speech-wide.png'
    WHEN 113 THEN '/static/uploads/kids_cards/dress-wide.png'
    WHEN 114 THEN '/static/uploads/kids_cards/a-pair-of-wide.png'
    WHEN 115 THEN '/static/uploads/kids_cards/reuse-wide.png'
    WHEN 116 THEN '/static/uploads/kids_cards/cut-down-on-wide.png'
    WHEN 117 THEN '/static/uploads/kids_cards/in-need-wide.png'
    WHEN 118 THEN '/static/uploads/kids_cards/useless-wide.png'
    WHEN 119 THEN '/static/uploads/kids_cards/make-use-of-wide.png'
    WHEN 120 THEN '/static/uploads/kids_cards/health-wide.png'
    WHEN 121 THEN '/static/uploads/kids_cards/wrong-wide.png'
    WHEN 122 THEN '/static/uploads/kids_cards/environment-wide.png'
    WHEN 123 THEN '/static/uploads/kids_cards/police-wide.png'
    WHEN 124 THEN '/static/uploads/kids_cards/outdoors-wide.png'
    WHEN 125 THEN '/static/uploads/kids_cards/keep-away-wide.png'
    WHEN 126 THEN '/static/uploads/kids_cards/heat-wide.png'
    WHEN 127 THEN '/static/uploads/kids_cards/mean-wide.png'
    WHEN 128 THEN '/static/uploads/kids_cards/zodiac-wide.png'
    WHEN 129 THEN '/static/uploads/kids_cards/be-named-after-wide.png'
    WHEN 130 THEN '/static/uploads/kids_cards/rat-wide.png'
    WHEN 131 THEN '/static/uploads/kids_cards/ox-wide.png'
    WHEN 132 THEN '/static/uploads/kids_cards/dragon-wide.png'
    WHEN 133 THEN '/static/uploads/kids_cards/snake-wide.png'
    WHEN 134 THEN '/static/uploads/kids_cards/goat-wide.png'
    WHEN 135 THEN '/static/uploads/kids_cards/paper-cutting-wide.png'
    WHEN 136 THEN '/static/uploads/kids_cards/during-wide.png'
    WHEN 137 THEN '/static/uploads/kids_cards/find-out-wide.png'
    WHEN 138 THEN '/static/uploads/kids_cards/stamp-wide.png'
    WHEN 139 THEN '/static/uploads/kids_cards/set-wide.png'
    WHEN 140 THEN '/static/uploads/kids_cards/meaning-wide.png'
    WHEN 141 THEN '/static/uploads/kids_cards/race-wide.png'
    WHEN 142 THEN '/static/uploads/kids_cards/finish-wide.png'
    WHEN 143 THEN '/static/uploads/kids_cards/winner-wide.png'
    WHEN 144 THEN '/static/uploads/kids_cards/stone-wide.png'
    WHEN 145 THEN '/static/uploads/kids_cards/finally-wide.png'
    WHEN 146 THEN '/static/uploads/kids_cards/fall-back-wide.png'
END
WHERE `priority_order` BETWEEN 97 AND 146;

COMMIT;
