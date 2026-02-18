"""
REST API 엔드포인트 테스트
===========================
FastAPI TestClient로 API를 테스트합니다.
실제 LLM 호출은 mock 처리합니다.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from ai_agent.api import app

client = TestClient(app)


class TestHealth:
    """헬스체크 엔드포인트 테스트."""

    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestAsk:
    """POST /api/ask 엔드포인트 테스트."""

    @patch("ai_agent.api.run", return_value="2 + 3은 5입니다.")
    @patch("ai_agent.api.config")
    def test_ask_success(self, mock_config, mock_run):
        mock_config.API_KEY = "test-key"

        response = client.post("/api/ask", json={"message": "2+3은?"})

        assert response.status_code == 200
        assert response.json() == {"answer": "2 + 3은 5입니다."}
        mock_run.assert_called_once_with("2+3은?", verbose=False)

    @patch("ai_agent.api.config")
    def test_ask_no_api_key(self, mock_config):
        mock_config.API_KEY = ""

        response = client.post("/api/ask", json={"message": "hello"})

        assert response.status_code == 200
        assert "API_KEY" in response.json()["answer"]

    @patch("ai_agent.api.run", side_effect=Exception("LLM 호출 실패"))
    @patch("ai_agent.api.config")
    def test_ask_agent_error(self, mock_config, mock_run):
        mock_config.API_KEY = "test-key"

        response = client.post("/api/ask", json={"message": "test"})

        assert response.status_code == 200
        assert "오류" in response.json()["answer"]

    def test_ask_missing_message(self):
        response = client.post("/api/ask", json={})

        assert response.status_code == 422
