---
name: voicescribe-dev
description: voicescribe/ 프로젝트의 코드를 고치거나 기능을 추가할 때 따르는 규칙. 새 음성인식 엔진·번역기·출력 포맷 추가, 테스트 실행, 웹 UI 수정 방법을 담고 있다.
paths: ["voicescribe/**"]
allowed-tools: Bash, Read, Edit, Write, Glob, Grep
---

# VoiceScribe 개발 규칙

## 절대 규칙

1. **무거운 라이브러리는 최상위에서 import 하지 않는다.** `faster_whisper`, `torch`,
   `transformers`, `fastapi`, `mcp` 는 반드시 함수 안에서 지연 import 한다.
   설치되지 않은 환경에서도 `import voicescribe` 와 테스트가 성공해야 한다.
2. **테스트는 인터넷과 AI 모델 없이 통과해야 한다.** 새 테스트에서 모델을 내려받지 않는다.
   합성 오디오(`tests/conftest.py` 의 `synth_speech`)와 `demo` 엔진을 쓴다.
3. **사용자에게 보이는 문자열은 한국어로 쓴다.** 에러 메시지에는 해결 방법을 함께 넣는다.
4. **유료 서비스를 기본값으로 두지 않는다.** 무료·로컬이 기본, 유료 API 는 선택 사항이다.

## 테스트

```bash
cd voicescribe && .venv/bin/python -m pytest tests/ -q
cd voicescribe && .venv/bin/python -m ruff check src tests
```

코드를 고쳤으면 **반드시** 위 두 가지를 돌려 통과를 확인한 뒤 보고한다.

## 새 음성인식 엔진 추가

1. `src/voicescribe/engines/<이름>_engine.py` 에 `TranscriptionEngine` 을 구현한다.
   - `is_available()` — 패키지 설치 여부만 확인(모델 다운로드는 확인하지 않는다).
   - `install_hint()` — `pip install` 명령을 포함한 안내.
   - `transcribe(audio, options, progress)` — `TranscriptionResult` 반환.
2. `engines/registry.py` 의 `_ensure_builtins()` 에 등록하고, 필요하면 `DEFAULT_PRIORITY` 를 조정한다.
3. `pyproject.toml` 에 optional-dependencies 항목을 추가한다.
4. `tests/test_engines_and_pipeline.py` 에 레지스트리 테스트를 추가한다.

## 새 출력 포맷 추가

1. `src/voicescribe/output/formatters.py` 에 `to_<포맷>(result, *, ...)` 함수를 만든다.
2. `FORMATTERS` 와 `FORMAT_DESCRIPTIONS` 에 등록한다.
3. 포맷터가 모르는 옵션은 `render()` 가 알아서 걸러 주므로, 필요한 인자만 선언하면 된다.
4. `test_every_format_accepts_shared_options` 가 자동으로 새 포맷을 검사한다.

## 웹 UI 수정

- `src/voicescribe/web/server.py` 에는 **`from __future__ import annotations` 를 넣지 않는다.**
  FastAPI 가 지연 import 한 타입을 해석하지 못해 500 에러가 난다.
- SSE 스트림 종료는 **방금 내보낸 이벤트의 status** 로 판단한다. 살아 있는 `job.status` 로
  판단하면 마지막 완료 이벤트가 유실된다(이미 한 번 발생했던 버그).
- 화면 문구를 바꿨으면 `tests/test_cli_web_mcp.py::TestWebApi` 를 돌려 확인한다.

## MCP 서버 수정

- `src/voicescribe/mcp_server.py` 는 mcp 1.x(`FastMCP`)와 2.x(`MCPServer`)를 모두 지원한다.
  둘 중 하나만 가정하고 고치지 않는다.
- 도구를 추가·삭제했으면 `TestMcpServer::test_server_builds_with_expected_tools` 의
  기대 목록도 함께 고친다.
