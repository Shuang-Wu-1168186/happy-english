# Migration: continue the kids card word list after Earth.
# The source page places satellite immediately after the existing Earth card.
# This migration is safe to re-run for priorities 71-96.

START TRANSACTION;

UPDATE `kids_english_card`
SET `word`='BeiDou Navigation Satellite System (abbr. BDS)',
    `translation`='北斗卫星导航系统',
    `phonics`='/ˌbeɪduː ˌnævɪˈɡeɪʃən ˈsætəlaɪt ˈsɪstəm/',
    `syllables`='Bei · Dou Nav · i · ga · tion Sat · el · lite Sys · tem B · D · S',
    `stress`='BEI-dou nav-i-GA-tion SAT-el-lite SYS-tem B-D-S',
    `phonics_focus`='ou → /uː/; tion → /ʃən/; sat → /sæt/; BDS 读字母名',
    `syllable_tip`='拆分练习：Bei / Dou Nav / i / ga / tion Sat / el / lite Sys / tem B / D / S。注意：tion → /ʃən/；BDS 读字母名。'
WHERE `priority_order`=69;

DELETE FROM `kids_english_card`
WHERE `priority_order` BETWEEN 71 AND 96;

INSERT INTO `kids_english_card`
(`word`, `translation`, `phonics`, `part_of_speech`, `level`, `syllables`, `stress`, `phonics_focus`, `syllable_tip`, `category`, `emoji`, `image_url`, `tip`, `priority_order`)
VALUES
('satellite', '人造卫星', '/ˈsætəlaɪt/', 'noun', 'Core', 'sat · el · lite', 'SAT-el-lite', 'a → /æ/; i_e → /aɪ/', '拆分练习：sat / el / lite。注意：i_e → /aɪ/。', 'Unit 4 · 13', '🛰️', NULL, NULL, 71),
('machine', '机器；装置', '/məˈʃiːn/', 'noun', 'Core', 'ma · chine', 'ma-CHINE', 'ch → /ʃ/; i_e → /iː/', '拆分练习：ma / chine。注意：ch → /ʃ/；i_e → /iː/。', 'Unit 4 · 13', '⚙️', NULL, NULL, 72),
('as before', '像以前那样', '/əz bɪˈfɔːr/', 'phrase', 'Core', 'as be · fore', 'as be-FORE', 'as → /əz/; ore → /ɔːr/', '拆分练习：as / be / fore。注意：as 在短语中弱读。', 'Unit 4 · 13', '🔁', NULL, NULL, 73),
('role model', '榜样', '/ˈroʊl ˌmɒdəl/', 'noun', 'Core', 'role mod · el', 'ROLE mod-el', 'o_e → /oʊ/; o → /ɒ/', '拆分练习：role / mod / el。', 'Unit 5 · 15', '🌟', NULL, NULL, 74),
('musician', '音乐家', '/mjuˈzɪʃən/', 'noun', 'Core', 'mu · si · cian', 'mu-ZI-cian', 'cian → /ʃən/; u → /juː/', '拆分练习：mu / si / cian。注意：cian → /ʃən/。', 'Unit 5 · 15', '🎵', NULL, NULL, 75),
('March of the Volunteers', '义勇军进行曲', '/mɑːrtʃ əv ðə ˌvɒlənˈtɪərz/', 'proper noun', 'Core', 'March of the Vol · un · teers', 'MARCH of the vol-un-TEERS', 'ch → /tʃ/; -eer → /ɪər/', '拆分练习：March / of / the / Vol / un / teers。', 'Unit 5 · 15', '🎼', NULL, NULL, 76),
('national anthem', '国歌', '/ˌnæʃənəl ˈænθəm/', 'noun', 'Core', 'na · tion · al an · them', 'NAT-ion-al AN-them', 'tion → /ʃən/; th → /θ/', '拆分练习：na / tion / al / an / them。', 'Unit 5 · 15', '🏛️', NULL, NULL, 77),
('person', '人', '/ˈpɜːrsən/', 'noun', 'Core', 'per · son', 'PER-son', 'er → /ɜːr/; o → /ə/', '拆分练习：per / son。', 'Unit 5 · 15', '🧑', NULL, NULL, 78),
('educator', '教育家', '/ˈedʒukeɪtər/', 'noun', 'Core', 'ed · u · ca · tor', 'ED-u-ca-tor', 'c → /k/; a_e → /eɪ/', '拆分练习：ed / u / ca / tor。', 'Unit 5 · 15', '👩‍🏫', NULL, NULL, 79),
('education', '教育（尤其学校）', '/ˌedʒuˈkeɪʃən/', 'noun', 'Core', 'ed · u · ca · tion', 'ed-u-CA-tion', 'tion → /ʃən/; c → /k/', '拆分练习：ed / u / ca / tion。注意：tion → /ʃən/。', 'Unit 5 · 15', '📚', NULL, NULL, 80),
('collection', '专辑；作品集', '/kəˈlekʃən/', 'noun', 'Core', 'col · lec · tion', 'col-LEC-tion', 'tion → /ʃən/; c → /k/', '拆分练习：col / lec / tion。', 'Unit 5 · 16', '🗂️', NULL, NULL, 81),
('reader', '读者', '/ˈriːdər/', 'noun', 'Core', 'read · er', 'READ-er', 'ee → /iː/; -er → /ər/', '拆分练习：read / er。', 'Unit 5 · 16', '📖', NULL, NULL, 82),
('Denmark', '丹麦（欧洲）', '/ˈdenmɑːrk/', 'proper noun', 'Core', 'Den · mark', 'DEN-mark', 'e → /e/; ar → /ɑːr/', '拆分练习：Den / mark。', 'Unit 5 · 16', '🇩🇰', NULL, NULL, 83),
('friendly', '友好的', '/ˈfrendli/', 'adjective', 'Core', 'friend · ly', 'FRIEND-ly', 'ie → /e/; y → /i/', '拆分练习：friend / ly。', 'Unit 5 · 16', '😊', NULL, NULL, 84),
('sugar pill', '糖丸', '/ˈʃʊɡər pɪl/', 'noun', 'Core', 'sug · ar pill', 'SUG-ar PILL', 's → /ʃ/; u → /ʊ/', '拆分练习：sug / ar / pill。', 'Unit 5 · 17', '💊', NULL, NULL, 85),
('develop', '研发；开发', '/dɪˈveləp/', 'verb', 'Core', 'de · vel · op', 'de-VEL-op', 'e → /ɪ/; e → /e/', '拆分练习：de / vel / op。', 'Unit 5 · 17', '🛠️', NULL, NULL, 86),
('polio', '脊髓灰质炎（小儿麻痹症）', '/ˈpoʊlioʊ/', 'noun', 'Core', 'po · li · o', 'PO-li-o', 'o → /oʊ/', '拆分练习：po / li / o。', 'Unit 5 · 17', '🩺', NULL, NULL, 87),
('spread', '扩散；传播', '/spred/', 'verb', 'Core', 'spread', 'SPREAD', 'ea → /e/', '拆分练习：spread。注意：ea → /e/。', 'Unit 5 · 17', '↔️', NULL, NULL, 88),
('vaccine', '疫苗', '/ˈvæksiːn/', 'noun', 'Core', 'vac · cine', 'VAC-cine', 'c → /k/; cine → /siːn/', '拆分练习：vac / cine。', 'Unit 5 · 17', '💉', NULL, NULL, 89),
('even', '甚至；即使', '/ˈiːvən/', 'adverb', 'Core', 'e · ven', 'E-ven', 'e → /iː/; e → /ə/', '拆分练习：e / ven。', 'Unit 5 · 17', '➗', NULL, NULL, 90),
('December', '十二月', '/dɪˈsembər/', 'proper noun', 'Core', 'De · cem · ber', 'de-CEM-ber', 'c → /s/; e → /e/', '拆分练习：De / cem / ber。', 'Unit 5 · 17', '📅', NULL, NULL, 91),
('million', '百万；许多', '/ˈmɪljən/', 'number', 'Core', 'mil · lion', 'MIL-lion', 'll → /lj/; i → /ɪ/', '拆分练习：mil / lion。', 'Unit 5 · 17', '🔢', NULL, NULL, 92),
('save ... from', '拯救；挽救……于……', '/seɪv frəm/', 'phrase', 'Core', 'save · from', 'SAVE from', 'a_e → /eɪ/; from → /frəm/', '拆分练习：save / from。', 'Unit 5 · 17', '🛟', NULL, NULL, 93),
('WHO (World Health Organization)', '世界卫生组织', '/ˌdʌbəljuː eɪtʃ ˈoʊ ˈwɜːrld helθ ˌɔːrɡənaɪˈzeɪʃən/', 'proper noun', 'Core', 'W H O (World Health Or · gan · i · za · tion)', 'W-H-O WORLD HEALTH or-gan-i-ZA-tion', '字母读名；tion → /ʃən/', '拆分练习：W / H / O / World / Health / Or / gan / i / za / tion。', 'Unit 5 · 17', '🌍', NULL, NULL, 94),
('up to', '直到', '/ʌp tuː/', 'phrase', 'Core', 'up to', 'UP TO', 'u → /ʌ/; oo → /uː/', '拆分练习：up / to。', 'Unit 5 · 17', '⬆️', NULL, NULL, 95),
('worth', '值得的；价值', '/wɜːrθ/', 'adjective', 'Core', 'worth', 'WORTH', 'or → /ɜːr/; th → /θ/', '拆分练习：worth。注意：th → /θ/。', 'Unit 5 · 17', '🏷️', NULL, NULL, 96);

