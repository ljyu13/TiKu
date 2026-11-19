#!/usr/bin/env python3
"""英语题目生成器：小学（3-6）、初中（7-9）、高中（10-12）。
词汇 + 语法模板，答案由素材表确定。
"""
from .core import fmt_num

# 分级词汇表：(单词, 词义, 词性)
WORDS = {
    "primary": [
        ("apple", "苹果", "n."), ("banana", "香蕉", "n."), ("cat", "猫", "n."),
        ("dog", "狗", "n."), ("egg", "鸡蛋", "n."), ("fish", "鱼", "n."),
        ("book", "书", "n."), ("pen", "钢笔", "n."), ("red", "红色", "adj."),
        ("blue", "蓝色", "adj."), ("green", "绿色", "adj."), ("yellow", "黄色", "adj."),
        ("big", "大的", "adj."), ("small", "小的", "adj."), ("happy", "快乐的", "adj."),
        ("sad", "伤心的", "adj."), ("teacher", "老师", "n."), ("student", "学生", "n."),
        ("school", "学校", "n."), ("home", "家", "n."), ("water", "水", "n."),
        ("milk", "牛奶", "n."), ("bread", "面包", "n."), ("rice", "米饭", "n."),
        ("bird", "鸟", "n."), ("tiger", "老虎", "n."), ("monkey", "猴子", "n."),
        ("panda", "熊猫", "n."), ("sun", "太阳", "n."), ("moon", "月亮", "n."),
        ("star", "星星", "n."), ("tree", "树", "n."), ("flower", "花", "n."),
        ("car", "汽车", "n."), ("bus", "公共汽车", "n."), ("bike", "自行车", "n."),
        ("head", "头", "n."), ("hand", "手", "n."), ("eye", "眼睛", "n."),
        ("foot", "脚", "n."), ("morning", "早晨", "n."), ("afternoon", "下午", "n."),
        ("one", "一", "num."), ("two", "二", "num."), ("three", "三", "num."),
        ("four", "四", "num."), ("five", "五", "num."), ("six", "六", "num."),
        ("seven", "七", "num."), ("eight", "八", "num."), ("nine", "九", "num."),
        ("ten", "十", "num."), ("father", "父亲", "n."), ("mother", "母亲", "n."),
        ("sister", "姐妹", "n."), ("brother", "兄弟", "n."), ("friend", "朋友", "n."),
        ("chair", "椅子", "n."), ("desk", "桌子", "n."), ("door", "门", "n."),
        ("window", "窗户", "n."), ("black", "黑色", "adj."), ("white", "白色", "adj."),
        ("hot", "热的", "adj."), ("cold", "冷的", "adj."), ("new", "新的", "adj."),
        ("old", "旧的", "adj."), ("long", "长的", "adj."), ("short", "短的", "adj."),
        ("tall", "高的", "adj."), ("thin", "瘦的", "adj."), ("fat", "胖的", "adj."),
        ("run", "跑", "v."), ("jump", "跳", "v."), ("swim", "游泳", "v."),
        ("sing", "唱歌", "v."), ("dance", "跳舞", "v."), ("eat", "吃", "v."),
        ("drink", "喝", "v."), ("sleep", "睡觉", "v."), ("read", "读", "v."),
        ("write", "写", "v."), ("play", "玩", "v."), ("look", "看", "v."),
        ("listen", "听", "v."), ("walk", "走", "v."), ("fly", "飞", "v."),
    ],
    "junior": [
        ("important", "重要的", "adj."), ("difficult", "困难的", "adj."),
        ("easy", "容易的", "adj."), ("different", "不同的", "adj."),
        ("same", "相同的", "adj."), ("interesting", "有趣的", "adj."),
        ("boring", "无聊的", "adj."), ("exciting", "令人兴奋的", "adj."),
        ("careful", "仔细的", "adj."), ("careless", "粗心的", "adj."),
        ("friendly", "友好的", "adj."), ("quiet", "安静的", "adj."),
        ("noisy", "吵闹的", "adj."), ("busy", "忙碌的", "adj."),
        ("free", "空闲的", "adj."), ("healthy", "健康的", "adj."),
        ("delicious", "美味的", "adj."), ("beautiful", "美丽的", "adj."),
        ("comfortable", "舒适的", "adj."), ("dangerous", "危险的", "adj."),
        ("decide", "决定", "v."), ("forget", "忘记", "v."), ("remember", "记得", "v."),
        ("understand", "理解", "v."), ("believe", "相信", "v."), ("improve", "改进", "v."),
        ("describe", "描述", "v."), ("discuss", "讨论", "v."), ("explain", "解释", "v."),
        ("compare", "比较", "v."), ("prepare", "准备", "v."), ("protect", "保护", "v."),
        ("pollute", "污染", "v."), ("recycle", "回收利用", "v."), ("invent", "发明", "v."),
        ("discover", "发现", "v."), ("suggest", "建议", "v."), ("refuse", "拒绝", "v."),
        ("accept", "接受", "v."), ("achieve", "实现", "v."),
        ("environment", "环境", "n."), ("pollution", "污染", "n."),
        ("technology", "技术", "n."), ("information", "信息", "n."),
        ("knowledge", "知识", "n."), ("experience", "经验；经历", "n."),
        ("problem", "问题", "n."), ("solution", "解决办法", "n."),
        ("future", "未来", "n."), ("past", "过去", "n."), ("present", "现在", "n."),
        ("trade", "贸易", "n."), ("traffic", "交通", "n."), ("tradition", "传统", "n."),
        ("culture", "文化", "n."), ("science", "科学", "n."), ("nature", "自然", "n."),
        ("energy", "能源", "n."), ("waste", "浪费；废物", "n."), ("habit", "习惯", "n."),
        ("hobby", "爱好", "n."), ("dream", "梦想", "n."), ("goal", "目标", "n."),
        ("chance", "机会", "n."), ("advantage", "优点", "n."), ("disadvantage", "缺点", "n."),
    ],
    "senior": [
        ("abandon", "放弃", "v."), ("absorb", "吸收", "v."), ("accompany", "陪伴", "v."),
        ("accomplish", "完成", "v."), ("accumulate", "积累", "v."), ("acknowledge", "承认", "v."),
        ("adapt", "适应", "v."), ("adjust", "调整", "v."), ("admire", "钦佩", "v."),
        ("adopt", "采纳；收养", "v."), ("advocate", "提倡", "v."), ("affect", "影响", "v."),
        ("afford", "负担得起", "v."), ("analyse", "分析", "v."), ("announce", "宣布", "v."),
        ("appeal", "呼吁；吸引", "v."), ("apply", "申请；应用", "v."), ("appreciate", "欣赏；感激", "v."),
        ("approach", "接近；方法", "v./n."), ("approve", "赞成", "v."), ("argue", "争论", "v."),
        ("assume", "假定", "v."), ("attach", "附上", "v."), ("attempt", "尝试", "v."),
        ("attract", "吸引", "v."), ("avoid", "避免", "v."), ("aware", "意识到的", "adj."),
        ("benefit", "益处；受益", "n./v."), ("brilliant", "杰出的", "adj."),
        ("capable", "有能力的", "adj."), ("challenge", "挑战", "n./v."),
        ("commit", "承诺；犯（错）", "v."), ("compete", "竞争", "v."), ("complex", "复杂的", "adj."),
        ("concentrate", "集中", "v."), ("concern", "关心；担忧", "v./n."),
        ("conclude", "得出结论", "v."), ("conduct", "进行；实施", "v."),
        ("confident", "自信的", "adj."), ("confirm", "确认", "v."), ("conflict", "冲突", "n./v."),
        ("consequence", "后果", "n."), ("consider", "考虑", "v."), ("consist", "组成", "v."),
        ("constant", "持续的", "adj."), ("contribute", "贡献", "v."), ("convince", "说服", "v."),
        ("crucial", "至关重要的", "adj."), ("curious", "好奇的", "adj."),
        ("decline", "下降；婉拒", "v./n."), ("defend", "保卫", "v."), ("demand", "要求", "v./n."),
        ("deny", "否认", "v."), ("depend", "依靠", "v."), ("deserve", "值得", "v."),
        ("determine", "决定；确定", "v."), ("devote", "致力于", "v."),
        ("dilemma", "困境", "n."), ("discipline", "纪律", "n."), ("distinguish", "区分", "v."),
        ("distribute", "分发", "v."), ("diverse", "多样的", "adj."), ("dominate", "支配", "v."),
        ("doubt", "怀疑", "v./n."), ("duty", "责任", "n."), ("eager", "渴望的", "adj."),
        ("efficient", "高效的", "adj."), ("eliminate", "消除", "v."), ("emerge", "出现", "v."),
        ("emphasize", "强调", "v."), ("encounter", "遭遇", "v."), ("endure", "忍受", "v."),
        ("enhance", "增强", "v."), ("enormous", "巨大的", "adj."), ("ensure", "确保", "v."),
        ("essential", "必要的", "adj."), ("establish", "建立", "v."), ("estimate", "估计", "v./n."),
        ("evaluate", "评估", "v."), ("evidence", "证据", "n."), ("exhibit", "展览", "v./n."),
        ("expand", "扩大", "v."), ("expect", "期待", "v."), ("explore", "探索", "v."),
        ("expose", "暴露", "v."), ("extend", "延伸", "v."), ("external", "外部的", "adj."),
        ("fascinating", "迷人的", "adj."), ("feasible", "可行的", "adj."),
        ("flexible", "灵活的", "adj."), ("focus", "集中；焦点", "v./n."),
        ("forbid", "禁止", "v."), ("forecast", "预测", "v./n."), ("fortune", "财富；运气", "n."),
        ("found", "建立", "v."), ("frequent", "频繁的", "adj."), ("fundamental", "基本的", "adj."),
        ("generate", "产生", "v."), ("genuine", "真正的", "adj."), ("gradual", "逐渐的", "adj."),
        ("guarantee", "保证", "v./n."), ("identify", "识别", "v."), ("ignore", "忽视", "v."),
        ("illustrate", "说明", "v."), ("impact", "影响", "n./v."), ("implement", "实施", "v."),
        ("imply", "暗示", "v."), ("impose", "强加", "v."), ("impress", "使印象深刻", "v."),
        ("improve", "改善", "v."), ("incident", "事件", "n."), ("independent", "独立的", "adj."),
        ("indicate", "表明", "v."), ("individual", "个人", "n./adj."), ("industry", "工业", "n."),
        ("inevitable", "不可避免的", "adj."), ("influence", "影响", "n./v."),
        ("inform", "告知", "v."), ("initial", "最初的", "adj."), ("innovation", "创新", "n."),
        ("insist", "坚持", "v."), ("inspire", "激励", "v."), ("install", "安装", "v."),
        ("institution", "机构", "n."), ("intend", "打算", "v."), ("interpret", "解释", "v."),
        ("introduce", "引进；介绍", "v."), ("investigate", "调查", "v."), ("involve", "涉及", "v."),
        ("isolated", "孤立的", "adj."), ("issue", "问题；发布", "n./v."),
        ("justify", "证明……正当", "v."), ("maintain", "维持；主张", "v."),
        ("major", "主要的；专业", "adj./n."), ("manage", "设法做到；管理", "v."),
        ("manufacture", "制造", "v./n."), ("mature", "成熟的", "adj."),
        ("measure", "测量；措施", "v./n."), ("mechanism", "机制", "n."),
        ("mention", "提到", "v."), ("method", "方法", "n."), ("mild", "温和的", "adj."),
        ("minimize", "使最小化", "v."), ("moderate", "适度的", "adj."),
        ("modify", "修改", "v."), ("monitor", "监控", "v."), ("motivate", "激励", "v."),
        ("multiple", "多样的", "adj."), ("neglect", "忽视", "v."), ("negotiate", "谈判", "v."),
        ("nevertheless", "然而", "adv."), ("normal", "正常的", "adj."),
        ("notice", "注意到", "v."), ("obtain", "获得", "v."), ("obvious", "明显的", "adj."),
        ("occupy", "占据", "v."), ("occur", "发生", "v."), ("offer", "提供", "v."),
        ("operate", "运作；手术", "v."), ("opportunity", "机会", "n."),
        ("oppose", "反对", "v."), ("optimistic", "乐观的", "adj."), ("option", "选择", "n."),
        ("ordinary", "普通的", "adj."), ("organize", "组织", "v."), ("origin", "起源", "n."),
        ("outcome", "结果", "n."), ("overall", "总的", "adj."), ("overcome", "克服", "v."),
        ("participate", "参与", "v."), ("particular", "特别的", "adj."),
        ("perceive", "感知", "v."), ("permanent", "永久的", "adj."),
        ("perspective", "视角", "n."), ("persuade", "说服", "v."), ("phenomenon", "现象", "n."),
        ("policy", "政策", "n."), ("potential", "潜在的；潜力", "adj./n."),
        ("precise", "精确的", "adj."), ("predict", "预测", "v."), ("prefer", "更喜欢", "v."),
        ("prejudice", "偏见", "n."), ("preserve", "保护", "v."), ("pressure", "压力", "n."),
        ("previous", "先前的", "adj."), ("priority", "优先事项", "n."),
        ("procedure", "程序", "n."), ("process", "过程", "n./v."), ("promote", "促进", "v."),
        ("proportion", "比例", "n."), ("propose", "提议", "v."), ("prospect", "前景", "n."),
        ("protect", "保护", "v."), ("prove", "证明", "v."), ("provide", "提供", "v."),
        ("pursue", "追求", "v."), ("quality", "质量", "n."), ("quantity", "数量", "n."),
        ("react", "反应", "v."), ("realistic", "现实的", "adj."), ("reasonable", "合理的", "adj."),
        ("recall", "回忆", "v."), ("recognize", "认出；承认", "v."), ("recommend", "推荐", "v."),
        ("reduce", "减少", "v."), ("reflect", "反映；反思", "v."), ("reform", "改革", "n./v."),
        ("regard", "认为", "v."), ("region", "地区", "n."), ("register", "登记", "v."),
        ("regret", "后悔", "v."), ("reinforce", "加强", "v."), ("reject", "拒绝", "v."),
        ("relevant", "相关的", "adj."), ("reliable", "可靠的", "adj."),
        ("relieve", "缓解", "v."), ("reluctant", "不情愿的", "adj."), ("remain", "保持", "v."),
        ("remarkable", "显著的", "adj."), ("remind", "提醒", "v."), ("remove", "移除", "v."),
        ("replace", "取代", "v."), ("represent", "代表", "v."), ("reputation", "名声", "n."),
        ("require", "要求", "v."), ("rescue", "营救", "v."), ("reserve", "保留；预订", "v."),
        ("resist", "抵制", "v."), ("resolve", "解决", "v."), ("resource", "资源", "n."),
        ("respond", "回应", "v."), ("responsible", "负责的", "adj."), ("restore", "恢复", "v."),
        ("restrict", "限制", "v."), ("retain", "保留", "v."), ("retreat", "撤退", "v."),
        ("reveal", "揭示", "v."), ("reverse", "颠倒", "v."), ("review", "复习；评论", "v./n."),
        ("revise", "修订", "v."), ("reward", "奖励", "n./v."), ("rigid", "僵化的", "adj."),
        ("rival", "对手", "n."), ("rough", "粗糙的；大约", "adj."), ("routine", "常规", "n."),
        ("rural", "农村的", "adj."), ("sacrifice", "牺牲", "v./n."),
        ("satisfy", "满足", "v."), ("scarce", "稀缺的", "adj."), ("schedule", "日程", "n."),
        ("scheme", "计划", "n."), ("secure", "安全的；获得", "adj./v."),
        ("seek", "寻求", "v."), ("sensitive", "敏感的", "adj."), ("separate", "分离", "v."),
        ("severe", "严重的", "adj."), ("shift", "转变", "v./n."), ("shortage", "短缺", "n."),
        ("significant", "重要的", "adj."), ("similar", "相似的", "adj."),
        ("simplify", "简化", "v."), ("sincere", "真诚的", "adj."), ("situation", "情况", "n."),
        ("skill", "技能", "n."), ("solution", "解决方案", "n."), ("sophisticated", "复杂精密的", "adj."),
        ("specific", "具体的", "adj."), ("stable", "稳定的", "adj."), ("standard", "标准", "n."),
        ("strategic", "战略的", "adj."), ("strength", "力量；优势", "n."),
        ("strengthen", "加强", "v."), ("stress", "压力；强调", "n./v."),
        ("strict", "严格的", "adj."), ("strike", "罢工；打击", "n./v."),
        ("struggle", "挣扎；努力", "v."), ("substantial", "大量的", "adj."),
        ("substitute", "替代", "v./n."), ("sufficient", "充足的", "adj."),
        ("summarize", "总结", "v."), ("superior", "优越的", "adj."),
        ("supply", "供应", "v./n."), ("support", "支持", "v./n."),
        ("suppose", "假设", "v."), ("survive", "幸存", "v."), ("sustain", "维持", "v."),
        ("switch", "转换", "v."), ("symbol", "象征", "n."), ("sympathy", "同情", "n."),
        ("tackle", "处理", "v."), ("temporary", "暂时的", "adj."), ("tendency", "趋势", "n."),
        ("tension", "紧张", "n."), ("term", "术语；学期", "n."), ("thorough", "彻底的", "adj."),
        ("threat", "威胁", "n."), ("thrive", "兴旺", "v."), ("tolerance", "容忍", "n."),
        ("tough", "艰难的；坚韧的", "adj."), ("trace", "追踪", "v."), ("trade", "贸易", "n."),
        ("tradition", "传统", "n."), ("transfer", "转移", "v."), ("transform", "转变", "v."),
        ("transparent", "透明的", "adj."), ("transport", "运输", "v./n."),
        ("tremendous", "巨大的", "adj."), ("trend", "趋势", "n."), ("trial", "试验；审判", "n."),
        ("trigger", "引发", "v."), ("ultimate", "最终的", "adj."), ("undergo", "经历", "v."),
        ("undertake", "承担", "v."), ("unique", "独特的", "adj."), ("universal", "普遍的", "adj."),
        ("urgent", "紧急的", "adj."), ("utilize", "利用", "v."), ("vague", "模糊的", "adj."),
        ("valid", "有效的", "adj."), ("value", "价值；重视", "n./v."),
        ("vary", "变化", "v."), ("vast", "广阔的", "adj."), ("vital", "至关重要的", "adj."),
        ("volunteer", "志愿者", "n."), ("wander", "漫步", "v."), ("warn", "警告", "v."),
        ("weakness", "弱点", "n."), ("wealth", "财富", "n."), ("weigh", "权衡；称重", "v."),
        ("welfare", "福利", "n."), ("widespread", "广泛的", "adj."), ("willing", "愿意的", "adj."),
        ("withdraw", "撤回", "v."), ("witness", "见证", "v./n."), ("worthwhile", "值得的", "adj."),
        ("yield", "产生；屈服", "v."), ("zone", "区域", "n."),
    ],
}


