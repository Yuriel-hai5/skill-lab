# 09 · 学习

## 适用信号

- "教我这个概念 / 这个技术栈"
- "我要准备面试 / 答辩 / 考试"
- "我想系统地学一遍 X"
- "给我出点练习题"
- 想真正掌握（而不是"看过一遍感觉会了"）

## 配方

### 主路线：`teach`

它是 **stateful** 的——把当前目录当成学习工作区，跨多个 session 持续教一个 topic。

**它会建立这套文件结构：**

| 文件 | 作用 |
|---|---|
| `MISSION.md` | 记录**你为什么**对这个 topic 感兴趣。所有教学都以它为 grounding |
| `RESOURCES.md` | 可探索的高质量资源列表（**先填这个**，别相信模型的记忆） |
| `reference/*.html` | 从课程里压缩出的速查材料（cheat sheet、语法、算法、术语表），适合打印 |
| `lessons/0001-*.html` | **主要教学单元**：一个自包含 HTML，教一个与 mission 绑定的窄主题 |
| `learning-records/0001-*.md` | 记录你已学到的东西（相当于学习界的 ADR），用来计算最近发展区 |
| `assets/*` | 跨课程复用的组件 |
| `NOTES.md` | 记你的偏好和工作笔记 |

**教学理念**（它明确区分两件事）：

- **Fluency strength**：当下能提取知识的能力 → 会给你"我掌握了"的错觉
- **Storage strength**：长期保持的能力 → **这才是真目标**

用 **desirable difficulty** 设计课程来建立 storage strength：
**retrieval practice**（从记忆里回忆）+ **spacing**（分散练习）+ **interleaving**（混合相关主题，仅用于技能练习）。

> 在 `RESOURCES.md` 填充充分之前，重点应该是**找高质量资源**获取 knowledge。
> **不要相信模型的参数化知识。**

### 想练手 → 配练习

- **`scaffold-exercises`**：创建含章节、题目、答案、讲解的练习目录结构，并确保通过 linting

### 毕设答辩特化

1. `teach` 建 workspace，`MISSION.md` 写清"答辩要讲什么、听众是谁"
2. `learning-records/` 记录你已经能讲清楚的部分，避免重复练已经会的
3. 用 `research` 补充领域事实（对照一手来源，别用模型记忆）
4. 需要做演示稿 → `slides`（HTML 演示稿 + Chart.js）

## 需确认

- **先确认 MISSION**：为什么学这个、学来干什么。它决定所有内容的选择
- 确认是**偏 knowledge**（如理论物理）还是**偏 skill**（如乐器、编程）——两类内容设计完全不同
- 多 session 学习时，每个 session 开始先读 `learning-records/` 确定当前水平

## 常见坑

1. **跳过 `RESOURCES.md` 直接讲。** 模型的参数化知识可能过时或错误，先找权威资源。
2. **把 fluency 当掌握。** 读完觉得懂了 ≠ 一周后还记得。要靠 retrieval practice 检验。
3. **不记 learning records。** 下个 session 会重复教已经会的东西。
4. **一次教太宽。** 一个 lesson 只教一个与 mission 绑定的窄主题。
5. **练习没有反馈。** 题目要带答案和讲解，否则练了也不知道对不对。

## 边界

- 只是查一个事实 → `research` 或 `ui-ux-pro-max`（设计类）
- 要学的是"怎么写代码"这种工程能力 → 直接做项目 + [05-implementation](05-implementation.md)，边做边学
