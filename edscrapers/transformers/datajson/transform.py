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

    dataset.landingPage = data.get('source_url')
    dataset.title = data.get('title')
    dataset.identifier = data.get('name')

    if data.get('tags'):
        dataset.keyword = h.transform_keywords(data.get('tags'))
    
    if data.get('notes'):
        dataset.description = data.get('notes')

    if data.get('date'):
        dataset.modified = data.get('date')

    publisher = Organization()
    publisher.name = h.get_office_name(target_dept)
    dataset.publisher = publisher

    if data.get('contact_person_name') and data.get('contact_person_email'):
        contactPoint = {
            "@type": "vcard:Contact",
            "fn": data.get('contact_person_name'),
            "hasEmail": "mailto:" + data.get('contact_person_email')
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
    resources = data.get('resources')
    for resource in resources:
        distribution = _transform_scraped_resource(target_dept, resource)
        distributions.append(distribution)

    dataset.distribution = distributions

    return dataset

def _transform_scraped_resource(target_dept, resource):

    distribution = Resource()

    downloadURL = str()
    if h.url_is_absolute(resource.get('url')):
        downloadURL = resource.get('url')
    else:
        downloadURL = h.transform_download_url(resource.get('url'),
            resource.get('source_url'))

    #remove spaces in links
    downloadURL = downloadURL.replace(' ','%20')
    distribution.downloadURL = downloadURL

    distribution.title = resource.get('name')
    distribution.description = resource.get('name')

    if resource.get('format'):
        distribution.resource_format = resource.get('format')
        distribution.mediaType = h.get_media_type(resource.get('format'))
    else:
        extension = h.extract_format_from_url(distribution.downloadURL)
        if extension:
            distribution.resource_format = extension
            distribution.mediaType = h.get_media_type(extension)

    return distribution
