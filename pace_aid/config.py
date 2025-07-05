"""Configuration for the PacE AID tool."""

from dataclasses import dataclass
from typing import List

@dataclass
class SiteConfig:
    url: str
    category: str

# Default configuration for the three domains
DEFAULT_SITES: List[SiteConfig] = [
    SiteConfig(url="https://www.professional.ucsb.edu/", category="Website"),
    SiteConfig(url="https://enroll.professional.ucsb.edu/", category="Course Pages"),
    SiteConfig(url="https://help.professional.ucsb.edu/", category="Help Desk"),
]
