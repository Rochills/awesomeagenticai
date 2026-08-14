#!/usr/bin/env python3
"""
check-links.py — 掃描所有 markdown 檔案的 URL，回報 4xx / 5xx / timeout。

用法：
    python scripts/check-links.py            # 檢查所有 .md 檔
    python scripts/check-links.py --fast     # 只查 GitHub repos（最容易 404）
    python scripts/check-links.py --quiet    # 只印失敗

環境需求：
    pip install requests
"""

import argparse
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md_fences import strip_code_blocks  # noqa: E402
from typing import Iterable

try:
    import requests
except ImportError:
    print("ERROR: 需要 requests。請先執行：pip install requests", file=sys.stderr)
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
MD_GLOB = "**/*.md"
EXCLUDE_DIRS = {".git", ".ai", "node_modules", "_build", ".venv"}

# 抓 markdown link [text](url) 的正則。處理 url 內可能含巢狀 ()。
# 用「至少 1 個非空白非右括號字元，後接任意可選 (...) 對」的策略。
LINK_RE = re.compile(
    r"\[([^\]]+)\]"
    r"\((https?://[^\s()]+(?:\([^\s()]*\))?[^\s)]*)\)"
)

TIMEOUT = 15
MAX_WORKERS = 10


def find_md_files(root: Path) -> list[Path]:
    files = []
    for fp in root.glob(MD_GLOB):
        # Relative to `root`, not fp.parts — matching the ABSOLUTE path makes a
        # checkout under an excluded-looking directory (e.g. `.ai/`, `book/`,
        # `.claude/worktrees/`) skip everything and report a silent all-clear.
        # Same bug as the 2026-08-02 check-locale-links.py fix.
        if any(part in EXCLUDE_DIRS for part in fp.relative_to(root).parts):
            continue
        files.append(fp)
    return files


def extract_urls(md_path: Path) -> list[tuple[int, str]]:
    """回傳 [(line_no, url), ...]，跳過程式碼區塊內的 URL。"""
    urls = []
    # Fenced code blanked by the shared parser (md_fences), not a local toggle —
    # see #95/#97. Without this the checker fetches every URL in every code
    # sample, which is both slow and a source of phantom "dead link" reports.
    text = strip_code_blocks(
        md_path.read_text(encoding="utf-8"), source=str(md_path)
    )
    for line_no, line in enumerate(text.splitlines(), start=1):
        # 也跳過 inline code（粗略：只在 ` ` 之間的 URL 不算）
        # Markdown 規範允許 inline code 內含 link 但通常不是真 link
        for match in LINK_RE.finditer(line):
            url = match.group(2).rstrip(".,;:!?")
            urls.append((line_no, url))
    return urls


# A real browser's headers. The old identifying UA
# ("awesome-agentic-ai-zh-link-check/1.0") was refused by several hosts, and the
# report then called those links BROKEN. A checker that is wrong that often stops
# being read, which is worse than not having one — see issue #94, where 3 of 14
# reported failures were nothing but this.
BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Statuses a checker CANNOT resolve: the server is answering, it just will not
# answer us. Login walls, bot/geo walls, rate limits. Reported separately and
# NOT counted as failures, because acting on them is impossible and their
# flakiness is what trains people to ignore the whole report — the same three
# URLs returned 200 to a browser one day and 403 the next while triaging #94.
UNVERIFIABLE_STATUSES = {401, 403, 429}

# 404/410 are the ONLY codes that speak about THIS resource. Every other 4xx can
# plausibly be about the host, which is what the root probe below is for — but a
# host-wide 404 must never excuse a page-level 404, or the checker loses the one
# thing it exists to detect.
#
# This is not hypothetical: `langchain-ai.github.io` is a GitHub Pages org site
# with no root page, so its root answers 404. Without this exclusion the probe
# classified both dead LangGraph URLs from issue #94 as "host-level block — do
# not fix", i.e. the gate would have argued against the commit that fixes them,
# and 33 links on that host plus 4 on deepseek-harness.github.io would have gone
# permanently undetectable.
NOT_FOUND_STATUSES = {404, 410}

