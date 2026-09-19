# 给 AI Agent 的安装指令

**用户给了你一个仓库链接**，或者**把压缩包拖进了对话** —— 两种情况下意思都一样：**「帮我装上」。**

⚠️ **先把"装上"理解清楚**：它指的是
**把 skill 复制到 WorkBuddy 的 skills 目录，让它以后能被调用**——
**不是**"解压到工作区看看"，**不是**"读一遍写个总结"，**不是**"介绍这个仓库有什么"。

判断依据：用户说「帮我装上」「这是我找到的 skill，装上」「安装一下」，
或者**只是丢了一个链接过来**（那也等于"帮我装上"）—— 全都按本文件执行。

按下面 5 步执行。**不要跳过第 0 步和第 5 步。**

---

## 第 0 步：确定目标目录（必做，不要猜）

WorkBuddy 有两个版本，skills 目录不同：

| 版本 | 目录 |
|---|---|
| 国际版 | `C:\Users\<用户名>\.workbuddy-ai\skills\` |
| 国内版 | `C:\Users\<用户名>\.workbuddy\skills\` |

**探测**（Windows，用 bash 或 PowerShell）：

```bash
ls -d "$USERPROFILE/.workbuddy-ai/skills" "$USERPROFILE/.workbuddy/skills" 2>/dev/null
```

**判断规则**：

| 探测结果 | 怎么做 |
|---|---|
| 只有一个存在 | 装那个 |
| 两个都存在**且都有内容** | ⚠️ **停下来问用户**："你两个版本都在用，装哪个？还是两个都装？"（这种情况真实存在，不要自己猜） |
| 两个都存在但只有一个是空的 | 装有内容的那个，顺带提一句另一个是空的 |
| 都不存在 | 问用户用的是哪个版本，然后手动建 `skills` 文件夹 |

**平局时的建议依据**（给用户做参考，别替他决定）：比一下两个目录的修改时间，新的那个通常是他在用的：

```bash
ls -ldt "$USERPROFILE/.workbuddy-ai" "$USERPROFILE/.workbuddy"
```

> macOS / Linux：`~/.workbuddy-ai/skills/` 或 `~/.workbuddy/skills/`，同样规则。
> 注意两个目录都存在不代表两个都在用——很多安装包会同时建出来，其中一个是空的。

---

## 第 1 步：拿到文件（两种入口，先看清是哪种）

### 入口 A · 用户给了**仓库链接**（GitHub）

克隆或下载都行。**`git clone` 在部分网络下会挂死**，挂死就换 codeload：

```bash
# 方式一：浅克隆（有 git 时首选）
git clone --depth 1 <仓库地址> <临时目录>

# 方式二：下 zip（clone 挂死 / 没装 git 时用这个）
curl -sL --max-time 180 -o pack.zip <仓库地址>/archive/refs/heads/main.zip
unzip -q pack.zip -d <临时目录>
```

> 仓库地址形如 `https://github.com/<owner>/<repo>`。
> 下完 zip 用 `unzip -t pack.zip` 验一下完整性。

### 入口 B · 用户拖了**压缩包**

```bash
unzip -q <压缩包路径> -d <临时目录>
```

（没装 `unzip` 就用 Python 的 `zipfile`。）

### 拿到之后：先找 skill 在哪

⚠️ **两种入口的目录结构不一样**，别搞混：

| 入口 | skill 在哪 |
|---|---|
| A · 仓库链接 | `<仓库根>/skills/` 下面 |
| B · 压缩包 | 包根目录下（和 `AGENTS.md` 同级） |

**怎么判断哪些是 skill**：skill 目录的特征是**里面有 `SKILL.md`**。

```bash
find <上面那个目录> -mindepth 2 -maxdepth 2 -name SKILL.md | grep -v '/optional/'
```

每条输出是 `<源目录>/<skill 名>/SKILL.md`，它的父目录名就是 skill 名
（数量可能变，以实际为准）。**`optional/` 下面的不算** —— 那是可选增强，见第 4 步。

---

## 第 2 步：复制所有 skill

### ⚠️ 先做冲突检查（**别跳过**）

