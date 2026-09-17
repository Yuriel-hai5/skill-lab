# 08 · 协作 / 上下文管理

## 适用信号

- "上下文快满了 / 要开新对话了"
- "这条消息我没看懂"、"它说的啥意思"
- "卡住我的东西在别人脑子里"
- "要换一个目录 / 换一个工具继续"
- "下一步该继续还是重开？"

## 配方

### 1. 阶段边界 —— 五个选项，选哪个是最模糊的决定

一个 **phase** 是 session 内的一段工作（grilling、implementation、QA）。在它们之间你有：

| 选项 | 什么时候用 |
|---|---|
| **Continue** | 原地不动。零成本零损失。**第一个要排除的选项**——不是默认跳过，而是先问"为什么不能继续" |
| **`/clear`** | 这里的内容对接下来的工作完全不重要 |
| **`handoff`** | 范围很窄：**换 harness**、**换目录**、**交给同事**，或阶段中途分叉 side task。买的是 **portability** |
| **Subagent** | 把 tightly-scoped task 送到自己的 context window，拿回一份报告 |
| **`/compact`** | 压缩并用 summary 播种 fresh session。**默认项，在决策树底部**，不是最先伸手够的 |

**在边界处做决定，不要阶段中途做。** 阶段中途要么继续，要么把剩余工作拆成 subagents。

> **smart zone**：context window 里模型还能保持敏锐推理的区间，最新模型约 **150k tokens**。
> 接近它时不要硬撑降级状态，在最近的阶段边界处理。

### 2. `handoff` —— 要换地方时

- 写一份 handoff document，让 fresh agent 能继续
- **保存到系统临时目录，不要保存进当前 workspace**
- 包含 "suggested skills" 段：建议下一个 agent 调用哪些 skill
- **不重复**已被其他 artifact 捕获的内容（spec、plan、ADR、issue、commit、diff）——用路径或 URL 引用
- 删掉敏感信息（API key、密码、个人身份信息）
- 可传参：`/handoff 下个会话要干什么`，据此调整文档

### 3. `wait-what` —— 没听懂时

对没有落地的消息的纠正。在**任何** skill 内部、对话中途都能用：
agent 会补上你缺的 context、用平实语言重新表述、并使用 `CONTEXT.md` 里的词汇。

> 它**事后**生效。根本解法是前置的：早早用 `grill-with-docs` 建立共享语言。

### 4. `to-questionnaire` —— 卡点在别人脑子里

当阻塞你的东西**不在你的头脑或 codebase 里**，而在**别人的**头脑里时：

- 它写一份 Markdown 问卷让对方填，可以异步填，也可以在一次会议里一起完成
- **它是 `grill-me` 的反向**：它不访问你关于主题，而是访问你关于**发送**——发给谁、你需要拿回什么，
  并把问题对准那个 gap
- **产出**：一份可直接发出去的问卷。拿回来的东西是 `grill-with-docs` 或 `to-spec` 的素材

### 5. 需要外部事实/调研时 → `research`

派后台 agent 去查，你继续干活。见 [01-kickoff](01-kickoff.md) 的 C。

## 需确认

- **边界处的选择要跟用户确认**——这是全流程里最模糊的决定，不要自己默默 `compact`
- `handoff` 前确认：有没有敏感信息需要剔除
- `to-questionnaire` 前确认：**发给谁、要拿回什么**（这两个决定了问卷长什么样）

## 常见坑

1. **阶段中途 compact。** 会把未完成的思考压成模糊的摘要。在边界处做。
2. **在 grilling → spec → tickets 这条链中间 clear。** 这条链必须连续，
   否则 spec 和 tickets 不是建立在同一组思考上。
3. **handoff 写进 repo。** 它是便携文档，应该进系统临时目录。
4. **handoff 里重复粘贴 spec 内容**。用引用，别复制。
5. **靠"我记得上次说过"继续。** 新 session 什么都不记得——该写进 `CONTEXT.md` 的要写进去。

## 边界

- 要开始一个新阶段 → 看对应阶段的配方（01–11）
- 不确定该用哪个 skill → `/ask-matt`
