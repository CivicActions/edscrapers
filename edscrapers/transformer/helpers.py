

map_office_name = {
    'ocr' : "Office for Civil Rights",
    'edoctae' : "Office of Career, Technical and Adult Education"
}

def get_office_name(target_dept):

    return map_office_name.get(target_dept)