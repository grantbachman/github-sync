import context
import pytest
import app
import json
from models import Pivotal, GitHubEvent
import mock
import unittest

class TestGitHubEvent(object):

    def test_get_pivotal_ids(self):
        text = ('blah``` Pivotal Story [#134395067](https://www'
                '.pivotaltracker.com/projects/922132/stories/134395067) blah')
        ret = GitHubEvent._get_pivotal_ids(text)
        assert ret == (922132, 134395067)


class TestPivotal(object):

    @mock.patch('requests.post')
    def test_create_story(self, mock_post):
        p = Pivotal(token='token')
        title = 'Title'
        description = 'Description'
        p.create_story(1, title, description)
        posted_data = json.dumps({'name': title, 'description': description})
        mock_post.assert_called_with(url=Pivotal.BASE_URL + '/projects/1/stories',
                                     headers=p.headers,
                                     data=posted_data)

    @mock.patch('requests.post')
    def test_create_comment(self, mock_post):
        p = Pivotal(token='token')
        p.create_comment(1, 1, text='test')
        posted_data = json.dumps({'text': 'test'})
        mock_post.assert_called_with(url=Pivotal.BASE_URL + '/projects/1/stories/1/comments',
                                     headers=p.headers,
                                     data=posted_data)