DELETE FROM `kids_english_card_sound_part`
WHERE `card_id` = (SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69);

DELETE FROM `kids_english_card_example`
WHERE `card_id` = (SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69);

INSERT INTO `kids_english_card_sound_part` (`card_id`, `part_order`, `chunk`, `pronunciation`) VALUES
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 1, 'BeiDou', '/ˌbeɪduː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 2, 'Nav', '/næv/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 3, 'i', '/ɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 4, 'ga', '/ɡeɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 5, 'tion', '/ʃən/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 6, 'Sat', '/sæt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 7, 'el', '/əl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 8, 'lite', '/laɪt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 9, 'Sys', '/sɪs/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 10, 'tem', '/təm/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 11, 'B', '/biː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 12, 'D', '/diː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 13, 'S', '/ɛs/');

INSERT INTO `kids_english_card_sound_part` (`card_id`, `part_order`, `chunk`, `pronunciation`) VALUES
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=71), 1, 'sat', '/sæt/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=71), 2, 'el', '/əl/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=71), 3, 'lite', '/laɪt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=72), 1, 'ma', '/mə/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=72), 2, 'chine', '/ʃiːn/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=73), 1, 'as', '/əz/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=73), 2, 'be', '/bɪ/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=73), 3, 'fore', '/fɔːr/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=74), 1, 'role', '/roʊl/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=74), 2, 'model', '/ˈmɒdəl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=75), 1, 'mu', '/mjuː/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=75), 2, 'si', '/ˈzɪ/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=75), 3, 'cian', '/ʃən/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=76), 1, 'March', '/mɑːrtʃ/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=76), 2, 'of', '/əv/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=76), 3, 'the', '/ðə/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=76), 4, 'Volunteers', '/ˌvɒlənˈtɪərz/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=77), 1, 'national', '/ˈnæʃənəl/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=77), 2, 'anthem', '/ˈænθəm/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=78), 1, 'per', '/pɜːr/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=78), 2, 'son', '/sən/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=79), 1, 'ed', '/ˈedʒ/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=79), 2, 'u', '/uː/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=79), 3, 'ca', '/keɪ/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=79), 4, 'tor', '/tər/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=80), 1, 'ed', '/ˌedʒ/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=80), 2, 'u', '/uː/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=80), 3, 'ca', '/ˈkeɪ/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=80), 4, 'tion', '/ʃən/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=81), 1, 'col', '/kə/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=81), 2, 'lec', '/ˈlek/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=81), 3, 'tion', '/ʃən/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=82), 1, 'read', '/riːd/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=82), 2, 'er', '/ər/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=83), 1, 'Den', '/den/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=83), 2, 'mark', '/mɑːrk/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=84), 1, 'friend', '/frend/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=84), 2, 'ly', '/li/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=85), 1, 'sug', '/ʃʊɡ/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=85), 2, 'ar', '/ər/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=85), 3, 'pill', '/pɪl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=86), 1, 'de', '/dɪ/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=86), 2, 'vel', '/ˈvel/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=86), 3, 'op', '/əp/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=87), 1, 'po', '/ˈpoʊ/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=87), 2, 'li', '/li/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=87), 3, 'o', '/oʊ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=88), 1, 'spread', '/spred/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=89), 1, 'vac', '/væk/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=89), 2, 'cine', '/siːn/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=90), 1, 'e', '/iː/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=90), 2, 'ven', '/vən/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=91), 1, 'De', '/dɪ/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=91), 2, 'cem', '/ˈsem/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=91), 3, 'ber', '/bər/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=92), 1, 'mil', '/ˈmɪl/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=92), 2, 'lion', '/jən/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=93), 1, 'save', '/seɪv/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=93), 2, 'from', '/frəm/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=94), 1, 'WHO', '/ˌdʌbəljuː eɪtʃ ˈoʊ/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=94), 2, 'World', '/wɜːrld/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=94), 3, 'Health', '/helθ/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=94), 4, 'Organization', '/ˌɔːrɡənaɪˈzeɪʃən/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=95), 1, 'up', '/ʌp/'), ((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=95), 2, 'to', '/tuː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=96), 1, 'worth', '/wɜːrθ/');

