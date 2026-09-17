# 11 · 环境配置 / 文档

## 适用信号

- "装不上 / 配不好 / 命令找不到"
- "要配 CI、要填密钥、要走第三方后台"
- "加个 pre-commit 检查"
- "帮我写个文档 / README / skill"
- "改一下 AGENTS.md"

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

## 需确认

- `wizard` 生成的脚本会**写 `.env` 和 secrets**——执行前确认目标位置
- `setup-pre-commit` 会改 `package.json` 和 git hooks——确认技术栈是 Node
- `setup-matt-pocock-skills` 要用户选 tracker / labels / docs 布局，**不要替他选**
- 装任何东西前确认**真的需要**（避免装了又不用，浪费空间）

## 常见坑

1. **环境问题先查真实环境再下结论。** 工具进程可能不继承真实环境变量（见 [06-debugging](06-debugging.md) 第 3 节）。
2. **把只有人能做的事硬塞给 agent。** 用 `wizard` 把流程结构化，而不是让 agent 猜。
3. **忘了 per-repo 配置。** 新项目第一次用工程流程前要跑 `setup-matt-pocock-skills`。
4. **文档写给人的而不是给 agent 的。** 两者的到达路径不同。
5. **装完不清理临时文件。** 下载的 zip、解压的源码用完就删。

## 边界

- 装的是第三方 skill 包 → 见用户级 `MEMORY.md`（国际版 `~/.workbuddy-ai/MEMORY.md`，
  国内版 `~/.workbuddy/MEMORY.md`）里「装 GitHub skill 包的通用注意」
  （大仓库下载会截断、硬编码路径要改、只装 skill 本体）
- 环境本身的问题（报错、找不到命令）→ [06-debugging](06-debugging.md)
