#!/usr/bin/env python3
"""TiKu 仓库维护工具：生成索引/目录，并做基础校验。

用法：
    python tools/tiku.py build
    python tools/tiku.py validate
"""

import hashlib
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANKS = ROOT / "banks"
INDEX = ROOT / "index.json"
CATALOG = ROOT / "docs" / "CATALOG.md"

STAGE_ORDER = {"primary": 0, "junior_high": 1, "senior_high": 2, "university": 3}
SUBJECT_ORDER = {
    "math": 0, "chinese": 1, "english": 2, "science": 3, "physics": 4,
    "chemistry": 5, "biology": 6, "history": 7, "geography": 8, "politics": 9,
}
STAGE_CN = {"primary": "小学", "junior_high": "初中", "senior_high": "高中", "university": "大学"}
SUBJECT_CN = {
    "math": "数学", "chinese": "语文", "english": "英语", "science": "科学",
    "physics": "物理", "chemistry": "化学", "biology": "生物",
    "history": "历史", "geography": "地理", "politics": "政治",
}
QUESTION_TYPES = {
    "single_choice", "multiple_choice", "true_false", "fill_blank",
    "calculation", "solution", "reading", "cloze", "writing", "other",
}
META_REQUIRED = {"id", "title", "stage", "subject", "grades", "count", "tagged", "source", "license", "updatedAt"}


def read_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def bank_files():
    """递归扫描所有来源集目录下的题库包，兼容一层与两层目录结构。"""
    return sorted(
        p for p in BANKS.glob("**/*.json")
        if p.name != "collection.json"
    )


def find_collection(path):
    """向上查找题库包所属的 collection.json（可能在上一级或上上级目录）。"""
    for parent in [path.parent] + list(path.parent.parents):
        cand = parent / "collection.json"
        if cand.exists():
            return cand
    return path.parent / "collection.json"


def load_banks():
    banks = []
    for path in bank_files():
        raw = path.read_bytes()
        data = json.loads(raw.decode("utf-8"))
        collection_path = find_collection(path)
        collection_id = collection_path.parent.name
        collection = read_json(collection_path)
        banks.append({
            "path": path,
            "data": data,
            "collection": collection_id,
            "collection_data": collection,
            "size": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "rel": path.relative_to(ROOT).as_posix(),
        })
    return banks


def check_bank(item):
    errors = []
    data, path = item["data"], item["path"]
    if data.get("format") != "wrong-notebook-question-bank":
        errors.append(f"{path.name}: format 不正确")
    if data.get("version") != 1:
        errors.append(f"{path.name}: version 必须为 1")
    meta = data.get("meta", {})
    missing = META_REQUIRED - set(meta)
    if missing:
        errors.append(f"{path.name}: meta 缺少 {sorted(missing)}")
    questions = data.get("questions", [])
    if not isinstance(questions, list) or not questions:
        errors.append(f"{path.name}: questions 不能为空")
        return errors
    if meta.get("count") != len(questions):
        errors.append(f"{path.name}: count={meta.get('count')} 与题数 {len(questions)} 不一致")
    if meta.get("id") != path.stem:
        errors.append(f"{path.name}: meta.id 与文件名不一致")
    if not meta.get("id", "").startswith(item["collection"] + "-"):
        errors.append(f"{path.name}: meta.id 未以来源集 id 开头")
    if meta.get("license") != item["collection_data"].get("license"):
        errors.append(f"{path.name}: 许可与 collection.json 不一致")
    ids = set()
    for q in questions:
        qid = q.get("id", "")
        if not qid:
            errors.append(f"{path.name}: 存在空 id")
        if qid in ids:
            errors.append(f"{path.name}: 重复 id {qid}")
        ids.add(qid)
        if q.get("questionType") not in QUESTION_TYPES:
            errors.append(f"{path.name}/{qid}: questionType 非法")
        if not q.get("text"):
            errors.append(f"{path.name}/{qid}: text 为空")
        opts = q.get("options")
        if opts:
            if len(opts) < 2:
                errors.append(f"{path.name}/{qid}: 选项少于两个")
            answer = str(q.get("answer") or "").replace(",", "").replace(" ", "")
            if q.get("questionType") == "single_choice" and answer and answer not in opts:
                errors.append(f"{path.name}/{qid}: 答案 {answer} 不在选项中")
    if item["size"] > 5 * 1024 * 1024:
        errors.append(f"{path.name}: 文件超过 5 MB")
    return errors


