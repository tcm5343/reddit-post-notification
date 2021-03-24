import pytest
import redditPostNotification as r

@pytest.mark.parametrize("keyword_list, test_string, expected_result", [
    (["tHis","string"], "This is a string", True),
    ([""], "This is a string", True),
    (["this","string"], "", False),
    (["i"], "This is a string", True)
    ])
def test_stringContainsAnElementInList(keyword_list, test_string, expected_result):
    result = r.stringContainsAnElementInList(keyword_list, test_string)
    assert result == expected_result

@pytest.mark.parametrize("keyword_list, test_string, expected_result", [
    (["tHis","string"], "This is a string", True),
    ([""], "This is a string", True),
    (["this","string"], "", False),
    (["This","not"], "This is a string", False)
    ])
def test_stringContainsEveryElementInList(keyword_list, test_string, expected_result):
    result = r.stringContainsEveryElementInList(keyword_list, test_string)
    assert result == expected_result

@pytest.mark.parametrize("filter, expected_result", [
    ({"notify": ["1580989241"]}, ["1580989241"]),
    ({"includes": ["wts"]},[]),
    ({"notify": ["1580989241","345234523"]}, ["1580989241","345234523"])
    ])
def test_determineWhoToNotify(filter, expected_result):
    result = r.determineWhoToNotify(filter)
    assert result == expected_result

