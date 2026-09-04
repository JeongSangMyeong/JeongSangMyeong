# 저장소 안내

이 저장소는 두 가지를 담고 있다.

1. **`README.md`** — GitHub 프로필 페이지. 건드릴 일이 있으면 반드시 먼저 물어본다.
2. **`voicescribe/`** — 녹음 파일을 텍스트로 바꾸는 도구(클로바노트 대안). 실제 개발 대상.

## VoiceScribe 빠른 시작

```bash
cd voicescribe
uv venv .venv --python 3.11
uv pip install --python .venv/bin/python -e ".[all]"

.venv/bin/python -m voicescribe.cli doctor                        # 설치 진단
.venv/bin/python -m voicescribe.cli web                           # 브라우저 UI
.venv/bin/python -m voicescribe.cli 녹음.m4a --engine fast -l ko   # 받아쓰기(한국어 고속)
```

엔진은 두 가지다. **한/일/중/영 녹음이면 `--engine fast`(SenseVoice)가 훨씬 빠르다**
(실측 실시간 대비 x16~19). 그 외 언어나 단어별 타임스탬프가 필요하면 `faster-whisper` 를 쓴다.

## 개발 시 지켜야 할 것

- 코드를 고쳤으면 `cd voicescribe && .venv/bin/python -m pytest tests/ -q` 를 돌려 통과를 확인한다.
- 무거운 라이브러리(`faster_whisper`, `torch`, `fastapi`, `mcp`)는 **함수 안에서 지연 import** 한다.
  설치되지 않은 환경에서도 `import voicescribe` 와 테스트가 성공해야 한다.
- 테스트는 **인터넷·AI 모델 없이** 통과해야 한다. 합성 오디오와 `demo` 엔진을 쓴다.
- 사용자에게 보이는 문자열은 한국어로 쓰고, 에러 메시지에는 해결 방법을 함께 넣는다.

자세한 규칙은 `.claude/skills/voicescribe-dev/SKILL.md` 에 있다.

## 설정된 MCP 서버

`.mcp.json` 에 세 개가 등록되어 있다(모두 무료). 처음 `claude` 를 실행하면 승인 여부를 묻는다.

| 서버 | 하는 일 | 비용 |
| --- | --- | --- |
| `voicescribe` | 대화 중에 바로 녹음 파일을 받아쓴다(로컬 처리) | 무료, 키 불필요 |
| `context7` | 라이브러리 최신 문서를 가져온다 | 무료(키 없이 사용 가능, 키 넣으면 제한 완화) |
| `playwright` | 브라우저를 열어 웹 UI 를 실제로 테스트한다 | 무료 |

`voicescribe` MCP 서버는 기본적으로 `voicescribe/.venv/bin/python` 을 사용한다.
다른 파이썬을 쓰려면 환경변수 `VOICESCRIBE_PYTHON` 에 실행 파일 경로를 넣는다.
윈도우라면 `VOICESCRIBE_PYTHON=<프로젝트경로>\voicescribe\.venv\Scripts\python.exe` 로 설정한다.
