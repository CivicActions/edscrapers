from scrapy.crawler import CrawlerProcess
from edscrapers.scrapers.edope.crawler import Crawler

def scrape(conf):
    process = CrawlerProcess(conf['SCRAPY_SETTINGS'])
    process.crawl(Crawler)
    process.start()