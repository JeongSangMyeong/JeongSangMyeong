<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/who-dark.svg">
  <img src="assets/who-light.svg" width="760"
       alt="const jsm = { name: '정상명', base: ['Java', 'Spring Boot', 'Oracle'], now: ['Claude Code', 'Next.js', 'Python'], mail: 'ajflsp@naver.com' }">
</picture>

**Java 백엔드 5년차 · AI(Claude Code)로 서비스 개발**

Java·Spring으로 공공·의료·금융 시스템을 만들어 온 백엔드 개발자입니다.<br>
퇴근 후에는 Claude Code로 서비스를 직접 만들어 운영합니다.

</div>
<div align="center">

![Java](https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white)
![Oracle](https://img.shields.io/badge/Oracle-F80000?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude%20Code-D97757?style=flat-square&logo=claude&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3FCF8E?style=flat-square&logo=supabase&logoColor=white)
![Flutter](https://img.shields.io/badge/Flutter-02569B?style=flat-square&logo=flutter&logoColor=white)
![Dart](https://img.shields.io/badge/Dart-0175C2?style=flat-square&logo=dart&logoColor=white)
![MariaDB](https://img.shields.io/badge/MariaDB-003545?style=flat-square&logo=mariadb&logoColor=white)

</div>

---

## AI와 일하는 방식

개인 프로젝트는 AI 코딩 도구인 Claude Code와 함께 만듭니다. 코드는 대부분 AI가 쓰고, 저는 무엇을 만들지 정하고 결과가 맞는지 확인합니다. 확인할 때 지키는 원칙은 세 가지입니다.

- **AI의 판단을 실제 데이터로 다시 확인합니다.** voice-record에서 녹음을 글로 바꾸는 엔진을 고를 때, AI는 짧은 문장 하나로 시험해 보고 새 엔진을 골랐습니다. 실제 회의 녹음으로 다시 해 보니 새 엔진은 단어가 엉뚱하게 붙거나 끊겨 읽기 어려워서 원래 엔진으로 되돌렸습니다.
- **테스트가 정말 버그를 잡는지 확인합니다.** 버그를 고친 뒤 그 버그를 일부러 다시 넣어 보고, 테스트가 실패하는지 봅니다. 화재경보기를 단 뒤 연기를 대 보는 것과 같습니다.
- **개인정보는 AI에게 보내기 전에 가립니다.** 통화 비서는 통화 내용을 AI에게 요약시키기 전에 주민번호와 카드번호부터 가립니다.

---

## 프로젝트

비공개 저장소는 연락 주시면 화면을 띄워 코드와 동작을 보여드립니다.

### 🏷 QR태그 · [qtag.kr](https://qtag.kr) <sub>비공개</sub>

**제품에 붙이는 QR 스티커 서비스입니다.** 소비자가 QR을 찍으면 제품명을 검색하지 않고 판매 페이지로 바로 갑니다.

- 기획부터 개발, 배포, 운영까지 혼자 맡고 있습니다.
- QR에는 자체 단축링크만 인쇄합니다. 스캔하면 서버가 등록·검증한 곳으로만 보내서 가짜 QR을 막습니다.
- 통합 점검에서 찾은 결함 74건을 모두 고쳤고, 같은 결함이 다시 생기면 DB 검사가 잡아냅니다.

`Next.js 15` `TypeScript` `Supabase` `Vercel` `Vitest`

### 📞 통화 비서 <sub>비공개</sub>

**통화 녹음을 받아써서 요약, 할 일, 말하기 코칭으로 정리해 주는 프로그램입니다.** 노트북에 띄워 두면 새 녹음을 알아서 처리하고 아침마다 브리핑을 보냅니다.

> 녹음 → 받아쓰기 → 말한 사람 나누기 → 민감정보 가리기 → 요약·할 일·코칭 → 노션·아침 브리핑

- 할 일과 코칭은 받아쓴 글에 있는 문장을 근거로 받고, 근거가 없으면 버립니다. AI가 통화에 없던 약속을 지어내지 못하게 하려는 장치입니다.
- 목소리로 사람을 구분하는 모델 세 개를 같은 통화로 시험해 보고 골랐습니다. 다른 두 모델은 대화의 92%를 한 사람 말로 몰았습니다.
- GPU가 없는 노트북에서도 긴 회의를 받아쓸 수 있게 모델을 가볍게 돌리고 여러 구간을 한꺼번에 처리합니다.

`Python` `Claude Code` `faster-whisper` `OpenVINO` `SQLite` `Notion` `Slack`

### 🎬 콘텐츠 제작 파이프라인 <sub>비공개</sub>

**쇼츠 영상, 카드뉴스, 블로그 글을 AI 에이전트들이 역할을 나눠 만드는 개인 제작 파이프라인입니다.**

> 주제 조사 → 원문·출처 확보 → 대본 → 검수 → 그림·음성·자막 → 영상 합성·검사 → 예약 게시

- 대본은 원문·출처와 맞춰 보고, 저작권은 판정 도구가 통과시킨 자료만 씁니다.
- 게시 직전에 올릴 계정을 다시 확인하고, 다른 계정이면 멈춥니다.
- 에이전트마다 필요 없는 규칙을 덜어 내서 첫 호출 토큰을 약 6.7만에서 1만으로 85% 줄였습니다.
- 매주 예약 실행으로 한 주 분량을 만들고, 멈추거나 게시에 실패하면 폰으로 알립니다.

`Python` `Claude Code 서브에이전트` `Remotion` `ffmpeg` `YouTube Data API`

### 🍽 QR 테이블오더 <sub>비공개</sub>

**식당 테이블의 QR을 찍으면 메뉴 선택부터 결제까지 끝나는 주문 웹앱입니다.** 손님, 주방, 사장님 화면이 따로 있습니다.

- 결제 금액은 손님 화면에서 받지 않고 서버와 DB에서만 계산합니다.
- 한 테이블에 앉은 여러 사람의 폰이 장바구니 하나를 같이 씁니다.
- 결제는 모의 결제로 처음부터 끝까지 확인했습니다. 실결제는 아직 해 보지 못했습니다.

`Next.js 16` `TypeScript` `Supabase` `PortOne V2` `GitHub Actions`

### 🎙 voice-record

**녹음 파일을 글로 바꿔 주는 무료 도구입니다.** 웹판과 PC판은 녹음이 그 기기 밖으로 나가지 않습니다.

- 휴대폰 브라우저 안에서 변환하는 웹판, 정확도가 가장 좋은 PC 프로그램, 여럿이 쓰는 서버판으로 나눴습니다.
- 실제 목소리 녹음 11개(1~5명)에서 말한 사람 수를 맞힌 녹음을 4개에서 11개로 늘렸습니다.
- '녹음을 기기 밖으로 보내지 않는다'는 원칙을 테스트로 지킵니다.

`Python` `faster-whisper` `transformers.js` `WebGPU · WASM` → **[저장소](https://github.com/JeongSangMyeong/voice-record)**

### 🖐 손 재활기기 게임

**손에 쥐는 재활기기를 기울이거나 눌러서 하는 태블릿 게임 앱입니다.** 벽돌깨기, 비행기 슈팅, 테트리스가 있습니다. 2024년에 개인 외주로 만들었습니다.

▶︎ **[시연 영상](https://youtu.be/1YC9MNHcwRc)**

- 페어링된 재활기기를 찾아 자동으로 연결하고, 실패하면 3초마다 다시 시도합니다.
- 블루투스 시리얼(SPP)로 받은 기울기와 압력 값을 게임 조작으로 바꿉니다.
- 2026년 8월에 Claude Code로 코드를 다시 점검해, 찍히지 않던 로그와 화면을 닫은 뒤에도 돌던 재연결을 고쳤습니다.

`Flutter` `Dart` `블루투스 시리얼(SPP)` `Android` → **[저장소](https://github.com/JeongSangMyeong/hand-rehab-game)**

---

## 공부하며 만든 것

- **[Spring-boot-Photogram](https://github.com/JeongSangMyeong/Spring-boot-Photogram)** · Spring Boot 3로 만든 인스타그램 클론입니다. 강의 코드의 버그를 고치고 기능을 붙인 부분은 [README](https://github.com/JeongSangMyeong/Spring-boot-Photogram#직접-구현한-부분)에 커밋까지 적었습니다.
- **[naver-search](https://github.com/JeongSangMyeong/naver-search)** · 네이버 검색 API 6종(블로그·뉴스·책·카페·지식인·지역)을 한 화면에서 검색합니다. Next.js 14로 만들었습니다.
