import os
import json
import hashlib

from datetime import datetime
from pathlib import Path
from slugify import slugify
from scrapy.exceptions import DropItem

from edscrapers.cli import logger


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        Path(f"./output/scrapers/{spider.name}").mkdir(parents=True, exist_ok=True)

    def close_spider(self, spider):
        pass

    def process_item(self, dataset, spider):

        slug = slugify('-'.join(dataset['source_url'].split('/')[3:]))[:100] # restrict slug to 100 characters
        hashed_url = hashlib.md5(dataset['source_url'].encode('utf-8')).hexdigest()
        hashed_name = hashlib.md5(dataset['name'].encode('utf-8')).hexdigest()
        file_name = f"{slug}-{hashed_url}-{hashed_name}.json"
        file_path = f"./output/scrapers/{spider.name}/{file_name}"
        self._log(dataset)
        logger.debug(f"Dumping to {file_path}")
        with open(file_path, 'w') as output:
            output.write(dataset.toJSON())

    def _log(self, d):
        logger.info("==================================================================================================")
        logger.success(f"{d['source_url']}")
        logger.info(f"Title: {d['title']}")
        logger.debug(f"Description: {d['notes']}")
        logger.debug(f"Name:{d['name']}")
        logger.info(f"Resources: {len(d['resources'])}")
        for r in d['resources']:
            logger.debug(f"\t{r['url']} > {r['name']}")



class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate dataset found: %s" % item)
        else:
            self.ids_seen.add(item['source_url'])
            return item
