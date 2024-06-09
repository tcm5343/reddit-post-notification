from unittest.mock import patch, PropertyMock

import pytest

from submission_filter.submission_filter import SubmissionFilter
from submission_filter import submission_filter


@pytest.fixture(autouse=True, name='mock_submission')
def f_mock_submission():
    with patch.object(submission_filter, 'Submission') as mock:
        yield mock


@pytest.mark.parametrize("test_title, test_filter, expected", [
    ("abc", ["^abc$"], True),
    ("abc", ["b"], True),
    ("abc", [".*"], True),
    ("abc", [""], True),
    ("abc", ["^abcd$"], False),
    ("", ["d"], False),
])
def test_regex(test_title, test_filter, expected, mock_submission):
    filter_def = {
        'title': {
            'regex': [test_filter]
        }
    }
    sub_filter = SubmissionFilter('some-filter', filter_def)
    mock_submission.title = test_title
    assert sub_filter.eval(mock_submission) == expected


@pytest.mark.parametrize("test_title, test_filter, expected", [
    ("abc", ["abc"], True),
    ("abc", ["b"], True),
    ("abc", [""], True),
    ("abc", ["d"], False),
    ("", ["d"], False),
])
def test_includes(test_title, test_filter, expected, mock_submission):
    filter_def = {
        'title': {
            'includes': [test_filter]
        }
    }
    sub_filter = SubmissionFilter('some-filter', filter_def)
    mock_submission.title = test_title
    assert sub_filter.eval(mock_submission) == expected


@pytest.mark.parametrize("test_title, test_filter, expected", [
    ("abc", ["abc"], False),
    ("abc", ["b"], False),
    ("abc", [''], False),
    ("abc", ["d"], True),
    ("", ["d"], True),
])
def test_excludes(test_title, test_filter, expected, mock_submission):
    filter_def = {
        'title': {
            'excludes': [test_filter]
        }
    }
    sub_filter = SubmissionFilter('some-filter', filter_def)
    mock_submission.title = test_title
    assert sub_filter.eval(mock_submission) == expected


def test_only_one_filter_passing_is_false(mock_submission):
    filter_def = {
        'title': {
            'includes': [['some']],
            'excludes': [['title']]
        }
    }
    sub_filter = SubmissionFilter('some-filter', filter_def)
    mock_submission.title = "some title"
    assert sub_filter.eval(mock_submission) is False


@pytest.mark.parametrize("post_part, test_filter, expected", [
    ("have", ["something"], True),
    ("have", ["else"], False),
    ("want", ["else"], True),
    ("want", ["something"], False),
    ("title", ['[h] something [w] else'], True),
    ("title", ['some text of'], False),
    ("body", ["some text of"], True),
    ("body", ["[h] something [w]"], False),
    ("post", ["some text of"], True),
    ("post", ["[h] something [w] else"], True),
    ("post", ["test.xyz"], False),
    ("url", ["test.xyz"], True),
    ("url", ["something.com"], False),
])
def test_all_parts_of_post(post_part, test_filter, expected, mock_submission):
    filter_def = {
        post_part: {
            'includes': [test_filter]
        }
    }
    mock_submission.title = "[h] something [w] else"
    mock_submission.selftext = "some text of the post"
    mock_submission.url = 'test.xyz/some/page.html?id=1'

    assert SubmissionFilter('some-filter', filter_def).eval(mock_submission) == expected


def test_one_part_matching_evals_true(mock_submission):
    filter_def = {
        "title": {  # doesn't match
            'includes': [["xyz"]]
        },
        "body": {  # matches
            'includes': [["some body"]]
        }
    }
    mock_submission.title = "some title"
    mock_submission.selftext = "some body"

    assert SubmissionFilter('some-filter', filter_def).eval(mock_submission) is True


def test_string_parts_are_lazily_evaluated(mock_submission):
    selftext_mock = PropertyMock()
    type(mock_submission).selftext = selftext_mock
    url_mock = PropertyMock()
    type(mock_submission).url = url_mock
    title_mock = PropertyMock()
    type(mock_submission).title = title_mock

    SubmissionFilter('some-filter', {}).eval(mock_submission)

    selftext_mock.assert_not_called()
    url_mock.assert_not_called()
    title_mock.assert_called_once()
