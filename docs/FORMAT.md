# TiKu 数据格式说明

本项目使用与「刷题宝」小程序兼容的题库包格式。小程序读取根目录 `index.json`，再按每个条目的 `file` 字段下载对应题库包。

## 文件分层

```
banks/<来源集>/collection.json   来源集声明：作者、来源、许可、维护者
banks/<来源集>/<包id>.json       题库包：一个学段、一个学科的题目集合
index.json                       索引，由 tools/tiku.py build 生成
docs/CATALOG.md                  人类可读目录，由 build 一并生成
```

`index.json` 和 `docs/CATALOG.md` 不要手工改。新增或修改题库包之后运行：

```bash
python tools/tiku.py build
python tools/tiku.py validate
```

## 来源集 collection.json

必填字段：

| 字段 | 含义 |
|---|---|
| `id` | 小写字母、数字、连字符，与目录名一致 |
| `title` | 展示名称 |
| `origin` | `original` 表示自编，`third_party` 表示整理自公开数据 |
| `source` | 来源名称 |
| `license` | 数据许可，例如 `CC-BY-NC-4.0` |
| `maintainers` | 至少一个 GitHub 用户名 |

`third_party` 还必须写 `sourceUrl`。本项目当前来源集是 `ljyu-original`，全部题目由 ljyu13 原创编写。

## 题库包

文件是无 BOM 的 UTF-8 JSON。排版约定为：第一行是 `format`/`version`，第二行是 `meta`，之后 `questions` 数组里每题一行。这样便于逐题查看改动。

顶层结构：

```json
{"format":"wrong-notebook-question-bank","version":1,
"meta":{"id":"ljyu-original-primary-math","title":"ljyu13 原创小学数学","stage":"primary","subject":"math","grades":[],"count":10,"tagged":true,"source":"ljyu13 原创编写","license":"CC-BY-NC-4.0","updatedAt":"2026-11-19"},
"questions":[
{"id":"ljyu-pm-01","grade":2,"questionType":"single_choice","text":"题干","options":{"A":"选项一"},"answer":"A"}
]}
```

### meta 字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 是 | 包 id，与文件名一致，且以来源集 id 开头 |
| `title` | 是 | 小程序里显示的题库名称 |
| `stage` | 是 | `primary` / `junior_high` / `senior_high` / `university` |
| `subject` | 是 | `math` / `chinese` / `english` / `science` / `physics` / `chemistry` / `biology` / `history` / `geography` / `politics` |
| `grades` | 是 | 包内年级数组；**若希望每题使用各自的 `grade`，请留空数组** |
| `count` | 是 | 必须等于 `questions.length` |
| `tagged` | 是 | 是否带知识点 |
| `source` | 是 | 来源名称 |
| `license` | 是 | 必须与所属 `collection.json` 一致 |
| `updatedAt` | 是 | `YYYY-MM-DD` |

> 刷题宝小程序的解析逻辑会优先取 `grades[0]` 作为题目年级。为了让同一包里不同年级的题目保持各自年级，本项目统一把 `grades` 写成 `[]`，并在每道题上写 `grade`。

### 题目字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | 是 | 包内唯一且稳定，发布后尽量不要改 |
| `text` | 是 | 题干，支持普通文本与 Markdown |
| `questionType` | 是 | 见下方题型表 |
| `options` | 否 | 选项对象，键为 `A`、`B`、`C` 等；选择题必须拆出选项 |
| `answer` | 否 | 答案；选择题写选项字母 |
| `analysis` | 否 | 答案解析 |
| `knowledgePoints` | 否 | 知识点名称数组 |
| `grade` | 否 | 1–6 小学，7–9 初中，10–12 高中 |
| `semester` | 否 | `上` / `下` / `全` |
| `difficultyStars` | 否 | 1–5 星 |
| `source` | 否 | 题目标注的出处 |
| `material` / `figureSvg` | 否 | 共用材料、内嵌 SVG 图形 |

题型取值：`single_choice`、`multiple_choice`、`true_false`、`fill_blank`、`calculation`、`solution`、`reading`、`cloze`、`writing`、`other`。

小程序把带 `options` 的题当选择题，其余当填空题；判断题与填空题都按文本作答处理，因此判断题答案写「正确」或「错误」即可。

## 索引 index.json

由脚本生成，顶层固定为：

```json
{"format":"wrong-notebook-question-bank-index","version":1,"updatedAt":"2026-11-19","packages":[]}
```

每个 `packages[]` 条目包含题库包 `meta` 的全部字段，外加：

| 字段 | 含义 |
|---|---|
| `collection` | 所属来源集 id |
| `file` | 相对仓库根目录的包路径，例如 `banks/ljyu-original/ljyu-original-primary-math.json` |
| `sizeBytes` | 文件字节数 |
| `sha256` | 文件内容校验值 |

## 新增题目的流程

1. 在对应来源集目录下编辑或新增题库包，保持 `meta.count` 与题数一致。
2. 运行 `python tools/tiku.py build` 更新索引和目录。
3. 运行 `python tools/tiku.py validate` 确认没有重复 id、答案越界等问题。
4. 提交后，小程序里选择「自定义题库」，输入 `ljyu13/TiKu` 即可拉取。
