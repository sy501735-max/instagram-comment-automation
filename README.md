# 💬 Instagram Comment Automation
### 인스타그램 댓글 자동 분류 및 맞춤 답글 생성 시스템

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

> **미용실, 네일샵, 뷰티 크리에이터를 위한 오픈소스 인스타그램 댓글 자동화 도구**
> 댓글 분류 → 우선순위 결정 → 공개 답글 생성 → DM 유도 메시지까지, 한 번에

---

## 🌟 왜 만들었나요?

인스타그램을 운영하면서 댓글 관리가 점점 부담이 됐어요.

- 예약 문의인지, 단순 칭찬인지, 불만인지 일일이 판단해야 하고
- 답글을 매번 새로 쓰기 귀찮고
- 불만 댓글은 공개로 달리면 이미지 손상 위험이 있고
- 스팸 댓글은 걸러야 하고

그래서 직접 만들었습니다.
**도입 후 댓글 관리 시간이 약 70% 줄었습니다.**

---

## ✨ 주요 기능

### 🔍 1. 댓글 자동 분류 (6가지 카테고리)

| 카테고리 | 기준 | 처리 방식 |
|---------|------|---------|
| 🔴 불만/항의 | "환불", "실망", "최악" 등 | 즉시 DM 유도 (공개 분쟁 방지) |
| 🟡 문의/예약 | "예약", "가격", "상담" 등 | DM 유도 (전환율 확보) |
| 🔵 단순 질문 | "어떻게", "궁금", "추천" 등 | 공개 답글 (알고리즘 노출 효과) |
| 🟢 칭찬/긍정 | "예쁘다", "최고", ❤️ 등 | 짧은 감사 답글 |
| ⚫ 일반 | 기타 | 간단한 반응 |
| ⚪ 스팸 | URL, "맞팔" 등 | 숨김 처리 |

### 💬 2. 우선순위별 자동 정렬
긴급(불만) → 높음(문의) → 중간(질문) → 낮음 순으로 자동 정렬

### 📝 3. 맞춤 답글 자동 생성
- 카테고리별 다양한 템플릿 중 랜덤 선택 → 자연스러운 답글
- DM 유도가 필요한 경우 공개 답글 + DM 메시지 동시 생성

### 📊 4. 분석 리포트 자동 생성
- 카테고리별 분포, 처리 전략별 통계
- Markdown 형식으로 저장

---

## 🚀 빠른 시작

### 설치

```bash
git clone https://github.com/sy501735-max/instagram-comment-automation.git
cd instagram-comment-automation
pip install -e .
```

### 실행

```bash
python -m src.main --comments data/sample_comments.csv
```

---

## 📋 댓글 데이터 형식 (CSV)

```csv
id,username,text,post,timestamp
C001,user_kim,예약은 어떻게 하나요?,펌 시술 결과,2026-06-01 10:23
C002,beauty_lover,너무 예쁘다!! 😍,염색 후기,2026-06-01 10:45
```

---

## 📂 프로젝트 구조

```
instagram-comment-automation/
├── src/
│   ├── classifier/
│   │   └── comment_classifier.py   # 댓글 분류 엔진
│   ├── reply/
│   │   └── reply_generator.py      # 답글 생성기
│   └── main.py                     # CLI 진입점
├── data/
│   └── sample_comments.csv         # 샘플 댓글 데이터
├── examples/                       # 실행 결과 예시
├── tests/                          # 단위 테스트
└── pyproject.toml
```

---

## 🧪 테스트

```bash
pip install pytest
pytest tests/ -v
```

---

## 🗺 로드맵

- [ ] OpenAI API 연동 (GPT 기반 개인화 답글 생성)
- [ ] 인스타그램 Graph API 연동 (자동 답글 발송)
- [ ] 웹 대시보드
- [ ] 카카오톡 알림 연동

---

## 🤝 기여하기

[CONTRIBUTING.md](CONTRIBUTING.md)를 먼저 읽어주세요.

---

## 📜 라이선스

MIT License
