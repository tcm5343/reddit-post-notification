import requests
from praw.models import Submission


class TelegramNotifier:
    def __init__(self, token):
        self.service = 'telegram'
        self.api_url = f'https://api.telegram.org/bot{token}/sendMessage'

    @staticmethod
    def __format_payload(post: Submission, user: str):
        return {
            'chat_id': user,
            'text': f'<a href="https://reddit.com{post.permalink}">{post.title}</a>',
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }

    def send(self, post: Submission, users: list[str]):
        for user in users:
            requests.post(self.api_url, self.__format_payload(post, user))
