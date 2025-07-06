"""Utility functions for OpenAI integration."""

import os
from typing import Optional

openai: Optional[object]

try:
    import openai
except Exception:  # pragma: no cover - optional dependency
    openai = None  # type: ignore


def _require_openai() -> object:
    """Return the OpenAI module after verifying configuration."""
    if openai is None:
        raise RuntimeError("openai package is not installed")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set")
    openai.api_key = api_key
    return openai


def summarize_text(text: str) -> str:
    """Return a short summary of the given text using OpenAI."""
    oai = _require_openai()
    try:
        resp = oai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Summarize the following text."}, {"role": "user", "content": text[:4000]}],
            max_tokens=60,
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        raise RuntimeError("OpenAI request failed")


def brand_voice_consistent(text: str) -> bool:
    """Return True if text matches the UCSB PaCE brand voice using OpenAI."""
    oai = _require_openai()
    try:
        resp = oai.chat.completions.create(
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
        raise RuntimeError("OpenAI request failed")
