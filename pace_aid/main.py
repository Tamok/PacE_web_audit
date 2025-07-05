"""Command line interface for PacE AID."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import DEFAULT_SITES
from .crawler import Crawler
from .indexer import Index
from .audit import run_audits, summarize


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="PacE AID website auditor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    crawl_p = subparsers.add_parser("crawl", help="Crawl websites")
    crawl_p.add_argument("--limit", type=int, default=20, help="Page limit per site")
    crawl_p.add_argument("--out", type=Path, default=Path("index.json"), help="Output file")

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

if __name__ == "__main__":  # pragma: no cover
    main()
