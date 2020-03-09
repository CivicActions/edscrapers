import os
import json
import hashlib

from pathlib import Path
from scrapy import Item, Field


class Dataset(Item):

    source_url = Field()

    title = Field()
    name = Field()
    notes = Field()
    publisher = Field()
    date = Field()
    contact_person_name = Field()
    contact_person_email = Field()

    tags = Field()
    resources = Field()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__['_values'],
                          sort_keys=False, indent=2)


class Resource(Item):

    name = Field()
    url = Field()
    source_url = Field()
    description = Field()
    format = Field()
