import json
from datetime import datetime

from edscrapers.transformers.base import helpers as h 

class Organization():

    organization_type = str()
    name = str()
    sub_organization_of = None

    def __init__(self):

        self.organization_type = "org:Organization"

    def to_dict(self):

        if not self.name:
            return None

        org_dict = {
            "@type": self.organization_type,
            "name": self.name
        }

        if self.sub_organization_of is not None:
            org_dict["subOrganizationOf"] = self.sub_organization_of.to_dict()

        return org_dict

class Catalog():

    catalog_id = str()
    catalog_type = str()
    context = str()
    conformsTo = str()
    describedBy = str()
    datasets = list() # datasets list

    def __init__(self):
        
        self.catalog_type = "dcat:Catalog"
        self.context = "https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld"
        self.conformsTo = "https://project-open-data.cio.gov/v1.1/schema"
        self.describedBy = "https://project-open-data.cio.gov/v1.1/schema/catalog.json"

    def to_dict(self):

        catalog_dict = {}

        if self.context:
            catalog_dict["@context"] = self.context

        if self.catalog_id:
            catalog_dict["@id"] = self.catalog_id

        if self.catalog_type:
            catalog_dict["@type"] = self.catalog_type

        if self.conformsTo:
            catalog_dict["conformsTo"] = self.conformsTo

        if self.describedBy:
            catalog_dict["describedBy"] = self.describedBy

        if len(self.datasets) > 0:
            catalog_dict["dataset"] = self.dump_datasets()

        return catalog_dict

    def dump_datasets(self):

        datasets_lst = []

        for dataset in self.datasets:
            datasets_lst.append(dataset.to_dict())

        return datasets_lst

    
    def dump(self):
        return json.dumps(self.to_dict(), sort_keys=False, indent=2)
    
class Dataset():
    
    dataset_type = str()
    title = str()
    description = str()
    keyword = list()
    modified = None
    landingPage = str()
    publisher = Organization()
    contactPoint = dict()
    identifier = str()
    accessLevel = str()
    bureauCode = list()
    programCode = list()
    dataset_license = str()
    spatial = str()
    temporal = str()
    theme = list()
    distribution = list() # resources list

    def __init__(self):
        
        self.dataset_type = "dcat:Dataset"
        self.accessLevel = "public"
        #self.dataset_license = "https://creativecommons.org/publicdomain/zero/1.0/"
        #self.dataset_license = "notspecified"
        self.spatial = "United States"
        self.description = "n/a"
        self.modified = datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):

        dataset_dict = {}

        if self.dataset_type:
            dataset_dict["@type"] = self.dataset_type
        
        if self.title:
            dataset_dict["title"] = self.title
        
        if self.description:
            dataset_dict["description"] = self.description

        if len(self.keyword) > 0:
            dataset_dict["keyword"] = self.keyword

        if self.modified:
            dataset_dict["modified"] = self.modified

        if self.publisher.to_dict():
            dataset_dict["publisher"] = self.publisher.to_dict()

        if self.landingPage:
            dataset_dict["landingPage"] = self.landingPage

        if self.contactPoint:
            dataset_dict["contactPoint"] = self.contactPoint

        if self.identifier:
            dataset_dict["identifier"] = self.identifier

        if self.accessLevel:
            dataset_dict["accessLevel"] = self.accessLevel

        if len(self.bureauCode) > 0:
            dataset_dict["bureauCode"] = self.bureauCode

        if len(self.programCode) > 0:
            dataset_dict["programCode"] = self.programCode

        if self.dataset_license:
            dataset_dict["license"] = self.dataset_license

        if self.spatial:
            dataset_dict["spatial"] = self.spatial

        if self.temporal:
            dataset_dict["temporal"] = self.temporal

        if len(self.theme) > 0:
            dataset_dict["theme"] = self.theme

        if len(self.distribution) > 0:
            dataset_dict["distribution"] = self.dump_resources()

        return dataset_dict

    def dump_resources(self):

        resources_lst = []

        for resource in self.distribution:
            resources_lst.append(resource.to_dict())

        return resources_lst

class Resource():

    resource_type = str()
    description = str()
    title = str()
    resource_format = str()
    mediaType = str()
    accessURL = str()
    downloadURL = str()

    def __init__(self):    
        self.resource_type = "dcat:Distribution"
        self.resource_format = "txt"
        self.mediaType = h.get_media_type(self.resource_format)

    def to_dict(self):

        resource_dict = {}

        if self.resource_type:
            resource_dict["@type"] = self.resource_type

        if self.title:
            resource_dict["title"] = self.title
        
        if self.description:
            resource_dict["description"] = self.description

        if self.downloadURL:
            resource_dict["downloadURL"] = self.downloadURL

        if self.accessURL:
            resource_dict["accessURL"] = self.accessURL

        if self.resource_format:
            resource_dict["format"] = self.resource_format

        if self.mediaType:
            resource_dict["mediaType"] = self.mediaType

        return resource_dict