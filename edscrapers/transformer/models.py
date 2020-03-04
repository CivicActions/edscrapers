import datetime
import json

class Catalog():

    catalog_id = str()
    catalog_type = str()
    context = str()
    conformsTo = str()
    describedBy = str()
    datasets = list() # datasets list

    def __init__(self):
        
        self.catalog_id = "datopian_data_json"
        self.catalog_type = "dcat:Catalog"
        self.context = "https://project-open-data.cio.gov/v1.1/schema/catalog.jsonld"
        self.conformsTo = "https://project-open-data.cio.gov/v1.1/schema"
        self.describedBy = "https://project-open-data.cio.gov/v1.1/schema/catalog.json"

    def to_dict(self):

        return {
            "@context": self.context,
            "@id": self.catalog_id,
            "@type": self.catalog_type,
            "conformsTo": self.conformsTo,
            "describedBy": self.describedBy,
            "dataset": self.dump_datasets()
        }

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
    modified = str()
    landingPage = str()
    #publisher =
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
        self.dataset_license = "https://creativecommons.org/publicdomain/zero/1.0/"
        self.spatial = "United States"

    def to_dict(self):

        return {
            "@type": self.dataset_type,
            "title": self.title,
            "description": self.description,
            "keyword": self.keyword,
            "modified": self.modified,
            "landingPage": self.landingPage,
            "contactPoint": self.contactPoint,
            "identifier": self.identifier,
            "accessLevel": self.accessLevel,
            "bureauCode": self.bureauCode,
            "programCode": self.programCode,
            "license": self.dataset_license,
            "spatial": self.spatial,
            "temporal": self.temporal,
            "theme": self.theme,
            "distribution": self.dump_resources()
        }

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

    def to_dict(self):

        return {
            "@type": self.resource_type,
            "title": self.title,
            "description": self.description,
            "downloadURL": self.downloadURL,
            "accessURL": self.accessURL,
            "format": self.resource_format,
            "mediaType": self.mediaType
        }