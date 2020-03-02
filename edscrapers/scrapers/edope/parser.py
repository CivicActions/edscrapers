import json

from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from edscrapers.scrapers.edgov.model import Dataset

import edscrapers.scrapers.base.helpers as h

data_extensions = {
    '.xlsx': 'Excel spreadsheet',
    '.xls': 'Excel spreadsheet',
    '.zip': 'ZIP archive',
    '.csv': 'CSV file',
}

document_extensions = {
    '.docx': 'Word document',
    '.doc': 'Word document',
    '.pdf': 'PDF file',
 }

deny_list = [

]

def parse(res):

    print(res)

    def _get_all_resources(dataset, extensions):
        for link in LxmlLinkExtractor(deny_extensions=[], deny=deny_list).extract_links(res):
            for extension in extensions.keys():
                if link.url.endswith(extension):
                    resource = {
                        'source_url': res.url,
                        'url': link.url,
                        'name': link.text,
                    }
                    dataset.add_resource(resource)

    dataset = Dataset()

    _get_all_resources(dataset, data_extensions)

    if len(dataset.resources) > 0:

        # We've got resources, so the documents might be relevant to them
        _get_all_resources(dataset, document_extensions)

        dataset.source_url = res.url
        dataset.title = res.xpath('//meta[@name="DC.title"]/@content').get('text')
        if not dataset.title or dataset.title == 'text':
            dataset.title = res.xpath('/html/head/title/text()').get('text')
        dataset.name = h.make_slug(res.url)
        dataset.notes = res.xpath('//meta[@name="DC.description"]/@content').get('text')
        dataset.dump()

        return json.loads(dataset.toJSON())

    return None