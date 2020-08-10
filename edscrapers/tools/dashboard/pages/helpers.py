from edscrapers.scrapers.edgov.offices_map import offices_map 
from edscrapers.transformers.base.helpers import map_office_name

def get_office_title(office_name):

    # search for the long name (eg. Office of Civil Rights (OCR))
    # returns it
    if office_name in offices_map.keys():
        return office_name

    # search for the long name (eg. Office of Civil Rights)
    # sets the short name (eg. ocr) and go to the next iteration
    for key,value in map_office_name.items():
        if value == office_name:
            office_name = key
            if office_name == 'nces':
                return 'National Center for Education Statistics (NCES)'
            break

    # search for the short name (eg. ocr)
    # returns the long name (eg. Office of Civil Rights (OCR))
    for key,value in offices_map.items():
        if value.get('name') == office_name:
            return key

    return office_name


def mapped_publisher_name(df):

    publisher_titles = []

    publisher_rows = df['publisher']
    for row in publisher_rows:
        publisher_titles.append(get_office_title(row))
    
    df['publisher'] = publisher_titles
    return df