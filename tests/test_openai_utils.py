import types
import pytest
from pace_aid import openai_utils


def test_require_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        openai_utils.summarize_text("text")


def test_summarize(monkeypatch):
    class FakeResp:
        def __init__(self, content):
            self.choices = [types.SimpleNamespace(message=types.SimpleNamespace(content=content))]

    class FakeChat:
        def __init__(self):
            self.completions = types.SimpleNamespace(create=lambda **_: FakeResp("sum"))

    class FakeOpenAI:
        def __init__(self):
            self.chat = FakeChat()
            self.api_key = None

    monkeypatch.setenv("OPENAI_API_KEY", "test")
    monkeypatch.setattr(openai_utils, "openai", FakeOpenAI())
    assert openai_utils.summarize_text("text") == "sum"

