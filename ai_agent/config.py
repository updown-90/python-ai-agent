"""
⚙️ 설정(Config) 관리
=====================
환경변수, API 키 등 설정값을 한 곳에서 관리합니다.

왜 따로 파일을 만들까?
  → 설정 로딩 코드가 여기저기 흩어지면 관리가 어려워요.
  → 한 곳에 모아두면 "설정 바꿀 땐 config.py만 보면 돼" 가 됩니다.
"""

import os
from dotenv import load_dotenv


# .env 파일에서 환경변수 로드
load_dotenv()


# ── 설정값들 ──

# Anthropic API 키
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# 사용할 AI 모델
MODEL = os.environ.get("MODEL", "claude-sonnet-4-5-20250514")

# 에이전트 루프 최대 반복 횟수 (가드레일)
MAX_ITERATIONS = int(os.environ.get("MAX_ITERATIONS", "10"))

# REST API 서버 설정
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))

# 시스템 프롬프트 (AI의 성격과 행동 지침)
SYSTEM_PROMPT = (
    "당신은 도움이 되는 한국어 AI 어시스턴트입니다. "
    "질문에 답하기 위해 필요하면 도구를 적극적으로 사용하세요. "
    "도구 결과를 바탕으로 자연스럽게 답변하세요."
)
