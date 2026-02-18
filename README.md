# 🤖 Python AI Agent

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
├── ai_agent/               # 소스코드 패키지
│   ├── __init__.py          #   패키지 초기화
│   ├── __main__.py          #   python -m ai_agent 지원
│   ├── main.py              #   진입점 (대화 인터페이스)
│   ├── agent.py             #   에이전트 루프 (핵심 로직)
│   ├── tools.py             #   도구 정의 + 실행 함수
│   └── config.py            #   설정 관리
├── tests/
│   └── test_tools.py        # 도구 테스트
├── pyproject.toml           # 프로젝트 설정 (의존성, 빌드, 도구)
├── .env.example             # 환경변수 템플릿
├── .gitignore
├── LICENSE
└── README.md
```

## 설치 & 실행

```bash
# 1. 클론
git clone https://github.com/YOUR_USERNAME/python-ai-agent.git
cd python-ai-agent

# 2. 가상환경 (추천)
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# 3. 설치 (editable 모드 - 코드 수정이 바로 반영됨)
pip install -e ".[dev]"

# 4. API 키 설정
cp .env.example .env
# .env 파일을 열어서 API 키 입력

# 5. 실행!
ai-agent
# 또는
python -m ai_agent
```

## 테스트

```bash
pytest
```

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

## 라이선스

MIT
