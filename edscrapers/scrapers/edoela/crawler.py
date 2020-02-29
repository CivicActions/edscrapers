from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor
from edscrapers.scrapers.edoela.parser import parse

class Crawler(CrawlSpider):

    name = 'edoela'
    allowed_regex = r'oela|ncela'
    allowed_domains = ['ed.gov']

    def __init__(self, conf=None):

        self.conf = conf

        self.start_urls = [
            'https://www2.ed.gov/about/offices/list/oela/index.html'
        ]

        # Make rules
        self.rules = [
            Rule(LinkExtractor(
                allow=self.allowed_regex,
                deny='.*(xls|xlsx|csv|zip|pdf|doc|docx)',
                #restrict_xpaths='//div[@id="maincontent"]'
            ), callback=parse, follow=True),
        ]


        # Inherit parent
        super(Crawler, self).__init__()