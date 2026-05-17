#!/usr/bin/env python3
"""
review_paper.py - AI Peer Review for Research Papers
Adapted from SakanaAI/AI-Scientist's perform_review.py

Sends your paper to an LLM for a structured academic review.
Returns scores, strengths, weaknesses, and an accept/reject decision.

Usage:
    python scripts/review_paper.py papers/my_paper.md
    python scripts/review_paper.py papers/my_paper.pdf
    python scripts/review_paper.py papers/my_paper.md --reflections 3
    python scripts/review_paper.py papers/my_paper.md --ensemble 3

Environment:
    ANTHROPIC_API_KEY or OPENAI_API_KEY must be set.
    REVIEW_MODEL (optional) to override the default model.
"""

import argparse
import json
import os
import sys

# Add scripts dir to path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llm_utils import get_client_and_model, call_llm, call_llm_multi_turn, extract_json_between_markers


REVIEWER_SYSTEM_PROMPT = (
    "You are a senior academic reviewer at a top-tier research venue (e.g. NeurIPS, IEEE, SSRN). "
    "You are reviewing a paper that has been submitted for publication. "
    "Be critical, fair, and constructive in your assessment. "
    "If the paper has serious flaws or you are unsure about its quality, reflect that in your scores."
)

REVIEW_FORM = """
Please review the paper using the following rubric. Consider each dimension carefully.

Respond in the following format:

THOUGHT:
<THOUGHT>

REVIEW JSON:
```json
<JSON>
```

In <THOUGHT>, briefly discuss your intuitions and reasoning for the evaluation.
Detail your high-level arguments and assessment. Be specific to this paper.
Treat this as the note-taking phase of your review.

In <JSON>, provide the review in JSON format with the following fields (in order):
- "Summary": A 2-3 sentence summary of the paper's content and contributions.
- "Strengths": A list of strengths (each a string).
- "Weaknesses": A list of weaknesses (each a string).
- "Originality": A rating from 1 to 4 (1=low, 2=medium, 3=high, 4=very high).
- "Quality": A rating from 1 to 4 (1=low, 2=medium, 3=high, 4=very high).
- "Clarity": A rating from 1 to 4 (1=low, 2=medium, 3=high, 4=very high).
- "Significance": A rating from 1 to 4 (1=low, 2=medium, 3=high, 4=very high).
- "Soundness": A rating from 1 to 4 (1=poor, 2=fair, 3=good, 4=excellent).
- "Presentation": A rating from 1 to 4 (1=poor, 2=fair, 3=good, 4=excellent).
- "Contribution": A rating from 1 to 4 (1=poor, 2=fair, 3=good, 4=excellent).
- "Overall": A rating from 1 to 10 (1=very strong reject, 10=award quality).
- "Confidence": A rating from 1 to 5 (1=low, 5=absolute certainty).
- "Questions": A list of clarifying questions for the authors.
- "Suggestions": A list of actionable suggestions for improvement.
- "Decision": Either "Accept" or "Reject".

Scoring guide for Overall:
  10: Award quality - technically flawless with groundbreaking impact.
   9: Very Strong Accept - technically flawless, excellent impact.
   8: Strong Accept - technically strong, novel ideas, excellent impact.
   7: Accept - technically solid, high impact on at least one area.
   6: Weak Accept - technically solid, moderate-to-high impact.
   5: Borderline Accept - reasons to accept slightly outweigh reasons to reject.
   4: Borderline Reject - reasons to reject slightly outweigh reasons to accept.
   3: Reject - technical flaws, weak evaluation.
   2: Strong Reject - major technical flaws, limited impact.
   1: Very Strong Reject - trivial results or fundamental issues.

This JSON will be automatically parsed, so ensure the format is precise.
"""

REFLECTION_PROMPT = """Round {current_round}/{num_reflections}.
Carefully reconsider the accuracy and fairness of the review you just wrote.
Think about whether you missed any important strengths or weaknesses.
Ensure the scores are consistent with your written assessment.

Respond in the same format as before:
THOUGHT:
<THOUGHT>

REVIEW JSON:
```json
<JSON>
```

If there is nothing to improve, repeat the previous JSON exactly and include "I am done" in your thoughts.
ONLY INCLUDE "I am done" IF YOU ARE MAKING NO MORE CHANGES."""


