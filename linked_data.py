""" module is intended to track if any dataset(s) or
dataset resources are linked across multiple offices.  """

import os
import pathlib
import collections
import json

from edscrapers.transformers.base import helpers as t_helpers
from edscrapers.scrapers.base import helpers as s_helpers

OUTPUT_PATH = os.getenv('ED_OUTPUT_PATH') # output path to write generated output files


class ModuleJSONEncoder(json.JSONEncoder):
    """ class provided json encoding for
    data structures in this module """

    def __init__(self, **kwargs):
        """ class constructor """
        super(ModuleJSONEncoder, self).__init__(**kwargs)
    
    def default(self, obj):
        """ override parent class to provide
        json encoding for data structures in this module """
        
        # check if the object to be encode is an instance of DatasetDict
        if isinstance(obj, (DatasetDict, ResourceDict, 
                            CollectionDict, SourceDict)):
            return obj.data
        else: # not an instance of any of the specified classes in this module
            return super(ModuleJSONEncoder, self).default(obj) # use parent implementation



class DatasetDict(collections.UserDict):
    """ class extends Dict to provide useful
    implementations for datasets
    """

    def __init__(self, initialData=None):
        """ class constructor """

        if isinstance(initialData, dict):
            super(DatasetDict, self).__init__(initialData)
        else:
            super(DatasetDict, self).__init__()

    def __eq__(self, other):
        """ overrides the __eq__() to provide
        unique == comparison for this class instances """
        return s_helpers.url_query_param_cleanup(url=self.get('scraped_from', None),
                                                 exclude_query_param=[]) == s_helpers.url_query_param_cleanup(url=other.get('scraped_from', None),
                                                                            exclude_query_param=[])
    
    def __hash__(self):
        """ensure this class instances are hashable"""
        return hash(s_helpers.url_query_param_cleanup(url=self.get('scraped_from', None),
                                                 exclude_query_param=[]))


class ResourceDict(collections.UserDict):
    """ class extends Dict to provide useful
    implementations for resources
    """

    def __init__(self, initialData=None):
        """ class constructor """

        if isinstance(initialData, dict):
            super(ResourceDict, self).__init__(initialData)
        else:
            super(ResourceDict, self).__init__()

    def __eq__(self, other):
        """ overrides the __eq__() to provide
        unique == comparison for this class instances """
        return s_helpers.url_query_param_cleanup(url=self.get('downloadURL', None),
                                                 exclude_query_param=[]) == s_helpers.url_query_param_cleanup(url=other.get('downloadURL', None),
                                                                            exclude_query_param=[])
    
    def __hash__(self):
        """ensure this class instances are hashable"""
        return hash(s_helpers.url_query_param_cleanup(url=self.get('downloadURL', None),
                                                 exclude_query_param=[]))


class CollectionDict(collections.UserDict):
    """ class extends Dict to provide useful
    implementations for collections
    """

    def __init__(self, initialData=None):
        """ class constructor """

        if isinstance(initialData, dict):
            super(CollectionDict, self).__init__(initialData)
        else:
            super(CollectionDict, self).__init__()

    def __eq__(self, other):
        """ overrides the __eq__() to provide
        unique == comparison for this class instances """
        return self.get('id', self['title']) == other.get('id', other['title'])
    
    def __hash__(self):
        """ensure this class instances are hashable"""
        return hash(self.get('id', self['title']))

class SourceDict(collections.UserDict):
    """ class extends Dict to provide useful
    implementations for sources
    """

    def __init__(self, initialData=None):
        """ class constructor """

        if isinstance(initialData, dict):
            super(SourceDict, self).__init__(initialData)
        else:
            super(SourceDict, self).__init__()

    def __eq__(self, other):
        """ overrides the __eq__() to provide
        unique == comparison for this class instances """
        return self.get('id', self['title']) == other.get('id', other['title'])
    
    def __hash__(self):
        """ensure this class instances are hashable"""
        return hash(self.get('id', self['title']))


