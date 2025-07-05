from pace_aid.indexer import Page
from pace_aid import audit

SIMPLE_HTML = """
<html>
  <head><meta name='description' content='desc'></meta></head>
  <header></header>
  <body>
    <h1>Title</h1>
    <img src='x.png' alt='desc'>
    <div style='color:#FFFFFF;background:#003660'>Text</div>
  </body>
  <footer></footer>
</html>
"""

page = Page(url='https://example.com', html=SIMPLE_HTML, text='Text', category='Website')

def test_run_audits():
    assert audit.run_audits(page) == []


def test_headings_check_fails():
    html = SIMPLE_HTML.replace('<h1>Title</h1>', '')
    bad_page = Page(url='https://bad.com', html=html, text='Text', category='Website')
    assert 'headings' in audit.run_audits(bad_page)


def test_meta_description_missing():
    html = SIMPLE_HTML.replace("<meta name='description' content='desc'></meta>", '')
    bad_page = Page(url='https://bad.com', html=html, text='Text', category='Website')
    assert 'meta_description' in audit.run_audits(bad_page)
