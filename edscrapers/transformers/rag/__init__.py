import functools

# create the dataset weighting system
# NOTE: 'dataset_key' is for the raw/parsed dataset;
# while 'datajson_key' is for the processed/transformed datajson
DATASET_WEIGHTING_SYS = {'Title': 
                            {'dataset_key': 'title',
                            'datajson_key': 'title', 
                            'score': 10}, 
                         'Description':
                            {'dataset_key': 'notes', 
                            'datajson_key': 'description',
                            'score': 9}, 
                         'Created':
                            {'dataset_key': 'date', 
                            'datajson_key': 'modified',
                            'score': 5},
                         'Publisher': 
                            {'dataset_key': 'publisher', 
                            'datajson_key': 'publisher',
                            'score': 8.5}, 
                         'Program code': 
                            {'dataset_key': '', 
                            'datajson_key': 'programCode',
                            'score': 1}, 
                         'Bureau code': 
                            {'dataset_key': '', 
                            'datajson_key': 'bureauCode',
                            'score': 1},
                         'Data level': 
                            {'dataset_key': '', 
                            'datajson_key': '',
                            'score': 7}, 
                         'Organization': 
                            {'dataset_key': '', 
                            'datajson_key': '',
                            'score': 8.5}, 
                         'License': 
                            {'dataset_key': '',
                            'datajson_key': 'license',
                            'score': 4},
                         'Frequency': 
                            {'dataset_key': '', 
                            'datajson_key': '',
                            'score': 5},
                         'Helpdesk Phone':
                            {'dataset_key': '',
                            'datajson_key': '',
                            'score': 4}, 
                         'Helpdesk Email': 
                            {'dataset_key': '', 
                            'datajson_key': '',
                            'score':4},
                         'Data Steward Name': 
                            {'dataset_key': 'contact_person_name', 
                            'datajson_key': 'contactPoint',
                            'score': 4},
                         'Data Steward Email': 
                            {'dataset_key': 'contact_person_email', 
                            'datajson_key': 'contactPoint',
                            'score': 4},
                         'Access level': 
                            {'dataset_key': '', 
                            'datajson_key': 'accessLevel',
                            'score': 1},
                         'Spatial': 
                            {'dataset_key': '',
                            'datajson_key': 'spatial',
                            'score': 6},
                         'Data Period / Start': 
                            {'dataset_key': '', 
                            'datajson_key': 'temporal',
                            'score': 10},
                         'Data Period / End': 
                            {'dataset_key': '', 
                            'datajson_key': 'temporal',
                            'score': 10},
                         'Tags': 
                            {'dataset_key': 'tags', 
                            'datajson_key': 'keyword',
                            'score': 9.5},
                         'Categories': 
                            {'dataset_key': '',
                            'datajson_key': 'theme',
                            'score': 9.5}
                         }

# calculate the total weight
TOTAL_WEIGHT = functools.reduce(lambda item1, item2: item1 + item2[2]['score'], 
                                                          DATASET_WEIGHTING_SYS.items(), 0)
