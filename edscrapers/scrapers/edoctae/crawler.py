from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from edscrapers.scrapers.edoctae.parser import parse

class Crawler(CrawlSpider):

    name = 'edoctae'
    allowed_regex = r'www2.ed.gov/about/offices/list/ovae/|sites.ed.gov/octae/'

    def __init__(self, conf=None):

        self.conf = conf

        self.start_urls = [
            'https://www2.ed.gov/about/offices/list/ovae/index.html',
            'https://sites.ed.gov/octae/'
        ]

        # Make rules
        self.rules = [
            Rule(LinkExtractor(
                allow=self.allowed_regex,
            ), callback=parse, follow=True),
        ]

        # Inherit parent
        super(Crawler, self).__init__()