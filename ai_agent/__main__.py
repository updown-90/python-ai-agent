"""
python -m ai_agent 으로 실행할 때 이 파일이 호출됩니다.

사용법:
  python -m ai_agent          → CLI REPL (대화형)
  python -m ai_agent serve    → REST API 서버 시작
"""

import sys

if len(sys.argv) > 1 and sys.argv[1] == "serve":
    from ai_agent.api import serve

    serve()
else:
    from ai_agent.main import main

    main()
