from pace_aid.indexer import Page
from pace_aid import audit

SIMPLE_HTML = """
<html>
  <header></header>
  <body>
    <img src='x.png' alt='desc'>
    <div style='color:#FFFFFF;background:#003660'>Text</div>
  </body>
  <footer></footer>
</html>
"""

page = Page(url='https://example.com', html=SIMPLE_HTML, text='Text', category='Website')

def test_run_audits():
    assert audit.run_audits(page) == []
