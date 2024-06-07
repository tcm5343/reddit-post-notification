from json import dumps

from praw.models import Submission
import requests


def __send_notification_to_slack(
        users: list,
        post: Submission,
        notification_config: dict) -> None:
    formatted_users = ""
    for user in users:
        formatted_users += "<@" + str(user) + "> "

    api_url = str(notification_config["slack"]["webhook-url"])
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


def __send_notification_to_telegram(
        users: list,
        post: Submission,
        notification_config: dict) -> None:
    for user in users:
        api_url = f'https://api.telegram.org/bot' \
                  f'{str(notification_config["telegram"]["token"])}/sendMessage'

        message = f'<a href="https://reddit.com{post.permalink}">{post.title}</a>'

        # Create json link with message
        data = {'chat_id': user, 'text': message, 'parse_mode': 'HTML', "disable_web_page_preview": True}
        requests.post(api_url, data)


def send_notification(users: list, post: Submission, notification_config: dict) -> None:
    if notification_config['app'].lower() == "slack":
        __send_notification_to_slack(users, post, notification_config)
    elif notification_config['app'].lower() == "telegram":
        __send_notification_to_telegram(users, post, notification_config)
    else:
        raise NotImplementedError(f'Notification app: {notification_config["app"]} '
                                  f'has not been implemented')
