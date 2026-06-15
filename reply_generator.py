"""
reply_generator.py
의도별 맞춤 자동 댓글 답변을 생성합니다.
"""

import random
from datetime import datetime


# 의도별 답변 템플릿 (여러 개 중 랜덤 선택 → 자연스러움)
REPLY_TEMPLATES = {
    "price_inquiry": [
        "안녕하세요! 가격은 시술 종류에 따라 달라서 프로필 링크의 예약 페이지에서 확인 부탁드려요 😊 더 궁금한 점은 DM 주세요!",
        "문의 감사합니다 💕 정확한 견적은 상담 후 안내드리고 있어요. DM으로 연락주시면 빠르게 도와드릴게요!",
        "안녕하세요~ 가격표는 프로필 링크에서 확인 가능하세요! 추가 문의는 DM 환영입니다 😊",
    ],
    "booking_inquiry": [
        "네 가능해요! 정확한 시간은 DM으로 문의주시면 빠르게 안내드릴게요 😊",
        "예약 도와드릴게요! 프로필 링크에서 원하시는 날짜 확인 후 DM 주세요 💕",
        "안녕하세요! 예약 문의는 DM으로 연락주시면 바로 확인해드려요 😊 감사합니다!",
    ],
    "location_inquiry": [
        "안녕하세요! 위치는 프로필 링크에서 확인 가능하세요 😊 찾아오시는 길 헷갈리시면 DM 주세요!",
        "오시는 길 안내드릴게요! 프로필 지도 링크 참고해주세요 💕",
    ],
    "compliment": [
        "감사합니다 💕💕",
        "너무 감사해요 😊 좋게 봐주셔서 힘이 나네요!",
        "감사합니다!! 다음에도 좋은 콘텐츠로 찾아올게요 💕",
        "와 감사합니다 😍 너무 행복하네요!",
    ],
    "complaint": [
        "불편을 드려 죄송합니다. DM으로 자세한 상황 알려주시면 바로 확인 후 도와드리겠습니다 🙏",
        "소중한 의견 감사합니다. DM 주시면 빠르게 해결방안 안내드릴게요.",
    ],
    "general": [
        "댓글 감사합니다 😊",
        "방문해주셔서 감사해요 💕",
    ],
}

# 시간대별 인사말 (선택적으로 앞에 붙일 수 있음)
GREETING_BY_TIME = {
    "morning": "좋은 아침이에요! ",
    "afternoon": "",
    "evening": "오늘 하루도 고생하셨어요! ",
}


class ReplyGenerator:
    """분류된 의도에 따라 자동 댓글 답변 생성"""

    def __init__(self, brand_name: str = "", use_greeting: bool = False):
        self.brand_name = brand_name
        self.use_greeting = use_greeting

    def _get_time_period(self) -> str:
        hour = datetime.now().hour
        if 5 <= hour < 11:
            return "morning"
        elif 11 <= hour < 18:
            return "afternoon"
        return "evening"

    def generate(self, comment: dict) -> dict:
        """
        단일 댓글에 대한 답변 생성

        Args:
            comment: {"username": str, "text": str, "intent": str, "priority_score": int}

        Returns:
            {"username": ..., "reply": ..., "intent": ..., "auto_send": bool}
        """
        intent = comment.get("intent", "general")
        templates = REPLY_TEMPLATES.get(intent, REPLY_TEMPLATES["general"])
        reply = random.choice(templates)

        if self.use_greeting:
            greeting = GREETING_BY_TIME[self._get_time_period()]
            reply = greeting + reply

        # 스팸/일반은 자동발송, 영업/불만 댓글은 검토 후 발송 권장
        auto_send = intent not in ("complaint", "spam")
        review_recommended = intent in ("complaint", "price_inquiry", "booking_inquiry")

        return {
            "username": comment.get("username", ""),
            "original_comment": comment.get("text", ""),
            "intent": intent,
            "reply": reply,
            "auto_send": auto_send,
            "review_recommended": review_recommended,
            "priority_score": comment.get("priority_score", 0),
        }

    def batch_generate(self, comments: list[dict]) -> list[dict]:
        """전체 댓글 목록에 대한 답변 일괄 생성, 우선순위 순 정렬"""
        results = [self.generate(c) for c in comments if c.get("intent") != "spam"]
        results.sort(key=lambda x: x["priority_score"], reverse=True)
        return results

    def to_markdown(self, replies: list[dict]) -> str:
        """답변 목록을 Markdown으로 출력"""
        lines = [
            "# 인스타그램 댓글 자동 답변 목록",
            f"\n> 생성일시: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"> 총 {len(replies)}건\n",
            "---\n",
        ]

        intent_label = {
            "price_inquiry": "💰 가격문의",
            "booking_inquiry": "📅 예약문의",
            "location_inquiry": "📍 위치문의",
            "compliment": "💕 칭찬",
            "complaint": "⚠️ 불만/문제",
            "general": "💬 일반",
        }

        for i, r in enumerate(replies, 1):
            label = intent_label.get(r["intent"], r["intent"])
            review_mark = " 🔍 검토 권장" if r["review_recommended"] else ""

            lines += [
                f"## {i}. @{r['username']} — {label}{review_mark}",
                f"**원본 댓글:** {r['original_comment']}",
                f"\n**자동 답변 (제안):**",
                f"> {r['reply']}",
                "",
                "---\n",
            ]

        return "\n".join(lines)
