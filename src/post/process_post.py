from copy import deepcopy
from datetime import datetime
from multiprocessing import Queue
from threading import Thread

from praw.models import Submission

from config.parse_config import determine_who_to_notify, handle_filter_attributes
from utils.logging import create_post_found_console_message
from utils.notification import send_notification


def __filter_post(post: Submission, specific_filter: dict, queue: Queue):
    # default flag initializations
    result = False
    post_title = post.title.lower()

    results_list = []

    for key, value in specific_filter.items():
        results_list.append(handle_filter_attributes(key, post_title, value))

    queue_dict = queue.get()

    # if a result has been found
    if False not in results_list:
        result = True
        queue_dict["who_to_notify"] = determine_who_to_notify(specific_filter)

    queue_dict["notify"] = result
    queue.put(queue_dict)


def __post_found(post, subreddit: str, who_to_notify: list, notification_config: dict) -> None:
    print(create_post_found_console_message(post.title, subreddit, datetime.now()))
    send_notification(who_to_notify, post, notification_config)


def process_submission(submission: Submission, subreddit_name: str, config: dict):
    number_of_filters = len(config["search"][subreddit_name]["filters"])
    queue = Queue()
    print("number of filters processed:", number_of_filters)

    threads = []
    return_vals = {
        "notify": False,
        "who_to_notify": set()
    }

    for filter_index in range(number_of_filters):
        ret = deepcopy(return_vals)
        queue.put(ret)

        thread = Thread(
            target=__filter_post,
            args=(submission, config["search"][subreddit_name]["filters"][filter_index], queue)
        )

        threads.append(thread)
        threads[filter_index].start()

    # when a thread is finished, a record is pulled off the queue and processed
    for thread in threads:
        thread.join()
        ret = queue.get()

        if ret["notify"]:
            return_vals["notify"] = True
            return_vals["who_to_notify"].update(set(ret["who_to_notify"]))

    if return_vals["notify"]:
        notification_config = config["notifications"]
        __post_found(submission, subreddit_name, list(return_vals["who_to_notify"]),
                     notification_config)
