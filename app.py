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
        g.handle_opened_issue()
    return "Thanks."



if __name__ == '__main__':
    app.run(debug=True, port=4567)
