import context
import app
import json
from models import Issue, Pivotal
import mock


def test_create_issue():
    with open('tests/static/github/issue_opened.json') as f:
        event = json.load(f)
    issue = app.create_issue(event)
    assert issue.title == 'Test Issue'
    assert issue.description == 'Issue description.'
    assert issue.poster == 'grantbachman'


class TestIssue(object):
    def test_mod_description_for_pivotal(self):
        issue = Issue(title='Title', description='Description', poster='grantbachman',
                      number=1, repository='my_repo')
        desc = 'Description\n\nGitHub Issue [#1](https://github.com/rentjungle/my_repo/issues/1)'
        assert issue.mod_description_for_pivotal() == desc


class TestPivotal(object):

    @mock.patch('requests.post')
    def test_create_story(self, mock_post):
        p = Pivotal(token='token')
        issue = Issue(title='Title', description='Description', poster='grantbachman')
        issue.description = issue.mod_description_for_pivotal()
        p.create_story(issue, 1)
        posted_data = json.dumps({'name': issue.title, 'description': issue.description})
        mock_post.assert_called_with(url=Pivotal.BASE_URL + '/projects/1/stories',
                                     headers=p.headers,
                                     data=posted_data)


