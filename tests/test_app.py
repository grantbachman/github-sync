import context
import app
import json


def test_create_issue():
    with open('tests/static/github/issue_opened.json') as f:
        event = json.load(f)
    issue = app.create_issue(event)
    assert issue.title == 'Test Issue'
    assert issue.description == 'Issue description.'
    assert issue.poster == 'grantbachman'


