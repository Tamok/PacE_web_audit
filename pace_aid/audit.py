"""Auditing utilities for pages."""

from __future__ import annotations

import re
from typing import List, Tuple

from bs4 import BeautifulSoup
from wcag_contrast_ratio import rgb

from .indexer import Page
from .openai_utils import summarize_text

# Example brand colors (hex) from the provided spreadsheet
BRAND_COLORS = {
    "#003660",  # UCSB blue
    "#FFCD00",  # yellow
    "#FFFFFF",  # white
}


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


def summarize(page: Page) -> str:
    return summarize_text(page.text)


def run_audits(page: Page) -> List[str]:
    """Run all audits and return list of failed checks."""
    failures: List[str] = []
    if not check_layout(page):
        failures.append("layout")
    if not check_alt_text(page):
        failures.append("alt_text")
    if not check_brand_colors(page):
        failures.append("brand_colors")
    if not check_contrast(page):
        failures.append("contrast")
    return failures
