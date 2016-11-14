from flask import Flask, request, json
from models import Issue

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
    return issue


def handle_issue_opened(event):
    return create_issue(event)


@app.route('/payload', methods=['POST'])
def github_issue():
    event = request.get_json()
    print json.dumps(event)
    return "Thanks."

if __name__ == '__main__':
    app.run(debug=True, port=4567)
