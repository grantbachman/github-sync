import requests
import config
import json
from github3 import GitHub
import re


class GitHubEvent(object):

    def __init__(self, event=None):
        self.event = event
        self.owner = 'rentjungle'

    def handle_issue_opened(self):
        # parse event
        title = self.event['issue']['title']
        description = self.event['issue']['body']
        poster = self.event['sender']['login']
        repo = self.event['repository']['name']
        issue_number = self.event['issue']['number']

        # send to pivotal
        piv_description = self.mod_description_for_pivotal(description, repo, issue_number, poster)
        piv = Pivotal(token=config.PIVOTAL_TOKEN)
        piv_project_id = config.project_mappings[repo]
        resp = piv.create_story(piv_project_id, title, piv_description)
        resp_json = resp.json()
        piv_story_id = resp_json['id']

        # Update GitHub with Pivotal ID
        g = GitHub(token=config.GITHUB_TOKEN)
        repo = g.repository(self.owner, repo)
        issue = repo.issue(issue_number)
        issue.edit(body=self.mod_description_for_github(description, piv_project_id, piv_story_id))

    @staticmethod
    def _get_pivotal_ids(text):
        """Given the body of a github issue, parse out the pivotal project/story
        :param text: A Github issue description text
        :return: pivotal_project_id, pivotal_story_id tuple
        """
        search_results = re.search('pivotaltracker.*projects/(\d+)/stories/(\d+)', text)
        if search_results:
            project_id, story_id = search_results.groups()
            return int(project_id), int(story_id)
        return None, None

    def handle_issue_comment_created(self):
        # parse event
        issue_body = self.event['issue']['body']
        comment_body = self.event['comment']['body']
        poster = self.event['comment']['user']['login']
        project_id, story_id = self._get_pivotal_ids(issue_body)
        p = Pivotal(token=config.PIVOTAL_TOKEN)
        piv_comment_body = self.mod_comment_for_pivotal(comment_body, poster)
        p.create_comment(project_id, story_id, piv_comment_body)

    @staticmethod
    def mod_comment_for_pivotal(text, poster):
        before = 'GitHub comment by **{}**:\n\n'.format(poster)
        return before + text

    @staticmethod
    def mod_description_for_pivotal(text, repo, issue_number, poster):
        """Modifies description to display a Github link to this issue
        """
        before = 'GitHub issue opened by **{}**:\n\n'.format(poster)
        after_template = '\n\nGitHub Issue [#{num}](https://github.com/rentjungle/{repo}/issues/{num})'
        after = after_template.format(repo=repo, num=issue_number)
        return before + text + after

    @staticmethod
    def mod_description_for_github(text, project_id, story_id):
        """Modifies description to display a Pivotal link to this issue
        """
        template = '\n\nPivotal Story [#{story_id}](https://www.pivotaltracker.com/projects/{project_id}/stories/{story_id})'
        tag = template.format(project_id=project_id, story_id=story_id)
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


