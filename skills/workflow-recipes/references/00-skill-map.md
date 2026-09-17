# 00 · 能力 → 实现 映射表

配方里点名的 skill 是**推荐实现**，不是硬依赖。这张表按**能力**列出它们，方便在别人的
skill 组合不同的情况下替换。

> **最重要的一点**：配方的方法论（访谈怎么追问、feedback loop 怎么建、动效路线怎么选、
> 重构怎么排序）**已经写在配方正文里**。所以即使一个配套 skill 都没装，配方依然可执行——
> 只是少了自动触发和结构化执行。**顺序是硬的，工具是可换的。**

---

## 路由 / 元

| 能力 | 推荐 skill | 没装时怎么办 |
|---|---|---|
| 查"该用哪个 skill" | `ask-matt` | 直接读本 skill 的阶段对照表（SKILL.md） |
| 按阶段给序列 | `workflow-recipes`（本 skill） | — |

## 访谈 / 对齐

| 能力 | 推荐 skill | 没装时怎么办 |
|---|---|---|
| 持续追问打磨想法（有 repo，留文档） | `grill-with-docs` | 按 [02-alignment](02-alignment.md) 正文自己执行：映射 design tree、按 rounds 推进 frontier、每个问题带推荐答案 |
| 同样的访谈但不留文件 | `grill-me` | 同上，只是不写 `CONTEXT.md` / ADR |
| 访谈引擎本身 | `grilling` | 同上 |

## 规格 / 拆解

| 能力 | 推荐 skill | 没装时怎么办 |
|---|---|---|
| 把讨论收束成 spec | `to-spec` | 按 [04-planning](04-planning.md) 正文手写 spec，落到 `.scratch/<feature>/spec.md` |
| 拆成 tracer-bullet tickets | `to-tickets` | 按正文的 vertical slice 规则 + blocking edges 手拆，一 ticket 一文件 |
| 外部 issue 分类 | `triage` | 按正文的五个 state role 手工标注 |

## 实现

| 能力 | 推荐 skill | 没装时怎么办 |
|---|---|---|
| 照 spec 实现（编排） | `implement` | 按 [05-implementation](05-implementation.md) 正文自己编排：tdd → 定期 typecheck → code-review → 提交 |
| 测试驱动开发纪律 | `tdd` | 按正文的「好测试标准 + 三条反模式 + 循环规则」执行 |
| 原型验证设计问题 | `prototype` | 按正文的 logic / UI 两分支规则手写 |

## 排错

| 能力 | 推荐 skill | 没装时怎么办 |
|---|---|---|
| 建 feedback loop 定位 bug | `diagnosing-bugs` | 按 [06-debugging](06-debugging.md) 正文的**十种 loop 建法**逐一尝试（这部分完全自包含） |
| 双轴代码审查 | `code-review` | 按 Standards + Spec 两个轴线手工过一遍 diff |
| 解 merge 冲突 | `resolving-merge-conflicts` | 按正文的「找 primary source → 按 intent 解决 → 不 --abort」执行 |

## 重构 / 代码健康

| 能力 | 推荐 skill | 没装时怎么办 |
|---|---|---|
| 找深化候选 | `improve-codebase-architecture` | 按 [07-refactoring](07-refactoring.md) 正文的摩擦信号清单 + deletion test 手工扫 |
| 设计模块形状 | `codebase-design` | 用正文的词汇（module / interface / depth / seam / adapter / leverage / locality）自行判断 |
| 领域模型与 ADR | `domain-modeling` | 手工挑战模糊术语，把难逆转的决策写成 `docs/adr/NNNN-*.md` |

## 规划 / 调研

| 能力 | 推荐 skill | 没装时怎么办 |
|---|---|---|
| 大工程画决策地图 | `wayfinder` | 按 [01-kickoff](01-kickoff.md) 正文手建 `map.md` + decision tickets（结构已在正文里） |
| 对照一手来源调研 | `research` | 自己查官方文档 / 源码 / spec，每个结论标来源 |

## 协作 / 上下文

| 能力 | 推荐 skill | 没装时怎么办 |
|---|---|---|
| 压缩对话成交接文档 | `handoff` | 按 [08-collaboration](08-collaboration.md) 正文手写，存系统临时目录 |
| 重述没听懂的话 | `wait-what` | 直接要求对方"用平实语言重讲一遍，用项目自己的词汇" |
| 向他人收集信息 | `to-questionnaire` | 按正文的「问发送而非问主题」原则手写问卷 |

