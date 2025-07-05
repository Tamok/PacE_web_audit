"""Website crawler used to fetch and index pages."""

from __future__ import annotations

import re
from collections import deque
from dataclasses import dataclass
from typing import Iterable, Optional, Set
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from .config import SiteConfig
from .indexer import Index, Page


@dataclass
class Crawler:
    site: SiteConfig
    index: Index
    visited: Set[str] = None

    def __post_init__(self) -> None:
        if self.visited is None:
            self.visited = set()

    def crawl(self, limit: Optional[int] = None) -> None:
        """Crawl pages starting from the site's root URL."""
        queue = deque([self.site.url])
        while queue:
            url = queue.popleft()
            if url in self.visited:
                continue
            self.visited.add(url)
            try:
                resp = requests.get(url, timeout=10)
                resp.raise_for_status()
            except requests.RequestException:
                continue
            soup = BeautifulSoup(resp.text, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            page = Page(url=url, html=resp.text, text=text, category=self.site.category)
            self.index.add_page(page)
            if limit and len(self.visited) >= limit:
                break
            for link in self._extract_links(soup, url):
                if link not in self.visited:
                    queue.append(link)

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> Iterable[str]:
        domain = urlparse(self.site.url).netloc
        for a in soup.find_all("a", href=True):
            href = a["href"]
            href = urljoin(base_url, href)
            parsed = urlparse(href)
            if parsed.netloc != domain:
                continue
            if re.match(r"^mailto:|^tel:", href):
                continue
            yield href