def cumulate_datasets_across_offices(path_to_datajson_files):
    """ function accumulates all the datasets from all available offices
    into a single iterator """

    if not path_to_datajson_files:
        raise TypeError("'path_to_datajson_files' must be provided")
    if not isinstance(path_to_datajson_files, (str, pathlib.Path)):
        raise TypeError("'path_to_datajson_files' must be a path-like value/object")
    
    # convert the parameter 'path_to_datajson_files' to a path object
    path_to_datajson_files = pathlib.Path(path_to_datajson_files)

    if not path_to_datajson_files.is_dir(): # the parameter must be a directory
        raise ValueError("'path_to_datajson_files' must be a directory path")

    if not path_to_datajson_files.exists(): # the parameter must be a directory
        raise ValueError("'path_to_datajson_files' must be a valid directory path")

    # iterate through the contents of the directory
    for json_file in path_to_datajson_files.iterdir():
        if json_file.suffixes == ['.data', '.json']: # if the file as extension .data.json
            # with the aid of imported helper function, read the json content
            datajson = t_helpers.read_file(json_file)
            if datajson: # datajson is not None
                # get each dataset in the datasets list in the datajson
                for dataset in datajson.get('dataset', []):
                    # get a stripped down version of each dataset
                    stripped_dataset = DatasetDict()
                    stripped_dataset.update(office=json_file.stem.split('.')[0],
                                            scraped_from=dataset.get('scraped_from', ''),
                                            collection=dataset.get('collection', []),
                                            source=dataset.get('source', []))
                    yield stripped_dataset # yield the stripped down dataset


def track_duplicate_datasets(datasets_iterator, collections_iterator,
                             sources_iterator):
    """ function tracks duplicate datasets from within
    the iterator provided """

    # ensure the parameter is really an iterator
    datasets_iterator = list(iter(datasets_iterator))
    collections_iterator = list(iter(collections_iterator))
    sources_iterator = list(iter(sources_iterator))

    # create a counter to track where duplicates exist
    dataset_counter = collections.Counter(datasets_iterator)

    for counter_key, counter_value in dataset_counter.items():
        if not counter_key: # if key is None
            continue # move to the next dataset

        if counter_value > 1: # if the value is >1, there is a duplicate dataset
            # filter out the actual datasets that match the counter_key
            filtered_datasets = list(filter(lambda dataset, compare_dataset=counter_key: dataset == compare_dataset,
                                       datasets_iterator))
            
            # identify the offices that share these filtered datasets
            linked_offices = {a_dataset.get('office') for a_dataset in filtered_datasets}
            # check if the dataset is linked across different offices
            if len(linked_offices) <= 0: # if only 1 office is listed, there is no link across offices
                continue # move to the next
            
            filtered_collections = list(filter(lambda collection, compare_dataset=counter_key: collection['id'] in compare_dataset.get('collection', []),
                                          collections_iterator))
            filtered_sources = list(filter(lambda source, compare_dataset=counter_key: source['id'] in compare_dataset.get('source', []),
                                          sources_iterator))
            # return a dict with the linked datsets information
            yield {'scraped_from': counter_key['scraped_from'],
                   #'number_of_times_linked': counter_value,
                   'linked_offices': list(linked_offices),
                   'number_of_collections_linked_to': len(list(set(filtered_collections))),
                   'number_of_sources_linked_to': len(list(set(filtered_sources))),
                   'datasets': filtered_datasets,
                   'linked_collections': list(set(filtered_collections)),
                   'linked_sources': list(set(filtered_sources))}


def cumulate_resources_across_offices(path_to_datajson_files):
    """ function accumulates all the resources from all available offices
    into a single iterator """

    if not path_to_datajson_files:
        raise TypeError("'path_to_datajson_files' must be provided")
    if not isinstance(path_to_datajson_files, (str, pathlib.Path)):
        raise TypeError("'path_to_datajson_files' must be a path-like value/object")
    
    # convert the parameter 'path_to_datajson_files' to a path object
    path_to_datajson_files = pathlib.Path(path_to_datajson_files)

    if not path_to_datajson_files.is_dir(): # the parameter must be a directory
        raise ValueError("'path_to_datajson_files' must be a directory path")

    if not path_to_datajson_files.exists(): # the parameter must be a directory
        raise ValueError("'path_to_datajson_files' must be a valid directory path")

    # iterate through the contents of the directory
    for json_file in path_to_datajson_files.iterdir():
        if json_file.suffixes == ['.data', '.json']: # if the file as extension .data.json
            # with the aid of imported helper function, read the json content
            datajson = t_helpers.read_file(json_file)
            if datajson: # datajson is not None
                # get each dataset in the datasets list in the datajson
                for dataset in datajson.get('dataset', []):
                    # get each resource in each dataset
                    for resource in dataset.get('distribution', []):
                        # get a stripped down version of each resource
                        stripped_resource = ResourceDict()
                        stripped_resource.update(office=json_file.stem.split('.')[0],
                                                belongs_to_dataset_from=dataset.get('scraped_from', ''),
                                                downloadURL=resource.get('downloadURL', ''))
                        yield stripped_resource # yield the stripped down resource