def load_paper(filepath):
    """Load paper content from Markdown or PDF."""
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".md":
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    elif ext == ".pdf":
        # Try multiple PDF extraction methods
        try:
            import pymupdf4llm
            return pymupdf4llm.to_markdown(filepath)
        except (ImportError, Exception):
            pass

        try:
            import pymupdf
            doc = pymupdf.open(filepath)
            text = ""
            for page in doc:
                text += page.get_text()
            if len(text) > 100:
                return text
        except (ImportError, Exception):
            pass

        try:
            from pypdf import PdfReader
            reader = PdfReader(filepath)
            return "".join(page.extract_text() for page in reader.pages)
        except (ImportError, Exception):
            pass

        print("Error: Cannot read PDF. Install one of: pymupdf4llm, pymupdf, pypdf")
        print("  pip install pymupdf4llm  (recommended)")
        sys.exit(1)

    elif ext == ".html":
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    else:
        print(f"Error: Unsupported file format '{ext}'. Use .md, .pdf, or .html")
        sys.exit(1)


def perform_review(paper_text, client, model, provider, num_reflections=3, temperature=0.4):
    """
    Perform an AI review of the paper.
    Uses iterative reflection to refine the review.
    """
    user_prompt = REVIEW_FORM + f"\nHere is the paper you are asked to review:\n```\n{paper_text}\n```"

    # Initial review
    messages = [{"role": "user", "content": user_prompt}]
    response = call_llm_multi_turn(client, model, provider, REVIEWER_SYSTEM_PROMPT, messages, temperature)
    messages.append({"role": "assistant", "content": response})

    review = extract_json_between_markers(response)

    # Iterative reflection
    if num_reflections > 1 and review is not None:
        for j in range(num_reflections - 1):
            reflection_msg = REFLECTION_PROMPT.format(
                current_round=j + 2,
                num_reflections=num_reflections,
            )
            messages.append({"role": "user", "content": reflection_msg})
            response = call_llm_multi_turn(client, model, provider, REVIEWER_SYSTEM_PROMPT, messages, temperature)
            messages.append({"role": "assistant", "content": response})

            new_review = extract_json_between_markers(response)
            if new_review is not None:
                review = new_review

            if "I am done" in response:
                break

    return review


def perform_ensemble_review(paper_text, client, model, provider, num_reviews=3, num_reflections=3, temperature=0.6):
    """
    Run multiple independent reviews and aggregate scores.
    Higher temperature for diversity across reviewers.
    """
    reviews = []
    for i in range(num_reviews):
        print(f"  Reviewer {i + 1}/{num_reviews}...")
        review = perform_review(paper_text, client, model, provider, num_reflections, temperature)
        if review is not None:
            reviews.append(review)

    if not reviews:
        print("Error: All reviews failed.")
        return None

    # Aggregate: use the first review as base, average the scores
    aggregated = reviews[0].copy()

    score_fields = {
        "Originality": (1, 4),
        "Quality": (1, 4),
        "Clarity": (1, 4),
        "Significance": (1, 4),
        "Soundness": (1, 4),
        "Presentation": (1, 4),
        "Contribution": (1, 4),
        "Overall": (1, 10),
        "Confidence": (1, 5),
    }

    for field, (lo, hi) in score_fields.items():
        scores = [r[field] for r in reviews if field in r and lo <= r[field] <= hi]
        if scores:
            aggregated[field] = round(sum(scores) / len(scores), 1)

    # Merge strengths and weaknesses (deduplicate)
    all_strengths = []
    all_weaknesses = []
    all_questions = []
    all_suggestions = []
    for r in reviews:
        all_strengths.extend(r.get("Strengths", []))
        all_weaknesses.extend(r.get("Weaknesses", []))
        all_questions.extend(r.get("Questions", []))
        all_suggestions.extend(r.get("Suggestions", []))

    # Simple deduplication
    aggregated["Strengths"] = list(dict.fromkeys(all_strengths))
    aggregated["Weaknesses"] = list(dict.fromkeys(all_weaknesses))
    aggregated["Questions"] = list(dict.fromkeys(all_questions))
    aggregated["Suggestions"] = list(dict.fromkeys(all_suggestions))

    # Decision based on average overall score
    aggregated["Decision"] = "Accept" if aggregated["Overall"] >= 5.5 else "Reject"
    aggregated["_num_reviewers"] = len(reviews)

    return aggregated


