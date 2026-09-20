-- Natural phonics: independent lesson table and seed data.
-- Safe to re-run: lesson_code is unique and seed rows are updated.

CREATE TABLE IF NOT EXISTS `phonics_lesson` (
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `lesson_code` VARCHAR(80) NOT NULL,
    `title` VARCHAR(200) NOT NULL,
    `subtitle` VARCHAR(200) NOT NULL,
    `pattern_text` VARCHAR(255) NOT NULL,
    `sound_text` TEXT NOT NULL,
    `learning_tip` TEXT NOT NULL,
    `review_examples_json` LONGTEXT NULL,
    `examples_json` LONGTEXT NOT NULL,
    `quiz_prompt` TEXT NOT NULL,
    `quiz_choices_json` LONGTEXT NOT NULL,
    `quiz_answer` VARCHAR(255) NOT NULL,
    `priority_order` INT NOT NULL DEFAULT 0,
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_phonics_lesson_code` (`lesson_code`),
    KEY `idx_phonics_lesson_active_order` (`is_active`, `priority_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='自然拼读课程表';

INSERT INTO `phonics_lesson` (`lesson_code`, `title`, `subtitle`, `pattern_text`, `sound_text`, `learning_tip`, `review_examples_json`, `examples_json`, `quiz_prompt`, `quiz_choices_json`, `quiz_answer`, `priority_order`, `is_active`) VALUES
    ('a-consonant-e', 'a + 辅音 + e', '第二十八讲 · 长元音 a', 'a + 辅音 + e → /eɪ/', 'a 发字母音 /eɪ/；词尾 e 不发音', 'a 和词尾 e 中间隔一个辅音时，a 通常读 /eɪ/。视频中的发音技巧是“压扁”。', '[{"word":"bag","focus":"a","sound":"/bæɡ/"},{"word":"fat","focus":"a","sound":"/fæt/"},{"word":"cat","focus":"a","sound":"/kæt/"}]', '[{"word":"face","focus":"a_e","sound":"/feɪs/"},{"word":"age","focus":"a_e","sound":"/eɪdʒ/"},{"word":"cake","focus":"a_e","sound":"/keɪk/"},{"word":"game","focus":"a_e","sound":"/ɡeɪm/"},{"word":"save","focus":"a_e","sound":"/seɪv/"},{"word":"wake","focus":"a_e","sound":"/weɪk/"}]', 'Which word follows the pattern a + 辅音 + e?', '["cake","cat","bag"]', 'cake', 1, 1),
    ('weak-a', '非重读 a 读 /ə/', '第二十九讲 · 轻松的 a', '非重读 a → /ə/', '轻读、放松，不要用力拉长', '视频通过 ago、across、arrest、above 等词示范非重读音节里的 a。发音时保持轻松。', '[{"word":"face","focus":"a_e","sound":"/feɪs/"},{"word":"age","focus":"a_e","sound":"/eɪdʒ/"},{"word":"cake","focus":"a_e","sound":"/keɪk/"}]', '[{"word":"ago","focus":"a","sound":"/əˈɡoʊ/"},{"word":"across","focus":"a","sound":"/əˈkrɔːs/"},{"word":"arrest","focus":"a","sound":"/əˈrest/"},{"word":"above","focus":"a","sound":"/əˈbʌv/"},{"word":"China","focus":"a","sound":"/ˈtʃaɪnə/"},{"word":"America","focus":"A","sound":"/əˈmerɪkə/"}]', 'Which word begins with the weak /ə/ sound?', '["above","cake","cat"]', 'above', 2, 1),
    ('long-e', 'e 的长音 /iː/', '第三十讲 · 拉长的 e', 'e → /iː/', '嘴角向两边展开，声音拉长', '视频先复习 bed、met、pet，再用 Chinese、Japanese、complete、gene、delete 练习 /iː/。', '[{"word":"bed","focus":"e","sound":"/bed/"},{"word":"met","focus":"e","sound":"/met/"},{"word":"pet","focus":"e","sound":"/pet/"}]', '[{"word":"Chinese","focus":"e","sound":"/ˌtʃaɪˈniːz/"},{"word":"Japanese","focus":"e","sound":"/ˌdʒæpəˈniːz/"},{"word":"complete","focus":"e","sound":"/kəmˈpliːt/"},{"word":"gene","focus":"e","sound":"/dʒiːn/"},{"word":"delete","focus":"e","sound":"/dɪˈliːt/"}]', 'Which word contains the long /iː/ sound from this video?', '["gene","pet","met"]', 'gene', 3, 1),
    ('weak-e', '弱读 e /ɪ/', '第三十一讲 · 干脆、轻松', '非重读 e → /ɪ/', '短促、干脆、放松', '视频用 elephant、pretty、pocket、ticket 练习弱读的 /ɪ/，提示是“干脆、轻松”。', NULL, '[{"word":"elephant","focus":"e","sound":"/ˈelɪfənt/"},{"word":"pretty","focus":"e","sound":"/ˈprɪti/"},{"word":"pocket","focus":"e","sound":"/ˈpɒkɪt/"},{"word":"ticket","focus":"e","sound":"/ˈtɪkɪt/"}]', 'Which word appeared in the video to practise weak e?', '["ticket","cake","nose"]', 'ticket', 4, 1),
    ('i-consonant-e', 'i + 辅音 + e', '第三十二讲 · 字母音 i', 'i + 辅音 + e → /aɪ/', '张开、饱满地读 /aɪ/', 'i 和词尾 e 中间隔一个辅音时，i 常读字母音 /aɪ/。视频的发音技巧是“夸张、饱满”。', NULL, '[{"word":"bike","focus":"i_e","sound":"/baɪk/"},{"word":"like","focus":"i_e","sound":"/laɪk/"},{"word":"kite","focus":"i_e","sound":"/kaɪt/"},{"word":"ice","focus":"i_e","sound":"/aɪs/"}]', 'Which word follows i + 辅音 + e?', '["kite","kit","sit"]', 'kite', 5, 1),
    ('o-consonant-e', 'o + 辅音 + e', '第三十三讲 · 字母音 o', 'o + 辅音 + e → /oʊ/', '先大圆，再收成小圆', 'o 和词尾 e 中间隔一个辅音时，o 常读 /oʊ/。视频提示“先大圆，再小圆”。', NULL, '[{"word":"coke","focus":"o_e","sound":"/koʊk/"},{"word":"nose","focus":"o_e","sound":"/noʊz/"},{"word":"close","focus":"o_e","sound":"/kloʊz/"},{"word":"explode","focus":"o_e","sound":"/ɪkˈsploʊd/"},{"word":"smoke","focus":"o_e","sound":"/smoʊk/"}]', 'Which word follows o + 辅音 + e?', '["nose","not","hot"]', 'nose', 6, 1),
    ('short-o-uh', 'o 读 /ʌ/', '第三十四讲 · 口型不大', 'o → /ʌ/', '短促，口型不大', '视频用 love、mother、honey、dozen、money、some 练习 o 的 /ʌ/ 音，发音提示是“干脆，口型不大”。', NULL, '[{"word":"love","focus":"o","sound":"/lʌv/"},{"word":"mother","focus":"o","sound":"/ˈmʌðər/"},{"word":"honey","focus":"o","sound":"/ˈhʌni/"},{"word":"dozen","focus":"o","sound":"/ˈdʌzən/"},{"word":"money","focus":"o","sound":"/ˈmʌni/"},{"word":"some","focus":"o","sound":"/sʌm/"}]', 'Which word has the /ʌ/ sound taught in this video?', '["money","nose","coke"]', 'money', 7, 1),
    ('weak-o', '非重读 o 读 /ə/', '第三十五讲 · 轻读 o', '非重读 o → /ə/', '轻读、放松', '视频用 tomorrow、police、connect、potato 等词练习弱读 o。', NULL, '[{"word":"tomorrow","focus":"o","sound":"/təˈmɒroʊ/"},{"word":"police","focus":"o","sound":"/pəˈliːs/"},{"word":"connect","focus":"o","sound":"/kəˈnekt/"},{"word":"potato","focus":"o","sound":"/pəˈteɪtoʊ/"}]', 'Which word begins with weak /ə/?', '["police","coke","nose"]', 'police', 8, 1),
    ('u-consonant-e', 'u + 辅音 + e', '第三十六讲 · 长音 u', 'u + 辅音 + e → /juː/ 或 /uː/', '注意 u 的长音', '视频用 use、cube、huge、mule、mute 练习长音 u。', NULL, '[{"word":"use","focus":"u_e","sound":"/juːz/"},{"word":"cube","focus":"u_e","sound":"/kjuːb/"},{"word":"huge","focus":"u_e","sound":"/hjuːdʒ/"},{"word":"mule","focus":"u_e","sound":"/mjuːl/"},{"word":"mute","focus":"u_e","sound":"/mjuːt/"}]', 'Which word follows u + 辅音 + e?', '["cube","cup","cut"]', 'cube', 9, 1),
    ('british-american', '英式与美式发音', '第三十七讲 · 听辨差异', 'BrE 与 AmE', '同一个词可能有不同读法', '视频用 student 和 love 对比英式、美式发音。', NULL, '[{"word":"student","focus":"BrE / AmE","sound":"/ˈstjuːdənt/ · /ˈstuːdənt/"},{"word":"love","focus":"BrE / AmE","sound":"/lʌv/"}]', 'Which word is used to compare British and American pronunciation?', '["student","cube","nose"]', 'student', 10, 1),
    ('weak-u', '非重读 u 读 /ə/', '第三十八讲 · 轻读 u', '非重读 u → /ə/', '轻读、放松', '视频用 upon、autumn、August、circus、virus、lotus 练习。', NULL, '[{"word":"upon","focus":"u","sound":"/əˈpɒn/"},{"word":"autumn","focus":"u","sound":"/ˈɔːtəm/"},{"word":"August","focus":"u","sound":"/ˈɔːɡəst/"},{"word":"circus","focus":"u","sound":"/ˈsɜːrkəs/"},{"word":"virus","focus":"u","sound":"/ˈvaɪrəs/"}]', 'Which word begins with weak /ə/?', '["upon","tune","blue"]', 'upon', 11, 1),
    ('long-u', 'u 的长音', '第三十九讲 · /uː/ 与 /juː/', 'u → /uː/ 或 /juː/', '听清 y 音是否出现', '视频用 student、ruler、tube、blue、tune 练习 u 的长音。', NULL, '[{"word":"student","focus":"u","sound":"/ˈstuːdənt/"},{"word":"ruler","focus":"u","sound":"/ˈruːlər/"},{"word":"tube","focus":"u_e","sound":"/tuːb/"},{"word":"blue","focus":"ue","sound":"/bluː/"},{"word":"tune","focus":"u_e","sound":"/tjuːn/"}]', 'Which word has long u?', '["tune","tub","sun"]', 'tune', 12, 1),
    ('soft-c', '软音 c /s/', '第四十讲 · c 在 e、i、y 前', 'c + e/i/y → /s/', '像 /s/ 一样轻读', '视频用 city、juice、bicycle 练习软音 c。', NULL, '[{"word":"city","focus":"c","sound":"/ˈsɪti/"},{"word":"juice","focus":"c","sound":"/dʒuːs/"},{"word":"bicycle","focus":"c","sound":"/ˈbaɪsɪkəl/"}]', 'Which word has soft c /s/?', '["city","cat","coke"]', 'city', 13, 1),
    ('c-sh', 'c 读 /ʃ/', '第四十一讲 · 特殊 c', 'c → /ʃ/', '注意 -cial、-cious 等组合', '视频用 delicious、official、precious、appreciate、special 练习。', NULL, '[{"word":"delicious","focus":"c","sound":"/dɪˈlɪʃəs/"},{"word":"official","focus":"ci","sound":"/əˈfɪʃəl/"},{"word":"precious","focus":"ci","sound":"/ˈpreʃəs/"},{"word":"appreciate","focus":"ci","sound":"/əˈpriːʃieɪt/"},{"word":"special","focus":"ci","sound":"/ˈspeʃəl/"}]', 'Which word has c pronounced /ʃ/?', '["special","city","cat"]', 'special', 14, 1),
    ('soft-g', '软音 g /dʒ/', '第四十二讲 · g 的变化', 'g → /dʒ/', '注意 g 后的元音', '视频用 orange、giant、Egypt、village、giraffe、ginger、energy 练习。', NULL, '[{"word":"orange","focus":"g","sound":"/ˈɒrɪndʒ/"},{"word":"giant","focus":"g","sound":"/ˈdʒaɪənt/"},{"word":"Egypt","focus":"g","sound":"/ˈiːdʒɪpt/"},{"word":"village","focus":"g","sound":"/ˈvɪlɪdʒ/"},{"word":"ginger","focus":"g","sound":"/ˈdʒɪndʒər/"}]', 'Which word has g pronounced /dʒ/?', '["giant","go","game"]', 'giant', 15, 1),
    ('n-ng', 'n 在 k、g 前读 /ŋ/', '第四十三讲 · 鼻音 n', 'n + k/g → /ŋ/', '张开嘴，鼻腔发声', '视频用 think、uncle、finger、language、tank、English 练习。', NULL, '[{"word":"think","focus":"n","sound":"/θɪŋk/"},{"word":"uncle","focus":"n","sound":"/ˈʌŋkəl/"},{"word":"finger","focus":"n","sound":"/ˈfɪŋɡər/"},{"word":"language","focus":"n","sound":"/ˈlæŋɡwɪdʒ/"},{"word":"tank","focus":"n","sound":"/tæŋk/"}]', 'Which word contains /ŋ/?', '["think","thin","tin"]', 'think', 16, 1),
    ('s-z', 's 读 /z/', '第四十四讲 · 浊音 s', 's → /z/', '声带振动', '视频用 music、cousin、desert、disease、season 练习。', NULL, '[{"word":"music","focus":"s","sound":"/ˈmjuːzɪk/"},{"word":"cousin","focus":"s","sound":"/ˈkʌzən/"},{"word":"desert","focus":"s","sound":"/ˈdezərt/"},{"word":"disease","focus":"s","sound":"/dɪˈziːz/"},{"word":"season","focus":"s","sound":"/ˈsiːzən/"}]', 'Which word has s pronounced /z/?', '["music","sit","sun"]', 'music', 17, 1),
    ('plural-s-z', '词尾 s 读 /z/', '第四十五讲 · 复数词尾', '词尾 s → /z/', '带着声音读词尾', '视频用 shoes、balloons、bags、cabs、mugs、Wednesday 练习。', NULL, '[{"word":"shoes","focus":"s","sound":"/ʃuːz/"},{"word":"balloons","focus":"s","sound":"/bəˈluːnz/"},{"word":"bags","focus":"s","sound":"/bæɡz/"},{"word":"cabs","focus":"s","sound":"/kæbz/"},{"word":"mugs","focus":"s","sound":"/mʌɡz/"}]', 'Which plural ends in /z/?', '["bags","cats","books"]', 'bags', 18, 1),
    ('s-zh', 's 读 /ʒ/', '第四十六讲 · 特殊 s', 's → /ʒ/', '声音柔和、连贯', '视频用 treasure、casual、television、pleasure、visual、decision、explosion、usually 练习。', NULL, '[{"word":"treasure","focus":"s","sound":"/ˈtreʒər/"},{"word":"casual","focus":"s","sound":"/ˈkæʒuəl/"},{"word":"television","focus":"s","sound":"/ˈtelɪvɪʒn/"},{"word":"pleasure","focus":"s","sound":"/ˈpleʒər/"},{"word":"decision","focus":"s","sound":"/dɪˈsɪʒn/"}]', 'Which word has s pronounced /ʒ/?', '["pleasure","season","sit"]', 'pleasure', 19, 1),
    ('t-sh', 't 的特殊读音', '第四十七讲 · /ʃ/ 与 /tʃ/', 'tion / ture', '注意字母组合整体发音', '视频用 operation、nation、station、picture、lecture、future、vacation 练习。', NULL, '[{"word":"operation","focus":"tion","sound":"/ˌɒpəˈreɪʃn/"},{"word":"nation","focus":"tion","sound":"/ˈneɪʃn/"},{"word":"station","focus":"tion","sound":"/ˈsteɪʃn/"},{"word":"picture","focus":"ture","sound":"/ˈpɪktʃər/"},{"word":"future","focus":"ture","sound":"/ˈfjuːtʃər/"}]', 'Which word contains tion pronounced /ʃn/?', '["nation","notionless","net"]', 'nation', 20, 1),
    ('x-sounds', 'x 的两种常见读音', '第四十八讲 · /ks/ 与 /ɡz/', 'x → /ks/ 或 /ɡz/', '听清 x 前后的声音', '视频用 axe、fox、six、exist、examine、exit、example、exam 练习。', NULL, '[{"word":"axe","focus":"x","sound":"/æks/"},{"word":"fox","focus":"x","sound":"/fɒks/"},{"word":"six","focus":"x","sound":"/sɪks/"},{"word":"exist","focus":"x","sound":"/ɪɡˈzɪst/"},{"word":"examine","focus":"x","sound":"/ɪɡˈzæmɪn/"},{"word":"exit","focus":"x","sound":"/ˈeɡzɪt/"},{"word":"example","focus":"x","sound":"/ɪɡˈzɑːmpəl/"}]', 'Which word has x pronounced /ɡz/?', '["exist","fox","six"]', 'exist', 21, 1)
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `subtitle` = VALUES(`subtitle`),
    `pattern_text` = VALUES(`pattern_text`),
    `sound_text` = VALUES(`sound_text`),
    `learning_tip` = VALUES(`learning_tip`),
    `review_examples_json` = VALUES(`review_examples_json`),
    `examples_json` = VALUES(`examples_json`),
    `quiz_prompt` = VALUES(`quiz_prompt`),
    `quiz_choices_json` = VALUES(`quiz_choices_json`),
    `quiz_answer` = VALUES(`quiz_answer`),
    `priority_order` = VALUES(`priority_order`),
    `is_active` = VALUES(`is_active`);
-- Seeded 21 natural phonics lessons.
