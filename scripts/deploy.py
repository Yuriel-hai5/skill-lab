#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deploy.py —— 把 skills/ 里的 skill 同步到 WorkBuddy 的 skills 目录。

用法:
    python scripts/deploy.py                  # 自动探测目标目录
    python scripts/deploy.py --dry-run        # 只看会改什么，不动手
    python scripts/deploy.py --target <路径>  # 手动指定目标
    python scripts/deploy.py --only <名字>    # 只部署某一个 skill
    python scripts/deploy.py --backup         # 覆盖前先备份目标里的旧版本

只增改本项目管理的 skill，**不删**目标目录里的其他 skill。
"""

import argparse
import os
import shutil
import subprocess
import sys
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(_HERE)                 # 项目根
SKILLS_SRC = os.path.join(ROOT, "skills")
VERSION_FILE = os.path.join(ROOT, "VERSION")
CONFIG_FILE = os.path.join(ROOT, ".deploy-target")   # 记住上次选的目标目录

# 不以 _ 开头的目录才算可部署的 skill
SKIP_PREFIX = "_"

CANDIDATES = [
    ("WorkBuddy 国际版", os.path.join(os.path.expanduser("~"), ".workbuddy-ai", "skills")),
    ("WorkBuddy 国内版", os.path.join(os.path.expanduser("~"), ".workbuddy", "skills")),
]


# ---------------------------------------------------------------- 目标目录

def probe_targets():
    """返回 [(版本名, 路径, 已有 skill 数), ...]，只含已存在的。"""
    out = []
    for label, path in CANDIDATES:
        if os.path.isdir(path):
            n = sum(1 for d in os.listdir(path)
                    if os.path.isdir(os.path.join(path, d)))
            out.append((label, path, n))
    return out


def resolve_target(explicit, remember=True):
    """确定部署目标。--target 会记住，下次不用再写。"""
    if explicit:
        path = os.path.abspath(explicit)
        if remember:
            try:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    f.write(path + "\n")
                print("目标: %s（已记住，下次不用再指定）" % path)
            except OSError:
                print("目标: %s" % path)
        else:
            print("目标: %s（dry-run，不记住）" % path)
        return path, None

    # 有记住的选择就用它
    if os.path.isfile(CONFIG_FILE):
        saved = open(CONFIG_FILE, encoding="utf-8").read().strip()
        if saved and os.path.isdir(saved):
            n = sum(1 for d in os.listdir(saved)
                    if os.path.isdir(os.path.join(saved, d)))
            print("目标: %s（上次记住的，已有 %d 个 skill）" % (saved, n))
            return saved, None
        print("上次记住的目录不存在了: %s" % saved)

    found = probe_targets()
    if not found:
        print("找不到 WorkBuddy 的 skills 目录。试过:")
        for label, path in CANDIDATES:
            print("  %-18s %s" % (label, path))
        print()
        print("请用 --target <路径> 手动指定，或先启动一次 WorkBuddy 让它建目录。")
        sys.exit(1)

    if len(found) == 1:
        label, path, n = found[0]
        print("目标: %s —— %s（已有 %d 个 skill）" % (label, path, n))
        return path, label

    # 两个都存在：谁非空用谁；都非空就必须选
    nonempty = [f for f in found if f[2] > 0]
    if len(nonempty) == 1:
        label, path, n = nonempty[0]
        empty = [f[0] for f in found if f[2] == 0]
        print("目标: %s —— %s（已有 %d 个 skill）" % (label, path, n))
        if empty:
            print("  注: %s 的目录是空的，跳过。" % "、".join(empty))
        return path, label

    print("两个版本的 skills 目录都有内容，需要你选一个：")
    print()
    for i, (label, path, n) in enumerate(found, 1):
        print("  %d) %-18s %s  (%d 个 skill)" % (i, label, path, n))
    print()
    print("选好后跑一次（会记住选择，以后不用再写）：")
    for label, path, n in found:
        print('    python scripts/deploy.py --target "%s"' % path)
    print()
    print("或者两个都装（各跑一次）。")
    sys.exit(1)


# ---------------------------------------------------------------- 清单

def list_skills(only=None):
    if not os.path.isdir(SKILLS_SRC):
        print("找不到 skills/ 目录: %s" % SKILLS_SRC)
        sys.exit(1)
    names = []
    for d in sorted(os.listdir(SKILLS_SRC)):
        if d.startswith(SKIP_PREFIX):
            continue
        p = os.path.join(SKILLS_SRC, d)
        if not os.path.isdir(p):
            continue
        if not os.path.isfile(os.path.join(p, "SKILL.md")):
            print("  跳过 %s（没有 SKILL.md）" % d)
            continue
        names.append(d)
    if only:
        if only not in names:
            print("skills/ 里没有 %s" % only)
            sys.exit(1)
        names = [only]
    return names


# ---------------------------------------------------------------- 检查

def check_paths(names):
    """检查 skill 文件里有没有本机绝对路径。

    跳过含 <占位符> 的行 —— 那是给人看的说明（比如版本对照表里的
    `C:\\Users\\<你>\\.workbuddy-ai\\skills\\`），不是真硬编码。
    """
    import re
    bad = []
    home = os.path.expanduser("~")
    needles = [home, home.replace("\\", "/"),
               "C:\\Users\\", "C:/Users/", "/Users/", "/home/"]
    placeholders = re.compile(r"<[^<>\s]{1,20}>")     # <你> <skills-dir> <用户名> ...
    for name in names:
        base = os.path.join(SKILLS_SRC, name)
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
            for f in files:
                if not f.endswith((".md", ".py", ".txt", ".json")):
                    continue
                p = os.path.join(root, f)
                try:
                    lines = open(p, encoding="utf-8").read().splitlines()
                except (UnicodeDecodeError, OSError):
                    continue
                for i, line in enumerate(lines, 1):
                    if placeholders.search(line):
                        continue          # 说明行，跳过
                    for needle in needles:
                        if needle and needle in line:
                            bad.append((os.path.relpath(p, ROOT), i, needle))
                            break
    return bad


# ---------------------------------------------------------------- 部署

def deploy_one(name, target, dry, backup):
    src = os.path.join(SKILLS_SRC, name)
    dst = os.path.join(target, name)
    exists = os.path.exists(dst)

    if dry:
        print("  [dry] %s %s" % ("覆盖" if exists else "新增", name))
        return "would-" + ("update" if exists else "add")

    if exists:
        if backup:
            stamp = time.strftime("%Y%m%d-%H%M%S")
            bak = os.path.join(target, "_backup", "%s-%s" % (name, stamp))
            os.makedirs(os.path.dirname(bak), exist_ok=True)
            shutil.copytree(dst, bak)
            print("  备份 %s → _backup/%s-%s" % (name, name, stamp))
        shutil.rmtree(dst)

    shutil.copytree(src, dst)
    return "updated" if exists else "added"


# ---------------------------------------------------------------- 索引

def rebuild_index(target):
    script = os.path.join(target, "workflow-recipes", "scripts", "rebuild-index.py")
    if not os.path.isfile(script):
        print("  跳过索引重建（没找到 %s）" % script)
        return
    try:
        r = subprocess.run([sys.executable, script],
                           capture_output=True, text=True, timeout=120)
        for line in (r.stdout or "").splitlines():
            if line.strip():
                print("  " + line)
        if r.returncode != 0 and r.stderr:
            print("  索引脚本报错:")
            for line in r.stderr.splitlines()[:10]:
                print("    " + line)
    except Exception as e:
        print("  索引重建失败: %s" % e)


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="把 skills/ 同步到 WorkBuddy skills 目录")
    ap.add_argument("--target", default=None, help="目标 skills 目录")
    ap.add_argument("--only", default=None, help="只部署某一个 skill")
    ap.add_argument("--dry-run", action="store_true", help="只看会改什么")
    ap.add_argument("--backup", action="store_true", help="覆盖前备份旧版本")
    ap.add_argument("--no-index", action="store_true", help="不重建全局索引")
    a = ap.parse_args()

    ver = "?"
    if os.path.isfile(VERSION_FILE):
        ver = open(VERSION_FILE, encoding="utf-8").read().strip()

    print("=" * 58)
    print("skill-lab deploy   版本 %s" % ver)
    print("=" * 58)

    target, _ = resolve_target(a.target, remember=not a.dry_run)
    names = list_skills(a.only)

    print()
    print("待部署 %d 个 skill: %s" % (len(names), ", ".join(names)))

    # 路径检查（警告，不阻断）
    bad = check_paths(names)
    if bad:
        print()
        print("  ⚠ 发现本机绝对路径（分享给别人会坏，建议改成 <skills-dir>）:")
        for rel, ln, needle in bad[:10]:
            print("      %s:%d" % (rel, ln))
        if len(bad) > 10:
            print("      … 还有 %d 处" % (len(bad) - 10))
    else:
        print("  ✓ 路径检查通过（无本机绝对路径）")

    print()
    added = updated = 0
    for name in names:
        r = deploy_one(name, target, a.dry_run, a.backup)
        if r.endswith("add"):
            added += 1
            print("  + %s" % name)
        else:
            updated += 1
            print("  ~ %s" % name)

    if a.dry_run:
        print()
        print("（dry-run，没有真的改动）")
        return

    print()
    print("结果: 新增 %d，更新 %d" % (added, updated))

    if not a.no_index:
        print()
        print("重建全局索引:")
        rebuild_index(target)

    print()
    print("=" * 58)
    print("⚠ 新开一个对话才生效 —— 已开着的对话读不到新 skill。")
    print("=" * 58)


if __name__ == "__main__":
    main()
