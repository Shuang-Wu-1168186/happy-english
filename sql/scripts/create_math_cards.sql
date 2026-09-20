-- Math knowledge cards: table definition and all initial data.
-- Safe to run more than once: existing cards with the same title are updated.
CREATE TABLE IF NOT EXISTS math_card (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    category VARCHAR(100) NOT NULL,
    title VARCHAR(200) NOT NULL,
    summary TEXT NOT NULL,
    key_points TEXT NOT NULL,
    common_mistakes TEXT NOT NULL,
    example_question TEXT NOT NULL,
    example_answer TEXT NOT NULL,
    example_image_url VARCHAR(255) DEFAULT NULL,
    sort_order INT NOT NULL DEFAULT 0,
    is_published TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_math_card_title (title),
    KEY idx_math_card_published_order (is_published, sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='数学知识点卡片';

INSERT INTO math_card
(category,title,summary,key_points,common_mistakes,example_question,example_answer,example_image_url,sort_order)
VALUES
('圆与扇形','圆的面积','把圆等分后可近似拼成长方形：长约为 πr，宽为 r。','面积公式：S = πr²。\n半径扩大 k 倍，面积扩大 k² 倍。','不要把周长 2πr 当成面积。\n题目给直径时，要先除以 2 得半径。','一个圆的半径是 4 cm，π 取 3.14，面积是多少？','S = 3.14 × 4² = 3.14 × 16 = 50.24 cm²。','/static/images/math_cards/circle_area.svg',1),
('圆与扇形','扇形面积','扇形面积由它的圆心角占整圆的比例决定。','S扇 = πr² × n ÷ 360°。\n先算整圆面积，再乘圆心角占比。','不要忘记除以 360°。\n半径和圆心角必须来自同一个扇形。','半径 6 cm、圆心角 90° 的扇形面积是多少？','S = 3.14 × 6² × 90 ÷ 360 = 28.26 cm²。','/static/images/math_cards/sector_area.svg',2),
('圆与扇形','弓形面积','弓形由一段弧和一条弦围成，可以拆成扇形和三角形。','弓形面积 = 扇形面积 − 三角形面积。\n先确认图中较小的弓形还是较大的弓形。','不要直接用圆面积减三角形面积。\n三角形必须是两个半径围成的三角形。','半径 10 cm、圆心角 90° 的小弓形面积如何表示？','先算 90° 扇形面积，再减去两条半径组成的直角三角形面积。','/static/images/math_cards/segment_area.svg',3),
('组合图形','整体减空白','复杂阴影图形常常比“逐块相加”更适合整体减去空白部分。','阴影面积 = 外部整体面积 − 内部空白面积。\n先找外边界，再找被挖去的图形。','不要漏掉内部空白。\n面积单位必须统一。','一个长方形中挖去一个圆，阴影面积怎样求？','长方形面积 − 圆面积；若给的是直径，先求半径。','/static/images/math_cards/composite_area.svg',4),
('分数计算','分数乘法','整数、分数和带分数相乘，都可转成分数乘法处理。','分子乘分子，分母乘分母。\n能先约分就先约分。\n带分数先化成假分数。','不能把分母相加。\n约分必须是分子和分母同时除以同一个数。','计算 2/7 × 3/5。','2×3 / 7×5 = 6/35，已经最简。','/static/images/math_cards/fraction_multiply.svg',5),
('分数应用','单位“1”与分数应用','应用题先明确“谁被平均分成几份”，这就是单位“1”。','求一个数的几分之几：单位“1”的量 × 分率。\n剩余量 = 原量 × (1 − 减少的分率)。','单位“1”找错，后面计算都会错。\n“比……多/少”要先判断比较对象。','一根绳子长 24 m，用去它的 3/4，还剩多少米？','剩余分率是 1 − 3/4 = 1/4；24 × 1/4 = 6 m。','/static/images/math_cards/fraction_application.svg',6)
,
('分数计算','分数乘整数','整数可看成分母为 1 的分数。','分母不变，分子与整数相乘。\n例如：2/7 × 7 = 2。','能约分时先约分，避免数字变大。','计算 3/8 × 12。','先约分：12÷8=3÷2，所以结果为 3×3÷2=9/2=4又1/2。','/static/images/math_cards/fraction_multiply.svg',7),
('分数计算','分数乘分数','两个分数相乘时，分别相乘分子和分母。','a/b × c/d = ac/bd。\n先约分，再相乘。','不要把分母相加，也不要只约一个分子。','计算 6/15 × 5/8。','6 和 8 约分为 3 和 4，5 和 15 约分为 1 和 3；结果为 1/4。','/static/images/math_cards/fraction_multiply.svg',8),
('分数计算','带分数乘法','带分数不能直接参与分子、分母相乘。','先把带分数化为假分数，再按分数乘法计算。','忘记把整数部分乘进分母是最常见错误。','计算 1又1/2 × 2/3。','1又1/2=3/2；3/2×2/3=1。','/static/images/math_cards/fraction_multiply.svg',9),
('分数计算','连锁约分','三个或更多分数连乘时，可让前一个分子的数与后一个分母的数依次约分。','相邻交叉约分：前一个分子的数可与后一个分母的数同除。\n全部约完后，常只剩第一个分母与最后一个分子。','约分只能除以同一个非零数；不要跨加减号约分。','计算 4/15 × 9/4 × 8/9。','4 与后一个分母 4 约去，9 与后一个分母 9 约去；只剩最后一个分子 8 和第一个分母 15，结果=8/15。','/static/images/math_cards/fraction_multiply.svg',10),
('分数技巧','乘法分配律拆括号','当括号内各项有相同分母或可共同计算时，可用分配律。','(a+b−c)×d=a×d+b×d−c×d。','符号必须跟着每一项一起分配，减号不能遗漏。','计算 (3/8+1/4)×8。','3/8×8 + 1/4×8 = 3+2=5。','/static/images/math_cards/fraction_multiply.svg',11),
('分数技巧','提取公因数','多项式中每项都有相同因数时，先提出可化简。','a×c+b×c=(a+b)×c。','只提取真正每一项都含有的因数。','计算 7/12×5 + 5/12×5。','提取 5： (7/12+5/12)×5 = 5。','/static/images/math_cards/fraction_multiply.svg',12),
('分数技巧','拆 1 分配','遇到接近 1 的分数，可把它写成 1−分数。','A×(1−1/b)=A−A/b。','括号和减号必须保留到每一步。','计算 18×(1−1/3)。','18−18/3=18−6=12。','/static/images/math_cards/fraction_multiply.svg',13),
('分数技巧','统一公因数','多个乘法项的分子含有共同倍数时，可用交换位置和拆分因数统一化简。','乘积不变：可交换因数位置，再拆分可约的因数。','只适用于纯乘法；加减法不能随意交换后约分。','计算 3/14×7/9×6。','把6拆成2×3，分别与14、9约分，再相乘。','/static/images/math_cards/fraction_multiply.svg',14),
('分数应用','求剩余量','“剩下多少”可先求减少量再相减，也可直接求剩余分率。','剩余分率=1−减少分率。\n剩余量=单位“1”的量×剩余分率。','题目若是连续减少，要逐次乘剩余分率。','一桶水有 60 L，倒出 2/5，剩多少？','60×(1−2/5)=60×3/5=36 L。','/static/images/math_cards/fraction_application.svg',15),
('分数应用','比一个数多或少几分之几','“比甲多 a/b”以甲为单位“1”。','乙=甲×(1+a/b)。\n“比甲少”则用 1−a/b。','不要把“多几分之几”误算成只取 a/b。','甲有 40 本书，乙比甲多 1/4，乙有多少本？','40×(1+1/4)=40×5/4=50 本。','/static/images/math_cards/fraction_application.svg',16),
('分数应用','移多补少','从甲给乙一部分后相等时，甲原来比乙多的量是给出量的 2 倍。','给出量=两者原来相差量÷2。','要分清“给出后相等”和“给出后还差多少”。','甲比乙多 12 个，甲给乙多少个后相等？','多出的12个要两边平分，甲给乙 6 个。','/static/images/math_cards/fraction_application.svg',17),
('分数应用进阶','和倍型占比（设份数法）','已知两个量的比或“甲是乙的 a/b”，可设为对应份数。','若甲是乙的a/b，可设甲a份、乙b份；总份数=a+b。','不要把 a/b 当成总份数；先统一单位。','甲是乙的 3/5，两数和为 64，甲是多少？','总份数8份，每份8；甲=3×8=24。','/static/images/math_cards/fraction_application.svg',18),
('分数应用进阶','兑水与连锁递推','每次剩余都是上一次剩余乘以本次剩余分率；递推题按前一天量继续算。','连续操作：最后量=原量×每次剩余分率的连乘。\n递推题写出相邻两步关系。','不能把连续减少的分率直接相加。','一杯水每次喝掉1/2，连续喝2次后剩多少？','1×(1−1/2)×(1−1/2)=1/4。','/static/images/math_cards/fraction_application.svg',19)
ON DUPLICATE KEY UPDATE
category=VALUES(category), summary=VALUES(summary), key_points=VALUES(key_points),
common_mistakes=VALUES(common_mistakes), example_question=VALUES(example_question),
example_answer=VALUES(example_answer), example_image_url=VALUES(example_image_url), sort_order=VALUES(sort_order);
