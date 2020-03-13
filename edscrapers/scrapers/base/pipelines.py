import os
import json
import hashlib

from datetime import datetime
from pathlib import Path
from slugify import slugify
from scrapy.exceptions import DropItem


class JsonWriterPipeline(object):

    log_file = None

    def open_spider(self, spider):
        Path(f"./output/{spider.name}").mkdir(parents=True, exist_ok=True)
        Path(f"./output/log").mkdir(exist_ok=True)
        self.log_file = Path(f"./output/log/{spider.name}-{datetime.now().isoformat()}.log")

    def close_spider(self, spider):
        pass

    def process_item(self, dataset, spider):

        slug = slugify('-'.join(dataset['source_url'].split('/')[3:]))[:100] # restrict slug to 100 characters
        hashed_url = hashlib.md5(dataset['source_url'].encode('utf-8')).hexdigest()
        hashed_name = hashlib.md5(dataset['name'].encode('utf-8')).hexdigest()
        file_name = f"{slug}-{hashed_url}-{hashed_name}.json"
        file_path = f"./output/{spider.name}/{file_name}"
        self._print(dataset)
        print(f"Dumping to {file_path}")
        with open(file_path, 'w') as output:
            output.write(dataset.toJSON())

        with open(self.log_file, "a") as log_file:
            for r in dataset["resources"]:
                log_file.write(f"{r['url']}\n")

    def _print(self, d):
        print("==================================================================================================")
        print(f"{d['source_url']}\nTitle: {d['title']}\nDescription: {d['notes']}\nName:{d['name']}")
        print(f"Resources ({len(d['resources'])}):")
        for r in d['resources']:
            print(f"\t{r['url']} > {r['name']}")



class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate dataset found: %s" % item)
        else:
            self.ids_seen.add(item['source_url'])
            return item
