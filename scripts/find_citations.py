#!/usr/bin/env python3
"""
find_citations.py - Automated Citation Finder
Adapted from SakanaAI/AI-Scientist's perform_writeup.py citation pipeline

Reads your paper draft, identifies gaps in citations, searches for relevant
papers, and suggests where and how to add them.

Usage:
    python scripts/find_citations.py papers/my_paper.md
    python scripts/find_citations.py papers/my_paper.md --rounds 10
    python scripts/find_citations.py papers/my_paper.md --engine openalex

Environment:
    ANTHROPIC_API_KEY or OPENAI_API_KEY must be set.
    S2_API_KEY (optional) for Semantic Scholar.
"""

import argparse
import json
import os
import sys
import time

import backoff
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llm_utils import get_client_and_model, call_llm_multi_turn, extract_json_between_markers

S2_API_KEY = os.getenv("S2_API_KEY")


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
                "fields": "title,authors,venue,year,abstract,citationCount,url",
            },
        )
        rsp.raise_for_status()
        results = rsp.json()
        time.sleep(1.0)
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
            authors = ", ".join(authors_list[:5])
            if len(authors_list) > 5:
                authors += " et al."
            papers.append({
                "title": work.get("title", ""),
                "authors": authors,
                "venue": venue,
                "year": work.get("publication_year"),
                "abstract": (work.get("abstract") or "")[:800],
                "citationCount": work.get("cited_by_count", 0),
                "url": work.get("doi", "") or "",
            })
        return papers

    else:
        raise ValueError(f"Unknown engine: {engine}")


CITATION_SYSTEM_PROMPT = """You are an academic researcher reviewing a paper draft to identify missing citations.
Your job is to find the most important papers that should be cited but are not yet referenced.

Focus on:
- Claims that need supporting evidence
- Related work that should be acknowledged
- Foundational papers in the field being discussed
- Competing or complementary approaches

Do NOT suggest citing papers that are already referenced in the draft.
You will be given {total_rounds} rounds to add citations, but you can stop early.
Aim for quality over quantity. Each suggestion should be well-justified."""

CITATION_FIRST_PROMPT = """Round {current_round}/{total_rounds}.

Here is the paper draft:
\"\"\"
{draft}
\"\"\"

Identify the most important citation that is still missing from this paper.

Respond in the following format:

THOUGHT:
<THOUGHT>

RESPONSE:
```json
<JSON>
```

In <THOUGHT>, reason about where citations are needed and what kind of paper would fill the gap.
If no more citations are needed, write "No more citations needed" in your thoughts.

In <JSON>, respond with:
- "Location": The specific section and sentence where the citation should be added.
- "Reason": Why this citation is needed.
- "Query": A search query to find the paper (e.g. the paper title or key terms).

This JSON will be automatically parsed, so ensure the format is precise."""

CITATION_SELECT_PROMPT = """The search returned these papers:

{papers}

Respond in the following format:

THOUGHT:
<THOUGHT>

RESPONSE:
```json
<JSON>
```

In <THOUGHT>, evaluate which paper(s) are most relevant to the citation gap you identified.
If none are appropriate, write "None appropriate" in your thoughts.

In <JSON>, respond with:
- "Selected": Index of the best matching paper (e.g. 0, 1, 2...), or -1 if none are appropriate.
- "Citation_Text": The suggested Markdown citation text, formatted as: Author(s) (Year). "Title." *Venue*. [URL](URL)
- "Integration": Exactly how to integrate this citation into the paper text. Include the sentence with the citation added."""


