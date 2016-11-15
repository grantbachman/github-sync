import requests
import config
import json


class Issue(object):

    def __init__(self, title=None, description=None, poster=None, repository=None, number=None):
        self.title = title
        self.description = description
        self.poster = poster
        self.repository = repository
        self.number = number

    def mod_description_for_pivotal(self):
        """Modifies description to display a link to this issue
        """
        template = '\n\nGitHub Issue [#{num}](https://github.com/rentjungle/{repo}/issues/{num})'
        tag = template.format(repo=self.repository, num=self.number)
        return self.description + tag


class Pivotal(object):

    BASE_URL = 'https://www.pivotaltracker.com/services/v5'

    def __init__(self, token=None):
        self.token = token
        self.headers = {'X-TrackerToken': self.token, 'Content-Type': 'application/json'}

    @staticmethod
    def get_project_id(github_issue, project_mappings):
        return project_mappings[github_issue.repository]

    def create_story(self, issue, project_id):
        """
        :param issue: An Issue object
        :param project_id: Pivotal Project ID
        :return:
        """
        issue.description = issue.mod_description_for_pivotal()
        to_post = {
            'name': issue.title,
            'description': issue.description
        }
        url = '{}/projects/{}/stories'.format(self.BASE_URL, project_id)
        resp = requests.post(url=url, headers=self.headers, data=json.dumps(to_post))
        return resp

