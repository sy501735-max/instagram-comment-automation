"""
comment_classifier.py
인스타그램 댓글을 의도별로 분류합니다.
(가격문의 / 예약문의 / 칭찬 / 불만 / 스팸 / 일반)
"""

import re
from typing import Optional


# 의도별 키워드 패턴
INTENT_PATTERNS = {
    "price_inquiry": [
        "가격", "얼마", "비용", "금액", "할인", "이벤트가",
        "원이에요", "비싸", "저렴",
    ],
    "booking_inquiry": [
        "예약", "방문", "언제", "시간", "가능한가요", "되나요",
        "오늘", "내일", "주말", "평일",
    ],
    "location_inquiry": [
        "어디", "위치", "주소", "찾아가", "근처", "지점",
    ],
    "compliment": [
        "예쁘", "이쁘", "대박", "완전", "찐", "최고", "멋지",
        "부럽", "잘하시", "감사", "❤️", "♥", "👍", "🔥",
    ],
    "complaint": [
        "별로", "실망", "환불", "불만", "최악", "안좋", "다시는",
    ],
    "spam": [
        "http", "www.", "팔로우", "맞팔", "광고", "홍보문의",
        "DM 주세요", "텔레그램",
    ],
}

# 우선순위 (먼저 매칭되는 게 우선)
INTENT_PRIORITY = [
    "spam",
    "complaint",
    "price_inquiry",
    "booking_inquiry",
    "location_inquiry",
    "compliment",
]


class CommentClassifier:
    """댓글 텍스트를 분석하여 의도(intent)를 분류"""

    def classify(self, comment_text: str) -> str:
        """
        댓글의 의도를 분류합니다.

        Returns:
            intent: "price_inquiry" | "booking_inquiry" | "location_inquiry" |
                    "compliment" | "complaint" | "spam" | "general"
        """
        text = comment_text.lower()

        for intent in INTENT_PRIORITY:
            patterns = INTENT_PATTERNS[intent]
            for pattern in patterns:
                if pattern.lower() in text:
                    return intent

        return "general"

    def extract_mentions(self, comment_text: str) -> list[str]:
        """댓글 내 @멘션 추출"""
        return re.findall(r"@(\w+)", comment_text)

    def needs_reply(self, intent: str) -> bool:
        """답변이 필요한 의도인지 판단"""
        # 스팸과 일반 칭찬(이모지만)은 자동 답변 우선순위 낮음
        return intent not in ("spam",)

    def get_priority_score(self, intent: str) -> int:
        """
        댓글 처리 우선순위 점수 (높을수록 빨리 처리해야 함)
        영업 기회 댓글을 최우선으로 처리
        """
        scores = {
            "complaint": 100,       # 즉시 대응 필요
            "booking_inquiry": 90,  # 영업 기회
            "price_inquiry": 85,    # 영업 기회
            "location_inquiry": 70,
            "compliment": 30,
            "general": 20,
            "spam": 0,
        }
        return scores.get(intent, 20)
