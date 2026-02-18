"""
🔄 에이전트 (Agent)
====================
AI 에이전트의 핵심 로직입니다.

에이전트 루프:
  AI 호출 → 도구 필요? → 실행 → 결과 전달 → 다시 AI 호출 → ... → 최종 답변
"""

import json
import anthropic

from ai_agent import config
from ai_agent.tools import TOOLS, run_tool


def run(user_message: str, verbose: bool = True) -> str:
    """
    에이전트 메인 루프.

    사용자 메시지를 받아서 AI가 도구를 활용해 답변을 만듭니다.

    Args:
        user_message: 사용자가 입력한 텍스트
        verbose: True면 도구 호출 과정을 출력 (디버깅에 유용)

    Returns:
        AI의 최종 답변 텍스트
    """

    # API 클라이언트 생성
    client = anthropic.Anthropic(api_key=config.API_KEY)

    # 대화 내역
    messages = [{"role": "user", "content": user_message}]

    # ── 에이전트 루프 ──
    for turn in range(config.MAX_ITERATIONS):

        if verbose:
            print(f"\n--- 🔄 AI 호출 #{turn + 1} ---")

        # Claude API 호출
        response = client.messages.create(
            model=config.MODEL,
            max_tokens=1024,
            system=config.SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        # ── 최종 답변 → 루프 종료 ──
        if response.stop_reason == "end_turn":
            for block in response.content:
                if hasattr(block, "text"):
                    if verbose:
                        print("--- ✅ 최종 답변 완성 ---")
                    return block.text
            return "(답변 없음)"

        # ── 도구 사용 요청 → 실행 후 계속 ──
        if response.stop_reason == "tool_use":

            # AI 응답을 대화 내역에 추가
            messages.append({"role": "assistant", "content": response.content})

            # 요청된 도구 실행
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    if verbose:
                        print(
                            f"    🔧 도구: {block.name}"
                            f"({json.dumps(block.input, ensure_ascii=False)})"
                        )

                    result = run_tool(block.name, block.input)

                    if verbose:
                        print(f"    📋 결과: {result}")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })

            # 도구 결과를 대화 내역에 추가
            messages.append({"role": "user", "content": tool_results})

            # → 루프 처음으로 돌아가서 AI 다시 호출

    return "⚠️ 최대 반복 횟수를 초과했습니다."