def _word_pool(g):
    if g <= 6:
        return WORDS["primary"]
    if g <= 9:
        return WORDS["junior"]
    return WORDS["senior"]


def w_en_cn(b):
    words = _word_pool(b.grade)
    w, mean, pos = b.rng.choice(words)
    others = b.rng.sample([x for x in words if x[1] != mean], 3)
    b.choice("单词 \"%s\" 的中文意思是？" % w, mean,
             [o[1] for o in others], "单词 %s 的意思是\"%s\"。" % (w, mean), ["词汇理解"])


def w_cn_en(b):
    words = _word_pool(b.grade)
    w, mean, pos = b.rng.choice(words)
    others = b.rng.sample([x for x in words if x[0] != w], 3)
    b.choice("\"%s\" 对应的英文单词是？" % mean, w,
             [o[0] for o in others], "\"%s\" 的英文是 %s。" % (mean, w), ["词汇拼写"])


def w_judge(b):
    words = _word_pool(b.grade)
    w, mean, pos = b.rng.choice(words)
    if b.rng.random() < 0.5:
        b.judge("单词 \"%s\" 的意思是\"%s\"。" % (w, mean), True,
                "%s 的中文释义确实是\"%s\"。" % (w, mean), ["词汇理解"])
    else:
        wrong = b.rng.choice([x for x in words if x[1] != mean])[1]
        b.judge("单词 \"%s\" 的意思是\"%s\"。" % (w, wrong), False,
                "%s 的意思是\"%s\"，不是\"%s\"。" % (w, mean, wrong), ["词汇理解"])