def find_citations(draft, client, model, provider, max_rounds=10, engine="semanticscholar"):
    """
    Iteratively find and suggest citations for a paper draft.
    Returns a list of citation suggestions.
    """
    system_msg = CITATION_SYSTEM_PROMPT.format(total_rounds=max_rounds)
    suggestions = []

    for round_num in range(1, max_rounds + 1):
        print(f"\n  Round {round_num}/{max_rounds}...")

        # Step 1: Identify what citation is needed
        messages = [{"role": "user", "content": CITATION_FIRST_PROMPT.format(
            current_round=round_num,
            total_rounds=max_rounds,
            draft=draft,
        )}]

        try:
            response = call_llm_multi_turn(client, model, provider, system_msg, messages)

            if "no more citations needed" in response.lower():
                print("  No more citations needed.")
                break

            json_output = extract_json_between_markers(response)
            if json_output is None:
                print("  Failed to parse response, skipping round.")
                continue

            query = json_output.get("Query", "")
            location = json_output.get("Location", "")
            reason = json_output.get("Reason", "")

            if not query:
                continue

            print(f"  Searching: '{query}'")

            # Step 2: Search for papers
            papers = search_papers(query, result_limit=10, engine=engine)
            if papers is None:
                print("  No papers found.")
                continue

            # Format papers for LLM
            paper_strings = []
            for i, paper in enumerate(papers):
                authors = paper.get("authors", "Unknown")
                if isinstance(authors, list):
                    authors = ", ".join(a.get("name", str(a)) for a in authors[:3])
                paper_strings.append(
                    f"{i}: {paper['title']}\n"
                    f"   Authors: {authors}\n"
                    f"   Venue: {paper.get('venue', 'Unknown')}, {paper.get('year', '?')}\n"
                    f"   Citations: {paper.get('citationCount', 0)}\n"
                    f"   Abstract: {paper.get('abstract', 'N/A')[:300]}"
                )
            papers_str = "\n\n".join(paper_strings)

            # Step 3: Select the best paper
            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "user", "content": CITATION_SELECT_PROMPT.format(papers=papers_str)})

            response2 = call_llm_multi_turn(client, model, provider, system_msg, messages)

            if "none appropriate" in response2.lower():
                print("  No appropriate paper found.")
                continue

            json_output2 = extract_json_between_markers(response2)
            if json_output2 is None:
                continue

            selected_idx = json_output2.get("Selected", -1)
            if selected_idx < 0 or selected_idx >= len(papers):
                continue

            selected_paper = papers[selected_idx]
            suggestion = {
                "location": location,
                "reason": reason,
                "paper": {
                    "title": selected_paper.get("title", ""),
                    "authors": selected_paper.get("authors", ""),
                    "year": selected_paper.get("year", ""),
                    "venue": selected_paper.get("venue", ""),
                    "url": selected_paper.get("url", ""),
                    "citations": selected_paper.get("citationCount", 0),
                },
                "citation_text": json_output2.get("Citation_Text", ""),
                "integration": json_output2.get("Integration", ""),
            }
            suggestions.append(suggestion)
            print(f"  Found: {selected_paper['title']} ({selected_paper.get('year', '?')})")

        except Exception as e:
            print(f"  Error in round {round_num}: {e}")
            continue

    return suggestions


def print_suggestions(suggestions):
    """Pretty-print citation suggestions."""
    print("\n" + "=" * 70)
    print("  CITATION SUGGESTIONS")
    print("=" * 70)

    if not suggestions:
        print("\n  No citations to suggest.")
        print("=" * 70)
        return

    print(f"\n  Found {len(suggestions)} citation(s) to add:\n")

    for i, s in enumerate(suggestions, 1):
        print(f"  {'─' * 60}")
        print(f"  Citation {i}:")
        print(f"    Paper: {s['paper']['title']} ({s['paper'].get('year', '?')})")
        print(f"    Venue: {s['paper'].get('venue', 'Unknown')}")
        print(f"    Citations: {s['paper'].get('citations', 0)}")
        print(f"    Where: {s['location']}")
        print(f"    Why: {s['reason']}")
        if s.get("citation_text"):
            print(f"    Reference: {s['citation_text']}")
        if s.get("integration"):
            print(f"    Integration: {s['integration']}")
        print()

    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Find missing citations for a research paper draft.",
        epilog="Example: python scripts/find_citations.py papers/my_paper.md",
    )
    parser.add_argument("paper", help="Path to paper .md file")
    parser.add_argument(
        "--rounds", type=int, default=10,
        help="Maximum number of citation search rounds (default: 10)",
    )
    parser.add_argument(
        "--engine", type=str, default="semanticscholar",
        choices=["semanticscholar", "openalex"],
        help="Search engine to use (default: semanticscholar)",
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="Save suggestions JSON to this file",
    )
    args = parser.parse_args()

    if not os.path.exists(args.paper):
        print(f"Error: File not found: {args.paper}")
        sys.exit(1)

    with open(args.paper, "r", encoding="utf-8") as f:
        draft = f.read()

    print(f"Analyzing paper: {args.paper}")
    print(f"Paper length: {len(draft)} characters")

    client, model, provider = get_client_and_model()
    print(f"Using model: {model} ({provider})")
    print(f"Search engine: {args.engine}")

    suggestions = find_citations(
        draft, client, model, provider,
        max_rounds=args.rounds,
        engine=args.engine,
    )

    print_suggestions(suggestions)

    # Save results
    output_path = args.output
    if not output_path:
        base = os.path.splitext(args.paper)[0]
        output_path = f"{base}_citations.json"

    with open(output_path, "w") as f:
        json.dump(suggestions, f, indent=2)
    print(f"Suggestions saved to: {output_path}")


if __name__ == "__main__":
    main()
