#!/usr/bin/env python3
"""
Internal anchor validator.

掃所有 .md 內的 cross-file + same-file anchor link、驗 anchor 真實存在
target file 的 H1-H6 內。GitHub markdown slugification 規則。

Usage:
    python scripts/check-anchors.py [--strict]

Exit codes:
    0 — 全部 anchor 都 valid
    1 — 有 broken anchor（strict mode）/ 一律 0（non-strict）

排除：.ai/, book/, node_modules/, .git/, archives/ 目錄。

mirror 檔（*.en.md / *.zh-Hans.md）**現在也驗**——歷史上曾排除（理由是
「漸進翻譯、anchor 可能晚於 zh-TW 同步」），但該豁免讓 97 個壞掉的對外
anchor 在 39 個 mirror 檔裡無聲累積（2026-05 P3e 清查）。全部修好後改為
強制驗，mirror outbound anchor 從此跟 canonical 同標準、回歸即時擋下。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# --- Config ---
# '.claude' holds git worktrees (.claude/worktrees/<name>/), each a full second copy
# of the tree. This walker uses Path.rglob, which — unlike glob.glob — descends into
# dot-directories, so a stray worktree doubles the work and can fail the build on a
# stale copy nobody is editing. Found 2026-08-02 alongside the same bug in
# zh-hans-localize.py and check-2026-freshness.py.
EXCLUDE_DIRS = {'.ai', 'book', 'node_modules', '.git', '.claude', 'archives', '.coord', '_build', '_site'}
EXCLUDE_PATTERNS: list[str] = []  # mirror files now validated (see module docstring)

# Markdown link with anchor: [text](path.md#anchor) or [text](#anchor)
# Anchor part: starts with # then any non-) char
ANCHOR_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]*?)#([^)]+)\)')

# Markdown header: ## or ### etc., capture H2-H6
HEADER_RE = re.compile(r'^(#{1,6})\s+(.+?)\s*$', re.MULTILINE)

# NOTE: a `CODE_FENCE_RE = re.compile(r'^```')` used to live here. It was never
# referenced — strip_code_blocks did its own `line.startswith` — and it encodes
# the fence rule that issue #95 proved wrong (any ``` opens or closes). Removed
# rather than left as a trap. The real fence matcher is _FENCE_RE below.


def slugify(text: str) -> str:
    """
    GitHub-style anchor slug (matches github-slugger npm package).

    Critical: GitHub does NOT collapse consecutive whitespace — each space
    becomes its own hyphen. So "Foo — Bar" (space em-dash space, em-dash
    removed) → "foo  bar" (2 spaces) → "foo--bar" (2 hyphens).

    Steps:
    1. Strip leading/trailing whitespace
    2. Lowercase ASCII (preserve Chinese characters)
    3. Remove emoji and other symbols (broad Unicode ranges including ⭐ U+2B50)
    4. Remove CJK punctuation: · ／ 「 」 、 （ ） 【 】 《 》 〈 〉 〔 〕
    5. Remove ASCII punctuation: . , : ; ! ? " ' / \\ ` ( ) — – etc.
       Keep: word chars, whitespace, hyphen, Chinese chars
    6. Replace EACH space with hyphen (one-to-one, no collapse)

    Does NOT strip leading/trailing hyphens (matches GitHub behaviour —
    a leading hyphen from a removed emoji at heading start IS preserved).
    """
    s = text.strip()
    # Lowercase ASCII (Chinese unaffected)
    s = s.lower()
    # Remove emoji & misc symbols
    # Ranges:
    #   U+1F000-U+1FFFF — emoji / pictographs
    #   U+2600-U+27BF   — misc symbols + dingbats (☀-➿)
    #   U+2300-U+23FF   — misc technical (⌀-⏿)
    #   U+2B00-U+2BFF   — misc symbols and arrows (⬀-⯿, includes ⭐)
    #   U+2900-U+297F   — supplemental arrows-B (⤀-⥿)
    s = re.sub(
        r'[\U0001F000-\U0001FFFF☀-➿⌀-⏿⬀-⯿⤀-⥿]',
        '',
        s,
    )
    # Remove CJK punctuation
    s = re.sub(r'[·／「」、（）【】《》〈〉〔〕]', '', s)
    # Remove ASCII punctuation (keep word chars, whitespace, hyphen, Chinese)
    s = re.sub(r"[^\w\s\-一-鿿]", '', s)
    # Each space → hyphen (NO collapse; matches github-slugger)
    s = s.replace(' ', '-')
    return s


_FENCE_RE = re.compile(r'^ {0,3}(`{3,}|~{3,})(.*)$')


def strip_code_blocks(content: str, source: str | None = None) -> str:
    """Blank out fenced code blocks, following CommonMark's fence rules.

    A naive "toggle on any line starting with ```" is WRONG in two ways that
    both shipped defects (issue #95):

    1. **A closing fence may not carry an info string.** In

           ```                <- opens
           ```python          <- info string, so this is CONTENT
           ...
           ```                <- THIS closes the block opened on line 1
           ```                <- and THIS opens a new one

       the naive toggler pairs 1-2 and 3-4, while the renderer pairs 1-3 and
       leaves 4 opening an unterminated block. In
       examples/stage-4/04-codeact-vs-json-tool/README.* that swallowed four
       `##` headings into a code block on the published site while every gate
       read green, because the gate and the renderer disagreed about which
       lines were code.

    2. **A closing fence must be at least as long as its opener**, which is how
       a block legitimately contains a shorter fence — the fix applied to those
       three files. A toggler treats the inner fence as a terminator.

    Also handles `~~~` fences and the up-to-3-space indent CommonMark allows.
    Lines are blanked rather than dropped so line numbers stay correct for
    diagnostics.

    KNOWN DEVIATIONS — this follows CommonMark, which is what GitHub renders,
    and GitHub is what check-anchors.py validates against. The site's renderer
    (pymdownx.superfences) differs in a few corners. All four are theoretical
    in this repo today (measured: zero occurrences of each), and each is listed
    so nobody reads "follows CommonMark" as "matches the site exactly":

      * 1-3 space indent at top level — CommonMark/GitHub accept it as a fence;
        superfences only honours indentation matching the container's content
        indent, so at top level it renders as a paragraph. Inside a list item
        both agree it is code, and that IS exercised in this repo (CLAUDE.md).
      * Unterminated fence at EOF — GitHub runs it to end of document, as here;
        superfences does not make a block at all. Now warns, see below.
      * 4-space indented code blocks — not handled at all. No fence markers in
        this repo are indented that far.
      * Backtick inside a backtick info string — handled, both renderers agree
        it is not a fence.
      * Fence inside a BLOCKQUOTE (`> ```bash`) — not recognised at all, since
        _FENCE_RE cannot match a `>`-prefixed line. Both renderers treat it as
        code, so the gate OVER-validates: it will check a link that renders as
        literal text. That direction is a loud false positive rather than
        silent under-validation. Latent here — 3 files, 6 fence lines, all one
        trio in walkthroughs/build-first-agent-in-7-steps.*, with no anchor
        links or headings inside them. Not a regression: the previous parser
        missed blockquote fences too.
    """
    out = []
    fence_char: str | None = None
    fence_len = 0
    for line in content.split('\n'):
        m = _FENCE_RE.match(line)
        if m:
            marker, rest = m.group(1), m.group(2)
            char = marker[0]
            if fence_char is None:
                # Opening fence. An info string is allowed — except that a
                # backtick info string may not itself contain a backtick
                # (CommonMark; pymdownx.superfences agrees, its language class
                # is [\w#.+-]+). Treating ```foo`bar as an opener would hide
                # the rest of the file from the gate while the renderer keeps
                # rendering it — the same divergence shape as #93/#95.
                if char == '`' and '`' in rest:
                    out.append(line)
                    continue
                fence_char, fence_len = char, len(marker)
                out.append('')
                continue
            # Inside a block: only a bare fence of the same char and at least
            # the opener's length closes it. Anything else is content.
            if char == fence_char and len(marker) >= fence_len and not rest.strip():
                fence_char, fence_len = None, 0
                out.append('')
                continue
            out.append('')
            continue
        out.append('' if fence_char is not None else line)

    if fence_char is not None and source is not None:
        # Everything from the unterminated fence to EOF was skipped. GitHub
        # agrees (an unclosed fence runs to end of document) but the site's
        # renderer does not, so the gate is now validating less than is
        # published — and would still print "All internal anchors valid".
        # Say so rather than under-validate in silence.
        #
        # Only warns when a source is named, so unit-test fixtures (which use
        # unterminated fences deliberately) do not emit CI annotations.
        # stdout, matching main()'s ::warning:: convention in this file.
        print(
            f'::warning::{source}: unterminated {fence_char * fence_len} fence — '
            f'the anchor gate skipped everything after it'
        )

    return '\n'.join(out)


def collect_anchors(content: str) -> set[str]:
    """All anchor slugs available in this file (from H1-H6)."""
    return {slugify(m.group(2)) for m in HEADER_RE.finditer(content)}


def parse_anchor_links(content: str, file_path: Path) -> list[tuple[int, str, str]]:
    """
    Extract (line_no, target_file, anchor) tuples from anchor-style links.
    Skips matches inside code blocks.
    """
    clean = strip_code_blocks(content, source=str(file_path))
    results = []
    for lineno, line in enumerate(clean.split('\n'), 1):
        for m in ANCHOR_LINK_RE.finditer(line):
            target_raw = m.group(2).strip()
            anchor = m.group(3).strip()
            # Skip external URLs (http://..., https://...)
            if target_raw.startswith(('http://', 'https://')):
                continue
            results.append((lineno, target_raw, anchor))
    return results


def should_skip(path: Path, repo_root: Path) -> bool:
    """Skip excluded dirs. Mirror files are validated (EXCLUDE_PATTERNS
    is empty by default; kept as a hook if a pattern ever needs re-adding)."""
    # Match on the path RELATIVE to the repo root. Testing path.parts instead
    # matches directory names anywhere in the ABSOLUTE path, so a checkout under
    # e.g. `.claude/worktrees/<name>/` skips every file and the gate reports a
    # silent all-clear. See the 2026-08-02 CHANGELOG entry — the same bug shipped
    # in check-locale-links.py and was live in check-catalog-counts.py.
    if any(part in EXCLUDE_DIRS for part in path.relative_to(repo_root).parts):
        return True
    for pat in EXCLUDE_PATTERNS:
        if path.name.endswith(pat):
            return True
    return False


def validate_file(path: Path, repo_root: Path) -> list[tuple[Path, int, str]]:
    """Validate anchors in one file. Returns list of (file, lineno, message)."""
    broken = []
    content = path.read_text(encoding='utf-8')
    own_anchors: set[str] | None = None  # lazy

    # Repo-relative, matching every other diagnostic this script prints.
    try:
        rel_for_msgs = path.relative_to(repo_root)
    except ValueError:
        rel_for_msgs = path

    for lineno, target_raw, anchor in parse_anchor_links(content, rel_for_msgs):
        anchor_slug = slugify(anchor)

        if target_raw == '':
            # Same-file anchor [text](#section)
            if own_anchors is None:
                own_anchors = collect_anchors(content)
            if anchor_slug not in own_anchors:
                broken.append((path, lineno, f'same-file anchor not found: #{anchor}'))
        else:
            # Cross-file: resolve target path relative to current file
            tgt_path = (path.parent / target_raw).resolve()
            try:
                tgt_path.relative_to(repo_root)
            except ValueError:
                # Target outside repo (shouldn't happen for relative .md links)
                continue
            if not tgt_path.exists():
                broken.append((path, lineno, f'target file not found: {target_raw}'))
                continue
            target_anchors = collect_anchors(tgt_path.read_text(encoding='utf-8'))
            if anchor_slug not in target_anchors:
                broken.append(
                    (path, lineno, f'anchor not found in {target_raw}: #{anchor}')
                )
    return broken


def main() -> int:
    # Force UTF-8 stdout so Chinese chars print correctly on Windows / older CI
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        except Exception:
            pass

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--strict', action='store_true', help='Exit 1 on broken anchors')
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    all_broken: list[tuple[Path, int, str]] = []

    for md in sorted(repo_root.rglob('*.md')):
        if should_skip(md, repo_root):
            continue
        try:
            all_broken.extend(validate_file(md, repo_root))
        except Exception as e:
            print(f'⚠ {md.relative_to(repo_root)}: scan error: {e}', file=sys.stderr)

    if not all_broken:
        print('✓ All internal anchors valid.')
        return 0

    for path, lineno, msg in all_broken:
        rel = path.relative_to(repo_root)
        prefix = '❌ ' if args.strict else '::warning::'
        print(f'{prefix}{rel}:{lineno}: {msg}')
    print(f'\nFound {len(all_broken)} broken anchor reference(s).')
    return 1 if args.strict else 0


if __name__ == '__main__':
    sys.exit(main())
