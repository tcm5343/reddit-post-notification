import time
from types import SimpleNamespace

import pytest

import reddit_post_notification as r

# to run the tests, simply type `pytest` in the directory


@pytest.fixture
def get_time_stamp() -> str:
    return r.get_time_stamp(time.time())


@pytest.mark.parametrize("keyword_list, test_string, expected_result", [
    (["tHis", "string"], "This is a string", True),
    ([""], "This is a string", True),
    (["this", "string"], "", False),
    (["i"], "This is a string", True),
    ([], "This is a string", False)
    ])
def test_string_contains_an_element_in_list(keyword_list, test_string, expected_result):
    assert r.string_contains_an_element_in_list(keyword_list, test_string) == expected_result


@pytest.mark.parametrize("keyword_list, test_string, expected_result", [
    (["tHis", "string"], "This is a string", True),
    ([""], "This is a string", True),
    (["this", "string"], "", False),
    (["This", "not"], "This is a string", False),
    ([], "This is a string", False)
    ])
def test_string_contains_every_element_in_list(keyword_list, test_string, expected_result):
    assert r.string_contains_every_element_in_list(keyword_list, test_string) == expected_result


@pytest.mark.parametrize("single_filter, expected_result", [
    ({"notify": ["1580989241"]}, ["1580989241"]),
    ({"includes": ["wts"]}, []),
    ({"notify": ["1580989241", "345234523"]}, ["1580989241", "345234523"]),
    ({"notify": []}, [])
    ])
def test_determine_who_to_notify(single_filter, expected_result):
    assert r.determine_who_to_notify(single_filter) == expected_result


@pytest.mark.parametrize("received_result, expected_result", [
    (time.mktime(time.strptime("2020-3-11 13:0:0", "%Y-%m-%d %H:%M:%S")), "03-11-2020 01:00:00 PM"),
    (time.mktime(time.strptime("1999-7-11 0:0:0", "%Y-%m-%d %H:%M:%S")), "07-11-1999 12:00:00 AM"),
    (time.mktime(time.strptime("2020-3-11 12:0:0", "%Y-%m-%d %H:%M:%S")), "03-11-2020 12:00:00 PM"),
    (time.mktime(time.strptime("2020-3-11 23:0:0", "%Y-%m-%d %H:%M:%S")), "03-11-2020 11:00:00 PM"),
    (time.mktime(time.strptime("2020-3-9 7:1:43", "%Y-%m-%d %H:%M:%S")), "03-09-2020 07:01:43 AM")
    ])
def test_get_time_stamp(received_result, expected_result):
    assert r.get_time_stamp(received_result) == expected_result


@pytest.mark.parametrize("post, subreddit, expected_result", [
    ({"title": "[WTS] Guitar"}, "GuitarSwap", " - GuitarSwap - [WTS] Guitar"),
    ({"title": ""}, "GuitarSwap", " - GuitarSwap - "),
    ({"title": "[WTS] Guitar"}, "", " -  - [WTS] Guitar")
    ])
def test_create_result_output(post, subreddit, expected_result, get_time_stamp):
    post_obj = SimpleNamespace(**post)
    expected_result = get_time_stamp + expected_result
    assert r.create_result_output(post_obj, subreddit) == expected_result
