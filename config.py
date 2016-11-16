import os

PIVOTAL_TOKEN = os.getenv('PIVOTAL_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# GitHub->Pivotal user names
user_mappings = {
    'grantbachman': 'grantbachman'
}

# Github Repo -> Privotal Project ID
_project_mappings = {
    'lead_parser': 922132
}

# Reverse keys/values for easy lookup
project_mappings = {}
for key, value in _project_mappings.items():
    project_mappings[key] = value
    project_mappings[value] = key
