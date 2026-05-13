"""Stage 7 練習 5：Deploy — Path A（FastAPI + Ollama、$0）。

把 agent 包進 FastAPI HTTP endpoint、production-style health check + structured logging。
本地端 `uvicorn starter:app` 就能跑、Docker / k8s / Lambda 都能 lift。

跑法：
    pip install -r requirements.txt
    ollama pull qwen2.5:3b
    ollama serve
    uvicorn starter:app --reload --port 8000
    # 另一個 shell: curl -X POST http://localhost:8000/chat -H 'Content-Type: application/json' -d '{"message": "hi"}'

驗證（不必啟 server）:
    python test.py
"""

from __future__ import annotations

import logging
import os
import sys
import time
import uuid
from typing import Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from fastapi import FastAPI, HTTPException
from openai import APIConnectionError, OpenAI
from pydantic import BaseModel

MODEL = os.environ.get("MODEL", "qwen2.5:3b")
OLLAMA_BASE = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434/v1")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("agent.api")


# === Schemas ===

class ChatRequest(BaseModel):
    message: str
    max_tokens: int = 300


class ChatResponse(BaseModel):
    request_id: str
    answer: str
    latency_ms: float
    model: str


# === Agent ===

def agent_call(message: str, max_tokens: int, llm: Any = None) -> str:
    llm = llm or OpenAI(base_url=OLLAMA_BASE, api_key="ollama")
    resp = llm.chat.completions.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": message}],
    )
    return resp.choices[0].message.content or ""


# === FastAPI app ===

app = FastAPI(title="Agent API", version="0.1.0")


@app.get("/health")
def health():
    """K8s / load balancer 用這個探測。Production 通常多檢查：DB / cache / upstream LLM ping。"""
    return {"status": "ok", "model": MODEL}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    request_id = str(uuid.uuid4())
    t0 = time.perf_counter()
    logger.info(f"[{request_id}] chat request: {req.message[:80]}")
    try:
        answer = agent_call(req.message, req.max_tokens)
    except APIConnectionError as e:
        logger.error(f"[{request_id}] upstream LLM unavailable: {e}")
        raise HTTPException(status_code=503, detail="LLM service unavailable") from e
    except Exception as e:  # noqa: BLE001
        logger.error(f"[{request_id}] unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal error") from e

    latency_ms = (time.perf_counter() - t0) * 1000
    logger.info(f"[{request_id}] chat done in {latency_ms:.0f}ms")
    return ChatResponse(
        request_id=request_id, answer=answer,
        latency_ms=latency_ms, model=MODEL,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
