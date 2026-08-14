#!/usr/bin/env python3
"""Regression tests for scripts/check-links.py's failure classification.

Pins issue #94. The checker reported 14 failures of which only 5 were real —
a 64% wrong rate. A gate that wrong stops being read, which is worse than not
having one, because the real rot hides inside the noise.

Three causes, all pinned here:

1. **It identified itself.** The old UA ("awesome-agentic-ai-zh-link-check/1.0")
   was refused by several hosts and the report called those links BROKEN.

2. **HEAD is widely mis-implemented.** Measured on this repo's own links,
   `openai.com/chatgpt/desktop` answers HEAD 404 / GET 200, and
   `learnshell.org` answers HEAD 415 / GET 200. The old code retried with GET
   only on 405/403, so both were reported dead.

3. **A refusal is not a 404.** 401/403/429 mean the host is answering and
   declining to serve a script; nothing about the link is actionable. Worse,
   they are FLAKY — while triaging #94, three URLs returned 200 to a browser one
   day and 403 the next. Mixing them into the failure list is what teaches
   people to skip the output.

Plus a host-level-block probe: some hosts refuse with a code that normally means
something else. Every Meta domain (ai.meta.com, developer.meta.com, llama.com)
answers 400 to a non-browser client, INCLUDING its own root. Asking the root
turns "is this page gone or is this host blocking me" from a guess into a
measurement.

Run:  python scripts/test_check_links.py     (plain asserts, no pytest needed)
 or:  pytest scripts/test_check_links.py
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

_SPEC = importlib.util.spec_from_file_location(
    "check_links", Path(__file__).with_name("check-links.py")
)
cl = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(cl)


class _Resp:
    def __init__(self, status, url=""):
        self.status_code = status
        self.url = url

    def close(self):
        pass


class _Fake:
    """Stand-in for requests, driven by {(method, url): status}."""

    def __init__(self, head=None, get=None, final=None):
        self.head_map = head or {}
        self.get_map = get or {}
        self.final = final or {}
        self.calls = []

    def head(self, url, **kw):
        self.calls.append(("HEAD", url))
        if url not in self.head_map:
            raise AssertionError(f"unexpected HEAD {url}")
        return _Resp(self.head_map[url], self.final.get(url, url))

    def get(self, url, **kw):
        self.calls.append(("GET", url))
        if url not in self.get_map:
            raise AssertionError(f"unexpected GET {url}")
        return _Resp(self.get_map[url], self.final.get(url, url))


def _with(fake):
    """Swap cl.requests for a fake, keeping the real exception class."""
    fake.exceptions = cl.requests.exceptions
    old = cl.requests
    cl.requests = fake
    cl._root_cache.clear()  # memoized per host; a stale entry would fake a pass
    return old


def _restore(old):
    cl.requests = old


def test_head_404_but_get_200_is_not_a_failure() -> None:
    """The exact openai.com/chatgpt/desktop shape. HEAD lies; GET is the truth."""
    u = "https://example.com/page"
    f = _Fake(head={u: 404}, get={u: 200})
    old = _with(f)
    try:
        _, status, msg = cl.check_url(u)
    finally:
        _restore(old)
    assert status == 200, f"HEAD's 404 was trusted over GET's 200 (got {status})"
    assert ("GET", u) in f.calls, "no GET retry was attempted after a 4xx HEAD"


def test_head_415_but_get_200_is_not_a_failure() -> None:
    """learnshell.org's shape. 415 is outside the old 405/403 retry set."""
    u = "https://example.com/shell"
    f = _Fake(head={u: 415}, get={u: 200})
    old = _with(f)
    try:
        _, status, _ = cl.check_url(u)
    finally:
        _restore(old)
    assert status == 200, f"415 from HEAD was not retried with GET (got {status})"


def test_refusal_statuses_are_classified_unverifiable_not_dead() -> None:
    # Assert the MEMBERS, not just "iterate whatever is in the set". Iterating
    # the set under test means emptying it passes vacuously — that mutation
    # survived until this line was added.
    assert cl.UNVERIFIABLE_STATUSES == {401, 403, 429}, (
        "Exact equality, not a subset. A subset check permits WIDENING, and "
        "adding 404 to this set makes the gate structurally incapable of ever "
        "reporting a dead link again — which passed every test until this line. "
        f"got {cl.UNVERIFIABLE_STATUSES!r}"
    )
    for code in sorted(cl.UNVERIFIABLE_STATUSES):
        u = f"https://example.com/{code}"
        f = _Fake(head={u: code}, get={u: code})
        old = _with(f)
        try:
            _, status, _ = cl.check_url(u)
        finally:
            _restore(old)
        assert status == code, (
            f"{code} was not returned unchanged (got {status}) — a refusal must "
            "reach the caller as itself so it can be bucketed as unverifiable"
        )
        assert status not in cl.NOT_FOUND_STATUSES, (
            f"{code} must never be treated as 'resource is gone'"
        )


