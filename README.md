# PacE Web Audit

PacE AID (Artificial Intelligence Dean) crawls the three PaCE domains and indexes every page. It validates layout, brand voice and accessibility using safe, modern libraries. The project is modular, thoroughly tested and intended for internal use only.

## Features
- **Crawling targets**
  - https://www.professional.ucsb.edu/ (Website)
  - https://enroll.professional.ucsb.edu/ (Course Pages)
  - https://help.professional.ucsb.edu/ (Help Desk)
- Parse and index the Website, Course Pages and Help Desk domains.
- Validate layout consistency, brand voice and ADA compliance.
- Ensure approved brand colors and logos are used. Inline SVG logos with data URIs are accepted.
- Check that each page includes one H1 heading and a meta description tag.
- Optional OpenAI integration for AI-assisted checks such as summarization.
- Output JSON data and a live HTML dashboard summarizing audit results.

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
