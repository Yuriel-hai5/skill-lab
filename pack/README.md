<!-- ============================================================
     🤖 如果你是 AI agent，被用户丢了这个仓库的链接、或拖了这个包进来：
     先读 AGENTS.md，那是给你的安装任务书。
     （给链接时它在仓库的 pack/ 目录下；给压缩包时它在包根。）
     本文件是给人看的说明。
     ============================================================ -->

# workflow-recipes 技能包 · 安装说明

自建 skill 合集：**不用记 skill 名字，说清处境，AI 自己给流程。**

---

> ## 懒人装法：把**链接**（或压缩包）丢给 WorkBuddy 对话框
>
> **方式一 · 给链接**（推荐）：把仓库地址贴进对话框，说 **「帮我装上」**。
>
> **方式二 · 给压缩包**：把 zip 拖进对话框，说 **「帮我装上」**。
>
> 两种都行。任务书 **`AGENTS.md`** 是专为这个场景写的，里面含
> 目录探测、拿到文件、冲突检查、复制、生成索引的完整流程。
>
> **想更稳就说全一点**：**「按 AGENTS.md 帮我装上」**。
> 只说"帮我装上"也能成，但 agent 有可能把"装上"理解成"解压到工作区"或"读一遍总结"，
> 加了这句指向，基本不会跑偏。
>
> ⚠️ **装完必须新开一个对话**才会生效——这一步 agent 替你做不了。
>
> 想自己动手 → 看下面第二节。

---

| Skill | 作用 | 触发方式 |
|---|---|---|
| `workflow-recipes` | 覆盖项目全生命周期的场景配方库。你说「我卡在 XX 阶段了」，它给出**用哪些 skill + 什么顺序 + 每步产出什么** | 自动（描述匹配就触发），也可 `/workflow-recipes` |
| `ui-upgrade` | 已有界面的视觉质感 + 动效升级配方（界面能跑、结构不动） | 自动（说「界面看起来廉价 / 加动效 / 高级感」就触发） |
| `skill-pack-sharing` | 把你自己的 skill 打包成能拖拽分享的压缩包 | 自动（说「打包这个 skill 分享给别人」就触发） |

这些 skill **零硬依赖**：配套 skill 没装也能跑，配方正文自带方法论。

---

## 一、装到哪

WorkBuddy 有两个版本，skills 目录不同。**先确认自己是哪个**：

| 版本 | skills 目录 |
|---|---|
| 国际版 | `C:\Users\<你的用户名>\.workbuddy-ai\skills\` |
| 国内版 | `C:\Users\<你的用户名>\.workbuddy\skills\` |

**怎么判断**：打开文件资源管理器，看 `C:\Users\你的用户名\` 下面有 `.workbuddy-ai` 还是 `.workbuddy`。
两个都有 → 看你平时用哪个客户端，或者**两个都装**（互不影响）。

> 目录不存在就手动建一个 `skills` 文件夹。

---

## 二、怎么装

把本包里的 **`workflow-recipes`** 和 **`ui-upgrade`** 两个文件夹，
整个复制进上面的 `skills` 目录。装完长这样：

```
C:\Users\<你>\.workbuddy-ai\skills\
├── workflow-recipes\
│   ├── SKILL.md
│   ├── references\        （12 个配方文件）
│   └── scripts\
└── ui-upgrade\
    └── SKILL.md
```

**装完新开一个对话。** 已开着的对话不会加载新 skill。

### 验证装上了

新对话里输入 `/`，列表里应该能看到 `workflow-recipes` 和 `ui-upgrade`。

---

## 三、怎么用（关键：不用记名字）

### 用法 A：直接说处境，什么都不用选

> 我的项目基础界面已经做完了，是个后台管理页面，技术栈是 Vue3 + Tailwind。
> 现在想做视觉质感升级和动画效果优化。

AI 会自动命中 `ui-upgrade`，按固定顺序编排：审计出清单 → 质感升级 → 动效（先过门禁再选路线）→ 收尾验证。

### 用法 B：说更宽泛的处境

> 我有个想法但还没想清楚要做什么，帮我理一下。
>
> 代码能跑但越改越乱，想重构但不知道从哪下手。
>
> 报了个 bug，复现都不稳定。

`workflow-recipes` 会先判断你在哪个阶段，读对应配方，**先把计划讲给你听**（"我打算按 X → Y → Z 走，每步产出 A、B、C"），你确认后再动手。

### 覆盖的 12 个阶段

| 你处在 | 对应配方 |
|---|---|
| 想法模糊、方向没定 | 01 起步 |
| 有想法，怕做偏 | 02 需求对齐 |
| 要做 / 改界面 | 03 设计 |
| 想清楚了，不会拆 | 04 规划 |
| 照 spec 写代码 | 05 实现 |
| 报错、慢、间歇故障 | 06 排错 |
| 能跑但难改 | 07 重构 |
| 上下文要满、要交接 | 08 协作 |
| 学新东西、准备答辩 | 09 学习 |
| 提交、review、合并 | 10 交付 |
| 装环境、配 CI、写文档 | 11 配置与文档 |

---

## 四、配套 skill（可选，装了更顺）

配方里会点名一些 skill。**没装不影响使用**——`workflow-recipes/references/00-skill-map.md`
里按**能力**列了每一项的替代做法，照着正文手做即可。

想装齐的话，这些是配方的主力：

| 包 | GitHub 地址 | 提供 |
|---|---|---|
| mattpocock skills 中文版 | `vinvcn/mattpocock-skills-zh-CN` | 29 个工程流程 skill（访谈 / 拆解 / TDD / 排错 / 重构 / 交付） |
| finesse-skill | `mouse-lin/finesse-skill` | 设计主力（4 register + 工艺底线 + 动效路线） |
| impeccable | `pbakaus/impeccable` | 22 命令式界面改造（audit / polish / bolder / animate …） |
| ui-ux-pro-max | `nextlevelbuilder/ui-ux-pro-max-skill` | 本地设计数据库（风格 / 配色 / 规范查询） |
| interface-design | `Dammyjay93/interface-design` | 产品界面方法论 |
| taste-skill | `Leonxlnx/taste-skill` | 落地页反 slop 风格 |

> 下载提示：`git clone` 拉 GitHub 容易挂死。用
> `curl -sL -o x.zip https://codeload.github.com/<owner>/<repo>/zip/refs/heads/main` 更稳。
> 大仓库可能下载不全，下完用 `unzip -t x.zip` 验一下。

