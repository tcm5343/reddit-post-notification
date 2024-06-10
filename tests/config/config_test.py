from unittest.mock import patch, PropertyMock, mock_open

import pytest

from config import config


@pytest.fixture(autouse=True, name='mock_submission')
def f_mock_submission():
    with patch.object(config, 'Submission') as mock:
        yield mock


@pytest.fixture(autouse=True, name='mock_submission_filter')
def f_mock_submission_filter():
    with patch.object(config, 'SubmissionFilter') as mock:
        yield mock


@pytest.fixture(autouse=True, name='mock_telegram_notifier')
def f_mock_telegram_notifier():
    with patch.object(config, 'TelegramNotifier') as mock:
        yield mock


@pytest.fixture(name='mock_open')
def f_mock_open():
    with patch("builtins.open", mock_open(read_data="data")) as mock:
        assert open("path/to/open").read() == "data"
