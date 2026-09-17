# 01 · 起步 / 方向

## 适用信号

- "我不知道要做什么"、"题目还没定"、"方向没想好"
- "想法很大但不知道从哪开始"、"路径看不清"
- 需要先搞清楚**外部事实**才能决定做什么（技术选型、有没有现成方案）
- 毕设开题、新项目启动、接一个陌生领域的需求

## 先分流：是「缺决策」还是「缺事实」

| 症状 | 走哪条 |
|---|---|
| 有明确目标，但中间该怎么做全是未知 | **路径模糊** → 用 `wayfinder` |
| 想做的事有很多候选，不知道选哪个 | **决策未定** → 用 `grill-me` / `grill-with-docs` |
| 缺的是资料、现成方案、技术可行性 | **缺事实** → 用 `research` |

## 配方

### A. 路径模糊 —— 一个 session 装不下的大块工作

1. **`wayfinder`**（主导）
   - 先在 issue tracker 上建一张 **map**（`Destination` / `Notes` / `Decisions so far` / `Not yet specified` / `Out of scope`）
   - 把路径上的未知拆成 **decision tickets**，每个只解决一个决策，标 blocking 关系
   - 逐个解决 frontier 上的 ticket（open + unblocked + unclaimed）
   - **产出**：`.scratch/<effort>/map.md` + `issues/NN-*.md`
   - **重要**：wayfinder 产出 **decisions，不是 deliverables**。地图清晰后它 hand off，不自己 build

2. map 清晰后 → **`to-spec`** 把互相链接的决策收束成可构建计划
3. 然后接 [04-planning](04-planning.md)

> **别用 wayfinder 做范围明确的功能。** 它更慢、认知负担最重，只给真的一个 session 装不下的 effort。
> 能塞进一个 session 的想法走 B。

### B. 决策未定 —— 想法能塞进一个 session

1. **有 repo** → `grill-with-docs`（访谈 + 就地写 `CONTEXT.md` 和 ADR）
   **没 repo** → `grill-me`（同样的访谈，不留文件）
2. 如果某个问题**必须跑起来才能回答**（状态机对不对、UI 长什么样）→ 绕行：
   `handoff` 导出 → `prototype` 回答 → `handoff` 把结论带回来
3. **产出**：`CONTEXT.md`（领域词汇）+ `docs/adr/*.md`（难逆转的决策）

### C. 缺事实

1. **`research`**（后台 agent，它读的时候你可以继续干别的）
   - 对照 **primary sources**：官方文档、源码、spec、第一方 API，不要二手解读
   - 每个 claim 标注来源
   - **产出**：repo 里一份带引用的 Markdown

2. 拿回来的材料 **带进 B**（`grill-with-docs`）——research 提供思考材料，不取代思考

## 需确认

- **先问一个问题**：你现在是「完全没方向」还是「有几个候选在纠结」还是「有方向但中间路径不清」？
  三种情况的配方完全不同，别猜。
- wayfinder 的 **Destination** 必须先跟用户确认（它决定每张 ticket 的形状）。

## 常见坑

1. **跳过这一步直接写代码。** 这是最贵的错误——方向错了，后面每一步都在放大错误。
2. **拿 wayfinder 做小功能。** 范围明确的东西直接用 `to-spec`。
3. **research 的产出当结论用。** 它是材料，决策仍然要在 grilling 里做。
4. **在 map 还没清晰时就想 build。** 那种"想直接做"的冲动通常说明你到了地图边缘，该 hand off 了。

## 边界

- 已经清楚要做什么、只是不知道怎么拆 → 不要用本配方，直接 [04-planning](04-planning.md)
- 只是想知道"用哪个 skill" → `/ask-matt`
