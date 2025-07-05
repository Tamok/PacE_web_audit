"""Simple in-memory index used for storing crawled pages."""

from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Page:
    url: str
    html: str
    text: str
    category: str

@dataclass
class Index:
    pages: Dict[str, Page] = field(default_factory=dict)

    def add_page(self, page: Page) -> None:
        self.pages[page.url] = page

    def get_pages(self) -> List[Page]:
        return list(self.pages.values())
