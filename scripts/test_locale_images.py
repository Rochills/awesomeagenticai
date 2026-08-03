#!/usr/bin/env python3
"""Regression tests for scripts/check-locale-images.py.

Pins the 2026-08 finding: 9 image references on .en.md / .zh-Hans.md pages
embedded Traditional-Chinese-only diagram assets. The alt text was localized but
the picture was not, so an English reader got an English caption above a diagram
rendered entirely in Traditional Chinese. No gate saw it — check-locale-links.py
matches `.md` targets only, so image paths are outside every existing check.

The checker rewrites reference targets under --apply, so a false positive breaks
a working image. These tests pin every exemption.

Run:  python scripts/test_locale_images.py     (plain asserts, no pytest needed)
 or:  pytest scripts/test_locale_images.py
"""
import importlib.util
import tempfile
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "check_locale_images", Path(__file__).with_name("check-locale-images.py")
)
cli = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(cli)

REPO_ROOT = Path(__file__).resolve().parent.parent


def _scan(body: str, suffix: str = ".en", assets=()):
    """Write body to a temp mirror file, create assets, return findings."""
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        for a in assets:
            (root / a).parent.mkdir(parents=True, exist_ok=True)
            (root / a).write_bytes(b"\x89PNG")
        fp = root / f"page{suffix}.md"
        fp.write_text(body, encoding="utf-8")
        return list(cli.scan_file(suffix, fp))


# --- the two finding classes -------------------------------------------------

def test_missing_when_no_sibling():
    """All 9 real-world hits are this class: the variant does not exist yet."""
    hits = _scan("![RAG](d/rag.jpg)\n")
    assert len(hits) == 1
    _, _, target, sibling, kind = hits[0]
    assert (target, sibling, kind) == ("d/rag.jpg", "d/rag.en.jpg", "MISSING")


def test_retarget_when_sibling_exists():
    hits = _scan("![RAG](d/rag.jpg)\n", assets=("d/rag.en.jpg",))
    assert len(hits) == 1
    assert hits[0][3] == "d/rag.en.jpg" and hits[0][4] == "RETARGET"


# --- exemptions --------------------------------------------------------------

def test_ignores_already_locale_suffixed():
    assert _scan("![RAG](d/rag.en.jpg)\n", assets=("d/rag.en.jpg",)) == []


def test_ignores_zh_hans_suffixed_asset():
    """`.zh-Hans` must be recognised as a locale suffix, not read as part of the stem."""
    assert _scan("![x](d/rag.zh-Hans.jpg)\n", suffix=".zh-Hans") == []


def test_ignores_external_urls():
    assert _scan("![badge](https://img.shields.io/badge/a-b.svg)\n") == []


def test_ignores_images_inside_fenced_code():
    assert _scan("```markdown\n![RAG](d/rag.jpg)\n```\n") == []


def test_ignores_markdown_links():
    """Must not touch .md links — that is check-locale-links.py's job."""
    assert _scan("See [docs](target.md) and [x](../a/b.md).\n") == []


def test_ignores_non_image_extensions():
    assert _scan("[data](d/table.csv) [z](d/a.zip)\n") == []


# --- locale + path handling --------------------------------------------------

def test_zh_hans_locale():
    hits = _scan("![图](d/rag.jpg)\n", suffix=".zh-Hans")
    assert hits[0][3] == "d/rag.zh-Hans.jpg"


def test_relative_parent_path():
    """Every real hit uses `../resources/diagrams/...` from stages/ or branches/."""
    hits = _scan("![RAG](../resources/d/rag.jpg)\n")
    assert hits[0][3] == "../resources/d/rag.en.jpg"


def test_reference_escaping_repo_root_does_not_crash():
    """Regression: `..`-heavy refs can resolve outside the repo.

    Path.relative_to raises ValueError there; an unhandled traceback exits
    non-zero and fails the CI step even under --advisory, whose whole contract
    is to warn without blocking. _display_path must degrade, not raise.
    """
    outside = REPO_ROOT.parent / "shared" / "logo.en.png"
    assert _display_path_ok(outside)
    inside = REPO_ROOT / "resources" / "diagrams" / "x.en.png"
    assert cli._display_path(inside) == "resources/diagrams/x.en.png"


def _display_path_ok(p: Path) -> bool:
    try:
        return bool(cli._display_path(p))
    except ValueError:
        return False


