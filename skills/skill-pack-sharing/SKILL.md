---
name: skill-pack-sharing
description: 把本机自建的 skill 打包成可分享的压缩包，让别人的 agent（WorkBuddy / Claude Code / Codex 等）能直接拖进对话完成安装。当用户说“打包这个 skill 分享给他人 / 发给别人 / 别人也能用 / 导出 skill / 做成压缩包分享”，或要把 skill 交给别人安装时使用。覆盖去硬编码、写 AGENTS.md 任务书、双版本目录探测、可移植性校验、端到端模拟测试。
---

# Skill Pack Sharing — 把 skill 打包给别人用

**核心难点不是压缩，是"别人的 agent 拿到后能不能自己装对"。**

本机跑得好好的 skill，直接打包发出去通常会坏在三处：

| 坏点 | 症状 |
|---|---|
| 硬编码本机路径 | 对方机器上没有那个路径，命令全失败 |
| 脚本依赖某个特定 skill 存在 | 对方没装 → 脚本直接报错 |
| 没说清"装到哪" | agent 解压到工作区就完事，skill 永远不生效 |

按下面 7 步走。

---

## 第 1 步：扫描硬编码（先扫再改）

```bash
grep -rn "C:/Users/\|C:\\\\Users\\\\\|/Users/\|/home/" <skill-dir> 2>/dev/null
grep -rn "~/\.workbuddy\|~/\.claude\|~/\.config" <skill-dir> 2>/dev/null
```

**只替换"本机专有"的路径**，不要无脑全替换：

- ✅ 该换：`C:\Users\<你>\.workbuddy-ai\skills\ui-ux-pro-max\scripts\search.py`
  → `<skills-dir>/ui-ux-pro-max/scripts/search.py`
- ❌ 不该换：版本对照表里**故意**写出的双版本路径（那是给人看的说明）

### 占位符方案：`<skills-dir>`

把本机专有前缀换成 **`<skills-dir>`**，并在 SKILL.md 里说明怎么推断：

> 取本 `SKILL.md` 自己所在目录的**父目录**——它就在 skills 目录下面。

**不要**在打包时把占位符替换成对方路径——你不知道对方路径，而且对方可能换版本。
让**运行时的 agent** 自己换。

### 同级 skill 引用用相对路径

skill A 引用 skill B 的文件，用 `../<skill-b>/path/to/file.md`，
不要用 `~/...` 或绝对路径。

---

## 第 2 步：脚本自包含化

打包的脚本**不能依赖"某个 skill 一定存在"**。让脚本从自身位置推断路径：

```python
_HERE       = os.path.dirname(os.path.abspath(__file__))   # .../<skill>/scripts
_SKILL_DIR  = os.path.dirname(_HERE)                        # .../<skill>
_SKILLS_DIR = os.path.dirname(_SKILL_DIR)                   # .../skills
```

再加一个 `--skills-dir` 参数做覆盖（**注意：所有内部函数都要用传入的值，别再用模块级默认值**——
这是个真踩过的坑，函数里写死默认值会让参数形同虚设）。

### 脚本输出要"对方友好"

对方 skill 集不同 → 脚本报"缺 N 个依赖"是**必然的**，不是错误。
输出必须写清：

```
配方引用校验：有 42 个点名的 skill 本机未安装
  —— 这不是错误。缺 skill 时按 references/00-skill-map.md 降级即可，顺序不变。
```

否则对方以为装坏了。

---

## 第 3 步：写 `AGENTS.md`（**最关键的一步**）

放在**包根**。这是给对方的 agent 看的任务书。

### 必须包含

1. **开门见山消歧义**——"装上"到底指什么：

   > ⚠️ 先把"装上"理解清楚：指的是**把 skill 复制到 skills 目录，让它以后能被调用**——
   > **不是**"解压到工作区看看"，**不是**"读一遍写个总结"，**不是**"介绍这个包有什么"。

   并给出触发措辞白名单（"帮我装上" / "这是我找到的 skill，装上" / "安装一下"）。

2. **目标目录探测**（含平局判据，见第 4 步）

3. **分步执行**：解压 → 复制 → 跑索引/初始化 → 处理可选项

4. **冲突保护**——**给可执行检查，不要只写"先问用户"**：

   ```bash
   for s in <skill-a> <skill-b>; do
     [ -e "<skills-dir>/$s" ] && echo "冲突: $s 已存在"
   done
   ```

   有输出就停下问用户。原因：`cp -r` 遇到同名目录**不报错**
   （GNU cp 嵌套一层，MSYS/Git Bash 静默合并），agent 不检查就会悄悄覆盖用户的改动。

5. **必须转达的收尾**：

   > **skill 在对话开始时加载，当前对话不会生效。必须新开一个对话。**
   > 这一步 agent 替用户做不了，**不许省略**。

6. **边界**（不要做的事）：不改其他 skill、不删用户已有内容、不做占位符全局替换。

---

## 第 4 步：目录探测要处理"两个都存在"

同一产品可能有多个版本目录，且**安装包常会同时建出两个**（其中一个是空的）。

```
C:\Users\<你>\.workbuddy-ai\skills\   ← 国际版
C:\Users\<你>\.workbuddy\skills\      ← 国内版
```

**判断规则**（写进 AGENTS.md）：

