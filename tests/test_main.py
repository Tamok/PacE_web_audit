from pathlib import Path
from pace_aid.main import write_dashboard


def test_write_dashboard(tmp_path: Path) -> None:
    data = {
        "https://example.com": {
            "category": "Website",
            "summary": "Summary",
            "failures": ["layout"],
        }
    }
    out = tmp_path / "dash.html"
    write_dashboard(data, out)
    html = out.read_text()
    assert "<table" in html
    assert "https://example.com" in html

