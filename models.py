import requests
import json

class Issue(object):

    def __init__(self, title=None, description=None, poster=None):
        self.title = title
        self.description = description
        self.poster = poster


class Pivotal(object):

    BASE_URL = 'https://www.pivotaltracker.com/services/v5'

    def __init__(self, token=None):
        self.token = token

    def create_story(self, issue, project_id):
        """
        :param issue: An Issue object
        :param project_id: Pivotal Project ID
        :return:
        """
        to_post = {
            'name': issue.title,
            'description': issue.description
        }
        headers = {'X-TrackerToken': self.token, 'Content-Type': 'application/json'}
        url = '{}/projects/{}/stories'.format(self.BASE_URL, project_id)
        resp = requests.post(url=url, headers=headers, data=json.dumps(to_post))
        return resp

