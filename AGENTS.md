# AGENTS.md — 给 AI 的项目约定

在这个项目里干活前先读这个文件。**这里的规矩优先于你的默认习惯。**

---

## ⚠️ 动手前：先扫技能库（别跳）

改这个项目的代码之前，先读本机 skill 索引 —— 很多 skill 是**按症状**命名的。
不扫，它们永远不会被用上。

读 `<skills-dir>/workflow-recipes/GLOBAL-INDEX.md`
（本机是 `C:\Users\<你的用户名>\.workbuddy-ai\skills\`；
如果它和 skills 目录对不上，先跑同目录的 `scripts/rebuild-index.py` 重建）。

| 你要做的事 | 先看哪个 skill |
|---|---|
| 改 skill 的写法 / 加配方 / 改 `description` | `writing-for-agents`（给 agent 写文档的 reference）；内置 `skill-creator` |
| 打包 skill 分享给别人 / 改 `pack/` | `skill-pack-sharing` |
| 用户描述处境、问"我现在该怎么做" | `workflow-recipes` |
| 改界面 / 做视觉设计 | `ui-upgrade` |

**为什么写死这条**：2026-09-20 实测 —— 在另一个项目里，`workflow-recipes` 的
`description` **已加载**（AI 复述出了新版独有措辞），但全程没查技能库，
把已装的 `wpf-visual-bug-triage` 里**已经写着**的东西重新推导了一遍。
事后自述：「**没查。这是我的疏漏。**」
**skill 不被读，等于不存在。**

> 出处：`skills/workflow-recipes/references/11-setup-docs.md` 的**配方 G**。

---

## 这是什么项目

`skill-lab` —— 荆丝的 agent skill 工坊。**skill 的源码在这里，不在对话里。**

为什么建：skill 是在对话里做出来的，但对话会删、会翻不到。所以把源码落到硬盘，
当正式项目维护 —— 有版本号、有历史、能回滚、能打包。

---

## 目录职责

| 目录 | 职责 | 能不能改 |
|---|---|---|
| `skills/` | **skill 源码，唯一源头** | ✅ 改 skill 只改这里 |
| `pack/` | 分享打包素材（收件人 agent 任务书 + 说明 + 打包脚本） | ✅ |
| `scripts/` | 部署 / 新建 skill 等工具脚本 | ✅ |
| `docs/` | 路线图、待改进清单、设计笔记 | ✅ |

**`~/.workbuddy-ai/skills/` 是部署目标，不是源头。** 不要直接改它。

---

## 铁律

### 1. `skills/` 是源头

```
skills/                          ← 改这里
   ↓  python scripts/deploy.py
~/.workbuddy-ai/skills/          ← WorkBuddy 读这里
```

直接改部署目录 → 项目源码落后 → 下次部署覆盖掉你的改动。

### 2. skill 文件里不许有本机绝对路径

❌ `C:\Users\<你的用户名>\.workbuddy-ai\skills\ui-ux-pro-max\scripts\search.py`
✅ `<skills-dir>/ui-ux-pro-max/scripts/search.py`

需要指代 skill 安装目录时用 **`<skills-dir>`**，并在 SKILL.md 里说明怎么推断
（取 SKILL.md 自己所在目录的父目录）。

**例外**：README / 路线图这类**给人看的说明**里可以写具体路径，那些不参与分发。

### 3. 同级 skill 互相引用用相对路径

`../<skill-b>/references/xxx.md`，不要用 `~/...` 或绝对路径。

### 4. 改完必须做四件事

1. 更新 `CHANGELOG.md`（写清**改了什么**，别写 "update"）
2. 升 `VERSION`（四级规则见下）
3. `python scripts/deploy.py`
4. **告诉用户"新开一个对话才生效"** —— 这一步你替不了他

### 5. 版本号四级 `x.x.x.x`

| 位 | 什么时候加 | 例子 |
|---|---|---|
| 主 `X.0.0.0` | 不兼容改动、架构重构、大改版 | 配方结构全重写 |
| 次 `x.X.0.0` | 新增配方 / 新增 skill / 新增能力 | 加了 `12-thesis.md` |
| 修订 `x.x.X.0` | 修 bug、改错字、补说明 | 修了一个错字 |
| 构建 `x.x.x.X` | 自动生成，**不手动管** | — |

### 6. 部署后自动重建全局索引

`deploy.py` 会跑 `rebuild-index.py`。如果没跑，手动跑：

```bash
python "<skills-dir>/workflow-recipes/scripts/rebuild-index.py"
```

### 7. 已知限制：deploy 只增改，不删

`deploy.py` **不会删除**部署目录里的东西。所以：

- 你在 `skills/` 里**删掉**一个 skill → 部署目录里的旧副本**还在**
- 你把 skill **改名** → 旧名字的副本**还在**

**要彻底删，得手动删部署目录里的那份**：

```bash
rm -rf "<skills-dir>/<已废弃的skill名>"
```

`deploy.py` 的设计是**宁可留垃圾也不误删**——它不碰任何它不认识的 skill
（部署目录里还有 40+ 个别人装的 skill，误删代价太大）。

---

## 干活时的注意

### 用户是这个项目的作者，不是外行

他是计算机科学与技术专业的学生。**该用术语就用术语，别过度简化。**
他不亲自逐行写代码是工作方式偏好，不是能力问题。

### 一次只问一个问题

需要确认时，问**一个**最关键的问题，别列一串。能自己查的（文件、代码、目录）自己去查。

### 改动前先说清计划

「我打算改 X → Y，因为 Z。可以吗？」—— 让他能判断这条路对不对，再动手。

### 别自作主张删东西

- 删文件前先问
- 不要为了"干净"去删 skill 或打包产物
- 桌面上其他文件夹与本项目无关，**不要碰**

### git

**提交前先问，不要自动提交、不要自动推送。** 没有例外。

---

## 当前状态

- 版本：**见 `VERSION` 文件** —— 不要在这里写死数字（写死的已经过期过一次）
- 3 个 skill：`workflow-recipes` / `ui-upgrade` / `skill-pack-sharing`

### 该读哪份文档

| 用户说什么 | 你先读 |
|---|---|
| "改 skill" / "按计划做" | **`docs/下次改动.md`** ← 已想清楚待做的，优先看这个 |
| "接下来做什么" / "有什么方向" | `docs/路线图.md`（4 个完善方向，含验收标准） |
| "记录一下" / 提到卡住的地方 | `docs/待改进.md`（追加，别覆盖） |
| "做到哪了" | `CHANGELOG.md` |

**下一步是"拿去用"，不是"继续加功能"。** 用过才知道要改什么。
