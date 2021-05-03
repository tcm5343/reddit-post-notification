#!/usr/bin/python3
import sys

from threading import Thread
from multiprocessing import Queue
from json import load, dumps
from copy import deepcopy
from sys import exit, argv
from datetime import datetime
from time import time, strftime, localtime, sleep

import sqlite3
import requests
import praw

from SQL3Database import SQL3Database

# if True
# - disables writing results to the db
# - disables the notification being sent
# - uses config_test.json
# - only processes a single post
DEBUGGING = False
E2E = False
CONFIG = dict()
NOTIFICATION_APP = str()
DB = SQL3Database("results.db")


def import_config():
    if DEBUGGING:
        config_file_name = "config_test.json"
    elif E2E:
        config_file_name = "config_e2e.json"
    else:
        config_file_name = "config.json"
    try:
        file = open(config_file_name)
        config = load(file)
        file.close()
        return config
    except FileNotFoundError as import_error:
        simple_error_message = f"Error: {config_file_name} is not found, \
            create it based on the example_config.json"
        output_error_to_log(simple_error_message, import_error)
        exit()
    except ValueError as import_error:
        simple_error_message = f"Error: {config_file_name} is not formatted correctly"
        output_error_to_log(simple_error_message, import_error)
        exit()
    except Exception as import_error:
        simple_error_message = "Error: Unhandled exception with regard to importing config"
        output_error_to_log(simple_error_message, import_error)
        exit()


# returns a time stamp for the logs
def get_time_stamp(now=datetime.now()) -> str:
    if isinstance(now, datetime):
        result = now.strftime("%m-%d-%Y %I:%M:%S %p")
    elif isinstance(now, float):
        result = strftime("%m-%d-%Y %I:%M:%S %p", localtime(now))

    return result


# creates string to be output to the log and console
def create_result_output(post, subreddit, timestamp=datetime.now()) -> str:
    message = get_time_stamp(timestamp) + " - " + subreddit + " - " + post.title
    return message


# creates payload and sends post request to the notification app
def send_notification(users, post) -> None:
    if NOTIFICATION_APP == "slack":
        formatted_users = ""
        for index, user in enumerate(users):
            formatted_users += "<@" + str(users[index]) + "> "

        api_url = str(CONFIG["notifications"]["slack"]["webhook-url"])
        message = {
            "text": post.title,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "<https://reddit.com" + post.permalink + "|" + post.title + ">"
                    }
                }
            ]
        }

        # adds users to be notified of post to message
        if formatted_users != "":
            message["blocks"][0]["text"]["text"] = \
                formatted_users + message["blocks"][0]["text"]["text"]

        # sends message to slack
        requests.post(
            api_url, data=dumps(message),
            headers={'Content-Type': 'application/json'}
        )
    elif NOTIFICATION_APP == "telegram":
        for user in users:
            api_url = f'https://api.telegram.org/bot' \
                      f'{ str(CONFIG["notifications"]["telegram"]["token"]) }/sendMessage'

            message = f'<a href="https://reddit.com{post.permalink}">{post.title}</a>'

            # Create json link with message
            data = {'chat_id': user, 'text': message, 'parse_mode': 'HTML'}
            requests.post(api_url, data)


# writes found post to the results.log file
def output_result_to_log(message, url) -> None:
    file = open("results.log", "a")
    file.write(message + " (" + url + ")\n")
    file.close()


# writes found post to the errors.log file
def output_error_to_log(message, error_message=None) -> None:
    print(message + "\n" + str(error_message))
    file = open("errors.log", "a")
    file.write(get_time_stamp(time()) + ": " + message + "\n" + str(error_message) + "\n\n")
    file.close()


# reads a filter to determine who to notify
def determine_who_to_notify(single_filter: dict) -> list:
    result = []
    if single_filter.get("notify"):
        for user in list(single_filter["notify"]):
            result.append(user)
    return result


# determines if a string contains every word in a list of strings
# not case-sensitive
def string_contains_every_element_in_list(keyword_list: list, string: str) -> bool:
    in_list = True
    # if list is empty
    if not keyword_list:
        in_list = False
    else:
        for keyword in [x.lower() for x in keyword_list]:
            if keyword not in string.lower():
                in_list = False
    return in_list


# determines if a string contains at least one word in a list of strings
# not case-sensitive
def string_contains_an_element_in_list(keyword_list: list, string: str) -> bool:
    in_list = False
    for keyword in [x.lower() for x in keyword_list]:
        if keyword in string.lower():
            return True
    return in_list


def parse_title_for_have(post_title: str):
    post_title = post_title.lower()
    return post_title[post_title.find("[h]") + 3:post_title.find("[w]")]


