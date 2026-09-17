# 07 · 重构 / 代码健康

## 适用信号

- "代码越来越难改"、"加个功能要动五个文件"
- "我想重构但不知道从哪下手"
- "没有测试，不敢改"
- "命名很乱，同一个词指三件事"
- 定期维护（不是修 bug，也不是加功能）

## 配方

### 1. `improve-codebase-architecture` —— 先找候选，别瞎改

- **先划定扫描范围（YAGNI）**：深化的收益是让**未来修改**更容易，所以关注**最近还在变**的区域。
  用户点名了方向就按方向；否则回看 commit history 找 hot spots
- spawn sub-agent 遍历 codebase，记录感到 friction 的地方：
  - 理解一个概念要在很多小模块间来回跳？
  - 哪些模块是 **shallow** 的（interface 几乎和 implementation 一样复杂）？
  - 哪些为可测性抽出的纯函数，真正的 bug 藏在**它们如何被调用**之处（缺 **locality**）？
  - 哪些紧耦合模块泄漏到了 seam 之外？
  - 哪些部分没测试，或很难通过当前 interface 测试？
- 对可疑对象跑 **deletion test**：删掉它会让复杂度**集中**，还是只是**搬家**？
  "集中"才是你要的信号
- **产出**：一份 self-contained HTML 报告（写到系统临时目录，**不落进 repo**），
  每个候选含 before/after 可视化 + 涉及文件 + 建议

> **它是 survey，不是 rescue。** 它负责找候选项，不会替你解开一团泥。
> 建议每隔几天跑一次，而不是等烂到不行。

### 2. `codebase-design` —— 设计选中的候选

这是**词汇层**（不是要运行的流程）：module、interface、depth、seam、adapter、leverage、locality。

- 目标：把大量 behavior 放在 clean seam 上的**小 interface** 后面
- 原则：deletion test、"the interface is the test surface"、"one adapter = 假设的 seam，two = 真的 seam"
- 用它统一表述，别漂移到 "component" / "service" / "API" / "boundary"

### 3. `domain-modeling` —— 顺手把词汇理清

- 挑战模糊术语、解决 overloaded word（一个 "account" 承担三件事）
- 把**难逆转**的决策记成 ADR
- 就地更新 `CONTEXT.md` 和 `docs/adr/`
- 文件缺失时**懒创建**——不要提前建空文件

### 4. 实施时用 `tdd` 锁住行为

重构前先有测试，否则无法确认行为没变。测试放在**预先确认的 seams** 上。

### 5. 全库机械改动 → expand–contract

影响整个 codebase 的改动（重命名列、改共享符号类型）**不能**硬做成一个 slice：

1. **expand**：在旧形式旁加入新形式，保持一切正常
2. **分批迁移**：按 blast radius 分批（按 package / 目录），每批一个 ticket，被 expand block；
   旧形式仍在，所以每批 CI 都 green
3. **contract**：确认没有 caller 残留后，在最后一个 ticket 里删掉旧形式

## 需确认

- `improve-codebase-architecture` 的报告写到**系统临时目录**，不要污染 repo
- 选中哪个候选项要用户决定，不要自己挑
- 重构前确认：**有没有测试能证明行为没变**？没有就先补

## 常见坑

1. **没有测试就重构**。无法区分"重构成功"和"行为悄悄变了"。
2. **一次改太多**。每个候选单独做，做完验证再下一个。
3. **为可测性抽出纯函数，但 bug 在调用处**（缺 locality）—— 这是它明确指出的反模式。
4. **把 wide refactor 当普通功能拆**，导致每片都不能保持 green。
5. **只跑一次就忘了**。这是维护动作，建议定期跑。

## 边界

- 是 bug 而不是结构问题 → [06-debugging](06-debugging.md)
- 只是要给现有代码补测试 → 直接用 `tdd`
