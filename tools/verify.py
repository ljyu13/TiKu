#!/usr/bin/env python3
"""题库包深度校验：题数、id/题干唯一、答案合法、解析齐全、年级正确。
比 tiku.py 的基础校验更严格，用于大规模生成后的质量把关。
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANKS = ROOT / "banks" / "ljyu-original"
TYPES = {"single_choice", "multiple_choice", "true_false", "fill_blank",
         "calculation", "solution", "reading", "cloze", "writing", "other"}

# 学段->年级范围
STAGE_RANGE = {"primary": (1, 6), "junior_high": (7, 9), "senior_high": (10, 12)}


def check(path):
    errs = []
    data = json.loads(path.read_text(encoding="utf-8"))
    meta = data["meta"]
    qs = data["questions"]
    stage = meta["stage"]
    grades = meta.get("grades", [])
    if len(qs) != 1000:
        errs.append("题数=%d（应为1000）" % len(qs))
    if meta.get("count") != len(qs):
        errs.append("count不符")
    grade_ok = grades[0] == 0 or grades[0] in range(*(lambda r: (r[0], r[1] + 1))(STAGE_RANGE[stage]))
    if len(grades) != 1 or not grade_ok:
        errs.append("grades=%s 不符学段" % grades)
    gid = grades[0] if grades else None
    ids, texts = set(), set()
    types = Counter()
    empty_analysis = 0
    for q in qs:
        qid = q.get("id", "")
        if qid in ids:
            errs.append("重复id %s" % qid)
        ids.add(qid)
        txt = " ".join(q.get("text", "").split())
        if txt in texts:
            errs.append("重复题干 %s" % txt[:30])
        texts.add(txt)
        t = q.get("questionType")
        types[t] += 1
        if t not in TYPES:
            errs.append("非法题型 %s" % t)
        if not q.get("text"):
            errs.append("%s 无题干" % qid)
        # 题型告知：必须有中文题型名，且题干带【题型】前缀
        tn = q.get("questionTypeName")
        if not tn:
            errs.append("%s 缺 questionTypeName" % qid)
        elif not q["text"].startswith("【%s】" % tn):
            errs.append("%s 题干缺题型前缀【%s】" % (qid, tn))
        if not q.get("answer"):
            errs.append("%s 无答案" % qid)
        if not q.get("analysis"):
            empty_analysis += 1
        # 防回归：题干不得把答案词摆在题干（原反向选择题）
        if "是下列哪一项的描述" in txt or "是下列哪一项的表述" in txt:
            errs.append("%s 残留反向选择题" % qid)
        # 防回归：解析不得是"随机错误词替换"式判断（原题干塞乱词）
        if "表述错误；正确的是" in q.get("analysis", ""):
            errs.append("%s 残留乱词判断题" % qid)
        # 填空题题干应含留空符 ___
        if t == "fill_blank":
            body = q["text"][len("【%s】" % tn):] if tn else q["text"]
            if "___" not in body:
                errs.append("%s 填空题题干无留空符" % qid)
        if q.get("grade") != gid:
            errs.append("%s 年级=%s 应为%s" % (qid, q.get("grade"), gid))
        opts = q.get("options")
        ans = str(q.get("answer", "")).replace(",", "").replace(" ", "")
        if t == "single_choice":
            # 选择题：必须恰好 ABCD 四个选项，答案为其中一项
            if not opts or set(opts.keys()) != {"A", "B", "C", "D"}:
                errs.append("%s 选择题选项不是ABCD" % qid)
            elif ans not in opts:
                errs.append("%s 答案%s不在选项" % (qid, ans))
        elif t == "true_false":
            # 判断题：必须恰好两个选项 A=正确、B=错误，答案为 A 或 B
            if opts != {"A": "正确", "B": "错误"}:
                errs.append("%s 判断题选项应为A正确B错误" % qid)
            if ans not in ("A", "B"):
                errs.append("%s 判断题答案非A/B: %s" % (qid, ans))
        elif t == "multiple_choice":
            if not opts:
                errs.append("%s 多选题无选项" % qid)
            else:
                for ch in ans:
                    if ch not in opts:
                        errs.append("%s 多选答案%s越界" % (qid, ans))
        else:
            # 填空/计算/解答等：走输入框，不应有选项
            if opts:
                errs.append("%s 非选择题不应有选项" % qid)
    if empty_analysis:
        errs.append("%d题缺解析" % empty_analysis)
    return errs, types


def main():
    files = sorted(f for f in BANKS.glob("**/*.json") if f.name != "collection.json")
    if len(sys.argv) > 1:
        files = [f for f in files if sys.argv[1] in f.name]
    if not files:
        print("没有找到题库包")
        return 1
    total_err = 0
    grand_q = 0
    all_types = Counter()
    for f in files:
        errs, types = check(f)
        grand_q += 1000
        all_types.update(types)
        if errs:
            total_err += len(errs)
            print("FAIL %-55s %s" % (f.name, "; ".join(errs[:5])))
        else:
            print("PASS %-55s 题型:%s" % (f.name, dict(types)))
    print("=" * 70)
    print("包数=%d 总题数=%d 错误数=%d" % (len(files), grand_q, total_err))
    print("全局题型分布:", dict(all_types))
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main())