def parse_title_for_want(post_title: str):
    post_title = post_title.lower()
    return post_title[post_title.find("[w]") + 3:]


def handle_filter_attributes(attribute: str, title: str, val: list) -> bool:
    try:
        return {
            "includes": string_contains_every_element_in_list(val, title),
            "excludes": not string_contains_an_element_in_list(val, title),
            "have": string_contains_every_element_in_list(val, parse_title_for_have(title)),
            "want": string_contains_every_element_in_list(val, parse_title_for_want(title)),
            "notify": True,
        }[attribute]
    except KeyError:
        print("The config includes unsupported attributes:", attribute)
        sys.exit()


def filter_post(post, single_filter: dict, queue):
    # default flag initializations
    result = False
    post_title = post.title.lower()

    results_list = []

    for key, value in single_filter.items():
        results_list.append(handle_filter_attributes(key, post_title, value))

    queue_dict = queue.get()

    # if a result has been found
    if False not in results_list:
        result = True
        queue_dict["who_to_notify"] = determine_who_to_notify(single_filter)

    queue_dict["notify"] = result
    queue.put(queue_dict)


def post_found(post, subreddit, who_to_notify) -> None:
    message = create_result_output(post, subreddit, datetime.now())
    print(message)

    if not DEBUGGING or E2E:
        send_notification(who_to_notify, post)
        DB.insert_result(time(), subreddit, post.title, post.permalink)
        output_result_to_log(message, post.permalink)
    else:
        print("post passed filters")


def process_post(post, subreddit):
    number_of_filters = len(CONFIG["search"][subreddit]["filters"])
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
            target=filter_post,
            args=(post, CONFIG["search"][subreddit]["filters"][filter_index], queue)
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
        post_found(post, subreddit, list(return_vals["who_to_notify"]))


def check_if_debugging():
    global DEBUGGING, E2E
    for arg in argv:
        if arg == "debug":
            DEBUGGING = True
            print("Debugging Mode")
            break
        elif arg == "e2e":
            E2E = True
            print("E2E Mode")
            break


def main() -> None:
    global CONFIG, NOTIFICATION_APP
    check_if_debugging()

    CONFIG = import_config()
    NOTIFICATION_APP = str(CONFIG["notifications"]["app"])

    # overwrite secrets for tests
    # reddit_client_id, reddit_client_secret, notification_app, notification_app_token
    if len(sys.argv) == 6:
        args = sys.argv[2:]
        CONFIG["reddit"]["clientId"] = args[0]
        CONFIG["reddit"]["clientSecret"] = args[1]
        NOTIFICATION_APP = args[2]
        if NOTIFICATION_APP == "telegram":
            CONFIG["notifications"]["telegram"]["token"] = args[3]
        elif NOTIFICATION_APP:
            CONFIG["notifications"]["slack"]["webhook-url"] = args[3]

    DB.create_database()

    # access to reddit api
    reddit = praw.Reddit(client_id=CONFIG["reddit"]["clientId"],
                         client_secret=CONFIG["reddit"]["clientSecret"],
                         user_agent="default")

    # list holds the names of subreddits to search
    subreddit_names = list(CONFIG["search"].keys())

    # store the time the last submission checked was created in unix time per subreddit
    last_submission_created = {}
    for subreddit in subreddit_names:
        last_submission_created[str(subreddit)] = time()

    number_of_posts = 0
    total_time = 0

    looping = True
    while looping:
        for subreddit in subreddit_names:
            if DEBUGGING or E2E:
                print("Processing", subreddit)
            # stores most recent post time of this batch of posts
            most_recent_post_time = 0

            # returns new posts from subreddit
            subreddit_obj = reddit.subreddit(subreddit).new(limit=5)

            for post in subreddit_obj:

                # updates the time of the most recently filtered post
                if post.created_utc > most_recent_post_time:
                    most_recent_post_time = post.created_utc

                if post.created_utc > last_submission_created[str(subreddit)]:
                    start = time()

                    last_submission_created[str(subreddit)] = post.created_utc
                    process_post(post, subreddit)

                    total_time += time() - start
                    number_of_posts += 1

                    # print("time to apply all", subreddit, "filters to the post:", num, "seconds")
                    print("new average time for", number_of_posts,
                          "post(s):", total_time / number_of_posts)
                    print(" ")

                    if DEBUGGING or E2E:
                        print(post.title)
                        looping = False
            sleep(1)


if __name__ == "__main__":
    try:
        main()
    except sqlite3.Error as error:  # sqlite3 error
        output_error_to_log(" ", error)
        sleep(5)
        main()
    except Exception as error:
        output_error_to_log(" ", error)
        sleep(5)
        main()
