import os
import json
import hashlib
from pathlib import Path
import edscrapers.scrapers.base.helpers as h

class Dataset():

    crawler_name = 'default'

    def __init__(self, title=None, name=None, notes=None, source_url=None):
        setattr(self, 'title', title)
        setattr(self, 'name', name)
        setattr(self, 'notes', notes)
        setattr(self, 'source_url', source_url)
        setattr(self, 'resources', [])

    def before_dump(self):
        print('==================================================================================================')
        print('{}\nTitle: {}\nDescription: {}\nName:{}'.format(self.source_url, self.title, self.notes, self.name))
        print('Resources ({}):'.format(len(self.resources)))
        for r in self.resources:
            print('\t{} > {}'.format(r.url,
                                   r.name,
                                   r.source_url))
            with open(f'{self.crawler_name}.log', 'a') as log_file:
                log_file.write(f'{r.url}\n')

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


class Resource():

    def __init__(self, name=None, url=None, source_url=None, description=None):
        setattr(self, 'name', name)
        setattr(self, 'url', url)
        setattr(self, 'source_url', source_url)
        setattr(self, 'description', description)
