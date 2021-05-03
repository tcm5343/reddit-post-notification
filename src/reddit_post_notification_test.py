from types import SimpleNamespace

import pytest
import time
from datetime import datetime
from unittest import mock

import src.reddit_post_notification as r

# to run the tests, simply type `pytest` in the directory


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
    (datetime(2020, 3, 11, 13, 0, 0), "03-11-2020 01:00:00 PM"),
    (datetime(1999, 7, 11, 0, 0, 0), "07-11-1999 12:00:00 AM"),
    (datetime(2020, 3, 11, 12, 0, 0), "03-11-2020 12:00:00 PM"),
    (datetime(2020, 3, 11, 23, 0, 0), "03-11-2020 11:00:00 PM"),
    (datetime(2020, 3, 9, 7, 1, 0), "03-09-2020 07:01:00 AM"),
    (time.mktime(time.strptime("2020-3-11 13:0:0", "%Y-%m-%d %H:%M:%S")), "03-11-2020 01:00:00 PM"),
    (time.mktime(time.strptime("1999-7-11 0:0:0", "%Y-%m-%d %H:%M:%S")), "07-11-1999 12:00:00 AM"),
    (time.mktime(time.strptime("2020-3-11 12:0:0", "%Y-%m-%d %H:%M:%S")), "03-11-2020 12:00:00 PM"),
    (time.mktime(time.strptime("2020-3-11 23:0:0", "%Y-%m-%d %H:%M:%S")), "03-11-2020 11:00:00 PM"),
    (time.mktime(time.strptime("2020-3-9 7:1:43", "%Y-%m-%d %H:%M:%S")), "03-09-2020 07:01:43 AM")
    ])
def test_get_time_stamp(received_result, expected_result):
    assert r.get_time_stamp(received_result) == expected_result


@pytest.mark.parametrize("test_date, post, subreddit, expected_result", [
    (datetime(2020, 3, 11, 13, 0, 0), {"title": "[WTS] Guitar"}, "GuitarSwap",
     "03-11-2020 01:00:00 PM - GuitarSwap - [WTS] Guitar"),
    (datetime(2020, 3, 11, 13, 0, 0), {"title": ""}, "GuitarSwap", "03-11-2020 01:00:00 PM - GuitarSwap - "),
    (datetime(2020, 3, 11, 13, 0, 0), {"title": "[WTS] Guitar"}, "", "03-11-2020 01:00:00 PM -  - [WTS] Guitar")
    ])
def test_create_result_output(test_date, post, subreddit, expected_result):
    post_obj = SimpleNamespace(**post)
    assert r.create_result_output(post_obj, subreddit, test_date) == expected_result


@pytest.mark.parametrize("post_title, expected_result", [
    ("[USA-TX] [H] 5700 XT 50th Anniversary Edition, Ryzen 7 2700x [W] Local Cash",
     " 5700 xt 50th anniversary edition, ryzen 7 2700x "),
    ("[USA-MS] [H] Paypal [W] Arctic Liquid Freezer II 360", " paypal "),
    ("[USA-GA][H] Lots of SSDs, G4400, 2x i5-6500, i3-6100, E5-2609V4, SATA HDDs, SAS HDDs [W] PayPal",
     " lots of ssds, g4400, 2x i5-6500, i3-6100, e5-2609v4, sata hdds, sas hdds "),
    ("[USA-VA] [H] RTX 3060 White [W] Local Cash / Possibly Asus G14",
     " rtx 3060 white "),
    ("[USA-TX] this doesn't have it [w] this won't be scanned", "sa-tx] this doesn't have it ")
])
def test_parse_title_for_have(post_title, expected_result):
    assert r.parse_title_for_have(post_title) == expected_result


@pytest.mark.parametrize("post_title, expected_result", [
    ("[USA-TX] [H] 5700 XT 50th Anniversary Edition, Ryzen 7 2700x [W] Local Cash",
     " local cash"),
    ("[USA-MS] [H] Paypal [W] Arctic Liquid Freezer II 360", " arctic liquid freezer ii 360"),
    ("[USA-GA][H] Lots of SSDs, G4400, 2x i5-6500, i3-6100, E5-2609V4, SATA HDDs, SAS HDDs [W] PayPal",
     " paypal"),
    ("[USA-VA] [H] RTX 3060 White [W] Local Cash / Possibly Asus G14",
     " local cash / possibly asus g14"),
    ("[USA-TX] this doesn't have it", "sa-tx] this doesn't have it")
])
def test_parse_title_for_want(post_title, expected_result):
    assert r.parse_title_for_want(post_title) == expected_result


@pytest.mark.parametrize("attribute, title, val, expected_result", [
    ("includes", "this is an example", ["example"], True),
    ("includes", "this is an example", ["keyboard"], False),
    ("excludes", "this is an example", ["keyboard"], True),
    ("excludes", "this is an example", ["example"], False),
    ("have", "[h] this is an example [w] this is nothing", ["example"], True),
    ("have", "[h] this is an example [w] this is nothing", ["nothing"], False),
    ("want", "[h] this is an example [w] this is nothing", ["example"], False),
    ("want", "[h] this is an example [w] this is nothing", ["nothing"], True),
])
def test_handle_filter_attributes(attribute, title, val, expected_result):
    assert r.handle_filter_attributes(attribute, title, val) == expected_result
