#!/usr/bin/env python3
"""题目生成引擎核心：题目构造、去重、校验。

设计原则：
- 所有题目由参数化模板 + 素材表生成，答案由程序计算或素材确定，保证正确。
- 每题带解析、知识点、难度、年级、来源，题干去重。
- 依赖确定性随机（seed + 年级 + 学科），可复现。
"""

import hashlib
import random

TODAY = "2026-11-19"
SOURCE = "ljyu13 原创编写"
LETTERS = "ABCD"

# 题型中文名：既写入 questionTypeName 字段，也作为题干前缀明确告知用户
TYPE_NAMES = {
    "single_choice": "单选题",
    "multiple_choice": "多选题",
    "true_false": "判断题",
    "fill_blank": "填空题",
    "calculation": "计算题",
    "solution": "解答题",
    "reading": "阅读题",
    "cloze": "完形填空",
    "writing": "写作题",
    "other": "其他题",
}

# 判断题固定两个选项：A=正确，B=错误
JUDGE_OPTIONS = {"A": "正确", "B": "错误"}


def new_rng(*parts):
    """按任意字符串种子构造确定性随机源。"""
    seed = hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()
    return random.Random(int(seed[:16], 16))


class Builder:
    """单个题库包的构造器：负责去重、分配 id、统计。"""

    def __init__(self, prefix, grade, stage, subject, rng):
        self.prefix = prefix
        self.grade = grade
        self.stage = stage
        self.subject = subject
        self.rng = rng
        self.items = []
        self._texts = set()
        self._n = 0

    def add(self, text, qtype, answer, analysis, kps,
            options=None, difficulty=2, semester=None, material=None):
        """添加一道题；题干重复则返回 False。题干自动加题型前缀，明确告知题型。"""
        type_name = TYPE_NAMES.get(qtype, "")
        text = "【%s】%s" % (type_name, text) if type_name else str(text)
        key = " ".join(str(text).split())
        if not key or key in self._texts:
            return False
        self._texts.add(key)
        self._n += 1
        item = {
            "id": "%s-%04d" % (self.prefix, self._n),
            "grade": self.grade,
            "questionType": qtype,
            "questionTypeName": type_name,
            "text": text,
        }
        if semester:
            item["semester"] = semester
        item["answer"] = answer
        item["analysis"] = analysis
        item["knowledgePoints"] = list(dict.fromkeys(kps)) if kps else []
        item["difficultyStars"] = difficulty
        item["source"] = SOURCE
        if options:
            item["options"] = options
        if material:
            item["material"] = material
        self.items.append(item)
        return True

    def choice(self, text, correct, wrongs, analysis, kps, difficulty=2,
               semester=None, shuffle=True):
        """生成单选题：正确答案 + 从干扰项池取 3 个，打乱后返回选项字典与字母。"""
        wrongs = [w for w in wrongs if w != correct]
        seen = {correct}
        picked = []
        for w in wrongs:
            if w not in seen:
                seen.add(w)
                picked.append(w)
            if len(picked) == 3:
                break
        # 干扰项不足时用占位补齐（正常素材均 >=3）
        while len(picked) < 3:
            filler = "以上都不对"
            if filler not in seen:
                seen.add(filler)
                picked.append(filler)
            else:
                picked.append("都不正确%d" % len(picked))
        opts_vals = [correct] + picked
        if shuffle:
            self.rng.shuffle(opts_vals)
        letter = LETTERS[opts_vals.index(correct)]
        options = {LETTERS[i]: opts_vals[i] for i in range(4)}
        full_analysis = "%s正确答案为 %s：%s。" % (analysis, letter, correct)
        return self.add(text, "single_choice", letter, full_analysis, kps,
                        options=options, difficulty=difficulty, semester=semester)

    def multi(self, text, corrects, wrongs, analysis, kps, difficulty=3):
        """多选题：答案为按字母升序的逗号串。"""
        pool = list(corrects) + list(wrongs)
        seen = set()
        uniq = []
        for x in pool:
            if x not in seen:
                seen.add(x)
                uniq.append(x)
        self.rng.shuffle(uniq)
        options = {LETTERS[i]: uniq[i] for i in range(min(4, len(uniq)))}
        ans = ",".join(sorted(k for k, v in options.items() if v in corrects))
        full_analysis = "%s正确选项为 %s。" % (analysis, ans)
        return self.add(text, "multiple_choice", ans, full_analysis, kps,
                        options=options, difficulty=difficulty)

    def judge(self, text, answer_bool, analysis, kps, difficulty=2):
        # 判断题作答方式：选项 A=正确、B=错误；answer 用字母，小程序点击选项即可判定
        letter = "A" if answer_bool else "B"
        word = "正确" if answer_bool else "错误"
        full = "%s本题表述%s，应选 %s（%s）。" % (analysis, word, letter, word)
        return self.add(text, "true_false", letter, full, kps,
                        options=dict(JUDGE_OPTIONS), difficulty=difficulty)

    def fill(self, text, answer, analysis, kps, difficulty=2):
        return self.add(text, "fill_blank", str(answer), analysis, kps,
                        difficulty=difficulty)

    def calc(self, text, answer, analysis, kps, difficulty=3):
        return self.add(text, "calculation", str(answer), analysis, kps,
                        difficulty=difficulty)

    def solve(self, text, answer, analysis, kps, difficulty=4):
        return self.add(text, "solution", str(answer), analysis, kps,
                        difficulty=difficulty)


def fmt_num(x):
    """数字格式化：整数去 .0，保留最多 4 位小数。"""
    if isinstance(x, int):
        return str(x)
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return ("%.4f" % x).rstrip("0").rstrip(".")


def pick_distractors(rng, value, kind="int", span=10, count=3):
    """围绕 value 生成数值型干扰项。"""
    out = []
    tries = 0
    while len(out) < count and tries < 60:
        tries += 1
        if kind == "int":
            d = value + rng.choice([-1, 1]) * rng.randint(1, span)
            if d < 0:
                d = value + rng.randint(1, span)
            v = fmt_num(d)
        elif kind == "decimal":
            d = round(value + rng.uniform(-span, span), 2)
            if d < 0:
                d = round(abs(value) + rng.uniform(0.1, span), 2)
            v = fmt_num(d)
        else:
            v = str(value)
        if v != fmt_num(value) and v not in out:
            out.append(v)
    while len(out) < count:
        out.append(fmt_num(value) + "+" + str(len(out)))
    return out
