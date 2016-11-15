from flask import Flask, request
from models import GitHubEvent


app = Flask(__name__)


@app.route('/github/hook', methods=['POST'])
def github_issue():
    event = request.get_json()

    g = GitHubEvent(event)

    # only handle issue events for now
    if request.headers.get('X-GitHub-Event') != 'issues':
        pass

    if event['action'] == 'opened':
        g.handle_issue_opened()
    if event['action'] == 'created':
        g.handle_issue_comment_created()
    return "Thanks."


@app.route('/pivotal/hook', methods=['POST'])
def pivotal_story():
    return 'Hi'


if __name__ == '__main__':
    app.run(debug=True, port=4567)
