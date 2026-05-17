"""
Shared LLM utilities for the research-paper-framework scripts.
Supports OpenAI and Anthropic APIs via environment variables.
"""

import json
import os
import re
import sys


def get_client_and_model():
    """
    Auto-detect which API to use based on available environment variables.
    Returns (client, model_name, provider) tuple.

    Priority: ANTHROPIC_API_KEY > OPENAI_API_KEY
    Override with REVIEW_MODEL env var (e.g. "gpt-4o", "claude-sonnet-4-20250514").
    """
    model_override = os.getenv("REVIEW_MODEL")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")

    if anthropic_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=anthropic_key)
            model = model_override or "claude-sonnet-4-20250514"
            return client, model, "anthropic"
        except ImportError:
            print("Warning: anthropic package not installed. pip install anthropic")

    if openai_key:
        try:
            import openai
            client = openai.OpenAI(api_key=openai_key)
            model = model_override or "gpt-4o"
            return client, model, "openai"
        except ImportError:
            print("Warning: openai package not installed. pip install openai")

    print("Error: No API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY.")
    sys.exit(1)


def call_llm(client, model, provider, system_message, user_message, temperature=0.7):
    """
    Send a message to the LLM and return the response text.
    Works with both OpenAI and Anthropic APIs.
    """
    if provider == "anthropic":
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            temperature=temperature,
            system=system_message,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text

    elif provider == "openai":
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content

    else:
        raise ValueError(f"Unknown provider: {provider}")


def call_llm_multi_turn(client, model, provider, system_message, messages, temperature=0.7):
    """
    Send a multi-turn conversation to the LLM.
    messages: list of {"role": "user"|"assistant", "content": "..."}
    Returns the response text.
    """
    if provider == "anthropic":
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            temperature=temperature,
            system=system_message,
            messages=messages,
        )
        return response.content[0].text

    elif provider == "openai":
        full_messages = [{"role": "system", "content": system_message}] + messages
        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=full_messages,
        )
        return response.choices[0].message.content

    else:
        raise ValueError(f"Unknown provider: {provider}")


def extract_json_between_markers(text):
    """
    Extract JSON from text that contains ```json ... ``` markers.
    Returns parsed JSON dict or None.
    """
    pattern = r"```json\s*(.*?)\s*```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            return None
    return None