| 探测结果 | 怎么做 |
|---|---|
| 只有一个存在 | 装那个 |
| 两个都有**且都有内容** | ⚠️ **停下来问用户**，不要自己猜 |
| 两个都存在但只有一个非空 | 装非空那个 |
| 都不存在 | 问版本，手动建 `skills` 目录 |

**平局判据**（给建议，不替用户决定）：

```bash
ls -ldt "$USERPROFILE/.workbuddy-ai" "$USERPROFILE/.workbuddy"
```

修改时间新的那个通常是他在用的。

---

## 第 5 步：三处冗余，别只写 README

**不确定对方的 agent 会先看哪个文件、会不会解压**，所以提示要冗余三份：

| 位置 | 内容 | 为什么 |
|---|---|---|
| **zip 文件名** | `xxx-pack（先读AGENTS.md）.zip` | agent **解压前**就能从文件名看到 |
| **包根 `AGENTS.md`** | 完整任务书 | agent 的约定入口文件名 |
| **`README.md` 顶部** | HTML 注释：`🤖 如果你是 AI agent，先读 AGENTS.md` | README 也是 agent 常读的名字 |

README 本身写给**人**看：怎么手动装、怎么用、FAQ、依赖说明。

---

## 第 6 步：端到端模拟测试（**别跳**）

在临时目录里**扮演收件人**跑一遍，不要只信"文件复制成功了"：

```bash
SB="$(mktemp -d)/dragtest"          # 用系统临时目录，别写死版本相关路径
mkdir -p "$SB/attachments" "$SB/fake-skills"
cp <zip> "$SB/attachments/"                    # 模拟拖入
unzip -q "$SB/attachments/<zip>" -d "$SB/extracted"
cp -r "$SB/extracted/<pack>/<skill-a>" "$SB/fake-skills/"
python "$SB/fake-skills/<skill-a>/scripts/<script>.py"
```

> Windows / Git Bash 下 `mktemp -d` 可用；若要固定位置，用 `<skills-dir>/../tmp`，
> **不要**写死 `~/.workbuddy-ai/`（那是国际版专有，自己先违反了第 1 步的规则）。

### 至少测三个场景

| 场景 | 期望 |
|---|---|
| **最小安装**（只有本包的 skill，零配套） | 脚本不报错，缺依赖提示友好 |
| **全量安装**（本机真实 skills 目录） | 校验通过 |
| **从不同子目录执行脚本** | 路径自动推断正确 |
| `--skills-dir` 等参数 | 真的生效（不是摆设） |

跑完**清理临时目录**。

---

## 第 7 步：打包与校验

用 Python `zipfile`（跨平台、能控压缩级别、能自校验）：

```python
import os, zipfile
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for root, dirs, files in os.walk(src):
        dirs.sort(); files.sort()
        for f in files:
            p = os.path.join(root, f)
            z.write(p, os.path.relpath(p, base))   # 保留顶层目录名
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
```

### 打包前排除

- ❌ **机器特定的生成物**（索引文件、缓存、构建产物）——对方的环境不同，这些是错的
- ❌ `.git/`、`node_modules/`、临时文件
- ✅ 保留：SKILL.md、references/、scripts/、AGENTS.md、README.md

### 第三方内容要查许可

包里若含**修改过的第三方文件**（比如改了别人的 skill），先查上游 license：

```bash
curl -sL "https://api.github.com/repos/<owner>/<repo>" | grep -i '"license"' -A3
```

MIT/Apache → 可分发，但**要在包内标注来源和修改说明**。

---

## 交付给用户时要说清

1. **zip 在哪**、多大、多少个文件
2. **对方怎么说**：最低限度「帮我装上」；更稳「按包里的 AGENTS.md 帮我装上」
3. **唯一 agent 替不了的一步**：装完要新开对话
4. **零硬依赖声明**：缺配套 skill 也能用，降级路径在哪

---

## 常见坑

| 坑 | 后果 | 对策 |
|---|---|---|
| 只改了 SKILL.md，漏了 references/ 里的路径 | 配方执行到某步才炸 | 全目录 grep，不只 grep 主文件 |
| 脚本函数里用模块级默认路径，忽略 `--skills-dir` | 参数形同虚设 | 所有路径参数透传，别在函数里回退默认值 |
| 把机器特定的索引文件打进包 | 对方看到别人的 skill 清单，误导 | 打包前删掉，让对方跑脚本生成 |
| 只说"复制到 skills 目录" | agent 不知道 skills 目录在哪 | 给出探测命令 + 平局判据 |
| README 写"必须说某句魔法话" | 显得脆弱，劝退分享对象 | 改软：说 X 通常够，加一句更稳 |
| 替换了版本对照表里的"故意路径" | 说明文字失去意义 | 先判断这处路径是"代码"还是"文档" |
| 打包后没模拟测试 | 对方装完才发现脚本炸了 | 第 6 步别跳 |
| 只写"已存在就先问用户"，没给检查命令 | agent 直接 `cp -r`，**静默覆盖或嵌套**——`cp` 遇到同名目录**不报错**（GNU 嵌套一层，MSYS/Git Bash 静默合并） | 必须给可执行的冲突检查 `for` 循环，让 agent 真的先查 |

---

## 边界

- **不要**为了让包"干净"去删用户的 skill 或改别人的包
- **不要**在包里塞二进制/大文件——skill 包应该轻（几十 KB 到几 MB）
- 用户只是问"能不能这样分享"时，**先回答可行性再动手**，别直接开始打包