# URLs that are correctly unreachable and always will be: they need a signed-in
# session. Listing them keeps them out of the report entirely rather than having
# a human re-triage them every run.
LOGIN_GATED = {
    "https://www.zotero.org/settings/keys",  # requires a Zotero account session
}


# Root probes are memoized per host: N dead links on one blocked host would
# otherwise mean N identical root requests. Short timeout — the probe is
# advisory, and a hanging one must not stall the whole run.
_ROOT_TIMEOUT = 5
_root_cache: dict[str, int | None] = {}
_root_lock = threading.Lock()


def _root_status(root: str) -> int | None:
    with _root_lock:
        if root in _root_cache:
            return _root_cache[root]
    try:
        rr = requests.get(root, timeout=_ROOT_TIMEOUT, allow_redirects=True,
                          stream=True, headers=BROWSER_HEADERS)
        rr.close()
        status = rr.status_code
    except requests.exceptions.RequestException:
        status = None
    with _root_lock:
        _root_cache[root] = status
    return status


ATTEMPTS = 2
RETRY_DELAY = 2


def check_url(url: str, fast_mode: bool = False) -> tuple[str, int | None, str]:
    """回傳 (url, final_status_code or None, message)。allow_redirects=True 表示
    final_status 不會是 3xx（會被 follow 到 2xx 或 4xx/5xx）。"""
    if fast_mode and "github.com" not in url:
        return url, None, "skipped (--fast)"
    if url in LOGIN_GATED:
        return url, None, "skipped (login-gated)"

    # A bounded LOOP, deliberately not recursion. The first version of this retry
    # called check_url again; flipping its guard to always-true turned it into an
    # unbounded recursion sleeping RETRY_DELAY per level — a multi-thousand-second
    # hang rather than a red test. A loop cannot express that bug.
    for attempt in range(1, ATTEMPTS + 1):
        try:
            r = requests.head(url, timeout=TIMEOUT, allow_redirects=True,
                              headers=BROWSER_HEADERS)
            # Retry with GET on ANY 4xx. HEAD is widely mis-implemented — measured on
            # this repo's own links, openai.com/chatgpt/desktop answers HEAD 404 and
            # GET 200, and learnshell.org answers HEAD 415 and GET 200. Retrying only
            # on 405/403 (the old behaviour) reported both as dead.
            if 400 <= r.status_code < 500:
                r = requests.get(url, timeout=TIMEOUT, allow_redirects=True, stream=True,
                                 headers=BROWSER_HEADERS)
                r.close()
            status = r.status_code

            # A 4xx that is NOT one of the obvious refusal codes might still be a
            # host-level block rather than a missing page. Ask the host's own root:
            # if that returns the same status, the host is refusing us and says
            # nothing about this URL. Measured case — every Meta domain
            # (ai.meta.com, developer.meta.com, llama.com) answers 400 to a
            # non-browser client, including its own root.
            if (400 <= status < 500
                    and status not in UNVERIFIABLE_STATUSES
                    and status not in NOT_FOUND_STATUSES):
                # Derive the root from the FINAL url, not the requested one. llama.com
                # is itself a root and redirects to developer.meta.com/ai/, so probing
                # its own root proves nothing; probing the root it LANDS on does.
                parts = urlsplit(r.url or url)
                root = f"{parts.scheme}://{parts.netloc}/"
                if root.rstrip("/") != url.rstrip("/"):
                    root_status = _root_status(root)
                    if root_status == status:
                        return url, status, f"host-level block ({parts.netloc} root returns the same)"

            return url, status, ""
        except requests.exceptions.RequestException as e:
            # One retry before calling a link dead. A single connection blip on
            # one of 700 URLs would otherwise fail the whole run, which is the
            # same "report is wrong, so nobody reads it" problem this file is
            # fixing — observed live while building this: one run exited 1, the
            # next exited 0 with no change to the tree.
            if attempt < ATTEMPTS:
                time.sleep(RETRY_DELAY)
                continue
            return url, None, str(e)[:80]


