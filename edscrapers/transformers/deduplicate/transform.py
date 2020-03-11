import json
from edscrapers.transformers.base.helpers import traverse_output


def transform(target_dept=None):
    transformer = Transformer(target_dept)

    with open(f'./output/deduplicated_{target_dept or "all"}.lst', 'w') as fp:
        for fname in transformer.urls_dict.values():
            fp.write(fname + '\n')

    print('Deduplicated list is ready.')


class Transformer():

    def __init__(self, target_dept=None):

        if target_dept is None:
            self.file_list = traverse_output()
        else:
            self.file_list = traverse_output(target_dept)

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
                self.urls_dict[self._normalize_url(j.get(key))] = str(f)


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
