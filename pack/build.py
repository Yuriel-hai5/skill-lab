#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py —— 把 skills/ 打成可分享的 zip。

用法:
    python pack/build.py                    # 打包全部 skill
    python pack/build.py --skills workflow-recipes ui-upgrade
    python pack/build.py --no-optional      # 不含 optional/ 增强
    python pack/build.py --out <路径>

产物: pack/dist/<包名>.zip
"""

import argparse
import os
import shutil
import sys
import zipfile

_HERE = os.path.dirname(os.path.abspath(__file__))     # .../pack
ROOT = os.path.dirname(_HERE)                           # 项目根
SKILLS_SRC = os.path.join(ROOT, "skills")
DIST = os.path.join(_HERE, "dist")

PACK_NAME = "workflow-recipes-pack"
ZIP_SUFFIX = "（先读AGENTS.md）"      # agent 解压前就能从文件名看到提示

# 打包时排除的东西
EXCLUDE_NAMES = {"__pycache__", ".git", ".finesse", ".scratch",
                 "node_modules", "dist", ".DS_Store"}
EXCLUDE_FILES = {"GLOBAL-INDEX.md"}    # 机器特定的生成物


def read_version():
    p = os.path.join(ROOT, "VERSION")
    if os.path.isfile(p):
        return open(p, encoding="utf-8").read().strip()
    return "0.0.0.0"


def collect_skills(only=None):
    if not os.path.isdir(SKILLS_SRC):
        print("找不到 skills/ 目录: %s" % SKILLS_SRC)
        sys.exit(1)
    names = []
    for d in sorted(os.listdir(SKILLS_SRC)):
        if d.startswith("_"):
            continue
        p = os.path.join(SKILLS_SRC, d)
        if os.path.isdir(p) and os.path.isfile(os.path.join(p, "SKILL.md")):
            names.append(d)
    if only:
        missing = [n for n in only if n not in names]
        if missing:
            print("skills/ 里没有: %s" % ", ".join(missing))
            sys.exit(1)
        names = only
    return names


def should_skip(path):
    parts = path.replace("\\", "/").split("/")
    if any(p in EXCLUDE_NAMES for p in parts):
        return True
    if os.path.basename(path) in EXCLUDE_FILES:
        return True
    return False


def add_tree(z, src_dir, arc_prefix, files_out):
    for root, dirs, files in os.walk(src_dir):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDE_NAMES)
        for f in sorted(files):
            if f in EXCLUDE_FILES:
                continue
            p = os.path.join(root, f)
            if should_skip(p):
                continue
            rel = os.path.relpath(p, src_dir).replace("\\", "/")
            arc = "%s/%s" % (arc_prefix, rel)
            z.write(p, arc)
            files_out.append(arc)


def main():
    ap = argparse.ArgumentParser(description="打包 skill 分享包")
    ap.add_argument("--skills", nargs="*", default=None, help="只打包指定 skill")
    ap.add_argument("--no-optional", action="store_true", help="不含 optional/ 增强")
    ap.add_argument("--out", default=None, help="输出 zip 路径")
    ap.add_argument("--no-version", action="store_true", help="文件名不带版本号")
    a = ap.parse_args()

    ver = read_version()
    skills = collect_skills(a.skills)

    print("=" * 58)
    print("skill-lab build   版本 %s" % ver)
    print("=" * 58)
    print()
    print("打包 %d 个 skill: %s" % (len(skills), ", ".join(skills)))

    # 检查素材是否齐
    ag = os.path.join(_HERE, "AGENTS.md")
    rd = os.path.join(_HERE, "README.md")
    missing = [p for p in (ag, rd) if not os.path.isfile(p)]
    if missing:
        print()
        print("  ⚠ 缺素材（收件人体验会变差）:")
        for m in missing:
            print("      %s" % os.path.relpath(m, ROOT))

    # 输出路径
    if a.out:
        out = os.path.abspath(a.out)
    else:
        os.makedirs(DIST, exist_ok=True)
        tag = "" if a.no_version else "-v" + ver
        out = os.path.join(DIST, "%s%s%s.zip" % (PACK_NAME, tag, ZIP_SUFFIX))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if os.path.exists(out):
        os.remove(out)

    files_out = []
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        # 根级素材
        for src in (ag, rd):
            if os.path.isfile(src):
                arc = "%s/%s" % (PACK_NAME, os.path.basename(src))
                z.write(src, arc)
                files_out.append(arc)

        # skill 本体
        for name in skills:
            add_tree(z, os.path.join(SKILLS_SRC, name),
                     "%s/%s" % (PACK_NAME, name), files_out)

        # 可选增强
        opt = os.path.join(_HERE, "optional")
        if not a.no_optional and os.path.isdir(opt):
            add_tree(z, opt, "%s/optional" % PACK_NAME, files_out)

    # 校验
    with zipfile.ZipFile(out) as z:
        broken = z.testzip()

    size = os.path.getsize(out) / 1024.0
    print()
    print("产物: %s" % out)
    print("文件数: %d   体积: %.1f KB   完整性: %s"
          % (len(files_out), size, "OK" if broken is None else "损坏: " + str(broken)))

    if broken is not None:
        print()
        print("打包失败：zip 校验不过。")
        sys.exit(1)

    print()
    print("包内容:")
    for f in files_out:
        print("  " + f.replace(PACK_NAME + "/", ""))

    print()
    print("=" * 58)
    print("发给别人后，让他拖进 WorkBuddy 对话框说：")
    print("  「按包里的 AGENTS.md 帮我装上」")
    print("=" * 58)


if __name__ == "__main__":
    main()