INSERT INTO `kids_english_card_example` (`card_id`, `example_text`, `translation`, `priority_order`) VALUES
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 'BeiDou Navigation Satellite System helps people find their way.', '北斗卫星导航系统帮助人们辨认方向。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 'The BeiDou Navigation Satellite System can show our location.', '北斗卫星导航系统可以显示我们的位置。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=71), 'The satellite travels around the Earth.', '这颗人造卫星绕着地球运行。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=71), 'We watched a satellite move across the night sky.', '我们看到一颗人造卫星划过夜空。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=72), 'This machine can clean the floor.', '这台机器可以清洁地板。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=72), 'The machine is easy for children to use.', '这台机器很容易让孩子使用。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=73), 'The classroom looks as bright as before.', '教室看起来像以前一样明亮。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=73), 'She smiled as before and said hello.', '她像以前一样微笑着打招呼。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=74), 'My role model always helps other people.', '我的榜样总是帮助别人。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=74), 'A good role model works hard and stays kind.', '一个好的榜样努力工作并保持友善。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=75), 'The musician plays the piano beautifully.', '这位音乐家钢琴弹得很好。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=75), 'The young musician practises every day.', '这位年轻的音乐家每天练习。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=76), 'We sang the March of the Volunteers together.', '我们一起唱了《义勇军进行曲》。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=76), 'The March of the Volunteers is our national anthem.', '《义勇军进行曲》是我们的国歌。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=77), 'Everyone stood up for the national anthem.', '大家为国歌起立。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=77), 'The national anthem began after the speech.', '演讲结束后，国歌响起。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=78), 'Every person can make a difference.', '每个人都可以带来改变。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=78), 'One person helped us find the way.', '一个人帮助我们找到了路。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=79), 'The educator teaches children with patience.', '这位教育家耐心地教孩子们。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=79), 'The educator wrote many books for teachers.', '这位教育家为教师写了很多书。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=80), 'Education opens doors to new opportunities.', '教育为新的机会打开大门。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=80), 'Good education helps children grow.', '良好的教育帮助孩子成长。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=81), 'This collection includes old songs.', '这个作品集收录了老歌曲。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=81), 'She showed me her stamp collection.', '她给我看了她的邮票收藏。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=82), 'The reader asked a good question.', '这位读者问了一个好问题。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=82), 'Every reader can learn something new.', '每位读者都能学到新东西。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=83), 'Denmark is a country in Europe.', '丹麦是欧洲的一个国家。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=83), 'She wants to visit Denmark one day.', '她希望有一天去丹麦。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=84), 'The friendly dog wagged its tail.', '那只友好的狗摇了摇尾巴。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=84), 'Our new neighbour is very friendly.', '我们的新邻居非常友好。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=85), 'The doctor gave the child a sugar pill instead of real medicine.', '医生给孩子服用了一颗糖丸，而不是真正的药。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=85), 'The sugar pill looked like real medicine.', '糖丸看起来像真正的药。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=86), 'Scientists develop new medicines.', '科学家研发新药。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=86), 'The team will develop a safer machine.', '团队将开发更安全的机器。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=87), 'The vaccine helped protect children from polio.', '疫苗帮助保护孩子们免受脊髓灰质炎侵害。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=87), 'Doctors worked hard to stop polio.', '医生们努力阻止脊髓灰质炎。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=88), 'Good news can spread quickly.', '好消息可以快速传播。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=88), 'The fire began to spread across the field.', '火开始在田野上蔓延。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=89), 'The doctor gave me a vaccine.', '医生给我打了一针疫苗。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=89), 'Vaccines help prevent some diseases.', '疫苗有助于预防一些疾病。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=90), 'Even a small act of kindness matters.', '即使是一个小小的善举也很重要。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=90), 'Even my little brother knows this rule.', '甚至我的弟弟也知道这条规则。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=91), 'School starts again in December.', '学校在十二月再次开学。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=91), 'We decorate the tree in December.', '我们在十二月装饰树。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=92), 'A million stars filled the picture.', '画面中有数百万颗星星。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=92), 'The video has a million views.', '这个视频有一百万次观看。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=93), 'The vaccine can save children from disease.', '疫苗可以挽救孩子们，使他们免受疾病侵害。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=93), 'Trees save the soil from washing away.', '树木防止土壤被水冲走。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=94), 'The WHO works to improve world health.', '世界卫生组织致力于改善全球健康。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=94), 'The WHO shares health information with countries.', '世界卫生组织与各国分享健康信息。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=95), 'The shop is open up to six o’clock.', '这家商店营业到六点。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=95), 'You can choose up to three books.', '你最多可以选择三本书。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=96), 'This book is worth reading.', '这本书值得一读。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=96), 'The painting is worth a million dollars.', '这幅画价值一百万美元。', 2);

