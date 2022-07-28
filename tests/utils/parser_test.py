import pytest
from utils.parser import string_contains_every_element_in_list, \
    string_contains_an_element_in_list


@pytest.mark.parametrize("keyword_list, test_string, expected_result", [
    (["tHis", "string"], "This is a string", True),
    ([""], "This is a string", True),
    (["this", "string"], "", False),
    (["i"], "This is a string", True),
    ([], "This is a string", False)
    ])
def test_string_contains_an_element_in_list(keyword_list, test_string, expected_result):
    actual_result = string_contains_an_element_in_list(keyword_list, test_string)
    assert expected_result == actual_result


@pytest.mark.parametrize("keyword_list, test_string, expected_result", [
    (["tHis", "string"], "This is a string", True),
    ([""], "This is a string", True),
    (["this", "string"], "", False),
    (["This", "not"], "This is a string", False),
    ([], "This is a string", False)
    ])
def test_string_contains_every_element_in_list(keyword_list, test_string, expected_result):
    actual_result = string_contains_every_element_in_list(keyword_list, test_string)
    assert expected_result == actual_result