def w_fill(b):
    words = _word_pool(b.grade)
    w, mean, pos = b.rng.choice(words)
    masked = w[0] + "___" if len(w) >= 5 else w[0][0] + "___"
    b.fill("根据中文提示补全单词：%s  →  %s（写出完整单词）" % (mean, masked),
           w, "%s 的英文单词是 %s。" % (mean, w), ["单词拼写"])


def w_pos(b):
    words = _word_pool(b.grade)
    cands = [x for x in words if x[2] in ("n.", "v.", "adj.", "adv.")]
    w, mean, pos = b.rng.choice(cands)
    wrongs = [p for p in ("n.", "v.", "adj.", "adv.") if p != pos]
    b.choice("单词 \"%s\"（%s）的词性是？" % (w, mean), pos, wrongs,
             "%s 意为\"%s\"，词性为 %s。" % (w, mean, pos), ["词性判断"])


# ---- 语法题（按学段） ----
def g_be(b):
    subjects = [("I", "am"), ("he", "is"), ("she", "is"), ("it", "is"),
                ("we", "are"), ("you", "are"), ("they", "are")]
    s, right = b.rng.choice(subjects)
    wrongs = [x for x in ("am", "is", "are") if x != right]
    b.choice("___  %s  a student. 选择正确的 be 动词。" % s, right, wrongs,
             "主语 %s 搭配的 be 动词是 %s。" % (s, right), ["be动词"])


