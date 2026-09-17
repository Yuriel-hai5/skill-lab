# 可选增强：ask-matt 全局 skill 索引

## 这是什么

`ask-matt` 来自 `vinvcn/mattpocock-skills-zh-CN`（MIT License）。
**原版只能查到它自己包里的 29 个 skill**，看不到你另外装的设计类 / 其他来源的 skill。

这里的 `SKILL.md` 是改造版，让它变成**全量 skill 路由器**：

- 回答前先读 `GLOBAL-INDEX.md`（列出本机**全部**已安装 skill、来源包、调用方式、用途分组）
- 索引过期（装了新 skill）会**自动重建**
- 新增 4 条路由规则：设计类任务优先指向包外、改造任务拆分、流程型 skill 不双主导等

## 前提

你已经装了 `vinvcn/mattpocock-skills-zh-CN`，skills 目录下有 `ask-matt/`。
**没装的话跳过这一步**——`workflow-recipes` 不依赖它。

## 装法

假设你的 skills 目录是 `<skills-dir>`（国际版 `~/.workbuddy-ai/skills/`，国内版 `~/.workbuddy/skills/`）：

```bash
# 1. 覆盖 SKILL.md（建议先备份原文件）
cp "<skills-dir>/ask-matt/SKILL.md" "<skills-dir>/ask-matt/SKILL.md.bak"
cp "SKILL.md" "<skills-dir>/ask-matt/SKILL.md"

# 2. 放入重建脚本
mkdir -p "<skills-dir>/ask-matt/scripts"
cp "scripts/rebuild-index.py" "<skills-dir>/ask-matt/scripts/rebuild-index.py"

# 3. 生成索引
python "<skills-dir>/ask-matt/scripts/rebuild-index.py"
```

Windows 示例：

```powershell
python "C:\Users\<你>\.workbuddy-ai\skills\ask-matt\scripts\rebuild-index.py"
```

## 验证

新开对话，输入 `/ask-matt` 问一个包外 skill 的问题，例如：

> 我的落地页做完基础结构了，想提升质感和加动效，该用哪些 skill？

回答里应该出现 `finesse-ui` / `impeccable` / `ui-ux-pro-max` 这类**包外** skill 的名字。
如果只提 mattpocock 包内的 skill，说明索引没生效。

## 注意

- 脚本输出 `GLOBAL-INDEX.md` 到 `ask-matt/` 目录下，**是本机特定的**，换机器要重跑
- 覆盖 SKILL.md 后，如果上游包更新，需要重新套用改造（改造内容见下）
- 改造只动了 `SKILL.md`，原包的 `PHASE-BOUNDARIES.md` / `agents/openai.yaml` 不动

## 改造内容（供上游更新后重套）

1. frontmatter `description` 扩展为"全部已安装 skills 的路由器"
2. 开头插入「⚠️ 第一步：校验并读全局索引（必做）」段，含过期自检 + 重建指令
3. 追加 4 条路由规则（设计类路由到包外 / 改造任务拆分 / 流程型不双主导 / 未知 skill 当独立用）
4. 新增 `scripts/rebuild-index.py`（自包含，路径自动推断）
