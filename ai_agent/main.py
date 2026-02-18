"""
🚀 메인 진입점
================
프로그램의 시작점입니다.

실행 방법:
  방법 1: python -m ai_agent        (모듈로 실행)
  방법 2: ai-agent                  (pip install 후 명령어로 실행)
"""

from ai_agent import config
from ai_agent.agent import run


def main():
    """프로그램 시작 함수."""

    # API 키 확인
    if not config.API_KEY:
        print("❌ ANTHROPIC_API_KEY가 설정되지 않았습니다!")
        print()
        print("방법 1: .env 파일에 추가")
        print('  ANTHROPIC_API_KEY=sk-ant-...')
        print()
        print("방법 2: 터미널에서 직접 설정")
        print('  export ANTHROPIC_API_KEY="sk-ant-..."')
        return

    print("=" * 45)
    print("🤖 나의 첫 AI 에이전트")
    print("=" * 45)
    print(f"모델: {config.MODEL}")
    print("도구: 계산기 | 현재시간 | 메모장")
    print("종료: quit")
    print()

    while True:
        user_input = input("👤 나: ").strip()

        if not user_input:
            continue
        if user_input in ("quit", "q"):
            print("👋 안녕!")
            break

        try:
            answer = run(user_input)
            print(f"\n🤖 AI: {answer}\n")
        except Exception as e:
            print(f"\n❌ 오류: {e}\n")


# python -m ai_agent 으로 실행할 때 사용
if __name__ == "__main__":
    main()
