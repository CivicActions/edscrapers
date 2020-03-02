from scrapy.crawler import CrawlerProcess
from edscrapers.scrapers.edoctae.crawler import Crawler

def scrape(conf):
    process = CrawlerProcess(conf['SCRAPY_SETTINGS'])
    process.crawl(Crawler)
    process.start()
