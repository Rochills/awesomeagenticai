"""Stage 3 練習 6 自我驗證 — Path B（Anthropic starter_*_anthropic.py）。

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

import starter_bad_anthropic as bad
import starter_good_anthropic as good


def block_text(text: str):
    return SimpleNamespace(type="text", text=text)


def block_tool_use(tool_id: str, name: str, inp: dict):
    return SimpleNamespace(type="tool_use", id=tool_id, name=name, input=inp)


def make_resp(stop_reason: str, *blocks):
    return SimpleNamespace(stop_reason=stop_reason, content=list(blocks))


def test_bad_schema_can_select_wrong_tool():
    client = MagicMock()
    client.messages.create.return_value = make_resp(
        "tool_use",
        block_text("The schemas are vague, so I will process the text."),
        block_tool_use("t1", "process_data", {"data": "32 Celsius to Fahrenheit"}),
    )
    result = bad.select_and_run("Convert 32 Celsius to Fahrenheit.", client=client)
    assert result["tool"] == "process_data"
    assert "processed generic data" in result["observation"]


def test_good_schema_selects_temperature_tool():
    client = MagicMock()
    client.messages.create.return_value = make_resp(
        "tool_use",
        block_text("This is clearly a temperature conversion."),
        block_tool_use("t1", "convert_temperature", {"value": 32, "unit": "celsius"}),
    )
    result = good.select_and_run("Convert 32 Celsius to Fahrenheit.", client=client)
    assert result["tool"] == "convert_temperature"
    assert result["observation"] == {"value": 89.6, "unit": "fahrenheit"}


def test_good_schema_has_required_fields_and_enum():
    bad_temp = next(tool for tool in bad.TOOLS_SPEC if tool["name"] == "convert_temperature")
    good_temp = next(tool for tool in good.TOOLS_SPEC if tool["name"] == "convert_temperature")
    assert "required" not in bad_temp["input_schema"]
    assert good_temp["input_schema"]["required"] == ["value", "unit"]
    assert good_temp["input_schema"]["properties"]["unit"]["enum"] == ["celsius", "fahrenheit"]


if __name__ == "__main__":
    test_bad_schema_can_select_wrong_tool()
    test_good_schema_selects_temperature_tool()
    test_good_schema_has_required_fields_and_enum()
    print("all pass")
