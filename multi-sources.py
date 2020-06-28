""" module is used to track if there are collections
belonging to multiple sources.
this identification is done using the graph model files which were
generated during the scraping and transforming processes.

NOTE: this module uses the ED_OUTPUT_PATH environment
varialbe same as the edscrapers toolkit """

import os
import pathlib

import pandas as pd
from edscrapers.scrapers.base.graph import GraphWrapper

OUTPUT_PATH = os.getenv("ED_OUTPUT_PATH")

def get_all_source_graph_output_file(dir_path=OUTPUT_PATH) -> list:
    """ function globs through the specified `dir_path` and collects the
    path to each source graph output i.e.
    files that end with {name}.source.pickle """

    if str(dir_path) == OUTPUT_PATH:
        # get the directory where all graph files are stored
        graph_dir_path = pathlib.Path(dir_path, 'graphs')
    else:
        graph_dir_path = pathlib.Path(dir_path)

    if not graph_dir_path.is_dir():
        raise TypeError("expected a directory path")

    offices_dir_list = [] # holds the directory for every office that has a graph model
    # iterate through the graph directory
    for dir_child in graph_dir_path.iterdir():
        if dir_child.is_dir():
            offices_dir_list.append(dir_child)
    
    sources_graph_files = [] # holds the sources graph for every office available
    # iterate through the list of office directories and get the collection graph file
    for office in offices_dir_list:
        sources_graph_files.extend(office.glob('*.sources.pickle'))
    
    return sources_graph_files

def identify_collections_with_multi_sources(graph_file_path):
    """ function identify collections with multiple sources """

    if isinstance(graph_file_path, (str, pathlib.Path)):
        # load the graph from the filepath provided
        GraphWrapper.load_graph(file_dir_path=pathlib.Path(graph_file_path).parent,
                                file_stem_name=pathlib.Path(graph_file_path).stem)
        # get the loaded graph object
        graph = GraphWrapper.get_graph()

        with graph.graph_lock:
            # select collections vertices that are in multiple sources
            collection_ver_seq = graph.vs.select(is_collection_eq=True, name_ne='base_vertex').\
                select(lambda vertex: 'in_source' in vertex.attribute_names() and vertex['in_source'] is not None and len(vertex['in_source']) > 1)
            
            # get the name of the office this graph belongs to
            office_name = pathlib.Path(graph_file_path).stem.split('.')[0]
            collection_ver_seq['office_name'] = office_name
            # info user that there are collection with multiple sources
            print(f'There are {len(collection_ver_seq)} collections with links to multiple Sources within the {office_name.upper()} office')
            
            return collection_ver_seq
    else:
        raise TypeError("Invalid 'graph_file_path' specified")
                

def output_to_csv(graph_vertex_seq, graph_office_name):
    """ function dumps the identified collection vertices that
    have multiple sources to a csv"""

    if len(graph_vertex_seq) == 0: #the sequence is empty so set some defaults
        graph_vertex_seq['source_urls'] = ''
        graph_vertex_seq['source_names'] = ''
        graph_vertex_seq['num_of_source'] = 0

    for vertex in graph_vertex_seq:
        vertex['source_urls'] = "\n".join([source['source_url'] for source in vertex['in_source']])
        vertex['source_names'] = "\n".join([source['source_title'] for source in vertex['in_source']])
        vertex['num_of_source'] = len(vertex['in_source'])

    # convert the vertex sequence to a panda frame
    df = pd.DataFrame(columns=['Collection URL', 'Collection Publisher', 'Number of Sources Linked To', 'Source URLs'])
    df['Collection URL'] = graph_vertex_seq['name']
    df['Collection Publisher'] = graph_vertex_seq['office_name']
    df['Number of Sources Linked To'] = graph_vertex_seq['num_of_source']
    df['Source URLs'] = graph_vertex_seq['source_urls']

    df.to_csv(pathlib.Path(OUTPUT_PATH, f'{graph_office_name}_collection_multi_source.csv'),
                columns=['Collection URL', 'Collection Publisher', 'Number of Sources Linked To', 'Source URLs'],
                header=True, index=False)


if __name__ == "__main__":
    
    graph_file_list = get_all_source_graph_output_file()

    # loop through the graph file paths provided
    for graph_file in graph_file_list:
        name_of_office = pathlib.Path(graph_file).name.split('.')[-3]
        v_sequence = identify_collections_with_multi_sources(graph_file)
        output_to_csv(graph_vertex_seq=v_sequence,
                      graph_office_name=name_of_office)