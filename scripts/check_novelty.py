#!/usr/bin/env python3
"""
check_novelty.py - Literature Novelty Checker
Adapted from SakanaAI/AI-Scientist's generate_ideas.py

Given a paper title and abstract (or a Markdown file), iteratively searches
Semantic Scholar or OpenAlex to determine if the research angle is novel.

Usage:
    python scripts/check_novelty.py --title "My Paper Title" --abstract "We propose..."
    python scripts/check_novelty.py papers/my_paper.md
    python scripts/check_novelty.py papers/my_paper.md --engine openalex
    python scripts/check_novelty.py papers/my_paper.md --rounds 5

Environment:
    ANTHROPIC_API_KEY or OPENAI_API_KEY must be set.
    S2_API_KEY (optional) for Semantic Scholar higher throughput.
    OPENALEX_MAIL_ADDRESS (optional) for OpenAlex polite pool.
"""

import argparse
import json
import os
import re
import sys
import time

import backoff
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llm_utils import get_client_and_model, call_llm_multi_turn, extract_json_between_markers

S2_API_KEY = os.getenv("S2_API_KEY")


# ---------------------------------------------------------------------------
# Paper search (Semantic Scholar / OpenAlex)
# ---------------------------------------------------------------------------

@backoff.on_exception(backoff.expo, requests.exceptions.HTTPError, max_tries=5)
def search_papers(query, result_limit=10, engine="semanticscholar"):
    """Search for papers using Semantic Scholar or OpenAlex."""
    if not query:
        return None

    if engine == "semanticscholar":
        headers = {"X-API-KEY": S2_API_KEY} if S2_API_KEY else {}
        rsp = requests.get(
            "https://api.semanticscholar.org/graph/v1/paper/search",
            headers=headers,
            params={
                "query": query,
                "limit": result_limit,
                "fields": "title,authors,venue,year,abstract,citationCount",
            },
        )
        rsp.raise_for_status()
        results = rsp.json()
        time.sleep(1.0)  # Rate limiting

        if not results.get("total"):
            return None
        return results["data"]

    elif engine == "openalex":
        try:
            import pyalex
            from pyalex import Works
        except ImportError:
            print("Error: pip install pyalex  (required for OpenAlex engine)")
            sys.exit(1)

        mail = os.environ.get("OPENALEX_MAIL_ADDRESS")
        if mail:
            pyalex.config.email = mail

        works = Works().search(query).get(per_page=result_limit)
        papers = []
        for work in works:
            venue = "Unknown"
            for loc in work.get("locations", []):
                if loc.get("source") and loc["source"].get("display_name"):
                    venue = loc["source"]["display_name"]
                    break
            authors_list = [a["author"]["display_name"] for a in work.get("authorships", [])]
            authors = " and ".join(authors_list) if len(authors_list) < 20 else f"{authors_list[0]} et al."
            abstract = work.get("abstract") or ""
            papers.append({
                "title": work.get("title", ""),
                "authors": authors,
                "venue": venue,
                "year": work.get("publication_year"),
                "abstract": abstract[:1000],
                "citationCount": work.get("cited_by_count", 0),
            })
        return papers

    else:
        raise ValueError(f"Unknown engine: {engine}")


# ---------------------------------------------------------------------------
# Extract title/abstract from Markdown
# ---------------------------------------------------------------------------

def extract_from_markdown(filepath):
    """Extract title and abstract from a Markdown paper file."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Try to find title (first H1)
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else ""

    # Try to find abstract section
    abstract = ""
    abstract_match = re.search(
        r"(?:^#+\s*Abstract\s*\n)(.*?)(?=\n#+\s|\Z)",
        content,
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if abstract_match:
        abstract = abstract_match.group(1).strip()
    else:
        # Fallback: use first ~500 chars after the title
        lines = content.split("\n")
        body_lines = []
        past_title = False
        for line in lines:
            if line.startswith("# ") and not past_title:
                past_title = True
                continue
            if past_title and line.strip():
                body_lines.append(line.strip())
                if len(" ".join(body_lines)) > 500:
                    break
        abstract = " ".join(body_lines)

    return title, abstract


# ---------------------------------------------------------------------------
# Novelty checking (adapted from AI-Scientist)
# ---------------------------------------------------------------------------

NOVELTY_SYSTEM_PROMPT = """You are a rigorous academic researcher evaluating whether a paper idea is novel.
Your job is to determine if the idea overlaps with existing published work.
Be a harsh critic for novelty. A paper must make a clear, distinct contribution beyond what already exists.

You will have access to academic search results (top 10 papers per query).
You will be given {num_rounds} rounds to search and decide, but you can exit early.

At any round, you may make a decision:
- "Decision made: novel." if after sufficient searching, no paper overlaps meaningfully.
- "Decision made: not novel." if you found a paper that covers the same ground."""

NOVELTY_PROMPT = """Round {current_round}/{num_rounds}.

The paper idea under evaluation:
Title: {title}
Abstract: {abstract}

The results of the last search query (empty on first round):
\"\"\"
{last_query_results}
\"\"\"

Respond in the following format:

THOUGHT:
<THOUGHT>

RESPONSE:
```json
<JSON>
```

In <THOUGHT>, reason about the idea and identify a search query to help evaluate novelty.
If you have enough evidence to decide, add "Decision made: novel." or "Decision made: not novel." to your thoughts.

In <JSON>, respond with:
- "Query": A search query to find potentially overlapping papers. Leave empty string if you have decided.
- "Reasoning": Brief explanation of your current assessment.

