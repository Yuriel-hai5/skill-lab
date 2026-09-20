# 11 · 环境配置 / 文档

## 适用信号

- "装不上 / 配不好 / 命令找不到"
- "要配 CI、要填密钥、要走第三方后台"
- "加个 pre-commit 检查"
- "帮我写个文档 / README / skill"
- "改一下 AGENTS.md"
- "skill 装了但 AI 一次都没用 / AI 不知道本机有哪些 skill"

## 配方

### A. 只有人能做的步骤 → `wizard`

用于：provisioning 基础设施、设置 credentials 或 CI secrets、在陌生的第三方 dashboard 里点操作、
运行一次性 migration 或 cutover。

它生成一个**交互式 bash script**，逐个打开 URL、捕获每个值、写入 `.env` 和 GitHub secrets——
这样该过程就不再需要每次向 agent 重新解释。

> **边界**：agent 自己能做的步骤**不许**用它。这个 skill 专给 human 真的在 loop 里的场景。

### B. 提交前自动检查 → `setup-pre-commit`

配置 Husky pre-commit hooks，集成 lint-staged（Prettier）、类型检查、测试。

### C. 防止危险 git 操作 → `git-guardrails-claude-code`

设置 hooks，在危险命令（`push`、`reset --hard`、`clean`、`branch -D`）执行**前**拦截。

> 只在 Claude Code 里生效。

### D. 每 repo 配置一次 → `setup-matt-pocock-skills`

首次在某个 repo 使用工程流程前跑一次，配置三样：

1. **Issue tracker**：GitHub / GitLab / **local markdown**（本地是 `.scratch/<feature-slug>/`）/ 其他
2. **Triage labels**：五个 canonical roles 的字符串映射
3. **Domain docs 布局**：single-context（root `CONTEXT.md` + `docs/adr/`）或 multi-context

**产出**：`AGENTS.md` 或 `CLAUDE.md` 的 `## Agent skills` block + `docs/agents/*.md`。

> **这是 per-repo 的**，换项目要重跑。之后想改配置直接编辑 `docs/agents/*.md` 即可。

### E. 写文档 → `writing-for-agents`

给 **agent 消费**的文档的 reference：skills、`AGENTS.md` / `CLAUDE.md`、以及任何被 pointer 指向的文档。

写文档时的关键区别：**agent 是通过 pointer 到达文档的**，所以文档要考虑"agent 怎么找到它、找到后怎么用"，
而不是只考虑"人读起来顺不顺"。

### F. 写一个新 skill → `skill-creator`

**这是 WorkBuddy 内置 skill**（不在 `<skills-dir>` 下，在应用安装目录里），可直接用。

创建或更新 skill 时用，含 frontmatter 规范、**description 写法**（它决定 skill 何时被触发，是最关键的一行）、
渐进披露结构（SKILL.md 保持轻量，深内容放 `references/`，按需加载）。

> 写完 skill 后记得跑一次 `rebuild-index.py` 让它进全局索引。

### G. 让 skill 真的被用上 → 给项目加 `AGENTS.md`

**症状**：skill 装了、`description` 也写对了，但 AI 干活时**一次都不调用** ——
自己把 skill 里**已经写着**的东西重新推导一遍。

**根因**：`description` 决定模型「**能看到**什么」，**不决定「会不会动手」**。
触发是模型的主动决策，它想不起来，skill 就等于不存在。

**解法**：把「动手前先扫技能库」写进项目根的 `AGENTS.md`。
`AGENTS.md` **每次对话自动注入**，不依赖模型主动回忆 —— 比 skill 的 `description` 可靠一个量级。

#### 可粘贴的 block

放在项目根 `AGENTS.md` 的**靠前**位置（别塞在末尾）：

```markdown
## ⚠️ 动手前：先扫技能库（别跳）

改这个项目的代码之前，先读本机 skill 索引 —— 很多 skill 是按**症状**命名的。
不扫，它们永远不会被用上。

读 `<skills-dir>/workflow-recipes/GLOBAL-INDEX.md`
（如果它和 skills 目录对不上，先跑同目录的 `scripts/rebuild-index.py` 重建）。

| 你要做的事 | 先看哪个 skill |
|---|---|
| <这个项目会遇到的场景> | <对应 skill 名> |
| <…> | <…> |

**扫到了就默默用 —— 别把 skill 名报给用户。**
说「我接下来怎么做」，不要说「我按哪个 skill 做」。
（唯一例外：需要用户在两个做法之间选时，才说清是什么。）

**为什么写死这条**：<这个项目踩过的实例 —— 什么时候、AI 漏了什么、事后怎么说的>
```

#### 表格行必须按项目自填

**不要照抄。** 一个 WPF 桌面项目和一个 Spring Boot 后端，相关 skill 完全不同 ——
抄错了等于没写，还占掉注意力。

填法：从 `GLOBAL-INDEX.md` 里挑**这个项目真的会用到**的，通常 3–6 行就够。
判据是「上次做 X 的时候，我是不是希望它先读 Y」—— 有这种事后懊悔的场景才值得写进去。