def test_host_level_block_is_not_reported_as_dead() -> None:
    """The Meta shape: a 400 whose own host root also 400s."""
    u = "https://developer.example.com/ai/models/x/"
    root = "https://developer.example.com/"
    f = _Fake(head={u: 400}, get={u: 400, root: 400})
    old = _with(f)
    try:
        _, status, msg = cl.check_url(u)
    finally:
        _restore(old)
    assert status == 400
    assert msg.startswith("host-level block"), (
        f"the host refuses everything including its own root, so this says nothing "
        f"about the page — got msg={msg!r}"
    )


def test_page_level_404_is_still_a_failure() -> None:
    """The guard must not swallow real rot: root is fine, page is gone."""
    u = "https://example.com/gone"
    root = "https://example.com/"
    f = _Fake(head={u: 404}, get={u: 404, root: 200})
    old = _with(f)
    try:
        _, status, msg = cl.check_url(u)
    finally:
        _restore(old)
    assert status == 404
    assert not msg.startswith("host-level block"), (
        "a genuinely dead page was excused as a host block — the root answered 200, "
        "so the host is NOT refusing us"
    )


def test_host_wide_404_does_not_excuse_a_page_level_404() -> None:
    """The C1 case. A host whose ROOT 404s must not make its dead pages invisible.

    `langchain-ai.github.io` is a GitHub Pages org site with no root page, so its
    root answers 404. The first version of the host-block probe therefore
    classified both dead LangGraph URLs from issue #94 as "host-level block — do
    not fix": the gate argued against the very commit that fixes them, and 37
    links across two *.github.io hosts became permanently undetectable.

    404/410 are the only codes that speak about the resource itself, so they must
    never reach the probe.
    """
    u = "https://org.github.io/proj/page/"
    root = "https://org.github.io/"
    f = _Fake(head={u: 404}, get={u: 404, root: 404})
    old = _with(f)
    try:
        _, status, msg = cl.check_url(u)
    finally:
        _restore(old)
    assert status == 404
    assert not msg.startswith("host-level block"), (
        "a host-wide 404 excused a page-level 404 — this is a GitHub Pages org "
        f"site with no root page, not a host refusing us. got msg={msg!r}"
    )
    assert ("GET", root) not in f.calls, (
        "the root was probed at all for a 404; 404/410 must short-circuit before "
        "the probe, otherwise every no-root-page host blinds the checker"
    )


def test_root_probe_follows_redirects_to_the_final_host() -> None:
    """llama.com's shape: a root that redirects to another host which blocks."""
    u = "https://www.llama.com/"
    final = "https://developer.meta.example/ai/"
    root = "https://developer.meta.example/"
    f = _Fake(head={u: 400}, get={u: 400, root: 400}, final={u: final})
    old = _with(f)
    try:
        _, status, msg = cl.check_url(u)
    finally:
        _restore(old)
    assert msg.startswith("host-level block"), (
        "the requested URL is itself a root, so its own root proves nothing; the "
        f"root it REDIRECTS to is the one to ask — got msg={msg!r}"
    )


def test_login_gated_urls_are_skipped_entirely() -> None:
    u = next(iter(cl.LOGIN_GATED))
    f = _Fake()  # any request at all would raise
    old = _with(f)
    try:
        _, status, msg = cl.check_url(u)
    finally:
        _restore(old)
    assert status is None and msg.startswith("skipped"), (
        "a URL that requires a signed-in session must not be probed every run"
    )
    assert not f.calls, "login-gated URL was still requested"


def test_browser_user_agent_is_sent() -> None:
    """The identifying UA was itself the cause of 3 of 14 reported failures."""
    ua = cl.BROWSER_HEADERS["User-Agent"]
    assert "Mozilla/5.0" in ua, f"not a browser UA: {ua!r}"
    assert "link-check" not in ua, (
        "the checker identifies itself again; hosts refuse that UA and the report "
        "then calls working links broken"
    )


def test_code_block_urls_are_not_checked() -> None:
    """URLs inside fenced samples are not links (issue #97 wired this up)."""
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "t.md"
        p.write_text(
            "[real](https://example.com/real)\n\n"
            "```\n[sample](https://example.com/in-code)\n```\n",
            encoding="utf-8",
        )
        urls = [u for _, u in cl.extract_urls(p)]
    assert "https://example.com/real" in urls
    assert "https://example.com/in-code" not in urls, (
        "a URL inside a code sample was queued for a network check"
    )


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    tests = [(n, f) for n, f in sorted(globals().items())
             if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
        except AssertionError as e:
            failed += 1
            print(f"FAIL {name}\n  {e}")
        except BaseException as e:
            failed += 1
            print(f"ERROR {name}: {type(e).__name__}: {e}")
    if failed:
        print(f"\n{failed}/{len(tests)} failed.")
        return 1
    print(f"{len(tests)}/{len(tests)} passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
