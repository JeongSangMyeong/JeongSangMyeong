# 🎙️ VoiceScribe

녹음 파일을 **100개 언어**의 텍스트로 바꾸는 도구입니다. 네이버 클로바노트와 비슷하지만
**전부 무료이고, 내 컴퓨터 안에서만 처리**됩니다. 음성 파일이 인터넷으로 나가지 않습니다.

```
녹음 파일 ─▶ 음성인식 ─▶ 텍스트 / 자막 / 회의록
   mp3        (Whisper)      txt · srt · vtt · md · json · csv
   m4a                       + 화자 구분  + 다른 언어로 번역
   wav
   webm
   mp4
```

## 무엇을 할 수 있나

| 기능 | 설명 |
| --- | --- |
| 받아쓰기 | 100개 언어 자동 감지 및 받아쓰기 |
| 자막 만들기 | SRT · WebVTT (유튜브·편집 프로그램에 바로 사용) |
| 화자 구분 | 누가 언제 말했는지 나눠서 표시 |
| 번역 | 받아쓴 내용을 다른 언어로 (원문·번역 나란히 보기 가능) |
| 회의록 | 마크다운 회의록 자동 생성 |
| 브라우저 UI | 드래그&드롭 업로드, 마이크로 바로 녹음 |
| Claude Code 연동 | 대화 중에 "이 녹음 받아써 줘" 로 사용 |

## 설치

파이썬 3.10 이상이 필요합니다.

```bash
# 1) 프로젝트 폴더로 이동
cd voicescribe

# 2) 가상환경 만들기
python3 -m venv .venv
source .venv/bin/activate        # 윈도우: .venv\Scripts\activate

# 3) 설치 (전체 기능)
pip install -e ".[all]"
```

가볍게 시작하고 싶다면 필요한 것만 고르세요.

```bash
pip install -e ".[stt]"        # 받아쓰기만 (권장 최소 구성)
pip install -e ".[stt,web]"    # 받아쓰기 + 브라우저 UI
pip install -e ".[stt,mcp]"    # 받아쓰기 + Claude Code 연동
```

설치가 잘 됐는지 확인합니다.

```bash
voicescribe doctor
```

> **ffmpeg 를 따로 설치할 필요가 없습니다.** `av` 패키지에 FFmpeg 라이브러리가 들어 있어
> mp3 · m4a · webm · ogg · mp4 를 그대로 읽습니다.

## 사용법

### 브라우저에서 (가장 쉬움)

```bash
voicescribe web
```

http://127.0.0.1:7860 이 열립니다. 파일을 끌어다 놓거나 **마이크로 바로 녹음**할 수 있고,
진행률이 실시간으로 표시되며 결과를 원하는 형식으로 내려받습니다.

### 명령줄에서

```bash
# 가장 기본 — 자동 감지 후 화면에 출력
voicescribe 회의녹음.m4a

# 한국어, 정확한 모델, 텍스트와 자막을 결과 폴더에 저장
voicescribe 회의녹음.m4a -l ko -m large-v3-turbo -f txt srt -o ./결과

# 화자 구분 + 시간 표시
voicescribe 회의녹음.m4a --diarize --timestamps -f md -o ./결과

# 영어로 번역해서 원문과 나란히
voicescribe 강의.mp3 -t en --bilingual -f txt -o ./결과

# 전문용어를 미리 알려 주면 인식률이 오릅니다
voicescribe 회의.wav --prompt "카카오, 리액트, 쿠버네티스, 배포"

# 여러 파일 한 번에
voicescribe 녹음1.m4a 녹음2.m4a 녹음3.m4a -o ./결과
```

주요 옵션:

| 옵션 | 설명 |
| --- | --- |
| `-l, --language` | 음성의 언어 (`ko`, `en`, `한국어` … 기본값 `auto`) |
| `-m, --model` | 모델 크기 (아래 표 참고) |
| `-f, --format` | `txt` `srt` `vtt` `md` `json` `csv` (여러 개 가능) |
| `-o, --output` | 저장 폴더 |
| `-t, --translate-to` | 번역할 언어 |
| `--diarize` | 화자 구분 |
| `--timestamps` | 시간 표시 |
| `--prompt` | 고유명사 힌트 |
| `--no-vad` | 무음 자동 제거 끄기 |

### 파이썬 코드에서

```python
from voicescribe import transcribe_file

result = transcribe_file("회의.m4a", language="ko", model="large-v3-turbo")
print(result.text)

for segment in result.segments:
    print(f"[{segment.start:.1f}초] {segment.text}")
```

## 모델 고르기

GPU 없이 CPU 만으로 돌릴 때의 기준입니다.

