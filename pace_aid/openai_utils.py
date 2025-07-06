"""Utility functions for OpenAI integration."""

import os
from typing import Optional

try:
    import openai
except Exception:  # pragma: no cover - optional dependency
    openai = None  # type: ignore


def summarize_text(text: str) -> str:
    """Return a short summary of the given text using OpenAI if API key is set."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not openai:
        return ""
    openai.api_key = api_key
    try:
        resp = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Summarize the following text."}, {"role": "user", "content": text[:4000]}],
            max_tokens=60,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return ""


def brand_voice_consistent(text: str) -> bool:
    """Return True if text matches the UCSB PaCE brand voice using OpenAI."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not openai:
        return True
    openai.api_key = api_key
    try:
        resp = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You check if the following text matches the UCSB PaCE brand voice."
                        " Reply with 'Yes' or 'No' only."
                    ),
                },
                {"role": "user", "content": text[:4000]},
            ],
            max_tokens=1,
            temperature=0,
        )
        answer = resp.choices[0].message.content.strip().lower()
        return answer.startswith("y")
    except Exception:
        return True
