-- Extracted from video/49.mp4, video/50.mp4 and video/51.mp4.
-- Existing schema: phonics_lesson; append after lessons 28-48 (orders 1-21).
-- See phonics_lessons_49_to_51.md for sources, timestamps and editorial additions.
-- Re-running updates only these three lesson_code values; no existing lessons are deleted.
-- Select the intended database before running this file.
SET NAMES utf8mb4;
START TRANSACTION;

INSERT INTO `phonics_lesson` (
    `lesson_code`, `title`, `subtitle`, `pattern_text`, `sound_text`, `learning_tip`, `review_examples_json`, `examples_json`, `quiz_prompt`, `quiz_choices_json`, `quiz_answer`, `priority_order`, `is_active`
) VALUES
    (
        'weak-final-y',
        '弱读词尾 y 读 /i/',
        '第四十九讲 · 咧开嘴角',
        '非重读词尾 y → /i/',
        '嘴角向两边展开，轻读词尾 y',
        '先复习 yoga、yes、you 中词首 y 的 /j/ 音，再练习 city、lovely、country、candy、sleepy。y 位于单词结尾的非重读音节时，通常读 /i/；视频提示“咧开嘴角”，前面的重读音节突出，词尾轻而干脆。自主拼读 happy、angry；跟读例句：I am very angry.',
        '[{"word":"yoga","focus":"y","sound":"/ˈjoʊɡə/"},{"word":"yes","focus":"y","sound":"/jes/"},{"word":"you","focus":"y","sound":"/juː/"}]',
        '[{"word":"city","focus":"y","sound":"/ˈsɪti/"},{"word":"lovely","focus":"y","sound":"/ˈlʌvli/"},{"word":"country","focus":"y","sound":"/ˈkʌntri/"},{"word":"candy","focus":"y","sound":"/ˈkændi/"},{"word":"sleepy","focus":"y","sound":"/ˈsliːpi/"},{"word":"happy","focus":"y","sound":"/ˈhæpi/"},{"word":"angry","focus":"y","sound":"/ˈæŋɡri/"}]',
        'Which word ends with y pronounced /i/?',
        '["yes","city","you"]',
        'city',
        22,
        1
    ),
    (
        'ai-long-a',
        '元音组合 ai 读 /eɪ/',
        '第五十讲 · 由扁到更扁',
        '重读音节中的 ai → /eɪ/',
        '从 /e/ 滑向 /ɪ/，口型由扁到更扁',
        '视频先用 tail、brain、paint 及一组 ai 单词引入元音字母组合，再练习 rain、nail、waitress、snail。把 ai 作为一个整体拼读，在这些重读音节中读 /eɪ/，发音技巧是“由扁到更扁”。自主拼读 waiter、train；跟读例句：Let''s get on the train.',
        '[{"word":"tail","focus":"ai","sound":"/teɪl/"},{"word":"brain","focus":"ai","sound":"/breɪn/"},{"word":"paint","focus":"ai","sound":"/peɪnt/"},{"word":"Spain","focus":"ai","sound":"/speɪn/"},{"word":"raise","focus":"ai","sound":"/reɪz/"},{"word":"gain","focus":"ai","sound":"/ɡeɪn/"},{"word":"maid","focus":"ai","sound":"/meɪd/"},{"word":"sail","focus":"ai","sound":"/seɪl/"},{"word":"wait","focus":"ai","sound":"/weɪt/"},{"word":"mail","focus":"ai","sound":"/meɪl/"},{"word":"failure","focus":"ai","sound":"/ˈfeɪljər/"}]',
        '[{"word":"rain","focus":"ai","sound":"/reɪn/"},{"word":"nail","focus":"ai","sound":"/neɪl/"},{"word":"waitress","focus":"ai","sound":"/ˈweɪtrəs/"},{"word":"snail","focus":"ai","sound":"/sneɪl/"},{"word":"waiter","focus":"ai","sound":"/ˈweɪtər/"},{"word":"train","focus":"ai","sound":"/treɪn/"}]',
        'Which word has ai pronounced /eɪ/?',
        '["city","card","rain"]',
        'rain',
        23,
        1
    ),
    (
        'ar-sounds',
        'ar 的重读、弱读与特殊读音',
        '第五十一讲 · 三种 ar 发音',
        'ar：重读 /ɑːr/；弱读 /ər/；w 后常读 /ɔːr/（美式）',
        '重读饱满有力，弱读轻声快速；注意保留美式 r 音',
        '视频用 party、card 练习重读 ar，用 dollar、beggar 练习非重读词尾 ar，并用 war 示范 w 后 ar 的另一种读音。重读发音技巧是“饱满、有力”；弱读轻声快速，不拖长。自主拼读 sugar、scarf。本课按视频的美式示范保留 r 音；/ər/ 也常记作 /ɚ/。',
        NULL,
        '[{"word":"party","focus":"ar","sound":"/ˈpɑːrti/"},{"word":"card","focus":"ar","sound":"/kɑːrd/"},{"word":"war","focus":"ar","sound":"/wɔːr/"},{"word":"dollar","focus":"ar","sound":"/ˈdɑːlər/"},{"word":"beggar","focus":"ar","sound":"/ˈbeɡər/"},{"word":"sugar","focus":"ar","sound":"/ˈʃʊɡər/"},{"word":"scarf","focus":"ar","sound":"/skɑːrf/"}]',
        'Which word has unstressed final ar pronounced /ər/ in American English?',
        '["party","beggar","scarf"]',
        'beggar',
        24,
        1
    )
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

COMMIT;
