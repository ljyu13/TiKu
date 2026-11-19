# TiKu

我自己的题库仓库，给「刷题宝」微信小程序直接拉取使用。题库格式与 `wrong-notebook-question-bank` 的读取接口兼容，但题目、答案、解析、说明和配套脚本都是本仓库独立编写的原创内容。

## 小程序怎么用

1. 打开小程序，进入「设置」。
2. 选择题库源选「自定义题库」。
3. 输入 `ljyu13/TiKu`，页面会显示自动识别出的 `index.json` 地址。
4. 点「拉取选中的题库」。小程序会自动试 `main` / `master` 分支，并按索引里的 `file` 逐个下载题库包。
5. 回到首页，按学段、年级、学科筛选后开始刷题。

如果拉取失败，优先在设置里切换下载代理；数据格式错误和域名校验失败换代理无效，按页面提示处理。

## 当前内容

题库按「来源集 → 学段 → 学科 → 年级」四级组织，**每个年级每个学科一个包，每包 1000 题**。当前来源集 `ljyu-original` 覆盖 20 个学科、72 个包、共 **72000 道原创题**：

- **小学**（4 科 × 6 年级 = 24 包，24000 题）：语文、数学、英语、科学
- **初中**（8 科 × 3 年级 = 24 包，24000 题）：语文、数学、英语、物理、化学、生物、历史、地理
- **高中**（8 科 × 3 年级 = 24 包，24000 题）：语文、数学、英语、物理、化学、生物、历史、地理

题型覆盖单选、判断、填空、计算，每题带答案、解析、知识点、难度和年级标记。数学与理科计算题的答案由程序精确计算，文科题答案由原创素材表确定；生成后经 `tools/verify.py` 逐包校验题数、唯一性、答案合法性与解析完整性。参考了主流试卷的常见题型（选择/判断/填空/计算）来设计模板。

目录和题数见 [`docs/CATALOG.md`](docs/CATALOG.md)，字段规则见 [`docs/FORMAT.md`](docs/FORMAT.md)。

## 仓库结构

```
TiKu/
├── index.json                  小程序读取的索引（生成）
├── docs/
│   ├── CATALOG.md              题库目录（生成）
│   └── FORMAT.md               数据格式与维护说明
├── schema/                     JSON Schema
├── banks/
│   └── ljyu-original/
│       ├── collection.json     来源集声明
│       ├── primary/            小学 24 包（g1-g6 × 4 科）
│       ├── junior-high/        初中 24 包（g7-g9 × 8 科）
│       └── senior-high/        高中 24 包（g10-g12 × 8 科）
└── tools/
    ├── tiku.py                 生成索引、基础校验
    ├── verify.py               深度校验（题数/唯一/答案/解析）
    ├── generate_all.py         批量生成全部 72 包
    ├── gen_banks.py            早期小批量题目数据源（保留）
    └── qgen/                   题目生成引擎
        ├── core.py             构造、去重、选项生成
        ├── math_gen.py         数学
        ├── chinese_gen.py      语文
        ├── english_gen.py      英语
        ├── science_gen.py      科学/物理/化学/生物
        └── humanities_gen.py   历史/地理
```

## 本地维护

需要 Python 3.9 或以上，不需要第三方依赖。

```bash
python tools/generate_all.py            # 重新生成全部 72 个题库包
python tools/generate_all.py "math-g5"  # 只生成匹配关键字的包（分批用）
python tools/verify.py                  # 深度校验全部包
python tools/tiku.py build              # 重新生成 index.json 和 docs/CATALOG.md
python tools/tiku.py validate           # 索引与题库包一致性校验
```

题目由 `tools/qgen/` 下的参数化模板引擎生成：改题目模板或素材表后，先跑 `generate_all.py` 重建包，再跑 `verify.py` 校验，最后跑 `tiku.py build` 更新索引。也可以直接编辑 `banks/` 下的 JSON 包，但要保证 `meta.count` 与题数一致；改完记得先 `build` 再提交，否则小程序读到的索引还是旧的。

## 许可

- 工具与文档：MIT，见 [`LICENSE`](LICENSE)。
- 题库数据：CC BY-NC 4.0，见各来源集的 `collection.json`。个人学习使用，商用请另行确认。
