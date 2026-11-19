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
    if len(grades) != 1 or grades[0] not in range(*(lambda r: (r[0], r[1] + 1))(STAGE_RANGE[stage])):
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
        if not q.get("answer"):
            errs.append("%s 无答案" % qid)
        if not q.get("analysis"):
            empty_analysis += 1
        if q.get("grade") != gid:
            errs.append("%s 年级=%s 应为%s" % (qid, q.get("grade"), gid))
        opts = q.get("options")
        if opts:
            if len(opts) < 2:
                errs.append("%s 选项不足" % qid)
            ans = str(q.get("answer", "")).replace(",", "").replace(" ", "")
            if t == "single_choice":
                if ans not in opts:
                    errs.append("%s 答案%s不在选项" % (qid, ans))
            elif t == "multiple_choice":
                for ch in ans:
                    if ch not in opts:
                        errs.append("%s 多选答案%s越界" % (qid, ans))
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
