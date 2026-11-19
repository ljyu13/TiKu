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

题库按来源集分目录，一个包只放一个学段、一个学科。当前来源集 `ljyu-original` 下有 3 个样例包：

- `ljyu-original-primary-math`：小学数学，二至六年级
- `ljyu-original-junior-high-physics`：初中物理，八至九年级
- `ljyu-original-senior-high-chemistry`：高中化学，十至十二年级

每包 10 道题，覆盖单选、判断、填空、计算、解答等题型，带答案、解析、知识点和难度标记。题量不大，主要是把结构跑通；后续按同样格式往包里加题即可。

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
│       └── <包id>.json         题库包
└── tools/
    └── tiku.py                 生成索引、校验数据
```

## 本地维护

需要 Python 3.9 或以上，不需要第三方依赖。

```bash
python tools/tiku.py build      # 根据 banks/ 重新生成 index.json 和 docs/CATALOG.md
python tools/tiku.py validate   # 校验字段、题数、id、答案与选项等
```

修改题库包后记得先 `build` 再提交，否则小程序读到的索引还是旧的。

## 许可

- 工具与文档：MIT，见 [`LICENSE`](LICENSE)。
- 题库数据：CC BY-NC 4.0，见各来源集的 `collection.json`。个人学习使用，商用请另行确认。
