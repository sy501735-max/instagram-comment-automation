"""
lead_extractor.py
영업 기회(가격/예약/위치 문의)가 있는 댓글을 추출하여
리드 목록으로 정리합니다.
"""

from datetime import datetime


LEAD_INTENTS = {"price_inquiry", "booking_inquiry", "location_inquiry"}


class LeadExtractor:
    """영업 기회 댓글을 리드(lead)로 추출 및 정리"""

    def extract(self, comments: list[dict]) -> list[dict]:
        """
        분류된 댓글 목록에서 영업 기회 댓글만 추출

        Args:
            comments: [{"username", "text", "intent", "post_id", "created_at", ...}]

        Returns:
            리드 목록 (영업 기회 댓글만, 시간순)
        """
        leads = []
        for c in comments:
            if c.get("intent") in LEAD_INTENTS:
                leads.append({
                    "username": c.get("username", ""),
                    "comment": c.get("text", ""),
                    "intent": c.get("intent"),
                    "post_id": c.get("post_id", ""),
                    "created_at": c.get("created_at", ""),
                    "status": "new",  # new -> contacted -> converted / lost
                })
        return leads

    def summary(self, leads: list[dict]) -> dict:
        """리드 요약 통계"""
        by_intent = {}
        for lead in leads:
            intent = lead["intent"]
            by_intent[intent] = by_intent.get(intent, 0) + 1

        return {
            "total_leads": len(leads),
            "by_intent": by_intent,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }

    def to_markdown(self, leads: list[dict]) -> str:
        """리드 목록을 Markdown 표로 출력"""
        summary = self.summary(leads)

        intent_label = {
            "price_inquiry": "💰 가격문의",
            "booking_inquiry": "📅 예약문의",
            "location_inquiry": "📍 위치문의",
        }

        lines = [
            "# 인스타그램 영업 리드 목록",
            f"\n> 생성일시: {summary['generated_at']}",
            f"> 총 리드 수: **{summary['total_leads']}건**\n",
        ]

        if summary["by_intent"]:
            lines.append("## 유형별 분포\n")
            for intent, count in summary["by_intent"].items():
                lines.append(f"- {intent_label.get(intent, intent)}: {count}건")
            lines.append("")

        lines += [
            "## 리드 상세",
            "| 사용자 | 문의 유형 | 댓글 내용 | 상태 |",
            "|--------|----------|-----------|------|",
        ]

        for lead in leads:
            label = intent_label.get(lead["intent"], lead["intent"])
            comment_preview = lead["comment"][:40] + ("..." if len(lead["comment"]) > 40 else "")
            lines.append(f"| @{lead['username']} | {label} | {comment_preview} | {lead['status']} |")

        return "\n".join(lines)