def build_index(banks):
    packages = []
    for item in banks:
        meta = dict(item["data"]["meta"])
        meta["collection"] = item["collection"]
        meta["file"] = item["rel"]
        meta["sizeBytes"] = item["size"]
        meta["sha256"] = item["sha256"]
        packages.append(meta)
    packages.sort(key=lambda p: (
        STAGE_ORDER.get(p.get("stage"), 99),
        SUBJECT_ORDER.get(p.get("subject"), 99),
        p.get("id", ""),
    ))
    return {
        "format": "wrong-notebook-question-bank-index",
        "version": 1,
        "updatedAt": date.today().isoformat(),
        "packages": packages,
    }


def write_index(index):
    INDEX.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_catalog(index):
    lines = [
        "# TiKu 题库目录",
        "",
        "> 本文件由 `python tools/tiku.py build` 生成，请勿手工修改。",
        "",
    ]
    pkgs = index["packages"]
    total_q = sum(p["count"] for p in pkgs)
    collections = {}
    for p in pkgs:
        collections.setdefault(p["collection"], {"count": 0, "questions": 0})
        collections[p["collection"]]["count"] += 1
        collections[p["collection"]]["questions"] += p["count"]
    lines.append(f"共 {len(collections)} 个来源集、{len(pkgs)} 个题库包、{total_q} 道题。")
    lines += ["", "## 来源集", "", "| 来源集 | 包数 | 题数 |", "|---|---:|---:|"]
    for cid, info in sorted(collections.items()):
        lines.append(f"| `{cid}` | {info['count']} | {info['questions']} |")
    for stage in ["primary", "junior_high", "senior_high", "university"]:
        group = [p for p in pkgs if p.get("stage") == stage]
        if not group:
            continue
        stage_total = sum(p["count"] for p in group)
        lines += ["", f"## {STAGE_CN.get(stage, stage)}（{stage_total} 题）", "",
                  "| 学科 | 题库包 | 名称 | 题数 | 年级 | 知识点 | 大小 |",
                  "|---|---|---|---:|---|---|---:|"]
        for p in group:
            grades = p.get("grades") or []
            grade_text = "逐题标注" if not grades else "、".join(str(g) for g in grades)
            tagged = "有" if p.get("tagged") else "无"
            size_kb = round(p["sizeBytes"] / 1024)
            lines.append(
                f"| {SUBJECT_CN.get(p.get('subject'), p.get('subject', ''))} "
                f"| [`{p['id']}`](../{p['file']}) "
                f"| {p['title']} | {p['count']} | {grade_text} | {tagged} | {size_kb} KB |"
            )
    CATALOG.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cmd_build():
    banks = load_banks()
    if not banks:
        print("没有找到题库包")
        return 1
    errors = []
    for item in banks:
        errors.extend(check_bank(item))
    if errors:
        print("校验失败，未生成索引：")
        for e in errors:
            print(" -", e)
        return 1
    index = build_index(banks)
    write_index(index)
    write_catalog(index)
    print(f"已生成 index.json 与 docs/CATALOG.md，共 {len(index['packages'])} 个包、"
          f"{sum(p['count'] for p in index['packages'])} 道题")
    return 0


def cmd_validate():
    banks = load_banks()
    errors = []
    for item in banks:
        errors.extend(check_bank(item))
    if not INDEX.exists():
        errors.append("缺少 index.json，请先运行 build")
    else:
        generated = build_index(banks)
        current = read_json(INDEX)
        if current.get("packages") != generated["packages"]:
            errors.append("index.json 与题库包不一致，请重新运行 build")
    if errors:
        print("校验失败：")
        for e in errors:
            print(" -", e)
        return 1
    print(f"校验通过：{len(banks)} 个包，"
          f"{sum(len(i['data']['questions']) for i in banks)} 道题")
    return 0


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in {"build", "validate"}:
        print(__doc__)
        return 2
    return cmd_build() if sys.argv[1] == "build" else cmd_validate()


if __name__ == "__main__":
    sys.exit(main())
