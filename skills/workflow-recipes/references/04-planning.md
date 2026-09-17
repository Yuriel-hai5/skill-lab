# 04 · 规划 / 拆解

## 适用信号

- "需求想清楚了，但不知道怎么下手"
- "这个功能太大了，一次做不完"
- "帮我列个任务清单 / 排个优先级"
- 已经有 spec 或设计稿，要转成可执行的开发任务

## 配方

### 1. `to-spec` —— 把讨论收束成 spec

- **它不做访谈**，只综合**已经聊过**的内容。所以前面的对齐必须先做完
- 发布到已配置的 issue tracker（本机是本地 markdown：`.scratch/<feature-slug>/spec.md`）
- **产出**：`spec.md`——可构建的完整规格

> 如果对话里还有没说清的地方，它会留空洞。**空洞要回 [02-alignment](02-alignment.md) 补**，别在 spec 里含糊过去。

### 2. `to-tickets` —— 拆成 tracer-bullet tickets

拆分规则（它内置的纪律）：

- 每个 slice 要**贯穿每一层**（schema → API → UI → tests）形成窄而完整的路径
  —— 是 **vertical slice**，不是某一层的 horizontal slice
- 每个 slice 做完能**独立 demo 或验证**
- 每个 slice 的大小要**塞得进一个 fresh context window**
- 为每个 ticket 声明 **blocking edges**（它开始前必须先完成的 ticket）
- **prefactoring 先做**：「Make the change easy, then make the easy change」

**例外 —— wide refactor**（影响整个 codebase 的机械改动，如重命名列、改共享符号类型）：
不要硬拆成 tracer bullet，按 **expand → 分批迁移 → contract** 排序，
每批一个 ticket 且被 expand block，保证每步 CI 都 green。

- **产出**：`.scratch/<feature-slug>/issues/NN-<slug>.md`，一 ticket 一文件（**绝不写成一个合并文件**）

### 3. `triage` —— **只用于不是你创建的 issue**

外部来的 bug report、feature request、收到的 PR。它让 issue 过一组状态机：
`needs-triage` → `needs-info` / `ready-for-agent` / `ready-for-human` / `wontfix`，
并写出 agent-ready brief。

> **`to-tickets` 产出的 ticket 已经是 agent-ready，不要再 triage 一遍。** 重复 triage 只制造噪音。

### 4. 然后接 [05-implementation](05-implementation.md)

**每个 ticket 一次 `implement`，中间 `/clear` 清空 context。** 每个 ticket 自包含，所以上一个的 context 可以丢。

## 需确认

- 拆完之后**问用户三个问题**（`to-tickets` 内置的）：
  1. 粒度合不合适（太粗还是太细）？
  2. blocking edges 对不对，每个 ticket 是不是只依赖真正 gate 它的？
  3. 要不要继续合并或拆分？
- **粒度宁细勿粗**：太粗的 ticket 塞不进一个 context window，会变成一次做不完的活。

## 常见坑

1. **context 卫生**：从 grilling 到 `to-tickets` 要留在**同一个未中断的 context window**，
   不要 compact / clear——spec 和 tickets 要建立在同一组思考上。
   接近 **smart zone**（约 150k tokens）时，在最近的阶段边界用 `/compact`，然后继续。
2. **horizontal slicing**：按层拆（先做完所有 DB、再做所有 API）会导致每片都不能独立验证。
3. **把多个 ticket 写进一个文件**。本地 tracker 的约定是一 ticket 一文件，这是 skill 能正确工作的前提。
4. **忘记 prefactoring**。让实现变容易的改动应该先做，而不是混在功能 ticket 里。
5. **triage 用在自建 ticket 上**（见上）。

## 边界

- 需求还有没说清的地方 → 回 [02-alignment](02-alignment.md)
- 工作量大到一个 session 装不下、路径本身还看不清 → 先 [01-kickoff](01-kickoff.md) 的 `wayfinder`