def g_plural(b):
    rules = [
        ("book", "books"), ("cat", "cats"), ("dog", "dogs"), ("pen", "pens"),
        ("bus", "buses"), ("box", "boxes"), ("watch", "watches"), ("dish", "dishes"),
        ("baby", "babies"), ("city", "cities"), ("boy", "boys"), ("key", "keys"),
        ("knife", "knives"), ("leaf", "leaves"), ("child", "children"),
        ("man", "men"), ("woman", "women"), ("foot", "feet"), ("tooth", "teeth"),
        ("mouse", "mice"), ("sheep", "sheep"), ("fish", "fish"),
    ]
    s, pl = b.rng.choice(rules)
    others = b.rng.sample([x[1] for x in rules if x[1] != pl], 3)
    b.choice("名词 \"%s\" 的复数形式是？" % s, pl, others,
             "%s 的复数是 %s。" % (s, pl), ["名词复数"])


def g_tense(b):
    bases = [("go", "went", "gone"), ("eat", "ate", "eaten"), ("see", "saw", "seen"),
             ("take", "took", "taken"), ("write", "wrote", "written"),
             ("speak", "spoke", "spoken"), ("get", "got", "gotten"),
             ("make", "made", "made"), ("do", "did", "done"), ("have", "had", "had")]
    base, past, pp = b.rng.choice(bases)
    b.choice("动词 \"%s\" 的过去式是？" % base, past,
             [pp, base, base + "ed"], "%s 的过去式是 %s。" % (base, past), ["动词过去式"])


