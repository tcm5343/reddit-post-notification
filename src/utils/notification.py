# from json import dumps
#
# from praw.models import Submission
# import requests


# def __send_notification_to_slack(
#         users: list,
#         post: Submission,
#         notification_config: dict) -> None:
#     formatted_users = ""
#     for user in users:
#         formatted_users += "<@" + str(user) + "> "
#
#     api_url = str(notification_config["slack"]["webhook-url"])
#     message = {
#         "text": post.title,
#         "blocks": [
#             {
#                 "type": "section",
#                 "text": {
#                     "type": "mrkdwn",
#                     "text": "<https://reddit.com" + post.permalink + "|" + post.title + ">"
#                 }
#             }
#         ]
#     }
#
#     # adds users to be notified of post to message
#     if formatted_users != "":
#         message["blocks"][0]["text"]["text"] = \
#             formatted_users + message["blocks"][0]["text"]["text"]
#
#     # sends message to slack
#     requests.post(
#         api_url, data=dumps(message),
#         headers={'Content-Type': 'application/json'}
#     )
