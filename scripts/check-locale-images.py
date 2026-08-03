#!/usr/bin/env python3
"""check-locale-images.py — keep mirror pages embedding their OWN locale's image.

Companion to check-locale-links.py, which deliberately only matches `.md`
targets (its LINK_RE demands a `.md` suffix), so image paths are invisible to it
and to every other gate in CI. That blind spot is how 9 references ended up
pointing at Traditional-Chinese-only diagram assets from `.en.md` / `.zh-Hans.md`
pages — with the alt text localized but the picture itself not, so an English
reader gets an English caption above a diagram rendered entirely in Traditional
Chinese.

Two distinct findings, because they need different fixes:

  RETARGET — the same-locale sibling EXISTS on disk but the page still embeds the
             canonical. Purely mechanical; `--apply` rewrites these.
  MISSING  — no same-locale sibling exists. Needs someone to actually produce the
             asset (see resources/diagrams/locale-variant-prompts.md); no script
             can fix it, so `--apply` leaves these alone.

Usage:
    python scripts/check-locale-images.py             # report (exit 1 if any)
    python scripts/check-locale-images.py --advisory  # report but exit 0
    python scripts/check-locale-images.py --apply     # rewrite RETARGET hits
    python scripts/check-locale-images.py --quiet     # summary lines only

Rule (conservative, mirroring check-locale-links.py — a reference is only
reported when ALL hold):
  1. the file is a mirror (`*.en.md` or `*.zh-Hans.md`),
  2. the reference is a markdown image `![alt](path)` with a relative path to a
     known image extension,
  3. the target carries no locale suffix already (`foo.en.png` is left alone),
  4. the reference is not inside a fenced code block.
A canonical-named asset embedded from a mirror page is always one of the two
findings above: either its sibling exists (retarget) or it does not (missing).
"""

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {".git", ".github", ".claude", ".ai", "_build", "node_modules", "book", ".venv"}
LOCALES = [(".en.md", ".en", "*.en.md"), (".zh-Hans.md", ".zh-Hans", "*.zh-Hans.md")]
LOCALE_SUFFIXES = (".en", ".zh-Hans")
IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg")
# Coverage note: markdown `![alt](path)` only. HTML <img src> is not matched —
# the repo's two <img> tags are external CDN badges with no locale variant, so
# there is nothing to check today. Add HTML handling here if a local asset ever
# gets embedded that way, rather than assuming this gate already sees it.

# ![alt](target) — relative image targets only (no scheme). Title strings like
# ![a](b.png "t") are not used anywhere in this repo; excluding whitespace from
# the target keeps the pattern from silently swallowing one if it ever appears.
IMAGE_RE = re.compile(
    r"!\[([^\]\n]*)\]\((?!https?:|data:|mailto:)([^)\s]+?("
    + "|".join(re.escape(e) for e in IMAGE_EXTS)
    + r"))\)",
    re.IGNORECASE,
)
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def split_locale(target: str) -> tuple[str, str, str]:
    """('a/b.en.png') -> ('a/b', '.en', '.png'); ('a/b.png') -> ('a/b', '', '.png').

    The extension keeps its original case, so an `.JPG` reference builds an
    `.en.JPG` sibling path. That is exact-match on a case-sensitive filesystem
    and would report MISSING against an existing `.en.jpg`. No uppercase-
    extension references exist in the repo; normalise here if any appear.
    """
    dot = target.rfind(".")
    stem, ext = target[:dot], target[dot:]
    for suffix in LOCALE_SUFFIXES:
        if stem.endswith(suffix):
            return stem[: -len(suffix)], suffix, ext
    return stem, "", ext


def _display_path(p: Path) -> str:
    """Repo-relative path for reporting, or the absolute path if it escapes.

    A reference like `![x](../../shared/logo.png)` can resolve outside the repo.
    Path.relative_to raises ValueError there, and an unhandled traceback exits
    non-zero — which would fail the CI step even under --advisory, whose whole
    contract is to warn without blocking.
    """
    resolved = p.resolve()
    try:
        return resolved.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return resolved.as_posix()


