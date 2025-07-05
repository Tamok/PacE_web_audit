# PacE Web Audit

PacE AID (Artificial Intelligence Dean) is a tool for crawling and auditing the UCSB Professional and Continuing Education websites. It indexes pages from the three PaCE domains and evaluates them for branding and compliance issues using reliable, well-tested libraries. The goal is a modular, transparent system suitable for internal use.

## Features
- **Crawling targets**
  - https://www.professional.ucsb.edu/ (Website)
  - https://enroll.professional.ucsb.edu/ (Course Pages)
  - https://help.professional.ucsb.edu/ (Help Desk)
- Validate layout consistency, branding, language, and ADA compliance.
- Check that pages include a single top-level heading, a meta description tag, and approved logos.
- Optional OpenAI integration for AI-assisted checks.
- Output a live HTML dashboard summarizing audit results.

## Usage
Install dependencies and run the audit:
```bash
pip install -e .[test]
pace-aid crawl --limit 10 --dashboard report.html
```

## Tests
Run unit tests using `pytest`:
```bash
pytest
```

## License
Internal use only.

## Project roadmap

### Current features
- Crawl specified PaCE domains and build an index
- Validate layout, alt text, headings, meta descriptions, brand colors, logo usage, and contrast
- Summarize page text with optional OpenAI integration
- Export results to JSON and an HTML dashboard

### Most important feature
Automated auditing of every PaCE page to ensure branding and accessibility compliance.

### MVP criteria
- Crawl all three domains
- Perform the set of audits listed above
- Generate JSON and dashboard outputs
- Provide a test suite and CI workflow

### Next steps
- Expand brand checks using the official spreadsheet
- Integrate additional compliance policies from UCSB PaCE
- Improve dashboard visualizations
