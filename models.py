import requests
import config
import json
from github3 import GitHub


class GitHubEvent(object):

    def __init__(self, event=None):
        self.event = event
        self.owner = 'rentjungle'

    def event_handler(self):
        if self.event['action'] == 'opened':
            self.handle_opened_issue()

    def handle_opened_issue(self):
        # parse event
        title = self.event['issue']['title']
        description = self.event['issue']['body']
        poster = self.event['sender']['login']
        repo = self.event['repository']['name']
        issue_number = self.event['issue']['number']

        # send to pivotal
        piv_description = self.mod_description_for_pivotal(description, repo, issue_number)
        piv = Pivotal(token=config.PIVOTAL_TOKEN)
        piv_project_id = config.project_mappings[repo]
        resp = piv.create_story(piv_project_id, title, piv_description)
        resp_json = resp.json()
        piv_story_id = resp_json['id']

        # Update GitHub with Pivotal ID
        g = GitHub(token=config.GITHUB_TOKEN)
        repo = g.repository(self.owner, repo)
        issue = repo.issue(issue_number)
        issue.edit(body=self.mod_description_for_github(description, piv_story_id))

    @staticmethod
    def mod_description_for_pivotal(text, repo, issue_number):
        """Modifies description to display a Github link to this issue
        """
        template = '\n\nGitHub Issue [#{num}](https://github.com/rentjungle/{repo}/issues/{num})'
        tag = template.format(repo=repo, num=issue_number)
        return text + tag

    @staticmethod
    def mod_description_for_github(text, story_id):
        """Modifies description to display a Pivotal link to this issue
        """
        template = '\n\nPivotal Story [#{num}](https://www.pivotaltracker.com/story/show/{num})'
        tag = template.format(num=story_id)
        return text + tag


class Pivotal(object):

    BASE_URL = 'https://www.pivotaltracker.com/services/v5'

    def __init__(self, token=None):
        self.token = token
        self.headers = {'X-TrackerToken': self.token, 'Content-Type': 'application/json'}

    def create_story(self, project_id, title, description=None):
        """
        :param project_id: Pivotal Project ID
        :param title: title of story
        :param description: description of story
        :return: response of the Pivotal API
        """
        post = {
            'name': title,
            'description': description
        }
        url = '{}/projects/{}/stories'.format(self.BASE_URL, project_id)
        return requests.post(url=url, headers=self.headers, data=json.dumps(post))

    def create_comment(self, project_id, story_id, text=None):
        """
        :param project_id: Pivotal Project ID
        :param story_id: Pivotal Story ID
        :param text: text description
        :return: response of the Pivotal API
        """
        post = {'text': text}
        url = '{}/projects/{}/stories/{}/comments'.format(self.BASE_URL, project_id, story_id)
        return requests.post(url=url, headers=self.headers, data=json.dumps(post))


