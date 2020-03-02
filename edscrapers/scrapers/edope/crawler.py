from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from edscrapers.scrapers.edope.parser import parse

class Crawler(CrawlSpider):

    name = 'edope'
    allowed_regex = r'ope/'

    def __init__(self, conf=None):

        self.conf = conf

        self.start_urls = [
            'https://www2.ed.gov/about/offices/list/ope/index.html',
            'https://www2.ed.gov/about/offices/list/ope/idues/eligibility.html',
        ]

        # Make rules
        self.rules = [
            Rule(LinkExtractor(
                allow=self.allowed_regex,
                deny='.*(xls|xlsx|csv|zip|pdf|doc|docx)',
                restrict_xpaths='//*[@id="maincontent"]'
            ), callback=parse, follow=True),
        ]

        # Inherit parent
        super(Crawler, self).__init__()


    