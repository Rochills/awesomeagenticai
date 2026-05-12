#!/usr/bin/env python3
"""
sync-language-switchers.py — 統一三語檔案頂部的 language switcher

4 語版 repo 結構：
  <file>.md         = zh-TW canonical
  <file>.en.md      = English mirror
  <file>.zh-Hans.md = zh-Hans mirror
  <file>.ru.md      = Russian mirror

每個檔案的頂部都需要 4-way switcher，把目前 active 的語言粗體、其他連結。

執行：
  python scripts/sync-language-switchers.py            # dry run，列出要改的
  python scripts/sync-language-switchers.py --apply    # 實際寫入檔案
  python scripts/sync-language-switchers.py --check    # CI 用，發現不同步就 exit 1

支援兩種 switcher 格式：
  1. README.md 用 <div align="right">...</div> 區塊
  2. 一般檔案用 `> [...](./...) | **...**` 一行 blockquote
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

# Force UTF-8 stdout on Windows (cp950 default can't handle CJK)
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent

# 哪些 .md 檔需要 switcher（zh-TW canonical）
# 排除：DESIGN.md、CONTRIBUTORS.md、CONTRIBUTING.md（內部 / 規則性質）
# 排除：.github/、scripts/、book/
EXCLUDE_PATHS = {
    "branches/DESIGN.md",
    "stages/DESIGN.md",
    "CONTRIBUTORS.md",  # 名單性質，不一定有 zh-Hans 翻譯
}
EXCLUDE_DIRS = {".github", "scripts", "book", ".ai", ".claude", "node_modules"}


def find_paired_files() -> list[tuple[Path, Optional[Path], Optional[Path], Optional[Path]]]:
    """找所有 (zh-TW, en, zh-Hans, ru) 四檔組合。"""
    quads = []
    for md_path in sorted(REPO_ROOT.rglob("*.md")):
        # 跳過 mirror 檔自己
        if (
            md_path.name.endswith(".en.md")
            or md_path.name.endswith(".zh-Hans.md")
            or md_path.name.endswith(".ru.md")
        ):
            continue
        # 跳過 EXCLUDE_DIRS
        if any(part in EXCLUDE_DIRS for part in md_path.relative_to(REPO_ROOT).parts):
            continue
        # 跳過 EXCLUDE_PATHS
        rel = md_path.relative_to(REPO_ROOT).as_posix()
        if rel in EXCLUDE_PATHS:
            continue

        en_path = md_path.with_suffix(".en.md")
        zh_hans_path = md_path.with_suffix(".zh-Hans.md")
        ru_path = md_path.with_suffix(".ru.md")
        if not en_path.exists():
            en_path = None
        if not zh_hans_path.exists():
            zh_hans_path = None
        if not ru_path.exists():
            ru_path = None

        # 至少要有 zh-TW + 一個 mirror 才算需要 switcher
        if en_path is None and zh_hans_path is None and ru_path is None:
            continue

        quads.append((md_path, en_path, zh_hans_path, ru_path))
    return quads


def make_readme_switcher(active: str, has_en: bool, has_zh_hans: bool, has_ru: bool) -> str:
    """README.md / README.en.md / README.zh-Hans.md / README.ru.md 用的 div 區塊 switcher。"""
    parts = []
    label_map = {"zh-TW": "繁體中文", "en": "English", "zh-Hans": "简体中文", "ru": "Русский"}

    for lang in ("zh-TW", "zh-Hans", "en", "ru"):
        if lang == "zh-Hans" and not has_zh_hans:
            continue
        if lang == "en" and not has_en:
            continue
        if lang == "ru" and not has_ru:
            continue
        label = label_map[lang]
        if lang == active:
            parts.append(f"<strong>{label}</strong>")
        else:
            href_map = {
                "zh-TW": "./README.md",
                "en": "./README.en.md",
                "zh-Hans": "./README.zh-Hans.md",
                "ru": "./README.ru.md",
            }
            parts.append(f'<a href="{href_map[lang]}">{label}</a>')

    return f'<div align="right">\n  {" | ".join(parts)}\n</div>'


def make_inline_switcher(active: str, base_name: str, has_en: bool, has_zh_hans: bool, has_ru: bool) -> str:
    """一般檔 blockquote 一行 switcher。"""
    parts = []
    label_map = {"zh-TW": "繁體中文", "en": "English", "zh-Hans": "简体中文", "ru": "Русский"}

    for lang in ("zh-TW", "zh-Hans", "en", "ru"):
        if lang == "zh-Hans" and not has_zh_hans:
            continue
        if lang == "en" and not has_en:
            continue
        if lang == "ru" and not has_ru:
            continue
        label = label_map[lang]
        if lang == active:
            parts.append(f"**{label}**")
        else:
            href_map = {
                "zh-TW": f"./{base_name}.md",
                "en": f"./{base_name}.en.md",
                "zh-Hans": f"./{base_name}.zh-Hans.md",
                "ru": f"./{base_name}.ru.md",
            }
            parts.append(f"[{label}]({href_map[lang]})")

    return "> " + " | ".join(parts)


def detect_switcher_block(content: str) -> tuple[Optional[int], Optional[int], str]:
    """
    找出檔案頂部的 switcher 區塊位置。
    回傳 (start_line, end_line, kind) 或 (None, None, '')。
    kind = 'div' 或 'inline' 或 ''。
    """
    lines = content.split("\n")

    # 嘗試找 <div align="right">...</div> 區塊
    for i, line in enumerate(lines):
        if line.strip().startswith('<div align="right">'):
            # 找 </div>
            for j in range(i, min(i + 5, len(lines))):
                if "</div>" in lines[j]:
                    return i, j, "div"
            break  # 找到 <div> 但找不到 </div>，放棄

    # 嘗試找 inline `> [English](./xxx.en.md) | **繁體中文**` 之類
    for i, line in enumerate(lines[:10]):  # 只看前 10 行
        if line.startswith("> ") and ("](./") in line and (
            "繁體中文" in line or "English" in line or "简体中文" in line or "Русский" in line
        ):
            return i, i, "inline"

    return None, None, ""


def update_file(path: Path, lang: str, has_en: bool, has_zh_hans: bool, has_ru: bool, apply: bool) -> bool:
    """更新單一檔案的 switcher。回傳 True 表示有改動需要寫入。"""
    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")

    start, end, kind = detect_switcher_block(content)

    # README 用 div block，一般檔用 inline
    is_readme = path.name.startswith("README")

    if is_readme:
        new_switcher = make_readme_switcher(lang, has_en, has_zh_hans, has_ru)
    else:
        # 從 path 名字算 base_name（去掉 .en / .zh-Hans / .ru suffix 後再去掉 .md）
        name = path.name
        if name.endswith(".en.md"):
            base_name = name[: -len(".en.md")]
        elif name.endswith(".zh-Hans.md"):
            base_name = name[: -len(".zh-Hans.md")]
        elif name.endswith(".ru.md"):
            base_name = name[: -len(".ru.md")]
        else:
            base_name = name[: -len(".md")]
        new_switcher = make_inline_switcher(lang, base_name, has_en, has_zh_hans, has_ru)

    if start is None:
        # 沒有現成 switcher，加在第一行 H1 之後
        # 找第一個 H1 標題
        for i, line in enumerate(lines):
            if line.startswith("# "):
                # 在 H1 後插入 switcher（先空一行 + switcher + 空一行）
                new_lines = lines[: i + 1] + [""] + new_switcher.split("\n") + [""] + lines[i + 1 :]
                new_content = "\n".join(new_lines)
                if apply:
                    path.write_text(new_content, encoding="utf-8")
                print(f"[ADD] {path.relative_to(REPO_ROOT)} ← (no existing switcher, inserted after H1)")
                return True
        # 沒 H1 就放在最頂
        new_lines = new_switcher.split("\n") + [""] + lines
        new_content = "\n".join(new_lines)
        if apply:
            path.write_text(new_content, encoding="utf-8")
        print(f"[ADD] {path.relative_to(REPO_ROOT)} ← (no existing switcher, inserted at top)")
        return True

    # 替換舊的 switcher
    old_switcher = "\n".join(lines[start : end + 1])
    if old_switcher.strip() == new_switcher.strip():
        return False  # 沒改動

    new_lines = lines[:start] + new_switcher.split("\n") + lines[end + 1 :]
    new_content = "\n".join(new_lines)

    if apply:
        path.write_text(new_content, encoding="utf-8")
    print(f"[UPDATE] {path.relative_to(REPO_ROOT)}:{start + 1}")
    print(f"  - {old_switcher[:100]}")
    print(f"  + {new_switcher[:100]}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Sync 3-way language switchers across .md / .en.md / .zh-Hans.md")
    parser.add_argument("--apply", action="store_true", help="actually write changes (default: dry-run)")
    parser.add_argument(
        "--check", action="store_true", help="exit 1 if any switcher is out of sync (CI use)"
    )
    args = parser.parse_args()

    quads = find_paired_files()
    print(f"Found {len(quads)} canonical zh-TW files with at least one mirror.\n")

    changed = 0
    for zh_tw, en, zh_hans, ru in quads:
        has_en = en is not None
        has_zh_hans = zh_hans is not None
        has_ru = ru is not None

        if update_file(zh_tw, "zh-TW", has_en, has_zh_hans, has_ru, args.apply):
            changed += 1
        if has_en and update_file(en, "en", has_en, has_zh_hans, has_ru, args.apply):
            changed += 1
        if has_zh_hans and update_file(zh_hans, "zh-Hans", has_en, has_zh_hans, has_ru, args.apply):
            changed += 1
        if has_ru and update_file(ru, "ru", has_en, has_zh_hans, has_ru, args.apply):
            changed += 1

    print()
    print("=" * 60)
    print(f"Total {len(quads)} files inspected, {changed} need updating.")

    if args.check:
        sys.exit(1 if changed > 0 else 0)
    elif not args.apply and changed > 0:
        print("\nDry-run mode. Re-run with --apply to write changes.")


if __name__ == "__main__":
    main()