INSERT INTO `kids_english_card_word_family` (`card_id`, `related_word`, `part_of_speech`, `meaning`, `priority_order`) VALUES
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=71), 'satellite', 'noun', '卫星', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=72), 'machinery', 'noun', '机器；机械', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=74), 'model', 'noun', '榜样；模型', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=75), 'music', 'noun', '音乐', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=79), 'educate', 'verb', '教育', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=80), 'educational', 'adjective', '教育的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=84), 'friendship', 'noun', '友谊', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=86), 'development', 'noun', '发展；研发', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=88), 'spreading', 'verb', '传播；扩散', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=89), 'vaccinate', 'verb', '给……接种疫苗', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=96), 'worthy', 'adjective', '值得的', 1);

UPDATE `kids_english_card`
SET `tip` = CONCAT('Chunk it: ', `syllables`, '. Focus on ', `phonics_focus`, '.')
WHERE `is_active`=1 AND `priority_order` BETWEEN 69 AND 96;

UPDATE `kids_english_card`
SET `image_url` = CASE `priority_order`
    WHEN 71 THEN '/static/uploads/kids_cards/satellite-wide.png'
    WHEN 72 THEN '/static/uploads/kids_cards/machine-wide.png'
    WHEN 73 THEN '/static/uploads/kids_cards/as-before-wide.png'
    WHEN 74 THEN '/static/uploads/kids_cards/role-model-wide.png'
    WHEN 75 THEN '/static/uploads/kids_cards/musician-wide.png'
    WHEN 76 THEN '/static/uploads/kids_cards/march-of-the-volunteers-wide.png'
    WHEN 77 THEN '/static/uploads/kids_cards/national-anthem-wide.png'
    WHEN 78 THEN '/static/uploads/kids_cards/person-wide.png'
    WHEN 79 THEN '/static/uploads/kids_cards/educator-wide.png'
    WHEN 80 THEN '/static/uploads/kids_cards/education-wide.png'
    WHEN 81 THEN '/static/uploads/kids_cards/collection-wide.png'
    WHEN 82 THEN '/static/uploads/kids_cards/reader-wide.png'
    WHEN 83 THEN '/static/uploads/kids_cards/denmark-wide.png'
    WHEN 84 THEN '/static/uploads/kids_cards/friendly-wide.png'
    WHEN 85 THEN '/static/uploads/kids_cards/sugar-pill-wide.png'
    WHEN 86 THEN '/static/uploads/kids_cards/develop-wide.png'
    WHEN 87 THEN '/static/uploads/kids_cards/polio-wide.png'
    WHEN 88 THEN '/static/uploads/kids_cards/spread-wide.png'
    WHEN 89 THEN '/static/uploads/kids_cards/vaccine-wide.png'
    WHEN 90 THEN '/static/uploads/kids_cards/even-wide.png'
    WHEN 91 THEN '/static/uploads/kids_cards/december-wide.png'
    WHEN 92 THEN '/static/uploads/kids_cards/million-wide.png'
    WHEN 93 THEN '/static/uploads/kids_cards/save-from-wide.png'
    WHEN 94 THEN '/static/uploads/kids_cards/who-world-health-organization-wide.png'
    WHEN 95 THEN '/static/uploads/kids_cards/up-to-wide.png'
    WHEN 96 THEN '/static/uploads/kids_cards/worth-wide.png'
END
WHERE `priority_order` BETWEEN 71 AND 96;

COMMIT;
