"""Stage 6 練習 4 自我驗證 — 用 mock LLM 跑完整 RAG pipeline。
"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter import KB_DOC, build_kb, chunk_doc, generate, rag, retrieve


def make_mock_llm(answer: str = "Mock answer."):
    llm = MagicMock()
    msg = SimpleNamespace(content=answer)
    choice = SimpleNamespace(message=msg)
    llm.chat.completions.create.return_value = SimpleNamespace(choices=[choice])
    return llm


def test_chunk_doc_produces_sections():
    chunks = chunk_doc(KB_DOC)
    # Sample has 4 ## sections + 1 # title → expect 5
    assert len(chunks) == 5, f"預期 5 個 chunk、得到 {len(chunks)}"
    print("✅ test_chunk_doc_produces_sections")


def test_retrieve_finds_relevant_section():
    collection = build_kb(KB_DOC)
    contexts = retrieve(collection, "vacation days", top_k=1)
    assert "15 days" in contexts[0], f"預期含 '15 days'、得到 {contexts[0]}"
    print("✅ test_retrieve_finds_relevant_section")


def test_generate_uses_context():
    llm = make_mock_llm("You get 15 days of vacation per year.")
    contexts = ["Full-time employees get 15 days of paid vacation."]
    answer = generate("How many vacation days?", contexts, llm=llm)
    # 確認 prompt 帶上了 context（mock 看 create() 收到的 messages）
    call_args = llm.chat.completions.create.call_args
    prompt = call_args.kwargs["messages"][0]["content"]
    assert "15 days" in prompt, "預期 prompt 含 context"
    assert "How many vacation days?" in prompt
    assert "15 days" in answer
    print("✅ test_generate_uses_context")


def test_rag_full_pipeline_with_mock_llm():
    llm = make_mock_llm("Python 3.11+.")
    result = rag("What Python version?", llm=llm)
    assert result["query"] == "What Python version?"
    assert len(result["contexts"]) > 0
    assert "Python 3.11" in result["answer"]
    print("✅ test_rag_full_pipeline_with_mock_llm")


def test_rag_top_k_retrieval():
    """確認 retrieve 真的拿了 top_k 個 chunk。"""
    llm = make_mock_llm("Answer.")
    result = rag("vacation", llm=llm, top_k=3)
    assert len(result["contexts"]) == 3
    print("✅ test_rag_top_k_retrieval")


if __name__ == "__main__":
    test_chunk_doc_produces_sections()
    test_retrieve_finds_relevant_section()
    test_generate_uses_context()
    test_rag_full_pipeline_with_mock_llm()
    test_rag_top_k_retrieval()
    print("\n🎉 全部通過 — RAG pipeline 完整邏輯正確")