def iter_mirror_files(root: Path):
    for md_suffix, asset_suffix, glob in LOCALES:
        for fp in sorted(root.rglob(glob)):
            # Match on the path RELATIVE to the repo root. Testing fp.parts
            # instead matches directory names anywhere in the absolute path, so
            # a checkout living under e.g. `.claude/worktrees/<name>/` excludes
            # every file in the repo and the gate reports a silent all-clear.
            if any(part in EXCLUDE_DIRS for part in fp.relative_to(root).parts):
                continue
            yield asset_suffix, fp


def scan_file(asset_suffix: str, fp: Path):
    """Yield (line_no, whole_ref, target, sibling_rel, kind) per finding."""
    lines = fp.read_text(encoding="utf-8").split("\n")
    in_fence = False
    for i, line in enumerate(lines, start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in IMAGE_RE.finditer(line):
            target = m.group(2)
            stem, existing_suffix, ext = split_locale(target)
            if existing_suffix:
                continue  # already locale-qualified
            sibling_rel = f"{stem}{asset_suffix}{ext}"
            kind = "RETARGET" if (fp.parent / sibling_rel).exists() else "MISSING"
            yield i, m.group(0), target, sibling_rel, kind


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="rewrite RETARGET hits in place")
    ap.add_argument("--advisory", action="store_true", help="report but always exit 0")
    ap.add_argument("--quiet", action="store_true", help="summary lines only")
    args = ap.parse_args()

    # Report contains ✓ and CJK paths; make stdout UTF-8 so a Windows console
    # (cp950/cp1252) can print it. CI on ubuntu-latest is already UTF-8.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    retarget = missing = files_touched = 0
    missing_assets: set[str] = set()
    for asset_suffix, fp in iter_mirror_files(REPO_ROOT):
        hits = list(scan_file(asset_suffix, fp))
        if not hits:
            continue
        files_touched += 1
        rel = fp.relative_to(REPO_ROOT).as_posix()
        if not args.quiet:
            print(f"--- {rel} ({len(hits)})")
        for line_no, _whole, target, sibling_rel, kind in hits:
            if kind == "RETARGET":
                retarget += 1
            else:
                missing += 1
                missing_assets.add(_display_path(fp.parent / sibling_rel))
            if not args.quiet:
                arrow = "->" if kind == "RETARGET" else "needs"
                print(f"    {line_no}: [{kind}] {target}  {arrow}  {sibling_rel}")

        if args.apply:
            fixable = [h for h in hits if h[4] == "RETARGET"]
            if fixable:
                text = fp.read_text(encoding="utf-8")
                for _, whole, target, sibling_rel, _ in fixable:
                    text = text.replace(whole, whole.replace(f"]({target})", f"]({sibling_rel})"), 1)
                fp.write_text(text, encoding="utf-8")

    total = retarget + missing
    print()
    if args.apply:
        print(f"Rewrote {retarget} retargetable image reference(s).")
    else:
        print(f"Found {total} cross-locale image reference(s) in {files_touched} mirror file(s): "
              f"{retarget} retargetable, {missing} missing-asset.")
    if missing_assets:
        print(f"\n{len(missing_assets)} asset(s) need producing before those can be fixed:")
        for path in sorted(missing_assets):
            print(f"    {path}")
        print("  Source prompts: resources/diagrams/locale-variant-prompts.md")
    if retarget and not args.apply:
        print("\nFix the retargetable ones with: python scripts/check-locale-images.py --apply")

    if not total:
        print("✓ All mirror pages embed their own locale's images.")
        return 0
    if args.advisory:
        print("\n::warning::Image locale parity: "
              f"{total} reference(s) still point at another locale's asset. "
              "Advisory only — not blocking this PR.")
        return 0
    return 1 if not args.apply else 0


if __name__ == "__main__":
    sys.exit(main())