def print_review(review):
    """Pretty-print the review to terminal."""
    if review is None:
        print("No review generated.")
        return

    print("\n" + "=" * 70)
    print("  AI PEER REVIEW")
    print("=" * 70)

    print(f"\n  Decision: {review.get('Decision', 'N/A')}")
    print(f"  Overall Score: {review.get('Overall', 'N/A')}/10")
    if "_num_reviewers" in review:
        print(f"  (Aggregated from {review['_num_reviewers']} reviewers)")
    print()

    # Score table
    scores = [
        ("Originality", 4), ("Quality", 4), ("Clarity", 4), ("Significance", 4),
        ("Soundness", 4), ("Presentation", 4), ("Contribution", 4), ("Confidence", 5),
    ]
    print("  Scores:")
    for name, max_val in scores:
        val = review.get(name, "N/A")
        bar = ""
        if isinstance(val, (int, float)):
            filled = int(round(val))
            bar = " " + "█" * filled + "░" * (max_val - filled)
        print(f"    {name:<15} {val}/{max_val}{bar}")

    print(f"\n  Summary:\n    {review.get('Summary', 'N/A')}")

    print("\n  Strengths:")
    for s in review.get("Strengths", []):
        print(f"    + {s}")

    print("\n  Weaknesses:")
    for w in review.get("Weaknesses", []):
        print(f"    - {w}")

    if review.get("Questions"):
        print("\n  Questions:")
        for q in review["Questions"]:
            print(f"    ? {q}")

    if review.get("Suggestions"):
        print("\n  Suggestions:")
        for s in review["Suggestions"]:
            print(f"    > {s}")

    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="AI Peer Review for Research Papers",
        epilog="Example: python scripts/review_paper.py papers/my_paper.md",
    )
    parser.add_argument("paper", help="Path to paper file (.md, .pdf, or .html)")
    parser.add_argument(
        "--reflections", type=int, default=3,
        help="Number of reflection rounds per reviewer (default: 3)",
    )
    parser.add_argument(
        "--ensemble", type=int, default=1,
        help="Number of independent reviewers to aggregate (default: 1, try 3 for better results)",
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="Save review JSON to this file (default: print to terminal only)",
    )
    parser.add_argument(
        "--temperature", type=float, default=0.4,
        help="LLM temperature (default: 0.4, higher for more varied ensemble reviews)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.paper):
        print(f"Error: File not found: {args.paper}")
        sys.exit(1)

    print(f"Loading paper: {args.paper}")
    paper_text = load_paper(args.paper)
    print(f"Paper length: {len(paper_text)} characters")

    client, model, provider = get_client_and_model()
    print(f"Using model: {model} ({provider})")

    if args.ensemble > 1:
        print(f"Running ensemble review with {args.ensemble} reviewers...")
        review = perform_ensemble_review(
            paper_text, client, model, provider,
            num_reviews=args.ensemble,
            num_reflections=args.reflections,
            temperature=max(args.temperature, 0.5),  # Ensure diversity
        )
    else:
        print(f"Running review with {args.reflections} reflection rounds...")
        review = perform_review(
            paper_text, client, model, provider,
            num_reflections=args.reflections,
            temperature=args.temperature,
        )

    print_review(review)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(review, f, indent=2)
        print(f"\nReview saved to: {args.output}")
    elif review:
        # Also save next to the paper by default
        base = os.path.splitext(args.paper)[0]
        output_path = f"{base}_review.json"
        with open(output_path, "w") as f:
            json.dump(review, f, indent=2)
        print(f"\nReview saved to: {output_path}")


if __name__ == "__main__":
    main()
