import json
from edscrapers.transformers.base.helpers import traverse_output


def transform(name=None, input_file=None):
    transformer = Transformer(name)

    if not input_file:
        out_file = f'./output/deduplicated_{name or "all"}.lst'
    else:
        out_file = input_file

    with open(out_file, 'w') as fp:
        for fname in transformer.urls_dict.values():
            fp.write(fname + '\n')

    print('Deduplicated list is ready.')


class Transformer():

    def __init__(self, name=None):

        if name is None:
            self.file_list = traverse_output()
        else:
            self.file_list = traverse_output(name)

        # Deduplicate using a Python dict's keys uniqueness
        self.urls_dict = dict()
        self._make_list('source_url')


    def _make_list(self, key):
        for f in self.file_list:
            with open(f, 'r') as fp:
                j = json.loads(fp.read())
                if '/print/' in j.get(key):
                    continue
                # In order to deduplicate with dicts, we need to normalize all keys
                self.urls_dict[self._normalize_url(j.get(key)) + '_' + j.get('name')] = str(f)


    def _normalize_url(self, url):
        # First strip protocol data
        url = url.replace('https://', '').replace('http://', '')
        # Remove www or www2
        url = url.replace('www2.', '').replace('www.', '')
        # Remove /print/ segment from printable pages
        # url = url.replace('/print/', '')
        # Lowercase all
        url = url.lower()

        return url
