from urllib.parse import urlparse

map_office_name = {
    'ocr' : "Office for Civil Rights",
    'edoctae' : "Office of Career, Technical and Adult Education"
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

def transform_download_url(target_dept, download_url, source_url):

    if target_dept == list(map_office_name.keys())[0]: #ocr
        download_url = download_url[2:]
        return source_url + download_url

    elif target_dept == list(map_office_name.keys())[1]: #edoctae
        return "https://www2.ed.gov" + download_url

def url_is_absolute(url):
    return bool(urlparse(url).netloc)