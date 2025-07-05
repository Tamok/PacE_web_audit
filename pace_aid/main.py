"""Command line interface for PacE AID."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from typing import Dict, Any

from .config import DEFAULT_SITES
from .crawler import Crawler
from .indexer import Index
from .audit import run_audits, summarize


def write_dashboard(data: Dict[str, Any], out: Path) -> None:
    """Write a simple HTML dashboard summarizing audit results."""
    rows = []
    for url, entry in data.items():
        failures = ", ".join(entry["failures"]) if entry["failures"] else ""
        rows.append(
            f"<tr><td><a href='{url}'>{url}</a></td><td>{entry['category']}</td>"
            f"<td>{failures}</td><td>{entry['summary']}</td></tr>"
        )
    html = (
        "<html><head><title>PacE AID Dashboard</title></head><body>"
        "<h1>PacE AID Report</h1><table border='1'>"
        "<tr><th>URL</th><th>Category</th><th>Failures</th><th>Summary</th></tr>"
        + "".join(rows)
        + "</table></body></html>"
    )
    out.write_text(html)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="PacE AID website auditor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    crawl_p = subparsers.add_parser("crawl", help="Crawl websites")
    crawl_p.add_argument("--limit", type=int, default=20, help="Page limit per site")
    crawl_p.add_argument("--out", type=Path, default=Path("index.json"), help="Output JSON file")
    crawl_p.add_argument("--dashboard", type=Path, help="Optional HTML dashboard output")

    args = parser.parse_args(argv)

    if args.command == "crawl":
        index = Index()
        for site in DEFAULT_SITES:
            crawler = Crawler(site=site, index=index)
            crawler.crawl(limit=args.limit)
        data = {
            url: {
                "category": p.category,
                "summary": summarize(p),
                "failures": run_audits(p),
            }
            for url, p in index.pages.items()
        }
        args.out.write_text(json.dumps(data, indent=2))
        print(f"Wrote results to {args.out}")
        if args.dashboard:
            write_dashboard(data, args.dashboard)
            print(f"Wrote dashboard to {args.dashboard}")

if __name__ == "__main__":  # pragma: no cover
    main()
