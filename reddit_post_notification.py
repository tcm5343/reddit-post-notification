#!/usr/bin/python3

import time
import sys
import sqlite3
import multiprocessing

from json import load, dumps
from copy import deepcopy
from datetime import datetime

import praw

# if True
# - disables writing results to the db
# - the notification being sent
# - uses config_test.json
DEBUGGING = True

CONFIG, NOTIFICATION_APP, CON, CUR = None, None, None, None


def import_config():
    config_file_name = "config.json" if not DEBUGGING else "config_test.json"
    try:
        file = open(config_file_name)
        config = load(file)
        file.close()
        return config
    except FileNotFoundError as import_error:
        simple_error_message = f"Error: {config_file_name} is not found, \
            create it based on the example_config.json"
        output_error_to_log(simple_error_message, import_error)
        sys.exit()
    except ValueError as import_error:
        simple_error_message = f"Error: {config_file_name} is not formatted correctly"
        output_error_to_log(simple_error_message, import_error)
        sys.exit()
    except Exception as import_error:
        simple_error_message = "Error: Unhandled exception with regard to importing config"
        output_error_to_log(simple_error_message, import_error)
        sys.exit()


# connect to database
def connect_to_database():
    global CON, CUR
    CON = sqlite3.connect('results.db')
    CUR = CON.cursor()


# closes the connection to the database
def close_database() -> None:
    CON.commit()
    CON.close()


# creates a sqlite3 database
def create_database() -> None:
    connect_to_database()
    CUR.execute('''CREATE TABLE if not exists results (
        id integer not null primary key,
        date_time text,
        subreddit text,
        post_title text,
        post_url text)''')

    close_database()


# writes results to sqlite3 database
def output_result_to_database(subreddit, post):
    connect_to_database()
    CUR.execute('INSERT INTO results VALUES (?,?,?,?,?)',
                (None, datetime.now(), subreddit, post.title, post.permalink))
    close_database()


# returns a time stamp for the logs
def get_time_stamp(now) -> str:
    return now.strftime("%m-%d-%Y %I:%M:%S %p")


# creates string to be output to the log and console
def create_result_output(post, subreddit) -> str:
    message = get_time_stamp(datetime.now()) + " - " + subreddit + " - " + post.title
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
        post(
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
            post(api_url, data)


# writes found post to the results.log file
def output_result_to_log(message, url) -> None:
    file = open("results.log", "a")
    file.write(message + " (" + url + ")\n")
    file.close()


# writes found post to the errors.log file
def output_error_to_log(message, error_message=None) -> None:
    print(message + "\n" + str(error_message))
    file = open("errors.log", "a")
    file.write(get_time_stamp(datetime.now()) + ": " + message + "\n" + str(error_message) + "\n\n")
    file.close()


# reads a filter to determine who to notify
def determine_who_to_notify(single_filter) -> list:
    result = []
    if single_filter.get("notify"):
        for user in list(single_filter["notify"]):
            result.append(user)
    return result


# determines if a string contains every word in a list of strings
# not case-sensitive
def string_contains_every_element_in_list(keyword_list, string) -> bool:
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
def string_contains_an_element_in_list(keyword_list, string) -> bool:
    in_list = False
    for keyword in [x.lower() for x in keyword_list]:
        if keyword in string.lower():
            return True
    return in_list


def filter_post(post, single_filter, queue):
    # default flag initializations
    result = False
    except_flag = True
    includes_flag = False

    if single_filter.get("includes"):
        includes_flag = string_contains_every_element_in_list(single_filter["includes"], post.title)
    else:
        includes_flag = True

    if single_filter.get("except"):
        except_flag = string_contains_an_element_in_list(single_filter["except"], post.title)
    else:
        except_flag = False

    queue_dict = queue.get()

    # if condition passes, a result has been found
    if includes_flag and not except_flag:
        result = True
        queue_dict["who_to_notify"] = determine_who_to_notify(single_filter)

    queue_dict["notify"] = result
    queue.put(queue_dict)


def post_found(post, subreddit, who_to_notify) -> None:
    message = create_result_output(post, subreddit)
    print(message)

    if not DEBUGGING:
        send_notification(who_to_notify, post)
        output_result_to_database(subreddit, post)
        output_result_to_log(message, post.permalink)


def process_post(post, subreddit):
    number_of_filters = len(CONFIG["search"][subreddit]["filters"])
    queue = multiprocessing.Queue()

    print(post.title)

    print("number of filters processed:", number_of_filters)

    processes = []
    return_vals = {
        "notify": False,
        "who_to_notify": set()
    }

    for filter_index in range(number_of_filters):
        ret = deepcopy(return_vals)
        queue.put(ret)

        process = multiprocessing.Process(
            target=filter_post,
            args=(post, CONFIG["search"][subreddit]["filters"][filter_index], queue)
        )

        processes.append(process)
        processes[filter_index].start()

    # when a process is finished, a record is pulled off the queue and processed
    for process in processes:
        process.join()
        ret = queue.get()

        if ret["notify"]:
            return_vals["notify"] = True
            return_vals["who_to_notify"].update(set(ret["who_to_notify"]))

    if return_vals["notify"]:
        post_found(post, subreddit, list(return_vals["who_to_notify"]))


def main() -> None:
    global CONFIG, NOTIFICATION_APP
    CONFIG = import_config()
    NOTIFICATION_APP = str(CONFIG["notifications"]["app"])

    create_database()

    # access to reddit api
    reddit = praw.Reddit(client_id=CONFIG["reddit"]["clientId"],
                         client_secret=CONFIG["reddit"]["clientSecret"],
                         user_agent="default")

    # list holds the names of subreddits to search
    subreddit_names = list(CONFIG["search"].keys())

    # store the time the last submission checked was created in unix time per subreddit
    last_submission_created = {}
    for subreddit in subreddit_names:
        last_submission_created[str(subreddit)] = time.time()

    while True:
        for subreddit in subreddit_names:
            # stores most recent post time of this batch of posts
            most_recent_post_time = 0

            # returns new posts from subreddit
            subreddit_obj = reddit.subreddit(subreddit).new(limit=5)

            for post in subreddit_obj:

                # updates the time of the most recently filtered post
                if post.created_utc > most_recent_post_time:
                    most_recent_post_time = post.created_utc

                # checks the time the post was created vs the most recent logged time to ensure
                # posts are not filtered multiple times
                if post.created_utc > last_submission_created[str(subreddit)]:
                    last_submission_created[str(subreddit)] = post.created_utc
                    process_post(post, subreddit)

            time.sleep(1.1)


if __name__ == "__main__":
    try:
        main()
    except sqlite3.Error as error: # sqlite3 error
        output_error_to_log(" ", error)
        time.sleep(5)
        main()
    except Exception as error:
        output_error_to_log(" ", error)
        time.sleep(5)
        main()
