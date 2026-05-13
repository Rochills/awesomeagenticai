"""Stage 3 練習 4 自我驗證 — Path B（Anthropic starter_anthropic.py）。

跑法：
    python test_anthropic.py

用 mock 取代 Anthropic client、不打真 API、$0/run。
Ollama 版本見 test.py（OpenAI-compat shape）。
"""

from __future__ import annotations

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from starter_anthropic import divide, react_loop, to_percentage


def block_text(text: str):
    return SimpleNamespace(type="text", text=text)


def block_tool_use(tool_id: str, name: str, inp: dict):
    return SimpleNamespace(type="tool_use", id=tool_id, name=name, input=inp)


def make_resp(stop_reason: str, *blocks):
    return SimpleNamespace(stop_reason=stop_reason, content=list(blocks))


def test_tools_handle_math_edges():
    assert divide(10, 2) == "5.0"
    assert divide(10, 0) == "0"
    assert to_percentage(0.3122) == "31.22"


def test_population_ratio_uses_four_tool_steps():
    client = MagicMock()
    client.messages.create.side_effect = [
        make_resp("tool_use", block_text("Need Taipei population."), block_tool_use("t1", "lookup_population", {"city": "Taipei"})),
        make_resp("tool_use", block_text("Need New York population."), block_tool_use("t2", "lookup_population", {"city": "New York"})),
        make_resp("tool_use", block_text("Divide the two populations."), block_tool_use("t3", "divide", {"a": 2602000, "b": 8336000})),
        make_resp("tool_use", block_text("Convert ratio to percent."), block_tool_use("t4", "to_percentage", {"ratio": 0.3122})),
        make_resp("end_turn", block_text("Taipei is about 31% of New York by population.")),
    ]
    result = react_loop("Compare Taipei and New York population.", client=client)
    tools = [entry["tool"] for entry in result["trace"] if entry["tool"]]
    assert tools == ["lookup_population", "lookup_population", "divide", "to_percentage"]
    assert "31%" in result["final"]
    assert result["steps"] == 5


def test_zero_population_path_still_finishes():
    client = MagicMock()
    client.messages.create.side_effect = [
        make_resp("tool_use", block_text("Need numerator."), block_tool_use("t1", "lookup_population", {"city": "Taipei"})),
        make_resp("tool_use", block_text("Need denominator."), block_tool_use("t2", "lookup_population", {"city": "Empty City"})),
        make_resp("tool_use", block_text("Divide safely."), block_tool_use("t3", "divide", {"a": 2602000, "b": 0})),
        make_resp("tool_use", block_text("Convert zero ratio."), block_tool_use("t4", "to_percentage", {"ratio": 0})),
        make_resp("end_turn", block_text("The denominator is zero, so the safe displayed percentage is 0%.")),
    ]
    result = react_loop("Compare Taipei with an empty city.", client=client)
    assert result["trace"][2]["obs"] == "0"
    assert result["trace"][3]["obs"] == "0.00"
    assert result["final"].endswith("0%.")


if __name__ == "__main__":
    test_tools_handle_math_edges()
    test_population_ratio_uses_four_tool_steps()
    test_zero_population_path_still_finishes()
    print("all pass")
