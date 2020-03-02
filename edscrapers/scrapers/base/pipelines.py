import os
import json
import hashlib
from datetime import datetime
from pathlib import Path

from slugify import slugify


class JsonWriterPipeline(object):

    log_file = None

    def open_spider(self, spider):
        Path(f"./output/{spider.name}").mkdir(parents=True, exist_ok=True)
        self.log_file = Path(f"./{spider.name}-{datetime.now().isoformat()}.log")

    def close_spider(self, spider):
        pass

    def process_item(self, dataset_dict, spider):

        slug = slugify(dataset_dict['source_url'])[:100] # restrict slug to 100 characters
        hashed = hashlib.md5(dataset_dict['source_url'].encode('utf-8')).hexdigest()
        file_name = f"{slug}-{hashed}.json"
        file_path = f"./output/{spider.name}/{file_name}"
        self._print(dataset_dict)
        print(f"Dumping to {file_path}")
        with open(file_path, 'w') as output:
            output.write(json.dumps(dataset_dict))

        with open(self.log_file, "a") as log_file:
            for r in dataset_dict["resources"]:
                log_file.write(f"{r['url']}\n")

    def _print(self, d):
        print("==================================================================================================")
        print(f"{d['source_url']}\nTitle: {d['title']}\nDescription: {d['notes']}\nName:{d['name']}")
        print(f"Resources ({len(d['resources'])}):")
        for r in d['resources']:
            print(f"\t{r['url']} > {r['name']}")
