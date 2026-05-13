"""練習 6 自我驗證 — Path A（Ollama starter_bad.py + starter_good.py）。

跑法：
    python test.py

驗證內容：
    - bad schema 在 mock 下可能挑錯 tool（process_data）
    - good schema 穩定挑到 convert_temperature
    - good schema 有 required + enum、bad schema 沒有

Anthropic 版本 test 見 test_anthropic.py。
"""

from __future__ import annotations

import json
import sys
from types import SimpleNamespace
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import starter_bad as bad
import starter_good as good


def make_tool_call(call_id: str, name: str, args: dict):
    return SimpleNamespace(
        id=call_id,
        type="function",
        function=SimpleNamespace(name=name, arguments=json.dumps(args)),
    )


def make_resp(content: str, tool_calls=None, finish_reason: str = "tool_calls"):
    msg = SimpleNamespace(content=content, tool_calls=tool_calls)
    return SimpleNamespace(choices=[SimpleNamespace(finish_reason=finish_reason, message=msg)])


def test_bad_schema_can_select_wrong_tool():
    """模糊 schema 下、LLM 把溫度轉換誤丟給 process_data。"""
    client = MagicMock()
    client.chat.completions.create.return_value = make_resp(
        "The schemas are vague, so I will process the text.",
        [make_tool_call("t1", "process_data", {"data": "32 Celsius to Fahrenheit"})],
    )
    result = bad.select_and_run("Convert 32 Celsius to Fahrenheit.", client=client)
    assert result["tool"] == "process_data"
    assert "processed generic data" in result["observation"]
    print("✅ test_bad_schema_can_select_wrong_tool")


def test_good_schema_selects_temperature_tool():
    client = MagicMock()
    client.chat.completions.create.return_value = make_resp(
        "This is clearly a temperature conversion.",
        [make_tool_call("t1", "convert_temperature", {"value": 32, "unit": "celsius"})],
    )
    result = good.select_and_run("Convert 32 Celsius to Fahrenheit.", client=client)
    assert result["tool"] == "convert_temperature"
    assert result["observation"] == {"value": 89.6, "unit": "fahrenheit"}
    print("✅ test_good_schema_selects_temperature_tool")


def test_good_schema_has_required_fields_and_enum():
    """直接檢查 schema 結構：good 有 required + enum、bad 沒有。"""
    bad_temp = next(t for t in bad.TOOLS_SPEC if t["function"]["name"] == "convert_temperature")
    good_temp = next(t for t in good.TOOLS_SPEC if t["function"]["name"] == "convert_temperature")
    assert "required" not in bad_temp["function"]["parameters"]
    assert good_temp["function"]["parameters"]["required"] == ["value", "unit"]
    assert good_temp["function"]["parameters"]["properties"]["unit"]["enum"] == ["celsius", "fahrenheit"]
    print("✅ test_good_schema_has_required_fields_and_enum")


if __name__ == "__main__":
    test_bad_schema_can_select_wrong_tool()
    test_good_schema_selects_temperature_tool()
    test_good_schema_has_required_fields_and_enum()
    print("\n🎉 全部通過 — Ollama path bad / good schema 對照邏輯正確")
