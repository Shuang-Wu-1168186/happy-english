# every day spoken sentences
CREATE TABLE everyday_sentence (
                                   id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
                                   tag VARCHAR(100) NOT NULL COMMENT '分类标签',
                                   en TEXT NOT NULL COMMENT '英文句子',
                                   cn TEXT NOT NULL COMMENT '中文释义',
                                   note TEXT COMMENT '备注说明',
                                   share_status TINYINT NOT NULL DEFAULT 0 COMMENT '共享状态：0-私有，1-共享',
                                   priority_order INT NOT NULL DEFAULT 0 COMMENT '排序值，越小越靠前',

                                   created_by BIGINT NOT NULL COMMENT '创建人ID',
                                   created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                   updated_by BIGINT DEFAULT NULL COMMENT '修改人ID',
                                   updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',

                                   PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='日常英文句子表';


CREATE TABLE `user` (
                        `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
                        `username` VARCHAR(100) NOT NULL COMMENT '用户名',
                        `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希',
                        `full_name` VARCHAR(100) NOT NULL COMMENT '姓名',
                        `email` VARCHAR(150) DEFAULT NULL COMMENT '邮箱',
                        `contact_number` VARCHAR(30) DEFAULT NULL COMMENT '联系电话',
                        `home_address` VARCHAR(255) DEFAULT NULL COMMENT '家庭住址',
                        `role` VARCHAR(50) NOT NULL DEFAULT 'user' COMMENT '角色',
                        `status` VARCHAR(50) NOT NULL DEFAULT 'active' COMMENT '状态',
                        `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                        `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                        PRIMARY KEY (`id`),
                        UNIQUE KEY `uk_user_username` (`username`),
                        UNIQUE KEY `uk_user_email` (`email`),
                        UNIQUE KEY `uk_user_contact_number` (`contact_number`),
                        KEY `idx_user_role` (`role`),
                        KEY `idx_user_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';


CREATE TABLE `login_audit` (
                              `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '登录审计记录主键ID',
                              `user_id` BIGINT UNSIGNED DEFAULT NULL COMMENT '成功登录的用户ID；未知账号登录失败时为空',
                              `username` VARCHAR(100) NOT NULL COMMENT '登录时输入的用户名',
                              `full_name` VARCHAR(100) DEFAULT NULL COMMENT '成功登录时的姓名快照',
                              `login_ip` VARCHAR(45) DEFAULT NULL COMMENT 'IPv4 或 IPv6 登录地址',
                              `user_agent` VARCHAR(1000) DEFAULT NULL COMMENT '浏览器 User-Agent',
                              `success` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否登录成功：0-失败，1-成功',
                              `logged_in_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '登录尝试时间',

                              PRIMARY KEY (`id`),
                              KEY `idx_login_audit_logged_in_at` (`logged_in_at`),
                              KEY `idx_login_audit_user_logged_in_at` (`user_id`, `logged_in_at`),
                              KEY `idx_login_audit_ip_logged_in_at` (`login_ip`, `logged_in_at`),
                              CONSTRAINT `fk_login_audit_user`
                                  FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户登录审计记录';


# kids English cards
# 主表保存卡片的核心信息；例句、音节发音片段和词族使用子表保存。
CREATE TABLE `kids_english_card` (
                                    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '卡片主键ID',
                                    `word` VARCHAR(100) NOT NULL COMMENT '英文单词或词组',
                                    `translation` VARCHAR(255) NOT NULL COMMENT '中文释义',
                                    `phonics` VARCHAR(100) DEFAULT NULL COMMENT '完整音标',
                                    `part_of_speech` VARCHAR(50) DEFAULT NULL COMMENT '词性：noun、verb、adjective 等',
                                    `level` VARCHAR(30) NOT NULL DEFAULT 'Core' COMMENT '学习难度：Core、Stretch 等',
                                    `syllables` VARCHAR(255) DEFAULT NULL COMMENT '音节拆分展示文本，例如 sun · light',
                                    `stress` VARCHAR(255) DEFAULT NULL COMMENT '重读位置展示文本，例如 SUN-light',
                                    `phonics_focus` VARCHAR(255) DEFAULT NULL COMMENT '自然拼读重点，例如 ai → /eɪ/',
                                    `syllable_tip` TEXT NULL COMMENT '音节拆分说明',
                                    `category` VARCHAR(100) NOT NULL COMMENT '卡片分类',
                                    `emoji` VARCHAR(32) DEFAULT NULL COMMENT '卡片图示或 emoji',
                                    `image_url` VARCHAR(255) DEFAULT NULL COMMENT '帮助记忆的插画路径',
                                    `tip` TEXT COMMENT '学习提示',
                                    `priority_order` INT NOT NULL DEFAULT 0 COMMENT '排序值，越小越靠前',
                                    `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用：0-否，1-是',
                                    `created_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '创建人ID',
                                    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                                    `updated_by` BIGINT UNSIGNED DEFAULT NULL COMMENT '修改人ID',
                                    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',

                                    PRIMARY KEY (`id`),
                                    KEY `idx_kids_card_category` (`category`),
                                    KEY `idx_kids_card_level` (`level`),
                                    KEY `idx_kids_card_active_order` (`is_active`, `priority_order`),
                                    CONSTRAINT `fk_kids_card_created_by` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON DELETE SET NULL,
                                    CONSTRAINT `fk_kids_card_updated_by` FOREIGN KEY (`updated_by`) REFERENCES `user` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='儿童英语学习卡片主表';


CREATE TABLE `kids_english_card_sound_part` (
                                                `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '音节片段主键ID',
                                                `card_id` BIGINT UNSIGNED NOT NULL COMMENT '儿童英语卡片ID',
                                                `part_order` INT NOT NULL COMMENT '音节顺序，从1开始',
                                                `chunk` VARCHAR(100) NOT NULL COMMENT '拼读片段，例如 play',
                                                `pronunciation` VARCHAR(100) NOT NULL COMMENT '该片段发音，例如 /pleɪ/',

                                                PRIMARY KEY (`id`),
                                                UNIQUE KEY `uk_kids_sound_card_order` (`card_id`, `part_order`),
                                                KEY `idx_kids_sound_card` (`card_id`),
                                                CONSTRAINT `fk_kids_sound_card` FOREIGN KEY (`card_id`) REFERENCES `kids_english_card` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='儿童英语卡片音节发音片段表';


CREATE TABLE `kids_english_card_example` (
                                             `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '例句主键ID',
                                             `card_id` BIGINT UNSIGNED NOT NULL COMMENT '儿童英语卡片ID',
                                             `example_text` TEXT NOT NULL COMMENT '英文例句',
                                             `translation` TEXT NOT NULL COMMENT '例句中文翻译',
                                             `priority_order` INT NOT NULL DEFAULT 0 COMMENT '例句排序值，越小越靠前',
                                             `is_active` TINYINT(1) NOT NULL DEFAULT 1 COMMENT '是否启用：0-否，1-是',

                                             PRIMARY KEY (`id`),
                                             KEY `idx_kids_example_card_order` (`card_id`, `priority_order`),
                                             CONSTRAINT `fk_kids_example_card` FOREIGN KEY (`card_id`) REFERENCES `kids_english_card` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='儿童英语卡片例句表';


CREATE TABLE `kids_english_card_word_family` (
                                                  `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '词族成员主键ID',
                                                  `card_id` BIGINT UNSIGNED NOT NULL COMMENT '儿童英语卡片ID',
                                                  `related_word` VARCHAR(100) NOT NULL COMMENT '相关词，例如 cyclist',
                                                  `part_of_speech` VARCHAR(50) DEFAULT NULL COMMENT '相关词词性',
                                                  `meaning` VARCHAR(255) DEFAULT NULL COMMENT '相关词中文释义',
                                                  `priority_order` INT NOT NULL DEFAULT 0 COMMENT '词族成员排序值',

                                                  PRIMARY KEY (`id`),
                                                  KEY `idx_kids_family_card_order` (`card_id`, `priority_order`),
                                                  CONSTRAINT `fk_kids_family_card` FOREIGN KEY (`card_id`) REFERENCES `kids_english_card` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='儿童英语卡片词族拓展表';


# Word List (1) image import.
# The imported core rows are enriched below with IPA, syllable splitting,
# phonics notes, memory illustrations, examples and optional word-family data.
INSERT INTO `kids_english_card`
(`word`, `translation`, `category`, `priority_order`)
VALUES
('northeast', '东北部', 'Unit 1 · 1', 1),
('beach', '海滩；沙滩', 'Unit 1 · 1', 2),
('wonderful', '极好的；精彩的', 'Unit 1 · 1', 3),
('safety', '安全', 'Unit 1 · 1', 4),
('rule', '规则；条例', 'Unit 1 · 1', 5),
('meaningful', '有意义的', 'Unit 1 · 2', 6),
('National Library of China', '中国国家图书馆', 'Unit 1 · 2', 7),
('on foot', '走路；步行', 'Unit 1 · 2', 8),
('China Science and Technology Museum', '中国科学技术馆', 'Unit 1 · 2', 9),
('far from', '离……远', 'Unit 1 · 2', 10),
('baby', '动物幼崽；婴儿', 'Unit 1 · 3', 11),
('chick', '小鸡', 'Unit 1 · 3', 12),
('sometimes', '有时', 'Unit 1 · 3', 13),
('go fishing', '去钓鱼', 'Unit 1 · 3', 14),
('daytime', '白天', 'Unit 1 · 4', 15),
('university', '大学', 'Unit 1 · 4', 16),
('Toronto', '多伦多', 'Unit 1 · 4', 17),
('Ottawa', '渥太华', 'Unit 1 · 4', 18),
('hospital', '医院', 'Unit 2 · 5', 19),
('move', '（使）移动', 'Unit 2 · 5', 20),
('head', '头', 'Unit 2 · 5', 21),
('helmet', '头盔；安全帽', 'Unit 2 · 5', 22),
('follow', '遵循；听从；跟踪', 'Unit 2 · 5', 23),
('stomachache', '胃痛；肚子痛', 'Unit 2 · 6', 24),
('touch', '触摸；碰触', 'Unit 2 · 6', 25),
('bowl', '碗；钵', 'Unit 2 · 6', 26),
('advice', '忠告；劝告；建议', 'Unit 2 · 6', 27),
('too much', '太多', 'Unit 2 · 6', 28),
('right after', '紧接着；在……之后', 'Unit 2 · 6', 29),
('those', '那些（that 的复数）', 'Unit 2 · 6', 30),
('fire', '失火；火灾', 'Unit 2 · 7', 31),
('turn into', '转变成；变成', 'Unit 2 · 7', 32),
('candle', '蜡烛', 'Unit 2 · 7', 33),
('danger', '危险；危险因素', 'Unit 2 · 7', 34),
('talk', '说话；交谈', 'Unit 2 · 7', 35),
('exit', '出口', 'Unit 2 · 7', 36),
('right away', '立刻；马上', 'Unit 2 · 7', 37),
('cover', '盖；覆盖', 'Unit 2 · 7', 38),
('lift', '电梯', 'Unit 2 · 7', 39),
('firefighter', '消防员', 'Unit 2 · 7', 40),
('put out', '熄灭', 'Unit 2 · 7', 41),
('blow', '擤（鼻子）；（风）刮、吹；吹气', 'Unit 2 · 8', 42),
('or', '或；或者；还是', 'Unit 2 · 8', 43),
('cup', '杯子', 'Unit 2 · 8', 44),
('stranger', '陌生人', 'Unit 2 · 8', 45),
('body', '（人、动物的）身体', 'Unit 2 · 8', 46),
('someone', '某人', 'Unit 2 · 8', 47),
('reason', '理由；原因', 'Unit 2 · 8', 48),
('uncomfortable', '不自在的；不舒服的', 'Unit 2 · 8', 49),
('technology', '科技', 'Unit 3 · 9', 50),
('habit', '习惯；惯例', 'Unit 3 · 9', 51),
('the past', '过去', 'Unit 3 · 9', 52),
('keep in touch', '保持联系', 'Unit 3 · 9', 53),
('change', '改变；变化', 'Unit 3 · 9', 54),
('communication', '交流；沟通', 'Unit 3 · 9', 55),
('anytime', '任何时候', 'Unit 3 · 9', 56),
('anywhere', '任何地点', 'Unit 3 · 9', 57),
('connect', '联系；连接', 'Unit 3 · 9', 58),
('Smart Education of China', '国家智慧教育公共服务平台', 'Unit 3 · 10', 59),
('platform', '平台', 'Unit 3 · 10', 60),
('VR (Virtual Reality)', '虚拟现实', 'Unit 3 · 10', 61),
('for example', '例如', 'Unit 3 · 10', 62),
('Finland', '芬兰', 'Unit 3 · 10', 63),
('railway', '铁路', 'Unit 3 · 11', 64),
('connect', '联系；连接', 'Unit 3 · 11', 65),
('go into service', '开始使用', 'Unit 3 · 11', 66),
('think', '思考', 'Unit 3 · 11', 67),
('build', '建造', 'Unit 3 · 11', 68),
('Beidou Navigation (abbr. BDS)', '北斗卫星导航系统', 'Unit 3 · 12', 69),
('Earth', '地球', 'Unit 3 · 12', 70);

# Enriched content for the imported 70-word list: IPA, phonics, images and child rows.
UPDATE `kids_english_card` SET `phonics`='/ˌnɔːrθˈiːst/', `part_of_speech`='noun', `level`='Core', `syllables`='north · east', `stress`='north-EAST', `phonics_focus`='or → /ɔːr/; ea → /iː/', `syllable_tip`='拆分练习：north / east。注意：or → /ɔːr/; ea → /iː/。', `image_url`='/static/uploads/kids_cards/northeast-wide.png', `tip`=NULL WHERE `priority_order`=1;
UPDATE `kids_english_card` SET `phonics`='/biːtʃ/', `part_of_speech`='noun', `level`='Core', `syllables`='beach', `stress`='BEACH', `phonics_focus`='ea → /iː/; tch → /tʃ/', `syllable_tip`='拆分练习：beach。注意：ea → /iː/; tch → /tʃ/。', `image_url`='/static/uploads/kids_cards/beach-wide.png', `tip`=NULL WHERE `priority_order`=2;
UPDATE `kids_english_card` SET `phonics`='/ˈwʌndərfəl/', `part_of_speech`='adjective', `level`='Core', `syllables`='won · der · ful', `stress`='WON-der-ful', `phonics_focus`='o → /ʌ/ in won; -ful → /fəl/', `syllable_tip`='拆分练习：won / der / ful。注意：o → /ʌ/ in won; -ful → /fəl/。', `image_url`='/static/uploads/kids_cards/wonderful-wide.png', `tip`=NULL WHERE `priority_order`=3;
UPDATE `kids_english_card` SET `phonics`='/ˈseɪfti/', `part_of_speech`='noun', `level`='Core', `syllables`='safe · ty', `stress`='SAFE-ty', `phonics_focus`='a_e → /eɪ/; y → /iː/', `syllable_tip`='拆分练习：safe / ty。注意：a_e → /eɪ/; y → /iː/。', `image_url`='/static/uploads/kids_cards/safety-wide.png', `tip`=NULL WHERE `priority_order`=4;
UPDATE `kids_english_card` SET `phonics`='/ruːl/', `part_of_speech`='noun', `level`='Core', `syllables`='rule', `stress`='RULE', `phonics_focus`='u_e → /uː/; final e silent', `syllable_tip`='拆分练习：rule。注意：u_e → /uː/; final e silent。', `image_url`='/static/uploads/kids_cards/rule-wide.png', `tip`=NULL WHERE `priority_order`=5;
UPDATE `kids_english_card` SET `phonics`='/ˈmiːnɪŋfəl/', `part_of_speech`='adjective', `level`='Core', `syllables`='mean · ing · ful', `stress`='MEAN-ing-ful', `phonics_focus`='ea → /iː/; -ing → /ɪŋ/', `syllable_tip`='拆分练习：mean / ing / ful。注意：ea → /iː/; -ing → /ɪŋ/。', `image_url`='/static/uploads/kids_cards/meaningful-wide.png', `tip`=NULL WHERE `priority_order`=6;
UPDATE `kids_english_card` SET `phonics`='/ˈnæʃənəl ˈlaɪbreri əv ˈtʃaɪnə/', `part_of_speech`='proper noun', `level`='Core', `syllables`='Na · tion · al Li · bra · ry of Chi · na', `stress`='NAT-ion-al LIB-rar-y of CHI-na', `phonics_focus`='tion → /ʃən/; br → /br/; ch → /tʃ/', `syllable_tip`='拆分练习：Na / tion / al Li / bra / ry of Chi / na。注意：tion → /ʃən/; br → /br/; ch → /tʃ/。', `image_url`='/static/uploads/kids_cards/national-library-of-china-wide.png', `tip`=NULL WHERE `priority_order`=7;
UPDATE `kids_english_card` SET `phonics`='/ɒn fʊt/', `part_of_speech`='phrase', `level`='Core', `syllables`='on foot', `stress`='ON FOOT', `phonics_focus`='oo → /ʊ/ in foot', `syllable_tip`='拆分练习：on foot。注意：oo → /ʊ/ in foot。', `image_url`='/static/uploads/kids_cards/on-foot-wide.png', `tip`=NULL WHERE `priority_order`=8;
UPDATE `kids_english_card` SET `phonics`='/ˈtʃaɪnə ˈsaɪəns ənd tekˈnɒlədʒi mjuˈziːəm/', `part_of_speech`='proper noun', `level`='Core', `syllables`='Chi · na Sci · ence and Tech · nol · o · gy Mu · se · um', `stress`='CHI-na SCI-ence and tech-NOL-o-gy mu-SE-um', `phonics_focus`='ch → /tʃ/; c → /s/ in science; -gy → /dʒi/', `syllable_tip`='拆分练习：Chi / na Sci / ence and Tech / nol / o / gy Mu / se / um。注意：ch → /tʃ/; c → /s/ in science; -gy → /dʒi/。', `image_url`='/static/uploads/kids_cards/china-science-and-technology-museum-wide.png', `tip`=NULL WHERE `priority_order`=9;
UPDATE `kids_english_card` SET `phonics`='/fɑːr frəm/', `part_of_speech`='phrase', `level`='Core', `syllables`='far from', `stress`='FAR from', `phonics_focus`='ar → /ɑːr/; from → /frəm/', `syllable_tip`='拆分练习：far from。注意：ar → /ɑːr/; from → /frəm/。', `image_url`='/static/uploads/kids_cards/far-from-wide.png', `tip`=NULL WHERE `priority_order`=10;
UPDATE `kids_english_card` SET `phonics`='/ˈbeɪbi/', `part_of_speech`='noun', `level`='Core', `syllables`='ba · by', `stress`='BA-by', `phonics_focus`='a → /eɪ/; y → /i/', `syllable_tip`='拆分练习：ba / by。注意：a → /eɪ/; y → /i/。', `image_url`='/static/uploads/kids_cards/baby-wide.png', `tip`=NULL WHERE `priority_order`=11;
UPDATE `kids_english_card` SET `phonics`='/tʃɪk/', `part_of_speech`='noun', `level`='Core', `syllables`='chick', `stress`='CHICK', `phonics_focus`='ch → /tʃ/; ck → /k/', `syllable_tip`='拆分练习：chick。注意：ch → /tʃ/; ck → /k/。', `image_url`='/static/uploads/kids_cards/chick-wide.png', `tip`=NULL WHERE `priority_order`=12;
UPDATE `kids_english_card` SET `phonics`='/ˈsʌmtaɪmz/', `part_of_speech`='adverb', `level`='Core', `syllables`='some · times', `stress`='SOME-times', `phonics_focus`='o → /ʌ/ in some; i_e → /aɪ/', `syllable_tip`='拆分练习：some / times。注意：o → /ʌ/ in some; i_e → /aɪ/。', `image_url`='/static/uploads/kids_cards/sometimes-wide.png', `tip`=NULL WHERE `priority_order`=13;
UPDATE `kids_english_card` SET `phonics`='/ɡoʊ ˈfɪʃɪŋ/', `part_of_speech`='phrase', `level`='Core', `syllables`='go fish · ing', `stress`='GO FISH-ing', `phonics_focus`='o → /oʊ/; sh → /ʃ/; -ing → /ɪŋ/', `syllable_tip`='拆分练习：go fish / ing。注意：o → /oʊ/; sh → /ʃ/; -ing → /ɪŋ/。', `image_url`='/static/uploads/kids_cards/go-fishing-wide.png', `tip`=NULL WHERE `priority_order`=14;
UPDATE `kids_english_card` SET `phonics`='/ˈdeɪtaɪm/', `part_of_speech`='noun', `level`='Core', `syllables`='day · time', `stress`='DAY-time', `phonics_focus`='ay → /eɪ/; i_e → /aɪ/', `syllable_tip`='拆分练习：day / time。注意：ay → /eɪ/; i_e → /aɪ/。', `image_url`='/static/uploads/kids_cards/daytime-wide.png', `tip`=NULL WHERE `priority_order`=15;
UPDATE `kids_english_card` SET `phonics`='/ˌjuːnɪˈvɜːrsəti/', `part_of_speech`='noun', `level`='Core', `syllables`='u · ni · ver · si · ty', `stress`='u-ni-VER-si-ty', `phonics_focus`='u → /juː/; er → /ər/; -ity → /əti/', `syllable_tip`='拆分练习：u / ni / ver / si / ty。注意：u → /juː/; er → /ər/; -ity → /əti/。', `image_url`='/static/uploads/kids_cards/university-wide.png', `tip`=NULL WHERE `priority_order`=16;
UPDATE `kids_english_card` SET `phonics`='/təˈrɒntoʊ/', `part_of_speech`='proper noun', `level`='Core', `syllables`='To · ron · to', `stress`='to-RON-to', `phonics_focus`='o → /ɒ/; final o → /oʊ/', `syllable_tip`='拆分练习：To / ron / to。注意：o → /ɒ/; final o → /oʊ/。', `image_url`='/static/uploads/kids_cards/toronto-wide.png', `tip`=NULL WHERE `priority_order`=17;
UPDATE `kids_english_card` SET `phonics`='/ˈɒtəwə/', `part_of_speech`='proper noun', `level`='Core', `syllables`='Ot · ta · wa', `stress`='OT-ta-wa', `phonics_focus`='short o → /ɒ/; unstressed a → /ə/', `syllable_tip`='拆分练习：Ot / ta / wa。注意：short o → /ɒ/; unstressed a → /ə/。', `image_url`='/static/uploads/kids_cards/ottawa-wide.png', `tip`=NULL WHERE `priority_order`=18;
UPDATE `kids_english_card` SET `phonics`='/ˈhɒspɪtəl/', `part_of_speech`='noun', `level`='Core', `syllables`='hos · pi · tal', `stress`='HOS-pi-tal', `phonics_focus`='o → /ɒ/; -al → /əl/', `syllable_tip`='拆分练习：hos / pi / tal。注意：o → /ɒ/; -al → /əl/。', `image_url`='/static/uploads/kids_cards/hospital-wide.png', `tip`=NULL WHERE `priority_order`=19;
UPDATE `kids_english_card` SET `phonics`='/muːv/', `part_of_speech`='verb', `level`='Core', `syllables`='move', `stress`='MOVE', `phonics_focus`='o_e → /uː/; final e silent', `syllable_tip`='拆分练习：move。注意：o_e → /uː/; final e silent。', `image_url`='/static/uploads/kids_cards/move-wide.png', `tip`=NULL WHERE `priority_order`=20;
UPDATE `kids_english_card` SET `phonics`='/hɛd/', `part_of_speech`='noun', `level`='Core', `syllables`='head', `stress`='HEAD', `phonics_focus`='ea → /ɛ/', `syllable_tip`='拆分练习：head。注意：ea → /ɛ/。', `image_url`='/static/uploads/kids_cards/head-wide.png', `tip`=NULL WHERE `priority_order`=21;
UPDATE `kids_english_card` SET `phonics`='/ˈhɛlmɪt/', `part_of_speech`='noun', `level`='Core', `syllables`='hel · met', `stress`='HEL-met', `phonics_focus`='short e → /ɛ/; closed syllables', `syllable_tip`='拆分练习：hel / met。注意：short e → /ɛ/; closed syllables。', `image_url`='/static/uploads/kids_cards/helmet-wide.png', `tip`=NULL WHERE `priority_order`=22;
UPDATE `kids_english_card` SET `phonics`='/ˈfɒloʊ/', `part_of_speech`='verb', `level`='Core', `syllables`='fol · low', `stress`='FOL-low', `phonics_focus`='ow → /oʊ/', `syllable_tip`='拆分练习：fol / low。注意：ow → /oʊ/。', `image_url`='/static/uploads/kids_cards/follow-wide.png', `tip`=NULL WHERE `priority_order`=23;
UPDATE `kids_english_card` SET `phonics`='/ˈstʌməkeɪk/', `part_of_speech`='noun', `level`='Core', `syllables`='stom · ach · ache', `stress`='STOM-ach-ACHE', `phonics_focus`='ch → /k/; ache → /eɪk/', `syllable_tip`='拆分练习：stom / ach / ache。注意：ch → /k/; ache → /eɪk/。', `image_url`='/static/uploads/kids_cards/stomachache-wide.png', `tip`=NULL WHERE `priority_order`=24;
UPDATE `kids_english_card` SET `phonics`='/tʌtʃ/', `part_of_speech`='verb', `level`='Core', `syllables`='touch', `stress`='TOUCH', `phonics_focus`='ou → /ʌ/; tch → /tʃ/', `syllable_tip`='拆分练习：touch。注意：ou → /ʌ/; tch → /tʃ/。', `image_url`='/static/uploads/kids_cards/touch-wide.png', `tip`=NULL WHERE `priority_order`=25;
UPDATE `kids_english_card` SET `phonics`='/boʊl/', `part_of_speech`='noun', `level`='Core', `syllables`='bowl', `stress`='BOWL', `phonics_focus`='ow → /oʊ/', `syllable_tip`='拆分练习：bowl。注意：ow → /oʊ/。', `image_url`='/static/uploads/kids_cards/bowl-wide.png', `tip`=NULL WHERE `priority_order`=26;
UPDATE `kids_english_card` SET `phonics`='/ədˈvaɪs/', `part_of_speech`='noun', `level`='Core', `syllables`='ad · vice', `stress`='ad-VICE', `phonics_focus`='i_e → /aɪ/; c → /s/', `syllable_tip`='拆分练习：ad / vice。注意：i_e → /aɪ/; c → /s/。', `image_url`='/static/uploads/kids_cards/advice-wide.png', `tip`=NULL WHERE `priority_order`=27;
UPDATE `kids_english_card` SET `phonics`='/tuː mʌtʃ/', `part_of_speech`='phrase', `level`='Core', `syllables`='too much', `stress`='too MUCH', `phonics_focus`='oo → /uː/; ou → /ʌ/', `syllable_tip`='拆分练习：too much。注意：oo → /uː/; ou → /ʌ/。', `image_url`='/static/uploads/kids_cards/too-much.png', `tip`=NULL WHERE `priority_order`=28;
UPDATE `kids_english_card` SET `phonics`='/raɪt ˈæftər/', `part_of_speech`='phrase', `level`='Core', `syllables`='right af · ter', `stress`='RIGHT af-ter', `phonics_focus`='igh → /aɪ/; er → /ər/', `syllable_tip`='拆分练习：right af / ter。注意：igh → /aɪ/; er → /ər/。', `image_url`='/static/uploads/kids_cards/right-after.png', `tip`=NULL WHERE `priority_order`=29;
UPDATE `kids_english_card` SET `phonics`='/ðoʊz/', `part_of_speech`='determiner', `level`='Core', `syllables`='those', `stress`='THOSE', `phonics_focus`='th → /ð/; o_e → /oʊ/; s → /z/', `syllable_tip`='拆分练习：those。注意：th → /ð/; o_e → /oʊ/; s → /z/。', `image_url`='/static/uploads/kids_cards/those.png', `tip`=NULL WHERE `priority_order`=30;
UPDATE `kids_english_card` SET `phonics`='/ˈfaɪər/', `part_of_speech`='noun', `level`='Core', `syllables`='fire', `stress`='FIRE', `phonics_focus`='ire → /aɪər/', `syllable_tip`='拆分练习：fire。注意：ire → /aɪər/。', `image_url`='/static/uploads/kids_cards/fire.png', `tip`=NULL WHERE `priority_order`=31;
UPDATE `kids_english_card` SET `phonics`='/tɜːrn ˈɪntuː/', `part_of_speech`='phrase', `level`='Core', `syllables`='turn in · to', `stress`='TURN IN-to', `phonics_focus`='ur → /ɜːr/; oo → /uː/', `syllable_tip`='拆分练习：turn in / to。注意：ur → /ɜːr/; oo → /uː/。', `image_url`='/static/uploads/kids_cards/turn-into.png', `tip`=NULL WHERE `priority_order`=32;
UPDATE `kids_english_card` SET `phonics`='/ˈkændəl/', `part_of_speech`='noun', `level`='Core', `syllables`='can · dle', `stress`='CAND-le', `phonics_focus`='-le → /əl/', `syllable_tip`='拆分练习：can / dle。注意：-le → /əl/。', `image_url`='/static/uploads/kids_cards/candle.png', `tip`=NULL WHERE `priority_order`=33;
UPDATE `kids_english_card` SET `phonics`='/ˈdeɪndʒər/', `part_of_speech`='noun', `level`='Core', `syllables`='dan · ger', `stress`='DAN-ger', `phonics_focus`='a → /eɪ/; ge → /dʒ/', `syllable_tip`='拆分练习：dan / ger。注意：a → /eɪ/; ge → /dʒ/。', `image_url`='/static/uploads/kids_cards/danger.png', `tip`=NULL WHERE `priority_order`=34;
UPDATE `kids_english_card` SET `phonics`='/tɔːk/', `part_of_speech`='verb', `level`='Core', `syllables`='talk', `stress`='TALK', `phonics_focus`='al → /ɔː/; l silent', `syllable_tip`='拆分练习：talk。注意：al → /ɔː/; l silent。', `image_url`='/static/uploads/kids_cards/talk.png', `tip`=NULL WHERE `priority_order`=35;
UPDATE `kids_english_card` SET `phonics`='/ˈɛɡzɪt/', `part_of_speech`='noun', `level`='Core', `syllables`='ex · it', `stress`='EX-it', `phonics_focus`='x → /ɡz/; short i → /ɪ/', `syllable_tip`='拆分练习：ex / it。注意：x → /ɡz/; short i → /ɪ/。', `image_url`='/static/uploads/kids_cards/exit.png', `tip`=NULL WHERE `priority_order`=36;
UPDATE `kids_english_card` SET `phonics`='/raɪt əˈweɪ/', `part_of_speech`='phrase', `level`='Core', `syllables`='right a · way', `stress`='RIGHT a-WAY', `phonics_focus`='igh → /aɪ/; ay → /eɪ/', `syllable_tip`='拆分练习：right a / way。注意：igh → /aɪ/; ay → /eɪ/。', `image_url`='/static/uploads/kids_cards/right-away.png', `tip`=NULL WHERE `priority_order`=37;
UPDATE `kids_english_card` SET `phonics`='/ˈkʌvər/', `part_of_speech`='verb', `level`='Core', `syllables`='cov · er', `stress`='COV-er', `phonics_focus`='o → /ʌ/; er → /ər/', `syllable_tip`='拆分练习：cov / er。注意：o → /ʌ/; er → /ər/。', `image_url`='/static/uploads/kids_cards/cover.png', `tip`=NULL WHERE `priority_order`=38;
UPDATE `kids_english_card` SET `phonics`='/lɪft/', `part_of_speech`='noun', `level`='Core', `syllables`='lift', `stress`='LIFT', `phonics_focus`='short i → /ɪ/', `syllable_tip`='拆分练习：lift。注意：short i → /ɪ/。', `image_url`='/static/uploads/kids_cards/lift.png', `tip`=NULL WHERE `priority_order`=39;
UPDATE `kids_english_card` SET `phonics`='/ˈfaɪərˌfaɪtər/', `part_of_speech`='noun', `level`='Core', `syllables`='fire · fight · er', `stress`='FIRE-fight-er', `phonics_focus`='ire → /aɪər/; igh → /aɪ/; er → /ər/', `syllable_tip`='拆分练习：fire / fight / er。注意：ire → /aɪər/; igh → /aɪ/; er → /ər/。', `image_url`='/static/uploads/kids_cards/firefighter.png', `tip`=NULL WHERE `priority_order`=40;
UPDATE `kids_english_card` SET `phonics`='/pʊt aʊt/', `part_of_speech`='phrase', `level`='Core', `syllables`='put out', `stress`='PUT OUT', `phonics_focus`='u → /ʊ/ in put; ou → /aʊ/', `syllable_tip`='拆分练习：put out。注意：u → /ʊ/ in put; ou → /aʊ/。', `image_url`='/static/uploads/kids_cards/put-out.png', `tip`=NULL WHERE `priority_order`=41;
UPDATE `kids_english_card` SET `phonics`='/bloʊ/', `part_of_speech`='verb', `level`='Core', `syllables`='blow', `stress`='BLOW', `phonics_focus`='bl → /bl/; ow → /oʊ/', `syllable_tip`='拆分练习：blow。注意：bl → /bl/; ow → /oʊ/。', `image_url`='/static/uploads/kids_cards/blow.png', `tip`=NULL WHERE `priority_order`=42;
UPDATE `kids_english_card` SET `phonics`='/ɔːr/', `part_of_speech`='conjunction', `level`='Core', `syllables`='or', `stress`='OR', `phonics_focus`='or → /ɔːr/', `syllable_tip`='拆分练习：or。注意：or → /ɔːr/。', `image_url`='/static/uploads/kids_cards/or.png', `tip`=NULL WHERE `priority_order`=43;
UPDATE `kids_english_card` SET `phonics`='/kʌp/', `part_of_speech`='noun', `level`='Core', `syllables`='cup', `stress`='CUP', `phonics_focus`='short u → /ʌ/', `syllable_tip`='拆分练习：cup。注意：short u → /ʌ/。', `image_url`='/static/uploads/kids_cards/cup.png', `tip`=NULL WHERE `priority_order`=44;
UPDATE `kids_english_card` SET `phonics`='/ˈstreɪndʒər/', `part_of_speech`='noun', `level`='Core', `syllables`='stran · ger', `stress`='STRAN-ger', `phonics_focus`='a → /eɪ/; str → /str/; ge → /dʒ/', `syllable_tip`='拆分练习：stran / ger。注意：a → /eɪ/; str → /str/; ge → /dʒ/。', `image_url`='/static/uploads/kids_cards/stranger.png', `tip`=NULL WHERE `priority_order`=45;
UPDATE `kids_english_card` SET `phonics`='/ˈbɒdi/', `part_of_speech`='noun', `level`='Core', `syllables`='bod · y', `stress`='BOD-y', `phonics_focus`='o → /ɒ/; y → /i/', `syllable_tip`='拆分练习：bod / y。注意：o → /ɒ/; y → /i/。', `image_url`='/static/uploads/kids_cards/body.png', `tip`=NULL WHERE `priority_order`=46;
UPDATE `kids_english_card` SET `phonics`='/ˈsʌmwʌn/', `part_of_speech`='pronoun', `level`='Core', `syllables`='some · one', `stress`='SOME-one', `phonics_focus`='o → /ʌ/ in some and one', `syllable_tip`='拆分练习：some / one。注意：o → /ʌ/ in some and one。', `image_url`='/static/uploads/kids_cards/someone.png', `tip`=NULL WHERE `priority_order`=47;
UPDATE `kids_english_card` SET `phonics`='/ˈriːzən/', `part_of_speech`='noun', `level`='Core', `syllables`='rea · son', `stress`='REA-son', `phonics_focus`='ea → /iː/; s → /z/', `syllable_tip`='拆分练习：rea / son。注意：ea → /iː/; s → /z/。', `image_url`='/static/uploads/kids_cards/reason.png', `tip`=NULL WHERE `priority_order`=48;
UPDATE `kids_english_card` SET `phonics`='/ʌnˈkʌmftəbəl/', `part_of_speech`='adjective', `level`='Core', `syllables`='un · com · fort · a · ble', `stress`='un-com-FORT-a-ble', `phonics_focus`='un- → /ʌn/; -able → /əbəl/', `syllable_tip`='拆分练习：un / com / fort / a / ble。注意：un- → /ʌn/; -able → /əbəl/。', `image_url`='/static/uploads/kids_cards/uncomfortable.png', `tip`=NULL WHERE `priority_order`=49;
UPDATE `kids_english_card` SET `phonics`='/tekˈnɒlədʒi/', `part_of_speech`='noun', `level`='Core', `syllables`='tech · nol · o · gy', `stress`='tech-NOL-o-gy', `phonics_focus`='ch → /k/; gy → /dʒi/', `syllable_tip`='拆分练习：tech / nol / o / gy。注意：ch → /k/; gy → /dʒi/。', `image_url`='/static/uploads/kids_cards/technology.png', `tip`=NULL WHERE `priority_order`=50;
UPDATE `kids_english_card` SET `phonics`='/ˈhæbɪt/', `part_of_speech`='noun', `level`='Core', `syllables`='hab · it', `stress`='HAB-it', `phonics_focus`='short a → /æ/; short i → /ɪ/', `syllable_tip`='拆分练习：hab / it。注意：short a → /æ/; short i → /ɪ/。', `image_url`='/static/uploads/kids_cards/habit.png', `tip`=NULL WHERE `priority_order`=51;
UPDATE `kids_english_card` SET `phonics`='/ðə pɑːst/', `part_of_speech`='phrase', `level`='Core', `syllables`='the past', `stress`='the PAST', `phonics_focus`='th → /ð/; a → /ɑː/', `syllable_tip`='拆分练习：the past。注意：th → /ð/; a → /ɑː/。', `image_url`='/static/uploads/kids_cards/the-past.png', `tip`=NULL WHERE `priority_order`=52;
UPDATE `kids_english_card` SET `phonics`='/kiːp ɪn tʌtʃ/', `part_of_speech`='phrase', `level`='Core', `syllables`='keep in touch', `stress`='KEEP in TOUCH', `phonics_focus`='ee → /iː/; ou → /ʌ/; tch → /tʃ/', `syllable_tip`='拆分练习：keep in touch。注意：ee → /iː/; ou → /ʌ/; tch → /tʃ/。', `image_url`='/static/uploads/kids_cards/keep-in-touch.png', `tip`=NULL WHERE `priority_order`=53;
UPDATE `kids_english_card` SET `phonics`='/tʃeɪndʒ/', `part_of_speech`='verb', `level`='Core', `syllables`='change', `stress`='CHANGE', `phonics_focus`='a_e → /eɪ/; ch → /tʃ/; ge → /dʒ/', `syllable_tip`='拆分练习：change。注意：a_e → /eɪ/; ch → /tʃ/; ge → /dʒ/。', `image_url`='/static/uploads/kids_cards/change.png', `tip`=NULL WHERE `priority_order`=54;
UPDATE `kids_english_card` SET `phonics`='/kəˌmjuːnɪˈkeɪʃən/', `part_of_speech`='noun', `level`='Core', `syllables`='com · mu · ni · ca · tion', `stress`='com-mu-ni-ca-TION', `phonics_focus`='tion → /ʃən/; u → /juː/', `syllable_tip`='拆分练习：com / mu / ni / ca / tion。注意：tion → /ʃən/; u → /juː/。', `image_url`='/static/uploads/kids_cards/communication.png', `tip`=NULL WHERE `priority_order`=55;
UPDATE `kids_english_card` SET `phonics`='/ˈenitaɪm/', `part_of_speech`='adverb', `level`='Core', `syllables`='an · y · time', `stress`='AN-y-time', `phonics_focus`='any → /eni/; i_e → /aɪ/', `syllable_tip`='拆分练习：an / y / time。注意：any → /eni/; i_e → /aɪ/。', `image_url`='/static/uploads/kids_cards/anytime-wide.png', `tip`=NULL WHERE `priority_order`=56;
UPDATE `kids_english_card` SET `phonics`='/ˈeniwer/', `part_of_speech`='adverb', `level`='Core', `syllables`='an · y · where', `stress`='AN-y-where', `phonics_focus`='wh → /w/; ere → /er/', `syllable_tip`='拆分练习：an / y / where。注意：wh → /w/; ere → /er/。', `image_url`='/static/uploads/kids_cards/anywhere-wide.png', `tip`=NULL WHERE `priority_order`=57;
UPDATE `kids_english_card` SET `phonics`='/kəˈnɛkt/', `part_of_speech`='verb', `level`='Core', `syllables`='con · nect', `stress`='con-NECT', `phonics_focus`='c → /k/; e → /ɛ/', `syllable_tip`='拆分练习：con / nect。注意：c → /k/; e → /ɛ/。', `image_url`='/static/uploads/kids_cards/connect-9.png', `tip`=NULL WHERE `priority_order`=58;
UPDATE `kids_english_card` SET `phonics`='/smɑːrt ˌedʒuˈkeɪʃən əv ˈtʃaɪnə/', `part_of_speech`='proper noun', `level`='Core', `syllables`='Smart Ed · u · ca · tion of Chi · na', `stress`='SMART ed-u-CA-tion of CHI-na', `phonics_focus`='tion → /ʃən/; ch → /tʃ/', `syllable_tip`='拆分练习：Smart Ed / u / ca / tion of Chi / na。注意：tion → /ʃən/; ch → /tʃ/。', `image_url`='/static/uploads/kids_cards/smart-education-of-china.png', `tip`=NULL WHERE `priority_order`=59;
UPDATE `kids_english_card` SET `phonics`='/ˈplætfɔːrm/', `part_of_speech`='noun', `level`='Core', `syllables`='plat · form', `stress`='PLAT-form', `phonics_focus`='pl → /pl/; or → /ɔːr/', `syllable_tip`='拆分练习：plat / form。注意：pl → /pl/; or → /ɔːr/。', `image_url`='/static/uploads/kids_cards/platform.png', `tip`=NULL WHERE `priority_order`=60;
UPDATE `kids_english_card` SET `phonics`='/ˌviː ˈɑːr ˈvɜːrtʃuəl riˈæləti/', `part_of_speech`='noun', `level`='Core', `syllables`='V · R Vir · tu · al Re · al · i · ty', `stress`='V-R VIR-tu-al re-AL-i-ty', `phonics_focus`='V、R 读字母名；-ity → /əti/', `syllable_tip`='拆分练习：V / R Vir / tu / al Re / al / i / ty。注意：V、R 读字母名；-ity → /əti/。', `image_url`='/static/uploads/kids_cards/vr-virtual-reality.png', `tip`=NULL WHERE `priority_order`=61;
UPDATE `kids_english_card` SET `phonics`='/fər ɪɡˈzæmpəl/', `part_of_speech`='phrase', `level`='Core', `syllables`='for ex · am · ple', `stress`='for ex-AM-ple', `phonics_focus`='ex → /ɪɡz/; pl → /pl/', `syllable_tip`='拆分练习：for ex / am / ple。注意：ex → /ɪɡz/; pl → /pl/。', `image_url`='/static/uploads/kids_cards/for-example.png', `tip`=NULL WHERE `priority_order`=62;
UPDATE `kids_english_card` SET `phonics`='/ˈfɪnlənd/', `part_of_speech`='proper noun', `level`='Core', `syllables`='Fin · land', `stress`='FIN-land', `phonics_focus`='short i → /ɪ/', `syllable_tip`='拆分练习：Fin / land。注意：short i → /ɪ/。', `image_url`='/static/uploads/kids_cards/finland.png', `tip`=NULL WHERE `priority_order`=63;
UPDATE `kids_english_card` SET `phonics`='/ˈreɪlweɪ/', `part_of_speech`='noun', `level`='Core', `syllables`='rail · way', `stress`='RAIL-way', `phonics_focus`='ai → /eɪ/; ay → /eɪ/', `syllable_tip`='拆分练习：rail / way。注意：ai → /eɪ/; ay → /eɪ/。', `image_url`='/static/uploads/kids_cards/railway.png', `tip`=NULL WHERE `priority_order`=64;
UPDATE `kids_english_card` SET `phonics`='/kəˈnɛkt/', `part_of_speech`='verb', `level`='Core', `syllables`='con · nect', `stress`='con-NECT', `phonics_focus`='c → /k/; e → /ɛ/', `syllable_tip`='拆分练习：con / nect。注意：c → /k/; e → /ɛ/。', `image_url`='/static/uploads/kids_cards/connect-11.png', `tip`=NULL WHERE `priority_order`=65;
UPDATE `kids_english_card` SET `phonics`='/ɡoʊ ˈɪntuː ˈsɜːrvɪs/', `part_of_speech`='phrase', `level`='Core', `syllables`='go in · to ser · vice', `stress`='GO IN-to SER-vice', `phonics_focus`='o → /oʊ/; oo → /uː/; c → /s/', `syllable_tip`='拆分练习：go in / to ser / vice。注意：o → /oʊ/; oo → /uː/; c → /s/。', `image_url`='/static/uploads/kids_cards/go-into-service.png', `tip`=NULL WHERE `priority_order`=66;
UPDATE `kids_english_card` SET `phonics`='/θɪŋk/', `part_of_speech`='verb', `level`='Core', `syllables`='think', `stress`='THINK', `phonics_focus`='th → /θ/; short i → /ɪ/', `syllable_tip`='拆分练习：think。注意：th → /θ/; short i → /ɪ/。', `image_url`='/static/uploads/kids_cards/think.png', `tip`=NULL WHERE `priority_order`=67;
UPDATE `kids_english_card` SET `phonics`='/bɪld/', `part_of_speech`='verb', `level`='Core', `syllables`='build', `stress`='BUILD', `phonics_focus`='ui → /ɪ/', `syllable_tip`='拆分练习：build。注意：ui → /ɪ/。', `image_url`='/static/uploads/kids_cards/build.png', `tip`=NULL WHERE `priority_order`=68;
UPDATE `kids_english_card` SET `phonics`='/ˈbeɪduː ˌnævɪˈɡeɪʃən ˈbiː diː ɛs/', `part_of_speech`='proper noun', `level`='Core', `syllables`='Bei · dou Nav · i · ga · tion B · D · S', `stress`='BEI-dou nav-i-GA-tion B-D-S', `phonics_focus`='ou → /uː/; tion → /ʃən/; BDS 读字母名', `syllable_tip`='拆分练习：Bei / dou Nav / i / ga / tion B / D / S。注意：ou → /uː/; tion → /ʃən/; BDS 读字母名。', `image_url`='/static/uploads/kids_cards/beidou-navigation-bds-wide.png', `tip`=NULL WHERE `priority_order`=69;
UPDATE `kids_english_card` SET `phonics`='/ɜːrθ/', `part_of_speech`='noun', `level`='Core', `syllables`='Earth', `stress`='EARTH', `phonics_focus`='ear → /ɜːr/; th → /θ/', `syllable_tip`='拆分练习：Earth。注意：ear → /ɜːr/; th → /θ/。', `image_url`='/static/uploads/kids_cards/earth.png', `tip`=NULL WHERE `priority_order`=70;

# Store the wide illustrations in the database. This is idempotent so it can
# also be run against an existing database after the cards were imported.
UPDATE `kids_english_card`
SET `image_url` = CASE `priority_order`
    WHEN 1 THEN '/static/uploads/kids_cards/northeast-wide.png'
    WHEN 2 THEN '/static/uploads/kids_cards/beach-wide.png'
    WHEN 3 THEN '/static/uploads/kids_cards/wonderful-wide.png'
    WHEN 4 THEN '/static/uploads/kids_cards/safety-wide.png'
    WHEN 5 THEN '/static/uploads/kids_cards/rule-wide.png'
    WHEN 6 THEN '/static/uploads/kids_cards/meaningful-wide.png'
    WHEN 7 THEN '/static/uploads/kids_cards/national-library-of-china-wide.png'
    WHEN 8 THEN '/static/uploads/kids_cards/on-foot-wide.png'
    WHEN 9 THEN '/static/uploads/kids_cards/china-science-and-technology-museum-wide.png'
    WHEN 10 THEN '/static/uploads/kids_cards/far-from-wide.png'
    WHEN 11 THEN '/static/uploads/kids_cards/baby-wide.png'
    WHEN 12 THEN '/static/uploads/kids_cards/chick-wide.png'
    WHEN 13 THEN '/static/uploads/kids_cards/sometimes-wide.png'
    WHEN 14 THEN '/static/uploads/kids_cards/go-fishing-wide.png'
    WHEN 15 THEN '/static/uploads/kids_cards/daytime-wide.png'
    WHEN 16 THEN '/static/uploads/kids_cards/university-wide.png'
    WHEN 17 THEN '/static/uploads/kids_cards/toronto-wide.png'
    WHEN 18 THEN '/static/uploads/kids_cards/ottawa-wide.png'
    WHEN 19 THEN '/static/uploads/kids_cards/hospital-wide.png'
    WHEN 20 THEN '/static/uploads/kids_cards/move-wide.png'
    WHEN 21 THEN '/static/uploads/kids_cards/head-wide.png'
    WHEN 22 THEN '/static/uploads/kids_cards/helmet-wide.png'
    WHEN 23 THEN '/static/uploads/kids_cards/follow-wide.png'
    WHEN 24 THEN '/static/uploads/kids_cards/stomachache-wide.png'
    WHEN 25 THEN '/static/uploads/kids_cards/touch-wide.png'
    WHEN 26 THEN '/static/uploads/kids_cards/bowl-wide.png'
    WHEN 27 THEN '/static/uploads/kids_cards/advice-wide.png'
    WHEN 28 THEN '/static/uploads/kids_cards/too-much-wide.png'
    WHEN 29 THEN '/static/uploads/kids_cards/right-after-wide.png'
    WHEN 30 THEN '/static/uploads/kids_cards/those-wide.png'
    WHEN 31 THEN '/static/uploads/kids_cards/fire-wide.png'
    WHEN 32 THEN '/static/uploads/kids_cards/turn-into-wide.png'
    WHEN 33 THEN '/static/uploads/kids_cards/candle-wide.png'
    WHEN 34 THEN '/static/uploads/kids_cards/danger-wide.png'
    WHEN 35 THEN '/static/uploads/kids_cards/talk-wide.png'
    WHEN 36 THEN '/static/uploads/kids_cards/exit-wide.png'
    WHEN 37 THEN '/static/uploads/kids_cards/right-away-wide.png'
    WHEN 38 THEN '/static/uploads/kids_cards/cover-wide.png'
    WHEN 39 THEN '/static/uploads/kids_cards/lift-wide.png'
    WHEN 40 THEN '/static/uploads/kids_cards/firefighter-wide.png'
    WHEN 41 THEN '/static/uploads/kids_cards/put-out-wide.png'
    WHEN 42 THEN '/static/uploads/kids_cards/blow-wide.png'
    WHEN 43 THEN '/static/uploads/kids_cards/or-wide.png'
    WHEN 44 THEN '/static/uploads/kids_cards/cup-wide.png'
    WHEN 45 THEN '/static/uploads/kids_cards/stranger-wide.png'
    WHEN 46 THEN '/static/uploads/kids_cards/body-wide.png'
    WHEN 47 THEN '/static/uploads/kids_cards/someone-wide.png'
    WHEN 48 THEN '/static/uploads/kids_cards/reason-wide.png'
    WHEN 49 THEN '/static/uploads/kids_cards/uncomfortable-wide.png'
    WHEN 50 THEN '/static/uploads/kids_cards/technology-wide.png'
    WHEN 51 THEN '/static/uploads/kids_cards/habit-wide.png'
    WHEN 52 THEN '/static/uploads/kids_cards/the-past-wide.png'
    WHEN 53 THEN '/static/uploads/kids_cards/keep-in-touch-wide.png'
    WHEN 54 THEN '/static/uploads/kids_cards/change-wide.png'
    WHEN 55 THEN '/static/uploads/kids_cards/communication-wide.png'
    WHEN 56 THEN '/static/uploads/kids_cards/anytime-wide.png'
    WHEN 57 THEN '/static/uploads/kids_cards/anywhere-wide.png'
    WHEN 58 THEN '/static/uploads/kids_cards/connect-9-wide.png'
    WHEN 59 THEN '/static/uploads/kids_cards/smart-education-of-china-wide.png'
    WHEN 60 THEN '/static/uploads/kids_cards/platform-wide.png'
    WHEN 61 THEN '/static/uploads/kids_cards/vr-virtual-reality-wide.png'
    WHEN 62 THEN '/static/uploads/kids_cards/for-example-wide.png'
    WHEN 63 THEN '/static/uploads/kids_cards/finland-wide.png'
    WHEN 64 THEN '/static/uploads/kids_cards/railway-wide.png'
    WHEN 65 THEN '/static/uploads/kids_cards/connect-11-wide.png'
    WHEN 66 THEN '/static/uploads/kids_cards/go-into-service-wide.png'
    WHEN 67 THEN '/static/uploads/kids_cards/think-wide.png'
    WHEN 68 THEN '/static/uploads/kids_cards/build-wide.png'
    WHEN 69 THEN '/static/uploads/kids_cards/beidou-navigation-bds-wide.png'
    WHEN 70 THEN '/static/uploads/kids_cards/earth-wide.png'
END
WHERE `priority_order` BETWEEN 1 AND 70;

DELETE FROM `kids_english_card_sound_part`;
DELETE FROM `kids_english_card_example`;
DELETE FROM `kids_english_card_word_family`;

INSERT INTO `kids_english_card_sound_part` (`card_id`, `part_order`, `chunk`, `pronunciation`) VALUES
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=1), 1, 'north', '/nɔːrθ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=1), 2, 'east', '/iːst/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=2), 1, 'beach', '/biːtʃ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=3), 1, 'won', '/wʌn/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=3), 2, 'der', '/dər/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=3), 3, 'ful', '/fəl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=4), 1, 'safe', '/seɪf/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=4), 2, 'ty', '/ti/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=5), 1, 'rule', '/ruːl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=6), 1, 'mean', '/miːn/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=6), 2, 'ing', '/ɪŋ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=6), 3, 'ful', '/fəl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=7), 1, 'Na', '/næ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=7), 2, 'tion', '/ʃən/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=7), 3, 'Li', '/laɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=7), 4, 'bra', '/brə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=7), 5, 'ry', '/ri/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=7), 6, 'Chi', '/tʃaɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=7), 7, 'na', '/nə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=8), 1, 'on', '/ɒn/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=8), 2, 'foot', '/fʊt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=9), 1, 'Chi', '/tʃaɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=9), 2, 'na', '/nə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=9), 3, 'Sci', '/saɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=9), 4, 'ence', '/əns/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=9), 5, 'Tech', '/tek/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=9), 6, 'nol', '/nɒl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=9), 7, 'o', '/ə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=9), 8, 'gy', '/dʒi/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=9), 9, 'Mu', '/mjuː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=9), 10, 'se', '/ziː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=9), 11, 'um', '/əm/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=10), 1, 'far', '/fɑːr/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=10), 2, 'from', '/frəm/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=11), 1, 'ba', '/beɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=11), 2, 'by', '/bi/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=12), 1, 'ch', '/tʃ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=12), 2, 'ick', '/ɪk/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=13), 1, 'some', '/sʌm/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=13), 2, 'times', '/taɪmz/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=14), 1, 'go', '/ɡoʊ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=14), 2, 'fish', '/fɪʃ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=14), 3, 'ing', '/ɪŋ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=15), 1, 'day', '/deɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=15), 2, 'time', '/taɪm/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=16), 1, 'u', '/juː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=16), 2, 'ni', '/nɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=16), 3, 'ver', '/vɜːr/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=16), 4, 'si', '/sə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=16), 5, 'ty', '/ti/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=17), 1, 'To', '/tə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=17), 2, 'ron', '/rɒn/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=17), 3, 'to', '/toʊ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=18), 1, 'Ot', '/ɒt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=18), 2, 'ta', '/tə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=18), 3, 'wa', '/wə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=19), 1, 'hos', '/hɒs/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=19), 2, 'pi', '/pɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=19), 3, 'tal', '/təl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=20), 1, 'move', '/muːv/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=21), 1, 'head', '/hɛd/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=22), 1, 'hel', '/hɛl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=22), 2, 'met', '/mɪt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=23), 1, 'fol', '/fɒl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=23), 2, 'low', '/loʊ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=24), 1, 'stom', '/stʌm/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=24), 2, 'ach', '/ək/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=24), 3, 'ache', '/eɪk/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=25), 1, 'touch', '/tʌtʃ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=26), 1, 'bowl', '/boʊl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=27), 1, 'ad', '/əd/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=27), 2, 'vice', '/vaɪs/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=28), 1, 'too', '/tuː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=28), 2, 'much', '/mʌtʃ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=29), 1, 'right', '/raɪt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=29), 2, 'af', '/æf/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=29), 3, 'ter', '/tər/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=30), 1, 'those', '/ðoʊz/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=31), 1, 'fire', '/faɪər/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=32), 1, 'turn', '/tɜːrn/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=32), 2, 'in', '/ɪn/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=32), 3, 'to', '/tuː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=33), 1, 'can', '/kæn/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=33), 2, 'dle', '/dəl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=34), 1, 'dan', '/deɪn/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=34), 2, 'ger', '/dʒər/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=35), 1, 'talk', '/tɔːk/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=36), 1, 'ex', '/ɛɡz/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=36), 2, 'it', '/ɪt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=37), 1, 'right', '/raɪt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=37), 2, 'a', '/ə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=37), 3, 'way', '/weɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=38), 1, 'cov', '/kʌv/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=38), 2, 'er', '/ər/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=39), 1, 'lift', '/lɪft/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=40), 1, 'fire', '/faɪər/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=40), 2, 'fight', '/faɪt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=40), 3, 'er', '/ər/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=41), 1, 'put', '/pʊt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=41), 2, 'out', '/aʊt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=42), 1, 'blow', '/bloʊ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=43), 1, 'or', '/ɔːr/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=44), 1, 'cup', '/kʌp/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=45), 1, 'stran', '/streɪn/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=45), 2, 'ger', '/dʒər/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=46), 1, 'bod', '/bɒd/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=46), 2, 'y', '/i/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=47), 1, 'some', '/sʌm/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=47), 2, 'one', '/wʌn/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=48), 1, 'rea', '/riː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=48), 2, 'son', '/zən/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=49), 1, 'un', '/ʌn/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=49), 2, 'com', '/kʌm/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=49), 3, 'fort', '/fɔːrt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=49), 4, 'a', '/ə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=49), 5, 'ble', '/bəl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=50), 1, 'tech', '/tek/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=50), 2, 'nol', '/nɒl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=50), 3, 'o', '/ə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=50), 4, 'gy', '/dʒi/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=51), 1, 'hab', '/hæb/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=51), 2, 'it', '/ɪt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=52), 1, 'the', '/ðə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=52), 2, 'past', '/pɑːst/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=53), 1, 'keep', '/kiːp/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=53), 2, 'in', '/ɪn/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=53), 3, 'touch', '/tʌtʃ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=54), 1, 'change', '/tʃeɪndʒ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=55), 1, 'com', '/kə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=55), 2, 'mu', '/mjuː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=55), 3, 'ni', '/nɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=55), 4, 'ca', '/keɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=55), 5, 'tion', '/ʃən/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=56), 1, 'an', '/en/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=56), 2, 'y', '/i/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=56), 3, 'time', '/taɪm/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=57), 1, 'an', '/en/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=57), 2, 'y', '/i/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=57), 3, 'where', '/wer/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=58), 1, 'con', '/kə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=58), 2, 'nect', '/nɛkt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=59), 1, 'Smart', '/smɑːrt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=59), 2, 'Ed', '/ed/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=59), 3, 'u', '/juː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=59), 4, 'ca', '/keɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=59), 5, 'tion', '/ʃən/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=59), 6, 'Chi', '/tʃaɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=59), 7, 'na', '/nə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=60), 1, 'plat', '/plæt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=60), 2, 'form', '/fɔːrm/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=61), 1, 'V', '/viː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=61), 2, 'R', '/ɑːr/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=61), 3, 'Vir', '/vɜːr/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=61), 4, 'tu', '/tʃuː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=61), 5, 'al', '/əl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=61), 6, 'Re', '/riː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=61), 7, 'al', '/æl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=61), 8, 'i', '/ə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=61), 9, 'ty', '/ti/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=62), 1, 'for', '/fər/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=62), 2, 'ex', '/ɪɡz/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=62), 3, 'am', '/æm/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=62), 4, 'ple', '/pəl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=63), 1, 'Fin', '/fɪn/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=63), 2, 'land', '/lənd/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=64), 1, 'rail', '/reɪl/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=64), 2, 'way', '/weɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=65), 1, 'con', '/kə/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=65), 2, 'nect', '/nɛkt/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=66), 1, 'go', '/ɡoʊ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=66), 2, 'in', '/ɪn/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=66), 3, 'to', '/tuː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=66), 4, 'ser', '/sɜːr/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=66), 5, 'vice', '/vɪs/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=67), 1, 'think', '/θɪŋk/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=68), 1, 'build', '/bɪld/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 1, 'Bei', '/beɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 2, 'dou', '/duː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 3, 'Nav', '/næv/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 4, 'i', '/ɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 5, 'ga', '/ɡeɪ/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 6, 'tion', '/ʃən/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 7, 'B', '/biː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 8, 'D', '/diː/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 9, 'S', '/ɛs/'),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=70), 1, 'Earth', '/ɜːrθ/');