def g_compare(b):
    pairs = [("good", "better"), ("bad", "worse"), ("many", "more"), ("much", "more"),
             ("little", "less"), ("far", "farther"), ("big", "bigger"),
             ("small", "smaller"), ("tall", "taller"), ("happy", "happier")]
    adj, comp = b.rng.choice(pairs)
    others = b.rng.sample([x[1] for x in pairs if x[1] != comp], 3)
    b.choice("形容词 \"%s\" 的比较级是？" % adj, comp, others,
             "%s 的比较级是 %s。" % (adj, comp), ["比较级"])


def g_article(b):
    words = [("apple", "an"), ("egg", "an"), ("orange", "an"), ("hour", "an"),
             ("book", "a"), ("cat", "a"), ("pen", "a"), ("university", "a"),
             ("useful book", "a"), ("honest boy", "an")]
    w, art = b.rng.choice(words)
    b.choice("___  %s 选择正确的冠词。" % w, art,
             ["a" if art == "an" else "an", "the", "/"],
             "%s 以%s音开头，用冠词 %s。" % (w, "元音" if art == "an" else "辅音", art),
             ["冠词用法"])


def g_relative(b):
    cases = [("The man ___ is speaking is my teacher.", "who"),
             ("The book ___ I bought is interesting.", "that"),
             ("This is the house ___ I lived last year.", "where"),
             ("I remember the day ___ we first met.", "when"),
             ("The girl ___ mother is a doctor is my friend.", "whose")]
    sent, right = b.rng.choice(cases)
    b.choice("选择正确关系词：%s" % sent, right,
             [x for x in ("who", "which", "whose", "where", "when", "that") if x != right][:3],
             "先行词与关系词对应关系，此处应填 %s。" % right, ["定语从句"], difficulty=3)


