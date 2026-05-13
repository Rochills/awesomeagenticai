"""
Stage 1 練習 5 自我驗證 — Path B（Anthropic starter_anthropic.py）。

跑法：
    python test_anthropic.py

驗證內容：
    - with_retry 對 RETRIABLE 錯誤會 retry
    - with_retry 對 non-retriable（譬如 AuthenticationError）直接 raise、不浪費 retry
    - 超過 max_attempts 後 raise 最後一個 exception
    - sleep 確實被叫（透過 mock sleep_fn）

Ollama 版本見 test.py（用 openai SDK 的 exception class）。
"""

from __future__ import annotations

import sys
from unittest.mock import MagicMock

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from anthropic import APIConnectionError, AuthenticationError, RateLimitError

from starter_anthropic import with_retry


def _make_connection_error():
    """anthropic.APIConnectionError 需要 request 參數、用 MagicMock 假裝。"""
    return APIConnectionError(request=MagicMock())


def _make_rate_limit_error():
    """anthropic.RateLimitError 需要 response 參數。"""
    return RateLimitError(message="rate limited", response=MagicMock(status_code=429), body=None)


def _make_auth_error():
    return AuthenticationError(message="bad key", response=MagicMock(status_code=401), body=None)


def test_no_retry_when_success_first_time():
    fn = MagicMock(return_value="ok")
    sleep = MagicMock()
    result = with_retry(fn, sleep_fn=sleep)
    assert result == "ok"
    assert fn.call_count == 1
    assert sleep.call_count == 0
    print("✅ test_no_retry_when_success_first_time")


def test_retry_on_connection_error_then_success():
    err = _make_connection_error()
    fn = MagicMock(side_effect=[err, err, "ok"])
    sleep = MagicMock()
    result = with_retry(fn, max_attempts=4, sleep_fn=sleep)
    assert result == "ok"
    assert fn.call_count == 3
    assert sleep.call_count == 2
    print("✅ test_retry_on_connection_error_then_success")


def test_retry_on_rate_limit():
    err = _make_rate_limit_error()
    fn = MagicMock(side_effect=[err, "ok"])
    sleep = MagicMock()
    result = with_retry(fn, sleep_fn=sleep)
    assert result == "ok"
    assert fn.call_count == 2
    print("✅ test_retry_on_rate_limit")


def test_raise_after_max_attempts():
    err = _make_connection_error()
    fn = MagicMock(side_effect=[err, err, err, err])
    sleep = MagicMock()
    try:
        with_retry(fn, max_attempts=4, sleep_fn=sleep)
    except APIConnectionError:
        assert fn.call_count == 4
        assert sleep.call_count == 3  # 4 次 attempt 之間 sleep 3 次
        print("✅ test_raise_after_max_attempts")
        return
    raise AssertionError("應該 raise APIConnectionError")


def test_no_retry_on_auth_error():
    """AuthenticationError 不是 RETRIABLE、應該第一次就 raise、不 retry。"""
    err = _make_auth_error()
    fn = MagicMock(side_effect=err)
    sleep = MagicMock()
    try:
        with_retry(fn, sleep_fn=sleep)
    except AuthenticationError:
        assert fn.call_count == 1, "AuthenticationError 不該被 retry"
        assert sleep.call_count == 0
        print("✅ test_no_retry_on_auth_error")
        return
    raise AssertionError("應該 raise AuthenticationError")


def test_exponential_backoff_delays():
    """驗 sleep 的延遲時間隨 attempt 指數增長（base * 2^attempt）。"""
    err = _make_connection_error()
    fn = MagicMock(side_effect=[err, err, err, "ok"])
    delays = []
    sleep = MagicMock(side_effect=lambda d: delays.append(d))
    result = with_retry(fn, max_attempts=4, base_delay=1.0, sleep_fn=sleep)
    assert result == "ok"
    # 預期：attempt 0 後 sleep ~1s、attempt 1 後 ~2s、attempt 2 後 ~4s
    assert 1.0 <= delays[0] < 1.5
    assert 2.0 <= delays[1] < 2.5
    assert 4.0 <= delays[2] < 4.5
    print("✅ test_exponential_backoff_delays")


if __name__ == "__main__":
    test_no_retry_when_success_first_time()
    test_retry_on_connection_error_then_success()
    test_retry_on_rate_limit()
    test_raise_after_max_attempts()
    test_no_retry_on_auth_error()
    test_exponential_backoff_delays()
    print("\n🎉 全部通過 — retry wrapper 邏輯正確（RETRIABLE 才 retry、exponential backoff 有效）")
