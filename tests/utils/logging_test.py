from datetime import datetime
from unittest.mock import patch

import pytest

from utils.logging import __convert_ts_for_logs, create_post_found_console_message


@pytest.mark.parametrize("received_result, expected_result", [
    # from datetime
    (datetime(2020, 3, 11, 13, 0, 0), "03-11-2020 01:00:00 PM"),
    (datetime(1999, 7, 11, 0, 0, 0), "07-11-1999 12:00:00 AM"),
    (datetime(2020, 3, 11, 12, 0, 0), "03-11-2020 12:00:00 PM"),
    (datetime(2020, 3, 11, 23, 0, 0), "03-11-2020 11:00:00 PM"),
    (datetime(2020, 3, 9, 7, 1, 0), "03-09-2020 07:01:00 AM"),
    # from float (seconds since epoch)
    (datetime(2020, 3, 11, 13, 0, 0).timestamp(), "03-11-2020 01:00:00 PM"),
    (datetime(1999, 7, 11, 0, 0, 0).timestamp(), "07-11-1999 12:00:00 AM"),
    (datetime(2020, 3, 11, 12, 0, 0).timestamp(), "03-11-2020 12:00:00 PM"),
    (datetime(2020, 3, 11, 23, 0, 0).timestamp(), "03-11-2020 11:00:00 PM"),
    (datetime(2020, 3, 9, 7, 1, 0).timestamp(), "03-09-2020 07:01:00 AM"),
    ])
def test_get_time_stamp(received_result, expected_result):
    actual_result = __convert_ts_for_logs(received_result)
    assert expected_result == actual_result


@pytest.mark.parametrize("post_title, subreddit, timestamp, expected_result", [
    ("[WTS] Guitar", "GuitarSwap", '03-11-2020 01:00:00 PM',
     "03-11-2020 01:00:00 PM - GuitarSwap - [WTS] Guitar"),
    ("", "GuitarSwap", '03-11-2020 01:00:00 PM', "03-11-2020 01:00:00 PM - GuitarSwap - "),
    ("[WTS] Guitar", "", '03-11-2020 01:00:00 PM', "03-11-2020 01:00:00 PM -  - [WTS] Guitar")
    ])
@patch('utils.logging.__convert_ts_for_logs')
def test_create_result_output(mock_convert_ts_for_logs, timestamp, post_title, subreddit,
                              expected_result):
    mock_convert_ts_for_logs.return_value = timestamp
    actual_result = create_post_found_console_message(post_title, subreddit, timestamp)

    assert expected_result == actual_result
