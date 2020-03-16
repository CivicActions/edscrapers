import os
import json
import pathlib

from slugify import slugify
from urllib.parse import urlparse
from urllib.parse import urljoin


map_office_name = {
    'edgov' : 'Department of Education',
    'ocr' : 'Office for Civil Rights',
    'edoctae' : 'Office of Career, Technical and Adult Education',
    'edope' : 'Office of Postsecondary Education',
    'edoela' : 'Office of English Language Acquisition',
    'edosers' : 'Office of Special Education and Rehabilitative Services',
    'edopepd' : 'Office of Planning, Evaluation and Policy Development',
    'edoese' : 'Office of Elementary and Secondary Education',
    'oese' : 'Office of Elementary and Secondary Education',
    'nces' : 'National Center for Education Statistics'
}

map_media_type = {
    'zip' : "application/zip",
    'txt' : "text/plain",
    'pdf' : "application/pdf",
    'xls' : "application/vnd.ms-excel",
    'xlsx' : "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    'csv' : "text/csv",
    'sas': 'application/sas-syntax-file',
    'dat': 'text/generic-data-file',
    'spss': 'application/spss-syntax',  # This may be an incorrect extension, but we will continue to search for it
    'db.': 'application/generic-data-base',
    'sql': 'text/structured-query-language-file',
    'xml': 'application/xml',
    'sps': 'application/spss-syntax',
    'sav': 'application/spss-data',
    'do': 'application/stata-syntax',
    'r': 'text/r-script',
    'rdata': 'text/r-data',
    'rda': 'text/r-data',
    'sd2': 'application/sas-data',
    'sd7': 'application/sas-data',
    'sas7bdat': 'application/sas-data'
}

def get_office_name(target_dept):
    return map_office_name.get(target_dept)

def get_media_type(format):
    return map_media_type.get(format)

def transform_download_url(download_url, source_url):
    return urljoin(source_url,download_url)

def url_is_absolute(url):
    return bool(urlparse(url).netloc)

def traverse_output(target=None):
    if target is None:
        results = pathlib.Path(f'./output').rglob('*.json')
    else:
        results = pathlib.Path(f'./output/{target}').glob('**/*.json')

    files_list = [f for f in results
                  if 'print' not in str(f).split('/')[-1].split('-')
                  and 'data.json' not in str(f)
                  and 'statistics.json' not in str(f)]
    return files_list

def read_file(file_path):
    with open(file_path, 'r') as fl:
        data = json.load(fl)
        return data

def transform_keywords(tags_string):

    keywords = list()
    for tag in tags_string.split(';'):
        tag = tag.strip()
        tag = tag.lower()
        tag = tag.replace(' ','-')
        if tag:
            keywords.append(tag)

    return keywords

def transform_dataset_title(title, url):

    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path

    slug = slugify(domain + path)
    new_title = slug

    if title:
        new_title = title + ' (' + slug + ')'
    
    return new_title
        

def transform_dataset_identifier(title, url):

    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    path = parsed_url.path

    if title:
        return slugify(title + '-' + domain + path)
    else:
        return slugify(domain + path)

def extract_resource_format_from_url(url):
    
    parsed_url = urlparse(url)
    base = os.path.basename(parsed_url.geturl())

    ### rsplit on base name to support multiple periods
    base_name_lst = base.rsplit('.', 1)

    if len(base_name_lst) == 0:
        ### return a default format
        return 'txt'
    
    extension = base_name_lst[-1]

    ### accepting only 5 char extensions
    if len(extension) < 6:
        return extension
    else:
        ### return a default format
        return 'txt'

def extract_resource_name_from_url(url):
    
    parsed_url = urlparse(url)
    base = os.path.basename(parsed_url.geturl())

    ### rsplit on base name to support multiple periods
    base_name_lst = base.rsplit('.', 1)
    
    if len(base_name_lst) == 0:
        ### return a default name
        ### slugify the url and return as a name
        return slugify(parsed_url.geturl())

    name = base_name_lst[0]

    if name:
        return name
    else:
        ### return a default name
        ### slugify the url and return as a name
        return slugify(parsed_url.geturl())