INSERT INTO `kids_english_card_example` (`card_id`, `example_text`, `translation`, `priority_order`) VALUES
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=1), 'Harbin is in the northeast of China.', '哈尔滨在中国的东北部。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=1), 'Walk northeast for two blocks, and you will see the library.', '向东北走两个街区，你会看到图书馆。', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=2), 'The word “beach” is useful in everyday English.', '单词“beach”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=2), 'Can you say “beach” clearly?', '你能清楚地说出“beach”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=3), 'The word “wonderful” is useful in everyday English.', '单词“wonderful”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=3), 'Can you say “wonderful” clearly?', '你能清楚地说出“wonderful”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=4), 'The word “safety” is useful in everyday English.', '单词“safety”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=4), 'Can you say “safety” clearly?', '你能清楚地说出“safety”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=5), 'The word “rule” is useful in everyday English.', '单词“rule”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=5), 'Can you say “rule” clearly?', '你能清楚地说出“rule”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=6), 'The word “meaningful” is useful in everyday English.', '单词“meaningful”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=6), 'Can you say “meaningful” clearly?', '你能清楚地说出“meaningful”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=7), 'We learned about National Library of China in class.', '我们在课堂上了解了“National Library of China”。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=7), 'Can you say “National Library of China” clearly?', '你能清楚地说出“National Library of China”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=8), 'I can use “on foot” in a sentence.', '我会用“on foot”造句。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=8), 'Can you say “on foot” clearly?', '你能清楚地说出“on foot”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=9), 'We learned about China Science and Technology Museum in class.', '我们在课堂上了解了“China Science and Technology Museum”。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=9), 'Can you say “China Science and Technology Museum” clearly?', '你能清楚地说出“China Science and Technology Museum”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=10), 'I can use “far from” in a sentence.', '我会用“far from”造句。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=10), 'Can you say “far from” clearly?', '你能清楚地说出“far from”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=11), 'The word “baby” is useful in everyday English.', '单词“baby”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=11), 'Can you say “baby” clearly?', '你能清楚地说出“baby”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=12), 'The word “chick” is useful in everyday English.', '单词“chick”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=12), 'Can you say “chick” clearly?', '你能清楚地说出“chick”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=13), 'The word “sometimes” is useful in everyday English.', '单词“sometimes”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=13), 'Can you say “sometimes” clearly?', '你能清楚地说出“sometimes”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=14), 'I can use “go fishing” in a sentence.', '我会用“go fishing”造句。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=14), 'Can you say “go fishing” clearly?', '你能清楚地说出“go fishing”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=15), 'The word “daytime” is useful in everyday English.', '单词“daytime”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=15), 'Can you say “daytime” clearly?', '你能清楚地说出“daytime”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=16), 'The word “university” is useful in everyday English.', '单词“university”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=16), 'Can you say “university” clearly?', '你能清楚地说出“university”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=17), 'The word “Toronto” is useful in everyday English.', '单词“Toronto”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=17), 'Can you say “Toronto” clearly?', '你能清楚地说出“Toronto”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=18), 'The word “Ottawa” is useful in everyday English.', '单词“Ottawa”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=18), 'Can you say “Ottawa” clearly?', '你能清楚地说出“Ottawa”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=19), 'The word “hospital” is useful in everyday English.', '单词“hospital”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=19), 'Can you say “hospital” clearly?', '你能清楚地说出“hospital”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=20), 'The word “move” is useful in everyday English.', '单词“move”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=20), 'Can you say “move” clearly?', '你能清楚地说出“move”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=21), 'The word “head” is useful in everyday English.', '单词“head”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=21), 'Can you say “head” clearly?', '你能清楚地说出“head”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=22), 'The word “helmet” is useful in everyday English.', '单词“helmet”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=22), 'Can you say “helmet” clearly?', '你能清楚地说出“helmet”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=23), 'The word “follow” is useful in everyday English.', '单词“follow”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=23), 'Can you say “follow” clearly?', '你能清楚地说出“follow”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=24), 'The word “stomachache” is useful in everyday English.', '单词“stomachache”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=24), 'Can you say “stomachache” clearly?', '你能清楚地说出“stomachache”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=25), 'The word “touch” is useful in everyday English.', '单词“touch”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=25), 'Can you say “touch” clearly?', '你能清楚地说出“touch”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=26), 'The word “bowl” is useful in everyday English.', '单词“bowl”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=26), 'Can you say “bowl” clearly?', '你能清楚地说出“bowl”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=27), 'The word “advice” is useful in everyday English.', '单词“advice”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=27), 'Can you say “advice” clearly?', '你能清楚地说出“advice”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=28), 'I can use “too much” in a sentence.', '我会用“too much”造句。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=28), 'Can you say “too much” clearly?', '你能清楚地说出“too much”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=29), 'I can use “right after” in a sentence.', '我会用“right after”造句。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=29), 'Can you say “right after” clearly?', '你能清楚地说出“right after”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=30), 'The word “those” is useful in everyday English.', '单词“those”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=30), 'Can you say “those” clearly?', '你能清楚地说出“those”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=31), 'The word “fire” is useful in everyday English.', '单词“fire”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=31), 'Can you say “fire” clearly?', '你能清楚地说出“fire”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=32), 'I can use “turn into” in a sentence.', '我会用“turn into”造句。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=32), 'Can you say “turn into” clearly?', '你能清楚地说出“turn into”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=33), 'The word “candle” is useful in everyday English.', '单词“candle”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=33), 'Can you say “candle” clearly?', '你能清楚地说出“candle”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=34), 'The word “danger” is useful in everyday English.', '单词“danger”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=34), 'Can you say “danger” clearly?', '你能清楚地说出“danger”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=35), 'The word “talk” is useful in everyday English.', '单词“talk”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=35), 'Can you say “talk” clearly?', '你能清楚地说出“talk”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=36), 'The word “exit” is useful in everyday English.', '单词“exit”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=36), 'Can you say “exit” clearly?', '你能清楚地说出“exit”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=37), 'I can use “right away” in a sentence.', '我会用“right away”造句。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=37), 'Can you say “right away” clearly?', '你能清楚地说出“right away”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=38), 'The word “cover” is useful in everyday English.', '单词“cover”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=38), 'Can you say “cover” clearly?', '你能清楚地说出“cover”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=39), 'The word “lift” is useful in everyday English.', '单词“lift”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=39), 'Can you say “lift” clearly?', '你能清楚地说出“lift”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=40), 'The word “firefighter” is useful in everyday English.', '单词“firefighter”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=40), 'Can you say “firefighter” clearly?', '你能清楚地说出“firefighter”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=41), 'I can use “put out” in a sentence.', '我会用“put out”造句。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=41), 'Can you say “put out” clearly?', '你能清楚地说出“put out”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=42), 'The word “blow” is useful in everyday English.', '单词“blow”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=42), 'Can you say “blow” clearly?', '你能清楚地说出“blow”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=43), 'The word “or” is useful in everyday English.', '单词“or”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=43), 'Can you say “or” clearly?', '你能清楚地说出“or”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=44), 'The word “cup” is useful in everyday English.', '单词“cup”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=44), 'Can you say “cup” clearly?', '你能清楚地说出“cup”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=45), 'The word “stranger” is useful in everyday English.', '单词“stranger”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=45), 'Can you say “stranger” clearly?', '你能清楚地说出“stranger”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=46), 'The word “body” is useful in everyday English.', '单词“body”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=46), 'Can you say “body” clearly?', '你能清楚地说出“body”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=47), 'The word “someone” is useful in everyday English.', '单词“someone”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=47), 'Can you say “someone” clearly?', '你能清楚地说出“someone”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=48), 'The word “reason” is useful in everyday English.', '单词“reason”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=48), 'Can you say “reason” clearly?', '你能清楚地说出“reason”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=49), 'The word “uncomfortable” is useful in everyday English.', '单词“uncomfortable”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=49), 'Can you say “uncomfortable” clearly?', '你能清楚地说出“uncomfortable”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=50), 'The word “technology” is useful in everyday English.', '单词“technology”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=50), 'Can you say “technology” clearly?', '你能清楚地说出“technology”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=51), 'The word “habit” is useful in everyday English.', '单词“habit”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=51), 'Can you say “habit” clearly?', '你能清楚地说出“habit”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=52), 'I can use “the past” in a sentence.', '我会用“the past”造句。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=52), 'Can you say “the past” clearly?', '你能清楚地说出“the past”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=53), 'I can use “keep in touch” in a sentence.', '我会用“keep in touch”造句。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=53), 'Can you say “keep in touch” clearly?', '你能清楚地说出“keep in touch”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=54), 'The word “change” is useful in everyday English.', '单词“change”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=54), 'Can you say “change” clearly?', '你能清楚地说出“change”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=55), 'The word “communication” is useful in everyday English.', '单词“communication”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=55), 'Can you say “communication” clearly?', '你能清楚地说出“communication”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=56), 'The word “anytime” is useful in everyday English.', '单词“anytime”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=56), 'Can you say “anytime” clearly?', '你能清楚地说出“anytime”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=57), 'The word “anywhere” is useful in everyday English.', '单词“anywhere”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=57), 'Can you say “anywhere” clearly?', '你能清楚地说出“anywhere”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=58), 'The word “connect” is useful in everyday English.', '单词“connect”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=58), 'Can you say “connect” clearly?', '你能清楚地说出“connect”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=59), 'We learned about Smart Education of China in class.', '我们在课堂上了解了“Smart Education of China”。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=59), 'Can you say “Smart Education of China” clearly?', '你能清楚地说出“Smart Education of China”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=60), 'The word “platform” is useful in everyday English.', '单词“platform”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=60), 'Can you say “platform” clearly?', '你能清楚地说出“platform”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=61), 'We learned about VR (Virtual Reality) in class.', '我们在课堂上了解了“VR (Virtual Reality)”。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=61), 'Can you say “VR (Virtual Reality)” clearly?', '你能清楚地说出“VR (Virtual Reality)”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=62), 'I can use “for example” in a sentence.', '我会用“for example”造句。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=62), 'Can you say “for example” clearly?', '你能清楚地说出“for example”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=63), 'The word “Finland” is useful in everyday English.', '单词“Finland”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=63), 'Can you say “Finland” clearly?', '你能清楚地说出“Finland”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=64), 'The word “railway” is useful in everyday English.', '单词“railway”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=64), 'Can you say “railway” clearly?', '你能清楚地说出“railway”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=65), 'The word “connect” is useful in everyday English.', '单词“connect”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=65), 'Can you say “connect” clearly?', '你能清楚地说出“connect”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=66), 'I can use “go into service” in a sentence.', '我会用“go into service”造句。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=66), 'Can you say “go into service” clearly?', '你能清楚地说出“go into service”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=67), 'The word “think” is useful in everyday English.', '单词“think”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=67), 'Can you say “think” clearly?', '你能清楚地说出“think”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=68), 'The word “build” is useful in everyday English.', '单词“build”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=68), 'Can you say “build” clearly?', '你能清楚地说出“build”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 'We learned about Beidou Navigation (abbr. BDS) in class.', '我们在课堂上了解了“Beidou Navigation (abbr. BDS)”。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=69), 'Can you say “Beidou Navigation (abbr. BDS)” clearly?', '你能清楚地说出“Beidou Navigation (abbr. BDS)”吗？', 2),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=70), 'The word “Earth” is useful in everyday English.', '单词“Earth”在日常英语中很有用。', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=70), 'Can you say “Earth” clearly?', '你能清楚地说出“Earth”吗？', 2);

