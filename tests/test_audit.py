from pace_aid.indexer import Page
from pace_aid import audit

SIMPLE_HTML = """
<html>
  <head><meta name='description' content='desc'></meta></head>
  <header></header>
  <body>
    <h1>Title</h1>
    <img src='https://www.professional.ucsb.edu/sites/default/files/2025-05/Logo_PaCE_2025_Full.png' alt='desc'>
    <div style='color:#FFFFFF;background:#003660'>Text</div>
  </body>
  <footer></footer>
</html>
"""

page = Page(url='https://example.com', html=SIMPLE_HTML, text='Text', category='Website')

def test_run_audits(monkeypatch):
    monkeypatch.setattr(audit, "check_brand_voice", lambda page: True)
    assert audit.run_audits(page) == []


def test_headings_check_fails():
    html = SIMPLE_HTML.replace('<h1>Title</h1>', '')
    bad_page = Page(url='https://bad.com', html=html, text='Text', category='Website')
    assert 'headings' in audit.run_audits(bad_page)


def test_meta_description_missing():
    html = SIMPLE_HTML.replace("<meta name='description' content='desc'></meta>", '')
    bad_page = Page(url='https://bad.com', html=html, text='Text', category='Website')
    assert 'meta_description' in audit.run_audits(bad_page)


def test_logo_check_fails():
    html = SIMPLE_HTML.replace('Logo_PaCE_2025_Full.png', 'bad_logo.png')
    bad_page = Page(url='https://bad.com', html=html, text='Text', category='Website')
    assert 'logos' in audit.run_audits(bad_page)


def test_logo_inline_svg_passes():
    svg_html = SIMPLE_HTML.replace(
        "<img src='https://www.professional.ucsb.edu/sites/default/files/2025-05/Logo_PaCE_2025_Full.png' alt='desc'>",
        "<svg class='logo'><image xlink:href='data:image/svg+xml;base64,AAAA'/></svg>"
    )
    svg_page = Page(url='https://example.com', html=svg_html, text='Text', category='Website')
    assert 'logos' not in audit.run_audits(svg_page)


def test_brand_voice_check_fails(monkeypatch):
    def fake_brand_voice_consistent(text: str) -> bool:
        return False

    monkeypatch.setattr(audit, "check_brand_voice", lambda page: fake_brand_voice_consistent(page.text))
    assert 'brand_voice' in audit.run_audits(page)
