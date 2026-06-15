"""tests/test_core.py — 핵심 기능 단위 테스트"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from src.classifier.comment_classifier import CommentClassifier
from src.reply.reply_generator import ReplyGenerator


@pytest.fixture
def classifier():
    return CommentClassifier()

@pytest.fixture
def generator():
    return ReplyGenerator(seed=42)


class TestCommentClassifier:
    def test_inquiry(self, classifier):
        assert classifier.classify("예약은 어떻게 하나요?") == "inquiry"

    def test_complaint(self, classifier):
        assert classifier.classify("환불 요청합니다 너무 실망이에요") == "complaint"

    def test_praise(self, classifier):
        assert classifier.classify("너무 예쁘다 최고예요 ❤️") == "praise"

    def test_spam(self, classifier):
        assert classifier.classify("맞팔해요 http://spam.com") == "spam"

    def test_question(self, classifier):
        assert classifier.classify("어떻게 예약하는지 알려주세요") in ["inquiry", "question"]

    def test_general(self, classifier):
        assert classifier.classify("안녕하세요") == "general"

    def test_complaint_priority_over_praise(self, classifier):
        # 불만이 칭찬보다 우선
        assert classifier.classify("최고인데 환불은 어떻게 하나요") == "complaint"

    def test_batch_analyze_sorted(self, classifier):
        comments = [
            {"id": "1", "username": "a", "text": "예쁘다", "post": "", "timestamp": ""},
            {"id": "2", "username": "b", "text": "환불해주세요", "post": "", "timestamp": ""},
            {"id": "3", "username": "c", "text": "예약하고 싶어요", "post": "", "timestamp": ""},
        ]
        result = classifier.batch_analyze(comments)
        # urgent(complaint)가 먼저 와야 함
        assert result[0]["category"] == "complaint"

    def test_summary(self, classifier):
        comments = [
            {"id": "1", "username": "a", "text": "예약 문의요", "post": "", "timestamp": ""},
            {"id": "2", "username": "b", "text": "감사합니다", "post": "", "timestamp": ""},
        ]
        analyzed = classifier.batch_analyze(comments)
        summary = classifier.get_summary(analyzed)
        assert summary["total"] == 2


class TestReplyGenerator:
    def test_public_reply_generated(self, classifier, generator):
        comment = {"id": "1", "username": "test", "text": "너무 예뻐요!", "post": "", "timestamp": ""}
        analyzed = classifier.analyze(comment)
        result = generator.generate(analyzed)
        assert result["public_reply"] is not None

    def test_dm_for_inquiry(self, classifier, generator):
        comment = {"id": "1", "username": "test", "text": "예약 가능한가요?", "post": "", "timestamp": ""}
        analyzed = classifier.analyze(comment)
        result = generator.generate(analyzed)
        assert result["dm_message"] is not None
        assert "test" in result["dm_message"]

    def test_no_reply_for_spam(self, classifier, generator):
        comment = {"id": "1", "username": "spammer", "text": "맞팔해요 http://spam.com", "post": "", "timestamp": ""}
        analyzed = classifier.analyze(comment)
        result = generator.generate(analyzed)
        assert result["public_reply"] is None

    def test_batch_generate(self, classifier, generator):
        comments = [
            {"id": str(i), "username": f"user{i}", "text": t, "post": "", "timestamp": ""}
            for i, t in enumerate(["예쁘다", "예약문의요", "환불해주세요"])
        ]
        analyzed = classifier.batch_analyze(comments)
        replies = generator.batch_generate(analyzed)
        assert len(replies) == 3