def track_duplicate_resources(resources_iterator):
    """ function tracks duplicate resources from within
    the iterator provided """

    # ensure the parameter is really an iterator
    resources_iterator = list(iter(resources_iterator))

    # create a counter to track where duplicates exist
    resource_counter = collections.Counter(resources_iterator)

    # TODO the commented out variable 'trashed' is a circuilt-breaker variable.
    # it is used to shorten the output & execution time when searching for linked reasources
    # remove the comments on any line which contains the variable 'trash' in order to use it
    #trash = 0
    for counter_key, counter_value in resource_counter.items():
        #if trash == 2:
            #return trash
        if not counter_key: # if key is None
            continue # move to the next resource

        if counter_value > 1: # if the value is >1, there is a duplicate resource
            # filter out the actual resources that match the counter_key
            filtered_resources = list(filter(lambda resource, compare_resource=counter_key: resource == compare_resource,
                                       resources_iterator))
            
            # identify the offices that share these filtered resources
            linked_offices = {a_resource.get('office').lower() for a_resource in filtered_resources}
            # check if the resource is linked across different offices
            if len(linked_offices) <= 1: # if only 1 office is listed, there is no link across offices
                continue # move to the next

            #trash +=1
            # return a dict with the linked resource information
            yield {'downloadURL': counter_key['downloadURL'],
                   'belongs_to_dataset_from': counter_key['belongs_to_dataset_from'],
                   'number_of_times_linked': counter_value,
                   'linked_offices': list(linked_offices),
                   'resources': filtered_resources}

def cumulate_collections_across_offices(path_to_datajson_files):
    """ function accumulates all the collections from all available offices
    into a single iterator """

    if not path_to_datajson_files:
        raise TypeError("'path_to_datajson_files' must be provided")
    if not isinstance(path_to_datajson_files, (str, pathlib.Path)):
        raise TypeError("'path_to_datajson_files' must be a path-like value/object")
    
    # convert the parameter 'path_to_datajson_files' to a path object
    path_to_datajson_files = pathlib.Path(path_to_datajson_files)

    if not path_to_datajson_files.is_dir(): # the parameter must be a directory
        raise ValueError("'path_to_datajson_files' must be a directory path")

    if not path_to_datajson_files.exists(): # the parameter must be a directory
        raise ValueError("'path_to_datajson_files' must be a valid directory path")

    # iterate through the contents of the directory
    for json_file in path_to_datajson_files.iterdir():
        if json_file.suffixes == ['.data', '.json']: # if the file as extension .data.json
            # with the aid of imported helper function, read the json content
            datajson = t_helpers.read_file(json_file)
            if datajson: # datajson is not None
                # get each collection in the collections list in the datajson
                for collection in datajson.get('collection', []):
                    # get a stripped down version of each dataset
                    stripped_collection = CollectionDict()
                    stripped_collection.update(office=json_file.stem.split('.')[0],
                                            scraped_from=collection.get('scraped_from', ''),
                                            id=collection.get('id', collection['title']),
                                            title=collection.get('title', ''),
                                            source=collection.get('source', []))
                    yield stripped_collection # yield the stripped down dataset


def cumulate_sources_across_offices(path_to_datajson_files):
    """ function accumulates all the sources from all available offices
    into a single iterator """

    if not path_to_datajson_files:
        raise TypeError("'path_to_datajson_files' must be provided")
    if not isinstance(path_to_datajson_files, (str, pathlib.Path)):
        raise TypeError("'path_to_datajson_files' must be a path-like value/object")
    
    # convert the parameter 'path_to_datajson_files' to a path object
    path_to_datajson_files = pathlib.Path(path_to_datajson_files)

    if not path_to_datajson_files.is_dir(): # the parameter must be a directory
        raise ValueError("'path_to_datajson_files' must be a directory path")

    if not path_to_datajson_files.exists(): # the parameter must be a directory
        raise ValueError("'path_to_datajson_files' must be a valid directory path")

    # iterate through the contents of the directory
    for json_file in path_to_datajson_files.iterdir():
        if json_file.suffixes == ['.data', '.json']: # if the file as extension .data.json
            # with the aid of imported helper function, read the json content
            datajson = t_helpers.read_file(json_file)
            if datajson: # datajson is not None
                # get each source in the sources list in the datajson
                for source in datajson.get('source', []):
                    # get a stripped down version of each source
                    stripped_source = SourceDict()
                    stripped_source.update(office=json_file.stem.split('.')[0],
                                            scraped_from=source.get('scraped_from', ''),
                                            id=source.get('id', source['title']),
                                            title=source.get('title', ''))
                    yield stripped_source # yield the stripped down source


