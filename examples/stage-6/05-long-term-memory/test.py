"""Stage 6 練習 5 自我驗證 — MemoryStore + maybe_remember_fact 邏輯。
"""

from __future__ import annotations

import sys
import uuid
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import MemoryStore, chat, maybe_remember_fact


def fresh_memory():
    """每個 test 用獨立 collection 避免 EphemeralClient 跨 test 共享 state。"""
    return MemoryStore(collection_name=f"test_{uuid.uuid4().hex[:8]}")


def make_mock_llm(answer: str = "ok"):
    llm = MagicMock()
    msg = SimpleNamespace(content=answer)
    llm.chat.completions.create.return_value = SimpleNamespace(
        choices=[SimpleNamespace(message=msg)]
    )
    return llm


def test_memory_remember_and_recall():
    mem = fresh_memory()
    mem.remember("User prefers Python over JavaScript.")
    mem.remember("User lives in Taipei.")
    mem.remember("Bananas are yellow.")  # unrelated

    recalled = mem.recall("what programming language does the user like", top_k=2)
    assert any("Python" in m for m in recalled), f"預期 recall Python、得到 {recalled}"
    print("✅ test_memory_remember_and_recall")


def test_memory_empty_recall():
    mem = fresh_memory()
    assert mem.recall("anything") == []
    print("✅ test_memory_empty_recall")


def test_maybe_remember_fact_triggers_on_self_statements():
    mem = fresh_memory()
    fid = maybe_remember_fact("I live in Taipei", mem)
    assert fid is not None
    assert mem.collection.count() == 1
    print("✅ test_maybe_remember_fact_triggers_on_self_statements")


def test_maybe_remember_fact_skips_non_self_statements():
    mem = fresh_memory()
    fid = maybe_remember_fact("What's the weather?", mem)
    assert fid is None
    assert mem.collection.count() == 0
    print("✅ test_maybe_remember_fact_skips_non_self_statements")


def test_chat_uses_memory_in_prompt():
    """chat 應該把 recalled memory 塞進 system prompt。"""
    mem = fresh_memory()
    mem.remember("User prefers Python over JavaScript.")

    llm = make_mock_llm("I recommend Python.")
    result = chat("Recommend a programming language.", mem, llm=llm)

    # mock 看 create() 收到的 messages
    call_args = llm.chat.completions.create.call_args
    system_msg = call_args.kwargs["messages"][0]["content"]
    assert "Python over JavaScript" in system_msg, "system prompt 應含 memory"
    assert "Python" in result["recalled"][0]
    print("✅ test_chat_uses_memory_in_prompt")


if __name__ == "__main__":
    test_memory_remember_and_recall()
    test_memory_empty_recall()
    test_maybe_remember_fact_triggers_on_self_statements()
    test_maybe_remember_fact_skips_non_self_statements()
    test_chat_uses_memory_in_prompt()
    print("\n🎉 全部通過 — long-term memory 邏輯正確")
