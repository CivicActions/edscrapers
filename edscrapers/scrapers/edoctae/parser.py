from .model import Model
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

extensions = {
    '.xls': 'Excel',
    '.xlsx' : 'Excel',
    '.pdf': 'PDF',
    '.zip': 'ZIP',
    '.csv': 'CSV',
}

def parse(res):

    if 'finaid' in res.url:
        print('FINAID!!')

    print(res)
    
    dataset = Model()

    with open('edoctae.log', 'a') as result_log:
        result_log.write(str(res) + '\n')
        for link in LxmlLinkExtractor(allow=(),deny_extensions=[]).extract_links(res):       
            for extension in extensions.keys():
                if link.url.endswith(extension):
                    resource = {
                        'url': link.url,
                        'name': link.text,
                    }
                    dataset.add_resource(resource)
                    #print('{} file: {}'.format(extensions[extension], link.url))
                    result_log.write('{}\n'.format(link.url))

    if len(dataset.resources) > 0:
        dataset.source_url = res.url
        dataset.title = res.xpath('/html/head/meta[@name="title"]/@content')
        #dataset.dump()
        return dataset

    return None