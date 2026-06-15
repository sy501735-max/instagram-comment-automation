"""
Instagram Comment Automation — Main Entry Point
인스타그램 댓글 자동 분류 및 답글 생성 시스템
"""

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.classifier.comment_classifier import CommentClassifier
from src.reply.reply_generator import ReplyGenerator


def load_comments(path: str) -> list[dict]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {p}")
    comments = []
    with open(p, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            comments.append({k: v.strip() for k, v in row.items()})
    return comments


def main():
    parser = argparse.ArgumentParser(description="인스타그램 댓글 자동 분류 & 답글 생성")
    parser.add_argument("--comments", default="data/sample_comments.csv")
    parser.add_argument("--output", default="examples")
    args = parser.parse_args()

    print("=" * 50)
    print("  💬 Instagram Comment Automation")
    print("  인스타그램 댓글 자동 분류 & 답글 생성")
    print("=" * 50)

    comments = load_comments(args.comments)
    classifier = CommentClassifier()
    analyzed = classifier.batch_analyze(comments)
    summary = classifier.get_summary(analyzed)

    print(f"\n  ✅ 전체 댓글: {summary['total']}건")
    print(f"  🔴 긴급 처리: {summary['urgent_count']}건")
    print(f"  📊 카테고리: {summary['by_category']}\n")

    replies = ReplyGenerator(seed=42).batch_generate(analyzed)

    Path(args.output).mkdir(exist_ok=True)
    with open(f"{args.output}/comment_analysis_report.md", "w", encoding="utf-8") as f:
        f.write(classifier.to_markdown(analyzed, summary))
    with open(f"{args.output}/auto_replies.md", "w", encoding="utf-8") as f:
        f.write(ReplyGenerator(seed=42).to_markdown(replies))

    print(f"  📄 분석 리포트: {args.output}/comment_analysis_report.md")
    print(f"  💬 답글 목록:   {args.output}/auto_replies.md")
    print("\n✨ 완료!\n")


if __name__ == "__main__":
    main()
