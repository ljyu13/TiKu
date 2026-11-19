#!/usr/bin/env python3
"""生成 TiKu 全部题库包：按学段/学科/年级拆包，每包 1000 题。

- 小学：语文、数学、英语、科学（1-6 年级）
- 初中：语文、数学、英语、物理、化学、生物、历史、地理（7-9 年级）
- 高中：语文、数学、英语、物理、化学、生物、历史、地理（10-12 年级）

共 20 个学科组合，72 个包，每包 1000 题。
用法：python tools/generate_all.py [包id关键字]  # 可选，只生成匹配年级的包，用于分批
"""
import json
import sys
from pathlib import Path

from qgen.core import new_rng, Builder, TODAY
from qgen import math_gen, english_gen, chinese_gen, science_gen, humanities_gen

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "banks" / "ljyu-original"
DIRS = {"primary": "primary", "junior_high": "junior-high", "senior_high": "senior-high"}
CODE = {"primary": "p", "junior_high": "jh", "senior_high": "sh"}
SUBCODE = {"chinese": "cn", "math": "ma", "english": "en", "science": "sc",
           "physics": "ph", "chemistry": "ch", "biology": "bi",
           "history": "hi", "geography": "ge"}
SUBJECT_CN = {"chinese": "语文", "math": "数学", "english": "英语", "science": "科学",
              "physics": "物理", "chemistry": "化学", "biology": "生物",
              "history": "历史", "geography": "地理"}
STAGE_CN = {"primary": "小学", "junior_high": "初中", "senior_high": "高中"}

# (stage, subject) -> (grades, generator)
PLAN = []
for g in range(1, 7):
    for s in ["chinese", "math", "english", "science"]:
        PLAN.append(("primary", s, g))
for g in range(7, 10):
    for s in ["chinese", "math", "english", "physics", "chemistry", "biology", "history", "geography"]:
        PLAN.append(("junior_high", s, g))
for g in range(10, 13):
    for s in ["chinese", "math", "english", "physics", "chemistry", "biology", "history", "geography"]:
        PLAN.append(("senior_high", s, g))


def gen_for(stage, subject, grade, builder):
    if subject == "math":
        math_gen.generate(builder)
    elif subject == "english":
        english_gen.generate(builder)
    elif subject == "chinese":
        chinese_gen.generate(builder)
    elif subject == "physics":
        science_gen.generate_physics(builder)
    elif subject == "chemistry":
        science_gen.generate_chemistry(builder)
    elif subject == "biology":
        science_gen.generate_biology(builder)
    elif subject == "science":
        science_gen.generate_science(builder)
    elif subject == "history":
        humanities_gen.generate_history(builder)
    elif subject == "geography":
        humanities_gen.generate_geography(builder)
    else:
        raise ValueError("unknown subject " + subject)


def make_one(stage, subject, grade, filter_kw=None):
    pid = "ljyu-original-%s-%s-g%d" % (DIRS[stage], subject, grade)
    if filter_kw and filter_kw not in pid:
        return None
    prefix = "ljyu-%s-%s-g%d" % (CODE[stage], SUBCODE[subject], grade)
    rng = new_rng(stage, subject, grade, "v1")
    builder = Builder(prefix, grade, stage, subject, rng)
    gen_for(stage, subject, grade, builder)
    bank = {
        "format": "wrong-notebook-question-bank",
        "version": 1,
        "meta": {
            "id": pid,
            "title": "ljyu13 原创%s%s（%d年级）" % (STAGE_CN[stage], SUBJECT_CN[subject], grade),
            "stage": stage,
            "subject": subject,
            "grades": [grade],
            "count": len(builder.items),
            "tagged": True,
            "source": "ljyu13 原创编写",
            "license": "CC-BY-NC-4.0",
            "updatedAt": TODAY,
        },
        "questions": builder.items,
    }
    folder = BASE / DIRS[stage]
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / (pid + ".json")
    path.write_text(json.dumps(bank, ensure_ascii=False, separators=(",", ":")) + "\n",
                    encoding="utf-8")
    return path, len(builder.items)


def main():
    kw = sys.argv[1] if len(sys.argv) > 1 else None
    ok = 0
    total_q = 0
    for stage, subject, grade in PLAN:
        result = make_one(stage, subject, grade, kw)
        if result:
            path, n = result
            ok += 1
            total_q += n
            print("OK %-55s %4d 题  %6d KB" %
                  (path.name, n, path.stat().st_size // 1024))
    print("完成：%d 个包，%d 道题" % (ok, total_q))


if __name__ == "__main__":
    main()
