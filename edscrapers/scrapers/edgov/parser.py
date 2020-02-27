# -*- coding: utf-8 -*-
import re
import json
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from edscrapers.scrapers import base
from edscrapers.scrapers.edgov.model import Dataset
import edscrapers.scrapers.base.helpers as h

extensions = {
    '.xlsx': 'Excel spreadsheet',
    '.xls': 'Excel spreadsheet',
    # '.pdf': 'PDF file',
    '.zip': 'ZIP archive',
    '.csv': 'CSV file',
    # '.doc': 'Word document',
    # '.docx': 'Word document'
}

def parse(res):

    # print(res)

    dataset = Dataset()

    for link in LxmlLinkExtractor(deny_extensions=[]).extract_links(res):
        for extension in extensions.keys():
            if link.url.endswith(extension):
                resource = {
                    'source_url': res.url,
                    'url': link.url,
                    'name': link.text,
                }
                dataset.add_resource(resource)

    if len(dataset.resources) > 0:
        dataset.source_url = res.url
        dataset.title = res.xpath('//meta[@name="DC.title"]/@content').get('text')
        if not dataset.title or dataset.title == 'text':
            dataset.title = res.xpath('/html/head/title/text()').get('text')
        dataset.name = h.make_slug(res.url)
        dataset.notes = res.xpath('//meta[@name="DC.description"]/@content').get('text')
        dataset.dump()
        return json.loads(dataset.toJSON())

    return None

