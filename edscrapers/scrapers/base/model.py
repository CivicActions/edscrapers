import os
import json
import hashlib
from pathlib import Path
import edscrapers.scrapers.base.helpers as h

class Model():

    crawler_name = 'default'

    def before_dump(self):
        pass

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=2)

    def dump(self):
        self.before_dump()
        crawler_name = getattr(self, 'crawler_name', 'default')
        self._setup_output(crawler_name)

        slug = h.make_slug(self.source_url)[:100] # restrict slug to 100 characters
        hashed = hashlib.md5(self.source_url.encode('utf-8')).hexdigest()
        file_name = "{}-{}.json".format(slug, hashed)
        file_path = './output/{}/{}'.format(crawler_name, file_name)
        print('Dumping to {}'.format(file_path))
        with open(file_path, 'w') as output:
            output.write(self.toJSON())

    def _setup_output(self, crawler_name):
        # Prepare output directory
        Path("./output/{}".format(crawler_name)).mkdir(parents=True, exist_ok=True)