INSERT INTO `kids_english_card_word_family` (`card_id`, `related_word`, `part_of_speech`, `meaning`, `priority_order`) VALUES
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=1), 'northern', 'adjective', '北方的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=2), 'beachside', 'adjective', '海滨的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=3), 'wonder', 'noun', '奇迹；惊叹', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=4), 'safe', 'adjective', '安全的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=5), 'ruler', 'noun', '统治者；尺子', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=6), 'meaning', 'noun', '意义', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=11), 'babies', 'noun', '婴儿；幼崽复数', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=12), 'chicken', 'noun', '鸡', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=20), 'movement', 'noun', '移动', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=23), 'following', 'adjective', '接下来的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=27), 'advise', 'verb', '建议', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=31), 'fiery', 'adjective', '火一般的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=34), 'dangerous', 'adjective', '危险的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=35), 'talkative', 'adjective', '健谈的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=38), 'covered', 'adjective', '被覆盖的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=40), 'firefighting', 'noun', '消防工作', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=45), 'strange', 'adjective', '陌生的；奇怪的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=48), 'reasonable', 'adjective', '合理的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=49), 'comfort', 'noun', '舒适；安慰', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=50), 'technological', 'adjective', '科技的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=51), 'habitual', 'adjective', '习惯性的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=54), 'changeable', 'adjective', '可改变的', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=55), 'communicate', 'verb', '交流', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=58), 'connection', 'noun', '联系；连接', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=64), 'rail', 'noun', '铁轨', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=67), 'thinker', 'noun', '思考者', 1),
((SELECT `id` FROM `kids_english_card` WHERE `priority_order`=68), 'builder', 'noun', '建造者', 1);

