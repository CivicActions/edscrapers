# -*- coding: utf-8 -*-
import re
import json
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from edscrapers.scrapers import base
from edscrapers.scrapers.base.models import Dataset
import edscrapers.scrapers.base.helpers as h


deny_list = []

def parse(res):

    # print(res)

    dataset = Dataset()
    dataset.crawler_name = globals()['__package__'].split('.')[-1]

    h.get_all_resources(res, dataset, h.get_data_extensions(), deny_list=deny_list)

    if len(dataset.resources) > 0:

        # We've got resources, so the documents might be relevant to them
        h.get_all_resources(res, dataset, h.get_document_extensions(), deny_list=deny_list)

        dataset.source_url = res.url
        dataset.title = res.xpath('//meta[@name="DC.title"]/@content').get('text')
        if not dataset.title or dataset.title == 'text':
            dataset.title = res.xpath('/html/head/title/text()').get('text')
        dataset.name = h.make_slug(res.url)
        dataset.notes = res.xpath('//meta[@name="DC.description"]/@content').get('text')
        dataset.dump()
        return json.loads(dataset.toJSON())

    return None


