#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重建全局技能索引，并校验 workflow-recipes 的配方引用。

用法（无需参数，会自动推断路径）:
    python <skills-dir>/workflow-recipes/scripts/rebuild-index.py

可选:
    --skills-dir <path>   手动指定 skills 根目录
    --out <file>          手动指定输出文件

路径推断规则：本脚本位于 <skills-dir>/<skill-name>/scripts/，
所以向上两级就是 skills 根目录。**不假定 .workbuddy-ai 还是 .workbuddy。**

输出：与本脚本同属一个 skill 目录下的 GLOBAL-INDEX.md
"""
import os, re, io, sys, argparse

# ---------- 路径自动推断 ----------
_HERE = os.path.dirname(os.path.abspath(__file__))          # .../<skill>/scripts
_SKILL_DIR = os.path.dirname(_HERE)                          # .../<skill>
_DEFAULT_SKILLS_DIR = os.path.dirname(_SKILL_DIR)            # .../skills

# 来源包映射：目录名 -> (包显示名, 一句话定位)
SOURCE_MAP = {
    # ---- mattpocock-skills-zh-CN ----
    "ask-matt": ("mattpocock", "全局 skill 路由器"),
    "grill-with-docs": ("mattpocock", "访谈打磨想法 + 产出 CONTEXT.md/ADR"),
    "grill-me": ("mattpocock", "访谈打磨（无 repo、不留文件）"),
    "grilling": ("mattpocock", "访谈引擎本身（design tree / frontier）"),
    "to-spec": ("mattpocock", "把对话整理成 spec 发布到 tracker"),
    "to-tickets": ("mattpocock", "spec 拆成带 blocking 的 tickets"),
    "implement": ("mattpocock", "照 spec/ticket 实现（内部驱动 tdd + code-review）"),
    "tdd": ("mattpocock", "测试驱动开发 reference"),
    "code-review": ("mattpocock", "Standards + Spec 双轴审查"),
    "diagnosing-bugs": ("mattpocock", "建 feedback loop 定位棘手 bug"),
    "resolving-merge-conflicts": ("mattpocock", "按 intent 逐 hunk 解冲突，绝不 --abort"),
    "prototype": ("mattpocock", "throwaway 原型回答设计问题"),
    "research": ("mattpocock", "后台 agent 对照一手来源调研"),
    "triage": ("mattpocock", "issues 过 triage 状态机"),
    "wayfinder": ("mattpocock", "大工程画 decision tickets 地图"),
    "improve-codebase-architecture": ("mattpocock", "扫描深化机会 + HTML 报告"),
    "codebase-design": ("mattpocock", "deep-module 设计词汇"),
    "domain-modeling": ("mattpocock", "打磨领域语言 + ADR"),
    "setup-matt-pocock-skills": ("mattpocock", "每 repo 配置一次 tracker/labels/docs"),
    "handoff": ("mattpocock", "压缩对话成交接文档"),
    "teach": ("mattpocock", "stateful workspace 跨 session 教学"),
    "to-questionnaire": ("mattpocock", "把答不了的决策变成问卷"),
    "wait-what": ("mattpocock", "用共享语言重述没懂的话"),
    "wizard": ("mattpocock", "生成 bash 向导走人工步骤"),
    "writing-for-agents": ("mattpocock", "为 agent 写文档的 reference"),
    "git-guardrails-claude-code": ("mattpocock", "危险 git 拦截 hooks（仅 Claude Code）"),
    "setup-pre-commit": ("mattpocock", "Husky + lint-staged 提交钩子"),
    "scaffold-exercises": ("mattpocock", "生成练习目录结构"),
    "migrate-to-shoehorn": ("mattpocock", "测试 as 断言迁移到 shoehorn"),
    # ---- UI 设计五件套 ----
    "finesse-ui": ("finesse", "★主力 4 register 全流程设计系统"),
    "impeccable": ("impeccable", "22 命令改造已有界面"),
    "ui-ux-pro-max": ("ui-ux-pro-max", "设计数据库查询（79 风格/192 配色/22 栈）"),
    "ui-styling": ("ui-ux-pro-max", "shadcn/ui + Tailwind 组件知识"),
    "design": ("ui-ux-pro-max", "品牌 VI / token / Logo 生成"),
    "design-system": ("ui-ux-pro-max", "三层 token 架构"),
    "brand": ("ui-ux-pro-max", "品牌声音与一致性"),
    "slides": ("ui-ux-pro-max", "HTML 演示稿 + Chart.js"),
    "banner-design": ("ui-ux-pro-max", "社媒/广告横幅"),
    "interface-design": ("interface-design", "产品界面方法论（只做 dashboard/admin）"),
    "taste-skill": ("taste", "落地页反 slop 三旋钮（v2 主）"),
    "taste-skill-v1": ("taste", "落地页 v1 旧行为"),
    "gpt-tasteskill": ("taste", "Python 真随机布局 + AIDA + GSAP"),
    "minimalist-skill": ("taste", "暖单色编辑风"),
    "brutalist-skill": ("taste", "瑞士印刷 × 军用终端"),
    "soft-skill": ("taste", "高端 agency 质感"),
    "redesign-skill": ("taste", "审计先行升级已有站点"),
    "output-skill": ("taste", "反截断，强制完整输出"),
    "stitch-skill": ("taste", "生成 DESIGN.md"),
    # ---- 其他 ----
    "github-push-via-api": ("内置", "github.com 不通时用 API 推送"),
    # ---- 自建编排 ----
    "ui-upgrade": ("自建", "★已有界面质感+动效升级固定配方"),
    "workflow-recipes": ("自建", "★场景配方库：按项目阶段给 skill 序列"),
    "skill-pack-sharing": ("自建", "★把 skill 打包成可拖拽安装的分享包"),
}

PKG_LABEL = {
    "自建": "自建编排",
    "finesse": "finesse-ui（设计主力）",
    "ui-ux-pro-max": "ui-ux-pro-max（设计数据库全家桶）",
    "impeccable": "impeccable（改造命令集）",
    "interface-design": "interface-design（产品界面方法论）",
    "taste": "taste-skill（落地页风格）",
    "mattpocock": "Matt Pocock Skills（工程流程）",
    "内置": "WorkBuddy 内置",
    "未分类": "未分类（需补 SOURCE_MAP）",
}
PKG_ORDER = ["自建", "finesse", "ui-ux-pro-max", "impeccable", "interface-design",
             "taste", "mattpocock", "内置", "未分类"]

USE_MAP = {
    "编排-元": ["workflow-recipes", "ask-matt", "skill-pack-sharing"],
    "设计-从零": ["finesse-ui", "taste-skill", "taste-skill-v1", "gpt-tasteskill",
                 "minimalist-skill", "brutalist-skill", "soft-skill", "interface-design",
                 "ui-styling", "design-system", "design", "brand", "banner-design", "slides"],
    "设计-改造": ["ui-upgrade", "impeccable", "redesign-skill", "improve-codebase-architecture"],
    "设计-查询": ["ui-ux-pro-max"],
    "设计-辅助": ["output-skill", "stitch-skill"],
    "工程-对齐": ["grill-with-docs", "grill-me", "grilling", "to-spec", "to-tickets"],
    "工程-实现": ["implement", "tdd", "prototype", "codebase-design"],
    "工程-排错": ["diagnosing-bugs", "code-review", "resolving-merge-conflicts"],
    "工程-规划": ["triage", "wayfinder", "domain-modeling", "research"],
    "工程-配置": ["setup-matt-pocock-skills", "setup-pre-commit", "git-guardrails-claude-code",
                 "scaffold-exercises", "migrate-to-shoehorn"],
    "协作-其他": ["handoff", "teach", "to-questionnaire", "wait-what", "wizard",
                 "writing-for-agents", "github-push-via-api"],
}

# 配方文件里常见的非 skill 词汇（命令 / label / CSS / 工具），校验时跳过
NON_SKILL = {
    "craft", "shape", "init", "document", "extract", "critique", "audit", "polish",
    "bolder", "quieter", "distill", "harden", "onboard", "animate", "colorize",
    "typeset", "layout", "delight", "overdrive", "clarify", "adapt", "optimize",
    "live", "generate",
    "soul", "diverge", "depth", "densify", "redesign",
    "clear", "compact", "review", "commit", "push", "clean", "rebase", "merge",
    "checkout", "stash", "blame", "bisect",
    "needs-triage", "needs-info", "ready-for-agent", "ready-for-human", "wontfix",
    "enhancement",
    "transform", "opacity", "prefers-reduced-motion", "animation-timeline",
    "backdrop-filter", "clip-path", "mask-image", "line-height", "minmax",
    "overflow-wrap", "overflow-x", "pointercancel", "env",
    "curl", "node", "python", "python3", "npx", "pnpm", "bun", "package.json",
    "pubspec.yaml", "AGENTS.md", "CLAUDE.md", "CONTEXT.md", "SKILL.md",
    "skill-creator",
    # frontmatter 字段名 / 通用术语 —— 不是 skill 名，别报成"未安装"
    "description", "name", "frontmatter", "disable-model-invocation",
}


def parse_frontmatter(path):
    try:
        s = io.open(path, encoding="utf-8").read()
    except Exception:
        return None
    m = re.match(r"^---\s*\n(.*?)\n---", s, re.S)
    if not m:
        return None
    fm = m.group(1)

    def field(k):
        mm = re.search(r"^%s:\s*(.+?)\s*$" % k, fm, re.M)
        return mm.group(1).strip().strip('"').strip("'") if mm else ""

    return {"name": field("name"), "description": field("description"),
            "dmi": field("disable-model-invocation").lower() == "true"}


def short(desc, n=110):
    d = re.sub(r"\s+", " ", desc or "").strip()
    return d[:n] + ("…" if len(d) > n else "")


def check_recipe_refs(real_names, skills_dir):
    """校验配方里引用的 skill 名是否真实存在（纯提示，不阻断）。"""
    d = os.path.join(skills_dir, "workflow-recipes")
    if not os.path.isdir(d):
        return
    files = [os.path.join(d, "SKILL.md")]
    rd = os.path.join(d, "references")
    if os.path.isdir(rd):
        files += [os.path.join(rd, f) for f in sorted(os.listdir(rd)) if f.endswith(".md")]
    bad = {}
    for p in files:
        if not os.path.isfile(p):
            continue
        txt = io.open(p, encoding="utf-8").read()
        for m in set(re.findall(r"`([a-z][a-z0-9-]{3,40})`", txt)):
            if m in real_names or m in NON_SKILL:
                continue
            bad.setdefault(m, []).append(os.path.basename(p))
    print()
    if not bad:
        print("  配方引用校验：通过（配方点名的 skill 全部已安装）")
        return
    print("  配方引用校验：有 %d 个配方点名的 skill 本机未安装" % len(bad))
    print("    —— 这不是错误。配方正文自带方法论，缺 skill 时按 references/00-skill-map.md")
    print("       的「没装时怎么办」一列执行即可，配方顺序不变。")
    print("       想装齐的话，00-skill-map.md 末尾列了配套包的 GitHub 地址。")
    print()
    print("    未安装清单：")
    for k, v in sorted(bad.items()):
        print("      %-26s <- %s" % (k, ", ".join(sorted(set(v)))))
    print()
    print("    （若上面出现的是命令名 / 标签名而非 skill，属正常误报，忽略。）")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills-dir", default=_DEFAULT_SKILLS_DIR,
                    help="skills 根目录（默认自动推断）")
    ap.add_argument("--out", default=None, help="输出文件（默认本 skill 目录下 GLOBAL-INDEX.md）")
    a = ap.parse_args()
    root = a.skills_dir
    out = a.out or os.path.join(_SKILL_DIR, "GLOBAL-INDEX.md")

    if not os.path.isdir(root):
        print("找不到 skills 目录: %s" % root)
        sys.exit(1)

    skills = []
    for d in sorted(os.listdir(root)):
        p = os.path.join(root, d, "SKILL.md")
        if not os.path.isfile(p):
            continue
        fm = parse_frontmatter(p)
        if not fm or not fm.get("name"):
            continue
        pkg, note = SOURCE_MAP.get(d, ("未分类", ""))
        skills.append({"dir": d, "name": fm["name"], "desc": fm["description"],
                       "dmi": fm["dmi"], "pkg": pkg, "note": note})

    by_pkg = {}
    for s in skills:
        by_pkg.setdefault(s["pkg"], []).append(s)

    L = ["# 全局技能索引（GLOBAL INDEX）", "",
         "> 由 `scripts/rebuild-index.py` 自动生成。安装/删除 skill 后重跑一次。",
         "> **本索引覆盖本机已安装的全部 %d 个 skill。**" % len(skills), "",
         "调用方式：**U** = user-invoked（只有输入 `/name` 才触发）；"
         "**M** = model-invoked（agent 判断匹配时自动触发）。", "",
         "## 规模概览", "", "| 来源包 | 数量 |", "|---|---|"]
    for pkg in PKG_ORDER:
        if pkg in by_pkg:
            L.append("| %s | %d |" % (PKG_LABEL.get(pkg, pkg), len(by_pkg[pkg])))
    L.append("| **合计** | **%d** |" % len(skills))
    L.append("")

    L += ["## 按用途速查", ""]
    used = set()
    for cat, dirs in USE_MAP.items():
        rows = [s for s in skills if s["dir"] in dirs]
        if not rows:
            continue
        used.update(dirs)
        L.append("**%s** — %s" % (cat, " · ".join("`%s`" % r["dir"] for r in rows)))
        L.append("")
    rest = [s for s in skills if s["dir"] not in used]
    if rest:
        L.append("**未归类** — " + " · ".join("`%s`" % r["dir"] for r in rest))
        L.append("")

    L += ["## 全部 skill 明细", ""]
    for pkg in PKG_ORDER:
        if pkg not in by_pkg:
            continue
        L += ["### %s（%d）" % (PKG_LABEL.get(pkg, pkg), len(by_pkg[pkg])), "",
              "| skill | 调用 | 作用 |", "|---|---|---|"]
        for s in sorted(by_pkg[pkg], key=lambda x: x["dir"]):
            L.append("| `%s` | %s | %s |" % (s["dir"], "U" if s["dmi"] else "M",
                                             short(s["note"] or s["desc"], 80)))
        L.append("")

    io.open(out, "w", encoding="utf-8").write("\n".join(L))
    print("已生成 %s —— 共 %d 个 skill" % (out, len(skills)))
    for pkg in PKG_ORDER:
        if pkg in by_pkg:
            print("  %-18s %d" % (pkg, len(by_pkg[pkg])))
    check_recipe_refs({x["dir"] for x in skills}, root)


if __name__ == "__main__":
    main()
