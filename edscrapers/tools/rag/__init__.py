import functools

# create the dataset weighting system
DATASET_WEIGHTING_SYS = {'Title': {'dataset_key': 'title', 'score': 10}, 
                         'Description':{'dataset_key': 'notes', 'score': 9}, 
                         'Created':{'dataset_key': 'date', 'score': 5},
                         'Publisher': {'dataset_key': 'publisher', 'score': 8.5}, 
                         'Program code': {'dataset_key': '', 'score': 1}, 
                         'Bureau code': {'dataset_key': '', 'score': 1},
                         'Data level': {'dataset_key': '', 'score': 7}, 
                         'Organization': {'dataset_key': '', 'score': 8.5}, 
                         'License': {'dataset_key': '', 'score': 4},
                         'Frequency': {'dataset_key': '', 'score': 5},
                         'Helpdesk Phone':{'dataset_key': '', 'score': 4}, 
                         'Helpdesk Email': {'dataset_key': '', 'score':4},
                         'Data Steward Name': {'dataset_key': 'contact_person_name', 'score': 4},
                         'Data Steward Email': {'dataset_key': 'contact_person_email', 'score': 4},
                         'Access level': {'dataset_key': '', 'score': 1},
                         'Spatial': {'dataset_key': '', 'score': 6},
                         'Data Period / Start': {'dataset_key': '', 'score': 10},
                         'Data Period / End': {'dataset_key': '', 'score': 10},
                         'Tags': {'dataset_key': 'tags', 'score': 9.5},
                         'Categories': {'dataset_key': '', 'score': 9.5}
                         }

# calculate the total weight
TOTAL_WEIGHT = functools.reduce(lambda item1, item2: item1 + item2[1]['score'], 
                                                          DATASET_WEIGHTING_SYS.items(), 0)