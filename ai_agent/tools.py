"""
🔧 도구(Tools) 모음
====================
AI가 사용할 수 있는 도구들을 정의하는 파일입니다.

도구는 2가지로 구성됩니다:
  1. TOOLS    : AI에게 보여주는 "설명서" (이런 도구가 있어요)
  2. run_tool : 도구를 실제로 실행하는 함수

새 도구를 추가하려면:
  1. TOOLS 리스트에 설명서 추가
  2. run_tool() 함수에 elif 추가
  3. 끝!
"""

import json
import math
import datetime


# ──────────────────────────────────────
# 📋 도구 설명서 (AI가 읽는 메뉴판)
# ──────────────────────────────────────

TOOLS = [
    # 🧮 계산기
    {
        "name": "calculator",
        "description": (
            "수학 계산을 합니다. "
            "사칙연산, 거듭제곱, 제곱근 등을 지원합니다. "
            "예: '2 + 3', '100 / 7', 'math.sqrt(144)', '2 ** 10'"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "계산할 수학 식. 예: '2 + 3 * 4'",
                }
            },
            "required": ["expression"],
        },
    },
    # 🕐 현재 시간
    {
        "name": "get_current_time",
        "description": "현재 날짜와 시간, 요일을 알려줍니다.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    # 📝 메모장
    {
        "name": "memo",
        "description": (
            "메모를 저장하거나 읽습니다. "
            "action이 'save'면 메모를 저장하고, 'read'면 저장된 메모를 읽습니다."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "'save' 또는 'read'",
                },
                "text": {
                    "type": "string",
                    "description": "저장할 메모 내용 (action이 'save'일 때만 필요)",
                },
            },
            "required": ["action"],
        },
    },
]


# ──────────────────────────────────────
# 💾 메모 저장소 (프로그램이 켜져 있는 동안만 유지)
# ──────────────────────────────────────
_memo_storage: list[str] = []


# ──────────────────────────────────────
# ⚙️ 도구 실행 함수
# ──────────────────────────────────────

def run_tool(tool_name: str, tool_input: dict) -> str:
    """
    AI가 요청한 도구를 실행하고 결과를 문자열로 돌려줍니다.

    Args:
        tool_name:  실행할 도구 이름 (예: "calculator")
        tool_input: 도구에 전달할 입력값 (예: {"expression": "2+3"})

    Returns:
        실행 결과 문자열
    """

    # 🧮 계산기
    if tool_name == "calculator":
        try:
            expression = tool_input["expression"]
            allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
            result = eval(expression, {"__builtins__": {}}, allowed)
            return f"계산 결과: {result}"
        except Exception as e:
            return f"계산 오류: {e}"

    # 🕐 현재 시간
    elif tool_name == "get_current_time":
        now = datetime.datetime.now()
        weekdays = ["월", "화", "수", "목", "금", "토", "일"]
        return (
            f"{now.strftime('%Y년 %m월 %d일')} "
            f"{weekdays[now.weekday()]}요일 "
            f"{now.strftime('%H시 %M분 %S초')}"
        )

    # 📝 메모장
    elif tool_name == "memo":
        action = tool_input.get("action", "read")

        if action == "save":
            text = tool_input.get("text", "")
            _memo_storage.append(text)
            return f"메모 저장 완료! (총 {len(_memo_storage)}개)"

        elif action == "read":
            if not _memo_storage:
                return "저장된 메모가 없습니다."
            lines = [f"  {i + 1}. {m}" for i, m in enumerate(_memo_storage)]
            return "저장된 메모:\n" + "\n".join(lines)

        else:
            return f"알 수 없는 action: {action} ('save' 또는 'read'를 사용하세요)"

    # ❓ 모르는 도구
    else:
        return f"알 수 없는 도구: {tool_name}"
