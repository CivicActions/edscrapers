from pathlib import Path

import edscrapers.transformers.base.helpers as h
from edscrapers.transformers.base import logger
from edscrapers.transformers.base.helpers import traverse_output, read_file
from edscrapers.transformers.datajson.models import Catalog, Dataset, Resource, Organization


def transform(target_dept, output_list_file=None):
    if output_list_file is None:
        file_list = traverse_output(target_dept)
    else:
        try:
            with open(output_list_file, 'r') as fp:
                file_list = [line.rstrip() for line in fp]
        except:
            logger.warn(f'Cannot read from list of output files at {output_list_file}, falling back to all collected data!')
            file_list = traverse_output(target_dept)
    logger.debug(f'{len(file_list)} files to transform.')

    catalog = Catalog()
    catalog.catalog_id = "datopian_data_json_" + target_dept

    datasets_number = 0
    resources_number = 0

    for file_path in file_list:

        data = read_file(file_path)
        if not data:
            continue

        dataset = _transform_scraped_dataset(data, target_dept)
        catalog.datasets.append(dataset)

        datasets_number += 1
        resources_number += len(dataset.distribution)

    logger.debug('{} datasets transformed.'.format(datasets_number))
    logger.debug('{} resources transformed.'.format(resources_number))
    Path(f"./output/").mkdir(parents=True, exist_ok=True)
    file_path = f"./output/{target_dept}.data.json"
    with open(file_path, 'w') as output:
        output.write(catalog.dump())
        logger.debug(f'Output file: {file_path}')
        print(f'Output file: {file_path}')

def _transform_scraped_dataset(data, target_dept):

    dataset = Dataset()

    dataset.landingPage = data['source_url']
    dataset.title = data['title']
    dataset.description = data['notes']
    dataset.identifier = data['name']

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


    ### testing and inserting dummy values for required fields
    if not dataset.contactPoint:
        dataset.contactPoint = {
            "@type": "vcard:Contact",
            "hasEmail": "mailto:info@viderum.com",
            "fn": h.get_office_name(target_dept)
        }

    if not len(dataset.bureauCode) > 0:
        dataset.bureauCode = ["018:40"]

    if not len(dataset.programCode) > 0:
        dataset.programCode = ["018:000"]

    if not len(dataset.keyword) > 0:
        dataset.keyword = [target_dept]

    distributions = []
    resources = data['resources']
    for resource in resources:
        distribution = _transform_scraped_resource(target_dept, resource)
        distributions.append(distribution)

    dataset.distribution = distributions

    return dataset

def _transform_scraped_resource(target_dept, resource):

    distribution = Resource()

    downloadURL = str()
    if h.url_is_absolute(resource['url']):
        downloadURL = resource['url']
    else:
        downloadURL = h.transform_download_url(resource['url'],
            resource['source_url'])

    #remove spaces from links
    downloadURL = downloadURL.replace(' ','%20')
    distribution.downloadURL = downloadURL

    distribution.title = resource['name']
    distribution.resource_format = resource['format']
    distribution.description = resource['name']
    distribution.mediaType = h.get_media_type(resource['format'])

    return distribution
