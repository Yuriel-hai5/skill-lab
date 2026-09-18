# skill-lab

我的 agent skill 工坊。**skill 的源码放这里，不在对话里。**

> 建这个项目的原因：skill 是在对话里做出来的，但对话会删、会翻不到。
> 所以把源码落到硬盘上，当成正式项目维护 —— 有版本号、有历史、能回滚、能打包。

---

## 30 秒速查（懵的时候看这个）

**平时你只需要做两件事：**

| 你想 | 怎么做 |
|---|---|
| **用** skill 干活 | 新开对话 → 直接说处境 → 完事 |
| **改** skill | 在 `Desktop\skill-lab\` 里开对话 → 说改什么 → 跑 `python scripts/deploy.py` → 再新开对话 |

**一句话理解整个项目**：

> `Desktop\skill-lab\` 是**原稿**，`~\.workbuddy-ai\skills\` 是**印出来的书**。
> 改原稿 → 印一次（deploy）→ **新开对话**才能读到新版。

其他都是一次性的，已经弄好了，不用管。

---

## 这里有什么

| 目录 | 放什么 |
|---|---|
| `skills/` | **skill 源码，唯一源头。** 改 skill 只改这里 |
| `pack/` | 分享打包用的素材（给收件人 agent 的任务书 + 说明 + 打包脚本） |
| `scripts/` | 部署脚本 —— 把 `skills/` 同步到 WorkBuddy 的 skills 目录 |
| `docs/` | [`路线图.md`](docs/路线图.md)（4 个完善方向）、[`下次改动.md`](docs/下次改动.md)（已想清楚待做的）、[`待改进.md`](docs/待改进.md)（用的时候随手记）、`参考/`（调研资料） |

### 当前 3 个 skill

| skill | 干什么 | 什么时候触发 |
|---|---|---|
| `workflow-recipes` | **主力。** 说清处境 → 给出「用哪些 skill + 什么顺序 + 每步产出什么」 | 你说"我卡在 XX 阶段了""下一步该做什么" |
| `ui-upgrade` | 已有界面的质感 + 动效升级配方 | 你说"界面看起来廉价""加动效""要高级感" |
| `skill-pack-sharing` | 把 skill 打包成别人能拖拽安装的分享包 | 你说"打包这个分享给别人" |

`workflow-recipes` 覆盖 11 个阶段：起步 / 对齐 / 设计 / 规划 / 实现 / 排错 / 重构 / 协作 / 学习 / 交付 / 配置文档。

---

## 怎么用（日常）

### 〇、开新对话时怎么开口

**不需要跟 AI 解释这个项目。** 项目根有 `AGENTS.md`，AI 一进来就会读。
你只需要说**今天要干什么**。

直接复制下面任一条：

**① 按计划改 skill**（最常用）
```
读 AGENTS.md 和 docs/下次改动.md，然后按里面的「待做 1」改。
```

**② 不知道干什么，先看现状**
```
读 AGENTS.md、README.md、docs/路线图.md，然后告诉我：
现在有什么、缺什么、建议下一步做什么。
```

**③ 用 skill 干活**（不是改它 —— 这条**不在**本项目里开，去你的项目工作区开）
```
我现在处在项目的【XX 阶段】，情况是【一句话】。
帮我看看该用哪些 skill、按什么顺序、每步产出什么。
```

**④ 有临时想法，先记下来不改**
```
把这个想法记到 docs/待改进.md：【一句话】。
```

> ⚠️ **别说"这是个半成品"** —— 它是正式维护的项目（版本见 `VERSION`）：功能完整、测过、能分享。
> 说"半成品"会让 AI 以为要大改，反而不按 `docs/路线图.md` 的计划走。

### 一、在项目里用 skill

**新开一个对话**，直接说处境就行，不用记 skill 名字：

```
我现在处在【XX 阶段】。
具体情况：【一句话说清在做什么、卡在哪】。
帮我看看该用哪些 skill、按什么顺序、每步产出什么。
```

> **为什么要新开对话**：skill 在对话开始时加载。旧对话里 skill 是"迟到"的，不会被自动认出来。
>
> **旧对话想用**：输入 `/workflow-recipes`（实测有效），或者让 AI 直接读
> `C:\Users\Administrator\.workbuddy-ai\skills\workflow-recipes\SKILL.md`。

### 二、改 skill

1. 改 `skills/<名字>/` 里的文件（**不要**直接改 `~/.workbuddy-ai/skills/`）
2. 跑部署：

```bash
python scripts/deploy.py
```

> **第一次**要指定目标目录（因为你这台机器两个版本都装了）：
> ```bash
> python scripts/deploy.py --target "C:\Users\Administrator\.workbuddy-ai\skills"
> ```
> 之后会**记住**，直接 `python scripts/deploy.py` 就行。
>
> 其他参数：`--dry-run` 只看不改 / `--backup` 覆盖前备份 / `--only <名字>` 只部署一个。

3. **新开对话**才生效
4. 改完更新 `CHANGELOG.md` 和 `VERSION`

### 三、分享给别人

```bash
python pack/build.py
```

产出的 zip 在 `pack/dist/` 下（文件名带版本号）。
发给别人，他拖进 WorkBuddy 对话框说「按包里的 AGENTS.md 帮我装上」即可。

---

## 关键约定

### ⚠️ 改 skill 时，对话要在这个文件夹里开

**在这个文件夹里开对话**（`C:\Users\Administrator\Desktop\skill-lab\`），项目根的 `AGENTS.md`
才会被自动加载，AI 才知道"源码在这里、部署目录是目标、改完要 deploy"。

在别的地方开对话，AI 读不到这些规矩，很可能**直接去改部署目录** ——
改完 skill 生效了，但项目源码落后了，下次 deploy 会把改动覆盖掉。

### `skills/` 是源头，`~/.workbuddy-ai/skills/` 是部署目标

```
skills/                          ← 你改这里
   ↓  python scripts/deploy.py