def track_duplicate_collections(collections_iterator, sources_iterator):
    """ function tracks duplicate collections from within
    the iterator provided """

    # ensure the parameter is really an iterator
    collections_iterator = list(iter(collections_iterator))
    sources_iterator = list(iter(sources_iterator))

    # create a counter to track where duplicates exist
    collection_counter = collections.Counter(collections_iterator)

    # TODO the commented out variable 'trashed' is a circuilt-breaker variable.
    # it is used to shorten the output & execution time when searching for linked reasources
    # remove the comments on any line which contains the variable 'trash' in order to use it
    #trash = 0
    for counter_key, counter_value in collection_counter.items():
        #if trash == 2:
            #return trash
        if not counter_key: # if key is None
            continue # move to the next resource

        if counter_value > 1: # if the value is >1, there is a duplicate resource
            # filter out the actual resources that match the counter_key
            filtered_collections = list(filter(lambda collection, compare_collection=counter_key: collection == compare_collection,
                                       collections_iterator))
            
            # identify the offices that share these filtered collections
            linked_offices = {a_collection.get('office').lower() for a_collection in filtered_collections}
            # check if the collection is linked across different offices
            if len(linked_offices) <= 0: # if only 1 office is listed, there is no link across offices
                continue # move to the next

            #trash +=1
            filtered_sources = list(filter(lambda source, compare_collection=counter_key: source['id'] in compare_collection.get('source', []),
                                          sources_iterator))
            # return a dict with the linked datsets information
            yield {'scraped_from': counter_key['scraped_from'],
                    'title': counter_key['title'],
                   #'number_of_times_linked': counter_value,
                   'linked_offices': list(linked_offices),
                   'number_of_sources_linked_to': len(list(set(filtered_sources))),
                   'linked_sources': list(set(filtered_sources))}

# run the script
if __name__ == "__main__":
    
    # get all collections available
    print("Accumulate all Collections....")
    collections_across_offices = list(cumulate_collections_across_offices(pathlib.Path(OUTPUT_PATH,
                              'transformers/datajson')))
    print("Done.")

    # get all sources available
    print("Accumulate all Sources....")
    sources_across_offices = list(cumulate_sources_across_offices(pathlib.Path(OUTPUT_PATH,
                              'transformers/datajson')))
    print("Done.")


    # get all datasets available
    print("Accumulating all Datasets....")
    datasets_across_offices = cumulate_datasets_across_offices(pathlib.Path(OUTPUT_PATH,
                              'transformers/datajson'))
    print("Done.")

    #track which datasets are duplicated across offices
    print("Finding linked datasets across offices....")
    duplicate_datasets = track_duplicate_datasets(datasets_across_offices,
                                                  collections_across_offices,
                                                  sources_across_offices)
    print('Done.')

    # write the result of the linked datasets search
    print('Producing output file at:',
           f"{pathlib.Path(OUTPUT_PATH, 'linked_datasets.json')}")
    # write the result of the linked dataset search to file
    with open(pathlib.Path(OUTPUT_PATH, "linked_datasets.json"), 'wt') as file_stream:
        json.dump(list(duplicate_datasets), file_stream,
                  cls=ModuleJSONEncoder, indent=2, sort_keys=False)
    print('Done.')

    ###
    #track which collections are duplicated across offices
    print("Finding linked collections across offices....")
    duplicate_collections = track_duplicate_collections(collections_across_offices,
                                                  sources_across_offices)
    print('Done.')

    # write the result of the linked collections search
    print('Producing output file at:',
           f"{pathlib.Path(OUTPUT_PATH, 'linked_collections.json')}")
    # write the result of the linked collection search to file
    with open(pathlib.Path(OUTPUT_PATH, "linked_collections.json"), 'wt') as file_stream:
        json.dump(list(duplicate_collections), file_stream,
                  cls=ModuleJSONEncoder, indent=2, sort_keys=False)
    print('Done.')

    #######
    # get all resources available
    """ print("Accumulating all Resources....")
    resources_across_offices = cumulate_resources_across_offices(pathlib.Path(OUTPUT_PATH,
                              'transformers/datajson'))
    print("Done.")

    #track which resources are duplicated across offices
    print("Finding linked resources across offices....")
    duplicate_resources = track_duplicate_resources(resources_across_offices)
    print('Done.')

    # write the result of the linked resources search
    print('Producing output file at:',
           f"{pathlib.Path(OUTPUT_PATH, 'linked_resources.json')}")
    # write the result of the linked resource search to file
    with open(pathlib.Path(OUTPUT_PATH, "linked_resources.json"), 'wt') as file_stream:
        json.dump(list(duplicate_resources), file_stream,
                  cls=ModuleJSONEncoder, indent=2, sort_keys=False)
    print('Done.') """