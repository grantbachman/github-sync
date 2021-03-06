from flask import Flask, request, abort
from models import GitHubEvent


app = Flask(__name__)


@app.route('/hooks/github', methods=['POST'])
def github_issue():
    event = request.get_json()

    g = GitHubEvent(event)

    # only handle issue events for now
    event_type = request.headers.get('X-GitHub-Event')
    action = event.get('action')
    if event_type == 'issues':
        if action == 'opened':
            g.handle_issue_opened()
        elif action == 'created':
            g.handle_issue_comment_created()
        elif action == 'closed':
            g.handle_issue_closed()
    elif event_type == 'create' and event.get('ref_type') == 'branch':
        g.handle_branch_create()
    else:
        return "Unrecognized action."
    return "Thanks."


@app.route('/hooks/pivotal', methods=['POST'])
def pivotal_story():
    return abort(501)


@app.route('/', methods=['GET'])
def root():
    return 'Hello, World.'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