This JSON will be automatically parsed, so ensure the format is precise."""


def check_novelty(title, abstract, client, model, provider, max_rounds=10, engine="semanticscholar"):
    """
    Iteratively search literature to determine if the paper idea is novel.
    Returns (is_novel: bool, reasoning: str, papers_found: list)
    """
    system_msg = NOVELTY_SYSTEM_PROMPT.format(num_rounds=max_rounds)
    messages = []
    papers_str = ""
    all_papers_found = []

    for j in range(max_rounds):
        user_msg = NOVELTY_PROMPT.format(
            current_round=j + 1,
            num_rounds=max_rounds,
            title=title,
            abstract=abstract,
            last_query_results=papers_str,
        )
        messages.append({"role": "user", "content": user_msg})

        try:
            response = call_llm_multi_turn(client, model, provider, system_msg, messages)
            messages.append({"role": "assistant", "content": response})

            if "decision made: novel" in response.lower():
                json_output = extract_json_between_markers(response)
                reasoning = json_output.get("Reasoning", "") if json_output else ""
                return True, reasoning, all_papers_found

            if "decision made: not novel" in response.lower():
                json_output = extract_json_between_markers(response)
                reasoning = json_output.get("Reasoning", "") if json_output else ""
                return False, reasoning, all_papers_found

            json_output = extract_json_between_markers(response)
            if json_output is None:
                continue

            query = json_output.get("Query", "")
            if not query:
                continue

            print(f"  Round {j + 1}: Searching '{query}'...")
            papers = search_papers(query, result_limit=10, engine=engine)

            if papers is None:
                papers_str = "No papers found."
                continue

            all_papers_found.extend(papers)
            paper_strings = []
            for i, paper in enumerate(papers):
                paper_strings.append(
                    f"{i}: {paper['title']}. {paper.get('authors', 'Unknown')}. "
                    f"{paper.get('venue', 'Unknown')}, {paper.get('year', 'Unknown')}.\n"
                    f"Citations: {paper.get('citationCount', 0)}\n"
                    f"Abstract: {paper.get('abstract', 'N/A')}"
                )
            papers_str = "\n\n".join(paper_strings)

        except Exception as e:
            print(f"  Error in round {j + 1}: {e}")
            continue

    # If we exhausted all rounds without a decision, lean towards novel
    return True, "No definitive overlap found after exhaustive search.", all_papers_found


def print_result(is_novel, reasoning, papers_found, title):
    """Pretty-print the novelty check result."""
    print("\n" + "=" * 70)
    print("  NOVELTY CHECK RESULT")
    print("=" * 70)
    print(f"\n  Paper: {title}")
    print(f"  Verdict: {'NOVEL' if is_novel else 'NOT NOVEL'}")
    icon = "✅" if is_novel else "⚠️"
    print(f"  {icon} {reasoning}")
    print(f"\n  Papers examined: {len(papers_found)}")

    if papers_found:
        print("\n  Most relevant papers found:")
        seen_titles = set()
        for p in papers_found[:10]:
            t = p.get("title", "Unknown")
            if t not in seen_titles:
                seen_titles.add(t)
                cites = p.get("citationCount", 0)
                year = p.get("year", "?")
                print(f"    - [{year}] {t} (citations: {cites})")

    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Check if a research paper idea is novel by searching existing literature.",
        epilog="Example: python scripts/check_novelty.py papers/my_paper.md",
    )
    parser.add_argument("paper", nargs="?", help="Path to paper .md file (extracts title & abstract)")
    parser.add_argument("--title", type=str, help="Paper title (if not using a file)")
    parser.add_argument("--abstract", type=str, help="Paper abstract (if not using a file)")
    parser.add_argument(
        "--rounds", type=int, default=10,
        help="Maximum number of search rounds (default: 10)",
    )
    parser.add_argument(
        "--engine", type=str, default="semanticscholar",
        choices=["semanticscholar", "openalex"],
        help="Search engine to use (default: semanticscholar)",
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="Save result JSON to this file",
    )
    args = parser.parse_args()

    # Get title and abstract
    if args.paper:
        if not os.path.exists(args.paper):
            print(f"Error: File not found: {args.paper}")
            sys.exit(1)
        title, abstract = extract_from_markdown(args.paper)
        if not title:
            print("Warning: Could not extract title from file. Use --title flag.")
    elif args.title:
        title = args.title
        abstract = args.abstract or ""
    else:
        print("Error: Provide either a paper file or --title and --abstract.")
        parser.print_help()
        sys.exit(1)

    print(f"Checking novelty for: {title}")
    if abstract:
        print(f"Abstract preview: {abstract[:150]}...")

    client, model, provider = get_client_and_model()
    print(f"Using model: {model} ({provider})")
    print(f"Search engine: {args.engine}")
    print(f"Max rounds: {args.rounds}\n")

    is_novel, reasoning, papers_found = check_novelty(
        title, abstract, client, model, provider,
        max_rounds=args.rounds,
        engine=args.engine,
    )

    print_result(is_novel, reasoning, papers_found, title)

    # Save result
    result = {
        "title": title,
        "abstract": abstract,
        "novel": is_novel,
        "reasoning": reasoning,
        "papers_examined": len(papers_found),
        "engine": args.engine,
    }

    output_path = args.output
    if not output_path and args.paper:
        base = os.path.splitext(args.paper)[0]
        output_path = f"{base}_novelty.json"

    if output_path:
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Result saved to: {output_path}")


if __name__ == "__main__":
    main()
