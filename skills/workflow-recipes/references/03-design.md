# 03 · 设计

## 适用信号

- "要做一个界面 / 页面 / 后台 / 落地页"
- "现在这个界面看起来很廉价 / 不够高级 / AI 味重"
- "加点动效 / 动画 / 让它活起来"
- "该用什么配色 / 字体 / 图表"
- "我要定视觉方向"

## 先分四条路（选错全盘错）

| 情况 | 走哪条 |
|---|---|
| 从零做新界面 / 新页面 | **A · `finesse-ui`** |
| 界面已完成，要升级质感 + 动效 | **B · `ui-upgrade`** |
| 只是要查一个设计事实（配色/规范/技术栈） | **C · `ui-ux-pro-max`** |
| 要特定风格（落地页/作品集/极简/粗野） | **D · `taste-skill` 系列** |

## A. 从零做 —— `finesse-ui`

1. **先定 register**（这是它的核心分流，必须先确定）：
   - **brand**：landing、品牌站、发布页、作品集 → 优化 spectacle + soul + 第一印象
   - **product**：dashboard、admin、分析、数据表、app 壳 → 优化清晰 + 密度 + 可用
   - **commerce**：PDP / PLP / 购物车 / 结账
   - **h5**：只在手机上存在的页面（390×844 固定框 + 安全区 + 原生家具）
2. 设三个旋钮：`SOUL` / `SPECTACLE` / `DENSITY`（product register 强制 SPECTACLE 低、DENSITY 高）
3. product register 再细分：**pages you READ**（dashboard）→ **pages you OPERATE**（向导/后台/设置）→
   **pages you DELEGATE**（AI 工作台/agent console，失败方式是**不可信**）
4. 交付前跑 `anti-cheap.md` + `mobile-floor.md` + `preflight.md`
5. **产出**：页面代码 + `.finesse/log.json`（反重复记忆，下次自动轮换风格）

> **铁律**：dashboard 不是"带图表的品牌页"。禁止把 grain / vignette / 巨型 hero 字体 / hero 引擎灌进产品界面。

## B. 已有界面升级 —— `ui-upgrade`（自动触发，不用点名）

用户说"升级质感 / 加动效 / 看起来不够高级"时直接用它。它内部编排：

1. 锁定三个变量（register / 技术栈 / 现状痛点）
2. `impeccable audit` + `critique` → **产出**问题清单
3. 按 `finesse-ui/references/anti-cheap.md` 硬禁项 + 工艺底线升级质感
4. 按 `motion.md` 门禁四项 + 六路线（R1→R6，停在第一条能胜任的）加动效
5. `impeccable polish` 收尾，有界验证（最多两轮）
6. **产出**：「改了什么 / 没动什么 / 降级表现」三段说明

**动效要点**：只动 `transform` 和 `opacity`；`prefers-reduced-motion` 要设计成**静止帧**而不是"关掉"；
元素要在**终态**下编写、从别处动过来，否则降级时永久不可见。

## C. 查设计事实 —— `ui-ux-pro-max`

```
python <skills-dir>/ui-ux-pro-max/scripts/search.py "<查询>" --domain <域>
# 域: style | product | color | typography | chart | icons | ux | gsap | landing
python .../search.py "<关键词>" --stack <栈>        # react / vue / nextjs / flutter / wpf …
python .../search.py "<产品> <行业>" --design-system  # 整站设计系统（新项目必做）
```

**一次只查一个主导意图**，2–5 个有意义关键词 + 一个约束。结果不对就换更窄的写法重试**一次**，
还不行就承认没查到，**不要凭记忆编配色**（编出来的一定是蓝色）。

库里有什么：79 风格（50 active）· 192 产品配色 · 74 字体搭配 · 119 条 UX 规范 · 105 图标 · 17 GSAP 预设 · 25 图表 · 22 技术栈。

## D. 特定风格 —— `taste-skill` 系列

- **`taste-skill`**：落地页 / 作品集 / 改版，三个旋钮 `VARIANCE`/`MOTION`/`DENSITY`（默认 8/6/4）
- **`minimalist-skill`**：暖单色编辑风 · **`brutalist-skill`**：瑞士印刷 × 军用终端
- **`soft-skill`**：高端 agency 质感 · **`redesign-skill`**：审计先行升级已有站点
- **`stitch-skill`**：生成 DESIGN.md · **`output-skill`**：反截断，强制完整输出

它要求先给一行 **Design Read**（页面类型 / 受众 / 调性 / 设计系统），再动手。

## 方法论补充（读了提升判断力）

`interface-design` —— 产品界面（dashboard/admin/SaaS）方法论，97K 单文件。核心：
- 动手前产出四样：**Domain**（≥5 个世界词汇）、**Color world**（≥5 个自然色）、
  **Signature**（只可能属于这个产品的元素）、**Defaults**（这类界面 3 个显而易见的选择）
- 检验：**把产品名去掉读方案，别人能看出它是干嘛的吗？**
- 写每个组件前声明 Intent / Hierarchy / Palette / Depth / Surfaces / Typography / Spacing

## 常见坑

1. **不分 register 就动手。** 后台用品牌页语法（大 hero、grain、暗色默认）= 一眼假。
2. **凭记忆编配色。** 查 `ui-ux-pro-max`，别猜。
3. **同时让 finesse 和 impeccable 主导。** 两个都是端到端流程，选一个主导，另一个只借检查清单。
4. **为 4 行效果引入 60KB 依赖。** 动效从 R1（CSS）开始选，停在第一条能胜任的路线。
5. **动效删掉后页面就不可用。** 那说明动效成了结构，是 bug 不是特性。

## 边界

- 需求还没对齐就谈视觉 → 先走 [02-alignment](02-alignment.md)
- 界面结构本身要重做（不是升级）→ `impeccable` 的 redesign 路径 或 `redesign-skill`