def main():
    # This script prints ✓ / ❌ / ⚠ and CJK paths. A default Windows console is
    # cp950, where the first ✓ raises UnicodeEncodeError and kills the run
    # PART WAY THROUGH — so the summary and the failure list never appear and
    # the output looks like a crash rather than a report. Every other gate in
    # scripts/ already does this; check-links did not.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (AttributeError, ValueError):
                pass

    parser = argparse.ArgumentParser(description="Check markdown links for rot.")
    parser.add_argument("--fast", action="store_true", help="只查 GitHub URL")
    parser.add_argument("--quiet", action="store_true", help="只印失敗")
    args = parser.parse_args()

    files = find_md_files(REPO_ROOT)
    print(f"Scanning {len(files)} markdown files...", file=sys.stderr)

    # 收集所有 URL（去重，但記下出現位置）
    occurrences: dict[str, list[tuple[Path, int]]] = {}
    for fp in files:
        for line_no, url in extract_urls(fp):
            occurrences.setdefault(url, []).append((fp, line_no))

    print(f"Found {len(occurrences)} unique URLs.", file=sys.stderr)

    failures = []       # actionable: the link is dead, fix or remove it
    unverifiable = []    # the server answered, but refuses non-browser clients
    ok_count = 0
    skipped = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(check_url, url, args.fast): url for url in occurrences}
        for i, fut in enumerate(as_completed(futures), start=1):
            url, status, msg = fut.result()
            if status is None and msg.startswith("skipped"):
                skipped += 1
                continue
            if status is None:
                failures.append((url, f"ERROR: {msg}"))
                if not args.quiet:
                    print(f"[{i}/{len(occurrences)}] ❌ {url} — {msg}")
            elif status in UNVERIFIABLE_STATUSES or msg.startswith("host-level block"):
                # Not a failure. The page exists; the host just will not serve a
                # script. Mixing these in with real 404s is what produced a 40%
                # wrong-report rate and taught everyone to skip the output.
                why = f"HTTP {status}" + (f" — {msg}" if msg else "")
                unverifiable.append((url, why))
                if not args.quiet:
                    print(f"[{i}/{len(occurrences)}] ⚠ {url} — {why} (unverifiable)")
            elif status >= 400:
                failures.append((url, f"HTTP {status}"))
                if not args.quiet:
                    print(f"[{i}/{len(occurrences)}] ❌ {url} — HTTP {status}")
            else:
                # 200-299 (3xx 已被 allow_redirects 跟過去 → final 是 2xx 或 4xx/5xx)
                ok_count += 1
                if not args.quiet:
                    print(f"[{i}/{len(occurrences)}] ✓ {url}")

    # 報告
    print()
    print("=" * 60)
    print(f"Total checked:   {len(occurrences) - skipped}")
    print(f"OK (2xx):        {ok_count}")
    print(f"Failed:          {len(failures)}")
    print(f"Unverifiable:    {len(unverifiable)}  (host refuses non-browser clients, or blocks at host level)")
    if skipped:
        # Printed unconditionally. Under --fast this is the GitHub-only filter;
        # in a full run it is the LOGIN_GATED list, and without this line those
        # URLs just vanish between "Found N" and "Total checked N-1".
        print(f"Skipped:         {skipped}  (--fast filter and/or login-gated)")
    print()

    if failures:
        print("=== Failures by file (ACTIONABLE — the link is dead) ===")
        for url, reason in failures:
            print(f"\n❌ {url}  [{reason}]")
            for fp, line_no in occurrences[url]:
                rel = fp.relative_to(REPO_ROOT)
                print(f"   {rel}:{line_no}")

    # Printed even under --quiet. Every automated invocation passes --quiet,
    # and --quiet is documented as "只印失敗" — but these are exactly what a
    # human still has to eyeball, since nothing else will ever flag them.
    if unverifiable:
        print()
        print("=== Unverifiable (NOT failures — do not 'fix' these) ===")
        print("The host answered and refused a non-browser client. The page may be")
        print("perfectly fine in a browser; these same URLs have flipped between 200")
        print("and 403 between runs. Open one yourself before touching the link.")
        for url, reason in unverifiable:
            print(f"\n⚠ {url}  [{reason}]")
            for fp, line_no in occurrences[url]:
                rel = fp.relative_to(REPO_ROOT)
                print(f"   {rel}:{line_no}")

    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
