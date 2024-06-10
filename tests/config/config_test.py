from unittest.mock import patch, PropertyMock, mock_open

import pytest

from config.config import Config
from config import config as config_file


@pytest.fixture(autouse=True, name='mock_submission')
def f_mock_submission():
    with patch.object(config_file, 'Submission') as mock:
        yield mock


@pytest.fixture(autouse=True, name='mock_submission_filter')
def f_mock_submission_filter():
    with patch.object(config_file, 'SubmissionFilter') as mock:
        yield mock


@pytest.fixture(autouse=True, name='mock_telegram_notifier')
def f_mock_telegram_notifier():
    with patch.object(config_file, 'TelegramNotifier') as mock:
        yield mock


@pytest.fixture(autouse=True, name='mock_open')
def f_mock_open():
    data = """
    creds:
        notifiers:
            telegram:
                token: some-token
    reddit:
        client_id: some-client-id
        client_secret: some-client-secret
        password: some-password
        username: some-username
    who:
      telegram:
        jack: some-telegram-user-id
    filters:
      filter1:
        title:
          includes:
            - [wts]
        notify:
          telegram:
            - jack
      filter2:
        title:
          includes:
            - [wts]
        notify:
          telegram:
            - jack
    search:
      universal:
        - filter2
      subreddits:
        subreddit1:
          - filter1
    """
    with patch('builtins.open', mock_open(read_data=data)) as mock:
        yield mock


def test_config():
    config = Config('some/path')
    assert True
