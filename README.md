# PacE Web Audit

PacE AID (Artificial Intelligence Dean) is a tool for crawling and auditing the UCSB Professional and Continuing Education websites.

## Features
- Crawl and index pages from the following domains:
  - https://www.professional.ucsb.edu/
  - https://help.professional.ucsb.edu/
  - https://enroll.professional.ucsb.edu/
- Validate layout consistency, branding, language, and ADA compliance.
- Optional OpenAI integration for AI-assisted checks.

## Usage
Install dependencies and run the audit:
```bash
pip install -e .[test]
pace-aid crawl --limit 10
```

## Tests
Run unit tests using `pytest`:
```bash
pytest
```

## License
Internal use only.
