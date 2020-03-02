# -*- coding: utf-8 -*-
import os
import logging
import logging.config
from dotenv import load_dotenv
load_dotenv('.env')


# Scrapy

SCRAPY_SETTINGS = {
    'SPIDER_MODULES': [
        'edscrapers.scrapers.edgov.crawler',
        'edscrapers.scrapers.ocr.crawler',
    ],
    'DOWNLOAD_DELAY': float(os.getenv('DOWNLOAD_DELAY', 1)),
    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware': 1,
        'edscrapers.scrapers.base.middlewares.RegexOffsiteMiddleware': 2,
        'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': 3,
    },
    'ITEM_PIPELINES': {
        'edscrapers.scrapers.base.pipelines.JsonWriterPipeline': 1,
    },
    'SCHEDULER_PRIORITY_QUEUE': 'scrapy.pqueues.DownloaderAwarePriorityQueue',
    # 'REDIRECT_ENABLED': False,
    'RETRY_ENABLED': False,
    'COOKIES_ENABLED': False,
    'HTTPCACHE_ENABLED': True,
    'AUTOTHROTTLE_ENABLED': True,
    'LOG_LEVEL': 'INFO',
}
