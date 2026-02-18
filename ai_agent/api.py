"""
REST API 레이어
================
FastAPI를 사용해 에이전트를 HTTP로 호출할 수 있게 합니다.

엔드포인트:
  POST /api/ask   — 에이전트에게 질문
  GET  /health    — 헬스체크
"""

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai_agent import config
from ai_agent.agent import run

logger = logging.getLogger(__name__)

# ── FastAPI 앱 ──

app = FastAPI(title="AI Agent API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Pydantic 모델 ──

class AskRequest(BaseModel):
    message: str


class AskResponse(BaseModel):
    answer: str


# ── 엔드포인트 ──

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/ask", response_model=AskResponse)
def ask(request: AskRequest):
    if not config.API_KEY:
        return AskResponse(answer="ANTHROPIC_API_KEY가 설정되지 않았습니다.")

    try:
        answer = run(request.message, verbose=False)
    except Exception as e:
        logger.exception("에이전트 실행 중 오류")
        return AskResponse(answer=f"오류가 발생했습니다: {e}")

    return AskResponse(answer=answer)


# ── 서버 시작 함수 ──

def serve():
    """uvicorn으로 API 서버를 시작합니다."""
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host=config.HOST, port=config.PORT)
