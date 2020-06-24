import os
import time
import pandas as pd
from ckanapi import RemoteCKAN, CKANAPIError


api_url = os.getenv('CKAN_API_URL')
api_key = os.getenv('CKAN_API_KEY')


ckan = RemoteCKAN(api_url, apikey=api_key)


def make_ckan_request(action, data_dict, retry=0):
    result = None
    try:
        time.sleep(0.1)
        result = ckan.call_action(action, data_dict)
    except CKANAPIError:
        if retry < 6:
            print('retrying...', end='')
            result = make_ckan_request(action, data_dict, retry+1)
        else:
            print('FAILED', end='')
            raise Exception('Max retries exceeded')
    return result

def get_all_organizations():
    organization_names = []
    organization_details = []
    organizations = []

    try:
        organization_names = ckan.call_action('organization_list')
        for organization in organization_names:
            print(f'Getting details for organization {organization}...', end='')
            organization_details.append(
                make_ckan_request(
                    'organization_show',
                    {'id': organization}))
            print('done.')
    except:
        raise Exception('Could not get organizations list, please retry.')

    organizations = [{o['id']: o['name']} for o in organization_details]
    return organizations

def get_all_datasets():
    datasets = []
    offset = 0

    datasets = get_datasets(offset)
    while len(datasets) == 500:
        offset = offset + 500
        datasets.extend(get_datasets(offset))
    print(f'Collected {len(datasets)} datasets.')
    return datasets

def get_datasets(offset):
    print(f'Collecting datasets between {offset} and {offset + 500}...', end='')
    result = make_ckan_request('package_list',
                               {'limit': 500,
                                'offset': offset})
    print('done.')
    return result

def get_dataset(name, retry=0):
    result = None
    try:
        time.sleep(0.1)
        result = ckan.call_action('package_show', {'id': name})
    except CKANAPIError:
        if retry < 6:
            print('retrying...', end='')
            result = get_dataset(name, retry+1)
        else:
            print('FAILED', end='')
            raise Exception('Max retries exceeded')
    return result

def get_datasets_df(datasets):
    ckan_packages = []
    errors = []
    # datasets = datasets[:3]
    for dataset in datasets:
        print(f'Getting details for package {dataset}...', end='')
        try:
            ckan_packages.append(make_ckan_request('package_show', {'id': dataset}))
            print(f'done')
        except:
            errors.append(dataset)
            print(f'ERROR: MAX RETRIES EXCEEDED.')
    return (ckan_packages, errors)

organizations = get_all_organizations()
datasets = get_datasets_df(get_all_datasets())

import ipdb; ipdb.set_trace()
