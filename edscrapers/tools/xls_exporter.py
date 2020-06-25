from __future__ import print_function
import os
import time
import pandas as pd
from ckanapi import RemoteCKAN, CKANAPIError


ckan_url = os.getenv('CKAN_API_URL', 'https://us-ed-testing.ckan.io')
api_url = os.getenv('CKAN_API_URL', ckan_url)
api_key = os.getenv('CKAN_API_KEY', None)
xlsx_file = os.getenv('CKAN_XLSX_FILE', 'output.xlsx')

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
        organization_names = make_ckan_request('organization_list', {})
        for organization in organization_names:
            print('Getting details for organization {}...'.format(organization), end='')
            organization_details.append(
                make_ckan_request(
                    'organization_show',
                    {'id': organization}))
            print('done.')
    except:
        raise Exception('Could not get organizations list, please retry.')

    organizations = {o['id']: o['name'] for o in organization_details}
    return organizations

def get_all_datasets():
    datasets = []
    offset = 0

    datasets = get_datasets(offset)
    while len(datasets) == 500:
        offset = offset + 500
        datasets.extend(get_datasets(offset))
    print('Collected {} datasets.'.format(len(datasets)))
    return datasets

def get_datasets(offset):
    print('Collecting datasets between {} and {}...'.format(offset, offset+500), end='')
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
        if result.get('type', 'dataset') != 'dataset':
            return None
        return {
            'ID': result.get('id', result.get('ID')),
            'Title': result.get('title', 'no title'),
            'URL': '{}/dataset/{}'.format(ckan_url, result['name']),
            'Source URL': result.get('scraped_from', 'n/a'),
            'Description': result.get('notes', ''),
            'Categories': ', '.join([str(g['display_name']) for g in result['groups']]),
            'owner_org': result.get('owner_org')
        }
    except CKANAPIError:
        if retry < 6:
            print('retrying...', end='')
            return get_dataset(name, retry+1)
        else:
            print('FAILED', end='')
            raise Exception('Max retries exceeded')

def get_datasets_df(datasets):
    ckan_packages = []
    errors = []
    for dataset in datasets:
        print('Getting details for package {}...'.format(dataset), end='')
        try:
            dataset_dict = get_dataset(dataset)
            if dataset_dict is not None:
                ckan_packages.append(dataset_dict)
                print('done')
            else:
                print('done, not a dataset.')
        except Exception as e:
            errors.append({dataset: e})
            print('ERROR.')
    result = (ckan_packages, errors)

    if len(result[1]):
        print('{} error(s) occured, please check the output before using it.'.format(len(result[1])))
        print(result[1])

    df = pd.DataFrame(result[0])
    return df


print('Collecting data from {}'.format(ckan_url))

df = get_datasets_df(get_all_datasets())
organizations = get_all_organizations()

existing_organizations = df['owner_org'].unique()
print('Got {} organizations.'.format(len(existing_organizations)))

if os.path.exists(xlsx_file): # clean up output
    os.unlink(xlsx_file)

for organization in existing_organizations:
    print('Dumping {} datasets'.format(organizations[organization]))
    result = df[df['owner_org']==organization]
    if os.path.exists(xlsx_file): # check if excel sheet exist
        writer_mode = 'a' # set write mode to append
    else:
        writer_mode = 'w' # set write mode to write
    with pd.ExcelWriter(xlsx_file, engine="openpyxl",
                        mode=writer_mode) as writer:
        result.to_excel(writer,
                        sheet_name=organizations[organization],
                        index=False,
                        engine='openpyxl')
