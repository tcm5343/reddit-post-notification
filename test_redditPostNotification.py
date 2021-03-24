import pytest, datetime
import redditPostNotification as r
from types import SimpleNamespace

@pytest.mark.parametrize("keyword_list, test_string, expected_result", [
    (["tHis","string"], "This is a string", True),
    ([""], "This is a string", True),
    (["this","string"], "", False),
    (["i"], "This is a string", True),
    ([], "This is a string", False)
    ])
def test_stringContainsAnElementInList(keyword_list, test_string, expected_result):
    assert r.stringContainsAnElementInList(keyword_list, test_string) == expected_result

@pytest.mark.parametrize("keyword_list, test_string, expected_result", [
    (["tHis","string"], "This is a string", True),
    ([""], "This is a string", True),
    (["this","string"], "", False),
    (["This","not"], "This is a string", False),
    ([], "This is a string", False)
    ])
def test_stringContainsEveryElementInList(keyword_list, test_string, expected_result):
    assert r.stringContainsEveryElementInList(keyword_list, test_string) == expected_result

@pytest.mark.parametrize("filter, expected_result", [
    ({"notify": ["1580989241"]}, ["1580989241"]),
    ({"includes": ["wts"]},[]),
    ({"notify": ["1580989241","345234523"]}, ["1580989241","345234523"]),
    ({"notify": []}, [])
    ])
def test_determineWhoToNotify(filter, expected_result):
    assert r.determineWhoToNotify(filter) == expected_result

@pytest.mark.parametrize("post, subreddit", [
    ({"title": "[WTS] Guitar"}, "GuitarSwap"),
    ({"title": ""}, "GuitarSwap"),
    ({"title": "[WTS] Guitar"}, "")
    ])
def test_createResultOutput(post, subreddit):
    p = SimpleNamespace(**post)
    assert r.createResultOutput(p, subreddit) == r.getTimeStamp(datetime.datetime.now()) + " - " + subreddit + " - " + p.title

@pytest.mark.parametrize("time, expected_result", [
    ( datetime.datetime(2020, 3, 11, 14, 0, 0), "3-11-2020 2:00 PM"),
    ( datetime.datetime(1999, 7, 11, 0, 0, 0), "7-11-1999 12:00 AM"),
    ( datetime.datetime(2020, 3, 11, 11, 0, 0), "3-11-2020 12:00 PM"),
    ( datetime.datetime(2020, 3, 11, 23, 0, 0), "3-11-2020 11:00 PM")
    ])
def test_getTimeStamp(time, expected_result):
    assert r.getTimeStamp(time) == expected_result
    