# 10 · 交付

## 适用信号

- "提交前帮我看看"
- "review 一下这个 branch / PR"
- "有 merge 冲突"
- "要发布了 / 要交付了"
- "这次改了什么，帮我写个说明"

## 配方

### 1. `code-review` —— 双轴审查

从**固定点**开始（commit / branch / tag / merge-base），两个轴线**并行**跑、并排报告：

- **Standards**：代码是否符合本仓库记录的编码标准？
- **Spec**：代码是否符合来源 issue / spec 的要求？

触发方式："review since X"、审查 branch / PR / 进行中的变更。

**产出**：两个轴线的审查结果并排呈现。

### 2. `resolving-merge-conflicts` —— 有冲突时

1. 查看当前 merge / rebase 状态，检查 git history 和冲突文件
2. **为每个冲突找到 primary source**：深入理解每个变更**为什么**产生、原始意图是什么。
   读 commit message、查 PR、查原始 issue / ticket
3. **逐个 hunk 解决**：尽可能保留双方意图。若二者不兼容，选择符合**本次 merge 目标**的一方，
   并**记录 trade-off**。**不要发明新行为。** **绝不 `--abort`**
4. 找到项目的 automated checks 并运行（通常是 typecheck / tests / format），修复 merge 引入的问题
5. 完成 merge / rebase：stage 全部并 commit；若在 rebase 中，继续直到所有 commit 完成

### 3. 提交

**提交前必须先问用户**，不要自动提交。

- 版本号按语义化规则：**主版本**（不兼容改动 / 架构重构）· **次版本**（向下兼容的新功能，对应一个阶段或迭代）·
  **修订号**（bugfix，发布前累积、发布时统一加一）
- 备注要写清**改了什么**，不要写 "update" 这种没信息量的词

### 4. 交付说明（给人看的）

```
## 改了什么
- [逐条，每条写"原来什么样 → 现在什么样"]

## 没动什么
- [明确说明保留了什么，让人放心]

## 怎么验证
- [跑什么命令、看什么结果]

## 已知限制 / 后续
- [还没做的、有风险的]
```

设计类交付另加一段「**降级表现**」：`prefers-reduced-motion` 下每个动效的静止帧是什么。

### 5. 推送失败时 → `github-push-via-api`

`git push` 报 502 / "server closed abruptly" 但 `api.github.com` 可达时用它：
通过 GitHub 的 Git Data API 重建同一个 commit，使生成的 SHA 与本地一致。

> 本机 `git clone` 直连 GitHub 会挂死，但 `codeload.github.com` 下 zip 正常——
> 拉代码优先用 `curl` 下 zip，别用 `git clone`。

## 需确认

- **提交前问用户**（每次都要问，不因为上次同意过就默认这次也同意）
- 冲突解决中若两边意图不兼容，**告诉用户你选了哪边、为什么**
- 版本号怎么变要跟用户说清（尤其涉及主版本）

## 常见坑

1. **没 review 就提交。** `implement` 内部已经带 review，手动写的代码要单独跑。
2. **`--abort` 掉冲突。** 那等于丢弃了一方的全部工作。永远不要。
3. **靠挑行解决冲突。** 要按 **intent** 解决，追溯到每侧的 primary source。
4. **冲突解决后不跑自动化检查。** merge 引入的问题往往在 typecheck / test 里才暴露。
5. **自动提交。** 每次都要先问。
6. **交付说明只写"改了 X"不写"没动什么"**。用户需要知道哪些是安全的。

## 边界

- 还没做完 → 回 [05-implementation](05-implementation.md)
- 提交后发现结构问题 → [07-refactoring](07-refactoring.md)
