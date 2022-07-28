from datetime import datetime
from time import strftime, localtime
from typing import Union


def __convert_ts_for_logs(now: Union[datetime, float] = datetime.now()) -> str:
    if isinstance(now, datetime):
        result = now.strftime("%m-%d-%Y %I:%M:%S %p")
    else:  # handles ts as float
        result = strftime("%m-%d-%Y %I:%M:%S %p", localtime(now))
    return result


def create_post_found_console_message(post_title, subreddit, timestamp=datetime.now()) -> str:
    message = __convert_ts_for_logs(timestamp) + " - " + subreddit + " - " + post_title
    return message
