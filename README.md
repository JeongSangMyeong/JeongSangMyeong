<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/who-dark.svg">
  <img src="assets/who-light.svg" width="760"
       alt="const jsm = { name: '정상명', base: ['Java', 'Spring Boot', 'Oracle'], now: ['Claude Code', 'Next.js', 'Python'], mail: 'ajflsp@naver.com' }">
</picture>

회사에서는 Java·Spring으로 공공·의료·금융 시스템을 만들어 왔다.<br>
퇴근하고는 Claude Code로 서비스를 만든다. 코드는 대부분 AI가 쓰고, 무엇을 만들지 정하고 결과를 확인하는 건 내 몫이다.

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

## 만든 것

### 🏷 QR태그 · [qtag.kr](https://qtag.kr) <sub>비공개</sub>

제품에 붙이는 QR 스티커 서비스. 소비자가 찍으면 제품명을 검색할 필요 없이 판매 페이지로 바로 간다. QR에는 자체 단축 주소만 찍고, 등록되지 않았거나 막힌 코드는 경고 페이지로 보낸다. 기획부터 운영까지 혼자 맡고 있다.

`Next.js` `TypeScript` `Supabase` `Vercel`

### 📞 통화 비서 <sub>비공개</sub>

통화 녹음을 받아써서 요약, 할 일, 말하기 코칭으로 정리해 준다. 노트북에 켜 두면 새 녹음을 알아서 처리하고 아침마다 브리핑을 보낸다. 주민번호와 카드번호는 AI에 보내기 전에 가린다. AI가 통화에 없던 약속을 지어내지 못하게, 할 일마다 근거 문장도 같이 받는다.

`Python` `Claude Code` `faster-whisper` `SQLite` `Notion` `Slack`

### 🎬 콘텐츠 제작 파이프라인 <sub>비공개</sub>

쇼츠 영상, 카드뉴스, 블로그 글을 역할을 나눈 AI 에이전트들이 만든다. 주제 조사부터 대본, 검수, 그림과 음성, 편집, 예약 게시까지 한 흐름으로 돈다. 매주 정해진 시간에 알아서 돌고, 멈추면 폰으로 알림이 온다.

`Python` `Claude Code` `Remotion` `ffmpeg` `YouTube Data API`

### 🍽 QR 테이블오더 <sub>비공개</sub>

테이블 QR을 찍으면 메뉴 고르기부터 결제까지 끝나는 주문 웹앱. 손님, 주방, 사장님 화면이 따로 있다. 같은 테이블에 앉은 사람들은 각자 폰으로 장바구니 하나를 함께 채운다. 결제 금액은 서버에서만 계산하고, 결제는 아직 모의 결제까지만 해 봤다.

`Next.js` `TypeScript` `Supabase` `PortOne`

### 🎙 voice-record

녹음 파일을 글로 바꿔 주는 무료 도구. 웹판은 휴대폰 브라우저 안에서 변환해서 녹음이 기기 밖으로 나가지 않는다. AI가 짧은 문장 하나로 시험해 보고 기본 엔진을 바꿨는데, 실제 회의 녹음으로 다시 돌려 보니 단어가 엉뚱하게 붙어서 원래 엔진으로 되돌렸다.

`Python` `faster-whisper` `transformers.js` → **[저장소](https://github.com/JeongSangMyeong/voice-record)**

### 🖐 손 재활기기 게임

손에 쥐는 재활기기를 기울이고 눌러서 하는 태블릿 게임. 벽돌깨기, 비행기 슈팅, 테트리스가 있다. 2024년에 개인 외주로 만들었다. ▶︎ **[시연 영상](https://youtu.be/1YC9MNHcwRc)**

`Flutter` `Dart` `블루투스 시리얼(SPP)` → **[저장소](https://github.com/JeongSangMyeong/hand-rehab-game)**

---

## 공부하며 만든 것

- **[Spring-boot-Photogram](https://github.com/JeongSangMyeong/Spring-boot-Photogram)** · Spring Boot 3로 만든 인스타그램 클론. 강의 코드의 버그를 고치고 기능을 붙인 부분은 [README](https://github.com/JeongSangMyeong/Spring-boot-Photogram#직접-구현한-부분)에 커밋까지 적어 뒀다.
- **[naver-search](https://github.com/JeongSangMyeong/naver-search)** · 네이버 검색 API 6종(블로그·뉴스·책·카페·지식인·지역)을 한 화면에서 검색. Next.js 14.