def g_virtual(b):
    cases = [("If I ___ you, I would accept the offer.", "were"),
             ("If he ___ here now, he would help us.", "were"),
             ("I wish I ___ more time.", "had"),
             ("If it ___ tomorrow, we would cancel the trip.", "rained")]
    sent, right = b.rng.choice(cases)
    b.choice("虚拟语气填空：%s" % sent, right,
             ["was" if right == "were" else "is", "are", "will be"],
             "与事实相反的假设用虚拟语气，此处填 %s。" % right, ["虚拟语气"], difficulty=4)


def g_passive(b):
    actives = [("They build bridges.", "Bridges are built by them."),
               ("People speak English worldwide.", "English is spoken worldwide."),
               ("He wrote a letter.", "A letter was written by him."),
               ("She cleans the room.", "The room is cleaned by her.")]
    act, pas = b.rng.choice(actives)
    b.choice("句子 \"%s\" 的被动语态是？" % act, pas,
             [act, pas.replace("is", "was").replace("are", "were"), "被动语态不适用"],
             "主动变被动：宾语提前作主语，动词变 be+过去分词。" , ["被动语态"], difficulty=3)


PRIMARY_G = [g_be, g_plural, g_article, g_compare]
JUNIOR_G = [g_be, g_plural, g_tense, g_compare, g_article, g_passive]
SENIOR_G = [g_tense, g_compare, g_relative, g_virtual, g_passive]


def generate(builder):
    g = builder.grade
    words = [w_en_cn, w_cn_en, w_judge, w_fill, w_pos]
    if g <= 6:
        grammars = PRIMARY_G
    elif g <= 9:
        grammars = JUNIOR_G
    else:
        grammars = SENIOR_G
    # 加权：选择/填空类题目多放，判断题偏少，保持题型均衡
    fns = [w_en_cn, w_en_cn, w_cn_en, w_cn_en, w_fill, w_fill, w_pos,
           w_judge] + grammars + grammars
    target = 1000
    stall = 0
    while len(builder.items) < target:
        before = len(builder.items)
        builder.rng.choice(fns)(builder)
        if len(builder.items) == before:
            stall += 1
            if stall > 60:
                # 兜底：循环词汇出题（换词保证不重复题干）
                word = builder.rng.choice(_word_pool(builder.grade))
                builder.judge("单词 \"%s\" 的意思是\"%s\"。" % (word[0], word[1]), True,
                              "%s 意为\"%s\"。" % (word[0], word[1]), ["词汇理解"])
        else:
            stall = 0
