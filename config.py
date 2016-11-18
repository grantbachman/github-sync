import os

PIVOTAL_TOKEN = os.getenv('PIVOTAL_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# GitHub->Pivotal user names
user_mappings = {
    'grantbachman': 'grantbachman'
}

# Github Repo -> Privotal Project ID
_project_mappings = {
    'insights_beaver': 922132,
    'insights_app': 1434396,
    'rentjungle_web': 922134,
    'property-type-classifier': 922132,
    'insights_api': 1434396,
    'data_services': 922132,
    'reviewtracker': 922132,
    'lead_parser': 922132,
    'spider': 922132,
    'chef': 1452136,
    'reviewtracker_api': 922132
}

# Reverse keys/values for easy lookup
project_mappings = {}
for key, value in _project_mappings.items():
    project_mappings[key] = value
    project_mappings[value] = key
