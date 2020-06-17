""" module is used to track if there are datasets
belonging to multiple collections.
this is identification is done using the graph model files which were
generated during the scraping and transforming processes.

NOTE: this module uses the ED_OUTPUT_PATH environment
varialbe same as the edscrapers toolkit """

import os
import pathlib

import igraph
from edscrapers.scrapers.base.graph import GraphWrapper

OUTPUT_PATH = os.getenv("ED_OUTPUT_PATH")

def get_all_collection_graph_output_file(dir_path=OUTPUT_PATH) -> list:
    """ function globs through the specified `dir_path` and collects the
    path to each collection graph output i.e.
    files that end with {name}.collection.pickle """

    # get the directory where all graph files are stored
    graph_dir_path = pathlib.Path(dir_path, 'graphs')
    if not graph_dir_path.is_dir():
        raise TypeError("expected a directory path")

    offices_dir_list = [] # holds the directory for every office that has a graph model
    # iterate through the graph directory
    for dir_child in graph_dir_path.iterdir():
        if dir_child.is_dir():
            offices_dir_list.append(dir_child)
    
    collections_graph_files = [] # holds the collections graph for every office available
    # iterate through the list of office directories and get the collection graph file
    for office in offices_dir_list:
        collections_graph_files.extend(office.glob('*.collections.pickle'))
    
    return collections_graph_files

def identify_datasets_with_multi_collections(graph_file_path):
    """ function identify datasets with multiple collections """

    if isinstance(graph_file_path, (str, pathlib.Path)):
        # load the graph from the filepath provided
        GraphWrapper.load_graph(file_dir_path=pathlib.Path(graph_file_path).parent,
                                file_stem_name=pathlib.Path(graph_file_path).stem)
        # get the loaded graph object
        graph = GraphWrapper.get_graph()

        with graph.graph_lock:
            # select datasets vertices that are in multiple collections
            dataset_ver_seq = graph.vs.select(is_dataset_eq=True, name_ne='base_vertext').\
                select(lambda vertex: 'in_collection' in vertex.attribute_names() and vertex['in_collection'] is not None and len(vertex['in_collection']) > 1)
            
            # get the name of the office this graph belongs to
            office_name = pathlib.Path(graph_file_path).stem.split('.')[0]
            # info user that there are datasets with multiple collections
            print(f'There are {len(dataset_ver_seq)} datasets with links to multiple Collections within the {office_name.upper()} office')
            
            return dataset_ver_seq
                

def output_to_csv(graph_vertex_seq):
    """ function dumps the identified dataset vertices that
    have multiple collections to a csv"""

    