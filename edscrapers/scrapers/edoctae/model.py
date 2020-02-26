import json

from edscrapers.scrapers.base.model import Model as BaseModel

class Model(BaseModel):

    source_url = ''
    title = ''
    name = ''
    notes = ''

    resources = []

    def __init__(self):
        pass

    def add_resource(self, resource):
        resource_keys = ['url', 'name']
        result = {}
        for k in resource_keys:
            if resource[k]:
                result[k] = resource[k]
            else:
                result[k] = ''
        self.resources.extend(result)

    def before_dump(self):
        if self.name:
            self.name = self.name.lower()

    def dump(self):
        self.before_dump()
        print('\n>>>>>>>>>    I AM DUMPING NOW!!!!!!!')
        print(json.dumps(self.json()))

    def json(self):
        return {
            'source_url' : self.source_url,
            'title' : self.title,
            'name' : self.name,
            'notes' : self.notes,
            'resources' : self.resources
        }