#### 最后那行「为什么」别省

**给实例，不给口号。** 「AI 漏了 X」比「skill 很重要」有用一个量级 ——
它是写给**下一个 agent** 看的，而 agent 只被具体证据说服。

#### 扫到之后：默默用，别报出来

上面那段解决"会不会去查"，这条解决"查完之后怎么说话"。**两个都要。**

**skill 是工具，不是对话内容。** 说「我接下来怎么做」，不要说「我按哪个 skill 做」。

| ❌ 别说 | ✅ 该说 |
|---|---|
| 「先按 skill 的铁律来：先量化，别猜」 | 「我先量一下截图，别靠感觉猜」 |
| 「我读了 `wpf-visual-bug-triage`」 | （不用说，直接做） |

**为什么**：报 skill 名是**元话语** —— 它没告诉用户"接下来会发生什么"，
只暴露了内部机制。用户不关心工具链，只关心结果。

**例外只有一处**：需要用户在**两个做法之间选**时，必须说清是什么 —— 不说清他没法选。

> **实测**（2026-09-20）：用户只说了一句「我看着别扭」（纯陈述），
> AI 回了「**先按 skill 的铁律来：先量化，别猜**」。
> 正例过了（它确实去查了 skill），但用户要的是**默默用** ——
> 原话：「你可以**默默思考中使用，别说出来**」。
>
> ⚠️ 它说「**铁律**」是从那个 skill 的标题 `## 铁律：先量化，别猜` 照搬的 ——
> **skill 文件里的措辞会泄漏到对话里。** 写「铁律」，用户就会听到「按铁律」。
> 所以：**skill 正文里只对 agent 有意义的词（铁律 / 必须 / 严禁），别让它出现在对用户说的话里。**

#### 两个都要做

| 手段 | 管什么 |
|---|---|
| `description`（见 F） | 模型**看得见**这个 skill |
| `AGENTS.md` 这段 | 模型**会动手**去查 |

**缺一个都不成立。** 只写 `description` → 装了不用（实测）。
只写 `AGENTS.md` → 索引里没有，查了也白查。

#### 边界

- 这是 **per-repo** 的（和 D 一样）—— 换项目要重新填表格行
- 别把 `AGENTS.md` 写成 skill 清单的复制品 —— 只列**这个项目会用到**的，其余指向索引
- `GLOBAL-INDEX.md` 是**本机生成物**，别提交进仓库、别打进分享包
  （见 [../../skill-pack-sharing/SKILL.md](../../skill-pack-sharing/SKILL.md) 第 7 步）

> **实测证据**（2026-09-20）：一次 WPF 动画修复，`description` 确认**已加载**
> （AI 复述出了新版独有措辞），但全程没查技能库，把已装的 `wpf-visual-bug-triage`
> 里**已经写着**的东西重新推导了一遍。事后自述：
> 「**没查。这是我的疏漏。**……不是『技能库没用』，是我压根没走那一步。」
> 结论：**问题不在 `description`，在"没有一步强制它去查"。**

## 需确认

- `wizard` 生成的脚本会**写 `.env` 和 secrets**——执行前确认目标位置
- `setup-pre-commit` 会改 `package.json` 和 git hooks——确认技术栈是 Node
- `setup-matt-pocock-skills` 要用户选 tracker / labels / docs 布局，**不要替他选**
- 加 `AGENTS.md` 的「先扫技能库」那段时（见 G），**表格行让他确认** ——
  他最清楚这个项目会踩什么坑，你猜的往往不对
- 装任何东西前确认**真的需要**（避免装了又不用，浪费空间）

## 常见坑

1. **环境问题先查真实环境再下结论。** 工具进程可能不继承真实环境变量（见 [06-debugging](06-debugging.md) 第 3 节）。
2. **把只有人能做的事硬塞给 agent。** 用 `wizard` 把流程结构化，而不是让 agent 猜。
3. **忘了 per-repo 配置。** 新项目第一次用工程流程前要跑 `setup-matt-pocock-skills`。
4. **文档写给人的而不是给 agent 的。** 两者的到达路径不同。
5. **装完不清理临时文件。** 下载的 zip、解压的源码用完就删。
6. **以为 `description` 写对了 skill 就会被用上。** 触发是模型的**主动决策**，不是自动的 ——
   必须另加一步强制它去查（见 G）。**"skill 装了没用过"多半是这个问题，不是 skill 写坏了。**
7. **把 skill 名报给用户。** 「按 skill 的铁律来」是**元话语** ——
   没告诉用户"接下来做什么"，只暴露了内部机制（见 G 的「扫到之后」）。

## 边界

- 装的是第三方 skill 包 → 见用户级 `MEMORY.md`（国际版 `~/.workbuddy-ai/MEMORY.md`，
  国内版 `~/.workbuddy/MEMORY.md`）里「装 GitHub skill 包的通用注意」
  （大仓库下载会截断、硬编码路径要改、只装 skill 本体）
- 环境本身的问题（报错、找不到命令）→ [06-debugging](06-debugging.md)
