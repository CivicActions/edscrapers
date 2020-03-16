import os
import json
import pathlib

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
    'xlsx' : "application/vnd.ms-excel",
    'csv' : "text/csv",
    'sas': 'application/sas-syntax-file',
    'dat': 'text/generic-data-file',
    'spss': 'application/spss-syntax',  # This may be an incorrect extension, but we will continue to search for it
    'db.': 'application/generic-data-base',
    'sql': 'text/structured-query-language-file',
    'xml': 'text/extensible-markup-language',
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
        results = Path(os.path.join(OUTPUT_DIR, 'scrapers')).rglob('*.json')
    else:
        results = Path(os.path.join(OUTPUT_DIR, 'scrapers', target)).glob('**/*.json')

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

def extract_format_from_url(url):
    path = urlparse(url).path
    extension = path.split('.')[-1]
    if len(extension) < 5:
        return extension
    else:
        return None
