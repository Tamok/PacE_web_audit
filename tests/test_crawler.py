import responses
from pace_aid.crawler import Crawler
from pace_aid.config import SiteConfig
from pace_aid.indexer import Index


@responses.activate
def test_crawl_single_page():
    html = "<html><body><a href='/a'>A</a></body></html>"
    responses.add(responses.GET, 'https://example.com/', body=html, status=200)
    responses.add(responses.GET, 'https://example.com/a', body=html, status=200)

    site = SiteConfig(url='https://example.com/', category='Website')
    index = Index()
    crawler = Crawler(site=site, index=index)
    crawler.crawl(limit=2)

    assert len(index.pages) == 2