---

## 五、可选增强：让 `ask-matt` 能查全部 skill

如果你装了 `vinvcn/mattpocock-skills-zh-CN`，会有一个 `ask-matt` skill。
**它默认只能查到它自己包里的 29 个 skill**，看不到你另外装的设计类 skill。

`optional/ask-matt-global-index/` 里是改造好的版本，让它变成**全量 skill 路由器**。

### 怎么装这个增强

1. 把 `optional/ask-matt-global-index/SKILL.md` 覆盖到你 skills 目录下的
   `ask-matt/SKILL.md`
2. 把 `optional/ask-matt-global-index/scripts/rebuild-index.py` 放到
   `ask-matt/scripts/rebuild-index.py`
3. 跑一次脚本生成索引：

```bash
python "C:\Users\<你>\.workbuddy-ai\skills\ask-matt\scripts\rebuild-index.py"
```

4. 新开对话，`/ask-matt` 就能路由到全部 skill。

> 原版 `ask-matt` 来自 `vinvcn/mattpocock-skills-zh-CN`（MIT License），此处为修改版。

---

## 六、维护

skill 数量变化后（装了新的 / 删了旧的），跑一次重建脚本刷新索引：

```bash
python "C:\Users\<你>\.workbuddy-ai\skills\workflow-recipes\scripts\rebuild-index.py"
```

它会：
- 扫描整个 skills 目录，生成 `GLOBAL-INDEX.md`（列全部 skill、来源包、调用方式、用途分组）
- 校验配方里引用的 skill 名是否真实存在，不存在会提示

> **脚本自带**，不依赖其他任何包。国内版把路径换成 `.workbuddy` 即可。

---

## 七、文件清单

```
workflow-recipes-pack/
├── AGENTS.md                          ← 给 AI 的安装指令（装 skill 时读这个）
├── README.md                          ← 本文件（给人看）
├── workflow-recipes/
│   ├── SKILL.md                       ← 主入口：三步走 + 阶段对照表
│   ├── references/
│   │   ├── 00-skill-map.md            ← 能力→实现映射（没装配套 skill 时查这个）
│   │   └── 01-kickoff.md … 11-setup-docs.md   ← 各阶段配方
│   └── scripts/rebuild-index.py       ← 索引重建（自包含）
├── ui-upgrade/
│   └── SKILL.md                       ← 质感 + 动效升级配方
├── skill-pack-sharing/
│   └── SKILL.md                       ← 把 skill 打包分享
└── optional/
    └── ask-matt-global-index/         ← 可选：ask-matt 全局路由增强
        ├── README.md
        ├── SKILL.md
        └── scripts/rebuild-index.py
```

---

## 八、常见问题

**Q：装了没反应？**
A：新开对话。skill 在对话开始时加载。

**Q：配方里点名的 skill 我没装，能用吗？**
A：能。查 `workflow-recipes/references/00-skill-map.md`，按「没装时怎么办」执行。
配方正文里已经写了方法论，skill 只是让它自动化和结构化。

**Q：我想加自己的 skill 进去？**
A：直接放进 skills 目录，跑一次 `rebuild-index.py`。新 skill 会被自动收录
（未在映射表里的会标为「未分类」，不影响使用）。

**Q：两个版本目录都装了会冲突吗？**
A：不会。各版本读各自的目录。

**Q：把链接（或压缩包）丢给 AI，它会自己装吗？**
A：**大概率会，但加一句指向更稳。** 丢过去后说「帮我装上」通常就够——
`AGENTS.md` 是专为这个场景写的任务书，agent 会读到它。
但"装上"有歧义，agent 可能理解成"解压到工作区"或"读一遍总结"。
**说「按 AGENTS.md 帮我装上」基本不会跑偏。**

**Q：装完为什么不生效？**
A：**要新开对话。** skill 在对话开始时加载，当前对话读不到。
