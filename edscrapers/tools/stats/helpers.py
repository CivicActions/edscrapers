""" File contains helper functions/utilities for 
'dataset_metrics' module"""

def filter_data_json_datasets(item):
    """ function filters the datasets in data.json to 
    get dataset that contain resources """

    if item.get('dataQuality', False) == True and\
            item.get('distribution', False) != False:
        return True
    else:
        return False


def map_data_json_resources_to_lists(dataset_dict):
    """ function helps map the resources obtained from
    a dataset in data.json file to a list which can then
    be converted to panda dataframe row """
    
    resource_list = [] # list to hold resource urls from this dataset
    for item in dataset_dict['distribution']: # get the resources in dataset
        if(item.get('downloadURL', False) == False): # no resource url available
            continue # skip it
        resource_list.append(item['downloadURL']) # get the url of resource
    return resource_list
