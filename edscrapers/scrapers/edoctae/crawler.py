import re
from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from edscrapers.scrapers.edoctae.parser import parse

class Crawler(CrawlSpider):

    name = 'edoctae'
    allowed_regex = r'ovae/|octae/'
    #|sites.ed.gov/octae/'

    def __init__(self, conf=None):

        self.conf = conf

        self.start_urls = [
            'https://www2.ed.gov/about/offices/list/ovae/index.html',
            'https://www2.ed.gov/about/offices/list/ovae/pi/memoperkinsiv.html',
        ]

        # Make rules
        self.rules = [
            Rule(LinkExtractor(
                allow=self.allowed_regex,
                deny='.*(xls|xlsx|csv|zip|pdf|doc|docx)',
                #restrict_xpaths='//*[@id="maincontent"]',
                process_value=self.process_value
            ), callback=parse, follow=True),
        ]

        # Inherit parent
        super(Crawler, self).__init__()

    def process_value(self, value):
        m = re.search("javascript:goToPage\('(.*?)'", value)
        if m:
            return m.group(1)
        else:
            return value