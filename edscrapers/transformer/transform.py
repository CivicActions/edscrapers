from pathlib import Path

from edscrapers.transformer.traverse import traverse, read_file
from edscrapers.transformer.models import Catalog, Dataset, Resource

def to_data_json(target_dept):

    catalog = Catalog()

    file_list = traverse(target_dept)
    for file_path in file_list:

        data = read_file(file_path)
        dataset = transform_scraped_dataset(data)

        catalog.datasets.append(dataset)
    
    Path(f"./data_json/").mkdir(parents=True, exist_ok=True)
    file_path = './data_json/' + target_dept + '.json'
    with open(file_path, 'w') as output:
        output.write(catalog.dump())

def transform_scraped_dataset(data):

    dataset = Dataset()

    dataset.landingPage = data['source_url']
    dataset.title = data['title']
    dataset.description = data['notes']
    
    '''
    data['name']
    data['publisher']
    data['tags']
    data['date']
    data['contact_person_name']
    data['contact_person_email']
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
    
