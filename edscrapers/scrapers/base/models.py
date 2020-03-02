import os
import json
import hashlib
from pathlib import Path
import edscrapers.scrapers.base.helpers as h

class Dataset():

    def __init__(self, title=None, name=None, notes=None, source_url=None):
        setattr(self, 'title', title)
        setattr(self, 'name', name)
        setattr(self, 'notes', notes)
        setattr(self, 'source_url', source_url)
        setattr(self, 'resources', [])

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=2)


class Resource():

    def __init__(self, name=None, url=None, source_url=None, description=None):
        setattr(self, 'name', name)
        setattr(self, 'url', url)
        setattr(self, 'source_url', source_url)
        setattr(self, 'description', description)