def test_all_image_extensions_detected():
    body = "".join(f"![a](d/x{e})\n" for e in cli.IMAGE_EXTS)
    assert len(_scan(body)) == len(cli.IMAGE_EXTS)


def test_split_locale():
    assert cli.split_locale("a/b.png") == ("a/b", "", ".png")
    assert cli.split_locale("a/b.en.png") == ("a/b", ".en", ".png")
    assert cli.split_locale("a/b.zh-Hans.png") == ("a/b", ".zh-Hans", ".png")
    # a dotted directory must not be mistaken for a locale suffix
    assert cli.split_locale("../a.b/c.jpg") == ("../a.b/c", "", ".jpg")


# --- the exclusion bug this gate shipped with --------------------------------

def test_excludes_are_relative_to_repo_root():
    """Regression: EXCLUDE_DIRS matched against the ABSOLUTE path.

    A checkout under `.claude/worktrees/<name>/` put `.claude` in every file's
    fp.parts, so every file was excluded and the gate printed a clean all-clear
    while 9 real violations sat in the tree. check-locale-links.py shipped the
    same bug; both now match on the path relative to the repo root.
    """
    with tempfile.TemporaryDirectory() as d:
        root = Path(d) / ".claude" / "worktrees" / "wt"
        (root / "stages").mkdir(parents=True)
        (root / "stages" / "p.en.md").write_text("![a](../d/x.jpg)\n", encoding="utf-8")
        found = list(cli.iter_mirror_files(root))
        assert len(found) == 1, "file under a .claude-prefixed root must still be scanned"
        assert found[0][0] == ".en"


def test_excluded_dirs_still_skipped_when_genuinely_nested():
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "node_modules").mkdir()
        (root / "node_modules" / "p.en.md").write_text("![a](x.jpg)\n", encoding="utf-8")
        assert list(cli.iter_mirror_files(root)) == []


# --- --apply semantics -------------------------------------------------------

def test_apply_fixes_retarget_only():
    """--apply must rewrite RETARGET and leave MISSING alone.

    Retargeting a MISSING reference would point the page at a file that does not
    exist, turning a wrong-locale image into a broken one.
    """
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "d").mkdir()
        (root / "d" / "has.en.jpg").write_bytes(b"\x89PNG")
        fp = root / "page.en.md"
        fp.write_text("![a](d/has.jpg)\n![b](d/none.jpg)\n", encoding="utf-8")
        hits = list(cli.scan_file(".en", fp))
        kinds = {h[2]: h[4] for h in hits}
        assert kinds == {"d/has.jpg": "RETARGET", "d/none.jpg": "MISSING"}


def test_alt_text_preserved_in_capture():
    """The whole-reference capture keeps alt text so --apply re-emits it intact."""
    hits = _scan("![RAG Pipeline Overview](d/rag.jpg)\n")
    assert hits[0][1] == "![RAG Pipeline Overview](d/rag.jpg)"


# --- live repo invariants ----------------------------------------------------

def test_repo_has_no_retargetable_references():
    """Hard invariant: if a locale variant exists on disk, the page must use it.

    Unlike the MISSING backlog this needs no new artwork — it is always a bug.
    """
    bad = [
        (fp.relative_to(REPO_ROOT).as_posix(), h[0], h[2])
        for suffix, fp in cli.iter_mirror_files(REPO_ROOT)
        for h in cli.scan_file(suffix, fp)
        if h[4] == "RETARGET"
    ]
    assert bad == [], f"mirror pages ignoring an existing locale variant: {bad}"


def test_no_missing_variants():
    """The 2026-08-02 backlog of 9 was cleared the same day; it must stay at 0.

    A MISSING hit means a mirror page embeds an asset that has no same-locale
    sibling — no script can fix that, someone has to produce the artwork. Add
    it with the source prompt in resources/diagrams/locale-variant-prompts.md.
    """
    missing = [
        (fp.relative_to(REPO_ROOT).as_posix(), h[0], h[3])
        for suffix, fp in cli.iter_mirror_files(REPO_ROOT)
        for h in cli.scan_file(suffix, fp) if h[4] == "MISSING"
    ]
    assert missing == [], f"mirror pages embedding a non-existent variant: {missing}"


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items())
             if n.startswith("test_") and callable(f)]
    failed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  PASS  {name}")
        except AssertionError as e:
            print(f"  FAIL  {name}: {e}")
            failed += 1
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    raise SystemExit(1 if failed else 0)
