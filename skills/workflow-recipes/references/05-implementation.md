# 05 · 实现

## 适用信号

- "照这个 spec 把功能做出来"
- "加一个新功能 / 新接口 / 新页面"
- "用测试驱动的方式写这段逻辑"
- 手里有 ticket，要开始写代码

## 配方

### 主路线：`implement`

它是编排型 skill，内部按固定顺序驱动下游：

1. 基于 spec 或 ticket 实现
2. **在预先约定好的 seams 上驱动 `/tdd`** —— 一次一个 red-green slice
3. 定期 typecheck，定期跑单个测试文件，最后跑完整测试套件
4. 完成后用 `/code-review` 审查这次工作
5. 提交到当前 branch

**产出**：可运行的代码 + 通过的测试 + 一次提交。

> **context 纪律**：每个 ticket 开一次 `implement`，从 **fresh session** 开始，只基于对应 ticket 工作。
> ticket 之间用 `/clear`。因为每个 ticket 自包含，最后一个的 context 可以丢。

### 只写一个具体行为 → 单独用 `tdd`

当没有完整 spec、只想 test-first 做一个 behavior 时：

- **只测预先认可的 seams**：写任何测试**前**，先写下要测哪些 seam 并跟用户确认。未经确认的 seam 不写测试
- **好测试的标准**：通过 public interface 验证 behavior，不碰 implementation details。
  代码可以完全重写而测试不该改。读起来像规格说明："user can checkout with valid cart"
- **三条反模式**（发现即回退）：
  - **实现耦合**：mock 内部协作者、测 private 方法、绕过 interface 直接查数据库
    → 特征是重构时测试失败但行为没变
  - **同义反复**：断言用和代码相同的方式重算期望值（`expect(add(a,b)).toBe(a+b)`）→ 天然通过，永远无法 disagree
  - **横切切片**：先写完全部测试再写全部实现 → 测的是想象的行为，对真实变化迟钝
- **循环规则**：red before green（先写失败测试，再写刚好让它通过的代码）；一次一个 slice；
  **refactoring 不属于循环**（归 code-review 阶段）

### 某个设计问题必须跑起来才知道 → `prototype`

- **logic 分支**（"这个状态模型感觉对吗"）→ 单个可分享 HTML，按钮 + 分页引导走查
- **UI 分支**（"这应该长什么样"）→ 同一路由上几个差异很大的变体，URL 参数 + 浮动底栏切换
- 规则：从第一天就是 throwaway、一条命令启动、默认不持久化、跳过 polish、每次操作后暴露完整 state
- **完成后 capture**：把验证过的决策折进真实代码，原型本身作为 **primary source** 留在非 main 的 branch 上

## 需确认

- **写测试前确认 seam**（`tdd` 的硬性要求）："公共接口是什么，我们要测哪些 seam？"
- `prototype` 的**分支选择**要先确认（logic 还是 UI）——选错整个原型白做
- 提交前确认是否要提交（**不要自动提交**）

## 常见坑

1. **在错误的 context 里实现。** grilling → spec → tickets 那条链要连续；每个 implement 要 fresh。
2. **预判未来的测试**。不要为"以后可能要"的功能写代码，`tdd` 明确禁止 speculative features。
3. **把 refactoring 混进 red-green 循环**。它属于 review 阶段。
4. **原型变成了生产代码**。throwaway 是对写法的约束，答案折回真实代码，原型留在 branch 上备查。
5. **跳过 code-review 直接提交**。`implement` 内置了这一步，别绕过。

## 边界

- 还没有 spec / ticket → 先 [04-planning](04-planning.md)
- 需求还没对齐 → 先 [02-alignment](02-alignment.md)
- 写的过程中发现代码结构本身在阻碍你 → 转 [07-refactoring](07-refactoring.md)
