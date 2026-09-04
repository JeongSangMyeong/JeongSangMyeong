# MCP 서버 · 스킬 추천 정리

이 프로젝트를 위해 **실제로 존재하고 무료인지 직접 확인한** 항목만 정리했습니다.
확인 방법은 npm 레지스트리 / PyPI API 조회와 공식 문서 확인입니다.

## 먼저 알아야 할 것

**MCP 서버는 프로그램을 동작시키는 부품이 아닙니다.** MCP 는 *Claude 가 개발할 때 쓰는 도구*를
늘려 주는 것이고, VoiceScribe 자체는 MCP 없이도 완전히 동작합니다.
그래서 "받아쓰기 프로그램을 만들기 위해 꼭 필요한 MCP" 같은 건 없습니다.
아래는 **개발과 사용을 편하게 해 주는** 것들입니다.

## 설정해 둔 것 (`.mcp.json`)

### 1. `voicescribe` — 직접 만든 서버 ⭐

```json
"voicescribe": {
  "command": "${VOICESCRIBE_PYTHON:-${CLAUDE_PROJECT_DIR}/voicescribe/.venv/bin/python}",
  "args": ["-m", "voicescribe.mcp_server"],
  "env": { "PYTHONPATH": "${CLAUDE_PROJECT_DIR}/voicescribe/src" }
}
```

`${VAR:-기본값}` 문법은 Claude Code 가 공식 지원합니다. 기본값으로 프로젝트 가상환경의
파이썬을 가리키므로 README 대로 설치했다면 추가 설정이 필요 없습니다.

- **비용: 무료.** API 키가 필요 없고 음성이 외부로 나가지 않습니다.
- 왜 직접 만들었나: 검색해 보면 whisper MCP 서버가 여러 개 있지만
  (`jwulff/whisper-mcp`, `SmartLittleApps/local-stt-mcp` 등) 대부분 **애플 실리콘 전용**이거나
  검증되지 않은 개인 프로젝트입니다. 우리 코드를 그대로 노출하는 편이 안전하고 기능도 많습니다.
- 제공 도구: `transcribe_audio`, `list_supported_languages`, `check_setup`
- **윈도우**에서는 가상환경 파이썬 경로가 달라 환경변수를 설정해야 합니다.
  `VOICESCRIBE_PYTHON=C:\프로젝트경로\voicescribe\.venv\Scripts\python.exe`
- 의존성이 없는 파이썬으로 실행되면 서버가 "MCP SDK 가 설치되지 않았습니다" 라는
  안내와 함께 종료됩니다. 그때는 경로를 확인하세요.

### 2. `context7` — 라이브러리 최신 문서

```json
"context7": { "type": "http", "url": "https://mcp.context7.com/mcp" }
```

- **비용: 무료.** API 키 없이 쓸 수 있고, 무료 키를 넣으면 요청 제한만 완화됩니다.
- 왜 유용한가: faster-whisper, FastAPI 같은 라이브러리의 API 는 자주 바뀝니다.
  실제로 이 프로젝트를 만들다가 **MCP SDK 2.x 에서 `FastMCP` 가 `MCPServer` 로 이름이 바뀐 것**을
  발견했습니다. 기억에 의존하면 이런 걸 놓칩니다.

### 3. `playwright` — 브라우저 자동화

```json
"playwright": { "command": "npx", "args": ["-y", "@playwright/mcp@latest"] }
```

- **비용: 무료** (Apache-2.0, Microsoft 제작).
- 왜 유용한가: 웹 UI 를 고친 뒤 Claude 가 직접 브라우저를 열어 눌러 보고 확인할 수 있습니다.
- Node.js 가 필요합니다. 안 쓸 거라면 `.mcp.json` 에서 지워도 됩니다.

## 일부러 넣지 않은 것

솔직하게 말하면 아래는 **넣어도 큰 도움이 안 됩니다.** MCP 서버가 많아질수록 시작이 느려지고
Claude 가 참고할 내용만 늘어납니다.

| 서버 | 왜 뺐나 |
| --- | --- |
| `@modelcontextprotocol/server-filesystem` | Claude Code 에 이미 파일 읽기/쓰기 도구가 있습니다. 중복입니다. |
| `mcp-server-fetch` (uvx) | Claude Code 의 WebFetch/WebSearch 와 중복입니다. |
| `@modelcontextprotocol/server-sequential-thinking` | 확장 사고 기능과 중복입니다. |
| `@modelcontextprotocol/server-memory` | 프로젝트 지식은 `CLAUDE.md` 로 관리하는 편이 낫습니다. |
| `@modelcontextprotocol/server-git` | `Bash(git …)` 로 충분합니다. |
| ElevenLabs MCP 등 음성 API | **유료입니다.** 무료 우선 원칙에 맞지 않습니다. |

필요하면 나중에 추가하면 됩니다. 예를 들어 파일시스템 서버는 이렇게 씁니다.

```bash
claude mcp add --scope project filesystem -- npx -y @modelcontextprotocol/server-filesystem ~/Documents
```

> 참고: 공식 저장소 README 에는 sequential-thinking 패키지 이름이 붙여쓰기로 적혀 있는 경우가
> 있는데, npm 에 실제로 존재하는 이름은 **하이픈이 들어간** `@modelcontextprotocol/server-sequential-thinking` 입니다.

## 설정한 스킬 (`.claude/skills/`)

스킬은 "매번 똑같이 설명해야 하는 절차"를 파일로 저장해 두는 기능입니다. MCP 와 달리
**추가 설치가 전혀 필요 없고, 쓸 때만 읽히므로 비용도 거의 없습니다.**

### `voice-transcribe`

"이 녹음 받아써 줘" 같은 요청이 오면 자동으로 읽힙니다. 담고 있는 내용:

- 실행 전에 `doctor` 로 설치 상태를 먼저 확인할 것
- 모델별 속도/정확도 표 — 큰 모델을 쓰기 전에 사용자에게 소요 시간을 알릴 것
- 파일을 못 찾으면 지어내지 말고 물어볼 것
- 받아쓴 결과를 임의로 고치지 말 것

### `voicescribe-dev`

`voicescribe/**` 파일을 건드릴 때만 읽힙니다(`paths` 설정). 담고 있는 내용:

- 무거운 라이브러리는 함수 안에서 지연 import 할 것
- 테스트는 인터넷·모델 없이 통과해야 할 것
- 새 엔진/포맷 추가 절차
- **이미 겪은 버그 두 가지**: `web/server.py` 의 `from __future__ import annotations` 금지,
  SSE 종료 판정은 보낸 이벤트 기준으로 할 것

## 승인 방법

`.mcp.json` 은 프로젝트 범위라서 처음 한 번 승인이 필요합니다.

```bash
claude          # 실행하면 .mcp.json 승인 여부를 물어봅니다
/mcp            # 연결 상태 확인
```

승인 기록을 초기화하려면 `claude mcp reset-project-choices` 를 씁니다.
