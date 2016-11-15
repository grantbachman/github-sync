from flask import Flask, request, json
from models import Issue, Pivotal
import config
import requests

app = Flask(__name__)


def create_issue(event):
    """Creates an Issue from a github event
    :param event: A github event
    :return: an Issue instance
    """
    issue = Issue()
    issue.title = event['issue']['title']
    issue.description = event['issue']['body']
    issue.poster = event['sender']['login']
    issue.repository = event['repository']['name']
    issue.number = event['issue']['number']
    return issue


def github_issue_created(event):
    """Create a Pivotal story from a Github issue.
    :param event: A Github event
    :return:
    """
    issue = create_issue(event)
    piv = Pivotal(token=config.PIVOTAL_TOKEN)
    piv_project_id = piv.get_project_id(issue, config.project_mappings)
    resp = piv.create_story(issue, piv_project_id)
    print 'Pivotal returned {}. {}'.format(resp.status_code, resp.text)



@app.route('/github/hook', methods=['POST'])
def github_issue():
    event = request.get_json()

    if event['action'] in ('opened', 'reopened'):
        github_issue_created(event)

    return "Thanks."

if __name__ == '__main__':
    app.run(debug=True, port=4567)
