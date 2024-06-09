import re

from praw.models import Submission


# pylint: disable=too-few-public-methods
class SubmissionFilter:
    def __init__(self, filter_name, filter_def):
        self.name = filter_name
        self.filters = filter_def
        self.notify_def = filter_def.get("notify", {})

    def __eval_includes(self, part, target_string: str):
        checks = self.filters[part].get('includes', [])
        if not checks:
            return True
        for check in checks:
            if all(substring in target_string for substring in check):
                return True
        return False

    def __eval_excludes(self, part, target_string: str):
        checks = self.filters[part].get('excludes', [])
        if not checks:
            return True
        for check in checks:
            if any(substring in target_string for substring in check):
                return False
        return True

    def __eval_regex(self, part, target_string: str):
        checks = self.filters[part].get('regex', [])
        if not checks:
            return True
        for check in checks:
            if all(re.search(pattern, target_string) for pattern in check):
                return True
        return False

    def eval(self, post: Submission) -> bool:
        """
        Evaluate a post to see if a notification should be sent.

        Criteria:
            1. Any filter (includes, excludes, ...) for a given part of a post (title, body, ...) must pass for truthy
                for includes and exlcudes: all elements of a filter must be present in the target string
            2. If any part is truthy, a message is sent
        """
        lowered_title = post.title.lower()
        string_parts = {
            'have': lambda: post.title[lowered_title.find("[h]") + 3:lowered_title.find("[w]")],
            'want': lambda: post.title[lowered_title.find("[w]") + 3:],
            'title': lambda: post.title,
            'body': lambda: post.selftext,
            'post': lambda: post.title + " " + post.selftext,  # post is defined as both title and body
            'url': lambda: post.url,
        }
        for key in self.filters:
            if key != 'notify':
                target_string = string_parts[key]()
                includes = self.__eval_includes(key, target_string)
                excludes = self.__eval_excludes(key, target_string)
                regex = self.__eval_regex(key, target_string)
                if includes and excludes and regex:
                    return True
        return False