UPDATE `kids_english_card`
SET `tip` = CONCAT('Chunk it: ', `syllables`, '. Focus on ', `phonics_focus`, '.')
WHERE `is_active` = 1 AND `priority_order` BETWEEN 1 AND 70;

# Replace the initial import placeholders with natural, contextual example sentences.
UPDATE `kids_english_card_example` AS e
JOIN `kids_english_card` AS c ON c.`id` = e.`card_id`
SET e.`example_text` = CASE CONCAT(c.`priority_order`, ':', e.`priority_order`)
    WHEN '1:1' THEN 'Harbin is in the northeast of China.'
    WHEN '1:2' THEN 'Walk northeast for two blocks, and you will see the library.'
    WHEN '2:1' THEN 'We built a sandcastle on the beach.'
    WHEN '2:2' THEN 'The beach is busy in summer.'
    WHEN '3:1' THEN 'We had a wonderful time at the science museum.'
    WHEN '3:2' THEN 'Your painting looks wonderful!'
    WHEN '4:1' THEN 'Wear a helmet for your safety.'
    WHEN '4:2' THEN 'Road safety is important for everyone.'
    WHEN '5:1' THEN 'Our class has a rule: be kind to everyone.'
    WHEN '5:2' THEN 'Please follow the rules in the library.'
    WHEN '6:1' THEN 'Helping others can be meaningful.'
    WHEN '6:2' THEN 'We had a meaningful talk about friendship.'
    WHEN '7:1' THEN 'The National Library of China has many old books.'
    WHEN '7:2' THEN 'We visited the National Library of China last weekend.'
    WHEN '8:1' THEN 'I walk to school on foot.'
    WHEN '8:2' THEN 'The park is only ten minutes away on foot.'
    WHEN '9:1' THEN 'We learned about space at the China Science and Technology Museum.'
    WHEN '9:2' THEN 'The China Science and Technology Museum is popular with children.'
    WHEN '10:1' THEN 'My home is far from school.'
    WHEN '10:2' THEN 'The bus stop is not far from here.'
    WHEN '11:1' THEN 'The baby is sleeping in the stroller.'
    WHEN '11:2' THEN 'The mother bird feeds her baby.'
    WHEN '12:1' THEN 'The little chick follows its mother.'
    WHEN '12:2' THEN 'A yellow chick is pecking at seeds.'
    WHEN '13:1' THEN 'I sometimes read before bed.'
    WHEN '13:2' THEN 'It sometimes rains in the afternoon.'
    WHEN '14:1' THEN 'My father and I go fishing on Sundays.'
    WHEN '14:2' THEN 'We went fishing by the lake.'
    WHEN '15:1' THEN 'Owls sleep during the daytime.'
    WHEN '15:2' THEN 'The stars are hard to see in the daytime.'
    WHEN '16:1' THEN 'My sister wants to study at a university.'
    WHEN '16:2' THEN 'The university has a large library.'
    WHEN '17:1' THEN 'Toronto is the largest city in Canada.'
    WHEN '17:2' THEN 'My cousin lives in Toronto.'
    WHEN '18:1' THEN 'Ottawa is the capital of Canada.'
    WHEN '18:2' THEN 'The Parliament buildings are in Ottawa.'
    WHEN '19:1' THEN 'The doctor works at the hospital.'
    WHEN '19:2' THEN 'We took Grandpa to the hospital.'
    WHEN '20:1' THEN 'Please move your chair closer to the table.'
    WHEN '20:2' THEN 'The bus started to move.'
    WHEN '21:1' THEN 'He shook his head when he heard the bad news.'
    WHEN '21:2' THEN 'Wear a hat to protect your head from the sun.'
    WHEN '22:1' THEN 'Always wear a helmet when you ride a bike.'
    WHEN '22:2' THEN 'His helmet is bright blue.'
    WHEN '23:1' THEN 'Follow the path to the playground.'
    WHEN '23:2' THEN 'Please follow your teacher.'
    WHEN '24:1' THEN 'I stayed home because I had a stomachache.'
    WHEN '24:2' THEN 'Too much candy can give you a stomachache.'
    WHEN '25:1' THEN 'Do not touch the hot pan.'
    WHEN '25:2' THEN 'The baby likes to touch soft toys.'
    WHEN '26:1' THEN 'Please put the soup in a bowl.'
    WHEN '26:2' THEN 'There are apples in the blue bowl.'
    WHEN '27:1' THEN 'My teacher gave me good advice.'
    WHEN '27:2' THEN 'Thank you for your advice.'
    WHEN '28:1' THEN 'There is too much sugar in this drink.'
    WHEN '28:2' THEN 'Do not watch too much television.'
    WHEN '29:1' THEN 'We ate dinner right after the game.'
    WHEN '29:2' THEN 'Call me right after school.'
    WHEN '30:1' THEN 'Those flowers smell lovely.'
    WHEN '30:2' THEN 'Who are those people by the gate?'
    WHEN '31:1' THEN 'Smoke can be a sign of fire.'
    WHEN '31:2' THEN 'Never play with fire.'
    WHEN '32:1' THEN 'Water can turn into ice in cold weather.'
    WHEN '32:2' THEN 'The caterpillar will turn into a butterfly.'
    WHEN '33:1' THEN 'Please light the candle carefully.'
    WHEN '33:2' THEN 'The candle made the room feel warm.'
    WHEN '34:1' THEN 'There is danger near the broken bridge.'
    WHEN '34:2' THEN 'The warning sign tells us about danger.'
    WHEN '35:1' THEN 'We like to talk after class.'
    WHEN '35:2' THEN 'Please do not talk during the test.'
    WHEN '36:1' THEN 'Use the exit in an emergency.'
    WHEN '36:2' THEN 'The exit is next to the stairs.'
    WHEN '37:1' THEN 'Please come here right away.'
    WHEN '37:2' THEN 'I will finish my homework right away.'
    WHEN '38:1' THEN 'Cover the food before you put it in the fridge.'
    WHEN '38:2' THEN 'Dark clouds covered the sky.'
    WHEN '39:1' THEN 'Take the lift to the sixth floor.'
    WHEN '39:2' THEN 'The lift is beside the stairs.'
    WHEN '40:1' THEN 'The firefighter helped the family leave safely.'
    WHEN '40:2' THEN 'A firefighter wears special protective clothing.'
    WHEN '41:1' THEN 'Use water to put out the campfire.'
    WHEN '41:2' THEN 'The firefighters put out the fire quickly.'
    WHEN '42:1' THEN 'Blow out the candle before you leave.'
    WHEN '42:2' THEN 'The wind can blow the leaves away.'
    WHEN '43:1' THEN 'Would you like tea or juice?'
    WHEN '43:2' THEN 'You can walk or take the bus.'
    WHEN '44:1' THEN 'Would you like a cup of tea?'
    WHEN '44:2' THEN 'He drank a cup of milk.'
    WHEN '45:1' THEN 'Do not go anywhere with a stranger.'
    WHEN '45:2' THEN 'Tell an adult if a stranger talks to you.'
    WHEN '46:1' THEN 'Exercise keeps your body strong.'
    WHEN '46:2' THEN 'Wash your hands to keep your body healthy.'
    WHEN '47:1' THEN 'Someone left a backpack on the chair.'
    WHEN '47:2' THEN 'Can someone help me carry this box?'
    WHEN '48:1' THEN 'What is the reason for being late?'
    WHEN '48:2' THEN 'There is a good reason to wear a seat belt.'
    WHEN '49:1' THEN 'These shoes feel uncomfortable.'
    WHEN '49:2' THEN 'I feel uncomfortable when the room is too hot.'
    WHEN '50:1' THEN 'Technology helps us learn in new ways.'
    WHEN '50:2' THEN 'This robot is an example of modern technology.'
    WHEN '51:1' THEN 'Reading every day is a good habit.'
    WHEN '51:2' THEN 'Make a habit of brushing your teeth twice a day.'
    WHEN '52:1' THEN 'People wrote letters by hand in the past.'
    WHEN '52:2' THEN 'We can learn from the past.'
    WHEN '53:1' THEN 'We keep in touch by sending messages.'
    WHEN '53:2' THEN 'Please keep in touch with your grandparents.'
    WHEN '54:1' THEN 'The weather can change quickly.'
    WHEN '54:2' THEN 'We need to change our plan because it is raining.'
    WHEN '55:1' THEN 'Good communication helps a team work well.'
    WHEN '55:2' THEN 'Talking and listening are both part of communication.'
    WHEN '56:1' THEN 'You can call me anytime.'
    WHEN '56:2' THEN 'You can visit the museum anytime during the holiday.'
    WHEN '57:1' THEN 'You can study anywhere with this book.'
    WHEN '57:2' THEN 'I cannot find my keys anywhere.'
    WHEN '58:1' THEN 'Use the cable to connect the computer to the screen.'
    WHEN '58:2' THEN 'The bridge connects the two sides of the river.'
    WHEN '59:1' THEN 'Smart Education of China offers many online lessons.'
    WHEN '59:2' THEN 'Our teacher showed us Smart Education of China in class.'
    WHEN '60:1' THEN 'The train arrived at platform three.'
    WHEN '60:2' THEN 'Please wait on the platform for the train.'
    WHEN '61:1' THEN 'VR can make a game feel real.'
    WHEN '61:2' THEN 'We used VR to explore the ocean in class.'
    WHEN '62:1' THEN 'For example, a dog is a friendly pet.'
    WHEN '62:2' THEN 'Many fruits are healthy; for example, apples and bananas.'
    WHEN '63:1' THEN 'Finland is a country in northern Europe.'
    WHEN '63:2' THEN 'Many people visit Finland to see the northern lights.'
    WHEN '64:1' THEN 'The railway connects the two cities.'
    WHEN '64:2' THEN 'We watched the train travel along the railway.'
    WHEN '65:1' THEN 'The new railway will connect the town to the airport.'
    WHEN '65:2' THEN 'Please connect your tablet to the Wi-Fi.'
    WHEN '66:1' THEN 'The new railway will go into service next month.'
    WHEN '66:2' THEN 'The bus went into service after its safety check.'
    WHEN '67:1' THEN 'Think carefully before you answer.'
    WHEN '67:2' THEN 'I think this puzzle is fun.'
    WHEN '68:1' THEN 'We will build a birdhouse this weekend.'
    WHEN '68:2' THEN 'Workers are building a new playground.'
    WHEN '69:1' THEN 'Beidou Navigation can help people find their way.'
    WHEN '69:2' THEN 'The phone uses Beidou Navigation to show our location.'
    WHEN '70:1' THEN 'Earth is the planet where we live.'
    WHEN '70:2' THEN 'Earth looks blue from space.'
    ELSE e.`example_text`