```bash
# SRC = 第 1 步找到的 skill 源目录
#   入口 A（仓库）   → SRC=<仓库根>/skills
#   入口 B（压缩包） → SRC=<解压目录>/workflow-recipes-pack
SRC=<skill 源目录>

SKILLS=$(find "$SRC" -mindepth 2 -maxdepth 2 -name SKILL.md \
         | grep -v '/optional/' | xargs -n1 dirname | xargs -n1 basename | sort -u)

for s in $SKILLS; do
  [ -e "<skills-dir>/$s" ] && echo "冲突: $s 已存在"
done
```

**只要有任何一行输出"冲突"，就停下来问用户**：
「`<skills-dir>` 下已经有 `xxx`，是你自己改过的版本吗？要覆盖还是换个名字装？」

**为什么必须显式检查**：`cp -r` 在目标同名目录已存在时**不会报错**——
GNU cp 会嵌套一层，MSYS/Git Bash 的 cp 会**静默合并**（旧文件保留、同名文件被覆盖）。
两种行为都不会给你任何提示，等用户发现时旧版本已经被动过了。

### 检查通过后再复制

```bash
for s in $SKILLS; do
  cp -r "$SRC/$s" "<skills-dir>/"
done
```

装完应该长这样（以本包实际内容为准）：

```
<skills-dir>/
├── workflow-recipes/
│   ├── SKILL.md
│   ├── references/     （配方文件）
│   └── scripts/
├── ui-upgrade/
│   └── SKILL.md
└── skill-pack-sharing/     ← 若本包包含
    └── SKILL.md
```

---

## 第 3 步：生成全局索引（推荐）

```bash
python "<skills-dir>/workflow-recipes/scripts/rebuild-index.py"
```

脚本会：
- 扫描整个 skills 目录，生成 `GLOBAL-INDEX.md`（列全部已装 skill、来源包、用途分组）
- 校验配方引用的 skill 是否都在

**看到「有 N 个配方点名的 skill 本机未安装」不是错误**——配方正文自带方法论，
缺的 skill 按 `references/00-skill-map.md` 降级即可。把这句话转达给用户，别让他以为装坏了。

---

## 第 4 步：`optional/` 是可选的，先问用户

`optional/ask-matt-global-index/` 是给**已装 `vinvcn/mattpocock-skills-zh-CN`** 的人用的，
把 `ask-matt` 从"只查自己包内 29 个"升级成"查全部已装 skill"。

- 用户装了 mattpocock 包 → 读 `optional/ask-matt-global-index/README.md` 按说明装
- 没装 → **跳过，并告诉用户这一项用不上**

不要不问就装。它会覆盖用户的 `ask-matt/SKILL.md`。

---

## 第 5 步：告诉用户「新开一个对话」（必做，别漏）

**skill 在对话开始时加载。当前这个对话不会生效。**

装完必须明确告诉用户：

> 装好了。**新开一个对话**才会加载——已开着的对话读不到新 skill。
> 验证方法：新对话里输入 `/`，列表里能看到 `workflow-recipes` 和 `ui-upgrade`。

---

## 关于 `<skills-dir>` 占位符

包内文件里会出现 **`<skills-dir>`** 这样的占位符，例如：

```
python <skills-dir>/workflow-recipes/scripts/rebuild-index.py
```

**这是设计意图，不要做全局替换。** 它是给未来的 agent 看的——
每次执行时按当前机器把占位符换成真实路径。SKILL.md 里写了怎么推断：
取 SKILL.md 自己所在目录的父目录。

---

## 边界（不要做的事）

- ❌ 不要改 `<skills-dir>` 下**其他** skill 的任何文件
- ❌ 不要删用户已有的 skill
- ❌ 不要为了"装干净"去清空 skills 目录
- ❌ 不要覆盖同名目录而不问
- ❌ 不要跳过第 5 步（不告诉用户新开对话，等于没装）

## 装完给用户的一句话总结（模板）

> 装好了：`<把实际装的 skill 名字列出来>` 已放进 `<实际路径>`。
> 索引已生成，本机共 N 个 skill。
> **新开一个对话生效**——之后你直接说处境就行，不用记 skill 名字，例如
> 「我界面做完了想升级质感和加动效」或「代码能跑但越改越乱，想重构」。
