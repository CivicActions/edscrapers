from pathlib import Path

import edscrapers.transformer.helpers as h
from edscrapers.transformer.traverse import traverse, read_file
from edscrapers.transformer.models import Catalog, Dataset, Resource, Organization

def to_data_json(target_dept):

    catalog = Catalog()

    catalog.catalog_id = "datopian_data_json_" + target_dept

    file_list = traverse(target_dept)
    for file_path in file_list:

        data = read_file(file_path)
        dataset = transform_scraped_dataset(data, target_dept)

        catalog.datasets.append(dataset)
    
    Path(f"./data_json/").mkdir(parents=True, exist_ok=True)
    file_path = './data_json/' + target_dept + '.json'
    with open(file_path, 'w') as output:
        output.write(catalog.dump())

def transform_scraped_dataset(data, target_dept):

    dataset = Dataset()

    dataset.landingPage = data['source_url']
    dataset.title = data['title']
    dataset.description = data['notes']

    publisher = Organization()
    publisher.name = h.get_office_name(target_dept)
    dataset.publisher = publisher

    if data['contact_person_name'] and data['contact_person_email']:
        contactPoint = {
            "@type": "vcard:Contact",
            "fn": data['contact_person_name'],
            "hasEmail": "mailto:" + data['contact_person_email']
        }

        dataset.contactPoint = contactPoint
    
    '''
    data['name']
    data['publisher']
    data['tags']
    data['date']
    '''

    resources = data['resources']
    for resource in resources:
        distribution = transform_scraped_resource(resource)
        dataset.distribution.append(distribution)

    return dataset

def transform_scraped_resource(resource):

    distribution = Resource()

    distribution.downloadURL = resource['url']
    distribution.accessURL = resource['source_url']
    distribution.title = resource['name']
    distribution.resource_format = resource['format']
    
    return distribution
    