## 学习

| 能力 | 推荐 skill | 没装时怎么办 |
|---|---|---|
| 跨 session 教学 | `teach` | 按 [09-learning](09-learning.md) 正文手建 workspace（MISSION.md / lessons/ / learning-records/） |
| 生成练习结构 | `scaffold-exercises` | 手工建「章节 / 题目 / 答案 / 讲解」目录 |

## 设计（从零）

| 能力 | 推荐 skill | 没装时怎么办 |
|---|---|---|
| 全流程设计系统（4 register） | `finesse-ui` | 按 [03-design](03-design.md) 配方 A 的 register 分流 + 工艺底线执行 |
| 落地页反 slop | `taste-skill` | 用配方 D 的三旋钮 + Design Read 自行判断 |
| 特定风格 | `minimalist-skill` / `brutalist-skill` / `soft-skill` | 按各自风格描述手工实现 |
| 产品界面方法论 | `interface-design` | 用配方末段的「四件套 + 组件前声明」自检 |
| 生成 DESIGN.md | `stitch-skill` | 手工写设计系统文档 |
| 反截断完整输出 | `output-skill` | 要求"输出完整代码，不要省略号占位" |

## 设计（改造 / 查询）

| 能力 | 推荐 skill | 没装时怎么办 |
|---|---|---|
| 已有界面质感 + 动效升级 | `ui-upgrade` | 按配方 B 的五步走手工执行 |
| 命令式改造（22 个动词） | `impeccable` | 按配方 B 挑对应动作手工做（audit / polish / bolder / quieter …） |
| 升级已有站点 | `redesign-skill` | 审计先行，按配方 B 执行 |
| 查设计事实 | `ui-ux-pro-max` | 查官方规范（WCAG、平台 HIG）或权威设计系统文档，**不要凭记忆编配色** |
| shadcn/Tailwind 组件 | `ui-styling` | 查 shadcn/ui 官方文档 |
| 演示稿 | `slides` | 手工做 HTML 演示稿 |
| 横幅 | `banner-design` | 手工按平台尺寸规范做 |

## 交付 / 配置 / 文档

| 能力 | 推荐 skill | 没装时怎么办 |
|---|---|---|
| 提交前审查 | `code-review` | 见「排错」节 |
| GitHub 推送（API 兜底） | `github-push-via-api` | 常规 `git push`；不通时手工走 Git Data API |
| 人工步骤向导 | `wizard` | 按 [11-setup-docs](11-setup-docs.md) 正文自己列步骤清单，逐条让用户执行并回报 |
| pre-commit 检查 | `setup-pre-commit` | 手工配 Husky + lint-staged |
| 危险 git 拦截 | `git-guardrails-claude-code` | 靠约定 + 人工确认 |
| 每 repo 配置 | `setup-matt-pocock-skills` | 手工建 `AGENTS.md` + `docs/agents/*.md` |
| 为 agent 写文档 | `writing-for-agents` | 按「agent 通过 pointer 到达文档」的原则自行组织 |
| 写新 skill | `skill-creator`（内置） | 按标准 Agent Skills 格式（SKILL.md + frontmatter）手写 |

---

## 怎么用这张表

1. **先按配方走**。配方点名的 skill 装了就直接用。
2. **没装 → 看这张表**找对应能力行，按「没装时怎么办」执行。
3. **表里也没有 → 问用户**："这一步需要一个能做 X 的 skill，你装了什么？"
   然后按能力对应关系替换，**配方顺序不变**。

## 推荐的配套包

如果想把配方跑得最顺，这些是配套（GitHub）：

| 包 | 地址 | 提供 |
|---|---|---|
| mattpocock skills 中文版 | `vinvcn/mattpocock-skills-zh-CN` | 29 个工程流程 skill |
| finesse-skill | `mouse-lin/finesse-skill` | 设计主力 |
| impeccable | `pbakaus/impeccable` | 22 命令改造集 |
| ui-ux-pro-max | `nextlevelbuilder/ui-ux-pro-max-skill` | 设计数据库 |
| interface-design | `Dammyjay93/interface-design` | 产品界面方法论 |
| taste-skill | `Leonxlnx/taste-skill` | 落地页风格 |

**不装也能用**——配方正文自带方法论。
