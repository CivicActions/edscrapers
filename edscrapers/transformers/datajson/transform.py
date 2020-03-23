import os
from pathlib import Path
from urllib.parse import urlparse
from urllib.parse import urljoin

import edscrapers.transformers.base.helpers as h
from edscrapers.cli import logger
from edscrapers.transformers.base.helpers import traverse_output, read_file
from edscrapers.transformers.datajson.models import Catalog, Dataset, Resource, Organization

OUTPUT_DIR = os.getenv('ED_OUTPUT_PATH')
resources_common_names = ['excel', 'doc', 'download excel', 'download se excel',
                        'dowload doc', 'download this table as an excel file.',
                        'download this table as a microsoft excel spreadsheet',
                        'excel download', 'download standard error excel']

dataset_title_list = []
dataset_identifier_list = []


def transform(name, input_file=None):
    if input_file is None:
        file_list = traverse_output(name)
    else:
        try:
            with open(input_file, 'r') as fp:
                file_list = [line.rstrip() for line in fp]
        except:
            logger.warn(f'Cannot read from list of output files at {input_file}, falling back to all collected data!')
            file_list = traverse_output(name)

    logger.debug(f'{len(file_list)} files to transform.')

    catalog = Catalog()
    catalog.catalog_id = "datopian_data_json_" + name

    datasets_number = 0
    resources_number = 0

    for file_path in file_list:

        data = read_file(file_path)
        if not data:
            continue

        dataset = _transform_scraped_dataset(data, name)
        catalog.datasets.append(dataset)

        datasets_number += 1
        resources_number += len(dataset.distribution)

    logger.debug('{} datasets transformed.'.format(datasets_number))
    logger.debug('{} resources transformed.'.format(resources_number))

    output_path = os.path.join(OUTPUT_DIR, 'transformers', 'datajson')
    Path(output_path).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(output_path, f'{name}.data.json')
    with open(file_path, 'w') as output:
        output.write(catalog.dump())
        logger.debug(f'Output file: {file_path}')

    if os.getenv('S3_ACCESS_KEY') and os.getenv('S3_SECRET_KEY'):
        S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'us-ed-scraping')
        S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
        S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')

        from botocore.client import Config
        from boto3.session import Session
        from botocore.handlers import set_list_objects_encoding_type_url

        session = Session(aws_access_key_id=S3_ACCESS_KEY,
                        aws_secret_access_key=S3_SECRET_KEY,
                        region_name="US-CENTRAL1")

        session.events.unregister('before-parameter-build.s3.ListObjects', set_list_objects_encoding_type_url)

        s3 = session.resource('s3', endpoint_url='https://storage.googleapis.com',
                            config=Config(signature_version='s3v4'))

        bucket = s3.Bucket(S3_BUCKET_NAME)
        # bucket.upload_file(file_path, f'{name}.data.json',  )
        with open(file_path, 'rb') as file_obj:
            bucket.put_object(Key=f'{name}.data.json', Body=file_obj)
        logger.info(f'File uploaded to https://storage.googleapis.com/us-ed-scraping/{name}.data.json')


def _transform_scraped_dataset(data, target_dept):

    dataset = Dataset()

    scraped_from = data.get('source_url')
    if '|' in scraped_from:
        scraped_from = scraped_from.split('|')[0]

    dataset.scraped_from = scraped_from
    
    ### removing leading and trailing withespaces from title
    title = data.get('title').strip()
    if title and title not in dataset_title_list:
        dataset.title = title
        dataset_title_list.append(title)
    else:
        dataset.title = h.transform_dataset_title(title, scraped_from)

    identifier = data.get('name')
    if identifier in dataset_identifier_list:
        identifier = h.transform_dataset_identifier(title, scraped_from)
    dataset.identifier = identifier
    dataset_identifier_list.append(identifier)

    if data.get('tags'):
        dataset.keyword = h.transform_keywords(data.get('tags'))
    
    if data.get('notes'):
        dataset.description = data.get('notes')

    if data.get('date'):
        dataset.modified = data.get('date')

    publisher = Organization()
    publisher.name = h.get_office_name(target_dept)
    dataset.publisher = publisher

    contactPoint = {
        "@type": "vcard:Contact",
    }

    if data.get('contact_person_name'):
        contactPoint['fn'] = data.get('contact_person_name')
    else:
        contactPoint['fn'] = h.get_office_name(target_dept)

    if data.get('contact_person_email'):
        contactPoint['hasEmail'] = "mailto:" + data.get('contact_person_email')
    else:
        contactPoint['hasEmail'] = "mailto:odp@ed.gov"

    dataset.contactPoint = contactPoint

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
    if urlparse(resource.get('url')).scheme:
        downloadURL = resource.get('url')
    else:
        downloadURL = urljoin(resource.get('source_url'), resource.get('url'))

    #remove spaces in links
    downloadURL = downloadURL.replace(' ','%20')
    distribution.downloadURL = downloadURL

    resource_name = str(resource.get('name'))
    if resource_name and resource_name.lower() not in resources_common_names:
        distribution.title = resource.get('name')
    else:
        distribution.title = h.extract_resource_name_from_url(distribution.downloadURL)

    if resource.get('description'):
        distribution.description = resource.get('description')

    if resource.get('format'):
        distribution.resource_format = resource.get('format')
        distribution.mediaType = h.get_media_type(resource.get('format'))
    else:
        extension = h.extract_resource_format_from_url(distribution.downloadURL)
        if extension:
            distribution.resource_format = extension
            distribution.mediaType = h.get_media_type(extension)

    return distribution