END,
e.`translation` = CASE CONCAT(c.`priority_order`, ':', e.`priority_order`)
    WHEN '1:1' THEN '哈尔滨在中国的东北部。'
    WHEN '1:2' THEN '向东北走两个街区，你会看到图书馆。'
    WHEN '2:1' THEN '我们在海滩上堆了一个沙堡。'
    WHEN '2:2' THEN '夏天的海滩很热闹。'
    WHEN '3:1' THEN '我们在科学博物馆玩得很开心。'
    WHEN '3:2' THEN '你的画看起来很棒！'
    WHEN '4:1' THEN '为了你的安全，请戴头盔。'
    WHEN '4:2' THEN '道路安全对每个人都很重要。'
    WHEN '5:1' THEN '我们班有一条规则：要善待每一个人。'
    WHEN '5:2' THEN '请遵守图书馆的规则。'
    WHEN '6:1' THEN '帮助别人可以是一件有意义的事。'
    WHEN '6:2' THEN '我们就友谊进行了一次有意义的谈话。'
    WHEN '7:1' THEN '中国国家图书馆有许多古老的书籍。'
    WHEN '7:2' THEN '上周末我们参观了中国国家图书馆。'
    WHEN '8:1' THEN '我步行去学校。'
    WHEN '8:2' THEN '步行十分钟就能到公园。'
    WHEN '9:1' THEN '我们在中国科学技术馆学习了太空知识。'
    WHEN '9:2' THEN '中国科学技术馆很受孩子们欢迎。'
    WHEN '10:1' THEN '我家离学校很远。'
    WHEN '10:2' THEN '公交车站离这里不远。'
    WHEN '11:1' THEN '宝宝正在婴儿车里睡觉。'
    WHEN '11:2' THEN '鸟妈妈在喂它的幼鸟。'
    WHEN '12:1' THEN '小鸡跟着妈妈走。'
    WHEN '12:2' THEN '一只黄色小鸡正在啄种子。'
    WHEN '13:1' THEN '我有时睡前阅读。'
    WHEN '13:2' THEN '下午有时会下雨。'
    WHEN '14:1' THEN '我和爸爸星期天去钓鱼。'
    WHEN '14:2' THEN '我们在湖边钓鱼。'
    WHEN '15:1' THEN '猫头鹰在白天睡觉。'
    WHEN '15:2' THEN '白天很难看见星星。'
    WHEN '16:1' THEN '我姐姐想去大学读书。'
    WHEN '16:2' THEN '这所大学有一个很大的图书馆。'
    WHEN '17:1' THEN '多伦多是加拿大最大的城市。'
    WHEN '17:2' THEN '我表哥住在多伦多。'
    WHEN '18:1' THEN '渥太华是加拿大的首都。'
    WHEN '18:2' THEN '议会大厦在渥太华。'
    WHEN '19:1' THEN '医生在医院工作。'
    WHEN '19:2' THEN '我们带爷爷去了医院。'
    WHEN '20:1' THEN '请把椅子移近桌子。'
    WHEN '20:2' THEN '公共汽车开始移动了。'
    WHEN '21:1' THEN '听到这个坏消息时，他摇了摇头。'
    WHEN '21:2' THEN '戴帽子保护头部免受阳光照射。'
    WHEN '22:1' THEN '骑自行车时一定要戴头盔。'
    WHEN '22:2' THEN '他的头盔是亮蓝色的。'
    WHEN '23:1' THEN '沿着小路走到操场。'
    WHEN '23:2' THEN '请跟着老师走。'
    WHEN '24:1' THEN '我因为胃痛待在家里。'
    WHEN '24:2' THEN '吃太多糖会让你胃痛。'
    WHEN '25:1' THEN '不要碰热锅。'
    WHEN '25:2' THEN '宝宝喜欢摸柔软的玩具。'
    WHEN '26:1' THEN '请把汤盛在碗里。'
    WHEN '26:2' THEN '蓝色的碗里有苹果。'
    WHEN '27:1' THEN '老师给了我很好的建议。'
    WHEN '27:2' THEN '谢谢你的建议。'
    WHEN '28:1' THEN '这杯饮料里的糖太多。'
    WHEN '28:2' THEN '不要看太多电视。'
    WHEN '29:1' THEN '比赛结束后我们立刻吃了晚饭。'
    WHEN '29:2' THEN '放学后立刻给我打电话。'
    WHEN '30:1' THEN '那些花闻起来很香。'
    WHEN '30:2' THEN '大门旁边的那些人是谁？'
    WHEN '31:1' THEN '烟可能是失火的信号。'
    WHEN '31:2' THEN '绝不能玩火。'
    WHEN '32:1' THEN '天气寒冷时，水会变成冰。'
    WHEN '32:2' THEN '毛毛虫会变成蝴蝶。'
    WHEN '33:1' THEN '请小心点燃蜡烛。'
    WHEN '33:2' THEN '蜡烛让房间感觉很温暖。'
    WHEN '34:1' THEN '破桥附近有危险。'
    WHEN '34:2' THEN '警示牌告诉我们有危险。'
    WHEN '35:1' THEN '我们喜欢课后聊天。'
    WHEN '35:2' THEN '考试期间请不要说话。'
    WHEN '36:1' THEN '紧急情况下请使用出口。'
    WHEN '36:2' THEN '出口在楼梯旁边。'
    WHEN '37:1' THEN '请马上过来。'
    WHEN '37:2' THEN '我会立刻完成作业。'
    WHEN '38:1' THEN '把食物放进冰箱前先盖好。'
    WHEN '38:2' THEN '乌云遮住了天空。'
    WHEN '39:1' THEN '乘电梯到六楼。'
    WHEN '39:2' THEN '电梯在楼梯旁边。'
    WHEN '40:1' THEN '消防员帮助这家人安全离开。'
    WHEN '40:2' THEN '消防员穿着特殊的防护服。'
    WHEN '41:1' THEN '用水扑灭篝火。'
    WHEN '41:2' THEN '消防员很快扑灭了火。'
    WHEN '42:1' THEN '离开前吹灭蜡烛。'
    WHEN '42:2' THEN '风会把树叶吹走。'
    WHEN '43:1' THEN '你想要茶还是果汁？'
    WHEN '43:2' THEN '你可以步行或者乘公交车。'
    WHEN '44:1' THEN '你想来一杯茶吗？'
    WHEN '44:2' THEN '他喝了一杯牛奶。'
    WHEN '45:1' THEN '不要跟陌生人去任何地方。'
    WHEN '45:2' THEN '如果陌生人和你说话，告诉一位成年人。'
    WHEN '46:1' THEN '锻炼使你的身体强壮。'
    WHEN '46:2' THEN '洗手能让身体保持健康。'
    WHEN '47:1' THEN '有人把一个背包落在椅子上了。'
    WHEN '47:2' THEN '有人能帮我搬这个箱子吗？'
    WHEN '48:1' THEN '迟到的原因是什么？'
    WHEN '48:2' THEN '系安全带是有充分理由的。'
    WHEN '49:1' THEN '这双鞋穿着不舒服。'
    WHEN '49:2' THEN '房间太热时我会觉得不舒服。'
    WHEN '50:1' THEN '科技以新的方式帮助我们学习。'
    WHEN '50:2' THEN '这个机器人是现代科技的一个例子。'
    WHEN '51:1' THEN '每天阅读是一个好习惯。'
    WHEN '51:2' THEN '养成每天刷两次牙的习惯。'
    WHEN '52:1' THEN '过去人们手写信件。'
    WHEN '52:2' THEN '我们可以从过去中学习。'
    WHEN '53:1' THEN '我们通过发消息保持联系。'
    WHEN '53:2' THEN '请和你的祖父母保持联系。'
    WHEN '54:1' THEN '天气会很快变化。'
    WHEN '54:2' THEN '因为下雨，我们需要改变计划。'
    WHEN '55:1' THEN '良好的沟通能帮助团队合作顺利。'
    WHEN '55:2' THEN '说和听都是沟通的一部分。'
    WHEN '56:1' THEN '你随时可以给我打电话。'
    WHEN '56:2' THEN '假期期间你可以随时参观博物馆。'
    WHEN '57:1' THEN '有了这本书，你可以在任何地方学习。'
    WHEN '57:2' THEN '我到处都找不到钥匙。'
    WHEN '58:1' THEN '用电缆把电脑连接到屏幕上。'
    WHEN '58:2' THEN '这座桥连接着河的两岸。'
    WHEN '59:1' THEN '国家智慧教育公共服务平台提供许多在线课程。'
    WHEN '59:2' THEN '老师在课堂上向我们展示了国家智慧教育公共服务平台。'
    WHEN '60:1' THEN '火车到达了三号站台。'
    WHEN '60:2' THEN '请在站台上等火车。'
    WHEN '61:1' THEN '虚拟现实能让游戏感觉很真实。'
    WHEN '61:2' THEN '课堂上我们用虚拟现实探索海洋。'
    WHEN '62:1' THEN '例如，狗是一种友好的宠物。'
    WHEN '62:2' THEN '许多水果很健康，例如苹果和香蕉。'
    WHEN '63:1' THEN '芬兰是北欧的一个国家。'
    WHEN '63:2' THEN '许多人去芬兰看北极光。'
    WHEN '64:1' THEN '这条铁路连接两座城市。'
    WHEN '64:2' THEN '我们看着火车沿铁路行驶。'
    WHEN '65:1' THEN '新铁路将把小镇与机场连接起来。'
    WHEN '65:2' THEN '请把平板电脑连接到无线网络。'
    WHEN '66:1' THEN '新铁路将于下个月投入使用。'
    WHEN '66:2' THEN '公交车通过安全检查后投入使用。'
    WHEN '67:1' THEN '回答前要认真思考。'
    WHEN '67:2' THEN '我觉得这个拼图很有趣。'
    WHEN '68:1' THEN '这个周末我们要建一个鸟屋。'
    WHEN '68:2' THEN '工人们正在建一个新操场。'
    WHEN '69:1' THEN '北斗导航可以帮助人们找到方向。'
    WHEN '69:2' THEN '手机使用北斗导航显示我们的位置。'
    WHEN '70:1' THEN '地球是我们生活的星球。'
    WHEN '70:2' THEN '从太空看，地球是蓝色的。'
    ELSE e.`translation`
END
WHERE c.`priority_order` BETWEEN 1 AND 70
  AND e.`priority_order` IN (1, 2);

# Continue the imported word list from Earth onward when this file is run by
# the MySQL client. The companion migration is also safe to run by itself.
source update_kids_cards_remaining.sql
source update_kids_cards_unit6_7.sql
source 20260925_add_learning_catalog.sql
source 20260925_redesign_learning_progress.sql
source 20260926_add_membership_material_management.sql
source 20260927_add_learning_course_material_mapping.sql
source 20260927_add_learning_topic_course_mapping.sql
