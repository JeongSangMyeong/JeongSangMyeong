---
name: voice-transcribe
description: 녹음 파일(mp3, m4a, wav, webm, mp4 등)을 텍스트·자막으로 받아쓰거나 다른 언어로 번역할 때 사용한다. "이 녹음 받아써 줘", "회의록 만들어 줘", "자막(SRT) 만들어 줘", "음성을 텍스트로", "화자 구분해 줘" 같은 요청에 쓴다. 무료·오프라인 VoiceScribe 를 사용하며 음성이 외부로 전송되지 않는다.
argument-hint: [오디오파일] [언어] [형식]
allowed-tools: Bash, Read, Glob
---

# 녹음 파일 받아쓰기

사용자의 음성 파일을 텍스트로 바꾼다. 이 저장소의 `voicescribe/` 도구를 쓴다.

## 1. 먼저 확인할 것

받아쓰기를 실행하기 전에 설치 상태를 확인한다.

```bash
cd voicescribe && .venv/bin/python -m voicescribe.cli doctor
```

`.venv` 가 없으면 먼저 만든다.

```bash
cd voicescribe
uv venv .venv --python 3.11 && uv pip install --python .venv/bin/python -e ".[all]"
```

`[음성인식 엔진]` 항목에서 `faster-whisper` 가 ❌ 라면 실제 받아쓰기가 되지 않는다.
그때는 사용자에게 다음을 안내하고 동의를 받은 뒤 설치한다(모델 다운로드로 수백 MB~3GB 를 쓴다).

```bash
cd voicescribe && uv pip install --python .venv/bin/python "faster-whisper"
```

## 2. 모델 고르기

사용자가 지정하지 않았다면 아래 기준으로 **먼저 제안하고 확인을 받는다**. 큰 모델은 CPU 에서 매우 느리다.

| 모델 | 크기 | CPU 속도(대략) | 추천 상황 |
| --- | --- | --- | --- |
| `tiny` | 75MB | 매우 빠름 | 내용 확인만 급할 때 |
| `base` | 145MB | 빠름 | 기본값, 짧은 메모 |
| `small` | 480MB | 보통 | 무난한 품질 |
| `large-v3-turbo` | 1.6GB | 느림 | **한국어 회의록 권장** |
| `large-v3` | 3GB | 매우 느림 | 최고 정확도가 필요할 때 |

1시간짜리 녹음을 `large-v3-turbo` 로 돌리면 4코어 CPU 기준 30분 이상 걸릴 수 있다. 실행 전에 알려 준다.

## 3. 실행

```bash
cd voicescribe && .venv/bin/python -m voicescribe.cli transcribe "<파일경로>" \
  -l ko -m large-v3-turbo -f txt srt -o "<저장폴더>"
```

자주 쓰는 옵션:

- `-l ko` — 언어 지정. 생략하거나 `auto` 면 자동 감지(짧은 파일은 틀릴 수 있으니 아는 경우 지정한다).
- `-f txt srt md json csv vtt` — 여러 형식을 한 번에 저장.
- `-o 폴더` — 저장 위치. 생략하면 화면에만 출력한다.
- `--diarize` — 화자 구분(누가 말했는지).
- `-t en --bilingual` — 영어로 번역해 원문과 나란히 저장.
- `--prompt "카카오, 리액트, 배포"` — 고유명사를 미리 알려 주면 인식률이 오른다.
- `--timestamps` — txt 에 시간 표시.

## 4. 결과 보고

작업이 끝나면 다음을 사용자에게 알린다.

- 감지된 언어와 전체 길이
- 저장된 파일 경로
- 본문 앞부분 미리보기(3~5줄)

## 주의사항

- **파일이 없으면 만들어 내지 말 것.** 경로를 못 찾으면 `Glob` 으로 찾아보고, 그래도 없으면 사용자에게 정확한 경로를 묻는다.
- **받아쓰기 결과를 임의로 고치지 말 것.** 오탈자가 보여도 원문을 유지하고, 수정이 필요하면 사용자에게 확인받는다.
- 첫 실행은 모델 다운로드 때문에 오래 걸린다. 진행이 멈춘 것처럼 보여도 기다린다.
- 30분이 넘는 파일은 백그라운드로 실행하고(`run_in_background`), 중간에 진행 상황을 확인한다.
