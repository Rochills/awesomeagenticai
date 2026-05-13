"""Stage 6 練習 1 — Path B 載入檢查 + OpenAI mock 對照。

跑法：
    python test_anthropic.py
"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np

from starter_anthropic import embed_openai


def test_embed_openai_with_mock():
    """Mock OpenAI client、確認 embed_openai 正確 normalize。"""
    fake_embeddings = [
        SimpleNamespace(embedding=[1.0, 0.0, 0.0]),
        SimpleNamespace(embedding=[0.0, 2.0, 0.0]),
    ]
    client = MagicMock()
    client.embeddings.create.return_value = SimpleNamespace(data=fake_embeddings)

    vecs = embed_openai(["a", "b"], client=client)
    # Both should be unit length after normalize
    assert abs(np.linalg.norm(vecs[0]) - 1.0) < 1e-6
    assert abs(np.linalg.norm(vecs[1]) - 1.0) < 1e-6
    print("✅ test_embed_openai_with_mock")


def test_starter_anthropic_loadable():
    import starter_anthropic
    assert hasattr(starter_anthropic, "MODEL")
    print("✅ test_starter_anthropic_loadable")


if __name__ == "__main__":
    test_embed_openai_with_mock()
    test_starter_anthropic_loadable()
    print("\n🎉 通過 — Path B 可載入 + normalize 正確")
