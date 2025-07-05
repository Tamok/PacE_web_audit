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
