# Python AI Agent

파이썬 초보자를 위한 간단한 AI 에이전트입니다.

[Anthropic의 에이전트 베스트 프랙티스](https://www.anthropic.com/research/building-effective-agents)를 기반으로,
프레임워크 없이 API 직접 호출로 구현했습니다.

## 핵심 구조

```
사용자 입력 → AI 호출 → 도구 필요? → Yes → 도구 실행 → 결과 전달 → 다시 판단
                                    → No  → 최종 답변 반환
```

## 프로젝트 구조

```
python-ai-agent/
├── ai_agent/
│   ├── __init__.py         # 패키지 초기화
│   ├── __main__.py         # python -m ai_agent 진입점 (CLI / serve 분기)
│   ├── main.py             # CLI 대화 인터페이스 (REPL)
│   ├── agent.py            # 에이전트 루프 (핵심 로직)
│   ├── tools.py            # 도구 정의 + 실행
│   ├── config.py           # 설정 관리 (환경변수)
│   └── api.py              # REST API (FastAPI)
├── tests/
│   ├── test_tools.py       # 도구 단위 테스트
│   └── test_api.py         # API 엔드포인트 테스트
├── pyproject.toml          # 프로젝트 설정 (의존성, 빌드, 도구)
├── .env.example            # 환경변수 템플릿
├── .gitignore
├── LICENSE
└── README.md
```

## 설치 & 실행

```bash
# 1. 클론
git clone https://github.com/YOUR_USERNAME/python-ai-agent.git
cd python-ai-agent

# 2. 가상환경
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# 3. 설치 (editable 모드 - 코드 수정이 바로 반영됨)
pip install -e ".[dev]"

# 4. API 키 설정
cp .env.example .env
# .env 파일을 열어서 ANTHROPIC_API_KEY 입력

# 5. 실행
ai-agent                       # CLI 대화 모드
python -m ai_agent serve       # REST API 서버 (port 8000)
```

## REST API 사용법

서버 시작 후 다른 터미널에서:

```bash
# 헬스체크
curl http://localhost:8000/health

# 질문하기
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"message": "2+3은 뭐야?"}'

# 응답 예시
# {"answer": "2 + 3은 5입니다."}
```

Spring 등 외부 서비스에서 HTTP로 호출할 수 있습니다.

## 테스트

```bash
pytest
```

---

## 동작 방식 상세 설명

### 1. 에이전트 루프 (`agent.py`)

이 프로젝트의 핵심입니다. "에이전트"란 AI가 스스로 판단해서 도구를 골라 쓰고,
그 결과를 보고 다시 판단하는 루프를 말합니다.

```
agent.run("지금 몇 시야?") 호출

┌─ 루프 시작 ──────────────────────────────────────────┐
│                                                       │
│  1) Claude API 호출                                    │
│     - messages: [{"role":"user", "content":"지금 몇 시야?"}]
│     - tools: [calculator, get_current_time, memo]      │
│                                                       │
│  2) Claude 응답 확인                                    │
│     └─ stop_reason == "tool_use"?                      │
│        ├─ Yes → 도구 실행 → 결과를 messages에 추가 → 1)로 │
│        └─ No  → 최종 텍스트 답변 추출 → return           │
│                                                       │
└───────────────────────────────────────────────────────┘
```

**핵심 포인트:**
- Claude가 도구를 쓸지 말지 **스스로 결정**합니다. 우리 코드에는 "이럴 때 이 도구를 써라"라는 if문이 없습니다.
- `tools` 파라미터로 "이런 도구들이 있어요"라고 설명서만 넘기면, Claude가 사용자 질문을 보고 적절한 도구를 골라서 호출을 요청합니다.
- 우리 코드는 요청받은 도구를 **실행만** 해주고, 결과를 다시 Claude에게 넘기는 역할입니다.

### 2. 도구 시스템 (`tools.py`)

도구는 두 부분으로 나뉩니다:

```python
# (1) 설명서 — Claude에게 "이런 도구가 있어요" 알려주는 JSON
TOOLS = [
    {
        "name": "calculator",
        "description": "수학 계산을 합니다...",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "계산할 수학 식"}
            },
            "required": ["expression"]
        }
    },
    ...
]

# (2) 실행 함수 — Claude가 "calculator 써줘"라고 하면 실제로 실행
def run_tool(tool_name, tool_input):
    if tool_name == "calculator":
        result = eval(expression, ...)  # 계산 실행
        return f"계산 결과: {result}"
```

Claude API 응답에 `stop_reason: "tool_use"`가 오면, 응답 안에 어떤 도구를
어떤 입력으로 호출해달라는 정보가 들어있습니다:

```json
{
  "type": "tool_use",
  "name": "calculator",
  "input": {"expression": "2 + 3"}
}
```

우리 코드(`agent.py`)가 이걸 받아서 `run_tool("calculator", {"expression": "2 + 3"})`을 실행하고,
결과 `"계산 결과: 5"`를 다시 Claude에게 전달합니다.

### 3. REST API 레이어 (`api.py`)

에이전트를 HTTP로 감싸는 얇은 레이어입니다.

```
Spring API (또는 curl, 브라우저, 다른 서비스)
    │
    │  POST /api/ask
    │  Body: {"message": "2+3은?"}
    ▼
FastAPI (api.py)
    │
    │  request.message를 꺼내서
    │  agent.run("2+3은?") 호출
    │
    ▼
에이전트 루프 (agent.py)
    │  Claude API 호출 → 도구 실행 → 최종 답변
    │
    ▼
FastAPI가 응답 반환
    {"answer": "2 + 3은 5입니다."}
```

**구성 요소:**

| 요소 | 역할 |
|------|------|
| `FastAPI()` | 웹 프레임워크. Spring의 `@RestController` 같은 것 |
| `@app.post("/api/ask")` | 엔드포인트 등록. Spring의 `@PostMapping` |
| `AskRequest` / `AskResponse` | Pydantic 모델. Spring의 DTO와 같은 역할. 요청/응답 JSON 구조 정의 + 자동 검증 |
| `CORSMiddleware` | 다른 도메인에서 호출 가능하게. Spring의 `@CrossOrigin` |
| `uvicorn` | ASGI 서버. Spring Boot에 내장된 Tomcat 같은 역할 |

### 4. 진입점 분기 (`__main__.py`)

```python
# python -m ai_agent        → CLI 대화 모드
# python -m ai_agent serve  → REST API 서버
```

`sys.argv`를 확인해서 `serve` 인자가 있으면 API 서버를,
없으면 기존 CLI REPL을 실행합니다.

### 5. 설정 관리 (`config.py`)

환경변수를 한 곳에서 관리합니다. `.env` 파일이나 `export`로 설정하면 됩니다.

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `ANTHROPIC_API_KEY` | (없음) | Claude API 키 (필수) |
| `MODEL` | `claude-sonnet-4-5-20250514` | 사용할 모델 |
| `MAX_ITERATIONS` | `10` | 에이전트 루프 최대 반복 |
| `HOST` | `0.0.0.0` | API 서버 바인드 주소 |
| `PORT` | `8000` | API 서버 포트 |

---

## 도구 추가하는 법

`ai_agent/tools.py` 에서 2가지만 하면 됩니다:

```python
# 1. TOOLS 리스트에 설명서 추가
TOOLS = [
    ...,
    {
        "name": "my_new_tool",
        "description": "이 도구가 뭘 하는지 설명",
        "input_schema": { ... }
    }
]

# 2. run_tool() 함수에 elif 추가
def run_tool(tool_name, tool_input):
    ...
    elif tool_name == "my_new_tool":
        return "실행 결과"
```

`agent.py`는 수정할 필요 없습니다!

## 참고 자료

- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Anthropic API Docs](https://docs.anthropic.com)
- [Tool Use 가이드](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [FastAPI 공식 문서](https://fastapi.tiangolo.com)

## 라이선스

MIT
