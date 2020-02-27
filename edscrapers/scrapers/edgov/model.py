# -*- coding: utf-8 -*-
import json
from edscrapers.scrapers import base
from edscrapers.scrapers.base.model import Model as BaseModel


class Dataset(BaseModel):

    crawler_name = 'edgov'

    def __init__(self, title=None, name=None, notes=None, source_url=None):
        setattr(self, 'title', title)
        setattr(self, 'name', name)
        setattr(self, 'notes', notes)
        setattr(self, 'source_url', source_url)
        setattr(self, 'resources', [])

    def add_resource(self, resource):
        r = Resource(name=resource.get('name', ''),
                     url=resource.get('url', ''),
                     source_url=resource.get('source_url'))
        self.resources.append(r)

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


class Resource(BaseModel):

    def __init__(self, name=None, url=None, source_url=None):
        setattr(self, 'name', name)
        setattr(self, 'url', url)
        setattr(self, 'source_url', source_url)
