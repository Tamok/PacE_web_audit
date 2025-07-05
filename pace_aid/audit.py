"""Auditing utilities for pages."""

from __future__ import annotations

import re
from typing import List, Tuple

from bs4 import BeautifulSoup
from wcag_contrast_ratio import rgb

from .indexer import Page
from .openai_utils import summarize_text
from .brand import BRAND_COLORS, LOGO_URLS


def _hex_to_rgb(value: str) -> Tuple[float, float, float]:
    value = value.lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    r = int(value[0:2], 16) / 255.0
    g = int(value[2:4], 16) / 255.0
    b = int(value[4:6], 16) / 255.0
    return r, g, b


def check_layout(page: Page) -> bool:
    """Check that header and footer exist."""
    soup = BeautifulSoup(page.html, "html.parser")
    return bool(soup.find("header") and soup.find("footer"))


def check_alt_text(page: Page) -> bool:
    soup = BeautifulSoup(page.html, "html.parser")
    images = soup.find_all("img")
    return all(img.has_attr("alt") and img["alt"].strip() for img in images)


def check_headings(page: Page) -> bool:
    """Ensure exactly one H1 heading is present."""
    soup = BeautifulSoup(page.html, "html.parser")
    h1s = soup.find_all("h1")
    return len(h1s) == 1


def check_brand_colors(page: Page) -> bool:
    soup = BeautifulSoup(page.html, "html.parser")
    colors_in_page = set()
    for tag in soup.find_all(style=True):
        styles = tag["style"].split(";")
        for style in styles:
            if "color" in style or "background" in style:
                match = re.search(r"#(?:[0-9a-fA-F]{3}){1,2}", style)
                if match:
                    colors_in_page.add(match.group(0).lower())
    return bool(colors_in_page & {c.lower() for c in BRAND_COLORS})


def check_contrast(page: Page) -> bool:
    soup = BeautifulSoup(page.html, "html.parser")
    for tag in soup.find_all(style=True):
        fg_match = re.search(r"color:\s*(#[0-9a-fA-F]{6})", tag["style"])
        bg_match = re.search(r"background(?:-color)?:\s*(#[0-9a-fA-F]{6})", tag["style"])
        if fg_match and bg_match:
            fg = _hex_to_rgb(fg_match.group(1))
            bg = _hex_to_rgb(bg_match.group(1))
            ratio = rgb(fg, bg)
            if ratio < 4.5:
                return False
    return True


def check_logos(page: Page) -> bool:
    """Ensure any logo images use approved sources."""
    soup = BeautifulSoup(page.html, "html.parser")
    logos = [img["src"] for img in soup.find_all("img", src=True) if "logo" in img["src"].lower()]
    if not logos:
        return True
    for src in logos:
        if not any(src.startswith(url) for url in LOGO_URLS):
            return False
    return True


def check_meta_description(page: Page) -> bool:
    """Ensure page has a meta description tag."""
    soup = BeautifulSoup(page.html, "html.parser")
    tag = soup.find("meta", attrs={"name": "description"})
    return bool(tag and tag.get("content"))


def summarize(page: Page) -> str:
    return summarize_text(page.text)


def run_audits(page: Page) -> List[str]:
    """Run all audits and return list of failed checks."""
    failures: List[str] = []
    if not check_layout(page):
        failures.append("layout")
    if not check_alt_text(page):
        failures.append("alt_text")
    if not check_headings(page):
        failures.append("headings")
    if not check_brand_colors(page):
        failures.append("brand_colors")
    if not check_contrast(page):
        failures.append("contrast")
    if not check_logos(page):
        failures.append("logos")
    if not check_meta_description(page):
        failures.append("meta_description")
    return failures
