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

题库按「来源集 → 学段 → 学科」三级组织，一个包只放一个学段、一个学科。当前来源集 `ljyu-original` 覆盖 20 个学科、共 132 道原创题：

- **小学**（4 科）：语文、数学、英语、科学
- **初中**（8 科）：语文、数学、英语、物理、化学、生物、历史、地理
- **高中**（8 科）：语文、数学、英语、物理、化学、生物、历史、地理

题型覆盖单选、判断、填空、计算、解答，每题带答案、解析、知识点和难度标记。题量还在积累阶段，后续按同样格式往包里加题即可。

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
│       ├── primary/            小学：语文、数学、英语、科学
│       ├── junior-high/        初中：语数英物化生史地
│       └── senior-high/        高中：语数英物化生史地
└── tools/
    ├── tiku.py                 生成索引、校验数据
    └── gen_banks.py            从集中定义的题目数据重建所有题库包
```

## 本地维护

需要 Python 3.9 或以上，不需要第三方依赖。

```bash
python tools/gen_banks.py       # 从题目数据源重建全部题库包（一般改题时用）
python tools/tiku.py build      # 根据 banks/ 重新生成 index.json 和 docs/CATALOG.md
python tools/tiku.py validate   # 校验字段、题数、id、答案与选项等
```

题目数据集中在 `tools/gen_banks.py` 的 `PRIMARY` / `JUNIOR` / `SENIOR` 三个字典里，改题后先跑 `gen_banks.py` 再跑 `build`。也可以直接编辑 `banks/` 下的 JSON 包，但要保证 `meta.count` 与题数一致；改完记得先 `build` 再提交，否则小程序读到的索引还是旧的。

## 许可

- 工具与文档：MIT，见 [`LICENSE`](LICENSE)。
- 题库数据：CC BY-NC 4.0，见各来源集的 `collection.json`。个人学习使用，商用请另行确认。
