import json
import edscrapers.scrapers.base.helpers as h

from edscrapers.scrapers.base.models import Dataset
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

def parse(res):

    print(res)

    dataset = Dataset()
    dataset.crawler_name = globals()['__package__'].split('.')[-1]

    h.get_all_resources(res, dataset, h.get_data_extensions())

    if len(dataset.resources) > 0:
        h.get_all_resources(res, dataset, h.get_document_extensions())

        dataset.source_url = res.url
        dataset.title = res.xpath('//meta[@name="DC.title"]/@content').get('text')
        if not dataset.title or dataset.title == 'text':
            dataset.title = res.xpath('/html/head/title/text()').get('text')
        dataset.name = h.make_slug(res.url)
        dataset.notes = res.xpath('//meta[@name="DC.description"]/@content').get('text')
        dataset.dump()
        return json.loads(dataset.toJSON())

    return None
