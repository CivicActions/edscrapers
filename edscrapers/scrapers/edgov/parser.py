# -*- coding: utf-8 -*-
import re
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from .. import base
from .model import Model


extensions = {
    'xls': 'Excel',
    'pdf': 'PDF',
    'zip': 'ZIP',
    'csv': 'CSV',
}


def parse(res):

    if 'finaid' in res.url:
        print('FINAID!!')
    #     import ipdb; ipdb.set_trace()

    # print('=======================================================================')
    print(res)
    # print('=======================================================================')

    dataset = Model()

    with open('edgov.log', 'a') as result_log:
        for link in LxmlLinkExtractor(allow=()).extract_links(res):
            for extension in extensions.keys():
                if link.url.endswith(extension):
                    resource = {
                        'url': link.url,
                        'name': link.text,
                    }
                    dataset.add_resource(resource)
                    print('{} file: {}'.format(extensions[extension], item.url))
                    result_log.write('{}\n'.format(item.url))

    if len(dataset.resources):
        dataset.source_url = res.url
        dataset.title = res.xpath('/html/head/meta[@name="title"]/@content')
        dataset.dump()
        return dataset

    return None

