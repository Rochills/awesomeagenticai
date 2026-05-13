"""Stage 7 練習 5：Deploy — Path B（FastAPI + Anthropic）。

跟 starter.py 同 HTTP API、agent_call 改成 anthropic SDK。

跑法：
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    uvicorn starter_anthropic:app --reload --port 8000
    curl -X POST http://localhost:8000/chat -H 'Content-Type: application/json' -d '{"message": "hi"}'

Production cost：1 chat ≈ $0.001（haiku、短 prompt）。
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

import anthropic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

MODEL = os.environ.get("MODEL", "claude-haiku-4-5")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("agent.api")


class ChatRequest(BaseModel):
    message: str
    max_tokens: int = 300


class ChatResponse(BaseModel):
    request_id: str
    answer: str
    latency_ms: float
    model: str
    input_tokens: int
    output_tokens: int


def agent_call_anthropic(message: str, max_tokens: int, client: Any = None) -> dict:
    client = client or anthropic.Anthropic()
    resp = client.messages.create(
        model=MODEL, max_tokens=max_tokens,
        messages=[{"role": "user", "content": message}],
    )
    return {
        "answer": " ".join(b.text for b in resp.content if b.type == "text"),
        "input_tokens": resp.usage.input_tokens,
        "output_tokens": resp.usage.output_tokens,
    }


app = FastAPI(title="Agent API (Anthropic)", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    request_id = str(uuid.uuid4())
    t0 = time.perf_counter()
    logger.info(f"[{request_id}] chat request")
    try:
        result = agent_call_anthropic(req.message, req.max_tokens)
    except anthropic.APIConnectionError as e:
        raise HTTPException(status_code=503, detail="LLM unavailable") from e
    except anthropic.RateLimitError as e:
        raise HTTPException(status_code=429, detail="Rate limited") from e
    except Exception as e:  # noqa: BLE001
        logger.error(f"[{request_id}] error: {e}")
        raise HTTPException(status_code=500, detail="Internal error") from e

    latency_ms = (time.perf_counter() - t0) * 1000
    logger.info(f"[{request_id}] done in {latency_ms:.0f}ms, tokens={result['input_tokens']}+{result['output_tokens']}")
    return ChatResponse(
        request_id=request_id, answer=result["answer"],
        latency_ms=latency_ms, model=MODEL,
        input_tokens=result["input_tokens"], output_tokens=result["output_tokens"],
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