| 모델 | 크기 | 속도 | 추천 |
| --- | --- | --- | --- |
| `tiny` | 75MB | 매우 빠름 | 내용만 급히 확인 |
| `base` | 145MB | 빠름 | 기본값 |
| `small` | 480MB | 보통 | 무난한 품질 |
| `large-v3-turbo` | 1.6GB | 느림 | **한국어 회의록 권장** |
| `large-v3` | 3GB | 매우 느림 | 최고 정확도 |

모델은 처음 쓸 때 한 번만 자동으로 내려받아 저장됩니다. 이후에는 인터넷 없이 동작합니다.

> ⏱️ 1시간짜리 녹음을 4코어 CPU + `large-v3-turbo` 로 처리하면 30분 이상 걸릴 수 있습니다.
> 급하면 `small` 로 먼저 확인하세요.

## Claude Code 연동 (MCP)

저장소 루트의 `.mcp.json` 에 이미 설정되어 있습니다. `claude` 를 실행하면 승인 여부를 물어보고,
승인하면 대화 중에 바로 쓸 수 있습니다.

```
나: ~/Downloads/회의.m4a 한국어로 받아써서 회의록 만들어 줘
```

제공하는 도구:

- `transcribe_audio` — 파일을 받아써서 원하는 형식으로 반환·저장
- `list_supported_languages` — 지원 언어 확인
- `check_setup` — 설치 상태 진단

직접 실행할 수도 있습니다.

```bash
voicescribe mcp        # 또는 voicescribe-mcp
```

## 번역

두 가지 방법이 있습니다.

```bash
# 1) Whisper 내장 번역 — 빠르지만 영어로만 번역됩니다
voicescribe 회의.m4a --task translate

# 2) 별도 번역 모델 — 아무 언어로나 번역됩니다
pip install -e ".[translate]"          # 가벼움, 오프라인 (Argos)
voicescribe 회의.m4a -t ja             # 일본어로

pip install -e ".[translate-hf]"       # 정확함, 용량 큼 (M2M100)
voicescribe 회의.m4a -t ja --translator hf
```

기본 번역 모델은 **M2M100(MIT 라이선스)** 으로 상업적 이용에 제약이 없습니다.
NLLB-200 은 더 정확하지만 **비상업(CC-BY-NC)** 라이선스라 기본값에서 제외했습니다.

## 화자 구분

```bash
voicescribe 회의.m4a --diarize
```

추가 설치 없이 동작하는 **간이 방식**이 기본입니다(음색을 비교해 묶습니다).
더 정확하게 하려면 pyannote 를 씁니다.

```bash
pip install -e ".[diarize]"
# https://huggingface.co/pyannote/speaker-diarization-3.1 에서 약관 동의 후
export HF_TOKEN=hf_xxxxx
voicescribe 회의.m4a --diarize
```

## 자주 묻는 것

**Q. 인터넷이 꼭 필요한가요?**
처음 모델을 내려받을 때만 필요합니다. 그 뒤로는 완전히 오프라인으로 동작합니다.

**Q. 녹음 파일이 서버로 전송되나요?**
아니요. 모든 처리가 이 컴퓨터 안에서 이루어집니다. 웹 UI 도 내 컴퓨터에서만 접속됩니다.

**Q. GPU 가 없어도 되나요?**
네. CPU 전용으로 설계되어 있습니다. GPU 가 있으면 `--device cuda` 로 훨씬 빨라집니다.

**Q. 윈도우에서 되나요?**
됩니다. `python -m venv .venv` → `.venv\Scripts\activate` → `pip install -e ".[all]"` 순서로 설치하세요.

**Q. 인식이 자꾸 틀려요.**
① 더 큰 모델(`-m large-v3-turbo`)을 쓰고 ② 언어를 직접 지정하고(`-l ko`)
③ `--prompt` 로 고유명사를 알려 주세요. 이 세 가지로 대부분 좋아집니다.

## 개발

```bash
cd voicescribe
uv venv .venv --python 3.11
uv pip install --python .venv/bin/python -e ".[all,dev]"

.venv/bin/python -m pytest tests/ -q       # 테스트 (모델·인터넷 없이 동작)
.venv/bin/python -m ruff check src tests   # 린트
```

## 라이선스

MIT. 사용하는 모델들의 라이선스는 각각 다음과 같습니다.

| 구성 요소 | 라이선스 | 상업적 이용 |
| --- | --- | --- |
| faster-whisper / Whisper 모델 | MIT | 가능 |
| M2M100 (기본 번역) | MIT | 가능 |
| NLLB-200 (선택) | CC-BY-NC | **불가** |
| pyannote (선택) | MIT (모델은 약관 동의 필요) | 가능 |