~/.workbuddy-ai/skills/          ← WorkBuddy 读这里
```

**别反过来改。** 直接改部署目录的话，项目里的源码就落后了，下次部署会把你的改动覆盖掉。

### 路径一律用 `<skills-dir>` 占位符

skill 文件里**不许出现** `C:\Users\Administrator\...` 这类本机路径 —— 否则分享给别人就坏了。

需要指代 skill 安装目录时，写 `<skills-dir>`，并在 SKILL.md 里说明怎么推断
（取 SKILL.md 自己所在目录的父目录）。

### 版本号：四级 `x.x.x.x`

| 位 | 什么时候加 |
|---|---|
| **主版本** X.0.0.0 | 不兼容的改动、架构重构、skill 大改版 |
| **次版本** x.X.0.0 | 新增配方 / 新增 skill / 新增能力 |
| **修订号** x.x.X.0 | 修 bug、改错字、补说明 |
| **构建号** x.x.x.X | 自动生成，不手动管 |

---

## 现在做到哪了

- ✅ 3 个 skill 功能完整、实测可加载、能分享
- ✅ 分享包验证过（最小安装 / 全量安装 / 冲突检查，全过）
- ✅ 项目骨架建好：源码 / 部署脚本 / 打包脚本 / 版本管理 / 路线图
- ⏳ **下一步：拿去用。** 用的时候哪里卡住就记到 `docs/待改进.md`，攒够了再改

> 改什么不要现在空想 —— **用过才知道**。

### 规划好的 4 个完善方向

见 **[`docs/路线图.md`](docs/路线图.md)**（都写了具体要做什么、验收标准）：

| 方向 | 一句话 | 建议顺序 |
|---|---|---|
| 1 · 扩更多场景配方 | 加论文写作 / 数据可视化 / 部署运维 —— 现在 11 个配方全是"写代码"的配套 | 2 |
| 2 · 工坊化 | 变成"你所有 skill 的家"，有模板和新建脚本 | 3 |
| 3 · 提升配方质量 | 从"告诉你该干什么"变成"告诉你具体怎么干" | **1** |
| 4 · 优化分享体验 | 让别人装得更可靠 | 4 |

---

## 相关位置

| 东西 | 路径 |
|---|---|
| 项目源码 | `C:\Users\Administrator\Desktop\skill-lab\` |
| 部署目标（WorkBuddy 读这个） | `C:\Users\Administrator\.workbuddy-ai\skills\` |
| 全局 skill 索引 | `<skills-dir>/workflow-recipes/GLOBAL-INDEX.md` |
