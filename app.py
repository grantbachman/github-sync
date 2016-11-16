from flask import Flask, request
from models import GitHubEvent


app = Flask(__name__)


@app.route('/github/hook', methods=['POST'])
def github_issue():
    event = request.get_json()

    g = GitHubEvent(event)

    # only handle issue events for now
    event_type = request.headers.get('X-GitHub-Event')
    if event_type == 'issues':
        if event['action'] == 'opened':
            g.handle_issue_opened()
        if event['action'] == 'created':
            g.handle_issue_comment_created()
        if event['action'] == 'closed':
            g.handle_issue_closed()
    elif event_type == 'create' and event.get('ref_type') == 'branch':
        g.handle_branch_create()

    return "Thanks."


@app.route('/pivotal/hook', methods=['POST'])
def pivotal_story():
    return 'Hi'


if __name__ == '__main__':
    app.run(debug=True, port=4567)
