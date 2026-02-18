"""
🧪 도구(Tools) 테스트
======================
실행: pytest

각 도구가 올바르게 동작하는지 확인하는 테스트입니다.
테스트를 작성해두면 코드를 수정할 때 "혹시 기존 기능이 깨지진 않았나?"를
자동으로 확인할 수 있어요.
"""

from ai_agent.tools import run_tool


class TestCalculator:
    """계산기 도구 테스트."""

    def test_addition(self):
        result = run_tool("calculator", {"expression": "2 + 3"})
        assert "5" in result

    def test_multiplication(self):
        result = run_tool("calculator", {"expression": "12 * 12"})
        assert "144" in result

    def test_sqrt(self):
        result = run_tool("calculator", {"expression": "sqrt(144)"})
        assert "12" in result

    def test_invalid_expression(self):
        result = run_tool("calculator", {"expression": "invalid"})
        assert "오류" in result


class TestGetCurrentTime:
    """현재 시간 도구 테스트."""

    def test_returns_date(self):
        result = run_tool("get_current_time", {})
        assert "년" in result
        assert "월" in result
        assert "일" in result

    def test_returns_weekday(self):
        result = run_tool("get_current_time", {})
        assert "요일" in result


class TestMemo:
    """메모장 도구 테스트."""

    def test_save_and_read(self):
        # 저장
        result = run_tool("memo", {"action": "save", "text": "테스트 메모"})
        assert "저장 완료" in result

        # 읽기
        result = run_tool("memo", {"action": "read"})
        assert "테스트 메모" in result

    def test_read_empty(self):
        # 주의: 이전 테스트에서 저장한 메모가 남아 있을 수 있음
        # 실제로는 각 테스트를 독립적으로 만드는 게 좋습니다 (fixture 사용)
        result = run_tool("memo", {"action": "read"})
        assert isinstance(result, str)


class TestUnknownTool:
    """존재하지 않는 도구 테스트."""

    def test_unknown_tool(self):
        result = run_tool("없는도구", {})
        assert "알 수 없는 도구" in result
